# Exported structural admission review

**Verdict: `EXPORTED_STRUCTURAL_ADMISSION_REFUSED`**

This is an independent Grok session over exact exported bytes. It is not whole-consumer `ACCEPT`, not product implementation, and not real host/compiler/crypto qualification. Semantic evaluator replay remains **UNEXECUTED** on every graph. A structurally admitted graph would still not be a complete accepted Run.

The six stores are claims. `objectTable` labels, claimed identities, and claimed completeness are not expected outputs. Nothing was reminted or repaired.

## Input custody

All 80 kit files, the consumer-input manifest, the original charter, `requirements.json`, the export manifest, and the six export stores rehash to the declared SHA-256 and byte lengths. See `verified-input-hashes.json`.

| Item | SHA-256 |
|---|---|
| kit manifest (`consumer-input-manifest.json`) | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` |
| parent frozen subject | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` |
| export manifest | `4101367795f1a30280601a3a01a8ea36a489f4891f9d0256e92481a8e6369129` |
| original charter | `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` |
| requirements.json | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` |

Exports (all PASS):

| Graph | Bytes | SHA-256 | Claimed RunId |
|---|---|---|---|
| syntax-code | 889354 | `8c3b68ab6d7b8823…0158` | `run3:d7b78def…c6fd` |
| syntax-code-tamper | 893182 | `f6e79d73…5985` | `run3:c624c90f…e7e3` |
| ts | 678620 | `ca1b44df…9086` | `run3:9fb05cf2…6190` |
| rust | 541150 | `3b4daf1c…d791` | `run3:db635639…b23a` |
| syntax-data | 490936 | `00fce98f…5099` | `run3:4ec370fb…1488` |
| rust-partial-clones | 501541 | `89fd6acc…004c` | `run3:4852e398…aca1` |

## What was checked

A from-scratch checker under `standalone-checker/` was derived from identity-and-evidence §3 (read start to end), identity-schemas.v3 custom annotations (`x-opensip-digest`, `x-opensip-order`, `x-opensip-digest-domains`, `x-opensip-payload-registry`), native-evidence (context/universe/toolchain/body/grammar), relation-payload-schemas.v2 (ladder, `anchorLaw`, `snapshotJoins`, `coverageTotality`, `coveragePartitionLaw`, clones body join), capability-manifest-domains.v2 (CVE1 identity and ADM-TYPE/CLOSED/DOMAIN/ORDER), execution-inputs, security S1/S2, and component-manifest-schemas.v11 as a **prose field table** (not a invented stock Draft-2020-12 root).

Assertions executed on exact retained operands include:

- blob rehash of every store member
- H-frame parse (`opensip.product.v1` NUL domain NUL uint64BE length C(X)), C round-trip, H recompute
- lexical JSON admission (duplicate keys, float/exponent, `-0`, integer range, UTF-8, depth/size)
- owning-schema validation including `x-opensip-order`
- digest-annotation walk (raw-artifact / canonical-record / h-identity / capability-manifest-id, plus the relation-document representations `snapshot-path` and `framed-body-identity`)
- Plan/snapshot config-scope agreement and `plan.budget == config.analysis.budget`
- analysis-spec parameter registry (at most one per row; evaluator3 required enumeration-plan and emission-plan)
- native context set equality; re-run of `admit_native_context` / universe binding over retained frames
- nested native identities and blobJoins
- fact2 C payloads, ladder membership, `universeRule`, `anchorLaw`, relation snapshotJoins
- clones body-identity frame (domain tag, raw-32 versions, L0 double length prefix)
- Coverage partition; file@enumerated totality; syntax unsupported-scope pairing
- citation / evaluationInputRefs membership

Stock JSON Schema error counts were never treated as admission.

## First actual refusal per graph

Later diagnostics are `notReached`. Nothing past the first refusal is a successful admission.

### syntax-code — REFUSED

- **Code:** `PREDICATE_INPUT_NOT_IN_EVALUATION`
- **Law:** identity-and-evidence.md §3: “Predicate input refs are a subset of evaluationInputRefs”
- **Operands:** `predicateProofs[].inputRefs` member `{domain: "rule-program", digest: "77b07390ddee3917485d15bdde2ab408992ec77236693895e7bc1e681ea66b8e"}` is not in `proof.evaluationInputRefs`
- **Class:** existing-law implementation miss. The subset law is literal. There is no documented exception because `proof.ruleProgramDigest` already names the program.
- Reached before refusal: 5 facts, 6 scopes, 6 coverages, 1 view, syntax context/universe, clones body join, coverage partition.

### syntax-code-tamper — REFUSED

Same first refusal, same `rule-program` digest `77b07390…6b8e`, same citation. Logical-result tamper is **not** a structural law. This graph was not compared for a false verdict. Replay remains unexecuted. It does not structurally admit.

### ts — REFUSED

- **Code:** `PREDICATE_INPUT_NOT_IN_EVALUATION`
- **Operands:** `{domain: "rule-program", digest: "bfc392674a431ed3b5e4ce966011236950fbab873273e86ef9a1319dddbeb615"}` not in `evaluationInputRefs`
- Reached before refusal: 7 facts, 7 scopes, 7 coverages, 1 import (runtime payload under the import registry), TypeScript context/universe, clones body join. `tsconfig.json` is inventoried and joined from `configGraphPaths`.

### syntax-data — REFUSED

- **Code:** `PREDICATE_INPUT_NOT_IN_EVALUATION`
- **Operands:** `{domain: "rule-program", digest: "71aaef89749857b54552f394b368a64df5a3c70df079daf7109ee1bcc9381b40"}`
- Reached: 1 fact, 3 scopes, 3 coverages. Clones Coverage over `notes.json` is `unknown` / `language-tier-unsupported` / `capability-missing` (data-document grammar; suffix not in the syntax dialect table). File inventory Coverage is `complete`. That pairing is consistent with native-evidence §1.2; it is not the first refusal.

### rust — REFUSED

- **Code:** `native.native-context-compiler-version-not-from-manifest`
- **Law:** native-evidence.md §11 (the join holds **for both languages**), §2.3/§2.4 `admit_native_context`; identity-and-evidence §3 requires Run closure to re-run that admission over retained frames. Literal equality; no Rust exception.
- **Operands:**
  - `NativeContextV2.toolchain.rustcVersion` = `1.80.0`
  - admitted `toolClosure.closureId` = `closure2:e150a3e4915c0d08bf7a260ae0fccc4bd1ea9a7b1019efbf291e98a8f3365352`
  - that closure’s `semanticVersion` = `1.0.0` (component manifest `version` is also `1.0.0`)
- Reached: snapshot inventory, toolchain/stdlib-family closures, one native context frame. Facts, universes, clones, and partial-ownership laws were **notReached**.

### rust-partial-clones — REFUSED

Same native compiler-version refusal, same `rustcVersion` `1.80.0` vs closure `semanticVersion` `1.0.0`, same `toolClosureId`. Partial-enumeration / empty-clones Coverage laws were notReached.

## Finding class

Both refusal families are **existing-law implementation misses** in the exported bytes. The recipes are present in the kit and were executed. No absent or contradictory recipe was required to decide these six graphs.

The TypeScript graphs set `compilerVersion` to the toolchain closure `semanticVersion` (`1.0.0`). The Rust graphs did not apply the same join to `rustcVersion`.

## Replay

Full semantic proof replay is outside this bounded review. **Replay remains UNEXECUTED** on every graph. No graph is an accepted complete Run. The tamper graph was not judged by comparing claimed logical result to recomputed truth.

## Reproduction

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-fresh-export-admission.v1/output/standalone-checker/check.py
```

Equivalent: `standalone-checker/reproduce.sh`.

The checker does not import author models, does not access other `/tmp/opensip-design-corrections` origins, and does not repair stores.

Machine-readable companion: `exported-admission-review.json`. Per-graph executed/notReached law rows live there under `graphs[].applicableLawCoverage`.

## Limitations

- After first refusal, remaining applicable laws are `notReached`, not passes.
- This review does not discharge the original consumer’s 134 reconstruction obligations.
- No real OS/compiler/crypto/SQLite or host-authentication qualification.
- Detached component-manifest signature envelopes are operational provenance (S1); this checker admits stored manifest **bytes** under the metadata profile and prose field table, and projects `type=file` tree rows. It is not a second signature verifier.
- Execution-input cell-outcome derivation and capability-manifest ADM gates were notReached on graphs that failed earlier.
- Architecture 13’s offline schema-closure rule was observed (no network retrieval).
