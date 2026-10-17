# Operability registry

## Events

### `log.stream.opened`

- level: info
- requires: request
- export: false
- template: log stream opened
- maxLine: 1089

| key | kind | class | bound |
| --- | --- | --- | --- |
| version | `Version` | P0 | 66 |
| platform | `Code<Platform>` | P0 | 66 |
| build | `Code<BuildProfile>` | P0 | 66 |
| sink | `Code<Sink>` | P0 | 66 |
| pid | `ProcessId` | P1 | 10 |

### `log.loss.counted`

- level: warn
- requires: request
- export: false
- template: log loss counted
- maxLine: 1793

| key | kind | class | bound |
| --- | --- | --- | --- |
| sink | `Code<Sink>` | P0 | 66 |
| counts | `Counts<LossCell,40>` | P0 | 841 |
| sink_error | `Code<IoErrorKind> (optional)` | P0 | 66 |
| errno | `Errno (optional)` | P0 | 11 |

Frozen index map for `counts`:

- 0: `refused`, `error`
- 1: `refused`, `warn`
- 2: `refused`, `info`
- 3: `refused`, `debug`
- 4: `refused`, `trace`
- 5: `budget`, `error`
- 6: `budget`, `warn`
- 7: `budget`, `info`
- 8: `budget`, `debug`
- 9: `budget`, `trace`
- 10: `queue-full`, `error`
- 11: `queue-full`, `warn`
- 12: `queue-full`, `info`
- 13: `queue-full`, `debug`
- 14: `queue-full`, `trace`
- 15: `prescope-full`, `error`
- 16: `prescope-full`, `warn`
- 17: `prescope-full`, `info`
- 18: `prescope-full`, `debug`
- 19: `prescope-full`, `trace`
- 20: `unpersisted`, `error`
- 21: `unpersisted`, `warn`
- 22: `unpersisted`, `info`
- 23: `unpersisted`, `debug`
- 24: `unpersisted`, `trace`
- 25: `sink-failed`, `error`
- 26: `sink-failed`, `warn`
- 27: `sink-failed`, `info`
- 28: `sink-failed`, `debug`
- 29: `sink-failed`, `trace`
- 30: `sink-stopped`, `error`
- 31: `sink-stopped`, `warn`
- 32: `sink-stopped`, `info`
- 33: `sink-stopped`, `debug`
- 34: `sink-stopped`, `trace`
- 35: `drain-abandoned`, `error`
- 36: `drain-abandoned`, `warn`
- 37: `drain-abandoned`, `info`
- 38: `drain-abandoned`, `debug`
- 39: `drain-abandoned`, `trace`

### `host.repair.completed`

- level: info
- requires: request
- export: false
- template: repair completed
- maxLine: 917

| key | kind | class | bound |
| --- | --- | --- | --- |
| kind | `Code<RepairKind>` | P0 | 66 |
| state | `Code<RepairState>` | P0 | 66 |

### `storage.commit.published`

- level: info
- requires: project+plan+execution+run
- export: true
- template: commit published
- maxLine: 784

| key | kind | class | bound |
| --- | --- | --- | --- |
| latched | `Flag` | P0 | 5 |

### `storage.commit.not_published`

- level: info
- requires: project+plan+execution
- export: true
- template: commit not published
- maxLine: 845

| key | kind | class | bound |
| --- | --- | --- | --- |
| outcome | `Code<CommitNotPublished>` | P0 | 66 |

### `host.phase.started`

- level: info
- requires: request
- export: false
- template: phase started
- maxLine: 945

| key | kind | class | bound |
| --- | --- | --- | --- |
| phase | `Code<Phase>` | P0 | 66 |
| parent | `Code<Phase> (optional)` | P0 | 66 |
| at | `Elapsed` | P0 | 20 |

### `host.phase.completed`

- level: info
- requires: request
- export: true
- template: phase completed
- maxLine: 1001

| key | kind | class | bound |
| --- | --- | --- | --- |
| phase | `Code<Phase>` | P0 | 66 |
| wall | `Elapsed` | P0 | 20 |
| cpu | `Elapsed` | P0 | 20 |
| outcome | `Code<PhaseOutcome>` | P0 | 66 |
| at | `Elapsed` | P0 | 20 |

### `provider.process.spawned`

- level: info
- requires: project+plan+execution
- export: false
- template: provider process spawned
- maxLine: 1029

| key | kind | class | bound |
| --- | --- | --- | --- |
| role | `Code<ProviderRole>` | P0 | 66 |
| universe | `Universe` | P1 | 80 |
| protocol | `Code<ProtocolMajor>` | P0 | 66 |
| pid | `ProcessId` | P1 | 10 |

### `provider.process.ready`

- level: info
- requires: project+plan+execution
- export: false
- template: provider process ready
- maxLine: 995

| key | kind | class | bound |
| --- | --- | --- | --- |
| role | `Code<ProviderRole>` | P0 | 66 |
| universe | `Universe` | P1 | 80 |
| start | `Elapsed` | P0 | 20 |
| transfer | `Elapsed` | P0 | 20 |

### `provider.stderr.reduced`

- level: info
- requires: project+plan+execution
- export: false
- template: provider stderr reduced
- maxLine: 992

| key | kind | class | bound |
| --- | --- | --- | --- |
| role | `Code<ProviderRole>` | P0 | 66 |
| universe | `Universe` | P1 | 80 |
| stderr | `Reduced` | P0 | 48 |

### `provider.fault.reduced`

- level: warn
- requires: project+plan+execution
- export: true
- template: provider fault reduced
- maxLine: 1313

| key | kind | class | bound |
| --- | --- | --- | --- |
| role | `Code<ProviderRole>` | P0 | 66 |
| universe | `Universe` | P1 | 80 |
| source | `Code<FaultSource>` | P0 | 66 |
| fault_kind | `Code<RustFaultKind> (optional)` | P0 | 66 |
| refusal_family | `Code<RefusalFamily> (optional)` | P0 | 66 |
| detail | `Reduced` | P0 | 48 |
| detail_code | `RegisteredCode<RustDetailCode> (optional)` | P0 | 66 |

### `provider.resources.reported`

- level: debug
- requires: project+plan+execution
- export: false
- template: provider resources reported
- maxLine: 1024

| key | kind | class | bound |
| --- | --- | --- | --- |
| role | `Code<ProviderRole>` | P0 | 66 |
| universe | `Universe` | P1 | 80 |
| resident | `Bytes (asserted)` | P0 | 20 |
| cpu | `Elapsed (asserted)` | P0 | 20 |
| handles | `Count (asserted)` | P0 | 20 |

### `supervision.liveness.missed`

- level: warn
- requires: project+plan+execution
- export: true
- template: liveness missed
- maxLine: 1122

| key | kind | class | bound |
| --- | --- | --- | --- |
| role | `Code<ProviderRole>` | P0 | 66 |
| universe | `Universe` | P1 | 80 |
| window | `Elapsed` | P0 | 20 |
| miss | `Code<LivenessMiss>` | P0 | 66 |
| refusal_family | `Code<RefusalFamily> (optional)` | P0 | 66 |

### `supervision.limit.breached`

- level: warn
- requires: project+plan+execution
- export: true
- template: limit breached
- maxLine: 1115

| key | kind | class | bound |
| --- | --- | --- | --- |
| role | `Code<ProviderRole>` | P0 | 66 |
| universe | `Universe` | P1 | 80 |
| limit | `Code<LimitKind>` | P0 | 66 |
| observed | `Count` | P0 | 20 |
| unit | `Code<LimitUnit>` | P0 | 66 |

### `supervision.sample.incomplete`

- level: warn
- requires: project+plan+execution
- export: false
- template: resource sample incomplete
- maxLine: 1020

| key | kind | class | bound |
| --- | --- | --- | --- |
| role | `Code<ProviderRole>` | P0 | 66 |
| universe | `Universe` | P1 | 80 |
| listed | `Count` | P0 | 20 |
| unsampled | `Count` | P0 | 20 |
| listing_failed | `Flag` | P0 | 5 |

### `supervision.cancel.sent`

- level: info
- requires: project+plan+execution
- export: false
- template: cancel sent
- maxLine: 1033

| key | kind | class | bound |
| --- | --- | --- | --- |
| role | `Code<ProviderRole>` | P0 | 66 |
| universe | `Universe` | P1 | 80 |
| inband | `Flag` | P0 | 5 |
| control_reason | `Code<ControlCancelReason>` | P0 | 66 |

### `supervision.cancel.forced`

- level: warn
- requires: project+plan+execution
- export: false
- template: cancel forced
- maxLine: 1040

| key | kind | class | bound |
| --- | --- | --- | --- |
| role | `Code<ProviderRole>` | P0 | 66 |
| universe | `Universe` | P1 | 80 |
| trigger | `Code<ForceTrigger>` | P0 | 66 |
| grace | `Elapsed` | P0 | 20 |

### `supervision.wait.expired`

- level: warn
- requires: project+plan+execution
- export: false
- template: wait expired
- maxLine: 1037

| key | kind | class | bound |
| --- | --- | --- | --- |
| role | `Code<ProviderRole>` | P0 | 66 |
| universe | `Universe` | P1 | 80 |
| wait | `Code<BoundedWait>` | P0 | 66 |
| limit | `Elapsed` | P0 | 20 |

### `supervision.teardown.started`

- level: info
- requires: project+plan+execution
- export: false
- template: teardown started
- maxLine: 1009

| key | kind | class | bound |
| --- | --- | --- | --- |
| role | `Code<ProviderRole>` | P0 | 66 |
| universe | `Universe` | P1 | 80 |
| cause | `Code<TeardownCause>` | P0 | 66 |

### `supervision.tree.swept`

- level: info
- requires: project+plan+execution
- export: false
- template: tree swept
- maxLine: 1025

| key | kind | class | bound |
| --- | --- | --- | --- |
| role | `Code<ProviderRole>` | P0 | 66 |
| universe | `Universe` | P1 | 80 |
| killed | `Count` | P0 | 20 |
| unattributed | `Count` | P0 | 20 |
| platform_limited | `Flag` | P0 | 5 |

### `supervision.scratch.retained`

- level: warn
- requires: project+plan+execution
- export: false
- template: scratch retained
- maxLine: 1030

| key | kind | class | bound |
| --- | --- | --- | --- |
| role | `Code<ProviderRole>` | P0 | 66 |
| universe | `Universe` | P1 | 80 |
| reason | `Code<ScratchRetainedReason>` | P0 | 66 |
| errno | `Errno (optional)` | P0 | 11 |

### `supervision.child.settled`

- level: info
- requires: project+plan+execution
- export: false
- template: supervision settled
- maxLine: 1053

| key | kind | class | bound |
| --- | --- | --- | --- |
| role | `Code<ProviderRole>` | P0 | 66 |
| universe | `Universe` | P1 | 80 |
| cause | `Code<TeardownCause>` | P0 | 66 |
| admissible | `Flag` | P0 | 5 |
| user_interrupted | `Flag` | P0 | 5 |

### `tool.process.spawned`

- level: info
- requires: project
- export: false
- template: tool process spawned
- maxLine: 785

| key | kind | class | bound |
| --- | --- | --- | --- |
| pid | `ProcessId` | P1 | 10 |

### `tool.process.reaped`

- level: info
- requires: project
- export: false
- template: tool process reaped
- maxLine: 1045

| key | kind | class | bound |
| --- | --- | --- | --- |
| pid | `ProcessId` | P1 | 10 |
| exit_class | `Code<ExitClass>` | P0 | 66 |
| max_rss_native | `Count` | P0 | 20 |
| rss_unit | `Code<RssUnit>` | P0 | 66 |
| max_rss_bytes | `Bytes (optional)` | P0 | 20 |
| cpu | `Elapsed` | P0 | 20 |

### `tool.limit.breached`

- level: warn
- requires: project
- export: false
- template: tool limit breached
- maxLine: 949

| key | kind | class | bound |
| --- | --- | --- | --- |
| limit | `Code<LimitKind>` | P0 | 66 |
| observed | `Count` | P0 | 20 |
| unit | `Code<LimitUnit>` | P0 | 66 |

### `tool.sample.incomplete`

- level: warn
- requires: project
- export: false
- template: tool resource sample incomplete
- maxLine: 854

| key | kind | class | bound |
| --- | --- | --- | --- |
| listed | `Count` | P0 | 20 |
| unsampled | `Count` | P0 | 20 |
| listing_failed | `Flag` | P0 | 5 |

### `tool.wait.expired`

- level: warn
- requires: project
- export: false
- template: tool wait expired
- maxLine: 871

| key | kind | class | bound |
| --- | --- | --- | --- |
| wait | `Code<BoundedWait>` | P0 | 66 |
| limit | `Elapsed` | P0 | 20 |

### `tool.teardown.started`

- level: info
- requires: project
- export: false
- template: tool teardown started
- maxLine: 843

| key | kind | class | bound |
| --- | --- | --- | --- |
| cause | `Code<TeardownCause>` | P0 | 66 |

### `tool.scratch.retained`

- level: warn
- requires: project
- export: false
- template: tool scratch retained
- maxLine: 864

| key | kind | class | bound |
| --- | --- | --- | --- |
| reason | `Code<ScratchRetainedReason>` | P0 | 66 |
| errno | `Errno (optional)` | P0 | 11 |

### `tool.child.settled`

- level: info
- requires: project
- export: false
- template: tool settled
- maxLine: 868

| key | kind | class | bound |
| --- | --- | --- | --- |
| cause | `Code<TeardownCause>` | P0 | 66 |
| user_interrupted | `Flag` | P0 | 5 |

## Code tables

### Phase

- provenance: registry-literal
- role: header
- cap: 32

- `request`
- `discovery`
- `snapshot`
- `plan`
- `provider`
- `provider.start`
- `provider.analysis`
- `provider.teardown`
- `admission`
- `evaluation`
- `commit`
- `delivery`
- `reuse`

### PhaseOutcome

- provenance: registry-literal
- role: code
- cap: 32

- `completed`
- `failed`
- `cancelled`
- `not-applicable`

### PathAnchor

- provenance: registry-literal
- role: path-anchor
- cap: 16

- `installation`
- `store`
- `log-root`
- `scratch`
- `project`
- `system-temp`
- `external`

### Sink

- provenance: registry-literal
- role: code
- cap: 64

- `file`
- `stderr`
- `harness`

### Platform

- provenance: registry-literal
- role: code
- cap: 32

- `linux-aarch64-gnu`
- `linux-x86_64-gnu`
- `macos-aarch64`
- `macos-x86_64`

### BuildProfile

- provenance: registry-literal
- role: code
- cap: 32

- `debug-assertions-on`
- `debug-assertions-off`

### IoErrorKind

- provenance: registry-literal
- role: code
- cap: 32

- `permission-denied`
- `no-space`
- `io-error`
- `other`

### CommitNotPublished

- provenance: registry-literal
- role: code
- cap: 64

- `undetermined`
- `refused`

### RepairKind

- provenance: registry-literal
- role: code
- cap: 64

- `registration`
- `store-directory`
- `ledger-file`
- `ledger-schema`
- `carrier-floors`
- `trust-directory`
- `trust-dependency`

### RepairState

- provenance: registry-literal
- role: code
- cap: 64

- `RW-R1`
- `RW-R2`
- `RW-R3`
- `RW-R4`
- `RW-R5`
- `RW-R6`
- `RW-R7`
- `RW-P1`
- `RW-P2`
- `RW-P3`
- `RW-L1`
- `RW-T1`
- `RW-T2`
- `RW-T3`

### ProviderRole

- provenance: registry-literal
- role: code
- cap: 64

- `typescript-semantic`
- `rust-semantic`

### ProtocolMajor

- provenance: registry-literal
- role: code
- cap: 64

- `typescript-semantic-2`
- `rust-semantic-3`

### RssUnit

- provenance: registry-literal
- role: code
- cap: 64

- `kib`
- `bytes`

### FaultSource

- provenance: registry-literal
- role: code
- cap: 64

- `control-fault`
- `control-refusal`
- `rust-provider-fault`

### ForceTrigger

- provenance: registry-literal
- role: code
- cap: 64

- `second-signal`
- `grace-expired`

### TeardownCause

- provenance: registry-literal
- role: code
- cap: 64

- `clean`
- `closure-recheck-failed`
- `session-spec-inconsistent`
- `spawn-failed`
- `handshake-deadline`
- `control-refusal`
- `provider-protocol`
- `unexpected-exit`
- `deadline`
- `liveness`
- `memory-ceiling`
- `process-count`
- `byte-bound`
- `scratch-bound`
- `user-cancel`
- `revoked`
- `observer-fail-stop`
- `host-fault`
- `abandoned`
- `confinement-refused`

### BoundedWait

- provenance: registry-literal
- role: code
- cap: 64

- `handshake`
- `liveness-window`
- `progress-absent`
- `wall-clock`
- `normal-exit-grace`
- `stage1-cancel-grace`
- `shutdown-ack`
- `term-to-kill`
- `reap-ceiling`
- `drain`

### LimitKind

- provenance: registry-literal
- role: code
- cap: 64

- `resident-memory`
- `process-count`
- `response`
- `scratch`
- `tool-output`

### LimitUnit

- provenance: registry-literal
- role: code
- cap: 64

- `bytes`
- `processes`

### ExitClass

- provenance: registry-literal
- role: code
- cap: 64

- `exited`
- `signaled`
- `unreaped`

### ScratchRetainedReason

- provenance: registry-literal
- role: code
- cap: 64

- `io-failure`
- `work-exhausted`
- `root-unreaped`

### LivenessMiss

- provenance: registry-literal
- role: code
- cap: 64

- `window-expired`
- `nonce-mismatch`

### RefusalFamily

- provenance: protocol-enum
- role: code
- cap: 64

- `RF-1`
- `RF-2`
- `RF-3`
- `RF-4`
- `RF-5`
- `RF-6`
- `RF-7`
- `RF-8`

### ControlCancelReason

- provenance: protocol-enum
- role: code
- cap: 64

- `user`
- `deadline`
- `supervisor-fault`

### RustFaultKind

- provenance: protocol-enum
- role: code
- cap: 64

- `compiler-crash`
- `input-rejected`
- `internal-invariant`

### RustDetailCode

- provenance: registry-literal
- role: code
- cap: 64


## Retired

none

## Sinks

- stderr: P0, P1, P2
- file: P0, P1, P2
- pre-scope: P0, P1, P2
- harness: P0, P1
- ring: P0, P1
- bundle: P0, P1; P2 only with per-member consent
- otlp: P0, export candidates only
- diagnostics: P0, the loss summary only
