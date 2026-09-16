# Frozen trial review: syntax-universe-10

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Private syntax-universe diagnostic on frozen09. **Not runtime selection. Not Plan/full closure/replay. Not inventory/runtime02 install.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-syntax-universe-review-10/review`. Live, frozen, and history not edited. No commits.

## Subject pin

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/trials/syntax-universe-10/subject.json` | 45418 | `70dc7cbaf8eceda1961eadec82ea2a896e16a475f494c3d0a04499e8e403af16` |
| adjacent `subject.tar.gz` / `archive-pin.json` | 1945024 | `bcf5f9de44f459e5ef2fc11e268b3f3ed6fcbb66c2b8396d2df4bb021b5ed616` |
| adjacent `syntax-universe-result.json` | 293 | `8a9733c5a12dd6e3650782faa38289d6d9066ad50288c55e0017ecd04aac3648` |
| export | `/tmp/opensip-implementation/m2-syntax-universe-subject-10` | 252/252 member pins match; tar 252/252 match; 0 extra; 0 missing |

252 subject paths are **not sorted** (trial hygiene; pins still exact; 0 duplicate paths).

Dependency pins all present and hash-match in architecture:

| Pin | Bytes | SHA-256 |
| --- | ---: | --- |
| frozen09 `native-case-09/subject.json` | 48220 | `6290b55b05a4c1a70f3edacf6e4efccc64cd4ad8c49b841b8acb69f9738087d6` |
| archived universe-binding `report.json` | 2714 | `d114bb0eac1868759d4ae59e34c6e482550b3ccc125091e1dc38ff0ced391626` |
| selected native `native_evidence_model.py` | 319944 | `e6784aa1a595222cfd5a3da55e2beaa3d0839c878d67d6821297682089bde2b9` |
| selected identity `identity_model.py` | 158555 | `619d6e3cf49d0cd58967688e35c1598c92eaeb32b95fd30bb67f634271c141e6` |

Product schemas inherited from 09, byte-identical: identity-v3 `311c1feb09ff8cd0b207233d2ec0d7440bb1c72fc0470de277ee1891c24bb68f` / 197480; native-v2 `e5834d37aebd96d77d352975878da349033f8633ecbd83322ad0fbea461f7773` / 280357; native-context-registry `269f25c1eb66f6cf31fc244c00ba3ee6f06b895d6b2e8ce1e4052071e1c7dd0a` / 2592.

## Delta on 09 (product)

Unchanged vs native-case-09 (among others): `native_context.rs`, `native-context-registry.json`, capabilities/plan_capability/unicode_case, identity crate, identity-v3, native-v2, native-context fixtures.

**Product code added/changed:**

| Path | Role | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `product/crates/evaluator/src/native_universe.rs` | new | 4606 | `4f5c8d484d7bcb16a5b888fc68a1d621b46f7d84df2178c320b059d0e4fa3d8f` |
| `product/crates/evaluator/src/lib.rs` | export | 716 | `c42ea8143d60b7958b6de53d8c50e4103c47d0f0693ef5d14b2bbe16502c5a33` |
| `product/crates/host/src/native_owner_tests.rs` | boundary test | 9976 | `999abf653463a4c3d754e10046d02f97136aae45af14a4cfb0f40e1c4328eb40` |

Trial machinery also adds harness `syntax-universe` mode, `check_syntax_universe10.py`, 47-vector corpus, and preserved `initial-harness-not-built.stderr` (FileNotFound on harness before compile; later `harness-build` + corpus). First premature harness launch is failed preparation, not a comparison result.

`native_universe.rs` is **not** a row in accepted inventory v12 (`repository-file-inventory.v12.json`). Live product has no such file. Trial10 is not runtime02 / live install. A future additive inventory is required before installation, matching the trial README.

## Law vs selected `bind_syntax_universe` (e678)

`inspect_syntax_universe(inputs, digest, work)` — no admission argument, no snapshot, no nested retained map, no Plan id:

1. **Row dispatch.** `frame_candidate(digest, SemanticUniverse, work)` rehashes the H-frame against the **current** identity-v3 `native-semantic-universe` set and admits `SyntaxUniverseV2ResolvedInputs` (`schemaVersion` const 2, `resolutionAttempted` const false, `selectedGrammarIds` minItems 1, uniqueItems, `x-opensip-order: utf8`). Then requires `language==syntax`, `contextForm==sha256-text`, `binding.entryPoint==bind_syntax_universe` else `RegistryLaw`. Non-syntax universe domain → `Unsupported("compiler universe retained-input owners")` **before** any compiler retained-input join.
2. **Named context rehash/domain.** Walk `row.contextField` (`nativeContextId`) on the universe descriptor; parse `sha256:`+64 lowercase hex; `frame_candidate(..., Context, work)`; require `context.domain()==row.contextDomain` (`native.context.syntax.v2`) else `ContextDomain`. Foreign rust context is this typed error (oracle `invalid`), not an ADMIT and not a caller-supplied admission mismatch refusal.
3. **Owner rerun every call.** Unconditional `inspect_native_context(inputs, context_digest, work)`. No memo. Removing the grammar-bundle closure from an otherwise golden universe still yields `native.native-context-closure-unretained:grammarBundle.closureId`. Missing context blob is `Frame(MissingBlob)`, not a cached success.
4. **Carried refusals then grammar subset.** `admission.refusals()` into a `BTreeSet`, then `selectedGrammarIds` must be a subset of `context.grammarBundle.grammars[].grammarId` else `native.syntax-grammar-not-in-bundle:<id>`. Matches e678 `bind_syntax_universe` after an independently computed admission. Empty/duplicate/unsorted selection fail at registered schema (`Frame(Schema(Mismatch))`), not as silent defaults.
5. **No snapshot / nested inputs.** Syntax identity-v3 row has empty `nestedIdentities` / `nestedRecords`. Compiler domains stay Unsupported. Nothing executes a parser, Plan selection, `close_run`, or replay.
6. **Typed errors / Limit.** `work` is forwarded to both frame admits and the context owner. `work=0` on a golden syntax universe is `Frame(Schema(Schema(Limit)))` — Limit is not collapsed into a string or success. `NativeUniverseError::{Frame,Context,Unsupported,RegistryLaw,ContextDomain}` stay distinct.

Does not take a caller ADMIT. Does not trust a previously golden universe id without the named context bytes.

## Reproduction (independent, rustc 1.95.0, `--locked --offline`)

- `cargo test --locked --offline -p opensip-host syntax_universe --lib`: **ok** (`syntax_universe_rechecks_the_named_context_and_selected_grammars`).
- Harness replay of frozen `syntax-universe-requests.ndjson`: **47/47**, 0 mismatches vs expected. 36 `checked`, 32 with native refusals, 2 unavailable (missing universe/context blobs), 9 invalid (corrupt context, empty/duplicate/unsorted/shape, foreign rust context → `ContextDomain`). Independent rerun bytes equal frozen `syntax-universe-actual.ndjson` (`ad07a78e…acf0`).
- Frozen `workspace.stdout` sums to **95** passing tests (0 failed); `clippy.stderr` finishes `-D warnings` with no diagnostics.
- Private probe (review tree only): golden `json.v1` selection empty refusals, context `d91e9cb3…9cbb`; `work=0` → `frame-schema-limit`; schema-valid rust universe frame → `Unsupported("compiler universe retained-input owners")` with **no** nested rust retained owners supplied; second call on the same maps still empty (no memo).
- Static bypass checklist on `native_universe.rs`: no admission parameter, reruns owner, no memo, compiler Unsupported, no `snapshot_inventory`/`snapshotInventory`, no `configGraph`/`nodeModulesLayout`.

Did not replay the Unicode 15 million-scalar corpus. Did not re-exec the Python oracle (review Python unidata is 16.0.0; oracle asserts 15.0.0). Comparison used the frozen expected rows produced under that oracle.

## requiredFindings

None.

## Notes (not required)

- Subject `files` array is unsorted.
- `reframed-rust.v1-suffix` is a fixture no-op (rust already owns `.rs`); other grammars do exercise suffix law.
- Inventory v12 lists `native_context.rs` / `plan_capability.rs` / `unicode_case.rs` and does **not** list `native_universe.rs`. Trial standing already says a future inventory is required; this is not a silent live install.
- Compiler-Unsupported is now runtime-probed; the 47 vectors never frame a rust/ts **universe** (they do frame a rust **context** under a syntax universe → `ContextDomain`).

## Verdict

No required findings. Private diagnostic matches the selected syntax bind: named context rehash, actual context owner every call, carried refusals, grammar subset, no caller ADMIT, no Plan/replay. Compiler bind stays Unsupported. Exact immutable identity-v3 / native-v2 / native-context-registry. Not a live/runtime02 selection.
