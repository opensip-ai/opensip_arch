# X8 r5

Claude Opus 5.5 leads. Grok is the single reviewer. Law review only. No product cargo. Git was read-only. `~/Library/Application Support/OpenSIP` is absent. The private 413 fixture was not read.

Verdict: **ACCEPT**. `noAcceptedOutcomeChanged` is true. r5 records five facts already decided by X3d r8, EC1, and the accepted X8c r1 build. It changes no accepted outcome of X8 r4 or of any other law.

| | |
|---|---|
| Subject | `docs/implementation/m2/refusal-suite-x8/PROPOSAL.md`, 51911 bytes, `ba6915b9e06dc8aabaefa4eec79f051183938860dc1294edff86973a3210e33d` |
| Preserved snapshot | `docs/implementation/m2/refusal-suite-x8/PROPOSAL-r4.md`, 46639 bytes, `3b0ead97b2e925ad1eef2456ad0f47b4fd5b963ffd0bfaea960faa7e83c85b00` |

The snapshot equals `subjectSha256` in `reviews/grok-refusal-suite-x8-r4/review.json`, whose verdict is ACCEPT. Reversing the title, the inserted `r4 ACCEPTED by Grok on 2026-10-02.` sentence, the r5 header, the item-5 corpus note, and the block after the B table reproduces `PROPOSAL-r4.md` byte for byte. The B-table rows are untouched. The insertions name codes and rows the B table and X3d r8 already name.

## Does r5 change any accepted outcome?

No. No item, trial result, case, group, code, fragment rule, feature, module, behavioural case, expected outcome or row, unit scope, dependency, or forbidden substitute of X8 r4 is edited. No accepted outcome of X3d r8, EC1, X9, X4, X4a, X5, X6, or X7 is edited. The notes sit beside the r4 sentences and state obligations those sources already have.

The two lines that are not copied from the snapshot are the title (`r4` to `r5`) and the r4 header, which carries `r4 ACCEPTED by Grok on 2026-10-02.` The snapshot omits that acceptance stamp. The working law already carried it, and the r4 review is ACCEPT on the snapshot bytes. That stamp records the existing acceptance.

## r5 may stand on the accepted X8c review

The r5 header names records 2 to 5 as lead decisions in `reviews/grok-refusal-cases-x8c-r1/REQUEST.md`, judgment calls 1, 3, 4, and 7, and says that if the X8c review changes one, a later record corrects the matching note. That sentence was accurate when the law was drafted. X8c r1 is now ACCEPT (`/tmp/opensip-implementation/reviews/grok-refusal-cases-x8c-r1/review.json`; subject diff `8b394a1b8a9c7f2079a9c49b43394c0cf48c60676da356322f3f4e3e9d6b712f`). The review left calls 1, 3, 4, and 7 in place and recorded notes (a) through (e) for this revision. r5 does not need to wait. The header's correction clause stays a standing rule, and it does not claim that the review changed a note.

`hashes.txt` still labels that X8c request "pending". The pin is the request file, which matches `c89e5f5a04c48243528d1c0ea127d51a2246b905ef196ece6189c909714a3590`. The label is the request's status at pinning. The verdict is the later acceptance.

## Each record stays inside its source

Both EXIT-PLAN entries list exactly these five: "X8 B2 wording owed (2026-10-02)" names the B2 comparison, the owner reading, and an unchanged B6; "X8 record notes owed after X8c (2026-10-02)" names the B2 wording and owner, the corpus path, the REV on B1, B2, and B4, B7's drift and B6's gate at the public boundary, and B0's `#[path]` route. There is no sixth item.

1. **B2.** X3d r8 item 3 step 1 says the `ReplayedRun`'s evaluator closure equals the session's core evaluator closure, derived by security from the same authenticated inventory as the core closure, exposed as `CommitSession::core_evaluator_closure()` (EC1). A mismatch stays item 9's invariant row. The r8 header records that r7's "selected core closure" is `core_closure()`, a `kind: "core"` id, and that replay requires `kind: "evaluator"`. The note states that comparison and the owner reading "X3d-2, binding X3d-3". The table cell still says `X3d-2`, and the diagnostic row stays the invariant row. B6's revocation still names the session's core closure. That is EXIT-PLAN's owed wording, X8c note (a), and the r4 pattern of leaving the accepted sentence in place.

2. **Corpus path.** The item-5 note says `crates/evaluator/tests/fixtures` holds no Run, and that the cases use host `crates/host/tests/fixtures/replay-fixtures.json` for B1 and B8, with B0's synthetic candidate. At product `a2c5e8b` that evaluator directory holds `policy-pack-plan-fixture.json`, `policy-pack-test-fixture.policy.json`, `policy-pack-test-registry.json`, and `capability-manifest.golden.cve1`. None of them is a Run. Host `replay-fixtures.json` is present. X8c call 3 and note (b) name this path. The header's phrase "only policy-pack fixtures" is the wording of that X8c request call, which X8c r1 accepted. The golden capability manifest is also in the directory. It is not a Run, and the operative record is the host replay path. That extra file does not make the corpus note unfaithful.

3. **REV on B1, B2, and B4.** X3d r8 item 7 step 1 appends one REV when the gate is latched. X8c call 4, accepted, says every certain refusal before admission latches the gate and that these cases assert REV 1 and CLN 0. The note adds that REV to the census the table already lists. B1's listed census is "no attempt row, no SEAL, no receipt"; B4's is the planted row, unchanged and alone, with no SEAL. A carrier REV is a further end-path count. X8c r1 records that count on these cases. The table bytes stay, and the note contradicts no cell.

4. **B6 and B7 at the public boundary.** X8c call 7 says `OperationGuard::drift` is `pub(crate)`, and that `PublishedCommit`, `SessionEnd`, and both `scenario` modules expose no drift reader. At `a2c5e8b` the only `fn drift` is `operation_guard.rs` `pub(crate) fn drift`, and `state()` on the guard is `pub(crate)`. The note shows B7 as `Committed` and not latched, with B0's census, and shows the publication through item 5a's self-checks. It shows B6 as `Refused` on `TRUST.COMPONENT_REVOKED_DURING_OPERATION`, with the one REV `finish` appends under item 7 step 1, and B3's census. It cites X4a's `an_unrelated_revocation_update_continues_as_drift_without_the_fence`, which at the pinned `operation_live_tests.rs` asserts `drift() == ["revocation-unrelated"]`. The note does not repeat the X8c request's phrase "the REV that `finish` owes only for a latched gate". The accepted X8c review's note (d) likewise states the REV a latched gate owes, without that word.

5. **B0's candidate route.** X8c call 1 and note (e) include storage's `crates/storage/src/crash_matrix_support/run_candidate.rs` through `#[path]`, with a test-crate shim over host's public `embedded_schema_registry()`, and pin the same 48 schema files in the same order (`the_candidate_registry_is_storages_selected_registry`). Storage's `commit_tests.rs` at `a2c5e8b` includes that file the same way. The candidate's crate-private reference is `crate::schema_sources::registry()`. X9 item 2 still says no manifest enables `crash-matrix`. The note says the include also serves B2 to B7, which is how X8c builds those cases, and that no product file, cfg site, feature, export, or site list changes. Item 4b stands.

## B7 and X3d item 7, as a note on X8c

X3d r8 item 7 step 1 appends one REV if a durable SEAL has no evidence commit, if the gate is latched, or if "a revocation was observed". Read on its own, that third bullet covers an unrelated revocation as well as a revoking match. B7 observes an unrelated revocation, and its accepted census is B0: no REV. r5 leaves that row alone.

At `a2c5e8b`, `StoppedSession::finish` appends the REV when the SEAL lacks evidence, when the guard state is latched, or when the guard cause is `StopCause::Revoked`. The X8c review records that an unrelated publication continues as drift `revocation-unrelated` and that B7 finishes with B0's census. The wide reading of the law sentence belongs against the X8c request's "only for a latched gate", which the accepted review did not carry forward. r5's own sentences stay inside the latched-gate REV for B1, B2, and B4, and inside item 7 step 1 for B6's one REV. Those sentences are right.

## Snapshot and preservation

`PROPOSAL-r4.md` is the accepted r4 subject, 46639 bytes, sha256 `3b0ead97b2e925ad1eef2456ad0f47b4fd5b963ffd0bfaea960faa7e83c85b00`. It already existed. Every accepted r4 sentence remains in place. The r5 header says what stands: item 4b's shared site list and joint predicate, X9 item 2, item 4e, every B row's alteration, expected outcome, and row, B6's core-closure revocation, X8c's dependencies, and "X8 adds no public code, row or detail".

Nothing else is wrong. The worktree was not committed.
