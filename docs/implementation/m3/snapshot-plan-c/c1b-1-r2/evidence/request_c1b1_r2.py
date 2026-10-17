"""Draft the C1b-1 r2 review request (codex-c1b-1-r2) from the built package: the subject's pin, the lane's base and
the candidate worktree. Submits nothing. Usage: request_c1b1_r2.py."""
from pathlib import Path
import hashlib, json
A = Path('/Users/sb/code/opensip-ai/opensip_arch'); PRE = 'docs/implementation/m3/snapshot-plan-c/c1b-1-r2'
SUBJECT = PRE + '-subject.json'; RV = Path('/tmp/opensip-implementation/reviews/codex-c1b-1-r2')
raw = (A / SUBJECT).read_bytes(); subject = json.loads(raw); sha = hashlib.sha256(raw).hexdigest()
for row in subject['files']:
    b = (A / row['path']).read_bytes(); assert len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256'], row['path']
source = json.loads((A / PRE / 'source.json').read_bytes()); rows = json.loads((A / PRE / 'product-map.json').read_bytes())['rows']
checks = json.loads((A / PRE / 'evidence/c1b1-checks-r2/checks.json').read_bytes()); assert checks['allPassed']
deriv = json.loads((A / PRE / 'evidence/c1b1-checks-r2/vcs-derivation.json').read_bytes())
WT = '/Users/sb/code/opensip-ai/opensip-c1b1'; PKG = '/Users/sb/code/opensip-ai/opensip'
RV.mkdir(parents=True, exist_ok=True); assert not (RV / 'review.json').exists()
(RV / 'REQUEST.md').write_text(f'''# Review request: C1B-1-r2 (the snapshot's Git reads; M3-C r8 item 4, C1b plan r6 sub-unit C1b-1), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`{RV}/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store, overlay or held-out entry, or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree, each writing under `/tmp`:
    - `python3 -I -B tools/security/snapshot_ledger_model.py --check --architecture {A} --packages-root {PKG}`;
    - `python3 -I -B tools/check_operability.py source --repository .`;
    - the package's `evidence/vcs_derivation_c1b1.py <worktree> <architecture>`;
    - the package's `evidence/receipt_specific_record_c1b1.py <worktree> {PKG} <architecture> <out>`.

## Subject

- **Manifest:** `{SUBJECT}` in `{A}` (uncommitted): {len(raw):,} bytes, SHA-256 `{sha}`, {len(subject["files"])} members. Rehash every member.
- **The lane base and candidate base:** product main `{source["productBase"]}`. It holds:
  - C1a4's blind refresh (`0772eb7`), the batch's accepted baseline;
  - C1b-0 (`c9c18f7`), which opened the C1b batch;
  - C1c-0 (`813d559`), which joined it;
  - C2a-1 with inventory v223 (`01769e9`), D2b-3a with inventory v224 (`59144e0`), CI-1 with inventory v225 (`50f1ac1`), C2a-2 with inventory v226 (`1749259`, `5de9fd4`), and the supervisor, operability and C2a-3k units (`d704ed4`, `274dccc`).
- **The candidate worktree:** `{WT}`, detached at that base, holding the exact bytes `product-map.json` lists ({len(rows)} files, {len(source["newPaths"])} new).
- **Your round 1:** `codex-c1b-1-r1` (REQUIRED-FINDINGS: C1B1-R1-RF-1; rulings on Q1 and Q2), at `/tmp/opensip-implementation/reviews/codex-c1b-1-r1/`. Its subject `c1b-1-r1-subject.json` and package `c1b-1-r1/` are unchanged.

## r1 dispositions

| r1 | r2 |
| --- | --- |
| **C1B1-R1-RF-1** (repository-proof construction allocated, uncharged) | `RepositoryProof::retained` is allocation-free: each candidate's label is compared in place against borrowed slices of the chain's spelling (`components_prefix`, `is_dot_git_label`), and the proof borrows X2's sample. Identity binding and innermost-first order are unchanged. No charge site is added, so the model, vectors and derivation are unchanged. `Observed::vcs` now builds the subject and the lent root inside the ledger's scope. New controls: `the_proof_selects_the_innermost_repository_at_every_depth` (three nested repositories, roots 40 deep and at every level) and `the_subject_is_built_without_allocating` (the source control over the proof, its helpers, `repository_proof` and `from_operation`). New mutations: an allocation reintroduced into the proof, and the borrowed prefix one component short (a label-length mutation was dropped as equivalent; `c1b1-checks-r2-void-attempt1`). |
| **Q1** (accepted) | Recorded in SCOPE LD-C1B1-5 as an explicit adjustment to PLAN-r6 §4's one-over control. |
| **Q2** (ruled) | Recorded in SCOPE LD-C1B1-8: the separate derivation suffices. |

## Authority

- **The plan:** C1b plan r6 (`docs/implementation/m3/snapshot-plan-c/c1b/PLAN-r6.md`; your `codex-c1b-plan-r6`, ACCEPT), with:
  - sub-unit C1b-1;
  - LD-C1B-1 to LD-C1B-8;
  - the r4, r5 and r6 changes and your Q6 and Q7 rulings;
  - §4's C1b-1 controls and §5's C1b-1 mutations.
- **The law:** M3-C r8 item 4 and the M3-C r9 law record's caps (`c1a-r9/RECORD-r9.md`).
- **X2:** item 6a and item 6b as built in `custody/git_tracking.rs`.
- **The batch so far:** C1b-0 r2 (`c1b-0-r2-unit.json`, `census-regeneration.json`) and C1c-0 r2 (`c1c-0-r2-unit.json`, its `receipt-specific.json` and `retention-cap-evidence.json`) as integrated.

## What to review

`SCOPE.md` opens with the r1 dispositions, then states the change table, eight lead decisions (LD-C1B1-1 to LD-C1B1-8), the derivation, the census accounting, the tests and the checks. Judge first **the RF-1 disposition**: the proof's construction allocates nothing (its code, the source control and the harness change), with identity binding and innermost selection preserved and the nested-selection control. Then confirm no regression in:

1. **The subject (LD-C1B-1, LD-C1B1-1, LD-C1B1-2):**
   - `VcsSubject` and `SnapshotRoot::from_operation`, with the proof taken in `snapshot_source.rs` rather than appended to `operation_handoff.rs`;
   - `RepositoryProof::retained`: the innermost `.git` from X2's evidence, over this very chain, by identity;
   - W taken from the `NoRepository` proof's own chain.
2. **The closed forms (LD-C1B-2):**
   - `HEAD`'s two forms and one symbolic level;
   - the loose ref, segment by segment, with only the current directory held;
   - `packed-refs`, with the header, peels and the ascending-order rule for duplicates (LD-C1B1-3);
   - the grammar, with UTF-8 required (LD-C1B1-4);
   - the long-component rule (r6);
   - unborn;
   - the refusal spellings (LD-C1B1-6).
3. **Custody and evidence (LD-C1B-4):** every object judged before it is read, on H's volume; the enclosing `.git`'s metadata against X2's sample.
4. **Members (LD-C1B-5) and the join (LD-C1B-3):**
   - `reach_member`, over borrowed segments, as item 6b reaches;
   - the member projection of every refusal;
   - the `.git` device check;
   - the `Internal` preconditions (LD-C1B1-7).
5. **The caps and the regime:**
   - the 4 MiB read cap;
   - custody's size rule before the read, as your Q1 ruling accepted (LD-C1B1-5);
   - the budget refusal typed, never an observation.
6. **The model and the derivation (LD-C1B-6):**
   - `VcsModel` against `snapshot_vcs.rs`, step by step, and its anchors;
   - the 9 exact cases and the reach pricing control;
   - `vcs_envelope` and `vcs_record_max`;
   - `vcs-derivation.json`: D\\* reproduced ({deriv["model"]["refDirectories"]}); the model's H\\* {deriv["model"]["headBytes"]:,} against the plan's {deriv["plan"]["headBytes"]:,}, and the reason stated; the model's term within the plan's term at the plan's coordinates.
7. **The census (LD-C1B-7):**
   - the `git_tracking.rs` re-pin;
   - the regenerated outputs, differing from main's in their pins only, with every `--check` passing;
   - the cumulative receipt record per receipt: the baseline, the batch so far (C1b-0 and C1c-0), C1b-1's own delta, the union, and the stale rendering;
   - the Q2 ruling as recorded (LD-C1B1-8).
8. **The lane** (`evidence/c1b1-checks-r2/`):
   - suites with equal failure sets and 24 new security tests;
   - Clippy and rustfmt, and the append-only check;
   - the focused tests, the vector moves and the derivation;
   - the census checks, the closure change and the receipt record;
   - FW-01, the environment exceptions, operability and verify_design;
   - the 13 mutations.
9. **Rules:** no new mint-census call, no environment read, no `let _ =`, and base-dirty files appended only.
10. **Inventory:** three new paths.

Write `review.json` as `{{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}}`, with ids `C1B1-R2-RF-n` / `C1B1-R2-NBO-n`.
''')
print(RV / 'REQUEST.md', sha)
