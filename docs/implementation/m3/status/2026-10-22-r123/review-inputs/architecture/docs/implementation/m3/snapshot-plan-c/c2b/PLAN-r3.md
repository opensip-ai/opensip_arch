# C2b-0 implementation plan r3: the `node_modules` layout (M3-C r8 items 3 and 10; NE §2.4)

**Lead plan, 2026-10-17. Proposed; it needs Codex review.** Round 3 answers Codex `codex-c2b0-plan-r2` (REQUIRED-FINDINGS: RF-1, NBO-1 to NBO-3, rulings on Q6 and Q7). Round 2 answered `codex-c2b0-plan-r1`. r1 and r2 are history, and their changes tables below are kept as history, superseded where r3 says so. The prior gating record is `C2B-GATING-r1.md`, which finds that the layout needs no manifest-admitted closure, while C2b's context half, C2b-1, waits for C2a. **This plan proposes one narrow amendment, A-C2B0-1, for acceptance with it** (LD-C2B0-11).

## r3 changes

| Finding | Change | Where |
| --- | --- | --- |
| **R2-RF-1** (no layout-only check) | The context-independent `realPath`/`installPath` membership check, now inline in `inspect_typescript_universe` (`native_universe.rs`:235-252), is **factored into one bounded shared evaluator helper**, `layout_real_path_faults`, and exported from `opensip-evaluator`. The existing consumer calls it, with its refusal strings and their set semantics unchanged, and so does C2b-0, after the layout's schema and order admission. C2b-0's scope gains the helper, its export, and regression controls that pin the consumer's existing refusals byte for byte. The retained-context, digest and Plan-selection checks stay with C2b-1 and later composition. No native identity is fabricated, and no second layout predicate exists. **Census:** no census or model tool pins an `opensip-evaluator` file (`tools/security/discovery_census.py`, `snapshot_ledger_model.py` and `snapshot_ledger_census.py` name none), so the helper adds no receipt delta. If the companion snapshot receipt, which C1a4's refresh unit defines, binds an evaluator file, C2b-0's lane names that delta under LD-C2B0-7. | LD-C2B0-9 (rewritten); LD-C2B0-14; §4; §5; §6 |
| **R2-NBO-1** (26,715 is a ceiling) | 26,715 is stated as a **conservative ceiling**, derived from each row's minimum encoded size. It is not attainable: distinct `installPath`s cannot all be one byte, and installed paths carry structural prefixes. The arithmetic is restated in **encoded string payload bytes**, escapes and UTF-8 included. The whole-record boundary controls use real, unique, schema-valid layouts. | LD-C2B0-8; §4 |
| **R2-NBO-2** (parser variants) | One case for each of the nine parser variants, adding `InvalidUnicode` (an unpaired escaped surrogate) and `InvalidJson` (a structural syntax error). A valid general-JSON float keeps `FloatForbidden` and is never described as malformed. | §4 |
| **R2-NBO-3** (C1-T24's replacement observations) | Each replacement observation is explicit. **First-party target:** before the layout reuses the walk's capture of `packages/x/package.json`, it makes a charged `fstatat(AT_SYMLINK_NOFOLLOW)` through the held enumerating parent from `reach_directory`, and compares the complete stored observation (device, inode, size, mtime, ctime). A difference refuses `Changed`, with no second source read. **Pruned manifest:** the layout's own repeated meetings (alias reuse) make the same charged observation. The rewrite between layout capture and read-set reach is C1c-1's observation (LD-C1C-6), and C2b-0's lane carries its control once C1c-1's reach is present. Cached-byte reuse and directory metadata never stand in for the file observation. | LD-C2B0-5; LD-C2B0-11; LD-C2B0-13; §4 |
| **Q6 and Q7 rulings** | **Q6:** the after-walk order is lawful with A-C2B0-1 and the observation duties above. B2's own before-walk control is unchanged, and an exclusion never turns a leftover into an authorized row. **Q7:** a session-owned parse handoff. It stays internal and bounded, parsing and allocation are charged first, the capture is unchanged on a parser failure, aliases may reuse parsed results under the ledger, and no raw-path parser or unbounded copy exists. | LD-C2B0-5; LD-C2B0-11; §7 |

## r2 changes (round 2, answering `codex-c2b0-plan-r1`)

| Finding | Change | Where |
| --- | --- | --- |
| **RF-1** (pnpm siblings unreachable) | The search directories are now **Node's own `NODE_MODULES_PATHS`** of each resolved package's `realPath`, restricted to the project: for each directory on the path from `realPath` up to the project root whose last segment is not `node_modules`, that directory's `node_modules` child. So for pnpm's `node_modules/.pnpm/foo@1/node_modules/foo`, the virtual-store parent `node_modules/.pnpm/foo@1/node_modules`, which holds foo's sibling dependencies, is searched, and so is `node_modules/.pnpm/node_modules`. The `.pnpm` store is never listed wholesale. `installPath` and `realPath` rows stay distinct. New fixtures assert the exact visited-directory set: a pnpm sibling reachable only through its virtual-store parent, scoped siblings, and an ancestor lookup from a workspace target. | LD-C2B0-1; LD-C2B0-3; §4 |
| **RF-2** (no visited or merge rule) | A **charged worklist and two visited sets**: search directories, keyed by normalized project-relative path, and real directories, keyed by `realPath`. Rows go in a **map keyed by `installPath`**. Each search directory and each real directory is enumerated **once**. A row met again is reused if its observation is identical, and refuses `Inconsistent` if not. Alias rows (two `installPath`s to one `realPath`) are all kept. A **filesystem symlink chain** (a link through a link, or an intermediate symlink component) refuses `Link`. A **dependency cycle** (A's search reaching B, whose search reaches A, through links to real directories) is allowed and terminates by the visited sets. New controls cover shared targets, repeated discovery, a diamond and an A→B→A cycle, each with exact rows and finite work. | LD-C2B0-4; LD-C2B0-13 (new); §4; §5 |
| **RF-3** (exclusions versus read-set eligibility) | **C2b-0 owns the two interfaces it needs**, built on C1c-0's opener and the shared rule, so the C1c plan (in review at r4) is not reopened:<br>- **a safe no-follow directory reach**, `reach_directory`;<br>- **a non-dependency exclusion check**, `excluded_path`, in `discovery_rule.rs`, which classifies a path's VCS, Cargo-output and exact custody-anchor exclusions **without** the read-set eligibility rule that `read_set_path` adds.<br>First-party workspace targets keep the ordinary opener, S3 custody and Walk-origin capture reuse. Every target keeps the boundary, `ignorePaths`, VCS, Cargo-output and custody-anchor exclusions. **The layout now runs after the session's walk**, so it takes C1c-0's `WalkEvidence`, the walk's own Cargo and member roots (LD-C1C-13), and the walk's captures of first-party manifests. That order is part of A-C2B0-1. `excluded_path` is a discovery-closure change, accounted for under RF-4. | LD-C2B0-6 (rewritten); LD-C2B0-11; LD-C2B0-14 (new); §4 |
| **RF-4** (interval ownership) | C2b-0 **joins an existing reviewed interval only before its final-input freeze**. Otherwise it **opens and owns a new interval**: a fresh accepted baseline, receipt-specific deltas, a pre-run review, a frozen-input mechanical blind refresh and a post-run review, all before anything relies on the receipts. Cumulative changes are tracked: an empty delta added to an already-stale receipt does not make it current. The cross-reference is updated to C1c plan r4's LD-C1C-9. | LD-C2B0-7 (rewritten) |
| **NBO-1** (the JSON profile) | The manifest parser is named exactly: the identity crate's `canonical::parse` (`canonical.rs`:61). It rejects floats, negative zero, integers outside −2^63 to 2^64−1, duplicate keys, depth beyond 32, invalid UTF-8 or Unicode, and more than 4 MiB (`canonical.rs`:5-8, :40-50). An unsupported manifest refuses `LayoutRefusal::Manifest(profile-error)` with the parser's own variant, never as "malformed JSON". Q3's ruling is applied in those terms. | LD-C2B0-5; §4 |
| **NBO-2** (the count versus record admission) | The row-count check (at most 100,000, the schema) is tested on its own. **The canonical encoder's 4 MiB limit** (`canonical.rs`:278-283) bounds the whole record. The largest admitting layout has **at most 26,715 rows**, reached only with one-character paths, names and versions; a realistic layout has far fewer. A larger record refuses `LayoutRefusal::Encoding`. The model covers record construction, sorting, admission, retention and the encoding buffers. | LD-C2B0-8; LD-C2B0-7; §4 |
| **Q1 to Q5 rulings** | **Q1:** no row for a directory without a regular `package.json`, as an explicit conservative subset. **Q2:** an escaping target refuses `Link`. **Q3:** an unsupported manifest refuses `Manifest`. **Q4:** composition owns the no-layout branch (LD-C2B0-12, new). **Q5:** the snapshot ledger, with the full term and the reconciliation in A-C2B0-1 (LD-C2B0-11). | LD-C2B0-2; LD-C2B0-4; LD-C2B0-5; LD-C2B0-11; LD-C2B0-12 |
| **Other conclusions** | The present-but-empty case gets an explicit policy (LD-C2B0-10). Manifest content comes only from the session's captured bytes, through a session-owned parse handoff (LD-C2B0-5). | LD-C2B0-5; LD-C2B0-10 |

**Bases:**
- product main `b753854`, as the subject manifest names: the v221 lock `3d1d771` plus D2b-0b's generation and its contract-175 lock, which touch none of the files this plan cites. C1a1 to C1a4 are integrated;
- the current architecture head;
- the C1c plan r4 in review (`c1c/PLAN-r4.md`). C2b-0 depends on C1c-0 as r4 defines it (`capture_pruned`, the pruned opener, `read_set_path`, `WalkEvidence`), and is revised if that review changes them.

**Authority:**
- **The law:** M3-C r8:
  - item 3 (`PROPOSAL.md`:302-321), with step 1 (:305) and the no-layout bullet (:311);
  - item 1's capture session (:207-226), including C1-T24 (:230);
  - item 2 (:271-279);
  - item 6's exclusions (:377-393);
  - item 10's TypeScript list (:564-571);
  - the Units table (:1182, :1184);
  - the r9 law record (`c1a-r9/RECORD-r9.md`).
- **The contracts:**
  - NE's `ResolvedNodeModulesLayoutV1` (`docs/v2/contracts/product-v1/native-evidence.md`:1399-1419) and its digest (NE:1490);
  - the schema (`opensip/schemas/sources/native-v2.schema.json`:6971-7016: `entries` at most 100,000; `packageName` and `packageVersion` 1 to 256 characters; `CanonicalPath` at most 4,096, :981-985);
  - IE:548-593 and SL:266-279.
- **Node's module resolution:** the published `NODE_MODULES_PATHS(START)` of the Node.js "Modules: CommonJS modules" documentation ("All together"). Its directory list, not its file-extension probing, is the search order this plan reproduces. It is cited as the source of the traversal, as Git's `check-ref-format` is cited in the C1b plan.
- **The reference consumer side:** `native_evidence_model.v2.py`:2811-2813 and :2925-2943. No reference function derives a layout, so the vectors are lead-authored.
- **Admission:** the evaluator's `inspect_typescript_universe` (`opensip/crates/evaluator/src/native_universe.rs`:142, :235-252).
- **Accepted and in-review records:** the C1a plan r6 (`c1a/PLAN-r6.md`:119, :194); the C1b plan r3 (LD-C1B-7, the census interval rules); the C1c plan r4 (LD-C1C-2, LD-C1C-5, LD-C1C-9, LD-C1C-12, LD-C1C-13).

## 1. What C2b-0 delivers

- **`resolve_node_modules_layout`**, in a new host module, `crates/host/src/node_modules_layout.rs`. Given:
  - the snapshot root and the capture session, after its walk, with that walk's `WalkEvidence`;
  - a TypeScript unit's root directory;
  - the walk's `SnapshotExtent`;
  - the caller's work scope,

  it returns either `None` (no layout), or an admitted `ResolvedNodeModulesLayoutV1` with its raw digest, or a typed refusal together with the captures it made (LD-C2B0-12).
- **Two security interfaces** (LD-C2B0-14):
  - `reach_directory`, in `crates/security/src/snapshot_read_set.rs`, beside C1c-0's opener;
  - `excluded_path`, in `custody/discovery_rule.rs`, beside `classify_path` and `read_set_path`.

It is library only, with no production caller. **C2b-0 on its own satisfies the law's C1c edge** "C1a; C2b's layout" (`PROPOSAL.md`:1182), so C1c-1 integrates after C2b-0 and is not held behind C2a.

## 2. Order and dependencies

| Unit | Depends on | Unblocks |
| --- | --- | --- |
| **C2b-0** | C1a (integrated); **C1c-0**: `capture_pruned`, the pruned opener, `WalkEvidence` (LD-C1C-2, LD-C1C-13) | C1c-1's integration (`PROPOSAL.md`:1182) |
| C2b-1 (not this plan) | C2a, C2b-0 | the TypeScript context and `bind_typescript_universe` |

C2b-0 may be **authored** now against C1c-0's r4 interface. It **integrates** after C1c-0. Within a request the order is: the session's walk, then C2b-0's layout, then C1c-1's read set, then sealing (A-C2B0-1).

## 3. Lead decisions

- **LD-C2B0-1. Where the resolver looks (r2, RF-1).**
  - **The search directories** of a starting directory `S` are Node's `NODE_MODULES_PATHS(S)`, restricted to the project:
    - for each directory `I` from `S` up to and including the project root, in that order, where `I`'s last segment is not `node_modules`, the candidate is `I/node_modules`;
    - a candidate is searched only if it exists as a directory, is reached by `reach_directory` (LD-C2B0-14), and is not excluded (LD-C2B0-6);
    - nothing above the project root is ever a candidate (IE:548-593).
  - **The seeds** are the unit root's search directories.
  - **Each row's `realPath`** contributes its own search directories when that real directory is first reached (LD-C2B0-13).
    - For an npm package at `node_modules/a`, that adds `node_modules/a/node_modules`, which holds its nested installs.
    - For a pnpm package at `node_modules/.pnpm/foo@1/node_modules/foo`, it adds `.../foo/node_modules`, then the virtual-store parent `node_modules/.pnpm/foo@1/node_modules`, which holds its siblings, then `node_modules/.pnpm/node_modules`, then the root's `node_modules`.
  - **The `.pnpm` store is never listed wholesale.** Its directories are searched only when a resolved `realPath` below them names them in its own path list.
- **LD-C2B0-2. Which entries are package directories.**
  - **Recognized:** in a search directory, a child `name`, or a child `@scope/name` of a scoped directory `@scope`.
  - **Not listed:** an entry beginning with `.`, such as `.bin`, `.cache` or `.pnpm`.
  - **A candidate row:** a recognized entry that is a directory, or a link resolving to one (LD-C2B0-4), and that holds a **regular** `package.json`.
  - **No row (Q1 ruling):** a recognized directory with no regular `package.json`. This is an explicit conservative subset: no manifest bytes are invented, and a provider read there stays outside the committed read set. A `package.json` that is a symlink, FIFO, socket or device is never opened as a manifest and is not a row.
- **LD-C2B0-3. Nesting.**
  - Each nested installed package is its own row. The enclosing row never stands for it (IE:572-577; C1-T12).
  - Nested directories are reached only through LD-C2B0-1's search directories, iteratively.
  - Depth is bounded only by `CanonicalPath`'s 4,096 characters (:981-985), and by the ledger.
- **LD-C2B0-4. Links are observed, never followed** (`PROPOSAL.md`:305; Q2 ruling).
  - A recognized entry that is a symlink is read with `readlinkat` on the held parent descriptor.
  - Its text is resolved **lexically** against the link's directory into a normalized project-relative `CanonicalPath`. That is `realPath`.
  - **Refused as `Link`:**
    - a target above the project root, absolute outside it, or containing NUL;
    - a target whose resolved path has a symlink as any intermediate or final component, which is a **filesystem symlink chain**.
  - The target is reached from the retained root by `reach_directory`, never through the link.
  - **`realPath` is itself an `installPath` of the layout** (NE:1405-1406; `native_evidence_model.v2.py`:2940-2943), so a reached real directory is also a row.
  - Rows for `installPath` and for `realPath` are distinct: `node_modules/foo` (a link) and `node_modules/.pnpm/foo@1/node_modules/foo` (real) are two rows, and the link row's `realPath` is the second row's `installPath`.
- **LD-C2B0-5. The manifest: one capture, parsed from the captured bytes (NBO-1; Q3 ruling).**
  - Each candidate's `package.json` is obtained **once** through the session, by whichever capture applies:
    - below a pruned anchor, `CaptureSession::capture_pruned` (C1c-0);
    - for a first-party target, the session's existing capture from the walk (origin `Walk`), reused **after a charged `fstatat(AT_SYMLINK_NOFOLLOW)` through the held enumerating parent, comparing the complete stored observation (r3, R2-NBO-3)**. A difference refuses `Changed`, with no second source read. Since C2b-0 runs after the walk (A-C2B0-1), the walk has captured every first-party file in its extent. A first-party target outside the walk's extent is excluded (LD-C2B0-6).
  - Content comes **only** from the capture's retained bytes, through a session-owned handoff, `CaptureSession::parse_captured`. It reads custody bytes and never reopens the project file (item 1, "One set of bytes", :218).
  - **The parser** is the identity crate's `canonical::parse` (`canonical.rs`:61). It is the product JSON profile, and it rejects:
    - floating-point numbers (`FloatForbidden`), negative zero (`NegativeZero`), and integers outside −2^63 to 2^64−1 (`IntegerRange`, `:7-8`);
    - duplicate keys (`DuplicateKey`), and depth beyond 32 (`DepthLimit`, `:6`);
    - invalid UTF-8 or Unicode, and more than 4 MiB (`ByteLimit`, `:5`).
    These apply to every field, including fields unrelated to `name` and `version`.
  - A manifest the profile rejects refuses `LayoutRefusal::Manifest(Profile(<variant>))`, naming the parser's variant. Such a manifest may be valid general JSON (a `1.5` value elsewhere), so the refusal is never labelled malformed JSON. This is a stated supported subset: supporting ordinary JSON with such values would need a separately selected bounded projection, which this plan does not choose.
  - `packageName` and `packageVersion` are the `name` and `version` strings. Anything else refuses `Manifest(Field)`: missing, non-string, empty, or over 256 characters.
  - `contentSha256` is the capture's raw SHA-256 (NE:1407-1408).
  - The 4 MiB bound is the reader's own and is reused as such. It imposes no config-file custody on installed trees (LD-C1C-2).
- **LD-C2B0-6. Exclusions first (r2, RF-3; LD-C1C-12).** Before any search directory, entry or target is reached, opened or read:
  - the walk's own `SnapshotExtent` applies: B2's `AdmittedBoundaries` and the validated Config2 `ignorePaths` (`snapshot_walk.rs`:69-90);
  - `excluded_path` (LD-C2B0-14) applies on the **full path**: VCS segments anywhere; a `target` under a Cargo root (the walk's first-party roots from `WalkEvidence`, and dependency-tree roots observed on the way, as LD-C1C-13 observes them); the exact root and member `.opensip` custody anchors.

  An excluded directory is never listed, an excluded target never reached, and an excluded manifest never captured. **First-party workspace targets** (outside every `node_modules` tree) are admitted only if they lie in the walk's extent and pass `excluded_path`. They keep S3 custody and the walk's capture. `read_set_path`'s dependency-tree eligibility is not applied to them, since they are not read-set paths (LD-C1C-3).
- **LD-C2B0-7. Ledger, model and census (r2, RF-4; Q5 ruling).**
  - **The ledger:** the snapshot ledger, the same session's (A-C2B0-1). Every reach, listing, link read, status read, capture, parse, worklist and visited-set insertion, row-map entry, sort, admission, digest and encoding buffer is charged before it is made, with no listing collected whole.
  - **The model:** C2b-0 owns a layout term in `snapshot_ledger_model.py`, with its anchors, its soundness vectors and its derivation. The term covers the reach, the graph state of LD-C2B0-13, the captures and parses, and the record's construction, sorting, admission, retention and encoding. The evidence states the cumulative subtotal on the full ledger (walk, session, sealing, C1b's VCS term and C1c's terms when accepted, and the layout), and shows that r9's fixed caps hold by r9's own 2× rule. If they do not, C2b-0 stops for a law-record revision; it never raises a cap. A capture is charged once, and a reused capture adds no charge.
  - **Census (receipt-specific, as C1c plan r4's LD-C1C-9):**
    - **the discovery receipt's bindings change**, because `excluded_path` changes `discovery_rule.rs`, a CLOSURE file. C2b-0 re-pins it whole and regenerates the discovery census's records;
    - **the companion snapshot receipt's recipe and pins change**, through the model, the vectors and the new module;
    - the generated-output `--check` commands pass after regeneration. Each lane names each receipt's exact changed bindings from public fields only. Malformed receipts, bad pins, missing artifacts and output differences stay failures, and nothing relies on a stale receipt.
  - **The interval (RF-4):**
    - C2b-0 **joins an existing reviewed interval only if it integrates before that interval's final-input freeze**, which its pre-run review sets. The interval's one refresh then covers C2b-0's bindings as well.
    - **Otherwise C2b-0 opens and owns a new interval** at its integration. It owns a fresh accepted baseline (whichever refresh last made each receipt current), its exact receipt-specific deltas, a pre-run review that freezes the inputs and the blind mode, the frozen-input mechanical blind refresh, and a post-run review. All of this completes before any dependent work relies on either receipt.
    - **Cumulative tracking:** when C2b-0 joins an interval that is already stale, its deltas are added to the interval's. An empty additional delta for a receipt does not make an already-stale receipt current.
    - **An earlier refresh never covers C2b-0's later recipe** (LD-C1C-9).
- **LD-C2B0-8. Refusals and the two bounds (r2, NBO-2).**
  - `LayoutRefusal {Link, Manifest(Field | Profile(variant)), Inconsistent, Changed, Membership, Bound, Encoding, Custody, Io}`. `Changed` and `Membership` are r3's (R2-NBO-3, R2-RF-1). Work exhaustion stays the ledger's `Budget` failure. The public projection is J2's (as LD-C1B-8 and LD-C1C-11).
  - **The row count:** more than 100,000 rows (the schema's `maxItems`) refuses `Bound`. It is tested at 100,000 and at 100,001 on its own, as a predicate over the row map.
  - **The record:** the canonical encoding of the whole layout must fit the encoder's 4 MiB (`canonical.rs`:278-283), or it refuses `Encoding`.
    - A row's encoding is 152 bytes plus its four strings (`contentSha256`'s 64 hex characters are counted), plus one separator per extra row. The record adds 32.
    - **(r3, R2-NBO-1)** In **encoded string payload bytes** (each string's JSON encoding, escapes and UTF-8 included, without its quotes), a row is 152 + p(installPath) + p(packageName) + p(packageVersion) + p(realPath). N non-empty rows encode in 31 + 157·N bytes at the very least.
    - So **26,715 rows is a conservative ceiling**: N = 26,715 gives 4,194,286 bytes, and N = 26,716 gives 4,194,443, over the limit. It is **not attainable**: distinct `installPath`s cannot all be one byte, and installed paths carry structural prefixes (`node_modules/`), so real layouts admit far fewer.
    - The whole-record controls therefore use real, unique, schema-valid layouts at the encoder's boundary, never the ceiling.
    - The schema's 100,000 is an upper bound, not a promise that a layout fits.
- **LD-C2B0-9. Admission, the digest and agreement.**
  - Rows are sorted by `installPath` bytes and admitted against `$defs/ResolvedNodeModulesLayoutV1` through the embedded registry, as B2-d2's rows are.
  - The digest is the raw SHA-256 of the canonical encoding (NE:1490; `native_evidence_model.v2.py`:2811-2813).
  - **(r3, R2-RF-1) The one shared membership check.** Before returning, C2b-0 calls the evaluator's exported helper `layout_real_path_faults(layout, steps)` on the admitted record (LD-C2B0-14). That helper is the code `inspect_typescript_universe` itself now calls in place of its inline loop (`native_universe.rs`:235-252). A non-empty result refuses `LayoutRefusal::Membership`, a defence in depth that cannot occur by construction (LD-C2B0-4). No context, universe or native identity is constructed. The retained-context, digest and Plan-selection checks are C2b-1's and later composition's.
  - That the layout is a Plan-selected context's own, and that its unit, extent and walk share one root, are **composition preconditions** of C2b-1, C4a and J2 (LD-C1C-1). Evaluator admission is necessary but cannot detect an unenumerated directory, which is why §4 asserts visited sets.
- **LD-C2B0-10. No layout, and an empty one.**
  - **`None`:** no search directory on the unit's chain exists and is eligible. NE makes the digest null exactly when `nodeModulesInReadSet=false` (NE:1490).
  - **`Some(entries: [])`:** at least one eligible search directory exists, but it yields no rows. That is an observed, committed empty installation, not an absence.
  - A wholly excluded search directory counts as not present.
- **LD-C2B0-11. A-C2B0-1, the amendment proposed for acceptance with this plan (Q5 ruling's reconciliation; RF-3).** It changes four accepted statements for **C2's layout reads only**. B2's reads are unchanged.
  - **C1a plan r6:119 and :194.**
    - :119, current: "B2's and C2's pre-walk captures use the discovery ledger (item 1); the walk uses the snapshot ledger." Replacement: "B2's pre-walk captures use the discovery ledger (item 1); the walk, and C2's layout captures after it (C2b-0), use the snapshot ledger."
    - :194, current: "B2's marker and manifest reads and C2's layout reads use it, on the discovery ledger." Replacement: "B2's marker and manifest reads use it, on the discovery ledger; C2's layout reads use the snapshot ledger, after the walk, through `capture_pruned` or the walk's own captures (C2b-0)."
  - **The r9 law record, §3 Q2 (`c1a-r9/RECORD-r9.md`:138, and the outside-r9 list at :195).** Current: "B2's and C2's pre-walk captures are discovery-ledger work" and "C2's layout reads (outside r9)". Replacement: B2's pre-walk captures stay discovery-ledger work. C2's layout reads are snapshot-ledger work, inside r9's caps, priced by C2b-0's layout term and gated by r9's own 2× rule at the unchanged caps (LD-C2B0-7). The caps themselves are unchanged.
  - **The order within a request.** The layout runs after the session's walk and before C1c-1's read set. Item 1 lists C2's layout reads among the session's reads without fixing their position (`PROPOSAL.md`:208-210).
    - C1-T24's layout leg (:230: a `package.json` "captured by … the layout, and rewritten before the walk reaches it") is then discharged at the read set. C1c-1 re-observes each layout-captured manifest through its enumerating parent, and a rewrite refuses `ChangedSinceCapture` (LD-C1C-6).
    - A first-party target's manifest is the walk's own capture, so a rewrite before the layout refuses at the layout's reuse, through the file observation LD-C2B0-5 specifies (r3).
    - This is Q6.
- **LD-C2B0-12. A refused layout's captures (Q4 ruling).**
  - C2b-0 never truncates, never returns a partial layout, and never releases or hides a capture. A refusal or a `Budget` failure is returned **with the exact set of captures it made** (`LayoutCaptures`).
  - The no-layout branch is composition's: item 3's `nodeModulesInReadSet=false` path, H-NM, `PROPOSAL.md`:311, owned by C4a and J2.
  - The composition plan must define how those captures stop being resolved-input dependencies without bypassing the leftover rule. Item 1 refuses a leftover only when "any resolved input depends on such a capture" (:219), while C1a3 treats every pre-walk capture as depended upon (LD-C1A3-1).
  - The session and ledger are never restarted to erase spent work.
- **LD-C2B0-13. The graph's state (r2, RF-2).**
  - **The worklist** holds search directories, in first-discovery order.
  - **`searched`** is the set of search directories enumerated, keyed by normalized project-relative path.
  - **`real_seen`** is the set of real directories whose own search directories have been queued, keyed by `realPath`.
  - **`rows`** is a map from `installPath` to row, holding name, version, `realPath`, the capture's digest and the reached directory's observation.
  - **Enumeration:** each search directory is enumerated exactly once, and each real directory contributes its search directories exactly once.
  - **A repeated row (r3: observed):** each meeting after the first makes a charged file `fstatat(AT_SYMLINK_NOFOLLOW)` of the manifest through the held parent before reuse (R2-NBO-3). A row met again at the same `installPath` (for example a pnpm self entry reached as a real directory and as a link target) is reused if name, version, `realPath`, digest and directory observation are identical. Any difference refuses `Inconsistent`.
  - **Aliases:** two `installPath`s with one `realPath` are both kept.
  - **A dependency cycle** (A's search reaching B, whose search reaches A, through links to real directories) terminates by `searched` and `real_seen`. It is not a refusal. A filesystem symlink chain is refused by LD-C2B0-4.
  - **Cost:** every insertion into the worklist, the sets and the map is charged (LD-C2B0-7). Total work is bounded by the distinct directories and rows, never by revisits.
- **LD-C2B0-14. The three interfaces C2b-0 owns (r2, RF-3; r3, R2-RF-1).**
  - **`reach_directory(root, path, work)`**, in security's `snapshot_read_set.rs`, beside C1c-0's opener. It reaches a directory from the retained root by no-follow opens, component by component.
    - Above a pruned anchor, it judges S3 directory custody, as `SnapshotRoot::open` does (`snapshot_source.rs`:495-584).
    - At and below the anchor, it applies descriptor discipline only (SL:266).
    - It returns a held directory descriptor and its observation. A symlinked component refuses, and an inode swap refuses.
    - It reuses C1c-0's opener's component walk and adds only the final directory open in place of the regular-file open.
  - **`excluded_path(path, evidence) -> Option<Exclusion>`**, in `custody/discovery_rule.rs`, over the rule's private tables (`:22-24`).
    - It reports, for a full project-relative path, a VCS-segment exclusion, a Cargo-output exclusion (a `target` whose parent is a Cargo root in the supplied evidence) or a custody-anchor exclusion (`custody_state` over the retained member roots, as `classify_path` uses it, :173-176).
    - It does not apply `read_set_path`'s rule that a path must lie in a dependency tree. So it can classify a first-party target such as `packages/x` separately.
    - `read_set_path` and `classify_path` are unchanged, and their vectors are re-checked byte for byte.
  - **(r3) `layout_real_path_faults(layout: &JsonValue, steps: usize) -> Result<Vec<String>, NativeUniverseError>`**, in `crates/evaluator/src/native_universe.rs`, exported from the crate root beside `inspect_typescript_universe`.
    - It takes an already admitted `ResolvedNodeModulesLayoutV1` value.
    - It refuses a typed `NativeUniverseError::LayoutBound` if `entries` exceeds `steps`, in the evaluator's step-budget convention (`TraversalBudget`, :305-309).
    - It returns, in ascending order, each fault string `native.universe-retained-input-mismatch:nodeModulesLayout.realPath:<realPath>` for a row whose `realPath` differs from its `installPath` and is not an `installPath` of the layout. These are exactly today's strings (:246-248).
    - **The consumer:** `inspect_typescript_universe` passes its own `work` as `steps` and inserts the returned strings into its refusal set. Its other checks, including `native.universe-retained-input-missing:nodeModulesLayout` (:252), stay in place. Its observable refusals are unchanged.
    - **C2b-0** charges its own `WorkScope` before the call, for the helper's set (one object and the path's bytes per `installPath`) and for its result. It passes the row count as `steps`.

## 4. Controls

The vectors are lead-authored synthetic trees, since no reference derivation exists. Each states its expected rows **and its expected visited sets** (`searched`, `real_seen`).
- **npm, flat and scoped;** **npm, nested** (`node_modules/a/node_modules/b` is its own row; C1-T12).
- **pnpm (RF-1):**
  - a top-level link into `.pnpm/foo@1/node_modules/foo`, with both rows;
  - a sibling `bar` reachable **only** through the virtual-store parent `.pnpm/foo@1/node_modules`;
  - a scoped sibling `@s/baz` there;
  - `node_modules/.pnpm/node_modules` searched;
  - no other `.pnpm` content listed;
  - every `realPath` an `installPath`.
- **A workspace target (RF-1, RF-3):**
  - `node_modules/x` → `packages/x`, reusing the walk's capture with no second read (the C1A-T1 spy);
  - `packages/x`'s own ancestor search directories visited.
- **Forbidden workspace targets (RF-3),** each never opened and never read (an open spy):
  - a target under first-party Cargo output (`crates/c/target/pkg`);
  - one inside `.git`;
  - one at the root `.opensip` custody anchor;
  - one under an `ignorePaths` entry;
  - one under an admitted boundary.
- **The graph (RF-2):**
  - two aliases to one target;
  - the same target discovered from two search directories;
  - a diamond (A and B both depending on C);
  - an A→B→A cycle through links.

  Each has deterministic complete rows, each directory searched once, and finite work with no `Inconsistent`, `Bound` or `Budget` refusal caused by the revisits.
- **An inconsistent repeat:** a row met twice with different observations (an injected change between the two meetings) refuses `Inconsistent`.
- **Links, refused:** a target outside the project root; one through `..` above the root; a link to a link; a link through an intermediate symlink component; a link to a file.
- **Manifests (NBO-1):**
  - a missing `name`, a non-string `version`, and a 257-character `name` refuse `Manifest(Field)`;
  - **(r3, R2-NBO-2)** one profile case per parser variant, all nine (`canonical.rs`:40-50), each refusing `Manifest(Profile(variant))`:
    - `FloatForbidden`: a valid JSON float in an unrelated field, which is never described as malformed;
    - `NegativeZero`: `-0`;
    - `IntegerRange`: `18446744073709551616`;
    - `DuplicateKey`;
    - `DepthLimit`: depth 33;
    - `InvalidUtf8`;
    - `InvalidUnicode`: an unpaired escaped surrogate `"\ud800"`;
    - `InvalidJson`: a structural syntax error, such as a trailing comma or a missing brace;
    - `ByteLimit`: 4 MiB + 1.

    Exactly 4 MiB of otherwise valid manifest admits;
  - a `package.json` that is a symlink or a FIFO is not opened;
  - a directory without `package.json` is not a row (Q1).
- **Descriptor discipline:** an inode swap between status and open refuses; a change during a manifest read refuses.
- **Bounds (NBO-2):** the count predicate admits at 100,000 and refuses `Bound` at 100,001. A whole-record layout at the encoder's boundary admits, and one byte over refuses `Encoding`. The ledger boundaries are tested at exhaustion (`Budget`). The charge equals the recorded calls' price.
- **Agreement (r3, R2-RF-1):**
  - each produced layout passes `layout_real_path_faults` with no fault, and its digest recomputes independently;
  - a constructed layout with an orphan `realPath` gives exactly today's fault string;
  - **the consumer's regression:** `inspect_typescript_universe`'s refusal sets over the existing native-context fixtures (`crates/host/tests/fixtures/native-context-fixtures.json` and `.current.json`), and over its evaluator tests, are byte-identical before and after the factoring, including the missing-layout and orphan-`realPath` cases;
  - `steps` below the entry count refuses `LayoutBound`.
- **(r3, R2-NBO-3) C1-T24's replacement observations:**
  - **first party:** `packages/x/package.json`, rewritten in place between the walk's capture and the layout's reuse, refuses `Changed` by the charged file `fstatat` through the held parent, with no second read (a read spy);
  - **pruned, alias:** a pruned manifest rewritten between its capture and a later alias meeting within the layout refuses `Changed` the same way;
  - **pruned, at the read set:** a pruned manifest rewritten between the layout's capture and C1c-1's reach refuses `ChangedSinceCapture` (LD-C1C-6). This is carried in C2b-0's lane once C1c-1's reach exists, and is otherwise C1c-1's own owed control;
  - in none of these does ordinary cached-byte reuse or a directory's metadata count as the observation.
- **No layout and empty (LD-C2B0-10):** no search directory gives `None`; an existing but empty one gives `Some([])`; a wholly excluded one gives `None`.
- **A refused layout** returns its exact capture set (LD-C2B0-12).
- **Model:** `snapshot_ledger_model.py --check` with the layout term, and the r9 cap derivation.
- **Census:** the discovery census's records are regenerated after the closure re-pin, and discovery's vectors are re-checked byte for byte.

## 5. Mutations

Each must fail the controls:
- a link followed;
- a nested package merged into its enclosing row;
- a `.`-prefixed entry listed;
- **(r3) the shared helper bypassed by an inline copy in C2b-0, or its fault strings changed;**
- **(r3) the first-party reuse made without the file observation;**
- **the virtual-store parent not searched (RF-1);**
- **`searched` removed, so a directory is enumerated twice or the cycle runs on to `Budget` (RF-2);**
- **a repeated row silently overwritten (RF-2);**
- an `ignorePaths` exclusion skipped;
- **`excluded_path` skipped for a first-party target (RF-3);**
- a manifest read twice, or reopened for parsing;
- `realPath` taken from the link text unresolved;
- the row bound off by one;
- a listing step uncharged;
- `Some([])` returned where `None` is due.

## 6. Checks

The lane covers:
- the host and security suites at base and candidate;
- warning-denied all-targets Clippy, and rustfmt;
- the focused layout, reach and exclusion tests;
- the snapshot model `--check`, and the census generated-output `--check` commands passing after regeneration, with the receipt-specific record of each receipt's delta and its interval (LD-C2B0-7);
- the environment exceptions, the operability source census with its mint audit, and verify_design;
- the mutations.

## 7. Open questions

- **Q6 (ruled in r3: lawful, with the observation duties).** Is A-C2B0-1's ordering lawful? The layout runs after the walk, and C1-T24's layout leg is discharged by the read set's re-observation (LD-C2B0-11). The alternative is to keep the layout before the walk and take first-party Cargo roots from B2's discovery derivation, which loses `WalkEvidence`'s structural provenance (LD-C1C-13).
- **Q7 (ruled in r3: a session-owned, bounded, internal handoff).** Is the parse handoff, `CaptureSession::parse_captured` (LD-C2B0-5), rightly a session method, or should the session expose the retained bytes to a parser C2b-0 owns?

## 8. Not delivered

- **C2b-1:** the TypeScript context, the options, `libSelection` and the stdlib join, the lockfile identity, and `bind_typescript_universe`. It waits for C2a.
- The read set (C1c-1), and the suffix table (C2's semantics, reviewed with F, `PROPOSAL.md`:310).
- The composition's no-layout branch (LD-C2B0-12).
- Any production caller.

## 9. Not claimed

- No context, universe, Plan selection or qualification.
- No reference-derived oracle for the layout.
- Not complete Node support: manifest-free packages (Q1) and non-profile manifests (LD-C2B0-5) are stated subsets.
