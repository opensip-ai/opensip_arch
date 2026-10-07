# G2 declared native import observation preimage r1

ACCEPT-DESIGN-UNIT. implementationVerdict ACCEPT-UNIT. requiredFindings empty.

Subject manifest `docs/implementation/m3/native-g/g2-import-observation-r1-subject.json` is 3077 bytes, sha256 `a5adc6a6eeadf1eeb2bac0651394f55c8a7db9b135cb07b288b78194bddeee44`. All 14 members match the stage bytes. Their paths are sorted and unique, and `successor.json` appears once. Successor `docs/implementation/m3/native-g/g2-import-observation-r1/successor.json` is 3418 bytes, sha256 `905e21e9a87549e775617f77b501c5bf702526bc54be3a677e1cc8ba6efb3b04`. Keys are `schemaVersion`, `standing`, `parents`, `passageOverrides`, and `candidates`. `passageOverrides` is `[]`. The record has no `passageSupersessions` key, so this review omits `supersededPassages`. Standing: "PROPOSED G2 declared native import observation canonical raw preimage only; no wrapper/importer/worker authority".

`candidates` is the other 13 subject members. The record path is absent. Each candidate pin equals its subject pin, and the candidate paths are sorted and unique.

Product HEAD `ba7a20556133616668bc23299e98d608918ec689` and architecture HEAD `acdf6167ec5801d3511b8baa7876162131552f07` are the pinned bases. Product is tracked-clean (967 files). Architecture is tracked-clean. Its untracked drafts stay outside this unit. `~/Library/Application Support/OpenSIP` is absent. Against that product tree, the candidate differs in exactly the two Rust files below. Stage copies match the candidate bytes, and those bytes match `productAfter`. The same paths at the product base match `productBefore`. `design-lock.json` does not yet contain this successor. The candidate lock matches that accepted lock; the source delta is the new constructor.

## Parents and authority

Two parents. The C r7 law is separate authority.

- Admitted imported schema `docs/implementation/m1/source-selection-v2/schemas/sources/imported.v1.schema.json` is 46315 / `edce21a3c7905f215c019eddc5776e08e6cff59a6ceea4b4e422275ead594b9e`. That pin is a candidate of bound successor `docs/implementation/m1/source-selection-v3/successor.json` (35266 / `e638c55c3e0c807fe4540c5c0ea2e462886fc25ef5e2ee7df55efe28d3784ae4`). The architecture file matches the pin. This unit's members leave that path in place.
- Admitted NE `docs/v2/contracts/product-v1/native-evidence.md` is 329013 / `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`, a design-lock input whose bytes match architecture HEAD. NE:2697-2708 makes every auxiliary digest the raw SHA-256 of the canonical bytes of an exact closed record retained as a blob. `observationDigest` is canonical `ImportObservationV1 {schemaVersion:1, kind, window|null, population|null, selection|null, revisionRange|null}`.

C r7 stays separately pinned. `PROPOSAL-r7.md` is 157110 / `a1ee9386da5913c135932891f6f8041cc72834b9bd531b1e6a51ccfccc1d40c6`. Its review is 6476 / `a2af42ba44ca696f1f7d497f54f89f115fdda0a942d25ef9f6ced101bd116329`, verdict ACCEPT, requiredFindings empty, and `subjectSha256` equals the law file. Item 13 names this six-field preimage and the raw `observationDigest`. Wrapper kind equality, payload, source correspondence, scope and build digests, completeness, producer and adapter closures, the identity join, `plan.importIds`, and `acquisitionSourcePath` stay with the host and NIJ-1. There is no passage override.

Inventory v166 remains 614780 / `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`. `prepared_inputs.rs` stays role `validator`. `prepared_inputs_tests.rs` stays role `test`. Neither row pins content.

## Constructor

`prepared_inputs.rs` inserts 2415 bytes at offset 18667 and deletes none. The accepted file is that prefix, this constructor, and the unchanged helper suffix. `inert_media` and `retain_blob` follow the insertion.

`DeclaredNativeImportKind` is `Dependency` or `Prepared`. `DeclaredNativeImportObservation` stores that kind, the canonical bytes, and the raw digest. The getters are `kind`, `canonical_bytes`, and `raw_sha256`. `declared_native_import_observation` takes only the kind and returns `Result<_, CanonicalError>`.

The object is `schemaVersion` 1, `kind` `dependency` or `prepared`, and `window`, `population`, `selection`, and `revisionRange` null. It is built as a `BTreeMap`. `canonical_bytes` is the shared encoder: compact JSON, lexical UTF-8 key order, and a colon with no space. `raw_sha256` is SHA-256 of those bytes. The function leaves the H-domain frame helper and ImportId unused.

Independent compact sorted JSON matches both goldens. Dependency is 109 bytes, raw SHA-256 `21d3cbc90760ce533d62c6a9ed54495efb8388f84ffef5c263b989bdf6234669`. Prepared is 107 bytes, raw SHA-256 `ba44387f9885bc20c9c3c23679b7f28b8bef5c7e33e28fcfa57b79c430ef8aac`.

`ImportObservationV1` in the admitted schema is an object with `additionalProperties` false and those six required members. `schemaVersion` is const 1. `kind` is an `ImportKind`, whose list is `runtime`, `test`, `history`, `dependency`, and `prepared`. The constructor enum is the two native-input kinds. Each of the four observation members allows an object or null; this constructor emits null.

Wrapper-kind equality, retention, custody, source correspondence, scope and build digests, core closures, native context, import, and the Plan/Run join remain with the host. NIJ-1, C, L, and the owner gates remain in force. `CanonicalError` remains the serializer error.

## Controls

`evidence/checks.py`, `evidence/author.py`, `evidence/freeze.py`, and `evidence/tests.py` were not run. The supplied logs and pinned receipts were read.

`prepared_inputs_tests.rs` keeps the 45714-byte product base as a prefix and appends 3564 bytes. The file's `#[test]` count goes from 36 to 39: `native_import_observation_dependency_has_exact_six_member_golden_raw_preimage`, `native_import_observation_prepared_has_exact_six_member_golden_raw_preimage`, and `native_import_observation_current_schema_requires_each_member_and_closed_kind`.

The golden tests compare the canonical bytes and `digest_hex` of `raw_sha256` with the two pinned strings. The schema test loads `RegisteredSchemas` through `source_requirements()`. The imported-evidence pin is `schemas/sources/imported-v1.schema.json`, 46315 bytes, sha256 `edce21a3c7905f215c019eddc5776e08e6cff59a6ceea4b4e422275ead594b9e`, and the product file equals the architecture parent. The logical document `workflows/schemas/imported-evidence.schema.json` maps to `urn:opensip:product-v1:workflows:imported-evidence`. For both kinds, `check_current_value_shape` accepts the constructor value at `#/$defs/ImportObservationV1`. Removing each of the six members fails. An extra `observation` null fails. Replacing `kind` with null or `unknown-kind` fails.

`unit-tests.log` is `cargo test --locked --offline --manifest-path providers/rust/Cargo.toml --lib`: 187 passed, 0 failed, 0 ignored, 0 filtered out. The three new tests are `ok`. `clippy.log` is the same package with `-- -D warnings`: zero `warning:` lines, zero `error:` lines, `Finished`. `format.log` is empty. `checks.json` records qualification false. This review does not select qualification.

After this dual acceptance and root assent, `verify_design` runs on the current main lock, the two Rust files land in one code commit, and this bind lands in a separate lock commit. Nothing is pushed. The record leaves NIJ-1, C3, and product qualification where they stand.
