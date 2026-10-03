# M3-Q0 quality-harness design record — r3

Draft r3. Claude Opus 5.5, implementation lead. Unit **M3-Q0** of the accepted M3 unit plan (`M3-PLAN.md:157`).

r1 (`DESIGN-r1.md`, sha256 `22df1afb…`, 65,990 bytes; schema `exploratory-quality-envelope.schema.v1-r1.json`, `4cdfbb60…`, 23,190 bytes) was reviewed by CODEX2 (method; `/tmp/opensip-implementation/reviews/codex2-harness-q0-r1/`), with 8 required findings and 5 non-blocking observations. r2 answers all of them. CODEX2 confirmed the cluster-product bound and the 29/299 floors as sound, so they are unchanged.

r2 (`DESIGN-r2.md`, sha256 `4225ca34…`, 91,319 bytes; schema `exploratory-quality-envelope.schema.v1-r2.json`, `df67c651…`, 50,098 bytes) was reviewed by CODEX2 (`/tmp/opensip-implementation/reviews/codex2-harness-q0-r2/`). Six r1 findings were resolved and two partly resolved, with 3 required findings and 4 non-blocking observations. r3 answers all of them and changes nothing else of substance.

## Standing

**This is a design record, not law and not a contract successor.** It changes no accepted contract, schema, gate, threshold or register row. It fixes the harness mechanisms that the accepted analysis-quality plan leaves to "the harness design" (AQP:235, AQP:480), so that K1, K2, I2, S-M and M3-M can be implemented from it directly. No product measurement, corpus fetch, adjudication or product run was performed for it. The numbers in §5 are arithmetic.

**What Q0 owes.** The M3-Q0 row (`M3-PLAN.md:157`) names the case model (AQP:130-135), the label ledger (AQP:249-263), the confidence rule (AQP:233-237), the exploratory envelope (AQP:419-425), the D12 runner, and the rule-catalog draft specs (AQP:167-191). Q0 also has to size K2, which the critical path leaves "unbounded until Q0 sizes it" (`M3-PLAN.md:222`, `M3-PLAN.md:241`).

**Who depends on it.**
- **M3-L's acceptance gate** includes Q0, D13 and the D2 draft (`M3-PLAN.md:160`).
- **S-M**'s report waits for the Q0 envelope and D13; its Q6-labelled samples wait for D12 (`M3-PLAN.md:158`).
- **K1 and K2** depend on Q0 (`M3-PLAN.md:172`), and so does **I2** (`M3-PLAN.md:171`).
- **M3-M** runs the measurement this record defines (`M3-PLAN.md:173`).

**Authority.** The mechanisms below are lead decisions (AQP:518), numbered **QD-n** so that reviewers can cite them. Three items need sign-off that this record cannot give: D12 (AQP:534), D13 (AQP:535) and the D4 revisit (AQP:525). §14 lists them.

Short names, as in the accepted plans:
- **AQP:** `docs/implementation/m3/analysis-quality/PLAN.md` (r4, accepted; lines of the live file)
- **M3-PLAN:** `docs/implementation/m3/M3-PLAN.md` (r4, accepted)
- **OPP:** `docs/implementation/m3/operability/PLAN.md` (r3, accepted; lines of the live file, which carries the acceptance note)
- **AQ / IE / NE / WS:** `docs/v2/contracts/product-v1/{admission-and-qualification,identity-and-evidence,native-evidence,workflows-and-surfaces}.md`
- **RS3:** `docs/coop/design-corrections/foundation/product-quality-report.schema.v3.json`
- **PQV:** `docs/coop/design-corrections/foundation/product-quality-validator.py`
- **CAN:** `docs/coop/design-corrections/foundation/canonical.py`
- **QG:** `docs/coop/design-corrections/qualification-gates.applied.v1.json`
- **AQC:** `docs/coop/completion/analysis-quality-completion.v2.md`
- **LQM:** `docs/coop/completion/language-quality-matrix.completed.v2.json`
- **SMAP:** `docs/coop/design-corrections/current-source-map.proposed.md`
- **ENV:** `docs/implementation/m3/harness/exploratory-quality-envelope.schema.v1.json` (drafted with this record)

---

## r3 changes and review responses

| Finding | Section | Change |
|---|---|---|
| C2-Q0-R2-01 (complete lifetime RSS) | §9.3, §9.5, ENV `runReason` | Linux figure (b) is complete only by a positive proof:<br>- an acknowledged pre-launch subscription on every online CPU, proven live by per-CPU sentinels;<br>- loss detection (receive errors and overruns, per-CPU connector sequence gaps, CPU-set changes);<br>- lifetimes keyed by (tgid, fork timestamp);<br>- one terminal record per thread group, selected by `ac_tgid` with `AGROUP`; per-thread records are never summed;<br>- draining that ends only when every lifetime has its terminal record and every per-CPU post-run sentinel has arrived;<br>- a two-channel cross-join.<br>Any failure, or anything that cannot be evaluated, is `incomplete` with a new typed reason. Completeness is never inferred from absence. K1c's calibration adds short-lived children, an early-exiting leader, induced loss and pid reuse. |
| C2-Q0-R2-02 (batch join) | §9.5, §9.6, §11, ENV | `operationalRecords[]` rows carry `batchId` and a typed run slot. Runner observations move to `batchObservations[]`, one row per batch. Per-runner calibration stays in `runner.calibration`. The validator's identity, coverage, uniqueness, orphan and sample-consistency checks are listed. |
| C2-Q0-R2-03 (slip slack) | §13 | The slip is recomputed through F1 → H → J2 with every dependency: M3-X = 26 + max(0, *s* − 3). That is 3 days of oracle slip, not 4. The split authoring/run alternative is named, and OI-12's list gains the slip rule. |
| N01–N04 | §5.2, §5.6, §5.8, §9.5 | The error wording is restricted to the Clopper–Pearson branch, with the product-branch example. The OI-17 cost estimate is withdrawn. "Exactly when" becomes "guaranteed when". Sample and reason consistency is assigned to the validator. |

## r2 changes and review responses

| Finding | Section | Change |
|---|---|---|
| C2-Q0-R1-01 (truth-input closure) | §3.3 | The truth-input digest is now the full selected-universe and resolution-input closure: the whole snapshot inventory, including additions and deletions, so a newly present resolution candidate changes it. Narrower rule-specific closures are allowed only through a reviewed soundness argument (none is admitted in r2). The unexplained-output trigger compares input components separately from output fields. |
| C2-Q0-R1-02 (advisory allocation) | §5.7, §5.8 | Water-filling allocation reaches the 100-finding floor whenever enough findings exist. Unused slots are redistributed, selection within each family stays uniform, and the floor applies per stratum and per evidence set. Population and sample are recorded separately, and the bound uses each family's sampled denominator. The cost estimate is redone with two votes and calibration. |
| C2-Q0-R1-03 (advisory census guard) | §3.4, §5.6, ENV `q2` | The guard is now two-sided and conservative. Unlabelled findings count as not true for the guard's lower value and as true for its upper value. FAIL needs the upper value below the target; a lower value below the target is INSUFFICIENT-EVIDENCE. Corpus, sampled, settled, pending and unlabelled counts are carried separately. A sample ratio is never called census precision. A sharper pooled inference rule is routed for approval as OI-17. |
| C2-Q0-R1-04 (repository execution) | §6.2, §7, OI-6 | At M3 only tool modes whose pin verifies, with a canary fixture, that no repository code executes. Executing differentials and Rust compile validation are deferred to the M5 authorized execution path (`M3-PLAN.md:347-352`). Confinement is an additional condition, never the authorization. |
| C2-Q0-R1-05 (lifetime RSS) | §9.3, QD-19 | Named counter sources and units. Every supervised descendant is registered, and its own counter is collected at exit. Lifetimes are keyed by (tgid, start time). Host values can only raise a figure, never replace one. Incomplete inventory or collection is an explicit NON-PASS, never filled from sampled peaks. macOS has no harness-readable own lifetime counter, so macOS runs are `incomplete` for RSS; this is open item OI-18. |
| C2-Q0-R1-06 (denominators) | §11, §12, ENV | Per-repository Q2 rows with line counts by class; Q3 and Q6 yield numerators and denominators; per-rule Q7 rows with populations, a score histogram and disposition counts. Measured sections must carry these fields; not-measured stays explicit. |
| C2-Q0-R1-07 (incomplete performance) | §9.3–§9.5, ENV `q6` | A closed `incomplete` variant with typed per-run reasons and null where a sample is unavailable; it can never be `within`. Batch identity and ordering: the first run is batch 1, the retry is batch 2, and the final verdict is the last batch. |
| C2-Q0-R1-08 (K2 schedule) | §13 | Each lane's oracle is frozen and reviewed before any producer output in that lane. K2 moves into the pre-day-0 window, and the M3-PLAN bounds to update under OI-12 are listed. |
| N01–N05 | §5, §4.4, §1.4, §2.1, §8.3, §9.6 | "Family-weighted" naming; the IID premise of the Clopper–Pearson branch; correct rounded-down reference values; the simulation claim removed in favour of the proof; κ rater slots; persistent held-out exposure; runner observations carried; AQP:168-174 field citations; the restricted Rust refactor domain. |

---

## 0. Ground rules the harness inherits

These come from accepted law. The design keeps every one of them.

- **Expected answers are independent.** A report cannot supply or alter its own expected subject, answers, runner or baseline (AQ:196-198). The gate computes counts and correctness itself and reads no PASS flag (AQ:263-266; PQV:24-27). K2 is authored before the producers for this reason (`M3-PLAN.md:172`).
- **RS3 is closed.** It has `additionalProperties: false` and a fixed required set (RS3:4-18), so it carries no `standing` member (AQP:419). The harness never adds a field to it.
- **The product statistic** is 3 warmups, then 7 measured runs; the median of the elapsed times and the maximum of the peak-RSS samples; 1.20× and 1.25× against a reviewed baseline; plus reviewed absolute bounds (AQ:268-276; RS3:78-101). The reference gate takes `sorted(elapsed)[3]` and `max(peakRss)` (PQV:28).
- **Offline runs.** Ordinary analysis and discovery are offline (AQ:346). Corpus acquisition is a separate, explicit, networked harness step, and runs read only pinned local bytes (AQP:207).
- **No repository code executes at M3** (`M3-PLAN.md:355`). S-P and S-M execute no build script, proc-macro or package script (`M3-PLAN.md:158`).
- **Freeze before measuring.** Metric definitions, denominators, rubrics and held-out sets are frozen and digest-pinned before any acceptance measurement (AQP:159).
- **Exploration is never promoted.** A G13 qualification run re-executes from scratch on the D12 lanes against the held-out set (AQP:433).

**Canonical bytes.** Every harness record digested below is serialized with the foundation canonicalization: sorted keys, compact separators, UTF-8, no floats, at most 4 MiB (CAN:67-74; floats are refused at CAN:61). **QD-1:** proportions and bounds are therefore stored as integer millionths (`…Ppm`). A lower bound is rounded down and an upper bound up, so rounding never helps a pass. Every pass/fail decision is computed in exact rational arithmetic (§5.6), never from the rounded value.

---

## 1. The case model

### 1.1 Case kinds

One record type, with a `caseKind` discriminator. Each kind maps to one accepted measurement.

| `caseKind` | Measures | Source of the expected answer |
|---|---|---|
| `cell-observation` | Q1, and Q4 on T1 | T1 oracle fixture: exact atoms and exit (AQ:240-246, AQ:256-266) |
| `finding` | Q3, Q4, and Q2 calibration items | the corpus oracle: T1, a validated seed, a fix reversal, a lookalike or a curated differential case (AQP:267-289) |
| `refactor-pair` | Q5 survival | the independently reviewed mapping oracle (AQP:306) |
| `determinism` | Q5 determinism | equality of canonical results (AQP:316-319) |
| `workload` | Q6 | the pinned workload manifest (AQP:333-338) |
| `config-shape` | Q8 | the pinned shape with its manual-correction count (AQP:146; SMAP:67) |

Q2 itself is not case-scored. It is measured on adjudicated T2 findings (AQP:140, AQP:228); §3 to §5 cover that.

### 1.2 The scoring unit and expected answers

A `finding` case is the scoring unit (rule, subject, required relation@rung, universe, configuration). Configuration means the mode, target, features, cfg and prepared-input set (AQP:130). Each case pins exactly one expected answer, independently of any candidate run (AQP:130-135):

| `expectedAnswer.kind` | Meaning | Required extra fields |
|---|---|---|
| `determinate-positive` | a finding is required | `expectedFinding`: rule, subject, correspondence expectation |
| `determinate-negative` | a retained no-match is required | none |
| `must-abstain` | required evidence is insufficient (NE:2260), with propagation applied (NE:2230) | `expectedDeficiency`: the deficiency class the case must surface (AQP:291-296); `positiveSoundUnderDeficiency`: boolean |

`positiveSoundUnderDeficiency` records whether a finding would still be sound under the deficiency. A sound positive under incomplete Coverage is a correct determinate fail, not a Q4 failure (AQP:298; WS:600-604). The oracle decides this when the case is authored, never the candidate run.

"Answerable" means `determinate-positive` or `determinate-negative`. The candidate's Coverage never chooses which cases are scored (AQP:135).

### 1.3 Outcome classification

The candidate result for a case is one of: `found`, `no-match`, `indeterminate(deficiency)`, `refused(code)` or `error`. Scoring is a fixed table (**QD-2**):

| Expected | `found` | `no-match` | `indeterminate` | `refused` / `error` |
|---|---|---|---|---|
| positive | Q3 hit | Q3 miss; cause classified (below) | Q3 miss, and a yield loss (AQP:141, AQP:157) | Q3 miss; defect |
| negative | case false positive (reported beside Q2, never inside it) | correct | yield loss, dispositioned (AQP:152) | defect |
| must-abstain | correct if `positiveSoundUnderDeficiency`, else a false positive | **Q4 failure**: an unsupported determinate negative (AQP:142) | correct if the deficiency matches; otherwise `deficiency-mismatch`, dispositioned | correct only if the case pins that typed refusal |

**Miss causes** (AQP:300-302). The oracle records whether the required evidence was complete:
- complete, but the detector or predicate erred: a **Q3 miss**;
- the candidate's Coverage claimed complete, but the oracle shows the evidence was missing: a **false completeness claim**, which is a **Q4 failure** and release-blocking.

On T1 a deficiency mismatch also fails Q1, because Coverage atoms are compared by exact set equality (AQC:127-130).

### 1.4 Case fields

| Field | Content |
|---|---|
| `caseId` | stable human-readable ID, unique in the case set |
| `caseKind` | §1.1 |
| `tier` | `T1`, `T2` or `T3` (AQP:201-205) |
| `origin` | `oracle-fixture`, `validated-seed`, `fix-reversal`, `negative-lookalike`, `curated-differential`, `curated-adjudication` |
| `family` | the independence family (§5.3), for T2 and T3 |
| `heldOut` | boolean: a member of the held-out repository set or a held-out mutation family (AQP:219, AQP:278). Held-out standing is **reserved and never exposed** (**QD-23**, N04). The ledger keeps a permanent `exposure` history (§3.2). Once a case, repository or family has been inspected outside an acceptance round (its findings viewed during development, its labels read, or used as a curated differential source during development), it loses held-out standing permanently. Rotating a freeze seed, or curating it again, never restores it. The acceptance gate checks this history, not the flag alone. |
| `inputs` | `fixtureManifestDigest` (T1) or `{repository, commit, treeDigest}` (T2, §10); for a seed, `controlTreeDigest` and `mutantPatchDigest` |
| `rule` | `ruleId` and `ruleSpecDigest` (§2) |
| `subject` | universe, subject kind, logical subject key |
| `requirement` | relation@rung and universe |
| `configuration` | mode, targets, features, cfg set, `dependencySourceSetId`, `preparedOutputSetId` (NE:1265, NE:1274) |
| `expectedAnswer` | §1.2 |
| `cell` | for `cell-observation` only: the CellId coordinates, expected atoms `{kind, subject, value}`, expected exit, and work and stress bounds (AQ:240-246, AQ:259-262) |
| `provenance` | the author or generator, plus the ledger records that settled the expected answer (§3) |
| `caseDigest` | SHA-256 of the canonical bytes of the record without `caseDigest` |

### 1.5 Pinning and digests

- **The case set** is a JSON Lines file. There is one canonical record per line, the lines are sorted by `caseId`, and the file ends with a newline. `caseSetDigest` is the SHA-256 of the file bytes.
- **T1 fixtures** live under `tests/qualification/fixtures/` in the product repository, with per-file SHA-256 and a manifest digest, like the preview corpus (AQP:203). A T1 case references the fixture manifest digest.
- **The freeze record.** Each measurement round is opened by one `freeze` record in the ledger (§3.4). It pins: `caseSetDigest`, `ruleSpecSetDigest`, `rubricSetDigest`, `familyMapDigest`, `heldOutSetDigest`, `metricDefinitionsDigest` and `preregistrationDigest` (§5.7). A case added after the freeze enters the next round, never the current one (AQP:159).
- **Change control.** A changed expected answer is a new case revision with a new digest. The old revision is kept, and the change must cite a ledger record. A candidate run can never change a case (AQP:152).

---

## 2. Rule-catalog draft specs

The draft catalog is a prerequisite for Q2 and Q3 scoring (AQP:167). I2 evaluates it non-authoritatively in the harness (`M3-PLAN.md:171`). Each rule is a `PolicyDocumentV2` rule (AQP:165; WS:593-597), evaluated under strong Kleene: under incomplete Coverage `none` is false on a match and otherwise indeterminate (WS:600-604). A universal negative therefore abstains by construction when its Coverage is incomplete.

### 2.1 The spec record

The fields follow AQP:168-175. Q0 adds one field, `propositionClass` (**QD-3**), because label carry-forward (§3.3) needs it.

| Field | Content |
|---|---|
| `ruleId`, `specRevision`, `specDigest` | identity |
| `propositionClass` | `existential`: true because a witness exists (a cycle, an unresolved specifier, a crossing edge). `universal-negative`: true because nothing in a universe refers to the subject (the unused and unreferenced rules). |
| `subjectPopulation` | universe, subject kind, include/exclude (AQP:168) |
| `predicate` | the exact proposition in words, plus an `emitWhen` sketch (AQP:169). I2 binds the relation IDs. |
| `configurations` | mode, targets, features, cfg and dev/build/test scope (AQP:170) |
| `closedWorld` | the `ClosedWorldV2` fields the rule needs (AQP:171; NE:2210-2224) |
| `minimumSufficiency` | the relation@rung and Coverage that must be complete for a determinate negative (AQP:172) |
| `lookalikes` | legitimate cases that must not fire (AQP:173) |
| `default` | gating, advisory, or gating only after declared policy (AQP:174) |
| `explanationTemplate`, `limitations` | (AQP:175) |
| `mutationFamilies` | §6.1, with the held-out family marked |
| `rubricDigest` | the frozen adjudication rubric (§4.1) |

### 2.2 The draft rules

The rules and defaults are AQP's (AQP:179-191); Q0 adds the proposition class, the minimum sufficiency and the lookalike set. Every dead-code rule also carries AQP:193's required truth fixtures: outside-workspace consumers, re-exports, `pub(crate)`, multi-crate workspaces, feature and cfg variants, test and build dependencies, and framework or generated entry points.

| Rule | Class | Minimum sufficiency for a negative | Required lookalikes | Default |
|---|---|---|---|---|
| `ws-unreferenced-export` (TS/JS) | universal-negative | complete in-universe reference Coverage at the semantic rung; no dynamic edge whose possible targets include the subject (NE:2230) | re-exported, `import *` namespace use, type-only use, use from a test or config file inside the universe | advisory (AQP:181) |
| `unused-export` (TS/JS) | universal-negative | as above, plus `exportsClosed=closed` and `externalConsumers=none-declared` (NE:2213-2224) | `private:true` alone (NE:2226), published subpath, `bin` entry | gating (AQP:182) |
| `unimported-file` (TS/JS) | universal-negative | `entryPointsRecognized=all`; complete import Coverage | convention-loaded framework file (L-FW1), side-effect import, config-referenced file | gating, otherwise indeterminate (AQP:183) |
| `rs-workspace-unreferenced-pub` | universal-negative | complete cross-crate reference Coverage over the selected targets and features | used only under a non-selected cfg; used only in tests; used through a re-export; used from a macro expansion | advisory (AQP:184) |
| `rs-unused-pub-item` | universal-negative | as above, plus closed world: not reachable from the published API and `externalConsumers=none-declared` | a library crate's public API; `pub(crate)` | gating (AQP:185) |
| `unused-dependency` | universal-negative | complete use Coverage across every selected target that declares it, counting build scripts, proc-macros, tests and features (AQP:187) | used only in `build.rs`; used only by a proc-macro; used only behind a feature; renamed dependency | gating per declared scope |
| `module-import-cycle` | existential | the witness edges are resolved | type-only import cycle, if the policy excludes it | gating only by declared policy (AQP:188) |
| `unresolved-import` | existential | the specifier and the resolution attempt are disclosed | an ambient module declaration; a path alias | advisory (AQP:189) |
| `clone-*` | existential | facts only; near clones are candidates (L-CL1) | generated code | advisory, never gating (AQP:190) |
| `boundary-violation` | existential | the crossing edge is resolved | an allowed exception in the declared layering | gating once declared (AQP:191) |

Repair eligibility is never a catalog rule. It stays per finding, through `deadCodeRepairEligible` (AQP:186; NE:2237-2242).

---

## 3. The label ledger

### 3.1 Storage format (QD-4)

- **One append-only JSON Lines file per round:** `ledger/<roundId>.jsonl`. Every line is one canonical record (CAN:67-74).
- **Chaining.** Each record carries `prevRecordDigest`, the digest of the previous line (`null` on the first), and `recordDigest`, the SHA-256 of its own canonical bytes with `recordDigest` removed.
- **Pinning.** `ledgerDigest` is the SHA-256 of the whole file. The exploratory envelope pins both it and the head record's digest (ENV `ledger`).
- **History.** Nothing is rewritten or deleted. A correction is a new `supersede` record that names the record it replaces and why (AQP:262).
- **T3 labels** stay in a separate local ledger. Only aggregate metrics and labels leave the machine, never source (AQP:205), so a T3 rationale cites `path:line` and contains no source text.

### 3.2 Record kinds

| `recordKind` | Content |
|---|---|
| `adjudicator` | voter registration: `voterId`; `kind` (`human` or `agent`); for an agent: `modelFamily`, `modelId` and `contextClass`; designated-expert flag; rules on which the voter is conflicted (§4.5) |
| `freeze` | the round's pinned digests (§1.5) |
| `item` | an adjudication item: the label key (§3.3), the queue, whether it is a calibration item (the flag is hidden from adjudicators), and the presentation digest (§4.2) |
| `vote` | one blind label: `itemId`, `voterId`, `label` (`true`, `false` or `unclear`), a rationale citing `path:line` at the pinned tree, `triageMillis`, and a `rubricDigest` |
| `escalation` | an item sent to the expert, with its reason: `disagreement` or `unclear-gating` |
| `resolution` | the settled label: `label`, `method` (`agreement` or `expert`), the vote records it rests on, and the expert's rationale when there is one |
| `carry` | a carry-forward decision: the source resolution, the new label key, the per-component compatibility result (§3.3), and `carried` (boolean) |
| `calibration-result` | per voter and round: items, correct answers, known-false items labelled true, and pass/fail against the bar (§4.3) |
| `agreement` | per rule and round: n, raw agreement, Cohen's κ, prevalence, and whether a trigger fired (§4.4) |
| `drift-audit` | per rule and round: the sample, its seed, the results, and whether drift fired (§3.5) |
| `exposure` | a held-out case, repository or family that was inspected outside acceptance: who, when and what was seen. It is permanent (QD-23). |
| `supersede` | the record replaced, and why |

### 3.3 The label key, and what each component binds

A label is bound to a **label key** (AQP:250-255). Q0 splits its components into two groups (**QD-5**).

**Hard components must be identical for a label to carry:**

| Component | Bound to |
|---|---|
| `propositionId`, `rubricDigest` | the adjudicated proposition and the rubric revision (AQP:251) |
| `ruleSpecDigest`, `ruleProgramDigest`, `detectorSemanticsMajor` | the rule definition, program digest and semantics major (AQP:252) |
| `configurationDigest` | mode, target, features and cfg (AQP:253) |
| `dependencySourceSetId`, `preparedOutputSetId` | NE:1265, NE:1274 (AQP:254) |

**The input component that may differ in form only:**

| Component | Bound to |
|---|---|
| `truthInputDigest` (TRI) | the truth-relevant input closure, defined next. It replaces r1's narrower lexical digest. |
| `treeDigest` | the repository tree (AQP:253). It is recorded, and it is covered by the TRI below. |

**Recorded outputs, which are never input components:**

| Output | Content |
|---|---|
| `evidenceRefs`, `messageParameters` | the finding's evidence references and message parameters (`finding3`, IE:190; AQP:255). These are detector output. They never justify reuse; they feed only the unexplained-output trigger. |

**The truth-input closure (QD-5, revised for C2-Q0-R1-01).** The TRI covers the subject, its incoming references and the proof's evidence references (AQP:257). It must not depend on the detector, and it must be **conservative**: any input change that could change the label's truth must change the TRI. r1's lexical, witness-based digest failed that test. In CODEX2's counterexample, adding `missing.ts` resolves `import './missing'` without touching any file in the old digest, and edits through aliases or re-exports need not contain the subject's name. The default TRI is therefore the **full selected-universe and resolution-input closure**, which is the SHA-256 of the canonical record of:
1. the **complete snapshot inventory**: every path in the analysed snapshot, with its mode and content digest, in the §10 tree-digest form. Additions and deletions anywhere in the snapshot change it. That includes previously absent resolution candidates (a new `missing.ts`, a new `index.ts`, a new crate directory) and generated inputs present in the snapshot.
2. the **resolution inputs outside the tree**: `configurationDigest`, `dependencySourceSetId` and `preparedOutputSetId` (already hard components), plus the digest of the harness's resolution environment (the pinned toolchain and closure identities in the freeze).

In practice the default TRI is unchanged exactly when the snapshot and the resolution inputs are byte-identical. A label then carries across product rebuilds that keep the detector semantics major, and across rounds on the same pinned commit, but never across a corpus commit bump.

**Narrower closures.** A rule-specific closure smaller than the default (for example, the files that can reach the subject through resolution) is permitted only when **all** of these hold:
- a written soundness argument covers aliases, re-exports, barrel files, configuration (path mappings, `exports` maps, cfg and features), generated inputs, and the negative searches that universal negatives depend on;
- that argument is reviewed independently of the rule's author;
- it is pinned by digest in the rule spec as `truthClosureSpecDigest`.

r2 admits none, so every rule uses the default.

**The carry rule** (AQP:257). A label carries only if every hard component is identical and the TRI is identical. The check is mechanical, and its per-component result is written as a `carry` record.

**Re-adjudication triggers** (AQP:258-261). Each trigger maps to a mechanical test, and the tests compare inputs and outputs separately (N04):
- a change to the rule, rubric, configuration, dependency set or prepared outputs: a hard component differs;
- a change to the subject or its incoming references, or to anything that could resolve to it: the TRI differs;
- a change in detector output that no input change explains: every hard component and the TRI are identical, but the recorded outputs (`evidenceRefs` or `messageParameters`) differ. This both re-queues the item and files a determinism defect (§8.4).

`finding-key2` is used only to *propose* which earlier label might apply. It is never a reason to carry one (AQP:256; IE:199-213).

### 3.4 Evidence counts

Following CODEX2's r2 observation N02 (`docs/implementation/m3/analysis-quality/reviews/codex2-analysis-quality-plan-r2/review.json`, C2-AQ-R2-N02), the populations are kept apart (**QD-6**, extended for C2-Q0-R1-03). Each count is carried per stratum and per repository (ENV `q2`):
- **corpus:** every finding the candidate emitted in a stratum;
- **sampled:** the findings drawn for adjudication. That is all of them for gating and repair-eligible rules (AQP:228), and the §5.7 allocation for advisory rules;
- **settled:** sampled findings with a resolution (true, false or unclear);
- **pending:** sampled findings without a resolution yet;
- **unlabelled:** corpus minus sampled. These findings were never drawn, so they are never labelled.
- **independent evidence units:** what the confidence rule counts (§5): families, with each family's sampled denominator.

**Naming rule.** "Census precision" is used only when unlabelled = 0 and pending = 0. A ratio computed from a sample is called the *sample ratio*, and it is descriptive only. It is never used for the census guard (§5.6).

Calibration items are never in any of these populations. A finding that appears in two rounds through a carried label counts once per round, not twice. Carried labels count as evidence only in the round that carried them.

### 3.5 Drift audit

Each round, for each rule, the harness samples carried labels: at least 5% and at least 20, or all of them when fewer than 20 were carried (AQP:263). The sample is drawn with a seed equal to `SHA-256(roundId ‖ ruleId ‖ head recordDigest at the freeze)`, so it is fixed by the freeze and can be recomputed. Each sampled item is re-adjudicated blind under §4.

**Drift** means one or more sampled items whose new settled label differs from the carried one. It triggers full re-adjudication of every carried label for that rule in that round (AQP:263).

---

## 4. The adjudication protocol

### 4.1 The rubric

There is one digest-pinned rubric per rule revision (AQP:242). Each rubric contains:
1. the exact proposition from the spec (§2.1), not "is this code good" (AQP:231);
2. a decision checklist ending in `true`, `false` or `unclear`;
3. the lookalike list, with the correct label for each one;
4. what a rationale must cite: `path:line` at the pinned tree, plus the configuration consulted;
5. a **time box**, default 20 minutes (**QD-7**). `unclear` is allowed only with a written reason: the time box ran out, the evidence is outside the pinned bytes, or the proposition is ambiguous for this case. Triage time is recorded on every vote, for Q7's triage-cost report (AQP:154).

### 4.2 Blind presentation

An adjudicator receives a **presentation** for each item: the rule's proposition and rubric, the subject (universe, kind, logical key, and declaration location), the selected configuration, and read access to the pinned tree. The presentation's digest is recorded on the `item` record.

The presentation withholds:
- the other label and its rationale;
- the detector's evidence path, its rationale and its message parameters (AQP:243);
- whether the item is a calibration item.

Calibration items are built in the same format from real T2 code (§4.3), so they cannot be told apart by their shape. Queue order is shuffled with a seed recorded in the freeze.

### 4.3 Calibration items

Known-true and known-false items are planted blind in each queue (AQP:244). **QD-8** sets the numbers:
- **Source.** Known-true items are validated seeds placed in real T2 code (§6). Known-false items are validated negative lookalikes, the hard cases of AQP:277. Both carry expected answers settled before the round.
- **Rate.** At least 10% of each queue, at least 5 items per voter per round, at least 2 of them known-false.
- **The bar.** Calibration accuracy of at least 0.90, and **no** known-false item labelled `true`.
- **Below the bar.** That voter's votes are excluded for the round, and their items are re-queued to other voters (AQP:244).
- **Counts.** Calibration items are excluded from every evidence count and from the agreement statistics (§3.4).

### 4.4 The agreement statistic

The harness records raw agreement and Cohen's κ per rule and round (AQP:247). With precision near 0.99, κ suffers the prevalence paradox: two voters can agree on 99% of items and still get a low κ. So **QD-9** fixes the trigger as follows:
- **Recorded every round:** n, raw agreement, κ, and the prevalence of `true`.
- **Rubric review triggers.** Any one of these sends the rule's definition back for review (AQP:247):
  - raw agreement below 0.90;
  - κ below 0.60, applied only when the minority label class has at least 10 items in the round;
  - `unclear` above 5% of the rule's settled labels.
- **Small rounds.** Below the κ applicability floor, κ is still recorded, labelled `kappa-unstable`. Calibration (§4.3) does the work there.
- **Rater populations (N04).** Each item has two ordered vote slots. Slot A holds the human vote, or the vote of the earlier-registered human when both votes are human. Slot B holds the other vote. The rule-level κ is Cohen's κ over the (A, B) pairs, so it measures agreement between the human slot and the independent second slot. Votes are mapped to slots only after the round closes, and voters never see their slot. The harness also records a pair-specific κ for each voter pair sharing at least 20 items. That is diagnostic only and does not trigger review. `unclear` is a third category in both calculations.

### 4.5 Votes, independence and the model-family rule

**The author rule.** The author of a rule does not adjudicate it (AQP:245).

**Voters.** A voter is a registered person or agent configuration (§3.2). For agents, **QD-10** makes AQP:245 operational:
- **Model family** means the vendor's model lineage: every Anthropic Claude model is one family, every OpenAI GPT or Codex model is one, every xAI Grok model is one, and so on. The `adjudicator` record pins `modelFamily` and `modelId`.
- **Same family, one vote.** Agents from the same family count as **one** vote. If they disagree among themselves, that family's vote is `unclear`.
- **Implementation context.** An agent has implementation context for a rule if it has seen the rule's source, the detector's code, the detector's output for the item, or implementation discussion of the rule. Such an agent counts as the rule's author and does not vote on that rule.
- **This lead's rules.** The draft catalog is authored by the lead, a Claude model. So for these rules, every Claude-family agent is treated as sharing implementation context and does not vote. Agents of other families may vote if they are given only the presentation (§4.2).
- **Agents never stand alone.** Agents assist; they are never independent ground truth on their own (AQP:245). So a settled label needs at least one human vote.

**Settling a label.**
1. Every item receives two votes from two different vote groups (AQP:243). At least one of the two is human.
2. If both are `true`, or both are `false`, the item resolves with method `agreement`.
3. A disagreement goes to the designated human domain expert, and so does every `unclear` on a gating or repair-eligible finding (AQP:246). A third procedural vote does not settle it (AQP:246).
4. If two votes on an advisory finding agree on `unclear`, the label resolves as `unclear` and counts as not true (AQP:232).

### 4.6 Escalation to the expert

**Who.** The expert is the owner or a named delegate (AQP:246), registered with the expert flag (§3.2). The roster is an owner action (`M3-PLAN.md:368`).

**What the expert sees.** The presentation and both rationales. The detector's evidence stays withheld, as in §4.2, so the expert is not anchored to the tool.

**The decision.** It is final for that label key and is recorded with a rationale. If the expert answers `unclear`, the label counts as not true (AQP:232).

**Pending items.** An exploratory report may close while gating or repair-eligible items are still pending. Those strata are reported as `not-yet-adjudicated` (`M3-PLAN.md:173`). Any later Q2 use requires every such item to be resolved (AQP:228, AQP:246).

---

## 5. The confidence rule

### 5.1 The estimand

AQP sets the target on a one-sided 95% lower bound of conservative precision, per stratum. Conservative precision counts unclear as not true (AQP:232). A stratum is rule × language × mode, and strata are never pooled (AQP:233).

The target generalizes beyond the corpus. The 95% statement is about repositories like those in the corpus, and the unit that is sampled from that population is the repository family (§5.3), not the finding.

**QD-11.** The bound is placed on the **family-weighted conservative precision** (N01: named for its actual weighting): the average, over independence families in which the rule fires, of each family's expected conservative precision. Two reasons:
- A finding-weighted bound over correlated findings invents independent evidence. This is the counterexample in the CODEX2 review that produced AQP:235 (the same review file, C2-AQ-R2-01 `analyticIllustration`).
- The family-weighted quantity is close to what a single team sees on its own repository.

**What it does not claim.** It is not a lower bound on the population's finding-weighted precision. The pooled guard in §5.6 does not make it one; the guard only stops a large, poor repository from being averaged away. Each Q2 result names its estimand (ENV `q2.strata[].estimand`). Whether qualification wants a finding-weighted estimand is OI-4, and family-wise confidence is OI-5. Both stay open for the DR-G13 successor.

### 5.2 Which bound applies

The method is chosen from the **structure** of the stratum's evidence before any label is read, so the choice cannot follow the labels. Let *k* be the number of families with at least one finding in the stratum, and let *a_j* be the number of **sampled** findings from family *j* (§5.7). *a_j* equals family *j*'s corpus count for gating rules.

- **Single-finding families** (AQP:234): every *a_j* = 1. **Method: exact Clopper–Pearson** (§5.4).
- **Clustered** (AQP:235): some *a_j* > 1. **Method: the cluster-level product bound** (§5.5).

**The Clopper–Pearson premise, stated (N01).** One finding per family gives distinct evidence units. That alone does not make them IID Bernoulli draws with a common success probability. The Clopper–Pearson branch adds the premise that the *k* families are independent draws from one population of families, with the finding drawn uniformly within each. Each sampled finding is then Bernoulli with the population's family-weighted mean. If that premise is doubted, the product bound remains valid without it, since it allows heterogeneous independent family means (§5.5). The two branches therefore rest on different premises, and each result records which one applied (ENV `method`).

**Where the single-finding design comes from.** The §5.7 allocation is guaranteed to give one finding per family when the stratum has at least 100 families with findings. Smaller strata of single-finding families also get one each, and the formal condition in the branch rule above decides. Gating strata are adjudicated in full (AQP:228), so they take the Clopper–Pearson branch only when every family has a single finding.

### 5.3 Independence families

The independence unit is a **family** of repositories, not a single repository (**QD-12**). Repositories go in one family if any of these hold:
- one is a fork, mirror, vendored copy or split of another;
- they share generated code from the same generator;
- they are parts of one multi-checkout workspace assembly (the D15 approximation is **one** family; AQP:217);
- they share an upstream project, for example a repository and its examples repository.

Sharing an organization alone does not merge two repositories.

Families are assigned in the T2 manifest by M3-T2, reviewed, and pinned by `familyMapDigest` at the freeze. Families with no finding in a stratum do not count toward that stratum's *k*. T3 repositories form their own families, labelled `T3-local` (AQP:205). Per-repository results are reported as well as per-family ones (§12), because a family may hold several repositories (AQP:238).

**The assumption every method needs.** Each bound treats the families as independent draws from the population of repositories the claim is about. T2 is purposely selected (AQP:213-219), not randomly sampled. The held-out discipline (§5.6) guards against tuning on the corpus, but not against unrepresentative selection. The envelope states this assumption on every Q2 result (ENV `q2.strata[].assumption`).

### 5.4 Exact Clopper–Pearson (single-finding strata)

Let *x* be the true count out of *k* single-finding families. The one-sided 95% lower bound *L* is the *p* that solves P(Bin(*k*, *p*) ≥ *x*) = α, with α = 0.05; *L* = 0 when *x* = 0. Equivalently, *L* is the α quantile of Beta(*x*, *k* − *x* + 1).

**Exact decision.** *L* ≥ *t* holds exactly when Σ_{i=x}^{k} C(*k*, *i*) *t*^i (1 − *t*)^{k−i} ≤ α. The harness evaluates this in exact rational arithmetic, with *t* = 99/100 or 9/10 and α = 1/20. It stores *L* rounded down to millionths: the largest *q*/10⁶ for which the tail at *q*/10⁶ is ≤ α.

**Reference values for K1b's self-test (N02).** These are stored integers, rounded down and computed exactly for this record:

| Case | `lowerBoundPpm` |
|---|---|
| *x* = *k* = 299 | 990030 |
| *x* = *k* = 29 | 901855 |
| *x* = 472, *k* = 473 (one error) | 990010 |
| *x* = 45, *k* = 46 (one error) | 900975 |

With one error, *k* = 473 is the smallest count reaching 0.99, and *k* = 46 the smallest reaching 0.90 (AQP:234 gives the zero-error examples).

### 5.5 The cluster-level product bound (clustered strata)

**Chosen method (QD-13), unchanged from r1.** For each family *j*, let *X_j* = *t_j* / *a_j* ∈ [0, 1] be that family's conservative precision **on its sampled findings**: its census value for gating rules, or its uniform within-family sample estimate for advisory rules (§5.7). The denominator is always the family's sampled count *a_j*, never its corpus count. Then

> *L* = α^{1/k} · (Π_j *X_j*)^{1/k}, that is, α^{1/k} times the geometric mean of the per-family precisions; *L* = 0 if any *X_j* = 0.

**Exact decision.** Pass iff Π_j *X_j* ≥ *t*^k / α, as an exact rational comparison.

**Why it is valid.** Fix any *m* in (0, 1]. Suppose the families are independent and the average of their expected precisions is at most *m*. For a sampled family, uniform selection within the family makes *E[X_j]* equal that family's precision. The product of the expectations of *X_j*/*m* is then at most 1 (AM–GM over the family means), so the product is an e-value. Markov's inequality gives P(Π *X_j* / *m^k* ≥ 1/α) ≤ α. Taking *m* to be the true mean, P(*L* ≥ true mean) ≤ α. CODEX2 verified this derivation (review §"Method assessment").

This needs no model of how findings correlate inside a repository, no prior, no asymptotics and no resampling. It also does not need the families to be identically distributed: it bounds the average of their means. It is the fixed-bet, all-in case of the betting confidence bounds for bounded means (Waudby-Smith and Ramdas, *JRSS-B*, 2024; Vovk and Wang, *Ann. Statist.*, 2021). The analytic proof is the evidence for validity. r1's simulation sentence is withdrawn (N03), because nothing about it was retained.

**The zero-error boundary.** If every family is all-true, *L* = α^{1/k}. That is exactly the Clopper–Pearson bound for *k* single observations. **At that all-success boundary**, it is also the most any method can claim without a within-repository model. If each repository were all-true or all-false with mean *μ*, the chance of *k* all-true repositories would be *μ*^k. So 300 findings from 3 perfect repositories give `lowerBoundPpm` 368403, as CODEX2's illustration requires. Identical all-true repositories are never resampled into a pass (AQP:235). Away from that boundary no optimality is claimed (N02).

**It uses partial information.** Unlike reducing each family to a single clean/unclean bit, a family at 0.995 contributes 0.995, not 0. Reference values, stored and rounded down:
- 30 families at 1.0: 904966;
- 29 at 1.0 and one at 0.90: 901793, a pass at 0.90;
- 29 at 1.0 and one at 0.50: 884296, not a pass.

**What it costs.** When findings inside a repository really are independent, the bound is more conservative than a model-based one. That is the price of assuming nothing about correlation within a repository.

**One harsh property, accepted.** A single family whose sampled findings in the stratum are all false or unclear sets *L* = 0. For a gating rule, a repository where every finding is wrong is a defect worth failing. Gating unclear labels go to the expert first (§4.5), so this happens only when the expert also cannot confirm a single finding in that repository.

**Rejected alternatives:**
- **Repository bootstrap.** It is degenerate at zero errors (AQP:235).
- **Beta-binomial or Bayesian hierarchical model.** At zero errors the data cannot identify the within-repository correlation, so the bound would be set by the prior on that correlation. A credible bound is also not the 95% confidence statement Q2 asks for.
- **Design-effect correction with an assumed intraclass correlation.** It is asymptotic, and it needs an assumed correlation that cannot be checked when there are no errors.
- **Reducing each family to a clean/unclean indicator, then Clopper–Pearson.** It is valid, but it throws away partial information.

### 5.6 Status rules, minimum counts, the pooled guard and INSUFFICIENT-EVIDENCE

**Minimum independent families.** At zero errors both methods give α^{1/k}, so a pass needs *k* ≥ *k*_min(*t*) = ⌈ln α / ln *t*⌉ (**QD-14**). These are stored values, rounded down:

| Target | *k*_min | Check |
|---|---|---|
| advisory 0.90 | **29** | *k* = 29 gives 901855; *k* = 28 gives 898534 |
| gating and repair-eligible 0.99 | **299** | *k* = 299 gives 990030; *k* = 298 gives 989997 |

The exact checks are 20·(9/10)^29 ≤ 1 < 20·(9/10)^28, and the same form for 99/100. These are floors: no stratum with fewer families can pass. In the single-finding (Clopper–Pearson) branch, any error raises the requirement (§5.4). In the product branch, an error raises it only if it lowers a family's precision enough. For example, 299 families with 298 at 1 and one at 999999/1000000 give *L* ≥ 0.990030 × 0.999999 > 0.99, which passes (C2-Q0-R2-N01).

**The pooled guard (QD-15, revised for C2-Q0-R1-03).** Let *N* be the stratum's corpus count, *T* and *F* its settled true and settled not-true counts (unclear counts as not true, AQP:232), and *U* = *N* − *T* − *F* the findings that are unlabelled or pending. The guard has two conservative values, computed exactly:
- **verified lower value:** *T* / *N*, which treats every unlabelled finding as not true;
- **optimistic upper value:** (*T* + *U*) / *N*, which treats every unlabelled finding as true.

When *U* = 0, the two coincide and equal the **census precision**. That is the only case in which that name is used. For gating strata, *U* = 0 once adjudication is complete (AQP:228). An unweighted sample ratio is never used for the guard. In CODEX2's counterexample (one family of 10,000 findings at 0.80, plus 99 single true findings, sampled one per family), *T* ≤ 8,099 and *N* = 10,099. The verified value is at most 0.802, so the stratum cannot pass. The upper value depends on the sampled labels, and it is FAIL only if the sample shows enough errors.

**Status, per stratum, evidence set and target, decided in this order:**
1. `NOT-YET-ADJUDICATED`: some **sampled** finding is pending (`M3-PLAN.md:173`). Exploratory only; it is never a Q2 result.
2. `INSUFFICIENT-EVIDENCE`: zero findings, or *k* < *k*_min(*t*) (AQP:236). The bound is still reported.
3. `FAIL`: the optimistic upper value is below *t*. Even if every unlabelled finding were true, pooled precision would miss the target.
4. `INSUFFICIENT-EVIDENCE`: the verified lower value is below *t*. The guard cannot be established without more labels.
5. `PASS`: *L* ≥ *t* by the exact decision in §5.4 or §5.5.
6. `INSUFFICIENT-EVIDENCE`: otherwise. The guard holds, but the bound does not.

If any guard input is unavailable (for example, the corpus count is missing), the stratum is `INSUFFICIENT-EVIDENCE` with the reason `guard-unavailable`, and PASS is prohibited. Neither non-pass status is ever a pass (AQP:236).

**A consequence for advisory rules.** Under this guard, an advisory PASS needs at least 0.90·*N* findings verified true, so in practice nearly the whole stratum must be adjudicated. A sharper rule would bound pooled precision from the sample: a per-family exact hypergeometric lower bound on true counts, at level α/*k* (Bonferroni), summed over families and divided by *N*. Unsampled families would contribute zero, and fully adjudicated families their exact count. That is a new inference rule, so r2 does not adopt it. It is routed for approval as OI-17, and until it is approved the conservative guard above is in force.

**Which families count for acceptance.** The acceptance computation counts only **held-out** families, whose findings and labels were never exposed during rule development (AQP:219, AQP:433; QD-23). Development families give exploratory numbers only, labelled `development`. Both are reported, and every count and status is computed separately for each evidence set.

**Downgrading** (AQP:237).
- A gating stratum that does not PASS at 0.99 is evaluated at 0.90. If it passes, the rule may ship as a qualified advisory rule.
- If it does not pass at 0.90 either, it may ship only as a declared-unqualified exploratory advisory rule. It gets no Q2 pass and no waiver, and it is listed in the envelope's `unqualifiedAdvisoryRules`.
- Both targets are fixed before measurement, so the downgrade involves no tuning.

**Confidence is per stratum.** 95% applies to each stratum, as AQP:233 states. With *S* strata, a release could hold false passes on up to about 0.05·*S* of them in expectation. The plan sets no family-wise correction, and this record does not invent one. §14 OI-5 routes the question to the DR-G13 successor.

### 5.7 Preregistration and advisory allocation

Before any acceptance measurement, the freeze record (§1.5) pins a **preregistration document** (`preregistrationDigest`). It fixes:
- α = 1/20, and the targets 99/100 and 9/10;
- the estimand (§5.1), and the method-selection rule (§5.2);
- the family map and the held-out set, with its exposure history (QD-23);
- the advisory allocation, below;
- the pooled guard and the status order (§5.6);
- the rounding rule (QD-1).

**Advisory allocation (QD-24, revised for C2-Q0-R1-02).**
- **Unit and floor.** The floor applies to each stratum (rule × language × mode), which satisfies AQP:228's "at least 100 per rule per language". It applies separately to the held-out and the development evidence sets. Let *N_j* be family *j*'s corpus count in the stratum and evidence set, and *T* = min(100, Σ*N_j*).
- **Water-filling.** Find the smallest integer *c* ≥ 1 such that Σ_j min(*N_j*, *c*) ≥ *T*, and set *a_j* = min(*N_j*, *c*). Families too small for their share give their unused slots to the others, so the total reaches *T* whenever enough findings exist, and is all of them when Σ*N_j* ≤ 100. The total may exceed 100 by less than *k*.
- **Effects.** With *k* ≥ 100 families, *c* = 1, which gives one per family and the Clopper–Pearson branch. In CODEX2's counterexample (*k* = 29, one family of 100 and 28 of 1), *c* = 72, so the allocation is 72 + 28 = 100.
- **Selection.** Within each family, *a_j* findings are drawn uniformly without replacement, with the seed `SHA-256(roundId ‖ stratumId ‖ evidenceSet ‖ family)`.
- **Recording.** *N_j* and *a_j* are both recorded per family and per repository. The bound uses *a_j* as the denominator (§5.5), and the guard uses *N* (§5.6).

None of these may change after the freeze for that round (AQP:159).

### 5.8 What this means in practice, reported to the owner

**Gating.** A **gating 0.99 PASS needs at least 299 held-out families with findings for that rule, language and mode**, and 299 error-free families suffice at that minimum. In the single-finding branch, one error raises the need to 473 (§5.4). In the product branch, an error costs extra families only to the extent that it lowers a family's precision (§5.6). Every gating finding in them must be adjudicated (AQP:228).

**Advisory.** A 0.90 PASS needs at least 29 held-out families. Under the in-force pooled guard, it also needs at least 0.90·*N* of the stratum's findings verified true. Example: 29 held-out families with 4 findings each give *N* = 116. All 116 are adjudicated: 232 votes, plus calibration of at least 10% of each of the two vote queues (about 13 items each), so about 260 votes, at least half of them human (§4.5). r2's lower estimate for OI-17 is withdrawn (C2-Q0-R2-N02). A sample from small families need not establish the proposed per-family hypergeometric bound, so approving OI-17 would not by itself reduce this cost.

**Scale.** T2 plans at least two repositories per language per size class, with one held out per class (AQP:218-219). Gating strata will therefore be INSUFFICIENT-EVIDENCE unless T2 grows by an order of magnitude. At the all-success boundary this is not a defect of the method: without a within-repository model, no valid 95% method can do better (§5.5). The choice is the D4 revisit (AQP:148, AQP:525) and D3 sizing (AQP:524); see OI-3.

---

## 6. Mutation and seeding (Q3, Q4)

### 6.1 Mutation families

A mutant is a candidate case only (AQP:269). Each family is a deterministic generator over sites chosen by a harness-owned syntactic enumerator. It is independent of the product's providers.

| Rule | Families (the **held-out** family is chosen by the freeze seed) | Expected answer |
|---|---|---|
| `ws-unreferenced-export` / `unused-export` | `EXP-ADD` (add an export with a fresh, lexically unique name); `REF-DEL` (delete the last in-universe reference); `REEXP-DEL` (remove one link of a re-export chain); `IMPORT-RETARGET` (move an import to a sibling export) | positive |
| `unimported-file` | `FILE-ADD`; `IMPORT-DEL` (remove a file's only import) | positive, or must-abstain under L-FW1 |
| `rs-workspace-unreferenced-pub` / `rs-unused-pub-item` | `PUB-ADD`; `USE-DEL` (remove the only cross-crate use); `CFG-HIDE` (move the only use under a non-selected cfg) | positive in the selected configuration |
| `unused-dependency` | `DEP-ADD`; `DEP-USE-DEL` | positive |
| `module-import-cycle` | `CYCLE-CLOSE`; `CYCLE-BREAK` | positive / negative |
| `unresolved-import` | `SPEC-BREAK` | positive |
| `boundary-violation` | `LAYER-CROSS` | positive once declared |

**Fix reversals** are documented dead-code, unused-dependency and cycle fixes from the pinned repositories' history, reverted. **Negative lookalikes** are the §2.2 lookalikes placed in real code (AQP:277). Both are case origins of their own, not mutation families.

At least one family per rule is held out for acceptance with the held-out repositories (AQP:278). It is named in the freeze, and its instances are generated only for the acceptance round.

### 6.2 Validation steps

Each mutant records its subject, the unmutated control, the expected introduced difference, the selected configuration and its expected answer (AQP:269-274). It is then validated:
1. **Applicability.** The site lies in a selected target, under the selected cfg and features, and inside the analyzed universe.
2. **Well-formedness.** The mutant parses with the pinned grammar. For TS/JS, the pinned TypeScript compiler type-checks it without emitting; this executes no repository code. For Rust, nothing that would run build scripts or proc-macros is used (`M3-PLAN.md:355`), so a Rust mutant has no compile check at M3. Compile validation waits for the authorized execution path in QD-17. Any tool used here carries the same non-execution canary pin as QD-17.
3. **Independent proposition check** (AQP:276). Simple families (`EXP-ADD`, `PUB-ADD`, `FILE-ADD`, `DEP-ADD`, `SPEC-BREAK`) have a mechanical validator: the name is lexically unique in the universe, the module is not star-re-exported into a published entry point, the crate is not a library's public surface (for gating rules), and so on. Every other family is adjudicated under §4, and its label settles the expected answer.
4. **Validator audit.** For each mechanical validator, the harness audits a sample (10% and at least 20 per family and round) by adjudication. One disagreement suspends the validator for that family until it is fixed. Mutants it validated in that round are then adjudicated individually.

### 6.3 Accounting

Every generated mutant ends in exactly one state (**QD-16**):
- `valid-positive`, `valid-negative`, `valid-abstain`;
- `invalid` (fails the proposition);
- `equivalent` (no semantic change);
- `not-enumerated` (outside the selected configuration);
- `ill-formed` (fails step 2);
- `unvalidatable` (would need repository-code execution).

All counts are reported per family (AQP:276). Only the three `valid-*` states become cases. Invalid states never become misses and never disappear from the totals.

---

## 7. The cross-tool differential (discovery only)

**Tools.** Knip and ts-prune for TS/JS; rustc `dead_code`/`unused`, cargo-udeps and cargo-machete for Rust (AQP:281). Each is pinned by version, executable-closure digest, compiler, configuration and adapter digest (AQP:281), and recorded in the envelope's `tools` list with role `differential`.

**Repository-code execution (QD-17, revised for C2-Q0-R1-04).**
- **The M3 rule.** At M3 no repository code executes (`M3-PLAN.md:355`; prepared mode imports, `M3-PLAN.md:301`). The harness is bound by the same rule.
- **What runs at M3.** Only a tool **mode** whose pin verifies that no repository code executes. The pin records the mode, its flags, and a **non-execution canary check**. The tool is run, in that mode, on a harness-owned canary fixture whose `build.rs`, proc-macro, package scripts and JS/TS configuration files would each write a distinct marker file, and whose formatter and linter plugins would do the same. The pin is accepted only if no marker appears. The canary fixture is harness-authored, not repository code, and it is re-run whenever the pin changes. A tool with no verified non-executing mode does not run at M3. `executesRepositoryCode` is recorded as `false` for every tool used at M3 (ENV `tools`).
- **Expected outcome, to be confirmed at pin time.** cargo-machete (lexical) and ts-prune are candidates for a verified mode. rustc's `dead_code`/`unused` lints through a build, and cargo-udeps, build the crate, which runs build scripts and proc-macros, so they have no M3 mode. Knip qualifies only if a mode without configuration or plugin loading passes the canary.
- **Deferred, not conditional.** Executing differentials and Rust compile validation (§6.2) are deferred to the later explicit authorized execution path: M5's `execution.rs` under the `RepoExecutionGrantV2` and the M5-EX successors (`M3-PLAN.md:319`, `M3-PLAN.md:347-352`), on public T2 bytes only, never T3. O7 confinement or a disposable container is an **additional** condition on that later execution. It is never the authorization or the milestone gate.
- See OI-6.

**Why a tool is not an oracle.**
- The tools answer different propositions. rustc's `dead_code` is crate-local and does not see cross-crate `pub` use, which is where OpenSIP adds value (AQP:184). cargo-machete is lexical. Knip uses its own entry-point heuristics.
- They have their own false positives, and their answers depend on configuration.

A tool's output is therefore never an oracle and never G13 evidence (AQP:288-289). The tools run only inside the harness, never as a product dependency or fallback (AQP:289).

**From disagreement to curated case:**
1. **Normalize.** Each tool's finding is mapped to a catalog proposition through that tool's published proposition mapping, or marked non-overlapping (AQP:282).
2. **Compare** against OpenSIP's result on the same case key (§1.2).
3. **Adjudicate** every normalized disagreement under §4 into one of four classes (AQP:283-287): `confirmed-comparable-defect`, `other-tool-false-positive`, `semantic-non-overlap` or `unresolved`.
4. **Curate.** Only a confirmed comparable defect becomes a case: `origin=curated-differential`, with its expected answer taken from the settled label and a ledger reference (AQP:288). It joins the **next** frozen round (§1.5). It is held out only if its repository is held out and unexposed (QD-23). Adjudicating a held-out repository's differential during development exposes it.

---

## 8. Refactor and determinism suites (Q5)

### 8.1 Transformations

Each transformation is a pinned generator (AQP:306). The formatters run with harness-owned configuration, so no repository formatter plugin is loaded.

| ID | Transformation | Expected mapping |
|---|---|---|
| `R-FMT` | Reformat with the pinned rustfmt or Prettier | all subjects unchanged |
| `R-ORDER` | Reorder top-level declarations that have no initializer side effects | unchanged |
| `R-MOVE` | Move a module and rewrite every specifier or `mod` path | subjects moved |
| `R-RENAME-UNRELATED` | Rename a symbol that is not a finding's subject or in its evidence. TS uses the pinned TypeScript language service's rename. Rust is limited to private items with a lexically unique name in their file. | renamed symbol changed; all others unchanged |
| `R-ADD-UNRELATED` | Add a self-contained module | expected new findings, which are correct CODE-NET-NEW; all others unchanged |
| `R-SPLIT` | Split a file, re-exporting from the original | subjects moved |

### 8.2 The independent mapping oracle

For each pair, the generator emits a mapping: unchanged, changed, moved or renamed subjects, and the expected differences in facts, findings and Coverage (AQP:306). A second, independent derivation must agree with it. That derivation is a harness-owned declaration matcher over the before and after trees, comparing declaration signature tokens and the path-move map, and it shares no code with the generator. Any disagreement goes to human review. The reviewed mapping is digested into the `refactor-pair` case.

### 8.3 Validation and comparison

**Validation** (AQP:307). Before scoring, the pair must preserve, modulo the mapping:
- import resolution, read from the pinned TypeScript compiler's program file list and resolved modules for TS, and from the harness's syntactic `mod` tree with an unchanged Cargo manifest for Rust;
- recognized entry points;
- prepared-output freshness. In prepared mode, the harness recipe regenerates the imported set (`M3-PLAN.md:163`).

A pair that fails is recorded with its reason and discarded, never scored.

**The restricted Rust domain (N05).** A syntactic `mod` tree plus an unchanged manifest does not establish that `use` resolution, cfg selection or macro expansion is preserved. A Rust pair is therefore eligible only when the transformation cannot affect them:
- formatting;
- reordering items with no attributes and no macro invocations;
- renaming a private item that is not referenced from any macro body, cfg-gated item or `use` path.

Any other Rust pair whose independent resolution invariant cannot be established is recorded as `unvalidated` and discarded, never scored. Expanding the semantic oracle is part of the full Q5 suite at M5 (AQP:484).

**Comparison** is against the oracle, not `finding-key2` alone (AQP:308-312):
- finding content: message parameters, severity, and evidence references mapped through the oracle;
- relevant proofs and Coverage;
- zero spurious CODE-NET-NEW and zero spurious CODE-FIXED (WS:352-353);
- ambiguous and unmatched findings counted explicitly (IE:1563-1567).

**Survival** is the share of oracle-unaffected findings that survive with matching correspondence, reported per rule × transformation (AQP:313). A pair with fewer than 20 unaffected findings is `insufficient`, never passing (AQP:313).

**Moved and renamed subjects** are reported but not scored for survival until D7's declaration mechanism exists (AQP:314, AQP:529). The full suite runs at M5 (AQP:484); at M3, K1 builds the driver and §8.4 runs.

### 8.4 Determinism checks

These run at M3 (AQP:481). They use identical semantic input closures, run repeatedly (AQP:317), with these variants (**QD-18**):

| Variant | What changes |
|---|---|
| V0 | baseline, 5 repeats |
| V1 | fresh corpus copies written in reverse path order |
| V2 | concurrency 1 against automatic |
| V3 | different scratch root, `TMPDIR` and harness `HOME` |
| V4 | different locale, `TZ` and umask |
| V5 | compatible runner lanes. Deferred while M3 claims only this host's platform family (`M3-PLAN.md:306`). |

**Comparison:**
- When the PlanIds are equal, every identity the contract derives from Plan-bound inputs must be byte-equal: scope, fact, Coverage, view and finding (IE:183-190).
- When an identical input closure gives a different PlanId within one lane, that is itself a determinism failure.
- Across lanes, only canonical semantic payloads and correspondence are compared. IDs are not expected to match across different Plans (AQP:318).
- Per-invocation identifiers (RequestId, ExecutionId) and timings are excluded.

Any difference fails; Q5 determinism is exact (AQP:143). This tests the obligation of independent replay across machines (IE:1806).

---

## 9. Performance (Q6)

### 9.1 Workloads

The T2 manifest pins one **workload manifest** per repository (AQP:333-338). It records:
- source counts by class: hand-written, generated, vendored and excluded;
- shape: files, packages, import and reference edges, and dependencies;
- the selected rules, cells and configuration;
- the exact cold and warm reset and priming steps (§9.2);
- the start and end events of each run.

**Workflows** (AQP:342-345):
- `core-analyze`, with inputs prepared;
- `first-use`, from a clean checkout with no OpenSIP state, including OpenSIP-driven preparation;
- `prep-invalidating-edit`.

The edit taxonomy follows INC-4's sequences (AQP:382): body-only, exported signature, import, feature/config, generated input, insert/delete, missing input, and a newly introduced dynamic edge.

**Controls:** clean, missing input, stale prepared output, and broken or partial build. Each control reports how far the unaffected units progressed, and yield always appears beside time (AQP:349). The user's own `cargo build` is reported separately and never counted (AQP:347).

### 9.2 Cold and warm resets

**Cold** (LQM:923; AQP:328). Before **every** run, warmups included, the harness:
- deletes the project's OpenSIP state and the disposable analyzer caches;
- starts a new process;
- records the OS page-cache state.

Warmups therefore never turn cold samples warm. The page cache is never claimed flushed unless that is verified (LQM:923), so the label is "cold OpenSIP state, page cache recorded".

**Warm, with retained evidence** (LQM:924). The harness runs one priming invocation on the same inputs. Each later run is a new process with the declared caches retained and no reused provider process. Cold and warm are separate fixtures (AQ:279-280).

**Order.** reset → 3 warmups → 7 measured runs, as RS3 requires (`warmupRuns` const 3, seven samples; RS3:78-101).

### 9.3 Elapsed time and RSS

**Elapsed** is measured on a monotonic clock, from spawn to the exit of the top process, after every descendant has been reaped. It is recorded as positive integer nanoseconds (AQ:268-269). The cell statistic is the median, `sorted[3]` (PQV:28).

**RSS per run** follows LQM:925 and AQP:329. The harness keeps two figures:
- **(a) the concurrent sum:** the highest observed sum of resident bytes across the live supervised process tree, sampled every 10 ms;
- **(b) the sum of own high-water marks:** the sum, over every process lifetime in the tree, of that process's **own** lifetime high-water counter, collected at its exit.

The run's value is the **larger of (a) and (b)**. The cell statistic is the maximum of the seven run values (AQ:270; PQV:28). A sampled peak is never used as an own counter. A run whose process inventory or counter collection is incomplete is NON-PASS (LQM:925) and recorded as `incomplete` (§9.5), never filled in.

**Process inventory and own counters (QD-19, revised for C2-Q0-R1-05).**

*Lifetime identity and de-duplication.* A process lifetime is keyed by (tgid, start time), where start time is the kernel's process start time (on Linux, `/proc/<pid>/stat` field 22, in clock ticks since boot). That key survives pid reuse. Threads are not separate lifetimes, because they share the process's address space.

An `exec` keeps the key but replaces the address space, so a lifetime is split into **image segments** at each exec. Each segment needs its own counter, with one exception: a segment that has no address space of its own (a `CLONE_VM` spawn, which has vfork/posix_spawn semantics) needs none. K1c establishes once per runner and pinned toolchain whether the supervisor's spawn path is `CLONE_VM`. It does this by tracing a calibration run's clone flags, and records the result in the runner record. Otherwise every pre-exec segment lacks a counter, and the run is incomplete with the reason `pre-exec-image-unmeasured`. A second exec within one lifetime has the same effect.

*Linux, the D12 reference platform (AQP:534). Completeness must be proven positively (QD-19, revised for C2-Q0-R2-01).* An empty cgroup plus the exits the harness happened to collect proves nothing. `cgroup.procs` excludes zombies, `populated` describes only live processes, and both event channels can lose messages. So figure (b) is **complete only when every item of the proof below holds for that run**. If any item fails, or cannot be evaluated, the run is `incomplete` with a typed reason. Completeness is never inferred from absence: a missing event, record or error is never read as "nothing happened". The kernel facts this relies on (per-CPU taskstats registration and its receive-buffer loss, `ac_tgid`, the `AGROUP` flag on the last thread's record, connector sequence numbers and send failures) are taken from the pinned kernel's documentation and source, as cited in CODEX2's review (`/tmp/opensip-implementation/reviews/codex2-harness-q0-r2/REVIEW.md`). They are **re-verified by K1c's calibration on the pinned D12 kernel**, whose version is recorded in the runner record. Until that calibration passes, Linux runs are `incomplete` with the reason `own-counter-unverified`.

1. **Channels.**
   - **Process events:** the kernel process-event connector (fork, exec and exit events, each carrying the CPU, a per-CPU sequence number, a timestamp, and pid and tgid).
   - **Own counters:** the taskstats per-task exit records from generic netlink `TASKSTATS`, with extended accounting.
   - **Containment:** the workload runs in a dedicated cgroup v2 group, which every descendant inherits.
2. **Acknowledged subscription before launch.**
   - The harness registers its taskstats listener for **every online CPU** and requests an acknowledgement. It subscribes to the connector with no event filter.
   - It records the online-CPU set, and enlarges both receive buffers.
   - It then runs a **pre-launch sentinel on every online CPU**: a short child pinned to that CPU, which forks and exits. The harness must receive, for each sentinel, its fork and exit events and its taskstats terminal record. That proves both channels are live on every CPU.
   - Failure is `subscription-unverified`.
3. **Loss detection during the run.** Any one of these makes the run `incomplete` with the reason `event-loss`:
   - any receive error or overrun (`ENOBUFS`) on either socket;
   - any gap in a CPU's connector sequence numbers between that CPU's pre-launch and post-run sentinels;
   - any change to the online-CPU set during the run.
4. **Stable identity.**
   - A **thread group lifetime** opens on the fork event that creates a new thread group (child pid = child tgid) whose parent chain, built from fork events, reaches the workload root. It is keyed by (tgid, fork timestamp).
   - A tgid cannot be reused until its process is reaped, so between that fork event and the lifetime's terminal record, the tgid names exactly one lifetime.
   - Exec events split the lifetime into the image segments described above.
   - A taskstats record or connector event for a subtree tgid that has no open lifetime is `unjoinable-identity`.
5. **Terminal record selection and de-duplication.**
   - Each thread emits a per-task record at exit. The **terminal** record for a lifetime is the single record carrying that lifetime's `ac_tgid` with the `AGROUP` flag set, which marks the group's last exiting thread.
   - Its `hiwater_rss` (KiB, converted ×1024) is the high-water of the shared address space at group exit, so it covers a worker that raised the peak after an early-exiting leader.
   - Non-terminal per-thread records are **never summed**, because that would count one address space several times. Each is only checked to be ≤ the terminal value, and a violation is a defect.
   - Zero terminal records, or more than one, for a lifetime is `terminal-record-missing` or `terminal-record-duplicate`.
6. **Draining and completion.** After the workload root has exited and the cgroup reports `populated 0`, the harness keeps reading both channels, and runs a **post-run sentinel on every online CPU**. Draining ends only when both of these hold:
   - every lifetime opened in step 4 has exactly one terminal record and a connector exit event for each of its threads;
   - every post-run sentinel's fork, exit and terminal record has arrived, which shows each CPU's queue has been read past the workload.

   A preregistered drain limit (default 10 s) that expires first gives `drain-timeout`.
7. **Cross-join.** Every subtree lifetime from the connector has a terminal taskstats record, and every terminal record for a subtree tgid has a lifetime. Either kind of orphan makes the run incomplete. Because each process must appear on **both** channels, losing one message on one channel cannot hide a process.

**Calibration (K1c) must show** that the mechanism records the right peak, and that the following are all detected as `incomplete`, never as complete:
- **A short-lived child.** It allocates a known peak and exits within 1 ms; its peak must be present.
- **An early leader.** The thread-group leader exits before a worker raises the peak; the terminal record must carry the later peak.
- **Induced event loss.** A shrunken receive buffer under a fork storm must be detected as `incomplete`.
- **Lost connector delivery.** The harness's test mode discards selected messages. The resulting sequence gap and the cross-join orphan must both be detected.
- **Pid reuse.** A stress run must not join records to the wrong lifetime.

**Diagnostics and figure (a).**
- **Diagnostics only.** `VmHWM` polled from `/proc/<pid>/status` (a lower estimate) and `wait4` `ru_maxrss` (KiB on Linux, aggregated over the reaped subtree) are recorded as cross-checks. They are never used as figure (b).
- **Concurrent sum (a).** The sum of `VmRSS` over the group's processes every 10 ms. It is a sampled figure, used only as AQP and LQM define it (LQM:925); it never proves inventory.

*macOS (lead workstation, and the later macOS lanes):*
- `wait4`'s resource usage covers the terminated process and its children, so `ru_maxrss` (bytes on macOS) is not an own counter. The harness has no identified own lifetime RSS high-water counter it can read for arbitrary descendants without privileged task access.
- Every macOS run therefore records figure (b) as unavailable, with the reason `own-counter-unavailable-platform`. Its RSS is `incomplete`, and it can never be within budget. The concurrent sum (a) is still recorded, labelled diagnostic.
- This matches the existing rule that macOS lead-workstation samples are never Q6-labelled (`M3-PLAN.md:158`). A macOS own-counter source must exist before any macOS G13 lane can qualify RSS (OI-18).

*Joining host observations.* The host's operational record reports peak RSS per process (OPP:249). Each entry must carry the lifetime key (tgid and start time). The harness maps it to its own (tgid, fork timestamp) key through the open lifetime for that tgid. The join rules:
- **Matching entry.** The figure-(b) value for that segment is the larger of the harness counter and the host value. The host value can only raise a figure, never replace a missing harness counter.
- **Host entry with no registered lifetime.** The inventory is incomplete (reason `unregistered-process`), so the run is NON-PASS.
- **Registered lifetime with no host entry.** Allowed, because the host does not see every descendant. It is recorded.
- **Host value higher than the harness counter.** A defect is filed.

### 9.4 Phase timings from the operational record

The harness reads each run's operational record (OPP:249). The record holds:
- phase spans: discovery, snapshot and sealing, Plan, each provider (start, analysis, teardown), admission and replay, evaluation, commit and delivery, and cache and reuse decisions (OPP:248);
- wall time, CPU time and peak RSS per process (OPP:249);
- the INC-8 reuse disclosure: which results were recomputed and which reused (AQP:390; OPP:249).

At M3 the record reaches the harness as internal instrumentation and the exploratory envelope (OPP:250). The harness checks that:
- every phase is present or marked not applicable;
- the spans nest correctly and are monotonic;
- the **unattributed** time, elapsed minus the sum of the top-level phases, is non-negative. It is reported, never dropped, because no OpenSIP work is excluded (AQP:340).

Reuse disclosure is stored only in the envelope's `operationalRecords`, never in a semantic result (AQP:390). A run with no record, or with a record that fails these checks, has null phase fields and a typed reason (`record-missing`, `record-invalid`, `phase-missing`, `negative-unattributed`); nothing is synthesized (ENV `q6`). Instrumentation stays at the same preregistered setting for every sample (OPP:251).

### 9.5 Statistics, budgets, incomplete measurements and continuous integration

**Budgets.** The §5.2 budgets apply per size class (AQP:353-360), with the product ratios against a reviewed baseline. A null baseline never qualifies a cell (AQ:272-276). The seven samples and their maximum are diagnostics only (AQP:330).

**Complete and incomplete results (QD-25, for C2-Q0-R1-07).** Each workload, workflow, reset, control and batch result is either complete or incomplete.
- **Complete:** 3 warmups and 7 measured runs, every elapsed value present, and both RSS figures present for every run. Status is `within`, `over` or `no-baseline`.
- **Incomplete:** at least one run lacks a value. Each run slot then carries its measured values where they exist, `null` where they do not, and a list of typed reasons:
  - `run-failed`, `timeout`;
  - `own-counter-missing`, `own-counter-unverified`, `own-counter-unavailable-platform`;
  - `unregistered-process`, `pre-exec-image-unmeasured`;
  - `subscription-unverified`, `event-loss`, `unjoinable-identity`, `terminal-record-missing`, `terminal-record-duplicate`, `drain-timeout`;
  - `inventory-incomplete`;
  - `record-missing`, `record-invalid`.

  Failed runs are kept, never dropped and never re-run to fill the slot. Status is `incomplete`, which is never `within` and never counts toward Q6. The median and maximum are left null unless all seven values exist.

**Batches (QD-20, revised for C2-Q0-R1-07).** Every result carries a `batchId` (SHA-256 of the canonical tuple of round, workload, workflow, reset, control and ordinal) and a `batchOrdinal`: 1 for the first batch, 2 for the CI retry. Both batches of a retry live in the same envelope.
- **The retry.** On a threshold failure or an incomplete result, CI runs one more full batch, as AQP:490 allows.
- **The final verdict** is the batch with the highest ordinal, whichever way it goes, and is marked `final: true`. Exactly one batch per key is final. A schema cannot express that cross-row rule, so the envelope validator checks it, together with the population sums (ENV `description`). The better batch is never kept by choice, and both batches are kept in the record.
- **The batch join (C2-Q0-R2-02).** Every piece of supporting evidence names its batch:
  - each `operationalRecords[]` row carries its `batchId` and a **run slot** (`priming`, `warmup` 0–2, or `measured` 0–6);
  - each batch has exactly one `batchObservations[]` row (§9.6), keyed by `batchId`.
- **What the envelope validator checks.** These are cross-row rules a schema cannot express:
  - **Identity.** Each `batchId` equals the SHA-256 of its canonical key tuple.
  - **Coverage.** Every Q6 row's batch has one observation row. Every warmup and measured slot of that batch has exactly one operational record, or the row is `incomplete` and that slot lists `record-missing`.
  - **Uniqueness.** No two records share (`batchId`, slot).
  - **No orphans.** No record or observation row names a batch absent from `q6`.
  - **Sample consistency (C2-Q0-R2-N04).** In an incomplete row, a slot has a null sample if and only if it has at least one reason. The median and maximum are non-null only when all seven values are. `phaseTimingsPresent` is false if and only if `phaseAbsenceReason` is non-null.

  A violation makes the envelope invalid, not merely the row incomplete.
- **Flips.** A non-pass followed by a pass is counted as a `flip`. Three flips in any ten consecutive CI runs of a workload send that workload to noise review.

**Baselines** advance only through a reviewed baseline-advance record (AQP:491).

### 9.6 The D12 reference runner

The requirements, for D12 (AQP:534):
- a dedicated 4 vCPU / 8 GiB worker, at concurrency 1 (AQC:138-141);
- one selected, signed platform-profile lane per report (AQ:228-230, AQ:238-239);
- no network.

It records the fields in `runnerRequired` (LQM:926-937): CPU model, OS version and build, kernel, filesystem, host and provider-closure digests, compiler and runtime digests, cache state and measurement-tool digest.

**Q0 adds (QD-21):**
- **Quiet.** No other lead run set (`M3-PLAN.md:270`), and a one-minute load average below 0.2 before each batch.
- **Fixed CPU frequency policy,** with swap and power state recorded.
- **Storage.** The corpus store is on the runner's local disk.
- **Kernel interfaces.** On Linux: cgroup v2, the process-event connector and taskstats extended accounting, with the privileges they need, and the §9.3 calibration passed.
- **Carrier (N04; batch-scoped for C2-Q0-R2-02).** Each batch records its observations in its own `batchObservations[]` row, keyed by `batchId`. That row holds: load average before the batch (milli-units), CPU frequency policy, swap bytes in use, power state, whether the corpus store is on local disk, and the online-CPU set before and after. The §9.3 calibration results (`ownCounterVerified`, `spawnIsCloneVm`, kernel release) are per runner and toolchain, so they stay in `runner.calibration`.

**Labelling.** Samples from any other machine are labelled `lead-workstation` or `ci` (ENV `runner.runnerClass`) and are never Q6-labelled (`M3-PLAN.md:158`). For qualification at M6, the runner's identity and keys are authenticated under AQ:191-198; exploratory runs don't need that.

---

## 10. The corpus fetch and store

`corpus fetch` is a harness command, never a product command (AQP:207). It is the only networked step.

**Steps.** For each manifest entry `{repository URL, commit, treeDigest, licence, family, heldOut, submodulePolicy}`, the harness:
1. fetches exactly that commit, shallow;
2. materializes it into the content-addressed store at `store/<treeDigest>/`;
3. verifies the digest, then makes the tree read-only.

**The tree digest (QD-22)** is the SHA-256 of the canonical JSON array of `[path, mode, sha256(content)]`, sorted by path bytes. It is independent of Git's object hash. The manifest also records the Git tree ID, for cross-checking.

**Submodules and LFS** are either pinned explicitly in the manifest or excluded explicitly. A missing pinned object fails the fetch.

**At run time:**
- Every exploratory and qualification run takes the store as a read-only input. It re-verifies the tree digests of the repositories it uses before starting, and refuses on a mismatch (AQP:207).
- Runs set `HOME`, the XDG directories, `CARGO_HOME` and the npm cache to per-run scratch directories, so that no tool reads the user's configuration or real home.
- No run path contains network code.

**T3** has its own local manifest and fetches from local paths. Its source never leaves the machine (AQP:205).

---

## 11. The exploratory envelope (D13)

The schema is drafted as ENV, `exploratory-quality-envelope.schema.v1.json`, beside this record. It is a **separate** carrier, because RS3 stays closed and unchanged (AQP:419).

| Requirement | Where ENV meets it |
|---|---|
| It references unchanged RS3-shaped observations by digest (AQP:420) | `rs3Observations[]`: `reportSha256`, `schemaId` const `opensip.qualification.product-report.3`, `signed` |
| It records the product commit, corpus and ledger digests, the scoring-harness digest, the runner and the tool versions (AQP:421) | `product`, `harness`, `corpus`, `ledger`, `runner`, `tools` |
| It pins every metric definition and denominator (AQP:422) | `definitions` pins the metric-definition, preregistration, rule-spec and rubric digests. Each measured section carries its own numerators and denominators: Q2 per stratum and per repository, with corpus, sampled, settled, pending and unlabelled counts and line counts by class; Q3 and Q6 yield counts; Q7 per-rule populations and score histograms. A measured section must carry them, enforced by the schema's `if`/`then`; not-measured stays explicit. (C2-Q0-R1-06) |
| It declares itself non-qualifying (AQP:423) | `standing` const `exploratory-never-promoted`; `qualificationEvidence` const `false` |
| D13's exploratory class for unqualified advisory rules (AQP:237) | `unqualifiedAdvisoryRules[]` |
| INC-8 provenance and phase timings, outside semantic Coverage (AQP:390; OPP:249) | `operationalRecords[]`, by digest, each joined to a Q6 batch and run slot (§9.5) |
| Incomplete performance results and retry batches (§9.5) | `q6.workloads[]` is a closed `oneOf` of complete and incomplete variants, with per-run nullable samples and typed reasons, `batchId`, `batchOrdinal` and `final` |
| Runner observations (§9.6) | `batchObservations[]` per batch; `runner.calibration` per runner |

**What a valid envelope does not do.** It is never a G13 input and is never promoted (AQP:425, AQP:433). Validating against ENV says nothing about whether the claims inside are true. Envelopes are signed only in the sense that their digests are pinned. They need no authenticated runner, because they claim nothing that requires one.

---

## 12. Report outputs and Q1–Q8

| Q | Envelope section | Reported values | Status values |
|---|---|---|---|
| Q1 | `q1.cells[]` | per cell: expected, actual, missing and extra counts and exit match, computed by the gate (PQV:24-27); the RS3 report digest | `exact`, `mismatch` |
| Q2 | `q2.strata[]`, `q2.repositories[]` | **Per stratum** (rule × language × mode × target × evidence set): estimand (`family-weighted`); method; *k*; corpus, sampled, settled, pending and unlabelled counts; true, false and unclear counts; the guard's verified and optimistic values; `censusPrecisionPpm` (null unless nothing is unlabelled or pending); the sample ratio (descriptive); resolved-label precision (descriptive, AQP:232); *L*; concentration (AQP:238); per-family *N_j*, *a_j* and true counts. **Per repository** (AQP:238, AQP:151): repository, commit, tree digest, family, evidence set, the same label and population counts, and analysed lines by class (hand-written, generated, vendored, excluded), with false positives split between hand-written and generated or vendored code, so that FP/KLOC and findings/KLOC can be recomputed from counts. False-positive cost (AQP:239) is carried as median triage time. | §5.6 |
| Q3 | `q3.strata[]` | answerable positives, hits, misses by cause (§1.3), abstentions on answerable cases, answerable negatives and determinate negatives, so that yield is determinate ÷ answerable (AQP:152), and mutant accounting by family (§6.3) | `measured`, `insufficient` (no answerable positives) |
| Q4 | `q4` | unsupported determinate negatives and false completeness claims (each must be 0; AQP:142), deficiency mismatches | `zero`, `nonzero` |
| Q5 | `q5.survival[]`, `q5.determinism[]` | survival per rule × transformation, with counts; spurious CODE-NET-NEW and CODE-FIXED; discarded and unvalidated pairs; determinism variant results | `measured`, `insufficient` (< 20); `exact`, `differs` |
| Q6 | `q6.workloads[]` | per workload × workflow × reset × control × batch: 7 elapsed samples and both RSS figures per run (nullable only in the incomplete variant), median, max, baseline, phase-timing state with a typed absence reason, unattributed time, yield as `determinateCases` ÷ `answerableCases`, runner class, `batchId`, `batchOrdinal` and `final` | `within`, `over`, `no-baseline`, `incomplete` |
| Q7 | `q7.rules[]` (M4, D8) | per rule: finding population; sample size (50, or all findings if fewer, labelled `small-population`); fields required and present; proof joins checked and failed; score histogram for 1 to 5 and the score sum; items scoring ≤ 2 and their dispositions; gating or repair-eligible items in the sample and their dispositions; median triage time; accepted and dismissed counts (AQP:408-411) | `measured`, `not-measured` |
| Q8 | `q8.shapes[]` | manual corrections per pinned shape (SMAP:67; AQP:146) | `measured`, `not-measured` |

Time to first trustworthy result is reported under Q6 (AQP:153). Before D13's DR-G13 successor is accepted, Q2–Q8 are never qualification evidence (AQP:427-431).

---

## 13. Implementation units and K2 sizing

| Sub-unit | Contents | Size (`M3-PLAN.md:146-150`) |
|---|---|---|
| K1a | case and ledger libraries, canonical digests, the freeze, `corpus fetch` and the store (§1, §3, §10) | M |
| K1b | the confidence module: exact rational Clopper–Pearson, the product bound, status rules, and a self-test against §5.4 and §5.5's reference values | S |
| K1c | the run driver: resets, the RSS sampler, operational-record ingestion, the determinism driver (§8.4, §9), and envelope emission | M |
| K2a | T1, TS/JS lane: 33 cells | XL part, 5 days |
| K2b | T1, Rust lane: 22 cells | XL part, 5 days |
| K2c | T1, syntax-only lane: 11 cells, per grammar (AQ:233-234) | 3 days |
| K2a-r, K2b-r, K2c-r | each lane's independence review and oracle freeze | 1 day each |

The cell counts are `M3-PLAN.md:58`. The T1 obligation is all 57 supported cells per mode, typed refusal for 6 and non-advertisement for 3 (AQP:481).

**K2 estimate: 16 days of serialized lane work** (5 + 5 + 3, plus 3 one-day lane reviews), using the plan's planning durations (`M3-PLAN.md:197-200`). This is a planning assumption, not a measurement. r1 counted 2 review days for all three lanes; r2 reviews and freezes each lane separately, so it costs one more day.

**The independence gate (QD-26, for C2-Q0-R1-08).** K2 is authored before the producers so that expected answers are independent (`M3-PLAN.md:172`). Finishing by day 21 does not by itself secure that, so the gate is per lane:
- **The freeze.** A lane's oracle is **frozen** by a ledger `freeze` record pinning its fixture-manifest and case-set digests, after its lane review. The review checks that no expected answer was derived from producer output.
- **The ordering.** The freeze must precede, in the ledger chain, the **first producer run on that lane's T1 fixtures**, and K2 authors never see producer output for those cells before it.
- **Enforcement.** The T1 runner refuses a lane that has no freeze. A producer may be *authored* earlier, and may be tested on its own unit fixtures, but it is not run on T1 fixtures before the freeze.

**The schedule against the M3 table (`M3-PLAN.md:202-227`).** The earliest producer activity in each lane sets that lane's deadline:

| Lane | Earliest producer activity on its inputs | Oracle frozen by | Placement |
|---|---|---|---|
| Rust (K2b) | G2-v, launch and validation from day 2 to day 3, after D1 (`M3-PLAN.md:210`, `M3-PLAN.md:215`) | before day 0 | **pre-day-0**: K2b + K2b-r, 6 days |
| syntax-only (K2c) | E2 parser work from day 3, after C2 (`M3-PLAN.md:206`, `M3-PLAN.md:212`) | before day 0 | **pre-day-0**: K2c + K2c-r, 4 days |
| TS/JS (K2a) | F1 from day 7, after C1, C2 and D3 (`M3-PLAN.md:213`) | end of day 6 | **days 0–6**: K2a + K2a-r, 6 days |

**Consequences.**
- **Pre-day-0.** 10 days of K2 join the pre-day-0 work, after Q0 is accepted, in parallel with S-M, T2b, S-P with G2 authoring, CF-P and L acceptance (`M3-PLAN.md:243-248`). If the other pre-day-0 items finish sooner, K2 becomes the latest pre-day-0 item, at Q0 + 10 days.
- **Days 0–6.** K2a has one day of margin before F1's day-7 start. If K2a-r slips, F1 may still be authored, but its first run on TS T1 fixtures waits.
- **Slip, computed through every dependency (C2-Q0-R2-03).** This record does not split F1's completion from its first T1 run, so conservatively a delay to that run delays F1's finish, and with it the whole F branch. Let *s* be the K2a freeze's slip past day 6, and *d* = max(0, *s* − 1) the resulting delay to F1. From the plan's rows (`M3-PLAN.md:208`, `M3-PLAN.md:213`, `M3-PLAN.md:217-227`):
  - F1 = 10 + *d*; F2 = 14 + *d*; F3 = 17 + *d*;
  - H = max(C4 = 12, F1) + 3; J2 = H + 3; J3 = max(J2, F2, G3 = 15) + 3; I2 = H + 2;
  - M3-M = max(J3, G4 = 18, F3, I2, K2 = 6 + *s*, …) + 3; M3-X = max(M3-M, R, J4 = J3 + 2, 23, O2_selected) + 2.

  r2 checked F2 against J3 alone and missed the path F1 → H → J2. With every other day-0 and branch assumption held (including O2_selected ≤ 24), the result is:

  | *s* (oracle slip) | *d* (F1 delay) | F1 | H | J2 | J3 | M3-M | M3-X |
  |---:|---:|---:|---:|---:|---:|---:|---:|
  | 0–1 | 0 | 10 | 15 | 18 | 21 | 24 | 26 |
  | 2 | 1 | 11 | 15 | 18 | 21 | 24 | 26 |
  | 3 | 2 | 12 | 15 | 18 | 21 | 24 | 26 |
  | 4 | 3 | 13 | 16 | 19 | 22 | 25 | 27 |
  | 5 | 4 | 14 | 17 | 20 | 23 | 26 | 28 |

  So **M3-X = 26 + max(0, *d* − 2) = 26 + max(0, *s* − 3)**. H's slack against F1 is 2 days (C4 finishes at 12 and F1 at 10), so 3 days of oracle slip fit (the 1-day margin plus 2), and every further day moves the host chain by a day. r2's "up to 4 days" is withdrawn.
- **If authoring and first T1 run are later split.** Should F1's law allow F1 to finish and feed H while only its T1 conformance run waits, H would no longer depend on the freeze. The slip would then reach M3-X only through F2, F3 and K2. That schedule is not assumed here, and OI-12 recomputes it if it is adopted.
- **Formulas with no slip.** K2 finishes by day 6. R = max(15, 6) + 2 = 17, and M3-M = max(21, 6) + 3 = 24, so the day-21 K2 condition (`M3-PLAN.md:233`) holds by construction.

**The M3-PLAN bounds to update under OI-12:**
- the K2 row (`M3-PLAN.md:222`): 16 days, 10 before day 0 and 6 by day 6;
- the R and M3-M rows (`M3-PLAN.md:225-226`): K2 = 6;
- the K2 clause of the condition (`M3-PLAN.md:233`, `M3-PLAN.md:239`);
- "K2's size" in the unbounded list (`M3-PLAN.md:241`): it is now bounded;
- the pre-day-0 list (`M3-PLAN.md:243-248`): add K2b and K2c, 10 days after Q0;
- F1's row (`M3-PLAN.md:213`): its first T1 run waits for K2a's freeze;
- the slip rule: M3-X = 26 + max(0, *s* − 3), for K2a freeze slip *s* past day 6, through F1 → H → J2 (C2-Q0-R2-03).

The rejected alternative was to delay every producer behind all three lane oracles. That would delay G2-v and E2 and lengthen the host chain.

---

## 14. Open items, with owners

| ID | Item | Owner | Blocks |
|---|---|---|---|
| OI-1 | **D13**: accept the exploratory envelope (ENV) | lead, owner sign-off (AQP:535) | S-M's report, M3-M (`M3-PLAN.md:158`) |
| OI-2 | **D13 successor**: the DR-G13/report/harness successor that carries this record's case model, ledger, confidence rule and oracles into qualification (AQP:427-431) | Language quality + Product + Release engineering (QG:264) | Q2–Q8 qualification at M6 |
| OI-3 | **Q2 achievability** (§5.8): grow T2 held-out families toward *k*_min, or revisit D4 | owner (D4, AQP:525); lead (D3 sizing, AQP:524) | any Q2 PASS |
| OI-4 | The estimand: family-weighted, with the pooled guard (QD-11, QD-15), against finding-weighted | DR-G13 successor owners | Q2 qualification |
| OI-5 | Per-stratum against family-wise confidence across strata (§5.6) | DR-G13 successor owners | Q2 qualification |
| OI-6 | Differential tools and Rust compile validation that execute repository code (QD-17, §6.2) are outside M3. They wait for the authorized execution path: M5 `execution.rs`, `RepoExecutionGrantV2` and the M5-EX successors (`M3-PLAN.md:319`, `M3-PLAN.md:347-352`). Confinement is an additional condition, not the authorization. | M5-EX successor owners (`M3-PLAN.md:347-350`); lead | the Rust differential; Rust mutant compile checks (M5 or later) |
| OI-7 | **D12**: select the reference runner (§9.6) | release engineering; lead with owner sign-off (AQP:534) | Q6-labelled samples |
| OI-8 | Q3 and Q5 confidence statements. AQP sets point targets and a population floor of 20 (AQP:141, AQP:313); this record adds no bound. | DR-G13 successor owners | Q3/Q5 qualification |
| OI-9 | **D7**: declared correspondence for moved and renamed subjects (§8.3) | lead + identity owner (AQP:529) | Q5 at M5 |
| OI-10 | **D8**: explanation fields (Q7) | lead + reporting owner (AQP:530) | Q7 at M4 |
| OI-11 | The operational-record carrier after M3: S-OP-1 and S-OP-6 (OPP:250) | OPP §9 owners | M4 `--timings` |
| OI-12 | Fold K2's estimate and lane gates (§13) into M3-PLAN's bounds, as listed in §13 | lead | the M3 total |
| OI-13 | **D1**: QG items[12] still says "cold/warm p95" (QG:268). The harness follows AQ:268-282 and PQV:28. | lead (AQP:522) | record hygiene only |
| OI-14 | The expert roster and capacity (§4.6) | owner (`M3-PLAN.md:368`) | resolving gating labels |
| OI-15 | **D2**: where the catalog lives (§2) | lead + evaluator owner, owner sign-off (AQP:523) | the M5 product pack |
| OI-16 | Family assignment for each T2 entry (§5.3) | M3-T2 (lead), D3 sign-off | the freeze |
| OI-17 | A sample-based pooled-precision guard: per-family exact hypergeometric lower bounds at α/*k* (§5.6). Until it is approved, the conservative verified-true guard is in force. | DR-G13 successor owners (QG:264); lead proposes | advisory Q2 PASS without near-complete adjudication |
| OI-18 | A macOS own lifetime RSS counter source (§9.3). Until one exists, macOS RSS is `incomplete`. | release engineering (D12); lead | any macOS G13 RSS qualification |

## Lead decisions in this record

QD-1 integer millionths and directional rounding · QD-2 outcome table · QD-3 proposition class · QD-4 JSON Lines ledger with a hash chain · QD-5 hard components and the full truth-input closure · QD-6 the separated populations · QD-7 the 20-minute time box · QD-8 calibration numbers · QD-9 agreement triggers · QD-10 the model-family rule · QD-11 family-weighted estimand · QD-12 independence families · QD-13 the cluster product bound · QD-14 *k*_min · QD-15 the two-sided pooled guard · QD-16 mutant states · QD-17 differential execution boundary · QD-18 determinism variants · QD-19 process inventory, the positive completeness proof and own RSS counters · QD-20 CI retry, batches and batch joins · QD-21 runner additions · QD-22 tree digest · QD-23 held-out exposure · QD-24 advisory water-filling allocation · QD-25 complete and incomplete performance results · QD-26 the K2 lane-freeze gate.

## Not claimed

- No product measurement, corpus fetch, adjudication or product run was performed for this record. The values in §5 are exact arithmetic, computed for this record. Validity rests on the analytic proof in §5.5.
- No contract, schema, gate, threshold or register row is changed. RS3 is unchanged.
- ENV is a draft for D13, not an accepted carrier.
- The differential tools' execution behaviour is to be confirmed by each pin's canary check (QD-17).
- The Linux counter mechanism (§9.3) is to be confirmed by K1c's calibration on the D12 kernel. Until then, Linux RSS is `incomplete`.
- The K2 estimate and its lane schedule are planning assumptions.
