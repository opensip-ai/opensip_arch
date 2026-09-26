Grok review the 463c code, r1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-embedded-revocation463c-r1. You own the serial native lane until your report is written. Host macOS 27.0. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline. Do not read or print the private 413 UUID fixture.

Law: docs/implementation/m2/initial-core-launch-463/PROPOSAL.md, r4 amendment items 4 and 5 as amended in r5 and r6 (accepted). Product HEAD bf49fcb. Two uncommitted files are pinned in hashes.txt. No file is added.

## Changes

- core_anchor.rs, `revocation(budget, &CapturedCore, store) -> Pair`: it rebuilds the manifest index over the anchor platform's embedded tree rows and selects `members.revocation.path`. The index pairs the envelope from `members.envelopes`, and the bytes come only from the store. `capture` is unchanged.
- core_authentication.rs, `authenticate_embedded_release(budget, anchor_ref, store) -> EmbeddedRelease`. It takes no revoked set; `authenticate` and its 323 tests are unchanged.
  1. `authenticate` with an empty set.
  2. The final root (last link, or the anchor), then `verify_revocation(final_root, body, env, {})`. The revoked set is the `keyId` entries.
  3. The inventory envelope (TR-CORE) and the bootstrap manifest envelope (TR-BUNDLE) are verified under the final root from `initial()`, then `filter_envelope_revoked`.
  4. `filtered_again(revoked)` must be Met for each link's continuity and possession, then the revocation's own quorum, then TR-CORE, then TR-BUNDLE.

  Nothing is returned before step 4, and there is no fallback. `ReleaseError` has the variants Authentication, RevocationMember, Revocation, KeySubject, Envelope(kind) and Quorum(kind).
- Tests: the existing fixtures carry placeholder TR-CORE, TR-BUNDLE and revocation material, so the test builds a synthetic signed release with the public quorum62 seeds (quorum-roots.json root "1"):
  - positive: a 2-root chain with revoked non-critical keys; a single root with an empty list; a single root revoking one of its own root keys;
  - refusals: self-revocation of its own signers → Quorum(Revocation); final-root keys → Quorum(Root); root-0 keys breaking continuity → Quorum(Root); TR-CORE → Quorum(Inventory); TR-BUNDLE → Quorum(Payload);
  - a missing revocation member, and a revocation at the wrong root version;
  - all 13 accepted core-auth323 rows refuse with RevocationMember, because of their placeholder revocation.

## Lead's replay

security lib 459/0; clippy `-D warnings` and fmt pass.

## Decide

- Does the code implement items 4 and 5 exactly, including the self-quorum re-filter, no fallback, and no fact before step 4?
- Is reading "every chain link's quorum" as each link's continuity and possession, and not the index-0 anchor (whose envelope is never verified), correct?
- **Question for you: non-key revocation entries.** The revoked set uses only `keyId` entries. Entries with subjectKind `release`, `namespace` or `catalogSnapshot` are verified but not applied. Should InitialCore refuse when the embedded revocation revokes this very release or its catalog snapshot, or is that owned by a later check? If you judge it required by the law as written, raise a finding; if it needs a law decision, say so.
- Is the synthetic release a sound test of the real path? What is untested (see below)?

Untested: an unlisted or ambiguous revocation envelope (index code), the Envelope(kind) carrier errors, KeySubject, schema-2 roots, budget counters, and a real signed tree (463g).

review.json must contain top-level "verdict" (ACCEPT-UNIT or REQUIRED-FINDINGS) and "requiredFindings". Write REVIEW.md and review.json. Do not commit.
