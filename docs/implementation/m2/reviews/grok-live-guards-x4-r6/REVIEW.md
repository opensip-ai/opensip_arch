# Review: live security guards X4 r6

Verdict: REQUIRED-FINDINGS.

Subject `docs/implementation/m2/live-guards-x4/PROPOSAL.md` is 26240 bytes, sha256 `c3582af110cdd217366aadae644dbdcca8009279c68d11bae2fd6b57e07837f8`, matching hashes.txt. Preserved r5 is 24823 bytes, sha256 `7fd4bf35751601ed0723e4f3c56cc13d90f137fb75e562fdc662630b773f9a4f`. Preserved r4 is 23968 bytes, sha256 `43174456e723ce7c529df3c68ba33952841d84c147cadc2a1478971685210ddc`. The live product HEAD is `8bfc78a741158e961f727dd44f481549ec09225d`. The real OpenSIP support directory is absent. No product cargo.

The diff against r5 is the header, item 5's observation loaders, and the role-standing paragraph. The per-observation ledger stays 256 objects, 4096 edges and 224 MiB. Policy drift stays on the project policy, because M2's global policy is empty.

## r5 RF-1

Closed. Item 5 retains `trust/stores/S` and `objects`, `records`, `publications` and `events`. Step 2 captures in X4T r5 item 2's order: `state.v1` by name; the descriptor and the event chain through `capture_p2`, `current_record_bindings::bind` and `bind_trace`, from `publications` and `events`, with `clock.record` inline; the root body and envelope through `bind_retained_head`, from `objects`; the root admission, the catalog and revocation bodies, envelopes and admissions, `history` and `timeEvidence` through X4T-a's `Budget::load`, signed bodies and envelopes from `objects` and node records from `records`; then X4T-a's `accepted.by` check. Each file is opened through the retained handle of that collection.

## r5 RF-2

The continuation-row half is closed. Both standings are admitted. Every M2 writer effect (journal append, object publication, ledger commit) is allowed under both. The grant does not publish X4T item 10's continuation row for an admitted standing. `Continuation::Refuse` stays X4T's admission refusal at the lease-free point.

The replacement new-process rule is one rule for both standings. That is the finding below.

## RF-1

`role_machine::continuation` returns `ExistingOnly` when the core and component are `Trusted` and the index is `Expired` or `StaleRevocation`, and `InstallGateRequiredForNewProcess` when the core, index and component are otherwise past the refuse cases. The `Continue` event is accepted for both. The comments on the two variants differ: `ExistingOnly` is an existing verified process and never a new-process grant; `InstallGateRequiredForNewProcess` permits continuing, and starting still needs `EV-INSTALL`.

The r6 paragraph says both withhold only starting a new process, which needs `EV-INSTALL`, and that starting a new process is withheld under both through `GRANT.*`. That gives `ExistingOnly` a gate that can open, and it withholds a new process under `InstallGateRequiredForNewProcess` after `EV-INSTALL` has been admitted. The standing does not change when that event is admitted: the three roles are already `Trusted`.

Required: keep the M2 writer allowance and the admission-row split already written. Split the new-process rule. From an `ExistingOnly` view the repository-execution grant never admits a new process, and the refusal is an existing `GRANT.*` detail. From an `InstallGateRequiredForNewProcess` view a new process is withheld until `EV-INSTALL` is admitted and is granted once that event is admitted; a withhold before that event is an existing `GRANT.*` detail. Neither case publishes X4T item 10's continuation row.
