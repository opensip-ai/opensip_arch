# Independent review — native child-directory binding 332

**Standing:** bounded native-**platform** review of frozen `native-directory-binding-checkpoint-332`. `RetainedChildDirectory` owns a cloned parent fd, an exact OS component, and a 331 child handle, plus a **relative name recheck** and **descriptor-relative** metadata/ACL samples. It is **not** enduring exclusion, current-name authority, census, or a security Budget owner. Installed product remains `fa72e50`. 331 REVIEW was read and is **unchanged**.

Python 3.12.13 `-I -B` used only for pin/extract. Rust 1.95.0 `--offline --locked`. Review-local copies. Frozen fixture/mutant directories were not overwritten. platform-r1=66 (PermissionsExt import move only); **final is platform-r2 / 66 / mutation-r1**. No new `unsafe`.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **6816336 B, 535 members, SHA256 `e2bce071d368b86cb78240890044979f601716f0606c07c50dbfc940e6a08567`**, `allMembersRehashed: true`, **482** product pins. Extract rehashed **535/535**. Parent 331 live tar SHA `c11efa51…1375` (6798428 / 534 / 481). 331 REVIEW `eadf696e…a8aa` unchanged.

Product vs 331: **479** unchanged, **2** changed (`filesystem.rs` private `mod directory_binding` + `pub use RetainedChildDirectory`; `lib.rs` adds that type to the existing filesystem `pub use`), **1** added (`filesystem/directory_binding.rs` SHA256 `cf661d93…aa35` 10158 B). 331 `directory_open.rs` remains `9c8eedaf…fcb2`. 330 `directory_entries.rs` remains `4e599caf…7915`. No security-crate caller. libc `=0.2.189`.

---

## Retained object versus current name

`bind_child_directory` calls 331 `open_child_directory` (component bounds, no-follow `openat`), clones the **parent fd**, copies the **raw** name, then runs `recheck` **after** a private no-arg seam. The seam can only mutate native names; it cannot inject handles or booleans. Failed match is `InvalidData`, not `NotFound`.

`recheck` samples retained parent kind/nlink, reopens **exactly** `saved name` under that parent, and compares **retained child** vs **currently named child** (`is_dir`, nonzero nlink, `dev`/`ino`). Only native `NotFound` is `Ok(false)`. Symlink / regular / permission / other errors stay `Err` — they must not become clean mismatch or fabricated absence. Mutants `missing-becomes-matching` and `wrong-kind-becomes-mismatch` are caught.

`observe_directory` / `observe_directories` call existing `observe_descriptor(&File)` — **no filename reopen**, no FD export. After the child **path** is replaced with a mode-777 decoy, the sample still has the **old inode** and mode 700, while `recheck()` is **false**. Mutant `reopen-name-for-observation` is caught (would sample the decoy). Sequential `[parent, child]` is all-or-error, not an atomic permission snapshot.

Parent `File` clone is identity retention only. 330 `visit_entry_names` still `openat`s an independent description (330 ADDENDUM: that stream is `!Send`/`!Sync` via `NonNull`).

---

## Observation versus enduring custody

A true `recheck` is a **point-in-time relative-edge observation**. The test **demonstrates** it is not exclusion:

- rename child away → `false`; restore the **same** name → `true` again (**ABA**).
- move the parent **path** and plant a decoy `child` there → still `true`, because the check does **not** walk ancestors; the retained parent fd still names the original directory.

No lock, barrier, retry, repair, or durable authority. Constructor post-recheck refuses a replacement between open and check (`skip-constructor-recheck` is caught). After caller `parent`/`name` drop, the bound still owns parent/name/child.

Do **not** promote `recheck==true`, a `DescriptorObservation`, or a 330 `Summary` to current attachment, fence, or census. 330 whiteout/zero-inode/null-without-errno-as-EOF and qualification limits remain. Linux observer stays `UnsupportedPlatform` (cfg-excluded here). Caller still owes root/UID/groups/ACL policy and exclusion through consumption.

---

## Live cargo

**Executed** review-local product, `cargo clean -p opensip-platform` then:

| Kind | Result |
|---|---|
| `cargo test --offline --locked -p opensip-platform` | **66 passed / 0 failed / 0 ignored**; `Compiling opensip-platform`; 0.18s; 5 new `child_binding_*` tests ok |
| Workspace Clippy `--all-targets -D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **18** unchanged security includes + 330/331 helpers + `directory_binding.rs` | exit 0 |

---

## Mutants

Eight compiled controls plus baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 not overwritten). Live `report.json` SHA256 **`208aa5c8…6e22`**, **byte-identical** to frozen r1. All **9** compiled.

| Control | First failure (class) |
|---|---|
| `skip-constructor-recheck` | replacement between open and check becomes `Ok` |
| `ignore-child-inode` | new directory at same name treated as match |
| `missing-becomes-matching` | `NotFound` → `true` |
| `wrong-kind-becomes-mismatch` | regular/symlink → `false` not `Err` |
| `parent-sampled-as-child` | parent/child inodes collapse |
| `reopen-name-for-observation` | decoy path sampled instead of retained child |
| `replace-saved-name` | stored name `"other"` |
| `retain-child-as-parent` | parent field is child clone |
| baseline | 66 passed |

---

## Findings

The type splits **retained fds** from **current name** and treats `recheck`/`observe` as samples, including documented ABA and parent-move cases. That honesty is required, not a grant. 331 opener and 330 visitor are unchanged and still not census/custody.

**Actionable defects in this freeze:** none that make bind/recheck/observe self-contradictory with those distinctions on the macOS 66 tests and 8 controls.

**Must not be counted closed:** enduring custody/fence; current-name authority; 330 library-scope; shared Budget / 64-cap census; Linux ACL observer; writers; M2–M6.

---

## Remaining (do not count closed)

ABA-proof exclusion; ancestor/path qualification; coherent atomic parent+child permissions; selected FS/libc; directory/entry accounting before materialization; 329 successor composition; original T/TCB; M2–M6.

---

## Verdicts

- [x] **332 as frozen private child-edge binding:** archive verified; 331 preserved; 331 open + post-retention recheck; `NotFound` is false not absence; observations are descriptor-relative not current-name; ABA/parent-move are explicit non-custody; live 66/0 ignored; Clippy/fmt; 8 compiled controls + baseline frozen-r1-equal.
- [ ] **Not** enduring custody, current authority, census, or product installation.
