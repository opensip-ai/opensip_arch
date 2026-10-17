# S-OP-2c. The four record tables

**Draft r1, PROPOSED, not accepted.** 2026-10-17. Claude, implementation lead. This is a contract successor to S-OP-2 r6 (`docs/implementation/m3/operability/s-op-2/PROPOSAL-r6.md`, 130,001 bytes, sha256 `ce8d3a4b783328915f0bf550dd111f227aa9901d5efddbcd9ccc8707cd4cb11d`), which S-OP-2-R selects as an accepted base. It is raised by D3a-3's cross-law memo (`supervisor-d/d3a-3-r2/BLOCKED-TABLES.md`; LD-D3A3-2) under the D3a plan r4's LD-D3A-10 (`supervisor-d/d3a/PLAN-r4.md`:143-150). Nothing here binds the unit, and no product file changes.

## The gap

Item 23 names four K1 tables without fixing their members: `StageKind`, `ProviderState`, `Signal` and `ProviderReason` (SOP2:871, :873, :879-881, :886). LD-D3A-10 lets D3 register a table only if it is resolved by S-OP-2 itself, by a pinned protocol enum, or by a law that lists its members in full. D3a-3 looked in the generated contracts, the carriers, M3-L and S-OP-2, and found none of the four resolved. So four events are blocked, and M3-D item 21 is not complete:
- `provider.stage.changed`, which needs `StageKind` and `ProviderState`;
- `provider.stage.terminal`, which needs `StageKind` and `ProviderReason`;
- `provider.process.reaped`, which needs `Signal`;
- `supervision.progress.absent`, which needs `StageKind`.

Item 3's ordinary registration admits a table of any of the three provenance classes without a successor (SOP2:226-230). What it cannot do is choose a source when item 23 names none and several pinned enums are candidates, or choose members where no pinned enum exists. Both choices give a field its meaning, and that is S-OP-2's content. One choice also changes one field's table in item 23's descriptor (`provider.process.reaped.signal`). This successor makes those choices and nothing else.

**What it does not change:** any kind, class, provenance class, sink, ceiling, bound, escaping rule, reader rule, event name, level, identity requirement, or other field. Every member below is at most 33 bytes (`snapshot-resolution-input-missing`) and matches K1's grammar (SOP2:220, :269). K1's encoded value bound is the fixed 66 B (SOP2:269), so item 14's per-event bounds are unchanged.

## The successor text

Item 23 gains item 23a, inserted after its closing sentence (SOP2:894). Item 23's `provider.process.reaped` row names `ChildSignal` in place of `Signal` (SOP2:881). The inserted text follows, byte for byte.

<!-- S-OP-2c item 23a begins -->
**23a. The four record tables (S-OP-2c r1).** Item 23 names `StageKind`, `ProviderState`, `Signal` and `ProviderReason` without fixing their members. This item fixes each one under item 3's provenance classes and adds `ChildSignal`. Where a table cites more than one closed enum, its members are exactly their union, and C-2 checks it against that union, member for member. No kind, class, provenance class, sink, bound, event or other field changes.
- **`StageKind`** (`protocol-enum`, LD-OPT-1). The source is the `operator` of each selectable protocol's stage record: TS2 `StageRequestV1.operator` and Rust3 `PlanStageV3.operator` (`schemas/wire/native-carriers-v1.json`, records `Ts2StageRequestV1` and `Rust3C2PlanStageV3`; generated `Ts2StageRequestV1Field2Value` and `Rust3C2PlanStageV3Field5Value`). The value is the operator of the Plan stage the event reports.
  - A stage whose operator is not a member gains one only by an ordinary registration that cites a closed, pinned member for it. Such stages are `host.reuse.disclosed`'s in-host syntax and host inventory stages. Until then their events are blocked, and are never recorded with another stage's kind.
  - Members: `semantic-provider`.
- **`ProviderState`** (`protocol-enum`, LD-OPT-2). The source is P3T's `phases` (`docs/coop/design-corrections/native/protocol3-transitions.v1.json`), in that order. T2O's `phases` (`docs/coop/design-corrections/native/typescript-protocol2-order.v1.json`) are a subset of them. The value is the phase of the host's transition engine after the transition the event reports, so a `typescript-semantic` event names only a T2O phase.
  - Members: `START`, `WAIT_HELLO_ACK`, `READY_OPEN_UNIVERSE`, `WAIT_UNIVERSE_ACCEPTED`, `READY_SNAPSHOT_MANIFEST`, `RECEIVING_SNAPSHOT`, `WAIT_SNAPSHOT_ACCEPTED`, `READY_DEPENDENCY_MANIFEST`, `RECEIVING_DEPENDENCY`, `WAIT_DEPENDENCY_ACCEPTED`, `READY_PREPARED_MANIFEST`, `RECEIVING_PREPARED`, `WAIT_PREPARED_ACCEPTED`, `WAIT_NATIVE_CONTEXT_VERIFIED`, `READY_ANALYZE`, `ANALYZING`, `READY_COMPLETE`, `WAIT_CANCELLED`, `WAIT_ZERO_EXIT`, `WAIT_EOF`, `DONE`, `FAULT`.
- **`Signal`** (`generated-contract`, LD-OPT-3). The source is COMMON4 `D9Signal` (`schemas/sources/common-v4.schema.json`; generated `Common4D9Signal`): the signals the host's handler receives (OPP §5.5). It is `host.signal.received`'s table only.
  - Members: `SIGINT`, `SIGTERM`, `SIGHUP`.
- **`ChildSignal`** (`registry-literal`, LD-OPT-4). This is the table of `provider.process.reaped`'s `signal`.
  - **Members.** They are the POSIX.1-2017 `<signal.h>` signals whose default action terminates the process (T or A), less `SIGPOLL`, which macOS does not define. These are the signals by which a child can end `signaled` on every supported platform.
  - **Mapping.** The host maps a raw termination-signal number to a member only by equality with that member's constant in the pinned `libc` crate for the host's platform. It keeps no number table of its own.
  - **Presence.** `signal` is present exactly when `exit_class` is `signaled` and the number equals a member's constant. Any other number leaves `signal` absent, and `exit_class` `signaled` still records that a signal ended the child.
  - Members: `SIGABRT`, `SIGALRM`, `SIGBUS`, `SIGFPE`, `SIGHUP`, `SIGILL`, `SIGINT`, `SIGKILL`, `SIGPIPE`, `SIGPROF`, `SIGQUIT`, `SIGSEGV`, `SIGSYS`, `SIGTERM`, `SIGTRAP`, `SIGUSR1`, `SIGUSR2`, `SIGVTALRM`, `SIGXCPU`, `SIGXFSZ`.
- **`ProviderReason`** (`protocol-enum`, LD-OPT-5). The source is the `reason` of the admitted `Unavailable` terminal payloads of both selectable protocols (`docs/coop/design-corrections/native/provider-startup.schemas.v1.json`): `PreAnalyzeUnavailableV1` (`native-context-mismatch` only), TS2 `TypeScriptUnavailableV2` and Rust3 `UnavailableV3` (generated `Startup1TypeScriptUnavailableV2Reason` and `Startup1UnavailableV3Reason`). `reason` is present exactly when `terminal` is `unavailable`, and is that payload's reason. Every other terminal leaves it absent.
  - Members: `capability-missing`, `dependency-source-incomplete`, `generated-cfg-unavailable`, `identity-version-mismatch`, `native-context-mismatch`, `node-modules-outside-read-set`, `prepared-output-not-inert`, `prepared-output-stale`, `semantic-universe-incomplete`, `snapshot-resolution-input-missing`, `unsupported-compiler-mode`.
<!-- S-OP-2c item 23a ends -->

## Lead decisions

**LD-OPT-1. `StageKind` is the protocols' stage `operator`.**
- **Why.** It is the only closed stage vocabulary that both selectable protocols pin on their stage records:
  - TS2: `native-carriers-v1.json`:3140 (`Ts2StageRequestV1`), with `operator` at :3160-3166, `const` `semantic-provider`;
  - Rust3: `native-carriers-v1.json`:4810 (`Rust3C2PlanStageV3`), with `operator` at :4867-4872, the same `const`;
  - generated: `crates/contracts/src/generated/protocol.rs`:6643-6646 and :7510-7513.

  One member is the truth today: every provider stage of both protocols has this operator. The field still separates provider stages from the other stage kinds named below once those are pinned.
- **Rejected:**
  - **The stage spec's `operation`.** It is an open token: "Provider-defined logical operation tokens, not a platform-wide enum or host-selected physical-plan labels" (`schemas/sources/identity-v3.schema.json`:3022-3028; M3-C r8:992).
  - **Rust3's `kind`** (`fact-derivation`, `native-carriers-v1.json`:4814-4819; `protocol.rs`:7505-7508). TS2's stage record has no such member, so it is not one table for both.
  - **`NativeContextLanguageV1`** (`rust`, `syntax`, `typescript`; `schemas/sources/native-v2.schema.json`:6775-6783). It classifies a universe, not a stage. It would give a universe's host inventory stage and its syntax or semantic stage the same kind (M3-C r8 LD8-2, :41), and on provider events it repeats `role`.
  - **M3-L's span names** (start, analysis, teardown, M3L item 13). They are span boundaries, not a member table, and do not cover `host.reuse.disclosed`.
- **What stays open.** `host.reuse.disclosed` covers in-host syntax stages and, since M3-C r8, a host inventory stage per universe (M3L item 10; M3-C r8 item 16). Neither has a closed pinned operator yet: the inventory stage's operation token is M3-C r8's X-9 (:1271). Their `StageKind` members follow by ordinary registration once a closed pinned member exists. That registration is the J and C4a owners'. D3's four events need only `semantic-provider`.

**LD-OPT-2. `ProviderState` is P3T's phase list.**
- **Why.** The host's state machine is the table engine over P3T and T2O (M3-D r5 item 10; D2b plan r3 LD-D2B-4, `supervisor-d/d2b/PLAN-r3.md`:111). Its state is a phase of these tables.
- **The sources.** Both tables are "NORMATIVE and CLOSED":
  - P3T: `docs/coop/design-corrections/native/protocol3-transitions.v1.json`:8-31, 14,845 bytes, sha256 `b0aca55d89482be14e9c34554c1febb66d9751754b7c3057a383a010515feb0b`;
  - T2O: `…/typescript-protocol2-order.v1.json`:7-24, 11,341 bytes, sha256 `007ef7affce224c7bac6af3bb7897e86691085e2dd788f4a613e45c1fa5b8bbb`. T2O is a design-lock input.

  The product vendors both as byte copies under `crates/components/data/`, with the same digests (LD-D2B-4).
- **The members.** T2O's 16 phases are a subset of P3T's 22. P3T's six extra phases are Rust3's dependency and prepared transfers. The union is therefore P3T's list. The Rust overlay (`p3-guard-successor.v1.json`) adds guards and no phase.
- **Rejected:**
  - **A reduced subset**, such as a span-level state. It would be a law-chosen projection of the engine's state with no source, and BLOCKED-TABLES offered it only as an alternative.
  - **Two per-protocol tables.** Item 23 gives the field one table, and `role` already separates the protocols.

**LD-OPT-3. `Signal` is COMMON4's `D9Signal`, for the host's received signals only.**
- **Why.** The memo said no pinned schema has a signal enum. That is true for a child's signal, but not for the host's. COMMON4 pins `D9Signal` (`schemas/sources/common-v4.schema.json`:280-286; generated `Common4D9Signal`, `crates/contracts/src/generated/evidence.rs`:11864-11871). OPP cites it as the `interrupted` signal set (OPP:88, OPP:329; WS:1363).
- **Provenance class.** It is a D9 vocabulary in a pinned generated module, so it is `generated-contract`, the class item 3 names for D9 codes (SOP2:216).
- **The split.** A child can die by signals the host never receives, such as `SIGKILL` and `SIGSEGV`, so `D9Signal` cannot be `provider.process.reaped`'s table. That field takes `ChildSignal` (LD-OPT-4). This is the one descriptor change, at SOP2:881.
- **Rejected:**
  - **One wide table for both fields.** It would give `host.signal.received` members its handler can never receive. It would also replace a pinned source with a law list.

**LD-OPT-4. `ChildSignal`'s members: a law choice, because no pinned enum exists.**
- **What the platform observes.** `ExitStatus::signal` returns the raw `WTERMSIG` number, 1 to 126 (`crates/platform/src/process.rs`:403-407). The supervisor holds it as `ExitClass::Signaled(i32)` (`crates/components/src/supervisor.rs`:354, :2569). The host itself sends only `SIGTERM` (15) and `SIGKILL` (9) (`supervisor.rs`:965-966; M3-D r5 items 18 and 19, :582, :635, :639-640).
- **The criterion.** A process ends `signaled` only by a signal whose default action terminates it. A handled, ignored, stop or continue disposition never yields `WIFSIGNALED`. So the observable set is POSIX's terminating signals: `<signal.h>` default action T or A.
  - That set is 21 signals.
  - One of them, `SIGPOLL`, is absent from macOS (`libc` 0.2.189 defines it for Linux only). It is dropped, so that every member names a signal on all four `PlatformFamily` targets (`native-v2.schema.json` `PlatformFamily`).
  - The 20 that remain are the smallest closed set that names every POSIX terminating signal on every supported platform.
- **The mapping.** The numbers differ by platform. For example, `SIGBUS` is 7 on Linux and 10 on macOS, and `SIGUSR1` is 10 on Linux and 30 on macOS. So the host matches by equality with `libc`'s constant for the target, never by a hand-written number table.
  - The crate is pinned: `Cargo.lock`:168-171, `libc` 0.2.189, checksum `3eaf3ede…612f2`; `crates/platform/Cargo.toml`:15, `=0.2.189`.
  - `evidence/check_sop2c.py` reads the 20 constants for macOS and for Linux x86_64 and aarch64 from the checksum-verified crate archive.
- **Numbers outside the table.** These are Linux's real-time signals, `SIGSTKFLT`, `SIGPWR` and `SIGIO`/`SIGPOLL`, and macOS's `SIGEMT`. They leave `signal` absent, while `exit_class` `signaled` keeps the fact. Item 23 already makes `signal` optional.
- **Rejected:**
  - **`{SIGTERM, SIGKILL}` only.** It names what the host sends but drops every crash signal (`SIGSEGV`, `SIGABRT`, `SIGBUS`, `SIGILL`, `SIGFPE`), which D3-T1's core-survival control produces (M3-D r5 item 27, :889).
  - **Every signal number with a platform name**, including real-time and platform-only signals. That gives one member a different meaning per platform and adds members no control reaches.
  - **A numeric field.** It needs a K2 reading of a code, and a new kind or class needs a successor (SOP2:231-239). It would also differ by platform.
- **Also usable by** D3's `tool.process.reaped`, which today omits `signal` (D3a-3 r2 LD-D3A3-2). Adding it there is D3's ordinary registration.

**LD-OPT-5. `ProviderReason` is the admitted `Unavailable` reasons of TS2 and Rust3.**
- **Why.** Item 22 already classes "closed terminal responses … and their NE §9 successors" as `protocol-enum` (SOP2:845). The M3 protocols' successors are the startup schema's payloads, which the carriers select by host phase (`native-carriers-v1.json`, `protocols.*.frames` `Unavailable`):
  - `PreAnalyzeUnavailableV1.reason`: `const` `native-context-mismatch` (`provider-startup.schemas.v1.json`:507; product `schemas/sources/startup-v1.schema.json`:509);
  - `TypeScriptUnavailableV2.reason`: six members (:607; product :609; `protocol.rs`:5100-5113);
  - `UnavailableV3.reason`: nine members (:656; product :658; `protocol.rs`:5251-5270).

  The arch and product copies' three `reason` schemas are equal. Their union has 11 members.
- **Presence.** Only `unavailable` carries a reason. `complete`, `cancelled` and `crash` have none. `provider-fault`'s closed `faultKind` is already `provider.fault.reduced`'s `fault_kind` (SOP2:883), so it is not repeated here. `budget-exhausted`'s payloads carry a dimension (TS2) or unit (Rust3), not a reason (`provider-startup.schemas.v1.json`:683, :734). A field for them is a later ordinary registration, not this table.
- **Rejected:**
  - **NE's `UnavailableReasonV3`** (`native-v2.schema.json`:4664). It is NE's general vocabulary, not the M3 protocols' admitted payloads. It lacks four members they admit (`generated-cfg-unavailable`, `semantic-universe-incomplete`, `snapshot-resolution-input-missing`, `unsupported-compiler-mode`).
  - **Per-protocol tables.** Item 23 gives the field one table, and `role` attributes the reason. TS2 and Rust3 share four members with one meaning each.
  - **Folding in budget dimensions or fault kinds.** They are a different namespace, and the second one would duplicate an existing field.

## The cross-law name: `supervision.child.settled`

M3-D r5 item 21 names `supervision.settled` (:690), which breaks item 2's three-segment grammar. D3a-3 registers `supervision.child.settled` (LD-D3A3-11). That name is an ordinary registration of D3's (item 21), not S-OP-2 text. M3-D is not a design-lock contract parent: no accepted successor has `supervisor-d/PROPOSAL-r5.md` as a parent. So this successor cannot override it, and does not. The adoption belongs to M3-D's next revision, whose owner is the lead.

## Open questions for review

- **Q1.** Is the stage `operator` the right `StageKind` source (LD-OPT-1), and is blocking `host.reuse.disclosed`'s syntax and inventory rows lawful until their operators are pinned?
- **Q2.** Do P3T's and T2O's `phases` qualify as pinned closed enums for `protocol-enum` (LD-OPT-2)? Both are stated "NORMATIVE and CLOSED"; T2O is a design-lock input; P3T is pinned by D2b-2's vendored copy and the overlay's parent.
- **Q3.** Is a `protocol-enum` table equal to the union of several cited closed enums lawful under item 3 without a new provenance class, given that C-2 checks the union member for member (`StageKind`, `ProviderState`, `ProviderReason`)?
- **Q4.** Is `generated-contract` the right class for `Signal` (`D9Signal`)? Is SOP2:881's change of table within a narrow successor?
- **Q5.** `ChildSignal` (LD-OPT-4): the T-or-A criterion, dropping `SIGPOLL`, the `libc`-constant mapping and the absent rule. Should the set be smaller instead?
- **Q6.** `ProviderReason` (LD-OPT-5): present only for `unavailable`, with budget dimensions and fault kinds excluded.
- **Q7.** Is it right to leave `supervision.child.settled` to M3-D's next revision?

## Not claimed

- No product code, Cargo command or test was run for this draft. No registration is made; D3's events are registered by D3's next unit once this record is accepted and bound.
- The Plan's stage ordinal is not added to any event. If a reviewer wants it, it is an ordinary field registration (SOP2:226-230), not this table.
- The citations are to product main `5de9fd4` and to the architecture files named, each re-read on 2026-10-17. `evidence/check_sop2c.py` re-derives every member list.
