# Independent review — complete formal initial-root owner / source / reference / generation unit 406

Reviewer: Claude Opus 5 (1M context), `claude-opus-5[1m]`. Capacity available; substantive review
performed. Read-only against live, frozen, history and locks; no commits, pushes or selects. Native
jobs run serially in the pinned lane.

**Top verdict: ACCEPT-DESIGN-UNIT. `requiredFindings: []`.**

Every structural, content and native claim I could check independently holds, and two of them are
stronger than stated. I also correct a factual error in my own 405 addendum that this unit's evidence
exposed — §7.

---

## 1. Subject and unit

`docs/implementation/m2/initial-root-binding-owner-selection-v1-subject.json`,
**18 865 B / `45e719a52313aca1427286dd90c09e2b841a5d6e0ee734727cb14dadf0757e32`** — matches the declared
pin, re-checked unchanged at the end of the review.

**82 / 82 members verified** byte-for-byte and by sha256; sorted; unique; all 82 under `U`; the
successor is included. Successor `…/successor.json`, 43 921 B / `3a713c5c…`, standing "PROPOSED complete
initial-root owner and diagnostic schema/reference/native-pin/generation integration; exact frozen
candidate requires actual substantive review and root assent."

---

## 2. Parents — 58/58 resolved, and the precedence trap avoided

My first resolver reported 46 of 58 parents unresolved. That was my error, not the unit's: I checked
only the effective approvals map and direct `design-lock.json` path entries, and omitted the third
channel — **candidate of a successor whose record is locked**, the one root corrected me on. With all
three channels indexed (87 locked successor records, 2 425 candidate paths):

| Channel | Parents resolved |
|---|---|
| successor candidate | 46 |
| `approvals.applicationManifest` | 6 |
| `design-lock.json` direct | 5 |
| `approvals.sourceManifest` | 1 |
| **unresolved** | **0** |

Every declared parent pin also matches live bytes.

**The manifest-precedence question is avoided rather than navigated.** The two approvals manifests
overlap on 182 paths and genuinely diverge on 23 (all documentation — `START-HERE.md`,
`COORDINATOR-DECISIONS.md` and similar). **Zero of the 58 parents lie in that diverging set.** So no
parent depends on which manifest wins, which is a stronger position than declaring the effective pin.

**The historical checker, vectors and projection checker are not declared as parents.** They appear
only as candidates at new paths under `reference/historical-source/`, byte-identical to their
originals, with `reference/reconciliation.json` recording original path, both manifest pins, the
effective accepted pin, the retained copy and `oldFullCheckerExecutedOrRequalified: false`. No frozen
original is edited and no stale whole model is frozen. The only `workflows_model.v1.py` **parent** is
the import-totality reference (`60dc11e2…`) — the latest selected reference successor.

---

## 3. Passage overrides — 12, none colliding

All 12 override parents resolve through a selection channel. **None collides with a selected
`inventoryPassageInheritance` key.** The four selected inheritance rows remain `/files/7`, `/files/13`,
`/files/503`, `/files/570` against v59 — the re-projected positions from the inventory59-r2 work — and
are untouched.

The one inventory override is a **direct** row, `/files/104/description` =
`crates/host/src/installation_lineage.rs`, whose live description equals the declared `before`. So the
result is **4 inherited + 1 direct = 5 effective descriptions with the inheritance row count still 4**,
exactly as claimed. The `after` text moves that row to the endpoint-only lineage join — the same file
whose per-hop marker walk I have flagged since 388.

The remaining 11 overrides are line/pointer selectors on `security-completion.v8.md` (×2),
`identity-and-evidence.md` (×2), `security-and-lifecycle.md` (×2), `workflows-and-surfaces.md`,
`effective-workflows-and-surfaces.md`, registry-v2 `owner.md` and `physical-placement.json`, and
`store-instance-lineage.v1.json` `/standing` — i.e. the creator / account-root / disclosure / storage
choice / durability / endpoint-lineage / doctor / inventory joins.

---

## 4. Owner body and origin

`owner.md` is **56 374 B / `35953d09bc34e7b3d5b68c971f2c0e0f36ee0f8122ae480dff8017f9c562bc55`** —
**byte-identical to my own retained 401 and 402 copies**. `owner-origin.json` pins the 402 archive
(`92d8b3f4…`) and manifest (`ebbef2b3…`), **my** 402 `findings.json` (`b656c754…`, matching my own
`hashes.txt` exactly) and root's assessment, and states plainly that this complete unit needs its own
acceptance and that historical headings and evidence limits in `owner.md` are retained. Prior 402 is
not treated as formal assent.

---

## 5. Schema, bindings and the native pin

### common.v4 — exact

| Check | Result |
|---|---|
| `$id` unchanged | ✓ `urn:opensip:product-v1:workflows:evaluator3:common:4` |
| First 317 enum positions | **exactly preserved, in order** |
| Appended | exactly `INSTALLATION.DURABILITY_NOT_CHECKED`, `INSTALLATION.NOT_INITIALIZED` |
| Candidate enum unique | ✓ 319 |
| Every other `$def` | **byte-identical** |
| Top-level keys | equal |

64 866 → 64 953 B, `6af81f35…` → `19da1845…`.

### Generated bindings — Common1/Common3 provably protected

`crates/contracts/src/generated/evidence.rs`: **+14 / −0 lines in three hunks**, all in the Common4
region; no added or removed line mentions Common1 or Common3. In the staged tree:

- `Common1DomainDetailCode` — **315**, neither new variant
- `Common3DomainDetailCode` — **315**, neither new variant
- `Common4DomainDetailCode` — **319**, both new variants

This is the 405 §D requirement, and 406 goes further than I asked: it is now enforced by a **compiled
regression**, `initialization_details_are_current_only_and_unknown_codes_still_refuse`, which asserts
the new codes deserialize as `Common4DomainDetailCode`, **fail** as `Common1DomainDetailCode` and
`Common3DomainDetailCode`, and that an unknown code still fails for Common4. A diff review can be
skipped; a test cannot.

### The native `SourcePin` — the consumer my 405 audit missed

`crates/identity/src/schema_registry.rs` changes **exactly two things**: `bytes: 64866 → 64953` and the
32-byte digest array for the common:4 pin. Nothing else in that file.

The retained `admission-pin-correction.md` is candid and correct: the first private run failed **22 of
23** tests with `SourceBytes` because `RegisteredSchemas` carries its own compiled pin, and updating
the JSON admission registry alone does not update that trust binding. **That refusal was right, and my
405 consumer map was incomplete** — I traced schema → maps → registry → closure → generated bindings
and never looked for a compiled-in `SourcePin`. Root found it by running the tests. The original
failing logs are retained rather than discarded.

### Staged delta — 12 mapped, 0 new

Derived independently from `git ls-files`: 592 tracked, **580 identical, 12 mapped, 0 new files**
(579 unchanged non-lock + the lock = 580). The 12 are exactly the declared set: `common-v4.schema.json`,
`source-map.json`, `admission-source-map.json`, `admission-registry.json`, `schemas/registry.json`,
`generator-closure.json`, `toolchain.json`, `build-receipt.json`, generated `evidence.rs` and
`report.ts`, `schema_registry.rs`, `schema_sources.rs`. **No new files, so no inventory row or package
change is needed** — consistent with the unchanged four inheritance rows.

`stage.py` verified every baseline and candidate pin before creating a private tree, left the inherited
lock unchanged (`selected: false`), and reported `liveProductModified: false`. My run reproduced the
author's record exactly: `mapped 12, unchangedNonLock 579, trackedFiles 592`.

---

## 6. Reference model and native replay

### The model delta is minimal and mechanically bounded

118 top-level statements in both base and candidate; **exactly two changed nodes, `terminate` and
`doctor`**; nothing added or removed. That is 116 other statements unchanged, matching the claim.

- **`terminate`** adds one `domainDetail` on the `reportProduced == False` branch
  (`DOCTOR.REPORT_NOT_PRODUCIBLE` plus a remedy). I stripped exactly that detail and compared ASTs:
  **identical to the base**. No other branch is touched. This closes the pre-existing golden/model
  divergence I identified in 405 §C — it is required by the already-selected
  `command-inventory.v3.json` golden, not new owner law.
- **`doctor`** replaces `len(defects)` with
  `sum(detail['code'] != 'INSTALLATION.DURABILITY_NOT_CHECKED' for detail in defects)`, with a comment
  stating the helper receives already-admitted bounded details and the assembler owns complete-root
  observation and the one notice. It **appends nothing**, so the existing two-defect no-note case is
  preserved, and only that one exact code is excluded — unknown codes still count.

### Native lane — all three replays pass

Pinned environment (`HOME=/Users/sb`, `PATH=/usr/bin:/bin`, shared offline `CARGO_HOME`, pinned
`RUSTC`/`RUSTDOC`, `LC_ALL=C LANG=C TZ=UTC`, `CARGO_INCREMENTAL=0`, `RUST_TEST_THREADS=1`, pinned
`TMPDIR`), fresh review-local `CARGO_TARGET_DIR`, my own staged tree, no author binary reused.

| Check | Command | Result |
|---|---|---|
| admission | `cargo test --locked --offline -p opensip-host --lib schema_sources::` | **24 passed, 0 failed, 45 filtered** |
| workspace | `cargo check --locked --offline --workspace --all-targets` | **clean, 13.38 s** |
| doctor reference | `check_doctor.py --architecture A --output FRESH` | **passed** |

The portable checker's own result corroborates my independent AST measurement:
`{"doctorCases": 8, "schemaMutationsRefused": ["boolean-count","detail-severity","doctor-field","unknown-code","oversized-array"], "nonDoctorOrTerminateTopLevelStatementsUnchanged": 116, "terminateChangedOnlyByExistingUnproducibleDetail": true, "currentCodes": 319, "checkedInputFiles": 48}`.

And it answers my 405 O-1: `check_doctor.py` loads `reference/input-pins.json` and **refuses any input
whose bytes/digest do not match** before executing. The helper now authenticates its inputs.

---

## 7. A correction to my own 405 addendum

This unit's `reconciliation.json` exposed an error in my addendum §3, and I state it plainly.

I reported that `approvals.applicationManifest` pinned **older** bytes for `check_workflows.v1.py`,
`workflow-cases.v1.json` and `workflows_model.v1.py`, and concluded that the effective accepted parent
was older than the live files. Checked directly against the `files` arrays now:

| Path | sourceManifest | applicationManifest | Agree |
|---|---|---|---|
| `check_workflows.v1.py` | 115 217 / `88edad11…` | 115 217 / `88edad11…` | **yes** |
| `workflow-cases.v1.json` | 245 182 / `f67d22f1…` | 245 182 / `f67d22f1…` | **yes** |
| `check-workflow-projection.v3.py` | 275 083 / `110c1b90…` | 275 083 / `110c1b90…` | **yes** |
| `workflows_model.v1.py` | 142 811 / `be37023f…` | 142 811 / `be37023f…` | **yes** |

The manifest was not amended — its only commit is `13e3d8701`, it is untouched in the last three arch
commits, and the digests I reported appear nowhere in its `files` rows. **The cause was my index.**
`application-subject.v46.json` has `files[]` rows carrying `{path, sha256, bytes, beforeSha256}` *and*
a separate `beforeImages[]` array of 76 pre-application rows. My recursive collector matched any nested
object with `path`+`sha256` and let the `beforeImages` rows overwrite the `files` rows for the same
paths. What I reported as "the application pin" was the **before-image** — which is exactly what
`reconciliation.json` correctly labels `beforeSha256`.

**What survives:** the mechanism is real — `verify_design.py:515-522` does iterate
`(sourceManifest, applicationManifest)` with last-write-wins, 23 paths genuinely diverge, and a future
successor naming one of those would have to resolve it. **What does not:** my claim that these
artefacts diverged, and therefore my argument that new copies were *necessary for that reason*. 406's
choice to carry them as provenance candidates rather than parents is correct on its own merits, and it
would have been correct either way.

---

## 8. Observations — none required

- **Generation 404 / rebuild 403 not replayed.** Root discloses the pipeline as prospective and
  unapproved until formal acceptance, with a fresh public-entrypoint drift check required after assent
  and no reproducible-build claim for the 7 202 304 B rebuilt executable. I did not run the generator,
  verify the 349-input closure beyond the pins already checked, or assess the 25 crate archives. The
  retained failure logs — missing ignored deps, the wrapper's wrong registry path, and the first freeze
  guard stopping before subject creation — are preserved rather than discarded, which is the right
  handling.
- **The five owner composition limitations and the prior owner-body limits persist**, unchanged and
  correctly restated. This unit adopts no 215, full S9.3 or transition-restore law.
- **TypeScript** (`report.ts` +166 B, 11 generated registry checks, strict compile) is recorded in the
  unit's evidence; I did not run a Node toolchain and make no independent claim about it.

---

## 9. Limits

- **Level:** pin and member verification, three-channel parent resolution, override collision analysis,
  byte and AST equivalence, staged-delta derivation, and native replay of the admission tests,
  workspace check and portable doctor reference.
- **Platform:** macOS arm64 development lane only.
- **Not qualified, and not claimed by this review:** native creator eligibility, shared budget, account,
  core, profile, custody, P0 construction, current authority, Linux, crash, power-loss, release.
- **Not replayed:** the 404 generation pipeline, the 403 rebuild, the TypeScript emit and runtime
  probe, and the full workflow checker (deliberately — it stays tied to its historical fixture graph).
- **Not re-reviewed on merits:** the owner body (byte-identical to the independently reviewed 402
  bytes), runtime32/34, inventory59, registry-v2, import-totality.
- **No selection or assent is inferred.** The unit is unselected; `selected: false` in the stage record.

---

## 10. Context HEADs — observed 2026-09-21T17:14:55-07:00

| Repository | HEAD | Subject |
|---|---|---|
| architecture | `89f4f3673f8444c91733f76e505ddfa4c4a5b894` | "Freeze initial installation owner and diagnostic contract integration for review" |
| product | `883f9634da5ffc422f07c8ac699a98ffdf7d4338` | "Add retained private directory staging and exclusive publication" (clean) |

The architecture repository advanced during this review, as anticipated; HEAD is qualified as an
observed timestamp only. The subject and successor digests above were re-checked unchanged at that
moment, and the byte pins — not the HEAD label — are the authority.

---

## 11. Attestation

Read-only against live, frozen, history, product and locks. No byte edited, no pin edited, no select
script run, no commits, no pushes. All writing went into this review directory; the private stage and
build tree are review-local. No author binary or target directory reused. The live product was
unmodified throughout and verified clean after.

This grants no root assent and no selection, and infers none. M2–M6 remain open. It does not qualify
native creator eligibility, shared budget, account, core, profile, custody, P0, current authority,
Linux, crash, power-loss or release. All existing review directories are untouched and keep their own
standing.

Reviewer: Claude Opus 5 (1M context).
