# Independent review — additive directory-publication inventory v59 (layout only)

Reviewer: Claude Opus 5 (1M context), `claude-opus-5[1m]`. Capacity available; substantive review
performed. **Layout only** — no source, owner397 or runtime assessment is made or implied.

**Top verdict: NEEDS-CHANGES**, one blocking finding.

The candidate itself is clean: exactly one additive row, every inherited row byte-equal, packages,
dependency graph and pending decisions untouched, parent correctly pinned to selected v58, and the new
row's role/package/naming consistent with its nine siblings. I could not fault a single byte of the
layout.

The blocking finding is about how the layout **carries forward**: the README requires the four
inherited description overrides to "project by stable file path", but the selected lock records them as
**array-index** JSON Pointers, and inserting a row at index 187 moves two of those four indices onto
different files. The candidate's `successor.json` — the machine-readable record consumed at
selection — asserts five things and says nothing about the overrides.

---

## 1. Pins and subject

| Artefact | Declared | Observed | Match |
|---|---|---|---|
| `…/directory-publication-inventory-v59-subject.json` | 647 B, `c262dffa679a5d7463ebcbf50c890a9d61369f440470f3d2b9d35a95ed87df05` | identical | ✓ |
| `…/repository-file-inventory.v59.json` | 280 949 B, `c2400990cf4f9ec0c6c4e4331e2194313dea272f17ad04c83866a23c9c1cb815` | identical | ✓ |

**3 / 3** subject members verified byte-for-byte and by sha256; sorted; unique:

- `docs/implementation/m2/directory-publication-inventory-v59/README.md` (1 042 B, `dac9782f…`)
- `docs/implementation/m2/directory-publication-inventory-v59/successor.json` (1 737 B, `6971d194…`)
- `docs/implementation/m2/repository-file-inventory.v59.json` (280 949 B, `c2400990…`)

All three are tracked, and committed blob id equals worktree blob id for each.

---

## 2. Additivity — verified row by row

Derived by comparing the two inventory documents directly, not from the successor's assertions.

| Check | Result |
|---|---|
| Rows | **705 → 706** |
| Added | **exactly one**: `crates/platform/src/filesystem/directory_publication.rs` |
| Removed | **0** |
| Existing rows changed in any field | **0** — every inherited row compares equal by value |
| Relative order of the 705 inherited rows | preserved |
| v59 file list sorted | yes |
| Top-level keys | identical (`schemaVersion`, `standing`, `files`, `packages`, `pendingDecisions`) |
| `packages` | **20 → 20**, byte-identical — no new package, no dependency-graph edge |
| `pendingDecisions` | **9 → 9**, byte-identical |
| `schemaVersion` | identical |
| `standing` | **changed, correctly** — see below |

The only non-`files` section that differs is `standing`, which *must* differ because it names the unit:

- v58: "PROPOSED additive shared store syntax layout from selected inventory57; no new crate/dependency
  edge, native authority or S9.3 selection"
- v59: "PROPOSED additive native directory publication layout; no creator/current authority or
  qualification"

That is a correct change, not a drift, and I record it explicitly so a mechanical "all sections
identical" check is not mistaken for a defect.

### Parent — selected v58 at its exact pin

The successor declares parent `docs/implementation/m2/repository-file-inventory.v58.json`, 280 320 B,
`f6c3c307332bf6bf04994b2ecbf3f2796465587fcd3e9d4c5e6042e13c5d5806`. That matches live bytes **and**
matches the product `design-lock.json` at five sites — `/inventorySuccessors/33/candidate` and
`/inventoryPassageInheritance/{0,1,2,3}/parent`. v58's assent unit
(`shared-store-codecs-inventory-v58-unit.json`) is `ACCEPTED-UNIT`, `rootSubstantiveAssent: true`, no
required findings, so the parent is genuinely selected and not merely present.

Neither v59 nor its successor appears anywhere in the lock — correct for an unselected candidate.

### Successor assertions — each independently re-derived

| Assertion | Verified |
|---|---|
| `parentArtifactBytesUnchanged: true` | ✓ v58 bytes untouched |
| `inheritedRowsEqualByValue: true` | ✓ 705/705 equal by value |
| `packageDependencyGraphUnchanged: true` | ✓ `packages` byte-identical, 20 entries |
| `pendingDecisionsInheritedUnchanged: true` | ✓ byte-identical, 9 entries |
| `addedFiles: ["crates/platform/src/filesystem/directory_publication.rs"]` | ✓ exactly that one |
| `carriedUnresolvedObligations` | ✓ 2 entries, both origin `repository-file-inventory.v54.json#/pendingDecisions`, both `UNRESOLVED` — the checkpoint‑211 inventory obligation and the account.rs/checkpoint‑218 observation obligation, carried with text and standing unchanged |

---

## 3. The new row — role, naming and placement

```json
{
  "path": "crates/platform/src/filesystem/directory_publication.rs",
  "package": "opensip-platform",
  "role": "adapter",
  "generated": false,
  "standing": "proposed",
  "description": "Own bounded private directory staging and exclusive same-parent publication through
   retained original descriptors. Preserve caller-held fence across rename, never adopt foreign staging,
   overwrite a winner, retry an uncertain publication or delete an abandoned/published tree. Return
   visibility observations only; complete P0, actor/profile/custody/ancestor/shared-budget admission and
   parent durability remain semantic-owner obligations."
}
```

Consistent on every axis I can check:

- **Package/role/generated/standing** match all nine existing `crates/platform/src/filesystem*` rows,
  which are uniformly `opensip-platform` / `adapter` / `generated: false` / `proposed`. `adapter` is an
  established value (30 rows use it).
- **Naming** fits the `directory_*` family — `directory_binding`, `directory_birth`,
  `directory_entries`, `directory_names`, `directory_open`, `directory_volume` — and
  `directory_publication` sorts into its place at index 187, between `directory_open.rs` and
  `directory_volume.rs`.
- **Description scope** matches the layout's claim and claims no more: staging and exclusive
  same-parent rename through retained descriptors, fence preserved across the rename, no adoption, no
  overwrite, no retry, no deletion, visibility observations only, and P0/actor/profile/custody/ancestor/
  shared-budget/parent-durability explicitly left to semantic owners. It asserts no authority,
  qualification or durability.
- The stated motivation — "This avoids further merging the new mechanism into the already large
  filesystem.rs" — is consistent with the existing module split, and I note without relying on it that
  `filesystem.rs` did just grow again under runtime32.

---

## 4. Blocking finding — the four description overrides do not project by path

The README states the requirement plainly: *"Project the four inherited description overrides by stable
file path without rewriting historical rows."* I checked whether the artefacts support that. They do
not.

The overrides live in the product `design-lock.json` as `inventoryPassageInheritance` entries, parented
to v58. Each entry carries exactly `{parent, selector: {jsonPointer}, before, after}` — **no path
field**. The pointers are positional, and for all four the parent's description at that index equals the
recorded `before`, which confirms they are resolved by index.

Inserting the new row at **index 187** shifts every later index by one:

| Entry | Selector | Target in v58 | Same index in v59 | Stable? |
|---|---|---|---|---|
| `[3]` | `/files/7/description` | `apps/cli/src/bootstrap.rs` | `apps/cli/src/bootstrap.rs` | ✓ |
| `[0]` | `/files/13/description` | `apps/report/package.json` | `apps/report/package.json` | ✓ |
| `[1]` | `/files/502/description` | `package.json` | **`docs/report.md`** | ✗ |
| `[2]` | `/files/569/description` | `schemas/sources/imported-v1.schema.json` | **`schemas/sources/import-source-context-v1.schema.json`** | ✗ |

Both intended targets survive intact — `package.json` moves to index **503** and
`imported-v1.schema.json` to index **570**, each with its description unchanged — so path projection is
achievable and the correct re-projected pointers are derivable. Nothing in the candidate is wrong; what
is missing is the record of the re-projection.

Why this blocks a layout review specifically: the `successor.json` is the machine-readable artefact a
selection consumes, and it asserts five properties, **none about the overrides**.
`inheritedRowsEqualByValue: true` is about row *values*, not about selector *positions*, so it does not
cover this. The requirement exists only in README prose. Depending on the selection machinery, the
outcome is either a silent retarget of two selected description overrides onto unrelated files, or a
selection failure — and a reviewer cannot tell which from the artefacts. Carrying the layout forward
correctly is the one thing this unit exists to do.

**Required.** Make the re-projection explicit in `successor.json` rather than in prose. Either:

- record a path alongside each selector so the override is keyed by `path` and index becomes advisory; or
- declare the re-projected pointers for this candidate — `/files/7` → `/files/7`, `/files/13` →
  `/files/13`, `/files/502` → **`/files/503`**, `/files/569` → **`/files/570`** — with the existing
  `before` text as the verification that each landed on its intended row.

Either form is a small addition, and both are checkable. I did not run any select script and express no
view on how root's selection tooling currently resolves these pointers; the point is that the artefacts
do not say.

---

## 5. What this review does not cover

- **No source assessment.** The private 396 source exists; this review is layout only and implies no
  source approval. I did not read, build or test it.
- **No owner397 dependency.** The owner397 review is separate, has its own verdict, and neither review
  depends on the other. This inventory selects no initialization law.
- **No native work.** No tests were run; none were needed.
- **Not re-reviewed:** v58 on its merits (only its currency, pin and selection status), runtime30/32,
  registry-v2.
- The row is a **planned** file entry. As the carried obligation says in its own words, no planned file
  entry proves implementation, custody or product readiness.

---

## 6. Context HEADs — as of 2026-09-21T15:42:23-07:00

Stated as of that sample only; the byte pins above, not these labels, are the authority.

| Repository | HEAD | Subject | Committed |
|---|---|---|---|
| architecture | `f657f2a40038c3c87d0133ed969147a054e85cc7` | "Select reviewed directory barrier runtime and freeze exclusive publication source" | 2026-09-21T15:40:11-07:00 |
| product | `ef3b1b51cba879151e58220e64975c5c3a7af441` | "Expose retained directory barrier observations with explicit limits" | 2026-09-21T15:36:08-07:00 |

Both trees clean at that instant. The product move is root's runtime32 integration, which I separately
confirmed is byte-identical to the candidate accepted in that review; it does not touch this inventory.

---

## 7. Attestation

Read-only against live, frozen, history, product and lock. No byte was edited, no pin was edited, no
select script was run, no commits, no pushes. All writing went into this review directory.

This grants no root assent, no formal selection, no source acceptance, no owner397 assent, no native
authority or qualification, no M2 completion and no release qualification. Actual selection requires
root's full read, assent and private/live validation.

Reviewer: Claude Opus 5 (1M context).
