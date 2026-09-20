# Independent review — retained payload / prospective BUNDLE 252 r2

**Standing:** bounded code review of frozen `retained-payload-binding-wip-252-r2`. **Not** complete metadata admission, staging, BEGIN/COMMIT, current trust, command-to-closure binding, or native effect authority. Archived 251 (`1d4d9875…0dce`) and 250 (`35576c02…c75f`) reports were not edited.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Siblings reconstructed from verified 251 r1 and 250 r2 extracts (plus 248/215/225 for the 250 crypto helper). Frozen fixture/variant directories were not overwritten. Optional `check_payload.py` fixture-output path used.

---

## Verification

Frozen archive: **20908 B, 211 members, SHA256 `3816972f605d83c566f6cefef4caf580b9b3fe46bf8d1354f1193e91e2e8ccff`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed 211/211. Standing: Incomplete WIP, not approval or source selection.

`payload_reference.py` SHA256 `f6403a406f175528f9d02230b3d19c7f78a635cfc3b154a6581fd144b841edaf`. `inputs.json` pins 251 `Operation` `15f43788…dbb6`, helper `dfff1a05…7653`, envelope `ea06a785…69d1`, payload2 schema `47bc09e5…f473`.

Included keys are **TEST ONLY**. The 250 helper still runs its own **42** cases while minting those keys.

---

## What 252 authenticates

`prepare` requires an actual 251 `Operation`. R2 validates `closure_ref` as a **closed NodeRef** (`M.I.shape('NodeRef', closure_ref)`) **before** capture. Typed load is `PayloadMetadataClosureV1` with `scope == recovery-full-signed-scope`. Nominated `replacement_ref` must be a `DocRef` **in** `closure.rootChain`.

Then: capture manifest body/envelope; closed payload2 schema; explicit manifest authorization hashes joined to the closure; 251 `op.authorization` (actual RA/replacement signatures); verify `payload.2` with the **authorized prospective** TR-BUNDLE keys and the supplied revocation-filtered quorum. No old-key fallback; no caller signer set. Held authority / complete revocation union remain 250 asserted inputs.

Signed inventory is joined to retained root-chain cardinality/body hashes, catalog/list DocRefs, RA, per-slot envelope/manifest/policy sets and UTF-8 path order, repair presence/absence, and artifact observation set/order/hash. Shared metadata index enforces declared envelope reads, portable path aliases/file-parent rules, pairing/preimage/ambiguity. Each closure DocRef envelope must equal the selected pair. Policy/repair bytes are captured. A second `root-recovery-authorization` envelope refuses (`extra-authorization-envelope`, 215). Other unselected listed envelopes stay shape/hash-retained and confer no authority; this slice does **not** add a blanket unpaired-envelope refusal.

Artifact `observedBytes`/custody remain asserted; artifact bodies are not recaptured. Fixtures use incomplete synthetic catalog/list/component bodies while payload/RA/root/BUNDLE crypto is real. Success does not license staging.

Standing `authenticated-recovery-bundle-and-retained-inventory-only` with six pending owners (catalog/list/member body+signature admission; complete current/incoming revocation union recheck; artifact capture/custody; held-root ancestry/floors/S4 time; command input and role/batch effects; native publication census/durability).

---

## R2 closed-reference regression

R1 `payload_reference-before-closed-reference.py` had **no** `NodeRef` shape on `closure_ref`. `before-closed.stderr` records the expected failure: extra member on `closure_ref` was **admitted** (`AssertionError: ('admitted', 'closed-closure-reference')`). R2 adds `M.I.shape('NodeRef',closure_ref)` plus two tests (`closed-closure-reference`, fail-stop). Independent probe: `extra=True` now refuses `shape:NodeRef`. The `reference` omission control removes that line and admits the extra-field pair. R1 source/tests/results remain in the archive. This is a closed API-root gap, not store migration.

---

## Reproduction

Fresh `payload-fixtures-live` and work-copy `variant-fixtures-r2` / `payload-variants-r2`. Frozen r1/r2 fixture dirs were not overwritten.

| Corpus | Result |
|---|---|
| `check_payload.py` | **32/32** equal frozen `payload-fixtures-r2/payload-report.json` |
| Counters | objects **14**, edges **40**, bytes **18329** |
| `check_variants.py` | **8/8** core-equal frozen `payload-variants-r2/results.json` |

r1 had **30** cases / **7** controls. r2 adds the two NodeRef cases and the `reference` control. Variant path SHA differs from local `S=Path` rewrite.

---

## Independent probes

| Probe | Result |
|---|---|
| Extra member on `closure_ref` | `shape:NodeRef` |
| Catalog envelope swapped onto authorization envelope | `retained-document-envelope-binding` |
| Old-root TR-BUNDLE keys | `bundle-signature:RJ-4 ENVELOPE_MISMATCH` |
| Short prospective BUNDLE quorum | `THRESHOLD-SHORTFALL` |
| Two of three BUNDLE keys revoked | `bundle-filtered-quorum` |
| Second RA envelope | `extra-authorization-envelope` |
| Unlisted store bytes | still admits (not candidates) |
| Artifact `observedBytes=999` | admits; pending includes artifact-capture-custody |
| Cross-slot portable alias `CATALOG.JSON` | `member-path-alias` (234-style index) |
| Shared budget | 14 / 40 / 18329 |

Emptying `rootChain` to test membership hits `shape:PayloadMetadataClosureV1` first (closure schema). Membership `replacement-not-in-retained-root-chain` remains in production after closed NodeRef/DocRef/typed closure. Command-to-closure semantic binding is **not** implemented.

**Scope vs 215/234/251:** required per-slot/order/artifact-hash joins and the single extra-RA rule are in this slice. Artifact **body** capture, full catalog/list/component schema/identity/signature, second-pass incoming union, and unpaired-envelope blanket refusal are correctly left pending / not invented.

---

## Remaining (do not count closed)

Catalog/list/member body and signature admission; complete current and incoming revocation union recheck; artifact capture/custody; held-root ancestry/floors/S4; command-to-closure join and role/batch effects; native publication. 252 does not stage.

---

## Verdict

- [x] Archive/pins/members verified. **32 / 8** reproduced. 250 helper 42-case key mint observed. Production `f6403a40…edaf`.
- [x] Prospective BUNDLE signatures on payload.2 plus retained inventory/index joins. R2 NodeRef closed-reference regression is real (r1 admitted extra members; r2 refuses and fail-stops).
- [x] Independent probes refuse old/short/revoked BUNDLE, extra RA, pair mismatches, path aliases, and open `closure_ref`. Artifact size stays asserted. Unlisted bytes are not candidates.
- [ ] **Not** complete metadata, current trust, staging, command-to-closure binding, or native authority.
