# Independent review — host installation/trust bundle 363

**Standing:** bounded **host composition** plus TEST-ONLY synthetic-home integration of frozen `host-installation-trust-checkpoint-363`. `ProvisionalInstallationTrust` privately owns 359 records and a 362 session under **one** opaque `InstallationReadFence`. Expected three-field S/G/K is derived from retained pair syntax; security compares independently parsed `C.store`. Host `failed` latch closes the bundle on **any** records or session error, even if the inner Budget would still be open. Copied census counts are structural only. This is **not** five-member `StoreGenerationBindingV1`, namespace/handle/registry, core/profile, current authority, or OS-home qualification. Product remains `fa72e50`. Prior 362 REVIEW `168809c4…dff1`, SOURCE-NOTE `772694b0…0cb8`, 361 `36b24bbd…4e81`, 358 ADDENDUM `84da081d…9a8b` were read and are **unchanged**.

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Isolated target; freeze workdir and frozen r1/r2 **not** overwritten. **This review reproduced:** host **68** (actually run), Clippy `-D warnings`, `cargo fmt --all --check`, rustfmt of **31** security includes, public cross-crate **16** cases (baseline + restored-baseline), and **4 compiled runtime** controls at the **intended** driver assertions. Security **388** **not rerun**. Frozen author: host-r1 **68**; integration-r2 16 + 4 controls + restored 16.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Parent 362 archive **594 / 7029028 B / `b4a45c75…fea8`** / 507 product pins rehashed before 363 extract. Independent rehash of 363 tar, 574 members, and extract: 0 mismatches.

Frozen archive: **6895004 B, 574 members, SHA256 `b07f1a6d879744b8f8a9772d4d167f79d8857ee2be016fcafe53a2db816fe3ad`**. 508 product pins.

Product vs 362: **506** unchanged, **1** changed, **1** added (host only):

| Path | SHA256 / bytes |
|---|---|
| `crates/host/src/lib.rs` | `cb544a3e…7054` / 538 |
| `crates/host/src/installation_trust.rs` **added** | `c25a7a37…599c` / 5273 |

`Cargo.lock` and `crates/host/Cargo.toml` identical to 362. Security/storage/lifecycle bytes unchanged. 126 fixtures unchanged. `lib.rs` only adds `#[cfg(target_os = "macos")] pub mod installation_trust`.

---

## Same fence / latch / comparison

The only constructor is `read_existing(fence)`. Fields `records` and `session` share `'fence`. Expected store is built from `records.selection()` (pair S/G/K). `NativeTrustReadSession::capture` then independently compares `C.store`. Records `recheck` runs **after** a failed current capture. `complete` / `recheck` / getters set `failed` on any error; later consumers return `Error::Closed` even after repair. `observe_successors` postchecks pair/marker; a callback that mutates selection cannot return successful counts.

No public session, File, root, or guard escape. No constructor for independently supplied captures. Three-field equality remains the 358 ADDENDUM’s provisional comparison.

---

## Integration (TEST-ONLY shadow)

Shadow substitutes **only** Found home bytes (credentials/`getpwuid_r` remain). r2 places the owned home under `/Users/sb/code/opensip-ai` (not shared macOS temp). Driver template `@@FIXTURE_HOME@@` is unsubstituted until the harness writes the example; it is **not** product source. Public `InstallationReadFence::try_acquire` and `ProvisionalInstallationTrust::read_existing` are actually invoked.

**Pilot r1 is FAILED evidence:** compiled; nine cases passed; then `unwrap` of `Records(Selection(Native(Error(Fence(Root(Descriptor(ChangedDuringRead)))))))` at replace-marker setup (`installation_trust_fixture.rs:56:189`). Exact mutator/ancestor was not established; concurrent native work shared temp ancestors. **Not an r1 pass and not a proved production defect.** r2 did not weaken production checks or add retries.

Live replay (fresh round, isolated target, r2 stable parent):

| Phase | Result |
|---|---|
| baseline | **16 PASS** |
| `skip-host-postcheck` | compiled; panic `callback-selection` **59:41** |
| `skip-host-record-consumption-checks` | compiled; panic `replace-selection` **64:38** |
| `skip-host-failure-latch` | compiled; panic `replace-current` **64:209** |
| `skip-current-store-comparison` | compiled; panic `current-generation` **54:17** |
| restored-baseline | **16 PASS** |

No `ChangedDuringRead` or `unwrap` in control stderr. Live `result.json` SHA256 **`fcc84c91dd8474f77a5abe47597579b8c1a16644393d328fc3e2799162e5b0fe`**, **byte-identical** to frozen **r2** (outcomes; fixture-home input pins differ). Owned home **removed**. Extracted 508 pins rehashed after run: unchanged.

---

## Live cargo (this review)

| Kind | Result |
|---|---|
| `cargo test -p opensip-host` | **68 passed** (actually run) |
| Workspace Clippy `-D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **31** includes | exit 0 |
| Security 388 | **not rerun** |

---

## Findings

363 is the host-owned **same-fence join** of 359 records + 362 session, with a host-level latch beyond inner Budget Closed, plus a public 16-case synthetic-home fixture that actually calls those constructors.

**Actionable defects in this freeze:** none that make one-fence construction, records postcheck after failed current, host Closed latch, callback-cannot-return-counts, or independent `C.store` comparison self-contradictory with the 16 cases, 4 intended control panics, and 68 host tests.

**Coverage, not a freeze contradiction:** no unit tests inside `installation_trust.rs`; composition coverage is the public example. Fixture is SYNTHETIC home, not 351 OS-home provenance. r1 ChangedDuringRead remains failed history.

**Must not be counted closed:** five-member `StoreGenerationBindingV1`; namespace/handle/registry; core/profile; current authority; writers; M2–M6; OS-home qualification. 362 SOURCE-NOTE still applies.

---

## Remaining (do not count closed)

Native five-member handle/registry. 323/229, 350 profile FS-name law, active-slot, writers. Inventory/runtime selection and materialization remain separate.

---

## Verdicts

- [x] **363 as frozen private host records/current/census composition plus TEST-ONLY synthetic-home integration:** archive verified against parent 362; two host-only deltas; one fence; host latch; live 68 + 16/4 intended panics/restored 16; Clippy/fmt31. r1 is retained FAILED evidence, not a pass. Matches the join request, not full binding or selected-I.
- [ ] **Not** `StoreGenerationBindingV1`, selected-I/current authority, OS-home qualification, writers, or product installation.
