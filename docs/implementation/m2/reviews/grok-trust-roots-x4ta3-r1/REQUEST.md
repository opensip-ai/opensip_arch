Grok review: X4T-a3, the reader successor of law X4T r10/r11 that separates the accepted root from the signing root. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-trust-roots-x4ta3-r1. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below.

Toolchain: `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin`; python3.14 for tools. Never touch the real `~/Library/Application Support/OpenSIP` (absent at the time of writing). Never read the private 413 UUID fixture.

## Law

- `docs/implementation/m2/trust-admission-x4t/PROPOSAL-r11.md` (53342 bytes, sha256 `7fe098fd…d384`), which you accepted in `reviews/grok-trust-admission-x4t-r11/`. The live PROPOSAL.md differs only by the acceptance note. The relevant parts are item 3 (the two roots, the closure join, `verify_captured_core` unchanged), item 4 (r11: revocation verified under `heads.root`), item 7 (the `rootVersion` floor is `clock.record`'s), item 10 (the closure-join refusal on the incomplete row), item 11 (N's files counted with the chain), item 12's r10 tests, item 13's X4T-a3, and the r10 note on X4B.
- Your r10 review `reviews/grok-trust-admission-x4t-r10/REVIEW.md`, which confirmed the split against `verify_captured_core`.

## Subject

The worktree `/Users/sb/code/opensip-ai/opensip-x4ta3`, detached at product main 0fc8ea2 (X4B-a integrated; the lock selects inventory v113). The unit was written on a34dc6b and rebased onto 0fc8ea2 before any review: the stash merged cleanly, beside X4B-a's `trust_bootstrap` child module in `current_trust_admission.rs`. Save `git -C /Users/sb/code/opensip-ai/opensip-x4ta3 diff` as `subject.diff` in your output directory: 38998 bytes, sha256 `ddd2e27ef0ebbf2f0ac214d4681988b37a93d7c7119a7a69e39f23881177ecb0`. It changes seven existing files and adds none. Pins are in hashes.txt.

## What it does

**`trust_ordinary_roots.rs` (the root owner).**
- `bind_chain_anchor(budget, closure_ref, &RetainedHead, store) -> Result<ChainAnchor, Error>`:
  1. loads the closure from `records` by the root admission's `parent` and admits it as `PayloadMetadataClosureV1`;
  2. refuses an empty `rootChain` (`EmptyChain`, a new variant);
  3. requires the last `rootChain` document to equal `head.document()` exactly, body and envelope references, or refuses `FinalIdentity`;
  4. loads `rootChain[0].body` from `objects` and admits it as a root (`FirstIdentity` if it isn't one).
- `ChainAnchor::authentication_context(chain_budget)` returns the existing `AuthenticationContext` with N as `accepted_ref`/`accepted_root`.
- `verify_captured_core`, `authenticate_shared`, `bind_retained_head` and `RetainedHead::authentication_context` are unchanged.

**`current_trust_admission.rs` (the reader).** In `authenticate`, after the root admission is opened and its `root` is checked against `heads.root.document`, the reader binds the anchor and passes `anchor.authentication_context(VIEW_CHAIN)` instead of the head's. `heads.root` stays the signing root passed to `prepare_authenticated_times`. `roots_row`'s existing catch-all already maps `EmptyChain`, `FinalIdentity`, `FirstIdentity` and `Shape` to the incomplete row; only a comment is added.

Nothing else in the reader changes. `open_heads` already verified the catalog envelope and `verify_revocation` against `input.head.root()` (M) at a34dc6b, which is what r11 item 4 requires. `admit_bound`'s epoch `rootVersion` and `Floors::of_clock` already read M's values. `Floors`, `floor_publication.rs` and `ordinary_targets.rs`'s `prepare_clock_input` are untouched.

**X4T-0 (`accepted_store_fixture.rs`, test-only).**
- **The knob.** `Spec.roots` (default 1) builds an n-root recorded chain. Root 1 is quorum root 1. Root k+1 (version k+1, `previousRootVersion` k) moves `rootKeys` through the public seed sets [0,1,2] → [20,21,22] → [23,24,25], cycling, and its envelope is signed by the previous and the new set.
- **The head.** `heads.root`, the root admission's `root`, the binding, `clock.record.rootVersion`, the list's `rootVersion` and the catalog's `rootVersionRequired` are all root n's.
- **Signing.** The revocation list is signed by two of root n's ROOT keys.
- **Listings.** The closure's `rootChain`, the manifest's `rootChain` and envelopes, and the closure's envelope members list the whole chain.
- **Test-only overrides.**
  - `root_signers` replaces root k's envelope signers.
  - `revocation_signers` replaces the list's signers.
  - `chain_end` sets how the closure's chain ends:
    - `Head` is the lawful store;
    - `OtherEnvelope` ends on the head's body with a second stored envelope of it, a value-only match;
    - `Short` drops the last root;
    - `Empty` lists none, and that one record is written past the shape check.
- **Defaults.** At the defaults every byte is r9's: n = 1, the list signed by [0,1], `rootVersion` 1. The measured byte totals are unchanged, which confirms this.

**Tests.**
- **`current_trust_admission_tests.rs`, five new tests.**
  - **Rotation admitted.** 1, 1→2 and 1→3 are admitted. The authentication proof's `original_accepted_ref` is `rootChain[0]`, `heads.root.document` is the signing root, there are n−1 links, and the chain ends at version n. `chain_bytes` equals N..M−1's bodies and envelopes. On a fenced, a report-only and a reread view, the epoch `rootVersion` and the `rootVersion` floor are both n. The one-root store is r9's.
  - **Chain end refused.** On the incomplete row (`CONFIG.CUSTODY_REFUSED`, `installation-incomplete`), on the fenced and the reread paths:
    - OtherEnvelope at n = 1 and 2, and Short at n = 2 and 3, refuse with `FinalIdentity`;
    - Empty at n = 1 and 3 refuses with `Shape`.
    - It also pins `roots_row` for the four join errors.
  - **First root below its threshold.** Each refuses `PAYLOAD-NOT-ADMISSIBLE` / `root` (`FirstQuorum`):
    - root 1's envelope with one signature;
    - root 1 signed by 0, 1 and 2 when the list (signed under root 2) revokes 1 and 2, so the keys are excluded before the threshold.
  - **A link failure takes its S5 row.**
    - Continuity: root 2 signed only by its own keys gives `ROOT.CHAIN_OLD_THRESHOLD` / `link:0`.
    - Possession: root 2 signed only by root 1's keys gives `ROOT.CHAIN_NEW_THRESHOLD` / `link:0`.
    - On 1→3, root 3 carrying one of root 2's keys gives `ROOT.CHAIN_OLD_THRESHOLD` / `link:1`.
    - On 1→3, a list revoking root 2's keys 20 and 21 gives `ROOT.CHAIN_NEW_THRESHOLD` / `link:0` (revoked keys excluded).
  - **Revocation under M (r11).** On 1→2, a list signed by root 2 is admitted and its entry carried. A list signed only by root 1's keys refuses `PAYLOAD-NOT-ADMISSIBLE`.
- **`floor_publication_tests.rs`, one new test.** A floor publication on a 1→2 store leaves the heads unchanged. The next invocation's fenced first read is admitted with epoch and floor `rootVersion` 2, and so is the native reread.
- **`accepted_store_fixture_tests.rs`, one new test.** For n = 2 and 3:
  - the closure lists n roots, the head last;
  - the root admission's `root` is the head;
  - each `rootVersion` is k+1;
  - root 1 carries 3 signatures and each link 6;
  - the list is at `rootVersion` n;
  - `current_record_bindings::bind` and `bind_retained_head` accept the store.
- **`trust_bootstrap_tests.rs` (X4B-a, as the r10 note requires).** `a_multi_link_root_chain_is_authenticated_and_recorded_in_full` pinned the confirming admission's `FirstIdentity` refusal as a stated gap. It now expects the confirming admission of X4B-a's rotated default release (1→2) to admit, with epoch `rootVersion` 2 and `rootVersion` floor 2. Its acceptance assertions are unchanged.
- **Without the reader change.** If `authenticate` passes the head's context instead, the rotation, first-root, link and revocation tests fail. The rotation refuses at `FirstIdentity` on the incomplete row, as your r10 review predicted.

**Moved pins.**
- `MEASURED` goes from (23, 44, 35371) to (23, 46, 35371): two edges, one each for the anchor's closure load and first-body load, both already retained, so there is no new object or byte. That is the "+2" the r10 drafter expected.
- `NATIVE_MEASURED` goes from (31, 253, 36008) to (31, 265, 36008), and `NATIVE_AFTER_FLOOR` from (31, 253, 32103) to (31, 265, 32103). A native load always revisits its location (`refresh_cached`), so each of the two loads charges six edges: the load, two each for `trust/` and its collection, and the file. Objects and bytes are unchanged.
- All stay within `TRUST_VIEW_COST`.

## Judgment calls (lead decisions, narrowest reading)

1. **No inventory successor; v120 unused.** No file is added, so there is no row to add. verify_design's `inventory_successor` admits only strictly additive successors: a proper superset of rows, with every inherited row equal by value. A v120 that changed only a description could not be selected.
   - The one description this unit makes false is X4B-a's `trust_bootstrap_tests.rs` row in v113. It ends "with the reader's current FirstIdentity refusal pinned as a stated gap", and that test now asserts admission. It is noted for the description-only successor batch, as v116's README left out-of-date descriptions ("now out of date" for `operation_handoff.rs`, and others).
   - Every other changed row stays true:
     - `current_trust_admission.rs`: "authenticates the accepted state from the accepted root", which is now r10's N;
     - `trust_ordinary_roots.rs`: generic.
   - The X4T-0 and test rows do not mention the knob or the new cases, as v116 recorded for `Spec.store`.
   - Precedent: 463h (v115 unused), 461a, 464 code.
   - The lead had asked for v120 on v113. This call declines it for the verifier reason above, and the lead is told.
2. **An empty `rootChain` is refused by the closed shape first.** `PayloadMetadataClosureV1` bounds `rootChain` to 1..64 documents, so admission refuses an empty one (`Shape`) before the join. The explicit `EmptyChain` check is kept as the stated join and cannot be reached through an admitted closure. Both take the incomplete row. The test drives the shape route with the one unshaped fixture record.
3. **The closure is loaded twice and charged once.** `bind_chain_anchor` loads it, and `ordinary_inventory::prepare` loads it again inside `prepare_authenticated_times`. `Budget` keys retained bytes by (collection, digest), so the second load costs only an edge. Passing the admitted closure into `prepare` would change the ordinary-inventory and ordinary-targets signatures, which r10 does not ask for.
4. **A first `rootChain` body that is not a root refuses `FirstIdentity`, on the incomplete row.** The closure is misbound. `ROOT.*` rows come only from chain evaluation (item 10), and `PAYLOAD-NOT-ADMISSIBLE` is for signatures and quorums.
5. **Uniform anchor path.** The one-root case is not special-cased. `bind_chain_anchor` always loads `rootChain[0].body`, which for n = 1 is the head's, already retained, so the result is r9's (item 3, "One root").
6. **The anchor is not kept in the view.** `AdmittedCurrentTrust` gains nothing: the epoch and floors were already M's. Tests observe N through the authentication proof (`original_accepted_ref`, `chain()`), which the reader's descendant test module can reach.
7. **r11 needed no reader change.** `open_heads` already passed `input.head.root()` (M) to `verify_revocation` and to the catalog's `verify_envelope`. The r11 test pins both directions on a rotated store.
8. **The fixture's rotation follows `signed_release`'s shape** (law 463 tests): `rootKeys` rotated to unused seeds, links signed by both sets, and the list under the final root's keys. It is X4T-0's own, built from `quorum_root` and `sign` only, not from X4B-a's producer or test release (item 13 rejects that coupling).
9. **Not added:** item 12's older "a root chain through expired intermediates" case. It is not in the r10 bullet assigned to X4T-a3, and the pre-time authentication never consults intermediate expiry.

## Checks on 0fc8ea2 + subject

- **Full workspace, three runs:**
  - Run 1: 1549 passed, 1 failed, 3 ignored. The failure was `custody::operation_handoff::tests::live::a_revoking_update_is_seen_by_the_checkpoints_own_final_observation`, which panicked in its scratch setup (`operation_handoff_tests.rs:110`) with `Custody { subject: "ancestor-acl" }`. Three other worktrees' `cargo test` runs were active at the time. This is the shared-temp churn residual that F4 named as candidate F5. The test uses the default one-root store, and this diff does not reach its setup. It then passed 3 of 3 times in isolation.
  - Runs 2 and 3, on the final bytes: 1550 passed, 0 failed, 3 ignored each. That is X4B-a's recorded 1543 plus the 7 new tests. The security lib had 886 passed and 2 ignored.
- **Targeted:** `cargo test -p opensip-security --lib -- current_trust_admission accepted_store_fixture floor_publication live_observation ordinary_roots ordinary_targets trust_bootstrap` gives 79 passed and 1 ignored (the existing real-host clock test). X4a's `live_observation` and `operation_live` tests pass unchanged.
- **Lint:** `cargo clippy --workspace --all-targets --locked -- -D warnings` and `cargo fmt --all -- --check` are clean.
- **Package edges:** `check_package_edges --lane host` against v113 passes, with 19 declared and 19 resolved.
- **verify_design:** the live run (`--architecture`, `--lock design-lock.json`, `--implementation`) passes, with 80 inventory successors, 72 contract successors, 16 inheritance rows and v113 selected.
- **No contract change.** No public code, registry row, schema or generated file is touched. The rows used (`CONFIG.CUSTODY_REFUSED`/`installation-incomplete`, `PAYLOAD-NOT-ADMISSIBLE`, `ROOT.CHAIN_OLD_THRESHOLD`, `ROOT.CHAIN_NEW_THRESHOLD`) are all existing.

## Decide

- **The law.** Does the diff implement item 3's two roots and closure join, item 4 (r11), item 10's incomplete row and item 12's r10 tests exactly? Is `verify_captured_core` unchanged?
- **The join.** Is it reference-exact (body and envelope), and does it run before the inventory's `SigningRoot` check could mask it?
- **The fixture.** Is the X4T-0 knob test-only, are its defaults byte-identical to r9's, and does it not depend on X4B-a?
- **X4B-a.** Is the flip of X4B-a's `FirstIdentity` pin to admission (epoch and floor 2) right?
- **The pins.** Are the moved pins explained: +2 edges in memory, +12 natively, no objects or bytes?
- **The judgment calls.** Are 1 to 9 sound and the narrowest reading? In particular:
  - 1: no inventory successor under verify_design's additive-only rule, with the X4B-a test row deferred to the description batch;
  - 2: the empty chain reached through the shape.
- **The run-1 failure.** Is it unrelated to this diff?
- **Anything else wrong?**

There is no inventory candidate, so verdict ACCEPT (not ACCEPT-UNIT) and no `inventoryCandidateAssessment`. review.json must contain top-level "verdict" (`ACCEPT` or `REQUIRED-FINDINGS`), "requiredFindings" and "subjectSha256" (the sha256 of subject.diff, `ddd2e27ef0ebbf2f0ac214d4681988b37a93d7c7119a7a69e39f23881177ecb0`). Write REVIEW.md and review.json. Do not commit.
