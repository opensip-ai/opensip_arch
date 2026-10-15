# B2-b4 implementation plan r1 review

Verdict: **REQUIRED-FINDINGS**. Three corrections are required before this plan can support an upper-bound census.

## Subject and review boundary

Verified the 452-byte `subject.json` SHA-256 `59131a8b8bb7431d91c367833c9a654c55dd2a1f8d9afd480de2c5577b03b982` and its sole member, the 12,171-byte plan SHA-256 `a59057dbdd6fb2e923e6424239459debc2b3a1587caf54d42a3a2e3d240485e6`. Product and architecture HEADs match the requested bases, and product main is clean.

Read plan r4 section 1.4/LD-B2B-4, M3-B r5 item 12, plan r3's listing-cost decision, the bound reference's population adapter, the walk-vector adapter and native test composition, acquisition/overlay documentation, the manifest, and the relevant native charge sites. No census or tests were executed. No stores or overlays were traversed, including lead-readable ones; no held-out store or overlay was joined, statted or opened. The optional estimate was not independently counted.

## B2B4PLAN-R1-RF-1 — Workspace member sums are not an established upper bound

Plan locations: section 1.5, line 54; LD-B2B4-4; related native controls in section 1.4.

An independently walked repository root is already lent to the walker. As an ordinary child below a workspace root, it incurs additional traversal and custody work. `discovery_walk.rs:782-805` classifies the child, allocates its spelling, opens/status-checks it, probes its VCS markers and observes `opensip.json`; line 813 allocates its frame. When a unit chain passes through that member root, `directory_passes` at lines 499-515 may capture its ACL/filesystem and allocate a memoized verdict. Automatic standalone traversal skips custody of the selected root itself (`enter` skips ancestor index zero and only judges a nonempty start path).

These charges are not merely the overlay root's listing. The clearest case is a member with a package marker at its root: standalone automatic discovery can capture the marker without judging the selected root; nested discovery also judges/captures the member directory. Counting its standalone cost plus the parent's listing does not establish that extra capture/probe/open work is covered. Deeper descendants can repeat the new ancestor judgment if it was not reached at the member root.

Required correction: run the model over an explicitly composed synthetic workspace, or define and justify an explicit conservative transition surcharge per mounted member. Cover boundary, depth, pruning and chain-custody effects. Specify which logical/native workspace walk is being bounded; walking the actual symlink overlay does not descend into members. Add a native synthetic workspace comparison and a mutation dropping the transition surcharge. The 52 existing individual-repository vectors do not validate the proposed additive workspace rule.

## B2B4PLAN-R1-RF-2 — A length-only maximum read-attempt count is undefined

Plan location: section 1.3, line 41.

`gitdir_target` calls `read_bounded_observed`. In `work_reader.rs:146-190`, the reader charges its initial object and an edge on every read-loop iteration. A positive short read advances the byte count; an EOF completes it. An `Interrupted` error at line 189 retries without advancing that count. Thus arbitrary additional charged attempts are possible for the same unchanged file length. There is no finite length-only maximum over all supported outcomes. The ledger's eventual budget refusal is not evidence of a successful walk with a 2x margin.

Required correction: define the read/retry envelope and precisely what the modeled bound promises. Account for short reads, EOF and interruptions under an explicit justified bound, or separate structural census costs from retry/exhaustion behavior and reconcile that limitation with the law-level margin claim. A future reader change, if selected, needs its own authorized review; it cannot be assumed by this plan. Add a focused control for the chosen retry treatment. The existing native vectors' ordinary reads cannot establish this bound.

## B2B4PLAN-R1-RF-3 — The pinned cost dependency set is incomplete

Plan location: section 1.3, line 36; LD-B2B4-3.

`platform/src/filesystem/directory_open.rs:32-42` calculates its directory-open edge cost as `1 + status.edges`, where `status` comes from `path_binding::status_read_cost`. That helper's objects/edges are defined in `platform/src/filesystem/path_binding.rs:121-126`, which the explicit pin list omits. Altering the helper changes the cost while leaving the pinned caller and its anchored expression unchanged. The promise that any charge change necessarily breaks the census therefore does not hold for the stated source set.

Required correction: pin and anchor the transitive cost-producing dependency closure, including `path_binding.rs`. Specify a charge-site-to-model-term inventory covering direct walker charges and delegated costs. Include a drift control changing the delegated status cost without changing its caller. The implementation should refuse unsupported expressions/dependencies rather than substituting remembered constants.

## Other assessments

The plan retains plan r4's all-entry gate: B2-b remains incomplete until every T2 entry has the required margin. Landing an honestly failing census as B2-b4a evidence is sound when failing rows cannot be mistaken for a passing margin. Returning caps to item 12 for an independently reviewed amendment, weighing a cheaper walker, and changing code caps only after that amendment is accepted preserves the law path. Held-out headroom remains outstanding; raising its decision to the owner does not infer approval or authorize access. Turning on a full margin assertion after a cap revision must still mean the censused population, with the all-entry held-out gate open.

The integrity design is coherent at plan level: reconstruct both QD-22 and Git-tree pins from stored bytes; no-follow traversal and symlink-text hashing; gitlink commit pins and placeholder population; exact mode/population checks; and refusal on mismatches. This is not verification of an implemented integrity checker. The manifest has 49 repositories, 39 lead-readable and ten held-out, plus five non-held-out workspaces. The early held-out flag/id branch and planted-digest control are appropriate; implementation must enforce the stated no-join/no-stat rule.

Reusing the accepted adapter and bound `walker_population`/`finish` keeps population and rule authority intact. Counts must represent actual operation multiplicities, including absent probes and repeat observations, not only unique paths in the projected filesystem. Inspecting the native code confirms charges for raw names including dot entries, owned name/path/validator records, observations and retained records, classification temporaries, directory opens/status reads, marker opens/status/captures, chain verdicts, root/frame records, and `.git` custody/read/target storage. A source-anchored mapping and native comparisons are useful controls, but the stated controls do not resolve the workspace, retry and dependency omissions above.

Avoiding machine-specific native store walks in product tests is sound; native comparisons can use synthetic scratch trees. The pre-census size calculation is prominently labeled an unverified estimate and is not offered as evidence. No cap change, binding, production caller, byte census or qualification is claimed.

Only `REVIEW.md` and `review.json` were written. Neither repository, stage nor controls were edited. No Cargo, tests, builds, lane, network, other panes or delegation were used. No private fixture, installation directory, signing keys, held trees or T2 held-out store/overlay was accessed.
