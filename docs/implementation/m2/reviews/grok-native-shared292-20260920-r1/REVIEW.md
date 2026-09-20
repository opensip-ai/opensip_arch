# Independent review — ordinary shared-metadata phase 292

**Standing:** bounded native-Rust review of frozen `native-ordinary-shared-checkpoint-292`. Private `prepare_shared` authenticates BUNDLE, catalog, and revocation-list signatures on the same 283 inventory and Budget as 284, then applies the finite retained∪incoming key union to **every shared group including the list**. Component **body** schema/semantics and DR-112 **authority**, and **all ROOT admission**, remain **pending**. This is not a T1 gate, current-context proof, signed-time proof, full catalog semantic admission, grant, or product installation. Installed product remains `fa72e50`. Keys are **TEST ONLY**. Archived 291 and `INERT-IDENTITY.md` were not edited.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/result directories were not overwritten. No workspace rerun (284's 529 is predecessor).

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **8088604 B, 866 members, SHA256 `554c8321c1ac96bb87ff8f0e03f36ae721b60420fe5c976a3f76cf1745509ea8`**. Standing: unselected private292 shared phase with pending component and ROOT admission. Extract rehashed **866/866**. Product-inputs **442/442**. Nested parent 291 pin `36147214…818c` equals reviewed 291; live 291 trial tar matches. Nested 265 `73c3b3f5…86df` live-matches. Product vs 291: **442** files, **440** unchanged. Changed only `trust_ordinary_quorums.rs` `5857d9d7…0b18`; added `shared292.ndjson`. `ordinary284.ndjson` byte-identical to 291. `prepare_shared` / `SharedEvidence` are `pub(super)`. Not in `lib.rs`.

---

## Shared vs Full

`prepare_inner` takes a private `MemberPass::{Full, Shared}` — no caller target boolean or `authenticated` flag. `prepare` still uses `Full` and still requires every component quorum. `prepare_shared` uses `Shared` and returns a distinct `SharedEvidence` with **no** conversion or accessor to full `Evidence`.

Both call 283 `ordinary_inventory::prepare` on the same Budget, then walk rootChain/catalog/list/manifests:

- **ROOT** pairs remain unresolved (including the supplied signing-root pair). SharedEvidence discloses those paths.
- **Catalog and list** still take actual signatures. List additionally keeps closed calendar, `rootVersion`, and `keyId` subject codec. The finite union filters **all** shared groups, and the list cannot exempt itself.
- **Manifests** in Shared: skip `verify_envelope` / threshold; record `pending_components`. The retained index already required presence, well-formed nonempty envelopes, kind/domain/literal-role route, and raw+canonical preimage identity. Component body schema/semantics and DR-112 authority are **not** done here. 285 catalog/component semantic joins are **not** claimed.
- Minimal 284 component bodies remain intentional pending state, not body admission.

Owned facts after input drop: retained inventory, revocation, union, shared groups (never Manifest), unresolved ROOT paths, pending component paths. Same capture cache, counters, and outer failure latch as 284.

50 cases: exact 46 signed 284 rows plus 4 missing/changed component body/envelope (no regenerated keys). **17** initial / **17** repeat positives. Baseline **12/31/16239**; repeat **12/62/16239**; **12** physical captures. Shared **succeeds** on bad-crypto / short well-formed signature / retained component key-loss (`*/manifest`), while the unchanged Full 284 suite still **rejects** those. Missing or mutated component body/envelope still **fails**. Shared catalog/list/BUNDLE faults still **fail**.

**Executed:** `cargo clean -p opensip-security` then **238/238** with `Compiling opensip-security` (includes inherited 284 Full test `(46,12,12)` and new Shared test). Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **nine** include files. 8/8 r1 compiled controls core-equal frozen `mutation-check-r1` (live baseline cargo skipped; unpatched source SHA matched frozen baseline `5857d9d7…0b18`). Frozen mutant dir not overwritten.

**Controls:** one first-failure **wrong shared-phase acceptance** — `omit-finite-union-filter` (`incoming-short/revocation` left true / right false). Seven other-first: `full-evidence-skips-component-authority` (Full happy-path groups 3 vs 4 before any wrong Full admission); `shared-phase-requires-component-authority` (pending list empty); `scope-away-shared-catalog` (catalog appears pending); `scope-away-shared-list`; `lose-pending-component-disclosure`; `lose-unresolved-root-disclosure`; `omit-shared-failure-latch`. Not operational exploits.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 292 pins before extract | match |
| Nested 291 / 265 live tars | match |
| Live `cargo test -p opensip-security` | **238/238** after force rebuild |
| Clippy / fmt / rustfmt 9 includes | pass |
| 292 r1 mutants | 8/8 frozen-equal; 1 wrong shared-phase / 7 other |
| Workspace | not rerun (284 529 predecessor) |

---

## Remaining (do not count closed)

Component body schema/semantics; component DR-112 authority for relied-on T1 members; 285 catalog/component semantic joins; ROOT chain admission (289) and current vs BEGIN population; 291 context planning join; signed time / minima / role-record effects; T1 completeness; durable custody/fence/census/writers; source selection; M3–M6. 290 `INERT-ROUTING` and 291 `INERT-IDENTITY` remain planning notes, not 292 approval. 292 is not shipped behavior or cumulative approval.

---

## Verdicts

- [x] **292:** archive/pins verified; shared BUNDLE/catalog/list + union including the list; components and ROOT explicitly pending; Full 284 path unchanged; 1/7 mutant classification reproduced; 238/238, Clippy, fmt, 9-file rustfmt.
- [ ] **Not** T1 ordinary-import gate, current-root/BEGIN proof, component body or authority admission, signed time, or product installation.
