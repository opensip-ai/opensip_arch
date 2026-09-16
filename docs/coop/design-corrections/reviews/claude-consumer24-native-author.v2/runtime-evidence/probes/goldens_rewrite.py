"""Rewrite ONLY the pinned run3/coverage2 id literals of run-termination-goldens.v1.json from a parent id probe to a
corrected id probe of the same golden scenarios (goldens_ids.py output). Every other byte is kept.

Two steps, both data-driven and reported:
1. SUBSTITUTE each parent Run id and Coverage id by the corrected id of the Coverage with the same stable key
   (universes, relation, rung, subjects, entry state). The all-zero `run3:` placeholder is a deliberate non-Run and is
   left untouched.
2. RE-DERIVE CARRIER ROLES inside a golden whose corrected derived carrier is a DIFFERENT member of the same carrier
   set than the substituted expectation (the contract picks among equal carriers by identity order, so new
   identities can exchange which carrier is primary). Only then are the two coverage ids exchanged inside that golden
   (expectation and its refused alternatives), so "the other carrier" stays the other carrier. Anything else that
   still differs from the corrected derivation refuses.

Refuses (exit 1, file untouched) on a conflicting or ambiguous mapping, an unmapped pinned id, or a golden that step 2
cannot reconcile. Usage: goldens_rewrite.py PARENT_IDS.json CORRECTED_IDS.json GOLDENS_PATH
"""
import json
import re
import sys
from pathlib import Path

PLACEHOLDER = "run3:" + "0" * 64
old = json.loads(Path(sys.argv[1]).read_text())
new = json.loads(Path(sys.argv[2]).read_text())
target = Path(sys.argv[3])
doc_text = target.read_text()
used = set(re.findall(r"(?:run3|coverage2):[0-9a-f]{64}", doc_text)) - {PLACEHOLDER}
mapping, problems = {}, []


def bind(a, b):
    if mapping.get(a, b) != b:
        problems.append({"conflict": a, "first": mapping[a], "second": b})
    mapping[a] = b


for gid, parent in old.items():
    corrected = new.get(gid)
    if corrected is None:
        problems.append({"missingGolden": gid})
        continue
    bind(parent["runId"], corrected["runId"])
    by_key = {}
    for cid, key in corrected["coverages"].items():
        by_key.setdefault(json.dumps(key, sort_keys=True), []).append(cid)
    for cid, key in parent["coverages"].items():
        candidates = by_key.get(json.dumps(key, sort_keys=True), [])
        if len(candidates) == 1:
            bind(cid, candidates[0])
        elif cid in used:
            problems.append({"ambiguousOrMissing": cid, "golden": gid, "candidates": candidates})
unmapped = sorted(i for i in used if i not in mapping)
if unmapped:
    problems.append({"unmappedPinnedIds": unmapped})
if problems:
    print(json.dumps({"problems": problems}, indent=1))
    raise SystemExit(1)


def substitute(value, table):
    if isinstance(value, str):
        return table.get(value, value)
    if isinstance(value, list):
        return [substitute(v, table) for v in value]
    if isinstance(value, dict):
        return {k: substitute(v, table) for k, v in value.items()}
    return value


doc = json.loads(doc_text)
swaps = {}
for golden in doc["goldens"]:
    if golden["kind"] != "termination":
        continue
    corrected = new[golden["id"]]
    expected = substitute(golden["expect"]["termination"], mapping)
    derived = corrected["derivedTermination"]
    if expected != derived:
        exp_cov, der_cov = expected.get("coverageId"), derived.get("coverageId")
        same_otherwise = {k: v for k, v in expected.items() if k != "coverageId"} == {k: v for k, v in derived.items() if k != "coverageId"}
        if not (same_otherwise and exp_cov and der_cov and der_cov in corrected["coverages"]):
            problems.append({"irreconcilable": golden["id"], "expected": expected, "derived": derived})
            continue
        swaps[golden["id"]] = {exp_cov: der_cov, der_cov: exp_cov}
if problems:
    print(json.dumps({"problems": problems, "applied": mapping}, indent=1))
    raise SystemExit(1)

# Apply textually so every other byte (layout, key order, prose) is kept: global id substitution, then the per-golden
# role exchange inside the exact text span of that golden object only.
text = doc_text
for a, b in sorted(mapping.items()):
    if a in used:
        text = text.replace(a, b)
for gid, table in swaps.items():
    start = text.index('"id": "' + gid + '"')
    following = text.find('"id": "', start + 1)
    end = following if following != -1 else len(text)
    a, b = list(table)
    span = text[start:end].replace(a, "\0SWAP\0").replace(b, a).replace("\0SWAP\0", b)
    text = text[:start] + span + text[end:]
target.write_text(text)
print(json.dumps({"rewritten": target.as_posix(), "substituted": {a: b for a, b in sorted(mapping.items()) if a in used},
                  "carrierRoleExchanges": swaps}, indent=1))
