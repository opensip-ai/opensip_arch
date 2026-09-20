# Independent review — component inventory body 293

**Standing:** bounded native-Rust review of frozen `native-component-inventory-checkpoint-293`. This implements the 291 `INERT-IDENTITY` inventory-shape vs host-admission split and composes it with 292 `prepare_shared`. Component DR-112 authority, host admission, ROOT admission, T1 scope, and operational trust remain **pending**. Installed product remains `fa72e50`. Keys are **TEST ONLY**. Archived 292 was not edited.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/result directories were not overwritten. No workspace rerun (284's 529 is predecessor).

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **8201436 B, 915 members, SHA256 `7a8555d3b8a7dd4fc5bcc16d0f40d18f3c5b08fd64757a7826eef29e153f9528`**. Standing: unselected private293 body/catalog phase with pending component authority and ROOT admission. Extract rehashed **915/915**. Product-inputs **444/444**. Nested parent 292 pin `554c8321…9ea8` equals reviewed 292; live 292 trial tar matches. Nested 265 `73c3b3f5…86df` live-matches. Oracle `check_manifest_completed_v1.py` SHA256 `48951bd4…7f7a` matches the request. Product vs 292: **444** files, **440** unchanged. Changed: `component_manifest.rs` `090ea074…65f8`, `trust_ordinary_metadata.rs` `a7616d0f…1241`. Added: `inventory293.ndjson`, `inventory293-signed.ndjson`. `trust_ordinary_quorums.rs`, `shared292.ndjson`, `metadata285.ndjson`, and `component_manifest_shape.rs` byte-identical to 292. Not in `lib.rs`.

---

## Inventory-body vs host-admission (INERT-IDENTITY)

Distinct `InventoryBody` and `Validated`. No conversion either way without running the matching validator. Shared `validate_inner`:

**Always (inventory-shape):** closed parse/schema; command grammar; reserved-name collision against **catalog** reserved names; platform/tree/entrypoint; capability/permission/dependency uniqueness; in-body `hostCore` nonempty + schema-version match; configuration namespace/key-shape and `config_ranges`; prerequisite **path** and **duplicate** refs; declaration path / typed-absence binding to those refs.

**Only when `Context` is `Some` (host-admission):** `approved_exceptions` membership; live-name collisions; exact `host_classifications` agreement. `validate_inventory(raw, reserved_names)` passes `context=None` and does **not** synthesize approvals. Full `validate(raw, &Context)` still runs the 285 host path.

This matches the recommended split: do **not** silently omit HostContext inside the full 285 function; keep intrinsic body rules on the inventory side.

`ordinary_metadata::inventory::prepare` uses the **same** Budget and `Q::prepare_shared` (292). Then full `recovery_catalog::validate`, then every `pending_components` path through `validate_inventory`. Joins: catalog 4-tuple; `envelope.namespace == provenance.publisher` (identity, **not** key delegation); raw body / canonical preimage / envelope digests; exact `hostCore` vs catalog `hostCoreConstraint`; catalog reserved names. Groups never include Manifest authority. Shared BUNDLE/catalog/list signatures remain mandatory. ROOT pairs stay unresolved via SharedEvidence.

Original `ordinary_metadata::prepare` still calls full 284 `C::prepare` + `F::validate` with actual HostContext. That test still runs.

301 body cases: **98** inventory-valid, **57** host-valid, **41** inventory-only, **0** host-only (host-valid ⊆ inventory-valid). 42 signed cases, **11/11** positives. Baseline **12/31/19295**; repeat **12/62/19295**; **12** captures. Catalog `envelopeDigest` is taken from the actual (including deliberately altered) component envelope **before** catalog signing, so bad-crypto isolates authority from digest mismatch. Undelegated matching publisher passes inventory; mismatching namespace/body or catalog digest/semantic defects refuse.

**Failed attempts (inspected, preserved):**

1. `security-body-r1`: test-only `crate::metadata::parse` → **E0433** (`component-manifest-before-test-import-fix.rs` retained). Production `validate_inner` already used `super::metadata::parse`. Test path corrected; algorithm unchanged.
2. Mutation r1 `full-live-name-check-skipped` replaced the live-name iterator with `&[][..]` → **E0282** type inference (`expectedOutcome` false). r2 uses `context.filter(|_|false).map_or(...)` in the **mutant only**, compiles, and is a wrong host-admission skip. Production bytes unchanged. Both r1/r2 dirs retained.

**Executed:** `cargo clean -p opensip-security` then **240/240** with `Compiling opensip-security` (includes 285 full catalog/component test, 292 shared test, new inventory-body and inventory-join tests). Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **nine** include files. r1 15 compiled + 1 compile-fail core-equal frozen `mutation-check-r1`; r2 single live-name control core-equal frozen `mutation-check-r2`. Frozen dirs not overwritten. Live baseline cargo skipped; unpatched `component_manifest.rs` SHA matched frozen baseline `090ea074…65f8`.

**Controls (16 compiled across r1+r2):** 13 wrong conditional acceptances — host skips (`full-host-approval-skipped`, `full-host-classifications-skipped`, r2 `full-live-name-check-skipped`); intrinsic skips (`inventory-reserved-names-skipped`, `intrinsic-config-key-shape-skipped`, `intrinsic-config-ranges-skipped`, `intrinsic-prerequisite-duplicate-skipped`, `intrinsic-path-tree-skipped`); inventory-join skips (`inventory-namespace-join-skipped`, `inventory-body-digest-skipped`, `inventory-preimage-skipped`, `inventory-envelope-digest-skipped`, `inventory-hostcore-join-skipped`). 3 other-first: `inventory-identity-forced-first-release` (panic index 0), `inventory-empty-component-list`, `inventory-semantic-failure-not-latched`. Not operational exploits.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 293 pins before extract | match |
| Nested 292 / 265 live tars | match |
| 265 manifest oracle SHA | `48951bd4…7f7a` |
| Live `cargo test -p opensip-security` | **240/240** after force rebuild |
| Clippy / fmt / rustfmt 9 includes | pass |
| 293 r1 mutants | 15 compiled + 1 E0282 frozen-equal; 12 wrong / 3 other |
| 293 r2 mutant | 1/1 frozen-equal; compiles the 13th wrong host skip |
| Workspace | not rerun (284 529 predecessor) |

---

## Remaining (do not count closed)

Component DR-112 for relied-on T1 members; 289 ROOT chain; current vs BEGIN/OLD/population; 291 context-to-T1 composition; signed time/minima/role effects; host-admission as a later gate; durable custody/fence/census/writers; source selection; M3–M6. 293 is not shipped behavior or cumulative approval.

---

## Verdicts

- [x] **293:** archive/pins verified; inventory-body vs host-admission split matches INERT-IDENTITY without relaxing intrinsic rules or the full 285 host path; composed with 292 SharedEvidence; catalog identity/digest/hostCore/reserved joins held; E0433 and r1 E0282 preserved honestly; 13/3 mutant classification plus r2 live-name catch; 240/240, Clippy, fmt, 9-file rustfmt.
- [ ] **Not** T1 gate, component authority, ROOT/current-head admission, host installation, or product installation.
