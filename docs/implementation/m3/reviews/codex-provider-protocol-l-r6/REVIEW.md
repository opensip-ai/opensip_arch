# Codex review: M3-L r6 delta

**Verdict: ACCEPT.** No required findings. One nonblocking citation observation. This accepts the exact law-text delta in review; it does not complete S-M, satisfy L-G1, put L in effect, accept a product implementation, or qualify a product.

## Subject and custody

Reviewed the diff from the accepted-in-review r5, with r5's full “Review and effect”, acceptance gate and item 9 as context. The earlier GROK2 review was read for predecessor standing, not used as a substitute for this independent review. No unanswered Grok request was used.

- Stage: `/tmp/opensip-implementation/provider-protocol-l-r6-stage`.
- Subject manifest: 3,328 bytes, SHA-256 `837c25f18a4621e91bb03f81c2dd66efa3dfaee8cd34f8c3a163c6831f007b47`.
- r6 law and `PROPOSAL-r6.md`: byte-identical, 187,464 bytes each, SHA-256 `47198cd5f79518dfe96912db9959292d3e851ac825011deeb9da79c120692b8f`.
- Diff: 24,063 bytes, SHA-256 `175e67e7f5fbcaeb81ade54efaaea867e1e7e9aa7ead5cab985bc611f098d3ab`. Independently generated normal diff is byte-identical.
- All six manifest members and all ten architecture context pins independently rehashed: no missing or mismatching member. The context pins also match their Git HEAD blobs.
- Architecture HEAD: `4229df9e73b604fd1c5c02d12f811ed0e0f4f272`. Product HEAD: `95279fa8ae086f98bd221cd827f6c0efc156c0c5`, clean.
- Product lock remains 630,770 bytes, SHA-256 `6f041cb13f35f04092268c6906008bb060658fbfadb470b3fd03f2ea8b53c409`, with 147 inventory successors through v187 and 161 contract successors.

## 1. Gate cycle

The cycle is real. r5 requires the S-M delta round to fill SM-11–SM-14 before L takes effect. The deferred complete values require post-effect owning inputs:

- M3-PLAN r10:79 records L-G10/L-G11 met; :80 makes day 0 L in effect. :306 and :497 keep C's effect dependent on L.
- MC8:1185 assigns Plan/stage specifications and orchestration to C4a. The plan's :481 and :525 place its work after day 0, finishing at day 19. Its Rust stage list and requested Coverage keys are needed for complete SM-13/SM-14.
- The plan's :311 assigns inventory, facts and Coverage to G3, whose dependency row and :540 place completion at day 20. Actual emission, census and batching inputs cannot be selected by S-M as substitutes for G3's binding.
- :538–540 corroborate the worker's G1a/G2/G2-v/G3 dependencies. G2 authoring may start after S-P; that does not provide the complete G1a worker/context/transport path before L.
- RL README:140 requires `commitments.analysisDomain` over both rebuilt subjects and `requestedCoverageDomain`. Thus the complete domain commitment cannot be supplied without the owning requested keys.
- RPP:600–606 corroborates the work-unit tuple recipe. MD5:546/:551 and RPP:118 already select the 2 GiB scratch bound and settlement accounting; the missing scratch input is the actual worker observation, not a missing D policy.

r6 does not defer the independent host/subject work merely because the production admission path remains open. Outside-product S-M keeps its existing experimental authority. Production native admission is not added as its gate.

## 2. Pre-effect S-M part

The two-part rule is coherent and introduces no owned stage, key, emission factor, batching, census kind or scratch quantity.

SM-11 requires fresh exact subject counts under RUST3-LIM's recipe, including workloads absent from the historical count evidence. Existing SM-4/SM-10 observations remain reportable with their actual unit coverage. A quotient is permitted only when that coverage exactly matches the first-party crates holding the counted subjects; dependency-inclusive or missing-root observations cannot silently become per-subject workload figures.

SM-12 preserves both independent host subject-array/subject-scope derivations now. Only the domain commitment needing bound keys and the actual worker derivation wait.

SM-13 requires compiler query/site observations labelled as sites, not fact candidates. Its exact fixed encoding overheads come from the registered schemas and RPP:137–150, with named reference-encoder standing. Candidate payload lengths and any conditional CBOR/container overhead must remain explicit in the closed formulas; fixed overhead is not a substitute for total encoded bytes. G3 emission/census/batching and C4a stage grouping remain unset owning parameters. See the citation observation below.

SM-14 preserves the tuple formula with exact workload subject counts and unset stage/key inputs. S_eff's snapshot-row term is available from SM-5; the final ceiling and measured stage budget remain unavailable until their other terms are measured. No pre-effect stage budget or final SM-13 value is authorized.

## 3. Completion round and dependent reliance

The fifth trigger is lawful as the explicit prospective amendment reviewed here. It is owed after effect and is excluded from the revised definition of “L in effect”; the first four triggers and all existing gate items remain. Accepting r6 alone satisfies none of those gates.

The completion change set is closed to item 9's SM-11–SM-14 measured values and the listed consequent records: S_eff, the stage budget, scope-rebuild materiality and census over-bound onset. The trigger's parenthetical highlights S_eff and the budget; its operative reference to item 9 covers the complete listed set. It grants no protocol-constant, unrelated item, F/T or outcome A–C change. A measured safety-limit problem still requires the owning successor; it cannot be repaired through this data-only trigger.

The completion run retains the same workloads, pinned public bytes, no repository execution, warmup/sample counts and preliminary host standing. Settlement scratch and a labelled sampled in-run peak remain distinct; the latter cannot be represented as D's exact settlement walk.

The interim F-4 statement is correct: response safety failures remain provider-protocol faults under RPP:152, never BudgetExhausted. Removing the completion round from L's effect gate does not invent the missing measured budget or promise safety-bound-free operation before that budget is established.

## 4. Delta scope and L-C1

Independently compared every diff hunk. All changes fall within the requested item 9 timing/decomposition, round/effect text, header/history/short-name/standing records, X17, R16 and reversal flag.

Items 1–8 and 10–22 are byte-identical to r5. SM-1–SM-10 and even the inherited SM-11–SM-14 table rows are unchanged. The F/T derivations and outcomes A–C are byte-identical. No protocol constant changes.

Item 13, the 32,573-byte L-C1 script (`50d8a35a11206e7b942b9ce68b41fcac66dc8569290f006d364494bb89b1bd12`) and its 50,554-byte report (`9fdff61cfd34ba7cfbc090590b79b3c62adf2bc1c762259a5f066029b2128fe2`) are unchanged. All twelve staged L-C1 source mirrors match the repository sources. The pinned log records a pass and exit 0. The expressly permitted staged `--check` was rerun independently and exited 0 with “L-C1 OK: item 13 equals the inventory derived from the pinned schemas”.

## 5. X17 and reviewer substitution

X17 routes the timing follow-ups to the next M3-PLAN revision, M3-C's X-RL-C2 leg, M3-G's X-RL-G2 default budget and RUST3-LIM's X-RL-L3. Day 20 is the cited DAG's G3 finish, not a newly promised date. C remains responsible for sequencing its stage/key leg and later measured-budget leg; G remains responsible for its emission and budget duties. This delta does not close full C4a/G3 or itself authorize their implementation, launch or qualification. RUST3-LIM bytes stay unchanged.

The reviewer substitution is lawful: the owner's current instruction assigns this exact review to Codex, the request records predecessor-reviewer unavailability, and r6 retains the diff-only review requirement. Its explicit unavailability exception preserves independent review rather than treating the lead's authorship as acceptance.

## Nonblocking observation

**M3L-R6-NBO-01 — capability-table citation.** At r6:589, “each relation@rung with a rust-cargo cell” cites NE:591–598, although `unresolved-edge@observed` is at NE:601. The full table runs through NE:601 and also includes candidate-only clone modes at :599–600. Use NE:590–601 as the complete reference and preserve the fact-relation/candidate distinction. This is nonblocking because the operative instruction covers each relation in the table rather than expressly limiting the population to those cited lines. It must not be implemented as a range-limited census that drops unresolved edges.

## Boundaries and actual standing

Only read-only hashing, JSON/source inspection, read-only Git and the explicitly permitted staged L-C1 check were performed. No compiler, Cargo, tests, measurement lane, network, other pane or delegation was used. No private 413 fixture, installation directory, signing key or held-tree content was read. No repository, stage or control file was edited. Only the two requested review outputs were written.

**SMComplete=false; LG1Met=false; effectiveL=false.** No placeholder is filled by this law-text review. Exact lead assent, fresh design/implementation verification and any later publication remain the lead's separate work.
