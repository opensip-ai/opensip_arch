#!/usr/bin/env python3
"""Mutation run: 24 prior binding4 mutants plus new candidate02 mutants.

Each mutant is killed or not by the subject's 56 tests, and optionally by the
independent probe scripts in this directory. The subject copy is never modified.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
COPY = HERE / "subject-copy"
SOURCE = (COPY / "tools/verify_design.py").read_text()
PROBES = [HERE / "probe_v4.py", HERE / "probe_sources.py"]

PRIOR = [
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
    ("M23 inherited after text replaced", "'before': override['before'], 'after': override['after']}", "'before': override['before'], 'after': override['before'] + '?'}"),
    ("M24 v4 dispatch skipped", "        result.update(successor_chain(architecture, lock, effective))", "        pass"),
]

NEW = [
    ("N01 JSON-parent line selector guard removed", "raise DesignError('v4 JSON parent passages require JSON Pointer selectors')", "pass"),
    ("N02 JSON detection by .json suffix only", "            if 'line' in override['selector']:", "            if 'line' in override['selector'] and override['parent']['path'].endswith('.json'):"),
    ("N03 malformed candidate path guard removed", "        if not isinstance(candidate.get('path'), str) or not candidate['path']:\n            raise DesignError('inventory candidate path must be a nonempty string')\n", ""),
    ("N04 source not joined to accepted design", "if expected is None or any(pin.get(key) != expected.get(key) for key in ('path', 'sha256', 'bytes')):", "if False:"),
    ("N05 accepted join ignores digest", "for key in ('path', 'sha256', 'bytes')):\n            raise DesignError('generation source is not selected", "for key in ('path',)):\n            raise DesignError('generation source is not selected"),
    ("N06 architecture bytes not rehashed", "        raw = pinned_bytes(architecture, pin)\n", "        raw = relative_file(architecture, pin['path']).read_bytes()\n"),
    ("N07 implementation copy not compared", "if relative_file(implementation, path).read_bytes() != raw:", "if False:"),
    ("N08 registry digest not compared", "if source is None or source.get('sourceSha256') != pin['sha256']:", "if source is None:"),
    ("N09 registry owner fields not compared", "if any(source.get(key) != row.get(key) for key in ('schemaId', 'declaredMajor', 'profile', 'semanticValidatorOwner')):", "if False:"),
    ("N10 schema $id not compared", "if object_value(decode(raw), 'generation source document').get('$id') != source.get('schemaId'):", "if False:"),
    ("N11 coverage equality removed", "if set(selected) != set(registered):", "if False:"),
    ("N12 coverage one-sided (map subset of registry)", "if set(selected) != set(registered):", "if not set(selected) <= set(registered):"),
    ("N13 duplicate mapped path allowed", "if not isinstance(path, str) or not path or path in selected:", "if not isinstance(path, str) or not path:"),
    ("N14 duplicate registry path allowed", "if not isinstance(path, str) or not path or path in registered:", "if not isinstance(path, str) or not path:"),
    ("N15 contract candidates not selected for preflight", "            selected.update({row['path']: row for row in unit['inputs']})", "            pass"),
    ("N16 source map top-level not closed", "if set(mapping) != {'schemaVersion', 'sources'} or type(mapping['schemaVersion']) is not int or mapping['schemaVersion'] != 1:", "if mapping.get('schemaVersion') != 1:"),
    ("N17 implementation symlink/escape check bypassed", "        if relative_file(implementation, path).read_bytes() != raw:", "        if (implementation / path).read_bytes() != raw:"),
    ("N18 preflight before design verification", "    object_value(lock, \"design lock\")\n", "    object_value(lock, \"design lock\")\n    if implementation is not None:\n        generation_sources(architecture, implementation, {})\n"),
    ("N19 v3 contractSuccessor ignored in preflight", "        if 'contractSuccessor' in result:\n            units = [result['contractSuccessor']]\n", ""),
]


def run(cmd, cwd, env):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env, timeout=900)


def main():
    use_probes = "--probes" in sys.argv
    rows = []
    for name, old, new in PRIOR + NEW:
        count = SOURCE.count(old)
        if count != 1:
            rows.append({"mutant": name, "error": f"anchor occurs {count} times"})
            print("ERROR", name, count)
            continue
        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp) / "unit"
            shutil.copytree(COPY, work)
            mutated = work / "tools/verify_design.py"
            mutated.write_text(SOURCE.replace(old, new))
            env = {"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin", "HOME": tmp}
            tests = run([sys.executable, "-m", "unittest", "discover", "-s", "tools/tests"], work, env)
            row = {"mutant": name, "killedByTests": tests.returncode != 0,
                   "testSummary": [l for l in tests.stderr.splitlines() if l.startswith(("FAILED", "OK", "Ran"))]}
            if use_probes:
                misses = []
                killed = False
                for probe in PROBES:
                    result = run([sys.executable, str(probe), str(mutated), "--no-write"], HERE, env)
                    killed |= result.returncode != 0
                    misses += [l[5:].split(" -> ")[0] for l in result.stdout.splitlines() if l.startswith("MISS ")]
                row.update(killedByProbes=killed, probeMisses=misses)
            rows.append(row)
            print(name, "tests=" + ("KILLED" if row["killedByTests"] else "survived"),
                  ("probes=" + ("KILLED" if row.get("killedByProbes") else "survived") + f" {row.get('probeMisses')}") if use_probes else "")
    out = HERE / ("mutation-results.json" if use_probes else "mutation-results-tests-only.json")
    out.write_text(json.dumps(rows, indent=2) + "\n")


if __name__ == "__main__":
    main()
