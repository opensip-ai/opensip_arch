# Review: stale descriptions 461b r1

Verdict: ACCEPT-DESIGN-UNIT.

Subject manifest `docs/implementation/m2/stale-descriptions-461b-subject.json` is 638 bytes, sha256 `56aea17905d007538e4c13532bf81a95bb4b60ef8396b869074d25457898d5e5`. The successor record is 11909 bytes, sha256 `2c8a4de79e156b0f0c47e579c2121adae07f804a505e3d19d3bb2b787596fad6`. README and `evidence/verify_scratch.py` match the manifest. Parent inventory v80 is 313526 bytes, sha256 `838a7f4072b408e8c4011249c89e0974d38616031cda110267c92ab762d0d1e7`, 749 files. Each of the eight passage overrides repeats that parent pin, and each `before` string is the live description at its pointer.

The unit was written against product `d4239a5`. Live HEAD is `d1b5edad4fc552122ca9ef7161d2a69cc30b0852` (461a). On these eight files that commit only moves three test scratch directories onto `acl_scratch`, compares `acl` in record capture, and gives the empty-bucket test the zero-rights owner allow. Those descriptions do not mention writer lists or the scratch directory, and they stay true at HEAD.

## The eight sentences

`installation_fence.rs` (236). `HeldFence` exposes the held directory, the actor, a recheck, and a filesystem sample. The carrier name is `lifecycle.fence`. `ReadSession` implements the trait for production readers: its `recheck` is the charged held-fence check. `SuppliedInstallationFence::try_acquire` is one nonblocking exclusive attempt, with custody checks before and after the lock, and `None` for busy. `NativeInstallationFence` adds native root provenance and maps a missing root to `RootAbsent`. Production census, current, platform, profile-census, and record capture take `&dyn HeldFence`. The trust read session passes `InstallationReadFence::held()`. The supplied and native factories are reached from the fence tests and from the native factory itself.

`installation_publication_tests.rs` (240). The readers test builds the fence with `installation_read_fixture::fence_at`, which returns `InstallationReadFence`, reads the pair, marker, and node through `capture_leaf` and `capture_descendant`, then reads the capsule through `NativeTrustReadSession::capture`. The rest of the v80 sentence is unchanged, and this file is unchanged since `d4239a5`.

`installation_session.rs` (247). `ObservationSession::begin` is called from `InstallationReadFence::acquire` and from `observe_installation_for_doctor`. No host or app command calls either. The carried session behavior (one session, one ledger, shared gate steps, `lifecycle.fence`, 25 ms / 5 s / 201 attempts, structural findings) is the existing module contract; this unit only replaces the consumer sentence.

`read_premise.rs` (250). `produce_read_platform` is what `acquire` and doctor's check use. `acquire` passes the receipt to `observation.retain`. Doctor passes it to `session.observe_with`. A development build ends at `CORE.NO_EMBEDDED_RELEASE` inside that producer, before any path is opened. No CLI command calls it.

`installation_observation.rs` (259). `acquire` produces the receipt, begins the session, and retains a complete I. Refusals from that path are `InstallationTermination` through `session_refusal`. `capture_descendant` rejects an invalid leaf, a depth above 256, or a bound outside 1..=4MiB before `session.capture`. `Error::termination` is `None` for those three reasons, so they have no 468 row. `ProvisionalHeldFile::bytes` calls `recheck_capture` first: the held fence, every retained edge, then the file. The session ledger is the one ledger those captures charge.

`native_census.rs` (316) and `native_record_capture.rs` (321). Both `capture` functions take `&dyn HeldFence` and the shared budget.

`native_read_session.rs` (320). `NativeTrustReadSession::capture` borrows one `InstallationReadFence` and charges `Budget::charged(fence.session())`. `append_with` and `observe_successors` lend `fence.held()` to the trust captures and call `fence.recheck()` once after that operation's reads. That method is the read session's full recheck. `check_all`, used between those full rechecks, calls `recheck_held`. The session exposes no reset and no raw file handle.

## Other rows changed since inventory v74

The stale phrases ("no consumer uses it yet", "no read path uses it yet", "native installation fence", "retained native fence", "borrowed native fence", "existing installation fence") occur on these eight v80 rows only. Fifty-seven product paths differ from `26d3d92` to `d4239a5`. Three siblings changed from `SuppliedInstallationFence` to `&dyn HeldFence` and are already described without the old fence name: `native_current.rs` still captures the current capsule and compares its store claim under one budget; `native_platform.rs` still joins process, boot, loader, and filesystem observations to the signed profile; `native_profile_census.rs` still combines that evidence under the same fence and budget. `installation_lineage.rs` is an inherited row. Its only change in that range is the shared `relative_components` spelling, and the projected inheritance text remains the selected meaning. The eight inherited pointers are `/files/7`, `13`, `106`, `161`, `258`, `276`, `546`, and `613`. None is one of these overrides.

## Successor shape

`schemaVersion` is 1 and standing is PROPOSED. There is one parent, the v80 pin. Eight overrides each have exactly `parent`, `selector`, `before`, and `after`, the selector is a JSON pointer to `/files/N/description`, and `before` differs from `after`. Candidates are the README and `verify_scratch.py`, which with the successor record are the subject manifest. I ran `evidence/verify_scratch.py` against the product checkout. It passed, selected inventory v80, reported 70 contract successors, and left `inventoryPassageInheritance` at 8. No product cargo.
