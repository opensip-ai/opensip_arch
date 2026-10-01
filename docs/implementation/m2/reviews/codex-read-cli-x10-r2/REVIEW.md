**Verdict: REQUIRED-FINDINGS — two narrow residual findings.**

Subject: X10 r2, `docs/implementation/m2/read-cli-x10/PROPOSAL.md`, 15,055 bytes, SHA-256 `a1ee7ce72a110f33bc441c6a1f6ef6e6a8fb3efb69c0f849b4c46c117cb6fa16`. It matches the r2 request's pin. I diffed it against `PROPOSAL-r1.md`; the preserved r1 file exactly matches the previously reviewed SHA-256 `589938a555c1105989ea059dc33e4fcb669b5ae9a3966edea541a9eb7475aa60`.

Product HEAD when inspected was `fdbedf4acc7ef57fb71eed424c3b08fa2af7fe98`. Its only changed path relative to the r1 product reference `d1b5eda` is `design-lock.json`; the relevant code and schemas remain unchanged. This is a law re-review, with no Cargo command, product build, native installation access, repository edit, commit, push or delegation. Paths below are relative to `/Users/sb/code/opensip-ai/`.

**Closure assessment.**

| R1 finding | R2 result |
|---|---|
| RF-1 — nested doctor kind | Closed. Item 3 now preserves the assembled result in both report branches, explicitly including its nested kind. Item 7 requires missing/wrong-kind negative validation. |
| RF-2 — outcome parity and diagnostic rendering | Substantially fixed. Doctor reports now render the complete termination, including the previously lost report-production detail/remedy, and outcome correctly maps to termination. The separate failure rendering rule still omits fault cause; see RF-2 below. |
| RF-3 — inaccessible cross-crate test seam | The crate-boundary problem is resolved by the layered decision. Security keeps its private test producers; host uses public result values; the real binary covers native dev behavior. Two remnants in the test coverage/unit list need correction; see RF-3 below. |

**RF-2 — Apply complete termination rendering to detailed failures too.**

Location: proposal item 4, lines 62–65.

The new rule at line 60 is explicitly under human output for `kind: doctor`. The separate `kind: failure` rule at line 62 remains the r1 list: Termination, Error, each Detail/Subject/Remedy, and Request. It does not include Fault cause. But line 65 now requires complete termination parity, including fault cause, for refused outcomes as well.

This affects concrete installation refusals, not a hypothetical future branch:

| Refusal | Envelope kind | Carried fault cause |
|---|---|---|
| Busy | failure | ledger-busy |
| Host I/O | failure | host-io |
| Budget exhausted | failure | host-invariant |

The values are fixed by `opensip/crates/host/src/installation_termination.rs:106` and proposal item 3. None is carried by the errors detail's code/subject/remedy fields. Following the enumerated failure layout therefore loses a fact required by the new parity rule. The F0 dev-binary test cannot expose this because its request-rejected termination has no fault cause.

Required change: add “Fault cause” when present to the failure rule, or explicitly reuse the complete termination-rendering rule for both kinds. Keep request-rejected envelopes free of an invented fault-cause field. Require the refused-outcome parity cases to include busy, host I/O and budget, in addition to request rejection.

This is a small remaining consistency correction. The doctor report branch, the outcome carrier correction, and the separation of unimplemented offline-window facts are otherwise correct.

**RF-3 — Finish the layered test specification and remove the retired seam.**

Location: proposal item 5, lines 70–82, and item 8, line 96.

The layering itself is buildable at the interface level: security unit tests can use `installation_read_fixture` and their private producers; host can construct the public `DoctorInstallation`, `InstallationFinding` and `InstallationTermination` values using its ordinary dependency; the binary needs no override. R2 also honestly disclaims a single real-producer-through-renderer test. I accept that decision and its rejection of a new cross-crate selector bridge.

The remaining coverage assignments do not fully match those interfaces:

- Line 73 places “one other defect” in the real-producer security layer. `DoctorInstallation` has only `Complete` and `Incomplete(Vec<InstallationFinding>)` (`opensip/crates/security/src/custody/installation_doctor.rs:39`). It cannot carry the non-installation `other` defects from r1's mixed-complete case. If this phrase instead means one structural defect, name that explicitly: the expected value is Incomplete and the resulting report has no note.
- Host's complete-report capacity tests need explicitly synthetic assembler inputs. `doctor_installation(Complete, other=[])` has no actual defects; every Incomplete observation suppresses the note (`opensip/crates/host/src/doctor_report.rs:222`). Thus security results alone cannot yield an actual defect plus the note, or 255 actual defects plus the note versus 256. The existing host tests already model these as supplied DomainDetail vectors (`opensip/crates/host/src/doctor_report_tests.rs:13`). State that these vectors remain synthetic host assembler/projection tests, using the existing `other` argument or report assembler, while production keeps `other=[]`.
- Line 96 still explicitly includes “the doctor ingress and its `run_with` test seam” in X10a. That contradicts item 5's replacement of the producer-injection seam with layered tests. Remove the retired seam from the deliverables; a pure result-to-envelope test boundary does not require it.

Required change: limit native security claims to actual complete/incomplete observations and refusal rows; assign mixed-complete and complete-capacity vectors explicitly to the synthetic host layer; retain partial 256/257 coverage there; and update X10a to name the chosen layered tests. These corrections need no feature, public test bridge, new capability or binary selector.

**Checks performed.**

I loaded the 48 raw schema sources selected by the host into the repository's TypeScript schema runtime and checked the v7 entry-point closure in memory. Results:

| Representative envelope | Schema-valid |
|---|---|
| R2 unproducible report, nested kind=doctor | Yes |
| Same envelope with doctor.kind omitted | No |
| Same envelope with doctor.kind=failure | No |
| Busy refusal with ledger-busy | Yes |
| Host-I/O refusal with host-io and no termination domainDetail | Yes |
| Budget refusal with host-invariant | Yes |

These checks close RF-1 at the law/schema level. They do not exercise an implemented X10 renderer or prove native release behavior. The layered arrangement was assessed against source visibility and signatures; no compilation was performed, as requested.

The inspected production observation wrapper still binds to `produce_read_platform`, `HomeSource::Native`, `OsClock` and `SessionSeam::live` (`opensip/crates/security/src/custody/installation_doctor.rs:51`). R2's one-producer-call and no-new-bridge requirements preserve that boundary. No current scratch-home selector was found on this route; the future code unit must still verify its implementation.

**Unchanged decisions.**

The installation-only scope, all-other-command refusals, doctor-versus-failure mapping, host-I/O errors entry, fixed informational label/counting, no writes/barriers, shared help/completion catalogue, source-schema validation and X11 backup-carrier deferral remain acceptable. There is no need for a new public code or schema member.

The r1 golden-reconciliation note still applies: the existing assembler texts differ from both doctor goldens, and the not-producible golden's situation must distinguish observation refusal from report-assembly failure. Item 8 already supplies the successor mechanism; complete that selection before accepting enabled output. I am not adding a new finding for that acknowledged work. The minor “two metadata-only forms” wording at line 50 also remains: the second empty-errors exception is interrupted pre-commit failure, not a metadata-only form.
