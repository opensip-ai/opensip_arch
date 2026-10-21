# CODEX2 Review — inherited CLI creator source-guard repair r1

## Verdict

**REQUIRED-FINDINGS**

## Required findings

### CLI-GUARD-R1-RF-1 — Bind the logging exception to the single accepted adapter and its actual operability resolution

`has_creator_commit_symbol` removes every exact textual occurrence of the two-line `finalize_invocation` body whenever the caller marks the file as `host/lib.rs`. It does not require exactly one occurrence, anchor that occurrence to the accepted top-level adapter, or establish that the path name `opensip_operability` resolves to the accepted operability crate.

That leaves a source-guard false negative. For example, an exact same-spelling body can be placed in a nested scope where `opensip_operability` is locally bound to a bridge in an unscanned host module. `text.replace(OPTIONAL_LOGGING, "")` deletes both the accepted block and the nested block; the alias declaration need not contain `finalize`, and the bridge file is outside the four host files this X11 test scans. The guard can therefore pass while an ingress-reachable exact body resolves to a different `finalize` authority. Multiple exact blocks are likewise all erased. The current synthetic controls cover direct, qualified, method, import and definition spellings, but do not exercise duplicate/nested blocks or name-resolution shadowing. The compiled all-false mutant only proves that the listed direct witnesses depend on the predicate; it does not close this exception path.

Make the exception fail closed unless it is the one accepted top-level adapter with the expected surrounding source boundary and an unshadowed `opensip_operability` binding. A bounded textual repair can require exactly one adapter occurrence, remove only that occurrence, and reject any additional declaration/import/alias of `opensip_operability`; a syntax-aware equivalent is also sufficient. Add controls for a duplicate or nested exact body and for an exact body under an aliased/shadowed `opensip_operability`, then freeze fresh owning evidence and a mutation that demonstrates the exception guard is observed.

## Authority ruling

Existing authority is sufficient for the corrected test-only repair. X11 requires the creator, ordinary writer, gate, pack admission, recovery and storage commit path to remain absent from the CLI and host ingress. The accepted S-OP-2 integration separately authorizes the current top-level `finalize_invocation(bool)` adapter whose body calls `opensip_operability::finalize(bool)` for optional logging finalization. Distinguishing that exact adapter from X11's storage commit coordinator is an implementation of the two accepted duties, not a new command, creator permission, logging behavior or storage authority. No additional design selection is required; the required work is to make the source predicate enforce the distinction it claims.

## Frozen-subject and evidence assessment

The requested `subject.json` SHA-256 is exact: `6cd37233efebd9aab561416fd98851b4a9b60e177f2ead02cf40828d78be5114`. All 38 declared members are present, there are no extra frozen subject files, and every declared byte count and SHA-256 matches. The candidate file equals the named worktree, the ten frozen production authority files equal accepted main and the worktree, both product checkouts are at `ca6f5be9ded80c50a143b2f219258c95c80db2e6`, and architecture is at `278d1a27b4cea095b37eed09e7109d8a98be7696`. The worktree diff is exactly the existing `apps/cli/tests/creator_commands_tests.rs`; `product-map.json` records that path and zero new paths.

Apart from the finding, the delta is appropriately narrow. Every other forbidden-name substring check is unchanged, the CLI source directory and four host ingress files remain the selected scope, the security owner/visibility assertions remain intact, and the six command/refusal/catalogue/zero-effect test bodies are byte-identical to the parent. Exact identifier matching correctly avoids the unrelated `finalize_invocation` identifier while retaining ordinary `finalize` calls, qualified calls, method calls, imports, definitions, raw-identifier punctuation and conservative Unicode identifier adjacency.

The inherited failure is correctly attributed to the old substring predicate on accepted production bytes. The isolated owning evidence records both selected source tests and all-target CLI Clippy passing. The weakening mutant compiled, failed at the direct storage-call witness, restored the candidate hash, and both controls passed freshly; compilation failure is not counted. The evidence accurately states that no CLI command, private fixture, installation read or production flow ran and that the full CLI or workspace matrix was not replayed. Those limitations do not cure CLI-GUARD-R1-RF-1.

This review does not accept any production change, Rust3 worktree, inventory/status update, whole-project gate or qualification. Existing-path inventory/hash binding and status work remain lead obligations after a corrected unit is independently accepted.

## Non-blocking observations

None.
