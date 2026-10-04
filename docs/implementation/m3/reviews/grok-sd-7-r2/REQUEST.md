GROK2 review: **SD-7 r2**, round 1. SD-7 is the contract successor that the accepted supervisor law M3-D r5 names for "NE §10's follow-ups from r4". r2 is drafted in law VD2's clean form:
- **(a)** a contract passage supersession conforms SD-5's bound NE:3540 row to item 24's root-command predicate (LD-R4-1);
- **(b)** a fresh override adds item 25's request-class row (LD-R4-2);
- **(c)** fresh overrides widen `PROVIDER.NOT_SELECTED`'s code-keyed remedy.

This is a **design-unit (contract successor)** review. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

**SD-7 r2 binds only after VD2-a and F8c are integrated** (one product commit, now with Codex). On main's tool it is refused, failing closed. Reviewing it now is lawful. Binding waits.

Write only under `/tmp/opensip-implementation/reviews/grok-sd-7-r2`.

**Lead note (reviewer change).** This request was written for Grok. **GROK2** reviews it, because Grok is busy with X3a-2. The directory keeps its name, because the builder emits this review path. Write your output under `/tmp/opensip-implementation/reviews/grok-sd-7-r2`. Remember the `supersededPassages` field this request requires in `review.json`. Don't run cargo.


**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git only read-only.
- No cargo, no builds, no tests, no crash-matrix binary or checker. P0's lanes are using this machine.
- If you run anything, use only the three evidence scripts named below, or read-only commands, with `nice -n 19` and `python3.14 -I -B` (`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`). Use a private 0700 `TMPDIR` under your review directory if you need scratch files.
- Do not write to the VD2-a worktree `/Users/sb/code/opensip-ai/opensip-vd2a`. It is read-only for you, as the product is.
- Do not import or execute the native reference models. `check_sd7.py` parses them with `ast`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` stays absent. Do not read or create it.
- Never read the private 413 UUID fixture.

## Subject

The pins are in `hashes.txt`. The subject manifest is `docs/implementation/m3/supervisor-d/sd-7-subject.json` (1,408 bytes, `74c9d407942b93950ec42e141d4e491b68c0f9bbb2d390fc528c824041fa8955`). Its seven members, all under `docs/implementation/m3/supervisor-d/sd-7/`:
- `README.md`: the proposal. Read it first.
- `successor.json`: the record. Three parents (NE and B-S9's two native-model copies), one `passageSupersessions` entry, three `passageOverrides`, six candidates.
- `PASSAGES.md`: generated. The entries' before and after, and the effective §10 rows.
- `evidence/fold-report.json`: generated. VD2 item 4's fold of NE, and the exact `supersededPassages` list.
- `evidence/build_sd7.py`, `evidence/check_sd7.py`, `evidence/verify_scratch.py`.

All of these are untracked in arch until acceptance. `sd-7-unit.json` next to the manifest is the lead's draft, `DRAFT-PENDING-REVIEW`, and names `reviews/grok-sd-7-r2/review.json`. It is not part of the subject.

**r1, for the record only.** SD-7 r1 used NE7, a complete successor copy of NE. It was held and its request (`reviews/grok-sd-7-r1/`) withdrawn unsent, so it was never reviewed. Its members are snapshotted in `reviews/grok-sd-7-r2/r1-members/` (subject `3c60a82b…`). r2 keeps r1's texts byte for byte and drops the copy.

**The locks.**
- **Main** is `design-lock.json@4c761e8` (94 contract successors). Read it with `git -C /Users/sb/code/opensip-ai/opensip show 4c761e8:design-lock.json`. SD-5 is bound there, at position 85.
- **The lock SD-7 r2 binds onto** is the VD2-a worktree's `design-lock.json`: main's 94 plus F8c's staged row, 95, whose review and assent pins are SCRATCH-F8C placeholders. The tool is the worktree's `tools/verify_design.py` (VD2-a, 43,630 bytes, `c01488fd…`). Both are in `hashes.txt`.

**The laws** (accepted snapshots):
- `docs/implementation/m3/supervisor-d/PROPOSAL-r5.md`, M3-D r5 (your ACCEPT, `224b9228…`): LD-R4-1 and LD-R4-2 (MD5:41-42); item 24 (MD5:754-826), with its predicate at MD5:780-795; item 25 (MD5:827-850); the SD-7 row (MD5:1182); X-D4-NE (MD5:1215); row 57 (MD5:1222).
- `docs/implementation/m3/verify-design-vd2/PROPOSAL-r1.md`, VD2 r1 (Codex ACCEPT, `2e4f70b4…`): rule items 1 to 4, especially check 2.7, the review list; probe R1 (VD2:147, VD2:163); the "SD-7 r2" section (VD2:194-211).
- SD-5 (`supervisor-d/sd-5/`, your ACCEPT-DESIGN-UNIT; bound at `052d3cb`) is the superseded meaning.

## What it does

| # | Entry | Parent, selector | Change |
|---|---|---|---|
| 1 | `passageSupersessions` | NE, `{"line": 3540}` | `supersedes` SD-5's record by exact pin (5,805 bytes, `5e115818…`), same parent and selector. `before` is SD-5's `after`. `after` is the raw release-declaration row, then SD-5's row conformed to item 24: EE-3b keeps only its capability form; EE-5a's root command is exactly (a), (b), (c); an analyzer's own mounted root is admitted; the remedy says "claim a project hook, a reserved or additional root command, or a probe". |
| 2 | `passageOverrides` | NE, `{"line": 3539}` (free) | The raw NOT-SELECTED row, then item 25's row: `request-rejected` 2, `REQUEST.UNSATISFIABLE`, `PROVIDER.NOT_SELECTED`, subject `excluded-form:<class>`, and no runId or executionId. |
| 3, 4 | `passageOverrides` | both NEM copies, `{"line": 1159}` | `PUBLIC_ROUTE_REMEDIES["PROVIDER.NOT_SELECTED"]` is widened. Both original clauses are kept, and the three request-class forms and "restate the request without it" are added. |

**The effective NE** (VD2 item 4) after SD-7 r2 is 380,848 bytes, `0dd155c2…`: SD-7 r1's NE7, byte for byte.

## The review must carry `supersededPassages`

Per VD2 rule item 2.7 (X-VD2-5), `review.json` must contain `supersededPassages`, equal by value and in order to the record's `supersedes` list. It is required because the record carries a contract passage supersession, and the tool refuses the binding without it. The exact value, which is also `evidence/fold-report.json`'s `reviewSupersededPassages`:

```json
[{"record": {"path": "docs/implementation/m3/supervisor-d/sd-5/successor.json", "bytes": 5805, "sha256": "5e11581804098116a4afa5052ff27ed426beaebcc6e0a38607d1628ea8a595e7"}, "parent": {"path": "docs/v2/contracts/product-v1/native-evidence.md", "bytes": 329013, "sha256": "83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0"}, "selector": {"line": 3540}}]
```

List it only if you accept the supersession of exactly that passage.

## Lead decisions for you to rule on

- **LD-7.1 (r2).** VD2's supersession for SD-5's row, and fresh overrides for item 25's row (NE:3539) and the remedy. Rejected: the complete copy (r1), an erratum, and a second override.
- **LD-7.2 (r2).** VD2 item 4's effective-text check: r2's effective NE equals r1's NE7.
- **LD-7.3 to LD-7.6 (r1's, carried).**
  - The conformed row changes only what MD5 changes.
  - Item 25's row follows the NOT-SELECTED row.
  - The remedy is widened in both NEM copies.
  - NES's route registry is not extended.

## Feasibility (the lead's runs)

- **`build_sd7.py`**, then `build_sd7.py --check`: identical bytes. It asserts:
  - the lock at `4c761e8` (94);
  - SD-5's pin, and that NE:3540 is bound only by SD-5 and NE:3539 by nothing;
  - no bound override on either NEM copy;
  - the fold equals r1's NE7.
- **`check_sd7.py`** passes. It checks every VD2 condition against the lock, folds NE independently and compares it with r1's snapshot NE7, and checks the texts, the remedy table and the codes.
- **`verify_scratch.py`:**
  - **VD2-a** over the staged lock, with the worktree as the implementation: 95 passes, with `contractPassageSupersessions` 0, and the SCRATCH-F8C placeholders rebuilt to the staged pins. **SD-7 r2 binds: PASS, 95 → 96, `contractPassageSupersessions` 1.** Inventory, inheritance, the 21 inventory supersessions, the 40 generation sources and the 48 admission sources are unchanged.
  - **VD2-a refuses,** with its exact messages: no review list ("not listed by its review"); a wrong list ("differ from the record"); a later override restating SD-5's row ("restates a superseded contract meaning"); a second link naming SD-5 ("double supersession"); a different second override of NE:3539 ("conflicting contract passage overrides").
  - **Plain tool at main `4c761e8`** (`c13d231e…`): main's lock passes at 94. SD-7 r2 is **REFUSED** over main's lock and over the staged lock: "passage supersession must select an inventory row description". It fails closed.

## Decide

1. **The supersession (R1).** Is it VD2's form exactly: target pin, same passage, `before` equal to SD-5's `after`, first link, and the review list? Is NE:3539 the right home for item 25's row?
2. **The conformed row (R2).** Does it state M3-D r5 item 24's predicate and admitted cases exactly, with EE-3b's capability form only and the remedy in MD5's words? Does it change anything MD5 does not?
3. **Item 25's row and the remedy (R3).** Is the row LD-R4-2's route exactly? Is the widened remedy a true next step for every condition that reaches `PROVIDER.NOT_SELECTED`?
4. **The effective NE (R4).** Is it r1's NE7, folded as VD2 item 4 says?
5. **Form.** Is the record well formed for `contract_successor` and for VD2's checks? Is the binding order right (only after VD2-a and F8c)? Is anything else wrong?

## Running the evidence (optional)

From any directory, with `nice -n 19 /opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B`:
1. `docs/implementation/m3/supervisor-d/sd-7/evidence/build_sd7.py --check`, which compares in memory and writes nothing. Always pass `--check`: without it the script rewrites the generated files.
2. `.../sd-7/evidence/check_sd7.py`. It reads the lock and the product's `common-v4.schema.json` through `git show 4c761e8:`.
3. `.../sd-7/evidence/verify_scratch.py`. It reads the VD2-a worktree's tool and lock and main's tool and lock (`git show 4c761e8:`). It holds synthetic reviews in memory, writes nothing, and uses the worktree read-only as the implementation.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `sd-7-subject.json`. The lead's value is `74c9d407942b93950ec42e141d4e491b68c0f9bbb2d390fc528c824041fa8955`;
- `"supersededPassages"`: the list above, exactly, if you accept;
- `"successor"`: `{path, bytes, sha256}` of `sd-7/successor.json`. The lead's value is 14,706 bytes, `350a249afaa001fc97292c2837395d930cc7bdc0d6b62b594b04df55d9767c04`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change text, give the exact replacement. Do not commit.
