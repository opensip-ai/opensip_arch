# D3A-PLAN-r2 review

Verdict: **REQUIRED-FINDINGS** — one required representation correction and two non-blocking observations. The principal round-1 design gaps are addressed.

## Exact subject

Verified the 566-byte manifest SHA-256 `c441c53735517cffeb038849bf695d492a60ad54e0868e5c3003a91216a191db` and both members:

- PLAN-r2.md: 46,262 bytes; SHA-256 `63fa40da2e5d4766f92227d74a013d17791cb85765e2f3cf811730ca435776c1`.
- Historical PLAN-r1.md: 26,606 bytes; SHA-256 `9b2d051d242667b669c2e04d313b7769c8348b23fabd61c4af854df9bae5b454`, unchanged.

Product remains at the named base `e937dac74c8e529fee3efb6f84439d05280e48ea`. Live architecture HEAD is `24fbf182c3d3144d8a159bee7d9d2a0e6418996c`; the subject pins remain exact. Reviewed the revised plan, applicable M3-D/S-OP-2 passages, existing platform/control/ledger interfaces and the in-flight FrameAccumulator as an interface dependency. This does not accept that candidate implementation.

## Required finding

### D3APLAN-R2-RF-1 — Resolve the no-errno scratch-exhaustion representation explicitly

Location: `docs/implementation/m3/supervisor-d/d3a/PLAN-r2.md:137`.

LD-D3A-12 correctly gives removal its own finite work budget and preserves admission on cleanup failure, but specifies supervision.scratch.retained {errno} for exhaustion with no errno. M3-D item 12 closes scratch to removed or retained(errno), item 20 requires retaining/logging the failure with its errno, and item 21 declares that event's errno field. LD-D3A-10 simultaneously promises exact required field/optionality preservation and a C-2 check rejecting missing or extra fields. Work-budget exhaustion is not a failed syscall and supplies no actual errno. As written, this path must either omit the promised required field, manufacture an errno, or construct a settlement outside the stated closed shape.

Required change: Choose and document a lawful typed representation for retained scratch caused by work-budget exhaustion, distinguishing it from retained(errno) for actual I/O failure. If that requires a narrow M3-D content/descriptor amendment, make it explicit in the lead decision and authority record rather than calling it unchanged field preservation. Align the settlement, event fields/optionality, registry descriptor check and exhaustion controls. Preserve cleanup noninterference with admission, and do not synthesize an OS errno for budget exhaustion.

## Round-1 resolutions

**RF-1 addressed.** Incremental prefix/digest/payload ownership is assigned to the participant through D2b-1's accumulator. Pending writes retain their buffer and offset, WouldBlock preserves state, and each callback makes at most one non-blocking I/O operation before the loop services other descriptors and timers. Split-frame, coalescing, partial EOF, short-write and interleaved health/deadline controls are now assigned. Whole-frame read_frame is correctly described as non-resumable. D3a-1 waits for the accumulator's reviewed integration; it does not claim that dependency is already accepted. The current candidate constructor also takes `remaining: Option<u64>` in addition to profile/depth; preserve that allowance in the concrete integration rather than relying on the abbreviated two-argument description in the changes table.

**RF-2 addressed in plan.** D3a-0 explicitly changes D1a's owner module first. try_reap uses WNOHANG; abandon consumes the Child into Unreaped, preserves the root hold, and prevents later signalling or blocking destructor reap. D3 owns the ceiling and outcome, including unwind cleanup. The syscall-recording survival control addresses the original destructor escape. Implementation review must verify that consuming abandon really suppresses Child's old Drop and that Unreaped destruction keeps the custody hold for the host process lifetime.

**RF-3 addressed.** The normal end now belongs to D3a-1: shutdown(reason: normal), closure of input/fd3, shutdownAck/exit/EOF joins and the protocol-specific grace. Missing acknowledgement or exit delivers deadline and enters at T-2; clean completion does not start the fault ladder. Both exit/EOF orders, missing acknowledgement and nonzero exit are controlled.

**RF-4 substantially addressed, with the finding above.** Iterative, no-follow measurement and removal are separate mechanisms charged through caller-supplied WorkScopes, with no whole-directory collection and no misuse of process counts. Each walk is finite, and cleanup failure does not reverse admission. The remaining issue is the typed record/settlement shape for budget exhaustion.

**RF-5 addressed for the original provider-event omission.** The revised inventory retains required fields, identities, units and optionality, including role/universe. Literal and protocol-derived provenance are distinguished, the empty RustDetailCode behavior is retained, and StageKind/ProviderState/Signal are explicit resolution blockers. An unresolved required field blocks its event and prevents an item-21 completion claim; no reduced substitute is authorized. The required-field descriptor check makes that limitation reviewable. The new scratch-exhaustion case must meet the same standard.

**RF-6 addressed as a wire-fixture design.** A harness-free first-party test target writes exact fd1 wire bytes without libtest output, and raw byte equality forbids filtering. The debug-only dev-dependency feature fits item 1. LaunchSpec::fixture is the additional exposed construction seam; existing public environment/recheck/VerifiedLaunch inputs permit its test launch without a production D4 constructor. NBO-1 below concerns identifying the artifact, not wire normalization or production fixture authority.

**RF-7 addressed.** D3a-2 supplies the checked pre-write materialization counter and the sourced 32 GiB + 1 GiB tool bound; C3 owns whole admitted-copy invocation and J1 owns public projection. Provider scratch limits are explicitly distinct. Synthetic exact-limit/one-over and after-write/wrong-limit controls cover the assigned interface without claiming C3 materialization is implemented.

**Prior NBOs addressed.** The lead explicitly accepts the single-owner equivalent of the stated CAS and specifies the guarded constructor, terminal state and one-time consumption, with re-entry/late-event/post-take Drop controls. Typed payload accounting and boundary EOF/truncation observations are now explicit. A non-Clone verified TerminalOutput, rather than a candidate count, gates one-time release/discard, with a bad-commitment control and later real-codec reruns. Keep its payload protocol-specific or opaque; it must not become a shared semantic frame representation across TS2 and Rust3.

## Split, questions and retained boundaries

The four-part order is sound: platform mechanisms first; loop/joins once D2b-1/-2 are integrated; resource policy; then admission/records/outcome joins. Unresolved table events remain blocked rather than being described as complete. D3b-only ladders stay behind LadderUnavailable and Linux remains outside this macOS scope.

Landing the exact ProcessEvent definition early is appropriate; both later codecs consume one unchanged definition. The participant remains the only fd1 reader/fd0 writer and the supervisor receives boundary observations and typed accounting. The fixture scopes and D5 reruns are properly separated from conformance. Project-only tool identity requirements remain an ordinary registration, and OwnerRoute remains a route discriminator with J2 owning D9 mapping and goldens.

**Q6:** choosing the existing discovery-profile numeric caps as a provisional D3 scratch-work policy is a reasonable bounded interim, provided it is recorded as this lead's reuse decision, not proof that M3-B established a scratch workload envelope. The plan now does so and records X-D3A-1. Freeze the selected values for this release and keep measurement/removal budgets separate; a future discovery-cap change must not silently change D3's policy. No new filesystem depth or entry count is inferred. The choice does not resolve the retained-scratch representation finding.

No regression was identified in prefix-before-body control acquisition, exact negotiated Rust waits, bounded typed expiry, health-versus-progress separation, stderr reduction, EOF/exit joins, discard on non-clean settlement or owner-route separation. The added platform sampler and budgeted walks are mechanisms; deadlines, ceilings, work limits and outcomes remain D3 policy. Numeric wait/memory/tool limits retain their cited values. No caller, real-codec conformance, completed item 21 while blocked, D3b completion or product qualification follows from this plan.

## Non-blocking observations

**D3APLAN-R2-NBO-1 — Bind the fixture path to this build rather than directory uniqueness** (`docs/implementation/m3/supervisor-d/d3a/PLAN-r2.md:122`). The harness-free executable resolves stdout contamination, but scanning the deps directory for a unique supervisor_fixture-<hash> does not identify the artifact produced by this invocation. Incremental target directories can contain several prior hashes, or only an unrelated stale artifact when a filtered test invocation did not build the fixture. Failing on ambiguity is safe but unnecessarily makes ordinary reruns brittle. Have the lane/build invocation supply or verify the exact test artifact path, require that the fixture target was built, and define a harmless no-behavior entry when Cargo runs the harness-free target on its own.

**D3APLAN-R2-NBO-2 — Qualify the no-child/no-scratch Drop control for disclosed ceiling failures** (`docs/implementation/m3/supervisor-d/d3a/PLAN-r2.md:168`). D3-T3 still says Drop in each state leaves no child and no scratch, and the mutation list still treats an unsettled Drop leaving a child as invariably wrong. The new Unreaped path intentionally retains custody and may leave a surviving root at the ceiling; bounded removal may intentionally retain scratch. State that the absolute cleanup assertion applies to killable/removable fixtures, and that ceiling or work-exhaustion fixtures instead assert finite settlement, correct retained/unreaped disclosure, custody preservation and no later signal/blocking reap. The new D3a-0 controls already support this distinction.

## Review boundaries

Used only read-only inspection, hashing, JSON parsing and Git queries. No Cargo, rustc, builds, tests, generators or lanes were run. No network, other pane, delegation, private 413 fixture, installation, signing key, held tree, T2 store or cache was accessed. Neither repository, worktrees nor control files were edited. Only the requested REVIEW.md and review.json were written.
