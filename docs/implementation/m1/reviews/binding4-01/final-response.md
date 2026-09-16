**Verdict: ACCEPT-UNIT, with no required findings and 6 non-blocking advisories.** Subject manifest SHA-256 is `8b21cac77b479b8d69c327b4aa01d26f32b45ca7ce9e8e4545dab20cec0235b0`. It covers the developer binding unit only; no integration or M1 completion is implied, and no future unit is approved.

**Integrity and scope**
- **Subject unchanged:** the manifest hash, all 4 file hashes and byte counts, and the exact file set match before and after. The review copy is byte-identical.
- **Baseline:** the live product tool, tests and lock match the accepted contract-binding-01 pins.
- **Verifier diff:** it adds `successor_chain` and the v4 field and dispatch lines, and changes the v2/v3 check from `>= 2` to `in (2, 3)`. Everything else is unchanged.
- **Tests and lock:** the 29 older tests are unchanged and 9 were added. The lock keeps the same pins, wrapped into chains, with an empty inheritance list.

**What I ran**
- **Tests:** 38/38 pass.
- **Real verification:**
  - The v4 lock passes against the architecture repo: 46 inputs, inventory3 (4 added files), metadata-v2 (9 candidates, 4 overrides), empty inheritance.
  - The accepted live v3 lock also still passes under the new verifier.
- **Why empty inheritance is correct:** the real row (`apps/cli/src/bootstrap.rs`) is at index 7 in both v1 and v3, so the v1 override matches the identical direct v3 override exactly. The real chain never shifts an index.
- **Synthetic probes, 46/46 as expected:** every fixture was fully rebound and refusals were matched on their error text, so an earlier digest failure can't hide a guard. They covered:
  - one-hop and two-hop reindexing
  - direct and ancestor conflicts
  - unsupported selectors
  - ordering, branches, cycles and reordered chains
  - reuse of an already-accepted path
  - earlier inventories and contracts still accepted as parents
  - versions 1–3 still passing and bad versions refused
- **Probes on a mirror of the real pinned files, 14/14 as expected:**
  - With the real v3 override removed from metadata-v2, the lock fails unless it lists the exact `/files/7` entry.
  - I added a synthetic reviewed v4 hop that moves `bootstrap.rs` from index 7 to 8. It needs exactly one `/files/8` entry (the v1 and v3 meanings merge) and leaves the v1 and v3 bytes unchanged.
- **Mutation testing, 24 mutants:** the tests kill 15 and my probes kill 22. Two mutants can never behave differently from the real code.

**Advisories**
- **B4-A01 (most important):** the 38 tests miss 7 behavior-changing mutants that my probes catch. Without these guards, all 38 tests still pass:
  - the inventory path-reuse guard, including its accepted-overlay check
  - the controlled refusal of unsupported selectors
  - the inherited-vs-direct and inherited-vs-inherited conflict checks (without the second, the last writer silently wins, which UNIT.md rules out)
  - the canonical sort
  - skipping the inheritance entry when an identical direct override exists

  The test named `…repeated_candidate_refuse` never tests a repeated candidate. The current code is correct, but add these tests before any lock uses a second hop or non-empty inheritance.
- **B4-A02:** conflicts are only caught when two overrides use the same selector. A line selector and a JSON Pointer can give the real inventory3 `bootstrap.rs` description two different meanings, and the lock still verifies. This would take two reviewed, assented records, so it isn't a present defect.
- **B4-A03:** the required inheritance order is lexicographic, so `/files/10` sorts before `/files/2`. It fails closed but isn't documented.
- **B4-A04:** an unhashable candidate path raises `TypeError` instead of a controlled `DesignError`; the CLI still exits 1.
- **B4-A05:** the "row changed" guard can't be reached, and the `seen` set is redundant with `accepted`. Both are harmless.
- **B4-A06:**
  - CB-A01 is resolved: path reuse is now refused against the whole accepted overlay.
  - CB-A02, CB-A04, CB-A05 and CB-A06 still apply.
  - CB-A03 is superseded by B4-A02.

**Limits:** all multi-hop and inheritance behavior was tested only with synthetic reviews and assents. I didn't reaudit the base approval, the content of inventory3 or metadata-v2, or the older v1–v3 guards.

Files are in `/tmp/opensip-implementation/m1-binding4-review-01`:
- `review.json`
- `review.md`
- `probe.py`
- `real_probe.py`
- `mutate.py`
- three result JSON files
- `copy/`
