# Bounded investigation — retained DocRef byte-length joins (252/258)

**Standing:** contract probe of reviewed 252/258 `_prepare`, not approval of unfinished native 264, not source selection, not current authority. 263 review (`ba7895f5…dca9`) and earlier reports were not edited. The 264 worktree was not reviewed or mutated. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`, Unicode 15.0.0, OpenSSL 3.6.3. Live Ed25519. New keys and reports only under this directory. Frozen 252 fixtures were not overwritten.

---

## Answer

A coherent raw SHA with a **wrong** `DocRef.envelope.bytes` on catalog, revocation list, or a non-replacement root **currently admits** `Operation.recovery_payload` / `_prepare`. That is a **retained-inventory honesty gap** at the existing SHA join, not a grant of current trust, and not an explicit deferral to the complete-graph walker.

Authorize, replacement, and payload/manifest envelopes **do** refuse the same lie, because `read_doc` loads both BlobRefs through `Budget.load`. Catalog/list/other-root **bodies** also refuse, because those BlobRefs are placed in the retained path map and loaded.

Closed `BlobRef` schema (`bytes` any integer 1..4194304, independent of `sha256`) is not itself a join.

---

## Pins (read-only)

| Subject | Bytes | Members | SHA256 |
|---|---|---|---|
| Frozen 258 `command-policy-composition-reference-wip-258-r1` | 18830192 | 1586 | `b36518ef3e96a911c77f5ab7eb818e98011d47e3f5f7679501b2d00efc90f622` |
| Frozen 252 r2 `retained-payload-binding-wip-252-r2` | 20908 | 211 | `3816972f605d83c566f6cefef4caf580b9b3fe46bf8d1354f1193e91e2e8ccff` |

Live tar SHA/bytes/members matched both pins. Probe used the exact local 258 candidate. 258 `trust_payload_reference.py` SHA256 `eb5a70792cf9d9ef7ee624c7ad07e6def91bb3e44e06f41b9f6b860a05d1bb5d`. Nested 252 helper `f6403a406f175528f9d02230b3d19c7f78a635cfc3b154a6581fd144b841edaf`. Bind/join in 258 `_prepare` is the same SHA-only algorithm as 252 `_prepare` (258 drops the public `prepare` wrapper; `Operation.recovery_payload` is the owned entry).

---

## Source ownership (258 candidate)

`bind(row, ref)` (payload helper lines 34–36) requires `row['sha256']==ref['sha256']` only. Catalog/revocation bind the **body** BlobRef into `paths` (line 39). Root-chain bind is also body-only (line 38). Envelope DocRefs for those documents are kept on `docs` for a later SHA compare.

After index `select`, line 62:

`hashlib.sha256(pair['body']).hexdigest()==doc['body']['sha256'] and hashlib.sha256(pair['envelope']).hexdigest()==doc['envelope']['sha256']`

Reason `retained-document-envelope-binding`. **No `bytes` field is read.** Envelope bytes for catalog/list/other-root are captured from `members.envelopes` slot blobs via `paths`, not from `DocRef.envelope`.

`A.read_doc` (`trust_authorization_reference.py` 25–27) loads `ref['body']` and `ref['envelope']` through `input_work.load` → `Budget.load(..., length=reference['bytes'])`. `_prepare` uses that for `closure['manifest']`, and `op.authorization` uses it for the RA DocRef and the caller `replacement_ref`.

Final `for path,ref in paths.items(): op.input_work.load(...)` (line 67) re-loads path refs: bodies plus slot blobs. It does not load catalog/list/other-root `DocRef.envelope`.

`Budget.available` **does** compare declared `bytes` to a cached object (operation-reference-bytes). Graph `Work.load` always compares `len(raw)==reference['bytes']`, including cache hits. `_prepare` never calls `op.walk`. 258 command-metadata composition also does not walk the closure.

Payload pending owners are catalog/list **member body and signature admission**, revocation union, artifact custody, held-root/S4, command effects, native publication. None of those is “join `DocRef.bytes` to captured pair length.” 253 leaves non-replacement roots **unresolved** (SHA vs replacement only); that is authentication, not this length join.

Signed inventory rows are `{path, sha256}` only. `bytes` lives on closure `DocRef` / slot `BlobRef`.

---

## Probe

Script: `probe_docref_length.py` (SHA256 `23f5b030e6ff6c39566754ba5fd45014b88715916c13fc2080835a131e7d498f`). Report: `probe-report.json` (SHA256 `26754067e8870c75ff3f8c35181a99718de16e66cfd16f685b9df4d8b5fdcd70`). 18 live cases. Fixture construction follows 252 `check_payload.fixture` (actual crypto, synthetic catalog/list/component **bodies**).

**Harness coincidence:** 252 `fixture()` aliases `closure['catalog']['envelope']` with the envelopes-slot blob (same dict). Mutating `bytes` on that shared object also poisons the captured member ref and refuses `operation-reference-bytes`. That is not the contract. The probe copies BlobRefs so the DocRef can lie while the slot blob stays correctly sized — allowed by schema and by `_prepare`.

| Case | Result |
|---|---|
| Baseline; baseline + held other-root | admit, standing `authenticated-recovery-bundle-and-retained-inventory-only` |
| Catalog `envelope.bytes` = actual+1, 1, or 4194304 (SHA unchanged) | **admit** |
| Revocation (list) `envelope.bytes` +1 | **admit** |
| Other-root (held, not replacement) `envelope.bytes` +1 | **admit** |
| Catalog / revocation / other-root **body**.bytes +1 | refuse `operation-capture-unavailable` ← `operation-reference-bytes` |
| Replacement / authorization / manifest `envelope.bytes` +1 | refuse `operation-reference-bytes` via `read_doc` |
| Catalog.sig **slot blob** `bytes` +1 | refuse `operation-reference-bytes` (this is the captured envelope) |
| Catalog `envelope.bytes` = 0 | refuse `shape:PayloadMetadataClosureV1` (schema, not join) |
| After catalog-envelope lie admits: same-op `Budget.load` of that DocRef.envelope | refuse `operation-reference-bytes` |
| After admit: fresh or same-op `walk('PayloadMetadataClosureV1', ...)` | refuse `operation-reference-bytes` |

So: inventory SHA-joins the envelope digest and ignores envelope length for catalog/list/other-root; any actual load of that lying BlobRef would refuse; `_prepare` simply never loads it.

---

## Graph vs inventory vs authority

Complete-graph walk **would** refuse the lie **if invoked**, because FULL extraction of `PayloadMetadataClosureV1` includes every `DocRef.envelope` BlobRef. That is incidental. Recovery payload does not walk, does not list graph as the owner of this join, and already claims only `authenticated-recovery-bundle-and-retained-inventory-only`. This is not current authority, staging, or catalog/list member admission.

---

## Smallest correction (do not implement here)

Authoritative 252/258 reference, existing reason `retained-document-envelope-binding`, after `index.select`:

`len(pair['body'])==doc['body']['bytes'] and len(pair['envelope'])==doc['envelope']['bytes']`

in addition to the two SHA equalities. Compare against **already captured** pair bytes. Do not depend on a later `Budget.load` of `DocRef.envelope` (easy to skip, as today) and do not invent a new refusal token.

Native requirement, if 264 continues to mirror 252: the same length equalities on the captured pair vs the closure DocRef. 261 already bounds both `SignedDocument` inputs by declared size before parse; this join is the inventory analogue for catalog/list/other-root DocRefs that 252 never `read_doc`s. Do not treat 236/258 graph walk as a substitute. Do not implement until root reconciles a coherent 252/258/native change.

This is DocRef honesty for a BlobRef that already has both fields, not a new catalog/list body-schema law (that owner remains pending).

---

## Out of scope

Unfinished 264 candidate/worktree; product/repo/history; frozen 252 fixture regeneration; cumulative protocol approval.
