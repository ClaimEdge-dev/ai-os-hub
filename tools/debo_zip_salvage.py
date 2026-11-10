"""Recover complete ZIP members from an archive truncated before its central directory.

Local-only, safe by default: does not execute or extract archive members. Builds a
new ZIP with only complete members whose local headers contain definitive sizes.
The original archive is never modified. Truncated or data-descriptor members are
not recovered. Validation uses ZIP CRC32, not cryptographic authenticity.
"""
from __future__ import annotations
import argparse
import json
import shutil
import struct
import zipfile
from pathlib import Path

LOCAL_FMT = '<IHHHHHIIIHH'
CD_FMT = '<IHHHHHHIIIHHHHHII'
EOCD_FMT = '<IHHHHIIH'


def scan_local_headers(path: Path):
    out = []
    stop = None
    size = path.stat().st_size
    with path.open('rb') as f:
        while True:
            offset = f.tell()
            raw = f.read(30)
            if len(raw) < 30:
                stop = 'missing_central_directory_or_eof'
                break
            (sig, version, flags, method, mtime, mdate, crc, compressed,
             uncompressed, nlen, xlen) = struct.unpack(LOCAL_FMT, raw)
            if sig != 0x04034B50:
                stop = f'non_local_header_at_{offset}'
                break
            name_raw = f.read(nlen)
            extra = f.read(xlen)
            if len(name_raw) != nlen or len(extra) != xlen:
                stop = f'truncated_filename_or_extra_at_{offset}'
                break
            name = name_raw.decode('utf-8' if flags & 0x800 else 'cp437', 'replace')
            if flags & 1:
                stop = f'encrypted_entry_{name}'
                break
            if flags & 8 or compressed == 0xFFFFFFFF or uncompressed == 0xFFFFFFFF:
                stop = f'unsupported_descriptor_or_zip64_{name}'
                break
            if method not in (0, 8):
                stop = f'unsupported_compression_{name}'
                break
            if compressed > size - f.tell():
                stop = f'partial_member_{name}'
                break
            f.seek(compressed, 1)
            out.append({'name':name, 'rawname':name_raw, 'offset':offset,
                        'end':f.tell(), 'version':version, 'flags':flags,
                        'method':method,'mtime':mtime,'mdate':mdate,'crc':crc,
                        'compressed':compressed, 'uncompressed':uncompressed,
                        'source_extra':extra})
    return out, stop


def rebuild(src: Path, target: Path):
    if src.resolve() == target.resolve():
        raise ValueError('output must differ from original')
    members, stop = scan_local_headers(src)
    if not members:
        raise ValueError('no complete members to salvage')
    limit = members[-1]['end']
    target.parent.mkdir(parents=True, exist_ok=True)
    with src.open('rb') as inf, target.open('wb') as outf:
        remaining = limit
        while remaining:
            block = inf.read(min(2**20,remaining))
            if not block: raise OSError('Unexpected EOF')
            outf.write(block)
            remaining -= len(block)
        cd_start=outf.tell()
        for m in members:
            name=m['rawname']
            data=struct.pack(CD_FMT,0x02014B50,0x0314,m['version'],m['flags'],m['method'],
              m['mtime'],m['mdate'],m['crc'],m['compressed'],m['uncompressed'],len(name),0,0,0,0,
              0o100644<<16,m['offset'])
            outf.write(data);outf.write(name)
        cd_size=outf.tell()-cd_start
        outf.write(struct.pack(EOCD_FMT,0x06054B50,0,0,len(members),len(members),cd_size,cd_start,0))
    with zipfile.ZipFile(target) as z:
        failed=z.testzip()
        verified=(failed is None)
    return {'complete_members':len(members),'stopped_because':stop,
            'source_bytes':src.stat().st_size,'salvaged_bytes':target.stat().st_size,
            'crc_all_complete_members_pass':verified,'first_failed_member':failed,
            'has_conversations':sum(m['name'].startswith('conversations-') for m in members),
            'has_asset_files':sum(m['name'].endswith('.dat') for m in members),
            'original_remains_untouched':True,
            'entry_names':[m['name'] for m in members]}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--report',type=Path)
    a=p.parse_args()
    result=rebuild(a.source,a.output)
    if a.report:
        a.report.parent.mkdir(parents=True,exist_ok=True)
        a.report.write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='entry_names'},indent=2))
if __name__=='__main__':main()
