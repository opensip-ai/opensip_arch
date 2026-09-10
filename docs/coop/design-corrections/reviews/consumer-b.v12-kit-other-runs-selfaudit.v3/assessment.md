I'll continue the same kit-only origin as a quality self-audit: verify the original charter, then re-check v2's four PASS claims and both remaining-property refusals against the charter's actual quantifiers.Charter SHA matches. Next I’ll read the full original charter and the structured requirements so the audit uses the charter’s actual quantifiers, not the v2 condensed map.The charter’s “at least one file-fact Run” is a set quantifier, not a per-Run demand. I’ll load identity-and-evidence §3 and native-evidence §2/§11 next and audit the checker against those laws.I’ll copy the checker into the v3 output with redirected paths, then read identity-and-evidence §3 and native-evidence §2/§11 in full.I’ll dump selected native fields and identity-law operands from the four stores, then assert each producing rule instead of treating schema or H presence as admission.v2 treated blob presence as tree-membership and never joined `rustcVersion` to the tool-closure `semanticVersion`. I’ll encode those producing-rule assertions and emit the self-audit plus successor reviews.**Successor verdict: `OTHER_RUNS_REFUSED`**

Same kit-only four-Run origin. v2 review bytes were preserved. This is not whole-consumer ACCEPT. Stores were not changed.

Wrote only `/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-selfaudit.v3/output/`: `review-selfaudit.md` / `.json` and successor `other-runs-review.md` / `.json`.

Original charter SHA-256 `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` matched. v2 snapshot still 343/343 `feb08879…`.

## Withdrawn grades

v2’s four-Run refusal on `R-RUN-CLONES-L0-AND-NORMALIZED` and `R-RUN-CLONES-CUSTODY` is **withdrawn**. The charter’s Phase 5 quantifier is **at least one** complete file-fact Run, which may be the same export as a TS, Rust, or syntax-code Run. That is not a per-language demand on every TS and Rust graph. Syntax-code is outside this recheck and is **pending global integration**, not a waiver and not a failure of each scoped graph.

v2 **structural/fullsemantic PASS** on ts, rust, and rust-partial is also **withdrawn**. Identity-and-evidence §3 requires Run closure to re-run owning native admission over retained bytes. Native-evidence §2 names field-producing recipes. Schema inhabitance, H-frame parse, and blob presence are not those recipes. Expected-proof C equality of a shared `compose_proof` does not establish them.

## Actual first structural refusals

| Run | Successor layers | First refusal |
|---|---|---|
| ts | structural REFUSED, fullsemantic **NOT_REACHED** | `compilerPackageDigest` `9fb7d4cc…` is a retained blob (`tsc-pkg`) but **not** a member of the signed toolchain tree (`bin/tsc`, `bin/node`, `bin/toolchain`). Schema retention is `closure-tree-member`. |
| rust | structural REFUSED, fullsemantic **NOT_REACHED** | `rustcVersion=1.80.0` ≠ tool-closure `semanticVersion=1.0.0` (`native-context-compiler-version-not-from-manifest`, native-evidence §2.3/§11). |
| rust-partial | same context as rust | same first refusal |
| syntax-data | all PASS | none on the executed producing/join set |

v2 never compared those operands. Fullsemantic PASS after an unexecuted native join is not successful replay.

Independently matched (not used as a blanket pass): rust `unitId` derivation from `H(native.compilation-unit.v1, UnitIdentityV1)`; TS config-node kind / `configOrigin`; rust `rustflags` / `configProjectionSha256` / `cfgSets ⊇ baseCfg`; vcs inventory C; evidence `importIds` = plan `importIds`.

Predicate `inputRefs` citing `rule-program` is schema-live (`ProofInputRef.domain`) and excluded from `evaluationInputRefs` by enumeration-contract §7. Recorded as a law-interaction, not the first refusal.

Reproduce:

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-selfaudit.v3/output/independent/selfaudit.py
```
