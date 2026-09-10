# Workflow-scope review (successor after self-audit of v1)

**Outcome: `WORKFLOW_SCOPE_REFUSED`**

Same-session kit-only validator. Bounded self-audit of workflow-review.v1; **not** a new origin; **does not reaffirm** the syntax-code pilot; **not** whole-consumer ACCEPT. Frozen Run admission is out of scope. Historical v1 output was **not edited**.

The consumer’s own `SCOPE_INCOMPLETE` is not an oracle. Fifteen of the **48 claimed reconstructed IDs** fail existing published laws (nine v1 refusals kept, six v1 admits withdrawn). Those are consumer corrections, not design gaps (`newMustIssues` / `newShouldIssues` empty; no absent or contradictory laws).

## Custody

| Object | SHA-256 | Result |
|---|---|---|
| kit manifest | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | 80/80 PASS |
| parent | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | match |
| requirements.json | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | unchanged |
| snapshot-manifest.json | `9fb3d13f0d58a65bea8aae46600ceeff12842e7f46c8b94b59214c831f23051c` | **224/224 PASS** |

Frozen Run stores match `frozen-run-hashes.json` (syntax-code `2e74a6b2…`, ts `885b8e45…`, rust `67dc12f8…`, syntax-data `1d07e4c8…`, rust-partial `b6c2b240…`). Hashes verified; Runs **not** admitted.

Self-audit probes: 169 checks, 143 pass, 26 fail. **Probe counts are not conformance counts.** v1 114/101/13 retained at `diagnostics/v1-originals/`.

Reproduction:

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-review.v2/output/diagnostics/self_audit_probes.py
```

Snapshot bytes were reviewed as-is. `scope_reconstruct.py` was **not** executed (it writes). Consumer evaluators were not expected-output oracles.

## First actual refusal (reconstructed IDs, charter order)

**`R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE`** — both “ownership selections” hash the identical `body-language-version` (edition 2018) and retain no `SourceUnitOwnershipV1` preimages. identity-schemas.v3 rust `languageVersionBinding` excludes ownership maps from the record, so a measured pair must show two ownership maps that derive one dialect. Stamping two labels onto one BLV is not that pair.

## Refused reconstructed rows (15)

Existing-law implementations. Unexercised declared firstRefusal is labelled separately from invalid produced values.

| ID | Kind | Class | Why refused | Selector |
|---|---|---|---|---|
| `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` | completeRunProperty | insufficient produced pair | identical BLV twice; no ownership-map preimages | identity-schemas.v3 rust languageVersionBinding |
| `R-RUN-UNSUPPORTED-GRAMMAR` | standaloneCanonicalVector | unexercised | declared `unsupported-file` flag; suffix/grammar-bundle admission not run | native-evidence.md §1.2 |
| `R-HIDDEN-MISMATCH-PER-LANGUAGE` | standaloneCanonicalVector | unexercised | declared firstRefusal dicts; no native context/universe admission | R-HIDDEN-MISMATCH-PER-LANGUAGE |
| `R-CLONES-NEGATIVE-VECTORS` | standaloneCanonicalVector | unexercised | hand-raised AdmissionError wrappers / assigned dicts | relation-payload-schemas.v2.json anchorLaw / bodyIdentityJoin |
| `R-REPAIR-AUTHORITY-PER-TARGET` | standaloneCanonicalVector | unexercised | constructed firstRefusal, not an executed correspondence join | evaluator-composition-contract.v3.md unmatched |
| `R-MIN-RESOLUTION-THREE-LEVELS` | standaloneCanonicalVector | incomplete + invalid expected | no type qualifying; `insufficientExpected=indeterminate` at resolved disagrees with kit measured `false` | atom-evaluation-contract.v1.md; identity-and-evidence.md §4 |
| `R-MIN-RESOLUTION-REPAIR-EVIDENCE` | standaloneCanonicalVector | incomplete | prose tied to the incomplete matrix, not repair-evidence records | same |
| `R-REPAIR-APPLY-KEY` | standaloneCanonicalVector | invalid produced key | **v1 admit withdrawn.** applyKey is not `C({operation, projectId, repairPlanId, baseSnapshotId})` | workflows-and-surfaces.md §1 |
| `R-CHAIN-ZERO-CONFIG-TO-RECEIPT` | standingRule | checklist | **v1 admit withdrawn.** four-arrow checklist; original verb forbids that | R-CHAIN-ZERO-CONFIG-TO-RECEIPT |
| `R-MULTI-UNIT-MISSING-CAPS` | standaloneConfigVector | citation | **v1 admit withdrawn.** named lists, not executed zero-config selection | native-capability-matrix.v2.json |
| `R-CANDIDATE-ONLY-CLONES` | standaloneConfigVector | citation | **v1 admit withdrawn.** flags, not `kinds=[]` + `candidateSourcePaths` | enumeration-contract.v1.md |
| `R-SCOPE-POLICY-ONLY-COMPARISON` | standaloneCanonicalVector | invalid produced value | **Schema pass.** identical `scopeDigest`s with `contextDelta.scopeChanged=true` | R-SCOPE-POLICY-ONLY-COMPARISON |
| `R-PIVOT-ONLY-FINGERPRINTS` | standaloneCanonicalVector | invalid produced example | **v1 admit withdrawn.** Schema pass. fingerprint in B and E0, not only in a pivot; counts mismatch classification | workflows-and-surfaces.md §3 |
| `R-HOST-CAPTURED-VS-CANDIDATE` | standaloneCanonicalVector | citation | **v1 admit withdrawn.** two gloss strings, not retained observations | execution-inputs-contract.v1.md |
| `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` | standaloneCanonicalVector | invalid produced value | **Schema pass** on GraphQueryRequest/Response. `file@enumerated` is graph-projectable no; success responses produced; failure is `QUERY.VIEW_UNKNOWN` not `QUERY.RELATION_UNSUPPORTED`. Cursor-`c1` and universal nonempty `coverageIds` grounds **withdrawn** (artifact `nextCursor` is null; §6 is selected-views) | query-projection-contract.v3.md §§3,5,6,7 |

A stock-schema pass, a file on disk, or a `firstRefusal` literal is not executed refusal. Graph algorithm vectors correctly labelled `underlyingRunAdmissionUnverified`; that does **not** license answering an unsupported relation.

## Admitted as the published kind (33; not as Runs)

Independently rechecked:

- **schemaEnvelope** failure/public/purge/D9 envelopes: Draft 2020-12 inhabitance; `exitCode` equals inherited `classToExitCode`. Six `StepTermination` classes. Single-step analyze; multi-step `default` then `fit`. Receipt/availability schema-valid and labelled synthetic host observation. `R-FAILURE-ENVELOPES-D9` actual path is `envelopes/failure-d9-complete.json` (v1 wrote `envelopes/d9-complete.json`).
- **Invocation disclosure:** 45 commands and query formats/parity from command-inventory.v3. This is inventory-derived disclosure, **not** a CommandEnvelope (v1 `admitted-schema-envelope` corrected).
- **Config graphs:** synthesized `{entryConfigPath: null, nodes: []}`; custom `tsconfig.app.json` kind `other` (basename law); `extendsResolved` order strict then base, base also reached via strict; jsconfig + shared other-filename base; `SHA-256(C(graph))` recomputed; hash is not a graph field.
- **JS body through TS:** independently rebuilt L0 identities; `javascript` ≠ `typescript` over the same bytes.
- **Three-valued:** `exists` with no Coverage independently `indeterminate`.
- **MutationReplayScopeV1** operation `purge` (repair-apply excluded). Not admitted as a digest pair against the withdrawn apply-key.
- **RepairPlanV1 / RepairPlanDescriptor** five-field `closedWorld` projection shape and fingerprint targets. `repairPlanId` is **not** `H("workflow.repair-plan", descriptor)` — admitted as schema inhabitance, not as the committed H recipe.
- **D9 map** equals `d9-exit-contract.v1.14.json#/classToExitCode`.
- **Comparison/baseline records** for missing / evidence-changed / empty / E0 vs E1–E3 / baseline-audit inhabit evaluator3 schemas with distinguishing pivot/delta fields. comparison2/baseline2 ids are **not** `H` of those descriptors. That is schema inhabitance, not a comparison engine.
- **Test/prep/repair authorization:** three CommandEnvelope refusals, not host execution.
- **Standing distinction documents** (promise vs availability, subsystem owners, four empty/partial/unavailable/missing labels, detector-compat listing vs manifest, semantic vs operational, mutation vs analysis): cited vectors whose **cited kit passages were read**. Presence alone was not treated as content review.

## 134 original IDs

Full rows: `workflow-review.json#/originalRequirementIds` and `diagnostics/id-dispositions.json`. Charter overlap is exact (8 standing + 123 requirements + 3 future).

| reviewedScope | Count |
|---|---:|
| in-scope reconstructed, independently **refused** | 15 |
| in-scope reconstructed, admitted as required kind | 33 |
| standing of consumer continuation (not re-executed here) | 24 |
| historical vector notReached this pass | 23 |
| out-of-scope frozen Run | 24 |
| out-of-scope frozen Run replay | 12 |
| futureQualification | 3 |
| **total** | **134** |

v1 markdown table listed frozen out-of-scope as 39 **and** futureQualification as 3 (sum 137). `out-of-scope` already included the three future ids. Corrected above.

## Not reached

Historical cap/CVE1/lexical/protocol traces; frozen TS/Rust/syntax-data/partial Run admission; generic digest-keyword engine; host auth execution; a graph walk over a **projectable** relation (`imports@resolved-target` with retained TargetAttributionV1, or `calls@resolved-callee`).

A later same-origin continuation may review remaining charter items. All 123 accept-blocking IDs remain.
