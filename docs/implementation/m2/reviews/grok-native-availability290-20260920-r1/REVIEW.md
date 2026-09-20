# Independent review — delegated-key availability 290

**Standing:** bounded native-Rust review of frozen `native-role-availability-checkpoint-290`. Private `role_availability::derive` computes six-role delegated-key arithmetic over a supplied full `ValidatedRootPayload` and revoked-key set. It does **not** select current vs BEGIN-prospective root, authenticate population/history, produce OLD-subject or recovery-restriction facts, evaluate transitions, grant trust, or implement the T1 DR-103/DR-112 gate. Installed product remains `fa72e50`. Keys are **TEST ONLY**. Archived 289 was not edited. A separate planning note is in `INERT-ROUTING.md`; it is **not** this bounded verdict.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/key/result directories were not overwritten. No workspace rerun (284's 529 is predecessor).

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **8033560 B, 931 members, SHA256 `f3012512d8ccb857716e6cd6f3641bf6a5ac163c57f1402936b15bf7609f9b80`**. Standing: unselected private290 delegated-key availability, no current context authority. Extract rehashed **931/931**. Product-inputs **439/439**. Nested parent 289 pin `45764043…bf03` equals reviewed 289; live 289 trial tar matches. Nested 265 `73c3b3f5…86df` live-matches. Product vs 289: **439** files, **436** unchanged; `trust.rs` `9b7680a4…ed01` plus `trust_role_availability.rs` `bdec1efd…78df` and `availability290.ndjson`. Nested as `mod role_availability` with `pub(super)` API. Not in `lib.rs`.

---

## What `derive` does

Lexical roles BUNDLE, COMPONENT, CORE, INDEX, PROFILE, REPAIR. Missing role object (schema1 has no PROFILE) or `standing != "active"` (typed-absent REPAIR/PROFILE) → `Availability::Absent` with `below = None`. Never a fabricated threshold-zero active quorum. Active: distinct `role.keys` minus supplied revoked keyIds, compared to **that role's** `threshold`. No message-signer list, namespace selector, wall, or expiry input. Availability spans every delegated namespace of the role (fixture oracle unions primary `root_keys_for_role` across `namespaces`; independently equal to `role.keys` on all eight admitted roots). Root/catalog expiry remain CLOCK causes, not per-key removal. Evidence owns root digest/canonical, the exact revoked set, and the six role facts after input drop.

C.2: available-key observation uses the **chosen** admitted root (current outside ceremony; BEGIN-bound prospective in RECOVERY). This helper does not choose. C.3 uses those observations after OLD-subject precedence to remove below-threshold roles from T1; 290 is not that planner.

1212 cases, 8 admitted roots: 6480 active, 792 absent, 1694 below-threshold facts. Schema1/2, old valid date ranges, explicit extension absence, multiple namespaces, ROOT threshold 3 distinct from role threshold 2, COMPONENT 3-of-4 with a TEST-ONLY extra public key (shape-valid delegation, not a signature claim). Independent re-execution against 265 primary `admit_root_document` + `root_keys_for_role` + `role_threshold` matched all 1212 rows.

**Executed:** `cargo clean -p opensip-security` then **236/236** with `Compiling opensip-security`. Workspace Clippy `-D warnings`, cargo fmt, rustfmt of **nine** include files. 14/14 r2 compiled controls core-equal frozen `mutation-check-r2` (live baseline cargo skipped; unpatched source SHA matched frozen baseline `bdec1efd…78df`). Frozen r1/r2 dirs not overwritten.

**r1 coverage gap (inspected, not a production change):** frozen `mutation-check-r1` `root-threshold-for-role` compiled and **passed** (`expectedOutcome` false) on the 876-case / 6-root corpus where every role threshold equaled 2, same as `rootThreshold`. r2 expanded mixed-threshold fixtures catch it (`left: 3 right: 2` on `root2-root-threshold-distinct/TR-BUNDLE`). Initial fixtures, helper, and r1 logs retained. Production `derive` algorithm unchanged; whole-file SHA differs because tests/counts changed.

**Controls:** availability/fact differences, not current-root admission or operational exploits. Availability-bit: `ignore-key-revocations`, `invert-key-filter`, `equality-is-below`, `one-key-is-enough`, `absent-is-quorum-loss`, `all-roles-absent`, `typed-absence-fabricates-active`, `use-bundle-for-every-role`, `root-threshold-for-role`. Owned-field / invented expiry: `lose-declared-keys`, `lose-root-identity`, `lose-root-canonical`, `lose-revocation-context`, `dated-document-removes-keys`.

---

## Combined reproduction table

| Kind | Result |
|---|---|
| 290 pins before extract | match |
| Nested 289 / 265 live tars | match |
| Independent 265 primary re-execution | 1212/1212 |
| Live `cargo test -p opensip-security` | **236/236** after force rebuild |
| Clippy / fmt / rustfmt 9 includes | pass |
| 290 r2 mutants | 14/14 frozen-equal; all result differences |
| 290 r1 `root-threshold-for-role` | inspected undetected on 876-case corpus |
| Workspace | not rerun (284 529 predecessor) |

---

## Remaining (do not count closed)

Admitted current vs BEGIN-prospective root and revocation population; OLD-subject / recovery-restriction producers; 287 target planning join; T1 DR-103/DR-112 signature scope (see `INERT-ROUTING.md`); signed time / current minima / role-record effects; durable custody / fence / census / writers / source selection; M3–M6. 290 is not shipped behavior or cumulative approval.

---

## Verdicts

- [x] **290:** archive/pins verified; delegated-key availability matches C.2/C.3 arithmetic and 265 primary lookups; Absent never fabricates a zero quorum; r1 ROOT-threshold gap documented and r2-caught; 236/236, Clippy, fmt, 9-file rustfmt.
- [ ] **Not** current-root selection, history admission, T1 gate, clock/publication, or product installation.
