# CLI enablement of the creator commands: the M2 scope — proposal X11 r1

2026-10-04. Claude Opus 5.5, implementation lead. Law for unit X11 of `EXIT-PLAN.md`, under owner.md §1a, §5 and §6, and the accepted laws 464 r2 (items 3, 4, 5 and 7), 468 r5 (items 1, 6, 7 and 8), 458c r6 (item 10), X10 r4 (items 1, 3 and 5), X1 r1 (item 7), X2 r8 (item 6), X3a r5 (item 2), X4B r5 (items 1 and 11), X5 r3, X7 r5 and X12 r3 (items 4 and 8). Items 1, 3 and 6 contain lead decisions made under the owner's standing direction of 2026-09-30 to proceed on the lead's recommendation; each names the alternative it rejects. Not code. It answers the question EXIT-PLAN's X11 row leaves to this law: whether the partial creator behavior ships before M3. It does not. No command is enabled.

## Problem

EXIT-PLAN's X11 row reads: "Wire `opensip`, `analyze`, `fit` and `audit` through the creator, the 468 gate and the `RetentionDisclosure` backup-status field (a contract successor for 468 item 7)." Its note adds: "These are analysis commands. Until M3 they can only create or admit the installation and then end on the existing not-implemented refusal; the X11 law must say whether that partial behavior ships before M3."

At product bccb6b4:
- **The binary.** `apps/cli/src/arguments.rs` maps no words to the metadata rejection "Default analysis is not implemented in this development build. Use opensip help.", and `analyze`, `fit` and `audit` to "Unknown command or arguments. Use opensip help.". Any creator flag (`--allow-backup-custody`, `--ephemeral`, `--project`, `--workspace-root`, `--trust-group`, `--trust-project-owner`, `--baseline`) is "Unknown command option. Use opensip help.". Each is `kind: failure`, `termination {request-rejected, REQUEST.UNKNOWN_OPTION}`, `errors: []`, one diagnostic, exit 2, built by `MetadataHost::execute` under process custody. The help catalogue (`host/src/outcomes.rs`) lists `completion`, `doctor`, `help` and `version` only.
- **The creator.** `security::custody::installation_routing::run_initial_creator` (468c) is `pub(crate)`. It runs the attempt, actor, `InitialCore` (F0), `InitialPlatform`, the intent with its stderr disclosure (464 item 3), the creator, then the 468 gate. No host or CLI code reaches it.
- **Policy-pack admission.** `host/src/configuration.rs` (X12b) has `admit_policy_selection`, with no caller. The release pack registry has zero rows (X12 r3 item 4), so every named pack is refused in M2.
- **No analysis producer exists before M3** (X5 r3 "Not claimed": "any analysis producer of candidate Runs (M3)"; X12 r3 item 9: "Until M3 no analysis producer exists").
- **The carry-ins** EXIT-PLAN assigns here are 464 item 7 (CLI enablement), 468 item 7 (the `RetentionDisclosure` backup-status carrier) and 458c r6 item 10 (the doctor human label).

## Decisions

1. **No creator command goes live in M2 (lead decision).** `opensip`, `analyze`, `fit` and `audit` keep their present refusals byte for byte until the M3 unit that wires the analysis producer. The partial behavior ("create or admit the installation, then end on the not-implemented refusal") does not ship. There are four reasons, each sufficient on its own:
   - **a. Pack admission comes first, and in M2 it cannot pass.** X12 r3 item 8 runs `admit_policy_selection` first in an analysis request, "before X1 write admission, X2 project admission or any fence". The creator takes the installation fence and the 468 gate, so it runs after pack admission. In M2 no source can form a selection: the configuration resolver is M3 (X12 item 1), and the release registry has zero rows (X12 item 4). A lawful M2 analysis request would therefore end at pack admission and never reach the creator. Creating I first would break item 8's order.
   - **b. A durable record of an analysis that cannot run.** The creator writes P0, whose `OperationInputV1.invocation` records the command and StepId 0 as "the initialization prelude of the command's first step" (464 item 5). Without an analysis producer that step never runs. Shipping creation would make I durably record the start of an analysis M2 cannot perform, and the stderr disclosure "first use creates the installation" would announce first use of a command that then refuses.
   - **c. The creator invocation can do nothing further with I.** After the route, the invocation gets no store (X3a r5 item 2), no trust bootstrap (X4B r5 item 1: acceptance runs only at an ordinary writer's fenced first read), and no second entry (X1 r1 item 7). In M2 the only result of shipping it would be an `Unbootstrapped` installation that no command uses.
   - **d. Nothing observable would be gained.** Every M2 build is a development build and ends at InitialCore F0 (`CORE.NO_EMBEDDED_RELEASE`). A release build on this BASELINE-ATTESTED host refuses at `/` (X10 r4, "Not claimed"). The creator path is already proven on scratch homes by 459–468's library tests.

   **Rejected:**
   - **The partial behavior** (create, gate, then the not-implemented refusal). It breaks item a's order and writes item b's false record.
   - **Wiring the commands to pack admission alone,** so that every analysis request ends on X12's row 1 (`CONFIG.INVALID`, subject `count:0`). The request selected nothing, because no resolver exists to select, and no flag exists to name a pack. X12-0's remedy ("name exactly one bundled policy pack id") would point the user at something they cannot do. It would also change the public outcome of four commands for no capability.
   - **A creator-only command**, for example an `opensip` that only creates I, or `install` creating. 464's eligibility set is closed to these four analysis commands, and `install` is `Outside` (`host::installation_entry`). Widening the set is forbidden by 464.
   - **Rewording the refusals now,** for example giving `analyze`, `fit` and `audit` the default's "not implemented" text. That is public text churn with no behavior behind it. The M3 unit replaces all four refusals at once.

2. **What each command does in M2, end to end.** The parser refuses before `MetadataHost` builds anything but the metadata envelope. No attempt, account observation, core, platform, intent, disclosure, gate, pack admission or file access occurs. The envelope is command-envelope v7's empty-errors diagnostic branch, unchanged.

   | Input (any order of `--format human\|json` and `--client-correlation-id`) | Diagnostic | Envelope | Exit |
   |---|---|---|---|
   | `opensip` (no command word) | "Default analysis is not implemented in this development build. Use opensip help." | `kind: failure`, `termination {request-rejected, REQUEST.UNKNOWN_OPTION}`, `errors: []` | 2 |
   | `opensip analyze`, `opensip fit`, `opensip audit` (with or without further words) | "Unknown command or arguments. Use opensip help." | the same | 2 |
   | any of them with a creator flag: `--allow-backup-custody`, `--ephemeral`, `--project`, `--workspace-root`, `--trust-group`, `--trust-project-owner`, `--baseline`, `--audit-profile`, `--closure-bundle`, `--accept-origin` | "Unknown command option. Use opensip help." | the same | 2 |
   | any of them with `--format agent`, `html` or `sarif` | "The selected format is not applicable to this command." | the same, with `errors: [OUTPUT.FORMAT_NOT_APPLICABLE]` | 2 |
   | `opensip help analyze` (or `fit`, `audit`, `default`) | "Unknown or unimplemented help topic." | the same | 2 |

   A row's diagnostic is exactly what bccb6b4 emits; where several parser failures compete, the existing last-failure-wins rule stands, and X11a's tests pin the resulting bytes rather than restating that rule. Human output is the existing failure renderer's "Termination", "Error", "Request" and diagnostic lines. Standard error is empty, because no disclosure runs. `help` and `completion` keep the four-row catalogue.

   **Every build behaves the same way**, because the refusal precedes every producer:
   - a development build (no embedded release) never reaches F0. `CORE.NO_EMBEDDED_RELEASE` is not emitted by these commands in M2;
   - on this BASELINE-ATTESTED host, `/` is never opened;
   - a release build, if the owner's keys arrive before M3, behaves the same. **Stated limit:** its default refusal would still say "in this development build". That text is replaced in M3 with the rest, and no release build exists in M2.

3. **Contract successors: none in M2 (lead decision).**
   - **The backup-status field.** The `RetentionDisclosure` backup-status carrier (468 item 7) is deferred to the M3 unit that first emits a `retentionDisclosure`. 468 item 7 deferred it "because no envelope is emitted before then", and item 1 keeps that condition true through M2. Until then 464 item 3's stderr notice stays the carrier, and in M2 it is not emitted either, because no creator runs.
   - **Recorded direction for that successor.** This direction binds the M3 successor's author; its exact shape is fixed by its own review.
     - **Shape.** One member `backupStatus` on `RetentionDisclosure` (invocation-v5 `$defs/RetentionDisclosure`, which `additionalProperties: false` closes). Its values are exactly the three `BackupClassification::disclosed` spellings: `backed-up`, `not-backed-up` and `unknown`.
     - **Presence.** It is present exactly when `firstUse` is true, and equals the classification held by this invocation's `CreationIntent`. Under 464 item 2 that is always `unknown`.
     - **Never fabricated.** It is never `not-backed-up` from a missing detector.
     - **The stderr notice stays.** It is still written and flushed before effects (464 item 3); the field adds a carrier, it does not replace the notice.
     - **The acknowledgement member** (464 item 4) joins the same successor only if a positive detector lands with it.
   - **Rejected: landing the field in M2.** No envelope would carry it, so it could not be tested end to end. It would also force a choice between two changes before any emitter exists: a new invocation and command-envelope major, which moves every current emitter (metadata, doctor and the delivery failure), or an in-place member append. Its presence rule depends on the M3 envelope that first carries it. And the 464 item 4 member would need a second successor later.
   - **Golden wording.** 468 item 8's golden text overrides already landed in contract successor 468a. No golden changes here.

4. **Carry-ins, closed or held.**
   - **458c r6 item 10, the doctor human label: closed.** X10 r4 item 4 placed it, and X10a shipped it at product 84a8bfd: `opensip_reporting::DURABILITY_NOT_CHECKED_LABEL`, "Informational: durability not checked".
   - **464 item 7, CLI enablement of the creator: held for M3** (item 5).
   - **468 item 7, the backup-status carrier: held for M3** (item 3).
   - **Other library-only paths that name X11 in their comments are not enabled by X11 in M2.** These are X6's read-only recovery route and its `store-gc` sweep step (`host/src/recovery_route.rs`, `host/src/maintenance.rs`), X7's finalization, and X3d's commit. X6 r3, X7 r5 and X3d list CLI enablement as not claimed. Each is enabled by the unit that ships its command, none before M3. Their source comments "no CLI command calls it before X11" stay true.

5. **Obligations of the M3 successor (deferred; not decided here).** The M3 unit that enables these commands needs its own law, either an X11 successor or the M3 analysis law. It inherits these constraints from accepted law, and must decide the open points:
   1. **Order** (X12 r3 item 8). Pack admission runs first and is pure. A refused pack leaves no disclosure, no attempt and no I. Then comes `installation_entry`, where `--ephemeral` on `analyze` or `fit` is `Outside` and never creates. Then the creator through 468c, then the 468 gate.
   2. **The creator's public entry.** `run_initial_creator` is `pub(crate)`. The successor decides its host-visible entry, as X10 did with `observe_installation_for_doctor()`: one call, no producer injection, and no home, profile or release selector (X10 r4 item 5). The CLI's standard error is the disclosure writer, and a failed write or flush refuses on the host I/O row (464 item 3, 468 item 6).
   3. **How the creator command ends after creation.** X3a r5 item 2 assigns this to X11: "X11 decides only how the creator command ends after creation: its termination and what it tells the user." The successor decides it together with the analysis flow, because the answer depends on how a first-use analysis reaches a store and a trust bootstrap. Four accepted rules meet here:
      - X1 item 7 allows one entry per process;
      - X3a gives the creator no store;
      - X4B allows no bootstrap in the creator invocation;
      - X2 r8 item 6 allows first registration under the creator's `AdmittedInstallation`.

      Any route, whether an amendment to X1 item 7, a second process, or an end-and-rerun termination, is the successor's to choose and review. X11 r1 does not pre-empt it.
   4. **One request identity.** The intent draws its own RequestId and ExecutionId (464 item 5), and P0 records them. The CLI's process-custody `RequestAuthority` draws another for the envelope. One invocation must expose exactly one RequestId: the successor binds the envelope's `requestId` to the intent's, or the reverse. This is part of the durable host audit ingress that X10 r4 item 3 assigns to the writing units.
   5. **Terminations.** Every creator and gate refusal ends on its 468 item 6 row through `installation_termination`, projected as X10 r4 item 3's refused branch (`kind: failure`, the row's `errors`, exit 2 or 4). Pack refusals end on X12 r3 item 7's rows.
   6. **The backup-status successor of item 3,** landing with its first emitter.
   7. **The analysis producer and the Run closure:** X12c (the DR-131 pack row), X12d (the Run-closure join) and X7's finalization of a real Run.
   8. **Binary behavior to restate:**
      - a development build ends at F0 after pack admission, before the intent, so no disclosure is written (in `run_initial_creator`, F0 precedes `mint_intent`);
      - a release build on a BASELINE-ATTESTED host refuses at `/`.

6. **Tests (lead decision on placement).** The tests below are binary and source tests of item 2. They live in a new file, `apps/cli/tests/creator_commands_tests.rs`, so that `startup_tests.rs` keeps its inventory description. They run the real built `opensip` with no override, as X10 r4 item 5's binary tests do. Rejected: appending to `startup_tests.rs`, whose inventory description ("help/version with unavailable … resources") would go stale.
   - **Refusal bytes.** For every input row of item 2, in both formats, the tests assert:
     - exit 2;
     - in JSON, validity against the selected command-envelope v7 source schema (as `doctor_tests.rs` `schema_valid` does), `kind: failure`, the exact termination, `errors` and the exact diagnostic;
     - in human, the exact rendered lines apart from the request id;
     - empty standard error;
     - a fresh, well-formed `req1_` id per run.
   - **Zero effects.** Two things are compared before and after every run:
     - the account's real `~/Library/Application Support/OpenSIP`: its existence and, when present, its (device, inode, mode, modification time). The comparison reads the account home from the test process only, as `doctor_tests.rs` does; the binary reads no HOME;
     - the run's scratch working directory, whose `.opensip/config.json` and `package.json` are deliberately invalid, as in `startup_tests.rs`. Its bytes must be unchanged.
   - **Catalogue.** `help` and `completion bash|zsh|fish` list exactly `completion`, `doctor`, `help` and `version`.
   - **Source pin.** The production text of `apps/cli/src`, `host/src/outcomes.rs`, `host/src/doctor_ingress.rs`, `host/src/request.rs` and `host/src/lib.rs` names none of the following:
     - the creator: `run_initial_creator`, `create_initial_installation`, `mint_intent`, `CreationIntent`;
     - the ordinary writer and the gate: `admit_ordinary_writer`, `produce_write_platform`, `DurableWriteGate`;
     - pack admission: `admit_policy_selection`;
     - the commit path: `finalize`, `route_recovery`.

     `apps/cli/src` also does not call `installation_entry`. In `opensip-security`, `run_initial_creator` and `admit_ordinary_writer` stay `pub(crate)`, and `lib.rs` re-exports neither. The pin reuses `doctor_tests.rs`'s `production` reader, which strips the test module and comments, and it widens X10's pin without weakening it.
   - **No test seam.** No new feature, `cfg`, environment variable or argument is added (X10 r4 item 5).

7. **Units after the law.**
   - **X11a (M2, tests only, with an inventory successor).** `apps/cli/tests/creator_commands_tests.rs` with item 6's tests. There are no production changes, so the bytes of `apps/cli/src` and `crates/*/src` are unchanged. The inventory successor adds one row for the new file. Its number is assigned when it is built, under the linear-chain rule: check `git ls-files` first, and rebuild on the current chain before review.
   - **No contract successor in M2** (item 3).
   - **M3: an X11 successor law** (item 5), then its code units and the backup-status contract successor. These depend on the M3 analysis producer, X12c and X12d, and on item 5.3's decision.

8. **EXIT-PLAN correction (record only).** The X11 row should read: "LAW X11 r1: no creator command is live in M2; unit X11a (binary and source pins, inventory successor); creator enablement, the backup-status successor and the creator-end decision move to M3 (X11 successor)." X11a is not on the M2 exit's critical path. X9 does not depend on it.

## Forbidden substitutes

- Wiring `opensip`, `analyze`, `fit` or `audit` to the creator, the 468 gate, the ordinary writer, pack admission or any producer in M2.
- Creating, admitting or bootstrapping an installation from any CLI command in M2.
- Emitting the first-use disclosure, or a `retentionDisclosure`, from any M2 command.
- A `backupStatus` of `not-backed-up` from a missing detector, now or in the successor.
- A pack selection fabricated to give an analysis request something to refuse.
- Widening 464's creator set, or making `install` or a new command create.
- Changing the bytes of the four commands' present refusals, or the catalogue, in M2.
- A HOME, environment, argument, feature or `cfg` seam in the binary or the host ingress.
- A new public code, detail, subject or envelope member.

## Not claimed

- Enabling any command. `doctor`, enabled by X10, is unchanged.
- The creator's host entry, the durable host audit ingress, one-request-identity binding and the creator-end termination (item 5, M3).
- The `RetentionDisclosure` backup-status contract successor and 464 item 4's acknowledgement member (item 3, M3).
- `--ephemeral` analysis, which needs the analysis producer (M3).
- CLI enablement of `repair recover`, `store-gc`, commit or any query surface.
- A positive backup detector.
- Signed releases and a measured macOS 27 row. Until the owner supplies keys, no build in M2 has an embedded release.
