# Blind review — consumer-b.v13 continuation.v2

**Verdict:** `ACCEPT-RECONSTRUCTABLE`

- Origin: `consumer-b.v13` (same fresh blind origin; not a new subject)
- Continuation: `consumer-b.v13-continuation.v2` after read-completion.v1
- Kit manifest: `afa3abfbb3dd26e10026058d433fc1871505fbd9d1c928f79e881d514e5cc40d`
- Parent subject: `fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`
- Root admission: **unobserved**
- Reading of the six original contracts: completed in read-completion.v1 and verified by root

## Measured complete positives

All five claimed complete Runs were independently schema-admitted (including published keywords and selected `$ref`s), closed (native re-admission + inventory totality + complete evaluator3 replay), and fresh-process replayed from export:

| Run | fresh ok |
|---|---|
| ts | True |
| rust | True |
| rust-partial | True |
| syntax-code | True |
| syntax-data | True |

From-scratch command:

```
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v13-continuation.v2/output/fresh_replay_all.py
```

## Graph query

- Schema `$id` `urn:opensip:product-v1:workflows:evaluator3:graph-query:3` major 3
- Operation over admitted `run3:e1818b84f065bbe004a0a6d6ebf1be1fed8ec07806f79b45f5e9f54fb5e8809d`
- Projectable rung `imports@resolved-target`
- `imports@syntactic-specifier` refused `QUERY.RELATION_UNSUPPORTED`
- Occupancy from retained TargetAttributionV2
- Neighbor order: utf-8 endpoint tuple then fact2 id
- `resolvedView` is `{runId}` only; `advisory` false

## False-result remint

Structural owning-schema admission passed. Public `close_run` complete replay refused the reminted claimed verdict (`replayRejectedAlteredResult=True`).

## Corrections this turn (helpers, kit-only)

See `pilot/helper-corrections-v2.json`. Original first-pass stores remain under `pilot/original-first-pass/`. Continuation.v1 artifacts remain untouched.

## Scope

Original 123 required items + 8 standing rules + 3 F-* future-qualification items. Copied v1 `executed` flags were not authority. Status now points at v2 measured artifacts for Runs/query/replay/invocation, and retained prior-origin vectors for standalone items that were not regenerated.

Unexecuted blocking IDs: `[]`

## Gaps

- `G-D9-HOST-INVARIANT-SUCCESSOR` is a disclosed owed D9 successor, not a reconstruction recipe and not a MUST for this reconstruction.
- Real OS/compiler/crypto/SQLite remain `F-OS-COMPILER-CRYPTO-SQLITE`.
- Synthetic TCB observations remain assumptions.

## Qualification

No product qualification or implementation authorization is claimed. An internal `ACCEPT-RECONSTRUCTABLE` never grants root acceptance.
