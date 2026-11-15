"""Local-only inventory of complete ChatGPT export ZIP. Outputs must remain private.

The tool does not contact networks, upload content, or extract attachments.
It stores titles and conversation IDs only in the user-specified private report.
"""
import argparse
import json
import re
import zipfile
from pathlib import Path


def inventory(path):
    result = {'conversations': 0, 'message_nodes': 0, 'assets_declared': None,
              'assets_present': 0, 'assets_indexed_present': 0, 'assets_indexed_missing': None,
              'matched_threads': []}
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        index_name = 'conversation_asset_file_names.json'
        asset_names = json.loads(z.read(index_name)) if index_name in names else {}
        if not isinstance(asset_names, dict): raise ValueError('Unexpected asset index structure')
        result['assets_declared'] = len(asset_names)
        result['assets_indexed_present'] = sum(n in names for n in asset_names)
        result['assets_indexed_missing'] = len(asset_names)-result['assets_indexed_present']
        result['assets_present'] = sum(n.endswith('.dat') for n in names)
        for filename in sorted(names):
            if not re.fullmatch(r'conversations-\d+\.json', filename): continue
            items = json.loads(z.read(filename))
            if not isinstance(items,list): raise ValueError('Unexpected conversations structure')
            for item in items:
                if not isinstance(item,dict): continue
                result['conversations'] += 1
                title=item.get('title') or ''
                nodes=item.get('mapping') or {}
                result['message_nodes'] += len(nodes)
                if re.search(r'DEBO|Skill|ClaimEdge|D.Wing|P Logistics|Thread', title,re.I):
                    result['matched_threads'].append({
                        'title':title,'conversation_id':item.get('conversation_id'),
                        'source_chunk':filename,'node_count':len(nodes),
                        'update_time':item.get('update_time')})
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path)
    p.add_argument('--private-report',type=Path,required=True)
    a=p.parse_args()
    data=inventory(a.source)
    a.private_report.parent.mkdir(parents=True,exist_ok=True)
    a.private_report.write_text(json.dumps(data,indent=2,ensure_ascii=False))
    print(json.dumps({k:v for k,v in data.items() if k!='matched_threads'},indent=2))
    print('Detailed thread references written to PRIVATE report only.')
if __name__=='__main__':main()
