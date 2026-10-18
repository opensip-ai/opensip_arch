# D3b-1 source preflight review

**Verdict: REQUIRED-FINDINGS**

**Subject manifest SHA-256:** `1e874146fcbff320744b628b0e78f662e2ecad22d0bca99c7e9c7c98e4e7d5fd`

This is a frozen-source preflight only. It is not unit acceptance, lane validation, qualification, or approval to integrate. I rehashed the manifest and all 28 members; the manifest hash and every member hash match. The 13 baselines match product commit `d154eb002fc536855b9c831d0d6484bfaf5335d3`, and the frozen plan and D3b-0 scope match their authority bytes.

## Required findings

### D3B1-PRE-R1-RF-1 — The snapshot neither records nor accounts for the root identity

The accepted plan requires the breadth-first snapshot to record `process_identity` for **each pid**, account for every pid inspected or queued, and still keep the root out of the by-pid target set (`PLAN-r3.md:100-112`). The candidate pushes the root into the bounded queue, but wraps both the `inspected` increment and `tree_identity` call in `if pid != root`; `queued` is incremented only for discovered children (`supervisor.rs:2940-2980`). Its public evidence comment expressly changes the rule to “root excluded” (`supervisor.rs:389-393`). A root-only snapshot therefore consumes one of the 4/64 bounded slots while reporting `queued = 0`, `inspected = 0`, and it cannot preserve a root identity read or its failure.

Record and account for the root as one distinct queued/inspected pid, while keeping it structurally excluded from `kill.targets` and every by-pid send. Add a root-only control and adjust the exact/over-bound controls so the evidence counts and the total bound use the same distinct-pid population.

### D3B1-PRE-R1-RF-2 — The provider's four-PID walk bound has no runtime control

The accepted D5-T4 control requires a fork loop at both sourced bounds: 4 for a provider and 64 for a tool (`PLAN-r3.md:100-105,311-321`). Both candidate boundary fixtures exercise only `tool_run` and the 64-PID tool path (`supervisor_tests.rs:4159-4200`). `the_walk_bound_is_four_times_the_class_count` merely recomputes constants (`supervisor_tests.rs:4259-4265`); it does not call `Supervision::walk_bound` for a provider or drive the provider snapshot. A mutation that returns the tool bound for providers can survive these controls.

Add a provider-class runtime boundary control proving three descendants plus the root can complete, while four descendants plus the root yields `BoundReached` and `IncompletePlatformLimited`.

### D3B1-PRE-R1-RF-3 — The alive-root side of the required root-state distinction is not directly proved

The plan requires separate controls for an alive root and a held zombie, including `exit: unreaped`, no by-pid root kill, and no group signal after reap or abandonment (`PLAN-r3.md:315-331`). The candidate's explicit ceiling test uses `reap_blocked`, so the root has exited and is a deliberately held zombie (`supervisor_tests.rs:4235-4257`). The group-kill-failure case reaches the alive-root path because the tree fixture ignores `SIGTERM`, yet its comment incorrectly says the root dies from `SIGTERM` and its assertions cover only the incomplete report and retained `killpg` errors (`supervisor_tests.rs:4057-4073`). It does not assert `ExitClass::Unreaped`, distinguish the confirm evidence from the held-zombie case, prove that the root was never a by-pid target, or prove that no group signal follows abandonment. It also does not clean up the intentionally surviving root.

Add a direct alive-root control with those assertions and bounded out-of-band cleanup, alongside the existing held-zombie control. The control must fail if the root is placed in the by-pid target set or if signaling resumes after abandonment.

## Non-blocking observations

- The production supervisor uses the bounded platform listings, and the obsolete unbounded `group_members` API is removed from the frozen candidate.
- Descendant-step failures retain the original borrowed `LaunchError` values in settlement evidence; group failures keep their call and errno, while `TreeEvidence` remains borrowed from `Settlement`.
- The confirm cadence is finite, services the ordinary turn between confirms, and preserves an earlier `Exceeded` through `confirm_exceeded`; a listing failure is latched. Reap-last and the ceiling's final reap attempt are present.
- `TreeSwept` counts only distinct by-pid `Sent` outcomes. The tool mapping, registration, readback descriptor, and event budget move together.
- The read-only no-cgroup checker scans tracked and unignored Rust sources under both source roots, includes tests, reports no exclusions, and explicitly reports `qualification: false`. Its scope is conservative relative to the accepted production-only rule.
- Linux/D3b-L and D3b-2 remain separate; this preflight makes no qualification claim. No builds, tests, or lanes were run, as required.
