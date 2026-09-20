# Correction to OWNER.md (source precedence)

**Standing:** assistance correction only. `OWNER.md` (`8b148484…5e36`) is **preserved unchanged**. This note withdraws or relabels several recommendations that followed from reading **only** the 251 primary extraction. It is **not** a review of mutable `m2-recovery-metadata-draft-254`, not approval, and not a 253 re-review (still `dcb6b43b…3169`). Historical extra-root / unresolved-context advice in OWNER.md §4 is **retained**.

Copies of the missing DR-103 / selection units now sit at `/tmp/opensip-implementation/m2-recovery-metadata-draft-254/dependencies/` and are byte-identical to `opensip_arch/docs/coop/completion/` (pins in that draft’s `dependency-pins.json`). Inherited checker report there: **187 / 187** (`inherited-report.json`).

---

## 1. Withdraw “manifest admitter absent / wait for a schema”

OWNER.md §1 treated `check-security-unit.v2.py` `admit_manifest` as missing because it is not in the 251 candidate tree, and offered either a **partial new** v11 subset or **waiting** for DR-103 JSON Schema.

**Correction:** full existing executable/schema already exist and are not unowned:

| Artifact | Architecture path | 254 `dependencies/` SHA256 |
|---|---|---|
| Checker | `docs/coop/completion/check_manifest_completed_v1.py` | `48951bd4…7f7a` |
| Schema | `docs/coop/completion/manifest-schema.completed.v1.json` | `a5140714…90af` |
| Contract | `docs/coop/completion/manifest-completion.contract.v1.md` | `da2b00f5…5deb` |
| SemVer helper | `docs/coop/completion/check_compatibility_design_v2.py` | `4931e728…3e93` |
| Constraint schema | `docs/coop/completion/version-constraint-schema.completed.v2.json` | `2a7e97a6…9968` |

Contract: v11 remains field/tree/permissions/typed-absence **authority**; `manifest-schema.completed.v1.json` is the complete **machine-readable** schema (`validate(raw, …)` in the checker). Status remains PROPOSED structural evidence, not shipping admission (`admitted: false` on POS cases).

**Do not** invent a partial schema and **do not** wait for an already-authored schema. Reuse `check_manifest_completed_v1.validate`. 251 extraction incompleteness is not source absence.

---

## 2. Withdraw exact `rootVersionRequired` / `revocationVersionRequired` pairing

OWNER.md §2 inferred **equality** (`catalog.rootVersionRequired == replacement.rootVersion`, list version exact) from 215 “exact prospective document contexts” and from **no comparison in 251**.

**Correction:** existing solver already states **minimum / ≥** semantics. `docs/coop/completion/compatibility-selection-model.v8.py` `solve` line 171 (copy `67111e35…7581`):

```text
root['rootVersion'] >= max(catalog['rootVersionRequired'], host['floors']['rootVersion'])
and rev['revocationVersion'] >= catalog['revocationVersionRequired']
```

Also `snapshotVersion >= host['floors']['catalogSnapshotVersion']` and catalog `issuedAt <= now < expiresAt` on the same line. Those **activation** predicates (expiry, freshness, floors) are what 215 **B.5 explicitly defers to COMMIT**. Current 254 leaves them pending. 215 does **not** rewrite the catalog’s required fields into exact root/list pairing.

No superseding 215 clause was found that replaces this ≥ law with equality. The OWNER.md equality reading is **withdrawn**. Do not implement exact pairing on that inference.

v8 `solve` lines 183–205 already enforce, for **selected registry entries**, not for inventing a new recovery-only catalog theory:

- duplicate catalog release tuples refused (`DUPLICATE-CATALOG-RELEASE`)
- unique catalog match per selected entry (`CATALOG-REGISTRY-RELEASE`, `len(matches)==1`)
- raw / preimage / envelope identity: `sha(raw)==entry.manifestDigest==release.manifestDigest`, `preimageSha256==release.manifestPreimageSha256`, `sha(env)==signatureRef==envelopeDigest`
- **EXACT** `release['hostCoreConstraint']==m['compatibility']['hostCore']` (`COMPATIBILITY-CATALOG-JOIN`)

OWNER.md’s claim that `hostCoreConstraint` is “lock selection via v3, not catalog completeness” is **too narrow**. Reuse **v8**, not v3 (`7e84a9f6…`). Exact hostCore join is catalog↔manifest; lock selection is a later `CORE.solve` step in the same function.

---

## 3. Reverse-completeness is unsupported

OWNER.md §2 listed as 215 B.5-owned: every catalog `releases[].manifestDigest` must appear as a retained payload manifest (no dangling catalog row).

**Correction:** 215 B.5 FULL signed scope forbids **skipping PRESENT members by role**. It does **not** say every catalog **record** must be shipped. v8 loops **selected registry-view entries** (`for e in view['entries']` if live and not shadowed), then unique-matches **that** release in `catalog['releases']`. Unpresented catalog releases are allowed.

Root’s intended recovery join: unique match for **each presented** manifest; catalog may contain unpresented releases; artifact closure still pending.

No contrary 215/v8/v11 clause requiring “all catalog releases present in the payload” was found. That reverse-completeness sentence is **unsupported**, not normative. Keep the forward join: each presented manifest has exactly one catalog release (stableId, publisher/sourceClass, version) with matching digests.

---

## 4. Permission-policy v8 vs v2

OWNER.md §3 pointed at **v2** `permission-policy.schema.json` (`3d7153d9…`) plus v8 `admit_policy_paths` / `merge_policy`.

**Clarification (verified):** architecture `security-schemas.v8/permission-policy.schema.json` is **byte-identical** to the v2 file (`3d7153d9…`, same `$id` `urn:opensip:design:permission-policy:1`, same required `policySchema/policyScope/grants/denies/consents`). 251’s `security-schemas.v8/` directory does **not** contain this file (only journal/revocation/root).

v8 **adds** `permission-policy-effective.schema.json` (`policyScope: "effective"`, `sources.global/project` digests) and the merge/path law in `security_unit_lib_v8.py`. Path-prefix normalization may be inherited; **current fields must not silently regress** to a v2-only reader that drops effective-document / sources identity. Reuse v8 raw + effective schemas and `merge_policy`, not a v2-only copy as if v8 were a different grant vocabulary.

---

## 5. What stands from OWNER.md

Unchanged and still applicable:

- One `Operation`; 252 `Index.select` then body validate
- Envelope `Verifier.verify` for catalog/manifest under the **prospective** replacement; `publisher_namespace` for component
- Repair: payload2 typed absence DR-110
- **§4 extra `rootChain` rows:** do not verify with prospective keys or 253’s current union; keep `unresolvedRootPairs` / `other-root-chain-context-admission`
- Do not claim staging, COMMIT activation, or implementation readiness
