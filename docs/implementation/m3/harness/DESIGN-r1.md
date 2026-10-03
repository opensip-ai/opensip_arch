# M3-Q0 quality-harness design record — r1

Draft r1. Claude Opus 5.5, implementation lead. Unit **M3-Q0** of the accepted M3 unit plan (`M3-PLAN.md:157`).

## Standing

**This is a design record, not law and not a contract successor.** It changes no accepted contract, schema, gate, threshold or register row. It fixes the harness mechanisms that the accepted analysis-quality plan leaves to "the harness design" (AQP:235, AQP:480), so that K1, K2, I2, S-M and M3-M can be implemented from it directly. Nothing here has been measured or run.

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
| `heldOut` | boolean: a member of the held-out repository set or a held-out mutation family (AQP:219, AQP:278) |
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
| `subjectPopulation` | universe, subject kind, include/exclude (AQP:169) |
| `predicate` | the exact proposition in words, plus an `emitWhen` sketch (AQP:170). I2 binds the relation IDs. |
| `configurations` | mode, targets, features, cfg and dev/build/test scope (AQP:171) |
| `closedWorld` | the `ClosedWorldV2` fields the rule needs (AQP:172; NE:2210-2224) |
| `minimumSufficiency` | the relation@rung and Coverage that must be complete for a determinate negative (AQP:173) |
| `lookalikes` | legitimate cases that must not fire (AQP:174) |
| `default` | gating, advisory, or gating only after declared policy (AQP:175) |
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

**Soft components may differ, provided the truth-relevant inputs are unchanged:**

| Component | Bound to |
|---|---|
| `treeDigest` | the repository tree (AQP:253) |
| `evidenceRefs` | the finding's evidence references (`finding3`, IE:190; AQP:255). These are detector output, recorded for the unexplained-change trigger below. They never justify reuse. |
| `truthInputDigest` | the truth-relevant input digest, defined next |

**The truth-relevant input digest (TRI)** covers the subject, its incoming references and the proof's evidence references (AQP:257). It must be computed **without the detector**. If the detector's own reference set were used, a new real reference that the detector missed would leave the TRI unchanged, and a stale "true" label would be carried. So the harness computes the TRI from its own lexical scan, using the spec's `propositionClass` (§2.1):
- **Existential rules.** The digests of the subject's declaring file, of every file named in the witness, and of the universe's manifest and resolution-configuration files (`package.json`, `tsconfig*.json`, `Cargo.toml`, `Cargo.lock`, `.cargo/config*`).
- **Universal-negative rules.** The declaring file's digest; the manifest and configuration files above; every file in the selected universe in which the subject's identifier occurs as a token, or which names the declaring module in an import or `use` specifier; and every file that contains a nonliteral loading construct (`require(` or `import(` with a nonliteral argument, `eval`, or reflective access). This is a deliberate over-approximation of the possible referrers.

**The carry rule** (AQP:257). A label carries only if every hard component is identical and either the soft components are identical, or only `treeDigest` differs and the `truthInputDigest` is identical. The check is mechanical, and its per-component result is written as a `carry` record.

**Re-adjudication triggers** (AQP:258-261). Each trigger maps to a mechanical test:
- a change to the rule, rubric, configuration, dependency set or prepared outputs: any hard component differs;
- a change to the subject or its incoming references: `truthInputDigest` differs;
- a change in detector output that no input change explains: every component of the key, `truthInputDigest` included, is identical, but `evidenceRefs` or the finding's message parameters differ. This both re-queues the item and files a determinism defect (§8.4).

`finding-key2` is used only to *propose* which earlier label might apply. It is never a reason to carry one (AQP:256; IE:199-213).

### 3.4 Evidence counts

Following CODEX2's r2 observation N02 (`docs/implementation/m3/analysis-quality/reviews/codex2-analysis-quality-plan-r2/review.json`, C2-AQ-R2-N02), three populations are kept apart (**QD-6**):
- **the corpus population:** every finding the candidate emitted in a stratum;
- **the adjudicated sample:** the findings with a settled resolution, all of them for gating and repair-eligible rules (AQP:228);
- **the independent evidence units:** what the confidence rule counts (§5).

Calibration items are never in any of the three. A finding that appears in two rounds through a carried label counts once per round, not twice. Carried labels count as evidence only in the round that carried them.

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

The target generalizes beyond the corpus. Gating findings on T2 are adjudicated in full (AQP:228), so precision on the frozen corpus is a census: the harness knows it exactly. The 95% statement is about repositories like those in the corpus, and the unit that is sampled from that population is the **repository**, not the finding.

**QD-11.** The bound is placed on the **repository-weighted conservative precision**: the mean over independence families (§5.3) of each family's conservative precision, among families in which the rule fires. Two reasons:
- A finding-weighted bound over correlated findings invents independent evidence. This is the counterexample in the CODEX2 review that produced AQP:235 (the same review file, C2-AQ-R2-01 `analyticIllustration`).
- The repository-weighted quantity is what a single team sees on its own repository.

AQP's pooled ratio, true ÷ all reported (AQP:232), is kept beside it as a census guard (§5.5), so a large, poor repository cannot be averaged away.

Reviewers should check this choice. If the DR-G13 successor wants a finding-weighted estimand instead, §14 OI-4 records the alternative.

### 5.2 Which bound applies

The method is chosen from the **structure** of the stratum before any label is read, so the choice cannot follow the labels. Let *k* be the number of families with at least one finding in the stratum, and let *n_j* be the number of evidence findings from family *j*.

- **Independent sample** (AQP:234): every *n_j* = 1. Each finding then comes from a different family, and the findings are independent Bernoulli draws with the repository-weighted mean as their success probability. **Method: exact Clopper–Pearson** (§5.4).
- **Clustered** (AQP:235): some *n_j* > 1. **Method: the cluster-level product bound** (§5.5).

**Where the independent design comes from.** For an advisory stratum with at least 100 families, the preregistered sampling draws exactly one finding per family, uniformly, with a recorded seed. That makes it an independent sample by construction (§5.7). AQP:228's minimum of 100 is then 100 families. Gating strata are adjudicated in full (AQP:228), so they are independent only when every family contributes a single finding.

### 5.3 Independence families

The independence unit is a **family** of repositories, not a single repository (**QD-12**). Repositories go in one family if any of these hold:
- one is a fork, mirror, vendored copy or split of another;
- they share generated code from the same generator;
- they are parts of one multi-checkout workspace assembly (the D15 approximation is **one** family; AQP:217);
- they share an upstream project, for example a repository and its examples repository.

Sharing an organization alone does not merge two repositories.

Families are assigned in the T2 manifest by M3-T2, reviewed, and pinned by `familyMapDigest` at the freeze. Families with no finding in a stratum do not count toward that stratum's *k*. T3 repositories form their own families, labelled `T3-local` (AQP:205).

**The assumption every method needs.** Each bound treats the families as independent draws from the population of repositories the claim is about. T2 is purposely selected (AQP:213-219), not randomly sampled. The held-out discipline (§5.6) guards against tuning on the corpus, but not against unrepresentative selection. The envelope states this assumption on every Q2 result (ENV `q2.strata[].assumption`).

### 5.4 Exact Clopper–Pearson (independent strata)

Let *x* be the true count out of *k* single-finding families. The one-sided 95% lower bound *L* is the *p* that solves P(Bin(*k*, *p*) ≥ *x*) = α, with α = 0.05; *L* = 0 when *x* = 0. Equivalently, *L* is the α quantile of Beta(*x*, *k* − *x* + 1).

**Exact decision.** *L* ≥ *t* holds exactly when Σ_{i=x}^{k} C(*k*, *i*) *t*^i (1 − *t*)^{k−i} ≤ α. The harness evaluates this in exact rational arithmetic, with *t* = 99/100 or 9/10 and α = 1/20. It reports *L* rounded down to millionths, found by bisection.

Reference values, computed for this record:
- *x* = *k* = 299 gives 0.990031, and 29 gives 0.901855 (AQP:234's examples);
- one error needs *k* = 473 to reach 0.99, and *k* = 46 to reach 0.90.

### 5.5 The cluster-level product bound (clustered strata)

**Chosen method (QD-13).** For each family *j*, let *X_j* ∈ [0, 1] be that family's conservative precision in the stratum: its census value for gating rules, or its uniform within-family sample estimate for advisory rules (§5.7). Then

> *L* = α^{1/k} · (Π_j *X_j*)^{1/k}, that is, α^{1/k} times the geometric mean of the per-family precisions; *L* = 0 if any *X_j* = 0.

**Exact decision.** Pass iff Π_j *X_j* ≥ *t*^k / α. Each *X_j* is the rational *t_j*/*n_j*, so this is an exact integer comparison.

**Why it is valid.** Fix any *m* in (0, 1]. Suppose the families are independent and the average of their expected precisions is at most *m*. Each *X_j*/*m* is non-negative, and the product of their expectations is at most 1 (by the AM–GM inequality, applied to the family means). So the product is an e-value, and Markov's inequality gives P(Π *X_j* / *m^k* ≥ 1/α) ≤ α. Taking *m* to be the true mean, P(*L* ≥ true mean) ≤ α.

This needs no model of how findings correlate inside a repository, no prior, no asymptotics and no resampling. It also does not need the families to be identically distributed: it bounds the average of their means. It is the fixed-bet, all-in case of the betting confidence bounds for bounded means (Waudby-Smith and Ramdas, *JRSS-B*, 2024; Vovk and Wang, *Ann. Statist.*, 2021).

**The zero-error boundary.** If every family is all-true, *L* = α^{1/k}. That is exactly the Clopper–Pearson bound for *k* independent observations. It is also the most any method can honestly claim without a within-repository model: if each repository were all-true or all-false (perfect within-repository correlation) with mean *μ*, the chance of seeing *k* all-true repositories would be *μ*^k. So 300 findings from 3 perfect repositories give *L* = 0.368, as CODEX2's illustration requires. Identical all-true repositories are never resampled into a pass (AQP:235).

**It uses partial information.** Unlike reducing each family to a single clean/unclean bit, a family at 0.995 contributes 0.995, not 0. With 30 families at 1.0, *L* = 0.904966. With 29 at 1.0 and one at 0.90, *L* = 0.901793, which passes 0.90. With 29 at 1.0 and one at 0.50, *L* = 0.884297, which does not.

**What it costs.** When findings inside a repository really are independent, the bound is far more conservative than it needs to be. That is the price of assuming nothing about how findings correlate within a repository. A simulation was run for this record. It is not a product measurement. There were 4,000 trials per scenario, with *k* from 30 to 300 and mean precision from 0.90 to 0.99, under three models:
- perfect within-repository correlation, which is the worst case: the bound reached or exceeded the true mean in 0.039 to 0.049 of trials, at or below α;
- within-repository independence: never;
- beta-distributed per-repository precision: never.

**One harsh property, accepted.** A single family whose findings in the stratum are all false or unclear sets *L* = 0. For a gating rule, a repository where every finding is wrong is a defect worth failing. Gating unclear labels go to the expert first (§4.5), so this happens only when the expert also cannot confirm a single finding in that repository.

**Rejected alternatives:**
- **Repository bootstrap.** It is degenerate at zero errors (AQP:235).
- **Beta-binomial or Bayesian hierarchical model.** At zero errors the data cannot identify the within-repository correlation, so the bound would be set by the prior on that correlation. A credible bound is also not the 95% confidence statement Q2 asks for.
- **Design-effect correction with an assumed intraclass correlation.** It is asymptotic, and it needs an assumed correlation that cannot be checked when there are no errors.
- **Reducing each family to a clean/unclean indicator, then Clopper–Pearson.** It is valid, but it throws away partial information.

### 5.6 Status rules, minimum counts and INSUFFICIENT-EVIDENCE

**Minimum independent families.** At zero errors both methods give α^{1/k}, so a pass needs *k* ≥ *k*_min(*t*) = ⌈ln α / ln *t*⌉ (**QD-14**):

| Target | *k*_min | Check |
|---|---|---|
| advisory 0.90 | **29** | 0.05^{1/29} = 0.901855; 0.05^{1/28} = 0.898534 |
| gating and repair-eligible 0.99 | **299** | 0.05^{1/299} = 0.990031; 0.05^{1/298} = 0.989998 |

These are floors, not sufficient counts: any error raises the requirement (§5.4).

**The census guard (QD-15).** The stratum's pooled conservative precision on the frozen corpus, true ÷ all reported (AQP:232), must also meet the target. This catches a large repository with poor precision that the repository-weighted bound would average down.

**Status, per stratum and target, decided in this order:**
1. `NOT-YET-ADJUDICATED`: some finding in the stratum's evidence lacks a settled label (`M3-PLAN.md:173`). Exploratory only; it is never a Q2 result.
2. `INSUFFICIENT-EVIDENCE`: zero findings, or *k* < *k*_min(*t*) (AQP:236). The bound is still reported.
3. `FAIL`: the census precision is below *t*.
4. `PASS`: *L* ≥ *t* by the exact decision in §5.4 or §5.5.
5. `INSUFFICIENT-EVIDENCE`: otherwise. The census meets the target, but the bound does not.

Neither non-pass status is ever a pass (AQP:236).

**Which families count for acceptance.** The acceptance computation counts only **held-out** families, whose findings and labels were not inspected during rule development (AQP:219, AQP:433). Development families give exploratory numbers only, labelled `development`. Both are reported.

**Downgrading** (AQP:237).
- A gating stratum that does not PASS at 0.99 is evaluated at 0.90. If it passes, the rule may ship as a qualified advisory rule.
- If it does not pass at 0.90 either, it may ship only as a declared-unqualified exploratory advisory rule. It gets no Q2 pass and no waiver, and it is listed in the envelope's `unqualifiedAdvisoryRules`.
- Both targets are fixed before measurement, so the downgrade involves no tuning.

**Confidence is per stratum.** 95% applies to each stratum, as AQP:233 states. With *S* strata, a release could hold false passes on up to about 0.05·*S* of them in expectation. The plan sets no family-wise correction, and this record does not invent one. §14 OI-5 routes the question to the DR-G13 successor.

### 5.7 Preregistration

Before any acceptance measurement, the freeze record (§1.5) pins a **preregistration document** (`preregistrationDigest`). It fixes:
- α = 1/20, and the targets 99/100 and 9/10;
- the estimand (§5.1), and the method-selection rule (§5.2);
- the family map and the held-out set;
- **advisory sampling.** If the stratum has at least 100 families, one finding per family. Otherwise ⌈100 / *k*⌉ findings per family, or all of that family's findings if it has fewer. Findings are drawn uniformly within each family, with the seed `SHA-256(roundId ‖ stratumId)`.
- the census guard and the status order (§5.6);
- the rounding rule (QD-1).

None of these may change after the freeze for that round (AQP:159).

### 5.8 What this means in practice, reported to the owner

Under this rule, a **gating 0.99 PASS needs at least 299 held-out families with findings for that rule, language and mode, and zero errors.** An advisory 0.90 PASS needs at least 29. T2 plans at least two repositories per language per size class, with one held out per class (AQP:218-219). Gating strata will therefore be INSUFFICIENT-EVIDENCE unless T2 grows by an order of magnitude.

This is not a defect of the chosen method. Without a within-repository model, no valid 95% method can do better (§5.5). The cheapest path to an advisory PASS is about 30 to 50 extra small public held-out repositories, sampled one finding per family, which is about 60 to 100 votes. The gating path costs 299 or more held-out families, with every gating finding adjudicated. Choosing between them is the D4 revisit (AQP:148, AQP:525) and D3 sizing (AQP:524); see §14 OI-3.

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
2. **Well-formedness.** The mutant parses with the pinned grammar. For TS/JS, the pinned TypeScript compiler type-checks it without emitting; this executes no repository code. For Rust, nothing that would run build scripts or proc-macros is used (`M3-PLAN.md:355`), so a Rust mutant has no compile check at M3.
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

**Repository-code execution (QD-17).**
- Some of these tools build the crate, which runs build scripts and proc-macros: rustc's lints through a build, and cargo-udeps. Knip can load and evaluate repository configuration files.
- At M3 no repository code executes (`M3-PLAN.md:355`). So these tools run only once the O7 profile or a disposable container with no network and no credentials is available, and only on public T2 bytes, never on T3.
- Until then, only tools that do not execute repository code run. Each tool's mode is checked when it is pinned, and the pin records it.
- See §14 OI-6.

**Why a tool is not an oracle.**
- The tools answer different propositions. rustc's `dead_code` is crate-local and does not see cross-crate `pub` use, which is where OpenSIP adds value (AQP:184). cargo-machete is lexical. Knip uses its own entry-point heuristics.
- They have their own false positives, and their answers depend on configuration.

A tool's output is therefore never an oracle and never G13 evidence (AQP:288-289). The tools run only inside the harness, never as a product dependency or fallback (AQP:289).

**From disagreement to curated case:**
1. **Normalize.** Each tool's finding is mapped to a catalog proposition through that tool's published proposition mapping, or marked non-overlapping (AQP:282).
2. **Compare** against OpenSIP's result on the same case key (§1.2).
3. **Adjudicate** every normalized disagreement under §4 into one of four classes (AQP:283-287): `confirmed-comparable-defect`, `other-tool-false-positive`, `semantic-non-overlap` or `unresolved`.
4. **Curate.** Only a confirmed comparable defect becomes a case: `origin=curated-differential`, with its expected answer taken from the settled label and a ledger reference (AQP:288). It joins the **next** frozen round (§1.5), and is held out if its repository is.

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
- **(b) the sum of high-water marks:** the sum, over every process in the tree, of that process's own high-water counter.

The run's value is the **larger of (a) and (b)**. The cell statistic is the maximum of the seven run values (AQ:270; PQV:28).

**Where the per-process counter comes from (QD-19).** It is the larger of two readings:
- the harness's own observation: `wait4` `ru_maxrss` for its direct child (bytes on macOS, KiB on Linux), and the polled per-process peak for every other descendant;
- the per-process peak RSS in the host's operational record (OPP:249).

A process with no counter makes the run NON-PASS (LQM:925). If the host reports a lower peak than the harness observed, a defect is filed.

### 9.4 Phase timings from the operational record

The harness reads each run's operational record (OPP:249). The record holds:
- phase spans: discovery, snapshot and sealing, Plan, each provider (start, analysis, teardown), admission and replay, evaluation, commit and delivery, and cache and reuse decisions (OPP:248);
- wall time, CPU time and peak RSS per process (OPP:249);
- the INC-8 reuse disclosure: which results were recomputed and which reused (AQP:390; OPP:249).

At M3 the record reaches the harness as internal instrumentation and the exploratory envelope (OPP:250). The harness checks that:
- every phase is present or marked not applicable;
- the spans nest correctly and are monotonic;
- the **unattributed** time, elapsed minus the sum of the top-level phases, is non-negative. It is reported, never dropped, because no OpenSIP work is excluded (AQP:340).

Reuse disclosure is stored only in the envelope's `operationalRecords`, never in a semantic result (AQP:390). A run with no record has null phase fields and a reason; nothing is synthesized. Instrumentation stays at the same preregistered setting for every sample (OPP:251).

### 9.5 Statistics, budgets and continuous integration

**Budgets.** The §5.2 budgets apply per size class (AQP:353-360), with the product ratios against a reviewed baseline. A null baseline never qualifies a cell (AQ:272-276). The seven samples and their maximum are diagnostics only (AQP:330).

**CI retry (QD-20).** On a threshold failure, CI runs one more full batch, as AQP:490 allows. The second batch's verdict stands, whichever way it goes, and both batches are kept in the record. A fail followed by a pass is counted as a `flip`. Three flips in any ten consecutive CI runs of a workload send that workload to noise review. The better batch is never kept by choice. This answers CODEX2's observation N02.

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
| It pins every metric definition and denominator (AQP:422) | `definitions` (metric-definition, preregistration, rule-spec and rubric digests); every result carries its explicit counts |
| It declares itself non-qualifying (AQP:423) | `standing` const `exploratory-never-promoted`; `qualificationEvidence` const `false` |
| D13's exploratory class for unqualified advisory rules (AQP:237) | `unqualifiedAdvisoryRules[]` |
| INC-8 provenance and phase timings, outside semantic Coverage (AQP:390; OPP:249) | `operationalRecords[]`, by digest |

**What a valid envelope does not do.** It is never a G13 input and is never promoted (AQP:425, AQP:433). Validating against ENV says nothing about whether the claims inside are true. Envelopes are signed only in the sense that their digests are pinned. They need no authenticated runner, because they claim nothing that requires one.

---

## 12. Report outputs and Q1–Q8

| Q | Envelope section | Reported values | Status values |
|---|---|---|---|
| Q1 | `q1.cells[]` | per cell: expected, actual, missing and extra counts and exit match, computed by the gate (PQV:24-27); the RS3 report digest | `exact`, `mismatch` |
| Q2 | `q2.strata[]` | per rule × language × mode × target: `heldOut` or `development`; method; *k*; census true/false/unclear counts; census precision; resolved-label precision (descriptive, AQP:232); *L*; concentration (AQP:238); per-family precision; FP/KLOC and findings/KLOC (AQP:151), stored as integers per million lines; false-positive cost (AQP:239) | §5.6 |
| Q3 | `q3.strata[]` | answerable positives, hits, misses by cause (§1.3), abstentions on answerable cases, yield (AQP:152), mutant accounting by family (§6.3) | `measured`, `insufficient` (no answerable positives) |
| Q4 | `q4` | unsupported determinate negatives and false completeness claims (each must be 0; AQP:142), deficiency mismatches | `zero`, `nonzero` |
| Q5 | `q5.survival[]`, `q5.determinism[]` | survival per rule × transformation, with counts; spurious CODE-NET-NEW and CODE-FIXED; discarded pairs; determinism variant results | `measured`, `insufficient` (< 20); `exact`, `differs` |
| Q6 | `q6.workloads[]` | per workload × workflow × reset: 7 elapsed and 7 RSS samples, median, max, ratio to baseline, budget, phase timings, unattributed time, yield, runner class | `within`, `over`, `no-baseline` |
| Q7 | `q7` (M4, D8) | field presence, proof-join failures, rubric average, every item scoring ≤ 2 with its disposition, triage time, accepted and dismissed counts (AQP:408-411). Below 50 findings, every finding is scored and the result is labelled `small-population`. | `measured`, `not-measured` |
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
| K2r | independence review of the K2 expected answers, done before any producer output exists (`M3-PLAN.md:172`) | 2 days |

The cell counts are `M3-PLAN.md:58`. The T1 obligation is all 57 supported cells per mode, typed refusal for 6 and non-advertisement for 3 (AQP:481).

**K2 estimate: 15 days serialized** (5 + 5 + 3 + 2), using the plan's planning durations (`M3-PLAN.md:197-200`). Q0 is pre-day-0 work (`M3-PLAN.md:245`). If K2 starts by day 0, it finishes by day 15, inside the day-21 condition of the conditional host-chain duration (`M3-PLAN.md:233`). This is a planning assumption, not a measurement. The lead updates the critical path accordingly (§14 OI-12).

---

## 14. Open items, with owners

| ID | Item | Owner | Blocks |
|---|---|---|---|
| OI-1 | **D13**: accept the exploratory envelope (ENV) | lead, owner sign-off (AQP:535) | S-M's report, M3-M (`M3-PLAN.md:158`) |
| OI-2 | **D13 successor**: the DR-G13/report/harness successor that carries this record's case model, ledger, confidence rule and oracles into qualification (AQP:427-431) | Language quality + Product + Release engineering (QG:264) | Q2–Q8 qualification at M6 |
| OI-3 | **Q2 achievability** (§5.8): grow T2 held-out families toward *k*_min, or revisit D4 | owner (D4, AQP:525); lead (D3 sizing, AQP:524) | any Q2 PASS |
| OI-4 | The estimand: repository-weighted with a census guard (QD-11, QD-15) against finding-weighted | DR-G13 successor owners | Q2 qualification |
| OI-5 | Per-stratum against family-wise confidence across strata (§5.6) | DR-G13 successor owners | Q2 qualification |
| OI-6 | Differential tools and mutant validation that need repository-code execution (QD-17, §6.2): available only with O7's profile or a container | owner (O7, `M3-PLAN.md:308-310`); lead (CF) | the Rust differential; Rust mutant compile checks |
| OI-7 | **D12**: select the reference runner (§9.6) | release engineering; lead with owner sign-off (AQP:534) | Q6-labelled samples |
| OI-8 | Q3 and Q5 confidence statements. AQP sets point targets and a population floor of 20 (AQP:141, AQP:313); this record adds no bound. | DR-G13 successor owners | Q3/Q5 qualification |
| OI-9 | **D7**: declared correspondence for moved and renamed subjects (§8.3) | lead + identity owner (AQP:529) | Q5 at M5 |
| OI-10 | **D8**: explanation fields (Q7) | lead + reporting owner (AQP:530) | Q7 at M4 |
| OI-11 | The operational-record carrier after M3: S-OP-1 and S-OP-6 (OPP:250) | OPP §9 owners | M4 `--timings` |
| OI-12 | Fold K2's estimate (§13) into the M3 critical path | lead | the M3 total |
| OI-13 | **D1**: QG items[12] still says "cold/warm p95" (QG:268). The harness follows AQ:268-282 and PQV:28. | lead (AQP:522) | record hygiene only |
| OI-14 | The expert roster and capacity (§4.6) | owner (`M3-PLAN.md:368`) | resolving gating labels |
| OI-15 | **D2**: where the catalog lives (§2) | lead + evaluator owner, owner sign-off (AQP:523) | the M5 product pack |
| OI-16 | Family assignment for each T2 entry (§5.3) | M3-T2 (lead), D3 sign-off | the freeze |

## Lead decisions in this record

QD-1 integer millionths and directional rounding · QD-2 outcome table · QD-3 proposition class · QD-4 JSON Lines ledger with a hash chain · QD-5 hard and soft key components · QD-6 three populations · QD-7 the 20-minute time box · QD-8 calibration numbers · QD-9 agreement triggers · QD-10 the model-family rule · QD-11 repository-weighted estimand · QD-12 independence families · QD-13 the cluster product bound · QD-14 *k*_min · QD-15 the census guard · QD-16 mutant states · QD-17 differential execution boundary · QD-18 determinism variants · QD-19 the RSS counter source · QD-20 CI retry · QD-21 runner additions · QD-22 tree digest.

## Not claimed

- No measurement, fetch, adjudication or run was performed for this record. The numerical values in §5 are arithmetic, computed for this record.
- No contract, schema, gate, threshold or register row is changed. RS3 is unchanged.
- ENV is a draft for D13, not an accepted carrier.
- The differential tools' execution behaviour is to be confirmed when each one is pinned (QD-17).
- The K2 estimate is a planning assumption.
