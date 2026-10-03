# GROK2 review: M3 analysis-quality plan, r1

**Verdict: REQUIRED-FINDINGS.**

Fact validation only. Claude Opus 5.5 leads. CODEX2 reviews method in parallel. This review did not run product code or tests, did not edit the repository, and did not read the private 413 fixture. `~/Library/Application Support/OpenSIP` was absent at the start and at the end.

## Subject

`docs/implementation/m3/analysis-quality/PLAN.md`

- 28038 bytes
- sha256 `4e1c090112ec7480753425605de052c77d2e36e6981bea493e437a3fe7145203`
- Matches the request pin.

The plan is a plan. It changes no contract by itself. The findings below are statements about the existing design that are not what the cited text says, or proposals that conflict with an accepted contract or gate and are not named as a successor in §11.

## Required findings

### RF-1. Product performance is median time and maximum RSS

§1 and §5.1 say each benchmark takes the median of 7 runs after 3 warmups, and that a regression fails above ×1.20 time or ×1.25 RSS (PLAN.md:42, PLAN.md:183), citing AQ:273-287.

`admission-and-qualification.md:268-272` records 3 warmups and 7 measured runs, then says the gate calculates **median elapsed time** and **maximum RSS**. The limits are 1.20× median time and 1.25× peak RSS. The report schema stores seven `elapsedNanos` samples and seven `peakRssBytes` samples (`product-quality-report.schema.v3.json:78-101`). The ×1.20 / ×1.25 ratios and the 3-then-7 sample shape are right. Applying "the median" to the benchmark as a whole is not.

Fix: say median elapsed time and maximum of the seven per-run peak RSS samples.

### RF-2. D-007 item 8 is a refusal, not an indeterminate rung

§1 states one decided rule: a missing semantic rung is typed and indeterminate, never a weaker answer, and cites D-007 item 8 together with DR-G25 (PLAN.md:38).

D-007 item 8 (`COORDINATOR-DECISIONS.md:885-888`) requires the role to **refuse**, typed and loud, rather than degrade to a weaker parser, syntactic tier, semantic model, graph, or finding model. DR-G25's acceptance text (`qualification-gates.applied.v1.json:507-508`) is **Coverage-indeterminate** for a missing required TypeScript semantic rung, with no silent syntax fallback. Its product expansion (line 511) forbids silent fallback for input-closure, resolution, external-world, and coverage deficiencies, and names stale input, provider-unavailable, and operational fault. It does not say every missing rung is indeterminate. Routing DR-G25 to M3 at `implementation-boundaries-and-build-plan.md:1029` is right.

Fix: state the refusal rule and the indeterminate-rung rule as two decisions.

### RF-3. Findings do not carry only messageCode and parameters

O5 says findings carry `messageCode` and parameters only, cited to IE:1282-1286 (PLAN.md:50).

Those lines are the parameter-digest record `{schemaVersion, messageCode, parameters}`. The finding identity at `identity-and-evidence.md:190` is a nullable fingerprint and explicit correspondence state, rule closure and ruleId, subject3 and display attribution, message code and parameters, severity, and evidence references. `FindingSurface` requires findingId, ruleId, subjectId, subjectPath, severity, messageCode, correspondence, fingerprint, and waived (`common.schema.json:1635-1648`).

The narrower gap is real. Nothing in that shape is an explanation rubric, a scope statement, or a suggested action, and the plan is right that remedies are carried on terminations. The word "only" is not.

Fix: cite IE:190 for the finding, and describe O5 as the missing explanation fields.

### RF-4. D-102 does not hold analyze or G13

§5.2 measures the proposed budgets on the slowest D-102 runner class each size class is held to (PLAN.md:187). §9 runs M6 G13 qualification on D-102 runners (PLAN.md:271).

D-102 (`COORDINATOR-DECISIONS.md:3980-3986`) adopts the hosted fleet class for G03/G04 and says it does not name G13. D-006 (`COORDINATOR-DECISIONS.md:761-764`) binds its runner classes to the core size, startup, and memory gates and puts `analyze` RSS deliberately outside those thresholds. Repository size classes are not D-102 holdings.

Fix: name the analyze runner the plan wants. Do not call it D-102.

### RF-5. Schema v3 has no exploratory standing

§7 says an exploratory quality report uses the product-quality report schema with `standing: "exploratory"` and is consistent with AQ:212-214 (PLAN.md:230-233). §11 does not ask for a schema successor.

`product-quality-report.schema.v3.json:4-18` is `additionalProperties: false` and its required members are the digests, cells, and `qualificationRequestId`. There is no `standing`. AQ:212-214 says synthetic reports are tagged reference-only and cannot be promoted. That sentence does not add a field, and it is about synthetic reports, not about real measurements taken before qualification. O7's claim that this class is undefined is fair. The proposal that the current schema already carries it is not.

Fix: ask in §11 for a report-schema successor, and drop the claim that schema v3 accepts `standing`.

### RF-6. T2 fetch is on the wrong side of the offline rule

§4.1 says the harness fetches each public repository at the pinned commit and that no source is vendored (PLAN.md:116). No §11 row flags that fetch.

Ordinary analysis and discovery are offline, with no implicit download (`admission-and-qualification.md:346`). DR-G06's acceptance text requires supported runs with no network (`qualification-gates.applied.v1.json:117`). The preview quality workload is no-network (`analysis-quality-completion.v2.md:139`). A harness whose only copy of T2 is a fetch during the run conflicts with those rules. The plan does not say the qualified run sees only already pinned bytes.

Fix: put acquisition outside the qualified run, or name an explicit exception in §11.

### RF-7. Cross-tool recall is not already consistent with D-007 and BP:716-717

§4.4 runs Knip, ts-prune, rustc `dead_code`/`unused`, and cargo-udeps/cargo-machete, treats a miss inside claimed-complete scope as a recall miss, and says this is consistent with D-007 and BP:716-717 (PLAN.md:161-162). §9 then scores Q3 inside G13 (PLAN.md:271). §11 does not amend DR-G13.

BP:716-717 says neither PATH nor a system compiler supplies an implicit provider fallback. D-007 item 8 says refuse a weaker model. Those rules support "not a product fallback." They do not admit the tools as qualification oracles. QG items[12] evidence is per-cell exact observations, Coverage negatives, native/prototype disposition, cold/warm p95, and process-tree RSS (`qualification-gates.applied.v1.json:267-271`), not a cross-tool differential.

Fix: keep the differentials outside G13, or add a §11 decision that changes DR-G13 and states the oracle tools are pinned harness inputs and never the analyzer.

## Citations that match

These §1, §2, §4, §5, and §8 claims match the cited text.

- AQC:127-130 is exact set equality for facts, Coverage, and graph results, with finite-corpus precision and recall both 1.0. AQ:257-266 requires exact oracle equality and gate-computed counts, and it does not read a submitted PASS flag.
- The matrix is 11 capabilities by 6 modes, 57 / 6 / 3. The citation range is short; the count is not wrong. See NBO-1.
- NE:304-306: `.py` is `unsupported-file` with `no-bundled-grammar`.
- IE:188-213: `finding-key2` excludes line offsets and messages, and a rename requires explicit subject correspondence.
- WS:352-358 lists the delta classes, including `CODE-NET-NEW`. WS:437-438 says a new bug hidden by removing its detector remains `CODE-NET-NEW` and can gate. WS:466-467 says zero emitted findings never establish complete analysis.
- CH13:94-98 is the three-way split among no matches, unsupported or inapplicable, and attempted but insufficient. CH13:77-84 requires pinned real repository shapes and manual-correction counts.
- QG items[12] is DR-G13. Its `requiredEvidence` still says cold/warm p95, and its `thresholdDisposition` still says thresholds DECIDED by D-369. The productExpansion sentence on public or consented repository shapes is quoted exactly. O9 is a real inconsistency. See NBO-4 for the other copy of the p95 regime.
- NE:2237-2242: `deadCodeRepairEligible` is true only with `exportsClosed=closed`, `entryPointsRecognized=all`, and no nonliteral loading.
- The 1,019-file pin is the top-level `files` array of `quality-corpus-manifest.v1.json` (`productExecution: false`). `native-cases.v2.json` has 477 cases and status PROPOSED. AQ:244-246 calls native reference scenarios semantic obligations and says executable fixtures must be admitted before a cell is QUALIFIED. Shared case lists are real: for syntax, imports, references, calls, types, reachability, unresolved-edge, clones-fact, clones-near, and inventory, the TypeScript/JavaScript modes and both Rust modes carry the same `corpusCases` tuple.
- SYN:275-276 records resident-host and incremental/changed-scope as open gaps, not as obligations. The warm-run phrase in §5.3 matches `language-quality-matrix.completed.v2.json` `warmDefinition`: new process, retained declared cache, no reused provider process.
- `10-mvp-and-future-scope.md:41` says additional languages require a later explicit support decision. BP:696-697 requires a reviewed grammar-registry successor. DR-119 / D-008 is the self-contained closure rule. DR-G14 is routed to M3 at BP:1018.
- Register line 402: D-372 condition 5, implementation authorization, is NOT MET. The product tree at `eb0d503` contains host, storage, lifecycle, and security crates, including M2 crash-matrix work, so §10 item 10's record mismatch is real.
- §10 item 9's four denials that no quality corpus exists are at the cited places, and they sit against DR-118's SATISFIED row. Chapter 10 lines 143 and 154, inside the historical non-binding map, still say the role list is open, against line 41. The DR-011 subledger (register:77-98) still shows OPEN residuals while condition 1 (register:398) says those residuals are MET.

## Not claimed

No product command was run. No measurement in the plan was re-taken. Licence and size of the named repositories were not checked. Method and target soundness are CODEX2's review.
