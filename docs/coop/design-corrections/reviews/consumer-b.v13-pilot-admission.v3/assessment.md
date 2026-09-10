This is a condition-level completeness pass, not another keyword map. I’ll copy v2, rebase helpers, then inventory every table entry and bind it to actual TS instance fields.Copy is in place and helpers are rebased. Next I’ll explode nested tables into individual conditions and bind them to the TS graph’s actual instance fields.Binding was too broad (every deficiency row against every Coverage). I’ll dispatch by sibling values and treat scalar join fields as operands, not separate required occurrences.Unknown digest representations were previously ignored; `snapshot-path` and `by-domain` now refuse. I’ll implement those variants from the kit instead of treating silence as a pass.I'll continue the condition-level admission work from the live digest-law gap: implement `by-domain` and `snapshot-path`, then re-trace required versus executed occurrences.I'll inspect the digest-law helpers, current coverage gap, and the first SCHEMA_REFUSED boundary so the next checks match the kit.The digest walker and required-occurrence binding still look incomplete; I'll read the rest of `_require_digest` and the kit digest-law next.The digest walker still drops sibling `domain` and `snapshot-path`; I'll pull those kit selectors and the current helper paths next.I’ll capture the current SCHEMA_REFUSED boundary first, then implement sibling `by-domain` and `snapshot-path` so traces match kit pointers.First SCHEMA_REFUSED boundary is preserved. Next I’ll implement sibling `by-domain` lookup and `snapshot-path` inventory joins in the digest walker.I’ll add a schema-site walker, then wire digest dispatch so `by-domain` uses the sibling `domain` and `snapshot-path` joins inventory.I’ll add per-entry traces in the law checkers, then rebuild the required-occurrence binder from the schema walk.Admit and close now pass. I’ll rebuild the TypeScript graph, regenerate the condition inventory, and run coverage traces.Instance IDs on nested records don’t match the traces. I’ll align extra admission paths with the actual object identities.Coverage difference is empty. Next I’ll add per-entry negatives, run a fresh replay, and write the assessment.**PILOT-CHECKPOINT-COMPLETED.** `reconstructionAccepted` is false. `rootAdmission` is unobserved. Whole-task acceptance remains prohibited.

The v2 claim that each keyword was reconciled to a checker is retracted. That is not the original all-applicable-conditions requirement: one annotation can contain many independent table entries, and a family row with 0 errors is not an execution trace. Original v2 evidence is kept.

## Condition-level coverage

| Item | Result |
|---|---|
| Selected documents | 19 |
| Walked conditions (no container whitelist) | 4620 |
| Required `(condition, instance, field)` | 1245 |
| Executed comparison-site traces | 2530 |
| **coverage-difference.open** | **0** |

Deliverables: `condition-inventory.json`, `required-occurrences.json`, `executed-condition-trace.json`, `coverage-difference.json`, revised `pilot-law-map.json`.

## Kit fixes (first failure preserved)

First SCHEMA_REFUSED is in `inventory/v3-first-schema-refused-by-domain.json`: `DIGEST_RETENTION` on `finding3:107686d2…` `evidenceRefs[N]/digest: by-domain None unregistered`.

- **by-domain** now reads the sibling `Ref.domain`, looks up `x-opensip-digest-domains.byDomain`, and dispatches the terminal representation. Missing/unregistered domain refuses.
- **snapshot-path** joins snapshot inventory when retention is `snapshot-inventoried`. `not-joined` and vcs `deleted` are inapplicable with operands. Unknown representations refuse.

## TS export and fresh replay

- Store SHA-256 `a2531c0ebd7e020a6167176e4dfc5400b41f0500718a920787cd2ab0d567eaa6`
- `run3:647e5eb239ef454c2df012403e55411075fc6535afa94b71b8f8917fcd756c1f`
- Proof C `4c63cd037bd9f8f406d30eecfa726f8d480da23ed04b7fddded804dd6a9f5a44`
- Claimed and derived verdict `fail`; 5 file subjects / 5 findings; 1 executionDeficiency
- Fresh-process replay from raw export bytes: admit, close, identities, complete proof comparison — pass
- Original TS attached properties retained (node_modules, config graph, import, ScopeDocument, file-inventory, clones)
- `import.producerClosure` kind is `provider`

## Negatives

Unit-boundary controls for each newly implemented variant are in `inventory/negatives-v3.json` (unexpectedPass none): unregistered/missing by-domain, snapshot-path absent, not-joined exemption, unhandled representation, uint64 length, config-node-kind, import.producerClosure kind, universeRule same-only.

Those isolated helper tests do **not** meet the original fully reminted semantic-negative requirement. v2 family negatives remain as historical evidence.

Original 123/8/3 is still required later. Next work is in `next-work.md`.
