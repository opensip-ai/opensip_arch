# Review: live security guards X4 r5

Verdict: REQUIRED-FINDINGS.

Subject `docs/implementation/m2/live-guards-x4/PROPOSAL.md` is 24823 bytes, sha256 `7fd4bf35751601ed0723e4f3c56cc13d90f137fb75e562fdc662630b773f9a4f`, matching hashes.txt. Preserved r4 is 23968 bytes, sha256 `43174456e723ce7c529df3c68ba33952841d84c147cadc2a1478971685210ddc`. Preserved r3 is 23266 bytes, sha256 `d075505c98371d3167668818e58b2f6901c165176d6158799a5a0dd31a53de00`. The request names product HEAD `99f1c35b50ddd7a3a2724d9acadf9c72f27ce7da`. The live product HEAD is `8bfc78a741158e961f727dd44f481549ec09225d`, and `99f1c35` is its ancestor. The trust sources this amendment cites are unchanged between those commits. The real OpenSIP support directory is absent. No product cargo.

The diff against the accepted r4 is the header, item 5's retained handles and per-observation ledger, and the new policy-drift and role-standing paragraph. The ledger figures match X4T r5's unchanged `TRUST_VIEW_COST`: 2 × 128 objects, 2048 edges and 112 MiB is 256 objects, 4096 edges and 224 MiB, inside the owner's 256 MiB cap. In M2 the global policy is `Source::Missing`, so a policy change can come only from the project policy, and the existing drift rules stay. Those two points are sound. The reading path and the continuation-row mapping are not.

X4T r5 is accepted in this sitting. Its item 2 is the loader list this amendment has to match.

## RF-1

Item 5 retains `trust/stores/S` and the four collection directories `objects`, `records`, `publications` and `events`. It then says each observation captures through X4T's existing binders, and step 2 opens every record the head names through the retained records handle.

X4T r5 item 2's loaders are a different set. `state.v1` is opened by name through the retained `trust/stores/S` handle. The publication descriptor, the inline `clock.record` and the event chain come from `native_current::capture_p2`, `current_record_bindings::bind` and `current_event_trace::bind_trace`: the descriptor is a publication, the events are events, and `clock.record` is an inline object. `heads.root`'s body and envelope come from `trust_ordinary_roots::bind_retained_head` in `objects`. The root admission, the catalog and revocation bodies, envelopes and admission records, `history` and `timeEvidence` are opened by X4T-a with `Budget::load`: `objects` for signed bodies and envelopes, and `records` for the node references (admission records, `history`, `timeEvidence`). X4T-a then checks `accepted.by` against the events `bind_trace` loaded.

The records handle does not open the publication, the events or the object files. The existing binders do not open the members X4T r5 assigns to X4T-a.

Required: item 5's observation captures in X4T r5 item 2's order through those loaders. Each file is opened through the retained handle of the collection that loader uses. `clock.record` stays inline. The `accepted.by` check stays X4T-a's. Keep the four directory names. Keep the per-observation ledger at 256 objects, 4096 edges and 224 MiB.

## RF-2

The r5 role-standing paragraph says the grant consults `ExistingOnly` and `InstallGateRequiredForNewProcess`, and that a standing which forbids the operation refuses on the continuation row, citing X4T item 10.

That row is X4T's admission refusal for `Continuation::Refuse` (`ContinueCoreNotTrusted`, `ContinueIndexNotTrusted`, `ContinueComponentNotTrusted`). The view is not admitted, and the published detail is `CONTINUE-CORE-NOT-TRUSTED`. `ExistingOnly` is core and component `Trusted` with the index `Expired` or `StaleRevocation`. `InstallGateRequiredForNewProcess` is the admitted standing in which continuing is permitted and starting still needs `EV-INSTALL`. `role_machine::continuation` accepts `Continue` for both. Publishing the continuation admission detail reports a trusted core as untrusted.

Item 8 already sends a refusal that happens before any admitted view to X4T's own rows. The grant sees only an admitted standing.

Required: the grant consults those two admitted standings. It allows an effect the standing allows and withholds an effect the standing does not allow. That withhold stays off X4T item 10's continuation row. Name an existing detail whose meaning is the withhold (the repository-execution grant's existing `GRANT.*` rows are the new-process grant's rows, item 8), or state that every M2 writer effect is a continuation those standings allow. `Continuation::Refuse` remains X4T's admission row at the lease-free point.
