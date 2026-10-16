# B3-B1 r3 review

Verdict: **ACCEPT-UNIT**.

Subject manifest: 7,046 bytes, SHA-256 `d05f8074d7b909d5f3f1069104e7aca1e912cbcd99a3818157b09043b964f4dd`. All 30 members were rehashed and match. Both product-map candidate files match the worktree and archived bytes; the existing source file's parent matches the product base. Source authority and design-lock pins also match.

Product main is clean at `25972e19f311fad556ee5b89cda154e950357167`; the detached candidate is at that base with exactly the two advertised source changes. Architecture HEAD is `9e90c68c4e86999758c39511983da3042da16697`, matching the corrected request. The candidate git_tracking.rs is 55,415 bytes, SHA-256 `64339eb8203475cd4fd55c7dff2eb45b755512d76213f16117581b7ae665c907`; the new tests are 22,292 bytes, SHA-256 `d12929eb2a898bf8ddcbb8c174402ec0a59c2e49dbc0e2df6e8220a5b65ce90b`.

No required findings or non-blocking observations.

## Root binding

**B3B1-R2-RF-1 is resolved.** RootObservation privately holds the observation and the borrowed ProjectChain actually supplied to observe_tracking. observe_root constructs that pair only after the existing observation succeeds. Its no_repository method returns a token containing that same chain only for Tracking::NoRepository. MemberInputs no longer supplies an independent chain. observe_members destructures the token and uses its chain for W, H's retained handle, W's descriptor and device, and the descendant opens.

A caller outside this implementation cannot construct or mutate the private pair, replace its chain or supply another root to the member API. The proof's lifetime keeps the borrowed chain alive. Dropping or consuming the wrapper does not change which chain a previously returned token borrows. Neither pathname labels nor an ancestor-subset comparison participate in the binding.

Both substitution controls exercise the intended distinction. For different spellings, W_A's proof admits its own a and returns evidence-changed for m that exists only under W_B; W_B's observation produces no proof. The same-spelling control retains and observes W_A, renames it aside, installs a repository at the old spelling, and retains W_B. The pass still reaches a through W_A's original retained descriptor, cannot reach W_B/m, and W_B produces no proof. This directly covers the counterexample in round 2. I inspected the controls and archived outcomes; I did not execute them under this request's no-test boundary.

**Retiring root-binding-skipped is correct.** The covers function, alternate chain input and mismatch refusal no longer exist. There is no corresponding runtime binding check to skip. The retained-chain API and substitution controls replace that mechanism; precondition-always now targets RootObservation::no_repository and is caught by both substitution controls and the repository-root precondition control.

## 6a and the earlier fixes

TrackingObservation and its existing accessors, and recheck_tracking, are byte-identical to the product base. observe_tracking is unchanged from r2; its shared-source calls retain the reviewed Pass::Tracking parameterization. Existing production callers remain unchanged. observe_root is additive and invokes observe_tracking once over the same inputs, without adding native observations or ledger charges.

The extracted layout still preserves 6a's steps, charge amounts, evidence order and refusal priority: the original custody and config functions remain behind Pass::Tracking, and repository performs the same subsequent index decode and marker match. The absent-index return remains equivalent. No decoder or configuration policy changes were introduced in r3.

**B3B1-R1-RF-1 remains resolved.** The r2-to-r3 source comparison leaves judge_decided and the decided config/environment/index paths intact. Ordinary capture outcomes are values outside charged scopes, retaining the same capture charge, shared-order custody check, trusted groups, omission premise and object-specific refusal subjects. Host I/O and budget failures still fail the pass. Reads and placement opens likewise preserve handled ordinary outcomes without reopening or replacing the ledger. I found no additional per-member refusal path that catches an already latched ordinary failure as a recoverable verdict.

**B3B1-R2-NBO-1 is resolved.** capture-refusal-latches preserves the member judge and fault queue, then moves the injected native outcome into a charged scope. Its archived failures explicitly report Budget(Closed) at the first-member continuation and pass-level refusal controls. This supplies the distinction missing from the earlier mutation, which bypassed the injector. The mutation's zero-cost charged scope is sufficient to test the ledger's error latch; it does not purport to measure capture cost or replace the platform capture implementation.

**B3B1-R1-NBO-1 remains resolved.** All eleven current mutation logs, including linked-worktree-dropped, are present and pinned. The evidence-path erratum correctly identifies the archived b3b1-checks-rN directories.

## Fidelity, controls and evidence

The reviewed member path retains the no-follow descriptor walk, device comparisons, intermediate/member VCS-marker probes, unchanged closed Git layout and exact index decoder. No HEAD, refs, packed-refs or shared-index bytes are read. commondir/config.worktree are positively probed for absence as the law requires. Gitlinks are returned for nested-boundary handling by the caller. No member write or fenced recheck evidence is added. The no-owner-waiver rule for Git evidence remains intact.

The lead decisions remain acceptable: unsupported pass-level configuration refuses every affected member; genuine host I/O and exhausted budgets fail the pass; invalidated placement uses evidence-changed; the device fixture is explicitly synthetic; and a real split index keeps the unchanged decoder's index-malformed verdict. Caller placement/disjointness and ascending order, the 64/65 cap before observation, reader integration and the member cost bound remain the declared later-unit obligations.

The archived security logs have the same 14 failing test names on base and candidate, with aggregate passes increasing from 1,128 to 1,139 across two suites. This substantiates eleven new passing tests and equal pre-existing failures, not an entirely passing security suite. The focused log reports 34 passing git_tracking tests. Archived warning-denied all-target Clippy, environment exceptions, census check and verify_design report success. The census check does not establish the future member-observation cost bound.

All eleven mutation logs show successful compilation followed by behavioral test failures at relevant controls. The new capture-latch and retargeted precondition mutations address the prior review gaps. These logs and the eleven added tests support the unit's stated scope; they do not establish product qualification or integration with a production caller.

The only executable check run by this reviewer was the expressly permitted operability source check in the candidate worktree: passed, 114 rows, no findings. No Cargo, rustc, tests, builds, lane, census or network command was run. No private fixture, installation directory, signing key, held tree or T2 held-out entry was read. No panes or delegation were used. Neither repository, the worktree nor control files were edited. Only REVIEW.md and review.json were written in the requested directory.
