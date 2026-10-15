# Review request: B2-B3C-r1 (the seam and the flag rows; M3-B unit B2-b3, sub-unit B2-b3c)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b2b3c-r1/`).

## Boundaries

Do not edit either repository, the worktree, the stage or the control files. Do not run Cargo, rustc, tests, builds or the lane. No network. Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry. Do not use other panes and do not delegate.

Read-only reading, hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository <tree>`, `tools/tests/test_environment_exceptions.py` and `tools/tests/test_discovery_fw01.py` in the candidate worktree are permitted.

## Subject

- **Stage.** `/tmp/opensip-implementation/b2b3c-r1-stage`
- **Subject manifest.** `docs/implementation/m3/config-discovery-b/b2-b3c-r1-subject.json`: 6390 bytes, SHA-256 `7cc7c41e5e4ce2dc92e3580eb55732c78f2595b4550b1a6c5e24b3f243c2a9b7`, 29 members. Rehash every member.
- **Bases.**
  - Product `aa037d09995f7710bda5f8993ff9133f829e3df3`, clean: B2-b3b is bound, inventory is v194, contract successors are 164.
  - Architecture `4d30d0a00473179625cf9403d208531cd0746666`: the B2-b3 plan r3 is published.
  - The candidate worktree `/Users/sb/code/opensip-ai/opensip-b2b3c` holds the exact bytes of `product-map.json`.

## Authority

- The accepted B2-b3 plan r3 (`codex-b2b3-plan-r3`): LD-B2B3-12 as amended.
- COV:5268-5407, the flag rows' method.
- X8 r3 item 4b and unit X9-1's site pin (`crates/security/src/crash_matrix_sites.rs`).
- The shared installation fixture's composition (`custody/installation_read_fixture.rs`, `InstallationAt::operation`).
- B2-b3a's `UpwardRecord` and B2-b3b's `discover_downward`, as bound.
- `source.json` pins them.

## What to review

`SCOPE.md` describes the unit. Judge:
1. **The seam's order and gates.**
   - Does `ScenarioHome::discover` follow LD-B2B3-12 (r3) exactly? Phase 1 with the explicit path, the typed waiver and the upward record; resolution over the captured carriers; item 5 with the waiver; tracking, first registration and `begin_operation` as `InstallationAt::operation` takes them; `discovery_root`; the walk and the core on a fresh discovery ledger, with the source chosen before traversal; `end`.
   - Does it reach only fixture gates that X8 names, and add no feature site that X9-1's pin would reject?
   - Is taking the invoking uid from the scratch home's owner sound for a test seam?
2. **The records.** Are they plain values that lend no authority? Is a refusal mapped through `UpwardRecord::discovery_refusal` and `WalkRefusal::discovery_refusal` only, with every other refusal `Err`?
3. **The flag rows.** Does each test meet COV:5288's and COV:5388's method, as plan r3 lists it?
   - Applicability and exact selection.
   - The waiver's reach.
   - Configuration never impersonating explicit consent.
   - The flag layer's precedence and provenance.
   - No fall-through.
   - The configuration alone and neither.
   - A resolution refusal stopping before item 5 and the walk.
   - Nothing lent.
4. **Placement.** Is the host unit-test module, declared `cfg(all(test, target_os = "macos"))` in `lib.rs` (B1-a's source pin holds `configuration.rs`'s own test includes exactly, so it does not join that module), sound, with `configuration.rs` unchanged?
5. **Evidence.**
   - `evidence/checks.json`, `test-comparison.json`, `legacy-probe.json` and `controls.json`.
   - Equal failure sets, with at least seven new host tests passing.
   - Clippy.
   - rustfmt, with its classification.
   - The pins, the vector checks, the census and verify_design.
   - The five mutations, each caught.
6. **Scope.** There is no production caller, public composition, export, environment read or law change, and the paths are exactly the product map's.

## Output

`review.json` must carry `nonBlockingObservations` and these fields, with your independently checked values:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "7cc7c41e5e4ce2dc92e3580eb55732c78f2595b4550b1a6c5e24b3f243c2a9b7",
  "implementsPlanR3Ld12": true,
  "seamOrderSound": true,
  "seamWithinX8Gates": true,
  "noNewFeatureSite": true,
  "flagRowsMeetCovMethod": true,
  "resolutionRefusalStopsBeforePhase2": true,
  "recordsLendNothing": true,
  "testFailureSetsEqualBase": true,
  "allTargetsClippyWarningsDenied": true,
  "controlsCaught": 5,
  "inventoryUnchanged": 194,
  "contractSuccessorsUnchanged": 164,
  "productionCallerAdded": false,
  "environmentReadAdded": false,
  "productQualification": false,
  "entirePlanComplete": false
}
```

The lead then gives its own assent and publishes the architecture record. Then comes the product code commit, and then the inventory successor (the one new path), reviewed and bound separately. Nothing is pushed.
