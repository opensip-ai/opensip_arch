# J-BS compiled source-pin maintenance r1

Verdict: ACCEPT-DESIGN-UNIT. Implementation verdict: ACCEPT-UNIT.

Accepted J-BS design, materialization, and admission stay closed. This unit only repairs the compiled invocation5 pin that those units left behind. Product HEAD is `4c780ee4a41f09ddea8ebecd70e260f72e358fe3` and architecture HEAD is `aaafe4e10eb1008bf199994de4f64e02aa777837`. Both tracked trees are clean. Inventory v166 remains 614780 bytes, sha256 `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`, and is the last selected inventory successor. Both product paths are already inventoried, and those rows do not pin content. The OpenSIP support directory is absent.

## Two product files

`RegisteredSchemas::source_requirements` returns `SOURCE_PINS`. `from_sources` refuses the whole registry with `AdmissionError::SourceBytes` when any input length or raw SHA-256 differs from its pin. The host embedded loader calls that function on `include_bytes!` of the selected sources and is otherwise unchanged.

On the current product tree the invocation5 pin is still 71161 bytes, sha256 `28aa0c42b05fa3ad13ae4d9aed1bac17983453577306b8e15678dc74af63f4fb`. The accepted source `schemas/sources/invocation-v5.schema.json` is 71837 bytes, sha256 `63f97dfcb77d3065c4a5f4af3194fbe0e874cc89a8b9e2533728da2a4af28ec0`. Loading those exact bytes through the current table necessarily refuses before schema admission.

The candidate changes that one block in `crates/identity/src/schema_registry.rs` (26808 / `ea3cc09ed006e652bdde32849a3855d2e471ed0ad7c8968e79fe3c0d06027f10` to 26815 / `a6e34a2fd26e8db5cdb639bdd8921067683fe79653345895f868949cd617cad3`). Schema id and path stay `urn:opensip:product-v1:workflows:evaluator3:invocation:5` and `schemas/sources/invocation-v5.schema.json`. The other 47 pins, the 15 aliases, and every byte outside that block stay equal. The resulting 48-row table equals `schemas/admission-registry.json`, and each row matches the candidate source file.

`tools/identity/dependency-policy.json` stays 56471 bytes and changes only `localSources` for `src/schema_registry.rs`, from the old Rust pin to 26815 / `a6e34a2fd26e8db5cdb639bdd8921067683fe79653345895f868949cd617cad3`. Dependency profiles, features, source censuses, and the other local pins are unchanged. Across 967 tracked product files, the candidate differs only in these two.

No schema, generated output, JSON admission registry, or admission source map changes. `crates/host/src/schema_sources.rs`, `tools/contracts/generator-closure.json`, and `tools/verify_design.py` keep their accepted pins.

## Contract successor

Subject manifest sha256 `b5f25de57ee6793a690fdb4e3f435579cda77d82a83e65387f71d8b537e7e5f1` (3183 bytes). All 14 members match. Successor `docs/implementation/m3/host-pipeline-j/j-bs-runtime-pins-r1/successor.json` is 3821 bytes, sha256 `0643e33d103705a3bbcd4c5f10b755cdd3108acd962f1011c38cc8e7f6148817`. `passageOverrides` is empty and there is no passage supersession. The candidates are the other 13 subject members.

The three parents are already accepted, and the architecture bytes match:

| Parent | Bytes | SHA-256 |
|---|---:|---|
| `docs/implementation/m3/host-pipeline-j/j-bs-admission-r1/schemas/admission-registry.json` | 17170 | `a4a02c4271245c7a0c3a401fea95dc93f1849004bee41c4c7b1a433e5ed19c30` |
| `docs/implementation/m3/host-pipeline-j/j-bs-r1/schemas/invocation-v5.schema.json` | 71837 | `63f97dfcb77d3065c4a5f4af3194fbe0e874cc89a8b9e2533728da2a4af28ec0` |
| `docs/implementation/m3/preview-pack-i1/i1-a/product/tools/identity/dependency-policy.json` | 56471 | `03deeac68b6da580180dd7794ae94a150fb54ad2227b1d1f6b51defa27b90f0c` |

The invocation parent equals the product schema. The policy parent equals the product policy before this edit.

## Evidence

The read-only checker was run as named. Its stdout matches `evidence/checks.json`, 369 bytes, sha256 `2737a75128ff4153c1629afa194a56eb2bd1b5d3be7f21b466844e593c8fa858`: 48 compiled sources, 47 unchanged pins, 15 unchanged aliases, and only the invocation pin and the one local-source policy pin changed. It writes nothing and does not claim consumer admission or qualification.

Supplied candidate logs, not re-executed here: host registry tests 7 passed and 180 filtered; identity library tests 57 passed; Rust provider library tests 108 passed. The identity dependency closure names eight registry tuples, all present in `Cargo.lock`, with `passed` true, `sourceFilesVerified` 305, and `productQualification` false. The identity and Rust provider Clippy logs finish with no warning lines. These are current registry load and the existing scoped controls. They are not a producer, native-admission, or product-qualification claim.

No required findings. Exact reviewed bytes follow assent. Product code and the design-lock bind stay separate commits, with no push.
