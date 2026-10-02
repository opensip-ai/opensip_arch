# X11 r1

Claude Opus 5.5 leads. Grok is the single reviewer. Law review of CLI enablement for `opensip`, `analyze`, `fit`, and `audit`. No product cargo. Git was read-only. `~/Library/Application Support/OpenSIP` is absent.

Verdict: **ACCEPT**. Required findings: none.

| | |
|---|---|
| Subject | `docs/implementation/m2/cli-enablement-x11/PROPOSAL.md`, r1, 19087 bytes, sha256 `b98debc9f8823f69ec95c84f7b4045ffbbaea990e69d7cc998f08328fbbe96e4` |
| Product | `bccb6b4e2879e6dee34c2149182cbb201a00f4ad`, clean, “Settle admitted attempts in an authorized sweep, one namespace at a time (store-gc).” |
| Arch | `d3dfa1400c77befda54384aa951fe8b79c5dfc5a`, “Draft law X11 r1 (no creator command live in M2) and assign it to Grok.” Parent `14961daeb23e9abd3049718102d7a6039f74bb52` is the HEAD this request names as already present. The subject path is tracked and clean, and its bytes match `hashes.txt`. |

The law answers EXIT-PLAN’s question: the partial creator behavior stays out of M2. The four commands keep the refusals `bccb6b4` already emits. Creator enablement, the backup-status successor, and the creator-end termination are recorded for an M3 successor.

## (a) Nothing live in M2

“Nothing live” is lawful, and it is the narrowest scope that keeps every accepted constraint.

464 r2 item 7 wires no CLI command. The present refusal stays until the unit that enables the creator, and the CLI changes in that unit. 467 has since composed the creator as library code. The remaining assignment is the enabling unit. X11 r1 places that unit in M3. 464 does not set an M2 deadline.

468 r5 item 7 defers the `RetentionDisclosure` backup-status carrier to the CLI-enablement unit “because no envelope is emitted before then,” and until then the stderr notice carries it. Item 1 keeps creators off the CLI, so no `retentionDisclosure` is emitted in M2. The stated reason still holds. The assigned unit may place the field on the first emitter. Landing the member in M2, with no envelope to carry it, is the alternative item 3 rejects, and that rejection matches the reason 468 gave.

X3a r5 item 2 says any store work happens in a later ordinary-writer invocation, and “X11 decides only how the creator command ends after creation: its termination and what it tells the user.” The “only” is a scope limit: the creator invocation gets no store, because a store in the same process would amend X1 item 7, and nothing proposes that amendment. r5’s header records that this was written so X11 would not be left an impossible store task. With no command live, there is no ending to publish in M2. Item 5 records the four rules that meet there and leaves the choice to the successor that can actually reach a store and a trust bootstrap. That is the decision X3a assigned, made at the time the command can run.

X4B r5 item 11 requires X4B-a, X4B-b, and X4B-c before X11. Those units are on `bccb6b4`. The sentence sequences X4B ahead of this law. It does not require this law to enable a command. Item 1 of X4B rejects acceptance on the creator path: 468c drops `InitialCore` before the gate, and X3a gives the creator invocation no store. X4B’s not-claimed list leaves CLI enablement to X11.

X10 r4 item 1 enables `doctor` and keeps every other command’s present refusal. Item 3 assigns the durable host audit ingress to the writing units, X1 and X11. Item 4 places the doctor label. The backup-status sentence says the field “stays deferred to X11, the first unit that runs the creator from the CLI.” X11 r1 is that owner, and it records that the first run is the M3 successor. X10’s not-claimed list leaves creator enablement and the backup-status field to X11. EXIT-PLAN asks this law to say whether the partial behavior ships before M3. X12 r3 item 4 already treats analysis as unreachable before M3 because X11 ends on the existing refusal, and the release registry has zero rows.

Shipping any of the rejected alternatives would change public bytes or create an installation. Keeping the present refusals is the scope that satisfies all five laws at once.

## (b) Pack admission, then the creator

X12 r3 item 8 is read correctly. `admit_policy_selection` runs first in an analysis request, before X1 write admission, X2 project admission, or any fence, and before providers, snapshots, facts, Coverage, Plan construction, and evaluation. It does no I/O, takes no lock, and is not charged. A refusal leaves nothing to clean up.

On `bccb6b4`, `host/src/configuration.rs` defines `admit_policy_selection` as `pub(crate)` and the only production-adjacent caller is `configuration_tests.rs`. A selection whose length is not one returns `PolicySelectionRefusal::Count`, projected as `CONFIG.INVALID` with subject `count:<n>` and the X12-0 remedy, which contains “name exactly one bundled policy pack id”. `crates/evaluator/src/pack-registry.json` has `"rows": []`. X12 item 1 keeps the resolver in M3, so an M2 request has zero sources. Pack admission would refuse that request, and the creator, which takes the installation fence and the 468 gate, would run only after a pack had been admitted. Creating I first would leave an installation behind a later pack refusal. That breaks item 8.

Pack-admission-only wiring is rightly rejected. With no resolver and no pack-naming flag, every analysis request would end on row 1, subject `count:0`, and the remedy would tell the user to name a bundled pack id that M2’s empty release registry cannot admit. That replaces the present refusal. X12 itself wires no CLI command.

Each of item 1’s four reasons stands on its own. (a) is this order. (b) matches 464 item 5: P0 records the command and StepId 0 as the initialization prelude of the command’s first step, and `deliver_disclosure` writes “opensip: first use creates the installation at …”. An analysis producer is M3 (X5 r3 not-claimed; X12 item 9). (c) matches X3a’s no-store rule, X4B’s rejection of creator-path acceptance, and X1 item 7’s one entry per process. (d) matches a development build’s `InitialCore` refusal: `produce_initial_core` fails `release.admit()` with `EmbeddedRootAbsent` before `mint_intent`, and `core_refusal` maps that to `NoEmbeddedRelease`. X10’s not-claimed line is the release-build limit: on this BASELINE-ATTESTED host a release build refuses at `/`.

## (c) Backup-status successor

Deferring the field is lawful. 468 item 7’s reason is the absence of an envelope. Item 1 keeps that absence through M2. 464 item 3 remains the carrier: the stderr notice is written and flushed before effects, and the envelope’s `retentionDisclosure` has no backup-status field until a schema successor. In M2 the notice is also absent, because `mint_intent` is the writer and these commands never call it.

The recorded direction matches 464 items 2 to 4 and the current schema.

`invocation-v5` `$defs/RetentionDisclosure` is `additionalProperties: false`, with required `policy`, `provenance`, `firstUse`, and `storageRoot`. There is no `backupStatus` member today. `BackupClassification::disclosed` spells `backed-up`, `not-backed-up`, and `unknown`. `classify_backup` returns `Unknown` for every target, and the comment on it records 464 item 2: a later detector fails to `Unknown`. Presence exactly when `firstUse` is true, equal to that invocation’s `CreationIntent` classification, adds a carrier beside the stderr notice. The acknowledgement member stays with a positive detector, which is 464 item 4: with classification always unknown, no acknowledgement is required, and P0 has no such member.

Landing the field in M2 would publish a member no envelope emits, and the presence rule depends on the M3 envelope. 468 item 8’s golden text is already in successor 468a. This law changes no golden.

## (d) The M2 table

Item 2 matches `arguments.rs` and `MetadataHost::execute` at `bccb6b4`.

`parse` strips `--format human|json` and `--client-correlation-id` in any order. A later failure overwrites `failure`, which is the last-failure-wins rule item 2 leaves to X11a’s byte pin. Empty words are the default diagnostic “Default analysis is not implemented in this development build. Use opensip help.” Any other unmatched word list, including `analyze`, `fit`, and `audit` with or without further words, is “Unknown command or arguments. Use opensip help.” A dash word outside `--help`/`-h`/`--version`/`-V`/`--format`/`--client-correlation-id` is “Unknown command option. Use opensip help.” That covers every creator flag in the table, including `--audit-profile`, `--closure-bundle`, and `--accept-origin`. `--format html|sarif|agent` is the sentinel `format-not-applicable`.

`reject` sets `kind: failure`, `exitCode: 2`, `termination {class: request-rejected, errorCode: REQUEST.UNKNOWN_OPTION}`, the diagnostic, and `errors: []`. The format sentinel passes `format_detail`, so `errors` is one `DomainDetail` `{code: OUTPUT.FORMAT_NOT_APPLICABLE, remedy: Choose an applicable output format.}`. `execute` sets exit 2 when `kind` is `failure`. An unknown help topic, including `analyze`, `fit`, `audit`, and `default`, hits the empty catalogue filter and “Unknown or unimplemented help topic.” `catalogue()` is exactly `completion`, `doctor`, `help`, `version`.

The empty-errors rows are command-envelope v7’s empty-errors diagnostic branch: `errors.maxItems: 0` then requires `kind: failure`, that same termination, `exitCode: 2`, and `diagnostics` of at least one item. The format row is the same termination with a non-empty `errors` array. `OUTPUT.FORMAT_NOT_APPLICABLE` is a `DomainDetailCode`, and `DomainDetail` requires `code` and `remedy`. Human rendering writes “Termination”, “Error”, “Request”, and the diagnostic lines. When `errors` is non-empty it also writes that entry’s “Detail” and “Remedy” between “Error” and “Request”. Item 6 pins the exact human lines, so the format row’s extra lines are part of the pin.

`bootstrap::run` calls `MetadataHost::begin` before `parse`, then sends every non-doctor request to `execute`. `begin` draws 16 bytes from `request_entropy` (`getrandom`) into an in-memory `RequestAuthority` and `project` formats `req1_` plus 32 hex characters. That allocation is the metadata envelope’s request id. It is not an attempt, an account observation, InitialCore, InitialPlatform, an intent, a disclosure, the 468 gate, pack admission, or a read of the account home or the working tree. Doctor is the only branch that observes an installation, and only the macOS `doctor()` path calls it. These four commands stay on `execute`. Standard error stays empty on the refusal path. Entropy failure is the existing stderr `HOST.IO_FAILURE: request identity allocation failed.` and exit 4, which is metadata ingress, outside the creator.

The same refusal runs on every build kind because it returns before `produce_initial_core`. These commands do not emit `CORE.NO_EMBEDDED_RELEASE`, and they do not open `/`. The stated limit is accurate: the default diagnostic still contains “in this development build”, that sentence is replaced with the rest of the M3 wiring, and M2 has no release build.

## (e) M3 constraints, and the two request ids

Item 5 records accepted constraints and leaves the open choices to the successor. The citations match the laws and the tree.

Order follows X12 item 8, then `installation_entry`. In `request.rs`, `Analyze` and `Fit` with `ephemeral` return `Outside`; `Default`, `Analyze`, `Fit`, and `Audit` are `Creator`; `Install` and `Update` are `Outside`; any other command with `ephemeral` returns `EphemeralNotAccepted`. The creator then runs through `run_initial_creator` (`pub(crate)`), which is 468c, and into the gate.

The public entry is still `pub(crate)`. Modeling it on `observe_installation_for_doctor()` — one call, no producer injection, no home, profile, or release selector — is X10 r4 item 5’s shape. `deliver_disclosure` writes and flushes before effects; `IntentRefusal::Disclosure` maps to `HostIo`, which is 464 item 3 and 468 item 6.

The creator-end termination stays with the successor. The four rules are real and they meet: X1 item 7 allows one of `run_initial_creator`, `admit_ordinary_writer`, or a 458c read entry per process; X3a gives the creator no store; X4B item 1 rejects acceptance inside the creator invocation; X2 r8 item 6 allows first registration under the creator’s `AdmittedInstallation` inside the same held fence. r1 names those rules and does not give the creator a store, amend X1 item 7, or pick end-and-rerun. That is the lawful content of X3a’s assignment while the command is still dark.

The one-RequestId gap is real. 464 item 5 draws a fresh RequestId and ExecutionId by CSPRNG before I exists, and `mint_intent` does that with two `request_entropy` calls, then stores them on `CreationIntent` for P0. The CLI’s `RequestAuthority::begin` draws a different id for the envelope. One invocation has to expose one RequestId. X10 item 3 assigns the durable host audit ingress that binds them to the writing units. Leaving the bind to the successor that first writes is the right place. Item 5.8 is also true in source: inside `run_initial_creator`, `produce_initial_core` runs and returns on F0 before `mint_intent`, so a development build writes no disclosure. A release build on this BASELINE-ATTESTED host refuses at `/`, which is X10’s not-claimed sentence.

Terminations, the backup-status successor landing with its first emitter, and the analysis producer (X12c, X12d, X7 finalization of a real Run) are the same obligations the cited laws already name.

## (f) Tests and the source pin

Item 6 proves item 2 without a seam and without weakening X10 r4 item 5.

The tests run the real `opensip` with no override, in a new `apps/cli/tests/creator_commands_tests.rs`, so `startup_tests.rs` keeps its inventory description. Refusal rows require exit 2, command-envelope v7 validity through the same `schema_valid` registry call `doctor_tests.rs` uses, the exact termination, errors, and diagnostic, exact human lines apart from the request id, empty stderr, and a fresh `req1_` id. `project` yields 37 characters (`req1_` plus 32 hex), which is the shape `doctor_tests.rs` already asserts. Zero effects compare the account installation’s existence and, when present, device, inode, mode, and mtime, reading `HOME` in the test process only, as `real_installation()` does. The scratch tree’s invalid `.opensip/config.json` and `package.json` are the `startup_tests.rs` fixture, and their bytes stay. Help and `completion bash|zsh|fish` list the four catalogue names. No new feature, `cfg`, environment variable, or argument is added.

At `bccb6b4`, the production reader from `doctor_tests.rs` (cut at `#[cfg(test)]\nmod tests`, then drop lines whose trim starts with `//`) leaves none of these identifiers in `apps/cli/src`, `host/src/outcomes.rs`, `doctor_ingress.rs`, `request.rs`, or `lib.rs`: `run_initial_creator`, `create_initial_installation`, `mint_intent`, `CreationIntent`, `admit_ordinary_writer`, `produce_write_platform`, `DurableWriteGate`, `admit_policy_selection`, `finalize`, `route_recovery`. `apps/cli/src` does not name `installation_entry`. `finalize` does not occur inside `finalization`, so a substring check and an identifier check agree. `run_initial_creator` and `admit_ordinary_writer` are `pub(crate)` (`installation_routing.rs`, `ordinary_writer.rs`). `crates/security/src/lib.rs` re-exports neither. `custody.rs` keeps both modules `pub(crate)`.

The widen keeps X10’s pin on X10’s files. `doctor_tests.rs` scans `apps/cli/src`, `doctor_ingress.rs`, `outcomes.rs`, and `request.rs` for `std::env::var`, `env::var`, `var_os`, `home_dir`, `cfg(feature`, `cfg(test)`, and `cfg(debug_assertions)`, and it requires exactly one `observe_installation_for_doctor()` in the ingress. Those assertions stay. `host/src/lib.rs` is added for the new names. Its `#[cfg(test)] mod native_owner_tests` survives the production reader, because the cutter looks for `mod tests`, and that attribute gates a test module. It is outside X10’s file set. Putting `lib.rs` under the `cfg(test)` ban would fail at `bccb6b4`, and item 7 allows no production change. The pin X11a writes checks the new names on the wider set and leaves the X10 scan where it is. That widens the pin and leaves every X10 prohibition in force. `doctor_ingress.rs` still has the one producer call.

## (g) The rest

The doctor label carry-in is closed in tree. `DURABILITY_NOT_CHECKED_LABEL` is “Informational: durability not checked” in `crates/reporting/src/human_renderer.rs`, re-exported through reporting and `doctor_report.rs`. Commit `84a8bfd7b4f28a52fc18bc9e66e02d1f40330d2c` is an ancestor of `bccb6b4` and already contains that string. X10 r4 item 4 is the placement.

X6 recovery, `store-gc`, X7 finalization, and X3d commit stay unwired. `apps/cli` names none of `route_recovery`, `finalize`, or the creator. The comments “no CLI command calls it before X11” are the module gates in `host/src/lib.rs` for `recovery_route` and `maintenance`. `recovery_route.rs` says no CLI command is wired. `maintenance.rs` says its CLI is X11’s and M5’s and that no command calls it. The finalization gate says no CLI command calls it (X11). All of those sentences stay true, because this law enables no command. X6 r3, X7 r5, and X3d already list CLI enablement as not claimed.

Item 7 is tests only: X11a adds `creator_commands_tests.rs` and one inventory row, with no production change and no M2 contract successor. The M3 successor depends on the analysis producer, X12c, X12d, and item 5.3. Item 8 is a record-only EXIT-PLAN sentence. This review does not edit EXIT-PLAN. The forbidden-substitutes list and the not-claimed list match items 1 to 5. `doctor` is unchanged.

## Replay

Law review. No product cargo, no target directory, no test run. The parser, `MetadataHost::execute`, `bootstrap`, `RequestAuthority`, `installation_entry`, `run_initial_creator`, `produce_initial_core`, `mint_intent`, `BackupClassification`, the invocation-v5 and command-envelope-v7 schemas, the pack registry, and the source pin were read at `bccb6b4`. The real OpenSIP home was absent before and after. Nothing was written outside this directory.
