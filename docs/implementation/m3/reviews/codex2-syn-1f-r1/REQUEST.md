CODEX2 review: **SYN-1F**, the foundation mirror successor of the accepted syntax law **M3-E1 r3**. It adds `source-parse-error` to the five foundation `NativeCause` copies and to the four product sources E2s materializes, and states that execution-inputs §6 applies unchanged to the syntax-only `clones-near` envelope. This is a **design unit** (a `verify_design` contract successor). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** with `subjectManifestSha256`, or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex2-syn-1f-r1`.

**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** A timing-sensitive crash-matrix lead set may be using this machine. Run no cargo, no tests and no crash-matrix binary or checker. Do not import or run any reference model.
- **Scripts.** If you run anything, use only the evidence scripts below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **`verify_design`.** Run it only through `evidence/verify_scratch.py`, which writes nothing and holds a synthetic review and assent in memory. Never edit the product or its lock.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**

## Subject

The pins are in `hashes.txt`. Every file is untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/syntax-e/syn-1f-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 17 members** are:
  - `syn-1f/successor.json`, `README.md` and `PASSAGES.md`;
  - the five copies under `syn-1f/design/foundation/`;
  - the four copies under `syn-1f/product/schemas/sources/`;
  - `materialization-map.json`;
  - `evidence/build_syn_1f.py`, `check_syn_1f.py`, `verify_scratch.py` and `copies-report.json`.
- **Not part of the subject:** `syn-1f-unit.json`, the lead's DRAFT-PENDING-REVIEW record.

**Product.** Main is `392499e` (`392499e3a42ab9f45d517b8c267a83031abf3863`, CRC-1 bound, 83 contract successors), read-only. The record is built and checked against `design-lock.json@392499e`, read with `git show`, not the live file. SYN-1F changes no product byte.

**Law and companions.**
- **Law:** `docs/implementation/m3/syntax-e/PROPOSAL-r3.md` (`d71031ff…`). This unit is item 19's SYN-1F row (E1:690).
- **SYN-1** (`codex2-syn-1-r2`, r2, subject `4ed2d9ba…`) is its companion: it adds the member to the native owner NES. EXM:851 holds the execution-input copy equal to NES, so the two bind in one commit, SYN-1 first, and neither binds alone. SYN-1's r2 changed none of the files this unit reads.
- **CRC-1**, M3-C's closure-role successor, is **accepted at r4 by Grok and bound at `392499e`** (`snapshot-plan-c/crc-1/successor.json` `29df5f5e…`, subject `ec896801…`). It puts three JSON Pointer overrides on I1-L's selected identity-schema copy, which is this unit's IDS parent:
  - the `manifestDigest` artifact text;
  - the `closureKinds` note;
  - the `closureMembership` selection law.

  This unit's IDS copy carries those three bound overrides. Their strings are the same in CRC-1 r2, r3 and r4: r3 and r4 changed only CRC-1's candidate pins. **CRC-1's record is one of this unit's parents (LD-F3).** Before CRC-1 was bound, verify_design refused SYN-1F alone, as a probe on `cd5958b` confirms. On `392499e` it binds.

**Build history.** Builds on CRC-1 r1 and r2 were never sent. The r3 build was assigned here but not reviewed. This is the final parent-only rebuild, on the bound r4. The IDS copy is byte-identical to the r2 and r3 builds (`73645b76…`).

## What it does

1. **Nine complete JSON successor copies, one member each.** In each, `source-parse-error` is inserted at its code-point position in the one `NativeCause` copy the parent holds:
   - EXS `#/$defs/NativeCause/enum`;
   - IDS `#/$defs/evaluation-deficiency/properties/nativeCause/oneOf/0/enum`;
   - SIS `#/$defs/NativeCause/enum`;
   - ENS `#/$defs/NativeCause/enum`;
   - EPR `#/$defs/NativeCause/enum`;
   - the four selected product sources: execution-inputs-v1, identity-v3, subject-inventory-v1 and enumeration-plan-v1.

   **Their sources and what they carry:**
   - The identity copies descend from **I1-L's** selected copies, so they keep I1-L's `cycle-representative` member and the overrides I1-L carried.
   - The design identity copy also carries **CRC-1's** three bound overrides.
   - The product identity copy carries neither EC1's nor CRC-1's text, matching its parent.
   - Every other parent has no bound override.
2. **One insert-only override of `execution-inputs-contract.v1.md`** (EXC:257, §6). It adds a paragraph: the syntax-only `clones-near` envelope is admitted by §6 and `derive_outcome` unchanged. Its producer is the core provider closure, as M3-C r6's X-C1 and CRC-1 record it; this unit adds no closure-role text. Its stage, its census (X-C2) and its pair follow SYN-1's NE §1.2 law, and `source-syntax-invalid` stays distinct.

## Lead decisions, for you to rule on

- **LD-F1** — Complete copies.
- **LD-F2** — Product copies in the subject, one per selected product source, even when byte-equal to the design copy.
- **LD-F3** — The IDS lineage: from I1-L's copy, carrying CRC-1's overrides, with CRC-1 as a parent.
- **LD-F4** — The code-point position (SYN-1 LD-8).
- **LD-F5** — The EXC paragraph cites CRC-1 and does not restate it.
- **LD-F6** — No model or checker change.
- **LD-F7** — EPR gets its design-only copy.

**Consequence for E2s:** its identity source carries I1-L's member, so E2s lands after I1-a, or carries I1-a's identity change with it.

## Decide

1. **Selectors.** Are these exactly E1's five foundation copies and the four product sources E2s needs, with no other cause or reason list touched?
2. **Copies.** Is each copy its effective parent plus one member, at the code-point position? Do the identity copies carry I1-L's and CRC-1's bound meanings correctly, and is the product copy right to carry neither EC1's nor CRC-1's text?
3. **Order.** Is the CRC-1 parent pin (LD-F3) right, now that CRC-1 is bound?
4. **EXC.** Is the §6 paragraph true and minimal, and does it stay off CRC-1's and C's ground?
5. **Selection.** Is the record well-formed under `verify_design`? Is anything else wrong?

## Running the evidence (optional)

Use `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, from `docs/implementation/m3/syntax-e/`.
1. **Build check.** `syn-1f/evidence/build_syn_1f.py --check` rebuilds everything and compares. It reads the lock at `392499e` and checks that its bound CRC-1 record is `29df5f5e…`.
2. **Content checks.** `syn-1f/evidence/check_syn_1f.py`.
3. **verify_design.** `syn-1f/evidence/verify_scratch.py`:
   - `--rev 392499e` binds SYN-1F alone, 83 → 84;
   - with `--chain` it appends SYN-1, SYN-1F and SYN-NS, 83 → 86;
   - without `--rev`, on the checkout, it also verifies the 40 generation and 48 admission sources.

The lead ran each of these, and each passed. The builds were byte-identical across two `--check` runs.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `syn-1f-subject.json`. The lead's value is `954265fc9de337844208f2f8b925d153a9180c6dea4ce3934c715f6617c62e76`.
- `"successor"`: `{path, bytes, sha256}` of `syn-1f/successor.json`. The lead's value is 9697 bytes, `736f2fed9e8df790e6c9e2d7b32c28275f8c1fb19b12cae93fc8e1b08506a460`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. Do not commit.
