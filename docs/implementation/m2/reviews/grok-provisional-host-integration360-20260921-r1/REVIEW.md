# Independent review — provisional host integration 360 (TEST-ONLY)

**Standing:** test-only **synthetic-account integration** of frozen `provisional-host-integration-checkpoint-360`. All **506** product files are byte-identical to frozen 359. A shadow build substitutes **only** the account-home string with a harness-owned temp path and adds one host example that calls the **public** `InstallationReadFence::try_acquire` and `ProvisionalInstallationRecords::read_existing`. This is **not** OS-home provenance, unmodified source selection, selected I, full `(S,G,K)`, `StoreGenerationBindingV1`, or current authority. Product remains `fa72e50`. Prior 359 REVIEW `ebe45147…9baf` (7218 B, no ADDENDUM), 358 `cdbad99c…c2d3`, store-binding ADDENDUM `84da081d…9a8b` were read and are **unchanged**. **361** (native session) is separately frozen/queued and is **not** this review.

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Isolated target; freeze workdir and frozen r1/r2 **not** overwritten. **This review reproduced:** 12 public cross-crate cases (baseline + restored-baseline) and **2 compiled runtime** fault controls (`skip-bundle-recheck`, `skip-marker-instance-binding`). Compile failures are not counted as caught controls. Security 375 / storage 96 / host 68 **not** claimed rerun here.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract. Parent 359 archive **549 / 6870648 B / `387a4881…6cf2`** / 506 product pins rehashed before 360 extract. Independent rehash of 360 tar, 545 members, and extract: 0 mismatches.

Frozen archive: **6891316 B, 545 members, SHA256 `145e511c0ba6325e8f166eb259ffcf480506b3e481396400f3a38a38d899bb28`**. 506 product pins.

Product vs 359: **506 unchanged, 0 changed, 0 added, 0 removed.** Freeze retains exact account+driver **shadow** deltas, patches, logs, and pins; not duplicate shadow trees or build outputs.

---

## What the fixture actually reaches

Shadow `account.rs` still calls `observe_with(credentials, …)` and `os_lookup` (`getpwuid_r`, UID, bounded buffer). Only the **Found home bytes** are replaced with the owned fixture path (0700 tempdir). No `HOME` env override, no public test factory, no dylib, no OS account creation, no writes to the real user I.

The driver (compile-time `@@FIXTURE_HOME@@`) builds `Library/Application Support/OpenSIP/preview-v1` **under that fixture**, then:

- `InstallationReadFence::try_acquire(&BTreeSet::new())` — public 355/357 fence
- second acquire is `None` (contention)
- `ProvisionalInstallationRecords::read_existing(&fence)` — public 359 join
- getters: `selection()` / `marker_raw()` / `contributing_filesystems()` (valid path: 8 samples)
- drop fence, reacquire succeeds

Failure cases assert the on-disk selection/marker bytes are **unchanged** (no missing⇒create/repair). After capture, replace-selection, replace-marker, and move-store-ancestor make **all three getters** err. `max-generation-claim` accepts `i64::MAX` **on purpose**: this bundle is provisional syntax + marker S, not admitted G/K.

---

## Live reproduction (this review)

Fresh scratch copy; absolute T/S/harness paths adapted; original driver/account templates preserved. Isolated `CARGO_TARGET_DIR`. Random fixture home ⇒ shadow source hashes differ from frozen r2 input-pins; **case outcomes** compared.

| Phase | Result |
|---|---|
| baseline | **12 PASS** |
| `skip-bundle-recheck` | compiled; panic `replace-selection` (marker getter not refused) |
| `skip-marker-instance-binding` | compiled; panic `mismatched-marker` (wrong S accepted) |
| restored-baseline | **12 PASS** |

Live `result.json` SHA256 **`f1daeb555a49e29e066ed2f3997ba55bc7c40fdca11595f9efef86cfc29cd704`**, **byte-identical** to frozen **r2** (outcome/exit/compiled/output lines; not path-dependent account hashes). Owned fixture home **removed** after the run. Extracted 506 product pins rehashed **after** run: unchanged. Frozen r1 12 PASS is history; r2 is the freeze image with controls.

---

## Findings

The fixture **does** reach the public 359 constructor and the 355 fence, including contention/drop/reacquire and getter postchecks on original File and earlier ancestor. It does **not** prove 351 OS-home source selection.

**Actionable defects in this freeze:** none that make “12 cases + two compiled runtime controls + restored 12” self-contradictory with this independent replay. A setup/compiler failure would not have been a caught control; these two controls compiled and panicked at the intended assertions.

**Must not be counted closed:** full five-member `StoreGenerationBindingV1`; namespace/registry/handle/lineage; core/profile; current authority; writers; M2–M6; OS-home provenance. 358 ADDENDUM still applies. **361 native session** is out of scope.

---

## Remaining (do not count closed)

Unmodified 351 account-home provenance. Independent security current `StoreBinding` as provisional comparison only. 323/229 closure, 350 profile FS-name law, active-slot, invocation groups, writers. 361 if later requested is a separate freeze.

---

## Verdicts

- [x] **360 as frozen TEST-ONLY synthetic-account integration:** 506 product pins identical to 359; public fence + 359 records actually invoked under owned fixture home; 12 cases + 2 compiled runtime controls independently reproduced; fixture cleaned; no real-user I writes. Not OS-home qualification or full binding.
- [ ] **Not** `StoreGenerationBindingV1`, selected-I/current authority, 361 native session, writers, or product installation.
