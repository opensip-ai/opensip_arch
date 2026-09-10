# Blind consumer reconstruction `consumer-b.v11`

**Verdict:** `ACCEPT-RECONSTRUCTABLE`

This is an independent reconstruction of the frozen normative kit. It is **not** product qualification, host qualification, compiler measurement, or implementation authorization. Synthetic trusted observations stand in for OS/compiler/cargo/crypto/SQLite; they are never native enforcement proof.

## Input custody

- Manifest SHA-256 `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` matched the expected value.
- Declared parent subject SHA-256 `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` matched.
- All **80** listed files matched published sha256 and byte length; disk set equalled the manifest (no extras, no missing).
- Eight CVE1 closed types were read from `docs/coop/artifacts/resolved-inputs.v2.json#planIdContract.canonicalValueEncoding`.
- Five product contracts were read from `docs/v2/contracts/product-v1/` together with the current-source map. Readiness/review records were not used as recipes. Successor selectors were applied only in their declared scope (notably `capability-manifest-domains.v2.json` for ADM-DOMAIN, identity-schemas.v3 / evaluator3 for output majors, PolicyDocumentV2 / RuleProgramV2, required `executionInputsDigest`).
- Unchanged native/input identities retained declared major-2 recipes. Output majors used profile 3 (`run3`, `proof3`, `evidence3`, `seal3`, `finding3`).
- No essential normative dependency was missing from the kit.

Custody record: `vectors/phase-0-custody.json`.

## What was reconstructed

C and H were implemented from identity-and-evidence §3 (not from author code):

`H(D,X) = SHA256(ASCII("opensip.product.v1") || 00 || ASCII(D) || 00 || uint64BE(len(C(X))) || C(X))`.

CVE1 round-tripped all eight closed types. Lexical admission was exercised on **raw JSON bytes** (floats, exponents, `-0`, duplicate keys, surrogates) separately from encoding already-parsed objects. A semantic Plan-id change moved `run3`; operational request-id/timestamp fields are excluded from Run identity. Source→Plan→View→Proof→Evidence→Seal→Run joins were constructed; putting EvidenceId on a proof-bundle is a closed-record refusal and a cycle.

Capability manifests were admitted **before** CVE1 encoding against `capability-manifest-domains.v2.json` gates ADM-TYPE, ADM-CLOSED, ADM-DOMAIN, ADM-ORDER. Negatives recorded the first refusal and hypothesized masked later gates (boolean `schemaVersion`, extra keys, platform case, rung-of-another-relation, unsorted arrays, duplicate providerId).

Provider protocol traces executed the published 34-row table in `protocol3-transitions.v1.json`. A complete Hello→…→Complete→zero-exit→eof trace reached DONE with `identityNegotiated` true before any source-byte frame. Discriminating unavailable, cancel, identity-fault (OpenUniverse without tokens, `sourceBytesSent=false`), process-fault, post-terminal, and FAULT-absorb traces were executed. Frame-payload validation and real process I/O remain future-host assumptions.

The relation/rung table was derived from `relation-payload-schemas.v2.json#/x-opensip-relation-registry` (13 relations). File remains `enumerated` only — no resolved rung was invented. RC-1 fact-absent cases used `not-applicable`/`attempted=false` on non-resolved rungs. Code vs data followed the grammar-capability registry: json/toml/markdown/yaml cannot mint clones. All six advertised language modes have a representable analysis path.

## Complete positive Runs

Each claimed positive has an object table plus all blob/frame bytes keyed by digest, identity-schema validation (including `x-opensip-order` after a helper correction), native-schema validation of context/universe records, independent retained closure, evaluator replay, and export. Independent root admission of those exact exported frames is `recompute.py` (exit 0).

| Kind | RunId | Replay verdict | Close |
|---|---|---|---|
| TypeScript ordinary project (`node_modules`, bare `left-pad`, config graph, ScopeDocumentV1 bound into analysis-spec, imported runtime payload member) | `run3:8a29076240d202df0f2009a70d6bb2785da2b7b210661c57811bcedd1da7d8d8` | pass | ok |
| Rust mixed-edition workspace (`#` marker dir, target edition 2024 ≠ package 2021, same `crates/beta/src/lib.rs` under two targets, large edition map, body dialect from ownership) | `run3:bceede3ee25e566e1adeaf1ff586039965c2bc30a8eb2562800d50e59698d5a1` | pass | ok |
| Rust partial enumeration / empty clone view (`coverage=unknown`, `deficiency=input-closure-incomplete`, `nativeCause=body-language-owner-unenumerated`; not complete-empty) | `run3:d899e37b9236e4833dd25e747767b1d207b9b4259133fc7d7885ef69283aae9b` | pass | ok |
| Syntax-only code (TypeScript grammar, no TS/Rust compilation unit, inventory + clones) | `run3:75f6f436b7b66558bbda1ea709f936294a16e70d8a1f2f64f21e838c9816c48d` | pass | ok |
| Syntax-only data/document (JSON grammar; clones request `language-tier-unsupported` / `capability-missing`, not a silent complete-empty) | `run3:5a2aad1f07efa4cd15cb7eb8b98a5b18865bd3803f0aad747713d91f0b3e8b63` | pass | ok |

File-fact inventory path/hash/length joins and L0 plus L1 clone body identities (level-specification bytes retained; `body-language-version` derived) are on the TypeScript export. Native context/universe H preimages are retained as frames.

Replay after admission derived subject enumeration, matchingFactIds, coverageIds, predicate address `p`, witnesses, findings, and verdict from retained program/views/facts/Coverage/scopes/imports. A types@checked atom with no Coverage and no match is **indeterminate**, not vacuous true/false. Tampering only the claimed proof verdict while preserving record identities is refused. Equal verdicts alone were not treated as admission: `recompute.py` re-parses exported H frames, recomputes C, re-runs closure, and compares replayed verdicts.

## Graph query (required reconstruction)

Owner: `query-projection-contract.v3.md` §§1–8, evaluator3 `graph-query.schema.json` major 3, workflows §8. Executed over the admitted TypeScript Run (no new engine).

- `graph.neighbors` outgoing from `ts:src/index.ts:hello` returned one `calls@resolved-callee` row to `left-pad` `pad` (`totalItems=1`, `countBasis=exact`, `traversalCoverage=complete`).
- `graph.path` produced a one-hop canonical path (`hopCount=1`).
- `graph.reach` with `includeStart=true` returned start plus callee.
- `file@enumerated` refused `QUERY.RELATION_UNSUPPORTED`.
- Malformed endpoint kind refused `QUERY.PARAMS_MALFORMED`.
- `{latest:true}` after a host observation naming a different Run refused `QUERY.VIEW_UNKNOWN` (pagination/latest bound to the same historical selection).
- Responses and failure envelopes validated against the selected evaluator3 schemas. Query does not seal a Run.

Vectors: `queries/graph-query.json`.

## Other executed vectors

Config (synthesized, custom multi-base with repeated-base order retained, JS shared base), JS body through the TypeScript engine (`languageId=javascript` ≠ provider language), clone negatives with first-refusal, repair descriptor/authority, min-resolution three levels × qualifying/insufficient, imported-observation boundary, mutation-replay-scope vs repair-apply-key inequality, complete pinned-purge refusal (`evidence.pinned` + pin inventory). Invocation disclosure, single-step and multi-step with different selections, promise vs installed availability vs candidate-only clones, public envelopes from internal refusals (config input, retained external, host-invalid internal, producer boundary), D9 composition/precedence, durable receipt. Baseline/comparison (missing, evidence-changed, empty-result, scope-policy-only vs discovery scope), E0 vs E1–E3, pivot-only fingerprints, host-captured vs candidate-only, complete-empty/partial/unavailable/missing-bytes distinguished, detector-compatibility file vs manifest body.

## Helper correction

- **Original failure:** `finding.evidenceRefs` failed `x-opensip-order: canonical-set` (not strict ascending unique C bytes).
- **Kit selector:** identity-and-evidence §3 closed order vocabulary; `identity-schemas.v3.json` `finding.evidenceRefs`.
- **Correction:** sort `evidenceRefs` by `C(item)` before minting `finding3`. Not a design gap.

## MUST / SHOULD / advisories

- `newMustIssues`: empty. No missing public recipe blocked a required vector; remaining implementation choices (L1 tokeniser internals, physical graph accelerator) are algorithm freedom left to implementations, with retained level-specification bytes and a canonical walk.
- `newShouldIssues`: empty.
- Advisories: synthetic TCB observations; no product/implementation authorization.

## From-scratch command

```text
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v11/output/recompute.py
```

Measured: exit 0 on all five exported stores (H-frame rehash, C equality, closure, replay verdict compare).

## Limitations

- No real OS, compiler, cargo, crypto, or SQLite measurements were demanded or performed.
- Native provider execution is not claimed as enforcement proof.
- Replay tamper control is evaluator reconstruction, not authentication/host qualification.
- Some workflow envelopes (repair apply, comparison axes) are independently constructed from the selected schemas and contracts; they are not additional sealed Runs.

Machine-readable status: `blind-review.json`, `requirement-status.json`, `checkpoints/phase-0.json` … `phase-11.json`. All 131 accept-blocking IDs are `executed`; three future-qualification IDs are labeled as such.
