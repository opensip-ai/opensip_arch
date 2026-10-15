# B2-b4 implementation plan r4 amendment review

Verdict: **ACCEPT**. Both round-three required findings are resolved and NBO-1 is addressed. No new required findings or non-blocking observations.

## Exact subject and scope

Independently rehashed the 452-byte subject.json to SHA-256 `e590eb2ca6cae2426056aedf15093f94cd10b12f7679c36ab806256a12cc38f6` and verified its sole member: PLAN-r4.md, 26,511 bytes, SHA-256 `c83ffe61a69ade46ecd2e43bf94e12155ac419d21c9c06884c0b5277ab3c7f2e`.

Both repository HEADs match the full subject bases. Product main is clean; the current lock selects inventory v196 and has 164 contract successors. The introduction now distinguishes historical r2 bases from the current product ec2d655d/architecture a84239c2, shared r96. The request's stale descriptive v195/r95 prose does not alter those exact reviewed bases.

Compared r4 with r3 and published accepted r2. Section 1 and the complete LD-B2B4-1..7 block are byte-identical to accepted r2. This review judges the section-2 amendment and its new decisions, without reopening the accepted census unit. Verified the accepted B2-b4a subject and both archived probe artifacts against their pins; no native probe or corpus census was rerun.

## Round-three corrections

**B2B4PLAN-R3-RF-1 — resolved.** The size inventory now explicitly includes usize, needed by classify_cost's segment term. More importantly, it is closed by rule: every size_of operand in an anchored byte formula must have a recorded, natively asserted size. Extraction from matched formula text must refuse an absent operand, and a planted unpinned-type formula must be caught. The enumerated current types cover the inspected byte formulas, including delegated platform status/capture/filesystem costs. Splitting assertions between security and a platform integration test is sound for type visibility. These are implementation requirements, not already executed native assertions.

**B2B4PLAN-R3-RF-2 — resolved.** Option (c) now derives its residual base, perRootByte and object count. It distinguishes relative retained keys from transient absolute spellings and explicitly names spell, root copies, frame/verdict spellings and scope-entry construction. Eliminating the root coefficient is a goal requiring corresponding allocation changes and verification, not an automatic consequence of re-keying. Pre-successor figures are labeled counterfactual estimates; only the bound successor census determines final caps under this option. This specific qualification governs the introductory statement about weighing measured option costs.

**B2B4PLAN-R3-NBO-1 — addressed.** Historical and current bases are labeled explicitly without changing section 1 or the original decisions.

## Facts and byte-model method

The stated storage concern is supported by the source and accepted probe evidence. The probe records aws-sdk-rust using 639,480,718 charged bytes at root length 134, under disclosed temporary higher limits. Item 19's member cap and the index/config/file-read bounds do not limit the walker's independent per-name allocations and their spelling lengths. The probe's temporary caps are not proposed product caps.

Checked the relevant native formulas: owned record overhead, raw/listed names and validator copies, absolute spellings and scope records, observation tuples, classify_cost's segment/target terms, root/frame/verdict records, directory/file opens and status buffers, ACL and filesystem capture branches, and bounded-reader growth/target storage. For a fixed population, the root prefix contributes linearly to absolute path lengths; relative-path/type/fixed-buffer terms form the base. The affine model is therefore sound as a planned structural upper bound when every charged formula is included and anchored. It measures cumulative ledger requests, not allocator RSS.

The byte-branch comparison is valid at the stated native sizes: the largest ACL record is 128 * 16 + 128 = 2,176 bytes, below the stated FS allowance of 2,368. The planned native assertions must verify the operand sizes and the model must derive the allowance from the pinned formulas. Full growth through the bounded-reader ceiling is conservative. The existing explicit interruption exclusion remains; this amendment does not promise completion under arbitrary I/O retries.

Extending completed-walk soundness checks to bytes at each scratch root's actual byte length is appropriate alongside source inspection and native size assertions. It retains all 52 walk vectors and composed workspaces and adds a mutation dropping a material per-name byte charge. The R=134 report cross-checks the accepted probe. R=1024 is a useful macOS pathname-scale report, not an implicit admission bound; R=4096 matches the explicit project-root spelling check in path_binding.rs::components. Descriptor-relative traversal makes those reporting points meaningfully distinct.

No byte predictions, native size assertions or byte margins are established by this plan acceptance. They must be supplied and reviewed in B2-b4b1.

## Options, caps and owner gate

The alternatives fairly cover preserving current behavior with census-derived caps at the existing spelling bound, adding a smaller spelling bound/refusal, and redesigning storage followed by a new census. The revised option (c) no longer assumes its cost reductions. The amendment must recommend one with its arithmetic and identify rejected alternatives; no numerical cap is selected here.

B2-b4b1 adds byte evidence without changing caps. B2-b4b2 separately amends item 12 using that evidence and corrects the prior byte-bound premise. B2-b4b3 changes code only after acceptance and, for a storage redesign, after the successor and re-census bind. It updates cap tests and closure pins and then asserts the lead-readable margin at the selected R. The 2x rule remains the source of final caps; no invented budget constants are authorized.

A recommendation changing behavior beyond caps is explicitly raised to the owner, including option (b)'s new refusal. Held-out margin remains outstanding and is escalated under LD-B2B-4; lead-readable success cannot complete B2-b. No owner assent, current law revision, code change, binding or product qualification is inferred.

Only read-only reading, hashing, JSON parsing and Git queries were used. No Cargo, tests, builds, lane, network, other panes or delegation were used. No private fixture, installation directory, signing keys, held trees or T2 store/overlay was accessed. Only REVIEW.md and review.json were written; neither repository, stage nor controls were edited.
