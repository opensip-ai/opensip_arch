# Independent review — pure registry codec 373

**Verdict: `ACCEPT-UNIT`**

Frozen **inert** complete-document registry + exact 92-byte PROJECT-ID-V1 marker decoder, intended identity placement. **Not** product source, **not** native custody/authority, **not** recovery/state machine, **not** S9.3, **not** five-field binding, **not** inventory/runtime selection. Placement advisory372 remains archived; this is not that producer/DAG decision relabeled.

Archive `3eaea6a1…808b2` / **29364 B / 143 members**; every subject member rehashed (0 mismatches). Codec `project_registry.rs` `f3bb0fb6…48fe5` / 10940 B. Selected owner/schema/model pins `14181ef7…` / `b9c1a19a…` (registry-selection-v1, product `2e90e02`, arch `90eb0f881`). Parent identity rlib `0155345b…` / 11802200 B verified before compile. Priors unchanged.

---

## Code vs selected owner (not only hashes)

`no_std` / `forbid(unsafe_code)` harness; values are typed getters only. `Registry::decode` admits the **whole** canonical document or nothing: closed `{schemaVersion:1, entries}`, cap 4 194 304 / 4096 rows, extra members refuse, then **canonical_bytes == raw**.

- **N order:** every consecutive pair must be **strictly increasing** (`>=` refuses), all statuses, so duplicate N cannot hide in RETIRED/ABANDONED.
- **Live uniqueness** only for `RESERVED|ACTIVE`: ProjectId, (platform,path), incarnation. Terminal rows may repeat PID/locator/incarnation; they may **not** reverse N order.
- **Both** `allocationKind` values decode; `lose-adoption-kind` fault is detected.
- **u64** device/inode: shortest decimal, no `+`/leading zeros except `0`, 0..=2^64−1.
- **i64** birth seconds full range; nanos 0..=999_999_999 as JSON integers.
- **Path:** hex → bytes starting `/`, no NUL, no `//`, no trailing `/` except root, no `.`/`..` components, hex length ≤ 8192.
- **Marker:** 92 bytes, prefix `opensip-project-id-v1\n`, `prj1-`+64 lower hex, final LF. Prefix-length fault detected.
- **Projection:** `registered_namespace_values` is ACTIVE∪RETIRED **values and order**; `has_reservations` is separate and is **not** the S9 start gate (RESERVED documents still decode). Probe asserts getter reconstruction equals canonical input.

This matches selected `registry_model.py` **decode/validate** law. It does **not** implement reservation, adoption completion, leases, or start-gate refusal — correctly out of codec scope.

---

## Independent replay

Compiled **from frozen extract** with rustc 1.95.0 + pinned identity rlib (not a whole-workspace build). `check_differential.py --probe` in a fresh output path: **37412** cases, **0** failures, corpus `eb30a71c…2b00` and outcomes `7a94a242…f945` **equal** author r2. Counts 13852/23560 registry/marker, 1638/1052 accepted.

Nine compiled semantic faults, each rebuilt and re-run: extra fields, duplicate N, live PID/locator/incarnation uniqueness, 4097 rows, lost adopt kind, marker prefix length, wrong projected namespace **all detected**. Extract `differential-r2.json` not overwritten. Author first artifact-directory miss never invoked the compiler (retained note).

---

## Residuals (not requiredFindings)

Product join must rebuild against current identity if that rlib is not the live crate. Physical move into `crates/identity` is a later byte-preservation/inventory unit. Codec must not be treated as native admission.

---

## requiredFindings

None.
