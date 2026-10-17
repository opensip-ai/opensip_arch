# Review request: D3A3-inventory-v227 (the additive inventory successor for D3a-3)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3a3-inventory-v227-r1/`).

## Boundaries

- Do not edit either repository, the stage or the control files.
- Do not run the compiler, Cargo, tests or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip`.

**This is inventory only, not a code re-review.** D3a-3's code is closed: you accepted it in `docs/implementation/m3/reviews/codex-d3a-3-r2/` (round 2), and it is integrated at `2fbb7795aa4225f778e65cee2a72670b9f6a61d3`.

## Subject

- **Stage:** `/tmp/opensip-implementation/d3a3-inventory-v227/architecture`
- **Subject manifest:** `docs/implementation/m3/supervisor-d/d3a3-inventory-v227-subject.json`, 683 bytes, SHA-256 `adfff413234f308c9cd572d2b192e6b9cb30814b52f7d0b7f3d45d6a0a4dcd79`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v226.json`, 749747 bytes, `b88cc78de9e207c0957c9beeb5a2f433f918d8f712617fb9b620fcb5c309ce93`. It is the lock's last inventory successor (186 successors, 176 contract successors).
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v227.json`, 750594 bytes, `b68ecfec78cbd49b22b6af6c9fa360bfddc50b3ca060cee0738bffbd666f6519`. Check that its path is the successor's (v227), not the parent's.
- **Record:** `docs/implementation/m3/supervisor-d/d3a3-inventory-v227/successor.json`, 6218 bytes, `055ae1a0a813105557e6eb2a5f221571db590ae1040dd331fea5db88494aa18d`.
- **Product:** clean product main `2fbb7795aa4225f778e65cee2a72670b9f6a61d3`, holding D3a-3's code commit `2fbb7795aa4225f778e65cee2a72670b9f6a61d3`. The architecture is at `30915c1918956445f24dc141b01ec5304dcd30b9`.

## What to review

1. **One added row,** for the accepted unit's one new path. It had no planned row.
   - `crates/components/src/supervisor_records.rs` (opensip-components, module, generated false)

   Check that the row has an accurate package, role (`module`), `generated` flag and description, with no claim beyond the accepted unit.
2. **No realized planned row.**
3. **Inherited content:**
   - **Every inherited row is equal by value,** including the unit's fourteen changed paths, whose inherited descriptions the lead judges still true:
     - `Cargo.lock`: "Pin the host workspace dependency resolution for reproducible executable builds."
     - `crates/components/Cargo.toml`: "Declare this package, explicit dependencies and build targets."
     - `crates/components/src/supervisor.rs`: "Supervise component lifetime, EOF/exit, cancellation and resource failures."
     - `crates/components/src/supervisor_tests.rs`: "M3-D unit D3a-1 tests (D3a plan r4, sec. 3; review rounds 2 and 3): each drives the real readiness loop over the harness-free fixture child, located by the lane-written path and SHA-256, and a fixture participant built from D2b-1's FrameAcc…"
     - `crates/components/tests/supervisor_fixture.rs`: "M3-D unit D3a-1 (item 1; LD-D3A-9): the supervisor's first-party fixture child, a harness-free test target whose fd1 carries only the frames it writes; its scripts answer the control frames on fd3/fd4 and the provider frames on fd0/fd1 as e…"
     - `crates/operability/registry-events.json`: "O1-a safe operational records package implementation; exact accepted code unit; no qualification claim."
     - `crates/operability/registry-events.md`: "O1-a safe operational records package implementation; exact accepted code unit; no qualification claim."
     - `crates/operability/src/emit.rs`: "O1-a safe operational records package implementation; exact accepted code unit; no qualification claim."
     - `crates/operability/src/kinds/registry.rs`: "O1-a safe operational records package implementation; exact accepted code unit; no qualification claim."
     - `crates/operability/src/kinds/registry_tests.rs`: "O1-a safe operational records control; exact accepted code unit; no qualification claim."
     - `crates/operability/src/lib.rs`: "O1-a safe operational records package implementation; exact accepted code unit; no qualification claim."
     - `crates/operability/src/readback.rs`: "O1-a safe operational records package implementation; exact accepted code unit; no qualification claim."
     - `crates/operability/src/transport.rs`: "O1-a safe operational records package implementation; exact accepted code unit; no qualification claim."
     - `tools/operability/exceptions.json`: "O1-a source/call audit, source-pinned catalog or control tooling; exact accepted code unit."

     The O1-a rows (`registry.rs`, `emit.rs`, `readback.rs`, `lib.rs`, `transport.rs`, the registry references and tests, `exceptions.json`) are generic, and remain true of an O1 file with D3a-3's ordinary registrations. `supervisor.rs`'s planned role stays its role, now partly realized (cancellation is D3b's). The two D3a-1 rows (`supervisor_tests.rs`, `supervisor_fixture.rs`) name D3a-1's controls and scripts; since D3a-2 and D3a-3 they are incomplete, not false. The lead overrides only false descriptions; judge whether any is false.
   - the 20 packages and 9 pending decisions are unchanged;
   - all 93 planned, still-absent paths are retained without implementation claims;
   - the candidate is a sorted, unique strict superset;
   - every tracked product path is covered.
4. **The census closure:** D3a-3 changed no census-bound file (its lane's `census-closure-unchanged` check). The inventory neither changes nor claims a census.
5. **The integration census:** the source check passes with 114 rows and no findings. The mint-audit census has 444 rows, D3a-3's reviewed `registry.rs` rows included. No mint authority is added.
6. **The successor record:**
   - the parent and candidate pins, and the unit's accepted review, subject and lead-assent pins, are exact;
   - `addedFiles`, `changedFiles`, `realizedPlannedFiles` and `inheritedPlannedFilesRetained` are exact;
   - no qualification is claimed.
7. **The bind** (for information): the lock commit appends inventory successor 187 and re-points every inherited passage row to v227. The contract successors stay at 176. The integrate script tolerates architecture advances on unrelated paths.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "adfff413234f308c9cd572d2b192e6b9cb30814b52f7d0b7f3d45d6a0a4dcd79",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v227.json",
    "bytes": 750594,
    "sha256": "b68ecfec78cbd49b22b6af6c9fa360bfddc50b3ca060cee0738bffbd666f6519",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v226.json",
      "bytes": 749747,
      "sha256": "b88cc78de9e207c0957c9beeb5a2f433f918d8f712617fb9b620fcb5c309ce93"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/supervisor-d/d3a3-inventory-v227/successor.json",
      "bytes": 6218,
      "sha256": "055ae1a0a813105557e6eb2a5f221571db590ae1040dd331fea5db88494aa18d"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
