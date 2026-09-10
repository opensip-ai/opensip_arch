# Blind review — `consumer-b.v13` / continuation `consumer-b.v13-continuation.v1`

Same-origin continuation of consumer-b.v13. Not a new independent session and not an acceptance reset.
Kit/parent hashes unchanged.

- Parent subject SHA-256: `fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`
- Manifest SHA-256: `afa3abfbb3dd26e10026058d433fc1871505fbd9d1c928f79e881d514e5cc40d`
- Write directory: `/tmp/opensip-design-corrections/consumer-b.v13-continuation.v1/output`
- Original output (unchanged): `/tmp/opensip-design-corrections/consumer-b.v13/output`

## Verdict

**ACCEPT-RECONSTRUCTABLE**

First-pass ACCEPT-RECONSTRUCTABLE is withdrawn. The original advisory approximating
`SelectedEnumeratorRef` as `{closureId}` and deferring owning-schema admission to root
violated the charter (no ACCEPT with unresolved helper approximations or unexecuted
required validation).

Continuation executed the required pilot discipline on the TypeScript Run, then the
remaining required Runs:

1. Owning-schema admission including selected `$ref`s and published `x-opensip-order` /
   `x-opensip-digest` nested canonical-record laws.
2. Retained digest/representation/closure and cross-record registry joins.
3. Exported-byte reload in a fresh process.
4. Independent complete proof derivation from retained program/evidence and comparison
   of every proof field.

Root admission of those exact exported frames remains **unobserved**.

## Helper corrections (original failure preserved)

See `pilot/helper-corrections.json` and `pilot/ts-original-admission-failure.json`.
Original first-pass stores are under `pilot/original-first-pass/`.

1. `configGraphPaths` UTF-8 order (`tsconfig.base.json` before `tsconfig.json`).
2. WaiverSet `schemaFamily` = `opensip.product.waivers`.
3. `ImportsPayloadV1.importer` SubjectIdV1 (`symbol:src/index.ts::x`).
4. `SelectedEnumeratorRef` = `{status: selected, closureId}`.

Additional construction/admission fixes found while executing the same laws:
languageFamily `tsjs`; program-predicate/node fragment retention; Rust ownership
`(path, unitId)` order; syntax suffixes UTF-8 order; declares SubjectIdV1 fields.

## Measured Runs

| Run | Admit | Close | Fresh replay complete-proof equal |
|---|---|---|---|
| ts | yes | yes | yes |
| rust | yes | yes | yes |
| rust-partial | yes | yes | yes (indeterminate) |
| syntax-code | yes | yes | yes |
| syntax-data | yes | yes | yes |

Fully reminted false-result graph: structural identities/joins admitted;
recomputed complete proof rejected the altered claimed verdict
(`vectors/false-result-remint.json`).

Negatives were invoked on the admission/evaluation path
(`vectors/negatives-invoked.json`); observed refusals retained.

Graph query neighbors/path/reach/cursor/history/limit/parity reconstructed over the
admitted TS Run (`query/graph-query.json`).

## From-scratch replay

```
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v13-continuation.v1/output/replay_export.py /tmp/opensip-design-corrections/consumer-b.v13-continuation.v1/output/runs/ts.store.json
```

## Counts

- executed: 131
- unexecuted: 0
- failed: 0
- futureQualification: 3
- blocking unexecuted/failed: none

No real compiler/OS/cryptographic/SQLite product qualification is claimed.
