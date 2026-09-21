# Independent review — native sampled child-directory policy 333

**Standing:** bounded native-**security** review of frozen `native-directory-policy-checkpoint-333`. Private `inspect` consumes a real 332 `RetainedChildDirectory`, does relative-name precheck → descriptor-relative parent+child observations → relative-name postcheck → existing `check_operational_chain_observations` on **both** samples with **no owner waiver**. Returned samples are **historical**, not enduring custody, current permissions, ancestor admission, census, or a write grant. Installed product remains `fa72e50`. 332 REVIEW was read and is **unchanged**.

Python 3.12.13 `-I -B` used only for pin/extract. Rust 1.95.0 `--offline --locked`. Review-local copies. Frozen fixture/mutant directories were not overwritten. security-r1=266/2 ignored then precheck-test seam strengthened; **final is security-r2 / 266 / mutation-r1**. No behavior correction. No new `unsafe`. No public API.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **6814108 B, 536 members, SHA256 `737730402840f28e03bcf0f437dc8cce987321e947cd150fbe4792a00879d7a5`**, `allMembersRehashed: true`, **483** product pins. Extract rehashed **536/536**. Parent 332 live tar SHA `e2bce071…8567` (6816336 / 535 / 482). 332 REVIEW `7c465c1f…ad56`, 331 `eadf696e…a8aa`, 330 REVIEW `75b9b10e…468e` and ADDENDUM `7b783d22…62ff` unchanged.

Product vs 332: **481** unchanged, **1** changed (`custody.rs` adds `mod directory_policy { include!(…); }`), **1** added (`custody/directory_policy.rs` SHA256 `c9b3d858…a963` 7443 B). Platform 330–332 helpers remain `4e599caf…7915` / `9c8eedaf…fcb2` / `cf661d93…aa35`. `inspect` is `pub(super)` only. libc `=0.2.189`.

---

## Helper (source)

Production `inspect` calls `inspect_with(..., || {})`. No caller-supplied observations or verdicts. UID/`authorized_groups` remain host-owned assertions.

1. `edge.recheck()` — 332 relative name. Native `Err` → `NameObservation`. `false` → `NameChanged` (not authorized absence).
2. `observe_directories()` — 332 sequential parent then child **descriptor** samples (no name reopen).
3. Test-only `after_observation` seam (native interposition). Production empty.
4. `recheck()` again.
5. `check_operational_chain_observations` iterates **every** sample with `check_descriptor_observation(..., Scope::Directory, …, false)` — **no owner waiver**. Empty chain refuses. Predicates carry component index.

The four native tests: both components’ OthersWrite/GroupWrite/ForeignOwner and explicit-group waiver; missing/replaced directory → `NameChanged` **before** the observation seam (panic if reached); regular/symlink → `NameObservation`; replacement after sample without repair → `NameChanged`; **same-inode chmod 700→777 after sample** returns old mode 700 while live observe is 777, then the next `inspect` is `OthersWrite` on child.

That last case is the honest limit: **both name checks can pass across permission mutation of the retained inode**. Samples are not current custody. 332 ABA and parent-move recheck boundaries are unchanged (this helper does not add ancestor checks or exclusion).

Linux ACL observation stays `UnsupportedPlatform`; 333 adds no fallback. Tests do not install every ACL form.

---

## Inherited 330–332

330 stream: whiteout/zero-inode skip, null-without-errno as EOF, `NonNull` `!Send`/`!Sync`. 331: `NotFound` is observation; wrong kinds are not absence. 332: `recheck` is a relative-edge sample, not fence; observe is retained-fd not current-name. 333 **reuses** those APIs and must not be read as closing them.

---

## Live cargo

**Executed** review-local product, `cargo clean -p opensip-security` then:

| Kind | Result |
|---|---|
| `cargo test --offline --locked -p opensip-security` | **266 passed / 0 failed / 2 ignored**; `Compiling opensip-security`; 12.58s; 4 new `directory_policy_*` tests ok |
| Workspace Clippy `--all-targets -D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **19** included modules (18 prior security includes + `directory_policy.rs`) | exit 0 |

---

## Mutants

Eight compiled controls plus baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 not overwritten). Live `report.json` SHA256 **`bfebd61c…b85a`**, **byte-identical** to frozen r1. All **9** compiled.

| Control | First failure |
|---|---|
| `skip-precheck` | already-changed name reaches observation-seam panic |
| `skip-postcheck` | replacement after sample returns `Ok` |
| `check-only-child` | child `OthersWrite` reported as component 0 / parent skipped |
| `check-only-parent` | child 777 next inspect does not refuse |
| `overwrite-observed-owner` | ForeignOwner waived by rewriting sample uid |
| `ignore-explicit-groups` | authorized gid no longer admits `0o720` |
| `skip-all-custody-policy` | 777 next inspect returns `Ok` |
| `name-error-as-mismatch` | symlink/regular `NameObservation` becomes `NameChanged` |
| baseline | 266 passed / 2 ignored |

---

## Findings

The helper is a sampled join of 332 name checks and existing operational descriptor policy. It correctly refuses using caller observations, collapsing native name errors into mismatch, checking only one component, or skipping policy. It also **documents** that a passing pair of name checks plus old samples is not a freeze of mode/ACL.

**Actionable defects in this freeze:** none that make `inspect` self-contradictory with those bounds on the macOS 266 tests and 8 controls.

**Must not be counted closed:** enduring custody/fence; current permission; ancestor admission; 330 library-scope; shared Budget / 64-cap census; 329 successor composition; original T/TCB; writers; M2–M6.

---

## Remaining (do not count closed)

Selected FS/libc qualification; ABA-proof exclusion; coherent atomic parent+child permissions; directory/entry accounting before materialization; Linux ACL observer; current-authority composition; M2–M6.

---

## Verdicts

- [x] **333 as frozen private sampled child-edge policy:** archive verified; 330–332 reports preserved; platform helpers unchanged; pre/post 332 recheck + both-component policy without owner waiver; historical samples not current grant; live 266/2 ignored; Clippy/fmt19; 8 compiled controls + baseline frozen-r1-equal.
- [ ] **Not** enduring custody, current authority, census, or product installation.
