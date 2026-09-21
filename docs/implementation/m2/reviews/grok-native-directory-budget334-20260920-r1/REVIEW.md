# Independent review — native shared-budget directory name scan 334

**Standing:** bounded native-**security** review of frozen `native-directory-budget-checkpoint-334`. Private `scan` enumerates **OS-returned names** under a caller-already-captured `Arc<RetainedChildDirectory>`, charging the **same** operation `Budget` (objects/edges/bytes from reference222 PERSISTENCE lines 98/125) **before** classification or diagnostics. It is **not** descriptor admission, a qualified successor census, capacity reservation, clean absence, current authority, or product installation. Installed product remains `fa72e50`. 333 REVIEW was read and is **unchanged**.

Python 3.12.13 `-I -B` used only for pin/extract. Rust 1.95.0 `--offline --locked`. Review-local copies. Frozen fixture/mutant directories were not overwritten. security-r1=270/2 fail/2 ignored (test fixtures only: `A64` vs `a64` on case-insensitive FS; shadowed `Budget` still held the handle); **final is security-r2 / 273 / mutation-r1**. No production behavior correction. No new `unsafe`. No public API.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **6834748 B, 559 members, SHA256 `6ccd06fe3ee30942d80d2143d82c149b5044170abb29166fe2bb904d92fcd411`**, `allMembersRehashed: true`, **484** product pins. Extract rehashed **559/559**. Parent 333 live tar SHA `73773040…d7a5` (6814108 / 536 / 483). 333 REVIEW `2b8d901b…0da9` unchanged.

Product vs 333: **480** unchanged, **3** changed (`custody.rs` `pub(crate) mod directory_policy`; `directory_policy.rs` `pub(crate) fn inspect` — visibility only; `trust.rs` Budget + include), **1** added (`trust/directory_name_scan.rs` SHA256 `c1693fcb…00f3` 13835 B). Platform 330–332 helpers unchanged. libc `=0.2.189`.

PERSISTENCE 98/125: 65536 objects / 131072 edges / 268435456 bytes; charge object bytes and every edge **before** retain/schedule; **64** canonical names per directory; **all** entries including noncanonical consume enumeration work; noncanonical reported, not read/adopted.

---

## Scan and Budget (source)

`scan` (inside `budget.scope`): 333 `inspect` → `Budget::directory(Arc)` → 330 `visit_entry_names(131072, 268435456)` with `entry` as visitor → 333 `inspect` again → sort canonical names.

`directory`: one **edge** per visit; `(device, inode)` object slot shared with `raw`; stores a strong `Arc<RetainedChildDirectory>` so the inode cannot be reused while memoized. **Not** a content digest. Caller already captured the edge; this is **not** retrospective pre-allocation of that open/ACL. Repeated visits of the same inode still run policy and still charge **entry** work (`(1,8,266)` then `(1,16,532)`).

`entry`: **edge + exact name bytes** before `canonical` / callback / push. Dots charged, not reported. Other non-canonical names: borrowed callback **after** charge; no open/read/adopt/mutate. Callback error → `Diagnostic` and latch. Lowercase 64-hex only → `[u8;32]`; duplicate digest refuses; **65th candidate refuses before push** (after that name is charged). Uppercase hex is foreign (`B64` in tests). Canonical **directories and dangling symlinks** still appear in `canonical()` — next content layer must refuse; this layer does not open them. Empty `canonical` is **not** authorized absence.

`available`/`retain` object limits use `raw.len() + directories.len()` in **both** orders. Failures set `failed`; later `edge`/`retain` are `Closed`.

---

## Inherited 330–333

330: OS stream ≠ all raw slots; whiteout/zero-inode skip; null-without-errno as EOF; `NonNull` `!Send`/`!Sync`. 332: relative recheck is not fence; ABA/parent-move remain. 333: samples are historical; same-inode chmod can pass both name checks. 334 post-scan `inspect` catches chmod/rename; it does **not** freeze permissions during the visit.

---

## Live cargo

**Executed** review-local product, `cargo clean -p opensip-security` then:

| Kind | Result |
|---|---|
| `cargo test --offline --locked -p opensip-security` | **273 passed / 0 failed / 2 ignored**; `Compiling opensip-security`; 13.01s; 7 new `directory_scan_*` tests ok |
| Workspace Clippy `--all-targets -D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **20** included modules | exit 0 |

---

## Mutants

Fifteen compiled controls plus baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 not overwritten). Live `report.json` SHA256 **`783c8124…8e6b`**, **byte-identical** to frozen r1. All **16** compiled.

| Control | First failure (class) |
|---|---|
| `skip-entry-charge` | counters `(1,1,0)` vs `(1,8,266)` |
| `charge-after-materialization` | panic-callback reached (`seen` 1 vs 0) |
| `allow-sixty-fifth` | 65 canonical names accepted |
| `skip-duplicate-refusal` | second `a64` not `Duplicate` |
| `drop-foreign-diagnostics` | foreign list empty |
| `ignore-diagnostic-error` | callback `Err` not `Diagnostic` |
| `skip-pre-policy` | visitor panic on 0o702 child |
| `skip-post-policy` | chmod/rename after names still `Ok` |
| `unsorted-results` | reverse sort |
| `raw-objects-ignore-directory-slots` | extra raw retain `Ok` |
| `directory-objects-ignore-raw-slots` | second directory not `ObjectLimit` |
| `skip-entry-name-bytes` | bytes 0 vs 128 |
| `skip-directory-edge` | first-name bytes leak into `(1,1,1)` vs `(1,1,0)` |
| `weak-directory-handle-retention` | `Arc` dies while Budget still holds key |
| `no-shared-failure-latch` | later `edge` `Ok` after policy fail |
| baseline | 273 passed / 2 ignored |

---

## Findings

The scanner matches PERSISTENCE 125’s “charge every examined name before materialization / 64 canonical / foreign untouched” **for names the 330 stream returns**. It does not admit content, reserve a 65th publication, or make empty names a clean absence. Directory `Arc` retention is identity pinning inside this Budget, not current attachment.

**Actionable defects in this freeze:** none that make `scan`/`Budget::directory`/`entry` self-contradictory with those bounds on the macOS 273 tests and 15 controls.

**Must not be counted closed:** qualified physical census; 330 libc holes; 332 ABA/exclusion; 333 historical samples; following-bucket/329 join; original T/TCB; writers; M2–M6.

---

## Remaining (do not count closed)

Selected FS/libc/custody/fence; full canonical **content** admission; following-bucket proof; root/parent capture accounting; current producers; M2–M6.

---

## Verdicts

- [x] **334 as frozen private shared-budget name scan:** archive verified; 333 preserved; 333 pre/post policy; every OS name charged before classify; 64-cap before push; directory+raw share object slots with strong Arc; empty names not absence; live 273/2 ignored; Clippy/fmt20; 15 compiled controls + baseline frozen-r1-equal.
- [ ] **Not** qualified successor census, content admission, capacity reservation, current authority, or product installation.
