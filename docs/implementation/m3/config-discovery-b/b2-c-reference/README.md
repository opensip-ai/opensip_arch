# B2-c0: the current native unit reference (contract successor 166)

**Proposed design unit, 2026-10-16, round 2.** It implements section 1 of the accepted B2-c plan r2 (Codex `codex-b2c-plan-r2`; architecture `7c55cdab`).

## r2 changes (Codex `codex-b2c0-reference-r1`, REQUIRED-FINDINGS)

**B2C0REF-R1-RF-1: both new boundary predicates omitted the directory-custody and DEPTH exclusions.** The predicates are LD-B2C0-1's filter and the member-consistency check.
- **The fix.** Both now use one full admitted-boundary predicate, `_admitted_boundary`: a nested repository, a nested project, or a directory-custody or `DEPTH` row. A `MARKER_CUSTODY` row still excludes only its marker file (the selected `_boundary_hit` with no marker name).
- **The anchor itself.** LD-B2C0-1 now tests whether the derived pruned anchor itself is at or below a boundary, as the override says.
- **New regressions:**
  - for `DIRECTORY_CUSTODY:ACL_UNREADABLE` and for `DEPTH`: a derived anchor inside the excluded directory, and a carried `.git` anchor there, both admit, while a disagreeing anchor outside still refuses;
  - a marker-custody row does not exclude unrelated content: a derived `node_modules` anchor beside the excluded marker refuses when missing, and so does a carried `.git` under it.
- **A sixth mutation,** `boundary-predicate-narrowed`, is caught.

**The oracle.** B2-c1's product instrument (`crates/host/src/discovery.rs`) is compared byte for byte against this reference. The reference makes the selected native model the current oracle without editing a byte of it. It adds one passage override, LD-B2C0-1, which resolves a conflict that the current composition exposes.

**Not included:** no NE schema, SLM, DD, product code or qualification change.

## What it is

`reference/native_unit_reference.py` loads the selected model (`b-s9/reference/native_evidence_model.py`, contract successor 81) at its accepted bytes.

**Where it runs.** The model runs with `__file__` set to the directory its sibling imports name (`docs/coop/design-corrections/native/`), with its whole loading closure pinned (plan r2 NBO-1): the two foundation modules, the base schema bundle, the capability matrix, and the historical shared rule it binds at load.

**What `load` returns:**
- **The historical module,** unchanged.
- **`Current`,** a second load of the same bytes with four documented substitutions of module globals. The model resolves each by name at call time:

| Global | Current value | Why |
| --- | --- | --- |
| `DD` | The B2-a rule (`discovery-defaults.sx1-r1.py`, successor 163), bound for each call to the admitted inventory's member roots | B2-a's corrections and SX-1's `.opensip` anchor, at the root and at each member root (B-S1) |
| `admit_current_boundary_inventory` | Admits `AdmittedBoundaryInventoryV3` only, validated in the merged bundle; V1 and V2 refuse | B-S1: V3 is the current inventory (plan r2 LD-B2C-3) |
| `validate_native` | The model's own `UnitDiscoveryV2` output check is deferred; this module validates the result as `UnitDiscoveryV3` | B-S1: V3 output (plan r2 RF-2) |
| `_boundaries_out` | Also emits `memberRepositories` (`UnitBoundariesV2`) | B-S1 |

**The merged bundle** is the base native bundle with B-S1's four `$defs` added, as its merge rule says: no base member replaced or removed.

**The current entry points** wrap the model's and add B-S1's U-8 member rules:
- A member is not a boundary. The model never sees it as one, so its contents are ordinary directories.
- A `vcs-tree` anchor `D/.git`, `.hg`, `.svn` or `.jj`, whether derived or carried, with D strictly below the root and not at or below an admitted boundary, refuses `native.boundary-inventory-mismatch` unless D is an admitted member. Admitted boundaries are those of LD-B2C0-1's predicate.

## LD-B2C0-1: anchors inside a boundary are not compared (a passage override)

**The conflict.**
- **U-8 (NE:837-841)** requires every anchor the native instrument derives from the marker inventory to appear in the admitted inventory.
- **S3 (SL:146-168)** records nested repositories and projects and never enters them. B2-b0's walker population (LD-B2B-5, contract successor 164) and the B2-b walker implement exactly that, so the admitted inventory carries no anchor inside a nested repository or project.
- **Where they meet.** A project whose nested repository holds a `node_modules` marker therefore refuses `native.boundary-inventory-mismatch` under the current composition. That includes the law's own join fixture, P3. The historical join sweep passed only because SLM's whole-tree collection over-observed.

**The resolution.** Only derived anchors outside every admitted boundary are compared.
- **In the reference,** a marker whose derived pruned anchor is at or below an admitted boundary (a nested repository, a nested project, or a directory-custody or `DEPTH` exclusion) is withheld from the model's anchor derivation.
- **Nothing else changes.** Such a marker is never a unit (U-4a), and its files are `outside-project-boundary` rows (U-4b item 4a, which precedes pruning).
- **In the contract text,** the record carries one passage override, on NE line 838 (`successor.json`), and binds it as the current meaning.
- **Rejected:**
  - letting security enter a nested repository to count its pruned trees, which S3 forbids;
  - dropping the subset test, which would lose the foreign-inventory refusal.

**Its effect on one case.** `units-boundary-inventory-whose-pruned-trees-disagree-with-the-marker-inventory-refuses` chose its disagreeing anchor inside the nested repository `vendor/lib`. On the current lane that anchor is not compared, so the step admits the root unit. The case's purpose, refusing an inventory that was not taken over this marker inventory, is kept by a current variant whose disagreeing anchor (`node_modules`) is outside every boundary, and which refuses. The schema-invalid `caller-ignores` step is unchanged.

## The checker

`evidence/check.py` writes `evidence/checks.json`. It runs:
- **Historical.** All 26 `units-*` cases of `native-cases.v2.json` pass under the model as loaded.
- **Current.** All 26 pass through `Current`, with each case's version-2 inventory argument projected to version 3 with no member. That projection is the checker's own, of the case input, and is not part of the reference. Seven cases differ, each explained:
  - six by SX-1's root `.opensip` anchor in `excludedPathPrefixes`;
  - one by LD-B2C0-1 (above).

  Any other difference fails the checker.
- **The B-S1 member cases** (plan r2 RF-2):
  - an empty-member V3 record with a root `.opensip` anchor admits, and `.opensip` is excluded in scope;
  - two admitted members are ordinary directories: their manifests are units, their `.git` anchors are accepted, a member's own `.opensip` is pruned (`opensip-custody-state`) and required of the inventory, and members add no excluded prefix;
  - a nested `vcs-tree` anchor whose parent is no admitted member refuses, whether carried or derived, and admits once the parent is a member;
  - (r2) directory-custody and `DEPTH` exclusions are boundaries for both rules, and a marker-custody row excludes only its marker;
  - the current lane refuses a version-2 inventory.
- **The join sweep, current on both sides.** B2-b0's `current` gives the P3 inventory, and this reference consumes it:
  - the root unit, and the boundary files outside;
  - both boundaries in scope;
  - both crossings refuse;
  - the subset test still refuses a derived anchor missing outside the boundaries, and admits once it is carried.
- **Mutations.** Each patches a copy of the reference, and the checker must then fail:
  - the member check dropped;
  - the LD-B2C0-1 filter dropped;
  - members not bound to the rule;
  - version 2 admitted;
  - the boundary predicate narrowed to repositories and projects (r2);
  - the historical rule kept.

  All six are caught.

## Binding

The record (`successor.json`) binds as contract successor 166. **Its parents** are:
- the model and its loading closure;
- the B2-a rule and the B-S1 additions;
- the native cases and the runner it uses;
- the security checker and the B2-b0 reference used by the sweep;
- NE, the override's parent.

**Its one passage override** is NE line 838.

`build_and_verify.py`, which supports the review and is not a subject member, shows the product's real `verify_design` passing on the base lock and with this record appended.
