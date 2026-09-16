# Advisory: retained-closure implementation boundaries

Not a design-unit acceptance. Not runtime. Not M2 complete. No new architecture law. Did not read the in-flight runtime-unit review. Frozen/live/history not edited.

Work-map v2 already says: **schema/identity closure alone must never mint ReplayedRun.** Inventory v11 already names `crates/identity/src/closure.rs` as object/blob identity joins, **not** complete evaluator replay, and `crates/evaluator/src/replay.rs` as minting opaque ReplayedRun only after full replay.

## Source pins

| Document | SHA-256 |
|---|---|
| `identity_model.proposed.v3.py` | `5ba928968c4894b76d4b11d2798fadef9703e4a769cd7cbc3879bcde2ab25369` |
| `admission-work-map.v2.json` | `36921d1acc30399a3cc982fd6605b5a90c600633eaf31c0cf8a2f588ad9e413f` |
| `repository-file-inventory.v11.json` | `0ae9d43939f924a8cdd1b7926129063c24e59c55ae58f6a72c1633b890461f62` |
| `identity.v3.schema.json` (selected = current product) | `311c1feb09ff8cd0b207233d2ec0d7440bb1c72fc0470de277ee1891c24bb68f` |
| `evaluator_replay_model.v3.py` | `26e88580acff3d93e67f35cc5882b48b6238572cb2804abc01523b98cbc8ab0d` |
| exact-profile `canonical.py` | `ad88e58fe90fe66531dbe39f4694f20ad3bc6ce2099ae4fc762c0251468496f7` |

## 1. Who owns which rule

**`crates/identity/src/closure.rs` (pure, objects/blobs supplied)**

From `open_run_closure` **except** native/import/capability owner callbacks:

- `identifier` + `ordered` + exact-profile `validate` on identity `$defs`
- `get`: missing key → `EvidenceUnavailable` (promised bytes gone; operational, not a false predicate). Present but wrong domain or `identifier(domain,value)!=key` → `AdmissionError('REFERENCE_IDENTITY')`
- `blob`: missing → `EvidenceUnavailable`; not bytes or SHA-256 mismatch → `BLOB_DIGEST`; `{path,sha256,bytes}` length mismatch → `BLOB_LENGTH`
- `digest_field` from `x-opensip-digest` **only** (never `*Digest` names): `retention` ∈ {preimage, fragment, derived, owner-retained}; `representation` ∈ raw-artifact / capability-manifest-id / by-domain / h-identity / canonical-record
  - **preimage**: fetch and re-hash
  - **fragment / derived**: do not fetch here; later explicit join/recipe
  - **owner-retained**: digest equality only, **do not demand bytes**
  - **raw-artifact** + `artifactClass=registered-schema-document`: membership in the payload-registry document set, not “any retained blob”
  - **h-identity**: visit `PREFIX[domain]:hex` or parse **frame** (`opensip.product.v1\\0` + D + `\\0` + u64BE + C(X)). `C(X)` at an h-identity field is invalid (`H_FRAME_PREFIX`); `SHA256(C(X))` is not `H(D,X)`
  - **canonical-record**: local identity `$defs` vs foreign document+selector vs `payloadClass` registry row; decode of canonical bytes is memoizable, **admission is not** (context-sensitive)
- `admit_closure_field_kinds` from `x-opensip-digest-domains.closureKinds.byField` (regeneration-key uses cache-key field table)
- schema walk: oneOf digest branches must be unique (`AMBIGUOUS_DIGEST_BRANCH`); untyped digest arrays refuse
- current vs retained: current admission aliases vs **exact retained document bytes** for historical readers (work-map `modelRelativePaths`)

Identity crate DAG: **contracts only**. It cannot call native admission without a new package edge.

**`crates/evaluator/src/replay.rs` (+ atoms/composition/enumeration/proofs)**

- `close_run` / `replay`: first `open_run_closure`, then `reconstruct` + atoms + `compare_complete_replay`
- claimed findings/verdicts **never** feed reconstruction
- `CompleteReplayMismatch` on regenerated proof/evidence/seal/run
- mint **opaque ReplayedRun only** at successful complete boundary
- policy-derivation3 only from a completely replayed Run
- **Native context/universe/capability/import producer admission** that the Python monolith inlines inside `open_run_closure` belongs here or in `opensip-components` / host fact-admission — **not** in identity — because those packages may depend on identity, not the reverse. Work-map M2-A04 remaining already lists native contexts/universes on the replay owner.

**Host / storage / security (M2-A06)**

- Supply the `objects`/`blobs` maps (no identity I/O)
- CAS restore; `EvidenceUnavailable` is host-io when promised bytes are gone
- `cache_key` is **pure identity** (schema+order, no bytes). Host may compute it to miss cheaply. `admit_cache_entry` is **post-construction** and calls **`close_run` first** — not a pre-analysis API, grants no evidence authority
- `commit_inventory` is the commit-receipt digest; journal/SEAL/ledger stay storage/security
- Origin of `CompleteReplayMismatch` vs `RegenerationMismatch` is the **invoking host boundary**, not identity

Work-map A04 currently names only `replay.rs` for “retained structural closure”; inventory v11 already split `identity/closure.rs` vs `evaluator/replay.rs`. That is a **composition/owner-file** overlay to align at the next work-map successor, not a new law: the model comments and inventory descriptions already split the primitive.

## 2. First structural subunit (no ClosedRun / ReplayedRun)

Implement **`crates/identity/src/closure.rs`** as a **retained identity graph**:

- Inputs: domain-tagged object map + blob map + one identity-v3 document (exact bytes) + exact-profile validator
- Walk identity `$defs` digest annotations; enforce missing vs invalid; closure field kinds; local canonical-record payloads; registered-schema-document membership if the closed document set is passed in (not fetched)
- Output: opaque handle with resolvers (`get`/`blob`/`visit`) and **no** `Run`/`ClosedRun`/`ReplayedRun` type; no `pub` constructor from JSON that skips admission
- **Do not** call `close_run`, replay, native_admission, import correspondence, capability ADM-DOMAIN, `admit_cache_entry`, or `commit_inventory`
- **Do not** name the API `open_run_closure` until native/import/capability joins exist in **evaluator/components** on top of this graph

That is a complete first slice of M2-A04’s identity half. It is **not** the model’s public `open_run_closure` and **not** a ClosedRun.

## 3. Traps

| Trap | Law |
|---|---|
| Missing vs invalid | Absent promised object/blob → `EvidenceUnavailable`. Wrong hash/domain/identifier/kind → `AdmissionError`. Do not treat miss as `false` predicate |
| Frame vs canonical | h-identity stores **H-frame bytes** under SHA-256(frame). Payload stores **C(X)** under SHA-256(C(X)) |
| Schema vs identity | ExactValidator on the **row selector**; then `ordered()`. Generated carriers are inert |
| Current vs retained | Current aliases for live admission; historical Runs keep **exact retained document bytes**. No URI/major fallback |
| Cache | `cache_key` reads nothing. Hit admission needs a **constructed Run** via `close_run`. Shared cache-key schema with regeneration-key; H domain differs |
| Decode vs admit | Canonical payload decode memo; registry-row/universe/schema-digest admission **every** reference |
| Ownership | Identity must not grow a native/evaluator dependency. Native admission re-run is required for a **frame to count as admitted**, but that call lives outside identity |
| Minting | `closure2:` identity ≠ selected Plan role ≠ ReplayedRun |

## 4. Native-owner semantics

**Whole native-owner admission is required** before claiming the model’s **`open_run_closure`** (frame proves retention, never admission; capability hash ≠ ADM-DOMAIN admit).

**It is not required** before a public **structural graph** that does not claim Run/closure admission and does not call native.

Do not execute compilers to prove this map.

## Recommended tests (identity graph only)

1. Missing object/blob → `EvidenceUnavailable`; corrupt blob → `BLOB_DIGEST`
2. `identifier` mismatch → `REFERENCE_IDENTITY`
3. Put `C(X)` where h-identity is owed → `H_FRAME_PREFIX`; wrong H domain → unregistered/domain error
4. Closure field kind mismatch (`evaluator` vs `provider`)
5. `retention: fragment` / `owner-retained` does not require the digest in `blobs`
6. `registered-schema-document` raw-artifact not in the closed set → `SCHEMA_DOCUMENT_UNREGISTERED`
7. `cache_key` succeeds with empty blob map; `admit_cache_entry` is **not** in this crate
8. No `ClosedRun`/`ReplayedRun` symbols in `opensip-identity`
9. `not`/`anyOf` cannot invert schema-faults (exact-profile already)

## Limits

Did not run native/compiler/checkers. Did not read the runtime-unit review. Did not implement code. 40-schema generation map vs 48 admission inventory is a later composition (work-map already says bind current aliases separately).
