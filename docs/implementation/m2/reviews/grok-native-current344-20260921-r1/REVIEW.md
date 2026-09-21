# Independent review — native current capture and P2-local joins 344

**Standing:** bounded native-**security** review of frozen `native-current-checkpoint-344`. `capture_head` reads the supplied installation's `trust/stores/S/state.v1` under a **borrowed** 341 fence. Budget keeps a **separate** current-path map keyed by the held store-directory `(dev, inode)`, not a fake Records alias. `SuppliedP2Current` owns `Head` + 343 `NativeStore` + decoded D + 328 local bindings, all borrowing the same fence. Expected `StoreBinding` is a **supplied constraint**, not selected I/S. This is **not** qualified census, current authority, writers, original T/action, or FS profile. Installed product remains `fa72e50`. 343 REVIEW `dfb45a53…dd28` and 342 REVIEW `759f16e8…b0ae` were read and are **unchanged**.

Python 3.12.13 `-I -B` for pin/extract. Rust 1.95.0 `--offline --locked`. Frozen mutant dirs not overwritten. **Final (this review reproduced):** security **324 / 2 ignored**, Clippy `-D warnings`, rustfmt of **26** included modules. Parent 343 workspace-r2 **640 / 0 / 2** is retained; **this review did not run a 344 whole workspace**. No new `unsafe` or dependency. Fixture bytes **unchanged** vs 343 (126 files). libc `=0.2.189`. `installation_fence.rs` SHA `e3547afc…302a` identical to 343.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Independent rehash of live tar, all 566 tar members, and the extract: 0 mismatches.

Frozen archive: **6846632 B, 566 members, SHA256 `7c383dcf2e0e957919cc84e78bce108b2bd6ef4d91a3e050012b1bc26877eb34`**. Extract 566/566. Parent 343 live tar SHA `b9e7e412…5e57` (6977700 / 602 / 490).

Product vs 343: **489** unchanged, **1** changed (`trust.rs` 620423/`997ab0f1…34b4` → 622923/`de7006f9…6c75`: current map + `capture_current` + private include), **1** added (`trust/native_current.rs` 22819 B, SHA256 `4fe0be4f6aabc828610483fc0c3ca9ab08a9f253602ecfc0cfd61f07415c10be`). 491 product pins.

`trust.rs` delta is 55 insertions / 3 deletions: `Budget.current`, counters/directory/`available` include `current.len()`, new `capture_current`, `mod native_current { include!(…) }`. No other product files.

---

## Head, current Budget, Files

`store_id` admits the expected StoreBinding **before** path construction: exact three fields, integer generation/schema, 32-byte id, then full 127 `StoreBinding`. Extra 1 MiB field and non-hex id refuse at `(0,0,0)` with no IO. Three prefixes `trust/stores/S`: each `edge` + bind + inspect + `directory` (inode identity **after** open — same 342 disclosure). Leaf is fixed `state.v1` via 335 `read_one` (`cap` before body, original File, single-link/mode/ACL/name). Full 127 `TrustCapsuleV1`; whole expected StoreBinding must equal `C.store`. Final `Head::recheck` covers original File, exact name `state.v1`, prefixes, and fence.

`capture_current` keys raw by the **already retained** parent store-directory `(dev, inode)`. Parent missing from `directories` is `Capture`. Shared object/byte limits count immutable raw + directories + current in both orders. First insert consumes one object and bytes once; every repeat still calls the read callback with `cap = old.len()`, then requires exact equal bytes (`Digest` if changed). Unique path counts once (`ptr_eq` on second Head raw). A Records `retain` of the same bytes is a **second** object and a **second** byte charge: after two heads `(4,14,1435)`, then Records `(5,14,2870)`. Unlink `state.v1` fails a third head **despite** cached current raw and the Records copy. Missing is an error, never genesis.

306 first capsule is 1435 bytes (`reference.bytes` and `canonical_bytes`). Exact limits `(4,7,1435)`; one-short object/edge/byte refuse and latch. Prior Objects `retain(b"x")` shares capacity → `(5,7,1436)`.

`Head<'f>` borrows the fence and owns prefix handles + File. Structural `Record`/`Arc` can move out; Files live on `Head`. Caller must keep Head/fence through consumption.

---

## P2 composition

`capture_p2` takes Head, then `load_at(Publications, C.publication, initial S)` on 343 `NativeStore`. Initial S is `C.store.storeInstanceId` **only** when `previousCapsule == Null` (343 provenance). First three 328 positives used here are rev-2 with non-null previous (`bbbb…`) → `by-predecessor` and `initial=None`. Then 328 `bind` on the **same** Budget (projection, retained-phase clock, `inputs::descriptor` **once**, optional outcome, 325 `bind_trace`). Final `recheck` is Head + NativeStore + Head. `NativeStore::recheck` errors collapse to `Error::Changed` at this boundary.

P0 Head observation is possible: 306 clock `phase: unevaluated` captures as Head, but `capture_p2` returns `Bindings(Phase)`. Local 328 bindings are **not** authority tokens.

First 328 positive counters, independently: current 7 edges + D 10 + operation 6 **once** + event 10 = **33**; eight unique directories + current/D/operation/event = **12** objects; bytes 4206+4957+402+789 = **10354** (event rawHex 789, operation rawHex 402; live test asserts the sum). r2 test arithmetic expected **39** (`operation6 twice`); actual production already 33. Inspected 328: same-store `descriptor()` loads OperationInput once and returns; 325 trace compares event refs and loads events, not a second operation. **Test-only** fix in r3; before-image `before-accounting-expectation-fix344.rs` still has `(12, 39, 10354)`. Production unchanged.

Exact/one-short composite limits `(12,33,10354)` / 11 / 32 / 10353. After success, unlinking current or descriptor makes `recheck` fail.

---

## Failure history (must not be hidden)

| Run | Result | Cause | Production? |
|---|---|---|---|
| native-current-r1 | **6 pass** | — | — |
| security-r1 / Clippy-r1 | **324 / 2 ignored**; Clippy | — | — |
| native-current-r2 | **5 pass / 1 fail** (`native_current_p2_…`) | test expected `(12, 39, 10354)`; live was `(12, 33, 10354)` | **test arithmetic only**; production unchanged |
| native-current-r3 / security-r2 / Clippy-r2 | 6 pass; **324 / 2 ignored**; Clippy | — | — |

Do not treat r2 as a production fail. Do not treat r1 six-pass as covering the later exact 33-edge assertion (that assertion did not exist yet).

---

## Live cargo (this review)

Review-local copy, `RUST_TEST_THREADS=1`, `cargo clean -p opensip-security` (forced `Compiling opensip-security`), `--offline --locked`:

| Kind | Result |
|---|---|
| `cargo test -p opensip-security` | **324 passed / 0 failed / 2 ignored**; 111.80s; all 6 `native_current_*` ok |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **26** included modules (24 `trust.rs` + 2 `custody.rs`) | exit 0 |
| Full workspace | **not run**; 343 workspace-r2 640/0/2 retained |

---

## Mutants

Ten compiled controls + six-test `native_current_` baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 not overwritten). Live `report.json` SHA256 **`6c737a9d1ebb4b271ee917041bdb596fd12ececf3381342e6a5ded9f53f40998`**, **byte-identical** to frozen r1. All **11** compiled. Baseline source pins match final product (`trust.rs` `de7006f9…6c75`, `native_current.rs` `4fe0be4f…10be`).

Actual first failures (live stdout):

| Control | First failure |
|---|---|
| `wrong-current-leaf` (`state.v2`) | exact path `(4,7,1435)` `Capture(Open(NotFound))` |
| `skip-full-store-shape` | invalid `g*32` StoreId proceeds to IO: `(2,5,0)` vs pre-IO `(0,0,0)` |
| `skip-full-store-identity` | wrong `storeGeneration` is not `Error::Store` |
| `skip-current-byte-cap` (`cap=CAP`) | one-short `(4,7,1434)` **succeeds** |
| `skip-current-raw-stability` | rewritten `state.v1` is not `Digest` |
| `cached-current-skips-file` | second **legitimate** `capture_head` is `Error::Reference` (`held` File never filled) — owned-File availability on repeat, **not** an unsafe missing-file accept |
| `omit-current-from-immutable-capacity` | P2 one-short objects `(11,33,10354)` succeeds; `retain` after 4-slot head is not `ObjectLimit` |
| `skip-head-final-recheck` | post-read file/parent/root/fence mutations accepted |
| `skip-composite-store-recheck` | unlink descriptor: `recheck().is_err()` fails (Head-only) |
| `fresh-descriptor-budget` | P2 `(8,23,5397)` vs `(12,33,10354)` — D native work hidden; remaining is current+op+event (4206+402+789, edges 7+6+10) |
| baseline | 6 `native_current_` tests, 1.21s |

---

## Findings

344 is the supplied-path `state.v1` reader plus the current-path Budget slot plus local P2 joins that 343 listed as root-next. Historical Records copies cannot satisfy current presence. Cache never skips the physical read unless mutated.

**Reproduction of r2:** frozen `native-current-r2.stdout` left `(12, 33, 10354)` right `(12, 39, 10354)` at the P2 composite test. Current source asserts 33. 328 same-store descriptor loads operation once.

**Reproduction of current vs Records:** same 1435-byte 306 image as current then as Records is two object slots and 2870 bytes. Unlink of `state.v1` still fails a later `capture_head`.

**Reproduction of cache-skip mutant:** returning cached raw without the read callback makes the **second** Head construction `Error::Reference` while the file still exists, because `held` stays `None`. That is File-availability, not a demo that missing current is accepted.

**Not defects vs stated standing:** evidence types have no fence lifetime; P2 maps NativeStore recheck to `Changed`; parent directory identity is charged after open; expected StoreBinding is a caller constraint; 338 census is not performed; P0 Head is observable and P2-refused.

**Actionable defects in this freeze:** none that make Head/`capture_current`/`SuppliedP2Current` self-contradictory with those bounds on the reproduced 324 tests and ten compiled controls.

**Must not be counted closed:** selected I/S/actor; native current **authority**; complete 338 successor census under fence; original T/action; writers; FS profile; Linux; M2–M6.

---

## Remaining (do not count closed)

Root-next (request): native current **plus complete 338 census under the fence** — **not** in 344. Fence-through-consumption remains a caller obligation. 337 profile; M2–M6.

---

## Verdicts

- [x] **344 as frozen private native current + local P2 joins:** archive verified; 343/342 preserved; separate current-path Budget; original File `state.v1`; P2 owns Head+NativeStore+328 bindings; live 324; Clippy/fmt26; 10 compiled controls + 6-test baseline frozen-r1-equal; r2 test-arithmetic fail **not** hidden and **not** a production defect.
- [ ] **Not** selected-I/current authority, census, original T, writers, or product installation.
