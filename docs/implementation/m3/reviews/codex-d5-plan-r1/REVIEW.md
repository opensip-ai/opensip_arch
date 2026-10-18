# D5 plan r1 review

**Verdict: REQUIRED-FINDINGS.** Four required findings and one non-blocking observation. This is a plan review; no control, platform, confinement or qualification result is accepted by it.

## Subject and authority verification

Verified the 378-byte manifest, SHA-256 `6c234d73f395d2f905806abcb1ae8b89213a41290d01bb205177d3c200e4af99`, and its sole 26,668-byte member, PLAN-r1.md, SHA-256 `9230130437faba34bc99242aa6d4a0103aa69b24b576449a5e531f812353492f`. All eleven source hash prefixes in the opening table match. Product mechanisms cited below were checked at the pinned `7a4be0b` base with Git queries. Reviewed MD item 27/F-7/gates, the structural rows, O7, D3b/D4 responsibilities, QG/REG, OPP §10, SOP2 and the carried codec/timing obligation.

## Assessment

The seven-way split is generally coherent. D3b-1/2 gate the kill/cancellation rerun, D2b-4b gates Rust3, D4 gates the completed G29 specification, D1b plus CF-1 gate F-7, and Linux/K1c work remains separately labelled. O7 is adopted but does not complete D1b or CF-1. Partial macOS work must not imply completion of the missing Rust3, confinement or Linux controls.

The proposed coverage data is a sound direction: compare requirement lists with their pinned sources, resolve owned test names, identify cited owners and distinguish not-run rows. It maps the six QG groups, ten REG classes and OPP areas, with J/E/D4 responsibilities identified. It remains an index of controls rather than proof of their semantics; its actual tests and cited deliveries must be reviewed at D5-4. The explicit shared-fake and real-codec rerun design can discharge D3A3-D5-codecs-and-timing once implemented and run, subject to the corrections below. No implementation or qualification is established by this plan.

## D5PLAN-R1-RF-1 (P2): Specify an enforced spawn-file restriction, not only a census owner label

Location: d5/PLAN-r1.md:129-134,174-183 (LD-D5-6, D5-S1).

Adding spawn/fork patterns to check_operability.py and assigning owner platform does not establish D5-S1's exact restriction to crates/platform/src/process.rs. At the pinned product base, source_check only compares per-file class counts with exceptions.json and accepts any owner in OWNERS; it does not enforce that spawn calls belong to that one file. A call in another platform file can be re-censused and accepted as an ordinary exception row. The proposed components-only planted negative proves a count mismatch, not the law's file boundary.

Required change: Extend the existing checker with an explicit production spawn-site predicate and narrowly scoped test-only exceptions, separate from ordinary process exit/abort census rows. Require refusal outside platform/process.rs even if its census row is present. Add a planted forbidden call in another platform file and a synchronized exception-row mutation; retain allowed native spawn and legitimate fixture controls.

## D5PLAN-R1-RF-2 (P2): Account for existing lawful environment calls before widening the exact exception scan

Location: d5/PLAN-r1.md:132 (D5-S3); Q4.

The proposed expansion to every workspace crate while holding the current exceptions exactly cannot pass the pinned base. test_environment_exceptions.py compares all discovered calls and allow attributes to a host/security-only EXPECTED set. Other crates already have test/fixture calls, including crates/platform/src/process_tests.rs:81 (vars_os) and crates/operability/src/producer_tests.rs:38 (OPENSIP_O1_PRODUCER_CASE), plus other operability/platform test helpers. Its Clippy-configuration test also assumes exactly two crates. Blindly widening CRATES either rejects existing lawful tests or encourages blanket owner exemptions.

Required change: Specify a read-only baseline census over the expanded scope, retaining the existing host/security entries unchanged and explicitly reviewing additional existing sites by file/function/key and test/fixture reachability. Keep the production-owner restriction exact, adapt the two-crate configuration assumption deliberately, and require the unmodified pinned base to pass alongside planted unauthorized production reads. Do not exempt entire platform or operability crates.

## D5PLAN-R1-RF-3 (P2): Compare deterministic results at the specified automatic concurrency

Location: d5/PLAN-r1.md:211 (D5-4 overhead control); MD:906; OPP:437; SOP2 C-11.

The plan substitutes identical facts at concurrency 1 and several concurrent supervisions for the source requirement. Several need not be the automatic value required by MD item 27 and OPP. Raw RecordFacts cannot be identical across real launches: they contain process ids, measured durations, CPU/RSS and schedule-dependent absence/sample observations. SOP2 C-11 explicitly compares deterministic results, excluding counters and timestamps. As written, this control either fails lawful runs or needs an unstated normalization that could hide a real result change.

Required change: Name the automatic-concurrency source and run at concurrency 1 and that actual value. Define the deterministic comparison projection (settlement/owner outcome, candidate release or discard and canonical result content as applicable), list telemetry excluded from equality, and check measured telemetry separately. Assign logging off/on and sink-level invariance to an explicit cited owner if emission remains outside D5. Add a mutation that changes a deterministic outcome only in the concurrent run.

## D5PLAN-R1-RF-4 (P2): Define per-API escape outcomes and preserve the non-denial F-7 expectations

Location: d5/PLAN-r1.md:151-154,218-226,251 (LD-D5-9 and D5-5).

The blanket call-name/errno record and only-denial-passes rule is insufficient for F-7. CFP records getaddrinfo returning EAI_NONAME and bootstrap_look_up returning BOOTSTRAP_NOT_PRIVILEGED: these use their own return-code domains, not necessarily errno. Errno alone cannot identify those results. F-7 also requires successful own-environment observation and writes inside scratch, and treats macOS E-TREE escape as its stated expected limit; those are not denial outcomes. Applying the self-review's generic rule to each attempt would reject required positive/residual observations or record misleading denial evidence.

Required change: Specify per-attempt result records with the actual return value/status domain, and errno only where that API defines it. Retain cleared per-call errno for errno APIs; distinguish getaddrinfo and Mach/bootstrap statuses explicitly. Separate denial-required operations, required positive controls and the platform-specific E-TREE outcome, preserving MD F-7 exactly. Require unconfined/fixture-validity controls where a generic error such as EAI_NONAME could otherwise be mistaken for confinement denial. Keep wrong-reason failures, missing execution and the DISCLOSURE-ONLY outcome rule.

## Non-blocking observation

D5PLAN-R1-NBO-1: Replaying shared script frames through the receiver establishes frame/schema/state expectations, but cannot rule out defects in the executable fake's fd plumbing, argv dispatch, fragmentation, EOF timing, resource growth or process-tree behavior. It is a useful check and shared lawful frames are appropriate for integration testing, but the statement that a later supervision failure cannot be a fake defect is too strong. State the replay's coverage precisely; supplement it with isolated executable smoke controls for the process behaviors used by each script, without claiming independent codec conformance.

## Explicit rulings

**Q1:** ACCEPT the shared first-party frame source for supervision/codec integration, with conformance remaining D2b's. Receiver replay validates the corpus, not all executable fake behavior; see NBO-1.

**Q2:** ACCEPT the release-waits policy with shortening confined to explicitly named expiry controls. It addresses the carried handshake-margin obligation without inventing a replacement production constant. Keep full-suite gates and three parallel candidate failure-set records; neither serial reruns nor the structural equality check alone proves adequate margin. Account for all retained release waits and escalation/cleanup budgets in outer test caps.

**Q3:** ACCEPT the dependency split: early structural/fake/codec controls can precede D4 because they do not exercise a D4 path. D5-4 and final D5/G29 coverage must wait for all D4 sub-units and cite their actual accepted controls. This does not relax D3b gates for D5-3 or the Rust3 participant gate.

**Q4:** ACCEPT extending the existing owner check in principle, but REQUIRED-FINDINGS on the unchanged-exception implementation prescription: RF-2 must resolve the expanded baseline and configuration assumptions. Preserve M3-B's existing exact exceptions and deny unauthorized production reads; no separate competing checker is needed.

**Q5:** WAIT for CF-1 acceptance and D1b integration for D5-5. MD:1250 is an explicit gate; O7 makes section F binding but its record does not mark CF-1 or D1b complete. Earlier CF-P/CF-1 trials, if separately authorized under their own scope, are not accepted D5-5 evidence and cannot waive this gate.

## Self-review, mutations and limits

No new production ledger work is proposed, so the charge/bound exclusions are appropriate. The pinned-source mutations and runtime-only mutation rule are useful. The claimed coverage of checklist items 3 and 4 needs the API-specific escape results and actual structural-policy predicates described above. D5-4 also needs the deterministic concurrency control rather than raw telemetry equality. Proposed mutation lists are requirements for future lanes, not evidence that those mutants have already been caught.

The privacy/sink and public-golden ownership split is reasonable if the G21 table retains those obligations as cited work; fact-level checks alone do not finish sink-level C-4 or C-11. Test-only fakes must remain first-party binaries, use synthetic inputs/canaries, preserve the no-repository-byte rule and never turn an unrun platform row into a pass. CF-1's outcome matrix continues to govern F-7 failures.

Only read-only inspection, hashing, JSON parsing and Git queries were used. No Cargo, rustc, build, lane, network, other pane or delegation was used. No forbidden fixture, installation, key, held tree/entry, store, overlay or cache was read. Only REVIEW.md and review.json were written; neither repository or worktree was edited.
