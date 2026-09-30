# Review: read premise 458c-a and inventory v77

Grok is the single reviewer. Claude Opus 5.5 leads. Implementation review of the read-side premise receipt and inventory v77. No repository edits and no product cargo.

Worktree `/Users/sb/code/opensip-ai/opensip-458ca` at `7237f931ae78330243edc4de1e7d64daf1b50fd2`, with the seven uncommitted files pinned in hashes.txt. Every pin matches, including `product.diff` (19391 bytes, sha256 `a48807d3ae9b61d227d531b928388a1c3a2c45d6037d7f61ada3976689bc6b35`). `~/Library/Application Support/OpenSIP` is absent and is not a symlink. Law is 458c r5 items 1 to 4 and the 458c-a bullet of item 10.

## Verdict

**ACCEPT-UNIT.**

The receipt is the creator's four producers and nothing else. The qualification cannot be built or widened by a caller. Inventory v77 adds the two new sources and leaves the inherited rows unchanged.

## Receipt

`produce_read_platform` takes no command, flag, or writer. It calls `InitialInstallationAttempt::begin`, `observe_actor`, `produce_initial_core`, and `produce_initial_platform`, in that order, through `produce_on`. Core runs before platform, so a development build stops at F0 on `NoEmbeddedRelease` before `produce_initial_platform`. There is no `mint_intent`, storage choice, disclosure, preparation, permit, stage, effect, or fence.

`ReadPremiseReceipt` keeps the attempt, actor, core, and platform in private fields. It is not `Clone`. Its `Debug` is `finish_non_exhaustive`. `AclOmissionPremise` is not `Clone`. `qualification()` is the only lending and returns `&impl ReadPremiseQualification`, so the caller does not receive `InitialPlatform`.

`ReadPremiseQualification` is sealed in a private module and implemented only for `InitialPlatform`. It lends `is_home_filesystem` (`qualifies_installation_filesystem`) and `omission_premise` (`acl_omission_premise`). It has no barrier method. `DurableBarrierQualification` stays a separate trait; both delegate to those same `InitialPlatform` methods. `AclOmissionPremise::admits` is unchanged: the premise still admits only through its own `fstatfs`, and this unit does not widen the path scope. The module is `pub(crate)` inside private `custody`, so it is not a crate export. `produce_on` is `pub(super)`, the same seam `route` uses, and production passes the four live producers.

Refusals use 468c's existing maps and add no row. `work` sends a ledger refusal to `BudgetExhausted`. Actor, core, and platform refusals use `actor_refusal`, `core_refusal`, and `platform_refusal`. `AttemptError::AlreadyAllocated` is `Invariant`. A lineage that `require_lineage` rejects latches the attempt and returns `Invariant` before a receipt exists. An admitted platform with no premise is returned, not refused.

`recheck` stays on the receipt. It re-runs the actor, core, and platform rechecks on the attempt the receipt already holds, through those same maps. Each of those rechecks latches on refusal. It does not walk to I, open the fence, or add a row. 458c-b step 2 needs this limb without the attempt becoming visible. Moving it would split the ledger from the receipt that owns it.

The live F0 test is accepted as written. It allocates with `for_tests` on its own flag, then uses the live `observe_actor` and `produce_initial_core`, and the platform closure panics if it runs. `produce_read_platform` is pinned by the signature `fn() -> Result<ReadPremiseReceipt, T>`. Its body is the four live producers passed to the same `produce_on`. A second `begin()` in this test binary would hit the process flag 468c's live test already takes, so it would not show F0.

The seven tests use `test_scratch::temp_dir()` and signed trees. They cover a minted premise and an admitted absence, equality with the gate's filesystem check, an empty scratch home before and after `recheck`, F0, one attempt after drop, `HomeSpelling` to `AccountRefused`, `/dev` to `InstallRootFilesystem`, a budget refusal to `BudgetExhausted`, a foreign platform to `Invariant`, and the sealed non-`Clone` receipt. The lead reported the workspace sum 1106/0 on two runs, with clippy and fmt clean. This review did not replay that suite.

## Inventory v77

`repository-file-inventory.v77.json` is 304222 bytes, sha256 `642dc4bba855112b9fac2d54079d137c6bed9237cf5b574a5aed09bf22f13ff1`. Parent v76 is 302690 bytes, sha256 `61e4ca6864127a0574ef06a9ca3452f58ed5cd72d381c1a33e0ee7d9c931a18a`. `successor.json` is 9500 bytes, sha256 `aa3a8f0e3345263218aaf2a51a91b3857f816d091a224f85acb8eed01c799e77`.

Rows go from 737 to 739. The only additions are `crates/security/src/custody/read_premise.rs` (composition, `opensip-security`) and `read_premise_tests.rs` (test). Paths are sorted and unique. Nothing is removed. Every inherited row is equal by value. Packages, dependencies, and pending decisions are unchanged. Standing names the 458c r5 receipt and keeps the same non-qualification sentence.

The eight description overrides are the v76 set. Selectors before the insertion stay on the same index. `initial_installation.rs`, `private_access.rs`, `package.json`, and `imported-v1.schema.json` move by two. Each parent selector's `before` equals both inventories' row description. The projection helper is the v76 helper, 2917 bytes, sha256 `c890b35f281bef71bc876088caae13886a6057c71717250348ee008e2612dfda`. Re-running it against `design-lock.json` printed 8 rows, PASS, 43 corruptions. `verification.stdout` is that same 124-byte record.

## Required findings

None.
