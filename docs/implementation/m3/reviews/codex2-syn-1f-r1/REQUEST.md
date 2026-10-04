CODEX2 review: **SYN-1F**, the foundation mirror successor of the accepted syntax law **M3-E1 r3**. It adds `source-parse-error` to the five foundation `NativeCause` copies and to the four product sources E2s materializes, and states that execution-inputs §6 applies unchanged to the syntax-only `clones-near` envelope. This is a **design unit** (a `verify_design` contract successor). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex2-syn-1f-r1`.

**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** A timing-sensitive crash-matrix lead set may be using this machine. Run no cargo, no tests and no crash-matrix binary or checker.
- **Scripts.** If you run anything, use only the evidence scripts below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **`verify_design`.** `evidence/verify_scratch.py` runs the real tool over an in-memory lock and writes nothing. If you run verify_design yourself, use a scratch copy of the lock with `--lock`.
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

**Product.** Main is `cd5958b`, read-only, with 82 contract successors. The lock is pinned as `design-lock.json@cd5958b` in `hashes.txt`. SYN-1F changes no product byte.

**Law and companions.**
- **Law:** `docs/implementation/m3/syntax-e/PROPOSAL-r3.md` (`d71031ff…`). This unit is item 19's SYN-1F row (E1:690).
- **SYN-1** (now at r2, `codex2-syn-1-r2`, subject `4ed2d9ba…`; r2 changed none of the files this unit reads) is its companion: it adds the member to the native owner NES. EXM:851 holds the execution-input copy equal to NES, so the two bind in one commit, SYN-1 first, and neither binds alone.
- **CRC-1** is M3-C's closure-role successor, now at **r3** (`docs/implementation/m3/snapshot-plan-c/crc-1/`, `successor.json` `01a995b9…`, subject `e030a1cf…`, in Grok's review at `docs/implementation/m3/reviews/grok-crc-1-r3/`). It puts three JSON Pointer overrides on I1-L's selected identity-schema copy, which is this unit's IDS parent:
  - the `manifestDigest` artifact text;
  - the `closureKinds` note;
  - the `closureMembership` selection law.

  This unit's IDS copy carries those three overrides **as CRC-1 r2 states them and r3 keeps them byte for byte**, and **CRC-1 r3's record is one of its parents**, so verify_design refuses SYN-1F until CRC-1 is bound (LD-F3). A scratch probe confirms the refusal.

  **Why r2.** GROK2's r1 finding changed CRC-1's `closureMembership` selection law, which now ends "…and is never selected otherwise, not even explicitly; the core adapter closure is never a member." That replaces r1's wrong "explicitly included". CRC-1's IE:285 changed the same way; that is a text override, and this unit does not carry it. r3 changed only the record's candidate pins (Grok's r2 finding was a stale review path in CRC-1's builder), so this unit's r3 build is a parent-only rebuild: the IDS copy is byte-identical to the r2 build (`73645b76…`), and only the parent pin, the record, the subject and the README's CRC-1 citation changed. Earlier builds on CRC-1 r1 and r2 were never sent.

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
   - The design identity copy also carries **CRC-1's** three overrides (r2's strings, unchanged in r3).
   - The product identity copy carries neither EC1's nor CRC-1's text, matching its parent.
   - Every other parent has no bound override.
2. **One insert-only override of `execution-inputs-contract.v1.md`** (EXC:257, in §6). It adds a paragraph: the syntax-only `clones-near` envelope is admitted by §6 and `derive_outcome` unchanged. Its producer is the core provider closure, as M3-C r6's X-C1 and CRC-1 record it; this unit adds no closure-role text. Its stage, its census (X-C2) and its pair follow SYN-1's NE §1.2 law, and `source-syntax-invalid` stays distinct.

## Lead decisions, for you to rule on

- **LD-F1** — Complete copies.
- **LD-F2** — Product copies in the subject, one per selected product source, even when byte-equal to the design copy.
- **LD-F3** — The IDS lineage: from I1-L's copy, carrying CRC-1's overrides, with CRC-1 as a parent. `--without-crc-1` is the fallback order, but it produces new bytes and needs a new review.
- **LD-F4** — The code-point position (SYN-1 LD-8).
- **LD-F5** — The EXC paragraph cites CRC-1 and does not restate it.
- **LD-F6** — No model or checker change.
- **LD-F7** — EPR gets its design-only copy.

**Consequence for E2s:** its identity source carries I1-L's member, so E2s lands after I1-a, or carries I1-a's identity change with it.

## Decide

1. **Selectors.** Are these exactly E1's five foundation copies and the four product sources E2s needs, with no other cause or reason list touched?
2. **Copies.** Is each copy its effective parent plus one member, at the code-point position? Do the identity copies carry I1-L's and CRC-1's meanings correctly, and is the product copy right to carry neither EC1's nor CRC-1's text?
3. **Order.** Is binding after CRC-1, enforced through the parent pin, right? Is the fallback acceptable?
4. **EXC.** Is the §6 paragraph true and minimal, and does it stay off CRC-1's and C's ground?
5. **Selection.** Is the record well-formed under `verify_design`? Is anything else wrong?

## Running the evidence (optional)

Use `python3.14 -I -B` at `nice -n 19`, from `docs/implementation/m3/syntax-e/`.
1. **Build check.** `syn-1f/evidence/build_syn_1f.py --check` rebuilds everything and compares. It reads the lock at `cd5958b` and CRC-1 r3's record at its pinned sha (`01a995b9…`).
2. **Content checks.** `syn-1f/evidence/check_syn_1f.py`.
3. **verify_design.**
   - `syn-1f/evidence/verify_scratch.py --rev cd5958b` appends CRC-1 r3, then SYN-1F, 82 → 84.
   - With `--chain` it appends SYN-1, CRC-1, SYN-1F and SYN-NS, 82 → 86.
   - Without `--rev` it runs on the checkout, with generation and admission sources verified.

The lead ran each of these, and each passed. The builds were byte-identical across two `--check` runs.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `syn-1f-subject.json`. The lead's value is `948b39a56a6cc0e483f834085689f20601e040f7221fb2f7ad2df2dbb4dba4fc`.
- `"successor"`: `{path, bytes, sha256}` of `syn-1f/successor.json`. The lead's value is 9697 bytes, `ee8f5e4e03d2f9317e2b6fb454d9c0a565aa5378fe57714fc990dc850d3a29f9`.

This is a contract successor, so it has no `inventoryCandidateAssessment`.

**If CRC-1 r3's bytes change in Grok's review,** this unit's pins change too. The lead will rebuild it and ask you for a recheck. Do not commit.
