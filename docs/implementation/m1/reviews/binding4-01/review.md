# Independent review: design-lock v4 successor chains

**Verdict: ACCEPT-UNIT.** There are no required findings.

- **Subject manifest SHA-256:** `8b21cac77b479b8d69c327b4aa01d26f32b45ca7ce9e8e4545dab20cec0235b0`. It was checked before and after the review.
- **Scope:** only the developer design-binding unit. This review does not cover integration, runtime authorization or product qualification. It does not imply M1 completion and does not approve any future unit.

## What was verified

**Subject integrity**
- The manifest hash, all 4 file hashes and byte counts, and the exact file set match both before and after the review.
- The review copy is byte-identical to the subject and contains no bytecode.

**Baseline**
- The live product files are the accepted binding3. Their hashes equal the pins in the contract-binding-01 subject.
- The verifier diff is additive:
  - It adds `successor_chain`, the v4 fields and the v4 dispatch.
  - The v2/v3 check changed from `version >= 2` to `version in (2, 3)`.
  - Every other function is byte-identical.
- The test diff only adds lines: 29 original tests plus 9 new chain tests. The lock diff only wraps the existing pins into one-element chains and adds an empty `inventoryPassageInheritance`.

**Tests and real verification**
- 38 of 38 tests pass (Python 3.14.6).
- The real v4 lock verifies with 46 inputs. It selects inventory3 (4 added files) and metadata-v2 (9 candidates, 4 overrides), with empty inheritance and `productQualification=false`.
- The accepted live v3 lock also verifies under the new verifier.
- The output digest is unchanged after all probes, and `--architecture .` fails closed.

**Real data**
- In v1, `files[7]` is `apps/cli/src/bootstrap.rs`. It is still at index 7 in inventory3, because the four additions sort after it.
- So the metadata-v2 v1 override projects exactly onto its identical direct v3 override, and the empty inheritance list is correct.
- The real chain never shifts an index.

**Synthetic probes: 46 of 46 expectations met**

Every fixture is fully rebound, and each refusal is matched on its diagnostic text, so an earlier digest failure cannot hide a guard. The probes covered:
- one-hop and two-hop reindexing
- omitted, stale, redundant and extra inheritance entries
- direct final overrides, identical and conflicting
- ancestor overrides that agree or conflict
- unsupported ancestor selectors (line, `/standing`, `/files/N/role`, `/packages/0/id`)
- lexicographic order
- reordered hops, branches and cycles
- path reuse against the accepted overlay, inventory candidates, and earlier contract members and records
- base, intermediate and final inventories, plus earlier contracts, as later parents
- forward parents
- malformed chains
- compatibility for v1, v2 and v3, and refusal of bad versions

**Real-mirror probes: 14 of 14 met**

These ran on a temporary mirror of every pinned file; the architecture repo was only read.
- **Removing the real v3 override:** with the direct v3 override removed from metadata-v2, the lock refuses unless it carries the exact projected `/files/7` entry. Giving v3 a conflicting meaning also refuses.
- **Synthetic reviewed v4 hop:** it moves `bootstrap.rs` from index 7 to 8.
  - It refuses with no inheritance entry or with the stale index 7.
  - It verifies with the single `/files/8` entry; the v1 and v3 meanings collapse into one.
  - The v1 and v3 bytes stay unchanged.
- **Later units:**
  - They can use as parents v1, v3, v4, the metadata-v2 member file and its record.
  - A member at a path already in the accepted overlay refuses.
  - A conflicting direct override on v4 refuses; an identical one replaces the inheritance entry.
  - A `/standing` override on real v1 refuses as unsupported.

**Mutation testing: 24 mutants**
- The 38 tests kill 15.
- The independent probes kill 22, including all 7 behavior-changing mutants that the tests miss.
- 2 mutants are equivalent: no input can make them behave differently.

## Advisories (non-blocking)

- **B4-A01: the tests do not isolate several key v4 guards.** These removals pass all 38 tests:
  - the inventory-candidate reuse guard, including its accepted-overlay check (M02, M03)
  - the unsupported-selector refusal (M07)
  - the inherited-vs-direct conflict check (M09)
  - the inherited-vs-inherited conflict check (M10); without it the last writer silently wins, which UNIT.md rules out
  - the canonical sort (M11)
  - suppression of the entry when an identical direct override exists (M15); only the real lock catches this one

  `test_inventory_branch_and_repeated_candidate_refuse` never tests a repeated candidate. Current behavior is correct. Add isolated tests before any lock uses a second hop or non-empty inheritance.
- **B4-A02: selector aliasing.** "Differing meanings for the same passage refuse" only holds when both overrides use the exact same selector. A line selector and a JSON Pointer can give the real inventory3 `bootstrap.rs` description two different meanings, and the lock still verifies (probe R13). Only reviewed, assented records could do this. Narrow the wording or require pointers for JSON parents.
- **B4-A03: undocumented order.** The canonical inheritance order is lexicographic by selector JSON, so `/files/10` sorts before `/files/2`. This fails closed but is not documented.
- **B4-A04: uncontrolled exception.** An unhashable candidate path raises `TypeError`, not `DesignError`. The CLI still exits 1.
- **B4-A05: equivalent mutants.** The "row changed" guard is unreachable under the additive profile, and `seen` is always a subset of `accepted`.
- **B4-A06: carried advisories.**
  - CB-A01 is resolved: reuse now refuses against the whole accepted overlay.
  - CB-A02, CB-A04, CB-A05 and CB-A06 still apply; that code is unchanged.
  - CB-A03 is superseded by B4-A02.
  - CB-A07's older mutation survivors remain.

## Limits

- The multi-hop and inheritance behavior was exercised only with synthetic reviews and assents.
- No base reaudit was done, and the substance of inventory3 and metadata-v2 was not reaudited.
- The architecture working tree has unrelated uncommitted changes; verification relies on the exact pins.
- The older v1–v3 guards were not re-mutated.
- Artifacts in this directory: `probe.py`, `probe-results.json`, `real_probe.py`, `real-probe-results.json`, `mutate.py`, `mutation-results.json` and the byte-identical review copy `copy/`.
