# Adoption receipt: NSS-F4, the F4 closure-interface rulings (X-F4-1, X-F4-3, X-F4-4), 2026-10-30

**Decision LD-COORD-NSSF4 (coordinator, session 9ce22ffd): ADOPTED, owner-delegated under OD-AUTO-1, as a law-class
change to DR-103's capability vocabulary, C2PM-1's analyzer selection and the NE recipes, after R3 review. It
follows LD-Q-53.**

## What it rules
- **X-F4-1:** the universe's `runtimeArtifactSha256` is T's id, and `providerArtifactSha256` is P's id. These are
  `closure2` suffixes, as explicit successor recipes. The minting host checks both, and `bind_typescript_universe`
  adds the runtime join.
- **X-F4-3:** the TypeScript native capability surface is six `typescript-semantic`/2 branches in a CMS successor
  copy:
  - the protocol row `typescript-semantic.protocol {capabilityTokens}`, whose set Hello's array carries;
  - five relation rows;
  - the native selection, which runs after every existing admission refusal;
  - C2PM-1's analyzer subprotocol, major 2, for TypeScript. T and S are at 1.
- **X-F4-4:** `runtimePayloadSha256` = `SHA-256(JCS({schemaVersion: 1, files}))` over an explicit runtime-support
  inventory. At M3 that inventory is exactly `{etc/openssl.cnf}`.
- **X-F4-2:** no release-format byte changes, and there is no CR-1 escalation.
- **The LD-Q-10 check:** only the manifest-schema digest moves, and its pins are live generation pins. No retained
  identity changes, and all 11,010 shape-oracle verdicts are kept.

## What was reviewed
| Artifact | sha256 |
|---|---|
| **`NSS-F4-r3.md`** | `27a9a9bc6ef54a0ac0456606143ebadd82cc3325c1c5684b6818e1a0ec3abf8b` |
| **`completion/manifest-schema.completed.v1.json`** (the CMS successor copy) | `e698f9d6ae305a2fbd2e4b47c1f66a77c712667350eac3e16227acb4f9df6af4` |
| **`overrides.json`** (six insert-only overrides) | `049f1fa5d9e78a6e5561ea3627062fd9b7dad1682f1409294bd45ec9b56986cb` |
| Evidence: `build_overrides.py`, `build_nss_f4.py`, `vectors.json` | as listed in `HANDOFF-ADOPTION.md` |
| **R3 review r3 (`NSS-F4: ACCEPT`, no findings):** `REVIEW-r3.md` | `0c6ac99cf26e914ec0099d558291941f0692fb10e5a8841daaf2f5289547e606` |
| R3 reviews r1 (RF-1, RF-2, NB-1) and r2 (R2-RF-1), REQUIRED-FINDINGS | `3d721915…`, `bf182530…` |
| The author's handoff | `823dc94284a641f1c4cf9eac9d0f650e08db30fa84e93325dad7842320cdd1b0` |

- **The reviewer:** opensip-nss-f4-review, Codex gpt-6-astra/high, R3-FRONTIER (workspace w10). It is a different
  vendor from the Claude author (opensip-nss-f1 / nss-f4, Opus 5.5 high).

## The assignments (LD-Q-58)
- **X-NSS4-B (the binding):** F4's first unit, **after NSS-F1's binding (F1-h0)**. It writes `successor.json` in
  FA-2's form, places the CMS copy, regenerates, re-pins `sources.json`, and re-runs `build_overrides.py` against the
  then-current lock. Regenerating the shape is part of this binding.
- **X-NSS4-F4:** F4. P's protocol row and relation rows, T and S at major 1, the payload digest, and
  `closure-build.json`.
- **X-NSS4-C4:** C4a-TS, with the C2b-1a interfaces. It mints the artifact members. **`manifestId` has no M3
  source:** C4a-TS's plan must name one, and goes to the coordinator (R3) if no published source exists. This is
  carried as CP-C4ATS-2.
- **X-NSS4-SEC and the native-selection half of X-NSS4-D:** C2a-4 (the R10a/ER10a admission wiring, where selection
  runs). It covers the extended reachability→calls pair rule, `AnalyzerSubprotocol`'s production constructor from
  the admitted protocol row, and the selection rule after the existing refusals.
- **X-NSS4-D's Hello half** (Hello's capability array taken from the protocol row): F1-h1, the host TS2 codec.
- **X-NSS4-G2:** G2, in RS1. The same form for `rust-semantic`/3, not decided here. It is carried.

## Binding order
F1-h0 (NSS-F1) first, then F4's X-NSS4-B.

## Owner notification
It is flagged to the owner as an owner-delegated, law-class adoption.
