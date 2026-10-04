# B-S2 r1 — Codex review

**Verdict: ACCEPT-DESIGN-UNIT.** No required findings. One non-blocking observation records the future materialization bindings. No replacement design passage is requested.

The accepted subject is `docs/implementation/m3/config-discovery-b/b-s2-subject.json`, 1,469 bytes, SHA-256 `9c17e1f674f64135111c3923a6dce7e847b75749a51af2416c4bd50bb5558d0a`. Its successor is `docs/implementation/m3/config-discovery-b/b-s2/successor.json`, 4,600 bytes, SHA-256 `1f089c83f8c80751145dde78623e79c8298bb2ac094e576f52b1791cc61467ad`. Acceptance applies to those exact bytes and their manifest members.

## Decisions

| Question | Decision and grounds |
|---|---|
| R1: same record name and selector | Accept. `#/$defs/vcs-observation` remains the selected record, now an exclusive union. `vcs-observation-v2` equals both accepted IDS definitions, including the `sourceInventoryDigest` annotation. No snapshot selector change is needed. |
| R2: fixed top level, commit width, member bounds and order | Accept. M3-B item 19's W2 establishes `NoRepository` at the workspace root; pinned M3-C item 4 establishes `none/null/false`. X2 r9 rejects `extensions.*` and nonzero repository format versions, so member HEAD names are SHA-1, exactly 40 lowercase hex digits. Members are closed Git rows, 1–64, with relative `LogicalPath` roots in strictly increasing UTF-8 path order. |
| R3: no schema-3 VCS-revision correspondence | Accept. The workspace top level names no commit. `import_joins.rs` already requires a non-`none` kind before a VCS revision can be consumed. It cannot silently choose a member. Per-member correspondence remains BS2-F1's separate M5 successor. Exact-snapshot correspondence remains available under its existing rules. |
| R4: IE allocation with VCS-1 | Accept. Only IE:542 and the blank IE:547 are overridden; IE:543–546 remain unchanged. A VCS-1 override of IE:542 must explicitly supersede B-S2's selected text as LD-7 says. There is no currently bound overlap. |

## Faithfulness and closure

The new paragraph and schema implement M3-B r2 item 22's per-member observation and pinned M3-C r6 item 4's root/member split. The version choice is explicit: at least one admitted member produces schema 3; no admitted member produces schema 2, including a workspace whose candidates were all excluded. This choice and the admitted membership remain host observations, consistent with IE's existing custody-walk limitation and NE:813–815's unretained security boundary inventory. The schema does not claim to reconstruct security admission from retained bytes.

Schema 2's structural equality establishes preservation of its complete admission constraints and annotations, beyond the two sample vectors. Its record values and canonical recipe are unchanged, so B-S2 introduces no new single-root snapshot bytes. Actual producer regression qualification remains C1b's obligation, including nested repositories and the all-candidates-excluded case.

Both observation branches and each member row use `additionalProperties: false` and complete required-field lists. Version constants 2 and 3 distinguish the branches; members are required only on schema 3, with a nonempty upper-bounded array. Strict `x-opensip-order: path` also refuses duplicate paths even when other member fields differ. `LogicalPath` bounds and the exact-end 40-hex pattern bound member strings. All local references resolve, and the digest annotation still names the whole source inventory.

The named product consumers remain compatible after C1b materializes the schema:

- `crates/evaluator/src/run_links.rs:364–373` reads the same record and inventory digest. The fixed schema-3 top level satisfies `VCS_KIND_JOIN` (`none` exactly when `commitId` is null), and `VCS_INVENTORY_JOIN` still compares the whole inventory.
- `crates/evaluator/src/import_joins.rs:205` and its `IMPORT_VCS_JOIN` consume the same top-level fields; schema 3 fails the VCS-revision join closed.
- `tools/contracts/options.json:758` continues to select the same definition for generation. No use of the concrete generated `Identity3VcsObservation` type was found outside its generated declaration.
- `crates/identity/src/closure.rs:839–862` already selects a unique `oneOf` branch before walking its annotated fields. Its canonical-record traversal follows the retained inventory digest through either branch. The product's array-order implementation and selected Rust/TypeScript pattern vocabularies already support the fragment's ordering and 40-hex pattern.

C1b still owns actual HEAD/ref reads, read custody and rechecks, unborn-HEAD refusal, and M3-C's `dirty: true` for every Git observation. A Boolean member `dirty` field does not supply proof of cleanliness or waive that producer rule. No read, repository admission or source correspondence is added by accepting this shape.

## Reconciliations and ordering

No conflicting rule was found in M3-B r2, pinned M3-C r6, X2 r9, X12 r4 or B-S1. X2 item 1 leaves additional Git objects to C1's observation law; B-S2 introduces no read. X12's configuration and pack-admission ordering is unaffected. B-S1's identity override is IE:552, separate from B-S2's anchors. `sourceInventoryDigest` remains one top-level digest covering members' files as part of the same snapshot inventory.

The I1-L ordering note is correct as a composition rule. Its complete foundation copy changes `closure`, `proof-bundle`, `program-predicate` and `stage-spec`; its product copy changes the last three. Both preserve `vcs-observation`, and neither defines B-S2's three new names. Thus applying B-S2's fragment to either I1-L copy preserves the schema-2 equality and I1-L's changes. A later implementation must preserve both transformations rather than replace the composed schema with an earlier frozen full copy; the required source bindings are noted below.

The successor is well formed for selection: the parent and both `before` strings match, the six candidates equal the manifest members excluding the record, and the two selectors do not overlap bound successors. Its proposed standing and the lead's `DRAFT-PENDING-REVIEW` assent were not treated as prior acceptance. This review supplies independent design judgment; root assent and product binding remain separate steps.

## Non-blocking observation

**BS2-NBO-01 — complete materialization bindings (C1b and I1-a).** README BS2-F2 and BS2-F3 name the schema merge, regeneration and ordering. When implementing them, select and pin the complete composed architecture schema and the complete updated admission registry. Re-point `schemas/source-map.json` and `schemas/admission-source-map.json`, update `schemas/registry.json`, `schemas/admission-registry.json` and applicable generator-closure input pins, and regenerate the product outputs. `tools/verify_design.py:455–574` requires equality to accepted complete architecture inputs; the fragment is not itself a complete source document. Whichever implementation lands second must retain both B-S2 and I1-L changes. These are future product-materialization obligations, and do not require changing this frozen design unit.

## Verification and limits

All 20 supplied pins matched. Accepted M3-C r6 was read from arch commit `3590205a9` with its acceptance note: 155,209 bytes, SHA-256 `a2f16b7bcf401f3c13f90915b0d48514cfaa7ab91f83decd3434e656bde8bab6`. The live r7 draft was not used.

The three permitted evidence scripts were run with pinned Python 3.14.6, `-I -B`, `nice -n 19`, private HOME and private 0700 TMPDIR under this review directory:

- `build_b_s2.py` ran twice on copied inputs under `arch-scratch`. The resulting manifest and every subject member match the original pinned bytes; both runs report the same manifest hash. See `build-first.json`, `build-second.json` and `rebuild-comparison.txt`.
- `check_b_s2.py` passed schema-2 equality, reference closure, both schema-2 samples, the schema-3 sample and all 13 negative vectors. The three canonical SHA-256 vectors match the README. See `check.json`.
- `verify_scratch.py --rev e093e90` passed design-only selection: 77 → 78 contract successors, two B-S2 overrides, six candidates, unchanged selected inventory and inheritance. See `verify-e093e90.json`.
- The current clean product checkout had advanced to `0ceb9ad96946e9427c5f2fd54d6d4cd5df9e9cac`, the I1-L binding; the difference from `e093e90` is `design-lock.json` only. `verify_scratch.py` also passed there: 78 → 79 successors and 40 generation sources verified, with inventory and inheritance unchanged. See `verify-current.json`. `ordering-context.json` records the schema-definition comparison and B-S1's separate IE anchor.

The scratch selection script uses its declared synthetic review and assent only to exercise selection. They are not independent acceptance or real root assent. These checks establish design consistency and binding form, not production schema admission, real snapshot regression results or C1b qualification.

No cargo, build, product test, crash-matrix run or checker, private 413 fixture, real OpenSIP home access, repository edit, commit, push or delegation occurred. All written artifacts are under the requested review directory.
