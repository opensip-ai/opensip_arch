# B2-b implementation plan r4 (M3-B unit B2-b: the S3 downward instrument)

**Lead plan record, 2026-10-15; r4. Not law, not code.** B2-b's dependencies are bound: B2-a (the rule, product `6c5b8e8`; its reference is contract successor 163), B1-b and B3-a. Product is at `94e5fde` (inventory v191, 163 contract successors). B2-b is size L. This plan splits it into a reference design unit and four product sub-units, each reviewed, recorded and bound in turn.

## r4 changes (Codex `codex-b2b-plan-r3`, REQUIRED-FINDINGS on the adapter)

| Finding | Resolution |
|---|---|
| **B2BPLAN-1:** r3 kept each anchor directory with its `.git` or `opensip.json` child, which lie strictly below a pruned anchor | **Pruning takes precedence over boundary detection** (1.0). A pruned anchor, of any of the four reasons, contributes only its own entry, which the walker observes by name from the parent, and **no child at all**, `.git` and `opensip.json` included. The boundary-evidence exception applies only to an **ordinary** directory, not pruned: it keeps its `.git` and `opensip.json` entries, which the walker sees when it lists that directory. New direct population assertions check that no child of any pruned anchor is present, under each of the four reasons. |
| **B2BPLAN-2 (reopened):** the explicit and config chain omitted ancestor `Cargo.toml`, so a join inside a Cargo `target` could be admitted | **The chain is built and walked parent-first, one level at a time** (1.0 and 1.3, LD-B2B-8). Each chain directory contributes its `Cargo.toml`, `.git` and `opensip.json` entries, observed by name. The next component is classified with the Cargo roots known so far. Building stops at the first pruned prefix, which is never entered. A crossing on an earlier level refuses first. That reproduces SLM's crossing-first order on the restricted population, so `JOIN_INSIDE_PRUNED_TREE:cargo-build-output:target` is kept for Codex's reproduction tree. New controls: explicit and config joins inside a Cargo `target`; an ordinary `target` without `Cargo.toml` admitted; a crossing above a pruned prefix refusing as a crossing; a nested repository below a pruned prefix never reported. |

## r3 changes (Codex `codex-b2b-plan-r2`: B2BPLAN-2 to B2BPLAN-5 resolved, B2BPLAN-1 partially resolved)

| Finding | Resolution |
|---|---|
| **B2BPLAN-1 (remainder):** swapping DD does not make SLM obey SX-1 for its other observations. `finish` collects nested repositories from every `fs` entry with `vcs`, including entries below `.opensip`, so a walker that never enters an anchor cannot match it byte for byte. | B2-b0 adds an explicit, reviewed **observation adapter** (1.0, LD-B2B-5): `walker_population(input)` restricts SLM's `fs` input to exactly what the native walker observes, and the current oracle runs SLM over that population. Nothing strictly below a pruned anchor (all four reasons, including SX-1), a nested repository or a nested project is in the population, decided outermost-first. Explicit and config sources keep only the named roots' chains (each chain directory with its `.git` and `opensip.json` children) and each root's subtree under the same rule. The upward-walk population is unchanged. No algorithm line of SLM is edited, and the historical replay stays separate. New controls: a hidden repository under `.opensip`, `node_modules`, `.git` and Cargo `target`; nested-in-nested repositories and projects; an explicit-mode nested repository in an unrelated sibling; and a check that no excluded-unit or boundary observation names a path outside the population. |

## r2 changes (Codex `codex-b2b-plan-r1`, REQUIRED-FINDINGS)

| Finding | Resolution |
|---|---|
| **B2BPLAN-1:** no usable V3 oracle; pending records against V3 serialization | **B2-b0**, a reference projection design unit, is added before the code (1.0). It runs SLM `discovery` with the bound B2-a reference (successor 163) in place of the original DD and projects the result to V3. Historical SLM replay is reported separately from current expected behavior. LD-B2B-3 now states exactly which fields compare before B3-b, which outputs are V3-validated, and how the pending provenance is made unserializable. |
| **B2BPLAN-2:** the source must be chosen before traversal | The unit source is chosen first, from the admitted resolution and the explicit joins, and each source has its own observation strategy (1.3, LD-B2B-8). Explicit and config modes observe only the named roots, each root's chain from the selected root, and each root's own subtree for boundary and pruning evidence. They never enumerate units or look outside those roots. Added: trace and budget controls for unrelated siblings, and for no fall-through to automatic discovery. |
| **B2BPLAN-3:** the all-entry T2 margin is a B2-b gate | The gate is kept whole (LD-B2B-4). B2-b4 censuses the entries the lead may read, re-verifying store integrity, with no-follow counting and objects and edges distinguished from bytes. The held-out margin stays **outstanding** until an authorized harness reports it without disclosure. **B2-b is not complete until it does.** The lead never reads held-outs. Partial census success cannot complete B2-b. |
| **B2BPLAN-4:** the typed owner waiver had no plumbing | Assigned to B2-b2 (the judgments) and B2-b3 (selection), with controls (LD-B2B-9). The waiver applies to the owner check only, on the explicit root's directories and its `opensip.json`, never on marker files (SLM:636, 665, 669-680). Legacy paths are unchanged. |
| **B2BPLAN-5:** the observation must carry identity | B2-b1's by-name observation returns kind **and** `st_dev`, `st_ino` and the no-follow metadata. The walker compares that identity with the opened descriptor before using the object. A change or absence refuses without retry. The swap control replaces an entry with another of the same kind. |

**Authority.**
- **M3-B r5** (MB): items 12 (MB:390-412), 13 (MB:414-450) and 15's FW-01 (MB:484-503); the B2-b row (MB:906); the order (MB:912-916); the test owners (MB:923-926).
- **B-S1** (successor 78): SX-1, LD-4, LD-10, LD-15, the V3 schema additions and its owed controls.
- **The B2-a plan's hand-offs:** LD-B2A-2 and LD-B2A-5.
- **SL S3**, as B-S1 overrides it.
- **SLM** `discovery` (SLM:581-906) and `boundary_inventory` (SLM:913-929).
- `security/discovery-cases.v1.json`.
- **X2 r9:** X2:231-248, X2:268, X2:272.
- **The T2 fetch spec** (T2F:41-55).

## 0. What exists (product `94e5fde`)

- **The rule.** `custody/discovery_rule.rs` (B2-a) is pure and `pub(crate)`.
- **The ledger.** Caps are 65,536 objects, 131,072 edges and 256 MiB (`work_ledger.rs:12-15`). `with_limits` can only lower them (:205-224). One ACL capture costs 131 edges.
- **Upward selection.** X2b's `select` and B1-b's analysis admission keep no walk rows, VCS kind or symlink flag. A symlink anywhere in the spelling refuses.
- **Listing.** `visit_entry_names` gives names only. No primitive returns a child's kind or identity by name without opening it.
- **Custody.**
  - `judge_project_object[_sampled]` and `check_project_object` (`project_chain.rs:433-574`).
  - `waive_owner` is always false (`custody.rs:71-92`).
  - `ProjectChainPolicy::from_grants` takes groups only.
- **Public rows.** The host `outcomes::Observation` rows exist (`outcomes.rs:1147-1322`). `InstallationTermination::ProjectExplicitPath` carries no subject.
- **SLM is not current.** It imports the original DD (no pruning correction, no SX-1), writes provenance `schemaVersion` 2, and recognizes versions 1 and 2 only (SLM:85, :623). It calls `DD.*` through its module global at call time (SLM:611-805).
- **No SLS discovery schema** is materialized in the product.
- **The T2 store** holds 49 materialized trees, ten of them held out. No bare repositories remain.

## 1. The units

### 1.0 B2-b0. The current discovery reference (design unit, contract successor 164)

`config-discovery-b/b2-b-reference/reference/discovery_scan_reference.py` (new, arch only):
- **The current oracle.** It loads SLM at its accepted bytes and replaces SLM's module global `DD` with the bound B2-a reference copy (successor 163). It does not edit SLM: no SLM byte changes, and DD and the B2-a copy keep theirs. The result is SLM's algorithm with the corrected outermost rule, parent-first Cargo roots and SX-1.
- **The observation adapter (r3).** `walker_population(input)` is a pure function that returns SLM's input with `fs` restricted to what the native walker observes. The oracle is SLM over `walker_population(input)`.
  - **Pass one: the selected root.** SLM runs once on the full input to obtain `selectedRoot` and the unit source, which the walker also chooses before traversal (LD-B2B-8). If that run refuses before `finish`, the refusal stands and no restriction applies.
  - **Upward population.** It is kept as is: every ancestor-or-self of `cwd` and of the explicit project path, with the entries the upward walk reads.
  - **Downward population, automatic source.** Built parent-first, one level at a time, as the walker lists. An entry is in the population only if its parent is an *ordinary listed directory*: in the population, and neither pruned nor a boundary. Then:
    - **a pruned anchor** (any of the four reasons, under the current rule, with Cargo roots taken from the `Cargo.toml` entries already admitted parent-first, and `.opensip` only at the root and member roots) enters as **its own entry only**. It is never a listed directory, so **no child of it** enters, `.git` and `opensip.json` included (r4);
    - **a nested repository or nested project** is a directory other than the selected root that is not pruned and holds `.git` (`vcs`) or `opensip.json`. The selected root is always an ordinary listed directory. It enters with exactly its `.git` and `opensip.json` entries, the evidence the walker sees by listing it, and is not otherwise listed;
    - **every other directory** is an ordinary listed directory.
  - **Downward population, explicit or config source.** For each named root, **the chain is built parent-first** (r4). At each chain directory, from the selected root down:
    - its `Cargo.toml`, `.git` and `opensip.json` entries enter, observed by name, so the Cargo roots known so far include that directory;
    - if the directory is a nested repository or project, the chain stops there, and SLM's crossing refusal applies;
    - the next component is classified with the Cargo roots known so far. A pruned prefix enters as its own entry only, and the chain stops there, so SLM's `JOIN_INSIDE_PRUNED_TREE` applies and nothing below is built.

    When the chain reaches the named root, the root's subtree enters under the automatic rule above. Unrelated siblings are absent.
  - **Why this order matches SLM.** On this population, SLM's crossing-first check sees only the boundaries above the first pruned prefix, and the pruned check sees the ancestor `Cargo.toml` entries. That is exactly what the parent-first native walk can know.
  - **Pass two.** SLM runs on the restricted input. The checker asserts that pass two's `selectedRoot` and unit source equal pass one's, and refuses otherwise. Every case whose pass-two outcome (status, refusal and detail) differs from pass one is listed with its cause: a pruned anchor or boundary that the walker cannot observe. A difference with any other cause fails the checker.
- **`project_v3(result)`.** It maps the result to the V3 shape: `schemaVersion` 3; `PrunedTreeRowV3` reasons; `memberRepositories` and `memberConfigs` as `[]`; the D9 projected to `DiscoveryD9V1`. It **omits `workspaceDeclarations`**, returning a *partial* V3 provenance tagged `pendingFields: ["workspaceDeclarations"]`.
- **`boundary_inventory_v3(result)`.** It applies the B2-a reference's V3 converter. This output is complete and is validated as `AdmittedBoundaryInventoryV3`.
- **Its checker runs every case twice** (both after the adapter has been checked against its own controls):
  - the **historical** SLM replay, unchanged and recorded as history;
  - the **current** projection.

  It reports each difference by case, and every difference must trace to the pruning correction, SX-1, the V3 delta or the adapter's exclusion of unobserved paths. It then validates:
  - every current boundary inventory, as `AdmittedBoundaryInventoryV3` in the merged SLS bundle;
  - every partial provenance, as `DiscoveryProvenanceV3` once its pending field is filled with each reader's `absent` row. That fill is used **only** to validate the other fields' shape; it is never emitted, and the checker labels it.
- **Adapter controls (r3, extended in r4).** Each runs on a synthetic `fs`, with expected outputs:
  - **(r4) direct population assertions.** For each of the four pruned reasons, an anchor holding `.git`, `opensip.json`, markers and subdirectories contributes only itself to `walker_population`; every child is absent;
  - **(r4) explicit and config joins inside a Cargo `target`.** Codex's tree (`/h/w/Cargo.toml`, a join to `target/u`) refuses `JOIN_INSIDE_PRUNED_TREE:cargo-build-output:target` through both the explicit and the config source; a `target/u` without any ancestor `Cargo.toml` is admitted as an ordinary directory;
  - **(r4) a crossing above a pruned prefix** (`r/` a nested repository, a join to `r/node_modules/x`) refuses as the crossing; a repository below a pruned prefix (a join to `node_modules/x/sub`, where `x` has `.git`) refuses as `JOIN_INSIDE_PRUNED_TREE`, and `x` is never reported;
  - a repository with `vcs` under `.opensip/`, under `node_modules/`, under `.git/` and under a Cargo `target/`, never reported;
  - a repository inside a nested repository, and a project inside a nested project, never reported;
  - an explicit or config root beside an unrelated sibling holding a nested repository, a nested project and markers, none of which is reported;
  - a marker below an anchor that never yields a unit, an exclusion or a Cargo root;
  - a property over every case: every path in `nestedRepositories`, `nestedProjects`, `units`, `excludedUnits` and `prunedTrees` is in the population, and every anchor row is the anchor itself, never a descendant.
- **No passage or schema change.** It is reviewed as ACCEPT-DESIGN-UNIT and bound as contract successor 164.

### 1.1 B2-b1. Platform primitives (`crates/platform`)

- **`WorkLedger::discovery_profile()`.** The only constructor above the platform caps: MB:396's provisional 2^20 objects, 2^21 edges and 2^30 bytes. `with_limits` is unchanged.
- **`RetainedDirectory::observe_child(name) -> ChildObservation`.** One charged `fstatat(AT_SYMLINK_NOFOLLOW)`, never an open, under the existing name grammar.
  - It returns `kind` (`Directory`, `File`, `Symlink`, `Other`) and the `DescriptorMetadata` (including `device` and `inode`), or `Absent`.
  - `ChildObservation::matches(&opened_metadata)` compares `device`, `inode` and kind.
- **Tests:**
  - exhaustion at exactly each cap and one below it;
  - the profile is unreachable through `with_limits`;
  - each kind on a scratch tree;
  - the observation does not change the parent's or the child's times;
  - a same-kind replacement between observation and open fails `matches`.

### 1.2 B2-b2. The pure discovery core (`custody/discovery_scan.rs`, new)

**What it mirrors.** The current reference (1.0) over an **observed scope**: the plain map the walker produces, like SLM's `fs` input. It implements:
- `finish(root)`;
- the exclusive source choice;
- `_explicit_units` with every `JOIN_*` detail;
- the automatic path through B2-a's `enumerate_units`;
- exclusions in SLM's order;
- the post-exclusion cap;
- per-object custody.

**Custody, with the typed waiver (LD-B2B-9).**
- A new `check_project_object_waived(…, waiver: Option<&ProjectOwnerWaiver>)` skips only the owner comparison, and only for directories on the explicit root's chain and for its `opensip.json`.
- Mode, ACL, link-count and size checks still apply.
- Markers are never waived.
- `check_project_object` and every legacy caller are unchanged.
- The SLS custody spellings (`FOREIGN_OWNER`, …) map from `project_chain`'s refusals in one table.

**Records (LD-B2B-3).**
- `DiscoveryProvenancePending` is the V3 provenance without `workspaceDeclarations`. It has no `Serialize`, no JSON projection and no conversion to a complete record, and it is `pub(crate)`.
- The completing function `complete(self, WorkspaceDeclarations) -> DiscoveryProvenanceV3` is **not written in B2-b**. `WorkspaceDeclarations` has no constructor until B3-b's readers. A pin test asserts that the module defines neither.
- `boundary_inventory(&pending) -> AdmittedBoundaryInventoryV3` is complete, serializable and V3-validated.

**Vectors.** `tools/security/discovery_scan_vectors.py` runs the bound current reference (successor 164) over every case plus SX-1, cap and waiver cases. The Rust test compares:
- every partial-provenance field, byte for byte, with `workspaceDeclarations` excluded by name;
- the complete boundary inventory, byte for byte;
- the refusal and its detail.

**Cases.**
- Cases whose upward behavior X2 r9 makes stricter are listed with their X2 r9 citation (LD-B2B-5). Their downward fields still compare when the selection admits.
- Cases needing a foreign uid, a mount or an unreadable ACL replay through the observed scope's synthetic metadata.

### 1.3 B2-b3. The walker (`custody/discovery_walk.rs`, new)

**Runs** after the handoff, over the root descriptor retained by `ProjectChain::root()`. It is charged to one discovery ledger, created once and never recreated, and never runs under the installation fence.

**The source is chosen first (LD-B2B-8).** From the admitted resolution (B1-a provenance tells a layer-6 `--workspace-root` from a config array) and the explicit joins, before any observation. Each source has its own strategy:

| Source | What is observed |
|---|---|
| **explicit-joins / config-workspace-roots** | For each named root, **parent-first** (r4): at each chain directory, observe its `Cargo.toml`, `.git` and `opensip.json` by name. A `.git` or `opensip.json` is the crossing refusal. Then classify the next component with the Cargo roots known so far: a pruned prefix is `JOIN_INSIDE_PRUNED_TREE:<reason>:<anchor>` and is never opened. At the named root, observe its own entries (its markers) and its subtree, for boundary and pruning evidence only (nested repositories, nested projects and pruned anchors, never units). Nothing outside the named roots and their chains is listed or observed. A present array never falls through to automatic discovery. |
| **automatic** | The selected root's tree, recursively. |

**Each listed parent.**
1. Observe each child by name (B2-b1), keeping its identity.
2. Apply `classify_entry` before any open, so a pruned anchor is never opened and only an anchor directory is recorded.
3. Open ordinary directories no-follow, and compare the opened descriptor's identity with the observation. A change or absence refuses and never retries.
4. Stop at 256 levels: deeper is `DEPTH`.
5. Record nested repositories and nested projects without entering them.

**Custody (LD-B2B-2).** Judged for each unit's chain and its markers, memoized per directory, with the same identity comparison. The waiver comes from the typed `ProjectOwnerWaiver` (LD-B2B-9). The core (1.2) decides; the walker only observes.

**Upward provenance.**
- B1-b's analysis selection is extended to keep the walk rows it already judges.
- `vcs` is the `.git` entry's kind. An indirection's `gitdir:` value is read as data under S3 file custody (4 MiB, SL:126-127) and never followed.
- `explicitPathWasSymlink` is false, because X2 r9 refuses a symlink anywhere in the spelling.
- An explicit `--project` with `--trust-project-owner` passes the typed waiver to the selection judgment of the explicit root alone.

**Exhaustion** is `WORK.BUDGET_EXHAUSTED`, with no partial result.

**Rows** project through the host's existing `outcomes::Observation` (LD-B2B-6).

**Tests (scratch trees).**
- **The CI trace (LD-B2A-5).** An instrumented run with `.opensip/` at the root shows only the parent's by-name observation of `.opensip`, and no open, listing or stat inside it. `.opensip` as a file or symlink is never source and has no row.
- **The chain controls (r4).** Codex's Cargo `target` join tree refuses through both explicit sources, with no open of `target`. An ordinary `target` without `Cargo.toml` is admitted. A crossing above a pruned prefix refuses as the crossing.
- **The scope trace (B2BPLAN-2).** An explicit root `a/u` beside a large unrelated sibling `b/` touches nothing in `b/`. With a ledger sized to the named roots, explicit mode succeeds while automatic mode exhausts. A config array that names one root never falls through, even when that root has no marker.
- **The swap control.** Same-kind replacement of a directory and of a marker between observation and open refuses, with the original identity compared.
- **Boundaries.** Nested repositories are never entered, and a `.git` file is never followed.
- **The waiver controls (LD-B2B-9):**
  - a foreign-owned project directory inside an otherwise admissible home is admitted with `--project` and `--trust-project-owner`;
  - refused without the flag;
  - refused with the flag but no `--project`, on the existing row;
  - refused on mode and on an ACL write even with the waiver;
  - a foreign-owned marker is still excluded.
- **Exhaustion** at the cap.
- **FW-01 for this module:** byte-identical records over a read-only tree, an untouched canary, and a structural pin.

The flag rows go to `crates/host/tests/discovery_tests.rs` through the test-only `ScenarioHome` seam (LD-B2B-7).

### 1.4 B2-b4. The T2 census and margin (MB item 12)

`tools/security/discovery_census.py`:
- **Integrity.** It re-verifies each lead-readable entry's materialized store against its pinned `gitTree` before counting: it recomputes the tree hash from the stored bytes, with no-follow traversal, and refuses any mismatch, symlink escape or extra file.
- **Counting.** Outside pruned segments (the B2-a reference rule), it counts directories, entries, unit chains and markers, the same population `git ls-tree` gives for the pinned tree.
- **Conversion and output.** It converts the counts to ledger objects and edges with B2-b3's cost model, which it pins from the code, and writes `custody/discovery_census.json`. Bytes are recorded separately, because MB bounds them by other means.
- **The product test** shows at least a 2× objects-and-edges margin for every censused entry.

**Held-out entries (LD-B2B-4).**
- The ten held-out entries are listed as `outstanding: held-out`, never read by the lead.
- B2-b is **not complete** until an authorized harness supplies non-disclosing margin results for them, or an accepted law change alters the gate.
- When B2-b4 reaches that point, the lead raises it to the owner as the decision it is.
- A failed margin returns the caps to the law. Nothing is raised by the lead.

## 2. Lead decisions

**LD-B2B-1. A design unit and four product sub-units, under one plan.**
- B2-b0 must precede B2-b2's vectors.
- **Rejected:** one unit; separate plans.

**LD-B2B-2. Custody is judged for unit chains and markers, not for every listed directory.**
- That is SLM's rule (SLM:682-718, :799-838). Listing admits no source, and C1 re-checks each read (SL:313-315). Judging every listed directory at 131 edges each cannot fit large T2 trees under 2^21 edges.
- **Rejected:** judging every listed directory.

**LD-B2B-3. V3 records are B2-b's, and their D15 content is B3-b's.**
- MB orders B2-b → B2-c → B3-b and gives B3-b "the readers; members in V3 records".
- **Before B3-b, these are compared** against the current reference:
  - every provenance field except `workspaceDeclarations`;
  - the complete `AdmittedBoundaryInventoryV3`, which is V3-validated;
  - the refusal and its detail.
- **The pending provenance** cannot be serialized or completed in B2-b. No `WorkspaceDeclarations` value can exist until B3-b, and a pin test holds that.
- No reader observation is invented. The checker's `absent` fill is shape-only and is never emitted.
- **Rejected:**
  - emitting invented `absent` rows;
  - building the readers in B2-b;
  - V2 records.

**LD-B2B-4. The census over lead-readable entries; the all-entry gate is kept whole.**
- The store is each pinned tree, re-verified at census time.
- Held-out entries are never read by the lead. Their margin is outstanding, and B2-b cannot complete without it.
- **Rejected:**
  - re-fetching, which uses the network for the same tree;
  - reading held-outs;
  - completing B2-b on a partial census.

**LD-B2B-5. Two replays.**
- **Historical:** SLM as accepted, recorded.
- **Current:** B2-b0, SLM with B2-a's corrections and SX-1, run over the walker's observation population and projected to V3, which is the oracle.
- **Why the adapter is lawful (r3).** SL S3 states that nested repositories and projects are "recorded, never entered" and that a pruned tree is never descended (SL:146-168, SL:187-216). SLM's whole-`fs` collection over-observes relative to that rule. The adapter removes exactly the paths the rule says are never observed, and nothing else.
- **Rejected:** editing SLM's `finish` (the accepted model's bytes stay as they are), and comparing only boundary inventories (the provenance fields would go unchecked).
- Where X2 r9 is stricter upward (symlinks in a spelling, roots outside H, X2b's selection), X2 r9 governs. Each such case is listed with its citation.
- **Rejected:** a root-only native harness.

**LD-B2B-6. Public rows go through the host's existing `outcomes::Observation`.**
- **Rejected:** a subject on `ProjectExplicitPath`.

**LD-B2B-7. The flag rows go through the test-only scenario seam until J1.**

**LD-B2B-8 (r2). The unit source is chosen before any traversal, and each source has its own observation strategy.**
- MB item 13: explicit and configured roots are exact roots, never scan roots, and a present array never falls through.
- Explicit modes observe the named roots' chains, their own entries and their subtrees' boundary and pruning evidence. That evidence is needed because a nested repository inside an exact root is still a boundary for that root's membership (U-8).
- **(r4)** The chain is walked parent-first, with each level's `Cargo.toml`, `.git` and `opensip.json` observed by name. A pruned prefix stops the chain unopened, so ancestor Cargo roots decide pruning before any named root is admitted, and nothing pruned is ever descended (SL:187-216).
- **Rejected:** a whole-root walk filtered afterwards, which scans and charges unrelated trees.

**LD-B2B-9 (r2). The typed owner waiver is narrow plumbing.**
- It applies only to the owner comparison, only on the explicit root's directory chain and its `opensip.json`, and never on markers (SL:129-130; SLM:636, 665, 669-680).
- It arrives as `Option<&ProjectOwnerWaiver>` through new functions, so legacy callers and X2 placement are unchanged.
- **Rejected:** a boolean parameter, which is an untyped grant; waiving markers.

## 3. Sequence

1. This plan (r4), reviewed by Codex.
2. **B2-b0:** reference, checker, ACCEPT-DESIGN-UNIT, records, lock bind (successor 164).
3. **B2-b1:** code, review, records, inventory.
4. **B2-b2:** code, review, records, inventory.
5. **B2-b3:** code, review, records, inventory.
6. **B2-b4:** census, review, records, inventory. Then the held-out margin is raised to the owner.
7. **Status rounds** as these bind.

B2-b is complete only when the all-entry margin holds.

## 4. Not claimed

- No native unit instrument, scope descriptor or `require_admitted_boundaries` (B2-c).
- No readers, members, `workspaceDeclarations` or D15 rows (B3-b).
- No read set (C1).
- No production caller (J1).
- No law change and no qualification.
- No held-out margin claimed.
