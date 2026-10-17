# CI-A3 r2 review

**Verdict: REQUIRED-FINDINGS.** Two required findings; no non-blocking observations. The revision addresses r1's missing quantities/native representations and NBO-1's platform-observation gap, but the package has a mismatched context pin and its new exact-charge assertion still equates executed work with envelope counts.

## Subject verification

The 1,075-byte manifest matches SHA-256 `e2a4223229e03bbb553aa3b919f12a98668b744c950a70af7e9a4780788c1997`. Three member pins match:

- CI-A3-r2.md: 24,960 bytes, `fd2b7ef49ff43387f0e4130d5c8d6f7c99a97f80bf7a396abc89faab0b524095`.
- Historical CI-A3-r1.md: 16,045 bytes, `afe383537a88f690cf75f48f5b1b9df2219994ee08a807c82a9f457aa02551d1`.
- PROPOSAL-r5.md: 63,707 bytes, `efdbf7e70ab48522fec855bbb74f144a5c695c27eefc194b2de000e8e3a54333`.

The CI-2 context member does not match; RF-1 gives both exact pins. The historical amendment itself remains unchanged. The architecture base commit exists. Used read-only Git for the specified d704ed4 product interfaces and read the permitted CI-2 candidate helpers as interface context, without treating that in-flight code or changed SCOPE as an accepted replacement authority. Read the prior review/JSON, the full revised amendment and its quoted LAW anchors. All quoted current LAW passages remain present verbatim in the matching PROPOSAL-r5 member.

## Required findings

### CIA3-R2-RF-1 — Restore an exact pinned CI-A2 context before accepting the package (P2)

**Location:** `docs/implementation/m3/component-install/ci-a3-r2-subject.json:27`.

The subject manifest itself matches its requested 1,075-byte pin, and CI-A3-r2.md, CI-A3-r1.md and PROPOSAL-r5.md match their member pins. The fourth member, ci-2-r1/SCOPE.md, does not: the manifest requires 21,806 bytes with SHA-256 29f4590b34c05eef5318e4229e1901fd6923339071bb66d34c23c1d0b4742dc2; the live path contains 24,520 bytes with SHA-256 02be51f77c59abebd14e5c0f401de1c5f639246782de27a77d746a835d71c2b1. Thus the assertion that every context member is unchanged from round 1 cannot be verified, and the submitted manifest does not identify the context bytes presently available at that path.

**Required change:** Supply the originally pinned context at an immutable review path and update the subject to point there, or rebase this amendment against the intended changed CI-A2 context and issue a matching subject manifest. Do not overwrite the in-flight CI-2 subject merely to satisfy this review. Recheck the relevant interface/price dependencies against the resulting exact context.

**Validation:** Independently rehash all four subject entries and require every member length/hash to match. Preserve the old history artifact and state explicitly whether the new round retains the old context or adopts a revised CI-A2 context.

### CIA3-R2-RF-2 — Separate exact executed charges from the remaining per-member upper bounds (P2)

**Location:** `docs/implementation/m3/component-install/CI-A3-r2.md:134`.

CI-T28 requires the run's charges to equal B_launch for actual counts, but the B_launch table still prices each lookup at at most ceil(log2 n)+1 comparisons and file reads at env(c), a read-attempt envelope. These are bounds, not necessarily executed counts. The reused charged_find charges each comparison actually made, and read_verified charges each read attempt until EOF. A zero-byte file needs one EOF read, while env(0)=2; a lookup can likewise match before its comparison bound. The new equality assertion therefore conflicts with the stated reused per-operation charging model even though the content/path quantities and representation charges have been corrected.

**Required change:** Either define a distinct exact accounting expression using independently observed comparison counts and read-attempt counts, with actual charges equal to that expression and bounded by B_launch and Bhat_launch, or redefine B_launch with explicit actual counts and reserve the comparison/read envelopes for its conservative bound. Do not precharge unused comparisons or perform unnecessary reads solely to satisfy the equality. Keep every charge before its actual operation and preserve typed Budget propagation.

**Validation:** Use an empty file, a one-chunk file and lookups that match at different search depths. The independently enumerated executed total must match actual charges even when strictly below the envelope; verify the bound inequalities separately, including one-unit-short failures before actual operations.

## Prior-round disposition and regression check

**CIA3-R1-RF-1:** the core representation corrections are addressed. Content length c now controls the read envelope; final path p and component/basename quantities control path/descent/native spelling sizes. The hop count is distinct from lookup count, hop temporaries have their own lengths, root Directory has an explicit nonnegative special case, and both basename and shared binding/result buffer terminators are priced. The store's owned path has a named charge site. CI-T28 adds the requested shapes and independent enumeration. The remaining exact-count versus envelope issue is RF-2; the revised controls must not require equality to unused worst-case work.

**CIA3-R1-NBO-1:** addressed. CI-3L explicitly owns two new platform mechanisms rather than claiming a published cost alone supplies the observation. The candidate helpers inspected still support the earlier observation: entry_status accepts a slash-free retained-directory-relative component and returns no device/inode; sample_identity takes an already opened file. The proposed absolute-spelling and retained-directory operations fill those distinct gaps.

The earlier Q conditions are applied without architectural regression. Entrypoint comes from the capability's own authenticated selected-platform association. Resolution uses the committed parent-plus-target rule, bounded hops instead of an allocating seen-set, and no filesystem symlink following. The final file/dir observation comes from retained-base component-by-component descent. The binding checks the exact composed absolute spelling, final kind and device/inode; identical contents alone are insufficient. Binding remains promised-tree corruption through existing HOST.IO_FAILURE/CORRUPT durably and no detail ephemerally; actual Io and Budget retain their own routes.

The amendment keeps the same-user window explicit. A pin prevents lawful GC and does not protect against same-principal writes; a directory inode does not attest descendant-byte immutability. Individually named files still receive their own rehashes. No new D1a sample or second digest recipe is proposed. The operation explicitly owns all relevant capabilities through child settlement; the LaunchMember borrow and sole production VerifiedLaunch construction path supplement that ownership rather than claiming to enforce it alone through clonable D1a data.

CI-3L now covers parts a-f, Binding, controls, store constructor changes and both platform helpers. It remains a separate post-CI-2/CI-3 unit with changed-path integration guards. D4-4 waits for the accepted amendment and the implemented/integrated operation. Acceptance of text alone never supplies that dependency. The mismatched CI-A2 context must be corrected without rewriting its in-flight review subject.

## Explicit rulings on r2

**Q1:** The content/path-length and owned-spelling corrections are accepted in design: c, p, b, k, h, q_i, L and P are distinct; the file basename includes its terminator; desc already covers descent spellings; the single P+1 launch buffer may be observed as CStr and transferred into the result without another allocation; and the store record has a separate one-time charge. Directory("") has zero resolution/descent work and a fresh retained-handle status plus path binding. Full accounting acceptance is withheld pending RF-2 and the exact-context correction RF-1. The proposed maxima dominate valid request work in principle, provided the root special case and empty symlink/directory maxima are explicitly handled without an undefined maximum, all final-path segment lengths are bounded and checked arithmetic precedes allocation. Actual comparisons/read attempts are not their envelopes.

**Q2:** Accepted. The new platform-owned path_status_no_follow(&CStr, work) can observe the exact absolute spelling and return kind/device/inode without allocating another path; directory_identity can obtain kind/mode/identity from the retained directory handle. Reusing P-7's st price is appropriate for one charged lstat/fstat. This accurately addresses NBO-1: the permitted CI-2 candidate's entry_status is single-component and omits identity, while sample_identity observes a TreeFile. Keep ENOENT/ENOTDIR and wrong kind/identity as Binding at the launch seam, true native observation errors as Io and refused charges as Budget. Off-macOS unsupported outcomes must be represented through the declared error types before charging; this adds no Linux standing. The pinned-context mismatch does not invalidate the amendment's explicit new primitive design.

**Q3:** Accepted. Charge the one owned L-byte admitted absolute store-path record immediately before its sole copy in ComponentStore::open_in, and in the fixture constructor, on the opening owner's existing ledger. It is not a per-launch cost, and it does not confer path authority. Adding a WorkScope changes the CI-3L constructor/call-site interface and must preserve typed Budget failure rather than collapse it into io::Error or create a new ledger. Account for exact path construction without unpriced intermediate joins. Carry the one-time term in the opening owner's model and control; the later launch recipe reuses it without charging it again. These changes belong after CI-2/CI-3 integration, not in its in-flight candidate.

## Controls and review limits

CI-T27's existing functional resolution, mutation, directory, binding and lifetime requirements remain appropriate. The new CI-T28 shapes, per-allocation/read/status exhaustion and native error-partition controls address the previous review, once exact work is separated from bounds. In particular, an empty-file test should prove a successful single EOF observation is charged once, not require a second attempt merely because the envelope allows it. An exhausted charge prevents the next operation and returns no path; earlier funded observations may already have occurred.

This review does not execute the proposed controls or accept CI-2/CI-3, CI-3L, production composition or qualification. It supplies no new cap, public diagnostic or route. Only REVIEW.md and review.json were written in this request directory. Neither repository, worktree nor control file was edited. No Cargo, rustc, build, lane, network, prohibited private fixture/key/installation material, held tree or entry, T2 store/overlay/cache, other pane or delegation was used.
