Grok review: **SD-7**, round 1. SD-7 is the contract successor that the accepted supervisor law M3-D r5 names for "NE §10's follow-ups from r4". It conforms SD-5's bound NE row to item 24's root-command predicate (LD-R4-1). It also adds item 25's request-class row (LD-R4-2) and widens `PROVIDER.NOT_SELECTED`'s code-keyed remedy. This is a **design-unit (contract successor)** review. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/grok-sd-7-r1`.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git only read-only.
- No cargo, no builds, no tests, no crash-matrix binary or checker. P0's lanes are using this machine.
- If you run anything, use only the three evidence scripts named below, or read-only commands, with `nice -n 19` and `python3.14 -I -B` (`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`). Use a private 0700 `TMPDIR` under your review directory if you need scratch files.
- Do not import or execute the native reference models. `check_sd7.py` parses them with `ast`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` stays absent. Do not read or create it.
- Never read the private 413 UUID fixture.

## Subject

The pins are in `hashes.txt`. The subject manifest is `docs/implementation/m3/supervisor-d/sd-7-subject.json` (1,614 bytes, `3c60a82b2bcd669150240d4345af29461581be900a76d1e961ba716454e58dde`). Its eight members, all under `docs/implementation/m3/supervisor-d/sd-7/`:
- `README.md`: the proposal. Read it first.
- `successor.json`: the record. Four parents, two line overrides, no supersession, seven candidates.
- `contracts/native-evidence.md`: generated. NE7, the complete successor copy of NE.
- `evidence/copies-report.json`: generated. The 39 bound overrides applied, the effective parent's digest, the two hunks, the raw-to-copy line map and the remedy overrides.
- `PASSAGES.md`: generated. The hunks, the effective rows and the remedy overrides.
- `evidence/build_sd7.py`, `evidence/check_sd7.py`, `evidence/verify_scratch.py`.

All of these are untracked in arch until acceptance. `sd-7-unit.json` next to the manifest is the lead's draft, marked `DRAFT-PENDING-REVIEW`, and names `reviews/grok-sd-7-r1/review.json`. It is not part of the subject.

**The lock** is `design-lock.json@6190e66`, current main (SYN-NS's binding, 92 contract successors). Read it with `git -C /Users/sb/code/opensip-ai/opensip show 6190e66:design-lock.json`. M3-D r5 was written at `218465f`; SYN-NS overrides no passage, so NE's effective text is the same at both. The product is read-only, and SD-7 changes no product byte.

**The source law.** `docs/implementation/m3/supervisor-d/PROPOSAL-r5.md`, M3-D r5, the accepted snapshot (your ACCEPT, `reviews/grok-supervisor-d-r5`, `224b9228…`). Read:
- the r4 changes rows for LD-R4-1 and LD-R4-2 (MD5:41-42);
- item 24: its class table (MD5:771-778), the root-command predicate (MD5:780-788), who refuses each form (MD5:789-794), SD-5's bound row (MD5:795) and D4-T4 (MD5:818-825);
- item 25: the route, its reasons and its rejections (MD5:827-851);
- the SD-7 row (MD5:1182), F14 and F15 (MD5:1204-1205), X-D4-NE (MD5:1215) and row 57 (MD5:1222).

**The superseded meaning** is SD-5 (`supervisor-d/sd-5/`, your ACCEPT-DESIGN-UNIT, bound at `052d3cb`). Its NE §10 row is the second line of its override of NE:3540.

## What it does

1. **NE7.** A complete successor copy of `docs/v2/contracts/product-v1/native-evidence.md` (B-S9's form). It is NE's effective text at `6190e66`, with all 39 bound line overrides from B-S1, FA-2, RUST3-LIM, SYN-1, FA-1 and SD-5 applied, plus exactly two hunks:
   - **copy line 3822, inserted:** item 25's request-class row, after the NOT-SELECTED row. It routes to `request-rejected` 2, `REQUEST.UNSATISFIABLE`, `PROVIDER.NOT_SELECTED`, subject `excluded-form:<class>` (the first of EE-2, EE-4, EE-6a), with `errors` exactly that detail, and no runId or executionId.
   - **copy line 3824, replaced:** SD-5's row, conformed to item 24. EE-3b keeps only its capability form. EE-5a's root command is exactly predicate (a), (b) and (c). An analyzer's own name-bound mounted root is admitted, and so is a live-name collision. A manifest the security owner refuses first keeps that route. The remedy phrase becomes MD5:1182's "claim a project hook, a reserved or additional root command, or a probe". The class, code, detail, subject and route sentences are SD-5's.

   The record's `standing` makes NE7 the selected NE. Every later NE successor overrides NE7.
2. **The remedy.** Line 1159 of both B-S9 native-model copies (`PUBLIC_ROUTE_REMEDIES["PROVIDER.NOT_SELECTED"]`, the only place the string lives) becomes: "this capability is not selected for that language mode, or the request asks for an external discovery or public-lifecycle endpoint, untrusted native or WASM admission, or network-granted analysis; no promise is made for it; restate the request without it". Both original clauses are kept, and NE7's new row quotes this string.

## Lead decisions for you to rule on

- **LD-7.1 (form).** B-S9's complete-copy form for NE, and fresh line overrides for the remedy. No line override can conform SD-5's row: `verify_scratch.py` shows that a second override of NE:3540 and a VD1 supersession of SD-5's entry both refuse. A `verify_design` successor is not needed, because the copy form is lawful today.
- **LD-7.2.** The copy carries the effective text, not the raw parent.
- **LD-7.3.** The conformed row changes only what MD5 changes.
- **LD-7.4.** Item 25's row sits right after the NOT-SELECTED row it reuses.
- **LD-7.5.** The remedy is widened in both model copies, with both clauses kept.
- **LD-7.6.** NES's route registry is not extended.

## Feasibility (the lead's runs)

- **`build_sd7.py`**, then `build_sd7.py --check`: identical bytes. It asserts:
  - the lock at `6190e66` has 92 successors;
  - every bound NE override's `before` matches its raw line;
  - no bound override touches either model copy;
  - SD-5's row and each conformed phrase occur exactly once.
- **`check_sd7.py`** passes:
  - it recomputes the effective NE independently and diffs it against NE7: exactly one insertion and one replacement;
  - the line map is exact over all 4,282 raw lines;
  - the conformed row's cells equal SD-5's except the remedy phrase, and it states the predicate;
  - the new row is LD-R4-2's route;
  - `PUBLIC_ROUTE_REMEDIES` is otherwise unchanged in both copies, and the only other key reaching `PROVIDER.NOT_SELECTED` is the NOT-SELECTED cell's;
  - every code is an existing one, and MD5's texts are as quoted.
- **`verify_scratch.py`**, at `--rev 6190e66` and on the main checkout:
  - **SD-7 binds:** 92 to 93, with two overrides and no supersession. The selected inventory and inheritance are unchanged, and 40 generation sources are verified on the checkout.
  - **The rejected forms refuse:** a second override of NE:3540, and a VD1 supersession of SD-5's entry.
  - **Later successors:** an NE7 line override passes; a second line-1159 override refuses; a raw NE line override passes. The last is the copy form's residual hazard, held by review.

## Decide

1. **The form (R1).** Is the complete-copy form for NE lawful and right here, given that NE is cited by line across the laws? Are the selection statement, the line map and the stated residual hazard sufficient? Would you instead require a `verify_design` successor?
2. **Exactness (R4).** Is NE7 exactly the effective NE at `6190e66` plus the two hunks? Are the two remedy `before`s exact?
3. **The conformed row (R2).** Does it state item 24's predicate and admitted cases exactly, with EE-3b keeping only its capability form and the remedy in MD5's words? Does it change anything MD5 does not?
4. **Item 25's row and the remedy (R3).** Is the row LD-R4-2's route exactly? Is the widened remedy a true next step for every condition that reaches `PROVIDER.NOT_SELECTED`, under NES's remedy-keying constraint?
5. **Form.** Is the successor well formed for selection under `verify_design`'s `contract_successor` and `successor_chain` rules? Is anything else wrong?

## Running the evidence (optional)

From any directory, with `nice -n 19 /opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B`:
1. `docs/implementation/m3/supervisor-d/sd-7/evidence/build_sd7.py --check`, which rebuilds in memory, compares with the files on disk and writes nothing. Always pass `--check`: without it the script rewrites the generated files.
2. `.../sd-7/evidence/check_sd7.py`. It reads the lock and the product's `common-v4.schema.json` through `git show 6190e66:`.
3. `.../sd-7/evidence/verify_scratch.py --rev 6190e66`. It execs `tools/verify_design.py` from `6190e66` through `git show`, holds synthetic reviews and probes in memory, and writes nothing.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `sd-7-subject.json`. The lead's value is `3c60a82b2bcd669150240d4345af29461581be900a76d1e961ba716454e58dde`;
- `"successor"`: `{path, bytes, sha256}` of `sd-7/successor.json`. The lead's value is 5,440 bytes, `c1b9baa76f0b888300cd72696d5b3e73ca5c94bdd3fdbd6e7a6249ab71914a4d`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change text, give the exact replacement. Do not commit.
