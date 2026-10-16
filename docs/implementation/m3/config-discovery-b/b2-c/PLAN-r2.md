# B2-c implementation plan r2: the native unit instrument (M3-B item 14; `crates/host/src/discovery.rs`)

**Lead plan, 2026-10-16. Proposed; it needs Codex review.**

## r2 changes (Codex `codex-b2c-plan-r1`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B2CPLAN-R1-RF-1:** the four names were internal aliases, not missing public codes | **The vocabulary gap is withdrawn** (section 2.3). The four names are in the registry's `internalAliases`, and its `aliasRule` keeps them out of public `DomainDetailCode`. The instrument decides with the reference's internal keys. One closed host map normalizes them at the host boundary to the public targets already in the product vocabulary. The map is an exact copy of the registry rows, pinned to the registry's bytes. Each internal refusal is tested against its registered public route. **B2-c0 is design only:** no product commit and no schema change. |
| **B2CPLAN-R1-RF-2:** the selected V3 contract must be implemented, not only accepted as input | **The output is `UnitDiscoveryV3`** in both the wrapper and the product: `PrunedTreeV3` rows (with SX-1's `opensip-custody-state` reason for the exact `.opensip` anchor at the root `""` and at each admitted member root) and `UnitBoundariesV2` carrying `memberRepositories`. **U-8's B-S1 member rules are implemented:** a member is not a boundary and enters no `excludedPathPrefixes`; the `vcs-tree` member-consistency check refuses a nested anchor whose parent is not an admitted member; an explicit root inside a member is ordinary; U-9 keys off surviving units, members included, at the root only. **No B3-b reader is built:** members come only from the admitted inventory. **New current cases:** an empty-member V3 record with a root `.opensip` anchor; a record carrying admitted members; a nested `vcs-tree` anchor whose parent is absent from `memberRepositories`, which refuses. The historical V1/V2 replay stays separate. |
| **NBO-1** | Section 1 now calls the "must equal" text stale commentary: the model already runs the `(path, reason)` subset test. The wrapper pins and supplies the model's whole loading closure: `foundation/canonical.py`, `foundation/identity-model.py`, `native-evidence.schemas.v2.json`, `native-capability-matrix.v2.json` and the selected shared rule, at their selected bytes. The model's bytes are kept. |
| **NBO-2** | Section 3's recommendation now states the candidate order and the package-name and subpath grammar. **It drops the partial-settlement carrier:** `UnitDiscoveryV3` is closed, so any unresolved `extends` edge refuses typed, which needs no new carrier. The recommendation is a direction for r8, which Codex reviews separately; it is not a claim of complete TypeScript resolver compatibility. |

**Bases:**
- product `c0e61a4`: inventory v200, 165 contract successors;
- architecture `ecd3c5a`: shared status r99.

**What precedes it.** B2-b is bound through B2-b4c: the downward walker, the census, the recorded caps and the blind held-out run. The repository-entry T2 margin holds. Workspace full-ledger margins wait for B3-b.

**Authority:**
- law M3-B r7, items 12 to 15 and the unit table at PROPOSAL-r7.md:971 ("B2-c: `discovery.rs`, the native unit instrument U-0 to U-9 (item 14), the JSONC reader shared with C2, the scope descriptor, default selection");
- NE §1.2 and §1.4 (NE:146-215, NE:619-948);
- the B-S1 successor (`AdmittedBoundaryInventoryV3`, U-8's V3 passages);
- the B2-a shared rule (contract successor 163) and the B2-b0 discovery reference (contract successor 164).

## 0. What B2-c delivers, and what it does not

**Delivers.** A pure, first-party host instrument in `crates/host/src/discovery.rs` covering:
- U-0, `admit_unit_roots`;
- U-1, unit kinds and modes, with effective `allowJs` as an input;
- U-2, Cargo workspace folding, parsing `Cargo.toml` `[workspace]` as data with the pinned `toml` crate;
- U-3 and U-4, membership, exactly once per file;
- U-4a, the shared rule, from B2-a's `custody::discovery_rule` only;
- U-4b, order, ordinals, rows and `membershipDigest`;
- U-7, the 4096 cap shared with security;
- U-8, `require_admitted_boundaries` over the B2-b `AdmittedBoundaryInventoryV3`: the subset test, `excludedPathPrefixes`, and B-S1's member rules (members are not boundaries; the `vcs-tree` member-consistency check);
- U-9, the syntax-only fallback;
- the Config2 join: `normalize_explicit_root` and `spell_root`, exact explicit roots, `native.explicit-root-without-marker`;
- `unit_scope_descriptor`, with at most 1024 roots, otherwise `PROJECT.SCOPE_LIMIT`;
- default selection (AQ:76-99), with an unavailable capability disclosed;
- the first-party, bounded JSONC reader and the effective-`allowJs` derivation over a `tsconfig`/`jsconfig` `extends` graph (section 2.2). C2 will call the same function.

**Not delivered:**
- **The snapshot inventory and its bytes** (C1). B2-c's instrument takes a marker inventory and a file list as inputs, as the reference does.
- **Production callers** (J1).
- **Framework recognition, the YAML subset reader and recommendation evidence** (B2-d, items 16 and 18).
- **D15 members and readers** (B3-b).

## 1. The current native unit reference (B2-c0, design unit; contract successor 166)

**Why a reference unit is needed** (as B2-b0 was for the walker). The selected native reference is `b-s9/reference/native_evidence_model.py` (contract successor 81). It holds `discover_units`, `assign_membership`, `unit_scope_descriptor`, `admit_unit_roots` and `default_capability_selection` (lines 95, 3841, 4018, 4183 and 4460). Three things keep it from being B2-c's oracle as it stands:
1. **It loads the shared rule from `HERE.parent / "discovery-defaults.py"`** (line 36). In the B-S9 copy that path does not exist. The rule it meant is now B2-a's `discovery-defaults.sx1-r1.py` (successor 163).
2. **It admits boundary inventories V1 and V2 only** (`BOUNDARY_INVENTORY_RECORDS`, line 188). B-S1 made U-8's input `AdmittedBoundaryInventoryV3`, and B2-b's walker produces V3.
3. **Its output is `UnitDiscoveryV2`.** B-S1 selects `UnitDiscoveryV3`: `PrunedTreeV3`, with SX-1's `opensip-custody-state`, and `UnitBoundariesV2.memberRepositories`. B-S1 also adds U-8's member rules. (The model already runs the `(path, reason)` subset test. Its docstring's "must equal", at lines 3841-3870, is stale commentary, not a missing algorithm; NBO-1.)

**B2-c0 is a reference wrapper, as B2-b0 was.** It loads the B-S9 model at its accepted bytes, with its whole loading closure pinned and supplied (NBO-1). Then:
- **The shared rule.** It binds `DD` to the B2-a shared rule, so SX-1's `.opensip` anchor is pruned with reason `opensip-custody-state`.
- **V3 input.** It admits V3 exactly as B-S1's schema defines it, and passes the boundary rows the model reads unchanged: `nestedRepositories`, `nestedProjects`, `custodyExcludedUnits` and `prunedTrees`.
- **The member rules (RF-2).** It applies them around the model's calls. A member is not a boundary, so the model never sees it as one, and its contents are discovered as ordinary directories. The `vcs-tree` member-consistency check runs over the derived and carried anchors.
- **V3 output (RF-2).** It emits `UnitDiscoveryV3`, validated against B-S1's schema: the model's pruned rows as `PrunedTreeV3` (the same four fields, with SX-1's widened reason set), and `boundaries` as `UnitBoundariesV2` with `memberRepositories`.

The model's bytes are not edited. Every difference from the historical replay is listed and explained.

**Checker.** All 26 `units-*` cases of `native-cases.v2.json` replay in two stages, historical and then current. In the current stage, each case that supplies a V2 inventory also runs with its V3 projection, which has empty `memberRepositories`. The same applies to the security sweep `admitted-boundary-inventory-joins-security-discovery-and-native-unit-discovery`.

**New current cases (RF-2):**
- an empty-member V3 record with a root `.opensip` anchor;
- a record carrying admitted members, whose `.git` anchors are accepted and whose contents are units and members;
- a nested `vcs-tree` anchor whose parent is absent from `memberRepositories`, which refuses.

Any exception fails the checker, and coverage is exact. The historical V1/V2 replay stays separate.

**Bound as contract successor 166** with `ACCEPT-DESIGN-UNIT`. Design only: no NE, SLM, schema or product change (RF-1).

## 2. The product sub-units

### 2.1 B2-c1: `discovery.rs`, the pure instrument

**Inputs**, as in the reference:
- a marker inventory `{markerPath -> {sha256, isCargoWorkspace?, allowJs?}}`;
- the explicit roots, raw Config2 or flags-layer strings;
- the admitted `AdmittedBoundaryInventoryV3`, or `None` for the standalone lane only;
- the file list;
- `ignorePaths`;
- the capability registry rows.

**Outputs:** `UnitDiscoveryV3` (r2), `UnitMembershipV1` with `membershipDigest`, the scope descriptor with `scopeDigest`, and the default capability request. Each is the same canonical JSON as the B2-c0 reference.

**Design:**
- **One module.** It contains no I/O, no `std::process`, socket or write API, and no environment read. FW-01's structural check (`tools/tests/test_discovery_fw01.py`) gains `discovery.rs` as a pinned file, with planted negatives.
- **The shared rule comes only from `custody::discovery_rule`,** which is `pub(crate)` in security today. B2-c needs a narrow `pub` surface from `opensip-security` exposing the classification and enumeration entry points the instrument calls, as typed functions. That is a public-API addition, recorded as such. **Rejected:** a host-side copy of the rule (law item 13 rejects it).
- **`require_admitted_boundaries` is the only operational entry.** It takes the V3 record the B2-b core produces (`discovery_scan`). A missing inventory refuses with the internal key `native.admitted-boundaries-required`, which has no public detail (section 2.3). The standalone `boundaries=None` lane is `cfg(test)`-only plus one documented pure entry for fixtures. It discloses `source: none`.
- **Cargo `[workspace]` detection** reads the manifest as data with the pinned `toml` crate. That crate is a dependency of `opensip-identity`. The host either reaches it through an identity function, or the plan adds the same pinned version to the host's `Cargo.toml`. The lead recommends an identity function (`toml_declares_workspace`), so the host's dependency set does not change.
- **Refusals.** The instrument decides with the reference's internal keys, and section 2.3's closed map normalizes them at the host boundary. `PROJECT.SCOPE_LIMIT` is the public scope refusal. The internal host invariants are `NATIVE_UNIT_ROOT_REPRESENTATION`, `NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT` and the missing-inventory key.

**Vectors.** `tools/host/discovery_unit_vectors.py` runs the B2-c0 reference over:
- every `units-*` case;
- the cap and scope sweeps: 4200 installed manifests admit; 4200 first-party directories refuse; 4096 admit; 1024 and 1025 roots;
- generated property cases;
- out-of-order and mis-numbered mutations.

It writes `crates/host/src/discovery_vectors.json`, and the host tests compare every record byte for byte.

**The joint sweep (U-8).** A security-crate test walks the P3 fixture with the B2-b walker and builds the V3 inventory. It hands that inventory to the host instrument through the test-only scenario seam, as LD-B2B-7 did, and asserts the subset test passes, then fails on a removed or re-reasoned anchor.

### 2.2 B2-c2: effective `allowJs` and the JSONC reader

**What the law fixes.** Effective `allowJs` (NE:527-545) is computed over the `extends` graph:
- a `jsconfig` node supplies `true` unless it writes `allowJs`;
- own options beat bases, and later `extends` entries beat earlier ones;
- after inheritance, a written `allowJs` wins; otherwise it derives from `checkJs`, which defaults to `false`.

The reader is first-party and bounded, and C2 must call the same function (law item 14).

**What no text fixes: how an `extends` specifier names a file before any TypeScript runs.**
- NE's `TypeScriptConfigGraphV1` records `extendsResolved` as project-relative paths (NE:1332-1340), but it does not say how a specifier resolves.
- The reference takes `allowJs` as a trusted marker observation (`markers[...]["allowJs"]`).
- The `units-config-effective-allowjs-*` cases supply it directly.

So the product needs a law decision before it can compute `allowJs` from bytes. That is item 3's step.

**B2-c2's code, once the law is set:**
- **`jsonc`, a first-party bounded parser:** comments, trailing commas, a depth and size bound; a duplicate key is last-wins, as the TypeScript parser does, and is recorded.
- **`effective_allow_js(entry, resolve)`,** the graph walk with cycle refusal.

The host gives it a resolver that reads each config as data under the snapshot custody C1 will own. Until C1, the resolver is a trait the tests implement over scratch trees, and no production caller exists (J1).

### 2.3 Internal decisions and their public details (r2, RF-1)

**The internal keys.** The instrument decides with the reference's internal keys:
- `native.explicit-root-grammar`;
- `native.explicit-root-crosses-boundary`;
- `native.boundary-inventory-mismatch`;
- `native.too-many-units`;
- `native.explicit-root-without-marker`.

**The normalization.** The host boundary normalizes each one through one closed map in `discovery.rs`. The map is an exact copy of the matching rows of `public-detail-registry.v1.json`'s `internalAliases`, and a test pins it to the registry's bytes:

| Internal key | Public detail | Class |
| --- | --- | --- |
| `native.explicit-root-grammar` | `PROJECT.EXPLICIT_PATH_INVALID` | `CONFIG.INVALID` |
| `native.explicit-root-crosses-boundary` | `PROJECT.EXPLICIT_PATH_INVALID` | `CONFIG.INVALID` |
| `native.boundary-inventory-mismatch` | `PROJECT.DISCOVERY_INVENTORY_MISMATCH` | `REQUEST.PRECONDITION_FAILED` |
| `native.too-many-units` | `PROJECT.WORKSPACE_UNIT_LIMIT` | `REQUEST.UNSATISFIABLE` |

- `native.explicit-root-without-marker` is a public record, already in the product vocabulary, and passes unchanged.
- **An unknown internal key refuses,** as the alias rule says.
- **Each refusal is tested** against its registered public route in the product's existing vocabulary (`schemas/sources/common-v4.schema.json`).
- **No schema or vocabulary changes.**

**A missing operational inventory.** `native.admitted-boundaries-required` (NE:850-855; law item 14) has no alias and no public record. Under the alias rule, "absence of an alias is a positive statement": its `DomainDetail` is lawfully absent, and the key is kept in the operational diagnostic record. Only a host composition that drops its inventory can reach it. **B2-c1 implements it as an internal refusal with no public detail, under the selected law; r8 need not decide it** (r1's recommendation is withdrawn).

## 3. A law step: pre-Plan `extends` resolution (M3-B r8, item 14 addition)

**The lead's recommendation for the r8 text** (Codex reviews the law separately):
- **Specifiers.** `extends` is a string or an array of strings.
  - A specifier starting `./` or `../` is resolved from the config's directory, inside the project root. `.json` is appended when the basename has no `.json` suffix, as TypeScript does.
  - An absolute specifier, or one that leaves the project root, is unresolved.
  - Any other specifier is a package specifier. It is resolved by a data-only `node_modules` lookup: from the config's directory up to the project root, read `node_modules/<name>/<subpath>`, or the package's `tsconfig.json` when there is no subpath, following TypeScript 5.6.3's `extends` resolution for those two forms only. `package.json` `exports` conditions are not evaluated.
- **Data only.** Config bytes are read as data. Nothing runs and nothing is fetched (FW-01). A read inside `node_modules` is a read-set access under C1's custody, not discovery descent: U-4a's "never descends" governs enumeration, and NE:735-741 already puts actually-read pruned bytes in the snapshot inventory.
- **Symlinks.** A symlinked config file or directory on the path is followed only as C1's snapshot custody allows. Before C1, B2-c2's tests use no symlinks, and the production resolver is J1's.
- **Candidate order (NBO-2).**
  - **A path specifier** S, from config directory D: `D/S` when S ends in `.json`; otherwise `D/S`, then `D/S.json`. The first regular file wins.
  - **A package specifier:** the name is `@scope/name` or `name` (the npm name grammar), and the subpath is the remainder after the name, possibly empty. At each directory from D up to the project root, the candidates are `node_modules/<name>/<subpath>`, then `node_modules/<name>/<subpath>.json`, then (only when the subpath is empty) `node_modules/<name>/tsconfig.json`. The first regular file wins.
  - `package.json` `exports` and its `tsconfig` field are not evaluated.
- **Unresolved (NBO-2).** Any `extends` edge of the graph that does not resolve makes the marker's effective `allowJs` unknown, whatever inheritance would settle. That is a typed `CONFIG.INVALID` refusal with a new detail `native.config-extends-unresolved`, whose remedy text uses B-S9's route. `UnitDiscoveryV3` is closed, so a partially settled graph has no lawful carrier, and r8 adds none.

  **Rejected:**
  - guessing `false`, which silently narrows JS out of the program;
  - guessing `true`, which silently widens it;
  - running `tsc`, a provider launch before the Plan (law item 14 rejects it).
- **Bounds.** At most 32 config nodes and 64 KiB per config file; each exceeded bound is the same typed refusal. A cycle refuses as `native.config-extends-cycle`, under `CONFIG.INVALID`.

**This step is a law revision (r8)** because it adds two public detail codes and decides a read rule. The codes are registered through a successor of the public registry, with B-S9's remedy route. It needs Codex acceptance before B2-c2's code. This plan's recommendation is a direction for r8, which Codex reviews separately. It claims no complete TypeScript resolver compatibility.

## 4. Lead decisions

- **LD-B2C-1. Four steps under one plan:**
  1. B2-c0, the reference (design);
  2. B2-c1, the instrument (product);
  3. M3-B r8, the `extends` law;
  4. B2-c2, `allowJs` and the JSONC reader (product).

  B2-c1 can proceed in parallel with r8, because effective `allowJs` is an input to it, as in the reference. **Rejected:** one unit, which would hold the instrument behind an open law question.
- **LD-B2C-2. The shared rule is consumed, never copied.** It comes from security through a narrow typed `pub` API. **Rejected:** moving `discovery_rule.rs` into a new crate (churn without need); a host copy (forbidden by item 13).
- **LD-B2C-3. V3 is the only operational boundary input, and `UnitDiscoveryV3` the only output (r2).** The reference's V1 and V2 are historical and are kept only in B2-c0's replay.
- **LD-B2C-4. The instrument is pure and caller-free in M3-B.** J1 composes it with the walker, C1's inventory and the resolver. **Rejected:** a host composition in B2-c, which would need C1's custody first.
- **LD-B2C-5. Cargo `[workspace]` through an identity function,** so the host's dependency set is unchanged.

## 5. Sequence

1. This plan, reviewed by Codex.
2. B2-c0: the reference and checker (design only); review, records, lock bind (contract successor 166).
3. B2-c1: code, review, records, inventory; status round.
4. M3-B r8: the `extends` law, reviewed by Codex. If it is accepted, the B-S9 remedy route gets its successor rows.
5. B2-c2: code, review, records, inventory; status round.

B2-c is complete when all four bind. **B2-b is complete only when B3-b's member-observation bound closes the workspace full-ledger margins** (M3-B r6 item 12).

## 6. Not claimed

- No snapshot inventory or read set (C1).
- No production caller (J1).
- No recognition, YAML or recommendation (B2-d).
- No D15 (B3-b).
- No qualification.
