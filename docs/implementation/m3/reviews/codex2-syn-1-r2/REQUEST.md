CODEX2 re-review: **SYN-1 r2**, the native contract successor of the accepted syntax law **M3-E1 r3**, after your r1 finding. This is a **design unit** (a `verify_design` contract successor). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** with `subjectManifestSha256`, or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex2-syn-1-r2`.

**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** Run no cargo, no tests and no crash-matrix binary or checker; a timing-sensitive lead set may be using this machine. Do not import or run the native model.
- **Scripts.** If you run anything, use only the evidence scripts below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **`verify_design`.** Run it only through `evidence/verify_scratch.py`, which writes nothing and holds a synthetic review and assent in memory. Never edit the product or its lock.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**

## Subject

The pins are in `hashes.txt`. The SYN-1 files are still untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/syntax-e/syn-1-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 12 members** are r1's eleven plus one new evidence file, `syn-1/evidence/key-forms.json`.
- **Not part of the subject:** `syn-1-unit.json`, the lead's DRAFT-PENDING-REVIEW record. It now carries the r2 pins and the review path `docs/implementation/m3/reviews/codex2-syn-1-r2/review.json`.

**Product.** Main is now `392499e` (`392499e3a42ab9f45d517b8c267a83031abf3863`), read-only, with 83 contract successors: CRC-1 r4 was bound on top of `cd5958b`, and that commit changes only `design-lock.json`. r2's record is built against `design-lock.json@cd5958b`, as r1 was; its generated members record that base. Nothing SYN-1 reads changed at `392499e`: CRC-1 binds no NE, NES or PNES selector, and the product native source is unchanged. So the subject stands, the build check still reads `cd5958b`, and the scratch verify runs on `392499e`.

**Law.** `docs/implementation/m3/syntax-e/PROPOSAL-r3.md` (`d71031ff…`), M3-E1 r3. This unit is still item 19's SYN-1 row, parts (a) to (f). E0 chose T-native (`E0-REPORT.md`, `c1011e83…`).

## What r2 changes

The diff base is the r1 subject, `1e4d8b3b…`, which you reviewed. Its exact bytes are in this directory's `r1-members/`: the r1 subject manifest and the five r1 members that change, each verified against the r1 pins. The other six members are byte-identical to r1:
- the two JSON copies;
- `materialization-map.json`;
- `copies-report.json`;
- `verify_scratch.py`;
- the law snapshot.

| Member | r1 | r2 | Change |
|---|---|---|---|
| `syn-1/evidence/build_syn_1.py` | 29827, `29139e34…` | 39144, `164f014a…` | **RF-SYN1-1.** NE:306's block gains, at its end, **"Syntax grammar context refusal keys and their emitted forms"**: one row per route key (25), with key, emitted form(s), subject, when raised, and branch. The NE:3530 sentence "Each key carries its colon-suffixed subject…" becomes "Each key is emitted exactly in the form §1.2's table of syntax grammar context refusal keys gives, bare or with the subject it shows, and the refusals are one sorted set." **NB-SYN1-1:** your replacement text, verbatim. `key-forms.json` is a static candidate. |
| `syn-1/successor.json` | 19863, `b9da5c6d…` | 28228, `c1309a7c…` | Exactly two `after` strings change: NE:306 (the NB text and the key table) and NE:3530 (the one sentence). Also the candidate pins, with the new evidence file added. The parents, selectors, `before`s, the other three `after`s and `standing` are byte-identical. |
| `syn-1/PASSAGES.md` | 15430, `f383bfb8…` | 23546, `d6aee874…` | regenerated: the same two texts |
| `syn-1/evidence/check_syn_1.py` | 7917, `7d9450a7…` | 17070, `5df3a985…` | **Your audit fix, section 6.** It parses the key table from the record. For each of the eleven existing keys it reads, with `ast` (never importing), the literal `refusals.append(...)` emission in all three model copies, and requires the table's form to be character-for-character equal: the frozen NEM, and B-S9's two selected copies `b-s9/reference/native_evidence_model{.v2,}.py`. For each chain key, it requires every subject spelling item 5 gives to occur in the law bytes and map to a table form, with nothing left over. Bare forms must have no colon, and the bare set must be exactly five keys. `--write` writes `key-forms.json`; without it, the check compares. |
| `syn-1/evidence/key-forms.json` | — | 16511, `d66845a1…` | **New.** For each key: its forms, its source, and the model lines in each copy (NEM 2435, 2437, 2440, 2442, 2450, 2463, 2466, 2470, 2472, 2477 and 3034; 3043 in B-S9's selected reference) or the law spellings. |
| `syn-1/README.md` | 23703, `022b918f…` | 30058, `b97ba9b5…` | The new **r2 changes** table, **LD-13** (the absence key is bare), **LD-14** (the table's placement and the tokens E1 left open), observation **O-1**, and updated counts and evidence. |

**The emitted forms, in brief:**
- **Bare (five keys):**
  - `native.syntax-grammar-version-not-from-manifest`, `native.syntax-grammar-bundle-not-in-closure` and `native.syntax-normalizer-spec-not-in-closure`, as the model emits them;
  - `native.syntax-grammar-closure-absent` (LD-13);
  - `native.syntax-grammar-bundle-not-the-registry`, for which E1 gives no subject.
- **The other eight existing keys:** the model's own subjects, for example `…-class-not-the-registered-one:<languageId>:declared=<syntaxClass>:registered=<syntaxClass>`.
- **The chain keys:** item 5's subjects. LD-14 fixes the tokens E1 left open:
  - `<member>` is a fixed tree path;
  - A5's field list;
  - A8's `name|version|fuelModel|<limit>|runtime`;
  - `-build-mismatch`'s four fields plus `linked-symbol-table`;
  - `<path>` is written `<treePath>`.

  `<kind>` widens to `<name>` under E-7.

**Why not your suggested sentence verbatim.** By the lead's direction the route row points at an exact per-key table, rather than at "that item's subjects where specified". It states the same rule per key, and the audit checks it.

**LD-6 is kept.** The native model and B-S9's two selected copies are unchanged.

**Probes.** The new audit refuses all three:
- r1's reading, a suffixed `-version-not-from-manifest`;
- a dropped subject on `-not-in-closure`;
- a reordered `declared`/`registered` subject.

## Decide

1. **RF-SYN1-1.** Is it resolved? Is every one of the 25 forms exact? The eleven existing keys should match the literal emissions, the chain keys item 5's subjects, and the absence key should be bare. Is the audit sufficient?
2. **LD-13.** Is a bare `native.syntax-grammar-closure-absent` right, and distinct from §2.3's closure keys (subject `grammarBundle.closureId`) for a named but unretained or invalid closure?
3. **LD-14.** Is the placement right (§1.2, with the route row citing it, rather than after the §10 table)? Are the fixed tokens right, and does any of them change a meaning E1 fixed?
4. **NB-SYN1-1.** Is the wording as you asked?
5. **Unchanged parts.** Confirm that nothing else changed against r1 (`r1-members/`) except what the table above lists.
6. **Selection.** Is the record well-formed under `verify_design`? Is anything else wrong?

## Running the evidence (optional)

Use `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, from `docs/implementation/m3/syntax-e/`.

1. **Build check.** `syn-1/evidence/build_syn_1.py --check`.
2. **Content checks.** `syn-1/evidence/check_syn_1.py --product /Users/sb/code/opensip-ai/opensip`, without `--write`.
3. **verify_design.** `syn-1/evidence/verify_scratch.py`:
   - `--rev 392499e` binds SYN-1 alone, 83 → 84;
   - `--rev 392499e --chain` binds SYN-1, SYN-1F and SYN-NS, 83 → 86 (CRC-1 r4 is bound, so it is not appended);
   - `--rev cd5958b` binds, 82 → 83 (the build base);
   - without `--rev`, on the checkout, it also verifies the 40 generation and 48 admission sources.

The lead ran each of these, and each passed. The builds were byte-identical across two `--check` runs.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `syn-1-subject.json`. The lead's value is `4ed2d9ba30e825a6f738f39e3b92462e61268f3bef0c13894154f15aa64c9828`.
- `"successor"`: `{path, bytes, sha256}` of `syn-1/successor.json`. The lead's value is 28228 bytes, `c1309a7cd091f062713671c3cbd5371797c87569dbd74f903935882cefce2f6c`.

This is a contract successor, so it has no `inventoryCandidateAssessment`.

SYN-1F binds with this unit; its request is `codex2-syn-1f-r1`, rebuilt on the bound CRC-1 r4. SYN-NS (`codex2-syn-ns-r1`) is queued after this. Neither unit's subject changed with r2. Do not commit.
