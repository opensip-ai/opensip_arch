# G2 declared system-input bytes and order r1

Verdict: ACCEPT-DESIGN-UNIT. Implementation verdict: ACCEPT-UNIT.

This appends `check_declared_system_inputs` to the existing compiler-tools module and nine controls to its existing test file. `check_declared_tools`, its helpers, and the previous test bytes stay identical. Product HEAD is `aa9d885657a7ba53b59ae1037f2b8e3054dc9368` and architecture HEAD is `a4ab565228697c2f9b9b3009fbbfe03f9a7c724a`. Both tracked trees are clean. Inventory v166 remains 614780 bytes, sha256 `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`, and is the last selected inventory successor. Both paths are already inventoried, and those rows do not pin content. The OpenSIP support directory is absent.

## Law and parents

Subject manifest sha256 `63ae8efa1aa84fec84ff383f26c901dd7e98e87128095eb6b0fb6e10867e632e` (2179 bytes). All ten members match. Successor `docs/implementation/m3/native-g/g2-system-inputs-r1/successor.json` is 2789 bytes, sha256 `c7fc94c91ec832eb09f359ae1c881b65b32088265420d26d927ecec485505c76`. `passageOverrides` is empty and there is no passage supersession. The candidates are the other nine subject members.

The three parents are already accepted, and the architecture bytes match:

| Parent | Bytes | SHA-256 |
|---|---:|---|
| `docs/implementation/m1/source-selection-v2/schemas/sources/native.v2.schema.json` | 280357 | `e5834d37aebd96d77d352975878da349033f8633ecbd83322ad0fbea461f7773` |
| `docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.v2.py` | 319894 | `4f800faaf75c36ffd38fa9ae0f3618bee1bedbe586026e280326b0d7d73ebca8` |
| `docs/v2/contracts/product-v1/native-evidence.md` | 329013 | `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0` |

`ToolchainIdentityV1.sysrootDigest` is `x-opensip-digest` representation `raw-artifact`: the raw SHA-256 of the admitted sysroot tree manifest bytes, retention `preimage`. `rustcDevLlvmDigest` remains the `h-identity` closure suffix. `standardLibraryComponentDigests` allows `minItems` 0 and `maxItems` 64, with `uniqueItems` and `x-opensip-order` `sequence`. The Rust branch of `admit_native_context` requires those component names to be strictly unique in ascending raw UTF-8 byte order and leaves the rows unrewritten. The product native schema equals that parent. Compiled source-pin maintenance is already bound: design-lock contract successor `j-bs-runtime-pins-r1/successor.json` is 3821 bytes, sha256 `0643e33d103705a3bbcd4c5f10b755cdd3108acd962f1011c38cc8e7f6148817`, and both the product and the candidate carry `schema_registry.rs` at 26815 / `a6e34a2fd26e8db5cdb639bdd8921067683fe79653345895f868949cd617cad3` with invocation5 at 71837 / `63f97dfc`.

## Two product files

`providers/rust/src/compiler_tools.rs` moves from 7010 / `a90064d9259ca53d46966502be71ace8f3af39d5d478854d46b0d73d4520e245` to 10232 / `b09afe2a372b4071feb7e2b290fd7691483543b54164fda3f67b12e27bea1195`. `providers/rust/src/compiler_tools_tests.rs` moves from 13901 / `f6b699b888474223baf869fa6c5027fcb5434e479f90659396c6d2f4d4d884f2` to 19998 / `7b1a977177314e9d7b330973211fbc94f5cface752236a954700b4f7818754c3`. The stage copies match the candidate. `lib.rs` stays 898 / `63f08ffbb47ea594072b8c48907a8225985c1451a0b5035a7c92c4ca6a29f63c`. No dependency-policy row names these files.

`check_declared_system_inputs` calls `check_declared_tools` first, so the current full Rust context frame, declared tool and dev-closure joins, selected-tool membership, version, target, and expected host digest are required before any system-input diagnostic. `frame_candidate` admits that frame against the current schema, which is where shape and the 64-component ceiling refuse. Claimant component order is then compared in place: a name whose raw UTF-8 bytes are less than or equal to the previous name returns `ComponentOrder`. The rows are never sorted or rewritten. After that order check, `sysrootDigest` and every declared component `sha256` are loaded with `RetainedInputs::blob`, which requires the raw bytes whose SHA-256 is the digest. An empty array yields `declared_components` 0. Two names that share one digest remain two rows.

Success exposes `CompilerToolChecks`, the declared sysroot digest, and the declared component count. The retained sysroot bytes in the new controls are the opaque fixture `unadmitted sysroot fixture`. Manifest grammar, stdlib closure selection, signed component membership, completeness, signatures, sysroot materialization, `NativeContextVerified`, body identity, and provider, Plan, Run, capability, or qualification authority remain separate owner duties. `ComponentOrder` stays a local Rust error.

The previous test file is an exact prefix. The nine appended controls cover opaque binary and Unicode preimages, an empty declaration, missing and substituted sysroot bytes, missing and substituted component bytes, unsorted and duplicate names, shared digests, host and tool joins before byte observation, and frame, shape, and 65-row refusals on the existing frame route. The authoring tree's `design-lock.json` is the predecessor of HEAD: HEAD adds only the already-bound runtime-pins successor. The forward product delta against HEAD is these two files.

## Evidence

Supplied logs, read and not re-executed: `cargo test --locked --offline` of the Rust provider library on the candidate reports 117 passed, 0 failed, including all nine new controls. The Clippy log finishes with no warning lines. The recorded runner used `nice -n 10`, `--locked --offline`, `-D warnings`, and private `0700` `TMPDIR` `/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-g2-system-x7a1fh_d`. `checks.json` records `qualification` false. These controls are declared retention and order. They leave native capability, O1-a, day-0, O7, HSR, and E2s gates in place.

No required findings. Exact reviewed bytes follow assent. Product code and the design-lock bind stay separate commits, with no push.
