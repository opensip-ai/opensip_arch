# GROK2 review: M3 unit plan r2

**Verdict: REQUIRED-FINDINGS**

Subject: `docs/implementation/m3/M3-PLAN.md`, 35300 bytes, sha256 `add49e2508816defdcc033a3720359fa8a639d8fcb94191950b91e8f5df8c841`. Previous snapshot `M3-PLAN-r1.md` matches `65bf6ac5…`. Product baseline `eb0d50398035fe3532dadc332f88cf1d8bc4cb69` is a clean worktree. No product build or test was run. `~/Library/Application Support/OpenSIP` is absent.

The listed host-chain sum is 2+3+2+3+2+3+3+3+3+2 = 26, and that column matches the finish days. The quoted confinement sentences match the cited law. The new errors are the unscheduled predecessors of that 26-day path, two citations that do not say what the plan attributes to them, and a confinement successor list that stops short of the contracts that refuse the enforcement item 4 would claim.

## r1 findings

| ID | Resolved | Where |
|---|---|---|
| RF-1 | yes | Section cites only. No `OPP:` line number remains. |
| RF-2 | yes | S-OP-12 is on M3-J and in the M3 milestone list. O7 is in M3-L's gate and before provider launch. |
| RF-3 | yes | Routing cites the coverage groups and BP:999-1036. BP:933-945 is named only as the population census. |
| RF-4 | yes | The twelve section objects and five fallow objects are cited on their own lines. `process.rs` is the M6 DR-G22 owner. |
| RF-5 | yes | `package.json`, `tsconfig.json`, and generated `protocol.ts` are present. CH14:507-517 and CH14:519-524 are absent. |
| RF-6 | yes | NE:7 is on E, F, and G. NE:10 is on D. NE:11 is on J2. NE:2 is split between B (§1.4) and E (syntax-only). |

RF-1. Operability r3 headings match the section claims used here: §3.1 is RequestId, phase-lawful identities, and the one host-owned subscriber; §3.5 says there is no environment side channel; §3.6 is O1(a); §5.1 is the supervision primitive; §5.5 is two-stage cancellation and the S-OP-12 phase join; §5.6 is O7, needed before M3 providers ship; §7 is enforcement; §8 is the milestone placement; §9 is the S-OP table, including S-OP-12 blocking M3 cancellation; §10 is the control table. The cited prefix `b49035f2…` is `operability/PLAN-r3.md`.

RF-3 and RF-4 were rechecked against the current build plan and coverage inventory. BP:895 says gate execution still belongs to M6. BP:999-1000 requires M6 qualification. BP:1014, 1017, 1018, 1025, 1027, 1029, and 1033 are the seven M3 gates. BP:1024 is DR-G20 at M5. BP:1026 is DR-G22 at M6, owner `crates/platform/src/process.rs`. The twelve section ids and FW-01, FW-03, FW-08, FW-13, and FW-14 sit on the cited coverage lines. The four `grants.rs` owner lines are COV:5277, 5317, 5337, and 5377. FW-14's source text is pinned shapes, reproducible workarounds, manual-correction counts, and positive and negative fixtures.

RF-5. At `eb0d503`, `package.json:7` is Node 24.16.0 and `:12` is TypeScript 6.0.3. `src/generated/protocol.ts:1` is inert types. CH14:506 is `package.json`, CH14:518 is the generated protocol, and CH14:525 is `tsconfig.json`. The eighteen implementation paths in CH14:507-517 and CH14:519-524 are absent.

RF-6. Native-evidence headings put §6 at 2562-2647, §9 at 2781-3316, and §10 at 3317-3858. U-8 is NE:816. U-9 is NE:879. The syntax-only mode row is NE:178, and NE:218-306 is the syntax-universe discussion. PO-0 through PO-4 are all inside NE:1803-1870.

## Required findings

### RF-1 — The 26-day host chain is not shown to be the critical path

**Location.** M3-PLAN.md:143, :147, :152, :168, :179, :181, :185, :187, :190-198, :263, :296, :300.

**Claim.** After M3-L, with the B, C, D, E, H, and J laws already accepted, the host chain determines M3 and finishes in 26 days. G2 is already finished. D1 through D3 finish on day 7.

**Evidence.** M3-D depends on P0, L, and CF. M3-CF is size L and does not start until the owner decides O7. The DAG's assumption list does not include CF, and CF has no row. D1 → D2 → D3 starts at day 0. J2, which is on the stated host chain, starts after D3. D3's day-7 finish is what leaves the host chain clear of D until day 15; nothing in the table bounds CF inside that slack.

The same paragraph says the D law is already accepted when the clock starts. The O7 risk says D1's Seatbelt trial decides feasibility before the D law is accepted. The trial is the first two days of that clock.

G2 is four days, placed after S-P and before L, with finish 0. Its scope runs the `rustc_driver` sidecar under the O7 profile. The O7 section says F4 and G2 run inside that profile, and D1 is the profile's primitive. Provider launch waits on the O7 decision, whose date the prelude leaves outside the model. The before-L paragraph accounts for T2a, Q0, S-M, T2b, and L's acceptance. It does not account for G2.

M3-M depends on J3, G4, F3, E3, I2, K2, and O1. The timing row waits for J3, G4, F3, I2, and K2, and then adds three days to reach day 24. E3 and O1 are absent from that row. I2, K1, K2, and O1 have no durations. M3-X depends on all units. B3, D4, D5, E, F4, J4, and R also have no finish bounds.

The drawn chain's own addition is consistent. It does not establish that those missing branches finish before it.

**Fix.** Give CF a predecessor edge into D, or state that CF is accepted before day 0 and put it in the assumption sentence. Place the Seatbelt trial before D-law acceptance, and place G2 after the O7 decision and the confinement primitive it runs under. Give every predecessor of M3-M and M3-X a duration or an explicit finish bound, including E3, O1, I2, and K. Recompute the longest path after those bounds exist. Until then, call 26 days the sum of the listed host chain only.

### RF-2 — AQP:236 does not let the exploratory report close with adjudication pending

**Location.** M3-PLAN.md:152.

**Claim.** M3-M's report completes with INSUFFICIENT-EVIDENCE or unclear strata where adjudication is still pending, citing AQP:236. Later labelling is not an exit threshold.

**Evidence.** AQP:236 says a stratum with too few findings for the bound, including zero findings, is INSUFFICIENT-EVIDENCE, never passes, and is remedied by more T2 repositories. AQP:228 says every gating and repair-eligible finding on T2 is adjudicated. AQP:231 defines *unclear* as a written label, beside *true* and *false*. AQP:246 sends every unclear label on a gating or repair-eligible finding to a designated human expert.

**Fix.** Cite AQP:236 only for too few findings. If this plan's exploratory exit allows a report to close before that adjudication finishes, say so as this plan's rule and name the AQP paragraphs that still require adjudication for any later Q2 use.

### RF-3 — OPP §10 does not list confinement escape cases

**Location.** M3-PLAN.md:143.

**Claim.** D5 is the G21 controls, including confinement escape cases, and OPP §10 is that source.

**Evidence.** Operability §10 (PLAN.md:422-437) lists Privacy, Correlation, Custody, Bounds, Outcomes, Crash, Capacity, Cancellation in phases A–E, Liveness, and Overhead. It has no network-escape, write-outside-scratch, or ambient-environment case. M3-PLAN.md:295 already lists those three as D5 and S-OP-11 work.

**Fix.** Cite OPP §10 for the ten areas it contains. State the three escape cases as new D5 and S-OP-11 controls.

### RF-4 — Item 4's enforcement needs the native and test-execution successors

**Location.** M3-PLAN.md:272, :274-280, :286-290, :298.

**Claim.** CF-1 (an SL S10 and S6 successor, an AQ §5 item 4 disposition, and a DR-128 record) plus M5 `execution.rs` carries item 4: repository-code execution runs only inside confinement or a container.

**Evidence.** The disclaimer quotes are accurate. SL:1113 says confinement is never claimed. SL:497 says no confinement is claimed. AQ:344 says no process or WASM boundary is claimed as a sandbox. NE:2554 says no sandbox is claimed. REG:366 says G21 does not claim security confinement. REG:317 is the open DR-128 sandbox row.

Item 4 claims an enforcement those other accepted texts independently refuse:

- NE:2440-2444 copies `AuthorizedExecutionV2` effect values from `permission-truth-tables.v9`. The native contract never asserts `ENFORCED-PLATFORM` itself and refuses a record that claims more than that table. The pinned child-process values for network, subprocess, and filesystem write are `DISCLOSURE-ONLY`.
- NE:2480-2487 says confinement is never claimed, and the mandatory pre-execution sentence says OpenSIP does not prevent network access or other effects on this platform.
- WS:1071-1081 says the test step discloses and does not confine. `ENFORCED-PLATFORM:<primitiveId>` is not a member of the test-execution enforcement vocabulary. Admitting it requires a successor truth-table profile and a successor test-execution schema. The mandatory sentence again says OpenSIP does not prevent network access or other effects.
- `test-execution.schema.json` `EnforcementValue` (lines 7-14) is `DISCLOSURE-ONLY`, `ENFORCED-BY-CONSTRUCTION`, and `ENFORCED-AT-HOST-BROKER`. Its description requires that same truth-table and schema successor before `ENFORCED-PLATFORM` can be claimed.

An S10 matrix change does not by itself replace the native admission record, the test-execution schema, or those mandatory sentences. M5 `execution.rs` is an implementation owner (BP:992), not those successors.

**Fix.** Add the native §5.2 admission and disclosure join, the WS test-execution schema join, and the measured truth-table profile to CF-1, or name them as an M5 successor package that is accepted before `execution.rs` claims confinement or container enforcement. Keep repository-code execution out of M3. Preserve the worker prohibition and the closed DR-128 untrusted-code scope.

## Non-blocking observations

**NBO-1.** `policy.rs:1086` is the pack lookup. The `NotBundled` return is `policy.rs:1087`. `policy.rs:1399` is the Plan-pack lookup. `PLAN_POLICY_PACK_NOT_BUNDLED` is `policy.rs:1401`. X12:125 starts the order rule (admission before Plan construction). The Plan builder taking policy only from an `AdmittedPack` is X12:134.

**NBO-2.** NE:2534 names `workerExecutesRepositoryCode`. The constant `false` is NE:2535.

**NBO-3.** COV:4770 is DR-G14's milestone M3. COV:4772 is the `installation.rs` owner string. The module's first milestone M5 is COV:8976. The recommendation bullet lists 4772 and 8976 together as the M5 cite.

**NBO-4.** The r2 response row says M3-L's acceptance gate covers the S-OP-4 join. The gate sentence requires S-M, complete T2 (T2b), Q0, D3, D13 and the D2 draft, S-OP-2 drafted, O1, and O7 decided. The join is listed in the law's contents.

**NBO-5.** AQ:344 also says G09 and G30 exercise the item-4 refusal and authority boundaries. M3-CF's gate column lists G21 and G29.

**NBO-6.** M3-L carries how providers launch under the O7 decision, and the O7 section also assigns launch rules to the D law.
