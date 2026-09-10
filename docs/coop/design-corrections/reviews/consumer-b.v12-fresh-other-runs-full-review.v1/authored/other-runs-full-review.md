# Bounded four-Run full review (independent kit-only)

**Scoped verdict: `FOUR_RUNS_REFUSED`**

This is not whole-consumer acceptance, product qualification, or implementation authorization. The original charter has 123 requirements plus standing rules. This review covers only the four exported complete Run kinds and the native, import, structural, and evaluator laws those graphs actually invoke.

Independent origin: `grok-kit-only-other-runs-full-review-v1`. No previous session, author helper, root checker, or implementation was consulted. Expected truth was not taken from claimed proof, witness, or output flags.

From-scratch command:

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-fresh-other-runs-full-review.v1/output/checker/main.py
```

## Input custody

| Item | Value |
|---|---|
| Kit manifest SHA-256 | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` |
| Parent subject SHA-256 | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` |
| Kit files | 80 / 80 path+sha256+bytes **PASS** |
| Export-manifest SHA-256 | `b515c415da8c0a496e0078b48dfb8b3eabb9364e3522d48929343492d116023b` (matches the required value) |
| Extra / missing kit files | none |

| Export | Run ID | Store SHA-256 | Bytes |
|---|---|---|---|
| TypeScript | `run3:26dd437679e894c1cf01d5fb4b94de66bc15cc4ce8c8aaf26b3864144bc60164` | `bac8d38326c538465293f664720a9386ef0b365f38cad3514292036af85510b6` | 709874 |
| Rust complete | `run3:9032d3b0a3816dbd898edbf08c3c42c8117a1765eb33e7c74920b0ddaaa35436` | `44989322177b44de73ec3e9d6426615673712dc7c05bfaba033043b130f7ab82` | 548285 |
| Syntax data | `run3:ab1d6fc49b671377fbab9d6043b976d7e9c4040cec104e0c5489a8552344ae7f` | `2c4f195099c5a3edf303349c1fcc182d325d73d3a65913fdcc3fe9a585b3cc7e` | 490800 |
| Rust partial | `run3:0f06d053d40d79a3ae4f89c48ecab63064fefd14fb26fd277d1dcebd60098c5b` | `ddd728769a6dd67f4ede521f496790122fef8dd2b157a5138dc6f92ec4469920` | 508684 |

All four blob tables rehashed 100% to their keys. Object-table byte lengths matched retained blobs.

## Layered results

Acceptance stops at the first actual prerequisite refusal. Later layers are `notReached` or explicitly `DIAGNOSTIC`, never `PASS` through a failed admission.

| Run | raw | structural | fullsemantic | scoped | first refusal |
|---|---|---|---|---|---|
| TypeScript | PASS | **REFUSED** | DIAGNOSTIC | REFUSED | `IMPORT_PRODUCER_KIND` (structural) |
| Rust complete | PASS | PASS | PASS | FULL_ADMIT | none |
| Syntax data | PASS | PASS | PASS | FULL_ADMIT | none |
| Rust partial | PASS | PASS | **REFUSED** | REFUSED | `PROOF_MISMATCH` (fullsemantic) |

Because two of four complete positives refuse independent admission or complete-bundle replay, the bounded four-Run verdict is **`FOUR_RUNS_REFUSED`**.

## What the independent checker actually did

The checker is under `checker/`. It loads every current kit owner (identity v3 digest domains and payload registry, relation registry, native evidence schemas and capability matrix, grammar-capability registry, deficiency-cause registry, enumeration/subject-inventory/emission/execution-input schemas, atom projection registry, PolicyDocumentV2 / RuleProgramV2, imported-evidence). It does not treat a stock JSON Schema pass as admission.

For each export it:

1. **Raw.** Parse `objectTable` + base64 blobs; rehash every blob; require a `run3:` root.
2. **Structural.** Parse H-frames (`opensip.product.v1` ‖ 00 ‖ domain ‖ 00 ‖ u64be(len) ‖ C(X)); recompute C and H; validate owning schemas including `x-opensip-order`; execute digest-domain snapshot/nested/blob joins; re-run native context/universe field agreement; apply relation ladder, anchor cardinality, and inventoried-file joins; recompute L0 clone `bodyIdentity` from body-span bytes + framed fact-identity grammar; check Coverage RC-6 and deficiency/nativeCause pairing against the native cause registry.
3. **Full semantic.** Re-admit enumeration plan vs requestedCapabilities vs inventories; derive execution-input cell outcomes; enumerate subjects from inventories (not from claimed findings); scan atoms over retained facts/Coverage/scopes; compose Kleene values, witnesses, rule outcomes, execution deficiencies, and sealed verdict; compare the complete proof bundle including `witnessDigest`.

Claimed proof/witness/verdict were comparison targets only.

Helper corrections (not design gaps) are in `measured/helper-corrections.json`: raw-artifact schemas are not C-records; ownership `pathField` is `markerPath` on `units`; witness hashing uses the closed predicate-witness record plus independently computed `programPredicateDigest`.

## Findings that refuse admission

### MUST-TS-IMPORT-PRODUCER-KIND

Owner: `identity-schemas.v3.json` `x-opensip-digest-domains.closureKinds.byField["import.producerClosure"] = "provider"` and the companion `import.adapterClosure = "adapter"` rule.

The TypeScript graph does contain a real import member `import2:86b1b376eafc5832422721f095788bdc6980682380fd563268141f3a3a9298f1` (kind `runtime`, completeness `complete`, payload schema digest of `imported-evidence.schema.json`). Both `producerClosure` and `adapterClosure` are `closure2:9c26e0f23ed995ec5941a8ce5197081ad667521310f2016b730bf25491818ad9`, whose retained closure record has `kind=adapter`.

That is a structural refusal. The import is not admitted. Later semantic replay on this Run is diagnostic only and must not be read as a complete positive.

Diagnostic (not admission): independently selected `subject3:6c0ff4ff…` (`src/index.ts`), atom `none`/`file`/`enumerated` is **false** because file fact `fact2:2a53f4d5…` matches, `witnessDigest` equals the retained claim, sealed verdict `pass`. L0 clone identities independently equalled the claimed payloads:

- `src/app.ts` → `sha256:283882e7438a63a8e015218d39282180d155433918d43be1f4919ce782bc5d47`
- `src/index.ts` → `sha256:aacf096e38b55e9c0c3c0468c24c57dd8937b57e12c9a562414a0ede3fd360f6`

Snapshot includes `node_modules/left-pad`. `ScopeDocumentV1` is an analysis-spec parameter (`include: src/**/*.ts`, `exclude: node_modules/**`). Those properties are exhibited as retained bytes; they do not rescue the import producer-kind refusal.

### MUST-PARTIAL-RULE-ENUMERATION

Owner: `evaluator-composition-contract.v3.md` §2 and §5.

Rust-partial **structural** clones law holds:

- `SourceUnitOwnershipV1.enumeration = partial`
- clones Coverage `coverage=unknown`, not complete-empty
- pairing `deficiency=input-closure-incomplete`, `nativeCause=body-language-owner-unenumerated` (allowed by `native-evidence.schemas.v2.json` `x-opensip-deficiency-cause-registry` for `input-closure-incomplete`)
- clones-fact file inventory `state=partial`, `rows=[]`

Complete semantic replay then refuses. The clones-fact cell stores `kinds=["file"]`. Composition §2: a partial inventory belongs in `incompleteInventoryRefs` even with zero rows; known rows still evaluate. The enabled gating rule `file-present` enumerates **file** subjects in the rust universe, so that partial file inventory makes rule-enumeration incomplete. §5: a gating rule with incomplete population is indeterminate.

| Field | Independent | Retained claim |
|---|---|---|
| rule `file-present` outcome | `indeterminate` | `pass` |
| rule enumeration state | `incomplete` | (claimed pass) |
| selected subject | `subject3:ab94b167…` still evaluated from the complete inventory cell | same subject in predicateProofs |
| sealed verdict | `indeterminate` | `indeterminate` |
| execution deficiency | `input-closure-incomplete` / `body-language-owner-unenumerated` | same |

Verdict-only comparison would hide this. Complete-bundle comparison refuses. This is not repaired by minting a waiver.

## Graphs that independently admitted and replayed

### Rust complete — FULL_ADMIT

Nonempty `plan.nativeContextDigests`. Three rust universes share one context and select different `SourceUnitOwnershipV1` records over the same physical file `#/a/src/lib.rs` (bin `targetEdition=2021` vs package default `a=2018`, plus lib-test). Universe `edition` is a large map (`a` plus `crate00`–`crate15` across 2015/2018/2021/2024). Inventoried `#/` marker paths are present. Nested cargo projection / dependency-source-set / unified-features frames joined. L0 clone identity independently equalled `sha256:92d56dc3a9124e028406f19d2265efa81a4d80545bce990bb1ccf7e08eb36aa0`. File-present `none` is false; sealed verdict `pass`; `witnessDigest` and rule outcome matched the retained proof.

No import is on this graph. Mixed-edition / hash-marker / target-edition properties are exhibited here.

### Syntax data — FULL_ADMIT

Syntax-only context grammar `languageId=json`, `syntaxClass=data-document`. Grammar-capability registry gives json only `file@enumerated`, `package@manifest-declared`, `vcs-change@vcs-reported` — not `clones@normalized-body-hash`. The export does **not** conceal that as complete-empty clones: Coverage is `unknown` with `language-tier-unsupported` / `capability-missing`, which is exactly the deficiency-cause-registry pair for `language-tier-unsupported`. Required clones-fact cell outcome is `partial`. Independent composition: rule `file-present` pass (notes.json file fact exists), required execution deficiency present, sealed verdict `indeterminate`. Complete proof bundle including `witnessDigest` matched.

Inventory capability is present. No TypeScript or Rust compilation unit. Semantic capabilities the grammar cannot serve are typed-unavailable.

## Global clone quantifier

`R-RUN-CLONES-L0-AND-NORMALIZED` is a global at-least-one, not a per-language demand. L0-verbatim was independently recomputed on TypeScript (diagnostic) and Rust complete. None of the four exports carries a non-L0 normalized/structural clone fact. That normalized level is unexhibited on this export set. No fifth Run kind was invented.

## Requirement coverage (bounded)

See `measured/requirement-coverage.json`. Original 134-consumer IDs are accounted as in-scope executed, failed, unexecuted-on-this-export-set, or out-of-scope (query; syntax-code Run; standalone vectors/envelopes/traces not requested here).

Failed in this bounded pass: `R-RUN-TS` (and therefore import-in-graph admission), `R-RUN-RUST-PARTIAL-EMPTY-CLONES` complete-bundle replay (structural clones pairing itself held).

Not claimed: `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR`. TypeScript was only prepared as a later query subject; it does not currently admit, so no query execution is possible without inventing a new engine over a refused graph.

## What this does not say

- It does not ACCEPT the original 134-consumer reconstruction.
- It does not qualify a product, compiler, host, or release.
- It does not authorize an implementation.
- Hash identity of a saved proof was never treated as replay success.
- Failed admission was not repaired by reminting inputs or inventing semantic waivers.
