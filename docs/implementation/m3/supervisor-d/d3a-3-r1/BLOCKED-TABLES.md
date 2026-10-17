# D3a-3: the four unresolved record tables (cross-law memo)

**Lead input, 2026-10-17.** LD-D3A-10 requires each of S-OP-2 item 23's code tables to be resolved by S-OP-2 itself, by a pinned protocol enum, or by a law that lists its members in full. D3a-3 looked first in the generated contracts (`crates/contracts/src/generated/`) and the native carriers (`schemas/wire/native-carriers-v1.json`, `schemas/sources/native-v2.schema.json`), then in M3-L (`provider-protocol-l`) and S-OP-2 r6. Four tables resolve nowhere. No member is invented. Each event that needs one of them is an **explicit blocker**, not registered in a reduced form, and M3-D item 21 is not claimed complete.

| Table | Blocked events (field) | Where it must be sourced | What exists now, and why it is not enough |
|---|---|---|---|
| **`StageKind`** | `provider.stage.changed` (`stage`), `provider.stage.terminal` (`stage`), `supervision.progress.absent` (`stage`). Also S-OP-2's `host.reuse.disclosed`. | **The Plan law's stage vocabulary**, as a `generated-contract` or `protocol-enum` table: the closed kinds a Plan stage may have, from the pinned plan schemas. An S-OP-2 successor, or M3-L, must name that source as the table's provenance. | The pinned Rust3 plan stage has a one-member `kind` (`fact-derivation`, `Rust3C2PlanStageV3Field0Value`), and TS2's stage request a one-member operator (`semantic-provider`). Neither is declared to be `StageKind`, and the two are not one closed table. M3-L names stages (start, analysis, teardown, M3L r1:400-402), but as span boundaries, not as a member table. |
| **`ProviderState`** | `provider.stage.changed` (`state`) | **P3T and T2O, the provider table laws** (D2b-2's pinned state tables), as a `protocol-enum`: the participant's phases, such as `START`, `READY_*`, `AWAIT_*`, `DONE` and `FAULT`. Alternatively, S-OP-2 may name a reduced closed subset in full. | The state tables exist as data for D2b-2's engine, but no law designates them, or a subset of them, as the record's `ProviderState` members, and the TS2 and Rust3 phase sets differ. |
| **`Signal`** | `provider.process.reaped` (`signal`, optional but typed). Also S-OP-2's `host.signal.received`. | **An S-OP-2 successor, or OPP §5.5 with M3-D item 19**, listing the members in full: the signals a reaped child may report on each supported platform (POSIX names, for example `SIGKILL`, `SIGTERM`, `SIGABRT` and `SIGSEGV`), and the host-received set (`SIGINT`, `SIGTERM`, …) for `host.signal.received`. | M3-D items 18 and 19 name only the two signals D3 sends (`SIGTERM`, `SIGKILL`), not those a child may die by. No pinned schema has a signal enum. `ExitClass` `signaled` already says a signal ended the child; the numeric signal is unrecorded until the table resolves. |
| **`ProviderReason`** | `provider.stage.terminal` (`reason`, optional) | **M3-L, or an S-OP-2 successor**, choosing which closed terminal reasons the record carries, each a `protocol-enum`. Candidates are the pinned `UnavailableReasonV3` (`native-v2.schema.json`), `Startup1UnavailableV3Reason` and `Startup1TypeScriptUnavailableV2Reason` (`protocol.rs`), and the budget-exhausted reasons. | The candidate enums are pinned, but they are several distinct closed sets, and no law says which, or their union, is `ProviderReason`. The table is not listed in LD-D3A-10 at all. |

**Already resolved, and therefore registered:** `StageTerminal` is a `protocol-enum` (NE:2025; `Native2StageTerminal` in `evidence.rs`). It is not registered yet only because its one event, `provider.stage.terminal`, is blocked on `StageKind` and `ProviderReason`.

**What unblocks each event.**
- `provider.process.reaped`: `Signal` alone.
- `supervision.progress.absent`: `StageKind` alone.
- `provider.stage.changed`: `StageKind` and `ProviderState`.
- `provider.stage.terminal`: `StageKind` and `ProviderReason`.

Once a table is listed by its law, its registration is ordinary (SOP2 item 3): the table, with its provenance, plus the event, plus C-2's inventory row.

## A name-only conflict, for M3-D's next revision

M3-D r5 item 21 (:690) names the settlement record `supervision.settled`. That name has two segments, and S-OP-2 item 2's grammar requires exactly three (domain, object, action); O1's `event_name_ok` refuses it at compile time. D3a-3 registers it as **`supervision.child.settled`**, with item 21's fields unchanged (LD-D3A3-11). M3-D's next revision should adopt that name.
