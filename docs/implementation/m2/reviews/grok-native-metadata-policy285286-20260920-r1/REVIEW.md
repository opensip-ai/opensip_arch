# Independent review — ordinary catalog/component semantics 285 and packaged policy 286

**Standing:** bounded native-Rust review of frozen `native-ordinary-metadata-checkpoint-285` and `native-ordinary-policy-checkpoint-286`. These continue 284 on the **same** Budget. They do **not** admit a current root/chain/history, adopt private policy, compute effective grants, or install product behavior. Archived 284 (`aa610b9a…4dbe`) was not edited. Installed product remains `fa72e50`. All root pairs remain unresolved. Keys are **TEST ONLY**.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/result directories were not overwritten. No workspace rerun (284's 529 is predecessor). One **232** security run on 286 covers inherited 285 tests; no separate 231 run was executed.

A separate integration assessment is in `ROOT-INTEGRATION.md`. It is **not** a 285/286 bounded verdict and does not implement or rewrite these candidates.

---

## Verification

**285** frozen archive: **5737936 B, 532 members, SHA256 `ee444e36e2128d1e1b681455ec19f7d5142e561bdcf34606d2202d70b65563aa`**. Pin/tar/members/subject hashes matched **before** extract; extract rehashed **532/532**. Product-inputs **430/430**. Nested parent 284 pin `adbdba19…122d` equals reviewed 284; live trial tar matches; `trust-before.rs` equals 284 `trust.rs`. Nested 265 `73c3b3f5…86df`. Product vs 284: **430** files, **427** unchanged, `trust.rs` `a3f05492…3b5b` plus `trust_ordinary_metadata.rs` `8ba0ad56…004e` and `metadata285.ndjson`. Not in `lib.rs`.

**286** frozen archive: **5755236 B, 526 members, SHA256 `9872efe37c9c497682604945e3228adf45a3376cac5155b5d010ca660040f3c4`**. Pin/tar/members/subject hashes matched **before** extract; extract rehashed **526/526**. Product-inputs **432/432**. Nested parent 285 pin `ee444e36…63aa` equals this 285 freeze; live 285 trial tar matches. `trust_ordinary_metadata.rs` byte-identical to 285. Product vs 285: **432** files, **429** unchanged, `trust.rs` `dca6e0d3…018d` plus `trust_ordinary_policy.rs` `b8bba542…b7bd` and `policy286.ndjson`. Not in `lib.rs`. 284/283 fixtures unchanged.

---

## 285 — catalog and component semantic joins

`ordinary_metadata::prepare` calls 284 on the same Budget, then requires **exactly one** retained Catalog pair. `recovery_catalog::validate` admits full closed shape, real calendar/positive validity, unique 4-tuple identities, strict versions, nonempty host-version constraints. Host-context keys must equal signed manifest paths. Catalog reserved commands feed `component_manifest::validate` with supplied typed `HostContext` (classifications, approved exceptions, live names). Each component joins an exact catalog release: envelope namespace = publisher; raw body SHA = `manifestDigest`; metadata **preimage** (not signature message) = `manifestPreimageSha256`; raw envelope SHA = `envelopeDigest`; `hostCore` identical. Unpresented catalog releases remain allowed; current minima/expiry stay deferred. Clippy nested-type visibility was aligned to `root_payload` (`metadata-before-catalog-visibility.rs`); no public API or admission-logic change.

40 signed cases, 4 initial / 4 repeated. Baseline 12/31/19295; repeat 12/62/19295; 12 physical captures.

**Executed:** inherited by the 286 **232/232** security run (`ordinary_metadata::tests::full_ordinary_catalog_and_component_joins_match_exact_reference` ok). 14/14 r1 mutants core-equal frozen `mutation-check-r1`. 30/30 probes include 285.

**Controls:** 9 wrong admissions (`omit-catalog-semantic-validation`, `omit-reserved-names`, `omit-publisher-namespace`, `omit-body-digest`, `omit-preimage`, `omit-envelope-digest`, `omit-compatibility`, `ignore-release-identity`, `ignore-live-names`). Other-first: `omit-context-set`; `ignore-host-classifications` (`left: false`); `lose-owned-components` (count 0); `omit-outer-failure-latch` counters `(12, 62, 19277)`.

**Verdict 285:** bounded match of documented catalog/component joins on the 284 Budget. Not current minima/expiry/population/custody. HostContext is a typed input, not a qualified registry producer.

---

## 286 — packaged policy structure, not adoption

`ordinary_policy::prepare` calls 285 on the same Budget, then reloads the closure and each `permissionPolicies` BlobRef (edges charged, captures cached). `packaged_recovery_policies::admit` (269, `pub(super)`) supplies v8 shape, path-prefix profile, duplicate grant/deny, and domain-separated policy preimage. Closure order is preserved; equal content under two paths is two owned entries. Empty packaged list is **not** private-policy absence. Never adopts consent, private global/project policy, or an effective grant digest.

40 signed cases, 14 initial / 14 repeated. Baseline 12/33/19373; repeat 12/66/19373; 12 physical captures. Inherited 269 335-shape / 41-boundary fixtures still run in the 232 suite.

**Executed:** `cargo clean -p opensip-security` then **232/232** with `Compiling opensip-security` (includes both 285 and 286 tests). Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **six** include files. 11/11 r1 mutants core-equal frozen `mutation-check-r1`. 30/30 probes.

**Controls:** 1 wrong admission (`omit-policy-semantics`). Other-first are counters/facts: skip-all/second policy `(12,32,19373)` / `(13,35,19713)`; omitted reference edges `(12,32,19373)`; `raw-sha-instead-of-preimage` digest mismatch; empty path / Null blob / Null body; latch `(12, 66, 19361)`.

**Verdict 286:** bounded match of packaged-policy structure reuse. Not private-policy custody, absence, adoption, or 280 effective merge.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 285/286 pins before extract | both match |
| Live `cargo test -p opensip-security` on 286 product | **232/232** after force rebuild |
| Clippy / fmt / rustfmt 6 includes | pass |
| 285 mutants | 14/14 frozen-equal; 9 wrong / 4 other |
| 286 mutants | 11/11 frozen-equal; 1 wrong / 9 other |
| Workspace | not rerun (284 529 predecessor) |
| Separate 231 run | **not executed** |

---

## Remaining (do not count closed)

Root-chain/current/history admission (see `ROOT-INTEGRATION.md`); retained population/non-key effects; current minima/time/accepted-role effects; artifact/repair/commands; native private-policy sources/absence/adoption/effective merge; physical capsule/fence/census/writers; runtime/source selection; M3–M6; T1 derived-target ordinary-import gate. These candidates are not shipped behavior or cumulative approval.

---

## Verdicts

- [x] **285:** archive/pins verified; catalog/component semantic joins on the 284 Budget; 9/4 mutant classification reproduced; inherited by the 232 run.
- [x] **286:** archive/pins verified; 269 admit reused without adoption; 232/232, Clippy, fmt, 6-file rustfmt; 1/9 mutant classification reproduced.
- [ ] **Neither** is current-root authority, complete ordinary import, private-policy adoption, or product installation.
