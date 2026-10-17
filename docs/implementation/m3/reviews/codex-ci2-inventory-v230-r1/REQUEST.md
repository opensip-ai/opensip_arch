# Review request: CI2-inventory-v230 (the additive inventory successor for CI-2 + CI-3)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-ci2-inventory-v230-r1/`).

## Boundaries

- Do not edit either repository, the stage or the control files.
- Do not run the compiler, Cargo, tests or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, held-out entries, any T2 store or overlay, or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip`.

**This is inventory only, not a code re-review.** CI-2 + CI-3's code is closed: you accepted it, with amendment CI-A2, in `docs/implementation/m3/reviews/codex-ci-2-r2/`, and it is integrated at `d113fa735225c416e3c9e903e706aec3a2a435fd`.

## Subject

- **Stage:** `/tmp/opensip-implementation/ci2-inventory/architecture`
- **Subject manifest:** `docs/implementation/m3/component-install/ci2-inventory-v230-subject.json`, 690 bytes, SHA-256 `9e181c379b61cd999cf04490e5b97b4ec82a0fbda09ef7d23999eb29c1d50690`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v229.json`, 754454 bytes, `328fa865bd90e3867f115fb3dff8bed7af424f669bb94730f9ba3a2f2740beb9`. It is the lock's last inventory successor (189 successors, 177 contract successors).
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v230.json`, 758386 bytes, `f815dabc6046b73fbaee8551c4900bf410bc919cf456113561abe057e5b97579`. Check that its path is the successor's (v230), not the parent's.
- **Record:** `docs/implementation/m3/component-install/ci2-inventory-v230/successor.json`, 6172 bytes, `83707a6c49b1ce7cd61c39e27f7eef8be2c3e4da9b72ad54e380dd9ba663dd26`.
- **Product:** clean product main `f31206e9730cf764e0ce8fbb7ca4178aec8c72ff`, holding CI-2 + CI-3's code commit `d113fa735225c416e3c9e903e706aec3a2a435fd`. The architecture is at `ed27dad31b03ab86395876517c12dd5f19334e01`.

## What to review

1. **Five added rows,** one for each new path of the accepted unit that had no planned row:
   - `crates/lifecycle/src/installation_tests.rs` (opensip-lifecycle, test, generated false)
   - `crates/lifecycle/src/retained_tree.rs` (opensip-lifecycle, service, generated false)
   - `crates/lifecycle/src/retained_tree_tests.rs` (opensip-lifecycle, test, generated false)
   - `crates/platform/src/component_tree.rs` (opensip-platform, adapter, generated false)
   - `crates/platform/src/component_tree_tests.rs` (opensip-platform, test, generated false)

   Check each row's package, role, `generated` flag and description, with no claim beyond the accepted unit.
2. **One realized planned row:** `crates/lifecycle/src/installation.rs`, inherited unchanged: "Stage and publish authorized immutable component generations.". Judge whether that inherited description is true of the module. It holds the component store, the installer transaction (staged, verified, finalized and funded), and the tree model and walk that CI-3's reader shares.
3. **Inherited content:**
   - **Every inherited row is equal by value,** including the unit's ten changed paths, whose inherited descriptions the lead judges still true:
     - `Cargo.lock`: "Pin the host workspace dependency resolution for reproducible executable builds."
     - `crates/lifecycle/Cargo.toml`: "Declare this package, explicit dependencies and build targets."
     - `crates/lifecycle/src/lib.rs`: "Expose the intentionally public API; keep internal modules private."
     - `crates/lifecycle/src/locations.rs`: "Construct closed relative namespace, store and paired ledger locations with independent namespace/store scope. Syntax and borrowing do not establish admitted bindings or leases."
     - `crates/platform/src/lib.rs`: "Expose the intentionally public API; keep internal modules private."
     - `crates/security/src/component_closure.rs`: "M3-C r8 items 7 and 8 (unit C2a-1; C2a plan r4): one verified component's unadmitted ClosureCandidate. The platform join to the catalog token and the same release's artifact, CR-1's kind, the regular-file projection, a charged bottom-up merge sort and duplicate pass, C2PM-1's presence check and four ordered guards with carried origins and the role support table, the exact protocolMajor copy, and the descriptor predicted, bounded, hand-encoded at its exact length and admitted against identity-v3's closure definition, with published WorkCost prices. A candidate authorizes no context, Plan, worker or selection; admission is C2a-3's after retention."
     - `crates/security/src/crash_matrix_sites.rs`: "X9-1's pin of every source site that names a test-only feature (law X9 r1 item 6, law X8 r3 item 4b), in every security test build: it scans every cfg and cfg! in crates/*/src and crates/*/tests and requires exactly the pinned table, the shared fixture gates under the one joint predicate any(test, feature = crash-matrix, feature = scenario-fixtures) (Image::Injected with the injected image and synthetic V2 profile set, HomeSource::Fixture with the creator path on a scratch H and the gate's test constructor, X4T-0 and its accessor, and the fenced state.v1 publisher, each with the closure it needs), the crash-matrix-only carrier fixtures, each crate's guard and support module, the census tests and X9-0's and X9 r2's platform sites; with a scanner self-test, a no-sleep pin over X9-1's sources, and tests of the shared producers (accepted trust installed, the fenced publisher advancing the revocation version and refusing without writing while another holder has the fence, a writer admitted) and of the inherited carrier fixture."
     - `crates/security/src/lib.rs`: "Expose admitted security services and opaque authority-session types with private constructors; never expose an unchecked operational grant or journal checkpoint."
     - `crates/security/src/trust.rs`: "Admit signed trust metadata, root chains and closure associations."
     - `crates/security/src/trust_admitted_components.rs`: "M3-C r8 item 7 (unit C2a-1): the trust owner's read-only bridge to the components the ordinary reader verified. Each AuthenticatedComponent lends its authenticated body bytes, verified envelope, validated manifest, CR-1 kind and catalog release row by reference; only the trust owner constructs one, and it authorizes nothing. A test holder runs real body validation with test release and envelope stand-ins."

     The changes:
     - `Cargo.lock` gains one internal edge;
     - lifecycle's `Cargo.toml` gains the security edge and the forwarded fixture features;
     - lifecycle's `lib.rs` gains the two public modules and the crash-matrix guard;
     - `locations.rs` gains the component store's name;
     - platform's `lib.rs` declares `component_tree`;
     - `component_closure.rs` and `trust_admitted_components.rs` widen C2a-1's types to `pub`, and `TestComponent` moves under the joint fixture predicate;
     - `trust.rs` and security's `lib.rs` re-export them;
     - `crash_matrix_sites.rs` pins shared gates 7 and 8, and lifecycle's guard, by name.

     Judge in particular whether `crash_matrix_sites.rs`'s parenthetical list of gates, and `trust_admitted_components.rs`'s "a test holder" sentence, stay true as summaries.
   - the 20 packages and 9 pending decisions are unchanged: lifecycle's opensip-security edge was already permitted;
   - all 91 planned, still-absent paths are retained without implementation claims;
   - the candidate is a sorted, unique strict superset;
   - every tracked product path is covered.
4. **The census closure:** CI-2 + CI-3 changed no census-bound file (its lane's `census-closure-unchanged` and `receipt-inputs-unchanged` checks). The inventory neither changes nor claims a census.
5. **The integration census:** the source check passes with 114 rows and no findings. The mint-audit census has 444 rows, unchanged. No mint authority is added.
6. **The successor record:**
   - the parent and candidate pins, and the unit's accepted review, subject and lead-assent pins, are exact;
   - `addedFiles`, `changedFiles`, `realizedPlannedFiles` and `inheritedPlannedFilesRetained` are exact;
   - no qualification is claimed.
7. **The bind** (for information): the lock commit appends inventory successor 190 and re-points every inherited passage row to v230. The contract successors stay at 177. The integrate script tolerates architecture advances on unrelated paths.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "9e181c379b61cd999cf04490e5b97b4ec82a0fbda09ef7d23999eb29c1d50690",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v230.json",
    "bytes": 758386,
    "sha256": "f815dabc6046b73fbaee8551c4900bf410bc919cf456113561abe057e5b97579",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v229.json",
      "bytes": 754454,
      "sha256": "328fa865bd90e3867f115fb3dff8bed7af424f669bb94730f9ba3a2f2740beb9"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/component-install/ci2-inventory-v230/successor.json",
      "bytes": 6172,
      "sha256": "83707a6c49b1ce7cd61c39e27f7eef8be2c3e4da9b72ad54e380dd9ba663dd26"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
