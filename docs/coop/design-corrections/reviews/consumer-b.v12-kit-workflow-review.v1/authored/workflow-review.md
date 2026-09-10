# Workflow-scope review (scope-v2 reconstruction)

**Outcome: `WORKFLOW_SCOPE_REFUSED`**

Same-session kit-only validator. This review is **separate from** the syntax-code pilot and **does not reaffirm** that pilot verdict. Not whole-consumer ACCEPT. Not product or host implementation. Frozen Run admission is out of scope.

The consumer’s own `SCOPE_INCOMPLETE` is not an oracle. Nine of the **48 claimed reconstructed IDs** fail existing published laws. Those are consumer corrections, not design gaps (`newMustIssues` / `newShouldIssues` empty).

## Custody

| Object | SHA-256 | Result |
|---|---|---|
| kit manifest | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | 80/80 PASS |
| parent | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | match |
| requirements.json | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | unchanged |
| snapshot-manifest.json | `9fb3d13f0d58a65bea8aae46600ceeff12842e7f46c8b94b59214c831f23051c` | **224/224 PASS** |

Frozen Run stores match `frozen-run-hashes.json` (syntax-code `2e74a6b2…`, ts `885b8e45…`, rust `67dc12f8…`, syntax-data `1d07e4c8…`, rust-partial `b6c2b240…`). Those hashes were verified; the Runs were **not** admitted here.

Independent probes: 114 checks, 101 pass, 13 fail after a validator schema-registry correction (D-CORR-WF-1). Original setup failures preserved in `diagnostics/workflow_scope_probes.original-schema-setup-fail.json`.

Reproduction:

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-review.v1/output/diagnostics/workflow_scope_probes.py
```

Snapshot bytes were reviewed as-is. `scope_reconstruct.py` was **not** executed (it writes). Consumer evaluators were not expected-output oracles.

## First actual refusal (reconstructed IDs, charter order)

**`R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE`** — both “ownership selections” hash the **identical** `body-language-version` (edition 2018). identity-schemas.v3 rust `languageVersionBinding` excludes ownership maps from the record, so a measured pair must show two ownership maps that *derive* one dialect. Hashing the same BLV twice is not that pair.

## Other refused reconstructed rows

These are existing-law implementations that were not executed, not missing design text.

| ID | Kind | Why refused | Selector |
|---|---|---|---|
| `R-RUN-UNSUPPORTED-GRAMMAR` | standaloneCanonicalVector | Declared `unsupported-file` flag; suffix/grammar-bundle admission not run | native-evidence.md §1.2 |
| `R-HIDDEN-MISMATCH-PER-LANGUAGE` | standaloneCanonicalVector | Declared firstRefusal dicts for TS and Rust; no native context/universe admission | R-HIDDEN-MISMATCH-PER-LANGUAGE |
| `R-CLONES-NEGATIVE-VECTORS` | standaloneCanonicalVector | `scope_reconstruct.py` raises `AdmissionError` in wrappers / assigns firstRefusal dicts | relation-payload-schemas.v2.json anchorLaw / bodyIdentityJoin |
| `R-REPAIR-AUTHORITY-PER-TARGET` | standaloneCanonicalVector | Negative is a constructed firstRefusal, not a fingerprint correspondence join | evaluator-composition-contract.v3.md unmatched / repair correspondence |
| `R-MIN-RESOLUTION-THREE-LEVELS` | standaloneCanonicalVector | Type level has only insufficient; no qualifying `types@checked` case. Vector `insufficientExpected=indeterminate` at resolved disagrees with kit (measured `false` is correct complete-absence) | atom-evaluation-contract.v1.md; identity-and-evidence.md §4 |
| `R-MIN-RESOLUTION-REPAIR-EVIDENCE` | standaloneCanonicalVector | Tied to the incomplete three-level matrix | same |
| `R-SCOPE-POLICY-ONLY-COMPARISON` | standaloneCanonicalVector | **Schema pass.** `baselineContext.scopeDigest` **equals** `currentContext.scopeDigest` while `contextDelta.scopeChanged=true` | requirement: only bound ScopeDocumentV1 changes |
| `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` | standaloneCanonicalVector | **Schema pass** on GraphQueryRequest/Response. All four graph ops request `file@enumerated`, which §3 of the query contract marks **graph-projectable no** (`QUERY.RELATION_UNSUPPORTED`). Cursor token is not `q3.<runId>.<selectionHash>.<position>`. `evidence.coverageIds` empty vs §6 disclosure | query-projection-contract.v3.md §§3,5,6 |

A stock-schema pass, a file on disk, or a `firstRefusal` literal is not executed refusal. Graph algorithm vectors correctly labelled `underlyingRunAdmissionUnverified`; that does **not** license answering an unsupported relation.

## Admitted as the published kind (not as Runs)

Independently checked:

- **schemaEnvelope** failure/public/purge/D9 envelopes: Draft 2020-12 inhabitance; `exitCode` equals inherited `classToExitCode` (request-rejected→2, operational-failed→4, policy-failed→1). Six `StepTermination` classes. Single-step analyze; multi-step `default` then `fit`. Invocation disclosure: 45 commands, query formats/parity from command-inventory.v3. Receipt/availability schema-valid and labelled synthetic host observation.
- **Config graphs:** synthesized `{entryConfigPath: null, nodes: []}`; custom `tsconfig.app.json` kind `other` (basename law); `extendsResolved` order strict then base; jsconfig + shared base; `SHA-256(C(graph))` recomputed; hash is not a graph field.
- **JS body through TS:** independently rebuilt L0 identities; `javascript` ≠ `typescript` over the same bytes.
- **Three-valued:** `exists` with no Coverage independently `indeterminate`.
- **Repair apply key ≠ mutation replay scope** (operation `purge`).
- **D9 map** equals `d9-exit-contract.v1.14.json#/classToExitCode`.
- **Comparison/baseline records** for missing / evidence-changed / empty / E0 vs E1–E3 / pivot-only inhabit evaluator3 schemas with distinguishing pivot fields. That is schema inhabitance, not a comparison engine.

Standing distinction documents (promise vs availability, subsystem owners, four empty/partial/unavailable/missing labels, detector-compat listing vs manifest) are cited vectors, not Runs.

## 134 original IDs

Full rows: `workflow-review.json#/originalRequirementIds` and `diagnostics/id-dispositions.json`.

| reviewedScope | Count |
|---|---:|
| in-scope reconstructed, independently **refused** | 9 |
| in-scope reconstructed, admitted as required kind | 39 |
| standing of consumer continuation (not re-executed here) | 24 |
| historical vector notReached this pass | 23 |
| out-of-scope frozen Run / property / replay | 39 |
| futureQualification | 3 |
| **total** | **134** |

## Not reached

Historical cap/CVE1/lexical/protocol traces; frozen TS/Rust/syntax-data/partial Run admission; generic digest-keyword engine; host auth execution; a graph walk over a **projectable** relation (`imports@resolved-target` with retained TargetAttributionV1, or `calls@resolved-callee`).

A later same-origin continuation may review remaining charter items. All 123 accept-blocking IDs remain.
