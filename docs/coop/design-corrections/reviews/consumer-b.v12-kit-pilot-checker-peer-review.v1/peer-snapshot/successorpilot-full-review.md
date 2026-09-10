# Successor pilot full review (producing-law self-audit)

**Verdict: `PILOT_FULL_ADMITS`**

Same P5 data-only kit origin as `consumer-b.v12-fresh-export-admission.v1` and `consumer-b.v12-kit-pilot-full-review.v1`. This is not a new fresh origin and not whole-consumer ACCEPT. The claim is under root review of these two exact stores only.

## Prior `PILOT_FULL_ADMITS` withdrawn

The `PILOT_FULL_ADMITS` issued in `consumer-b.v12-kit-pilot-full-review.v1` is **WITHDRAWN**.

That grade compared derived proof C after treating hashed, schema-valid `ExecutionInputsV1` (`selectedRefs`, `cellOutcomes`, `nativeCoverageAccounts`) and `SubjectInventoryV1` rows as self-authenticating population and selection. Current producing law requires those records as **inputs subject to producing joins**, not as truth because they rehash. A matching C is conclusive only after the entire expected record is produced by current law. The prior passing grade therefore exceeded measured current-law coverage.

This successor re-grades the **same two exact stores** (no remint, no repair, no new inputs) after independently reconstructing those joins. After the joins executed and passed, no store defect remains on the positive; the tamper remains a complete-replay semantic mismatch.

## Input custody

| Item | SHA-256 | Result |
|---|---|---|
| original 80-file kit manifest | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | PASS |
| parent frozen subject | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | PASS |
| original charter | `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` | PASS |
| original requirements.json | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | PASS |
| already-supplied export-manifest.json | `11863ac536312335d5d36876e95feafdc9fdf187f91b5d5ef322b7c2d234363f` | PASS |
| exports/syntax-code.store.json | `a85223b13a32c6ffcde7100dfccd526b049e7bfc848578fd5b47696e65605924` (889218 bytes) | PASS |
| exports/syntax-code.tamper.store.json | `0d868e579f937af46006d790d0f5b7a7ea72ab8fc908d27551df0dee0c045a8f` (893046 bytes) | PASS |

Claimed RunIds:

- positive: `run3:4b58935ae046491d0389306cbf9670e7c70a638b73e8835ac476bf08e310ff7b`
- tamper: `run3:8e81be4e966a29396f50b60b838b0d8257cdd213752faa903e5c26f6e8cfb49c`

## Per-graph status

| Graph | Structural | Producing joins | Semantic | First failure |
|---|---|---|---|---|
| syntax-code (positive) | ADMIT | 60 pass / 0 fail | **REPLAY_MATCH** | none |
| syntax-code.tamper | ADMIT | 60 pass / 0 fail | **REPLAY_REFUSE** | `REPLAY_PROOF_MISMATCH` after structural admit and producing joins |

Tamper identities, schema, citations, native/closure joins, **and producing joins** admitted before the logical disagreement was counted. The positive has no earlier prerequisite failure, so the tamper is an isolated logical-negative.

### Positive — derived proof equals retained claim

Independently reconstructed `selectedRefs`, file extent `{hello.rs}`, complete file inventory totality, empty package extent, symbol `examinedPaths`, derived complete cell outcomes, and derived native coverage accounts (including `vcs-change` `inapplicable-vcs` from VCS `kind=none`). Subject minted: `subject3:8bf8bec7e09259f035cb9fb392a27ffa0cf7e579b164c20c0181198704b6a3ab` (`hello.rs`, syntax universe, kind=file).

Atom `none` of `file@enumerated` filter `subject eq hello.rs`: known matching file fact ⇒ **none = false**. `emitWhen` false ⇒ no finding. Gating rule, complete population, no live finding ⇒ verdict `pass`.

Complete proof C SHA-256 `eb2a3bd6a2da159fd68c24436b47cdd0eaa064f0276bf83878ee4565f5fdae71` equals the retained proof. Enclosing identities:

- proof3 `8b21407c0b0ca62952a95201c142e66e494dd4af6524188dd1ca70202a68a521`
- evidence3 `4746de6ff54a67c062c1d23bca7ebdb6d280f598585500b0b3821ee21a57925b`
- seal3 `df983e7b0fe612a6fd8859db7b528bf9a47ecb38f9b01436dd6163533e18c713`
- run3 `4b58935ae046491d0389306cbf9670e7c70a638b73e8835ac476bf08e310ff7b`

### Tamper — structural and producing admit, then semantic refuse

Independently derived proof is the same as the positive (`none=false`, verdict `pass`, no findings, proof C `eb2a3bd6…ae71`). Claimed proof disagrees: verdict `fail`, finding `finding3:0c895614…3cdb`, proof C `2d2df6df…c9da`, Run `run3:8e81be4e…b49c`.

Mismatches: `PROOF_C_MISMATCH`, `VERDICT_MISMATCH`, `FINDING_IDS_MISMATCH`, `PREDICATE_PROOFS_MISMATCH`, `EVIDENCE_ID_MISMATCH`, `SEAL_ID_MISMATCH`, `RUN_ID_MISMATCH`.

## Producing-law coverage (measured)

Documents read start-to-end: `execution-inputs-contract.v1.md`, `enumeration-contract.v1.md`, `atom-evaluation-contract.v1.md`, `evaluator-composition-contract.v3.md` plus incorporated schemas/annotations.

Per graph: 80 inventoried assertions (60 applicable executed-pass, 0 fail, 20 inapplicable/notReached justified by admitted committed inputs). A paragraph count is not this coverage. Full law/assertion/operand/result account: `producing-law-inventory.json` and `pilot-producing-law-selfaudit.md`.

Inapplicable branches include import atoms, incoming-search, target-attribution, `all-covered`, `count-at-most`, candidate-only cells, baseline/comparison, finding emission (emitWhen false), and `discover_units` re-execution (not in the 80-file kit). Extents were still derived from retained membership+snapshot+scope.

## Helper correction retained

Predecessor Run-closure over-application of `stableId` remains corrected: S1 delivery selector is `platforms[]` `{os, arch, tree, entrypoint}` plus RJ-3. Install-registry `stableId` is not a retained Run operand.

## Reproduction

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-producing-law-selfaudit.v1/output/standalone-checker/check.py
```

## Scope

`PILOT_FULL_ADMITS` scoped to these two syntax-code stores. Not whole-134 consumer ACCEPT, not product/compiler qualification.
