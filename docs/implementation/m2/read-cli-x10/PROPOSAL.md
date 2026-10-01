# Read-only CLI enablement: `opensip doctor` — proposal X10 r1

2026-09-30. Claude Opus 5.5, implementation lead. Law for unit X10 of `EXIT-PLAN.md`, under owner.md §1a, §5 and §6, and laws 464 (item 7), 468 r5 (items 6, 7 and 8), 458c r6 (items 1, 5, 7, 10 and 12) and 461 r3. Items 1, 4, 5 and 7 contain lead decisions made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each names the alternative it rejects. Not code. It enables one read-only command; it enables no creator, writer or project path.

## Problem

The product at d1b5eda has every library piece doctor needs:
- the read receipt (`produce_read_platform`, 458c-a);
- the charged observation session and `observe_installation_for_doctor` (458c-b1, b2 and c);
- the host report assembler, `DoctorReportSession` / `doctor_installation` (458c-c);
- the 468 item 6 projection, `installation_termination` (468c).

None of it is reachable from the binary. `apps/cli` is a metadata-only ingress:
- `arguments::parse` knows `help`, `version` and `completion`, and refuses everything else as `REQUEST.UNKNOWN_OPTION`;
- `MetadataHost::execute` builds only `kind: meta` or `kind: failure` envelopes;
- `opensip_reporting::render_human` renders only help, version and a failure that carries `diagnostics`.

Law 464 item 7 left CLI enablement to its own unit. 468 item 7 deferred the backup-status carrier to it, and 458c-c deferred the human label "Informational: durability not checked" to the renderer.

## Decisions

1. **What X10 enables (lead decision).** Exactly one command, `opensip doctor`, with no flags, in `--format human` and `--format json`.
   - **The command inventory row** (`command-inventory.v4.json`, `doctor`: `requestClass: lifecycle`, `authority: none`, `steps: [doctor, render]`, `flags: []`, `writesTrackedIntent: false`, `repositoryExecution: never`) is honoured as written.
   - **`--format agent`** stays the existing `OUTPUT.FORMAT_NOT_APPLICABLE` refusal, because no agent renderer exists.
   - **Doctor's only check in X10 is the installation check** (458c items 7 and 12). Doctor's other check families (provider closures, platform spawnability, trust expiry and the offline window) have no producer in the product. They contribute no entries and are not claimed. `doctor_installation`'s `other` parameter is passed empty.
   - **Every other command keeps its present refusal,** byte for byte, including `trust doctor` and `store status`. Neither has a report producer, so neither can carry the note. That covers every `query`-class surface: `query`, `baseline show`, `policy show`, `inspect`, `candidates`, `review brief` and `recommend`. Each needs runs, stores or policy owners that M2's exit units (X3–X7) have not built, so none has "full semantics today".
   - **Rejected alternative:** enabling a query surface that answers from an empty or partial store. Owner §5 forbids fabricated empty data, and `query-latest-empty` would be a false claim before any store admission exists.
2. **How doctor reaches the installation.**
   - **The call.** Doctor calls `observe_installation_for_doctor()` exactly once. That runs `produce_read_platform` (the process's one `InitialInstallationAttempt`, the actor, `InitialCore` and `InitialPlatform`; 458c item 1), then the observation session.
   - **One attempt.** No other attempt, receipt or session is made in the doctor process. A second request in the same process is impossible, because the CLI handles one invocation per process.
   - **Development builds.** A development build ends at F0 with `CORE.NO_EMBEDDED_RELEASE` before any path is opened (458c item 4). That is the real, shipped behaviour of every non-release build, and X10 does not hide it.
   - **Doctor is `Outside`** in `installation_entry` (`host/src/request.rs`). It never mints an intent, never creates, and never applies the not-initialized rule of owner §6. An absent installation reaches doctor only as the observation's `ObservedAbsent`, which 458c routes to `INSTALLATION.NOT_INITIALIZED` with no report (458c item 12).
3. **Envelope and exit mapping.** Doctor's envelope is command-envelope v7 (`Envelope7Root`), built by a new doctor ingress in host beside `MetadataHost`, under the same process-custody `RequestAuthority` for its `requestId`.
   - **Why process custody is enough.** Doctor writes nothing durable (owner §5: no barrier, no write). The durable host audit ingress belongs to the writing units (X1, X11).
   - **A produced report** (`DoctorOutcome::Report` whose termination class is success) is `kind: "doctor"`:
     - `doctor` is the `Invocation5DoctorResult` exactly as assembled;
     - `termination: {class: "success"}`, plus `domainDetail` `DOCTOR.DEFECTS_FOUND` with its registered remedy only when `defectsFound > 0`;
     - `exitCode: 0`.
   - **A report that cannot be produced** (`DoctorOutcome::Report` with operational-failed) is `kind: "doctor"`:
     - `doctor: {reportProduced: false, defectsFound: 0, defects: []}`;
     - `termination: {class: "operational-failed", errorCode: "HOST.IO_FAILURE", faultCause: "host-io", domainDetail: DOCTOR.REPORT_NOT_PRODUCIBLE}`;
     - `exitCode: 4`.

     The schema's `kind: doctor` branch allows exactly success, operational-failed and interrupted.
   - **An unreachable installation** (`DoctorOutcome::Refused(row)`) is `kind: "failure"` with no `doctor` member:
     - `termination` is the row's `InstallationTerminationV1` (class, `errorCode`, `faultCause` only on operational-failed, and `domainDetail` with the row's detail and subject);
     - `errors` is that same one detail;
     - `exitCode` is the row's exit (2 or 4).

     The schema requires a non-empty `errors` on every `kind: failure` except the two metadata-only forms. 468c's host I/O row names no domain detail, so its one `errors` entry uses the existing common4 detail code `HOST.IO_FAILURE`, and its `termination` carries no `domainDetail`. No code is added: `HOST.IO_FAILURE` is already a registered `DomainDetailCode`.
   - **Remedies.** Each `domainDetail` remedy is the registered remedy for that code where the public detail registry or a selected golden fixes one. Otherwise it is one fixed text per row, reviewed with X10's code unit. There is no new code, subject or envelope member.
   - **Exit codes** derive from the class by the fixed table (0, 2, 4), never from anywhere else. Output delivery failure keeps `deliver_required`'s existing exit 4 rule.
   - **Backup status.** The `retentionDisclosure` backup-status carrier that 468 item 7 deferred is not emitted by doctor, which neither creates nor discloses a root. It stays deferred to X11, the first unit that runs the creator from the CLI.
4. **Human rendering and JSON parity (lead decision on layout).**
   - **JSON** is `opensip_reporting::render_json` of the same `Envelope7Root`, unchanged.
   - **Human output for the `doctor` kind** is rendered from the same projection, one line per fact:
     - "Report produced: yes|no";
     - "Defects found: N";
     - one block per entry with "Detail:", optional "Subject:" and "Remedy:", in report order. The `INSTALLATION.DURABILITY_NOT_CHECKED` entry is labelled exactly "Informational: durability not checked" (owner §5) in place of "Detail:", followed by its remedy;
     - "Termination:" with the class, and "Error:" when there is an error code;
     - "Request:" with the request id.
   - **Human output for a `failure` with `errors` and no `diagnostics`** renders "Termination", "Error", each "Detail"/"Subject"/"Remedy", and "Request". The existing rule that a metadata failure requires `diagnostics` is kept only for the metadata ingress's own failures.
   - **Parity.** Every human fact is a field of the JSON envelope. The inventory row's parity fields that the product carries are compared by test between the two formats: report produced, defects found, defects, and termination class. The `outcome` and `offline-window` parity fields have no carrier in `Invocation5DoctorResult` and no producer, and are not claimed (item 1).
   - **Rejected alternative:** a free-form human summary such as "Your installation is healthy". It adds facts the envelope does not carry.
5. **Tests, and no override seam in the binary (lead decision).** Owner §1a forbids any HOME, XDG, PATH, configuration or CLI override of I. So the binary gets no seam: no environment variable, argument, feature or `cfg` that points it at another home, profile or release.
   - **End-to-end tests on scratch homes** run in-process, against a host entry point with the producers passed in. That entry point is `DoctorIngress::run_with(producers, format, …)`, built over 458c-a's `produce_on` seam and 458c-b's `observe_with`. It is `#[cfg(test)]`, or `pub(crate)` with a `#[cfg(test)]` caller, so it does not exist in a release build.
   - They use the existing scratch-home fixtures, synthetic signed V2 profiles and `installation_read_fixture`, and assert the full rendered bytes and exit code for:
     - a complete installation, with the note;
     - one other defect plus the note;
     - an incomplete installation, with one entry per finding;
     - 255 entries plus the note, versus 256;
     - the partial 256 versus 257 bounds;
     - each unreachable row: account, missing H, omitted ACL without a premise, busy, budget and not initialized.
   - **Binary tests** run the real built `opensip doctor`, in both formats. They assert exactly the shipped behaviour of a development build: `CORE.NO_EMBEDDED_RELEASE`, exit 2, a schema-valid `kind: failure` envelope, and that `~/Library/Application Support/OpenSIP` is untouched. That exercises argument parsing, the ingress, the projection, both renderers and delivery end to end, with no override.
   - **Pin.** A source check over `apps/cli` and the host doctor ingress's non-test text forbids `std::env::var`, `var_os`, `home_dir` and any `cfg(feature` that selects a home, profile or release. A test asserts that `run_with` is unreachable from `bootstrap::run`.
   - **Rejected alternative:** a test-only environment variable read by the binary. It would be a production override behind a convention, which owner §1a forbids.
6. **Help and completion.** The compiled command catalogue in `outcomes.rs` gains one row, `doctor` (`opensip doctor [--format human|json]`, "Report the health of this account's OpenSIP installation."), so `help`, `help doctor` and `completion` list it. Help text describes only what X10 implements.
7. **Envelope schema validation (lead decision).** Every doctor envelope produced in tests is validated against the selected command-envelope v7 source schema, as the metadata ingress's tests already do. It is never validated by checking only that it deserializes into `Envelope7Root`. Rejected alternative: trusting the generated types alone. Their `serde_json::Value` members (for example `Invocation5DoctorResult.kind`) do not enforce the schema's constants.
8. **Units after the law.**
   - **X10a (code):**
     - the doctor ingress and its `run_with` test seam;
     - argument parsing for `doctor`;
     - the envelope projection of item 3;
     - human rendering for `kind: doctor` and for detailed failures;
     - the catalogue row;
     - the tests and pins of items 5 and 7;
     - an inventory successor for the new files.
   - **X10b (contract successor), only if needed:** an X10 golden for doctor's report and refusal, if the selected command inventory's two doctor goldens (`doctor-defects-found`, `doctor-report-not-producible`) need text overrides to match item 3. The `doctor-report-not-producible` remedy "check permissions on the private store root" names a cause that X10's report-production failure (an over-bound or unrenderable report) does not have.

## Forbidden substitutes

- A HOME, XDG, PATH, environment, argument, feature or `cfg` override of the installation, profile or release in the binary.
- A second attempt, receipt or session in one doctor process.
- Doctor minting an intent, creating, barriering or writing.
- A fabricated empty or "healthy" report when the installation is unreachable.
- Truncating defects, or counting the note.
- The note on any command but `doctor`.
- A new public code, subject, envelope member or defect classification.
- Enabling any other command.
- A human fact with no JSON field.

## Not claimed

- Any command other than `doctor`.
- Doctor's provider, platform, trust or offline-window checks.
- The `agent` format.
- The backup-status `retentionDisclosure` (X11).
- Creator enablement (X11).
- Signed releases.
- A measured macOS 27 row. Until the owner supplies signing keys, every real run of `opensip doctor` on a development build ends at `CORE.NO_EMBEDDED_RELEASE`, and a release build on this BASELINE-ATTESTED host refuses at `/`.
