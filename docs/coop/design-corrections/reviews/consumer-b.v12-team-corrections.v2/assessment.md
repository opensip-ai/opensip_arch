I’ll continue in the v2 team-corrections copy: verify kit and team-input hashes, read both scope-review successor and self-audit, then replace the remaining placeholder vectors without touching the frozen syntax-code pilot.Hashes match. Next I’ll extract the 134-row dispositions and original requirement verbs, then inspect the placeholder vectors.I’ll pull original requirement verbs and owning schemas next, then preserve historical vectors before any reconstruction.I’ll extend schema admission and add a reconstruction script that builds real owning-schema records and executes the refusals.I’ll write the reconstruction script next: real owning-schema records, computed identities, and executed refusals.**Verdict: `SCOPE_INCOMPLETE`** — not whole-consumer acceptance, and historical `ACCEPT-RECONSTRUCTABLE` is not reaffirmed. The syntax-code pilot validator’s outcome was not used.

Kit and all four scope-review files hashed to the expected values (80/80 kit files). Copied scripts were path-corrected into this v2 output only. Historical placeholders are under `preserved-failures/scope-placeholders-original/`.

## Frozen Run stores (unchanged)

| Store | SHA-256 |
|---|---|
| syntax-code (v1 pilot) | `2e74a6b2dd2b94152d6c4ce266dbe1bc4b23dc257b0fea12a6c947d36fe08fe7` |
| ts | `885b8e4575235fe47fbee893d83e97d650aea230f9af870b8a711f25d943075d` |
| rust | `67dc12f88fc19fb320385d30f6a740197c64ca9d574627b8db81cdb2f2000315` |
| syntax-data | `1d07e4c8040035965a8821559a5916cf82014e19198e1e6acaf6e9b5ecdd6092` |
| rust-partial-clones | `b6c2b240e11fff9699aeeacdd8a68a7ee7119f241029e3de0e4c955e2b058246` |

## What this pass actually reconstructed

48 IDs now inhabit their **owning** records (not CommandEnvelope-for-everything): failure envelopes, InvocationRecord single/multi-step, inventory disclosure, StepTermination, D9 `classToExitCode` equality, receipts bound to the syntax-code Run, three TypeScriptConfigGraphV1 shapes with `SHA-256(C(graph))` (hash is not a graph field), ComparisonResult/BaselineArtifact cases, repair/mutation records with a computed apply-key inequality, min-resolution atom values, clone/JS/hidden-mismatch refusals, an independently recomputed ownership-stable L0 pair, and typed `graph.neighbors|path|reach` plus cursor, failure envelope, and unprojectable-fact disclosure.

Graph queries over the TS store are labeled **`underlyingRunAdmissionUnverified`**. That is graph-algorithm behavior, not `close_run`.

Command:

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v2/output/scripts/scope_reconstruct.py
```

Measured: exit 0; 48 reconstructed IDs; 0 stock-schema failures on those records.

## Why incomplete

**`R-REPLAY-EXPORT`** is still missing for ts/rust/syntax-data/rust-partial (stores frozen; other-Run rebuild is a later pass). Independent closure/replay/root admission of those Runs is not claimed. Rust-partial cell state was not rewritten; law still derives **`partial`**. All 123 original accept-blocking IDs remain in force.

134-ID mapping: `output/scope-correction-review.json` (and `.md`).
