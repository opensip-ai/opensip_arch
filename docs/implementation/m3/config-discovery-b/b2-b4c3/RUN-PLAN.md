# B2-b4c3: the blind held-out receipt refresh (pre-run gate)

**Lead record, 2026-10-16. For Codex's pre-run review; nothing has been run.** This is the remediation that Codex's B3-b plan review (`codex-b3b-plan-r1`, NBO-1) found was needed.

## What went wrong

The B2-b4c blind receipt (`crates/security/src/custody/discovery_census_held_out.json`) binds its reference-loading code, which includes `tools/contracts/generator-closure.json`. Unit **S10-TSC** (product `25d0f79`) re-pinned four schema rows of that file: `schemas/source-map.json` and `schemas/sources/common-v{1,3,4}.schema.json`. The receipt therefore became stale, and since lock `1f70dba` the ordinary census `--check` fails on main:
- exactly the ten held-out rows read `outstanding: held-out (blind receipt stale)`;
- `heldOutMargin` reads `outstanding`;
- every lead-readable and workspace row is unchanged.

The S10-TSC and B2-c2 lanes did not run the census check, so the regression went unnoticed. The lead records it as its own miss. Status r101's statement that "the 2× margin holds for every repository entry" has not been backed by a current receipt since `1f70dba`. The next status round corrects it, whatever this refresh yields.

## Evidence that the drift is inert (`evidence/drift.json`)

Every receipt binding is compared with the current bytes:
- **The only drifted file binding** is `tools/contracts/generator-closure.json`.
- **Its changed rows** are the four schema rows above.
- **No `tools/contracts/python-packages/` row changed.** Those rows pin the only part of that file the reference loading uses.
- **Its other keys are equal.**
- **Unchanged:** the census tool (`6ea8a1ab…`, the reviewed B2-b4c1 bytes), the whole cost closure, the manifest, the sizes, the limits, the root lengths and every other reference row.

## The run (`evidence/run_b2b4c3_blind.py`), once, after this gate is accepted

1. **A detached worktree of product main** (`opensip-b2b4c3`), clean. The tool's bytes are asserted equal to the reviewed `6ea8a1ab…`.
2. **The stale receipt is removed in that worktree only.** The reviewed `--held-out-blind` mode runs exactly once. The lead sees only its one-line summary, its exit code and stderr, which must be empty. The method and the population are the owner's of 2026-10-16, unchanged.
3. **The ordinary mode** runs `--write`, then `--check`.
4. **The recorded comparison:**
   - the new receipt's rows, state and standing against the old receipt's;
   - which bindings changed (expected: `reference` only, its generator-closure row);
   - whether the regenerated census record is byte-identical to main's committed one.

   **Expected:** rows equal, the state still `holds (blind census)`, and the census record byte-identical, so the product change is the receipt file alone.
5. **If any row differs, or the run errors,** nothing is committed. The result goes to Codex and the owner as data, and the held-out margin is recorded as outstanding.

**After the run:** Codex's post-run review of the receipt and the composed census. Then the lead's assent, a product commit of the receipt, and the B3-b plan r2. Inventory is unchanged, because the path exists.

## Not claimed

- No held-out content is opened or disclosed beyond the owner's allowlist.
- No new method, population or access.
- No change to the tool or the closure.
