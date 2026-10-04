Grok review: **SD-5**, round 1. SD-5 is the successor that the accepted supervisor law M3-D r3 names for the public projection of its internal refusals. This unit is its `ExcludedForm` half for **R10a**: the public route of a manifest-class excluded form refused at pre-draw component admission. M3-J1 r4 records it as successor S20. This is a **design-unit (contract successor)** review. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/grok-sd-5-r1`.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git only read-only.
- No cargo, no builds, no tests, no crash-matrix binary or checker. P0's lanes are using this machine.
- If you run anything, use only the three evidence scripts named below, or read-only commands, with `nice -n 19` and `python3.14 -I -B` (`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`). Use a private 0700 `TMPDIR` under your review directory if you need scratch files.
- Never touch the real home: `~/Library/Application Support/OpenSIP` stays absent. Do not read or create it.
- Never read the private 413 UUID fixture.

## Subject

The pins are in `hashes.txt`. The subject manifest is `docs/implementation/m3/supervisor-d/sd-5-subject.json` (1,203 bytes, `8b9a4998a6c1e86d7c57ca655203241d2d2f0bc5e267ac552485c51cd3dbbca4`). Its six members, all under `docs/implementation/m3/supervisor-d/sd-5/`:
- `README.md`: the proposal. Read it first.
- `successor.json`: the record. One parent (NE), one line override, no supersession, five candidates.
- `PASSAGES.md`: generated. The override's exact `before` and `after`, the effective table rows around it, and the new row cell by cell.
- `evidence/build_sd5.py`, `evidence/check_sd5.py`, `evidence/verify_scratch.py`.

All of these are untracked in arch until acceptance. `sd-5-unit.json` next to the manifest is the lead's draft, marked `DRAFT-PENDING-REVIEW`. It is not part of the subject.

**The lock** is `design-lock.json@cd5958b`, 82 contract successors. Read it with `git -C /Users/sb/code/opensip-ai/opensip show cd5958b:design-lock.json`. The product is `/Users/sb/code/opensip-ai/opensip` at main `cd5958b`, read-only. SD-5 changes no product byte.

**The source laws** (accepted snapshots; pins in `hashes.txt`):
- `docs/implementation/m3/supervisor-d/PROPOSAL-r3.md`, M3-D r3 (GROK2 ACCEPT, `9679dbc4…`): item 24, the manifest-class refusals at R10a (MD:708-746), and in it the internal refusal and its recommended projection (MD:733); item 25, the request class (MD:748-763); the successor table's SD-5 and SD-6 rows (MD:1091-1092).
- `docs/implementation/m3/host-pipeline-j/PROPOSAL-r4.md`, M3-J1 r4 (GROK2 ACCEPT, `c18c0d3c…`): R10a's order row and bullet (MJ:325, MJ:337-349), ER10a (MJ:426), the outcome matrix and its totality (MJ:638-708), row 27 (MJ:673), and S20 (MJ:774).
- The J1 r4 drafter's note: "Until SD-5 lands, J1's outcome-matrix totality is incomplete for `ExcludedForm`. SD-5 must also keep that refusal distinct from matrix row 27 (indeterminate, exit 3)."

## What it does

One insert-only line override of `docs/v2/contracts/product-v1/native-evidence.md` (NE, `83b99783…`). After §10's "invalid authenticated RELEASE DECLARATION" row (NE:3540), it adds one row to the same five-column admission and event route table: "**component manifest that is an excluded form**". The route:
- **Condition.** An authenticated component manifest that current trust admits and the analysis step can select, refused at component admission before any analysis attempt's `ExecutionId` is drawn or reserved, durable or ephemeral, as `ExcludedForm {class, subject}`. The classes are EE-1, EE-3b, EE-4's manifest part and EE-5a, as MD:728-731 represents them.
- **Class, exit and code.** `request-rejected` 2, `EXTENSION.ADMISSION_REJECTED`. That is D9 v1.14's own `extension-admission-rejected` cause and golden, SL S12's admission family, and MD:733's recommendation.
- **Detail.** `domainDetail` is `PAYLOAD-NOT-ADMISSIBLE` (SL:1306's admission row for a signed document that is not admissible), with subject `excluded-form:<class>:<manifestDigest>` (at most 84 characters) and one fixed 355-character remedy. `errors` is exactly that detail, and there is no runId or executionId. With several refusals, the least `manifestDigest` and its first class are named; every `ExcludedForm` goes to the operational record.
- **Distinct from row 27.** It is never a `provider-unavailable` deficiency and never the not-installed golden (WS:1374). A required closure that is not installed, or that current trust does not admit (including an ephemeral request with no trust view), is never an excluded form and keeps that golden.

The README also gives J1's matrix row 56, word for word, for S20.

## Lead decisions for you to rule on

- **LD-S1.** The form: a passage successor to NE §10's admission table, owned by the NE and WS public-route owners. WS:1340-1344 already delegates envelope composition to native §10, so no WS byte changes.
- **LD-S2.** The class and code, against `REQUEST.UNSATISFIABLE`, `REQUEST.PRECONDITION_FAILED` and indeterminate 3.
- **LD-S3.** The detail. Reusing `PAYLOAD-NOT-ADMISSIBLE` is weighed against `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`, `CONTINUE-CORE-NOT-TRUSTED`, `native.release-declaration-invalid`, `CONFIG.INVALID`, an absent detail, and a new code, which MD item 24 forbids.
- **LD-S4 and LD-S5.** One deterministic detail with a fixed-length subject, and one remedy true for all four classes, selected by the subject prefix.
- **LD-S6.** The scope is R10a's and ER10a's `ExcludedForm` only. Item 25's request class is cross-law item X-SD5-1, and the rest of SD-5 stays owed.

## Feasibility (the lead's runs)

- **`build_sd5.py`**, then `build_sd5.py --check`: identical bytes. It asserts:
  - the `before` text;
  - the table header and the row's five columns;
  - that NE is an accepted lock input at its pinned bytes;
  - that no bound successor overrides NE:3540, and that no unbound draft on NE (FA-1, FA-2, rust3-lim, SYN-1) does.
- **`check_sd5.py`** passes:
  - every code-shaped token in the row is an existing member of D9 v1.14, the public detail registry or the product's `DomainDetailCode` at `cd5958b`;
  - D9's golden and SL:1306 give the stated class and code;
  - the remedy is ASCII, at most 1,024 characters and true for each class;
  - row 27, WS:1374 and WSE:1447 read as cited, and the new row differs from them in class, code and detail;
  - MD's and MJ's texts are as cited.
- **`verify_scratch.py`**, at `--rev cd5958b` and on the main checkout:
  - **SD-5 binds:** 82 to 83, with one override and no supersession. The selected inventory and inheritance are unchanged, and 40 generation sources are verified on the checkout.
  - **Binding order:** FA-1, FA-2 and SYN-1 each bind with it in both orders (84).
  - **A later override of NE:3540** refuses: `conflicting contract passage overrides`.

## Decide

1. **Exactness.** Is the `before` the exact parent line, and the `after` that line plus one well-formed row of the table? Is every cited law, contract line and code real and quoted correctly?
2. **The route (LD-S2, LD-S3, LD-S5).** Are the class, exit, code and detail lawful existing values? Is `PAYLOAD-NOT-ADMISSIBLE` with an `excluded-form:` subject and a subject-selected remedy an honest reuse? Or does "two remedies behind one code" (D9's `codeVocabulary.rule`; SL S12's `MIGRATION.CORRUPT` note) make it a defect that needs a dedicated code, and so an owner decision against MD item 24? This is R2, and the question the lead most wants ruled.
3. **Distinctness.** Is the boundary with row 27 complete and stated in the contract text, on the durable, first-use and ephemeral paths?
4. **Totality.** Is J1's row 56, as the README gives it, total for R10a's and ER10a's `ExcludedForm`? Is leaving item 25's request class to X-SD5-1 lawful, and is X-SD5-1's recommendation sound?
5. **Placement (LD-S1).** Is NE §10's admission table the right route table, with no WS byte changed?
6. **Form.** Is the successor well formed for selection under `verify_design`'s `contract_successor` and `successor_chain` rules? Is anything else wrong?

## Running the evidence (optional)

From any directory, with `nice -n 19 /opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B`:
1. `docs/implementation/m3/supervisor-d/sd-5/evidence/build_sd5.py --check`, which rebuilds in memory, compares with the files on disk and writes nothing. Always pass `--check`: without it the script rewrites the generated files.
2. `.../sd-5/evidence/check_sd5.py`. It reads the product's `schemas/sources/common-v4.schema.json` through `git show cd5958b:`.
3. `.../sd-5/evidence/verify_scratch.py --rev cd5958b`. It execs `tools/verify_design.py` from `cd5958b` through `git show`, holds synthetic reviews in memory and writes nothing.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `sd-5-subject.json`. The lead's value is `8b9a4998a6c1e86d7c57ca655203241d2d2f0bc5e267ac552485c51cd3dbbca4`;
- `"successor"`: `{path, bytes, sha256}` of `sd-5/successor.json`. The lead's value is 5,805 bytes, `5e11581804098116a4afa5052ff27ed426beaebcc6e0a38607d1628ea8a595e7`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change text, give the exact replacement. Do not commit.
