**Verdict: REQUIRED-FINDINGS — three required findings.**

Reviewed law X10 r1, `docs/implementation/m2/read-cli-x10/PROPOSAL.md`, 12,808 bytes, SHA-256 `589938a555c1105989ea059dc33e4fcb669b5ae9a3966edea541a9eb7475aa60`. The bytes match the request's `hashes.txt`. Product reference: `d1b5edad4fc552122ca9ef7161d2a69cc30b0852`.

This is a law review. I read the requested owner/law context, the selected source schemas and command inventory, and the relevant current producer, assembler, ingress and renderer code. I ran no Cargo command, built no product, delegated no work, and made no repository edits, commits or pushes. The schema checks below ran entirely in memory. Paths prefixed `opensip/` and `opensip_arch/` are relative to `/Users/sb/code/opensip-ai/`.

**RF-1 — The unproducible-report object omits a required field.**

Location: proposal item 3, lines 39–40.

The literal `doctor: {reportProduced: false, defectsFound: 0, defects: []}` is not an `Invocation5DoctorResult`. `opensip/schemas/sources/invocation-v5.schema.json:1808` requires a nested `kind`, whose constant is `"doctor"`. The outer envelope's `kind` does not discharge that requirement. The current assembler already supplies the field in every result (`opensip/crates/host/src/doctor_report.rs:135`).

I constructed item 3's complete unproducible envelope, giving `termination.domainDetail` a valid code/remedy object, and checked it against the selected v7 source schema. It failed. Adding only `doctor.kind: "doctor"` made it pass. This isolates the missing field from the proposal's shorthand for the termination detail.

Required change: preserve the assembled `Invocation5DoctorResult` for both report branches, or explicitly include the nested kind in the failed-report object. Item 7's validation should cover this branch and a missing/wrong-kind negative case.

**RF-2 — Outcome has an existing carrier; the proposed human layout drops its diagnostic.**

Location: proposal item 4, lines 54–63.

The statement that `outcome` has no carrier or producer is incorrect. The selected reference explicitly maps `outcome` to `termination`: `opensip_arch/docs/implementation/m2/initial-root-binding-owner-selection-v1/reference/doctor_projection.py:46` and `:59`. The inventory lists `outcome` separately from `termination-class` (`opensip_arch/docs/implementation/m1/metadata-v2/command-inventory.v4.json:1129`). It is not required to be a member of `Invocation5DoctorResult`; it is already carried by the enclosing envelope.

On an unproducible report, item 4's layout would show report-produced=no, count=0, operational-failed, HOST.IO_FAILURE and the request ID. There are no defects to render, and the layout never renders `termination.domainDetail`, so the user receives neither `DOCTOR.REPORT_NOT_PRODUCIBLE` nor its remedy. JSON retains both. The layout also omits the carried fault cause, and on a produced report with actual defects it omits the `DOCTOR.DEFECTS_FOUND` termination detail/remedy. Comparing only the termination class does not establish outcome parity.

Required change: retain outcome parity and render the carried termination facts, including fault cause when present and domain-detail code, optional subject and remedy. Require tests for the complete carried outcome, especially the empty-defects/unproducible branch. The offline-window producer can remain outside X10's claimed scope; that does not justify dropping outcome.

**RF-3 — The host test seam cannot reach the proposed real-producer fixtures as specified.**

Location: proposal item 5, lines 65–75.

The existing boundaries at the pinned product are concrete:

- `produce_on` is `pub(super)` inside security (`opensip/crates/security/src/custody/read_premise.rs:125`).
- `observe_with` is likewise `pub(super)` (`opensip/crates/security/src/custody/installation_session.rs:284`).
- `installation_read_fixture` is `pub(crate)` and `cfg(all(test, target_os = "macos"))` (`opensip/crates/security/src/custody.rs:1797`).
- The signed `ReadProducers` re-export is also crate-private and test-only (`opensip/crates/security/src/trust.rs:10`); `HomeSource::Fixture` is test-only (`opensip/crates/security/src/custody/installation_admission.rs:435`).
- Host uses security as a normal dependency (`opensip/crates/host/Cargo.toml:17`). A host unit test does not compile that dependency with access to its private `cfg(test)` internals.

Consequently, adding `DoctorIngress::run_with` under host's `cfg(test)` or making it `pub(crate)` does not create the promised scratch-home composition. A mock returning `DoctorInstallation::Complete` or a vector of findings can exercise the host projection but is not a real-producer test. The “other defect” and capacity vectors also need an explicit assembler/projection injection layer: the production installation-only ingress correctly passes `other = []`.

Required change: name a buildable crate/test arrangement for the claimed composition, or explicitly amend the claim to layered native-producer tests in security, projection/rendering tests in host, and dev-binary tests. Keep the scratch-home/profile capability out of ordinary release callers; a feature-selectable public fixture bridge is not a solution under this law. Also correct the assertion that a `pub(crate)` function necessarily does not exist in release merely because its caller is `cfg(test)`; compilation exclusion and unreachability are different guarantees.

The current native wrapper is appropriately closed: `observe_installation_for_doctor` calls `produce_read_platform`, then uses `HomeSource::Native`, `OsClock` and `SessionSeam::live` (`opensip/crates/security/src/custody/installation_doctor.rs:51`). I found no scratch-home selector on that inspected production route. This is not an attestation of an X10 release binary: the new ingress does not exist yet. The source pin must cover any new bridge introduced to implement the revised test arrangement, not just environment reads in CLI/host text.

**Disposition of the requested decisions.**

| Item | Assessment |
|---|---|
| 1 — scope | Sound. Enable only doctor's installation check; keep `other` empty and every other command's refusal. Do not invent an admitted empty query domain. Keep agent refusal. The narrower scope avoids the project-admission prerequisite in 461 r3 item 9. |
| 2 — ingress | Sound. One call to the existing observer preserves the attempt/receipt/session ownership. Doctor remains outside creator ingress, and only typed observed absence becomes NOT_INITIALIZED. Earlier account/core/platform/custody/I/O refusals retain precedence. |
| 3 — envelopes | The doctor-versus-failure split and 468 mapping are sound, subject to RF-1. Host I/O gets a registered HOST.IO_FAILURE entry in `errors`, with no termination domainDetail; that shape validates. Preserve each row's subject and class/error/fault pairing. Process-only request custody and the existing delivery-failure exit rule are appropriate here. |
| 4 — rendering | The exact informational label and numeric count excluding the note are right. Rendering from the envelope is right. Outcome parity requires RF-2. |
| 5 — tests | The prohibition on a binary override and the dev-binary F0 checks are right. The proposed cross-crate scratch-home composition requires RF-3. Source-token checks supplement, rather than establish by themselves, the producer/selector boundary. |
| 6 — help/completion | Sound. Add doctor through the shared compiled catalogue and describe installation health only. `help doctor` must remain metadata-only and must not invoke the installation observer. |
| 7 — schema validation | Sound and necessary. Check actual source-schema conformance for reports and refusals; generated deserialization does not enforce a `serde_json::Value` constant. RF-1 demonstrates why the requirement matters. |
| 8 — units/goldens | Code plus contract-successor separation is reasonable. The existing remedy mismatch already triggers the proposed successor work; resolve the exact selected texts before accepting the enabled CLI output. See below. |

The complete/partial report semantics remain those of 458c r6: complete I gets exactly the fixed informational entry, it consumes one slot and contributes zero to the count; 255 actual defects plus the note fits, 256 does not; without the note, 256 fits and 257 does not. Refusal to reach I produces no doctor report. No barrier, creator, repair, or query semantics are added. Deferring the backup-status carrier to X11 is appropriate because doctor performs no creation disclosure; X11 still owes 468 item 7.

**Golden reconciliation is already needed.**

Item 8 explicitly provides the mechanism, so I am not counting this acknowledged work as a fourth finding. Its “if needed” condition is satisfied for the current assembler's texts:

| Detail | Selected v4 golden | Current assembler |
|---|---|---|
| DOCTOR.DEFECTS_FOUND | `CI must inspect doctor.defectsFound; exit 0 means the report was produced` | `inspect doctor.defects; exit 0 means the report was produced` |
| DOCTOR.REPORT_NOT_PRODUCIBLE | `check permissions on the private store root` | `Resolve the report-production failure and run doctor again.` |

Evidence: `opensip_arch/docs/implementation/m1/metadata-v2/command-inventory.v4.json:2004` and `:2013`; `opensip/crates/host/src/doctor_report.rs:36`.

The not-producible golden's situation also says the private store cannot be opened. Under 458c item 12 and X10 item 3, an observation I/O refusal is the failure/host-I/O row, while bounded report-assembly failure is doctor/REPORT_NOT_PRODUCIBLE. Reconcile that situation as well as its remedy, and preserve the inherited golden bytes through the prescribed successor. For defects-found, either use the selected golden text in the ingress or select its explicit override. Do not silently treat the assembler's two constants as registered golden remedies. This requires contract text/selection work, not a new schema field or public code.

**Lead decisions and rejected alternatives.**

- Item 1: agree with installation-only doctor and reject enabling empty/partial query surfaces; no admitted store means no honest query result.
- Item 4: agree with fact-by-fact envelope rendering and reject an unsupported “healthy” summary; amend the layout for RF-2.
- Item 5: agree with rejecting a binary environment override; amend the test arrangement for RF-3 rather than weakening that boundary.
- Item 7: agree with original-schema validation and reject reliance on generated types alone.

One minor explanatory correction: item 3 line 50 calls both empty-errors exceptions “metadata-only forms.” The second is the interrupted pre-commit failure with an owned signal and exit 130 (`opensip/schemas/sources/command-envelope-v7.schema.json:696`), not a metadata-only form. This does not change any of the proposed non-interrupted doctor rows and is not a separate required finding.

**Verification and limits.**

Using the installed Node 24.16.0 and the repository's TypeScript schema runtime, I transpiled `exact-json.ts`, `patterns.ts` and `schema.ts` in memory, loaded the 48 raw source documents named by host's embedded schema registry, checked the v7 entry-point closure, and evaluated these representative envelopes:

| Probe | Source-schema result |
|---|---|
| Item 3 unproducible result without nested kind | Invalid |
| Same envelope with nested kind=doctor | Valid |
| Host-I/O failure, HOST.IO_FAILURE in errors, no termination domainDetail | Valid |
| F0 failure, CORE.NO_EMBEDDED_RELEASE in errors and termination domainDetail | Valid |
| Complete report, count=0 and the fixed informational entry | Valid |

These probes establish shape conformance only; their placeholder refusal remedies do not select public wording or prove native behavior. No Cargo build/test, native observation, installation access, or release-binary reachability test was performed for this law review. The required changes belong in the proposal and its later implementation units, not in repository edits by this reviewer.
