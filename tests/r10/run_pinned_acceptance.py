#!/usr/bin/env python3
"""R6: run genuine canonical + R4 + R5 auditors on ONE verified checkout.

No network, no source edits, no overwrites. The exact checkout commit and required
sources must be available locally; the tool fails closed rather than faking a run.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

PIN = 'ea4891221250719948fb641fd1b52d7fc7e40ff3'
SCHEMA = 'DEBO-RECOVERY-DELTA-BRIDGE-v1'


def within(path: Path, parent: Path) -> bool:
    return path == parent or parent in path.parents


def preflight(repo: Path, r4: Path, r5: Path, output: Path, expected: str = PIN) -> dict:
    repo = repo.resolve(strict=True)
    if not repo.is_dir():
        raise ValueError('repo must be a directory')
    output = output.resolve(strict=False)
    if within(output, repo):
        raise ValueError('output must be outside source checkout')
    if output.exists():
        raise ValueError('refuse existing output directory')
    required = [repo / 'SKILL_REGISTRY.md', repo / 'tools' / 'debo_skill_delta.py',
                repo / 'tools' / 'debo_registry_audit.py', r4.resolve(strict=True), r5.resolve(strict=True)]
    for path in required:
        if not path.is_file():
            raise ValueError(f'missing required source {path}')
    proc = subprocess.run(['git','-C',str(repo),'rev-parse','HEAD'], capture_output=True,text=True)
    if proc.returncode != 0:
        raise ValueError('not an inspectable Git checkout')
    actual = proc.stdout.strip()
    if actual != expected:
        raise ValueError(f'checkout SHA mismatch, got {actual}, expected {expected}')
    status = subprocess.run(['git','-C',str(repo),'status','--porcelain'],capture_output=True,text=True)
    if status.returncode or status.stdout.strip():
        raise ValueError('checkout must be clean; refuse mutable/untracked source')
    return {'checkout_commit':actual,'repo':str(repo),'r4':str(r4.resolve()),'r5':str(r5.resolve()),'output':str(output)}


def run(repo: Path, r4: Path, r5: Path, output: Path, expected: str = PIN) -> dict:
    context = preflight(repo,r4,r5,output,expected)
    repo = Path(context['repo']); output=Path(context['output']); output.mkdir(parents=True)
    commands = [
        [sys.executable,str(repo/'tools/debo_skill_delta.py'),'--repo',str(repo),'--include-projects','--validate-contracts','--output',str(output/'canonical.json')],
        [sys.executable,str(r4.resolve()),'--root',str(repo),'--output',str(output/'recovery.json')],
        [sys.executable,str(r5.resolve()),'--recovery-report',str(output/'recovery.json'),'--canonical-report',str(output/'canonical.json'),'--output',str(output/'bridge.json')],
    ]
    try:
        for command in commands:
            p=subprocess.run(command,capture_output=True,text=True,timeout=120)
            if p.returncode:
                raise RuntimeError(f'command failed ({p.returncode}): {command[1]}: {p.stderr[-1000:]}')
        canonical=json.loads((output/'canonical.json').read_text())
        recovery=json.loads((output/'recovery.json').read_text())
        bridge=json.loads((output/'bridge.json').read_text())
        if canonical.get('schema')!='DEBO-SKILL-DELTA-v1' or recovery.get('schema_version')!=1 or bridge.get('schema')!=SCHEMA:
            raise RuntimeError('report schema mismatch')
        if bridge.get('summary',{}).get('hash_mismatches'):
            raise RuntimeError('source hash mismatch; no source writes permitted')
        if bridge.get('summary',{}).get('ambiguous_names'):
            raise RuntimeError('ambiguous skill identity; no source writes permitted')
        result={'mission':'DEBO-SKILLS-001-R6','run_status':'PASS_LOCAL_PINNED_CHECKOUT',
                'pinned_checkout':context['checkout_commit'],'canonical_summary':canonical.get('summary'),
                'recovery_summary':recovery.get('summary'),'bridge_summary':bridge.get('summary'),
                'run_type':'real_code_local_checkout_no_network_no_install',
                'limitations':['GitHub source does not demonstrate ChatGPT native installation',
                               'Nested and plugin skills may be outside canonical root/project scan']}
        (output/'acceptance.json').write_text(json.dumps(result,indent=2)+'\n')
        return result
    except Exception:
        (output/'FAILED_NO_WRITEBACK.txt').write_text('One or more acceptance checks failed. Inspect local log; no GitHub or account writeback performed.\n')
        raise


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo',required=True,type=Path)
    p.add_argument('--r4-script',required=True,type=Path)
    p.add_argument('--r5-script',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args()
    print(json.dumps(run(a.repo,a.r4_script,a.r5_script,a.output),indent=2))

if __name__=='__main__':main()
