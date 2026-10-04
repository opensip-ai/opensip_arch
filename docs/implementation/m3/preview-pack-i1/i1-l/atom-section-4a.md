## 4a. `cycle-representative`, the graph atom (contract successor M3-I1-L)

This section is added by contract successor I1-L (`docs/implementation/m3/preview-pack-i1/i1-l/`). Its body is items 2.1 to 2.9 of law M3-I1 r2 (`docs/implementation/m3/preview-pack-i1/PROPOSAL-r2.md`, sha256 `1eb47d1e292660b15cb0016a280899a384364f2c3d99ab61d18f12b133eba2c7`, accepted by CODEX2 on 2026-10-04), verbatim. In that text, "item N" names an item of that law; "r2", "I1-RF-n" and "I1-NB-n" name its review history; the short names (AQC, ATOM, COMP, ENUM, EPLAN, EXI, FAULT, IE, NE, PAC, PDS, QP, RA, REG, RPS, SIS, WS, X12) are those of its Short names table, and ATOM is this contract; line citations are to the files, and product paths to product main 2967905, as that law checked them. The precisions P0 to P7 after the verbatim text are the successor's own: they fix choices the verbatim text leaves open, and change none of it. The reference model is `docs/implementation/m3/preview-pack-i1/i1-l/evidence/cycle_representative_model.py`; `evidence/check_cycle_representative.py` beside it runs the discriminating cases.

**2.1 Syntax.**
```json
{"op":"cycle-representative","relation":"imports","minResolution":"resolved-target","filters":[]}
```
- It has no `n`. The schema already forbids `n` outside `count-at-most` (PDS:339-363).
- It has no `endpoint` (the default is `source`, ATOM:26) and no `evidence`.

**2.2 Admission (op law).** The schema enum admits the token (item 4). The rule law then also requires all of the following:
- the atom is its rule's whole `emitWhen`, never an operand of `and`, `or` or `not`;
- `relation` is `imports` and `minResolution` is `resolved-target`;
- `filters` is `[]`;
- `endpoint` and `evidence` are absent;
- the rule's `subjectEnumeration.subjectKind` is `file`.

**Any violation** is the existing rule-law detail `POLICY.UNKNOWN_RULE` (`policy.rs:341-362`):
- in a bundled document, X12 row 4 (X12:111);
- in a caller's document, the resolver refusal of WS:666-668, which is reachable only at M5.

**The kind check.** For this op only, the subject-kind check is "the subject is a file". It replaces the relation source-kind check (`policy.rs:260-289`), because the op's subject is the importer's file, not the importer symbol (item 2.3).

**Rejected:** allowing the op inside boolean trees. Negating "is the representative" has no reviewed meaning, and nesting adds Kleene cases nobody needs.

**2.3 The graph.** It is built once per rule evaluation.
- **Vertices V.** The rule's selected file subjects (COMP:26), each `subject3` = (universe, `file`, path) (ATOM:20; IE:189).
- **Facts read.** Admitted `imports` facts at rung ≥ `resolved-target` (ATOM:72) whose `sourceUniverse` is a universe of V. A fact at `syntactic-specifier` is never an edge and never a fallback (PAC:129-132).
- **The source vertex.** The importer maps to the unique retained symbol-inventory row of `fact.sourceUniverse` whose `nativeSubjectId` byte-equals it (exact-id, ATOM:40). The source vertex is that row's `path` in that universe. A symbol row's path is the enumerator's trusted attribution (SIS:509-513, SIS:533-535; RPS:15). No `SubjectIdV1` spelling is parsed (ATOM:32; QP:79).
  - If that path is not a selected vertex, the fact is not read further. An edge entering V from outside can close a cycle only together with an edge leaving V, and the target rule below already makes that edge uncertain.
  - If there is no unique row, the importer could be in V. That case is an uncertain edge (see "Unplaceable endpoints").
- **The target** of a fact whose source is a vertex, or whose importer has no unique row. Each target comes from the same reconciled occupancy that atom matching and graph projection use (ATOM:52; QP:68, QP:81-84):
  - **External:** not an edge. This is the host's explicit partition (AQC:59-61); ATOM:52 calls it a "known nomatch".
  - **First-party `file`:** the vertex (`fact.targetUniverse`, `file`, `evaluationNativeId`) (ATOM:34).
  - **First-party `symbol`:** the vertex at that symbol's inventory-row path, mapped as for the importer.
  - **Unknown occupancy, or no unique exact-id mapping (QP:84):** an **uncertain edge**, cause `target-kind-unknown` (ATOM:423).
- **Unplaceable endpoints.** In these cases the edge is an **uncertain edge**, cause `population-unknown` (ATOM:430) with the endpoint's universe:
  - a first-party `package` target;
  - a first-party target that is not a selected vertex;
  - an importer with no unique inventory row.

  Uncertain edges are never dropped (AQC:59-61). Both causes are existing members of the closed registry (ATOM:421-432).
- **Edges.** Known edges E are the distinct pairs (u, w). Several facts for one pair are one edge (AQC:58-59), and all of them are that edge's facts.
- **Unresolved imports.** `unresolved-edge` facts whose payload `relation` is `imports` (NE:2189-2192) are uncertain facts of their referrer's vertex.
- **Cyclic components K.** The SCCs of (V, E) with at least two vertices, or with one vertex and a self-edge (AQC:55-56).
- **Representative order.** Ascending UTF-8 bytes of the path, then the bytes of the universe identifier (AQC:57). The representative `rep(C)` is the first member of C in this order.

**2.4 The proposition and its value.** P(s) is: "file s lies on a directed import cycle of project files, and no file before s in the representative order is mutually reachable with s through **this Run's** admitted edges". The second conjunct is relative to the admitted evidence, so for one Run it is decided. Only the first conjunct, about the whole project graph, can be unknown. For a selected s:

| Case | Value | Why it is sound |
|---|---|---|
| s = rep(C), C ∈ K | **true** | C's cycle is made of admitted facts, and more evidence only adds edges, which keeps every cycle. No earlier member of C is mutually reachable through this Run's edges, by the definition of rep. True names the representative of the **current** admitted component (r2, I1-NB-1). |
| s ∈ C ∈ K, s ≠ rep(C) | **false** | rep(C) precedes s and is mutually reachable through this Run's admitted edges. |
| s in no member of K, the graph completeness of 2.5 is complete, and there is no uncertain edge | **false** | The admitted graph is the whole project graph leaving V (see below). |
| otherwise | **indeterminate** | An unseen or unplaceable edge could put s on a cycle. |

**This is strong Kleene in the sense of WS:600-604 and COMP:34.** A known match decides, true or false, whatever unrelated Coverage is missing. The negative answer needs completeness (ATOM:76-87).

**What is monotone, and what is not (I1-NB-1).** The existence of a known cycle is monotone: more evidence keeps it, so a fail decided on it is stable (item 6). The representative is not. A later Run with more edges can merge C with a component that holds an earlier path, and the former representative becomes false there. That is why the finding is transient and a representative-path waiver fails closed (2.7).

**Why the third row's false needs no file-population condition (I1-RF-3).** Take s on a cycle in the true project graph. Every vertex on that cycle is a project file.
- If every vertex is in V, every edge of the cycle is an admitted fact. This is because 2.5(b) and (c) establish that every expected importer of V's universes was examined and fully resolved. The assurance is as strong as the admitted Coverage attests, which is the same trust every outgoing negative already rests on (ATOM:74, ATOM:76-87). So s would be in K.
- If some vertex x of the cycle is outside V, the cycle has an edge from a vertex of V to x. By 2.5(b) and (c) that edge is an admitted fact, and its target is a first-party file that is not a selected vertex, or has unknown occupancy. Either way it is an uncertain edge (2.3).

Either way, the third row's condition fails. A partial or unresolved **file** population is therefore not the atom's question. Composition already makes such a gating rule indeterminate, with its own enumeration deficiency (COMP:28, COMP:56, COMP:161-166). A lawful partial file inventory is semantic evidence, never a fault (FAULT:18).

**Under complete Coverage**, P(s) holds exactly for each cyclic component's representative. So the rule emits exactly one finding per cyclic component, and parallel edges add none (AQC:56-59).

**2.5 Graph completeness.** It is computed once per rule evaluation, and has the result shape `{complete, unknown, causes, coverageIds, scopeIds, nativeDeficiencies}` (ATOM:76-80). It is complete only when all three of these hold:
- **(a) Bindings.** The shared prelude and outgoing step 1, for relation `imports` and the universes of V, give no `missing-relation-coverage` and no `selector-unbound` (ATOM:113-141).
- **(b) The source census, positively covered at the universe extent (r2, I1-RF-1).** `imports` subjects are symbols, and "any capability question about them can only be answered at the coarser retained extent" (RPS:15). The op therefore applies, to each universe U of V, the expected-source law that incoming accounting already uses (ATOM:257, ATOM:259, ATOM:210-212):
  1. **Owed programs.** These are the EnumerationPlan bindings for `capabilityForRelation[imports]` at U. Contributors are per (U, provider closure) (ATOM:257).
  2. **The census.** The expected sources E_U are the union by U of the rows of those bindings' `imports` inventories. Those inventories are kind `symbol` (EPLAN:96-98). Expected IDs come only from inventory rows (ATOM:257).
     - If any such inventory is `partial` or `unavailable`, or none exists, the census is unknown: cause `population-unknown`, universe U ("Partial/unavailable inventory ⇒ `population-unknown`, not fake IDs", ATOM:257; ATOM:210-211).
     - The known rows of a partial inventory are still checked in step 3 (ENUM:120).
     - A complete **file** inventory never closes this census. The rule's own population is a different inventory kind (COMP:166).
  3. **Exact-id coverage.** The source presence S_U is the union of the `subjects` of every retained exact (`imports`, `resolved-target`) scope whose source universe is U, whatever its target universe (ATOM:259). Scope subjects are inventory rows (ENUM:93).
     - Every e in E_U must be in S_U. Each that is not emits `uncovered-expected-source-subject`, universe U (ATOM:211-212).
     - A broad partition may cover many sources (EXI:169).
     - If U has no such scope at all, the same cause is emitted, as outgoing step 2 does (ATOM:142-144). So a complete-empty census closes only through an explicit empty-subjects scope with complete Coverage (ATOM:242-245).
  4. **Pairing.** Every such scope has a paired Coverage (outgoing step 3, `scope-without-coverage`, ATOM:145-153).

  This is the same census and the same membership test as the native account of a supported-available cell (EXI:169). The op computes it itself, for three reasons:
  - **It does not depend on the cell's `required` flag.** An optional cell's census gap leaves only an incomplete account with the carrier `(null, null)` and no required-cell deficiency (EXI:190, EXI:198-211). So the op must not rely on one.
  - **No carrier is manufactured.** A census gap is never reported as `provider-unavailable` (EXI:198-204). The two causes above are existing atom causes (ATOM:423, ATOM:430).
  - **Real carriers are kept.** A real typed carrier on an inventory or Coverage record is retained alongside.
- **(c) Sufficiency.** Each paired Coverage's sufficiency view is satisfied (step 4, `coverage-unknown` with its `nativeCause`, ATOM:154-158) under this fixed requirement: `{relation: imports, minResolution: resolved-target, minConfidenceMillionths: 0, completeness: complete, quantifier: universal-negative, unresolvedEdgePolicy: forbid, externalConsumerPolicy: forbid}`.
  - NE:2008-2010 requires `universal-negative` with forbid/forbid for a negative. The steps are at NE:2262-2272.
  - RC-2 makes a Coverage `complete` only when the examined partition is exhaustive and no `imports` unresolved edge is admitted (NE:2113-2117). So a non-literal dynamic import, an unresolved specifier or a parse failure leaves (c) unsatisfied (AQC:61-63).

**File population is composition's job, not the atom's (r2, I1-RF-3).** r1's condition (d), "the rule's file population is complete", is removed. Composition owns that question: an incomplete or unresolved population makes a gating rule indeterminate, with its own enumeration deficiency, unless a live finding fails it (COMP:28, COMP:56, COMP:161-166). Item 2.4 shows why the atom's false stays sound without (d).

**A missing required rung** reaches the rule as a typed cause, never as a syntax fallback (PAC:129-132; REG:370; NT-3, PAC:204-208).

**Every indeterminate answer carries a blocking native cause.** This matters because COMP:56 makes an indeterminate root with no blocking cause a pass. By construction the table answers indeterminate only when (a), (b) or (c) fails or an uncertain edge exists. Each of those carries a cause: (a) to (c) as above, and each uncertain edge its cause from 2.3. So an empty cause set is reachable only through an implementation defect. That is a host-invariant fault, and the value must not be emitted. A lawful partial inventory of either kind always reaches a semantic result instead:
- a symbol inventory gives `population-unknown` here;
- a file inventory gives composition's enumeration deficiency.

**2.6 The witness.** Each selected subject gets one `native-atom` witness (COMP:32), without `countLimit`.
- **`matchingFactIds`:**
  - for rep(C), the facts of every edge with both ends in C;
  - for another member of C, the facts of C's edges leaving that member;
  - for every other subject, empty.
- **`uncertainFactIds`:** these are retained even when a known value dominates (ATOM:415). They are:
  - the facts of uncertain edges leaving the subject;
  - the `imports` unresolved-edge facts whose referrer maps to it;
  - if the subject's value is indeterminate, the facts of uncertain edges whose importer has no unique row. Such an edge could leave any vertex.
- **`coverageIds`, `scopeIds`, causes and `nativeDeficiencies`:** those of 2.5's result, including the census causes of 2.5(b), plus the causes of every uncertain edge in the graph. Each subject therefore carries every blocking cause, which item 2.5 requires. The causes become evaluation deficiencies through COMP §9.5's existing atom-mapped rule (COMP:176-182), with no new mapping.
- **Order and size.** Fact lists are canonical sets (COMP:91). A known fact appears in at most two witnesses. An uncertain fact with an unplaced importer appears once per indeterminate subject, which the S·F term of item 2.8's charge bounds.

**2.7 The finding, message code and parameters.**
- **Emission** uses the existing `declarative-subject-v1` profile (COMP:42-44). There is one `finding3` per true subject, which means one per cyclic component, sitting on rep(C).
- **`messageCode`** is the ruleId `module-import-cycle`, because the pack omits `Rule.messageCode` (COMP:42; PDS:526).
- **Parameters** use the existing record `{schemaVersion: 2, messageCode, parameters: {ruleId, subjectPath, qualifiedName, subjectKind, subjectLanguage, matchingFactCount, matchingImportCount}}` (COMP:44; IE:1282-1286):
  - `subjectPath` and `qualifiedName` are rep(C)'s path (COMP:46);
  - `subjectKind` is `file`;
  - `matchingFactCount` is the number of distinct facts of C's edges;
  - `matchingImportCount` is 0.
- **Fingerprint.** File subjects always correspond (COMP:46). The fingerprint is `finding-key2` with rep(C) as subject and empty related keys (COMP:48; IE:188).
- **Presentation** is frozen here and rendered at M4:
  - the member paths are the endpoints of the root witness's `matchingFactIds`, sorted by UTF-8 bytes;
  - the spans are those facts' anchors, and each `imports` fact carries at least one (RPS:280-284).

  Nothing is shown that no admitted fact or inventory row states (AQC:57-58).
- **Under incomplete Coverage**, the findings are the known cyclic components. Each is a real cycle, but two of them may later prove to be one component, and a member set may grow. The rule still fails (item 6). Its retained deficiencies disclose the gap (COMP:36).
- **Waivers.** An exact `(ruleId, subjectPath)` waiver names rep(C)'s path (COMP:54). If new evidence moves the representative, the waiver stops matching and the finding fails again. This fails closed.

**2.8 Budget.** COMP:38's formula is unchanged (lead decision).
- **The charge.** This rule has N(r) = 1 and A(r) = 1, so the preflight charge is at least E + S·(1 + F + I + K).
- **The op's work** is:
  - one projection over the F facts and E inventory rows;
  - one SCC pass over at most S vertices and F edges;
  - one completeness pass over the K Coverage records and the scopes outgoing atoms already read (ATOM:142-153). The 2.5(b) census reads inventory rows already counted in E, and each scope's subjects once. That is at most E + S + F + K plus those scope reads, which the charge bounds whenever S ≥ 1. When S = 0, nothing is evaluated (COMP:26).
- **The evaluator computes the graph and 2.5 once per rule evaluation**, never per subject.
- **Output bounds still apply** (COMP:38). A component whose edges carry more than 100,000 facts exceeds the witness array bound, and fails as `EVALUATION.OUTPUT_BOUND_EXCEEDED` without truncation. RA:194-195 makes no large-cycle promise.

**2.9 The algorithm is free.** What is accepted is the cyclic-component set, the representative, the value table, the witness sets and the causes. Any SCC algorithm with identical outputs is an implementation substitution (AQC:80-82). Nothing depends on encounter order.

**Successor precisions (I1-L).**
- **P0. Where it is evaluated.** This atom is evaluated once per rule, over the rule's whole selected population (item 2.3), never by §8's per-subject `evaluate_atom`. §§5 to 9 do not apply to it, except §7's cause registry and its retention of uncertain ids.
- **P1. Cause universes on uncertain edges.** `target-kind-unknown` carries the fact's `targetUniverse`. An unplaceable target carries `population-unknown` with the fact's `targetUniverse`; an importer with no unique row carries `population-unknown` with the fact's `sourceUniverse`. An uncertain edge carries every cause that applies to it, its importer's and its target's.
- **P2. Order and accumulation of 2.5.** The shared prelude runs once, and its P2 return (`missing-relation-coverage`) is the only return of the whole computation. The universes of V are then accounted in ascending UTF-8 order of their identifiers, each in full, with no return across universes. In a universe with no available owed binding, outgoing step 1's `selector-unbound` ends that universe's account. Within a universe, every exact scope is cited in `scopeIds`, every unpaired scope emits `scope-without-coverage`, and every paired Coverage is evaluated: outgoing step 3's return is not taken. `scopeIds` and `coverageIds` follow §4's selection order.
- **P3. Unique rows.** The exact-id lookup of item 2.3 reads every retained `symbol` inventory of the universe. Byte-identical `(nativeSubjectId, path)` observations count once; one `nativeSubjectId` at two paths has no unique row.
- **P4. Unplaced unresolved edges.** An `imports` unresolved-edge fact whose referrer maps to no selected vertex is in no witness. It bears on the value only through 2.5(c), whose Coverage RC-2 already counts it (NE:2113-2117).
- **P5. Census carriers.** The census's `population-unknown` and `uncovered-expected-source-subject` carry `nativeCause` null, as incoming's do. An incomplete inventory's own typed carrier stays on that retained inventory, which every atomic node cites through `inputRefs` = EI (composition §9.2).
- **P6. Member order.** The finding's member list is sorted by item 2.3's representative order: path bytes, then universe bytes.
- **P7. The sufficiency answer.** 2.5(c)'s view is the native owner's `sufficiency_v2` answer under the fixed requirement stated there. The atom neither recomputes it nor accepts an answer computed under another requirement. An unsatisfied answer's `DeficiencyV2` values are the result's `nativeDeficiencies`.
