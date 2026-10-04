# Preview policy pack (X12c) — proposal M3-I1 r1

2026-10-03. Claude Opus 5.5, implementation lead. Law for unit M3-I1 of the accepted M3 unit plan (M3P:166). It covers three things:
- the frozen rule IR of the DR-131 preview rule `module-import-cycle`;
- the policy-language contract successor that X12:191 makes conditional;
- the contract successor for `opensip.preview.typescript.pack:1` (X12c).

**Draft r1, not accepted. Not code.** No product crate is touched before X9-6 is integrated (M3P:5, M3P:272). The code units are in [UNITS.md](UNITS.md).

**Short names.** Lines were checked against the files named here, on 2026-10-03.
- **X12** `docs/implementation/m2/policy-admission-x12/PROPOSAL.md` (r3, accepted; X12:12). **M3P** `docs/implementation/m3/M3-PLAN.md` (r4, accepted). **AQP** `docs/implementation/m3/analysis-quality/PLAN.md`.
- **AQC** `docs/coop/completion/analysis-quality-completion.v2.md` (sha256 `08fb0806…`, the pin the application manifest carries). **AAM** `docs/coop/completion/architecture-application.v1.json`. **RA** `docs/coop/completion/reference-architecture.v2.md`. **QCM** `docs/coop/completion/quality-corpus-manifest.v1.json`. **LQM** `docs/coop/completion/language-quality-matrix.completed.v2.json`.
- **PAC** `docs/coop/artifacts/preview-analyze-contract.v2.json`. **REG** `docs/v2/architecture/08-decision-and-readiness-register.md`. **CH13** `docs/v2/architecture/13-evidence-workflows-and-product-contracts.md`. **BP** `docs/v2/architecture/implementation-boundaries-and-build-plan.md`.
- **WS / IE / NE** `docs/v2/contracts/product-v1/{workflows-and-surfaces,identity-and-evidence,native-evidence}.md`.
- **COMP** `docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md`. **ATOM** `…/foundation/atom-evaluation-contract.v1.md`. **IDS** `…/foundation/identity-schemas.v3.json`. **EPS** `…/foundation/evaluator-emission-plan.schema.v1.json`. **RPS** `…/foundation/relation-payload-schemas.v2.json`. **SIS** `…/foundation/subject-inventory.schema.v1.json`.
- **PDS** `docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json`. **COMMON** `…/workflows/schemas/common.schema.json`. **QP** `…/workflows/query-projection-contract.v3.md`.
- Product paths are under `opensip/` at main `2967905`. X12a was integrated at `b642c45` and X12b at `6dd7363`.

**Authority.**
- DR-131 is SATISFIED under D-369, with the "exact preview pack/rule" accepted (REG:320).
- The application manifest's `QUALITY.RULE` target pins AQC §2 (AAM:1089-1098). The drafter recomputed AQC's sha256 and it matches that pin.
- PAC froze the pack's identity, but not its "rule IR", "evaluation algorithm" or "default numeric constants" (PAC:98-108). It "Does not freeze public rule IR" (PAC:240).
- X12 r3 left the row and the bytes to X12c (X12:191) and forbade inventing a cycle atom outside a successor (X12:73).

Items 1 to 9 are lead decisions, made under the owner's standing direction to proceed on the lead's recommendation. Each one names the alternatives it rejects. Item 9 lists the open points.

## Problem

**The product has no preview pack.**
- The release registry has zero rows (`crates/evaluator/src/pack-registry.json:1-5`), and its documents table is empty (`crates/evaluator/src/policy.rs:716-721`).
- `opensip.preview.typescript.pack:1` is therefore `NotBundled` (`policy.rs:1086-1088`), and `check_plan_pack` refuses any Plan that names it (`policy.rs:1399-1402`).
- Both are pinned by tests: `crates/evaluator/src/policy_pack_tests.rs:151-175` and `:580-600`, and `crates/host/src/configuration_tests.rs:102-111`.
- Every real Plan needs this pack (M3P:184). C4 and J depend on I1 (M3P:163, M3P:170).

**AQC states the rule** (AQC:53-63):
- Find the directed strongly connected components, over host-admitted `imports` facts at `resolved-target`, that have at least two project files or a self-edge.
- Emit one transient finding per cyclic component.
- Sort member paths by UTF-8 bytes, and present paths and spans only from admitted facts. Multiple edges do not multiply findings.
- Ignore external vertices only after the host's explicit project-domain partition.
- A dynamic import without a static target is unknown Coverage, never a guessed edge.

The thresholds are in AQC:65-72: fail on one or more cyclic components; zero passes only with sufficient Coverage; incomplete Coverage is the existing typed indeterminate.

**Today's DSL cannot express this rule.** There are four reasons.
1. **The predicates are per subject.** The atoms are exactly `exists|none|count-at-most|all-covered`, plus `and|or|not` (WS:597-600). The schema closes that set (PDS:296-303), and the evaluator refuses any other op (`crates/evaluator/src/atoms.rs:3263-3268`). No combination of them computes a transitive closure or an SCC.
2. **Emission is unary.** Composition emits exactly one finding for each subject whose `emitWhen` is true (COMP:42), under the one profile `declarative-subject-v1` (COMP:11; EPS:70-71). Its fingerprint has empty related-subject keys (COMP:48).
3. **The importer is a symbol.** An `imports` fact's importer is a symbol (RPS:279). So an `imports` atom over `file` subjects fails today's kind check (`policy.rs:260-289`), and an `imports` atom over symbols would emit per symbol, not per component.
4. **There is no pack schema to extend.** No pack schema exists under `docs/coop/design-corrections/workflows/`. The only pack mention there is `policy init [--packs ID,...]` (`docs/coop/design-corrections/workflows/command-inventory.v3.json:604`). The pack carrier is X12's registry row (X12:38-43).

## Decisions

### 1. The policy-language successor is needed (lead decision)

X12:191's condition holds: the rule needs a construct that `PolicyDocumentV2` and the atom registry do not have. Items 2 to 4 give the successor's exact content.
- **Owner.** X12:191 says it is "owned by DR-131's execution remainder". The lead authors it under the owner's standing direction, as for X12-0 (`docs/implementation/m2/config-remedy-x12-0-unit.json:22`). No register row is edited.
- **Ordering.** It must be accepted before the row ships (X12:191).

**Rejected:**
- **Authoring the rule with the existing ops.** This is impossible, for the four reasons in "Problem".
- **A per-file `in-cycle` op.** It emits one finding per member file, against AQC:56-59.
- **A cycle fact or relation produced by the provider or the evaluator.**
  - The provider supplies facts and Coverage, never rule evaluation (AQC:74-76; PAC:209-213).
  - A fact producer must be a provider closure (ATOM:48).
  - A new relation would also need a relation-registry successor (RPS:15).
- **A built-in rule program selected by `contributionId` or `programDigest`.** The rule's meaning would live outside the declarative document. That contradicts "Declarative-only" (PAC:101) and "Packs remain data-only contributions" (CH13:302).
- **A new component emission profile with n-ary fingerprints.** COMP:11 allows reviewed profiles. But this one needs an EPS successor (the `emissionProfile` const, EPS:70-71), a COMP §4 rewrite, new finding parameters, and baseline and comparison joins (COMP:62-64). Item 2 meets AQC with the existing unary profile. A later successor may still add this profile.

### 2. The frozen rule IR: the `cycle-representative` atom

Items 2.1 to 2.9 are the normative text the successor adds to the atom contract as a new §4a (item 4).

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

**2.4 The proposition and its value.** P(s) is: "file s lies on a directed import cycle of project files, and no file before s in the representative order is mutually reachable with s through admitted edges". For a selected s:

| Case | Value | Why it is sound |
|---|---|---|
| s = rep(C), C ∈ K | **true** | C's cycle is made of admitted facts, and more evidence only adds edges, which keeps every cycle. No earlier member of C exists, by the definition of rep. |
| s ∈ C ∈ K, s ≠ rep(C) | **false** | rep(C) precedes s and is mutually reachable through admitted edges. No evidence can undo that. |
| s in no member of K, the graph completeness of 2.5 is complete, and there is no uncertain edge | **false** | The admitted graph is the whole project graph on V. Every edge leaving V is external. |
| otherwise | **indeterminate** | An unseen or unplaceable edge could put s on a cycle. |

**This is strong Kleene in the sense of WS:600-604 and COMP:34.** A known match decides, true or false, whatever unrelated Coverage is missing. The negative answer needs completeness (ATOM:76-87).

**Under complete Coverage**, P(s) holds exactly for each cyclic component's representative. So the rule emits exactly one finding per cyclic component, and parallel edges add none (AQC:56-59).

**2.5 Graph completeness.** It is computed once per rule evaluation, and has the result shape `{complete, unknown, causes, coverageIds, scopeIds, nativeDeficiencies}` (ATOM:76-80). It is complete only when all four of these hold:
- **(a) Bindings.** The shared prelude and outgoing step 1, for relation `imports` and the universes of V, give no `missing-relation-coverage` and no `selector-unbound` (ATOM:113-141).
- **(b) Scopes, at the universe extent rather than per subject.** `imports` subjects are symbols, and "any capability question about them can only be answered at the coarser retained extent" (RPS:15). So:
  - every retained scope at exact (`imports`, `resolved-target`) whose source universe is a universe of V has a paired Coverage (outgoing step 3, `scope-without-coverage`, ATOM:145-153);
  - each such universe has at least one such scope (otherwise `uncovered-expected-source-subject`, as in step 2, ATOM:142-144).
- **(c) Sufficiency.** Each paired Coverage's sufficiency view is satisfied (step 4, `coverage-unknown` with its `nativeCause`, ATOM:154-158) under this fixed requirement: `{relation: imports, minResolution: resolved-target, minConfidenceMillionths: 0, completeness: complete, quantifier: universal-negative, unresolvedEdgePolicy: forbid, externalConsumerPolicy: forbid}`.
  - NE:2008-2010 requires `universal-negative` with forbid/forbid for a negative. The steps are at NE:2262-2272.
  - RC-2 makes a Coverage `complete` only when the examined partition is exhaustive and no `imports` unresolved edge is admitted (NE:2113-2117). So a non-literal dynamic import, an unresolved specifier or a parse failure leaves (c) unsatisfied (AQC:61-63).
- **(d) Population.** The rule's population is complete. Composition already treats an incomplete or unresolved population as indeterminate for a gating rule, with its own deficiency (COMP:28, COMP:56). The op does not restate that.

**A missing required rung** reaches the rule as a typed cause, never as a syntax fallback (PAC:129-132; REG:370; NT-3, PAC:204-208).

**Every indeterminate answer carries a blocking native cause.** This matters because COMP:56 makes an indeterminate root with no blocking cause a pass. The causes are those of (a) to (c) plus each uncertain edge's cause from 2.3. Reaching indeterminate with an empty cause set is a host-invariant defect, and the value must not be emitted.

**2.6 The witness.** Each selected subject gets one `native-atom` witness (COMP:32), without `countLimit`.
- **`matchingFactIds`:**
  - for rep(C), the facts of every edge with both ends in C;
  - for another member of C, the facts of C's edges leaving that member;
  - for every other subject, empty.
- **`uncertainFactIds`:** these are retained even when a known value dominates (ATOM:415). They are:
  - the facts of uncertain edges leaving the subject;
  - the `imports` unresolved-edge facts whose referrer maps to it;
  - if the subject's value is indeterminate, the facts of uncertain edges whose importer has no unique row. Such an edge could leave any vertex.
- **`coverageIds`, `scopeIds`, causes and `nativeDeficiencies`:** those of 2.5's result, plus the causes of every uncertain edge in the graph. Each subject therefore carries every blocking cause, which item 2.5 requires.
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
- **The op's work** is: one projection over the F facts and E inventory rows; one SCC pass over at most S vertices and F edges; and one completeness pass over the K Coverage records and the scopes outgoing atoms already read (ATOM:142-153). That is at most E + S + F + K plus those scope reads, which the charge bounds whenever S ≥ 1. When S = 0, nothing is evaluated (COMP:26).
- **The evaluator computes the graph and 2.5 once per rule evaluation**, never per subject.
- **Output bounds still apply** (COMP:38). A component whose edges carry more than 100,000 facts exceeds the witness array bound, and fails as `EVALUATION.OUTPUT_BOUND_EXCEEDED` without truncation. RA:194-195 makes no large-cycle promise.

**2.9 The algorithm is free.** What is accepted is the cyclic-component set, the representative, the value table, the witness sets and the causes. Any SCC algorithm with identical outputs is an implementation substitution (AQC:80-82). Nothing depends on encounter order.

### 3. Versioning: widen in place (lead decision)

`PolicyDocumentV2` stays `schemaMajor` 2 (PDS:692), and `RuleProgramV2` stays `schemaVersion` 2 (PDS:723). The proof3 and program-predicate `operation` enums gain the token without a domain relabel. The reasons:
- **No existing byte changes meaning.** Every existing document, program, proof and digest is unchanged.
- **Records are unchanged.** COMP:7 says an unchanged record shape "does not require relabelling its domain". Here the record shape is unchanged and only one enum's value space widens.
- **Old readers fail closed.** An older reader refuses the new token on schema, never misreads it.
- **The bundled pack is the only producer** until M5's policy commands (X12:229).

**The tension.** IE:213-214 says "Schema/domain changes require a new identifier major and reviewed migration, not a permissive parser". That sentence closes the finding-fingerprint paragraph (IE:199-214). The lead reads it as governing identity recipes and domains whose existing records would change meaning. Under that reading, this widening needs no major, because it changes no existing record and no `finding-key2`. If the reviewer reads IE:213-214 as covering any proof3 or program-predicate schema change, LD-3 flips to new identifier majors for those two domains.

**Rejected:**
- `PolicyDocumentV3` or an evaluator output profile 4. These would need new majors for the policy, the program, proof3 and the policy-test suite (WS:653-655), all for a change that reinterprets nothing.

**Risk.** This is the decision most likely to need the reviewer's correction (item 9, LD-3).

### 4. The successor's exact content

The successor is one contract-successor record of passage overrides and an appended section, like X12-0's `passageOverrides` (`docs/implementation/m2/config-remedy-x12-0/successor.json:16`). Frozen contract text is never edited.

| Document | Selector | Change |
|---|---|---|
| WS | 598 | after "`all-covered`" add: ", the graph atom `cycle-representative` (only as a rule's whole `emitWhen`, only over `imports` at `resolved-target` with no filters, only for subject kind `file`)" |
| WS | 603-604 | after "`all-covered` indeterminate" add: "; `cycle-representative` is true for the least-path file of a cyclic component of the admitted resolved project import graph, false for its other files, and otherwise false only under complete graph Coverage, else indeterminate (atom contract §4a)" |
| PDS | 296-303 (`Atom.op`), 937-944 (`AtomSuccessorV1.op`) | append `"cycle-representative"` |
| IDS | 1221-1231 (`proof-bundle` `predicateProofs[].operation`), 2781-2791 (`program-predicate.operation`) | append `"cycle-representative"` after `"all-covered"` |
| COMP | 34 | append: "`cycle-representative` with a known cyclic component is true at its representative and false at the component's other members (atom contract §4a)." |
| ATOM | new §4a after §4's last line, before §5 (ATOM:370) | items 2.1 to 2.9 verbatim |

**Unchanged:**
- EPS: the emission profile stays `declarative-subject-v1`.
- The atom and projection registries: the op law lives in §4a and the schema enum, so a second op table would be a second authority.
- RPS, IE and NE.
- The policy-test suite schema. It takes `PolicyDocumentV2` by `$ref` (`schemas/sources/policy-test-v2.schema.json:25`). So M5's `policy test` unit must implement the op in the fixture verifier (WS:638-649), or refuse it, before that command ships (X12:229).

The product copies (`schemas/sources/policy-v2.schema.json:296-303`; `identity-v3.schema.json:1221-1231`, `:2781-2791`), their registry pins and the generated enums change in unit I1-a.

### 5. The contract successor for `opensip.preview.typescript.pack:1`

**5.1 Identity.**
- The name is `opensip.preview.typescript.pack`, the version is `1`, and the packId is `opensip.preview.typescript.pack:1`.
- Matching is byte-exact (X12:47-59; PAC:99-100).
- Name and version enter PlanId through `analysisSpecDigest`, and the content through `policyDigest` (X12:59; PAC:114-118).

**5.2 The bundled document.** These are its canonical bytes exactly, with no trailing newline:

```
{"gateSeverityAtLeast":"error","rules":[{"emitWhen":{"filters":[],"minResolution":"resolved-target","op":"cycle-representative","relation":"imports"},"enabled":true,"evidenceUse":[],"gate":true,"ruleId":"module-import-cycle","ruleProgramRef":{"contributionId":"opensip.preview.typescript","programDigest":"8e8936af513ae93eeb8227fb991330b523761930d85d077b044f4312706a57de","ruleStableId":"module-import-cycle","semanticsMajor":1},"severity":"error","subjectEnumeration":{"subjectKind":"file","universe":"typescript"}}],"schemaFamily":"opensip.product.policy","schemaMajor":2}
```

The choices:
- **One rule** (AQC:54).
- **`universe: "typescript"`** is a token of the closed universe map (COMP:26).
- **No `include` or `exclude`**, which means all paths (COMP:26).
- **`evidenceUse: []`** and **`enabled: true`**.
- **`ruleStableId: "module-import-cycle"`** with **`semanticsMajor: 1`**.
- **`contributionId: "opensip.preview.typescript"`.** `ContributionId` forbids `:` (COMMON:84-88), so the packId cannot serve. The detector is identified by this contribution (WS:277-281).

**5.3 Digest rules.**
- **`programDigest`** is the raw SHA-256 of C(`emitWhen`). No normative recipe exists (PDS:461 types it only as `Sha256Hex`). This is the recipe the reference fixtures use (`docs/coop/design-corrections/foundation/check-identity.py:72`; `evaluator_graph_fixture.v3.py:170`). It is frozen for bundled packs only.
- **`policySha256`** is the raw SHA-256 of C(document), and equals the SHA-256 of the file bytes. That is stricter than X12 item 6.5 (X12:95; `policy.rs:1100-1104`), which canonicalizes the bytes first.
- **The compiled `RuleProgramV2` digest** (`AdmittedPack::program_digest`, `policy.rs:808-811`) is pinned.

**Provisional values.** They are computed by the drafter with a sorted-key compact encoder. The content is ASCII, so IE:122-125's rules coincide.

| Value | Digest |
|---|---|
| `programDigest` | `8e8936af513ae93eeb8227fb991330b523761930d85d077b044f4312706a57de` |
| `policySha256` | `96675a5e20fcfd8ba6501f20b9017aa205e300b9f1984d7e74ad534996acdcd1` (574 bytes) |
| `ruleProgramDigest` | `e796f81764d0ee452c591c852e98f59647518a1894d4bd0fd5c70b674ecc3ecb` (457 bytes) |

I1-P recomputes them with the design encoder (IE:134), and I1-c with `canonical_bytes`. A mismatch blocks acceptance. It is resolved in the encoder, never by editing the document.

**5.4 The registry row.** It has the exact key set X12a enforces (`policy.rs:953-965`):

```json
{"contributions":["opensip.preview.typescript"],"name":"opensip.preview.typescript.pack","packId":"opensip.preview.typescript.pack:1","policyDocument":"preview-typescript-pack.v1.policy.json","policySha256":"96675a5e20fcfd8ba6501f20b9017aa205e300b9f1984d7e74ad534996acdcd1","version":1}
```

The `standing` text names this law and states "one row".

**5.5 Placement.**
- The document is `crates/evaluator/src/preview-typescript-pack.v1.policy.json`.
- It is included with `include_bytes!` as the sole entry of `RELEASE_PACKS.documents` (`policy.rs:716-721`), under the name the row's `policyDocument` gives (`policy.rs:1005-1011`).
- There is one row and one document (`policy.rs:1009-1021`).
- Nothing is read at run time (X12:43).

**5.6 Self-checks** (unit I1-c):
- **S1:** the registry is self-consistent (`policy.rs:930-1023`) with exactly one row.
- **S2:** the file's bytes equal `canonical_bytes(parse_json(file))`; its SHA-256 equals `policySha256`; and there is no trailing newline.
- **S3:** X12 item 6's steps 6.1 to 6.7 pass for the release row (X12:87-101).
- **S4:** each rule's `programDigest` equals SHA-256(C(`emitWhen`)).
- **S5:** the packId, `policySha256`, `programDigest` and compiled program digest equal the values the accepted I1-P record pins.
- **S6:** the source pin:
  - the release build names one document and no test row;
  - the `include_bytes!(` count goes from 7 to 8 (`policy_pack_tests.rs:638`);
  - `&RELEASE_PACKS` still appears exactly twice.
- **S7:** NT-1, which has three parts:
  - `opensip.preview.typescript.pack:1` admits;
  - `:2`, the bare name, `:01`, case variants, a trailing newline and other names stay row 1;
  - `Supplied` with the release document's exact bytes stays row 2 (X12:92, X12:207).
- **S8:** `check_plan_pack` behaves as follows:
  - a Plan naming the pack with the matching `policyDigest` admits;
  - any other digest is refused (`policy.rs:1403-1406`).
- **S9:** host `admit_policy_selection(Named(pack:1))` returns the `AdmittedPack`, and every other host row is unchanged (X12b).
- **S10:** over synthetic admitted inputs (unit I1-b2), the corpus golden sets hold:
  - `cycle`: one finding on `cycle/a.ts`, with members `cycle/a.ts` and `cycle/b.ts`;
  - `self`: one finding on `self/self.ts`;
  - `acyclic`, `empty` and `shadow`: pass;
  - `unresolved`, `malformed` and `dynamic`: indeterminate.

  The sources are QCM:7-124 and LQM:232.

### 6. Thresholds, severity and outcome

**Gating.** `gate: true`, `severity: error` and `gateSeverityAtLeast: error` make the rule gate (COMP:56).

**The threshold is one component.** Any live unwaived finding fails the rule (COMP:56), which is AQC:66's "at least one cyclic component". No numeric constant is needed.

**Pass** requires every subject false: complete graph Coverage and no known cycle (AQC:66-67). **Indeterminate** is everything else, typed by item 2.5's causes (AQC:67-69).

**`policyOutcome`** comes from the pure core, inside CoreCompletion (PAC:119-128). The host maps only existing D9 classes. It derives nothing from a component count (PAC:224-233; REG:373).

**No new D9 code, detail or remedy** (AQC:71-72; X12:220). The indeterminate causes reach D9 through the NE §11 carriers J2 owns (M3P:170), for example `required-relation-missing` at NE:3374.

**Rejected:**
- **`warning`/`warning`.** It behaves identically today, but reads worse.
- **"Indeterminate whenever Coverage is incomplete, even with a known cycle".** A known cycle is a known match. Strong Kleene and COMP:56 make it fail, and AQC's "existing typed indeterminate result" (AQC:68) is that same existing law (item 9, LD-4).

### 7. Amendments to X12 r3, for M3 only

These take effect when unit I1-c lands:
- **Item 4's "zero rows"** (X12:67) becomes "exactly the one row of M3-I1 item 5".
- **Item 10's NT-1 bullet** "in the release registry, `opensip.preview.typescript.pack:1` itself (not bundled in M2)" (X12:160) becomes: that ID admits, and its variants stay row 1.
- **Item 10's "in M2 there are zero release rows"** (X12:169) becomes "exactly one".

Everything else in X12 r3 stands: rows 1 to 4, the order, the `Supplied` refusal of bundled bytes, the `cfg(test)` registry, `check_plan_pack`, and X12d.

### 8. How I1 feeds C4, H, J and I2

**C4 (the Plan builder, with X12d; M3P:163):**
- It takes the policy only from an `AdmittedPack`, writing `analysis-spec.policyPackIds = ["opensip.preview.typescript.pack:1"]` and `plan.policyDigest` (X12:134).
- It commits the bundled policy bytes, the compiled program, an `EnumerationPlanV1` covering `typescript` file subjects, and an `EvaluatorEmissionPlanV1` row binding the rule to its detector closure (IE:1508-1512; COMP:9). The detector closure is LD-10.
- It selects capability `typescript.imports` (AQC:90) whenever the pack is selected. A Plan without it is lawful but can only be indeterminate.
- X12d then applies `check_plan_pack` in replay. Real Plans pass, and the synthetic corpus moves to the test pack (X12:192).

**H (fact admission; M3P:169):**
- I1 adds no admission law.
- H must admit what item 2.3 reads: `imports` facts at `resolved-target`, `unresolved-edge` facts, `TargetAttributionV2` occupancy, symbol-inventory rows with paths, and scopes and Coverage.
- I1-b2's fixtures fix those shapes for H's tests.

**J (M3P:170):**
- **Order.** J2 calls `admit_policy_selection` first (X12:125-132).
- **Default selection.** Recommendation for the B configuration law: the zero-config default is `Named("opensip.preview.typescript.pack:1")` through `admit_pack`, never a bypass. CH13:309 says "The preview accepts only its bundled cycle pack".
- **Evaluation.** J2 evaluates through `derive_evaluation` with I1-b2. `policyOutcome` reaches D9 only through existing classes.
- **Gates.** DR-G25's missing-rung path is item 2.5 (REG:370). DR-G28 is item 6 (REG:373). DR-G24's corpus names are unchanged (X12:6).

**I2 (the draft catalog; M3P:171):**
- **Same IR.** The catalog's `module-import-cycle` (AQP:196) uses this op and this semantics, with its own document, whose default is "gating only by declared policy" (AQP:196). It should reuse `ruleStableId` `module-import-cycle` and `semanticsMajor` 1, because the semantics are the same.
- **Never a release row.** I2 runs only in the harness (AQP:500; M3P:171). The product pack stays at M5 (AQP:542). An I2 document never enters the release registry.
- **Other atoms.** Any other new atom a catalog rule needs is its own successor. Item 2.2's restrictions bind I2 until one is accepted.
- **The oracle.** I1-L's reference model is available as I2's harness oracle for this rule.

### 9. Open questions, decided by the lead

| ID | Question | Decision | Rejected |
|---|---|---|---|
| LD-1 | Is a successor needed? | Yes (item 1). | The existing ops, provider or derived facts, built-in programs. |
| LD-2 | What shape should the IR take? | A root-only atom with representative emission (item 2). | A per-file op; a component emission profile (heavier, later). |
| LD-3 | Major bump? | Widen in place (item 3). | `PolicyDocumentV3` or profile 4. |
| LD-4 | Known cycle with incomplete Coverage? | Fail, with deficiencies retained (items 2.4, 6). | Indeterminate. |
| LD-5 | At what grain is completeness decided? | The universe extent (item 2.5(b), RPS:15). | Per subject: no path law exists for symbol relations. |
| LD-6 | Sufficiency posture? | forbid/forbid. Step 7 (NE:2271) is target-relative, and this requirement names no target scope, so it tests nothing here. **Reviewer to confirm.** | `disclose` or `assume-closed`, which are advisory postures (NE:2010-2012). |
| LD-7 | Unknown or unplaceable edges? | Uncertain, with `target-kind-unknown` or `population-unknown` (item 2.3). | Dropping them; minting a cause code. |
| LD-8 | Representative? | The least path by UTF-8 bytes, then the universe (item 2.3). | Encounter order; `fact2`-id order. |
| LD-9 | Pack constants? | Item 5.2. `messageCode` is absent, so it equals the ruleId. | An explicit `messageCode`, which is redundant. |
| LD-10 | Detector closure for a bundled pack? | **Recommendation for C4 and C2:** a host-derived `closure2` of kind `detector` (IDS:274 lists `detector` among the closure kinds), with the bundled document as its exact data tree, the pack version as `semanticVersion`, and the signed core's manifest. This is decided in the C law. | The evaluator closure, which COMP:9 forbids; a separately shipped detector, which contradicts X12 item 2; an EPS change allowing no detector. |
| LD-11 | Order of I1-c and I1-b2? | I1-c may land before I1-b2. Until then, evaluation refuses the op structurally (`ATOM_OP`, `atoms.rs:3263-3268`), never as false. J2 depends on I1-b2. | Holding I1-c for I1-b2. That delays C4 with no gain, since no producer exists before J2. |
| LD-12 | Type-only and re-export imports? | Counted. The payload has no field to tell them apart (RPS:267-301), and inventing one is out of scope. This is a disclosed limitation. | An `imports` payload successor at I1. |

## Units after the law

These are detailed in [UNITS.md](UNITS.md).

**Design only** (arch; allowed before X9-6, with no product edit):
- I1-L, the policy-language successor record (items 2 to 4), with a reference model.
- I1-P, the pack contract successor (item 5).

**Product**, after X9-6, each scheduled by the lead:
- I1-a: schemas, pins and generated enums.
- I1-b1: evaluator admission law.
- I1-b2: evaluator semantics, plus the fixtures for S10.
- I1-c: the row, the document and the self-checks S1 to S9.

**Order:** I1-L → I1-P; I1-L → I1-a → I1-b1 → I1-c; I1-a → I1-b2. C4 needs I1-c, and J2 needs I1-b2.

## Forbidden substitutes

**Carried from X12:196-222, unchanged.**
- **Bundling:**
  - a run-time read of a pack, policy or registry;
  - a row in the release declaration registry;
  - a placeholder or contentless row;
  - a reachable `cfg(test)` row.
- **Identity:**
  - normalization;
  - a name-only match;
  - admission by digest or bytes;
  - admitting `Supplied` bytes, including the bundled bytes.
- **Declarativeness:**
  - a caller's imperative member that surfaces as anything but row 3;
  - a contribution outside the row's set;
  - a script, hook, WASM or component closure as a contribution.
- **Order:**
  - admission after a provider, snapshot, facts or evaluation;
  - a Plan whose `policyPackIds` or `policyDigest` did not come from an `AdmittedPack`;
  - more than one pack, or a merged policy.
- **Types and codes:**
  - a host wrapper around `AdmittedPack`;
  - a boolean or string standing in for admission;
  - silent admission, or a waived refusal;
  - a new public code.

**Added by I1:**
- **Shipping too early:** shipping the row before I1-L and I1-P are accepted, or with bytes other than item 5.2's.
- **Moving the rule out of the core:**
  - a provider-supplied cycle fact or finding (AQC:74-76; PAC:209-213);
  - evaluating the rule anywhere but the pure core (PAC:119-128).
- **Escape hatches:** a built-in program selected by `contributionId` or `programDigest`.
- **Verdict and D9:** a host-derived verdict, D9 class, exit or termination from a component count (PAC:224-233).
- **Edges and indeterminacy:**
  - dropping an edge whose occupancy is unknown or whose endpoint cannot be placed (AQC:59-61);
  - a guessed edge for a dynamic or unresolved import (AQC:61-63);
  - an indeterminate value with no blocking cause;
  - turning indeterminate into pass (AQC:68-69).
- **Emission:**
  - one finding per member file or per edge (AQC:56-59);
  - a representative chosen by encounter order.
- **Bytes:** a document file whose bytes differ from its canonical bytes.
- **The release registry and I2:** an I2 catalog document in the release registry; any second release row before its own successor.

## Not claimed

- DR-G24, G25 or G28 qualification, which is M6 (BP:999-1000). Measured G13 rows. Any live-provider evidence.
- Durable or stable preview identities. DR-131's unstable-identity list stands (PAC:133-148), and REG:438 governs any later authoritative upgrade.
- M4 human rendering and its presentation catalogue entry. `policy show`, `init`, `test` and `waive` at M5 (X12:229), including the fixture verifier for the op. User or third-party packs.
- A component emission profile. Precision or recall claims for real repositories.
