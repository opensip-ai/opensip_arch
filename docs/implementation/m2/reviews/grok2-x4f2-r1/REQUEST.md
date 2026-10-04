GROK2 review: unit X4-F2 r1, expiry at the fenced read. It implements law X4T r12, accepted by Codex on 2026-10-04 (`reviews/grok2-x4t-f2-r1/`, verdict ACCEPT, no required findings, one nonblocking observation). X4T r12 closes the follow-up you found in X4-F1 r1 (your judgment call 6), which M2-COMPLETE r3 §5 row 23 records: "the fenced read computes the expiry flags but never applies them". Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-UNIT** on the diff. This is a product code unit, a successor to X4T-a, X4T-b and X4-F1. It adds no file, so it has no inventory successor and no design selection, as for X4-F1.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/grok2-x4f2-r1`. If you build or test, use a `CARGO_TARGET_DIR` under that directory.
- Run git read-only, and only against the worktree named below.
- Don't run a crash-matrix run set while any other `cargo`, `rustc` or test binary is running on this machine, and don't run cargo while someone else's run set is running: the 5 s timing guard fails under load. Check `ps` first, and ask the lead if in doubt.
- Run every command at `nice -n 19` (a run set at normal priority, with nothing else running), with a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## Law

All under arch `docs/implementation/m2/`, accepted. Pins are in `hashes.txt`.
- **`trust-admission-x4t/PROPOSAL-r12.md`** (X4T r12, 79182 bytes, sha256 `cf566db7…`, equal to Codex's `subjectSha256`; accepted at arch `d13dc1e23`). The live `PROPOSAL.md` carries only the acceptance note; review against the r12 snapshot. The parts this unit implements:
  - **Item 6, "Expiry at the fenced read" (lead decision).** At tEval (`TimeAdmission.evaluation`), never W, F or a monitor sample, the fenced read applies `EV-CLOCK` to the stored roles over S4's three states (`TimeAdmission.expired`), by X4B r5 item 4's mapping through `role_machine::clock`. It is the admission's last decision, after every refusal of items 2 to 5 and S4's steps 1 to 4. Nothing is recorded. Report-only computes the same states, join and refusal. Each read clocks its own capsule's stored states once; a reread never clocks the start view's clocked states. If the states are absent, the read refuses on the host I/O row.
  - **Item 1 (r12).** Every read joins twice: over the stored states before authentication, and over the clocked states. The view carries the clocked states (`role_states`) and the second join's standing.
  - **Item 7 (r12), "Before a clocked refusal too".** The fenced read performs its normal write-ahead (same producers, publication and owner advance, only when S4 proposes a change), then publishes the continuation row, and returns no view. Check 3 and the closing rechecks run where they run today, and their refusals are published instead. The owner has advanced inside the read, and the gate's failed step spends the gate, so the refusal is never relabelled `required-files-changed`.
  - **Item 9 (r12).** The clocked continuation refusal is published at the lease-free point, before any lease. The unfenced reread is unchanged.
  - **Item 10 (r12).** Only the existing continuation row: request-rejected, exit 2, `EXTENSION.ADMISSION_REJECTED`, detail `CONTINUE-CORE-NOT-TRUSTED`, subject `core:expired` or `core:stale-revocation`, expiry winning when both apply. A final root expired at tEval is never `ROOT.FINAL_EXPIRED`. A catalog expiry alone is `ExistingOnly`, admitted.
  - **Item 12 (r12)** lists the tests, and **item 13 (r12)** the unit: its scope (`admit_bound` and `fenced_first_read`; `live_observation`, the reread and every row and code unchanged), X4T-0's three test-only knobs, the controls and the X9 regression subset.
  - **Forbidden substitutes (r12):** an unclocked fenced view; a clock at any instant but tEval; a clocked refusal before the write-ahead, or a write-ahead skipped because the read will refuse; a recorded `EV-CLOCK` or a rewritten role state; a reread clocked from the start view's clocked states; `ROOT.FINAL_EXPIRED`, `TRUST.NO_ADMITTED_TIME_CONTEXT` or a new code or subject for a clocked expiry; a refusal on a catalog expiry alone.
- **Codex's law review**, `reviews/grok2-x4t-f2-r1/REVIEW.md` and `review.json` (the directory name was kept when the law moved from you to Codex). Its **X4T-R12-NB-01** asks that the sticky-refusal control's "writes nothing" assertion use an **anchor-preserving clock sample**: a same-boot backward deviation greater than 24 hours, with no excusing witness and no F or L advance, so S4 keeps the anchor and `needs_write` is false. A smaller set-back rewrites the anchor and correctly publishes. The unit's control uses exactly such a sample (below).
- **The selector** `reviews/grok2-x4t-f2-r1/evidence/x9-rows.py` and its pinned output `x9-rows.json`.
- For context, as X4-F1 pinned them: `live-guards-x4/PROPOSAL.md` (X4 r7: item 8's lease-free row, and its r5 note that `Continuation::Refuse` stays X4T's admission refusal), `trust-bootstrap-x4b/PROPOSAL-r5.md` (X4B r5 item 4's mapping), the security contract's S4 (`docs/v2/contracts/product-v1/security-and-lifecycle.md`), and your X4-F1 review, `reviews/grok2-observer-expiry-x4f1-r1/REVIEW.md` (judgment call 6).

## Subject

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-x4f2`, detached at product main `3f6f9a5a2543b70c0c259e041dc65d7e29164a0d` (S21). Nothing is committed or staged, and no file is added, removed or renamed. `crates/security`, `storage`, `host` and `platform` are unchanged from `15c0779` (X4-F1's integration) to `3f6f9a5`.
- **Diff:** `git -C /Users/sb/code/opensip-ai/opensip-x4f2 diff 3f6f9a5` is 47332 bytes, sha256 `ffc4ef1e038199c13b2c1fa0139405239f57f362ee274f46bb26835a3f6835be`, with 10 files, +620 −42. A copy is at `evidence/x4f2.diff`.
- **Toolchain:** `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin`, Python `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`.
- **Evidence:** `evidence/` in this directory. Every file is pinned in `hashes.txt`.
  - **Scripts, as run:** `lanes.sh`, `release.sh`, `set.sh`, `x9.sh`, `compare.py` and `results.py`. They name the lead's scratch paths.
  - **`lanes-summary.txt`** and **`results.json`** (test counts and the X9 summary).
  - **`release-absence.json`** and **`release-summary.txt`.**
  - **`x9/`:** the selection (`x9-rows-main.json`, `rows-storage.txt`, `rows-host.txt`); `source-pins-first.txt` (taken before the lanes) and `source-pins.txt` (rerun on the final diff); `waits.txt` (the load checks); `overlap.txt` (the 10 s sampler); `x9.summary`; `compare.json`; and the four run sets' `matrix.json` files.

## The gap, at `3f6f9a5`

- **The fenced branch never clocks.** In `current_trust_admission.rs`, `admit_bound` (`:969`) joins the stored role states once (`:981`, `let standing = standing_of(&roles)?`). Its `ReadMode::Fenced` arm admits time, then returns `(roles, standing, Some(admission))` (`:1058`): the stored roles and the stored standing. `TimeAdmission.expired` carries S4's three states at tEval, and nothing reads it there. Only the `ReadMode::Reread { at }` arm (X4-F1) clocks.
- **Consequence.** A store already expired or stale at the handoff's tEval is admitted at the lease-free point, takes its lease, runs X3b's floor step and the carrier start, and fail-stops as `OBSERVER.FAIL_STOP` `standing` at its first tick or checkpoint: the wrong class and remedy (your X4-F1 r1 call 6; M2-COMPLETE r3 §5 row 23).
- **Why X4T-0's default store hides it.** Its L is the list's issue time, 2026-10-01, so S4's plausibility bound (W ≤ A + 90 d) stops a fenced read's W exactly at the list's staleness boundary.

## What X4-F2 changes

**`current_trust_admission.rs`, `admit_bound` (the fenced arm, `:1107`–`:1127`).**
- After S4's own refusals, the arm takes `admission.expired` (absent: `TrustRow::HostIo`, cause `expiry`, as X4B-a's `refuse(TrustRow::HostIo, "expiry")`), clocks the stored roles with X4-F1's own `clock_roles` (`:1005`), and joins them with X4-F1's `standing_of` (`:976`). The view carries the clocked roles and that standing; with no state true they equal the stored ones.
- A refusal from that join is **not a view**. It returns `Admission::Clocked`, which carries the refusal, the floors, the unchanged `TimeAdmission` and the pending write-ahead (`PendingWrite`), and nothing else.
- The first join over the stored states still runs before authentication (`:1036`) and still refuses there (X4B's stored `Expired` and `StaleRevocation` stores keep their precedence); its standing is no longer kept, because the view's standing is the second join's.
- The `ReadMode::Reread { at }` arm (`:1075`) is untouched: it clocks its own capsule's stored roles at its own instant, once.

**`current_trust_admission.rs`, the new private `Admission` (`:243`–`:292`).** `View(Box<AdmittedCurrentTrust>)` or `Clocked(Box<ClockedRefusal>)`. Both are boxed because the two differ by 432 bytes, which clippy's `large_enum_variant` refuses under `-D warnings`. Its methods: `floors()`, `time()`, `take_pending()` and `into_view()`, which turns `Clocked` into `Err(refusal)`.
- `admit_bound`, `admit_bound_native` and the new private `admit_current` (the former body of `admit_current_trust`, `:1181`) return `Admission`.
- `admit_current_trust` (`:1169`) keeps its signature and returns `admit_current(…)?.into_view()`: the reread (`live_observation`), the in-memory tests and every other caller see a clocked refusal as a plain `TrustRefusal` and write nothing.
- `admit_native` (test-only for fenced reads) converts after its closing `state.v1` recheck (`:1230`).

**`floor_publication.rs`, `fenced_first_read` (`:948`–`:1001`).** It calls `admit_current` and holds the `Admission`. Check 3 compares `admission.floors()`. The pending write is `admission.take_pending()`, judged by `needs_write` against `admission.time()` exactly as before. The refusal comes out by `admission.into_view()` where r11 returned `Ok(view)`: after a confirmed `publish` (`:995`), or after the closing fence and owner rechecks (`:1000`). Check 3's rollback, a failed build or publish, and a failed recheck all still return first.

**Unchanged:** `live_observation.rs`, `operation_guard.rs`, `operation_handoff.rs`, `trust_time.rs`, `role_machine.rs` and `trust_bootstrap.rs` (no byte); every row, code and subject; the write-ahead's producers, protocol and reservation; every ledger and charge; every crash point and scope; every read, write and clock sample.

**X4T-0's three test-only knobs (`accepted_store_fixture.rs`).** `Spec` gains `manifest_issued`, `root_expires` and `catalog_expires`, each `Option<&'static str>`, `None` by default.
- Each is signed into its document by the fixture's existing signing path: the bootstrap manifest's `issuedAt`, the signing root's `expiresAt` (through `signed_chain`'s existing `final_expires`), the catalog's `expiresAt`. No stored byte is edited.
- They apply on both paths: X4B's producer (`produce`, the macOS default) and the module's own `construct`. In `construct`, F and L follow the acceptance's own rule, max(2026-10-02, the manifest's issue time).
- With every knob `None` the format strings and arguments are those of `3f6f9a5` (`ISSUED`, `CATALOG_EXPIRES` and `ACCEPTED` are the old literals), so every default store is byte-identical. The fixture is compiled into the `crash-matrix` and `scenario-fixtures` builds (`accepted_store_files`), so the X9 comparison below confirms this for the matrix's stores.

**Test plumbing.** `root_payload::write_accepted_trust_issued` (re-exported in `trust.rs`; `write_accepted_trust` delegates to it), `ReadFixture::accept_trust_issued` (`write_trust` delegates to a private `write_trust_issued`), `eligible_on` in `operation_handoff_tests.rs` (`eligible` delegates to it), and `try_begin_shifted` in `operation_live_tests.rs` (X4-F1's `begin_live_shifted` is now `try_begin_shifted(…).unwrap()`, with the same seam).

| File | Change |
|---|---|
| `crates/security/src/trust/current_trust_admission.rs` | `Admission`, `ClockedRefusal`, the fenced arm's clock, `admit_current` |
| `crates/security/src/trust/floor_publication.rs` | `fenced_first_read` publishes a clocked refusal after its write-ahead or closing rechecks |
| `crates/security/src/trust/accepted_store_fixture.rs` | the three knobs |
| `crates/security/src/trust/root_payload.rs`, `trust.rs`, `custody/installation_read_fixture.rs`, `custody/operation_handoff_tests.rs` | test plumbing |
| `current_trust_admission_tests.rs`, `floor_publication_tests.rs`, `custody/operation_live_tests.rs` | eight new tests; `try_begin_shifted` |

## Tests

The stores use X4T-0's knobs. The acceptance's wall (its anchor) is 2026-10-02T00:00:00Z on boot `boot-1`. With the bootstrap manifest issued at 2026-10-03T00:00:00Z (the latest the acceptance admits: not beyond its wall plus 24 h), the store's A, F and L are 2026-10-03 and S4's plausibility bound reaches 2027-01-01T00:00:00Z. The list is still issued 2026-10-01, so it is stale strictly after 2026-12-30T00:00:00Z: a fenced read can now reach staleness. Every knobbed store is X4B's producer's (`produced` is asserted). The fenced reads observe on another boot than the anchor's, so continuity does not apply and tEval = W.

**In memory, through `admit_current_trust` (`current_trust_admission_tests.rs`):**
- `a_fenced_read_refuses_a_list_already_stale_at_its_t_eval` (`:444`): at exactly 2026-12-30T00:00:00Z the read is admitted, `InstallGateRequiredForNewProcess`, the four carried roles `trusted`, tEval = W and `expired = (false, false, false)` (S4's strict `>`). One second later it refuses `core:stale-revocation`, `CONTINUE-CORE-NOT-TRUSTED`.
- `a_fenced_read_refuses_a_root_already_expired_at_its_t_eval` (`:469`): with the signing root expiring 2026-11-01, one second before is admitted and `expiresAt` itself refuses `core:expired` (S4's `>=`), never `ROOT.FINAL_EXPIRED`. With the root expiring 2026-12-31 on the later-manifest store, 2026-12-30T00:00:01Z refuses `core:stale-revocation` and 2026-12-31T00:00:00Z, where both hold, refuses `core:expired`.
- `a_catalog_expired_alone_at_the_fenced_read_is_admitted_existing_only` (`:495`): with the catalog expiring 2026-11-01, one second before is `InstallGateRequiredForNewProcess`; at it, `ExistingOnly`, with `role_states` TR-INDEX `expired`, bundle, component and core `trusted`, profile and repair `unbootstrapped`; `time().expired = (false, true, false)` and the handoff clock is set.
- `the_fenced_reads_clock_is_x4f1s_mapping_and_transition_and_report_only_agrees` (`:527`): one store whose catalog (2026-11-01), staleness (after 2026-12-30) and root expiry (2026-12-31) all fall inside its window. At eight walls from 2026-10-03 to 2027-01-01 (each boundary, a second before and after where it matters), for both live and report-only reads, it computes the expected states independently (S4's `>=`, `>=`, `>`), applies `clock_roles` and `standing_of` to the stored roles, and requires the fenced read to give exactly that: on admission the standing, every `role_states` entry, `expired` and `report_only`; on refusal the row.
- `a_reread_after_a_clocked_fenced_read_clocks_its_own_stored_states` (`:573`): after a fenced read admitted `ExistingOnly` (catalog expired), a reread at T = tEval (`HandoffClock::advanced` on the same sample) gives the same states and standing and no time; a reread advanced by monotonic time past staleness (with a 2020 wall) refuses `core:stale-revocation` from the store's own stored, all-`trusted` roles.

**On native files, under a held fence (`floor_publication_tests.rs`):**
- `a_clocked_refusal_comes_after_its_confirmed_write_ahead_and_is_sticky` (`:801`), run twice: through X4T-b's `fenced_first_read` and through X4B-b's `bootstrapping_first_read` (with `BootstrapSource::unreached()`; the first result is not F absent, so it is returned as is).
  - **Write-ahead, then refusal.** A fenced read at 2026-12-30T00:00:01Z (`boot-2`, mono 100) refuses `core:stale-revocation`. The owner holds exactly one confirmation; `state.v1` on disk is the confirmed bytes and the owner's; its F (`evalHighWater`) is tEval and its anchor is this sample; L, every `roles` member and each carried role's `ST-TRUSTED` are unchanged; the revision rose by one.
  - **Sticky, with an anchor-preserving sample (NB-01).** A later invocation binds a new owner to that `state.v1` and reads at 2026-12-28T00:00:00Z on `boot-2`, mono 160: the same boot as the anchor, about two days behind its continuity (W − (anchor wall + 60 s) < −24 h), with no excusing witness. S4 records `SessionRegression`, keeps the anchor, and evaluates at tEval′ = max(F, W′, A) = F; F and L do not advance. The read refuses the same way, the owner has no confirmation, `state.v1` is byte-identical and the trust tree has the same number of files.
- `a_report_only_or_horizon_refused_read_of_an_expired_store_writes_nothing` (`:855`): report-only at the same wall refuses `core:stale-revocation`. A wall beyond A + 90 d (2027-01-01T00:00:01Z, another boot), where the list is also stale, refuses `beyond-horizon` before any clock. Neither writes: same bytes, same inode, same file count, no confirmation.

**Through the real handoff (`operation_live_tests.rs`):**
- `a_list_already_stale_at_the_first_reads_t_eval_refuses_at_the_lease_free_point` (`:520`). The fixture's P0 store is replaced by the later-manifest accepted store (`accept_trust_issued`), the project is registered (`eligible_on`), and the scripted monitor clock's wall is shifted so the first read's tEval is 2026-12-30T00:00:01Z.
  - The handoff refuses as `OperationRefusal::Trust` with `TrustRow::Continuation("core:stale-revocation")`, whose `row()` is `OperationRow::Installation(T::TrustContinuation { subject: "core:stale-revocation" })`: X4T's own row (request-rejected, exit 2, `EXTENSION.ADMISSION_REJECTED` through host's map), never `OBSERVER.FAIL_STOP`, never `required-files-changed`.
  - At every monitor clock sample, the probe saw the fence held and both lease carriers free.
  - The floor publication was confirmed: `state.v1` changed, its F is the first wall, and its `roles` are the accepted ones.
  - No `trust/carrier-floors` (X3b's floor step never ran), no `grant-journal.sqlite` or witness, and the fence and N are free. The guard and its observer never existed.

**Mutation checks (phase 1, then restored):**
- With the fenced arm's clock removed (`clock_roles` not applied), all eight new tests fail.
- With the clocked refusal returned before the write-ahead (the rejected order), the native write-then-refuse test and the handoff test fail; the report-only and horizon test still passes, as it should.

**Existing tests that must not move (item 12, r12), all in the lanes below:** X4-F1's, among them `a_list_going_stale_during_the_operation_fail_stops_before_any_further_effect` (its first read's tEval two seconds before staleness, so still admitted) and `a_rereads_clock_follows_x4b_item_4_and_the_role_machine`; X4B-a's and X4B-b's (stored `Expired` and `StaleRevocation` still refuse at the stored-state join, before time; the confirming admission's clock at the acceptance's tEval gives the recorded states); X4T-b's floor-publication tests, `time_refusals_take_their_rows`, and the S4 reference fixtures.

## Judgment calls

1. **A clocked refusal is a type, not a flag.** Item 13 says the refusal "travels with the fenced read's pending write, and is never published as a view". `Admission::Clocked` carries only what item 7 needs (floors for check 3, the S4 outcome for `needs_write`, the pending write) and the refusal; it has no standing and no epoch, and the only way out is `into_view()`, which yields `Err`. **Rejected:** a refusal field inside `AdmittedCurrentTrust`, which every consumer would have to remember to check; and a richer error type on `admit_current_trust`, which would change the reread's and every test's signature for a case only the fenced read has.
2. **Where it is published.** Exactly where r11 returned the view: check 3 first (its `trust-rollback` wins), then either the write-ahead (only when `needs_write`, unchanged) followed by the refusal, or the closing fence and owner rechecks followed by the refusal. A failed build, publish or recheck returns its own row first. This is item 7 r12's "Check 3 … and the read's closing rechecks run where they run today, and a refusal either raises is published instead".
3. **The hold after the refusal is unchanged code.** After a confirmed `publish`, the owner has advanced inside the read; `fenced_operation_read`'s `?` drops the confirmations with the error, and the handoff's failed `gate_step` spends the gate, so no later recheck compares the predecessor's sample (as Codex checked for the law, and as X4B-b's recorded-acceptance-then-continuation-refusal control shows). The handoff test pins the observable result: `TrustContinuation`, never `required-files-changed`.
4. **The first join is kept for its refusals only.** Its standing would be stale once the second join runs. A stored state that does not continue (`Expired`, `StaleRevocation`, `Revoked`, `QuorumLost`, `Recovery`, `Unbootstrapped`) still refuses there, before authentication and before time, with the stored state in its subject, as in r11 and as X4B's tests pin. So a store whose core was recorded `StaleRevocation` refuses `core:stale-revocation` even at a tEval where its root has since expired; the clock is consulted only for stores the stored join admits.
5. **Absent states are the host I/O row,** cause `expiry`, exactly X4B-a's treatment (`trust_bootstrap.rs:639`). S4's `finish` sets them on every admitted evaluation, so this is unreachable today; it is never read as "not expired" (S4 step 2).
6. **The knob is the bootstrap manifest's issue time.** Item 13 asks for "a later issue time for one signed document, which raises A". The manifest's `issuedAt` enters the view only through `newest` (`ordinary_targets.rs:531`), that is A, at the acceptance and at every fenced read. The list's issue time is the staleness anchor itself, so raising it would move the boundary with A; the catalog's is also read by its schema owner (`recovery_catalog.rs:192`) and the root's by the root owners (`admitted_roots.rs:49`). The latest value the acceptance admits is its wall plus 24 h, 2026-10-03T00:00:00Z, which gives a two-day staleness window, 2026-12-30T00:00:01Z to 2027-01-01T00:00:00Z. Is that the document you would pick?
7. **The knobs also work on `construct`.** That path is the fixture's for stores X4B's producer cannot reach. Its F and L were a fixed 2026-10-02; with a later manifest they become max(2026-10-02, the manifest's time), which is what the acceptance's own rule would record. The r12 tests run only on produced stores; this keeps the fixture coherent if a later unit combines a knob with an unlawful spec.
8. **The sticky control's sample (NB-01).** It is a same-boot sample about two days behind the anchor's continuity, not merely a lower wall. A set-back within 24 h would rewrite the anchor and publish, correctly, so it could not assert "writes nothing" (Codex's observation). `needs_write` and item 7 are unchanged.
9. **The mapping test is table-driven against X4-F1's functions** rather than restating the mapping. The clocked role states are only observable on an admitted view, so refused rows are compared by row; X4-F1's `a_rereads_clock_follows_x4b_item_4_and_the_role_machine` already pins `clock_roles` itself, including the states `EV-CLOCK` never moves.
10. **The fixture file is touched; the X9 harness is not.** `accepted_store_fixture.rs` builds the matrix's stores (`accepted_store_files`) but is not on item 13's harness pin list. With every knob `None` its output is byte-identical by construction, and the X9 comparison (equal post-state hashes and child traces in every selected row, equal censuses) confirms it.
11. **Boxing.** `Admission`'s variants differ by 432 bytes (measured with `size_of` in phase 1: 3456 against 3024), and clippy's `large_enum_variant` fails `-D warnings` at 200. Both are boxed; one allocation per fenced read.
12. **Phase note.** The phase 1 diff (`cc663a8e…`) put the two test re-exports in one braced `use`, which rustfmt orders differently; the final diff gives `write_accepted_trust_issued` its own `use` line. No other byte changed, and every lane below ran on the final diff.

## Not claimed

- Expiry detected between reads, native scheduling of the 5 s and 10 s bounds, recorded `EV-CLOCK` transitions, and F9's fixture date refresh (law r12, "Not claimed"). For X4T-0's self-constructed stores (L 2026-10-02), a fenced read on the native clock now refuses `core:stale-revocation` from 2026-12-30T00:00:01Z (the second X4-F1 already moved rereads to); default produced stores refuse `beyond-horizon` from that second anyway. F9's 2026-12-01 deadline covers both.
- Linux.

## No inventory

The diff adds, removes and renames no file, so the selected inventory (v135 at `3f6f9a5`) stands. Inventory rows carry no bytes, and the touched files' descriptions remain true. As with X4-F1, there is no inventory successor and no `inventoryCandidateAssessment`. (X3a-2's candidate v136 is independent of this unit.)

## Lead results

**How they ran:** every lane ran on `3f6f9a5` plus the final diff (`evidence/lanes.sh`), serially, at `nice -n 19`, with a private 0700 TMPDIR and `--locked --offline`. The summary is `evidence/lanes-summary.txt`, and the counts are in `evidence/results.json`. The real home was absent before and after. The lanes ran from 08:45 to 09:13 PDT. Grok's X3a-2 review lanes, in their own worktree and target directory, started at 08:59 and overlapped the second workspace run, the doctests and the crash-matrix feature lane, which all passed. The X9 run sets below waited for a quiet machine.

| Lane | Result |
|---|---|
| `cargo fmt --all --check` | clean |
| `cargo build --workspace --all-targets` | pass |
| `cargo build` of platform, security, storage and host, `--features crash-matrix --all-targets` | pass |
| `cargo build` of security, storage and host, `--features scenario-fixtures --all-targets` | pass |
| `cargo build -p opensip-security --features opensip-platform/crash-matrix` | pass |
| `cargo clippy --workspace --all-targets -- -D warnings` | clean |
| `cargo clippy`, the crash-matrix lane (four packages, `--all-targets`, `-D warnings`) | clean |
| `cargo clippy`, the scenario-fixtures lane (three packages, `--all-targets`, `-D warnings`) | clean |
| The 8 new tests and 6 neighbouring X4-F1 and X4a tests (security lib, `--test-threads=1`) | 14 passed, 0 failed |
| `cargo test --workspace --all-targets --no-fail-fast`, run 1 | 1739 passed, 0 failed, 3 ignored (20 binaries, 549 s) |
| The same, run 2 | 1739 passed, 0 failed, 3 ignored (549 s) |
| `cargo test --workspace --doc` | 18 passed |
| `cargo test`, platform, security, storage and host, `--features crash-matrix --all-targets --no-fail-fast` | 1637 passed, 0 failed, 3 ignored (567 s) |
| `verify_design.py --architecture ../opensip_arch --implementation .` | pass: v135 selected, 95 inventory and 93 contract successors, 100 inheritance rows, 21 supersessions, 40 generation and 48 admission sources |
| `check_package_edges.py --lane host` against v135 | pass: 12 workspace packages, 22 declared and 20 resolved internal edges |
| `check_package_edges.py --lane rust-provider` against v135 | pass |
| `tools/tests/test_package_edges.py` | 14 run, OK |
| `check_dependencies.py --feature-profile security-crypto-workspace` | pass: 11 dependencies, 8 local sources |
| `check_identity_dependencies.py` | pass: 8 dependencies, 305 sources |
| `tools/tests/test_dependency_policy.py` | 9 run, OK |
| `tools/tests/test_identity_dependencies.py` | 5 run, OK |
| `python3.14 -m unittest tools/tests/test_check_crash_matrix.py` | 26 tests OK |
| X9 regression (below): two sets, 54 storage rows and both censuses | identical to the X9-6 evidence, 0 differences |

**Notes on the results:**
- **Counts.** At `3f6f9a5` the workspace has 1731 all-target tests and 18 doctests (P0's figures; no commit since adds or removes a Rust test), and the crash-matrix lane 1629. The 8 new tests make 1739 and 1637. `no_manifest_enables_the_crash_matrix_feature` and `every_test_feature_site_is_on_the_pinned_list` pass in both workspace runs.
- **An aborted first run.** The first lane run stopped at fmt (the phase 1 diff's braced `use`, judgment call 12). It was killed during its first workspace test run, the line was fixed, and every lane above was run again from the start on the final diff. Its logs are not evidence.
- **Phase 1** (security crate only, on the phase 1 diff): `cargo check` clean in all three feature configurations, and `cargo test -p opensip-security` 990 passed, 0 failed, 2 ignored, plus the mutation checks above.

## Crash barriers, traces and the X9 rows

**No crash point, scope, read, write or clock sample is added, removed or moved.** `git diff 3f6f9a5` touches no `crash_barrier!`, `crash_scope!`, `observe_clock` or `native_clock` line, and every `cfg` and file I/O line it adds is in a test or a `cfg(test)` helper. A store that r11 admitted with an expiry already reached at tEval performed the same write-ahead under r11; r12 only replaces the returned view with the refusal after it. No required run's store reaches a clocked state: X9 r16 item 3's scripted wall is 2026-10-04T00:00:00Z plus 3600 s per child ordinal, and the nearest boundary in the matrix's stores is the list's staleness, 2026-12-30T00:00:00Z.

### The regression (law item 13), run 2026-10-04 on `3f6f9a5` plus the final diff

**Source pins first** (`evidence/x9/source-pins-first.txt`, taken before the lanes; `source-pins.txt`, the same check rerun on the final diff after the runs, with the same result):
- Item 13's harness sources are byte-identical at `3f6f9a5` and at X9-6's C, `3d2d5b5`, and the diff touches none of them: `tools/check_crash_matrix.py` and its test, `crates/platform/src/crash_barrier.rs`, storage's `commit_tests.rs` and host's `commit_matrix_tests.rs`, both `required-runs.v1.json` files, and security's `crash_matrix_sites.rs`. So are `crates/platform`, security's `crash_matrix_census.rs` and `crash_matrix_support`, and storage's and host's `tests` trees.
- `crates/security`, `storage`, `host` and `platform` are unchanged from `15c0779` to `3f6f9a5`. (Item 13 stated this at `218465f`; `3f6f9a5` is main two commits later, and neither commit touches `crates/`.)
- The checker's suite passes (26 tests, OK), and X9-0's `no_manifest_enables_the_crash_matrix_feature` and X9-1's `every_test_feature_site_is_on_the_pinned_list` pass in both workspace runs.
- The diff does touch `accepted_store_fixture.rs`, which builds the matrix's stores (judgment call 10).

**The selection.** The law's selector, `reviews/grok2-x4t-f2-r1/evidence/x9-rows.py`, run on current main's checkout gives output byte-identical to the pinned `x9-rows.json`, and run on the worktree it gives the same selection (`evidence/x9/x9-rows-main.json`). Storage: 54 rows, all F00: 34 `x4t.floor-publication` kills and 20 `x3b.floor` kills. Host: no row; its `OPENSIP_X9_ROWS` is `X4F2-NO-ROW`, which matches no row, so the host run set is its census alone. The selector asserts that the harness's prefix rule selects exactly these rows.

**The runs.** `evidence/set.sh` ran X9-6's run-set entry, `x9_6_matrix` (census, then the selected rows), storage then host, as two sets, `x4f2-1` and `x4f2-2`, one after the other, with a private 0700 TMPDIR, after release absence.
- **Load.** Before release absence and before each target's run, the script required that no `cargo`, `rustc` or test binary be running, polling every 60 s (`evidence/x9/waits.txt`):
  - release absence waited 300 s for Grok's X3a-2 crash-matrix lane;
  - `x4f2-1-storage` started at once;
  - `x4f2-1-host` waited 600 s: another agent's `cargo test -p opensip-host --lib schema_sources` was first seen compiling at the moment `x4f2-1-storage` ended (16:23:21Z), then the lead's own confirmation `cargo test --workspace` ran;
  - `x4f2-2-storage` and `x4f2-2-host` started at once.

  From just after `x4f2-1-host` started until the comparison ended, a 10 s sampler (`overlap.txt`) saw no foreign process. None of the 54 selected rows carries a `timingGuard` (checked in every run record of both sets), so the late foreign build at `x4f2-1-storage`'s end could not touch a guard.
- **Times:** storage 221 s and 216 s; host 35 s and 35 s. Every run PASS (54 of 54 in each set). The real home stayed absent.

**The comparison** (`evidence/compare.py`, X4-F1's method; output `evidence/x9/compare.json`) is against the accepted X9-6 evidence, arch `crash-matrix-x9/evidence/3d2d5b5…/` (its run files and both targets' `matrix.json`).
- **What it compares**, for every run in both sets: verdict, `postState.normalizedSha256`, the ladder, `notApplicable`, every child's role, ordinal, exit, `lastHeld`, outcome and trace `{records, sha256}`, and whether `timingGuard` is present. Per target and set: the run list against the selection, the census, and the kill set.
- **The result: identical, with 0 differences.**
  - Storage: 54/54 runs equal in both sets. Census: 259 points, trace 1379 records, `e9add21e…`. Kill set: 321 points.
  - Host: no run, as selected, in both sets. Census: 218 points, trace 1195 records, `93d0922a…`. Kill set: 271 points.
- **Expected differences, not compared:** each `matrix.json`'s `product` is `{commit: 3f6f9a5, worktreeClean: false}`, because the subject is uncommitted, and `releaseAbsence` carries the new binary below.

The equal post-state hashes and child traces in the 34 publication-kill rows, whose children run the fenced read over the matrix's generated stores, also confirm judgment call 10: the fixture's default stores are byte-identical.

A full two-target `check` with `matrixPass` needs a clean commit, so it can only run at integration; the lead decides whether to run it then.

## Release absence

`evidence/release.sh`, record `evidence/release-absence.json`:
- `cargo build --release -p opensip-cli` (no features) gives `target/release/opensip`, 6314160 bytes, sha256 `9dd734457effe53f049cd4aad007c23262577292e71a05b629a6fcab13ea458d`.
- Neither `OPENSIP_X9_` nor any of the 25 registered scope names appears in it (`found: []`, `passed: true`).
- The release builds of storage and of host with `--features crash-matrix` are each refused at the compile guard (exit 101).
- X4-F1 recorded 6314800 bytes, `4055dd66…`, on `e093e90`. The binary differs because main has moved since and the security code it links changed.

## Decide

- **Law:** does the change implement X4T r12 items 1, 6, 7, 9 and 10 exactly: the instant (tEval only), the three states, X4B r5 item 4's mapping through `role_machine::clock`, the second join, the write-ahead before a clocked refusal and its place after check 3, report-only, and the row and subjects? Does it change nothing else (`live_observation`, the reread, every row and code)?
- **Composition:** is it right that each read clocks its own capsule's stored states once, and that nothing reads the start view's clocked states?
- **Never a view:** can a clocked refusal escape as an `AdmittedCurrentTrust` on any path, including `admit_native` and `bootstrapping_first_read`?
- **The hold:** is the hold after a published clocked refusal the one item 7 r12 describes, with no `required-files-changed` relabelling?
- **Fixture:** are the three knobs lawful (signed into their documents, `cfg(test)` or feature-gated with the generator, default stores unchanged), and is the manifest the right document for the first (call 6)?
- **Tests:** do they pin each boundary (strict `>` for staleness, `>=` for expiry), expiry winning, catalog-only `ExistingOnly`, report-only equivalence, write-then-refuse on native files through both entry points, NB-01's anchor-preserving stickiness, S4's precedence, the real lease-free termination, and the composition with rereads?
- **X9:** is the regression complete for item 13's subset, and are the waits and the late foreign build at `x4f2-1-storage`'s end handled acceptably?
- **Judgment calls:** are calls 1 to 12 acceptable? Call 6 asks you a direct question.

Write REVIEW.md and review.json under the output directory. review.json needs:
- `"verdict"`: `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`;
- `"subjectSha256"`: `ffc4ef1e038199c13b2c1fa0139405239f57f362ee274f46bb26835a3f6835be`, the diff's sha256, as a single string.

No `subjectManifestSha256` or `inventoryCandidateAssessment` is needed: the unit has no inventory or design selection. Do not commit.
