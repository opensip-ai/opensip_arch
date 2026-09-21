# Independent review — native original-core successor authentication 323

**Standing:** bounded native-Rust review of frozen `native-core-auth-checkpoint-323`. Private unselected composition: 322 byte capture on the **same** `Budget`, then unchanged 297 **time-free** `authenticate_root_chain` on **every later** embedded root, using a caller-supplied **original** revoked-key set. Final authenticated head must equal 322’s final **declared** binding. It does **not** produce original-core TCB, revocation completeness, accepted store head/role, current authority, S4, or publication. Installed product remains `fa72e50`. Keys are **TEST ONLY** Ed25519 (`signed-fixtures/keys/TEST-ONLY-{old,new}-0..2.pem`).

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local copies only. Frozen fixture/mutant directories were not overwritten.

322 is accepted **only** as byte resolution (`core_anchor.rs` SHA256 `d9fd86d4…1380`, byte-identical). 321 child-census time scoping, current-event shells, operation-ref stop, and physical qualification remain **open**. This review does not close them and does not inherit 322 as TCB.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **13517936 B, 2037 members, SHA256 `5ba848330c77e6e69932f0ad3603bd2c1d47cc313951e2c15bce34d1e7e5421f`**, `allMembersRehashed: true`, **471** product pins. Standing: private unselected 323 embedded successor authentication; original TCB/revocation completeness not supplied, no current authority. Extract rehashed **2037/2037**. Nested 322 pin `2a1f6ab7…cb51` (13499412 B / 2063 / 469 product) matches live 322 tar.

Product vs 322: **468** unchanged, **1** changed (`trust.rs` **only** private `include!("trust/core_authentication.rs")`, SHA256 `fc9190ab…a395`), **2** added (`trust/core_authentication.rs` SHA256 `bba53ae2…3c2c` 10442 B; `tests/fixtures/core-auth323.ndjson` SHA256 `3c8fb9a2…e211` 3839935 B). `lib.rs` has **no** public export. 297 kernel `security_lifecycle_model_v1.py` SHA256 **`df45c9c5444790b5f89b458efbee5cb068781d5fc1e82483c2678d2f10712299`**. Native `authenticate_root_chain` / `verify_root_chain` bodies were **not** edited.

Preserved: 322 REVIEW `62b48167…2a6c`; 321 REVIEW `537a71e7…54ea`; 318 REVIEW `7748038b…77be`. SCOPE-NOTES.md is author WIP that still says “322 review pending”; that sentence is stale relative to the completed 322 byte-resolution review and is not a 323 product defect.

---

## Challenge 1 — index-zero TCB vs successor signatures

229 C.1: the anchor is **always** `rootChain[0]`; a later embedded root is an ordinary dual-threshold **edge**, never an anchor. C.3: retained bytes are the declared index-0 root of that inventory; TR-CORE inventory signatures are circular; a self-written CoreAnchor is not writer integrity. C.4: why the anchor is trusted is **outside** the trust store (install/launch TCB). Index zero is the chain authentication **anchor**; recovery uses the **final** authenticated head, not a shorter prefix.

Native `authenticate`: `Core::capture` (322) then `first = &core.roots()[0]` parsed as root **body** policy (`admit`, no envelope crypto), then `roots().iter().skip(1)` as `WireRootLink`s into **`authenticate_root_chain`** (`time: None`). First envelope is 322-retained (subject/domain/preimage) and is **not** a successor link.

That is faithful to C.1/C.3/C.4 **if** no one reads the two invalid-first-self-sig positives as TCB:

| Label | First self-sig | Result |
|---|---|---|
| `anchor-self-signature-not-independent-tcb` | synthetic invalid | **accept** (two-root later links real) |
| `anchor-only-no-selfsig-tcb-premise-not-supplied` | synthetic invalid | **accept** (no later edge) |

Those cases prove first self-sig is **not** the authorization of the anchor. They are **not** evidence of a trusted initial core. Later links (`bad-successor`, `only-old-quorum`, `only-new-quorum`) refuse unless **both** actual thresholds hold. `later-invalid-no-prefix` refuses the whole chain (no prefix fallback). `wrong-anchor-last-root` (use last pair as first) first-fails `Chain(Gap)` on a good two-root case. `skip-all-successors` first-fails `Head` because 322’s final binding is the last declared root, not index zero.

**Hold:** index zero is external TCB **premise**, not a successor edge. This type authenticates edges **relative to** the supplied anchor.

---

## Challenge 2 — original revocation population

Caller `BTreeSet<[u8; 32]>` is passed into `ChainAuthenticationContext.revoked` and **cloned** onto `EmbeddedAuthentication`. It is a conditional input, not a producer of complete original history. Bootstrap/source BUNDLE/shared quorums and sealed original-context derivation remain owed.

`discard-original-revocations` (empty set at the kernel) **false-accepts** `old-revoked`. `discard-owned-revocations` still authenticates but drops owned set (`[]` vs expected key) — **ownership**, not completeness. Healthy single-key revocations and unrelated ids remain positives; two-key old/new revokes and isolated filters refuse. **Do not** treat a supplied set as complete revocation context.

---

## Challenge 3 — exact 297 time-free source projection

Primary extracts **function definitions only** from frozen `prepare_core322_reference.py`, wraps original 229 with isolated 319 `SEM.version`, and projects `verify_root_chain` by deleting **five** AST nodes from the pinned kernel (two timestamp parses, three relative-time guards: `EXPIRED_NO_CHAIN`, `FINAL_EXPIRED`, `FINAL_FUTURE`). Original model file **unmodified**. Recorded `phase-projection.json` `sourceSha256` equals `df45c9c5…2299`; live `A.removed` has length 5.

Native uses existing `authenticate_root_chain` (`time=None`), not `verify_root_chain`. No wall/eval argument, no skip-time flag. Intrinsic calendar/interval/order still refuse (`bad-calendar`, `empty-interval`, `gap`, `backdated`). `bad-crypto-even-when-expired` still refuses crypto.

Independent full current-time oracle at **`2026-09-20T00:00:00Z`** on the three time-free **positives**:

| Label | Time-free 323 | Full oracle |
|---|---|---|
| `expired-original-final-time-free` | accept | `ROOT.FINAL_EXPIRED` |
| `future-original-final-time-free` | accept | `ROOT.FINAL_FUTURE` |
| `expired-anchor-only-time-free` | accept | `ROOT.EXPIRED_NO_CHAIN` |

Pinned `phase-comparison.json` matches live. `invent-current-expiry-check` wrongly refuses `expired-original-final-time-free` (`Head`) — current wall must not be smuggled into this kernel. This cannot satisfy S4 or metadata acceptance.

---

## Challenge 4 — shared-budget failure handling

Capture and successor crypto share `budget.scope`. Baseline **9 / 17 / 24214**, repeat **9 / 34 / 24214** (edges recharged, no recapture). Signature failures set `failed` and the latch (`bad-successor` et al.). `discard-shared-budget` first-fails counters on the good two-root case. `suppress-crypto-failure-latch` first-fails `bad-successor` round-1 counters. Crypto failures are **not** allowed to leave the outer Budget open.

---

## Primary oracle and live cargo

Independent replay of frozen ndjson through extract-local `core_auth_reference323.py`: **38/38**, **0** mismatches, **13** first / **12** second positives (including the two invalid-first-self-sig cases). Actual surviving signers/thresholds/messages and owned raw bytes compared.

**Executed** on a review-local product copy, `cargo clean -p opensip-security` then:

| Kind | Result |
|---|---|
| `cargo test --offline --locked -p opensip-security` | **257 passed / 0 failed / 2 ignored**; `Compiling opensip-security`; tests 12.55s |
| Workspace Clippy `--all-targets -D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **15** includes | exit 0 |

**Seven compiled controls plus baseline** replayed into `grok-out/io/mutation-check-live-r1` (frozen r1 not overwritten). Live `report.json` SHA256 **`20fb570e…e03f`**, **byte-identical** to frozen r1. All **8** compiled; no compile-fail counted as a kill.

---

## Findings

Index-zero handling is faithful to 229 C.1/C.3/C.4 and the existing 297 time-free chain owner: first pair is 322-bound, not a successor; later links use both actual ROOT thresholds; no prefix; no invented current expiry. Original revocation **completeness** and original TCB remain **upstream premises**. No overall current authority.

**Actionable defects in this freeze:** none that make the private successor authenticator self-contradictory with pinned 322 capture + projected 297 time-free kernel on the 38 signed cases.

Not claimed: TCB, complete original revocation, accepted head/role, 321 constructors, S4, or product installation.

---

## Remaining (do not count closed)

Original external TCB producer; sealed complete original revocation context; full original time/floor replay; 321 census/event/physical constructors; custody/fence/capacity/final age; BUNDLE/shared quorums; M2–M6.

---

## Verdicts

- [x] **323 as frozen successor authentication relative to a supplied anchor:** archive verified; 322 bytes reused; 297 time-free projection exact; 38/38 primary; three time-free positives refuse full oracle; live 257/2 ignored; Clippy/fmt15; 7 compiled controls + baseline frozen-equal.
- [ ] **Not** TCB, revocation completeness, current authority, 321 standing, or product installation.
