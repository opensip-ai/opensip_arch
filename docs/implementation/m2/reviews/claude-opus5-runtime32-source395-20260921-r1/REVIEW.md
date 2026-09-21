# Independent review — corrected source 395 and formal runtime32

Reviewer: Claude Opus 5 (1M context), `claude-opus-5[1m]`. Capacity available; substantive review
performed.

**Top verdict: ACCEPT-DESIGN-UNIT. `requiredFindings: []`.**

All three required findings from my source393 / formal31 review are **substantively closed against the
new bytes**, not carried over: each correction was read in the 393→395 diff, checked against the code
it describes, and — for RF-2 — re-measured by re-running my own adversarial probe against the 395 tree.
The delta is coherent and minimal: one file, five hunks, four of them documentation.

Root's choice not to install 393/31 is respected here. That unit keeps its own ACCEPT plus its three
required findings as historical record, and I verified its bytes are untouched.

---

## 1. Verification

### Declared pins — checked before extraction

| Artefact | Declared | Observed | Match |
|---|---|---|---|
| `…/trials/directory-barrier-checkpoint-395/subject.tar.xz` | 6 929 608 B, `70cc98839c68977d381c31298a305e7d645f65f85beb1286f0753c4f199c67cd` | identical | ✓ |
| `…/trials/directory-barrier-checkpoint-395/subject.json` | 114 086 B, `231adcb36f455b82a96e78cb50530103ee9401d6cd2b5e7fd6508c76753aae16` | identical | ✓ |
| `…/native-runtime-selection-v32-subject.json` | 2 521 B, `1de2e8016adb9bc87737b514f5e0c98dc01e6d9c31f6758a0441f8901852e7e5` | identical | ✓ |

### Formal unit — runtime32

| Check | Result |
|---|---|
| Declared members | 12 |
| Members verified against live bytes + sha256 | **12 / 12**, 0 failures |
| Member list sorted, unique | yes, yes |
| Successor `…/native-runtime-selection-v32/successor.json` | 3 078 B, `15089a49ac02f58eecd0f44a6a3f21cc67024903273177ff94f25ba707ffa293` |
| Candidates | 11, sorted, unique |
| `candidates + successor == subject` | yes |
| `passageOverrides` | `[]` |
| Candidate ∩ parents | empty |
| Any candidate already in the lock | none |
| Successor itself in the lock | no — correct, it is unselected |

**The candidate list references only 395 artefacts.** There is no 393/v31 leakage into the new
candidate set — I checked every entry. v31 is correctly **not** a parent: it was never selected, so it
cannot be one.

### Parents — current, pinned and genuinely selected

Selection is a lock entry **plus** a per-item assent unit, not a document's own `standing` header. All
three check out, and every assent unit's pin matches the lock:

| Parent | Live match | Lock site(s) | Assent unit | Status |
|---|---|---|---|---|
| `…/native-runtime-selection-v30/successor.json` | ✓ | `/contractSuccessors/51/record` | `native-runtime-selection-v30-unit.json` | `ACCEPTED-DESIGN-UNIT`, `rootSubstantiveAssent: true`, 0 required findings |
| `…/project-registry-owner-selection-v2/successor.json` | ✓ | `/contractSuccessors/48/record` | `project-registry-owner-selection-v2-unit.json` | `ACCEPTED-DESIGN-UNIT`, true, 0 |
| `…/repository-file-inventory.v58.json` | ✓ | `/inventorySuccessors/33/candidate` + 4 × `/inventoryPassageInheritance/*/parent` | `shared-store-codecs-inventory-v58-unit.json` | `ACCEPTED-UNIT`, true, 0 |

One mechanical note for anyone re-deriving this: `inventorySuccessors[33]` carries **both** a `record`
(the `shared-store-codecs-inventory-v58/successor.json` document) and a `candidate` (the inventory file
itself). The v32 parent pin matches the **candidate**, so a lookup that reads only `record` will
wrongly report this parent as unlocked. Live lock counts are as stated: 46 inputs, **34** inventory
successors, **52** contract successors.

### Source archive

**607 / 607** members match the manifest byte-for-byte and by sha256; 0 missing, 0 extra, 0 mismatched,
0 unsafe (no symlink, hard link, absolute path, `..` component or non-regular member). Composition:
**591 product + 15 evidence + 1 README**.

### Stage

`native-runtime-selection-v32/stage.py` is **byte-identical** to the v30 and v31 helpers
(`3a71d80af89babf7059a3ebe71c127a7dcc43a896f35b7cb6ce1de4cee03b1c4`), so staging behaviour has not
changed across three units. My own run into a review-local directory reproduced the author's record
exactly apart from that path:

```
{"archiveMembersVerified": 607, "nonLockSourceFilesVerified": 590, "mapped": 2,
 "unchangedNonLock": 588, "liveProductUnchanged": true, "runtimeAcceptance": false}
```

The historical source lock is excluded by **exact relative path** `design-lock.json`, not by basename,
so `tools/typescript-boundary/tests/fixtures/product/design-lock.json` remains verified. I ran no root
select script.

### Delta against live product — derived independently

From `git ls-files` in the live product repository, not from the author's manifest:

- 591 live tracked files; **589 identical**, **2 differing**, 0 live-only, 0 archive-only.
- `crates/platform/src/filesystem.rs` 73 907 → **81 671** B, sha256
  `87636b866277a93811b93e38337d753666ba339246774ec153e49bdf4a5f029a` ✓ as declared.
- `crates/platform/src/lib.rs` 3 792 → **3 817** B, sha256
  `8cbed576766b977fdb8e8804c2667cd5472e8f56077560f7fa4e48251b8e8467` ✓ as declared.

588 unchanged non-lock + the historical lock = 589. 0 new files, 0 package-graph changes.

---

## 2. What changed from 393, exactly

I still hold my own 393 staged tree, so I diffed the two staged products directly rather than reasoning
from the manifests. **591 files each; exactly one differs.**

`crates/platform/src/lib.rs` is **byte-identical to 393** — the export list was already correct.

`crates/platform/src/filesystem.rs`: **5 hunks, 20 added lines, 7 removed**
(`evidence/filesystem-393-to-395.diff`):

1. struct doc — receipts coexist, no exclusion / single-use / enduring namespace guarantee (O-2)
2. `is_for` doc — handle-object identity, not inode or path; a separate handle to the same inode does
   not match (O-1)
3. `confirm_directory_barrier` doc — two new paragraphs (RF-2 and RF-3)
4. test renamed `directory_barrier_receipt_binds_original_owner_and_reports_actual_primitive` →
   `directory_barrier_receipt_binds_original_handle_owner` (RF-1)
5. the vacuous macOS assertion removed (RF-1)

**`confirm_directory_with` is byte-identical between 393 and 395** — I extracted the 31-line function
body from both trees and hashed it, rather than inferring it from hunk positions. No executable line of
the primitive changed, and the existing `sync_directory` / `directory_barrier_with` / `fsync_directory`
fallback helpers are untouched. The claim "runtime behaviour unchanged" is verified structurally.

The unit test count is **115 in both 393 and 395** — the rename neither dropped a test nor collided
with an existing name.

---

## 3. Closure of the three required findings

Checked against the new bytes and the behaviour they describe, not accepted as carryover.

### RF-1 — vacuous macOS assertion and over-claiming test name — **CLOSED**

My finding gave two options: assert the value actually expected on the macOS lane, or remove the claim
from the name. Root took the second, and the correction account gives the reason: *"local actual
FullFlush is reviewer393 evidence, not made into a portability assertion."*

**That is the better branch, and I want to be explicit about it.** Asserting `FullFlush` would have
converted my one-host measurement into a portability claim the unit cannot support — exactly the kind
of over-reach the rest of this API carefully avoids. Removing the irrefutable
`matches!(…, Fsync | FullFlush)` and renaming to `directory_barrier_receipt_binds_original_handle_owner`
leaves a test whose name states precisely what its body asserts, and the new name additionally encodes
O-1. The conditional Linux `assert_eq!(receipt.barrier(), DirectoryBarrier::Fsync)` is retained without
any Linux execution claim; on this target it is not compiled.

The first-paragraph claim "The receipt exposes which completed" survives and is **still backed** — by
`directory_barrier_receipt_preserves_the_primitive_not_a_stronger_promise`, which asserts through the
seam that `barrier()` returns each injected variant. What is no longer claimed is *which* variant runs
on macOS, which is an environment fact rather than an API property. Correct scoping.

### RF-2 — inert nlink guard and the unnamed remedy — **CLOSED**

The new paragraph says what I asked for and slightly more:

> The link-count guard is only a descriptor check, not portable attachment evidence: macOS can keep a
> positive count after rmdir and successfully flush that unlinked directory. [`Self::is_reachable`] is a
> separate available reachability observation. Even that observation does not replace the caller's
> original parent/name checks or exclusion through consumption; this primitive deliberately performs no
> reachability/path lookup.

It states the platform asymmetry, states the *consequence* (a receipt is issued for an unlinked
directory), names `is_reachable`, and — as I required — does **not** wire reachability into the
primitive. I confirmed no reachability call was added: `confirm_directory_with` is byte-identical.

**Re-measured against the 395 bytes, not carried over.** I re-ran my public-API probe against a private
copy of the 395 tree (`evidence/reviewer-probe.stdout`). R4 reports, on these bytes:

```
nlink after rmdir = 2; is_reachable = Ok(false); confirm = Ok(FullFlush)
```

So each clause of the new sentence is true of the code it documents.

I also verified the one structural risk the fix introduces. `[`Self::is_reachable`]` is a rustdoc
intra-doc link, and a broken one fails silently under `cargo check`. I ran a reviewer-added pass —
`cargo doc --locked --offline -p opensip-platform --no-deps` with
`RUSTDOCFLAGS="-D rustdoc::broken_intra_doc_links"` — and it **passes**: the link resolves to
`RetainedDirectory::is_reachable`.

### RF-3 — undocumented error precedence — **CLOSED**

The new paragraph states which error wins, why, what is lost, and what the owner must do:

> Post-barrier descriptor observation has error precedence: if metadata() fails or its checks fail,
> that error replaces any barrier error. Otherwise the original barrier error is returned. … it does
> not preserve both causes. A post error therefore cannot prove whether the barrier succeeded or even
> what error it returned. All such errors require the owner to stop the act, without inferring
> unchanged durability or retry permission.

I checked it line by line against the unchanged code. `let after = self.0.metadata()?;` returns the
metadata error first; the `is_dir` / `nlink` / `dev` / `ino` guard returns `InvalidData "retained
directory changed"` second; `barrier: attempted?` propagates the barrier error only if both pass. The
documented order is exactly the code's order, and the doc correctly scopes itself to the **post**
observation — the pre-flush guard runs before any barrier error can exist.

---

## 4. Independent replay

Against my own staged tree, fresh review-local `CARGO_TARGET_DIR`, serial. No author binary, target
directory or script reused. Environment exactly as pinned — `HOME=/Users/sb` unchanged,
`PATH=/usr/bin:/bin`, the shared offline `CARGO_HOME`, pinned `RUSTC`/`RUSTDOC`, `LC_ALL=C LANG=C
TZ=UTC`, `CARGO_INCREMENTAL=0`, `RUST_TEST_THREADS=1`, pinned `TMPDIR`.

| Check | Result |
|---|---|
| `cargo test --locked --offline -p opensip-platform directory_barrier` | **5 passed, 0 failed, 110 filtered out** — all five names, including the renamed one |
| `cargo check --locked --offline --workspace --all-targets` | **clean, 15.80 s** (author 16.12 s) |
| `cargo test … --lib -- --list` | **115 tests** — unchanged from 393 |
| `cargo doc … --no-deps` with `-D rustdoc::broken_intra_doc_links` *(reviewer addition)* | **clean** |

**The existing fallback test was not rerun for 395, and the author does not claim it was.**
`checks.json` carries two entries, and the 393 `fallback-tests.stdout/stderr` were *removed* from the
archive rather than re-presented as fresh output. That is the honest handling. Its algorithm is
byte-identical — I confirmed `directory_fallback_accepts_only_named_unsupported_errors` and the helpers
it exercises are unchanged — and my own 393 replay (1 passed / 114 filtered) stands as the historical
record, cited here as historical rather than rerun.

### Reviewer probes re-run against the 395 bytes

Public API only, against a private copy whose `filesystem.rs` hashes identically to the staged one. All
six reproduce, and three of them are now the direct evidence for the new documentation:

| Probe | Result on 395 | Documents |
|---|---|---|
| R1 handle vs directory identity | second handle on the same inode rejected | new `is_for` doc (O-1) |
| R2 exclusion / one-shot | two live receipts, both `is_for` true, nothing consumed | new struct doc (O-2) |
| R3 name taken over before confirm | receipt covers the original inode while the name resolves elsewhere; `FullFlush` | unchanged claims |
| R4 unlinked directory | `nlink = 2`; `is_reachable = Ok(false)`; `confirm = Ok(FullFlush)` | **RF-2 paragraph** |
| R5 actual primitive on this lane | `FullFlush` | the measurement root deliberately did not turn into an assertion |
| R6 non-directory | refused at `from_retained_handle` | unchanged |

---

## 5. Preservation of the earlier unit

Verified rather than assumed:

- `native-runtime-selection-v31-subject.json` `4cb93ab3…` 2 521 B, `…v31/successor.json` `c889ecd5…`
  3 078 B, `…/directory-barrier-checkpoint-393/subject.tar.xz` `ea32681e…` 6 888 848 B and its
  `subject.json` `46a1f258…` 113 891 B are **all byte-unchanged** from the values in my 393 review.
- v31 is **still not in `design-lock.json`**, and v32 is not either.
- My 393 `REVIEW.md` and `review.json` are carried inside the 395 archive at
  `evidence/previous-review/`. I compared those copies against my own originals: **byte-identical**
  (`3d7123e8…` and `1a0befa6…`). The acceptance and its three required findings travel intact, not
  edited or summarised.

---

## 6. Observations — recorded, not required

Nothing here blocks acceptance; all of it is context worth keeping with the unit.

- **The measured macOS primitive now lives only in history.** With the assertion removed, the unit
  contains no record that `FullFlush` is what actually completes on the qualified lane. My probe R5 —
  in the 393 review and re-measured here — is the only record. Root's reasoning for not asserting it is
  right; I am noting it so the fact is not lost, not asking for a change.
- **RF-3's precedence is documentation-only by construction.** Of the three paths it describes, only
  the barrier-error path is asserted (by `directory_barrier_failure_is_once_and_never_a_receipt`). The
  other two are unreachable through the public API: for an owned descriptor `is_dir`, `dev` and `ino`
  cannot change, so in production only `nlink → 0` (a concurrent `rmdir`, on Linux) or a failing
  `metadata()` can trigger them. That is what I asked for — documentation — but the rule is prose.
- **O-3 stands declined, and its consequence persists.** No `Debug` on the receipt, so downstream code
  still cannot write `confirm_directory_barrier().unwrap_err()`. The correction account says so
  explicitly. A derive remains impossible (`RetainedDirectory` has no `Debug`); a manual impl would be
  needed. Not a correctness matter.
- **O-4 – O-8 are unchanged and were not in scope**: the confirm-time kind guard is still unreachable
  publicly; no test drives `confirm_directory_barrier` through the fsync fallback arm; fixtures run on
  the pinned `TMPDIR` volume, not a prospective installation-root volume; descendant modules of
  `filesystem` could still construct the receipt directly, and none does.
- **The v32 successor `standing` string is identical to v31's** ("PROPOSED retained directory barrier
  receipt; independent source/formal review required"). It carries no hint that this is the corrected
  candidate. The v32 README and the 395 trial README both do, so nothing is misstated — but a reader
  scanning successors alone cannot tell the two apart.
- **The v32 and 395 artefacts are not yet committed.** They are frozen on disk and byte-verified, but
  `git ls-files` reports all four as untracked at arch HEAD `613d3c7a8`. Root may commit during the
  review; the pins verified here, not the HEAD label, are the authority.

---

## 7. Limits

- **Level:** source reading, formal-pin verification, native test replay, a reviewer-added rustdoc link
  pass, and public-API probing.
- **Platform:** macOS arm64 development lane only.
- **Not qualified:** Linux execution (the retained `cfg(target_os = "linux")` assertion is not compiled
  here and no Linux claim is made or checked), power-loss and crash durability, filesystems other than
  the pinned APFS `TMPDIR` volume, custody, actor identity, native profiles, GC, release.
- **Not rerun:** the existing fallback test — carried historical evidence from author393 and my own 393
  replay, cited as historical.
- **Not re-reviewed on their merits:** runtime30, registry-v2, inventory58 — only currency, pins and
  selection status.
- **Unselected references remain unselected:** the 392 owner and its corrections, S9.3,
  `docs/v2/architecture/store-instance-lineage.v1.json`, `host-foundation-completion.v2.md`, and
  runtime31/source393 itself.
- **Replay caveat:** the two replayed checks are the author's own tests, so they establish
  reproducibility. The independent parts are the 393→395 staged-tree diff, the byte-level
  `confirm_directory_with` identity check, the `git ls-files` delta, the 115-test count, the rustdoc
  link pass, the byte comparison of the carried 393 report copies, and probes R1–R6 re-run on the 395
  bytes.

---

## 8. Context HEADs — sampled at the END

| Repository | HEAD | Subject | Committed |
|---|---|---|---|
| architecture | `613d3c7a85b8726e4d27cbea9805c29484dd70dd` | "Resolve initial creation review gaps and freeze directory barrier candidate" | 2026-09-21T14:53:01-07:00 |
| product | `cd5af4dbf524b81ac98876029798d569ccdc0052` | "Capture native project paths without relaxing internal name rules" | 2026-09-21T14:25:22-07:00 (clean) |

Product is still `cd5af4d` on runtime30/inventory58, so neither runtime31 nor runtime32 is integrated —
confirmed against the lock, not inferred. The architecture repository did not advance during this
review; the v32/395 artefacts are untracked at that HEAD, as §6 records.

---

## 9. Attestation

Read-only against live, frozen, history, product and lock. No architecture, product, frozen, history or
lock byte was edited; no pin was touched; no root select script was run. No commit, no push. All
writing went into this review directory; extraction and both build trees are review-local. The author's
binary and target directory were not reused.

This grants no root assent, no formal selection, no owner392 selection, no native initialization or
current authority, no S9.3 adoption, no M2 completion and no release qualification. Integration of
runtime32 requires this review, root's assent and prospective validation. The source393 / formal31
ACCEPT-DESIGN-UNIT with its three required findings, the owner390 NEEDS-CHANGES, the owner392
NEEDS-CHANGES and the 392 eligibility audit are all untouched and keep their own standing.

Reviewer: Claude Opus 5 (1M context).
