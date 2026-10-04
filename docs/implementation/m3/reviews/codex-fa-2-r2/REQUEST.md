Codex review: **FA-2 r2**, the native contract successor that gives a TypeScript or Rust provider's symbol census a lawful carrier on TS2 and Rust3. It answers M3-H's X-H1. This is round 2 of a **design unit** (a `verify_design` contract successor). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex-fa-2-r2`.

**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** A timing-sensitive crash-matrix lead set may be using this machine. Run no cargo, no tests and no crash-matrix binary or checker.
- **Scripts.** If you run anything, use only the evidence scripts below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**

## Subject

The pins are in `hashes.txt`. Every file is untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/native-successors-fa/fa-2-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 11 members** are the same paths as r1. Three changed: `fa-2/successor.json`, `fa-2/README.md` and `fa-2/evidence/build_fa2.py`. The rest are byte-identical to r1.
- **For diffing:** r1's changed members, and its subject manifest and unit record, are kept in `reviews/codex-fa-2-r2/r1-members/`. Your r1 review is copied into `reviews/codex-fa-2-r1/` with status REQUIRED-FINDINGS.
- **Not part of the subject:**
  - `native-successors-fa/fa-2-unit.json`, the lead's DRAFT-PENDING-REVIEW record, now pointed at this review;
  - `reviews/codex-fa-2-r2/scratch_verify.py` and its log `scratch-verify.txt`, the lead's selection check.

**Parents:** unchanged, five accepted lock inputs at their pinned bytes. They are NE (13 line overrides); the provider-startup schema and its selected product copy (3 pointer overrides each); and the provider-handshake schema and its product copy (complete successor copies).

**Product and lock.** `/Users/sb/code/opensip-ai/opensip`, read-only. Main is `cd5958b` (82 contract successors). The lock is pinned in `hashes.txt` as `design-lock.json@cd5958b`; read it with `git show cd5958b:design-lock.json`. FA-2 changes no product byte.

**Context, not subject:** M3-L r4 (`provider-protocol-l/PROPOSAL.md`), in review with Grok beside this unit. Its item 22 joins FA-2. Its third delta-round trigger reopens L for any forced change to a part of FA-2 that sets a wire member, a key's commitment, the admission point or the reuse treatment, which includes every §0 row. M3-H r1 (`fact-admission-h/PROPOSAL-r1.md`) remains the obligation's source.

## What r2 changes

The README's "r2 changes" table has the details.
1. **FA2-R1-01.** The NE:1927 insertion now reads "(for a `symbol`-kind key in a TypeScript or Rust universe, the census admitted under §9.8)". That is your exact text, in the generator, the successor and the README row. LD-F2's host bullet says the same.
2. **FA2-R1-02.** X-FA2-C is your exact row, with two additions:
   - host-derived inventories are routed to X-H3, "routed to M3-C r8 and CRC-2";
   - a clause that syntax universes have no child (X-FA2-E1).
3. **FA2-N1-01.** Recorded, not changed. The design-evidence models are neither parents nor members, they are historical evidence, and you asked for no byte change. The implementing owners track successor-aware loading and the conditional symbol-key check (X-FA2-D, X-FA2-H).
4. **FA2-N1-02.** The evidence count is your exact text: 7 valid, 5 refused, 2 projected-SIS.
5. **Re-pinned and re-verified.**
   - `build_fa2.py` now checks the locks at `e093e90`, `15c0779` and `cd5958b`, and rebuilds byte-identically.
   - The product's own `tools/verify_design.py@cd5958b` was run on a scratch lock: `cd5958b`'s 82 successors plus FA-2 r2 as the 83rd, with labelled synthetic review and assent that exist only in scratch. It passed, with 10 candidates and 19 overrides.

No carrier, commitment, wire member, admission point or reuse treatment changes.

## Decide

1. **FA2-R1-01 and FA2-R1-02.** Are both answered exactly? Is the narrowed X-FA2-C consistent with LD-F6, §9.8's "When a census is owed", X-FA2-E1 and X-H3? Are the two additions to your row right?
2. **FA2-N1-01.** Is recording it, with the stated reasons and owners, an adequate disposition?
3. **Scope.** Did r2 change anything else? Diff the three changed members against `r1-members/`, and confirm the other eight are byte-identical.
4. **Selection.** Is the successor well formed under `verify_design`'s `contract_successor` and `successor_chain` rules at `design-lock.json@cd5958b`? You may re-run `scratch_verify.py`; it redirects only the two synthetic acceptance paths and writes only to its scratch directory.
5. **Anything else wrong.**

## Running the evidence (optional)

Use `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`.
1. **Dependencies.** Reuse your r1 `deps` directory, or reinstall offline into this review directory: `python3.14 -m pip install --no-index --no-cache-dir --find-links ~/opensip-deps/wheels --target /tmp/opensip-implementation/reviews/codex-fa-2-r2/deps jsonschema==4.25.1`.
2. **Build check.** Run `docs/implementation/m3/native-successors-fa/fa-2/evidence/build_fa2.py --product /Users/sb/code/opensip-ai/opensip --deps <deps> --check`.
3. **Scratch selection.** Run `docs/implementation/m3/reviews/codex-fa-2-r2/scratch_verify.py --product /Users/sb/code/opensip-ai/opensip --scratch /tmp/opensip-implementation/reviews/codex-fa-2-r2/verify`.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `fa-2-subject.json`, which is in `hashes.txt`;
- `"successor"`: `{path, bytes, sha256}` of `fa-2/successor.json`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change bytes, give the exact replacement text. Do not commit.
