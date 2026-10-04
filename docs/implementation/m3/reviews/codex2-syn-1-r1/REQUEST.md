CODEX2 review: **SYN-1**, the native contract successor of the accepted syntax law **M3-E1 r3**. It adds the `NativeCause` member `source-parse-error`, the per-file parse outcome law, the syntax grammar context route and the syntax backend fault route. This is a **design unit** (a `verify_design` contract successor). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex2-syn-1-r1`.

**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** A timing-sensitive crash-matrix lead set may be using this machine. Run no cargo, no tests and no crash-matrix binary or checker.
- **Scripts.** If you run anything, use only the evidence scripts below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **`verify_design`.** `evidence/verify_scratch.py` runs the real `tools/verify_design.py` over an in-memory lock with a synthetic review. It writes nothing. If you run verify_design yourself, do so at `nice -n 19` against a scratch copy of the lock passed with `--lock`, never editing the product.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**

## Subject

The pins are in `hashes.txt`. Every file is untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/syntax-e/syn-1-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 11 members** are:
  - `syn-1/successor.json`, `README.md` and `PASSAGES.md`;
  - the two JSON successor copies, `syn-1/design/native/native-evidence.schemas.v2.json` and `syn-1/product/schemas/sources/native-v2.schema.json`;
  - `materialization-map.json`;
  - `evidence/build_syn_1.py`, `check_syn_1.py`, `verify_scratch.py` and `copies-report.json`;
  - the law snapshot `../PROPOSAL-r3.md`, the bytes Codex accepted (README LD-10).
- **Not part of the subject:** `syn-1-unit.json`, the lead's DRAFT-PENDING-REVIEW record.

**Product.** Main is `cd5958b`, read-only: I1-P is bound, giving 82 contract successors. The record is built against it, and it also binds on `15c0779` (81). SYN-1 changes no product byte. Unit E2s will copy the product schema source later.

**Law and record.**
- **Law:** `docs/implementation/m3/syntax-e/PROPOSAL-r3.md` (`d71031ff…`), M3-E1 r3, accepted by Codex. This unit is item 19's SYN-1 row (E1:689), parts (a) to (f).
- **E0 report:** `docs/implementation/m3/syntax-e/E0-REPORT.md` (`c1011e83…`, arch `c87d311f4`), a record in GROK2's review. **E0 chose T-native** (P5 failed at 0.818 MiB/s). So the unit is written for `native-linked-v1`, and its `wasm32-fuel-v1` text is marked inactive unless the lead's M4 re-decision selects it.

## What it does

The README has the full tables. In brief:

1. **Five insert-only line overrides of `native-evidence.md`.** NE's bound lines are only B-S1's, and none is touched.
   - **NE:288** — a data-document row is a format definition, never a parser.
   - **NE:306** — a new section, "Per-file parse outcomes under the syntax universe". It holds:
     - the outcome table: `parsed`, `syntax-error` (→ `input-closure-incomplete` / `source-parse-error`), `truncated:<bound>` (→ `budget-exhausted`) and `backend-fault` (no Coverage);
     - the selected branch's residual risk;
     - the whole-file rule, precedence, and clones;
     - **tree validation, with the reserved ERROR symbol 65535 as the one exception**, which is E0's record item;
     - the byte layout's status, which is not contract;
     - the `clones-near` envelope, case by case, and the group retention rule;
     - no envelope after a fault, and the trust limit.
   - **NE:3366** — the §10 row gains `source-parse-error`.
   - **NE:3530** — a new route row, **syntax grammar context**: `request-rejected` / `REQUEST.PRECONDITION_FAILED`, before PlanId. It names 25 keys:
     - NEM's eleven existing §1.2 keys;
     - E1's chain keys, split by branch;
     - one new key, `native.syntax-grammar-closure-absent`, for a missing closure (LD-4).
   - **NE:3541** — a new route row, **syntax backend fault**: `operational-failed` / `SYSTEM.OUTCOME.ILLEGAL_STATE` (`host-invariant`) / `HOST.INVARIANT_VIOLATED`, with subject `native.syntax-backend-fault:<grammarId>`.
2. **Two complete JSON successor copies**, I1-L's form:
   - NES → `design/native/native-evidence.schemas.v2.json`;
   - its selected product source PNES → `product/schemas/sources/native-v2.schema.json`.

   In each, `source-parse-error` is inserted at its code-point position in `#/$defs/NativeCause/enum` and in `…/input-closure-incomplete/allowedCauses`. That row's `rule` text, which said "twelve", is restated for thirteen. Nothing else changes, and no override is bound to either parent.
3. **(f): no startup-schema, `UnavailableReasonV3`, `DeficiencyV2` or D9 change, and no NEM change** (LD-6).

## Lead decisions and deviations, for you to rule on

- **LD-1** — T-native is primary; T-wasm text is marked inactive.
- **LD-2** — ERROR 65535 is the one exception to "a symbol in the table". It is not a `SymbolTableV1` row, and the error flag must agree with it.
- **LD-3** — The decoded validation law is contract; `SyntaxTreeV1`'s byte layout is not. E2a fixes the layout, and E0's probe layout is cited as non-normative.
- **LD-4** — The new key `native.syntax-grammar-closure-absent`.
- **LD-5** — A new row after NE:3530 rather than a widened NE:3530 cell.
- **LD-6** — No NEM change, so no copy of B-S9's NEM copies.
- **LD-7** — Descriptions change only where they become false.
- **LD-8** — The code-point position, not appended last.
- **LD-9** — The product copy rides in this subject.
- **LD-10** — The law snapshot as a candidate.
- **LD-11** — SYN-1 and SYN-1F stay two units, but bind together in one commit: SYN-1, then CRC-1 if it is unbound, then SYN-1F. The merge was considered and rejected.
- **LD-12** — The backend-fault row uses only existing members. The D9 owner's assent is recorded, and J1's rows go to its next revision (X-J1).
- **Deviations E-1 to E-8,** record items for E1's next revision:
  - the ERROR exception;
  - wasm headers and eager compilation (T-wasm only);
  - NEM unchanged;
  - `-normalization-map-mismatch` missing from item 19's (d) list;
  - no key for a missing closure;
  - A12 widened to SYN-NS's level files;
  - E0's E2a observations.

## Decide

1. **Outcome law.** Is the NE:306 section exactly E1 items 10, 11 and 14a for `native-linked-v1`, with every T-wasm difference marked? Is anything missing or wrong in the envelope cases, the precedence or the retention rule?
2. **ERROR.** Is LD-2's exception right, and is the flag-agreement rule sound on both branches? Is E0's evidence (P3: 8,351 identical trees; the Rust binding's treatment of ids ≥ 65,534) enough?
3. **Keys.** Is the route row complete (`check_syn_1.py` proves its 25 keys against NEM and E1), correctly split by branch, and correctly routed? Is LD-4's new key right?
4. **Backend fault.** Is the row right, and is X-J1 (J1's row 52 and a new J1 row) the right way to give `outcomes.rs` its projection?
5. **Copies.** Is each copy exactly its parent plus the stated edits, with the design-and-product relation kept? Is (f) right, and is any other cause or reason list touched?
6. **NEM.** Is LD-6 right that no NEM byte must change?
7. **Selection.** Is the record well-formed under `verify_design`'s `contract_successor` and `successor_chain` rules? Is anything else wrong?

## Running the evidence (optional)

Use `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, from `docs/implementation/m3/syntax-e/`.

1. **Build check.** `syn-1/evidence/build_syn_1.py --check` rebuilds everything in memory and compares it with the files on disk. It reads the product lock at `cd5958b` with `git show`.
2. **Content checks.** `syn-1/evidence/check_syn_1.py --product /Users/sb/code/opensip-ai/opensip`.
3. **verify_design.**
   - `syn-1/evidence/verify_scratch.py --rev cd5958b` binds SYN-1 alone, 82 → 83.
   - With `--chain` it appends SYN-1, CRC-1 (which SYN-1F needs first), SYN-1F and SYN-NS, 82 → 86.
   - Without `--rev` it runs on the product checkout, verifying the 40 generation and 48 admission sources too.

The lead ran each of these, and each passed. The builds were run twice with `--check`, giving byte-identical results.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `syn-1-subject.json`. The lead's value is `1e4d8b3bf3f5d5613eebb37893fc80f7a952aec9ac201d33b077a9c2993b0da4`.
- `"successor"`: `{path, bytes, sha256}` of `syn-1/successor.json`. The lead's value is 19863 bytes, `b9da5c6d510f19c180227453d95a08fb4ad83cbb0ba45a1cc15a828639eb1dd8`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change bytes, give the exact replacement text.

SYN-1F (`codex2-syn-1f-r1`) binds with this unit and is best reviewed right after it. SYN-NS (`codex2-syn-ns-r1`) is independent. Do not commit.
