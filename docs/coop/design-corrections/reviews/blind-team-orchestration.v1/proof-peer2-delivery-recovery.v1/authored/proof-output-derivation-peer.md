# Proof-output derivation peer (MUST recheck)

**Verdict: `ACCEPT_SCOPED`**

Same Grok coauthor peer as COMPLETE41. Not blind. Not whole-design acceptance. Not readiness. Not a global source pass. Source pins for the two edited files are deliberately stale and were not resealed or bypassed. Isolated identifier/schema joins here are not a Run. Prior96 controls remain historical scoped evidence.

COMPLETE41 artifacts are unchanged under `complete41-immutable/`.

## Disposition of prior findings

| Prior | Disposition |
|---|---|
| MUST-1 Seal3/Run3 field value sources unpublished | **Addressed.** §9.7 now has complete Seal3 and Run3 tables. Every schema-required key is named; `additionalProperties: false` forbids extras. Values join proof, Plan, snapshot, and `ID(...)`. Policy-derivation3 remains the closed six-field record, now explicitly `{schemaVersion:3, planId:run.planId, proofBundleId:seal.proofBundleId, policyDigest:plan.policyDigest, waiverDigest:plan.waiverDigest, verdict:proof.verdict}` with typed identifier `ID(policy-derivation, descriptor)`. Replay reconstruction uses the same keys. |
| MUST-2 `identifier` named as field law; proposed `x-opensip-prefix` | **Addressed, with a correction to COMPLETE41’s suggested remedy.** Identity-and-evidence §3 defines `H(D,X)` as the **unprefixed** framed SHA-256. The prefixed spelling is the identifier: prefix, colon, lowercase H hex. `identity-schemas.v3.json` has **no** `x-opensip-prefix` member. Root keeps that split: `H` is the digest; `ID(D,X) = prefix(D) + ":" + lowercaseHex(H(D,X))`. The output prefix rows are the existing identity-and-evidence §3 domain/prefix table subset (and the same pairs as `identity-model.v3` `PREFIX` for those domains). COMPLETE41’s proposed `H`:=prefixed form and nonexistent selector are rejected. |
| MUST-3 `program-predicate` said RuleProgramV1 | **Addressed.** Description now names RuleProgramV2. Digest selector remains `#/$defs/RuleProgramV2`. No RuleProgramV1 remains in the patched schema. |
| W-1 evidence3 `importIds` Plan-order vs canonical-set | **Addressed.** Now `importIds: Cset(plan.importIds)`. Schema stays `x-opensip-order: canonical-set`. |
| W-2 `canonical.py` in §9 notation | **Addressed.** Notation cites identity-and-evidence §3. |

No new MUST. Residual informal “finding3 H ids” / “finding-key2 H” on two finding lines is the older local spelling; the Output identities block and schema patterns (`finding3:`, `finding-key2:`) uniquely require the prefixed `ID`. Not a second field law.

## Seal / Run / policy-derivation / identifier joins

H frame in §9 equals identity-and-evidence §3 and `canonical.identity`: SHA256 of `ASCII("opensip.product.v1") ‖ 00 ‖ ASCII(D) ‖ 00 ‖ uint64BE(byteLength(C(X))) ‖ C(X)`. `byteLength` / `length` are the canonical UTF-8 byte count.

Output prefixes checked against the owning table (identity-and-evidence §3 Domain/prefix rows) and against reference `PREFIX` for the same domains:

| Domain | prefix |
|---|---|
| evaluation-subject | subject3 |
| finding-fingerprint | finding-key2 |
| finding | finding3 |
| proof-bundle | proof3 |
| semantic-evidence | evidence3 |
| evaluation-seal | seal3 |
| run | run3 |
| policy-derivation | policy-derivation3 |

Also matches `x-opensip-evaluator-profile.changedIdentifierMajors` / `newIdentifierDomains`.

Seal3 fields = schema required list. Run3 fields = schema required list, including `capabilityManifestId` retaining the declared capability-manifest-id recipe. Evidence3 still lists `importIds: Cset(plan.importIds)` and is not `EI`.

Reference `replay` / `derive_policy_result` reconstruct the same seal/run/policy-derivation keys. That is reconstruction evidence, not a claimed Run from this recheck. No model file changed (patch is only the composition contract and identity-schemas.v3.json).

## Checks and limits

Bounded Python joins: `probes/recheck-seal-run-id.v1.json`. Did not re-run Prior96. Did not invoke `close_run`. Did not reseal or rewrite pins. Composition pin `a762dd61…` ≠ current `c5b8fd2f…`; schema pin `cc60e9a5…` ≠ current `0d27a4fc…`. Those mismatches are expected after prose/schema-description edits and are not a pass.

## Inputs

| Path | SHA-256 |
|---|---|
| `evaluator-composition-contract.v3.md` | `c5b8fd2f1de1c5c1e77c5c074b35f3581004318c1c1e0983aa34cb09a83ecf8e` |
| `identity-schemas.v3.json` | `0d27a4fcd6e3f928262999bdceca711ccb82c99a25663cddebc02616288820ba` |
| `correction.patch` | `72f25ee3d28a9313237a1b6ffd45d2e3625802fdbbed61578686ccd3752db1f7` |
| `assessment.md` | `1d5d91d9972490751d2dadee474bf3a62d7e9afdfe6df7da8bec36d5e546814f` |

Proposed two files are byte-identical to isolated `target-proof-successor.v1`.
