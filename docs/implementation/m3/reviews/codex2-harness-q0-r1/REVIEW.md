# CODEX2 review: M3-Q0 quality-harness design record r1

**Verdict: REQUIRED-FINDINGS.**

The cluster-product bound is valid under the stated independent-family assumption, and the 29/299 minimum-family counts correctly prevent an all-success clustered sample from inventing independent evidence. Eight design revisions remain: sound label reuse; advisory allocation; the advisory census guard; the M3 execution boundary; lifetime RSS counters; metric denominators; incomplete performance records; and K2's independence gate.

This is a method/design review. It accepts no contract successor, owner signoff, measurement or qualification claim.

The subjects matched REQUEST.md in both hash and byte count:

| Subject | Bytes | SHA-256 |
|---|---:|---|
| [DESIGN.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/DESIGN.md:1) | 65,990 | `22df1afb5b97f419a04e7c7cd5ffcb519f0a7311b8b4cddd7a1d90764aa831b3` |
| [exploratory-quality-envelope.schema.v1.json](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json:1) | 23,190 | `4cdfbb60b70ffaf74ddcf64c8757c6adbebe5f64cf1a0e9e3c7a915149064877` |

Locations below are repository-relative. AQP, M3-PLAN, OPP, LQM, RS3, PQV and CAN mean the files defined at DESIGN:19-31; line references were checked against the current files.

## Required findings

### C2-Q0-R1-01 (P1) — Use a sound truth-input closure before carrying labels

**Location:** docs/implementation/m3/harness/DESIGN.md:218-227 (§3.3, QD-5)

**Problem.** Detector independence alone does not make the lexical/witness TRI a conservative truth-input closure. It can remain unchanged after an input change that invalidates the old label.

**Evidence.**

- **docs/implementation/m3/harness/DESIGN.md:219-222:** Existential TRI includes the declaring/witness files and manifest/configuration files; a tree-only change with identical TRI permits carry.
- **docs/implementation/m3/harness/DESIGN.md:220,226:** Universal-negative TRI uses original identifier/module tokens and selected dynamic constructs; the incoming-reference trigger relies entirely on that digest.
- **docs/implementation/m3/analysis-quality/PLAN.md:257-261:** Carry requires unchanged recorded truth-relevant inputs; subject/reference and unexplained detector-output changes require re-adjudication.
- **Analytic counterexample; no files or product runs:** main.ts imports './missing', labelled true for unresolved-import. Adding missing.ts resolves the import without changing main.ts, manifests or old witness files. A detector that still misses the target can emit the same evidence. The proposed TRI stays identical and carries the stale true label. Alias/re-export consumer edits also need not contain the original identifier or declaring-module specifier, defeating the claimed referrer over-approximation.

**Fix.** Use a full selected-universe tree/enumeration and resolution-input digest as the conservative fallback, including additions, deletions and previously absent resolution candidates. Permit narrower rule-specific closures only after an independent soundness argument covers aliases, re-exports, configuration, generated inputs and negative searches. Re-adjudicate when that closure changes. Compare unchanged input components separately from output evidence/message fields in the unexplained-output trigger.

### C2-Q0-R1-02 (P2) — Make advisory allocation meet the accepted sample floor

**Location:** docs/implementation/m3/harness/DESIGN.md:341,433,443 (§5.2, §5.7, §5.8)

**Problem.** The capped per-family allocation can leave available findings unlabelled while selecting fewer than the accepted minimum of 100. The practical vote-cost example also describes one finding per family below the design's own 100-family branch.

**Evidence.**

- **docs/implementation/m3/analysis-quality/PLAN.md:228:** Advisory rules require a stratified sample of at least 100 per rule/language, or all findings when fewer exist.
- **docs/implementation/m3/harness/DESIGN.md:433:** Below 100 families the allocation caps each family at ceil(100/k), with no redistribution of unused slots.
- **Analytic counterexample; no product run:** For k=29, one family has 100 findings and 28 have one each. The cap is four, so the design selects 4+28=32 of the 128 available findings.
- **docs/implementation/m3/harness/DESIGN.md:443:** The suggested 30-50-family one-finding sample and 60-100 votes do not by themselves meet the advisory sample floor or the below-100-family allocation.

**Fix.** Preregister an allocation that reaches the accepted total whenever enough findings exist, redistributing unused slots while preserving uniform selection within each family. State the rule/language and mode allocation, including held-out-only evidence. Record population and sample sizes separately and use the sampled per-family denominator for the bound. Update the practical cost estimate, including two votes and calibration, to match this allocation.

### C2-Q0-R1-03 (P1) — Define the advisory census guard and separate its population from the sample

**Location:** docs/implementation/m3/harness/DESIGN.md:231-238,369,407-414,433; docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json:304-335

**Problem.** The status rule requires exact pooled corpus precision, but advisory adjudication supplies only a sample. No rule assigns labels to the unadjudicated population, estimates its pooled precision, or prevents the sample ratio from being used as the claimed census.

**Evidence.**

- **docs/implementation/m3/harness/DESIGN.md:235,341,433:** Advisory evidence consists of sampled findings; full adjudication is required only for gating/repair-eligible findings.
- **docs/implementation/m3/harness/DESIGN.md:407,412:** The guard is true/all reported on the frozen corpus and determines FAIL before the confidence-bound pass.
- **docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json:304-319,330-335:** Only one findings/label-count set is carried, including censusPrecisionPpm; there are no distinct corpus, sampled, settled and unlabelled denominators.
- **Analytic counterexample; no product run:** With 100 families, let one have 10,000 findings at precision 0.80 and the other 99 have one true finding each. The pooled corpus precision is 8099/10099, about 0.802. The one-per-family sample can be all true and pass the advisory bound. Calling that sample's 1.0 ratio a census defeats the large-repository guard.
- **docs/implementation/m3/analysis-quality/PLAN.md:232,238; docs/implementation/m3/harness/DESIGN.md:233-236:** Conservative precision and the separate corpus/sample/independent-unit populations must remain explicit.

**Fix.** Specify an implementable guard: obtain complete labels, or use a preregistered conservative verified-true/corpus-total guard, or explicitly route another pooled-precision inference rule for approval. If the required guard is unavailable, report that fact and prohibit PASS. Carry corpus, sampled, settled, pending and unlabelled counts separately, with the denominator used for each family estimate and each pooled statistic. An unweighted stratified sample ratio must never be named census precision.

### C2-Q0-R1-04 (P1) — Keep repository-executing tools outside M3

**Location:** docs/implementation/m3/harness/DESIGN.md:493-497,746 (QD-17, OI-6)

**Problem.** The availability of an O7 profile or disposable container is presented as permission to run repository-executing differential tools and Rust compile validation. That condition does not satisfy the accepted categorical M3 prohibition.

**Evidence.**

- **docs/implementation/m3/harness/DESIGN.md:494-496:** The record identifies build scripts, proc-macros and repository configuration evaluation, then permits those tools once a profile or container is available.
- **docs/implementation/m3/harness/DESIGN.md:746:** OI-6 repeats profile/container availability as the gate for the Rust differential and mutant compile checks.
- **docs/implementation/m3/M3-PLAN.md:301,355-356:** No repository-code execution in M3; prepared sets are imported and the worker prohibition stands.
- **docs/implementation/m3/M3-PLAN.md:347-352:** Later M5 execution has its own successor/authorization path; O7 provider hardening does not replace it.

**Fix.** At M3 permit only tool modes whose pins verify that no repository code executes. Defer executing differentials and compile validation to the later explicit authorized execution path and applicable successors. Treat confinement/container availability as an additional execution condition, never the authorization or milestone gate. Update QD-17 and OI-6 together.

### C2-Q0-R1-05 (P1) — Specify lifetime per-process RSS counters and complete process accounting

**Location:** docs/implementation/m3/harness/DESIGN.md:611-621 (§9.3, QD-19)

**Problem.** QD-19 names wait4 for the direct child but only a polled peak for other descendants. It does not identify a lifetime counter source, final collection or complete descendant registration. Sampled observations and an unspecified host peak cannot establish the required sum of individual high-water counters.

**Evidence.**

- **docs/implementation/m3/harness/DESIGN.md:612-619:** Concurrent RSS is sampled every 10 ms, while the proposed individual source is wait4 for the direct child and a polled per-process peak for descendants, combined with an operational-record peak.
- **docs/coop/completion/language-quality-matrix.completed.v2.json:925; docs/implementation/m3/analysis-quality/PLAN.md:329:** The accepted method requires both sampled concurrent sum and each process's own high-water counter; missing child counters are NON-PASS.
- **docs/implementation/m3/operability/PLAN.md:249:** The operational record promises peak RSS per process but does not itself specify the lifetime counter or collection protocol.
- **Linux kernel /proc documentation:** VmHWM is a peak resident-set field distinct from current VmRSS. A maximum of current-RSS polls is not that lifetime counter. [Primary documentation](https://docs.kernel.org/filesystems/proc.html).
- **Apple wait4 documentation:** Returned resource usage covers the terminated process and its children; the design must specify field-specific own-versus-aggregate semantics rather than assume an own-process reading. [Primary documentation](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/wait4.2.html).
- **Analytic observation; no process launched:** A descendant or an allocation spike can exist entirely between polls. Without launch/exit registration and final counter collection, an unobserved process cannot even trigger the stated missing-counter check.

**Fix.** Name the macOS and Linux lifetime counter APIs/fields, their units and own-versus-aggregate semantics. Register every supervised descendant and retain its final own counter through exit/reaping. Define de-duplication and how host observations are joined to the same process lifetime. Preserve the two accepted RSS quantities; incomplete process inventory or counter collection is an explicit NON-PASS, never replaced by sampled peaks.

### C2-Q0-R1-06 (P2) — Carry the missing metric denominators and repository-level results

**Location:** docs/implementation/m3/harness/DESIGN.md:693,707,711-712; docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json:304-338,477-537

**Problem.** The claim that every result carries explicit counts is false for Q2 noise, Q6 yield and Q7 scoring. Family aggregation also replaces the accepted per-repository precision report. Definition digests alone do not supply these measured populations.

**Evidence.**

- **docs/implementation/m3/analysis-quality/PLAN.md:151-152,238,408-411,422:** Noise is per rule/repository with hand-written-line counts and generated/vendored separation; yield reports its answerable population; per-repository precision is required; explanation field/proof checks and a 50-per-rule rubric sample must be reportable; every denominator is pinned.
- **docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json:321-338:** Q2 has optional aggregate per-million-line rates and family rows, but no repository rows or analyzed-line denominators.
- **docs/implementation/m3/harness/DESIGN.md:345-349:** A family may contain multiple repositories, so per-family precision cannot substitute for per-repository precision.
- **docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json:477,511:** Q6 carries yieldPpm without determinate and answerable counts.
- **docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json:522-537:** Q7 has fieldPresencePpm and rubricAverageMilli but no fields-present/required counts, scored population or score sum, and no per-rule rows. Even status=measured requires no measurements.
- **docs/implementation/m3/harness/DESIGN.md:693:** The D13 requirement is claimed to be met because every result has explicit counts.

**Fix.** Add closed per-repository Q2 rows with pinned repository/workload identity, family membership, label/population counts and line counts by class. Add Q6 yield numerators and denominators. Add per-rule Q7 sample counts, score totals or histogram, field/proof populations and disposition accounting. Require those fields when the section is measured; retain explicit not-measured states. Use digest-linked measured records instead if their shapes and joins are defined here. Update §11/§12 to match the actual carrier.

### C2-Q0-R1-07 (P2) — Represent incomplete performance measurements without inventing samples

**Location:** docs/implementation/m3/harness/DESIGN.md:621,635,641; docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json:78-83,477-512

**Problem.** The closed Q6 shape cannot express the design's required missing-counter NON-PASS or the reason for a missing operational record. It requires complete positive arrays and permits only within, over or no-baseline.

**Evidence.**

- **docs/implementation/m3/harness/DESIGN.md:621:** A process with no counter makes the run NON-PASS.
- **docs/implementation/m3/harness/DESIGN.md:635:** Missing operational records produce null phase fields and a reason; nothing is synthesized.
- **docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json:78-83,477-488,503-512:** Seven positive values are required for each RSS series. There is no incomplete/invalid status, missing-counter field or absence-reason member.
- **docs/implementation/m3/harness/DESIGN.md:641; docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json:237-242,477-512:** Both retry batches must be retained with the second verdict final, but the carrier does not define batch identity/order or a link between separate envelopes.

**Fix.** Define a closed incomplete/invalid measurement variant with typed failure/absence reasons and unavailable samples represented explicitly. Such results cannot be within budget or Q6 PASS. Keep measured values that do exist; do not omit failed runs or fabricate RSS. Define batch identity, first/retry ordering and final-verdict selection, either within the envelope or through explicit linked batch envelopes, so the prescribed retry policy is reviewable.

### C2-Q0-R1-08 (P2) — Reconcile the K2 estimate with the independent-oracle schedule gate

**Location:** docs/implementation/m3/harness/DESIGN.md:726-733 (§13)

**Problem.** The 15-day estimate meets the day-21 finish condition but does not explain how oracle review finishes before producer output. The same section requires that independence gate, while the cited schedule allows producer validation/output much earlier.

**Evidence.**

- **docs/implementation/m3/harness/DESIGN.md:729,733:** K2r must be done before any producer output exists, yet the conditional example starts K2 at day 0 and completes the serialized work at day 15.
- **docs/implementation/m3/M3-PLAN.md:172:** K2 is authored before producers so expected answers are independent.
- **docs/implementation/m3/M3-PLAN.md:212-217:** The bounded schedule has G2-v launch/validation at day 3, E3 at day 7, F2 facts at day 14 and G3 facts at day 15.
- **docs/implementation/m3/M3-PLAN.md:222,233; docs/implementation/m3/harness/DESIGN.md:752:** Q0 owes K2 sizing; satisfying the finish-by-21 condition is separate from the before-producer requirement. OI-12 assigns folding the result into the path but supplies no reconciliation.

**Fix.** State a feasible start date and explicit oracle-freeze/review gates before affected candidate producer outputs. K2 can be scheduled earlier as pre-day-0 work, or producer validation/output can be delayed behind reviewed lane oracles. Show the resulting branch assumptions and identify the bounds to update under OI-12. Do not claim that completion by day 15 alone preserves the cited independence requirement.

## Method assessment

**Confidence derivation.** For independent nonnegative family estimates \(X_j\), let \(\mu_j=E[X_j]\) and \(\bar\mu=k^{-1}\sum_j\mu_j\). For any positive \(m\) with \(\bar\mu\le m\),
\[
E\left[\frac{\prod_j X_j}{m^k}\right]
=\frac{\prod_j\mu_j}{m^k}
\le\left(\frac{\bar\mu}{m}\right)^k
\le1.
\]
Independence supplies the first equality, AM–GM the first inequality, and Markov bounds the probability that this product reaches \(1/\alpha\) by \(\alpha\). Inverting gives \(L=(\alpha\prod_jX_j)^{1/k}\). This proof does not require identical family distributions or a model of within-family finding correlation. If the true mean is zero, all nonnegative family estimates are zero almost surely and the lower bound is zero.

The bound concerns the average family mean under the sampling assumption; it is not evidence that the deliberately selected T2 corpus represents a wider repository population. DESIGN:355 and ENV:340-341 disclose that assumption. The proof is checked analytically; the simulation is not needed to establish validity.

| Requested check | Assessment |
|---|---|
| Estimand, method selection and exact CP (§5.1–§5.4) | Family weighting and the separate pooled guard are explicit. Structure is selected before labels. CP's IID/common-probability premise should be explicit (N01); sampled advisory findings do not establish the claimed census (R1-03). |
| Cluster method and alternatives (§5.5) | Product/Markov/AM–GM argument is correct. A family with zero precision gives zero bound. All true families give \(0.05^{1/k}\), so three families give about 0.368. Ordinary empirical bootstrap degenerates at that boundary; hierarchical/prior or assumed-correlation approaches need extra assumptions; clean/unclean reduction is valid but discards information. |
| Counts, status, acceptance and downgrade (§5.6–§5.8) | 29/299 floors, exact rational target comparisons, conservative unclear labels, specified status order, held-out-only evidence and both advisory paths follow the plan. One error needs 46/473 in the CP branch, as stated. No family-wise confidence is claimed; OI-5 remains a qualification decision. The practical zero-error wording needs N02, and advisory counts/cost need R1-02. |
| Ledger and adjudication (§3–§4) | Append-only chained history, hard input bindings, frozen rubrics, blind presentations, calibration exclusion, same-model grouping, implementation-context conflicts, a human vote and domain-expert escalation are operational. The calibration bar is a design control, not a statistical guarantee of label truth. TRI is unsound as written (R1-01). |
| Recall, honesty and mutation (§1.3, §6–§7) | Candidate Coverage cannot choose answerability. Positive abstentions are misses; false completeness is release-blocking Q4; sound positives under deficiency are permitted. Mutant terminal states, independent checks, validator audits and next-round curated differentials are specified. Execution-dependent tools must remain outside M3 (R1-04). |
| Stability and determinism (§8) | Generator-independent declaration matching plus human review is present; content/proof/Coverage and both spurious delta directions are compared. The 20-unaffected-findings floor prevents a vacuous pass. Traversal, concurrency, scratch and environment variants are defined; compatible cross-lane runs and moved/renamed correspondence are expressly deferred. Rust's restricted invariant check needs the eligibility limit in N05. |
| Resets, phases, retry and D12 (§9) | Cold reset is repeated for every run including warmups; warm fixtures prime once and use new processes with retained declared caches. Product 3+7/median/max statistics are correct. OPP's phase inventory and nonsemantic reuse route are preserved. The second full CI batch is chosen by a predetermined rule, with both batches retained and flips reviewed. Lifetime counters and their carrier need R1-05/R1-07. D12 runner and signoff are specified separately from other machines. |
| D13 carrier (§11, ENV) | Separate RS3 digest/schema references and fixed nonqualifying declarations comply with AQP:419-425. Every object schema is closed. Integer fields together with mandatory CAN parsing/canonicalization reject lexical floats; the schema alone is not that parser. Missing measured populations and failure shapes require R1-06/R1-07. |
| Q0 scope and K2 (§13) | Case model, catalog specs, ledger, confidence method, runner requirements, envelope and a serialized 15-day K2 estimate are supplied. The sizing arithmetic is correct. Its oracle-before-output requirement needs an explicit schedule gate (R1-08). |

D12/D13, the D2 product pack, D7/D8 and the DR-G13 qualification successor remain separately owned open items. This review does not require them to be accepted as part of Q0, nor does a draft exploratory PASS qualify a release.

## Non-blocking observations

### C2-Q0-R1-N01

**Location:** docs/implementation/m3/harness/DESIGN.md:326-355,375-377,744-745

The family-weighted lower bound is not a population finding-weighted lower bound, and a corpus census guard does not make it one. OI-4 explicitly leaves that estimand choice to the qualification successor, which is an appropriate boundary for this exploratory design. A family can contain several repositories. One finding per family also establishes distinct evidence units, not by itself IID/common-success-probability Bernoulli observations.

**Follow-up.** Name the estimand explicitly in reported results, prefer 'family-weighted' where that is the actual weighting, preserve OI-4 and OI-5 before qualification, and state the IID/common-p premise of the CP branch. Keep the product method's validity for heterogeneous independent family means distinct.

### C2-Q0-R1-N02

**Location:** docs/implementation/m3/harness/DESIGN.md:364,405,441-443,724

The formal 29/299 floors and the one-error 46/473 examples are correct. However, §5.8 says a gating PASS needs zero errors, although larger samples can pass with errors. The 'no method can do better' argument is specifically an all-success-boundary limitation. The 299-success displayed value 0.990031 uses nearest rounding; the required downward stored bound is 990030 ppm, relevant to K1b's reference self-test.

**Follow-up.** Say 299 error-free families suffice at the minimum; errors require more evidence. Limit the optimality claim to its proved boundary. Mark display approximations separately and supply the correct downward-rounded integer reference values.

### C2-Q0-R1-N03

**Location:** docs/implementation/m3/harness/DESIGN.md:7,383-386,764

The record reports a 4,000-trial-per-scenario simulation and empirical frequencies, while the standing and final disclaimer say nothing was run and §5 contains only arithmetic. This does not invalidate the analytic proof, but the provenance statements contradict each other.

**Follow-up.** Distinguish 'no product measurement or corpus run' from the method simulation. Give its seed/code digest and retained output if using it as supporting evidence, or remove the empirical claim and rely on the proof.

### C2-Q0-R1-N04

**Location:** docs/implementation/m3/harness/DESIGN.md:215,227,281-301,453-465,509,655-657; docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json:178-194

Several operational details should be explicit before implementation: unchanged input components versus output fields in the unexplained-change trigger; the ordered rater slots or pair-specific calculation used for Cohen's kappa; persistent held-out reservation/exposure history; and the carrier for load, frequency, swap, power and local-disk observations.

**Follow-up.** Use §418's never-inspected condition as the controlling acceptance gate across rounds, so rotating a freeze seed or curating a differential cannot restore exposed cases to held-out standing. Define kappa's rater populations, and map QD-21 observations to a closed runner or digest-linked operational record.

### C2-Q0-R1-N05

**Location:** docs/implementation/m3/harness/DESIGN.md:139-145,535

The catalog field citations to AQP:169-175 are shifted by one for subject population through default; AQP:168-174 are the corresponding rows. Rust's syntactic mod tree plus an unchanged manifest is also a limited check, so Q5 validation must not treat unsupported use/cfg/macro resolution as proven preserved.

**Follow-up.** Correct the field citations. Document the restricted Rust refactor domain and discard/unvalidate pairs when the independent resolution invariant cannot be established; expand the semantic oracle in the later full Q5 suite.

## Review boundary

The complete two subject files, the request, relevant accepted AQP/M3/OPP sections, prior CODEX2 r2/r3 confidence reviews, RS3/PQV/CAN, the QG DR-G13 row and cited contract/matrix passages were inspected. Primary OS documentation was consulted for counter semantics. Supporting agents independently checked statistics, operational method and carrier/schedule consistency; the verdict and findings were consolidated by CODEX2.

Read-only inspection and analytic reasoning only. No product code, builds, tests, corpus fetches, benchmarks or qualification runs. No access to the real OpenSIP runtime home or the 413 fixture. No commits. Only `REVIEW.md` and `review.json` are written under `/tmp/opensip-implementation/reviews/codex2-harness-q0-r1/`.
