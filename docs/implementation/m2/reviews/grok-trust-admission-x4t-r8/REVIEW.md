# Law X4T r8 — trust admission, accepted.by by reference

Law review only. No product cargo. The OpenSIP support directory is absent. Subject `trust-admission-x4t/PROPOSAL.md` is 45076 bytes, sha256 `4a333c8660ea3f548d2fe3d8fc36ef570f53c1f6fe3666396b39c641de03fe81`, matching `hashes.txt`. Preserved r7 is `PROPOSAL-r7.md`, 35671 bytes, sha256 `7a8283063b4c47fa801cb3954e7ed7dc8e79d6e1fd6f2193bc31e12a7e34a7b1`, equal to the accepted r7 `review.json` subjectSha256. Live product HEAD is `920941bd30f49c7ee856585ff9c0b83272851a8d`. The trust and custody files this amendment cites are unchanged since `66bdd05`.

The diff from r7 is items 1, 2, 7, 8, 11, 12 and 13, the Forbidden substitutes, and Not claimed: the reference load, the rollback comparison, the retained owner, the 47-to-53 count, and unit X4T-a2.

## What holds

The r7 contradiction is real. Item 7's floor publication lists only its clock-write event, and it forbids rewriting `accepted.by`. `publication_events::bind_events` requires the new event's `previous` to equal the head, so that publication cannot re-list the acceptance events. After the first floor write, `accepted.by` names no event `bind_trace` loaded, and `check_accepted_by` refuses `installation-incomplete`. r8 closes that without walking history. One `Budget::load_at` in `Collection::Events` per role, at most six, opens the missing event. Its `previous` is never followed. The loaded event must be an accepted `role-event` of that role in this store, with sequence lower than the current descriptor's first listed event. `load_at` binds the bytes to the reference's sha256 and length. The count goes from 47 to 53. The ceiling stays 128 objects, 2048 edges and 112 MiB, which still covers 53 files and 16 links. Accepting the reference without loading it, re-listing the acceptance events, rewriting `accepted.by`, and walking `history` are the right rejections.

Checks 1 and 2 match the time-evidence schema and use only the evidence item 1 already opens. `TimeEvidenceV1` is an `s4-evaluation` input or an `s4.5-epoch` input. Checks 1 and 2 apply to the first. An `s4.5-epoch` input is S4.5's recovery, the act that sets F to `issuedAt`, which may sit below `observation.wall`, so leaving it out of the comparison is required. `beforeClock` is a `ClockPhase`: `retained` carries a `RetainedClockRecord` with all five floors, `evaluated` carries a `P1Projection` with F and L, and `unevaluated` carries only `phase`. `observation` is an `Anchor` whose `wall` is the W of S4 step 5, and that step writes F = tEval ≥ W. The whole-file restore limit is stated correctly. Every SC-TRUST member lives under I, so restoring I or `trust/` rolls the capsule and its closure together and checks 1 and 2 still pass. That is the same selected-limit form as S6's carrier anchor bound. No accepted law defines a durable anchor outside that tree. Reading the predecessor is an extra read outside the closure, and no law requires that image to remain in `trust/records`. The successor bucket is X4B item 6's lawful crash residue, a successor written while the pointer still names the predecessor. X3b r2 item 7's carrier floor is `{highWaterSchema, projectKeyDigest, grantGeneration, lastSeq, tailSha256}`, records no trust epoch, and lives under I. A new floor file outside I would be a new custody owner.

The retained owner matches item 8, X2 r5, and X4B item 5. At `66bdd05`, and still on these files, X3a-1's `EndpointValues` keeps `CurrentStore` (S, G, K) and the `RequiredFile` sample, and `decode_current_store` drops the bytes after the parse. r8 keeps those bytes from that same read, decodes the capsule from them, and binds `trust/stores/S` by a no-follow metadata recheck of device, inode, and the full sample. The owner advances only after the reopen: the bytes reread at the name equal the written bytes, the capsule comes from that reread, and the post-rename sample replaces the `RequiredFile` sample. The predecessor becomes provenance. That is X2 r5's one-owner replacement rule and X4B item 5's confirming reopen. Item 8 takes that owner and does not read `state.v1` again. X4T-b opens the store handle and passes it in; X4T-a2 and X4T-b may be one unit.

## RF-1

Item 7 check 3 names X4B's acceptance and requires each of the five `clock.record` floors to be at least the same floor of every capsule this fence hold retained before the advance.

The capsule retained before that acceptance is the P0 `state.v1`. Its clock is the `unevaluated` phase, `{phase}` only, with no `record`. It has none of `evalHighWater`, `lastAccepted`, `rootVersion`, `revocationVersion`, or `indexSnapshotVersion`. Check 1 says an unevaluated clock has nothing to compare. Check 3 has no such exception.

X4B's confirming admission runs X4T items 2 to 7 on the new capsule after the owner has advanced in that same fence hold, and X4B requires that admission to succeed. Check 3, applied to the predecessor it names, has no floor to compare, so the lawful first acceptance has no result that both follows the sentence and admits.

Required: a predecessor whose clock is `unevaluated` has nothing to compare, and check 3 admits X4B's acceptance.

## Verdict

REQUIRED-FINDINGS. RF-1.
