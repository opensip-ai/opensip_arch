# B2-b3d implementation plan r2 (M3-B unit B2-b, sub-unit B2-b3d: the walker storage redesign)

**Lead plan, 2026-10-16. For Codex review.** It implements law M3-B r6 item 12's walker-storage requirement (`config-discovery-b/PROPOSAL.md`, item 12; Codex `codex-m3b-r6-r2`).

**Bases.** Product `84caf3f` (inventory v197; B2-b4a and B2-b4b1 bound). Architecture `194fcad1` (shared r97, after law r6 at `fa0ee631`).

**Sequence after this unit.** The redesigned walker's census sets the discovery caps by r6's rule. A recording revision of item 12 then records the caps with the arithmetic, and B2-b4b3 changes the constants (B2-b4 plan r4 section 2.3).

## r2 changes (Codex `codex-b2b3d-plan-r1`, REQUIRED-FINDINGS)

| Finding | Resolution |
| --- | --- |
| **B2B3DPLAN-R1-RF-1:** raw rejected specifications must stay raw | **Section 1.1 is narrowed.** Only fields that hold a resolved absolute path today are rebuilt from the root spelling. Every other field keeps exactly its current construction: a rejected specification (`JOIN_PATH_GRAMMAR` in explicit-joins and config-workspace-roots modes, for example `../other`, backslash and dot-segment specifications) and every other raw or absent-path value. The rule is that **every record is byte-identical to today's for the same input**. The unchanged walk and scan vectors, including `explicit-join-escaping-the-root-refuses`, hold it. |
| **B2B3DPLAN-R1-RF-2:** listing failures keep their priority over name validation | **The one-pass conversion keeps today's order (section 1.2).** The visitor charges and converts each name in listing order. At the first name that does not form a logical path, it keeps a bounded, precharged copy of that name (and its index). It stops converting, but keeps visiting and charging, so the listing still runs to completion. Then, in today's order: a listing failure (the native error, the entry or name-byte limit, the close) refuses first; only then does a kept invalid name become `NAME_UNREPRESENTABLE`, with its absolute parent built at that point. A refused listing is never partly observed. **New focused controls:** a pure `ListingConversion` state machine, fed synthetic name sequences and terminal outcomes, shows that an invalid name followed by an entry limit, a native error or a close failure refuses with the listing failure, and that a successful listing with an invalid name refuses `NAME_UNREPRESENTABLE` with today's detail. A native control repeats the second case. |
| **NBO-1:** the production trace control | **A structural control (section 3).** `trace` and `before_open` take a closure that builds the spelling. The `cfg(not(test))` stubs take the closure and never call it. A lane check (in the FW-01 pin's way: code with comments and literals blanked) asserts that every call site in `discovery_walk.rs` passes a closure, and that no production path builds an absolute spelling outside a terminal refusal. A planted direct-string call must fail it. This replaces r1's test-only allocation-probe mutation. |

## 0. What r6 requires

- Discovery's per-entry storage carries **no absolute spelling**, and **no listed name is stored twice**:
  - the observed scope is keyed by root-relative path;
  - each child is observed and opened by name from its parent's retained descriptor;
  - the raw listing names are converted in one pass;
  - a per-name slot keeps only the observation.
- The population, evidence and records stay equal to the B2-b0 reference.
- Every charge still comes before its allocation (B2B3B-R1-RF-3).
- The residual costs are derived by the census, not assumed.

## 1. The changes

### 1.1 The core (`custody/discovery_scan.rs`)

- **The key.** `ObservedScope.entries` is keyed by root-relative path. The root is `""`; a descendant is `a/b`, with no leading slash.
  - `Judge::custody`, `markers`, `unit_custody` and every core read build relative keys.
  - The root-relative helpers (`join_rel`, the parent of a relative path) replace the absolute `join`, `parent` and `base` for keys.
- **The records are unchanged, byte for byte (r2, RF-1).**
  - **Fields that hold a resolved absolute path today are rebuilt from the root spelling,** exactly as today's `join(root, …)` builds them (the root `/` keeps its special case). These are `nestedRepositories`, `nestedProjects`, the resolved `units[].path` and `excludedUnits` paths, `prunedTrees`, the warnings that name a resolved path, resolved refusal paths and `UnobservedAcl.path`.
  - **Every other field keeps exactly its current construction.** A rejected specification stays its raw spelling: `JOIN_PATH_GRAMMAR` in both explicit-joins and config-workspace-roots modes returns `spec` unchanged (`discovery_scan.rs`), for example `../other`. So do absent-path values and any other raw input.
  - The core takes no `WorkScope`, as now.
  - The boundary inventory is unchanged: it already converts back to locators.
- **The order is unchanged.** `BTreeMap` order of keys with the shared root prefix removed is the same, and the root still sorts first. So push order is unchanged.

### 1.2 The walker (`custody/discovery_walk.rs`)

- **No per-entry absolute spelling.**
  - `Frame` keeps its retained descriptor and its relative path only.
  - `listed` and `verdicts` are keyed by relative path.
  - `spell` is removed.
  - The root spelling is kept once, for the core handoff.
- **Absolute spellings are built only on two cold, terminal paths:**
  - a refusal's detail: `Changed(..)` and `NAME_UNREPRESENTABLE`'s parent, which is a public detail;
  - the test-only trace.
- **Refusal records stay exempt as terminal,** as in B2-b3b r2. Each is built only when the walk ends.
- **The test-only trace stays absolute.** `trace`, `before_open` and `vcs_evidence`/`gitdir_target`'s `at` argument take the relative path. Under `cfg(test)` alone, a thread-local root set at the walk's start rebuilds the absolute spelling for the trace and hook. In production they build nothing.
  - `project_admission.rs`'s `at: &Path` stays. The walker passes the relative path, and the test-only `trace_child` prefixes the walk's root when `at` is relative.
  - Upward selection, which passes absolute paths, is unchanged.
- **Names stored once.**
  - `list` converts and validates each name inside the listing visitor, in listing order. The raw `Vec<Vec<u8>>` goes, and `.` and `..` are dropped there.
  - **Listing failures keep their priority (r2, RF-2).**
    - At the first invalid name, the visitor keeps a bounded, precharged copy of it and stops converting. It still visits and charges every later name, so the listing runs to completion.
    - Afterwards, a listing failure refuses first: the native error, the entry or name-byte limit, or the close.
    - Only then does the kept name become `NAME_UNREPRESENTABLE`, with today's detail and its absolute parent built at that point.
    - A refused listing observes no child.
    - The logic is a pure `ListingConversion` state machine that the visitor drives, so its order can be tested without a filesystem.
  - Each child keeps one owned root-relative path. Its name is the path's last segment, borrowed, with no second copy.
  - `LogicalPath::parse`'s validator copy stays a charged temporary.
  - The per-name slot keeps only the `ChildObservation`, in a vector parallel to the paths.
- **The scope key** is its own owned relative path, charged as an owned record of that path plus `ObservedEntry`.

  **Considered and kept for a later unit:** moving each child's path into the scope instead of copying it. Level iteration needs the directory children's paths after observation. The census measures the result either way.

### 1.3 The tests

The closed B2-b3b, B2-b2, B2-b4a and B2-b4b1 tests change only where they read storage that r6 redesigns. Every behavioral assertion stays.
- **`discovery_walk_tests.rs`.**
  - The population comparison maps the relative scope keys to `/h/w/…` instead of mapping absolute ones. The vectors are unchanged.
  - Direct scope-key reads (`entries.get_mut(unit_abs)`, `contains_key(...)`) use relative keys.
  - Traces, hooks, `Changed` paths and `NAME_UNREPRESENTABLE` details are unchanged: they stay absolute.
  - The two exact charge-count tests (the per-child prefix copies) are rewritten for the new charges. They keep their purpose: a deep chain is charged per child, and the explicit-spec half is charged per spec.
- **`discovery_scan_tests.rs`.**
  - The vector runner converts each vector's absolute keys to root-relative keys, dropping keys outside the root, which the core never reads. The vectors themselves stay pinned and unchanged.
  - Hand-built scopes use relative keys. Expected records stay absolute.
- **`discovery_census_tests.rs`, `scenario.rs`, `discovery_flag_tests.rs`.** No path changes. Records and details stay absolute.

### 1.4 The census (in this unit)

- **The tool.** `tools/security/discovery_census.py`'s model is updated to mirror the redesigned walker step for step. Its closure pins, anchors and size inventory are regenerated.
- **The records.** The census and vector records are regenerated over the same integrity-verified stores and vectors.
- **The controls.** The soundness tests, the five model mutations (re-anchored) and the probe cross-check carry over.
  - **The probe cross-check is retired** for this census: the lead probe walked the old walker. The census instead records a new lead probe of the redesigned walker over the same four stores, with the same throwaway method, as supporting evidence.
- **The outcome.** The census reports objects, edges and bytes at R = 134, 1,024 and 4,096, and the caps the r6 rule would set. **It claims no margin.** The caps are recorded and changed in the next steps.

## 2. Lead decisions

- **LD-B2B3D-1. Relative keys in the core,** with absolute records rebuilt from the root spelling. **Rejected:** keeping absolute keys and spelling them lazily, which still retains one absolute string per entry.
- **LD-B2B3D-2. The test-only trace stays absolute,** rebuilt under `cfg(test)` from a thread-local root. **Rejected:** changing the trace expectations to relative paths. Keeping them absolute keeps the closed controls' meaning unchanged.
- **LD-B2B3D-3. Refusal details stay absolute and terminal,** built only when the walk refuses.
- **LD-B2B3D-4. Names converted in the visitor, stored once,** with a parallel observation vector. A listing failure keeps its priority over a name refusal (r2, RF-2).
- **LD-B2B3D-5. The census moves with the walker** in this unit, so the census check never runs against a stale walker. Its caps are stated as the rule's arithmetic and not set here.

## 3. Checks

- The security suite at base and candidate. The failure sets are equal; the only expected changes are the rewritten charge-count tests, with the same names, which still pass.
- The walk, scan, upward and census vectors and checks, with every vector unchanged.
- Warning-denied all-targets Clippy (host, security, platform).
- rustfmt.
- The FW-01 and environment pins.
- The operability census and verify_design.
- The census controls and model mutations.
- New mutations and controls:
  - **a mutation that restores an absolute scope key:** the population map must fail;
  - **a mutation that drops the parallel observation:** a native walk must refuse;
  - **(r2, RF-2) a mutation that lets the name refusal win:** the `ListingConversion` controls must fail;
  - **(r2, NBO-1) the structural trace check.** Every `trace` and `before_open` call site passes a closure, and the production stubs never call it. A planted direct-string call must fail the check.

## 4. Not claimed

- No cap change, law change or production caller.
- No held-out or workspace full-ledger margin.
- No qualification.

B2-b is not complete.
