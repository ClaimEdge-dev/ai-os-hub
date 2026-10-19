#!/usr/bin/env python3
"""Read-only DEBO repository bootstrap validator. Python 3.10+, stdlib only."""
from pathlib import Path
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "governance/DEBO_AUTONOMOUS_EXECUTION_STANDARD_v2.md",
    "governance/DEBO_RUNTIME_BOOTSTRAP_v2.md",
    "governance/DEBO_COMMUNICATION_RECOVERY_STANDARD_v1.md",
    "governance/DEBO_PREVENTIVE_OPERATIONS_PLAYBOOK_v1.md",
    "governance/DEBO_SELF_IMPROVEMENT_AND_ANTI_REPEAT_ENGINE_v1.md",
    "governance/DEBO_INSTALLATION_AND_VERIFICATION_REGISTER_v1.md",
    "governance/SISTER_BRAIN_PROFILE_TEMPLATE_v2.md",
    "projects/dwing-exterior/DEBO_PROFILE_v2.md",
]
SISTERS = ["JCT","RRR","MOR","CE","PLG","BULLDOGS","CWA","BBS","CREDIT","SCHOOL","HOUSING","SETTLESURE"]
REQUIRED += [f"governance/sister-brains/{x}_PROFILE_v1.md" for x in SISTERS]
def check():
    errors=[]
    for path in REQUIRED:
        file=ROOT/path
        if not file.is_file():
            errors.append(f"Missing: {path}")
        elif not file.read_text(encoding="utf-8").strip():
            errors.append(f"Empty: {path}")
    bootstrap=ROOT/"governance/DEBO_RUNTIME_BOOTSTRAP_v2.md"
    if bootstrap.exists():
        text=bootstrap.read_text(encoding="utf-8")
        for name in ["DEBO_COMMUNICATION_RECOVERY_STANDARD_v1.md","DEBO_PREVENTIVE_OPERATIONS_PLAYBOOK_v1.md","DEBO_SELF_IMPROVEMENT_AND_ANTI_REPEAT_ENGINE_v1.md"]:
            if name not in text:
                errors.append(f"Bootstrap missing reference: {name}")
    return {"result":"PASS" if not errors else "FAIL","checked":len(REQUIRED),"profiles":13,"errors":errors,"note":"Repository file checks only; does not verify ChatGPT, plugins, Neon or other runtime activation."}
if __name__=="__main__":
    result=check()
    print(json.dumps(result,indent=2))
    sys.exit(0 if result["result"]=="PASS" else 1)
