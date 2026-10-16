# B3-B3C-r1 review

Verdict: **ACCEPT-UNIT**.

Required findings: none. Non-blocking observations: none.

The subject manifest independently matches 7948 bytes and SHA-256 `91b0ea21228cf12812dded61de03c8c428a2a6b2ce4b554c86749167aef3b313`. All 34 members match their sizes and hashes. Product main is clean and the candidate is detached at `fb63a93adb77f7ef50663be41241edba4c3f966d`; architecture is at `f6b561d75e70c34d010a76dd11e9ecc1047e2cb8`. Authority, product-lock and product-map pins match. The candidate changes exactly the four mapped files.

## Companion record and plan fidelity

LD-1 is acceptable without a plan amendment. Section 4.3 requires workspace full-ledger rows, their 2x classification and return of failing caps to law; it does not prescribe the filename holding those rows. The companion is generated from the existing census model and carries its manifest, closure, sizes, limits and root lengths. The Rust classification ties the workspace identities/member sets to the original census and requires both the companion and repository census caps claims to hold. This supplies the required workspace result without weakening receipt staleness or introducing another blind refresh.

The original record remains explicitly walker-only. Its superseded outstanding string must be read with this companion and SCOPE's explanation; it is not the authoritative full-ledger result after this unit. Keeping that known legacy text is acceptable for this bounded implementation choice, given the explicit companion and executable joint classification. It must not be used to report workspace margins as still outstanding after this unit is integrated. Changing it later must continue to respect the receipt-binding gate.

## Branches and D15 shape

LD-2 correctly avoids using branch A alone as the workspace margin. Branch A configures every member mount and pays item 6b at the full workspace member count. Branch B admits the rendered carrier's providers and uses automatic discovery, which can cost more walker edges even with fewer admitted members. Both are calculated separately, including their actual composition ordering, and a workspace passes only if both pass. Configured roots and explicit joins use the same accepted member/charged walk path for these member-mount inputs; different provenance does not require a third cost branch. These are the stated corpus compositions, not a universal bound over arbitrary additional user configurations or changed trees.

LD-3 follows the accepted conventional-Git control: W is outside a repository, every verified member mount receives a conventional .git directory, and carrier entries come from the overlay's rendered link map. Undeclared consumer-only mounts remain boundaries in branch B; branch A admits all mounts. Python has no reader/carrier and admits no branch-B member, but branch A still exercises both configured members.

Empty modeled .git directories are safe for this upper bound: the walker prunes their contents, and the reused member model already charges layout/config/index and session evidence at its ceilings. Assuming no index gitlink boundaries retains the larger traversed population. The synthetic shape is not a claim that the corpus has real Git metadata or that native T2 measurements were taken.

## Verification and model reuse

The tool first verifies every readable member store with the existing held-out guard and integrity model, and verifies each overlay's canonical record, digest, archived acquisition copy and mount targets. Held-out workspaces are skipped before their store/overlay work; held-out members cannot pass store_path.

It reuses the census's composition, D15 terms and full-ledger arithmetic and the accepted carrier renderer, adding no new modeled native charges. Branch A refuses if any mount is unadmitted. Cargo rendering must equal the cache file byte for byte before its text is installed into the modeled tree, with the verified overlay node's size checked too. npm refuses an existing conflicting carrier. Carrier pins are derived from the exact rendered bytes.

The companion pins its generator, census, member model and link tool in addition to the shared inputs. I independently rehashed those pins and every closure/manifest pin, and compared all shared input fields and overlay digests with the census. The Rust test independently checks input/workspace/member correspondence, member-set constraints, all four additive totals (objects, edges, base bytes and per-root bytes), every branch/workspace verdict, failingWorkspaces and caps, and the joint repository/workspace caps claim. Stored per-mille margin fields are produced by the reused arithmetic; I independently recomputed every margin and byte-at-root value in this candidate as well.

## Results

All five workspaces hold under both modeled branches. The independently recomputed margins (objects / edges / bytes at R=4096, per mille) are:

| Workspace | Branch B | Branch A |
| --- | --- | --- |
| serde-json | 1362229 / 5899 / 42683 | 1086888 / 5904 / 23090 |
| aws-lambda-tokio | 210314 / 5326 / 6770 | 161462 / 5568 / 5972 |
| smithy-powertools | 187849 / 5399 / 33847 | 126008 / 5633 / 19877 |
| smithy-sdk | 10867 / 2630 / 6546 | 11172 / 3842 / 7484 |
| boto | 99864380 / 77672296 / 82228658 | 57371 / 5351 / 17138 |

The tightest workspace margin is smithy-sdk branch B's 2630 per mille edges. The tightest workspace byte margin is aws-lambda-tokio branch A's 5972 per mille. FailingWorkspaces is empty and caps remains recorded-margin-holds. The repository/held-out results remain those accepted in B3-b3a1/B3-b3b.

## Controls and evidence

I ran only the two expressly permitted commands: the ten synthetic/hermetic workspace controls pass, and the companion --check over readable stores/overlays passes. The controls exercise Cargo/npm/Python shapes, providing/all-member distinctions, per-member costs, carrier/refusal checks, input bindings, a failing branch returning caps and an unread held-out workspace.

The four archived mutations are caught by the intended gates: removing repository markers makes branch A fail admission; dropping branch A fails shape/coverage and failing-cap controls; suppressing carrier rendering loses branch-B providers; zeroing a recorded member term fails Rust's additive classification. These substantiate the new mechanisms alongside the accepted model's native soundness evidence.

The census tool, member model, link tool, census record, census vectors and blind receipt are independently byte-identical to main. The archived ordinary census check passes, so the current blind receipt is preserved. I did not execute that command because it is outside this request's runnable command list.

Final evidence records equal named security failure sets (14 at base and candidate) and one new passing Rust test: 1166 versus 1167 total passes. Those full suites retain the base failures. Formatting is clean, warning-denied all-targets Clippy passes with and without scenario fixtures, the census/control checks pass, and verify_design passes with qualification false. These executions were reviewed from pinned evidence rather than rerun here.

Acceptance is for the workspace-margin unit. Its inventory and integration/status work remain separate; qualification and completion of B3-b, B2-b or M3-B are not conferred by this review.

Only REVIEW.md and review.json are written. Neither repository, worktree nor control files were edited. No Cargo, rustc, builds, lane, blind mode, network, prohibited fixture/installation/key/held-tree access, held-out store or overlay, other panes or delegation was used. No native tests were rerun; the sole executed tests were the explicitly permitted hermetic Python controls.
