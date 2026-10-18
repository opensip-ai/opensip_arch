# D5 plan r2 review

**Verdict: REQUIRED-FINDINGS.** Four required findings and one non-blocking observation. The revisions substantially address round 1, but the revised structural and validation rules still need the corrections below.

## Pins and scope

Verified the 563-byte manifest, SHA-256 `091699f80bdb2c762ad66ec36e5d0968983699c4fff82061ad140f55b512d05c`, and both members. PLAN-r2.md is 44,878 bytes, SHA-256 `b09274a915bbbffd2ea0badcaaca42c28ac9a39356f3204597ed1c069ac100e3`; the 26,668-byte r1 history remains `9230130437faba34bc99242aa6d4a0103aa69b24b576449a5e531f812353492f`. All eleven opening source hash prefixes match.

Used Git to inspect product sources at `4e475c753002d21ed99e0d53e64218e55af0cb1f`, preserving the request's base if main advances. Git confirms the 7a4be0b-to-base change set is D3a-4's 16 files. No plan checker, build, lane or test was executed.

## Round-1 disposition

- **RF-1: partly resolved.** A separate file-bound predicate and synchronized census mutation are the right correction. The production launcher exception and module reachability remain incorrect/incomplete (RF-1/RF-2 below).
- **RF-2: baseline prescription resolved.** The additional environment sites listed in r2 match the base: platform build script, crash-matrix reads, platform/operability/lifecycle/storage test sites and CLI test sites, with host/security's existing entries retained. Review by function/key/reachability before widening and the SCAN_SCOPE/CLIPPY_CRATES split address the earlier impossible unchanged-EXPECTED prescription. The shared reachability correction still applies.
- **RF-3: substantially resolved, with a validation gap.** The actual resolver, explicit gate, defined output projection, telemetry separation and cited C-11 owners address round 1. Automatic=1 needs an honest evidence/mutation state (RF-4); the per-script determinism qualification is NBO-1.
- **RF-4: substantially resolved, with one contradictory validity rule.** The API domains, positive controls, platform-specific E-TREE expectation and numeric-address exception are appropriate. The blanket differential rule still rejects the documented POSIX setsid result (RF-3).
- **NBO-1: resolved.** Frame replay is now correctly limited to frame admission; executable smoke controls separately cover plumbing, dispatch, fragmentation, EOF, resource growth and process trees. Codec conformance is not claimed.

The earlier Q1-Q5 rulings are otherwise applied: shared frame source and release-waits policy retained; D4 gates completed D5-4/G29 work; the existing tools are extended; D5-5 waits for D1b and CF-1. No earlier trial is substituted for D5-5. The seven-unit split, no-qualification limits and carried production/codec/Linux obligations remain intact.

## D5PLAN-R2-RF-1 (P2): Preserve the law's production execve site in the D1b launcher

Location: d5/PLAN-r2.md:158-163 (LD-D5-6); MD:192.

The revised predicate includes libc::execve and the exec family but permits production calls only for libc::posix_spawn in platform/process.rs. MD item 1 explicitly permits execve in section F's launcher. D5-5 waits for that production D1b launcher, so the proposed permanent rule would refuse a lawful prerequisite as soon as it lands. The only proposed exception class is test-only-feature code, which cannot represent the production launcher. This overcorrects round 1's missing owner restriction.

Required change: Separate process creation, PATH-search execution and the launcher's absolute execve rule. Keep posix_spawn file-bound to process.rs and the PATH-search family forbidden. Carry a narrowly pinned production execve site owned by D1b's accepted launcher, with no broad app/crate exemption. Add positive and negative controls proving that the lawful launcher site is admitted and the same call in an unrelated production file is refused.

## D5PLAN-R2-RF-2 (P2): Propagate test and production reachability through ordinary module declarations

Location: d5/PLAN-r2.md:159-162,164-182 (reachability); product tools/tests/test_environment_exceptions.py:109-139.

The cited M3-B analysis follows include! edges and inline cfg(test) module regions; it does not follow external mod declarations or #[path] module edges. Directory classification plus that analysis is insufficient for the promised reachability predicate. At the base, platform/lib.rs declares the external process_tests module under cfg(test), while process_tests.rs has no enclosing inline test module. Conversely a production #[path = "tests/helper.rs"] mod helper declaration can make code in a tests directory production-reachable, yet the cited include-only graph would classify it as a test target. The new shared fake source is itself planned to use #[path]. Filename exemptions would recreate the hole the plan says it avoids.

Required change: Specify the expanded graph explicitly: Cargo target roots, external mod/#[path] declarations and include! edges, with cfg(test) and exact feature gates propagated across each edge. Any production path to a file must prevent a test-only exemption, regardless of its name/directory. Validate the crash-matrix exception through its gated ancestor chain. Add controls for an external test module, a production #[path] import of a tests-directory helper, and a file reached through both test and production edges; keep the census synchronized in the forbidden-spawn mutation.

## D5PLAN-R2-RF-3 (P2): Exempt the documented POSIX setsid failure from the must-differ rule

Location: d5/PLAN-r2.md:218,223-228 (LD-D5-9); CFP:178-181.

The plan correctly recognizes that a provider's setsid fails with EPERM because it is already a session leader, not because of Seatbelt. It then universally requires every denial-required attempt to differ from the same unconfined attempt. The same provider launch/session context remains a session leader without confinement, so setsid fails with EPERM on both sides. A correct F-7 observation therefore fails the new validity rule even though MD F-7 explicitly accepts this POSIX outcome.

Required change: Make validity expectations per attempt. For the provider setsid case, require and label the same POSIX EPERM result in the confined and equivalent unconfined session-leader contexts; do not credit it as confinement enforcement. If a positive setsid sanity check is needed, use a separately labelled non-session-leader child. Preserve differential success/denial checks for operations actually intended to be blocked by the profile and add a control catching misclassification of the POSIX failure as Seatbelt denial.

## D5PLAN-R2-RF-4 (P2): Handle a lawful automatic value of 1 without claiming a concurrent mutation was caught

Location: d5/PLAN-r2.md:233-236,326 (automatic-concurrency control and mutation).

OPP's automatic resolver can lawfully return 1. The plan then runs concurrency 1 against the same value but still requires the release-when-no-other-supervision mutation to be caught at the automatic value only. With the resolver returning 1 and no overlapping supervision, the mutant and the baseline behave identically. The new resolver gate alone does not make that mutation or the cross-supervision path non-vacuous.

Required change: Define separate evidence states for zero fit, automatic=1, and automatic>1. Preserve the actual resolver value in the invariance run. Require a genuine overlapping-supervision execution for the mutation, either on a lane whose observed inputs resolve above 1 or as a separately labelled multi-supervision interaction control. If that execution is unavailable, keep it outstanding/not run and do not mark the mutation caught or the concurrency-interaction evidence complete.

## Non-blocking observation

D5PLAN-R2-NBO-1: The projection is much better than raw fact equality, but reap signal and the set of later causes are not inherently deterministic for every fault script. Existing accepted facts-then-hang controls permit either SIGTERM or SIGKILL; sampling, exit and escalation ordering can vary with scheduling. Exact stderr byte counts likewise need a script whose production is complete before teardown. Calling all these fields deterministic needs a per-script contract. At D5-4, name the scripts and synchronization that fix each compared field. For lawful operational variation, check the allowed outcome separately rather than silently normalizing it, while retaining strict equality for the requested result, admissibility/release, owner outcome and canonical candidate content. Do not discard a meaningful result change as telemetry.

## Explicit rulings

**Q6:** ACCEPT the resolver dependency and an explicit not-run row until it lands; do not invent a memory budget or claim completed overhead evidence while gated. RF-4 must additionally distinguish automatic=1 from an executed multi-supervision mutation. The coverage table must retain that outstanding evidence state.

**Q7:** ACCEPT the SCAN_SCOPE/CLIPPY_CRATES split. Keep M3-B's host/security Clippy configurations and allow-attachment rules unchanged; the widened source scan supplies policy coverage for other targets without crate-wide exemptions. The listed environment sites match the pinned base, with function/key/gate details to be recorded at D5-0. Complete the module reachability described in RF-2.

**Q8:** ACCEPT omitting the unconfined numeric-public-address connect. For the macOS CFP case, require the valid confined connect attempt to return EPERM; ENETUNREACH, timeout and generic failure are not substitutes. Record its different validity method explicitly rather than claiming a paired unconfined success. This avoids deliberate unconfined public egress; it does not itself prove no egress if the confinement being tested fails. Linux result expectations must follow its owning API/profile contract, not be inferred from the macOS probe.

## Review limits

This is plan assessment, not implemented-checker or runtime acceptance. Proposed mutation lists are future validation obligations. The self-review's charge exclusions remain appropriate for test work; its reachability, per-API validity and concurrency assertions must incorporate the findings above before being treated as complete.

Only read-only inspection, hashing, JSON parsing and Git queries were used. No Cargo, rustc, build, lane, network, other pane or delegation was used. No forbidden fixture, installation, key, held tree/entry, store, overlay or cache was read. Only REVIEW.md and review.json were written; neither repository or worktree was edited.
