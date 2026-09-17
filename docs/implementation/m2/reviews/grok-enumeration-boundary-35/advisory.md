# Advisory: remaining enumeration owner

**Reviewer:** Grok. Root remains lead. Not Claude agreement.  
**Kind:** Bounded implementation map for the remaining enumeration owner: membership order/row recomputation, snapshot binding, named-package projection, full enumeration joins, and the TOML/JSON parser boundary. **Not ACCEPT-DESIGN-UNIT. Not projection34 acceptance. Not full M2. Not Run/replay.**  
**Work tree:** `/tmp/opensip-implementation/m2-grok-enumeration-boundary-35/review`. No live/frozen/history/product edits. No dependency installs. No commits.

## Pins (selected vs planned vs live)

| Source | Bytes | sha256 |
| --- | ---: | --- |
| Selected `enumeration_model.v1.py` | 49811 | `69b0eee39a45a941d7ab1ef22c0c8be161edd436b1441b27017f98fd1bcffe85` |
| Selected native `capability-totality-reference-selection-v1/reference/native_evidence_model.py` | 319944 | `e6784aa1a595222cfd5a3da55e2beaa3d0839c878d67d6821297682089bde2b9` |
| Physical NV load of the selected enumeration file (`docs/coop/.../native/native_evidence_model.v2.py`) | 319376 | `7d1c0acf2c7d74e52c6570bba66dcb846c03710f64cb61a2c83bd1c39abab8be` |
| Contract `enumeration-contract.v1.md` | 24366 | `b7858bc8a70a41280bb6d7d1b461cc267ae22598b0dc851d4f1061bcbfa1bc59` |
| Schema `enumeration-plan.schema.v1.json` | 19975 | `10627cb6a22a9ff1674c16c5fa4863a58dc86e5df8ac7ae55c45747b0e60197c` |
| Planned trial-34 `enumeration.rs` (extent helper only; **not accepted**) | 8783 | `b8750ad69d34e49d2a23e1b2023ea6f04732297dd886fa5050d4ef6f01971b2a` |
| Live evaluator `Cargo.toml` | 261 | `cef1245cbfec7e96892ea2cc7ffdead83d82cf3bc425c1ea98bd106d730b2f56` |
| Live identity `Cargo.toml` |  | sha2-const-stable `=0.1.0`, unicode-normalization `=0.1.24` `default-features=false` |

Live lock observed **22** inventory / **31** contract (`design-lock.json` **66066** / `116fefcc…514e3`). Live evaluator has **no** `enumeration.rs`. Live evaluator `lib.rs` **2459** / `cca6c6d8…72fb` is still capability/native/import owners only.

`assign_membership` / `admit_unit_roots` / `_family_of` **byte-equal** between selected native `e6784aa1` and the sibling v2 the enumeration file loads. Other native bytes differ (**568** characters). Next composition must **overlay the selected native** for the port, not assume the sibling file.

Projection34 (`project_enumeration_extent`, file/symbol only) is **private groundwork**. This advisory does **not** accept that source. Its own comment: it does not admit membership, classify package manifests, or mint subjects.

`open_run_closure` does **not** call `admit_enumeration`. Enumeration is a **later Plan-bound owner** (contract v1: joins, not `close_run`). Do not fold it into `inspect_retained_walk`.

## Selected obligations (existing law)

From `admit_enumeration` (**584–1048**) and `project_named_packages` (**365–432**). Internal fault keys only; ADMIT is enumeration-join admission, **not** a Run.

**A. Membership (every admission, including when Run supplies no derivation witness)**

1. `NV.admit_unit_roots` before any prefix/join (`ENUMERATION_MEMBERSHIP_UNIT_ROOT`).
2. Membership row paths cover `snapshot_paths` exactly, unique (`ENUMERATION_ADMISSION_PRECONDITION`).
3. `_membership_order_law` (**525–581**), native-evidence U-4b:
   - units strictly ascending `(UTF-8 rootPath, UTF-8 languageFamily)`, `unitOrdinal == index`;
   - each `memberPackageRoots` strictly ascending UTF-8;
   - tsjs `unitKind == NV.TSJS_UNIT_KIND[languageMode]`; no TS/JS kind on another family;
   - rows strictly ascending UTF-8 path;
   - `unsupportedFiles` / `outsideBoundaryFiles` are the row-order projections of those memberships.
4. Row derivation: `NV.assign_membership(units, inside_paths, None)` must `C.equal_typed` the non-outside rows. Outside rows: `unitOrdinal is None` and `languageFamily == NV._family_of(path)`.
5. Optional `membership_derivation` (`discover_units` + `assign_membership` with bounds) only when the caller supplies it. **Run closure does not.** Order law still runs.

**B. Snapshot binding**

- Full inventory: host TCB Blob rows; used manifest bytes must match `sha256` and `bytes` (`_manifest_bytes` **338–362**). Path list derived from inventory; `snapshot_paths` if present must equal that list.
- Standalone fixture: `snapshot_paths` only, no blob index.
- Missing bytes for a used `package.json` / `Cargo.toml` is **precondition**, not `syntax`.

**C. Named-package projection** (when any cell `kinds` contains `package`)

Host projection from **retained snapshot bytes**, not a caller oracle list (**367–371**).

For each first-party-scoped path whose basename is `package.json` or `Cargo.toml`:

| Basename | Parse | Named | Unnamed | Failed |
| --- | --- | --- | --- | --- |
| `package.json` | `C.parse(blob)` (strict canonical JSON) | `name` non-empty `str` | key `name` absent | `AdmissionError` → `syntax`; non-object / non-string/empty name → `classification` |
| `Cargo.toml` | **`tomllib.load` of the entire blob** (Python 3.11+ stdlib, **TOML 1.0.0** only) | `package` table with non-empty string `name` | no `package` key, or table without `name` (`workspace-only` if `"workspace" in data` else `no-name`) | `TOMLDecodeError` → `syntax`; non-table document / `package` not a table / name not non-empty str → `classification` |

Key presence is `"package" in data` / `"workspace" in data`, not truthiness. Candidate extent = named paths **union** parse/classification failures. Nameless / workspace-only manifests are **not** subjects and **not** in `candidatePaths`. Sort named by `C.canonical(path)`.

**D. Remaining joins** (after extents exist)

Plan snapshot/scope/membership digests; cell tuples vs `requestedCapabilities`; kind map; workspace root under scope; programBindings overflow/default-unit; enumerator selected/unselected; context/universe/engine domain; programEntry vs U-1/`entryConfigPath`; host file/symbol/package extents **equal** binding `extents[].paths`; inventory schema, missing/unexpected records, file/package totality, package `nativeSubjectId`/`qualifiedName` from the projection, `subject3:` mint (`evaluation-subject` + `packageManifestPath` for packages). Any fault → `REFUSE`. Empty faults → `ADMIT` with sorted evaluation-subject index.

**E. Preconditions this module does not redo**

Does not call `admit_native_context`, `bind_*`, or symbol extraction; does not re-hash native universe H. Those stay native owners. File/symbol **extent formulas** are selected (`host_file_extent` / `host_symbol_extent`); projection34 attempted those only.

## Product purity / dependency boundary (existing constraint)

| Crate | Constraint |
| --- | --- |
| `opensip-evaluator` | `#![no_std]`, `forbid(unsafe_code)`, **only** `opensip-identity`. Description: pure owners over supplied immutable evidence. |
| `opensip-identity` | `#![no_std]`, `forbid(unsafe_code)`, exact JSON `parse`/`encode`, two production crates pinned by `tools/identity/dependency-policy.json` (sha2-const-stable, unicode-normalization `default-features=false`). No serde. |
| `opensip-host` | std; evaluator is **dev-dependency**. Host must not become the parser of record. |

`tools/check_package_edges.py` itself uses `tomllib` to **read product Cargo manifests** as a developer check. That is not the enumeration owner and does not license a host-supplied parse of snapshot `Cargo.toml`.

Identity `Value` has **no float**. `C.parse` refuses JSON floats. `tomllib` **does** produce Python `float` / `datetime` for TOML floats and times (**conversion table**, Python 3.14 docs). Those values can appear in a lawful Cargo.toml even when `package.name` is a string. A parser that rejects floats as “not our JSON profile” would mis-mark valid TOML as `syntax`. The TOML value domain is **not** identity `JsonValue`. Do not smash TOML into `JsonValue` and then `C.parse`.

## Parser location (proposed; successor required before any crate)

**Selected law** is full-document `tomllib` (TOML **1.0.0**) plus identity `C.parse` for JSON. The following are **not** selected and must not silently substitute:

- A Cargo-only subset lexer (`[package] name = …` only).
- Host/`serde` deserialize into a claimed record.
- Current `toml` crate **default** line (docs.rs / lib.rs **1.1.x + spec-1.1.0** as of 2026-09). `tomllib` explicitly does **not** implement TOML 1.1.
- Putting a TOML crate on **evaluator** (would be its first non-identity dependency; breaks the pure-owner crate).

**Proposed ownership (choice, not yet law):**

1. **Identity** owns exact retained-byte parsers that yield typed values used in admission. JSON already lives there. A TOML **1.0.0** parse-to-table API belongs beside `parse_json`, returning a **TOML value tree** (tables/arrays/strings/ints/bools/floats/datetimes), not `JsonValue`.
2. **Evaluator enumeration owner** calls that API, then applies `project_named_packages` classification (`package`/`workspace` key presence, name string). It never takes a pre-parsed table from the caller.
3. **Host** supplies snapshot bytes (and Blob sha/len). No parse result on the wire as authority.

**Successor required before adding parser dependencies** (actual blocker for Cargo.toml):

- Formal **identity dependency-policy successor** (same class as unicode-normalization): crate identity, version, `default-features`, checksum, full source census, `no_std`, `forbid(unsafe_code)` or equivalent geiger-visible `forbid`, no serde-into-product-structs requirement.
- Explicit **TOML 1.0.0 / tomllib profile** in that successor. Do not take `toml` 1.1 defaults. If the crate can select 1.0.0, pin that mode. Independent replay means another host classifies the same bytes the same way.
- Qualification corpus: `syntax` / `classification` / `no-name` / `workspace-only` / named, including dotted keys, inline tables, `[workspace]` without `[package]`, floats/dates elsewhere in the file, duplicate keys. Compare to CPython `tomllib.load` on the same blobs. Drift is a product defect, not a fixture preference.
- If no crate meets no_std + 1.0.0 + no-unsafe + tomllib parity: **do not add a dependency**. Keep fail-closed (below). An owned identity parser is a larger successor, not a silent subset.

**Fail-closed until that successor:** a scoped `Cargo.toml` must not be dropped from the candidate algorithm. The owner should **refuse** (`Unsupported("toml package projection")` or composition `ENUMERATION_PACKAGE_PARSE` / precondition) rather than classify it as unnamed or skip package cells. JSON `package.json` projection can proceed on identity `parse` **now**.

## Minimal faithful next composition (after projection34, not accepting it)

Do **not** grow the extent helper into admission. New evaluator module (planned name `enumeration.rs` as **joins owner**, distinct from the private extent functions):

| Stage | Selected work | Parser |
| --- | --- | --- |
| 1 | Port `admit_unit_roots` + `_membership_order_law` + `assign_membership(..., None)` over retained `UnitMembershipV1` + snapshot path set | none |
| 2 | `_snapshot_index` + membership covers snapshot; when full inventory, rehash used manifest blobs | none (sha256 already identity) |
| 3 | `project_named_packages` for `package.json` via identity `parse` | JSON only |
| 4 | Same function for `Cargo.toml` | **blocked** on parser successor; fail-closed |
| 5 | Remaining `admit_enumeration` joins (plan digests, cells, bindings, extents equality, inventories, `subject3:` mint) | uses stage 3/4 projection |

File/symbol extent formulas may **call** the private projection helper once that helper is accepted; they are not this unit’s acceptance. Package extent **is** the named-package projection, not the file extent.

`inspect_enumeration` (name is a proposal) takes retained plan, analysis-spec, scope, membership, enumeration-plan, inventories, already-admitted native maps, snapshot inventory/blobs. Copied `TraversalBudget` like other owners. Returns counts + refusals. **Not** a Run token.

Public default inspect paths stay fail-closed. Do not catch `Unsupported` as success.

## Compatibility risks

- **TOML 1.1 vs 1.0.0:** current `toml` crate line advertises spec-1.1.0. `tomllib` is 1.0.0. Trailing commas, `\e`, optional seconds, etc. can flip `syntax` vs named.
- **Floats/datetimes:** identity JSON forbids floats; TOML does not. Classification only reads `package`/`workspace`/`name`, but **parse** must succeed on the whole document.
- **Key presence vs dotted keys:** `package.name` as a dotted key still yields a `package` table in TOML 1.0; a subset scanner of `[package]` headers can disagree.
- **Workspace-only:** `"workspace" in data` after a full parse. A scanner that never builds the root table cannot distinguish `workspace-only` from `no-name`.
- **JSON path:** must stay `C.parse` / identity `parse`, not `serde_json`. Non-canonical `package.json` is `syntax`.
- **Membership `boundaries=None` in row derivation** vs operational derivation with bounds: do not pass Plan-time boundaries into the U-4b recompute of **inside** rows; selected code passes `None` (**573**).
- **Loader skew:** selected enumeration file imports sibling native v2 and sibling `identity-model.v3.py` (**157684** / `a6dc5f99…`), not selected I `7b6750a9`. `evaluation-subject` prefix is `subject3` in both. Bind the **selected** native for `assign_membership`; re-check identifier parity against product identity before minting `subject3:` in Rust.

## Actual blockers

1. **No lawful Cargo.toml parse in-tree** under evaluator/identity purity. Adding any TOML crate requires an identity (not evaluator) dependency-policy successor with a **TOML 1.0.0 / tomllib** pin. Until then, package cells that see a scoped `Cargo.toml` cannot complete selected projection.
2. **Do not accept projection34** as membership, snapshot, package, or joins.
3. **Do not put the parser in host** or accept an externally claimed table.
4. Enumeration owner is **not** `inspect_retained_walk`. Separate composition.

## What is not a successor

Porting `assign_membership` / order law / snapshot sha checks / JSON `package.json` projection / remaining joins that consume an already-computed projection. Those are selected algorithms. The successor is **only** the TOML parser identity and its dependency census.

## Verdict

**NOT ACCEPTANCE.** Next faithful slice: membership order/row + snapshot binding + identity JSON package projection + remaining joins, with Cargo.toml **fail-closed** until an identity TOML 1.0.0 successor. Evaluator stays identity-only `no_std`. Partial TOML and claimed parsed records are incompatible with selected `project_named_packages`. Root remains lead; projection34 stays independently reviewed.
