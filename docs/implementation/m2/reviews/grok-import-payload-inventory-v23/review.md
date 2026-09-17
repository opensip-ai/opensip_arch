# Import-payload inventory v23 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Not runtime acceptance. Not source29. Not import-totality reference. Not Run/replay. Frozen/live/history not edited. Root remains lead.

**subjectManifestSha256** `29f3027f086e3f33991594715ad9c9c90c61d8675c3408216b1fb9981858a6e4`  
`docs/implementation/m2/import-payload-inventory-v23-subject.json` **632** bytes, 3 members, sorted unique, **0** pin mismatches. Unit directory is README + successor only.

## Parent is live inventory-22 **candidate**

Live lock: **20 inventory / 29 contract** (`61156` / `f23ec6c5…740b`). Last inventory **candidate** is

`docs/implementation/m2/repository-file-inventory.v22.json` **143331** / `f13eed68a5c70f58b3571e4712657a64702ed3522affeed7852afff1b1722376`

That is this unit’s `successor.parent` (bytes and sha256 match). Last contract is `native-runtime-selection-v14/successor.json` **12020** / `2fff7326…bfe3`. The three new paths are absent from live product.

## Candidate assessment: **ACCEPT**

Successor flags **both required true**: `parentArtifactBytesUnchanged`, `inheritedRowsEqualByValue`. `verify_design.py` inventory successor 106–107.

| Claim | Check |
| --- | --- |
| 387 inherited rows | v22 has 387 unique sorted paths; all present in v23; **0 mutated** |
| 3 new files | identical to `successor.addedFiles`; none removed |
| 390 total | 387+3 |
| 20 packages / DAG | `packages` (20) and `pendingDecisions` (9) identical; `schemaVersion` 1; no identity→evaluator; no new package |
| v22 path order | subsequence of v23 |
| row shape | `{description, generated, package, path, role, standing}` |

New rows:

| Path | Package | Role | Index |
| --- | --- | --- | ---: |
| `crates/evaluator/src/import-payload-registry.json` | opensip-evaluator | registry, `generated: false` | 64 |
| `crates/evaluator/src/import_payloads.rs` | opensip-evaluator | validator | 67 |
| `crates/host/tests/fixtures/import-payload-fixtures.json` | opensip-host | fixture | 114 |

`import_payloads.rs` is snake_case, sibling of `import_joins.rs` (validator). Registry is kebab closed extract of two-key kind/payloadDomain rows with independently derived identity/workflow document/selector/digest bindings and drift check; **not** caller schema authority. Host fixture is tests-only; shared blob pool; “preserves existing per-document parser limits” (live `MAX_BYTES` remains 4 MiB). Host `imports.rs` stays **service** I/O (inherited row, not rewritten). Correspondence remains `import_joins.rs`. No new identity API.

This layout does **not** accept payload source29, import-totality reference, or runtime.

## Description overrides — project by **stable file path**

Do not hard-code “three”. Live lock currently has **3** `inventoryPassageInheritance` rows parented at **v22**. Runtime-14 is **selected** and adds a **direct** v22 `/files/261` override on `schemas/sources/imported-v1.schema.json`. After this candidate, `verify_design.py` 312–346 inherits ancestor meaning onto v23 by filepath. All four parent rows are **unchanged** in v23.

| Source | Stable path | v22 index | v23 index |
| --- | --- | ---: | ---: |
| live inheritance | `apps/cli/src/bootstrap.rs` | 7 | **7** |
| live inheritance | `apps/report/package.json` | 13 | **13** |
| live inheritance | `package.json` | 194 | **197** |
| runtime-14 direct (selected) | `schemas/sources/imported-v1.schema.json` | 261 | **264** |

Four total after runtime-14. Activation must emit inheritance against the **v23** pin with those projected `/files/{index}/description` selectors (lexicographic selector JSON, not numeric file order). The imported-schema after-text assigns pure correspondence to `import_joins.rs` and payload admission to the evaluator crate; it does not implement source29.

## requiredFindings

None.

## Scope / limits

No product files created here. No payload source, totality reference, correspondence source re-acceptance, or live write.
