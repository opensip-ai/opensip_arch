# O1-b whole code unit r2

Verdict: **ACCEPT-UNIT**. Required findings: none. **O1B-R1-01** is closed. This accepts the full O1-b code unit. It authors no inventory, qualifies no product, and does not close M3.

Subject `subject.json` is 5095 bytes, sha256 `def506bb4f139c16b4b472b2ac3de99f4a16369cea8390308ad7fe9d1f9d9487`, with 28 sorted unique members. Every pin matches the frozen candidate. Against product `790153f929f16823591be725686cc7e5ef86600b` the tree differs in exactly those 28 paths: 24 modifications and four new files, `phase.rs`, `phase_clock.rs`, `harness_writer.rs`, and `harness_writer_tests.rs`. `design-lock.json` is byte-identical to that base, 590236 bytes. Product HEAD is that base. Architecture HEAD is `6d5e6c7ea455672696cb829ed18fda11a6bbaddd`. Inventory remains v169, with 129 inventory successors and 140 contracts.

Relative to the frozen rejected r1 candidate, three files differ: `registry-events.json`, `registry-events.md`, and `crates/operability/src/kinds/registry_tests.rs`. Every other file is byte-identical, including `registry.rs` and the host, writer, phase, and harness sources. The r1 review's runtime conclusions stand for these bytes. The copied r1 evidence matches the original r1 evidence byte for byte. The r2 logs name an authoring tree that is byte-identical to this candidate.

## O1B-R1-01

The committed reference now lists seven events. `host.phase.started` is info, requires request, export false, template `phase started`, maxLine 945, with `phase`, optional `parent`, and `at`, all P0. `host.phase.completed` is info, requires request, export true, template `phase completed`, maxLine 1001, with `phase`, `wall`, `cpu`, `outcome` as `Code<PhaseOutcome>`, and `at`. The code tables are ten, including `PhaseOutcome` with provenance `registry-literal`, role `code`, cap 32, and members `completed`, `failed`, `cancelled`, and `not-applicable`. The sink list includes `harness` at P0 and P1 in both artifacts. The `Sink` code table still contains the `harness` member.

`render_json` and `render_markdown` emit those descriptors from the `Event` implementations and `tables()`, and `the_committed_registry_reference_matches_the_registry` passes. A separate control reads the unexpanded `registry.rs` text: `name: "` declarations, the custom `const NAME` literal, the `loss_event!` name, and every `code_table!` name. Replaying that scan on the candidate yields the same seven events and the same ten tables as both artifacts, and both artifacts contain the harness P0/P1 row. The test also rejects eight omissions: each of `host.phase.started`, `host.phase.completed`, `PhaseOutcome`, and `harness`, removed from JSON and from Markdown. That test passes in the 90 default, 94 development, and 92 harness library runs. `r2-reference-generation.log` is the earlier drift failure from before the generated files were copied. It is not the controlling run.

## Census and boundaries

Source control reports 113 rows and no findings. The checker reports 18 passed. The lock check reports no findings. `exceptions.json` is unchanged from r1, so the ordinary rows and the 431 mint-audit rows are unchanged. Default and combined-feature warning-denied Clippy for operability finish with no warning line. The featureless release, descriptor, stall, digest, phase, and profile controls remain the r1 logs on this identical runtime. Timing figures stay unqualified. The driver digest remains the C-13 byte digest. Provider `ComponentRole`, O1-c, O1-S, S-OP-6, and strict M6 stay outside this unit.

`inventoryAuthored` is false. `productQualification` is false. `entirePlanComplete` is false. Integration still needs lead assent, the code commit, and the architecture receipt, then a separate additive inventory.
