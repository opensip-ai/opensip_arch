Codex review: **FA-2**, the native contract successor that gives a TypeScript or Rust provider's **symbol census** a lawful carrier on TS2 and Rust3. It answers cross-law item X-H1 of the fact-admission law M3-H. This is a **design unit** (a `verify_design` contract successor). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex-fa-2-r1`.

**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** A timing-sensitive crash-matrix lead set may be using this machine. Run no cargo, no tests and no crash-matrix binary or checker.
- **Scripts.** If you run anything, use only the evidence script below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **`verify_design` is not needed.** The lead did not run the real `tools/verify_design.py`. If you run it, do so at `nice -n 19` against a scratch copy of the lock passed with `--lock`, never editing the product.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**

## Subject

The pins are in `hashes.txt`. Every file is untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/native-successors-fa/fa-2-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 11 members**, under `native-successors-fa/fa-2/`:
  - `successor.json`, the record;
  - `README.md`, the design: lead decisions LD-F1 to LD-F9, the candidates evaluated, findings F-1 to F-3, and the cascade;
  - `section-9-8.md`, the exact NE §9.8 text that the NE:3313 override appends;
  - the two handshake successor copies, `design/native/provider-handshake.schemas.v1.json` and `product/schemas/sources/handshake-v1.schema.json`, which are identical;
  - the new census schema, `design/native/symbol-census.schemas.v1.json`, and its identical product copy `product/schemas/sources/symbol-census-v1.schema.json`;
  - `materialization-map.json`;
  - `evidence/build_fa2.py`, `evidence/copies-report.json` and `evidence/vectors.json`.
- **Not part of the subject:** `native-successors-fa/fa-2-unit.json`, the lead's DRAFT-PENDING-REVIEW record.

**Parents** (all accepted lock inputs, at their pinned bytes):
- NE, `docs/v2/contracts/product-v1/native-evidence.md`: 13 line overrides;
- `docs/coop/design-corrections/native/provider-startup.schemas.v1.json` and its selected product copy `docs/implementation/m1/source-selection-v2/schemas/sources/startup.v1.schema.json`: 3 JSON Pointer overrides each;
- `docs/coop/design-corrections/native/provider-handshake.schemas.v1.json` and `.../source-selection-v2/schemas/sources/handshake.v1.schema.json`: complete successor copies.

**Product.** `/Users/sb/code/opensip-ai/opensip`, read-only. The assigned base is main `e093e90` (77 contract successors). Main is now `15c0779` (81 successors: I1-L, B-S1, B-S2, B-S9, then X4-F1). B-S1 binds eleven NE line overrides (NE:714, 719, 730, 731, 822, 824, 863, 931, 939, 940 and 4135), all disjoint from FA-2's. No bound unit overrides HS, PHS, ST or PST. FA-2 changes no product byte. D2b will copy the two product schema sources later (`materialization-map.json`).

**Context, not subject:**
- **M3-H r1** (`fact-admission-h/PROPOSAL-r1.md`, `69f50bb1…`): item 17 and X-H1 (H1:490-519, H1:724-732) state the obligation, and its FA-2 row (H1:684) is the lead's first recommendation, which FA-2 refines. H r1 was reviewed by Grok (REQUIRED-FINDINGS on an unrelated item). Its r2 is being drafted in the live file and is not cited.
- **M3-L r3** (`provider-protocol-l/PROPOSAL.md`), in review with Grok at the same time. Its item 22 joins FA-2, and its G10 makes FA-2's acceptance a condition of L taking effect. You are not reviewing L.
- **M3-I1 r2** and **I1-L** (accepted). The cycle atom needs symbol inventories and symbol scopes (MI:113, MI:155-165).

## What FA-2 does

The README has the full tables. In brief:

1. **The carrier (LD-F1).**
   - A new optional, non-identity capability token, `symbol-census-v1`.
   - Under it, **one member, `symbolCensus`, is added to the existing `Analyze` and `Complete` payloads** of TS2 and Rust3: `TypeScriptAnalyzeV2`/`TypeScriptCompleteV2` and `AnalyzeV3`/`CompleteV3`.
   - On Analyze it is the census request, `{enumeratorClosure}`. On `Complete` it is the census, either `complete` `{examinedPaths, rows}` or `over-bound` `{rowCount, examinedPathCount}`.
   - No other terminal carries a census.
   - The pattern is `target-attribution-v2` / `FactBatchV3` (NE:2797-2814, NE:3061-3069; EXC:270-272).
2. **The ordering problem (LD-F2).**
   - Before spawn, every `symbol`-kind key commits to the census **rule**: the §4.1a commitment of its descriptor with `subjects: []` (D∅).
   - On return, each `symbol`-kind Coverage entry commits to the census **values**: the same descriptor with the census's `nativeSubjectId`s, in canonical-set order.
   - The host runs §4.1a unchanged, with a symbol scope's `D` built from the admitted census.
   - Only NE:3279's request equality gains an exception, for symbol keys under the token. Terminal entries, the pre-Analyze conversion and an empty census all carry D∅ unchanged.
3. **Host projection (LD-F3).** At clean settlement only, the host projects the census into one `SubjectInventoryV1` per owed locator. It fills the locator, `kind`, the state carrier, `subjectLanguage` and `projections: []`. The records are host-derived typed inputs under EXC §§6-7, and owner admission is H's (item 17).
4. **Bounds and states (LD-F4, LD-F5).** There is no partial census on the wire. An `over-bound` census is never truncated; it takes the subject-scope scope-limit route (H's X-H6).
5. **The Plan need (LD-F6).** A census is owed where an expected symbol inventory binds the worker's universe. The enumerator is the worker's provider closure, and the token becomes "a token the Plan needs".
6. **F-1 and LD-F7.** NE §0 never superseded the inherited request-key commitment rules: DLV `keyConstruction` and `workerRule`, and RPP `coverageDomainAlgorithm[3]`. They conflict with §4.1a for **every** key. §0 row C supersedes them for the key commitment only, keeping the inherited file-set proofs.
7. **Form (LD-F8).**
   - 13 insert-only NE line overrides, one of which appends §9.8.
   - 3 + 3 pointer overrides on the startup copies.
   - Complete copies of the handshake schema: the token appended last to both enums, `maxItems` +1, a `supersedes` entry for the registered `CapabilityToken`, and a `symbolCensus` wire-law entry.
   - A new census schema whose inherited stage-request arrays are named by selector, not restated.
8. **Majors.** No frame, phase, terminal kind, transition row, limit member, identity token or version, or major changes.

## Decide

1. **Lawfulness of the carrier.** Is a negotiated member on `Analyze` and `Complete` lawful within TS2 and Rust3's current majors, by the `target-attribution-v2` precedent, under F02:271-273 and EXC:270? Is `Complete` the right frame (LD-F1)? Rule on each rejected candidate in the README's table, and on any carrier the lead missed.
2. **The two-phase key (LD-F2).**
   - Is D∅ then D_census lawful against NE §4.1a (steps 1-6, "Join with scope2", "No circularity") and IE §3?
   - Is NE:3279's symbol-key exception the minimal change?
   - Do terminal, pre-Analyze and empty-census entries really need no exception?
   - Check `vectors.json`, including the canonical-set versus row-order pair.
3. **Projection and admission (LD-F3).** Do the host-filled fields and the wire row together make exactly a valid SIS symbol inventory? Is `projections: []` lawful at M3? Is the EXC §§6-7 ownership right?
4. **LD-F4 to LD-F6.** Rule on: no partial census; the over-bound variant and its byte bound; the Plan-need rule; and requiring the enumerator to be the worker's closure, given NE:3054-3059's "not blanket-identical".
5. **F-1 and LD-F7.** Is the conflict real on the cited bytes? Is §0 row C's scope (every key; key commitment only; file-set proofs retained) right?
6. **Exactness.** Is every `before` the exact parent line or pointer value? Is every `after` insert-only, true and minimal? Is each copy exactly its parent plus the stated edits (`copies-report.json`)? Is the census schema well-formed and consistent with §9.8 and SIS?
7. **Consequential passages.** Does any other accepted passage still say the census has no carrier, or state the inherited key rule, the closed token list, or the Analyze and Complete payloads, without FA-2's change? Look at NE, the startup and handshake schemas' other strings, `fact-batch.schema.v3.json`, `native-cases.v2.json` and the reference models.
8. **Selection.** Is the successor well formed for selection under `verify_design`'s `contract_successor` and `successor_chain` rules, at `e093e90` and at `15c0779`? Is anything else wrong?

## Running the evidence (optional)

Use `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`.

1. **Dependencies.** The schema validation imports `jsonschema` through the design encoder. Install it offline into your review directory: `python3.14 -m pip install --no-index --no-cache-dir --find-links ~/opensip-deps/wheels --target /tmp/opensip-implementation/reviews/codex-fa-2-r1/deps jsonschema==4.25.1`.
2. **Build check.** Run `docs/implementation/m3/native-successors-fa/fa-2/evidence/build_fa2.py --product /Users/sb/code/opensip-ai/opensip --deps <that dir> --check`. It:
   - rebuilds every generated file in memory and compares it with the files on disk;
   - checks the lock at `e093e90` and `15c0779` (add `--lock-commit <sha>` for a later main);
   - checks the encoder against NE's scope2 oracle case;
   - runs 14 schema cases.

   It reads the lock and one base blob with `git show`, read-only. Leave out `--deps` to skip the schema cases.

The lead ran it twice with `--check`, with identical results.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `fa-2-subject.json`. The lead's value is in `hashes.txt`;
- `"successor"`: `{path, bytes, sha256}` of `fa-2/successor.json`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change bytes, give the exact replacement text. Do not commit.
