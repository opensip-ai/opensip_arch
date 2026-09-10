# Pilot-admission checkpoint — TypeScript Run

**Verdict: `PILOT-CHECKPOINT-COMPLETED`**

`reconstructionAccepted` is **false**. `rootAdmission` is **unobserved**. This checkpoint does **not** emit `ACCEPT-RECONSTRUCTABLE` and does **not** claim the original 123/8/3 reconstruction is done.

## What this checkpoint is

Same-origin continuation of `consumer-b.v13` after continuation.v2. Bounded work: one TypeScript complete Run, with every original attached property, by auditing the **executed bodies** of admission/closure/replay helpers against the kit and correcting OPEN laws.

Copied continuation.v2 `ACCEPT-RECONSTRUCTABLE` and executed flags are historical claims. They were not treated as authority.

## Measured TS export

| Field | Value |
|---|---|
| Run | `run3:36658b14c908d10d051535c276b845f8ec04558167d915e163548aee69d75dd9` |
| Export | `runs/ts.store.json` |
| SHA-256 | `b868de2e3f95f3167b5638f2e73d6279d15ebae9b98eedc698053ff656dca789` |
| Size | 1465092 bytes |
| Objects / blobs / frames | 138 / 240 / 137 |
| Schema admission | pass (`admit_graph.admit_store`) |
| Public close_run | pass (native re-admission + independent evaluator3 replay) |
| Fresh-process replay | pass (`pilot_ts_fresh_replay.py` and `replay_export.py`) |
| Complete proof C | `8cd0293c6054ac40af21e4cff6d8f9c3497acbc8ee87b188a9dd961ddb816944` claimed = derived |
| Verdict | `fail` (file.exists gates on five inventoried file subjects) |
| H-frame identities | 67 checked, 0 mismatches; framed preimage retained under H, not C(X) |

## Original attached properties (still present)

- TypeScript sources (`src/index.ts`) and ts-tsconfig native context/universe
- `node_modules/left-pad` layout blobJoin (package pruned from snapshot inventory, bytes retained)
- Config graph: `tsconfig.json` extends `tsconfig.base.json` (duplicate edge retained); kind law `tsconfig` vs `other`
- Imported runtime `import2` payload
- ScopeDocumentV1 analysis-spec parameter (`include **/*`, `exclude node_modules/**`)
- File inventory totality: five snapshot paths, five `file@enumerated` facts, five independently derived `subject3`
- Clones L0-verbatim and L1-lexical with framed body identity

Default ts-tsconfig request still names all 11 non-NOT-SELECTED matrix ids. Candidate-only cells have complete-empty candidate envelopes and no fabricated Coverage. `imports@syntactic-specifier` remains RC-1 not-applicable (not the matrix imports relation).

## What continuation.v2 named vs what this checkpoint executed

Continuation.v2 `HC-V2-CLOSE-RUN-COMPLETE-REPLAY` described calling `admit_native_context`, `bind_universe`, and `compose_proof`. The bodies still:

- selected subjects from stored `subject3` (one path), not from retained inventories
- skipped clones `bodyIdentityJoin`
- treated h-identity as “object exists”, without parsing the H frame
- omitted expected inventories / cell outcomes for the 11 requested capabilities
- did not check U-4 or analysis-spec parameter cardinality at close_run

Those are helper omissions, not missing recipes. Corrections are in `pilot/helper-corrections-pilot-admission.json`. Historical continuation.v2 store: `pilot/continuation2-ts.store.json`. First-pass store remains `pilot/original-first-pass/ts.store.json`.

Independent replay now derives five file subjects from retained `SubjectInventoryV1` rows (`package-lock.json`, `package.json`, `src/index.ts`, `tsconfig.base.json`, `tsconfig.json`) and remints five findings. A supplied subject list is not the source of truth.

## Law map

`pilot-law-map.json`: 21 PASS, 0 FAIL, 0 OPEN, 3 INAPPLICABLE (count-at-most/all-covered/imported-atom; incoming-search; D9 host-invariant successor). Inapplicable rows are unexplained feature families this selected input does not use.

Byte retention is proven separately from structural admission: every H identity’s blob is the parsed frame; SHA-256(frame) equals the digest; C(X) equals the frame remainder; C(X) is also retained under SHA-256(C(X)) and is not the H object.

## Commands (reproducible)

```
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v1/output/pilot_ts_rebuild.py

/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v1/output/pilot_ts_fresh_replay.py

/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v1/output/replay_export.py \
  /tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v1/output/runs/ts.store.json
```

Fresh replay reloads exported bytes in a new process. It does not read `runs/ts.replay.json` as an oracle.

## What remains of the original charter

This checkpoint completes only the one-pilot-first prerequisite. Rust, rust-partial, syntax-code, syntax-data, graph-query, workflow/envelope/vector collections, and the rest of the original 123/8/3 are **not** executed by this TS-only work. Copied artifacts for those items remain historical. See `next-work.md`.
