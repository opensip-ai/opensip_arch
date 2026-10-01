# Review: store admission X3a r5

Verdict: ACCEPT.

Subject `docs/implementation/m2/store-admission-x3a/PROPOSAL.md` is 14850 bytes, sha256 `310197d33f4851eb0c198073e2516a6ea14192cebde751f64a0861f5f98f8ba3`, matching hashes.txt. The diff against `PROPOSAL-r4.md` (13862 bytes, sha256 `c1908bc190e006f5c6af4fb8b03f9f9d5445fe2cc85bae633fc69803718364ce`) is the r5 header and item 2's creator paragraph. Live product HEAD is `f7acb6d7f8acadcbc0bf81d141f39077d817f043`. The real OpenSIP support directory is absent. No product cargo. Item 5 is unchanged, so no new public detail or route is introduced.

## RF-1

RF-1 is closed. A creator invocation produces no endpoint and performs no store operation. Item 2 names the three constraints that make that unavoidable: 468 r5 item 1 drops the attempt and `InitialCore` before the gate continues; X1 r1 item 7 forbids `admit_ordinary_writer` once that attempt and `DurableWriteGate::begin` are spent; 467 item 9 forbids promoting `PublishedInstallation`'s closure. `AdmittedInstallation` stays off the producer list. The rejected alternatives are carrying the creator core through `route`, and a second attempt in the same process.

Store work is a later invocation that enters as an ordinary writer through X1, with that process's own receipt and selected core. That is X1 item 3's `NotInitializedWhenAbsent` class, or a `CommandOwnerDecides` command whose owner decides it writes. `opensip`, `analyze`, `fit` and `audit` stay `InstallationEntry::Creator` on every invocation (`host::request::installation_entry`), so a later run of those commands is another creator invocation and also stops short of a store. X11 decides the creator command's termination and what it tells the user, including 468 item 7's backup-status disclosure, and must not give that invocation a store. A store in the same invocation needs an X1 item 7 amendment, and none is proposed.

The producers remain `OrdinaryWriteAdmission`'s `DurableInstallation` and `ReadSession`'s `InstallationObservation`. The sentence that those sessions already read the pair, the marker and every node now sits in the second rejection bullet. It is the same fact as r3, and it does not add a producer.

## Otherwise

Items 1, 3, 4, 5, 6, 7 and 8 stand as accepted in r3. The header still says X1 r1 is under review, and the body still says `fdbedf4`. X1 r1 is accepted. Those stamps were left standing in r3.
