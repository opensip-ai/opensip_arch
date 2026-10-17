# D3A-PLAN-r3 review

**Verdict: REQUIRED-FINDINGS.** One required correction to the amendment's event descriptor; one nonblocking fixture-build observation. Under this request's joint gate, neither the plan nor LD-D3A-17 is accepted in this round.

## Exact subject

Verified the 752-byte manifest SHA-256 `1e6681d3782b91855c59068253550c79c793054238d3e929013e99f2e8422b45` and all three members:

| Member | Bytes | SHA-256 |
|---|---:|---|
| PLAN-r3.md | 52,932 | 63cfd25a805d0a855aa2072eeb9437a9b503eb04a03909438d3d63530c8bc2e9 |
| PLAN-r2.md | 46,262 | 63fa40da2e5d4766f92227d74a013d17791cb85765e2f3cf811730ca435776c1 |
| PLAN-r1.md | 26,606 | 9b2d051d242667b669c2e04d313b7769c8348b23fabd61c4af854df9bae5b454 |

Both historical files remain unchanged. Product HEAD is the manifest's `e937dac74c8e529fee3efb6f84439d05280e48ea`; architecture HEAD is its `24fbf182c3d3144d8a159bee7d9d2a0e6418996c`. Compared r3 against r2 and read the prior review, the revised decisions and controls, M3-D items 12, 20 and 21, S-OP-2's kinds/ordinary-registration/initial-event rules, and the product Errno implementation.

## Required finding

### D3APLAN-R3-RF-1 — Keep the scratch-retention errno field in existing kind K2

`docs/implementation/m3/supervisor-d/d3a/PLAN-r3.md:141`

LD-D3A-10 assigns the amended event an errno K3 Errno field. S-OP-2 item 5 defines Errno as K2: a numeric P0 field obtained from raw_os_error(). K3 is RegisteredCode<T>, a registered external text-code match with an unrecognized-text reduction. The product Errno type implements numeric encoding with push_i32 (crates/operability/src/kinds.rs:283-290). Thus the proposed descriptor kind is inconsistent with the actual I/O errno and with the existing-kind ordinary-registration rule. LD-D3A-17 explicitly aligns the amendment with this descriptor and the C-2 kind check, so accepting the amendment as written would accept the wrong field kind.

**Required correction:** Change the errno field to K2 Errno, preserving the actual syscall errno, numeric encoding and P0 class. Align the amended required-field inventory, descriptor and C-2 controls with that kind. Keep reason as K1 ScratchRetainedReason and errno present exactly for io-failure, absent for work-exhausted; no new kind or synthetic errno is needed.

## Round-2 resolution and amendment assessment

**R2-RF-1 is substantially resolved, subject to the kind correction above.** LD-D3A-17 now expressly proposes replacements to all three affected law passages. The settlement is a closed typed sum: Removed, Retained(IoFailure(Errno)), or Retained(WorkExhausted). The event adds the literal reason table and makes errno conditional on an actual removal I/O failure. Exhaustion has no errno and none is manufactured. LD-D3A-12 carries the same distinction into removal policy; the controls emit both valid shapes, reject both invalid reason/errno combinations, and test I/O failure and exhaustion without changing admission.

The amendment is appropriately narrow and sourced to the conflict between item 20's bounded removal and the former errno-only retention shape. It preserves item 6's later sweep, the no-follow/held-descriptor discipline, and item 20's admission gate. Measurement exhaustion still starts scratch-bound teardown; removal exhaustion is a cleanup outcome and does not reverse admission. The amendment introduces no privacy class, sink, provenance class or SafeField kind. With K2 corrected, adding the reason field and its two-member registry-literal table fits S-OP-2 item 3's ordinary-registration authority. S-OP-2 item 23's common role/universe and Project/Plan/Execution requirements remain intact; its provider/supervision event inventory is not reduced.

The acceptance gate is explicit in the authority section: the original law remains in force until acceptance, and the work-exhausted implementation paths in D3a-0 and D3a-3 wait for that acceptance. This review does not waive that gate.

**R2-NBO-1 is partly resolved.** The exact compiler-artifact path replaces directory scanning, the handoff is beside the test executable, no environment variable read is introduced, and an argument-free harness-free fixture exits successfully without writing bytes. The mtime claim still needs care as described below.

**R2-NBO-2 is resolved.** D3-T3 now reserves the absolute no-child/no-scratch assertion for killable/removable fixtures. Ceiling and exhaustion fixtures instead assert finite settlement, the applicable unreaped/retained disclosure and custody preservation. The mutation list separately catches leaving a killable child alive and signalling or blocking after abandonment. This matches the platform survival controls rather than contradicting them.

## Regression assessment

The r2-to-r3 comparison preserves the prior resolutions: participant-owned resumable provider acquisition and offset-preserving writes; one nonblocking I/O operation per callback; separate normal shutdown and fault teardown; nonblocking reap and custody-preserving abandonment; separately budgeted iterative scratch measurement/removal; complete registry field inventories or explicit blockers; a harness-free wire fixture without filtering; and pre-write tool materialization accounting with C3/J1 ownership.

The four-subunit order remains appropriate. D3a-1 still waits for reviewed, integrated D2b-1 and D2b-2. The outstanding D2b-1 accumulator findings are implementation dependency work, not accepted by this plan review. Typed participant accounting, the opaque one-shot TerminalOutput, single-owner settlement guard, exact negotiated Rust waits, EOF/exit joins, stderr reduction and route-versus-D9 ownership are retained. D3b-only ladders remain gated, unresolved event tables still prevent an item-21 completion claim, and real-codec conformance remains D5's. No additional plan regression was identified.

## Nonblocking observation

### D3APLAN-R3-NBO-1 — Do not use artifact modification order as proof of the build invocation

`docs/implementation/m3/supervisor-d/d3a/PLAN-r3.md:131`

Reading the exact supervisor_fixture compiler-artifact executable path removes directory-scan ambiguity, and the harmless standalone entry resolves the prior startup question. However fixture mtime >= test-executable mtime does not prove that the path file was written by the current invocation. A stale path file and unchanged executables can pass it on a later filtered run; a valid build can reuse an older cached fixture while rebuilding the test executable and fail it. The claimed automatic rejection of every invocation that did not build the fixture does not follow.

Make the build-and-run wrapper own this association explicitly: consume the artifact records from the successful current build, refresh or invalidate its path handoff, and run the exact test artifacts selected by that build. Define direct Cargo runs without that wrapper as unsupported or provide an explicit invocation binding; do not present mtime ordering as proof. This remains a test-lane reliability observation, not a production authority gap.

## Boundaries

Used only read-only reading, hashing, JSON parsing and Git queries. No Cargo, rustc, build, lane, network, other pane or delegation was used. No private 413 fixture, installation directory, signing key, held tree, T2 store or T2 cache was read. Only this REVIEW.md and review.json were written; neither repository, worktrees nor control files were edited.
