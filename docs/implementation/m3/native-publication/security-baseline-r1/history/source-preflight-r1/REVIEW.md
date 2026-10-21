# CODEX2 Review — Security Baseline Test-Only Source Preflight r1

## Verdict

**REQUIRED-FINDINGS**

## Required findings

### SECBASE-PRE-R1-RF-1 — Match the exempt helper receiver exactly

The revised settlement guard claims that every `.settle(` occurrence in `components/src/supervisor.rs` and `host/src/archive_decoder/tar.rs` is one of the file's exact private `self.settle` helper calls. It establishes that by counting every `.settle(` and separately summing `line.matches("self.settle(")` (`product/crates/security/src/custody/commit_session_tests.rs:938-960`). The second pattern has no lexical boundary before `self`, so it also matches a different receiver whose identifier ends in `self`, such as `myself.settle(` or `not_self.settle(`.

That creates a concrete false acceptance. One existing helper call can be replaced by a direct or unrelated settlement through a receiver named `myself`; the total `.settle(` count remains three or two, the supposed `self.settle(` count also remains three or two, the private helper signature remains present, and both assertions pass. A production ledger receiver can therefore occupy an exempt slot without containing the separately guarded `.ledger.settle(` spelling. This contradicts the scope's requirement that the exemptions be precisely the existing `self` helper calls and creates an implicit path exemption.

Count an exact `self` receiver with a token boundary, or compare every non-comment `.settle(` occurrence in each exempt file against the exact accepted helper-call forms/locations. Add negative controls using at least `myself.settle(` and another non-`self` receiver while preserving the total count, and require both to fail the guard. Keep the exact private signatures and the existing global ledger, reserve, wrapper, and ordinary-writer counts.

## Scope and evidence review

The frozen subject manifest is 2,699 bytes with SHA-256 `35e8bf19d32f0743734f8e108c22ac5522206a462a318259a283035a70a99830`. All 14 declared members match their recorded byte counts and SHA-256 values. All nine product authorities match product commit `09e302f6bdfc195b9e0b193bafcdc8bf1979dbb9`, and all five architecture authorities match architecture commit `9e89627bef006ab33e1f1036898653e55c0d5fc1`; those commits are the current repository heads. The two tracked parent files match the product base, their candidates match the archived members, and the declared new fixture is absent from the base and matches its candidate/archive pin. The tracked diff changes only the two declared Rust test paths; the map separately and correctly records the untracked fixture path.

The frozen baseline log records 1,277 passing security tests, 14 failures, seven ignored tests, and six passing doctests. Thirteen failures reach `journal_store::fixtures::replay`; the remaining failure is the old settlement caller-set assertion. This is baseline evidence only. The candidate has not been compiled or tested, and I did not run any test, build, Cargo, or lane command.

## Replay companion assessment

The historical security replay case is value-identical to the historical host `packet-0-original` case. Its selected object list contains 23 unique keys and its blob list 46 unique keys; its object and blob pools are exactly those selected entries from the historical host pools, with no omission or extra entry.

The new companion's `case` is value-identical to the accepted current host companion's `packet-0-original` case, including current run ID `run3:36e5b6298464492386aa5ca8f4f2d2db12c03c9f817518da8069015b3e77e6c0`, expected result, and ordered selections. Its 23 object values and 46 blob values are byte-derived JSON values exactly equal to the selected entries in the accepted current host pools, and its pool key sets have no extras. The current host fixture has the accepted candidate SHA-256 `a71dde8e9a57cbe0576a283c5b6e83bf494acb4dc2435b16a488a717450ed6ef` pinned by the accepted scope, map, review, integration record, and inventory v182 unit.

The source change remains under `#[cfg(test)]`. `fixture()` still reads the unchanged historical journal document, so all 321 record cases retain their original bytes and selection. Only `fixtures::replay()` selects the current companion. It continues to build `RegisteredSchemas` from the registered current source requirements and retains the existing traversal, owner-invocation, capture-entry, and retained-byte limits. The 814,277-byte companion remains below the unchanged 4 MiB product JSON parser limit. No fallback, schema registration, guard, recipe, admission source, production type, or runtime path changes.

## Settlement guard assessment

At the pinned source, the global scan finds the expected one `reserve_settlement` and one `.ledger.settle` call in `security/src/initial_installation.rs`; three `.settle(` calls in the supervisor; two in the tar decoder; and nine in the ordinary writer. The supervisor and tar sources contain the stated private signatures. The existing reserve/settle wrapper maps and the ordinary-writer signature checks remain unchanged. The finding concerns the new exemption's ability to distinguish the exact `self` receiver, not the current pinned call counts.

Full candidate checks, before/after reproduction of the 14 failures, complete owning tests, refusal-preserving mutations, independent unit acceptance, and the additive inventory successor for the new path remain owed. This verdict is source preflight only and does not accept, integrate, inventory-bind, or qualify the repair.
