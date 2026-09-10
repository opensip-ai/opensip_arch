# Blind consumer reconstruction — consumer-b.v13

**Verdict:** `ACCEPT-RECONSTRUCTABLE`

This is a new independent origin. It did not author the design, did not read
author models, fixtures, goldens, or prior reviews, and did not spawn agents.
It is **not** product qualification and **not** implementation authorization.
External root admission of the exported frames remains a separate, unobserved
gate.

## Input custody

| Check | Result |
|---|---|
| Manifest SHA-256 `afa3abfbb3dd26e10026058d433fc1871505fbd9d1c928f79e881d514e5cc40d` | PASS |
| Parent subject `fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d` | PASS |
| 87 kit files, hashes and sizes | all PASS, no extras, none missing |
| Eight CVE1 types | null, false, true, unsigned-64, negative-signed-64, NFC-UTF8-string, array, string-keyed-map |
| Five contracts | identity, security, native, workflows, admission — via `docs/v2/contracts/product-v1/README.md` |
| Current-source map | used for scope only |
| Readiness/review records | excluded; not used as recipes |

Selected profile: identity/evaluator **output major3** (`finding3` / `proof3` /
`evidence3` / `seal3` / `run3` / `policy-derivation3` / `subject3`),
PolicyDocumentV2 / RuleProgramV2, required `executionInputsDigest`. Unchanged
native/input identities retain declared **major2** recipes. Effective
capability-manifest ADM-DOMAIN registry:
`native/capability-manifest-domains.v2.json` (successor of DELIVERY v4
`valueDomains` within its declared scope). Attribution owner is
TargetAttributionV2.

## What was reconstructed

Independently implemented from kit prose:

- Canonical JSON **C** and framed **H** (`opensip.product.v1`)
- **CVE1** encode/decode of all eight types
- Lexical admission on **raw UTF-8 JSON** (floats, exponents, `-0`, duplicate keys)
- Semantic-field vs operational RequestId/ExecutionId
- Acyclic source → Plan → View → Proof → Evidence → Seal → Run
- Capability-manifest admission **before encoding**: ADM-TYPE, ADM-CLOSED,
  ADM-DOMAIN, ADM-ORDER, then CAP-MANIFEST-ID-V1
- Protocol-3 traces from `protocol3-transitions.v1.json` (complete, unavailable,
  cancel, fault, identity-before-source, post-terminal). `zero-exit`/`eof` are
  labelled future-host assumptions
- Full registered relation/rung table; file stays `enumerated`; no invented
  resolved rung

## Complete positive Runs (exported)

Each has an object table, all blob/frame bytes keyed by digest, independent
identity recompute, and a **fresh** proof derivation from retained
program/evidence (not from the saved replay JSON).

| Graph | Export | Fresh replay |
|---|---|---|
| TypeScript (`node_modules` / bare `left-pad` / ScopeDocumentV1 / import2 member) | `runs/ts.store.json` | identities match; complete proof bundle equal; verdict `fail` (gated `file.exists` true) |
| Rust mixed-edition workspace, `#` marker `crates/foo#bar`, target edition 2021 ≠ package 2018, same `shared.rs` under two selections | `runs/rust.store.json` | identities match; bundle equal; body identity **stable** when only ownership selection changes without dialect change; two editions **differ** |
| Rust partial enumeration, empty clone view | `runs/rust-partial.store.json` | `none(clones)` is **indeterminate** (unknown Coverage + `body-language-owner-unenumerated`), not vacuous pass |
| Syntax-only code (no TS/Rust compilation unit) | `runs/syntax-code.store.json` | identities match; bundle equal |
| Syntax-only data/document (markdown/json); clones `language-tier-unsupported` | `runs/syntax-data.store.json` | identities match; bundle equal; unsupported analysis not concealed as complete-empty |

Tamper control: preserve record identities and citation membership, change
claimed verdict → complete-bundle comparison **refuses**. This is evaluator
replay, not host authentication.

## Graph query

Executed over the admitted TypeScript Run using
`query-projection-contract.v3` §§1–8 and evaluator3 `graph-query.schema.json`
major3: `graph.neighbors`, zero-hop `graph.path`, `graph.reach`, cursor bound
to historical `runId`, page vs operation bounds, malformed/mismatched failure
envelopes with synthetic host `RequestId`. Query is read-only and does not seal
a Run. Vectors: `query/graph-query.json`.

## Helper correction (kit-only)

| Original failure | Kit selector | Correction |
|---|---|---|
| `replay_export` `KeyError`: `executionInputsDigest` blob not retained | `execution-inputs.schema.v1.json` `additionalProperties: false`; composition §9.1 digest is SHA-256 of `C(ExecutionInputsV1)` | Strip helper-private `_inventoryRefs` before C/hash/retention so the digest names the closed record actually stored |

No open helper failure remains on a claimed positive.

## From-scratch command

```
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v13/output/reconstruct.py
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v13/output/replay_export.py /tmp/opensip-design-corrections/consumer-b.v13/output/runs/ts.store.json
```

`replay_export.py` reloads the export, recomputes H identities, and re-derives
the complete proof from retained policy, facts, Coverage, subjects and
execution-inputs. Saved `*.replay.json` files are inspection output only.

## Issues

- **MUST:** none (`newMustIssues` empty after all accept-blocking IDs executed)
- **SHOULD:** none
- **Advisories:**
  - `ADV-ENUMERATION-PLAN-SHAPE` — ProgramBinding enumerator used a minimal
    `{closureId}` object. Root admission of the exact exported frames is the
    external gate.
  - `ADV-STOCK-SCHEMA-NOT-ADMISSION` — a stock JSON Schema pass is only one
    stage; published `x-opensip-order` / `x-opensip-digest` and registry joins
    were independently implemented in helpers and must be re-checked at root.

## Limitations

- External **root admission** of these exact exported frames is unobserved here
  and must not be inferred from helper self-consistency.
- Real OS/compiler/crypto/SQLite measurements, native cargo/tsc execution as
  enforcement, and host authentication are **future qualification**.
- Synthetic TCB observations (compiler versions, process exit) are labelled
  assumptions, never native enforcement proof.

## Requirement status

131 executed + 3 future-qualification. No accept-blocking ID remains
unexecuted or failed. Machine-readable rows: `requirement-status.json`.
Checkpoints: `checkpoints/phase-0.json` … `phase-11.json`.
