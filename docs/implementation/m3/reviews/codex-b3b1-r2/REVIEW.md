# B3-B1 r2 review

Verdict: **REQUIRED-FINDINGS**.

Subject manifest: 7,043 bytes, SHA-256 `d01790f7445e590e300812ad19beba41b8f11752356e3f8a90032cb9c804cba9`. All 30 members match their byte counts and hashes. Product-map parent, candidate and archived bytes match; the candidate reference file is 55,266 bytes, SHA-256 `1d5c0fff3c3dad13d4ad223404d5dc7c6dc9bfede229313992150f0005b88194`. Source authority and product-lock pins also match.

Product main is clean at `25972e19f311fad556ee5b89cda154e950357167`; the detached candidate is at that base with the two advertised source changes. The product base differs from r1 only in design-lock.json. Architecture HEAD is actually `9e90c68c4e86999758c39511983da3042da16697`, as source.json records, rather than REQUEST.md's `67b8f8b...`. The intervening commit publishes B3-b0 and its review records; the pinned B3-b1 authorities remain unchanged. This metadata discrepancy does not account for the semantic finding below.

## Required finding

**B3B1-R2-RF-1 (P1): NoRepository::covers binds pathname labels, not the retained root.**

Location: `crates/security/src/custody/git_tracking.rs:1075-1088`; use in `observe_members` before its independently supplied chain selects W.

The original cross-spelling substitution is now rejected. However, `covers` examines only the supplied chain's spelling, component count and whether the observation contains matching `Sample::Absent` labels. Neither the observation nor the proof records the retained chain/root identity used by 6a. A chain for a different directory object with the same spelling passes exactly the same checks.

A concrete source-derived counterexample for the lead's scratch controls:

1. Retain chain A for a non-repository root at H/code/w and obtain its NoRepository observation/token.
2. Keep A and the observation alive, move that directory aside, and place a different conventional repository at H/code/w, with a conventional nested repository m.
3. Retain chain B for the replacement root, using the same H and spelling, and pass B with A's token to observe_members.
4. Every absence label required by covers is still present in A's observation, so the check returns true. The pass then derives W from B and checks only the descendants on the path to m; it does not observe the replacement W's own VCS marker. With otherwise valid evidence it can admit m under a W that fails W2.

This is a retained-object substitution, not a demand to recheck whether the original root's filesystem state has changed. The typed observation must authorize the retained root whose member descriptors are used. Comparing historical pathname labels does not establish that relation. The check also accepts a shorter ancestor chain when its labels are a subset of the observation, despite the documented exact-chain claim.

Required: preserve a binding to the retained chain/root actually used by 6a, and derive W from it or validate that binding before any member work. Keep 6a's operational behavior unchanged and add a same-spelling/different-retained-root control alongside the current different-spelling control. No new Git evidence read or fenced member recheck is required merely to bind the token to its subject.

The counterexample was established by source tracing; I did not create scratch repositories or execute tests, consistent with this request's boundaries. **B3B1-R1-RF-2 remains partially unresolved.**

## Round-1 resolutions and ledger audit

**B3B1-R1-RF-1 is resolved in the revised source.** Pass::Members routes every shared Git/global custody judgment through judge_decided. It uses capture_descriptor_acl_observed, so Changed, Malformed and Unsupported are returned as values after the same capture charge and translated to the object's existing custody subject outside a latching scope. The shared-order pure check, explicit trusted groups, omission premise and absence of an owner waiver preserve the intended judgment. MemberInputs builds the policy from the same custody facts. Capture I/O and premise filesystem-sampling failures remain pass failures, while budget failures remain immediate failures.

The new controls cover a Changed capture on the first member followed by an admitted member, a lone Malformed configuration capture, and an Unsupported pass-level global capture returning refusal vectors through the enclosing ledger scope. These are appropriate outcomes. Reads use the observed read helper; placement directory-open errors are values until after work.run; configuration, environment and index decoding similarly decide ordinary refusals outside charged scopes. Positive-marker lookup and descriptor/filesystem sampling errors are host I/O, which intentionally fail the pass. I found no additional path translating an already latched ordinary native failure into a recoverable member refusal.

**B3B1-R1-NBO-1 is resolved.** All eleven mutation logs, including linked-worktree-dropped, are present and pinned. The package builder's work-directory filter no longer drops that filename.

## 6a fidelity and scope

Inspection against the product base shows the extracted layout preserves 6a's native operations, charges, sample order, configuration parsing, index-byte reading and refusal order. Pass::Tracking still calls the original config and judge_project_object. repository performs the same subsequent marker-path derivation and charged index decode/match, including the equivalent absent-index return. The new decided judge is used only by members; project_chain.rs is unchanged.

The member walk retains no-follow opens, device checks and positive VCS-marker observations between W and M and at M. The closed layout reads no HEAD, refs, packed-refs or shared-index bytes. The commondir/config.worktree absence probes are the required layout observations. Gitlinks are returned from the unchanged decoder; no member write or fenced recheck evidence is added.

LD-1's all-members refusal for unsupported pass-level effective configuration remains appropriate; actual host I/O and budget exhaustion retain LD-2's pass-failure behavior. LD-3's evidence-changed for invalidated placement, LD-4's expressly synthetic device control, and LD-5's preservation of the real split-index index-malformed verdict remain acceptable. Git evidence receives no owner waiver. Ordering, caller placement/disjointness, 65-member pre-observation cap and integration with readers remain B3-b2 obligations; the member producer has no caller or ledger bound in this unit.

## Checks and observations

The archived logs substantiate 1,128 base passes and 1,138 candidate passes across two suites, with the same 14 failing test names on both. These are equal existing failures, not a completely passing security suite. The focused log reports 33 passing git_tracking tests. Archived all-target warning-denied Clippy, environment exceptions, census check and design verification report success. The 6b producer remains outside the census closure; that check is not a bound on member costs. I inspected this evidence without rerunning it.

All eleven archived mutations compile and fail behavioral tests at relevant assertions. The ten added tests cover the prior seven controls plus capture continuation, pass-level capture refusal and different-spelling root substitution. The new same-spelling substitution above remains uncovered.

**B3B1-R2-NBO-1:** the member-custody-latches mutation bypasses judge_decided and therefore bypasses its test-only injected_capture queue. Its failures are admitted/admitted versus refusal vectors, rather than Budget(Closed). It is a meaningful guard against replacing the member judge, but is not a direct demonstration of native capture failure crossing a latching scope. A fault seam at the native capture boundary would let an observed-to-accounted mutation exercise the same injected error and establish that distinction. This does not negate the source-level RF-1 fix.

The only executable check run by this reviewer was the expressly permitted operability source check in the candidate worktree: passed, 114 rows, no findings. No Cargo, rustc, tests, builds, lane, census or network command was run. No private fixture, installation directory, signing key, held tree or T2 held-out entry was read. No panes or delegation were used. Neither repository, worktree nor control files were edited. Only REVIEW.md and review.json were written in the requested directory.
