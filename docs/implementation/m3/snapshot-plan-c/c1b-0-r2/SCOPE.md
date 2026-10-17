# C1b-0 r2: S4's materialization, `vcs-observation` schema 3 (C1b plan r3, sub-unit C1b-0)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 2.**

## Round 2

Round 1 (`codex-c1b-0-r1`, subject `0eebcd4d…`) returned REQUIRED-FINDINGS, with one RF. Every schema and code result was verified (its dispositions 1 to 5 and 7 to 9), and those are unchanged here.
- **C1B0-R1-RF-1 (the census transition from the batch-entry baseline).** Round 1's lane ran on a base whose discovery receipt was already stale and which had no companion receipt. So its "no regeneration needed" held only because nothing on that base was current. C1b plan r3 LD-C1B-7 requires the batch to open from C1a4's accepted blind refresh. On that baseline, C1b-0's closure change stales both receipts, since the companion's bindings nest discovery's. Both census records then re-render their held-out rows. Round 2 therefore:
  - **gates on the baseline:** the lane of record runs only on a main holding C1a4's accepted refresh. There, both receipts must be current for main's own inputs, by the tools' own binding functions, and both records must render every held-out row as `blind-census`. `evidence/regenerate_c1b0_census.py` checks this first and stops while it is not so;
  - **regenerates the two records**, `discovery_census.json` and `snapshot_ledger_census.json`, with the tools' ordinary `--write` over the lead-readable cache, and adds them to the product map: fourteen paths;
  - **records both receipts' deltas** from that baseline: the discovery receipt's is exactly the generator-closure digest, and the companion's is exactly that digest nested in its `discovery` binding. It also records that every other record field is unchanged, except those the tools derive from the held-out results;
  - **preserves both receipts** byte-equal to main's, as historical baseline evidence for the stale interval;
  - **runs all three output `--check`s** after the regeneration;
  - **makes the stale check** (`check_c1b0_census_stale.py`) the regeneration's read-only `--verify`;
  - **guards base moves:** the integration re-runs the census checks and the `--verify` if main moved, so a permitted base move cannot silently change the reviewed output set.

  No held-out material is opened and no blind run is made. A design unit with product code: verdict `ACCEPT-DESIGN-UNIT` binds it as a contract successor.

It implements sub-unit C1b-0 of the C1b plan r3 (`../c1b/PLAN-r3.md`, accepted by Codex `codex-c1b-plan-r3`). It materializes M3-B successor S4 into the product: the record B-S2 defines (`config-discovery-b/b-s2/`), with VCS-1's meaning of `dirty`. Library and schema only:
- no Git read (C1b-1);
- no sealing of `kind: git` or schema 3 (C1b-2);
- no caller.

**History note (C1BPLAN-R3-NBO-1).** PLAN-r3's "r2 changes" table is superseded history. Its RF-1 row's "record an expected `--check` failure" and its assignment of the VCS model term to C1b-2 are replaced by r3:
- the output `--check`s pass, and the stale receipt is recorded separately;
- C1b-1 owns the term.

This unit follows r3.

**Base (r2):** product main holding C1a4's accepted blind refresh, as the subject manifest names. The candidate is built by three scripted, re-runnable steps:
1. `evidence/prepare_c1b0.py --rebuild`;
2. `evidence/run_c1b0_generation.py`;
3. `evidence/regenerate_c1b0_census.py`.

**Integration timing (r2).** The lane of record runs on the main that holds C1a4's accepted refresh, so that refresh is this unit's base. A later move of main is admitted only if:
- this unit's base remains an ancestor of main;
- the move touches none of the fourteen paths;
- the generation determinism check, the operability census, both census output checks and the `--verify` all pass again on the moved worktree.

The contract successor number is the next one at that time.

## What it changes

| File | Change |
| --- | --- |
| `schemas/sources/identity-v3.schema.json` | **B-S2's merge rule** (its fragment's `mergeRule`), applied to the product copy:<br>- `#/$defs/vcs-observation` becomes `oneOf [vcs-observation-v2, vcs-observation-v3]`;<br>- `vcs-observation-v2` is the product's current `vcs-observation`, asserted equal to the fragment's;<br>- `vcs-observation-v3` and `vcs-member-observation` are added, placed directly after `vcs-observation` (LD-C1B0-2).<br>Nothing else changes, and the file keeps its own serialization (indent 2, ASCII, final newline). The product copy is I1-L's, whose `vcs-observation` is unchanged, as B-S2's BS2-F3 foresaw. The same bytes are this package's architecture source, `product/schemas/sources/identity-v3.schema.json`. |
| `schemas/source-map.json`, `schemas/admission-source-map.json` | identity-v3's `architectureSource` re-pointed to that copy. The admission map's `registryArchitectureSource` is re-pointed to the package's `admission-registry.json`. |
| `schemas/admission-registry.json` | identity-v3's row re-pinned (bytes, sha256); every other row unchanged. |
| `crates/identity/src/schema_registry.rs` | identity-v3's compiled `SourcePin` re-pinned. |
| `tools/contracts/options.json` | Three entry points for the added definitions: `Identity3VcsObservationV2`, `Identity3VcsObservationV3`, `Identity3VcsMemberObservation` (LD-C1B0-1). |
| `tools/contracts/generator-closure.json`, `schemas/registry.json` | The closure re-pinned (identity-v3, the source map, the options) and the recipe (the source set, the closure digest, the options digest). |
| `crates/contracts/src/generated/identity.rs`, `apps/report/src/generated/report.ts` | Regenerated by the selected pipeline (`evidence/run_c1b0_generation.py`). `Identity3VcsObservation` becomes the generated `oneOf` of `…V2` and `…V3`. No product code uses the generated type. |
| `crates/evaluator/src/run_links.rs` | The Run closure's VCS joins become one helper, `vcs_joins`: `VCS_KIND_JOIN` stays at the top level for schema 2 and 3, and `VCS_MEMBER_JOIN` requires each schema-3 member to be `kind: git` with a commit (BS2-F2). One test (LD-C1B0-4). |
| `crates/host/src/schema_sources.rs` | A control module, `s4_vcs_observation_tests` (2 tests, below). |
| `crates/security/src/custody/discovery_census.json`, `crates/security/src/snapshot_ledger_census.json` | **(r2)** Regenerated by the tools' ordinary `--write` from the accepted baseline (LD-C1B0-6): each held-out row re-rendered `outstanding: held-out (blind receipt stale)`, with `heldOutMargin: outstanding`, and the fields derived from the held-out results with them. The two receipts are unchanged. |

## Lead decisions

- **LD-C1B0-1. The entry points follow identity-v3's existing rule.** Every top-level identity-v3 definition already has an entry point whose `typeName` is `Identity3` followed by the definition's PascalCase spelling, in module `identity`. The prepare script asserts this of all of them. The three added definitions follow it mechanically. No other options member changes.
- **LD-C1B0-2. The added definitions sit directly after `vcs-observation`.** The product's `$defs` is not sorted, and B-S2's merge rule gives no position. Placing the three next to the record they serve changes no other definition's position relative to the others. JSON Schema references are by name, so the position carries no meaning.
- **LD-C1B0-3. The architecture IDS bundle and the evaluator's scanner pin are unchanged.**
  - B-S2's fragment is the accepted successor of record for IDS (`docs/coop/design-corrections/foundation/identity-schemas.v3.json`). BS2-F2 assigns C1b only the product copy. This unit rewrites neither the architecture bundle nor I1-L's design copy.
  - `crates/evaluator/src/atom-registry.json`'s `scannerIdentitySchema` pins I1-L's design copy of IDS (198,423 bytes, `eb6ec957…`), an architecture reference that nothing in the product reads. It keeps its pin.
- **LD-C1B0-4. The member join is a testable helper.** Identity admission already enforces the member shape: `kind` const `git` and the 40-hex `commitId` pattern. So through admission alone `VCS_MEMBER_JOIN` cannot fire, and a test through the Run closure could never reach it. The join is therefore factored into `vcs_joins`, and its test calls it on values directly: the top-level join for schema 2 and 3, each member refusal, and the valid cases. The plan's C1b-0 row asked for the join; this is how it is made testable.
- **LD-C1B0-5. "Before and after S4" is fixed by B-S2's pre-S4 vectors** (C1b plan r3, NBO-2's rule, as C1b-0 records the pre-S4 side). B-S2's schema-2 vectors were computed under the accepted schema 2 (`check_b_s2.py`): 154 bytes `fd32de2c…` for `kind: none`, and 190 bytes `b7a78032…` for `kind: git`.
  - The control canonicalizes the same inputs and asserts those exact bytes and digests under the merged schema, through identity admission and through the Run closure's record check.
  - It also asserts that they admit under `vcs-observation-v2`, the accepted record copied.
  - The schema-3 vector (365 bytes, `b6e0334a…`) admits under the merge, and not under schema 2.
  - The snapshot-level preservation, a fixed tree's descriptor and `snapshot2` under each tracking observation, is C1b-2's (PLAN-r3 §4).
- **LD-C1B0-6 (r2). C1b-0 opens the census batch, from the accepted baseline** (PLAN-r3 LD-C1B-7 and its Q5 ruling; Codex C1B0-R1-RF-1).
  - **The baseline** is C1a4's accepted blind refresh on main: both receipts are current, and both records render every held-out row `blind-census`.
  - **The bindings that change:** the generator closure is a reference-loading binding of the discovery receipt (`discovery_census.py`:1067, `REFERENCE_PRODUCT`). The companion receipt nests the discovery receipt's bindings in its own `discovery` binding (`snapshot_ledger_census.py`, `Census.bindings`). So C1b-0's closure change stales both.
  - **The records that change:** each tool renders its held-out rows from its receipt only while it is current (`discovery_census.py`:1205-1218; `snapshot_ledger_census.py`, `compose_held_out`). C1b-0 therefore regenerates both records, and includes them in its product map.
  - **The receipts** stay byte-equal to main's: historical baseline evidence until the batch's one reviewed refresh after C1b-2. Neither is refreshed here, and no held-out material is opened.
  - **The record:** `evidence/census-regeneration.json`, from public fields only:
    - the baseline's currency;
    - both binding deltas (exactly the closure digest, nested for the companion);
    - which outputs changed (exactly the two records);
    - field by field, that each change is the held-out rendering and its derived fields.
  - **In the lane,** the three output `--check`s pass over the regenerated records, and `check_c1b0_census_stale.py` re-proves the record read-only (`--verify`).

## The tests

- **`the_s4_vectors_admit_with_their_published_bytes`** (host): B-S2's three vectors, built from the same inputs as `check_b_s2.py`.
  - Their canonical lengths (154, 190, 365) and SHA-256 are B-S2's.
  - Each admits under `vcs-observation` and through `RetainedInputs::identity_record_shape`, the check `run_links.rs` makes on `vcsDigest`.
  - The schema-2 pair also admits under `vcs-observation-v2`, and schema 3 does not.
- **`the_s4_negatives_refuse_at_admission_and_at_the_run_closure`** (host): B-S2's twelve negatives refuse both ways:
  - top-level `git`; top-level `dirty`;
  - empty `members`; `members` on schema 2; schema 3 without `members`;
  - unordered members;
  - an uppercase `commitId`; a 64-hex `commitId`;
  - an `hg` member;
  - an absolute member path; a `..` member path;
  - 65 members.

  Schema 3 also refuses under `vcs-observation-v2`.
- **`the_vcs_joins_read_the_top_level_and_every_member`** (evaluator): `VCS_KIND_JOIN` for schema 2 and 3; `VCS_MEMBER_JOIN` for a non-Git member and for a null `commitId`.

## Checks

Lane r2, `evidence/c1b0-checks-r2/` (the lane of record), on main `72e0787`, passed every check (`allPassed`). That main holds C1a4's accepted blind refresh (`0772eb7`) and D3a-1's code; both receipts are current there.
- **The suites, at base and candidate:** equal failure sets, with no isolated reruns needed:

  | Suite | Failures (base = candidate) | Passed (base → candidate) |
  | --- | --- | --- |
  | contracts | 0 | 0 → 0 |
  | identity | 0 | 72 → 72 |
  | host | 8 | 409 → 411 (2 new) |
  | storage | 33 | 137 → 137 |
  | evaluator | 0 | 47 → 48 (1 new) |
  | security | 14 | 1187 → 1187 |
- **rustfmt** on the edited, base-clean Rust files, and warning-denied all-targets Clippy on contracts, identity, host and evaluator;
- **the focused controls:** the two S4 host tests and the evaluator join test;
- **the generation's determinism:** the selected pipeline, re-run, reproduces the outputs byte for byte;
- **the design preflight:**
  - verify_design refuses only `generation source is not selected by accepted design`, for the package's identity-v3 copy;
  - with the two package copies accepted, it passes, with 43 generation sources and 52 admission sources, equal to the base;
  - the changed paths are exactly the fourteen;
- **the pre-binding refusals:** the public generator entry point and the public TypeScript checker refuse for exactly that reason;
- **the TypeScript lanes, with the copies accepted:** the report lane passes, and the generator lane's refusal equals the base's;
- **the census output checks** (discovery census, workspace ledger, snapshot census) pass over the regenerated records;
- **both receipts' stale state from the accepted baseline** (`check_c1b0_census_stale.py`, the regeneration's read-only `--verify`; and `evidence/census-regeneration.json`, the regeneration itself):
  - the baseline: both receipts are current on main, and both records render every held-out row `blind-census`, with `heldOutMargin: holds (blind census)`;
  - the deltas: the discovery receipt's is exactly the generator-closure digest (`e09d7bfe…` to `325fabbb…`), and the companion's is exactly that digest at its `discovery/reference` binding;
  - the outputs changed are exactly the two records. In `discovery_census.json` only `entries` (its held-out rows) and `heldOutMargin` change, and in `snapshot_ledger_census.json` only `heldOutEntries` and `heldOutMargin`. Each held-out row is now `outstanding: held-out (blind receipt stale)`, and both margins are `outstanding`;
  - both receipts are byte-equal to main's;
- **repository checks:** FW-01, the environment exceptions, the operability source census and the census-closure check;
- **four mutations,** each failing its named detector.

**After the lane (r2),** main moved by one lock-only commit, the v222 lock `0985273`, which changes only `design-lock.json`. The worktree moved onto it, and `evidence/c1b0-postlane-check-r2/` re-proved the candidate there: the census `--verify`, the design preflight, the generation determinism check, the operability source census and the three census output checks all pass. The subject's product base is `0985273` and its lane base `72e0787`.

Round 1's lanes (`c1b-0-r1/evidence/`) are history.

## Not delivered

- **The Git reads, the complete VCS term and its cap derivation:** C1b-1.
- **Sealing `kind: git` and schema 3, and the snapshot-level preservation controls:** C1b-2.
- **The batch's blind refresh:** after C1b-2 (LD-C1B-7).
- **The IDS architecture bundle's rewrite:** not owed (LD-C1B0-3).

## Not claimed

- No Git observation, no sealing, no caller, no qualification; C1b's completion is not claimed.

## Inventory

No new path. The edited paths are inventoried already.
