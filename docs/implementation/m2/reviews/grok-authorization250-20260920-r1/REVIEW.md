# Independent review — recovery authorization reader 250 r2

**Standing:** bounded code review of frozen `recovery-authorization-reader-wip-250-r2`. **Not** cumulative approval, current trust/activation, BEGIN/COMMIT, native command authority, store migration, or full payload/BUNDLE quorum. Archived 247 and 248/249 reports were not edited (`d5a7d732…4984`, `c407f4f4…b15c`).

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Sibling names reconstructed from the verified 248 r1 extract plus pinned 215/225 owner prose (archive `owner-inputs` byte-identical to those pins). Frozen variant/check output directories were not overwritten. Hardcoded `/tmp/opensip-implementation/m2-command-composition-reference-248/...` was redirected in the review copy.

---

## Verification

Frozen archive: **35248 B, 117 members, SHA256 `dbf1aa27eda8c4434e4fbf0f005e9bffadab7288d9ac71bc55b33d2b854ecf85`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed 117/117. Standing: Incomplete WIP, not approval or source selection.

`authorization_reference.py` SHA256 `6b6f0fb25577b255a37589806945de647bb12fa1eed14c38b08b749fe5c03353` — **byte-identical to r1**. r2 only adds three schema-pair positives in the test grid (`check_authorization-before-schema-grid.py` retained). Accepting signed root bytes across schema 1/2 is not store migration or entry eligibility.

`inputs.json` pins match reconstructed siblings: 248 `envelope_reference.py` `ea06a785…69d1`, `trust_operation_reference.py` `bf92db33…fb3b`, RA schema `527f8552…412a`, 215 OWNER `780a6dd5…0d60`, 225 TIME-PRODUCER `804134cd…0843`.

Generated keys in the archive and live rerun are **TEST ONLY**.

---

## What 250 r2 authenticates

Same 248 `Operation` captures **both** authorization and replacement body/envelope `DocRef`s (four objects). Closed seven-field RA body (`authorizationSchema`, `kind`, `authorityRoot`, `replacementRoot`, `recoveries`, `issuedAt`, `notAfter`); recoveries UTF-8 sorted. Held and replacement roots must `admit_root_document` for schemas (1,2).

`RootBinding` is `{rootSchema, rootVersion, rootDigest}` where `rootDigest` is the existing domain-separated `opensip.metadata.root.{1|2}` digest, **not** raw file SHA-256. Probe: raw SHA ≠ domain digest; substituting raw SHA as `authorityRoot.rootDigest` refuses `held-authority-root-binding`.

Existing `Verifier` derives actual signers (no caller signer set): held **RECOVERY** on the authorization, replacement **self-ROOT** on the new root. Required sorted unique `revoked_keys` filters **both** verified quorums; each remainder must meet threshold. Empty list is a TCB assertion (`complete-current-revocation-union` stays pending), not evidence of no revocations. Unsorted/duplicate lists refuse `revocation-population-shape`.

Standing `authenticated-authorization-and-replacement-only` with **six** pending owners: held-authority selection/custody; complete current revocation union; accepted ancestry and store floors; full payload closure and bundle quorum; S4 current time and activation; role/batch and durable publication. No state write, stage, BEGIN, or COMMIT.

This module imports 248 `trust_operation_reference.Operation` itself. Primary relocation must keep **one shared Operation identity** when composing with delivery; that integration is **not** present here.

---

## Window and version vs 215 / 225

Implemented structural predicates:

- `replacement.rootVersion > authority.rootVersion`
- `held.issuedAt <= replacement.issuedAt`
- `replacement.issuedAt <= RA.issuedAt < RA.notAfter <= replacement.expiresAt`

**Fit:** 215 says the authorization window must lie in the replacement root’s validity interval; old authority expiry does **not** by itself prevent verification of this authorized replacement; `issuedAt <= tEval < notAfter`, floors, TRUSTED-entry, and catalog/list currency are **COMMIT** predicates. 225 says replacement needs higher version, `issuedAt >= authority.issuedAt`, and that old authority expiry is not consulted to authenticate this authorization; `tEval < notAfter` and replacement expiry as entry guards remain COMMIT/S4.

250 matches that split: expired held authority **admits**; API has **no** `tEval`; current time/floors/ancestry are pending, never inferred from the signed pair. Do not read a successful 250 result as COMMIT eligibility or current authority.

---

## Reproduction

Live run used `--output` under `grok-out/io/check-r2-live` and a fresh work-copy `authorization-variants-r1` / `variant-fixtures-r1`. Frozen `check-r1/`, `check-r2/`, and `authorization-variants-r1/` were not overwritten.

| Corpus | Result |
|---|---|
| `check_authorization.py` | **42/42** equal frozen `check-r2/report.json` (source `6b6f0fb2…3353`) |
| Positive counters | objects **4**, edges **4**, bytes **10180** |
| `check_variants.py` | **7/7** core-equal frozen variant results (path SHA differs from local `S=Path` rewrite) |

r1 had **39** cases; r2 adds `actual-root-schema-pair-1-1`, `1-2`, `2-1` (with the original schema2/schema2 case covering all four pairings). r1 `sourceSha256` is the same production bytes. r1 seven controls still bind that source.

---

## Independent probes

| Probe | Result |
|---|---|
| Domain digest vs raw SHA as `rootDigest` | raw ≠ domain; raw substitution `held-authority-root-binding` |
| Invalid held root (no `rootKeys`) | `authority-root-shape` |
| Schema pair 1/2 | `authenticated-authorization-and-replacement-only` |
| Unsorted / duplicate `revoked_keys` | `revocation-population-shape` |
| Empty revocation list | admits; pending includes `complete-current-revocation-union` |
| Incomplete incoming-union (omit revocations) | still admits if threshold remains |
| Four-member shared budget | 4 / 4 / 10180 |
| Missing auth body / fail-stop | `operation-capture-cap` then `operation-budget-closed` |
| Expired held authority | admits |
| Signed role-order / bad calendar | `authorization-role-order` / `authorization-calendar` |
| Replacement signed with old ROOT keys | `signature-carrier:RJ-4 ENVELOPE_MISMATCH` |
| `tEval` / caller `signers` parameters | absent |

No native exploit is claimed by the seven omission controls (crypto, revocation filter, held binding, replacement binding, window, version, shared accounting).

---

## Remaining (do not count closed)

Held-root selection/custody; complete current revocation population / incoming-list union; ancestry and store floors; full payload closure and BUNDLE quorums; S4/tEval/activation; role/batch/durable publication. 250 does not stage or COMMIT. Sharing one `Operation` with 247/248/249 delivery is future composition.

---

## Verdict

- [x] Archive/pins/members verified. **42 / 7** reproduced. Production source identical r1/r2; r2 adds three schema-pair positives only.
- [x] Actual Verifier-derived Ed25519 quorums (held RECOVERY, replacement self-ROOT) plus domain-separated root bindings, closed RA shape, UTF-8 role order, structural 215/225 window/version, and revocation filtering after verify. Expired held root is intentionally not a reject. Empty revocation list is an assertion.
- [x] Independent probes refuse raw-hash bindings, bad root shape, malformed signed calendar/role order, old-root signatures, unsorted revocations, missing captures, and fail-stop. Counters 4/4/10180. Current authority is not inferred.
- [ ] **Not** current trust, COMMIT eligibility, full payload/BUNDLE authentication, native custody, or delivery composition.
