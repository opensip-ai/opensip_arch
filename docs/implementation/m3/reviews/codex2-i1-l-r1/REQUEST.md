CODEX2 review: **I1-L**, the policy-language contract successor that executes items 2 to 4 of the law M3-I1 r2 you accepted. It adds the graph atom `cycle-representative`, its one additive identity member and the atom contract's §4a. This is a **design unit** (a `verify_design` contract successor). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex2-i1-l-r1`.

**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** A timing-sensitive crash-matrix lead set may be using this machine. Run no cargo, no tests and no crash-matrix binary or checker.
- **Scripts.** If you run anything, use only the evidence scripts below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **`verify_design` is not needed.** The lead did not run the real `tools/verify_design.py` tonight. If you run it, do so at `nice -n 19` against a scratch copy of the lock passed with `--lock`, never editing the product.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**

## Subject

The pins are in `hashes.txt`. Every file is untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/preview-pack-i1/i1-l-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 15 members** are:
  - `i1-l/successor.json`;
  - `README.md`;
  - `atom-section-4a.md`;
  - the four JSON successor copies under `i1-l/design/` and `i1-l/product/`;
  - `materialization-map.json`;
  - `evidence/build_i1l.py`, `cycle_representative_model.py`, `check_cycle_representative.py`, `cases-report.json` and `copies-report.json`;
  - the law snapshots `PROPOSAL-r2.md` and `UNITS-r2.md`, the bytes you accepted (LD-L7).
- **Not part of the subject:** `i1-l-unit.json`, the lead's DRAFT-PENDING-REVIEW record.

**Product.** Main is `e093e90`, read-only: F8b, bound on top of `3e64266`. Its lock now has 77 contract successors, F8b being the 77th. F8b changed no file this unit pins. I1-L changes no product byte. Unit I1-a will copy the two product schema sources later.

**Law.** `PROPOSAL-r2.md` (`1eb47d1e…`, your r2 ACCEPT) and `UNITS-r2.md` (`0c3c0f44…`).

## What it does

The README has the full tables. In brief:

1. **Eleven text passage overrides**, all line selectors on Markdown parents and all insert-only:
   - WS:598 and WS:603;
   - their copies in WS's selected effective copy WSE (`source-selection-v2/reference/effective-workflows-and-surfaces.md`), at 602 and 607;
   - IE:214 (the law's exception paragraph, word for word);
   - IE:1266, IE:1334 and IE:1544 (the §4 table row);
   - COMP:34 and COMP:109;
   - ATOM:366, whose `after` appends §4a.

   The law-sourced texts (WS:598, WS:603, IE:214, COMP:34 and the `majorLaw` sentence) were checked mechanically to occur verbatim in the law bytes.
2. **Four complete JSON successor copies** at new paths:
   - IDS → `design/foundation/identity-schemas.v3.json`;
   - PDS → `design/workflows/schemas/policy-document.v2.schema.json`;
   - PIDS → `product/schemas/sources/identity-v3.schema.json`;
   - PPDS → `product/schemas/sources/policy-v2.schema.json`.

   Each copy is its parent's raw bytes with exactly these edits, in place:
   - `cycle-representative` appended **last** to each closed operation enum (IDS and PIDS: two each; PDS: `Atom.op` and `AtomSuccessorV1.op`; PPDS: `Atom.op`);
   - the `majorLaw` sentence (IDS, PIDS);
   - the `description`'s predicate list (PDS, PPDS);
   - **the parent's bound passage overrides carried**: four on IDS (predicate-matching-v2, stage-meta, EC1 ×2) and two on PIDS (EC1 did not override PIDS).

   `copies-report.json` lists every hunk.
3. **§4a** (`atom-section-4a.md`), which has:
   - a heading and a preamble that resolves the law's internal references;
   - law lines 88 to 221 (items 2.1 to 2.9) **verbatim**;
   - successor precisions P0 to P7.
4. **A reference model**, the harness oracle of law item 8, built on `foundation/canonical.py`. It runs 41 cases and 5 op-law refusals:
   - QCM's eight corpus projects, plus S = 0;
   - UNITS cases 1 to 19 and their variants;
   - seven extra cases.

   Every case is also checked to be independent of input encounter order and to agree between two SCC algorithms, and every indeterminate value is checked to carry a blocking cause.

## Deviations from the law, for you to rule on

The README's "Deviations from law r2" records nine items, each resolved by a lead decision:
1. **JSON passages cannot be passage overrides.** A v4 lock refuses line selectors on a JSON parent, and a JSON Pointer override replaces exactly one string. So the PDS and IDS enum appends, and with them `majorLaw`, are carried by complete successor copies, 468a's common4 form (LD-L1).
2. **Inexact anchors.**
   - WS:598 has no `` `all-covered` `` code span.
   - "603-604" and "213-214" each change one line.
3. **IDS placement.** The law says "after `all-covered`", but also "appended", and the IE passage says "changes no ... order". The member is appended last, so no existing member moves (LD-L3).
4. **Five consequential passages are added:** IE:1266, IE:1334, the IE §4 table, COMP:109, and PDS's and PPDS's `description`. Each would otherwise be false or incomplete with an eighth member. This makes the law's "IE changes only by the one passage above" inexact, though not its narrowness, since the three IE passages add no rule (LD-L4).
5. **WSE gets WS's overrides** (LD-L5), following X12-0 and initial-root-binding.
6. **Copies carry their parents' bound overrides** (LD-L2). Raw copies would revert four accepted meanings.
7. **§4a's precisions P0 to P7** fix choices that items 2.3 and 2.5 leave open but that set proof bytes (LD-L6):
   - cause universes on uncertain edges;
   - multi-universe accumulation, and not taking outgoing step 3's return;
   - unique-row dedup;
   - unplaced unresolved edges;
   - census carriers;
   - member order;
   - the sufficiency answer.
8. **The projection registry's inert `AtomSuccessorV1`** keeps four ops, as item 4 keeps the registries unchanged. It is disclosed.
9. **UNITS I1-a is incomplete** for `verify_design`:
   - it needs a 468a-form contract-successor record carrying its new `schemas/admission-registry.json` arch copy;
   - its source maps must re-point to the copies;
   - its atom-registry pins must move, path included.

## Decide

1. **Exactness.** Is every `before` the exact parent line? Is every `after` an insertion that is true and minimal? Is each law-sourced text verbatim?
2. **The copies.**
   - Is each copy exactly its parent plus the stated edits?
   - Is carrying the bound overrides into the copies (LD-L2) right, and is PIDS's omission of EC1's text right?
   - Is appending at the end (LD-L3) the right reading of item 4?
3. **Consequential passages.** Rule on LD-L4's five, on LD-L5, and on whether any other accepted passage still enumerates the closed set. For example: WS, IE, COMP, ATOM, the policy-test schema, `evaluator-projection-registry.v1.json`, and the reference models and checkers, which law item 4 keeps unchanged.
4. **§4a.**
   - Is the verbatim block exactly law lines 88 to 221?
   - Is the preamble's reference resolution right?
   - Is each precision P0 to P7 consistent with items 2.3 to 2.9 and ATOM §4? Is any one wrong or unnecessary?
   - Is any other choice still open?
5. **The model.**
   - Does it implement items 2.2 to 2.7 and P0 to P7?
   - Does each case's expectation follow from the law (UNITS r2's cases 1 to 19 and the corpus table)?
   - Is a discriminating case missing?
6. **Rules.** Rule on LD-L7 (law snapshots as candidates) and LD-L8 (binding order and timing).
7. **Selection.** Is the successor well-formed for selection under `verify_design`'s `contract_successor` and `successor_chain` rules? Is anything else wrong?

## Running the evidence (optional)

Use `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`.

1. **Build check.** `docs/implementation/m3/preview-pack-i1/i1-l/evidence/build_i1l.py --product /Users/sb/code/opensip-ai/opensip --check` rebuilds everything in memory and compares it with the files on disk. It reads the product lock and base blobs read-only.
2. **Dependencies for the cases.** The design encoder imports `jsonschema`. Install it offline into your review directory: `python3.14 -m pip install --no-index --no-cache-dir --find-links ~/opensip-deps/wheels --target /tmp/opensip-implementation/reviews/codex2-i1-l-r1/deps jsonschema==4.25.1`.
3. **Cases.** `.../evidence/check_cycle_representative.py --deps <that dir>` re-runs all cases and compares the result with `cases-report.json`. Leave out `--write`.

The lead ran both twice, with byte-identical results.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `i1-l-subject.json`. The lead's value is `51581c186119fb5e0ea3695e8c0e5fea225b9afd32f46e7ebc3ad73e4eaadcd4`.
- `"successor"`: `{path, bytes, sha256}` of `i1-l/successor.json`. The lead's value is 35443 bytes, `9c490137998222627a011eec72af8c0ed3bb568e3085725fdf11b8610d42c6a1`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change bytes, give the exact replacement text. I1-P (`codex2-i1-p-r1`) depends on this unit and is best reviewed after it. Do not commit.
