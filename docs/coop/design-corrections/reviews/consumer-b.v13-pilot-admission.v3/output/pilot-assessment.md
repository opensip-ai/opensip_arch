# consumer-b.v13-pilot-admission.v3

**Verdict:** `PILOT-CHECKPOINT-COMPLETED`  
**reconstructionAccepted:** false  
**rootAdmission:** unobserved  
Whole-task `ACCEPT-RECONSTRUCTABLE` remains prohibited.

This turn closed the **condition-level** gap in the original all-applicable-CONDITIONS admission requirement. It is not a new product engine and does not qualify unselected capabilities.

## Retracted v2 keyword-only complete claims

Pilot-admission.v2 said it reconciled each KEYWORD to a checker, with 0 unmapped OPEN keywords. That is not what the original requirement establishes:

- One annotation can contain many independent mandatory table entries.
- Loading or printing an entire table as operands while a function hardcodes only some entries does not check the table.
- One negative in an annotation family does not establish every alternative in that annotation.

Original v2 evidence is kept. The keyword-only complete claim is retracted.

## Condition inventory and coverage

| Item | Count |
|---|---|
| Selected documents (graph + followed `$ref` / `record.document`) | 19 |
| Walked conditions (no container whitelist) | 4620 |
| Annotations / predicate-entries / metadata | 580 / 3907 / 133 |
| Required `(condition, instance, field)` | 1245 |
| Executed traces at comparison sites | 2530 |
| **coverage-difference.open** | **0** |

Deliverables: `condition-inventory.json`, `required-occurrences.json`, `executed-condition-trace.json`, `coverage-difference.json`.

Required occurrences are counted from kit tables × this TS graph (schema×instance walk plus published registry keys), not from handler case labels. Traces are emitted where operands are compared or rejoined. Conditional inapplicability records the evaluated condition and operands. Delegated checks emit entry-specific traces.

## Helper corrections (kit selectors)

Preserved first SCHEMA_REFUSED boundary: `inventory/v3-first-schema-refused-by-domain.json` — `DIGEST_RETENTION` on `finding3:107686d2…` `evidenceRefs[N]/digest: by-domain None unregistered`.

| Original failure | Kit selector | Correction |
|---|---|---|
| `by-domain None unregistered` | identity-schemas.v3.json `#/$defs/FindingEvidenceRef/properties/digest` and `#/$defs/Ref/properties/digest`; `x-opensip-digest-domains.byDomain` | Dispatch through sibling `Ref.domain`; refuse unregistered/missing domain; forbid terminal `by-domain` |
| `unhandled representation snapshot-path` | relation-payload-schemas.v2.json FilePayloadV1.path / PackagePayloadV1.manifestPath; digest-law `snapshot-inventoried` / `not-joined` | Join snapshot inventory; `not-joined` and vcs `deleted` are inapplicable with operands |
| Unknown representation returned success | identity-and-evidence closing digest law | Unknown owed variant refuses |
| Keyword-level map treated as execution | original all-applicable-CONDITIONS | Per-entry traces; required minus executed |

Also: `codec: uint64` byteLength vs retained blob length; config-node-kind-law basename table; `universeRule: same-only`; `closureKinds.byField` iterated including `import.producerClosure=provider`.

## TS pilot export (exact)

- Store SHA-256 `a2531c0ebd7e020a6167176e4dfc5400b41f0500718a920787cd2ab0d567eaa6`
- `run3:647e5eb239ef454c2df012403e55411075fc6535afa94b71b8f8917fcd756c1f`
- `plan2:f7ecea9f850bd4a3f02371f6253648bca4c83c4e9feab05bf2c4a3af43c7588a`
- `proof3:c20121a953d495b0d746e134ece3f4ba8fbf0e6c7ce53d625dbcca3db57c6e10`
- Proof C `4c63cd037bd9f8f406d30eecfa726f8d480da23ed04b7fddded804dd6a9f5a44`
- Claimed and derived verdict `fail`; 5 file subjects; 5 findings; 10 facts; 14 coverage; 1 executionDeficiency (`language-tier-unsupported` / `capability-missing` on json/config partition)
- `import.producerClosure` kind `provider`
- Original TS attached properties retained (node_modules, config graph, import, ScopeDocument, file-inventory, clones)
- Fresh-process replay from raw exported bytes: schema admit, close_run, identities, complete proof comparison — PASS (`pilot/ts-fresh-replay.json`)

Historical v2 identities (not this export): store `b62d7aed…`, run3 `9bb6c377…`, proof C `86c3c464…`.

## Negatives

Unit-boundary (not complete-Run) for each newly implemented applicable variant: `inventory/negatives-v3.json`, unexpectedPass none.

- `NEG-BY-DOMAIN-UNREGISTERED`, `NEG-BY-DOMAIN-MISSING-SIBLING`
- `NEG-SNAPSHOT-PATH-ABSENT`, `NEG-SNAPSHOT-PATH-NOT-JOINED-EXEMPT` (inapplicable, not inventoried)
- `NEG-UNHANDLED-REPRESENTATION`, `NEG-UINT64-LENGTH`
- `NEG-CONFIG-NODE-KIND` (`tsconfig.base.json` is `other`)
- `NEG-IMPORT-PRODUCER-KIND`, `NEG-UNIVERSE-RULE-SAME-ONLY`

A missing-record prerequisite refusal is not used as evidence for a later comparison. These isolated helper tests do **not** meet the original fully reminted semantic-negative requirement.

v2 family negatives remain in `inventory/negatives.json` (unexpectedPass 0) as historical family-level controls.

## What this does not do

- Does not ACCEPT the original 123/8/3.
- Does not observe root admission.
- Does not expand rust/syntax Runs, graph-query, or workflow collections.
- Does not claim D9 host-invariant successor or `F-*` as executed.
