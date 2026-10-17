# CI-A3-r3 review

**REQUIRED-FINDINGS.** Two required findings; no non-blocking observations. This is an amendment review, not acceptance of CI-3L implementation or launch qualification.

## Subject and boundaries

The 1,693-byte subject manifest hashes to `22726fc07d84f0ac237f59512aec2a0722b0dcec98062b32a68640b1e1debda8`. All six members match their lengths and hashes. The 37,281-byte archived CI-A2 scope hashes to `d79e838a4c63383a22e3090290d6feb309b776187afd3ab0f3fa0e49f7e2c4b8` and exactly matches the SCOPE.md entry inside the pinned CI-2-r2 subject manifest and that package's scope bytes. The obsolete r2 live-file pin remains history. CIA3-R2-RF-1 is resolved.

Only read-only reading, hashing, JSON parsing and Git queries were performed, including permitted reads of opensip-ci2. No project checker, Cargo, rustc, build, test, lane, network, other pane, delegation or prohibited private/store material was used. Only this directory's REVIEW.md and review.json were written; neither repository, worktree nor control file was edited.

## Required findings

### CIA3-R3-RF-1 (P2): Define the early refusal needed for the no-matching-kind pre-bound

Location: `docs/implementation/m3/component-install/CI-A3-r3.md:49-50, 118-125, 168`.

The general resolution procedure follows symlink rows before checking the final requested kind, but the no-rows special case asserts that only one lookup can occur and budgets only that lookup. A valid flat tree can contain file f and symlink l targeting f, with no dir rows. Directory("l") follows l, allocates the one-byte joined path f, looks up f, and then refuses Association for its type. For the retained order [f,l], the existing binary search makes one comparison for l and two for f. That failure prefix costs three edges plus one object/one byte, while the stated no-dir-row pre-bound has at most two edges and zero objects/bytes. No explicit early kind-absence rule currently prevents that execution. CI-T28 specifically requires the bound relation for this case.

Required: Normatively require refusal before following a symlink or allocating its joined path when the requested kind has no rows (with at most the priced initial lookup), or fund the complete possible failed-resolution prefix. Make the refusal-prefix accounting explicit where there is no resolved member m. Add the file-plus-link/no-dir Directory("l") case to CI-T28 and verify actual charges against the pre-bound.

### CIA3-R3-RF-2 (P2): Preserve the capability latch for Budget failures too

Location: `docs/implementation/m3/component-install/CI-A3-r3.md:163, 181; opensip-ci2/crates/lifecycle/src/retained_tree.rs:151, 167, 426-429`.

The interaction text excludes Budget from launch_member's capability latch because the ledger latches itself, then concludes that no later launch or transfer of the capability proceeds. These are different lifetimes. The accepted CI-2-r2 transfer explicitly stores Latched::Budget in the capability; later calls return Budget(Closed) before charging even if passed another scope. The proposed launch API also accepts a caller-supplied WorkScope on every call and does not bind the capability to one ledger. A launch exhausted on ledger A therefore need not stop a later transfer/launch on fresh ledger B under the proposed exception. This contradicts both the claimed extension of the existing latch and CI-T27's unconditional cross-operation latching rule.

Required: Latch Budget on the capability as transfer already does, and specify the later Budget(Closed) result consistently, rather than relying only on the exhausted ledger. Add a failed-launch Budget control followed by launch and transfer using a fresh funded scope, requiring no additional charge or observation. If a different lifetime policy is intended, explicitly amend the invariant and enforce a capability-to-ledger association; do not assert it follows from a ledger latch alone.

## Rulings

**Q1.** The new separation of exact executed comparisons/read attempts from their envelopes is accepted in principle and resolves CIA3-R2-RF-2's equality problem: E uses s_j and a, B uses their bounds, and neither unused comparisons nor extra reads are executed. Empty files have one EOF attempt. The maxima, checked arithmetic and Directory("") special case are defined. Full E≤B≤Bhat acceptance is withheld pending CIA3-R3-RF-1: a no-matching-kind failure can follow a symlink and exceed its single-lookup pre-bound unless the early refusal is made an explicit operation rule. Refusal prefixes also need an explicit interpretation when no member m resolves.

**Q2.** Accepted. All six members rehash exactly. The CI-A2 context copy is byte-equal to the SCOPE.md pin inside the exact CI-2-r2 subject manifest and to the corresponding packaged scope. The amendment adopts that revised context rather than reconstructing the obsolete live-file pin. CI-A2-b supplies the retained component index and CI-A2-c the at-most ceil(log2 n)+1 search comparisons charged individually, matching CI-A3. The archived copy removes dependence on future edits to the CI fork's working scope; the old r2 manifest need not be repaired as history.

**Q3.** Accepted for the spelling and reservation terms: the native basename uses CI-A2-h's fixed stack buffer without an owned-record charge; the single heap launch-path buffer remains P+1 and is borrowed as CStr for lstat and reused in the result; the store path remains a separate one-time L-byte opening charge. CI-A2-e's full installer reservation does not change per-operation launch charging. The latch extension is not accepted as written because of CIA3-R3-RF-2: excluding Budget loses the accepted capability-level poison when a later call supplies another ledger.

## Remaining assessment

The prior exact-accounting defect is corrected: E_launch uses observed search counts and read attempts, including one EOF attempt for an empty file; B_launch replaces those counts with the lookup/read envelopes. CI-T28 now independently enumerates representations and operations, requires exact E equality, tests lookups at different depths and checks inequalities separately. The pre-bound's successful-member maxima dominate componentwise with empty maxima zero, bounded segment lengths and checked arithmetic. RF-1 concerns the additional failed-resolution case, not a request to precharge unused work or read to an envelope.

The other previously accepted design remains intact: entrypoint comes from the authenticated selected-platform association; lexical links resolve against the retained index rather than the filesystem; parent descent is componentwise and no-follow; file bytes are rehashed through the retained buffer; directory identity/mode is checked without claiming descendant-content attestation. Directory("") uses the retained tree root with no index lookup or descent. The one composed NUL-terminated path is observed by lstat and reused without another owned spelling. ENOENT/ENOTDIR, wrong kind or mismatched identity become Binding; other observation errors remain Io; refused work remains Budget.

The operation's ownership of the capability through child settlement is explicit, with the borrow serving as a guard and the sole factory path/lifetime controls supplying the operative discipline. The same-principal path substitution window remains disclosed, with no D1a change or claim that the pin closes it. The new platform-owned lstat/directory-fstat mechanisms retain P-7's published status price and unsupported-target refusal. The store's one-time owned path belongs on the opening owner's existing ledger, preserving typed Budget failure and avoiding unpriced intermediate joins, as the prior ruling requires.

CI-3L remains a separate unit after CI-2/CI-3 integration, covering the new operation, Binding, constructor/path changes, platform primitives and controls. D4-4 depends on that implementation as well as amendment acceptance. No code, production caller, public termination code or qualification is accepted here.
