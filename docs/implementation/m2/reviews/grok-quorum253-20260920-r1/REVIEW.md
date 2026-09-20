# Independent review — recovery quorum union 253 r1

**Standing:** bounded code review of frozen `recovery-quorum-union-wip-253-r1`. **Not** full metadata semantic admission, staging, S4/current authority, historical-root authentication, or native effects. Archived 252 (`b8efa554…4381`) and 251 (`1d4d9875…0dce`) reports were not edited.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Siblings reconstructed from verified 252 r2 / 251 r1 / 250 r2 extracts. Frozen fixture/variant directories were not overwritten. Optional `check_quorums.py` fixture-output path used.

---

## Verification

Frozen archive: **14736 B, 126 members, SHA256 `164dd2fa5045acf44b1ef3a465178eeee174d031be05b41aa9280456b6bdf8b7`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed 126/126. Standing: Incomplete WIP, not approval or source selection.

`quorum_reference.py` SHA256 `d708990d5608e8997440d7c110a558d49af0604d05edabd0af5e63617103e788` — **identical** in the 34-case r1 report and the 35-case r2 report. The extra-root test is test-only; production is unchanged.

`inputs.json` pins 252 r2 payload `f6403a40…edaf` and 251 revocation schema `14302736…fad4`. Helpers reproduced **250’s 42** and **252’s 32** cases while minting TEST-ONLY keys.

---

## What 253 adds

Uses 252 `prepare` on the **same Operation** to obtain actual RA / replacement self-ROOT / prospective BUNDLE facts, then verifies catalog, revocation, and component-manifest signatures under that **exact prospective replacement**, first filtering the **supplied retained** revoked keys.

The candidate list must pass the existing closed revocation schema, calendar-valid `issuedAt`/`revokedAt`, **exact** replacement `rootVersion`, integer `revocationSchema`, and lowercase 64-hex `keyId` subjects. Its **actual ROOT** quorum must verify **before** it contributes incoming keys. Invalid list signatures refuse `incoming-signature:revocation:…` and cannot enlarge the union.

Then one finite union `retained | incoming-keyId`. One second pass re-filters **every** internally verified, unchanged signature fact: old RECOVERY auth, new self-ROOT, payload, catalog, **the list itself**, and every component manifest. No recursive list replacement, write, or time witness.

Non-key namespace/release/catalog entries stay in the retained list and are **not** treated as keys (`unionRevokedKeyIds` stays empty; pending `namespace-release-and-catalog-revocation-semantics`). Supplied retained population custody/completeness remains a premise.

Other `rootChain` pairs that are not the authorized replacement are `unresolvedRootPairs`. They are not verified against the prospective root and current revocations are not blindly applied to historical proofs. Extra old-root pair with invalid signatures returns `['other-root.json']` and keeps `other-root-chain-context-admission`. Empty unresolved paths still do **not** grant staging.

Standing `authenticated-recovery-signature-quorums-only` with six pending owners, including catalog/component/policy/artifact shapes/identities/joins (fixtures keep synthetic catalog/component bodies).

**Fit to 215 B.5/B.6:** incoming-key union after the list’s own quorum, then recheck of relied-on signature facts including the list, matches that owner’s finite union/second-pass shape. This slice does **not** claim full member admissibility, current TRUSTED-entry, or complete incoming-list custody.

---

## Reproduction

Fresh `quorum-fixtures-live` and work-copy `variant-fixtures-r1` / `quorum-variants-r1`. Frozen dirs were not overwritten.

| Corpus | Result |
|---|---|
| `check_quorums.py` | **35/35** equal frozen `quorum-fixtures-r2/quorum-report.json` |
| Counters | objects **14**, edges **40**, bytes **18414** |
| `check_variants.py` | **5/5** core-equal frozen results |

r1 had **34** cases; r2 adds `other-root-context-explicitly-unresolved` only. Controls: skip list self second-pass; skip old-RECOVERY second-pass; drop retained keys from the union; substitute asserted ROOT keys for actual list crypto; omit list/root binding. Baseline refuses; mutant admits a signature-only result. Variant path SHA differs from local `S=Path` rewrite.

---

## Independent probes

| Probe | Result |
|---|---|
| Happy path kinds | auth, root, payload, catalog, revocation, manifest |
| List revokes one of two list signers | `incoming-union-quorum:revocation` |
| List revokes one replacement self key (3-of-2) | admits; replacement self still meets threshold |
| Retained+incoming each drop one replacement key | `incoming-union-quorum:root` |
| Union order of incoming keyIds | invariant sorted set |
| Invalid list signatures | `incoming-signature:revocation:RJ-4 ENVELOPE_MISMATCH` |
| Namespace entry | admits; union `[]` |
| Extra other-root with bad old signatures | admits; `unresolvedRootPairs=['other-root.json']` |
| Bad list calendar / wrong `rootVersion` | `revocation-body-shape-or-calendar` / `revocation-root-binding` |
| Shared budget | 14 / 40 / 18414 |

No native exploit is claimed by the five omission controls.

---

## Remaining (do not count closed)

Retained revocation population custody/completeness; other-root chain/ancestry admission; catalog/component/policy/artifact body identity and signature semantics; namespace/release/catalog revocation role semantics; held-root floors/S4 time; command/role/batch and native publication. Zero unresolved paths is not a staging grant.

---

## Verdict

- [x] Archive/pins/members verified. **35 / 5** reproduced. Production source identical across 34- and 35-case reports. Helpers 42+32 observed.
- [x] Finite incoming-key union after actual list ROOT quorum; second pass over all relied-on facts including the list and old RECOVERY. Extra roots stay unresolved, not authenticated history.
- [x] Independent probes: self-revoking list, retained∪incoming, order invariance, invalid list cannot supply union, namespace not a key, calendar/root binding, extra-root pending owner.
- [ ] **Not** full metadata/current/root-history admission, staging, or native authority.
