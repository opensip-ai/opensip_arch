# D3a-3 r2: discard, admission gating, records and the outcome route (M3-D r5 items 20 to 22; D3a plan r4, sub-unit D3a-3)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 2.**

## Round 2

Round 1 (`codex-d3a-3-r1`, subject `a6e9a3c5…`) returned REQUIRED-FINDINGS: D3A3-R1-RF-1 and RF-2, with no non-blocking observation. It accepted the rest: the gate, the registrations and their provenance, the four blockers (item 21 rightly not claimed complete), and `supervision.child.settled` for item 21's two-segment name (LD-D3A3-11). It also judged treating the base's 12 handshake-deadline failures as isolation-flaky reasonable for the comparison, while noting that this is not proof that the base parallel suite passes and that the timing margin remains a D5 concern. Both findings are fixed as directed:

| Finding | Change |
| --- | --- |
| **RF-1** (tool facts needing provider identities) | A tool has only a Project (item 21, :692): no Plan, Execution, provider role or universe. Its supervision records are now **six Project-only ordinary registrations** in the `tool` domain: `tool.limit.breached`, `tool.sample.incomplete`, `tool.wait.expired`, `tool.teardown.started`, `tool.scratch.retained` (the same three typed shapes) and `tool.child.settled {cause, user_interrupted}`. Each has emission on `ProjectScope`, a reader descriptor, a C-2 inventory row and a budget slot (`BUDGET_EVENTS` 23 → 29).<br>The supervision routes every fact through its class: `RecordFact::for_tool` maps each class-neutral supervision fact to its `tool.*` counterpart. A provider-only fact (spawn, readiness, stderr, faults, resources, liveness, cancel) has none, because a tool has no protocol or control plane, so none is produced. `RecordFact::requires()` names the identity set each fact's event needs.<br>**Control:** a normal tool, a timed-out tool, an output-bound tool, a sample-failing tool and a scratch-retaining tool each produce only facts whose registered event requires exactly a Project. All eight tool events are produced across them. A provider's facts each require Project, Plan and Execution. No Plan, Execution, role or universe is fabricated. |
| **RF-2** (the cancel recorded when queued) | The pending control write now carries the record its full write makes. T-1's `CancelSent` fact is attached to its frame when queued, and made exactly once when the last byte is written. It is kept across short writes and `WouldBlock`, and dropped unrecorded when the write fails (the reader gone) or the frame is abandoned at settlement. Control-session validation and sequencing are unchanged.<br>**Controls:** driving the loop by hand, there is no `CancelSent` once the cancel is queued, none after three of its bytes are written (a seam caps the bytes written), and exactly one once the rest is written. A child whose control reader closes (`close-control`) has its cancel's write fail, and no `CancelSent` is recorded. |

**Mutations added (4):** the tool's facts unmapped; a tool's settlement as the provider record; the cancel recorded when queued; the cancel recorded despite a failed write. Round 1's fifteen still apply.

**Carried obligations** (`carried-obligations.json`): the lead proposes an owner for each obligation this unit leaves open, for the coordinator to confirm at assent:
- the four blocked tables (S-OP-2 successors, with M3-C, D2b, OPP §5.5 and M3-L as sources);
- the `supervision.child.settled` name (M3-D's next revision);
- the records' emission over the real emitter (J2b);
- `supervision.cancel.forced` and `supervision.tree.swept`'s producers (D3b);
- the codec re-run and the tests' 2 s handshake margin (D5).


It implements sub-unit D3a-3 of the D3a plan r4 (`../d3a/PLAN-r4.md`, accepted by Codex `codex-d3a-plan-r4` with the LD-D3A-17 amendment):
- **item 20's gate and discard**, through the one-shot `TerminalOutput`;
- **item 21's records:** the registry registrations, each event complete or an explicit blocker (LD-D3A-10);
- **item 22's outcome join**, as a route name (LD-D3A-11).

It also carries the two observations later rounds gave D3a-3:
- D3a-1's **D3A1-R2-NBO-1**: the liveness fault's reduced provenance;
- D3a-2's **D3A2-R1-NBO-1**: sampling failures distinguished from a member that exited.

- **Library only:** no production caller. J2b composes the supervision with D4. It holds the minted scope, universe and pid mint, and emits the records (LD-D3A3-1).
- **Base:** product main `5de9fd4` (inventory v226). Round 1's base was `f05c5d5`. Since then inventory v225 (`50f1ac1`), C2a-2 (security fixtures, `1749259`) and inventory v226 have landed, and none touches a D3a-3 path. Round 2 was built on `50f1ac1`, and the worktree was moved forward with its files unchanged before the lane of record.
- **Item 21 is not claimed complete.** Four S-OP-2 events are explicit blockers: their tables resolve in no pinned source (`BLOCKED-TABLES.md`, the cross-law memo).

## What it changes

| File | Change |
| --- | --- |
| `crates/operability/src/kinds/registry.rs` (O1's registry) | **Code tables**, each with its provenance class (SOP2 item 3):<br>• **registry-literal:** `ProviderRole` (SOP2:340), `ProtocolMajor` (:379; NE:2785), `RssUnit` (SOP2:881), `FaultSource` (SOP2:883), `ForceTrigger` (SOP2:889), `TeardownCause` (item 12's causes, :446), `BoundedWait` (item 14's waits), `LimitKind` and `LimitUnit` (item 16), `ExitClass` (:440), `ScratchRetainedReason` (`io-failure`, `work-exhausted`, `root-unreaped`; LD-D3A-17 and LD-D3A-18), `LivenessMiss` (D3a-3's), and `RustDetailCode` (an empty K3 table, SOP2:844);<br>• **protocol-enum:** `RefusalFamily` (CC's RF-1 to RF-8), `ControlCancelReason` (CC:37) and `RustFaultKind` (RPP:445).<br>**Twenty-three events** (seventeen in round 1, six more in round 2). Twelve are S-OP-2 item 23's: `provider.process.spawned`, `.process.ready`, `.stderr.reduced`, `.fault.reduced`, `.resources.reported`; `supervision.liveness.missed`, `.limit.breached`, `.cancel.sent`, `.cancel.forced`, `.wait.expired`. Item 21's ordinary registrations: `supervision.teardown.started`, `.tree.swept`, `.scratch.retained`, `.child.settled` (LD-D3A3-11), `tool.process.spawned` and `tool.process.reaped`. D3a-3's own: `supervision.sample.incomplete`, and (r2, RF-1) a tool's six Project-only supervision records: `tool.limit.breached`, `tool.sample.incomplete`, `tool.wait.expired`, `tool.teardown.started`, `tool.scratch.retained` and `tool.child.settled`. Each has S-OP-2's exact fields, kinds, classes and optionality, with `role` and `universe` first on every `provider.*` and `supervision.*` event.<br>A new `supervision_event!` macro, used for the D3a-3 events only, adds optional and asserted fields (SOP2 item 4: `asserted`), and a crate-private constructor where only typed builders may make a value. `supervision.scratch.retained` has exactly three builders (`io_failure(errno)`, `work_exhausted()`, `root_unreaped()`), so an errno is present exactly for `io-failure`. `supervision.liveness.missed` has two: `window_expired` and `nonce_mismatch(family)`.<br>**The `tool` domain** and **`IdentitySet::Project`**: ordinary registrations (SOP2 item 3) for item 21's tool events (:692). |
| `crates/operability/src/emit.rs`, `transport.rs` | `EmitOn<PlanAttemptScope>` for each provider and supervision event, the only scope with exactly Project, Plan and Execution. `EmitOn<ProjectScope>` for the tool events. Each event has its own per-name budget slot; `BUDGET_EVENTS` grows from 6 to 29. |
| `crates/operability/src/readback.rs` | Item 13a's reader descriptors for the twenty-three events, built from the registry's own keys, classes, bounds and privacy, with each field's reader kind beside it (a new generic `FieldKind::Code(table)` for K1). `IdentitySet::Project` requires the header's Project. |
| `crates/operability/src/lib.rs` | Re-exports the new tables, events and `Universe` (K9). |
| `crates/operability/src/kinds/registry_tests.rs` | The tables with their provenance in both references; the events in both renderings; **C-2 extended** (below); the typed shapes of `scratch.retained` and `liveness.missed`; the asserted and Project-only renderings. O1's test asserting `tool.process.spawned` invalid now asserts it valid, and `tools.process.spawned` invalid. |
| `crates/operability/registry-events.json`, `registry-events.md` | Regenerated, checked by O1's drift test. |
| `crates/components/src/supervisor_records.rs` (new) | **`RecordFact`** (LD-D3A3-1): one mint-free value per event. Each carries every field except the minted `role`, `universe` and `pid`, as host-held counts, lengths, durations and closed codes. `event()` names the event; `supplies()` lists the fields it carries. The mapping functions from the supervisor's types to the registry's tables, one `match` each, with no conversion trait. **`OwnerRoute`** and its functions (LD-D3A-11): `settlement_route`, `cause_route`, `run_error_route` and `supervisor_error_route`. |
| `crates/components/src/supervisor.rs` | **Item 20:**<br>• `TerminalOutput` now holds the `Spool` (the admitted candidates, not `Clone`);<br>• `Settlement::release()` is the gate: the output, once, only from an admissible settlement, and dropped otherwise. It replaces round 1's `take_output`;<br>• at settlement, a settlement that is not admissible calls the new `Participant::discard()`, so the participant drops every candidate it still spools.<br>**Records:**<br>• `Supervision::record_facts(FactSink)`, the caller's sink, receives each fact as it happens, the unwind's included;<br>• `append` maps `WaitExpired` (with the wait's configured bound), `TeardownStarted` and `LivenessMissed` (with the window and provenance) to their facts;<br>• `breached(kind, observed)` records each bound with its observed value and unit;<br>• the spawn, the `fault` and `refusal` frames (detail reduced to its length), `resourceReport` (asserted), the cancel as written, and the settlement's stderr count, retained scratch, tool reap and settled record.<br>**Spans (M3-L r1:400):** `ParticipantStep.boundaries`, with `Boundary {TransferStarted, TransferEnded, ContextVerified}`. `provider.process.ready`'s `start` (spawn to the context's verification) and `transfer` sub-span come from these.<br>**D3A2-R1-NBO-1:** the sampler classifies each member's `resident_bytes` failure. `ESRCH` is a member that exited, and is lawful. Any other failure, or a failed group listing, is disclosed as `SampleIncomplete` (an event and a fact), recorded once per change of shape, and never reported as a complete sum. A partial sum over the ceiling is still a breach: it is a lower bound.<br>**Route:** `Settlement::route()`, and `is_tool()`. Test seams: `listing_fails`, `sample_errno`, `removal_errno` and the facts. |
| `crates/components/src/supervisor_tests.rs` | D3a-3's controls (below). The fixture participant spools each `FactBatch`, reports the span boundaries, discards, and can refuse a terminal whose commitment fails. |
| `crates/components/tests/supervisor_fixture.rs` | Scripts: `facts-then-fault`, `facts-then-exit` and `facts-then-hang` (two `FactBatch` frames, then a protocol fault, an early exit, or the deadline); and `canary`, a canary written to stderr and as a control `fault` detail. |
| `tools/operability/exceptions.json` | The mint audit's rows for `crates/operability/src/kinds/registry.rs`, a mint-owner file, re-censused by `check_operability.py`'s own `mint_inventory`. They gain the five new builder definitions (`io_failure`, `work_exhausted`, `root_unreaped`, `window_expired`, `nonce_mismatch`), one each more of `new`, `project_fields`, `project_fields_human` and `projected_truncated`, and one more `usize::from(` call (the macro's truncation count, as `event!`'s). There is no mint call outside operability, and no new mint authority. |
| `crates/components/Cargo.toml`, `Cargo.lock` | The `opensip-operability` edge, normal: the O1-a package policy's `dependencyAdditions` row (components to operability). |

## Lead decisions

- **LD-D3A3-1. Records are built in two halves** (the coordinator agreed, 2026-10-17). Every provider and supervision event's field set needs three minted values: the `PlanAttemptScope`, the universe's K9 digest and the K11 process id. Only the host's `CapabilitySet` holds their mints, components has no lawful one, and there is no test constructor for an attempt scope.
  - **D3a-3 in operability:** registers every event and table, adds the emission (`EmitOn`) on the right scope, and tests emission with operability's own mints.
  - **D3a-3 in components:** each event's host-held values as a mint-free `RecordFact`, through a public sink.
  - **J2b:** holds the minted scope, universe and pid mint, builds each registry event and emits it.

  This matches the plan's "J2b composes" and adds no mint call outside operability. Its completeness is a components control: each fact's `event()` is a registered name, and its `supplies()` plus the minted keys equal that event's fields.
- **LD-D3A3-2. Four events blocked (LD-D3A-10).** The coordinator agreed. `StageKind`, `ProviderState`, `Signal` and `ProviderReason` resolve in no generated contract, carrier or law, so four events are not registered in any reduced form:
  - `provider.stage.changed`;
  - `provider.stage.terminal`;
  - `provider.process.reaped`;
  - `supervision.progress.absent`.

  `BLOCKED-TABLES.md` records where each table must be sourced. Item 21 is not claimed complete. `StageTerminal` resolves (`Native2StageTerminal`) but is not registered, because its only event is blocked.
- **LD-D3A3-3. The `tool` domain and `IdentitySet::Project`** are ordinary registrations (SOP2 item 3 lists "a domain"), for item 21's tool events. O1's assertion is updated.
- **LD-D3A3-4. The tool events' fields** are D3a-3's ordinary registration, since item 21 names none (r2: with the six `tool.*` supervision records of RF-1, each a provider supervision record's fields without `role` and `universe`, and `tool.child.settled` without `admissible`, since a tool is never admissible):
  - `tool.process.spawned {pid}`;
  - `tool.process.reaped {pid, exit_class, max_rss_native, rss_unit, max_rss_bytes?, cpu}`. It has no `signal` until a `Signal` table resolves; `exit_class` `signaled` says that a signal ended the child.
- **LD-D3A3-5. The liveness provenance (D3A1-R2-NBO-1).** `supervision.liveness.missed` gains two ordinary fields: `miss` K1 `LivenessMiss` (`window-expired`, `nonce-mismatch`), and `refusal_family`, present exactly for a mismatch. No nonce, frame or detail text is recorded.
- **LD-D3A3-6. A breach's observed value.** `observed` is the value the breach was judged on:
  - for memory, the observed sum, or the asserted value when that is larger;
  - for the process count, the members listed;
  - for the TS2 response and the tool's output, the running totals;
  - for scratch, where the bounded walk stopped past the limit.

  When the scratch walk could not finish (its ledger exhausted, or an I/O failure), no observed value exists. The `LimitBreached` event and the `scratch-bound` cause record the breach, and no `limit.breached` record is made with an invented value.
- **LD-D3A3-7. `supervision.sample.incomplete` (D3A2-R1-NBO-1).** A new ordinary event, with `{listed, unsampled, listing_failed}`, recorded when the sample's shape changes. A persistent failure is therefore one record, not one per interval.
- **LD-D3A3-8. Spans from the participant.** `provider.process.ready`'s boundaries are admitted transitions only the participant sees (M3-L r1:400). The participant reports them on its step. When no transfer was marked, nothing was transferred, and `transfer` is zero.
- **LD-D3A3-9. The route table.** The cause routes are as follows:
  - **ProviderProtocol:** `handshake-deadline`, `control-refusal`, `provider-protocol`, `unexpected-exit`, `deadline`, `liveness`, `memory-ceiling`, `process-count`, `byte-bound(response)` and `scratch-bound` (item 22's provider-protocol row);
  - **Tool:** `byte-bound(tool-output)` and every tool settlement but an abandoned one (the tool row);
  - **ClosureBytesCorrupt:** `closure-recheck-failed`;
  - **ClosureUnspawnable:** `spawn-failed` with `ENOENT`, `EACCES` or `ENOEXEC`;
  - **HostIo:** any other spawn error, and `host-fault`;
  - **HostInvariant:** `session-spec-inconsistent`;
  - **Interrupted:** `user-cancel`;
  - **Revoked, ObserverFailStop and Abandoned:** their own rows;
  - **MemoryBudgetBelowCeiling:** zero fit.

  `userInterrupted` is checked first.
- **LD-D3A3-11. `supervision.child.settled`.** Item 21 names the settlement record `supervision.settled` (:690), which has two segments. S-OP-2 item 2's grammar requires exactly three (domain, object and action), and O1's `event_name_ok` refuses it at compile time. It is registered as `supervision.child.settled`, with item 21's fields unchanged. This is a name-only cross-law correction for M3-D's next revision.
- **LD-D3A3-10. C-2's `protocol-enum` check lives in components.** Operability's only edge is platform, so its tests cannot read the generated contracts. A components control compares each of the three protocol-enum tables with its generated enum, with an exhaustive `match` so that a new member fails to compile.

## The tests

- **Item 20's gate:**
  - an admissible settlement releases its output once, with its one spooled candidate, and nothing is discarded;
  - **D3-T22:** `facts-then-fault`, `facts-then-exit` and `facts-then-hang` each spool two candidates, discard them all, and release nothing;
  - **D3-T23:** a clean `Complete` with exit 3 is not admissible, is discarded, and releases nothing;
  - **D3-T24:** an injected removal failure (`EIO`) and removal exhaustion each leave the settlement clean, admissible and released, with the scratch retained and recorded;
  - **the bad-commitment gate (NBO-2):** a terminal whose commitment fails mints no output, faults, and releases nothing;
  - **admission requires the output:** a settlement that is clean, terminal, zero-exit and at EOF, but holds no `TerminalOutput`, is not admissible and releases nothing; with one, it is admissible and releases it.
- **Records:**
  - **a clean run's facts:** spawned (Rust3, the real pid), ready once (with `start` at least `transfer`), the stderr count, and settled `clean` and admissible last;
  - **each fact's values:**
    - the process count's observed 2 processes, and the memory breach's observed bytes;
    - the wall clock's configured bound;
    - the cancel sent with `deadline`;
    - the liveness provenance both ways;
    - the asserted 9 GiB, which is never progress;
  - **D3A2-R1-NBO-1:** an `EPERM` sample and a failed listing are each disclosed once; an `ESRCH` sample records nothing;
  - **C-4 with D3's fixture:** a canary in stderr and in a control `fault` detail reaches no fact, event or settlement, nor does its SHA-256. The fault is recorded as its length;
  - **a tool's facts:** spawned with its pid, reaped `exited`, no provider stderr record, and the Tool route.
- **C-2:**
  - **extended (operability):** each of the twenty-three descriptors (name, level, identities, export, fields, kinds, classes, optionality and assertion) equals the required field inventory, transcribed by hand from SOP2:877-890 and item 21. The four blocked names are absent from the registry source. A planted missing field, extra field, changed optionality, changed class or missing event is each caught;
  - **the protocol-enum tables (components):** each equals its generated enum;
  - **each fact's completeness (components):** as LD-D3A3-1 describes.
- **Typed shapes:**
  - `scratch.retained` has its three shapes, with the errno exactly for `io-failure`;
  - `liveness.missed` has its two provenance shapes, and its P1 `universe` is projected out at P0;
  - the references render `asserted` and `requires: project`.
- **Routes:** every cause has one route; no host-observed cause takes the provider-protocol route; `userInterrupted` comes first; and the pre-spawn, zero-fit and unspawnable routes are each checked.

## Checks (round 2)

Lane r2, `evidence/d3a3-r2-checks/` (the lane of record), on main `5de9fd4`, passed every check (`allPassed`):
- **the suites** at base (main's checkout) and candidate, with equal failure sets after isolated reruns:
  - **components:** the candidate has 0 failures and 127 passing, with 17 new tests (round 1's 14 and round 2's 3).
    - The base run, under the lane's parallel load, again had isolation-flaky failures: 9 of the same D3a-1 and D3a-2 supervisor tests, which missed the tests' 2 s handshake (`HandshakeDeadline`).
    - Each passed 6 of 6 times in isolation, 3 at each checkout.
    - Round 1's review accepted this treatment for the comparison, and the margin is D5's (`carried-obligations.json`);
  - **operability:** 0 failures each side, 95 → 99. The six new events are checked by the extended C-2 and the drift test, not by new tests;
- **rustfmt, Clippy (warning-denied, components and operability) and the workspace check;**
- **the fixture record** in both checkouts;
- **the focused supervisor and registry tests;**
- **the package edges** (components to contracts, identity, operability and platform);
- **the `test-fixture` scope, the environment exceptions, the operability source census** with the re-censused mint audit (`registry.rs`'s three new builder definitions for `tool.scratch.retained`), **the census-closure check and verify_design;**
- **nineteen mutations,** each failing its focused tests: round 1's fifteen, and round 2's four (the tool's facts unmapped; a tool's settlement as the provider record; the cancel recorded when queued; the cancel recorded despite a failed write).

**History:**
- **Attempt 1** (`/tmp/opensip-implementation/d3a3-r2-checks-attempt1`, on `50f1ac1`) passed every check and caught 18 of its 19 mutations. The one not caught was the failed-write mutation: its control's early-closing control reader made the host's earlier health write fail first, so no cancel was ever queued. The control now injects `EPIPE` on the queued cancel itself (`control_write_fails`), and keeps the early-closing case as a second assertion.
- **Two later starts** stopped at their opening base assertion, before any build, as main moved to `1749259` and then to `5de9fd4`.

## Checks (round 1, history)

Lane r1, `d3a-3-r1/evidence/d3a3-r1-checks/` (round 1's lane of record), on main `f05c5d5`, passed every check (`allPassed`):
- **the suites** at base (main's checkout) and candidate, with equal failure sets after isolated reruns:
  - **components:** the candidate has 0 failures and 124 passing, with 14 new tests (D3a-3's supervisor controls).
    - The base run, under the lane's parallel load, had 12 failures. All were existing D3a-1 and D3a-2 supervisor tests whose fixture missed the tests' shortened 2 s handshake (`HandshakeDeadline`).
    - Each passed 3 of 3 times in isolation, at both the base and the candidate (`isolated-*.json`, `flakyInIsolation`), so the failure sets are equal.
    - This is a pre-existing timing margin in those tests, not a D3a-3 change; it is noted for D5's re-run with the real codecs;
  - **operability:** 0 failures each side, 95 → 99 (4 new: C-2 extended, the typed scratch and liveness shapes, and the asserted and Project-only renderings);
- **rustfmt** on the new and base-clean edited files (every edited Rust file is base-clean); warning-denied all-targets Clippy on components and operability; a workspace all-targets check;
- **the fixture record** (LD-D3A-9 r4) in both checkouts;
- **the focused tests:** the supervisor tests and the registry and read-back tests;
- **the package edges:** components to contracts, identity, operability and platform, all normal, under the O1-a package policy;
- **the `test-fixture` scope;**
- **repository checks:** the environment exceptions, the operability source census with the mint audit (the re-censused rows), the census-closure check and verify_design;
- **fifteen mutations,** each failing the focused tests of its package:
  - **the plan's D3a-3 list:**
    - a non-clean settlement keeping its candidates;
    - the gate releasing without admission;
    - a nonzero exit admitted;
    - a terminal admissible without its output;
    - a scratch-removal failure becoming a fault;
    - a host-observed cause on the provider-protocol route;
  - **the records:**
    - the interrupted row not first;
    - the liveness provenance dropped;
    - an incomplete sample hidden;
    - an exited member taken as a failure;
    - a fault detail's length dropped;
    - a breach's observed value dropped;
  - **the registry:**
    - an errno on exhaustion;
    - an inventory field made optional;
    - the asserted label dropped.

**Attempt 1** (`/tmp/opensip-implementation/d3a3-r1-checks-attempt1`, history), on main `feb7739`, passed every check row but the mutation controls. It caught 11 of its 15 mutations. Two defects in it are fixed:
- **The runner:** a stale `focused_for` override left from D3a-2's runner sent the three registry mutations to the components tests instead of the registry's.
- **A missing control:** "a terminal admissible without its output" had no test where everything but the output admits. The control `admission_requires_the_terminal_output` is added.

The worktree then moved onto `f05c5d5` (CI-1: security paths only), with its files unchanged.

## Not claimed

- **Item 21 complete:** four events are blocked (LD-D3A3-2).
- **Emission by the supervision:** J2b emits (LD-D3A3-1). C-4's sinks, C-11 and C-12's persisted read-back are S-OP-2's and J2b's controls over a real emitter; this unit runs C-4's canary over its own facts.
- **Codec conformance:** the gate and records run against the fixture participant; D5 re-runs them with D2b-3's and D2b-4's codecs.
- No Linux claim (`rss_unit` is `bytes` on macOS); no qualification.

## Inventory

One new path, `crates/components/src/supervisor_records.rs`, needs an inventory successor.
