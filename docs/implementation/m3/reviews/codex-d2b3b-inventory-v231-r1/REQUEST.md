# Review request: D2B3B-inventory-v231 (the additive inventory successor for D2b-3b)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d2b3b-inventory-v231-r1/`).

## Boundaries

- Do not edit either repository, the stage or the control files.
- Do not run the compiler, Cargo, tests or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip`.

**This is inventory only, not a code re-review.** D2b-3b's code is closed: you accepted it in `docs/implementation/m3/reviews/codex-d2b-3b-r2/`, and it is integrated at `f16f50d4022c013055027072fcc7972afeb0c96b`.

## Subject

- **Stage:** `/tmp/opensip-implementation/d2b3b-inventory/architecture`
- **Subject manifest:** `docs/implementation/m3/supervisor-d/d2b3b-inventory-v231-subject.json`, 686 bytes, SHA-256 `093d8520f8106da3212c57a3e220c32518f41c86033d341cb20df8341687e10e`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v230.json`, 758386 bytes, `f815dabc6046b73fbaee8551c4900bf410bc919cf456113561abe057e5b97579`. It is the lock's last inventory successor (190 successors, 177 contract successors).
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v231.json`, 760618 bytes, `f93e6e821788f81dcefcffebeb715f18e096b154d16287c3e2d5ff44a78cfcd3`. Check that its path is the successor's (v231), not the parent's.
- **Record:** `docs/implementation/m3/supervisor-d/d2b3b-inventory-v231/successor.json`, 5841 bytes, `86227f4d62e624c3e0ead184d6942b8d8d7ae131611e4991b8597c62e7f19281`.
- **Product:** clean product main `f16f50d4022c013055027072fcc7972afeb0c96b`, holding D2b-3b's code commit `f16f50d4022c013055027072fcc7972afeb0c96b`. The architecture is at `d899cdf8a93bcacf5416a14f65962c8b0c2d4d67`.

## What to review

1. **Three added rows,** one for each new path of the accepted unit. None had a planned row.
   - `crates/components/src/provider_protocol/ts2/participant.rs` (opensip-components, adapter, generated false)
   - `crates/components/src/provider_protocol/ts2/send.rs` (opensip-components, codec, generated false)
   - `crates/components/src/provider_protocol/ts2_send_tests.rs` (opensip-components, test, generated false)

   Check that each row has an accurate package, role, `generated` flag and description, with no claim beyond the accepted unit.
2. **No realized planned row.**
3. **Inherited content:**
   - **Every inherited row is equal by value,** including the unit's three changed paths, whose inherited descriptions the lead judges still true:
     - `crates/components/src/provider_protocol/ts2.rs`: "M3-D unit D2b-3a (D2b plan r3 as amendments A1 and A2 amend it): the TS2 codec's receive side. Each worker frame takes the envelope, its closed schema, LD-D2B-15's contextual admission against the immutable DispatchContext (the echoes, LD-D2B-18's HelloAck exact echo with A2's descriptor fields, the stage correlation and batch counters, the candidate and anchor laws, the terminals' coverage) with every commitment recomputed over the received bytes, then the T2O table step, before conversion into the generated carriers; the TS2 depth bounds. Library only, with no caller."
     - `crates/components/src/provider_protocol/ts2_tests.rs`: "M3-D unit D2b-3a tests: a lawful TS2 session, each step's refusals before the table and before publication, the HelloAck echo, the stage correlation and batch counters, the candidate and anchor laws, the terminals' coverage with piecewise admission, every commitment recomputed over received bytes with the provenance control, and the depth bounds recomputed from the documents."
     - `crates/components/src/supervisor.rs`: "Supervise component lifetime, EOF/exit, cancellation and resource failures."

     `ts2.rs` gains the two modules, their re-exports and two read-only accessors on `Ts2Receiver` (`admits`, `terminal_kind`). `ts2_tests.rs`'s depth witness becomes a lawful Coverage frame. `supervisor.rs` gains `ParticipantStatus::HostFault` and its one `apply_step` arm.
   - the 20 packages and 9 pending decisions are unchanged;
   - all 91 planned, still-absent paths are retained without implementation claims;
   - the candidate is a sorted, unique strict superset;
   - every tracked product path is covered.
4. **The census closure:** D2b-3b changed no census-closure file (its lane's census-closure check). The inventory neither changes nor claims a census.
5. **The integration census:** the source check passes with 114 rows and no findings. The mint-audit census has 444 rows, unchanged. No mint authority is added.
6. **The successor record:**
   - the parent and candidate pins, and the unit's accepted review, subject and lead-assent pins, are exact;
   - `addedFiles`, `changedFiles`, `realizedPlannedFiles` and `inheritedPlannedFilesRetained` are exact;
   - no qualification is claimed.
7. **The bind** (for information): the lock commit appends inventory successor 191 and re-points every inherited passage row to v231. The contract successors stay at 177. The integrate script tolerates architecture advances on unrelated paths.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "093d8520f8106da3212c57a3e220c32518f41c86033d341cb20df8341687e10e",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v231.json",
    "bytes": 760618,
    "sha256": "f93e6e821788f81dcefcffebeb715f18e096b154d16287c3e2d5ff44a78cfcd3",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v230.json",
      "bytes": 758386,
      "sha256": "f815dabc6046b73fbaee8551c4900bf410bc919cf456113561abe057e5b97579"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/supervisor-d/d2b3b-inventory-v231/successor.json",
      "bytes": 5841,
      "sha256": "86227f4d62e624c3e0ead184d6942b8d8d7ae131611e4991b8597c62e7f19281"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
