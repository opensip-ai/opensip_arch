# NSS-F1: the TS2 native-context inputs carrier (native contract successor, binding candidate)

Status: **PROPOSED binding candidate (X-NSS-B, F1 plan r6 §3.12.1, sub-unit F1-h0).** The successor's text is
NSS-F1 r2, adopted as LD-COORD-NSSF1 after R3 review (`ADOPTION-NSS-F1.md`, `NSS-F1-r2.md`). This directory
materializes it in FA-2's form. The binding's own review question is byte fidelity to NSS-F1 r2 and its evidence
files, and nothing else. It needs that independent `ACCEPT-DESIGN-UNIT` and root assent before selection.

`NSS-F1-r2.md` is the authority. This README only summarizes it and indexes the files.

## What the successor does (NSS-F1 r2 §2, §6)
- **The token.** `native-context-inputs-v1`, a new optional, non-identity `typescript-semantic` capability token,
  appended last to `TypeScriptCapabilityToken` (`TypeScriptCapabilitiesV2.maxItems` 12 to 13). The Rust token enum
  is unchanged. It is a token the Plan needs for every TypeScript worker (LD-N2).
- **The carrier.** Under the token, `OpenUniverse` carries `TypeScriptOpenUniverseV3`: `TypeScriptOpenUniverseV2`
  with every member unchanged plus `nativeContextInputs` (the exact retained bytes of the Plan-bound context, the
  configuration graph and, when non-null, the layout, plus the unit root). The worker checks the digest joins before
  `UniverseAccepted`, takes only the selection and re-derives everything else.
- **The outcomes.** A context mismatch stays `PreAnalyzeUnavailableV1`. A graph-only disagreement or a closed-key
  refusal is the new token-gated `TypeScriptPreAnalyzeInputMismatchV1`.
- **Without the token** every frame, payload, vector, identity and PlanId is byte-identical.

## Files
| Path | What | Source |
|---|---|---|
| `NSS-F1-r2.md`, `ADOPTION-NSS-F1.md`, `section-9-5a.md`, `overrides.json` | the successor, its adoption receipt, the NE §9.5a prose, the 18 insert-only passage overrides | NSS-F1, byte copies |
| `design/native/provider-handshake.schemas.v1.json`, `product/schemas/sources/handshake-v1.schema.json` | the two handshake successor copies (identical) | NSS-F1, byte copies |
| `design/native/native-context-inputs.schemas.v1.json` | the new schema document (`opensip.product.native-context-inputs.1`) | NSS-F1, byte copy |
| `product/schemas/sources/native-context-inputs-v1.schema.json` | its product copy | the design document's bytes |
| `evidence/build_overrides.py`, `build_nss_f1.py`, `vectors.json`, `bound_selectors.py`, `bound-selectors.txt` | NSS-F1's evidence (§12) | NSS-F1, byte copies |
| `product/schemas/{admission-registry,admission-source-map,registry,source-map}.json`, `product/tools/contracts/generator-closure.json` | the five handshake live pins after the re-pin, with the new schema's admission rows | the product candidate's bytes |
| `successor.json` | the record: parents, `overrides.json`'s passage overrides verbatim, candidates | `evidence/build_binding.py` |
| `materialization-map.json`, `../nss-f1-subject.json` | product paths of the candidates; the review subject | `evidence/build_binding.py` |

## Parents
NE (`native-evidence.md`, `83b99783…`); the RCA-r2 startup copies ST and PST (`e8b2aae5…`, four pointer overrides
each); the TypeScript protocol-2 order table T2O (`007ef7af…`, one pointer override); the RCA-r2 handshake copies HS
and PHS (`1fc57cbc…`, replaced by complete copies `260fb535…`). NE carries nine line overrides (125, 127, 1620, 2853,
2862, 2953, 3007 appending §9.5a, 3192, 3215). No selector is already bound by the product lock's 191 successors.

## Product rows (NSS-F1 §9 X-NSS-B; LD-N11's pin census)
- `schemas/sources/handshake-v1.schema.json` takes the successor copy. Its five live pins move:
  `schemas/admission-registry.json`, `schemas/admission-source-map.json`, `schemas/source-map.json`,
  `schemas/registry.json` (the source digest, the recipe's source set and its generator-closure digest) and
  `tools/contracts/generator-closure.json` (the handshake and source-map pins).
- `crates/components/tests/data/native-rust3-profile-cases.v1.json` re-pins `currentAuthority.sha256`; its two
  digest constants in `rust3/replay_tests.rs` follow.
- The handshake `SourcePin` in `crates/identity/src/schema_registry.rs` (bytes and a decimal digest array, which a
  hex grep does not find) moves with the source, or the embedded registry cannot select it.
- The new schema gains its admission-registry and admission-source-map rows and its product file. It is
  admission-registered only. Its Rust embedding and identity source pin need an identity pattern row for
  `^(?:[0-9a-f]{2})+(?![\s\S])` (the table has only the capturing form). Its generation rows and carriers, and the
  `native-carriers-v1` records, belong to F1-h1 (X-NSS-D).

## Not done here
- The regenerated carriers. `crates/contracts/src/generated/protocol.rs`, `providers/typescript/src/generated/protocol.ts`
  and `apps/report/src/generated/report.ts` (whose header pins the registry and closure digests) must be regenerated
  with the pinned generator.
- The held-out census receipts (`crates/security/src/custody/discovery_census_held_out.json`,
  `crates/security/src/snapshot_ledger_census_held_out.json`) pin `generator-closure.json` and go stale. They need a
  refresh.

## Reproduce
```
python3.14 -I -B evidence/build_binding.py --source <lead nss-f1> --arch <opensip_arch> --product <opensip> --check
python3.14 -I -B evidence/build_overrides.py --arch <opensip_arch> --product <opensip> --check
python3.14 -I -B evidence/build_nss_f1.py --arch <opensip_arch> --product <opensip> --check
```
