Grok review: **B-S9**, round 1. B-S9 is the contract successor that accepted law M3-B r2 names as S9: the `CONFIG.INVALID` remedy text. The lead split it out of B-S1. This is a **design-unit (contract successor)** review. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/grok-b-s9-r1`.

(Lead note: this request was written for GROK2. Grok reviews it because Grok was free. Product main has moved from `e093e90` to `0ceb9ad`, which is I1-L's binding-only commit with 78 contract successors. B-S9 binds there too, 78 → 79, per its `verify_scratch.py --rev 0ceb9ad`.)

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git only read-only.
- No cargo, no builds, no tests, no crash-matrix binary or checker. A timing-sensitive crash-matrix lead set may be using this machine.
- If you run anything, use only the three evidence scripts named below, or read-only commands, with `nice -n 19` and `python3.14 -I -B` (`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`). Use a private 0700 `TMPDIR` under your review directory if you need scratch files.
- Do not import or execute the native model copies. Parse them only, as `check_b_s9.py` does with `ast`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` stays absent. Do not read or create it.
- Never read the private 413 UUID fixture.

## Subject

The pins are in `hashes.txt`. The subject manifest is `docs/implementation/m3/config-discovery-b/b-s9-subject.json` (1,694 bytes, `dbe62e5b6e577b76fb6ceff2b8ce58ebed9354ac320a0a98bc14e4ee62c0dd24`). Its members, all under `docs/implementation/m3/config-discovery-b/b-s9/`:
- `README.md`: the proposal. Read it first.
- `successor.json`: the record, with three parents, no passage override and seven candidates.
- `reference/native_evidence_model.py`: the successor copy of the selected native reference.
- `reference/native_evidence_model.v2.py`: the successor copy of the frozen native model.
- `evidence/copies-report.json`, `evidence/build_b_s9.py`, `evidence/check_b_s9.py`, `evidence/verify_scratch.py`.

All of these are untracked in arch until acceptance. `b-s9-unit.json` next to the manifest is the lead's draft, marked `DRAFT-PENDING-REVIEW`. It is not part of the subject.

**The law and the split.** In `docs/implementation/m3/config-discovery-b/PROPOSAL.md`, M3-B r2, which you accepted, read:
- item 4 (MB:130-166, with S9's requirement at MB:155);
- item 25's S9 row (MB:780);
- the units table (MB:841-843).

The table puts S9 in B-S1. By the lead's decision of 2026-10-04 it is its own unit, so that B-S1's SX-1 and D15 content does not wait on S9's binding form. B1-a's dependency "B-S1 (S9 text)" becomes "B-S9".

**The superseded meaning** is X12-0, `docs/implementation/m2/config-remedy-x12-0/` (README and `successor.json`). It is bound in the product lock, and it overrides line 1158 of both native-model files. **The form's precedent** is `docs/implementation/m2/capability-totality-reference-selection-v1/`, which took a complete successor copy of this same file and made it the selected native reference. The I1-L draft's LD-L1 and LD-L2 (`docs/implementation/m3/preview-pack-i1/i1-l/README.md`) state the same form for schemas.

**The product** is `/Users/sb/code/opensip-ai/opensip` at main `e093e90` (the F8b binding; 77 contract successors), read-only. The string's product carriers are:
- `crates/host/src/configuration.rs:21-24`;
- `crates/host/src/configuration_tests.rs:338-343`;
- `crates/host/src/doctor_ingress.rs:216`.

## What it does

- **Two candidates.** Each is a complete copy of a native-model file at a new path, and each is its parent's effective text under the `e093e90` lock with line 1158 replaced by the S9 remedy. The effective text applies X12-0's line-1158 override, which is the only bound entry on either file.
- **Nothing else changes.** No other line differs, `PUBLIC_ROUTE_REMEDIES` keeps every other key and value, and the two copies differ from each other exactly as their parents do (CT's correction is carried).
- **Selection.** The record's `standing` makes `b-s9/reference/native_evidence_model.py` the current selected native reference, and names the `.v2.py` copy as the successor text of the file law X12 names. The parents, and X12-0's meaning on them, become historical.
- **The new string** is 706 ASCII characters. The capability and policy clauses keep their words, and a leading clause covers configuration documents, flags and requests. The README's table maps every key that reaches public detail `CONFIG.INVALID` to the next step it gives.

## Feasibility (the lead's runs)

- **`build_b_s9.py`** reproduces identical bytes on a second run. It reads the lock through read-only `git show e093e90:design-lock.json`.
- **`check_b_s9.py`** passes:
  - it recomputes each effective parent independently;
  - only line 1158 changes, and both copies parse with `ast`;
  - the remedy table is unchanged except `CONFIG.INVALID`;
  - the 12-line difference between the parents is carried;
  - the remedy is ASCII, within 1,024 characters, and keeps both check-identity predicates and every next step in the table.
- **`verify_scratch.py`**, at `--rev e093e90` and on the main checkout:
  - **B-S9 binds:** 77 to 78 contract successors, with no override and no supersession. The selected inventory and inheritance are unchanged, and 40 generation sources are verified on the checkout.
  - **The rejected forms refuse,** both checked as probes:
    - a second line-1158 override gives `conflicting contract passage overrides` (`tools/verify_design.py:381-383`);
    - VD1 supersessions of X12-0 give `passage supersession must select an inventory row description` (`:342-345`).
  - **Later successors after B-S9:**
    - an override of the copy's line 1158 passes;
    - an override of an old file's line 1158 refuses, as today;
    - an override of an old file's other line passes. verify_design has no notion of selection, so that residual hazard is held by review, as it is for CT's copy.
- **A scratch check outside the subject** appended B-S1, B-S2 and B-S9 together. It passes with 80 successors.

## Decide

1. **The string (R2).** Is it true for every key that reaches public detail `CONFIG.INVALID` once B1 lands? Is the README's table complete? Are both check-identity predicates and X12's three rows kept?
2. **The form (R1, R3).**
   - Is each copy exactly its effective parent with line 1158 replaced?
   - Is the selection statement a sound way to end X12-0's two meanings without an override?
   - Is the residual hazard acceptable?
3. **Conflicts.** Is the README's reconciliation with M3-B r2 right: item 4's "through X12-0's route" kept, and the units-table split? Is the reconciliation with X12 r4 and X12-0 right? Is anything else frozen in the way?
4. **Form.** Is the successor well formed for selection? Anything else wrong?

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `b-s9-subject.json`. The lead's value is `dbe62e5b6e577b76fb6ceff2b8ce58ebed9354ac320a0a98bc14e4ee62c0dd24`;
- `"successor"`: `{path, bytes, sha256}` of `b-s9/successor.json`. The lead's value is 3,371 bytes, `aeb9ed95f170f82b0a42c858d8e784d7f6391314330d86ec0b0ed7cb92b72dff`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change the string, give the exact replacement. Do not commit.
