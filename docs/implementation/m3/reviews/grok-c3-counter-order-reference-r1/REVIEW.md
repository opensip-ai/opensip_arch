# C3 inert counter-order authoring reference r1

ACCEPT. requiredFindings empty. testsPassed 13. contentChargingBoundarySelected false. activationDerived false. admissionGranted false. fullC3aComplete false. productQualification false.

This is an inert replay of supplied candidate observations. It does not acquire, decode, validate, or materialize a package, and it does not admit a route or activate a candidate. The accepted C3 producer and profile evidence stays closed. No inventory, lock, or law change is proposed.

## Pins

Subject manifest `docs/implementation/m3/snapshot-plan-c/c3-counter-order-reference-r1-subject.json` is 1663 bytes, sha256 `6eb7160c26410f29ee9722a8c9697b53696cd2d9d3f70cc021d8872c1afe0095`. All 7 members are sorted and unique, and each byte and hash pin matches.

Product HEAD is base `bf1ce2566120bcb7db339c3c8a1ee3853f300c8c`, and that worktree is clean. Architecture HEAD is base `5f1030e493e9e006095ea0851cc4babdd1bd66a5`. At that commit, `PROPOSAL-r7.md` is 157110 / `a1ee9386da5913c135932891f6f8041cc72834b9bd531b1e6a51ccfccc1d40c6`.

## Two populations

The pinned rule 7 keeps the populations separate. Acquisition, before activation, allows 16,384 sources, 4,000,000 logical files, and 32 GiB. The final protocol check, once after admission and activation, allows 4,096 packages, 1,000,000 files, and 8 GiB. Exact totals stay inside the bound. One more source, file, or content byte crosses.

`replay_acquisition` sorts candidates by the UTF-8 bytes of `(name, version, sourceId)` and keeps each candidate's supplied event order. It counts every candidate toward acquisition, including those labelled inactive or rejected. A source past 16,384 returns before that candidate's file events are applied. Inside one grouped event, the crossing index is the earlier of the file-count crossing and the content crossing, and a tie reports files. The returned acquisition value is `Bound(field, observed, limit)` at that first breach. A completed run under every limit returns the three totals instead.

`final_population` sums only candidates labelled both admitted and activated. `final_overflow` returns every field whose total is past 4,096, 1,000,000, or 8 GiB. It does not pick one final field when files and content both cross. Admission and activation remain supplied labels. The replay grants neither.

A single file of 8 GiB + 1 stays inside the 32 GiB acquisition bound. It crosses the final content bound only when that candidate is labelled admitted and activated. The withdrawn protocol-threshold shortcut is not reintroduced.

The thirteen recorded controls cover those exact and one-over boundaries, inactive and rejected labels, version-then-source UTF-8 order (`z` before the UTF-8 bytes of `é`), input permutations, and a same-file files-before-content crossing. Recomputing them in memory against the staged `reference.py` gave the same results as `tests.log`. `run.py` imports the authoring path and was not executed.

## What the replay leaves open

Grouped `FileEvent` values are uniform whole-file observations used for arithmetic. They are not a tar size declaration, and the content total is the sum through the completed crossing file. Production incremental charging under real read chunks is not selected. The replay also does not establish archive or tree order, exclude path packages, bound earlier I/O, or project a wire refusal key. Decoder counters D1–D4, the final descriptor, the wrapper, scratch, and native launch stay outside this reference.

`source.json` records the same false flags, including `fullC3aComplete` and `productQualification`. `~/Library/Application Support/OpenSIP` is absent. Neither repository was edited. The architecture worktree still has its eleven pre-existing untracked operability and E2s paths; they are outside this subject.
