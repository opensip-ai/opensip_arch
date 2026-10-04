# I1-P — the `opensip.preview.typescript.pack:1` pack contract (contract successor)

2026-10-04. Claude Opus 5.5, implementation lead. Status: **PROPOSED frozen candidate.** It needs CODEX2's `ACCEPT-DESIGN-UNIT` and root assent before selection, and I1-L must be selected first.

I1-P executes item 5 of the accepted law M3-I1 r2: `../PROPOSAL-r2.md`, 52522 B, `1eb47d1e…`. This is X12c's pack contract (X12:191). It fixes four things:
- the exact bytes of the bundled document (5.2);
- its registry row (5.4) and the whole registry file;
- the digests of 5.3, recomputed with the design encoder;
- the self-checks S1 to S10 that unit I1-c implements.

Base: product main `3e64266`. It changes no product file; I1-c copies its two data files.

## The pack

| | Value |
|---|---|
| packId | `opensip.preview.typescript.pack:1` (name `opensip.preview.typescript.pack`, version 1; byte-exact, X12:47-59) |
| Document | `product/crates/evaluator/src/preview-typescript-pack.v1.policy.json`, 574 B, `96675a5e…`, no trailing newline, its own canonical bytes |
| Rule | `module-import-cycle`, `gate: true`, `severity: error`, `emitWhen` = `{"filters":[],"minResolution":"resolved-target","op":"cycle-representative","relation":"imports"}`, subjects `file` in `typescript` |
| Contribution | `opensip.preview.typescript`; `ruleStableId` `module-import-cycle`, `semanticsMajor` 1 |

The document's bytes are taken from the law's 5.2 block by `evidence/build_i1p.py`. They are not retyped.

## Digests (5.3), recomputed

The design encoder is `docs/coop/design-corrections/foundation/canonical.py` (6465 B, `d47f25db…`), the C(X) that identity-and-evidence §3 names (IE:134). The exact-schema profile's `exact-schema-profile-selection-v1/reference/canonical.py` (8995 B, `ad88e58f…`) recomputes every value as a cross-check, and the two agree byte for byte.

| Value | Recipe | Recomputed | Law 5.3 |
|---|---|---|---|
| `programDigest` | raw SHA-256 of C(`emitWhen`) | `8e8936af513ae93eeb8227fb991330b523761930d85d077b044f4312706a57de` | equal |
| `policySha256` | raw SHA-256 of C(document) = SHA-256 of the file (574 B) | `96675a5e20fcfd8ba6501f20b9017aa205e300b9f1984d7e74ad534996acdcd1` | equal |
| `ruleProgramDigest` | raw SHA-256 of C(RuleProgramV2) (457 B; COMP:103, `policy.rs:584-606`) | `e796f81764d0ee452c591c852e98f59647518a1894d4bd0fd5c70b674ecc3ecb` | equal |

So no mismatch blocks acceptance. The compiled RuleProgramV2's canonical text is recorded in `evidence/digests.json`. It is `{schemaVersion: 2, policyDigest, rules: [{ruleId, ruleProgramRef, emitWhen}]}`, the shape `compile_program` builds.

## Registry (5.4)

The row is 5.4's exactly. Its key set is the one `policy.rs:953-965` enforces, and its `contributions` equal the document's `contributionId` set. `product/crates/evaluator/src/pack-registry.json` (I1-c's new registry file) holds that row and this `standing`, which names this law and states "one row":

> Bundled first-party policy packs compiled into the signed core (law X12 r3 items 2 to 4). Admission is by exact packId against these rows only. One row (law M3-I1 r2 item 5, contract successor I1-P): opensip.preview.typescript.pack:1, the DR-131 preview pack.

The file keeps the base file's form: two-space indentation, key order `schemaVersion`, `standing`, `rows`, and a trailing newline. `materialization-map.json` records two files:
- the registry: 305 B, `crates/evaluator/src/pack-registry.json` at `3e64266` → the new file;
- the document, which is new (`before: null`).

## Schema admission (evidence)

`evidence/build_i1p.py` validates with the exact-schema profile (`ExactValidator` over `exact_registry`), using common v1 as `urn:opensip:product-v1:workflows:common`:

| Schema | `PolicyDocumentV2` | `RuleProgramV2` |
|---|---|---|
| I1-L's design PDS copy | admitted | admitted |
| I1-L's product PDS copy (I1-a's `schemas/sources/policy-v2.schema.json`) | admitted | admitted |
| PDS and PPDS, the parents | refused at `emitWhen` | refused |

It also checks:
- **Meta-schema.** All four of I1-L's copies are valid Draft 2020-12 schemas.
- **Op law.** I1-L's model's 2.2 admits the rule.

This covers X12 item 6's steps 6.1 (lexical, by the design encoder's `parse`), 6.3 (schema), 6.5 (digest) and 6.7 (the compiled program's schema), plus the op law of 6.6, all in the reference. The product's imperative classifier (6.2) and its rule law run in I1-c's S3.

## Self-checks (5.6), for I1-c

`pack-contract.json` lists S1 to S10 with the law's wording. S5's values are this record's: `identity.packId` and `digests.*.value`.

At `3e64266`, S6's pins hold as the law states:
- `policy_pack_tests.rs:638` asserts 7 `include_bytes!(`;
- `&RELEASE_PACKS` appears twice in `policy.rs`.

S10's expectations are I1-L's oracle: `../i1-l/evidence/cases-report.json`, cases `corpus-*`. I1-b2's fixtures must reproduce them.

## Parents and binding

There are three parents, all accepted once I1-L is bound:
- the law snapshot `PROPOSAL-r2.md`, an I1-L candidate;
- I1-L's design PDS copy;
- I1-L's product PDS copy.

So the lock must bind I1-L before I1-P, which is the I1-L → I1-P edge. The build's checks treat I1-L's subject members as accepted for that reason. I1-P has no passage overrides.

After acceptance, the lead appends I1-P's `contractSuccessors` entry after I1-L's in a binding-only product commit. Selecting it changes no product byte.

## Lead decisions

| ID | Decision | Rejected |
|---|---|---|
| LD-P1 | I1-P fixes the whole `pack-registry.json`, including `standing`, so I1-c is a mechanical copy. | Naming only the row, which leaves the standing text as unreviewed design text inside a code unit. |
| LD-P2 | Product data files are candidates under `product/` with a materialization map (F8b's form). The pack contract is its own record, `pack-contract.json`. | Extra keys in `successor.json`, whose role `verify_design` fixes. |
| LD-P3 | IE:134's `foundation/canonical.py` is the design encoder. The exact-profile encoder is the cross-check and the validator. Both run read-only, against a scratch dependency directory built offline from the pinned wheels. | A hand-written C(), which is not "the design encoder". |
| LD-P4 | The parents are the law and I1-L's PDS copies, so the binding order carries the I1-L → I1-P edge. | PAC or AQC as parents: neither is changed or superseded. |
| LD-P5 | S10's oracle is I1-L's model. | A separate S10 fixture set at I1-P, which would be a second oracle. |

## Cross-law notes

- **None in the pack bytes.** All three provisional digests recompute exactly, and the row, the document and the contribution set agree.
- **I1-c's job shrinks.** UNITS r2 says I1-c ships "the `pack-registry.json` row and standing". Under LD-P1, I1-P fixes those bytes and I1-c copies them.
- **Schema admission depends on I1-L.** The document is admissible only under I1-L's copies (PDS and PPDS refuse it). So I1-c's S3 passes only after I1-a has materialized I1-L's product copy. That is UNITS's I1-a → I1-b1 → I1-c order.

## Checks run

All runs were at `nice -n 19` with `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B`. `--deps` names a scratch directory holding jsonschema 4.25.1 and its four dependencies, installed with `pip install --no-index --find-links ~/opensip-deps/wheels --target <dir> jsonschema==4.25.1`. No cargo, product tool or test was run.
- `evidence/build_i1p.py --product <opensip> --deps <dir>` writes the record. `--check` compares instead, and two runs were byte-identical.
- Its checks restate `verify_design`'s `contract_successor` rules for this record:
  - every parent is accepted at its pinned bytes, counting I1-L's members;
  - the candidates equal the subject minus the record;
  - no candidate path is already accepted.
