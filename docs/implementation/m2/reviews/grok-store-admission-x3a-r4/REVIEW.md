# Review: store admission X3a r4

Verdict: REQUIRED-FINDINGS.

Subject `docs/implementation/m2/store-admission-x3a/PROPOSAL.md` is 13862 bytes, sha256 `c1908bc190e006f5c6af4fb8b03f9f9d5445fe2cc85bae633fc69803718364ce`, matching hashes.txt. The diff against `PROPOSAL-r3.md` (13114 bytes, sha256 `adf5552dbe2a84f7f19222c419c9e883806e37edf67510d683278e183a1b0ce6`) is the r4 header and item 2's producer paragraph. The preserved file is the accepted r3 text plus the 35-byte stamp `r3 ACCEPTED by Grok on 2026-09-30. `; the r3 acceptance itself was 13079 bytes, sha256 `9956fd143a4b3f07a66158020dbe71be3c7704118a3f28996e7af513f312ad97`. Live product HEAD is `f7acb6d7f8acadcbc0bf81d141f39077d817f043`. The real OpenSIP support directory is absent. No product cargo.

## What holds

Dropping the creator attempt and `InitialCore` before the gate matches 468 r5 item 1 and 467 item 9. In `installation_routing.rs`, `route` ends the attempt in its own block, then calls `DurableWriteGate::begin` and `admit` with only this invocation's `InitialPlatform`. `DurableInstallation` holds the fence, the chain, the required files and the two barriers. `AdmittedInstallation` adds `Entered` and no session receipt. `OrdinaryWriteAdmission` is the write value that retains a receipt, and that receipt holds `InitialCore`. Item 1 joins the pair's `coreClosure` to that receipt's selected core. The creator gate has no such receipt.

`Entered::Published` still carries `PublishedInstallation`, whose `closure` is the creator handoff value. 467 item 9 and that type's own comment keep it out of ordinary authority. Copying it through `route` so the join has a core would promote a creator observation. `LostRace` and `NotPristine` carry no closure at all. Rejecting that copy, and taking `AdmittedInstallation` off the producer list, is the consistent half of the amendment. The two remaining producers are `OrdinaryWriteAdmission`'s `DurableInstallation` and `ReadSession`'s `InstallationObservation`. Item 8 already names those two. Items 1, 3, 4, 5, 6 and 7 are the accepted r3 text.

The header still says X1 r1 is under review, and the body still says `fdbedf4`. X1 r1 is accepted. Those stamps were left standing in r3.

## RF-1

RF-1 stands. A creator command that publishes, loses the race, or finds I not pristine continues in the same invocation through the durable write gate (468 r5 item 1) and must not call `admit_ordinary_writer` (X1 r1 item 7). That process already spent its one attempt and its one `DurableWriteGate::begin`. The amendment then says this invocation produces no endpoint, and that X11 decides how the creator commands reach a store within those two constraints.

No producer remains inside that invocation. The held value is `AdmittedInstallation`, which item 2 correctly refuses. A second `admit_ordinary_writer` is `Invariant`. A read entry is the process's other single entry, already used. The creator closure is the value item 2 rejects. X11's row wires `opensip`, `analyze`, `fit` and `audit` through the creator and the 468 gate, then ends on the existing not-implemented refusal until M3. It does not admit a store, and the constraints the sentence cites leave it no lawful admission to add.

The continuation 468 requires therefore holds the fence with no `SelectedStoreEndpoint`. Any store use in that command skips item 1's core join or promotes the creator closure.

Required: keep `AdmittedInstallation` off the producer list, and keep the rejection of carrying the creator's core values through `route`. State that this invocation's gate continuation admits no endpoint. A store is admitted by a later process, through X1's `OrdinaryWriteAdmission` or a read entry's `ReadSession`, each with its own session receipt and selected core. X11 wires the creator command through the creator and the gate. It does not admit the endpoint and does not open a second entry.
