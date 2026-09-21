# Independent review — native following-bucket observations 338

**Standing:** bounded native-**security** review of frozen `native-directory-provers-checkpoint-338`. Private `observe` inspects a caller-materialized BEFORE under an already-retained `by-predecessor` root: 127 shape and exact saved root component **before I/O**; root identity on the **same** `Budget`; every bucket lookup charged **before** 331 bind; 333 root policy **even on failed opens**; only actual `NotFound` is `Bucket.candidates = None` (`is_observed_missing`). Present buckets run 336 (335 capture + 329 bind of **all** canonical names). For **every** immediate link, reconstruct AFTER and inspect **all** following records on that Budget, including original **278** structural restore / DIRECT terminal. Supported indices are recorded **only after** each following bucket is fully admitted. No early exit on first support or fork. Output is **not** qualified census, clean/behind/fork, durability, or current authority. Installed product remains `fa72e50`. 336 and 337 REVIEW were read and are **unchanged**.

337’s narrower incorporated-TCB boundary is **accepted**: no hostile-kernel / raw-deleted-slot theorem. **Retained obligations:** declared FS/case profile, held cooperative fence, native constructors. Saved component is a **caller request**; case aliases are **not** disambiguated here (339 is named, not done).

Python 3.12.13 `-I -B` for pin/extract. Rust 1.95.0 `--offline --locked`. Frozen mutant dirs not overwritten. security-r1=293; r2=294 (isolated DIRECT negative + wrong-root); **final is security-r3 / 294 / mutation-r2**. mutation-r1 `fresh-following-budget` **compiled and survived** (self-derived limits) — **not a kill**. Independent fixed-fixture assertion added; production unchanged. No new `unsafe`. No public API.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **6833460 B, 587 members, SHA256 `1970c46c1deae217bdd2bb46e11096c17eeb8eb61361c5b4585224d6f89bfbdc`**, `allMembersRehashed: true`, **487** product pins. Extract 587/587. Parent 336 live tar SHA `750951cc…d1a0` (6825256 / 545 / 486). 336 REVIEW `2c317a30…afc5` and 337 REVIEW `3d58a154…c97e` unchanged.

Product vs 336: **485** unchanged, **1** changed (`trust.rs` include), **1** added (`trust/directory_provers.rs` SHA256 `d1561f2a…dead` 18616 B). 336 `directory_successors.rs` remains `3665640c…14cf`. 329 bind remains `c29e126f…1d2f`. libc `=0.2.189`.

Independent fixed-fixture count **(6, 17, 9511)**: 2×4478 B descriptors + shared 421 B operation + 134 name bytes (2×67) = 9511; 3 directories + 2 publications + 1 operation = 6 objects; root edge + 2 lookups + 2×(2+5) visit/capture edges = 17.

---

## Source (absence, following, 278)

`observe`: admit BEFORE; require `root.component() == "by-predecessor"` (counters stay `(0,0,0)` if not); 333 inspect; `Budget::directory(root)`. `bucket`: admit BEFORE; **charge lookup edge**; 333 inspect; 331 `bind_child_directory(sha)`; post-open 333 inspect; `NotFound` → `candidates: None`; other `Open` errors **refuse**. Present → 336 `inspect` (all canonical, 329 every candidate, 278 restore when restore-recovery).

Then for **each** immediate `link`, `bucket` with `link.clock().bound().capsule()` as next BEFORE. Push following **always**. Push `supported` only if following has ≥1 structural link. Restore test: removing **only** DIRECT terminal of original proof (keeping immediate operation) refuses and latches. Late bad following after two supported children refuses (no partial). Regular/symlink child is `Open`, not missing. Root rename during open is `Root`, not missing.

Materialized BEFORE, store-callback physical custody, selected ancestors, fence, and FS/case profile remain **external**. Dependent 329 reads may outlive 335 samples.

---

## Live cargo

**Executed** review-local product, `cargo clean -p opensip-security` then:

| Kind | Result |
|---|---|
| `cargo test --offline --locked -p opensip-security` | **294 passed / 0 failed / 2 ignored**; `Compiling opensip-security`; 13.26s; 7 new `directory_provers_*` tests ok |
| Workspace Clippy `--all-targets -D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **23** included modules | exit 0 |

---

## Mutants

**r1 (historical, not a kill):** `fresh-following-budget` compiled, **7 passed / 0 failed** on `directory_provers` (self-derived limit test). Other nine compiled controls caught. Evidence retained.

**r2 (final):** ten compiled controls + full-security baseline replayed into `grok-out/io/mutation-check-live` (frozen r1/r2 not overwritten). Live `report.json` SHA256 **`9ce9ba2a…305b`**, **byte-identical** to frozen r2. All **11** compiled.

| Control | First failure |
|---|---|
| `skip-root-component` | `"wrong"` root accepted |
| `skip-root-budget` | `(0,1,0)` vs `(1,2,0)` |
| `skip-lookup-budget` | `(1,1,0)` vs `(1,2,0)` |
| `errors-as-missing` | regular/symlink treated as missing |
| `skip-post-open-root` | root rename during open not `Root` |
| `only-first-following` | late-bad still `Ok` (1 vs 2 followings) |
| `wrong-following-before` | `(4,17,5033)` vs `(6,17,9511)` |
| `fresh-following-budget` | `(4,9,4966)` vs `(6,17,9511)` — **now caught** |
| `discard-following` | following len 0 vs 1 |
| `invert-prover-existence` | supported `[]` vs `[0]` |
| baseline | 294 passed / 2 ignored |

---

## Findings

Missing / empty / unproven are distinct. Regular/symlink/root mutation are not `NotFound`. All following buckets run; 278 DIRECT is required for restore-following; late failure is not a prefix. Independent (6,17,9511) is what made r2 catch a fresh Budget. 337 case/fence/profile work remains **outside** this helper.

**Actionable defects in this freeze:** none that make `observe`/`bucket` self-contradictory with those bounds on the macOS 294 tests and ten r2 controls.

**Must not be counted closed:** qualified census; case-alias disambiguation; fence/profile; 329 nested full-historical 279; current authority; writers; M2–M6.

---

## Remaining (do not count closed)

337 FS/case/fence/planted-name qualification; 339 exact-name observation without lifetime-root enumeration (named, not done); selected ancestors; Linux; original T/TCB; source-selection; M2–M6.

---

## Verdicts

- [x] **338 as frozen private following-bucket observations:** archive verified; 336/337 preserved; 337 TCB narrowing accepted with constructor/fence/case obligations retained; `NotFound` only for missing; all following + 278 DIRECT; no early exit; independent (6,17,9511); r1 fresh-budget survival **not** a kill; r2 ten controls frozen-equal; live 294/2 ignored; Clippy/fmt23.
- [ ] **Not** qualified census, clean/behind/fork, durability, current authority, or product installation.
