# G2 declared Rust body-language-version r1

ACCEPT-DESIGN-UNIT. implementationVerdict ACCEPT-UNIT. requiredFindings empty.

Subject manifest `docs/implementation/m3/native-g/g2-language-version-r1-subject.json` is 2208 bytes, sha256 `920bf4f12c1c19d29481b45303bde708d27e188b9255d8c5eb06dc195620be56`. All 10 members match. Successor `docs/implementation/m3/native-g/g2-language-version-r1/successor.json` is 2830 bytes, sha256 `ee19ead8eb0c70a61dde07f9d98d9d1be82c451bb7d9c9056d306979709c393e`. `passageOverrides` is `[]`. The record has no `passageSupersessions` key, so this review omits `supersededPassages`. Candidates are the other nine members, with the manifest pins. Standing: "PROPOSED G2 declared Rust body-language-version canonical record/rawSHA256 candidate; two existing files, no FACT/body identity or native admission".

Product HEAD `fc9ef1db5b1e848f14d2b2f74667ac16d00ddc9b` and architecture HEAD `d46ae06bc05143d951e5756eaf4e99eba73ca698` are the pinned bases and are tracked-clean. Stage copies match the candidate.

| Path | Before | After |
|---|---|---|
| `providers/rust/src/body_dialect.rs` | 5658 / `018eb6637f90837ab7f7c3ad4c41b6fefd81782421bebf23bd9d4fe84bf07634` | 10331 / `4a43b88cfb628ffa6a3680deb1cd697e7d784b567ea3711e70d5ceede66d80c7` |
| `providers/rust/src/body_dialect_tests.rs` | 21187 / `b337f9038ef969a5a541b8c2cf718dd034547a105dbd6a315798498f69bebc32` | 31035 / `54af3b7596ca2379c0a11e9014b80cf2d832778205fadeda29675c8ad92317e6` |

Removing the inserted language-version API from the new Rust file reproduces the accepted dialect checker and helpers byte for byte. The old test file is an exact prefix: 13 existing `#[test]` functions stay, and eight are appended. `derive_declared_body_language_version` is called only from those tests.

## Parents

All three parents are already accepted, and the architecture bytes match the pins.

- `docs/implementation/m3/preview-pack-i1/i1-l/product/schemas/sources/identity-v3.schema.json`, 198423 / `eb6ec9571f0a14f88139a42184a54d2dfc50042be304174ac23dce90bf3580b0`, is a candidate of the bound i1-l successor.
- `docs/implementation/m3/native-g/g2-system-inputs-r1/product/providers/rust/src/compiler_tools.rs`, 10232 / `b09afe2a372b4071feb7e2b290fd7691483543b54164fda3f67b12e27bea1195`, is a candidate of the bound G2 system-inputs successor. Product `providers/rust/src/compiler_tools.rs` matches that pin.
- `docs/v2/contracts/product-v1/native-evidence.md`, 329013 / `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`, is a design-lock input.

Bound TOML views and the Cargo.lock join are already on this HEAD. `crates/identity/src/lib.rs` stays 3274 / `27e4bbf2f35612dbd696baefe28045ffffd3faf473e710134aa67d9a3c2a32cf`, `crates/identity/src/toml.rs` stays 13423 / `55294d354966713f4d11fd79117138e1a21f3ac849580646033681a362684c0e`, and `tools/identity/dependency-policy.json` stays 56472 / `c1e2f006f51a2c5b6c85214e6963816318f6d39204d86a9ff59004942f6176a5`. `Cargo.lock` stays 13130 / `532e04105b6157d25fb52f7379e3b8ae2cd67741711e6cb15a731d9cd7c23bf1`. The bound lock-join files `dependency_inputs.rs` 14597 / `a50331159e43ae403bcc17d3a7a3d3120f469e119c11368a78b9deeae1ad68f9` and `dependency_inputs_tests.rs` 31984 / `8b7231aa284f518258b3351b9bf61bc7ec66bc3300a27d8b466e39419a820464` are equal on the product and the candidate. No pending source or policy bytes are used as law.

## Law and behavior

Identity `languageVersionBindingLaw` defines the FACT-IDENTITY `languageVersion` component as the raw 32 bytes of SHA-256 of the canonical `body-language-version` record. The Rust row at `native.semantic-universe.rust.v2` fixes `compilerName` to `rustc`, `compilerVersion` to `toolchain.rustcVersion`, `compilerBuild` to `toolchain.rustCommitHash`, and `dialect.edition` to the selected compilation-target edition. `bodyLanguage` is `rust`. The closed record requires `schemaVersion` 1, `languageId` in {typescript, javascript, rust}, and `dialect.edition` in {2015, 2018, 2021, 2024}. Encoding is `raw-32-byte-sha256-of-canonical-record`. Native evidence §11 names the same boundary: the interpreter of the body span and the selected dialect enter the record; operational platform, sysroot, standard-library components, the code-generation backend, Cargo and resolver versions, paths, and unrelated crate names stay out. A uniform edition map does not skip ownership. There is no single-edition shortcut.

`derive_declared_body_language_version` calls `check_declared_body_dialect` first. That accepted path still requires the universe, context, nested, snapshot, and ownership joins, refuses partial enumeration before it reads relation rows, and selects by exact anchor path and `selectedUnitIds`. A missing, partial, or ambiguous ownership result remains `BodyLanguageVersionError::Dialect` and does not reach tool retention. The universe edition map and each `targetEdition` are already closed to those four years by the native schema, or null when the target defers to its crate entry.

It then calls the unchanged `check_declared_tools`. That join retains the toolchain and `rust-dev-llvm` closure trees, requires kind and tool membership, requires `semanticVersion` to equal `toolchain.rustcVersion`, requires the context and toolchain target triples to agree, and requires the context digest to equal the caller-supplied host digest. The closure manifest bytes stay an opaque retained blob. The checker emits no `NativeContextVerified` frame and does not establish signed-manifest or compiler-build authenticity.

The record is then exactly `schemaVersion` 1, `languageId` `rust`, `compilerName` `rustc`, `compilerVersion` copied from `toolchain.rustcVersion`, `compilerBuild` copied from `toolchain.rustCommitHash`, and `dialect.edition` set to the selected edition. `opensip_identity::canonical_bytes` is the canonical JSON encoder. `raw_sha256` hashes those bytes to `[u8; 32]`. The success value carries the canonical bytes, that digest, the dialect observations, and the tool observations. The literal candidate exercised by the tests is:

`{"compilerBuild":"<40 zeros>","compilerName":"rustc","compilerVersion":"1.95.0","dialect":{"edition":2024},"languageId":"rust","schemaVersion":1}`

Changing `rustcVersion`, `rustCommitHash`, or the selected edition changes the digest. Changing `hostTriple`, `targetTriple`, `cargoVersion`, or `sysrootDigest` changes the context identity and still yields the same record digest. An unrelated crate in the edition map, and two selected owners that agree, leave the digest unchanged while `selected_owner_count` can be 2. A forged display version that disagrees with the closure `semanticVersion` is `CompilerToolError::CompilerVersion`. Missing `rustc` bytes and a context with no retained closure are retained-tool errors. `src/lib.rs.more` stays `NotCompiled` against an exact `src/lib.rs` owner. The only caller is the test module.

Fixtures use `b"inert unadmitted manifest"`, synthetic tool bytes, and the existing owned universe. They do not admit a signed closure, a real compiler build, or an ownership producer.

## Evidence and inventory

Supplied logs, read only. `evidence/checks.py` takes the lane lock, runs rustfmt and Cargo, and writes its own checks file. It was not executed.

`evidence/unit-tests.log` (14127 / `ecb817f309fd4e5b11f28a62792f4888bc56bb38e94784f59957ac689250653f`) is `cargo test --locked --offline` of `providers/rust` on the candidate. It finished the test profile in 17.56s, ran 134 tests, and reported `ok. 134 passed; 0 failed` in 4.48s. All eight new tests passed. That is the prior 126 Rust-provider library tests plus these eight.

`evidence/clippy.log` (935 / `6cb0af9ccf11eed97d1d2155598212d96747e6718162eeadfaa71d5adcfea539`) is the authoring script's `cargo clippy --locked --offline --lib -- -D warnings` run. It checks `opensip-rust-provider` on the candidate and finishes the dev profile in 13.15s with no warning text. `evidence/format.log` is empty. `evidence/checks.json` records `passed` true, `newTests` 8, private `0700` directory `/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-g2-language-cnbwcjgq`, inventory 166, and `qualification` false.

Inventory v166 is still 614780 / `d1d5e69aeacbef99d33fcfd4f4881c72e8671cda04e036156f1412c17c30926d`, the last inventory successor. Both Rust paths are already rows. Row keys are `description`, `generated`, `package`, `path`, `role`, and `standing`, with no content sha256. Across 967 tracked product files, the candidate differs only in these two Rust files and `design-lock.json`.

The candidate lock is 560797 / `8065495fd247dd4f9941a9bb7fc3187b26388854b910e26ca878e7bd254d2b64` (111 contract successors). HEAD is 563455 / `768a0daf6e93a0324f57f10205e8f6cc0dadc63c3da58a4ac110878c43bceffe` (114). The candidate lock is a prefix. The three later records are the already-bound G2 system-inputs successor `c7fc94c91ec832eb09f359ae1c881b65b32088265420d26d927ecec485505c76`, the TOML-views successor `33c92dc7afdf704008ab0a18dc24478319f9de852035ff27fef0f32da5f86649`, and the G2 lock-joins successor `365784b23b8092049593398bb2959e4deb2c01ef8539ff1ad541c4d9dce908a5`. Approvals, inputs, the 126 inventory successors, and inheritance match. The code commit lands on HEAD and leaves that lock in place. Design-lock binding is a separate commit. Nothing is pushed.

`~/Library/Application Support/OpenSIP` is absent. This record supplies the declared canonical-byte recipe and its prerequisite observations. It does not admit a FACT-IDENTITY token, a normalized body, Coverage, native context, a Plan, a Run, a provider, or a qualification.
