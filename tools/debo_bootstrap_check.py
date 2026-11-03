#!/usr/bin/env python3
"""Read-only DEBO repository bootstrap validator. Python 3.10+, stdlib only."""
from pathlib import Path
import argparse
import hashlib
import json
import posixpath
import re
import sys
import tempfile
ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "AGENTS.md",
    "DEBO_BOOTSTRAP.md",
    "debo/policies/DEBO_JARVIS_AUTONOMOUS_V2.md",
    "governance/DEBO_AUTONOMOUS_EXECUTION_STANDARD_v2.md",
    "governance/DEBO_RUNTIME_BOOTSTRAP_v2.md",
    "governance/DEBO_COMMUNICATION_RECOVERY_STANDARD_v1.md",
    "governance/DEBO_PREVENTIVE_OPERATIONS_PLAYBOOK_v1.md",
    "governance/DEBO_SELF_IMPROVEMENT_AND_ANTI_REPEAT_ENGINE_v1.md",
    "governance/DEBO_INSTALLATION_AND_VERIFICATION_REGISTER_v1.md",
    "governance/SISTER_BRAIN_PROFILE_TEMPLATE_v2.md",
    "projects/dwing-exterior/DEBO_PROFILE_v2.md",
    "governance/DEBO_AGENT_BOARD_ROLE_MAP_v1.md",
    "governance/DEBO_AGENT_COVERAGE_REGISTER_v1.json",
    "skills/agent-talent-manager/SKILL.md",
    "prompts/DEBO_PERPLEXITY_SPEED_RESEARCH_MISSION_v1.md",
]
SISTERS = ["JCT","RRR","MOR","CE","PLG","BULLDOGS","CWA","BBS","CREDIT","SCHOOL","HOUSING","SETTLESURE"]
REQUIRED += [f"governance/sister-brains/{x}_PROFILE_v1.md" for x in SISTERS]
PROJECT_PROFILES = {
    "DEBO": None,
    "DWE": "projects/dwing-exterior/DEBO_PROFILE_v2.md",
    **{name: f"governance/sister-brains/{name}_PROFILE_v1.md" for name in SISTERS},
}
BRIEF_SOURCES = [
    "governance/DEBO_RUNTIME_BOOTSTRAP_v2.md",
    "governance/DEBO_AUTONOMOUS_EXECUTION_STANDARD_v2.md",
    "debo/policies/DEBO_JARVIS_AUTONOMOUS_V2.md",
    "governance/DEBO_COMMUNICATION_RECOVERY_STANDARD_v1.md",
    "governance/DEBO_PREVENTIVE_OPERATIONS_PLAYBOOK_v1.md",
    "governance/DEBO_SELF_IMPROVEMENT_AND_ANTI_REPEAT_ENGINE_v1.md",
    "tools/debo_bootstrap_check.py",
    "governance/DEBO_AGENT_BOARD_ROLE_MAP_v1.md",
    "governance/DEBO_AGENT_COVERAGE_REGISTER_v1.json",
    "skills/agent-talent-manager/SKILL.md",
    "prompts/DEBO_PERPLEXITY_SPEED_RESEARCH_MISSION_v1.md",
]


def section(text, heading):
    """Extract one non-empty level-two section from the canonical source."""
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError as exc:
        raise ValueError(f"Missing required brief section: {heading}") from exc
    end = next((i for i in range(start + 1, len(lines))
                if lines[i].startswith("## ")), len(lines))
    if not any(line.strip() for line in lines[start + 1:end]):
        raise ValueError(f"Empty required brief section: {heading}")
    return "\n".join(lines[start:end]).strip()


def render_brief(project="DEBO"):
    """Derived, read-only source view; never substitutes for current private state."""
    if project not in PROJECT_PROFILES:
        raise ValueError(f"Unknown project: {project}")
    bootstrap = (ROOT / BRIEF_SOURCES[0]).read_text(encoding="utf-8")
    rules = brief_links(section(bootstrap, "## Golden rules"), BRIEF_SOURCES[0])
    triggers = brief_links(section(bootstrap, "## Load specialist detail when relevant"),
                          BRIEF_SOURCES[0])
    communication = (ROOT / "governance/DEBO_COMMUNICATION_RECOVERY_STANDARD_v1.md").read_text(encoding="utf-8")
    inheritance = section(communication, "## Cross-thread inheritance and cumulative snowball rule (2026-11-02)")
    # Copy only the four recovery/closure requirements into the compact brief.
    # This is source-derived, not a separate policy or a new cross-app memory guarantee.
    essentials = [line.strip() for line in inheritance.splitlines()
                  if re.match(r"^(1|2|7|8)\\. ", line)]
    if len(essentials) != 4:
        raise ValueError("Continuity policy is missing a required inheritance/checkpoint instruction")
    continuity = ("## Cross-thread continuity (canonical-source excerpt)\\n"
                  + "\\n".join(essentials)
                  + "\\nFull policy: [communication and recovery](../DEBO_COMMUNICATION_RECOVERY_STANDARD_v1.md)."
                  + " Current state still requires a supported, authorized checkpoint read.")
    board_source = "governance/DEBO_AGENT_BOARD_ROLE_MAP_v1.md"
    board_doc = (ROOT / board_source).read_text(encoding="utf-8")
    chain = brief_links(section(board_doc, "## Chain of command"), board_source)
    board = json.loads((ROOT / "governance/DEBO_AGENT_COVERAGE_REGISTER_v1.json").read_text(encoding="utf-8"))
    main_roles = [role for role in board.get("roles", []) if role.get("project_id") == "DEBO"]
    aliases = [role.get("alias") for role in main_roles]
    if len(aliases) != 13 or len(set(aliases)) != 13 or any(not alias for alias in aliases):
        raise ValueError("Expected exactly 13 unique documented main DEBO agent aliases")
    board_view = ("## Main DEBO agent board (routing labels, not active workers)\\n"
                  + "\\n".join(f"- {role['alias']}: {role['title']}" for role in main_roles)
                  + "\\nThe current agent authority remains in [agent board rules](../DEBO_AGENT_BOARD_ROLE_MAP_v1.md)"
                  + " and [agent talent manager](../../skills/agent-talent-manager/SKILL.md)."
                  + " Names and skill files do not establish installed or running agents.")
    sources = list(BRIEF_SOURCES)
    parts = [
        "# DEBO compact startup brief v1",
        "> GENERATED from canonical sources. Do not edit this derived view. "
        "The repository auto-update workflow refreshes saved briefs after source changes; "
        "existing AI sessions still require a supported loader.",
        f"## Selected project: {project}",
        "Current project state: UNKNOWN until the latest authorized checkpoint is "
        "recovered or confirmed still current in the active context. A static profile "
        "does not establish live status.",
        rules,
        triggers,
        continuity,
        chain,
        board_view,
    ]
    profile = PROJECT_PROFILES[project]
    if profile:
        parts.extend(["## Selected project profile (static routing)",
                      brief_links((ROOT / profile).read_text(encoding="utf-8").strip(),
                                  profile)])
        sources.append(profile)
    parts.append("## Source fingerprints (local SHA-256)")
    parts.extend(f"- `{path}`: `{hashlib.sha256((ROOT / path).read_bytes()).hexdigest()}`"
                 for path in sources)
    parts.append("This verifies a derived local source view, not runtime activation, "
                 "a fresh remote checkpoint, live integration or a measured speedup. "
                 "Regenerate after relevant source changes; detailed policies remain governing.")
    return "\n\n".join(parts) + "\n"


def brief_links(text, source):
    """Keep relative Markdown source links valid in the generated output folder."""
    def replace(match):
        label, target = match.groups()
        if re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", target) or target.startswith("#"):
            return match.group(0)
        path, marker, fragment = target.partition("#")
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), path))
        relative = posixpath.relpath(resolved, "governance/runtime-briefs")
        return f"[{label}]({relative}{marker}{fragment})"
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace, text)


def sync_briefs(write=False):
    """Check or atomically refresh deterministic public-source views only."""
    directory = ROOT / "governance/runtime-briefs"
    if directory.is_symlink():
        raise ValueError("Brief output directory must not be a symlink")
    directory.resolve().relative_to(ROOT.resolve())
    expected = {f"{project}.md": render_brief(project) for project in PROJECT_PROFILES}
    stale = [name for name, content in expected.items()
             if (directory / name).is_symlink() or not (directory / name).is_file()
             or (directory / name).read_text(encoding="utf-8") != content]
    updated = []
    if write and stale:
        directory.mkdir(parents=True, exist_ok=True)
        for name in stale:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                             dir=directory, delete=False) as stream:
                temporary = Path(stream.name)
                try:
                    stream.write(expected[name])
                except BaseException:
                    temporary.unlink(missing_ok=True)
                    raise
            try:
                temporary.replace(directory / name)
            finally:
                temporary.unlink(missing_ok=True)
            updated.append(name)
        stale = []
    return {"result": "FAIL" if stale else "PASS", "briefs": len(expected),
            "stale": stale, "updated": updated,
            "note": "Generated repository-source views; not cross-chat activation or live project state."}

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
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--brief", action="store_true",
                       help="Emit compact golden rules and one static project profile")
    modes.add_argument("--write-briefs", action="store_true",
                       help="Refresh all derived governance/runtime-briefs files")
    modes.add_argument("--check-briefs", action="store_true",
                       help="Fail if any derived brief is missing or stale; do not write")
    parser.add_argument("--project", type=str.upper, choices=list(PROJECT_PROFILES),
                        default="DEBO", help="Resolved project ID for --brief (default: DEBO)")
    args = parser.parse_args()
    if not args.brief and args.project != "DEBO":
        parser.error("--project requires --brief")
    result = check()
    if result["result"] != "PASS":
        print(json.dumps(result, indent=2))
        return 1
    if args.write_briefs or args.check_briefs:
        try:
            synced = sync_briefs(write=args.write_briefs)
        except (OSError, UnicodeError, ValueError) as exc:
            print(f"Brief sync unavailable: {exc}", file=sys.stderr)
            return 1
        print(json.dumps(synced, indent=2))
        return 0 if synced["result"] == "PASS" else 1
    if not args.brief:
        print(json.dumps(result, indent=2))
        return 0
    try:
        brief = render_brief(args.project)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Brief unavailable: {exc}", file=sys.stderr)
        return 1
    print(brief, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
