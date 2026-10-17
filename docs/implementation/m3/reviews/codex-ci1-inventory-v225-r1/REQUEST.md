# Review request: CI1-inventory-v225 (the additive inventory successor for CI-1)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-ci1-inventory-v225-r1/`).

## Boundaries

- Do not edit either repository, the stage or the control files.
- Do not run the compiler, Cargo, tests or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only hashing, JSON parsing, Git queries, and `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip`.

**This is inventory only, not a code re-review.** CI-1's code is closed: you accepted it in `docs/implementation/m3/reviews/codex-ci-1-r2/`, and it is integrated at `f05c5d5cda5f68aec607cdc8731c277e4e29491b`.

## Subject

- **Stage:** `/tmp/opensip-implementation/ci1-inventory-v225/architecture`
- **Subject manifest:** `docs/implementation/m3/component-install/ci1-inventory-v225-subject.json`, 690 bytes, SHA-256 `77e3baa0e9cdd2191a314593d69cbed8222e4efa9ab19ae8251e8ee9d84f0509`. Its three members are the candidate, the integration census and the successor record.
- **Parent** (architecture): `docs/implementation/m2/repository-file-inventory.v224.json`, 746712 bytes, `0756b1995b06d1ecb3bdcca948e2703a0f7ea74788ce0cb173effbc3af50ebb7`. It is the lock's last inventory successor (184 successors, 176 contract successors).
- **Candidate:** `docs/implementation/m2/repository-file-inventory.v225.json`, 748353 bytes, `09a8382a73b2dc35b43baafc5d359ba63a51283b23f00313607b517aa5935088`. Check that its path is the successor's (v225), not the parent's.
- **Record:** `docs/implementation/m3/component-install/ci1-inventory-v225/successor.json`, 5763 bytes, `fcf885d4ee6b8124816eb843aa45ebe4f8719046cfeff4df0cb9a7265a51ad3b`.
- **Product:** clean product main `f05c5d5cda5f68aec607cdc8731c277e4e29491b`, holding CI-1's code commit `f05c5d5cda5f68aec607cdc8731c277e4e29491b`. The architecture is at `90888628b8d833b0cdb973cae765d3d8b85d2b0b`.

## What to review

1. **Two added rows,** one for each new path of the accepted unit. Neither had a planned row.
   - `crates/security/src/archive_profile.rs` (opensip-security, codec, generated false)
   - `crates/security/src/archive_profile_tests.rs` (opensip-security, test, generated false)

   Check that each row has an accurate package, role, `generated` flag and description, with no claim beyond the accepted unit.
2. **No realized planned row.**
3. **Inherited content:**
   - **Every inherited row is equal by value,** including the unit's two changed paths, whose inherited descriptions the lead judges still true:
     - `crates/security/src/crash_matrix_sites.rs`: "X9-1's pin of every source site that names a test-only feature (law X9 r1 item 6, law X8 r3 item 4b), in every security test build: it scans every cfg and cfg! in crates/*/src and crates/*/tests and requires exactly the pinned table, the shared fixture gates under the one joint predicate any(test, feature = crash-matrix, feature = scenario-fixtures) (Image::Injected with the injected image and synthetic V2 profile set, HomeSource::Fixture with the creator path on a scratch H and the gate's test constructor, X4T-0 and its accessor, and the fenced state.v1 publisher, each with the closure it needs), the crash-matrix-only carrier fixtures, each crate's guard and support module, the census tests and X9-0's and X9 r2's platform sites; with a scanner self-test, a no-sleep pin over X9-1's sources, and tests of the shared producers (accepted trust installed, the fenced publisher advancing the revocation version and refusing without writing while another holder has the fence, a writer admitted) and of the inherited carrier fixture."
     - `crates/security/src/lib.rs`: "Expose admitted security services and opaque authority-session types with private constructors; never expose an unchecked operational grant or journal checkpoint."

     Security's `lib.rs` gains one public module, `archive_profile`, appended. `crash_matrix_sites.rs` gains shared gate 6 by name: `archive_profile.rs` under the joint predicate, two sites, with its module-doc entry. Its inherited description names the shared fixture gates' kinds parenthetically; gate 5 was already not named there. Judge whether the description, read as a summary, stays true with gate 6, or whether it needs a changed row.
   - the 20 packages and 9 pending decisions are unchanged;
   - all 93 planned, still-absent paths are retained without implementation claims;
   - the candidate is a sorted, unique strict superset;
   - every tracked product path is covered.
4. **The census closure:** CI-1 changed no census-bound file (its lane's `census-closure-unchanged` and `receipt-inputs-unchanged` checks). The inventory neither changes nor claims a census.
5. **The integration census:** the source check passes with 114 rows and no findings. The mint-audit census has 439 rows, unchanged. No mint authority is added.
6. **The successor record:**
   - the parent and candidate pins, and the unit's accepted review, subject and lead-assent pins, are exact;
   - `addedFiles`, `changedFiles`, `realizedPlannedFiles` and `inheritedPlannedFilesRetained` are exact;
   - no qualification is claimed.
7. **The bind** (for information): the lock commit appends inventory successor 185 and re-points every inherited passage row to v225. The contract successors stay at 176. The integrate script tolerates architecture advances on unrelated paths.

## Output

`review.json` must carry the following, with your independently checked values, plus `nonBlockingObservations`:

```json
{
  "verdict": "ACCEPT-UNIT",
  "requiredFindings": [],
  "subjectManifestSha256": "77e3baa0e9cdd2191a314593d69cbed8222e4efa9ab19ae8251e8ee9d84f0509",
  "productQualification": false,
  "inventoryCandidateAssessment": {
    "verdict": "ACCEPT",
    "requiredFindings": [],
    "path": "docs/implementation/m2/repository-file-inventory.v225.json",
    "bytes": 748353,
    "sha256": "09a8382a73b2dc35b43baafc5d359ba63a51283b23f00313607b517aa5935088",
    "parent": {
      "path": "docs/implementation/m2/repository-file-inventory.v224.json",
      "bytes": 746712,
      "sha256": "0756b1995b06d1ecb3bdcca948e2703a0f7ea74788ce0cb173effbc3af50ebb7"
    },
    "successorRecord": {
      "path": "docs/implementation/m3/component-install/ci1-inventory-v225/successor.json",
      "bytes": 5763,
      "sha256": "fcf885d4ee6b8124816eb843aa45ebe4f8719046cfeff4df0cb9a7265a51ad3b"
    }
  }
}
```

The lead gives its own assent, then publishes the architecture record. The separate lock commit binds the inventory successor, with fresh verify_design. Nothing is pushed.
