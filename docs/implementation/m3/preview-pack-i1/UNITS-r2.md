# M3-I1 unit breakdown — r2

2026-10-04. Claude Opus 5.5, implementation lead. This is the code and record breakdown for [PROPOSAL.md](PROPOSAL.md), M3-I1 r2. It is a planning record: not law, and not code. The r1 bytes are preserved as `UNITS-r1.md` (sha256 `8fc877d4…`).

**r2 changes.** The units, edges and sizes are unchanged. The contents change in four places:
- **I1-L** adds the identity-contract passages for IE:213-214 and IDS:4978 (I1-RF-2).
- **I1-a** carries the product copy of the `majorLaw` text.
- **I1-b2** implements the census law of 2.5(b) and drops r1's condition (d) (I1-RF-1, I1-RF-3).
- **Cases 15 to 19** are added.

## Gates

**Product units wait for X9-6.** No product unit (I1-a, I1-b1, I1-b2, I1-c) starts before X9-6, the M2 exit gate, is integrated (M3P:5, M3P:272). The lead schedules each one.

**Design units can go first.** I1-L and I1-P edit only arch, so they may proceed once the law is accepted.

**Inventory numbers.** Inventory successor numbers are assigned by the lead at launch, after checking `git ls-files`. X9-6 may still take the next number.

**Reviewers.**
- Design units need `ACCEPT-DESIGN-UNIT` (contract successors).
- Product units with an inventory need `ACCEPT-UNIT` plus `inventoryCandidateAssessment`.
- The reviewer assignments below are suggestions; the lead decides.

## Units

| Unit | Kind | Content | Depends on | Size |
|---|---|---|---|---|
| **I1-L** | Design: contract successor | The policy-language successor of PROPOSAL items 2 to 4. A `successor.json` holds the passage overrides (WS:598, WS:603-604; PDS:296-303, PDS:937-944; IDS:1221-1231, IDS:2781-2791; COMP:34) and the appended ATOM §4a. **r2** adds the identity-contract passages IE:213-214 and IDS:4978 (`majorLaw`), which authorize the one additive member (PROPOSAL item 3). The evidence is a reference model, `cycle_representative_model.py`, with the discriminating cases below, built on `foundation/canonical.py`. No product change. | law accepted | M |
| **I1-P** | Design: contract successor | The pack contract of PROPOSAL item 5. A candidate document file holds the exact bytes of 5.2. The record names the registry row of 5.4 and the digests of 5.3, recomputed with the design encoder. It carries the self-check list S1 to S10. | I1-L | S |
| **I1-a** | Product: schemas and generated code | Product schema copies:<br>- widen `schemas/sources/policy-v2.schema.json:296-303`;<br>- widen `schemas/sources/identity-v3.schema.json:1221-1231` and `:2781-2791`, and append the r2 `majorLaw` text at `:4984`.<br>Re-pin the changed sources:<br>- `crates/identity/src/schema_registry.rs:161`, `:188`;<br>- `schemas/registry.json:169`, `:265`;<br>- `schemas/admission-registry.json:91`, `:109`;<br>- `schemas/source-map.json:111`, `:141` and `schemas/admission-source-map.json:137`, `:164`;<br>- the identity-schema pin in `crates/evaluator/src/atom-registry.json:946`, plus its `fieldFilterSchema` pin of the design PDS (`:11`).<br>Regenerate the enums in `crates/contracts/src/generated/identity.rs` (CountAtMost at `:4190`, `:4417`) and `evidence.rs` (`:38891`).<br>**No behaviour change:** the evaluator still refuses the op (`atoms.rs:3263-3268`; `policy.rs:260-289`).<br>**Tests:** schema admission of the token, plus the unchanged suites. Inventory successor. | I1-L; X9-6 | M |
| **I1-b1** | Product: evaluator admission | PROPOSAL 2.2 in `policy.rs`:<br>- root-only;<br>- `imports` at `resolved-target`;<br>- `filters: []`;<br>- no `endpoint` and no `evidence`;<br>- subject kind `file`, replacing the source-kind check for this op only.<br>This holds in both the policy pass and the program pass (`policy.rs:332-373`, `:608-642`), with `POLICY.UNKNOWN_RULE` on any violation.<br>**Tests:** under a `cfg(test)` registry, a test pack using the op admits, and each violation is row 4 with `PackDefect::RuleLaw`. | I1-a | S |
| **I1-b2** | Product: evaluator semantics | PROPOSAL 2.3 to 2.9:<br>- in `atoms.rs`: the graph projection, the SCC computed once per rule, the value table, the witness sets, and the causes;<br>- universe-extent completeness, including **r2's census law (2.5(b))**: the imports symbol census, exact-id source coverage, `population-unknown` and `uncovered-expected-source-subject`, all independent of the cell's `required` flag. There is no file-population condition; composition owns that;<br>- in `composition.rs`: the `operation` in predicate proofs;<br>- replay parity through `derive_evaluation` and `replay_run`.<br>**Fixtures:** synthetic retained inputs (facts, imports symbol inventories, the file inventory, `TargetAttributionV2`, scopes with subjects, and Coverage) for the QCM projects and the cases below. No live provider. | I1-a, I1-b1 | L |
| **I1-c** | Product: the row | Ships the pack:<br>- the `pack-registry.json` row and standing;<br>- `crates/evaluator/src/preview-typescript-pack.v1.policy.json` (5.2's bytes);<br>- the `RELEASE_PACKS.documents` entry.<br>Flips the tests:<br>- `policy_pack_tests.rs:151-175`, `:580-600`, `:603-640` (the `include_bytes!(` count goes from 7 to 8);<br>- `crates/host/src/configuration_tests.rs:102-134`.<br>Adds self-checks S1 to S9. Inventory successor. | I1-P, I1-b1 | S |

**Edges:**
- I1-L → I1-P;
- I1-L → I1-a → I1-b1 → I1-c;
- I1-b1 → I1-b2.

**Downstream:** C4 (with X12d) needs I1-c, and J2 needs I1-b2. Under LD-11, I1-c may land before I1-b2, because the op stays a structural refusal at evaluation until then.

## Discriminating cases (I1-L model, I1-b2 fixtures)

**From the corpus.** QCM:7-124 with LQM:232's target:

| Project | Expected result |
|---|---|
| `cycle` | one finding on `cycle/a.ts`, with members `cycle/a.ts` and `cycle/b.ts` |
| `self` | one finding on `self/self.ts` (a self-edge) |
| `acyclic`, `empty`, `shadow` | pass, with complete Coverage |
| `unresolved`, `malformed`, `dynamic` | indeterminate, with a blocking cause. The exact cause follows NE §4.6 and the §10 precedence, not QCM's design label |

**Added cases:**
1. **Two disjoint cycles** give two findings.
2. **A three-file SCC with duplicate edges** gives one finding. `matchingFactCount` counts every fact.
3. **Representative order is by UTF-8 bytes.**
   - `B.ts` precedes `a.ts`.
   - `a.ts` precedes `a/b.ts`, because `.` (0x2E) precedes `/` (0x2F).
   - A tie on path is broken by the universe id.
4. **An external target edge** is ignored. The result is pass when complete.
5. **An unknown-occupancy edge**, with no known cycle, is indeterminate with `target-kind-unknown`.
6. **A first-party package target**, with no known cycle, is indeterminate with `population-unknown`.
7. **A known cycle plus an unresolved import elsewhere** fails. The finding stands, and `coverage-unknown` is retained.
8. **Two known components that unknown edges might merge** give two findings, with reps b and d, and the outcome is fail.
9. **An edge entering V from a non-selected file** is not read. The result is pass when complete.
10. **An importer with no unique inventory row** is indeterminate with `population-unknown`. Its fact is in every indeterminate witness.
11. **No `typescript.imports` binding** gives `missing-relation-coverage`. It is indeterminate, never pass (DR-G25 path).
12. **A waiver** on the representative path waives the finding. If a smaller member appears later, the waiver stops matching.
13. **Op-law refusals:** the op nested under `not`; filters present; `endpoint: target`; subject kind `symbol`; relation `references`.
14. **Budget:** the graph is computed once per rule. A 1000-module linear chain (QCM:127-131) passes.

**r2 cases** (I1-RF-1 and I1-RF-3):

15. **A complete subset partition** omits another expected importer, which is CODEX2's counterexample. The census is complete, {A, B}; the one optional-cell scope holds A only, with complete Coverage; there are no facts. The result is indeterminate, with `uncovered-expected-source-subject` for B. It is never pass, whatever the cell's `required` flag.
16. **A partial symbol census with a complete file population** is indeterminate with `population-unknown` for that universe. The known rows of the partial census are still checked for coverage.
17. **Complete broad partitions**, each scope covering several importers, with every expected source covered and complete Coverage, pass when acyclic.
18. **A complete-empty census:**
    - an explicit empty-subjects scope with complete Coverage passes;
    - no scope at all is indeterminate with `uncovered-expected-source-subject`.
19. **Population-only partial file inventory** (I1-RF-3). The file inventory is partial and retains `a.ts`. The imports binding, the complete imports census, every scope and sufficient Coverage are present, with no facts, cycles or uncertain edges. The atom answers false at `a.ts`. The rule outcome is indeterminate, through composition's `incomplete-inventory` enumeration deficiency (COMP:162). There is no host fault.

## Not in these units

- **C4's detector-closure binding** (PROPOSAL LD-10) belongs to the C law.
- **The B law's default selection** (PROPOSAL item 8).
- **The M4 renderer** for the member list.
- **The M5 fixture verifier** for `policy test`.
- **I2's catalog documents.**
