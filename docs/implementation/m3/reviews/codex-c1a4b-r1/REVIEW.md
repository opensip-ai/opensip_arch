# C1A4-BLIND-r1 pre-run review

**Verdict: REQUIRED-FINDINGS. `runAuthorized: false`.** One required finding and one non-blocking observation. The missing pinned post-run checker prevents authorization of the complete procedure as written. No blind run was performed.

## Subject and boundary verification

The subject manifest is 26,750 bytes, SHA-256 `fb601e98c772d6cd6b79ef62859828c08bd99152fb4a2cbc08fed7745461fd2f`. **All 107 members rehash correctly.** All four candidate product files match product-map.json and their archived copies; the three existing parent files match the pinned product base. Every authority pin in source.json also matches.

Both product main and the detached candidate worktree are at `b7538549b727e13013f36d3b7c2e2917e767f3f2`. The candidate has exactly the four declared changes, including the one new synthetic-control path. Its architecture base is `7e8f5377373a0b35a3ee15fa8424feb3c3733f59`.

Only permitted read/hash/JSON/Git inspection and the three expressly allowed checks were used. No lane lock, Cargo, rustc, build, census with --t2-cache or --held-out-blind, run driver, blind-equivalence program, installation, private fixture, signing key, held-out tree/store/overlay or T2 cache was accessed. Reading archived evidence did not rerun it. Only the requested REVIEW.md and review.json were written.

## Required finding

### C1A4B-R1-RF-1: Include the post-run checker in the pinned run package

`docs/implementation/m3/snapshot-plan-c/c1a4-blind-r1/RUN-PLAN.md:31`

The reviewed run plan invokes run_c1a4b_post_checks.py after the one blind run, but no such file is present in the committed-path package or its 107-member subject manifest. The only located runner is /tmp/opensip-implementation/run_c1a4b_post_checks.py, 2555 bytes, SHA-256 9a5d167071a4e4eb8cd34d0c47870ddb9c871a61fe95e82c9633f4bbfea5e799. Its current source uses the intended census tests, synthetic controls and verify_design, but those bytes and its location are not bound by this subject, and the bare invocation does not resolve from the stated committed architecture path. The exact end-to-end procedure whose authorization is requested is therefore incomplete, even though the two blind-mode commands themselves are reviewable.

Required change: Archive the actual post-run checker under the package, include its exact bytes/hash in the subject, and update RUN-PLAN.md to an unambiguous interpreter/path invocation. Alternatively replace that invocation with the exact reviewed post-run commands and lane/environment procedure in the pinned run plan. Resubmit the updated manifest for the pre-run gate; do not spend the one blind run before the complete procedure is accepted.

## Code and confidentiality assessment

The companion uses discovery's held_out_store_path with the same module instance's _BLIND token, followed by verified_tree. Ordinary record generation skips held-out repositories and workspaces and composes held-out results only from the receipt. A second consumer of the existing guarded join is consistent with the explicitly reviewed companion mode; it introduces no second digest-to-store join.

The exception paths are appropriately closed. Integrity/access failures become IO or INTEGRITY; measure, member/population evaluation and model failures become IO or MODEL; a mismatched population becomes POPULATION. Exception text and SystemExit payloads are discarded. Internal require messages do not enter rows. Remaining blind-run exceptions, exits and interrupts reach main's BaseException handler and print only the generic failure line. Argument-parser exits occur before store access, and abbreviations are disabled. The pinned measure/model/member/reference paths do not print held-out paths or content. The source inspection and canary controls together support this conclusion; the canary alone is not the entire argument.

Measured, over-item-5 and error rows use closed formats. In the over-item-5 row, population is the literal boolean true representing a successful equality check, not a size or count. That follows the lead's stated allowlist ruling. No margin is claimed for that row, and it is neither a measured pass nor a failure. Any error makes the state incomplete; otherwise a measured failure makes it fails; passing measured and over-item-5 rows yield holds. validated_receipt checks keys, booleans, nonnegative integer margins, unique ids, passes2x and derived state. compose_held_out checks current bindings before composing rows and requires exact id coverage for a current receipt.

One measure path supplies both ordinary and blind costs, including walk, session and sealing, and both use the reference population check. Floor-per-mille margin at 2000 agrees with twice-cost fitting. The archived equivalence program filters to heldOut=false before calling the blind row with a synthetic held-out label, so it opens only lead-readable stores. Its evidence reports 39 equal rows: 35 measured and 4 over item 5. It was not rerun here.

## Bindings and record identity

snapshotSources derives the model's whole-file and anchored dependencies, session dependencies, ledger, sealing, canonical encoding/path-bound and discovery depth sources. The other bindings carry discovery's complete public receipt bindings, the four tools, caps, item-5 bounds, maximum depth and sealing term. Discovery's nested bindings also retain the reference-loading code and generator closure. This covers the source reads/pricing inputs inspected here. The synthetic bound-product construction and completeness check support the closure; the lifecycle tests additionally demonstrate stale results on drift in all seven bindings and on actual bound source/tool/member-model byte changes.

The margin test now compares unique lead-readable ids, in order, against discovery's compiled repository/workspace rows, and held-out ids against discovery's compiled held-out rows. It does not trust self-consistent record counts alone. The two record mutations demonstrate the intended protection against consistent truncation and duplicated ids.

Independent comparison with the parent confirms the record changes are limited to the three added top-level fields, counts.heldOut, the companion tool pin and standing. Every lead-readable and workspace row is equal. The receipt remains absent and its ten companion rows outstanding; this is not held-out margin evidence.

## Run assessment

Apart from RF-1, the run's sequence is appropriate: one lane hold at nice 10 with private 0700 TMPDIR, clean main/worktree checks, exact companion hash from product-map.json and four unchanged tool hashes, removal only of the stale discovery receipt, then one discovery blind command and one companion blind command only after discovery's successful command/empty stderr/receipt creation. The runner captures command status and the permitted summaries/receipts. Ordinary generation/checks follow; they obtain held-out results only from receipts. No other code in the inspected run or post-check source opens a held-out store.

The expected discovery binding deltas are correct at the frozen base. Independent public-pin comparison confirms exactly the two closure source changes, the generator-closure reference change, changed tool and unchanged memberModel. The source/evidence support unchanged discovery caps, root lengths and size inventory. The expected list explicitly includes all eight bindings, including sizes, avoiding B3-b3b's omission. All seven companion bindings are new. Source-preserving discovery cost/cap changes justify expecting old/new discovery rows to be equal; that equality is a post-run assertion to review, not a held-out result verified now.

The freeze is sufficient as an explicit operational precondition: only the reviewed gate code may follow b753854 before the run, and C1b-0 stays after it. NBO-1 distinguishes that condition from the runner's narrower implemented checks. The recorded comparison and exact four expected output files support the post-run review. Nonzero ordinary commands, unexpected bindings/rows/changed files, stderr, or error rows must remain failures in that review even though the driver records data rather than committing. No failure authorizes a rerun. A measured companion margin below 2× returns the caps to the law; over-item-5 classification claims no margin. X-C2/B or later recipe work is outside this frozen run.

One inventory successor after the run for the new control and companion-receipt paths is acceptable within the scope explicitly proposed here, after the run's independent review and bind. It does not waive either review or claim the held-out result in advance.

## Validation

Live checks permitted by this request all passed:

- Companion synthetic blind controls: 21 tests.
- Discovery synthetic blind controls: 25 tests.
- Discovery vector-only --check: verified.

The pinned b753854 lane evidence records 18 successful check rows, including warning-denied security Clippy, edited-file rustfmt, eight focused census tests, equality projection, three lead-readable-cache --checks, the 39-store equivalence, unchanged 19-file census closure, environment checks, operability (114 rows), verify_design (175 successors) and eight caught mutations. Both security suite runs have 1,187 passing tests and the same 14 failures, with no new test or differing failure name. This is equal baseline/candidate failure evidence, not a wholly passing suite. The earlier 3d1d771 lanes are history and were not used as the acceptance lane.

## Non-blocking observation

### C1A4B-R1-NBO-1: Make the stated freeze and detached-worktree preconditions executable

`docs/implementation/m3/snapshot-plan-c/c1a4-blind-r1/evidence/run_c1a4_blind.py:48`

The runner verifies equal main/worktree HEADs, clean status and the five tool hashes. It does not independently verify that the worktree is detached or that main is exactly b753854 plus only the gate code commit. Those stronger conditions are explicit RUN-PLAN preconditions and remain necessary: the five hashes alone do not freeze every bound Rust/identity/reference source.

Suggested change: Before removing the old receipt, assert detached HEAD and the exact approved code commit/base relationship and changed-path set, or record a separate exact preflight proving these conditions. Do not interpret the existing equal-HEAD/tool checks as a substitute for the broader freeze.

