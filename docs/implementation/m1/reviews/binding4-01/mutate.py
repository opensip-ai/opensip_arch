#!/usr/bin/env python3
"""Mutation run over the v4 successor-chain code: 38 subject tests vs independent probes."""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
COPY = HERE / "copy"
SOURCE = (COPY / "tools/verify_design.py").read_text()

MUTANTS = [
    ("M01 immediate-predecessor guard removed", "if previous is not None and binding.get('parent') != previous:", "if False:"),
    ("M02 inventory candidate reuse guard removed", "if candidate.get('path') in accepted or candidate.get('path') in seen:", "if False:"),
    ("M03 inventory reuse checks chain only (not overlay)", "if candidate.get('path') in accepted or candidate.get('path') in seen:", "if candidate.get('path') in seen:"),
    ("M04 contract member reuse guard removed", "if any(row['path'] in accepted or row['path'] in seen for row in members):", "if False:"),
    ("M05 contract reuse checks chain only (not overlay)", "if any(row['path'] in accepted or row['path'] in seen for row in members):", "if any(row['path'] in seen for row in members):"),
    ("M06 cross-contract conflict guard removed", "if key in overrides and overrides[key] != override:", "if False:"),
    ("M07 unsupported inherited selector guard removed", "if len(parts) != 4 or parts[1] != 'files' or not parts[2].isdigit() or parts[3] != 'description':", "if False:"),
    ("M08 inherited row changed guard removed", "if target != row:", "if False:"),
    ("M09 inherited-vs-direct conflict guard removed", "if overrides[key] != projected:", "if False:"),
    ("M10 inherited-vs-inherited conflict guard removed", "if key in inherited and inherited[key] != projected:", "if False:"),
    ("M11 inheritance not canonically sorted", "expected_inheritance = [inherited[key] for key in sorted(inherited)]", "expected_inheritance = list(inherited.values())"),
    ("M12 lock inheritance comparison removed", "if lock['inventoryPassageInheritance'] != expected_inheritance:", "if False:"),
    ("M13 no reindex after sorted additions", "f'/files/{index}/description'", "f'/files/{parts[2]}/description'"),
    ("M14 no inheritance at all", "if parent['path'] not in ancestor_pins:", "if True:"),
    ("M15 direct identical override still emits inheritance", "            continue\n        if key in inherited", "            pass\n        if key in inherited"),
    ("M16 later hops parented on base inputs", "parents = lock['inputs'] if previous is None else [previous]", "parents = lock['inputs']"),
    ("M17 empty chains allowed", "if not isinstance(inventories, list) or not inventories or not isinstance(contracts, list) or not contracts:", "if not isinstance(inventories, list) or not isinstance(contracts, list):"),
    ("M18 only base parent treated as ancestor", "ancestor_pins = {row['path']: row for row in inventory_pins[:-1]}", "ancestor_pins = {row['path']: row for row in inventory_pins[:1]}"),
    ("M19 inventory candidates not accepted parents", "accepted[candidate['path']] = candidate", "pass"),
    ("M20 contract members not accepted parents", "accepted[row['path']] = row", "pass"),
    ("M21 final inventory is first candidate", "final_pin = inventory_pins[-1]", "final_pin = inventory_pins[1]"),
    ("M22 seen set dropped from inventory reuse", "if candidate.get('path') in accepted or candidate.get('path') in seen:", "if candidate.get('path') in accepted:"),
    ("M23 inherited before text taken from final override placeholder", "'before': override['before'], 'after': override['after']}", "'before': override['before'], 'after': override['before'] + '?'}"),
    ("M24 v4 dispatch skipped", "        result.update(successor_chain(architecture, lock, effective))", "        pass"),
]


def main():
    rows = []
    for name, old, new in MUTANTS:
        count = SOURCE.count(old)
        if count != 1:
            rows.append({"mutant": name, "error": f"anchor occurs {count} times"})
            continue
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "unit"
            shutil.copytree(COPY, work)
            (work / "tools/verify_design.py").write_text(SOURCE.replace(old, new))
            env = {"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin"}
            tests = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tools/tests"], cwd=work, capture_output=True, text=True, env=env)
            probes = subprocess.run([sys.executable, str(HERE / "probe.py"), str(work / "tools/verify_design.py")], capture_output=True, text=True, env=env)
            missed = [line[5:].split(" -> ")[0] for line in probes.stdout.splitlines() if line.startswith("MISS ")]
            summary = [line for line in tests.stderr.splitlines() if line.startswith(("FAILED", "OK", "Ran"))]
            rows.append({"mutant": name, "killedByTests": tests.returncode != 0, "testSummary": summary,
                         "killedByProbes": probes.returncode != 0, "probeMisses": missed})
    out = HERE / "mutation-results.json"
    out.write_text(json.dumps(rows, indent=2) + "\n")
    for row in rows:
        if "error" in row:
            print("ERROR", row["mutant"], row["error"])
            continue
        print(f"{row['mutant']}: tests={'KILLED' if row['killedByTests'] else 'survived'} probes={'KILLED' if row['killedByProbes'] else 'survived'} {row['probeMisses']}")


if __name__ == "__main__":
    main()
