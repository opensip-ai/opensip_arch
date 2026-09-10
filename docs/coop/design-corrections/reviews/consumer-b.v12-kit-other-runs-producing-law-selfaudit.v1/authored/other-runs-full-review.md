# Successor bounded four-Run review (after producing-law self-audit)

**Scoped verdict: `FOUR_RUNS_REFUSED`**

Same kit-only origin as COMPLETE49. Original rust `FOUR_RUN_FULL_ADMIT` is withdrawn. Syntax-data is re-admitted only after independent producing joins and complete `C(proof)` plus reminted evidence/seal/run identities. Original TS import-producer and rust-partial enumeration findings are not waived. This is not whole-consumer acceptance, product qualification, or implementation authorization.

Exact stores unchanged (export-manifest SHA `b515c415da8c0a496e0078b48dfb8b3eabb9364e3522d48929343492d116023b`).

From-scratch command:

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-producing-law-selfaudit.v1/output/checker/main.py
```

Frozen original checker: `checker-original/`. Pathdiff: `history/checker-pathdiff.txt`.

## Layered successor results

| Run | raw | structural | producing | fullsemantic | scoped | first refusal |
|---|---|---|---|---|---|---|
| TypeScript `run3:26dd4376…` | PASS | **REFUSED** | notReached | DIAGNOSTIC | REFUSED | `IMPORT_PRODUCER_KIND` (preserved) |
| Rust complete `run3:9032d3b0…` | PASS | PASS | **REFUSED** | DIAGNOSTIC | REFUSED | membership does not cover snapshot paths |
| Syntax data `run3:ab1d6fc4…` | PASS | PASS | PASS | PASS | FULL_ADMIT | none on successor C-path |
| Rust partial `run3:0f06d053…` | PASS | PASS | **REFUSED** | DIAGNOSTIC | REFUSED | same membership/extent producing refusal |

## Withdrawn original grade (Rust complete)

COMPLETE49 treated selected-field proof equality as full replay and never independently derived file extents or membership snapshot cover.

Executed now:

- `C(UnitMembershipV1)` equals `enumerationPlan.membershipDigest` (`b4a827ed…`) — join holds.
- Membership **rows** are only `#/a/src/lib.rs`. Snapshot also has `#/Cargo.toml`, `#/a/Cargo.toml`, `Cargo.lock`. Enumeration §8: a missing row is not a silent exclude. **First refusal.**
- Inventory-cell claimed file extent is `[#/a/src/lib.rs]`. Independently remaining first-party snapshot paths are the four files. Claimed `KindExtentV1` is not producing-law.

Diagnostic (not admission): complete `C(proof)` equals retained proof (`649a60b5…`) and reminted `run3` equals `run3:9032d3b0…`. That is exactly the trap composition §7 forbids: a matching proof over unadmitted producing inputs.

Package parse (executed): workspace-only `#/Cargo.toml` (`[workspace] members=["a"]`) is not a named package; `#/a/Cargo.toml` name `a` matches the complete package inventory. That join is not enough to admit the graph.

## Syntax-data successor FULL_ADMIT (new basis)

COMPLETE49 `proofCompare: []` was a projection. Successor reconstructs `selectedRefs`, derives clones-fact outcome `partial` from unknown clones Coverage, derives `executionDeficiencies.inputRefs` from that cell's inventory digest `3148550880c15c379d0d41ab02b7c6b76da46068e2713ede1f248fa81fe7c850`, then `encode_c(proof)` equals the retained proof and reminted `run3:ab1d6fc4…` equals the export. Clones remain `unknown` + `language-tier-unsupported`/`capability-missing`, not complete-empty.

The original comparison *basis* is withdrawn even though the successor re-admits this one graph.

## Preserved findings

- TS `import.producerClosure` is kind `adapter` (must be `provider`).
- Rust-partial diagnostic: claimed `file-present` enumeration omits the clones-fact partial file inventory and claims outcome `pass`; independent `C(ruleResults)` still differs. First refusal is now the earlier membership/extent producing join.

## Bounded atom law

Admitted programs are `none` of `file@enumerated`. Atom incoming/import/resolved sufficiency branches are inapplicable on these actual RulePrograms. No unbounded generic analyzer was invented.
