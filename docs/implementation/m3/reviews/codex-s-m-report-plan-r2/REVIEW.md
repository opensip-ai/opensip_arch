# Codex review: S-M-REPORT-PLAN-r1, round 2

**Verdict: ACCEPT.** No required findings or nonblocking observations. **SM-REPORT-PLAN-R1-RF-01, SM-REPORT-PLAN-R1-RF-02 and SM-REPORT-PLAN-R1-NBO-01 are resolved.** Acceptance covers PLAN-r2 as a plan for definitions and work still owed, not completion of those measurements or effect of L.

## Subject and preservation

Stage: `/tmp/opensip-implementation/s-m-report-plan-r1-stage`.

`subject.json`: 1450 bytes, SHA-256 `51d98e20d496d992e51e8bc375b972c949cb69f8f75dedfe7bca7db9044ad994`. All six members independently rehashed and match:

| Member under docs/implementation/m3/s-m-report-plan | Bytes | SHA-256 |
|---|---:|---|
| PLAN-r1.md | 16828 | 372d3d8d97898c4c7cb08b5dd902f317a288e3ccf2b21ad67569705f1a3977e9 |
| PLAN-r2.md | 21077 | b4f7c3326c8d48906095feb6fce784e5df7392d72137c4a73041d68d0131bbca |
| gap-inventory-2026-10-13.md | 46306 | 8ca97e6ecea09ff316ef9f7a11d17c0a4c63463713f958ecdaa8e9c149d82e12 |
| make_plan_r2.py | 8144 | d15756c7480e138bbe6d7265f744ebac06dc8b85972bbbc6834450cea2f2c749 |
| runners/freeze_s_m_report_plan_r1.py | 6403 | c5778b08123e16b58237c73de4c928c6b6c9ce9fa9d62eb2e8885e6bd7fa8920 |
| runners/freeze_s_m_report_plan_r2.py | 7711 | 45719ade8b354f104ca8c6d849b1737155e19ba3e75d2838f499d953cc0ebcb8 |

The three original members also match the preserved round-1 stage byte-for-byte and its original manifest. PLAN-r1 and the round-1 review remain unchanged. Inspected both freeze scripts without executing them. Independently reconstructed the seven literal replacements and two section replacements declared in make_plan_r2.py from its parsed text; the result equals PLAN-r2 byte-for-byte. The author script was not executed.

Live bases match: clean product `95279fa8ae086f98bd221cd827f6c0efc156c0c5`; architecture `5d474f97f9d41564999e6ccc6247f6bc487a23e3`. Architecture's existing untracked held E2s directory was not read or changed.

## Round-1 resolution

**RF-01:** D-9 at PLAN-r2:106-107 now takes the measured snapshot2-equivalent inventory population, descriptor bytes, total bytes and bound standing from SM-5. Dependency-source rows remain separate from snapshot rows. It removes the average-byte extrapolation from the required term and explicitly confines any such estimate to informational presentation outside S_eff. This matches M3-L r6:559 and :591 and resolves the estimated-term substitution. Final S_eff remains unfilled.

**RF-02:** §3a at :123-132 explicitly includes smithy-rs, rspack, deno and conditionally sui. It recognizes that the lack of an outcome dependency does not make their pre-effect inputs optional. U-7 at :118 assigns site census for analysed Smithy/Deno entries and exact coverage/unavailability records for the remaining entries; U-4 covers the admitted-row term for all twelve Rust workloads. U-6 at :119 depends on U-7 as well as U-1 through U-5. U-3 supplies query mapping, fixed overheads and formulas with later-owned parameters unset. Together these units cover the required S-M part while preserving honest partial/unavailable coverage and deferred worker figures.

**NBO-01:** D-1 at :39-42 now says counted sources and workload source-count scenarios, identifies Rust S as input subjects rather than analysed coverage, removes the smallest-graph claim and requires actual SM-2/SM-4 coverage beside the synthetic figure. Any subsequent F, T or outcome using it is expressly conditional on the D-1 convention.

## Large-workload evidence and citations

Checked §3a directly against the cited records, not the research inventory's derived numbers:

| Workload | Exact S | Snapshot-equivalent rows | Descriptor bytes |
|---|---:|---:|---:|
| smithy-rs | 1084 | 3632 | 647602 |
| rspack | 1384 | 23980 | 4085164 |
| deno | 1052 | 14920 | 2227549 |
| sui, if S-P permits | 3318 | 19063 | 3509292 |

The subject counts and two independent host 3+7 derivations match the accepted Rust-scope report and Sui-scope report. Rows, descriptor bytes and within-bounds standing match sealing-typed-remaining REPORT.md:11, :13-14, :20 and :35. These are repository-only snapshot-equivalent observations, not native admission.

Smithy's ten represented entries are the two fuzz entries, one HTTP-fuzz entry and seven hierarchy entries. The hierarchy report expressly labels concurrent-review timings informational, as the plan preserves. Its partial analyses do not establish full first-party coverage. The r8 REPORT.md:7 confirms Smithy rust-runtime's 5115131-byte and Deno root's 22825382-byte experimental descriptors exceed the unchanged 4194304-byte prototype bound. These are prototype prelaunch refusals, not canonical native snapshot-bound outcomes.

The r7 REPORT.md:7 supports the stale-lock refusal for aws-smithy-fuzz and the Sui Move symlink exclusion. The r1 large-workspace report retains incomplete original outcomes; r2 REPORT.md:7 limits its retries to Smithy, Deno and Sui. Rspack is assigned exact retained-outcome review rather than an invented successful graph. The two Deno analysis reports support partial binary/SQLite coverage. No quotient by S is justified for these partial populations, and §3a expressly records none. U-7 still owes the exact per-entry evidence and census; this review accepts that assignment, not its completion.

## Authority, definitions and scope

D-1 remains a lawful explicitly labelled synthetic benchmark convention under M3-L r6:563. It binds no production G3 emission factor and establishes no real-workload replay bound. Narrowing the control correction concerns the synthetic benchmark requirement; it does not overturn the prior finding that source counts and monotone synthetic timings establish no real-workload work-dominance relation. The historical product37581132 replay boundary remains disclosed; current-head replay timing is not established.

D-2 remains consistent with NE's activated non-path population, separate path snapshot custody, set identities and snapshot-before-dependency transport, DS4-P1 CONTRACT.md:5 and M3-C r7:600. The accepted axum dependency fragment contains 187 packages/7338 files; the different graph-expanded map contains 6403 files. The latter does not complete normative SM-7. U-2 is appropriately assigned new measurement work without requiring native admission first.

D-3 through D-8 retain the reviewed scope and disclosures: two overlay children, included startup/map work and TS start over-count, Rust unit coverage, public compiler-call granularity, reset labels, whole-process RSS and accepted T2-manifest subject recipes. Harness DESIGN.md:798-807 supports the reset requirements. Cold-run variants must satisfy all cold-reset requirements, including every warmup, rather than treating a page-cache record alone as sufficient if disposable state is introduced. Overlay median/maximum statistics must use corresponding per-run sums. These are execution requirements for the later units, not new findings against this revision.

U-1 explicitly remains a new executor variant, leaving the closed executor unchanged. No stage, requested key, production emission factor, census kind, batching policy or worker scratch count is chosen. No placeholder, F, T or outcome is recorded. SMComplete, LG1Met, effectiveL and productQualification remain false. O7, D3 and D13 remain closed; L-G1 remains open. Exact lead assent and fresh verification before architecture publication remain separate lead work.

Only read-only file inspection, hashing, JSON/source parsing and Git queries were used. No compiler, Cargo, tests, driver, lane, network, other pane or delegation. No private 413 fixture, installation directory, signing keys or held-tree content was read. Neither repository, stage, control state nor round-1 review was edited. Only this REVIEW.md and review.json were written. Nothing was pushed.
