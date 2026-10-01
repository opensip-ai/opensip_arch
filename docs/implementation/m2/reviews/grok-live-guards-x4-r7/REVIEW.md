# Review: live security guards X4 r7

Verdict: ACCEPT.

Subject `docs/implementation/m2/live-guards-x4/PROPOSAL.md` is 26577 bytes, sha256 `fc8490f4e751e486bc4cf6dc15e04eb541672112bda2eab8c15759c31eaf0224`, matching hashes.txt. Preserved r6 is 26240 bytes, sha256 `c3582af110cdd217366aadae644dbdcca8009279c68d11bae2fd6b57e07837f8`. Preserved r5 is 24823 bytes, sha256 `7fd4bf35751601ed0723e4f3c56cc13d90f137fb75e562fdc662630b773f9a4f`. The live product HEAD is `8bfc78a741158e961f727dd44f481549ec09225d`. The real OpenSIP support directory is absent. No product cargo.

The diff against r6 is the header and the role-standing paragraph. Item 5's loaders and the per-observation ledger (256 objects, 4096 edges, 224 MiB) are unchanged. Policy drift stays on the project policy.

## r6 RF-1

Closed. `ExistingOnly` is core and component `Trusted` with the index `Expired` or `StaleRevocation`. Existing verified work continues, and the repository-execution grant never admits a new process from that view. The refusal is an existing `GRANT.*` detail.

`InstallGateRequiredForNewProcess` permits continuing. A new process is withheld on an existing `GRANT.*` detail until `EV-INSTALL` is admitted, and is granted once that event is admitted. The standing value does not change when the event is admitted.

Every M2 writer effect (journal append, object publication, ledger commit) stays allowed under both. Neither standing publishes X4T item 10's continuation row. `Continuation::Refuse` stays X4T's admission refusal at the lease-free point. The new-process grant is the repository-execution grant, and it is outside M2.
