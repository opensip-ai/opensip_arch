# CODEX2 Review — SECURITY-BASELINE r1

## Verdict

**ACCEPT-UNIT**

This acceptance is limited to the frozen three-path, test-only repair. It does not integrate the unit, bind the new fixture into inventory, waive the seven ignored controls, or qualify the product.

## Package and authority verification

The subject manifest is 13,479 bytes with SHA-256 `b05c7773c58f5d00f8d8e5f86b19e7fa1bbc3ff748b0068179f06888c2e4b72e`. All 56 declared members match their byte counts and SHA-256 values, with no missing or undeclared stage member.

The six frozen architecture authorities match architecture commit `f603fe0948320cc43e4cb9e2c10965368fd192e0`. They establish independent acceptance and integration of the current host replay corpus, its inventory-v182 binding, and D3b-2 at product commit `c436c2cc98837c8771a6e9a9a00cbc3874cc1d29`. All nine product authorities match that product commit, including the accepted current host fixture at SHA-256 `a71dde8e9a57cbe0576a283c5b6e83bf494acb4dc2435b16a488a717450ed6ef`. The product design lock is 710,140 bytes with SHA-256 `54f84f2fd1cea35dd438cd9b3d8626bc4825aeefd296ad4e8882becead767817`.

The exact three-row product map is sound. Both existing Rust parents match the product base, the new fixture is absent there, and all three candidate pins match their archived members. `product.diff` contains exactly those three paths and three hunks. It adds no dependency, production path, schema registration, recipe, guard, parser limit, or public API.

## Current replay companion

The historical journal `replay.case` is value-identical to the historical host's sole `packet-0-original` case. Its object and blob pools are exactly the case's 23 and 46 selected historical entries, with no omitted or extra key. The unchanged historical journal document still contains all 321 record cases, and the historical host, journal, and accepted current host fixture bytes all match their product-base pins.

The new companion's complete `case` is value-identical to the accepted current host's sole `packet-0-original` case, including run ID `run3:36e5b6298464492386aa5ca8f4f2d2db12c03c9f817518da8069015b3e77e6c0`, ordered selections, and expected result. Its object pool is exactly the 23 selected current-host object values, and its blob pool is exactly the 46 selected current-host blob values. Both key sets have no extra or missing member.

Only `journal_store::fixtures::replay`, inside the existing `#[cfg(test)]` module, selects the companion. `fixture()` continues to select the historical journal document. The replay helper still constructs `RegisteredSchemas` from the registered current source requirements, converts the selected object and blob values into retained inputs, applies the unchanged traversal, owner-invocation, capture-entry, and retained-byte limits, and calls the real evaluator to produce an owned `ReplayedRun`. The 814,277-byte companion remains below the unchanged 4 MiB JSON limit. Production journal source before the test-only fixture module is byte-identical to the product base.

## Settlement guard and preflight finding

`SECBASE-PRE-R1-RF-1` is closed. The supervisor exemption now recognizes only a trimmed full line equal to `self.settle();`; the tar exemption recognizes only `self.settle()?;`. Their exact private signatures occur once, their accepted call lines occur exactly three and two times, and the complete non-comment `.settle(` totals in those files are also three and two. A different receiver therefore cannot occupy an exempt slot while preserving both checks.

The four source-level negatives replace one accepted call with `myself`, `not_self`, `ledger`, and `éself`. Each preserves the private signature and total `.settle(` count while reducing the exact helper count by one. This directly covers identifier suffixes, the production ledger spelling, and a non-ASCII prefix that defeated broader substring reasoning.

There is no blanket file exemption: each supervisor or tar row is removed from the global settlement map only after its signature, exact helper-line count, and total occurrence count pass. The existing global assertions still require the sole production `.reserve_settlement(` and `.ledger.settle(` calls in `initial_installation.rs`; nine ordinary-writer settlement calls plus its private helper signature; and the three exact reserve/settle wrapper locations. The candidate changes no production settlement code.

## Validation evidence

The initial lane used separate rebuilt test artifacts for current main and the candidate. The exact selected set reproduced 0 passes and 14 failures on current product `c436c2cc98837c8771a6e9a9a00cbc3874cc1d29`, then passed 14/0 on the candidate. The complete candidate security library passed 1,291 tests with zero failures and seven ignored controls; six doctests passed; and all-target Clippy with warnings denied passed.

Both final mutations caused fresh recompilation and failed at runtime as required. Restoring the historical replay selector failed the two real seal-binding controls. Restoring the unbounded `self.settle(` substring matcher failed the preserved-total receiver control. The runner restored all three exact source pins, rebuilt, and passed the selected 14 again. The frozen candidate worktree and archived source currently match those same three pins.

The workspace all-target check, security fixture-feature check, environment-exception controls, operability source and lock checks, receipt-input non-overlap check, and design verification all exited successfully. The historical full result of 1,277 passes, 14 failures, and seven ignored controls is correctly labeled as evidence from product `09e302f6bdfc195b9e0b193bafcdc8bf1979dbb9`; the package does not present it as a new whole-suite run of current main. No private fixture, held-out, T2, census, or qualification result is inferred.

## Non-blocking observations

### SECBASE-R1-NBO-1 — Bind the new fixture after integration

The new `crates/security/tests/fixtures/journal-seal-replay.current.json` path needs an additive inventory successor after this exact accepted code is integrated. No inventory binding exists for it yet.

### SECBASE-R1-NBO-2 — Preserve the distinct ignored-control lanes

The seven unchanged ignored tests remain assigned to their documented helper, T2 reconstruction, and real-host clock lanes. This unit's acceptance supplies no waiver or platform, custody, or project qualification for them.
