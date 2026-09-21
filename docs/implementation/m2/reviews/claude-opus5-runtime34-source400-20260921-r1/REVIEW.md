# Independent review — corrected native source 400 and formal runtime34

Reviewer: Claude Opus 5 (1M context), `claude-opus-5[1m]`. Capacity available; substantive review
performed.

**Top verdict: ACCEPT-DESIGN-UNIT. `requiredFindings: []`.**

All three required findings from my source396 / formal33 review are resolved. RF-1's remedy is not
merely documented — I ran the sequence the new documentation prescribes and it works. The claim that
nothing but documentation changed is verified mechanically, not accepted on report.

---

## 1. Verification

### Declared pins — checked before extraction

| Artefact | Declared | Match |
|---|---|---|
| `…/native-runtime-selection-v34-subject.json` | 2 493 B, `84cb1cfabd4c4447aae2b5a0766218ea714fe9708c01b2abad69bf9a968196af` | ✓ |
| `…/trials/directory-publication-400/subject.tar.xz` | 6 904 592 B, `76a78c344a01d3eb52b46af9cfa6b80e20f720ac1df430ee2dee59c5c46546c2` | ✓ |
| `…/trials/directory-publication-400/subject.json` | 115 903 B, `6e57e50aa632c239fa8055ebbfe9b2f1d1bc164aa75c9803d191defe994c1a36` | ✓ |
| `crates/platform/src/filesystem/directory_publication.rs` (staged) | 27 048 B, `1f10531ad3046d53863aaab2b263cff6a4487f7ea2feb05bda7a4f05cc66a916` | ✓ |

### Formal unit — runtime34

**12 / 12** members verified byte-for-byte and by sha256; sorted; unique. Successor
`…/native-runtime-selection-v34/successor.json`, 3 076 B, `373a5d9f…`. 11 candidates, sorted, unique;
`candidates + successor == subject`; `passageOverrides: []`; no candidate/parent collision; nothing
already locked; successor not locked.

The **same three parents** as runtime33, each live-matching, lock-pinned and carrying an assent unit
with `rootSubstantiveAssent: true` and zero required findings: runtime32 (`/contractSuccessors/52/record`),
registry-v2 (`/contractSuccessors/48/record`), inventory v59 (`/inventorySuccessors/34/candidate` plus
four passage-inheritance parents). Live lock reads 35 inventory / 53 contract successors, and product
is clean at `4b298da` — the stated baseline.

### Source archive

**617 / 617** members match the manifest byte-for-byte and by sha256: 0 missing, 0 extra, 0 mismatched,
0 unsafe. Composition: **592 product + 10 evidence + 1 README + 14 `historical396/` members** — the
prior unit's evidence tree carried forward intact rather than re-labelled as fresh.

### Lock provenance — verified in both directions again

The archive carries the runtime30-era lock (`63081729…`), not the live one. In my own stage:
`staged/product/design-lock.json` = **`48a8f67b…`**, byte-identical to live, while
`staged/product/tools/typescript-boundary/tests/fixtures/product/design-lock.json` = `ac65d09c…`, also
byte-identical to live. So the historical lock was excluded by **exact relative path**, the live lock
was separately composed, and the fixture lock remains verified.

### Stage and delta

`native-runtime-selection-v34/stage.py` is byte-identical to the v30–v33 helpers (`3a71d80a…`); five
units now share one staging behaviour. My run reproduced the author's record exactly apart from the
output path: `archiveMembersVerified 617, nonLockSourceFilesVerified 591, mapped 3, unchangedNonLock
588, liveProductUnchanged true, runtimeAcceptance false`.

Delta from `git ls-files`: 591 live tracked, 592 staged — **589 identical, 2 modified, 1 new**, 0
absent, 0 archive-only.

---

## 2. The decisive check: documentation only

The unit claims that relative to 396, only rustdoc comments changed. I verified it mechanically against
**my own retained 396 staged tree**, not against the manifest.

**Across the whole staged product, exactly one file differs between 396 and 400** —
`crates/platform/src/filesystem/directory_publication.rs`. `filesystem.rs` and `lib.rs` are
byte-identical to their 396 versions, so the two declaration/export edits are untouched.

Within the module, stripping every line whose trimmed form begins with `//` (covering `//`, `///` and
`//!`) and every blank line:

| | 396 | 400 |
|---|---|---|
| File | 25 152 B / 650 lines | 27 048 B / 675 lines |
| Comment lines | 49 | 74 (**+25**) |
| Non-comment, non-blank lines | **600** | **600** |
| sha256 of the non-comment remainder | `9c9bb601a63827a3c2b201b5b1fb01db…` | **identical** |

So the algorithm, the public API, the private fault seam and all twelve tests are byte-identical. The
claim holds, and the prior review's native evidence transfers legitimately — the tests are the same
bytes exercising the same code.

I still ran fresh checks, because a documentation-only change can break a doc build:

| Check | Result |
|---|---|
| `cargo test … -p opensip-platform directory_publication` | **12 passed, 0 failed, 115 filtered out** |
| `cargo test … --lib -- --list` | **127 tests** — unchanged from 396 |
| `cargo check … --workspace --all-targets` | **clean, 15.99 s** |
| `cargo doc --no-deps` with `-D rustdoc::broken_intra_doc_links` | **clean** |

The rustdoc pass matters here more than usual: the new text introduces intra-doc references
(`` `publication.parent_directory()` ``, `is_for`) and a broken link would pass `cargo check` silently.

---

## 3. Closure of the three required findings

### RF-1 — the receipt/handle seam — **CLOSED, and the remedy is verified to work**

New module-level documentation states the duplicate explicitly, names the identity model, and — the
part I did not ask for and should have — gives the **concrete sequence**:

> The stage owns a duplicate of the caller's parent descriptor in a distinct retained handle object. A
> directory barrier receipt uses handle-object identity: a receipt made on the caller's parent does not
> `is_for` this stage/publication parent. For a receipt associated with the publication, confirm the
> barrier on `publication.parent_directory()` after publication, while holding the original fence; use
> that same accessor for `is_for`. This does not replace the caller's separate original ancestry,
> custody and name checks.

with matching notes on `create_private_directory_stage` and on both `parent_directory()` accessors. No
new comparison API was added, as required.

**I ran the prescribed sequence.** Probe RF1, public API only, against a private copy:

```
receipt.is_for(publication.parent_directory()) = true
receipt.is_for(caller_parent)                  = false
caller barrier = FullFlush; publication barrier = FullFlush
```

So the documented remedy is implementable and produces a matching receipt, while remaining correctly
distinct from the caller's own handle. My P1 probe made the problem concrete; this one makes the fix
concrete.

### RF-2 — the missing error-precedence direction — **CLOSED**

> …error is retained when both rename and post-check fail. **When rename succeeds but the post-check
> fails, the post-check error is returned with indeterminate visibility; the successful rename is not
> reported as a success.**

That is exactly the direction that was absent, stated in the terms the code implements.

### RF-3 — conservative `Indeterminate` and the grammar/NAME_MAX distinction — **CLOSED**

> Indeterminate also covers syscall refusals that could in principle be known pre-effect, such as a name
> exceeding the filesystem's component limit. The 1023-byte syntactic limit is not a NAME_MAX oracle:
> the caller owes platform name-length admission before this call. No error permits an implicit retry.

It also closes my non-required **O-1** in the same breath:

> A failed stage is consumed and not returned for resumption; without a separate authorized cleanup
> owner, any surviving stage remains on disk.

---

## 4. What is unchanged, and still limits this unit

Everything in my source396 review's observations O-2 to O-6 stands unchanged, because the code is
unchanged: `0o700` remains subject to umask and inherited ACLs; the parent `nlink() == 0` arm keeps the
macOS caveat; `O_NONBLOCK` is incidental; the fault seam stays private with one production closure;
tests run on the pinned APFS `TMPDIR` volume and are macOS-only in effect. Zero production callers.

---

## 5. Limits

- **Level:** source reading, formal-pin verification, mechanical comment-stripped equivalence against my
  own retained 396 tree, fresh native checks, and public-API probing.
- **Platform:** macOS arm64 development lane only. No Linux, crash, power-loss or profile qualification
  is claimed or checked.
- **Historical evidence:** the author's twelve 396 tests and my own twelve-test 396 replay are carried
  as historical and are not claimed as rerun for 400 — though I did rerun the same twelve here, which
  is meaningful precisely because §2 establishes they are the same bytes.
- **Not re-reviewed:** runtime32/source395, inventory59, registry-v2 — only currency, pins, lock presence
  and assent status.
- **Unselected references remain unselected:** owner399, owner401 (reviewed separately), owner392, S9.3,
  215. This unit adopts none of them; accepting it grants no creation or current authority.

---

## 6. Context HEADs — as of 2026-09-21T16:27:41-07:00

| Repository | HEAD | Subject |
|---|---|---|
| architecture | `35bb623b76bb6ec259946c25092f20fa71aa9328` | "Clarify publication receipts and freeze initialization reconciliation corrections" |
| product | `4b298dae44e553e8317cf68350f5201cd3fc6771` | "Select directory publication module layout with explicit inherited descriptions" (clean) |

Product clean; runtime34 not integrated. Stated as of that sample only; the byte pins above are the
authority.

---

## 7. Attestation

Read-only against live, frozen, history, product and lock. No byte edited, no pin edited, no select
script run, no commits, no pushes. All writing went into this review directory; extraction and both
build trees are review-local. No author binary or target directory reused.

This grants no root assent, no formal selection, no native creation permission, no owner399/401
acceptance, no current authority, no P0 or power-loss qualification, no M2 completion and no release
qualification. Every earlier report is untouched and keeps its own standing.

Reviewer: Claude Opus 5 (1M context).
