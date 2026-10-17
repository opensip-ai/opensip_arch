"""Draft the C1b-0 r1 review request from the built subject manifest (run after build_c1b0_package.py). Writes
/tmp/opensip-implementation/reviews/codex-c1b-0-r1/REQUEST.md and checks it with the backtick pre-check. Submits
nothing."""
from pathlib import Path
import hashlib, json, re, sys
A = Path('/Users/sb/code/opensip-ai/opensip_arch'); W = A.parent / 'opensip-c1b0'
PRE = 'docs/implementation/m3/snapshot-plan-c/c1b-0-r1'; SUBJECT = PRE + '-subject.json'
Q = Path('/tmp/opensip-implementation/reviews/codex-c1b-0-r1')
raw = (A / SUBJECT).read_bytes(); manifest = json.loads(raw); sha = hashlib.sha256(raw).hexdigest()
for row in manifest['files']:
    b = (A / row['path']).read_bytes(); assert len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256'], row['path']
checks = json.loads((A / PRE / 'evidence/c1b0-checks-r1/checks.json').read_bytes()); assert checks['allPassed']
base = manifest['productBase']; rows = json.loads((A / PRE / 'product-map.json').read_bytes())['rows']
lane = checks['productBase']
Q.mkdir(parents=True, exist_ok=True)
text = f"""# Review request: C1B-0-r1 (S4's materialization: `vcs-observation` schema 3; C1b plan r3, sub-unit C1b-0), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{Q}/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - with `python3 -I -B`, the package's `evidence/check_c1b0_preflight.py <out>` and `evidence/check_c1b0_census_stale.py <out>`, which are read-only and open no T2 data;
  - B-S2's `check_b_s2.py`;
  - in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `{SUBJECT}` in `{A}` (uncommitted): {len(raw)} bytes, SHA-256 `{sha}`, {len(manifest['files'])} members. Rehash every member.
- **The candidate base and lane base:** product main `{base}` (lane base `{lane}`).
- **The candidate worktree:** `{W}`, holding the exact bytes that `product-map.json` lists ({len(rows)} files, none new).
- **The verdict this unit needs** is `ACCEPT-DESIGN-UNIT`. It binds as a contract successor, because its identity-v3 and admission-registry copies become accepted inputs.

## Authority

- **The C1b plan r3** (`docs/implementation/m3/snapshot-plan-c/c1b/PLAN-r3.md`; your `codex-c1b-plan-r3`, ACCEPT, whose NBO is answered in SCOPE's history note): sub-unit C1b-0, LD-C1B-7's census batch, and §4's C1b-0 controls.
- **B-S2 (M3-B successor S4):** `docs/implementation/m3/config-discovery-b/b-s2/README.md`, `successor.json`, the fragment `schemas/identity-schemas.v3.b-s2-additions.json` and its `mergeRule`, `evidence/check_b_s2.py`, and BS2-F2 and BS2-F3.
- **VCS-1:** `snapshot-plan-c/vcs-1-r1/CONTRACT.md`.
- **The precedents:** RCA-1's materialization (`docs/implementation/m3/native-publication/rust3-identity-materialization-r1/`) and D2b-0b (`supervisor-d/d2b-0b-r1/`).

## What to review

`SCOPE.md` states the change table, six lead decisions (LD-C1B0-1 to 6), the tests and the checks. Judge:
1. **The merge:**
   - `vcs-observation` is replaced by exactly B-S2's `oneOf`;
   - `vcs-observation-v2` is the product's current record;
   - the two definitions added are the fragment's;
   - nothing else changes, and the serialization is the file's own (LD-C1B0-2);
   - it is applied to I1-L's product copy, as BS2-F3 foresaw.
2. **The re-pins:**
   - the source and admission maps, the admission registry and its architecture copy, and the compiled `SourcePin`;
   - the three entry points under the existing naming rule (LD-C1B0-1);
   - the closure and the recipe;
   - the regenerated carriers. Check the generation's determinism run.
3. **The evaluator join** (LD-C1B0-4): `vcs_joins`, the member join beside `VCS_KIND_JOIN`, and its direct test.
4. **The controls** (LD-C1B0-5):
   - B-S2's vectors at their published bytes, through identity admission and through the Run closure's record check;
   - the schema-2 pair admitting under `vcs-observation-v2`, the pre-S4 side;
   - all twelve negatives refusing both ways.
5. **LD-C1B0-3:** the IDS architecture bundle and the evaluator's scanner pin are unchanged.
6. **The census batch** (LD-C1B0-6, PLAN-r3 LD-C1B-7):
   - all three census output `--check`s pass;
   - the stale-receipt record shows exactly the closure digest, from public fields only;
   - the snapshot census inputs are unchanged.
7. **The design preflight:** verify_design refuses only the package's unaccepted copies, and passes with them accepted, at the base's source counts. The public generator entry point refuses only the unaccepted closure.
8. **The lane** `evidence/c1b0-checks-r1/`:
   - the suites (host 2 and evaluator 1 new tests, the rest none);
   - Clippy and rustfmt;
   - the TypeScript lanes: the public checker refuses for the pre-binding reason; with the copies accepted (`evidence/check_c1b0_typescript.py`, the product checker unchanged), the report lane passes and the generator lane's refusal equals the base's;
   - attempts 1 and 2, kept as void history, and SCOPE's account of them;
   - FW-01, the environment exceptions, operability and the census-closure check;
   - four mutations, two of them re-pinning identity-v3 so that the semantic controls, not the pin, catch them.
9. **Rules:** no new mint-census call outside generated output, no environment read, no `let _ =`, rustfmt on base-clean files only.

Write `review.json` as `{{"verdict": "ACCEPT-DESIGN-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}}`, with ids `C1B0-R1-RF-n` / `C1B0-R1-NBO-n`.
"""
(Q / 'REQUEST.md').write_text(text)
assert not re.search(r'[^`]``[^`]', text), 'backtick pre-check'
print(Q / 'REQUEST.md', len(text), sha)
