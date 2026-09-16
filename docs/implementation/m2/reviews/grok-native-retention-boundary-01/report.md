# Advisory: NativeRetention vs `open_run_closure` nested frame walk

**Reviewer:** Grok. Root remains lead. **Not** ACCEPT-DESIGN-UNIT, not frozen, not runtime-02, not Plan/Run/replay.
**Work tree:** `/tmp/opensip-implementation/m2-grok-native-retention-boundary-01/review`. Did not edit trial-13, live, frozen, or history.

## Sources read

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| trial-13 `native_universe.rs` | 44549 | `a3bd2f5f…9269` |
| trial-13 `lib.rs` | 919 | `e61bba0b…cd6e` |
| trial-13 `native_context.rs` | 15809 | `c16fe03d…8a2e` (unchanged vs 09) |
| trial-13 `identity-v3.schema.json` | 197480 | `311c1feb…b68f` |
| trial-13 `native-v2.schema.json` | 280357 | `e5834d37…7773` |
| selected `identity_model.py` | 158555 | `619d6e3c…41e6` (`open_run_closure` ~909; nested `snapshot_joins`/`path_values`/`admit_frame` **1557–1642**) |

Registry rows used: `domainSets.native-context` / `native-semantic-universe` / `native-nested` in identity-v3. `NativeFrameSet::name()` is `native-context` / `native-semantic-universe` / `native-nested`.

## What the walker actually is

`inspect_native_retention(inputs, digest, set, snapshot_id, budget)` rehashes one **explicit snapshot**, then walks **one** registered native root:

| Root | Retention walk (row-driven) | Owner after walk (not memoized) |
| --- | --- | --- |
| `Context` | snapshotJoins, blobJoins, nestedRecords (raw C), nestedIdentities (H / `native-nested`), closureJoins (kind + manifest + **tree bytes**) | `inspect_native_context` — refusals → `Refused` |
| `SemanticUniverse` | same, then **visits named context** via `contextField`/`sha256-text` | `inspect_{syntax,typescript,rust}_universe` (context owner runs **again** inside the binder) |
| `Nested` | same joins; **no** native binder | none |

Counts only (`frames`/`blobs`/`closures`). Not Plan-selection, grant, metadata-security, or `close_run`. General identity-walker native joins stay Unsupported until later composition.

Memo: `frames` skips **join traversal** on re-entry; **context/universe owners still run**. Closure **kind is checked on every join** even if the closure id is cached (stricter than `visit()`, which returns immediately when `key in seen`).

## Matches `admit_frame` (keep)

- `path_values` `[]` vs field steps, including empty path `[]` on `native.cargo-config-projection.v2` blobJoin.
- Nested **raw** `canonical-record` vs nested **H** `sha256-text` / `bare-hex` + `domainSet=native-nested`.
- `nullable` Null skip vs `Law` when required.
- Snapshot `inventoried-paths` (optional `pathField`) and `inventoried-path-and-digest`.
- Frame `blobJoins` with optional `lengthField` → `require_length` / `BlobLength` (file-manifest `byteLength`, prepared-output row blobs).
- Closure `closure2-identity` vs `closure2-suffix`; tree members hashed with `bytes`.
- Universe does not treat missing nested blobs as binder `Ok(None)` — missing is `MissingBlob` (closer to `canonical_bytes`/`blob()`).

## Missing obligations / false-claim traps (actionable)

1. **Oracle ≠ three nested functions alone.** `admit_frame` does **not** call `bind_*`. Binding is later in `open_run_closure` (~1715–1737) and needs `admission`, merged `retained`, and `snapshotInventory`. Retention **universe** roots already call the binder. AST-extract `snapshot_joins`/`path_values`/`admit_frame` as the **frame-walk** oracle; keep **native binder as a second oracle**. Mixing them will mis-label binder field faults as retention faults.

2. **`visit()` memo is a bad closure oracle.** Reference skips kind on the second `closureJoin` to the same id. Retention re-checks kind. A dual-kind fixture (`toolchain` then `stdlib` on one id) must **fail retention** and must **not** be expected to fail a naive `visit` shim.

3. **Nested-record `blobJoins` have no `lengthField` in `admit_frame`.** Frame `blobJoins` do. TS `nodeModulesLayout` entry `contentSha256` is nested-record blobJoin **without** length. File-manifest lengths apply only after that nested **H** frame is admitted. Do not apply `lengthField` in the nested-record loop of a copied `admit_frame`.

4. **Rust `configProjectionSha256` is universe `nestedIdentities` `bare-hex` with no `retainedAs`.** Binder `inspect_rust_universe` only **rehashes** the in-descriptor projection; it does **not** `frame_candidate` that digest. Retention **does** require the Nested H-frame. A hash-matching projection **without** stored H-preimage must **fail retention / `admit_frame`**, not the binder-only API.

5. **Error classes are not `AdmissionError` strings.** Required Null → `Law`; inventory miss → `SnapshotPath` / `SnapshotSource`; owner refusals → `Refused`. Map them at the harness; do not expect `NATIVE_CONTEXT_PATH_NOT_INVENTORIED` from retention.

6. **Budgets.** `steps` decrements on frame/closure/blob/path expansion; `depth` is nested-frame depth; `descriptor_work` is copied into each `frame_candidate` / `inspect_current_record` and is **not** reduced by those calls. Rust universe → context → `packages[]/fileManifestSha256` needs **`depth >= 2`**. `inspect_current_record` using remaining `steps` as a **copy** does not consume walker steps.

7. **Binder `MissingBlob` → diagnostic missing is not retention.** `nested_record` / `nested_frame` in TS/Rust binders still translate `MissingBlob` to `None` + `…-missing`. Retention must not copy that. Shims: `blob`/`get` **raise** (or return hard missing), never skip.

8. **Do not claim member-blob authority from `inspect_native_context`.** That owner is still descriptor-only (`c16fe03d…`). Retention is what fetches closure **manifest + tree bytes** and nested member blobs. Counts are not “every snapshot blob retained.”

9. **Syntax/context roots still require a real snapshot object** even when `snapshotJoins` is `[]`. That is the isolated-API substitute for `run['snapshotId']`, not a Plan join.

10. **Out of scope (do not implement here):** `NATIVE_CONTEXT_SET_JOIN`, language-mode request, prepared-resolution **grant**, pruned-tree-not-a-read, fact/scope universe fields, capability/plan joins.

## Proposed independent negatives (small, no prior corpora)

1. Dependency file-manifest row `byteLength` ≠ blob length → `BlobLength` / `NATIVE_NESTED_MEMBER_LENGTH`.
2. Prepared-output row blob length mismatch (nested H, then `blobJoins`).
3. Closure tree `bytes` ≠ blob length; second `closureJoin` same id **wrong kind**.
4. TS context `lockfileIdentity` digest ≠ inventory (nullable null vs present mismatch).
5. Universe `configProjectionSha256` hash matches descriptor but Nested H-preimage **absent**.
6. `preparedOutputSetId` non-null, Nested blob missing → hard missing, not binder `…-missing`.
7. Extra unrelated blob does not change `{frames,blobs,closures}`.
8. Rust universe with `depth=1` Limits before file-manifest nested frames; `depth=2` proceeds.
9. `steps=0` or `depth=0` at API root → `Limit` before snapshot walk.
10. Nested record noncanonical JSON (parse ok, `canonical_bytes` differs).
11. `inventoried-paths` with `pathField` (`ownership.path`, `units.markerPath`) vs bare strings (`crateRootPaths`).
12. Syntax universe + well-formed snapshot with empty joins still **rehashes** snapshot; missing snapshot → `MissingObject`.
13. Same digest requested as `Context` vs `Nested` → two memo keys; Nested must not run `inspect_native_context`.
14. Universe binder refusal (e.g. cfg subset) after successful join walk → `Refused`, counts discarded.

## Advice to root (tests)

- Portable oracle = **extracted `admit_frame` + `path_values` + `snapshot_joins`** with in-memory `blob`/`get`/`closure visit`; **plus** a separate binder call for universe roots only.
- Closure shim: **kind on every join**, tree `sha256`+`bytes` on first insert only.
- `blobJoins` length only when the **join** has `lengthField`; nested-record blobJoins currently have none.
- Keep identity walker native joins Unsupported; do not teach retention to walk `run`.
