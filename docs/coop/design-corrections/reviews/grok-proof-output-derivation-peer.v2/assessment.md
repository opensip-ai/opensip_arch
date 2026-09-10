I'll re-check MUST-1/2/3 against the two files root actually patched, using identity-and-evidence §3's raw framed H and the real domain/prefix table—not the selector I proposed. Previous peer artifacts stay immutable.The two patched files match successor. I’ll read the patch and the owning H/ID tables next, then check seal/run/policy-derivation joins against those bytes.Seal/run/policy-derivation tables match schema and the identity §3 H/ID split. I’ll preserve COMPLETE41 bytes, then write this recheck only.**Verdict: `ACCEPT_SCOPED`.** Not whole-design acceptance, not readiness, not a global source pass.

COMPLETE41 MUST-1/2/3 and the importIds/canonical-owner wording are addressed in the two patched files. Source pins for those files are stale by design and were not resealed or bypassed.

### Disposition
| Prior | Status |
|---|---|
| MUST-1 Seal3/Run3 field sources | **Addressed.** Full tables; schema-required keys only. |
| MUST-2 `identifier` / `x-opensip-prefix` | **Addressed, with a correction to COMPLETE41’s remedy.** |
| MUST-3 RuleProgramV1 | **Addressed** as RuleProgramV2. |
| W-1 importIds order | **Addressed:** `Cset(plan.importIds)`. |
| W-2 `canonical.py` | **Addressed:** identity-and-evidence §3. |

COMPLETE41’s suggested `H` as a prefixed identifier and an `x-opensip-prefix` registry were wrong. Identity-and-evidence §3 defines **H as the unprefixed framed SHA-256**. The prefixed form is **ID**: `prefix(D) + ":" + lowercaseHex(H(D,X))`. Root uses that split and the existing §3 domain/prefix table. `identity-schemas.v3.json` has no `x-opensip-prefix`.

Seal3, Run3, and policy-derivation3 tables join schema required lists, that H/ID law, and replay reconstruction keys. No model change. This recheck is not a Run. Prior96 stays historical.

Residual informal “finding3 H ids” / “finding-key2 H” is resolved by the Output identities block and schema prefixes; not a new MUST.

COMPLETE41 bytes are under `complete41-immutable/`. Recheck notes: `probes/recheck-seal-run-id.v1.json`.
