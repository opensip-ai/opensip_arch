# GROK2 fact review — M3 analysis-quality plan r2

Verdict: **REQUIRED-FINDINGS**.

Subject: `docs/implementation/m3/analysis-quality/PLAN.md`, 58201 bytes, sha256 `dd351ffe79b59f920b91da6372c7f132c1e9e69ea20bf1fd280b942f1d1936ed`. That matches the request pin. The r1 snapshot `PLAN-r1.md` is unchanged at `4e1c0901…`. Read-only. No product code was run. `~/Library/Application Support/OpenSIP` was absent. The private 413 fixture was not opened.

r2 is still a plan. It changes no contract. Owner decisions D4, D5, D6, D9 (timing), D10, D11, D14, D15 and D16 were checked for recording accuracy only.

## r1 findings

All seven are fully resolved.

| ID | Resolved | Where |
|---|---|---|
| RF-1 | yes | PLAN:47, PLAN:96, PLAN:309. Median elapsed time and the maximum of the seven peak-RSS samples; 1.20× median time and 1.25× peak RSS. AQ:268-272 and RS3:78-101 say that. RSS is no longer called a median. |
| RF-2 | yes | PLAN:48, PLAN:91-93. D-007 item 8 is the typed refusal (CD:885-888). DR-G25 is Coverage-indeterminate for a missing required TypeScript semantic rung, with no silent fallback for closure, resolution, external-world and Coverage deficiencies (QG:507-511). Routed to M3 at BP:1029. |
| RF-3 | yes | PLAN:49, PLAN:105. The shape is `finding3` at IE:190 and `FindingSurface` at CS:1635-1648. O5 is the absence of a scope statement, suggested action and quality requirement. |
| RF-4 | yes | PLAN:50, PLAN:335, D12 at PLAN:516. D-102 adopts the hosted fleet class for G03/G04 and does not name G13 (CD:3980-3986). D-006 leaves `analyze` RSS out (CD:761-764). The reference runner is a new proposed decision. |
| RF-5 | yes | PLAN:51, PLAN:401-407, D13. RS3:4-18 is a closed object (`additionalProperties` false, required list ends at `qualificationRequestId`) and has no `standing`. Exploratory results use a separate envelope. AQ:212-214 remains the synthetic-report rule. |
| RF-6 | yes | PLAN:52, PLAN:192. `corpus fetch` is a separate networked harness step. Exploratory and qualification runs read pinned local bytes with no network (AQ:346, QG:117, AQC:139). |
| RF-7 | yes | PLAN:53, PLAN:262-271. Differentials stay outside G13, never as an oracle. BP:716-717 is used only for the implicit PATH or system-compiler fallback, which is what those lines say. A case counts only after adjudication. |

## New findings

### RF-1 — Product RSS is defined as the opposite of the preview method it cites

PLAN:311 says RSS is the high-water mark of the concurrent process tree's summed RSS, and not a sum of separate peaks, citing AQC:142-146.

AQC:142-145 says the budget is peak RSS of the whole host-plus-worker process tree, measured as the high-water resident sum over the supervised process tree. It does not reject a sum of per-process peaks. The completed profile for that same workload states the method in full at LQM:925: sum resident bytes across simultaneously live supervised processes, sample every 10 ms, also read per-process high-water counters, report the maximum observed sum and the sum of the individual high-water counters, and use the larger as the conservative budget value. A missing child counter is NON-PASS.

A gate that drops the sum of per-process peaks accepts runs the preview method would fail. PLAN:313 correctly keeps the preview's p95 sample regime on the preview. That does not make AQC:142-146 a citation for excluding the sum of peaks.

**Fix.** State both quantities. If the product cells follow the preview method, the value that meets the budget is the larger of the two. If the product cells use only the concurrent sum, record that as a new measurement choice and stop attributing it to AQC:142-146.

### RF-2 — INC-1 misstates what facts and Coverage bind, and INC-4 then requires those identities to match across a new snapshot

PLAN:352 says facts, scopes and Coverage bind their snapshot and Plan, citing IE:177-182, and that full replay of an old Run is not evidence for a new snapshot, citing IE:1586-1592. PLAN:364 then requires paired full-versus-incremental sequences, including body edits and insert/delete, to give canonically equal findings, facts, Coverage and replay outcomes.

IE:177-182 is the domain-table header through `plan2`. The rows the sentence names are the next ones:

- `scope2` (IE:183) binds the snapshot, not the Plan.
- `fact2` (IE:184) binds the snapshot, not the Plan.
- `coverage2` (IE:185) binds the scope, not the Plan.

`view2` (IE:186) is the record that binds a Plan together with scopes, facts and Coverage.

IE:1586-1592 says a policy or waiver change needs a separately admitted Plan and Run, that `close_run` performs complete replay, and that cache and storage admission against an authoritative Run inherit that replay. The sentence "New source or policy creates a new Plan/Run" is IE:1605-1606. It does not say that replaying an old Run fails as evidence for a new snapshot, and it is outside the cited range.

The cache half of INC-1 is right. IE:1615-1626 admits a hit only against the closure this Run requires, including this Plan and this snapshot's scopes, and a cleared hit is reusable producer output, never evidence authority, and never a re-sealed Run.

INC-2 is compatible with that cache rule. IE:1580-1584 reconstructs the Run being sealed from its retained closure. A cache hit feeds producer output into that reconstruction. It does not carry the old Run's standing. "Reconstructed" here is not a ban on the INC-1 hit.

INC-4 is not compatible with `fact2`. A body edit is new source. INC-1's own rule, read against IE:1605-1606 and `snapshot2`, makes a new snapshot, and `fact2` includes that snapshot, so the fact identities differ. Replay of the two Runs recomputes different Run IDs. PLAN:300 already says IDs are not expected to match across different Plans. INC-4 does not say that.

**Fix.** Cite IE:183-185 and say scope and fact bind the snapshot, and Coverage binds the scope. Point the new-source sentence at IE:1605-1606, and do not use IE:1586-1592 for a new-snapshot rule those lines do not state. Keep the cache-hit sentence. Make INC-4 compare the semantic payloads and correspondence the contract treats as comparable, and exclude `fact2`, `coverage2` and Run identities that contain the snapshot or the Plan.

### RF-3 — INC-6 cites the writer lease for a grant that is not there

PLAN:368 says the single writer and the current grant are preserved, citing IE:1657-1660.

IE:1657-1660 is the per-project lifecycle lease: one writer holds the fence through source admission, evaluation and atomic commit, and read-only clients take a committed snapshot. Those lines do not mention a grant. `executionCapableResolution` is explicitly not a host execution grant; the grant is the operational `RepoExecutionGrantV2` reference outside the Plan (NE:1273). IE:467 and IE:1702 name that grant elsewhere.

**Fix.** Keep IE:1657-1660 for the single writer. Name `RepoExecutionGrantV2` at its own citation as the grant the resident host preserves.

## Checked, and not findings

**Statistics.** With zero errors, the one-sided 95% Clopper–Pearson lower bound is `0.05^(1/n)`. At n=298 it is 0.9899976, below 0.99. At n=299 it is 0.9900309. At n=28 it is 0.89853, below 0.90. At n=29 it is 0.90186. PLAN:218's n ≥ 299 and n ≥ 29 are right, and PLAN:133's "about 299" is right. Strata are not pooled. The advisory sample of at least 100 is the plan's own sample size.

**Shared corpus tuple.** Ten capabilities use one `corpusCases` tuple for their TS/JS modes and both Rust modes: `syntax`, `imports`, `references`, `calls`, `types`, `reachability`, `unresolved-edge`, `clones-fact`, `clones-near` and `inventory`. `clones-cross-tsjs` does not: its Rust modes are `NOT-SELECTED` with an empty tuple. PLAN:101's count is right. The 66 cells are 57 `SUPPORTED-DESIGN`, 6 `UNSUPPORTED-TYPED` and 3 `NOT-SELECTED`.

**INC-5.** BP:717 says the current worker protocols are TS2/Rust3. The handshake names are on BP:719. The protocols are not unselected.

**Cold fixtures and the D12 worker.** LQM:923 is the cold definition (new process, empty disposable analyzer cache). AQ:279-280 keeps cold and retained-evidence workloads as separate fixtures. AQC:138-141 is a dedicated four-vCPU / eight-GiB worker at concurrency 1. D12 takes that worker shape. The same lines also carry the preview's five warmups and 30 samples; PLAN:313 leaves that sample regime on the preview. AQ:229-230 and AQ:238-239 are the per-profile lane and the one-report-per-lane rule the budgets sit on.

**Other new citations that match.** WS:593-610 is `PolicyDocumentV2` under strong Kleene, including a true `exists` on a match under incomplete Coverage (WS:600-604). WS:1163-1165 is the graph-query bound. NE:2113 is RC-2. NE:2230-2235 is dynamic-edge propagation. NE:2237-2242 is `deadCodeRepairEligible`. NE:2260 starts sufficiency v2. NE:1233-1237 is `mixed-native-partial`, and §4.2 uses it that way. NE:304-306 is `.py` as `unsupported-file` / `no-bundled-grammar`. NE:1261-1276 contains `dependencySourceSetId` and `preparedOutputSetId`. IE:1563-1567 is the unmatched state. IE:199-213 excludes concrete evidence from the fingerprint. CH13:37-40 enables no additional rule pack. CH13:94-98 is the three-way omission distinction. SMAP:67 and CH13:77-84 require the real-repository measurement and invent no numeric target there. BP:887-888 puts complete CLI `analyze` at M4. BP:696-697 requires a grammar-registry successor for a new grammar. Chapter 10 line 41 requires an explicit support decision for another language. `14-repository-and-module-layout.md:474` gives `agent_server` no alternate admission or mutation authority. REG:315 is DR-126 SATISFIED for the preview baseline. REG:435 binds four canonical machine IDs. REG:402 leaves D-372 condition 5 NOT MET. SYN:290 is the corpus sentence; SYN:297-299 says the synthesis is steering advice. AQC:52-63 is the one preview rule, `module-import-cycle`.

**Owner-decision recordings.** D14 names Apache-2.0 and design-repo commit `eb439532`. That commit adds `LICENSE`, and the file is the Apache License 2.0 text. The product repository has no `LICENSE` yet, as PLAN:527 says. D16's directory `docs/implementation/m3/record-hygiene/` exists and holds a proposal. D6 gates T3 on that licence unit. D9 leaves the analyzer open and pins Python T2 during M3. D10 and D11 match the rows above. D4 and D5 are recorded as decided targets with the revisit and the staging the plan states; their merits were not reviewed.

## Non-blocking

1. **PLAN:202 and D15.** SMAP:54 is FW-01, zero-config/recommend. SMAP:67 is FW-14, the real-configuration corpus. Neither line names a workspace assembled from separate repositories. §11 already says a SMAP or discovery successor if needed. The owner decision itself stands.
2. **PLAN:331.** "How far the unaffected units progressed (NE:1233)" uses the `mixed-native-partial` outcome as if it were a progress report for the missing-input, stale-output and broken-build controls. §4.2's citation of the same line is the accurate one.
3. **PLAN:301.** IE:1804-1806 lists independent replay across machines as one pre-shipping implementation acceptance item. It does not define equality under varied traversal order. PLAN:300's comparison rule is the plan's own, and it is the right place for the ID exception INC-4 needs.
4. **PLAN:358.** NE:1276 is the rust-v2 resolved-inputs rule that any field change changes `PlanId`. TypeScript binds `PlanId` through the context digest at NE:1576-1581. The effect matches; the cited sentence is the Rust rule.
5. **PLAN:190.** The no-telemetry sentence is QG:271. CH13:82-84 says not to collect private repositories, and it invents no numeric target.

## Purpose

The plan names the catalog, the corpus tiers, the scoring unit, the confidence rule, the exploratory envelope, the milestone split, and a decision for every successor it needs. What is still wrong for that purpose is the three findings above: the RSS value a budget compares, the identity equality an incremental law would require, and which grant the resident host preserves. Nothing further is missing once those three sentences match the contracts they cite.
