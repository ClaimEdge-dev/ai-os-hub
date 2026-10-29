import importlib.util, pathlib, sys

ROOT=pathlib.Path(__file__).resolve().parents[1]

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

vote=load("vote",ROOT/"python"/"jersey_temporal_vote.py")

# Known strong #9 consensus.
result=vote.choose_jersey([
    {"text":"9","ocr_conf":.95,"quality":.9},
    {"text":"9","ocr_conf":.90,"quality":.8},
    {"text":"8","ocr_conf":.40,"quality":.4},
], roster_numbers={"1","7","8","9","16","19","23"})
assert result["status"]=="CANDIDATE"
assert result["candidate"]=="9"

# Ambiguous/no evidence must abstain.
result=vote.choose_jersey([], roster_numbers={"9"})
assert result["status"]=="ABSTAIN"

print("PASS core tests")
