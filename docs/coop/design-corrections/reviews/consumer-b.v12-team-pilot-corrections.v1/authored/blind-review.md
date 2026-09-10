# Blind consumer reconstruction — consumer-b.v12

**Verdict: `ACCEPT-RECONSTRUCTABLE`**

This is an independent reconstruction of the frozen OpenSIP product-contract kit. It is **not** product qualification and **not** implementation authorization. External root admission of the exported frames is a separate later gate and was **not** observed here.

## Input custody

- Manifest SHA-256 `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` matches expected `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8`.
- Parent subject `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` matches.
- **80/80** kit files hash- and size-verified (`hash-verification.json`).
- Eight CVE1 closed types are present in `resolved-inputs.v2.json#planIdContract.canonicalValueEncoding`.
- Five product contracts were read via `docs/v2/contracts/product-v1/README.md`. Successor-over-inherited is applied only within declared scope (notably `capability-manifest-domains.v2.json` as ADM-DOMAIN successor of delivery.v4 `valueDomains`). Readiness/review records were not used as recipes.

## What was reconstructed

Canonical JSON **C**, identity **H**, and **CVE1** were implemented from prose (not author code). Lexical admission was exercised on **raw bytes** (duplicate keys, floats, exponents, `-0`, integer range, unpaired surrogates). Semantic field changes move snapshot2; RequestId/ExecutionId/wall-clock do not enter H.

Capability-manifest admission runs **ADM-TYPE → ADM-CLOSED → ADM-DOMAIN → ADM-ORDER** before encoding. Negatives record the first refusal and that later gates are masked.

Provider protocol3 traces were executed from `protocol3-transitions.v1.json` (complete, unavailable, cancel, process-fault, OpenUniverse without identity with `sourceBytesSent=false`, post-terminal). Frame payload validation and OS waitpid/EOF remain future-host assumptions.

Relation/rung applicability, RC-0/1/2 count-class-attempt (including fact-absent), code-vs-data matrix, and advertised language-mode paths were derived from the registries. File facts stay on `enumerated`.

### Complete positive Runs (exported stores)

| Run | Path | Notes |
|---|---|---|
| Syntax-code (pilot) | `runs/syntax-code.store.json` | `run3:aa19beddb09888f33cc29eb127574259331922655122840e74293ff0c1704835` — rust grammar, no TS/Rust compilation unit, file+declares+clones L0/L1, replay |
| TypeScript | `runs/ts.store.json` | `run3:1908c594bab9c7120d4d96053763454a518667d8c0413e55903d95849b02264c` — node_modules/left-pad, bare specifier, ScopeDocumentV1 parameter, import2 member |
| Rust | `runs/rust.store.json` | `run3:da14a1f03dfdd1fa623883ce48cdbd56173c7f3a129168f778fe27eb49bc541b` — `#/` marker directory, mixed editions, bin target edition 2021 ≠ package 2018, large edition map, measured L0 pair |
| Syntax-data | `runs/syntax-data.store.json` | `run3:5d0fc9fab63c2756597fe82befe0451061e0e3073d6d65c1f7a4c77b89966532` — json data-document; clones unknown + language-tier-unsupported/capability-missing (not complete-empty) |
| Rust partial clones | `runs/rust-partial-clones.store.json` | `run3:41926396a6c6da9e093ab614d330d9b2b65321c84f82080d661043edfa748707` — partial ownership, empty clone facts, unknown Coverage + input-closure-incomplete / body-language-owner-unenumerated |

From-scratch recompute:

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12/output/scripts/replay_from_export.py \
  /tmp/opensip-design-corrections/consumer-b.v12/output/runs/syntax-code.store.json
```

Each claimed positive was stock-schema-validated including independently implemented `x-opensip-order`, then closed under retained joins (file inventory path/digest/length/blob; L0 recompute; capability-manifest derived id; acyclic proof↛evidence/run), then replayed. A tamper that preserves citations and changes `proof.verdict` produces different C and is refused. Missing Coverage with no match is Kleene indeterminate, not vacuous true/false.

Graph query: `query/measured-neighbors.json` walks the admitted TypeScript Run's `imports@resolved-target` fact. Without TargetAttributionV1 the contract omits the edge (`unprojectable-fact`); that limitation is recorded rather than inventing a target kind.

## Helper correction

Protocol3 post-terminal matching initially used `tuple | set` (TypeError). Corrected from the published `preMatchLaw` to a set union. Original failure preserved in `checkpoints/phase-3.json`. Not a design gap.

## Issues

`newMustIssues`: none. No essential kit recipe was missing; no invention of a semantic contract was required.

`newShouldIssues`: none.

Advisories: L1 tokenisation belongs to the retained level specification (algorithm freedom). Graph imports projection requires TargetAttributionV1 (already specified). Root admission remains external.

## Limitations (not MUST/SHOULD)

- Real OS/compiler/crypto/SQLite measurements are future qualification.
- Native rustc/cargo/tsc execution is not claimed as enforcement proof.
- Synthetic closures/toolchains are trusted observations for identity reconstruction, never native TCB proof.
- Host authentication is out of scope.

## Requirement status

All 8 standing rules and 123 reconstruction IDs are `executed`. Three items remain `futureQualification`. Phase 11 `requirementIdsUnexecuted` is empty.
