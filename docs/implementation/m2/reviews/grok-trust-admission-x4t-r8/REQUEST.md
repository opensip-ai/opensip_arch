Grok review: law X4T r8, an amendment to the accepted r7. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-trust-admission-x4t-r8. This is a law review: run no product cargo. Product HEAD is 66bdd05.

Subject: docs/implementation/m2/trust-admission-x4t/PROPOSAL.md r8 (pinned in hashes.txt). Diff it against PROPOSAL-r7.md, which is the accepted r7 bytes (sha256 7a8283063b4c47fa801cb3954e7ed7dc8e79d6e1fd6f2193bc31e12a7e34a7b1, equal to your r7 review.json subjectSha256).

Context:
- X4B r4 (`trust-bootstrap-x4b/PROPOSAL.md`, item 5 and item 6);
- X3b r2 item 7 (the carrier floor);
- X2 r5's registry replacement rule;
- the security contract's S4, S4.5 and S6 (the carrier anchor bound);
- product `trust/current_trust_admission.rs` (`check_accepted_by`), `current_event_trace.rs` (`bind_trace`), `publication_events.rs` (`bind_events`) and `custody/installation_admission.rs` (`RequiredFile`, `EndpointValues`), all at 66bdd05.

## Why r8

Starting X4T-b found a contradiction in r7. Item 7's floor publication lists only its clock-write event. Item 1 required every accepted role's `accepted.by` to name an event of the current chain, and forbade walking `history`. A clock-write-only publication can't re-list earlier events, because `bind_events` requires `previous` to equal the head, and item 7 forbids rewriting `accepted.by`. So every store would refuse as `installation-incomplete` after its first floor write, which is after its first operation.

## Changes (all lead decisions, 2026-10-01)

1. **Items 1, 2 and 11.** An `accepted.by` outside the loaded chain is opened by reference: one `Budget::load_at` in `Collection::Events` per role, so at most six.
   - It must be an accepted role event of that role, in this store, earlier than the current descriptor's first listed event.
   - Its `previous` is never followed, and `history` is never walked.
   - Item 11's count goes from 47 to 53 files. The ceiling is unchanged.
   - Rejected: accepting the reference without loading it.
2. **Item 7, rollback at the handoff.** The comparison now names exactly what it compares against, using only what the view has already read:
   - the time evidence's `beforeClock`;
   - F against at least the evidence's `observation.wall`;
   - the floors this fence hold has already retained.

   An S4.5 epoch input is not compared. A whole-file restore of an older, self-consistent `state.v1` with its closure is a stated limit, not detected; no M2 unit closes it. Rejected: reading the predecessor capsule, probing the successor bucket, the carrier floor, and a new floor file outside I.
3. **Items 7 and 8, the retained `state.v1` owner.** At 66bdd05, X3a-1 keeps only the `RequiredFile` sample and `C.store` from its one read.
   - The owner is now that read's bytes (X4T-b keeps them; no new read), the capsule decoded from those bytes, and the read's sample.
   - `trust/stores/S` is bound to the owner by a metadata recheck, not a content read.
   - The owner advances only after a confirmed publication. Its capsule comes from the reopen, and its post-rename sample replaces the `RequiredFile` sample.
   - The publication protocol has one owner, shared with X4B-a.
4. **Item 13.** A new code successor, X4T-a2: the `accepted.by` load, its tests, and the measured cost constants. X4T-b depends on it, and the two may be one implementation unit.

## Decide

- Is the r7 contradiction real, and does r8 close it without walking history?
- Is the rollback comparison exact and lawful? Is the whole-restore limit stated correctly, and is the rejection of each alternative sound? Is there a cheap lawful closure r8 missed?
- Is the retained owner consistent with item 8, X2's registry rule and X4B item 5?
- Is anything else wrong?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
