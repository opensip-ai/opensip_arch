# Record hygiene: current-applicability notes for stale design text

- **Date:** 2026-10-02
- **Repository:** `opensip_arch`, base `HEAD fb8472da8`
- **Author:** Claude subagent, drafting for the implementation lead (Claude Opus 5.5)
- **Owner approval:** the owner approved this record-only batch (relayed by the lead)
- **Standing:** proposal. It changes no decision, contract, gate, threshold or requirement.

## 1. Purpose and form

Some stale sentences in the design record contradict current authority (D-369, D-371, D-372). This batch
adds a dated **current-applicability note** next to each stale sentence. Each note names the current
authority and cites it. No historical, frozen or contract text is rewritten.

The form follows the repository's existing pattern. That pattern is the chapter banners
`> **Current applicability — D-372:** …` (chapters 01–05, 07 and 09) and the chapter 10 banner
`> **Current direction — binding scope selection under D-371:** …`. A note is a blockquote paragraph
that starts `> **Current applicability (2026-10-02) — <authority>:**`. In a table, the note goes directly
after the table and names its row, because a blockquote cannot sit inside a Markdown table row.

No file under `docs/v2/contracts/` and no text in `docs/coop/COORDINATOR-DECISIONS.md` is touched.
Chapter 11 receives no notes. It has no applicability notes of its own, so its stale points are only
listed (§5).

## 2. Blocking finding: most target files are live-pinned

Before applying anything, I checked which current verifiers bind the exact bytes of each target file:

| File | D-372 application manifest (`application-subject.v46.json`, 197 files) | Product `design-lock.json` (checked by product `tools/verify_design.py`) | Other current pins |
|---|---|---|---|
| `08-decision-and-readiness-register.md` | pinned | **pinned** (`de21a7e0…`, 130283 bytes) | — |
| `10-mvp-and-future-scope.md` | pinned | — | `design-corrections/{foundation,native,security}/source-pins*.json` (native checker `check_native_evidence.v2.py` reports `PIN-MISMATCH` on drift) |
| `02-distribution-and-components.md` | pinned | — | — |
| `05-v1-to-v2-relationship.md` | pinned | — | — |
| `12-architecture-completion-goal.md`, root `README.md` | pinned | — | — |
| `prototype-evidence-reference.md` | not pinned | — | historical review subjects and `historical-preservation-report.v*.json` only |
| `11-three-reviewer-direction-synthesis.md` | not pinned | — | historical review subjects only |

Two consequences follow.

1. **Register (08).** I tested this on a copy of the product verifier. Appending one line to the register
   makes the verifier fail with `design digest mismatch: docs/v2/architecture/08-decision-and-readiness-register.md`.
   Appending a line to 02, 05, 10 or the prototype reference did not make it fail. Every file was restored
   byte-for-byte afterwards. So a register edit needs a product `design-lock.json` successor, which is
   product-repository work and outside this batch.
2. **D-372-applied files (02, 05, 08, 10, 12, README).** D-372 is "ADOPTED at design level only when the
   D-372 activation verifies". The activation's `bindingRule` says: "Verify both pinned artifacts and each
   current applied file against the application manifest." All 197 files match today. Editing any of them in
   place would make that verification fail, which would change D-372's verifiable standing. This batch must
   not change any decision.

**Recommendation (lead decision required):** record a small reviewed successor for these annotations.
D-372 itself says "New current-head/navigation/register annotations are prospectively authorized by this
act", but it binds them through an application manifest. The successor should:

- carry an application-manifest successor or activation addendum listing the new after-image hashes for the
  six files;
- come with a product design-lock successor for the register in the next product unit;
- then apply `staged-notes.patch` (`git apply docs/implementation/m3/record-hygiene/staged-notes.patch`).
  The patch applies cleanly to `fb8472da8`.

Until then, only the one unpinned file is edited.

## 3. Items

### Item 1 — "No digest-pinned quality corpus exists"

Current authority: the register's DR-118 row (`08…:307`, **SATISFIED 2026-09-04 (D-369)**, "corpus and product thresholds accepted") and `docs/coop/completion/quality-corpus-manifest.v1.json` (SHA-256 `2a4c2fe01d07426b5c9574cff913043097283b8995013cd18f4a7ff852ba2039`; 1,010 `.ts` + 9 `.json` files; `kind: language-native-design-corpus`, `productExecution: false`). That corpus is the TypeScript preview only. The executable JS/Rust product corpus remains OPEN under DR-G13 `harness.DR-G13.product-v1`. Admission-and-qualification §3 (`docs/v2/contracts/product-v1/admission-and-qualification.md:244-246`) says executable native fixtures must be admitted at implementation qualification before a cell is QUALIFIED.

**1a.** `docs/v2/architecture/prototype-evidence-reference.md:26-30`. Verified: "does **not** establish a digest-pinned language-quality corpus … do not exist in this V2 snapshot and remain OPEN".

- **Insert:** a new blockquote paragraph after `docs/v2/architecture/prototype-evidence-reference.md:30`, separated by blank lines. APPLIED in the working tree.
- **Exact text:**

```markdown
> **Current applicability (2026-10-02) — DR-118/DR-G13:** The statement above that no digest-pinned language-quality corpus exists describes this reference's original snapshot. DR-118 is SATISFIED under D-369 (see the DR-118 row of the [register](08-decision-and-readiness-register.md)), and its digest-pinned design corpus is [`quality-corpus-manifest.v1.json`](../../coop/completion/quality-corpus-manifest.v1.json) (SHA-256 `2a4c2fe0…`). That corpus covers the TypeScript preview only: 1,010 `.ts` sources, `productExecution: false`. The executable JS/Rust product corpus remains OPEN under DR-G13 `harness.DR-G13.product-v1` ([admission-and-qualification §3](../contracts/product-v1/admission-and-qualification.md#3-full-product-matrix-and-report-schema)). No language-quality cell is QUALIFIED. This note changes no grade or requirement.
```

**1b.** `docs/v2/architecture/02-distribution-and-components.md:334-342`. Verified at 336-338: "No such digest-pinned quality corpus or accepted measurement manifest exists in this V2 snapshot". **Same-kind addition** at 339-341: "The exact languages … are product decisions; V2 does not invent a support list or choose analyzer implementation languages." That is superseded by D-371's TS/JS + Rust selection. One note covers both.

- **Insert:** a new blockquote paragraph after `docs/v2/architecture/02-distribution-and-components.md:342`, separated by blank lines. STAGED in `staged-notes.patch` (not applied; see §2).
- **Exact text:**

```markdown
> **Current applicability (2026-10-02) — DR-118/DR-G13 and D-371:** The two statements above are stale. First, "No such digest-pinned quality corpus … exists": DR-118 is SATISFIED under D-369 (see the DR-118 row of the [register](08-decision-and-readiness-register.md)), and its digest-pinned design corpus is [`quality-corpus-manifest.v1.json`](../../coop/completion/quality-corpus-manifest.v1.json) (SHA-256 `2a4c2fe0…`). That corpus covers the TypeScript preview only: 1,010 `.ts` sources, `productExecution: false`. The executable JS/Rust product corpus remains OPEN under DR-G13 `harness.DR-G13.product-v1` ([admission-and-qualification §3](../contracts/product-v1/admission-and-qualification.md#3-full-product-matrix-and-report-schema)). No language-quality cell is QUALIFIED. Second, "V2 does not invent a support list": [D-371](../../coop/COORDINATOR-DECISIONS.md#d-371--one-product-design-implemented-in-stages) selects TypeScript/JavaScript and Rust as the native language roles ([scope chapter](10-mvp-and-future-scope.md#one-product-design)). This note changes no requirement.
```

**1c.** `docs/v2/architecture/05-v1-to-v2-relationship.md:102`. Verified, table row "Language capability and baseline quality … OPEN: future digest-pinned role/corpus capability matrix". The note goes after the table.

- **Insert:** a new blockquote paragraph after `docs/v2/architecture/05-v1-to-v2-relationship.md:102`, separated by blank lines. STAGED in `staged-notes.patch` (not applied; see §2).
- **Exact text:**

```markdown
> **Current applicability (2026-10-02) — DR-118/DR-G13:** In the row "Language capability and baseline quality", the text "OPEN: future digest-pinned role/corpus capability matrix" is stale. DR-118 is SATISFIED under D-369 (see the DR-118 row of the [register](08-decision-and-readiness-register.md)), and its digest-pinned design corpus is [`quality-corpus-manifest.v1.json`](../../coop/completion/quality-corpus-manifest.v1.json) (SHA-256 `2a4c2fe0…`). That corpus covers the TypeScript preview only: 1,010 `.ts` sources, `productExecution: false`. The executable JS/Rust product corpus remains OPEN under DR-G13 `harness.DR-G13.product-v1` ([admission-and-qualification §3](../contracts/product-v1/admission-and-qualification.md#3-full-product-matrix-and-report-schema)). No language-quality cell is QUALIFIED.
```

**1d.** `docs/v2/architecture/08-decision-and-readiness-register.md:329`, the DR-203 row. Verified: "no digest-pinned language-quality corpus or accepted measurement baseline is yet recorded", and "the quality half stays OPEN there". The note goes after the five-review table (after line 331).

- **Insert:** a new blockquote paragraph after `docs/v2/architecture/08-decision-and-readiness-register.md:331`, separated by blank lines. STAGED in `staged-notes.patch` (not applied; see §2).
- **Exact text:**

```markdown
> **Current applicability (2026-10-02) — DR-203/DR-118:** The DR-203 finding "no digest-pinned language-quality corpus or accepted measurement baseline is yet recorded", and the impact "the quality half stays OPEN there", record the 2026-08-13 scope. DR-118 is SATISFIED under D-369 (see the DR-118 row of the [register](08-decision-and-readiness-register.md)), and its digest-pinned design corpus is [`quality-corpus-manifest.v1.json`](../../coop/completion/quality-corpus-manifest.v1.json) (SHA-256 `2a4c2fe0…`). That corpus covers the TypeScript preview only: 1,010 `.ts` sources, `productExecution: false`. The executable JS/Rust product corpus remains OPEN under DR-G13 `harness.DR-G13.product-v1` ([admission-and-qualification §3](../contracts/product-v1/admission-and-qualification.md#3-full-product-matrix-and-report-schema)). No language-quality cell is QUALIFIED. DR-203's grade is unchanged.
```

### Item 2 — Chapter 10 says language roles are open

Current authority: `10-mvp-and-future-scope.md:40` ("TypeScript/JavaScript through the TypeScript role, and Rust through the Rust role") under D-371 (`COORDINATOR-DECISIONS.md` D-371: "TypeScript/JavaScript and Rust supply the selected depth").

**2a.** `10-mvp-and-future-scope.md:143`. Verified: "exact supported roles remain an open product decision". The note goes after the MVP table (after line 145).

- **Insert:** a new blockquote paragraph after `docs/v2/architecture/10-mvp-and-future-scope.md:145`, separated by blank lines. STAGED in `staged-notes.patch` (not applied; see §2).
- **Exact text:**

```markdown
> **Current applicability (2026-10-02) — D-371:** In the row "Self-contained runtime/tool closure", the text "exact supported roles remain an open product decision" is superseded. [D-371](../../coop/COORDINATOR-DECISIONS.md#d-371--one-product-design-implemented-in-stages) selects TypeScript/JavaScript (TypeScript role) and Rust (Rust role); see [the selected design scope](#one-product-design). DR-118/119 still settle each capability/platform cell, and DR-G13 product qualification remains unperformed.
```

**2b.** `10-mvp-and-future-scope.md:154`. Verified: "role list and parity thresholds remain open; no list is invented here". Additional languages beyond TS/JS and Rust do remain open (line 40), so the note limits the supersession to the MVP set. The note goes after the deferred table (after line 156).

- **Insert:** a new blockquote paragraph after `docs/v2/architecture/10-mvp-and-future-scope.md:156`, separated by blank lines. STAGED in `staged-notes.patch` (not applied; see §2).
- **Exact text:**

```markdown
> **Current applicability (2026-10-02) — D-371:** In the row "Additional language/tooling roles", the MVP role set is no longer open. D-371 selects TS/JS and Rust ([selected design scope](#one-product-design)). Only languages beyond that set need a later explicit support decision. Thresholds for selected product cells are in [admission-and-qualification §3](../contracts/product-v1/admission-and-qualification.md#3-full-product-matrix-and-report-schema).
```

### Item 3 — DR-011 residual subledger reads OPEN

`docs/v2/architecture/08-decision-and-readiness-register.md:83-98`. Verified: R01–R05 and R08–R16 read OPEN; R06 and R07 read NARROWED. Current authority: D-372 condition 1 **MET** (`docs/v2/architecture/08-decision-and-readiness-register.md:398`). `docs/coop/design-corrections/inherited-residuals.applied.v1.json` (SHA-256 `ae6901d1813d3026a45bb73fc5c20d01ab207177a85911853cb09fc6ef6c99b8`) carries all 16 residuals, each `designGrade: ACCEPT-DESIGN`, effective through `application-activation.v1.json`.

- **Insert:** a new blockquote paragraph after `docs/v2/architecture/08-decision-and-readiness-register.md:98`, separated by blank lines. STAGED in `staged-notes.patch` (not applied; see §2).
- **Exact text:**

```markdown
> **Current applicability (2026-10-02) — D-372 condition 1:** The OPEN and NARROWED statuses in this subledger are the pre-D-372 record. Under D-372, condition 1 is MET ([condition table](#unified-product-design-readiness)). All sixteen residuals DR-011-R01–R16 carry ACCEPT-DESIGN dispositions in [`inherited-residuals.applied.v1.json`](../../coop/design-corrections/inherited-residuals.applied.v1.json) (SHA-256 `ae6901d1…`). R12's evaluation sub-residuals are disposed in [`evaluation-residual-dispositions.applied.v1.json`](../../coop/design-corrections/evaluation-residual-dispositions.applied.v1.json), and the blind consumer B continuation closes R10. These dispositions take effect through the [D-372 activation](../../coop/design-corrections/application-activation.v1.json). They are design-level only. DR-012 implementation and release qualification remains unperformed, and no old rejected or unreviewed checker gains standing.
```

### Item 4 — G17 and G26 say SARIF is dropped

`docs/v2/architecture/08-decision-and-readiness-register.md:362` (DR-G17: "dropped / inapplicable (D-077 SARIF drop; D-086). not required-now") and `:371` (DR-G26: "D-077 drop stands", "G17 remains inapplicable"). Both verified. Current authority:

- D-372, "Explicit product and output re-entry acts" (`COORDINATOR-DECISIONS.md:24152-24156`), re-enters SARIF exactly for default, analyze, audit and repair-verify, and reactivates DR-G17.
- `qualification-gates.applied.v1.json` (SHA-256 `33b8d13c63b49b4d4526b5a4b6daa0fd986a7df0abfa2286c1ff642e0e63a0ce`): `items[16]` (G17 "REACTIVATED for full product") and `items[25]` (G26 "Preview non-advertisement remains historical only … no broad SARIF drop").

**Same-kind addition:** the DR-123 row (`:312`) says "G17 inapplicable (D-077)" twice. The note also covers it. The register's per-row map at `:431` (DR-122) is already current. One note after the gate table (after line 377) covers G13 (item 5), G17 and G26.

- **Insert:** a new blockquote paragraph after `docs/v2/architecture/08-decision-and-readiness-register.md:377`, separated by blank lines. STAGED in `staged-notes.patch` (not applied; see §2).
- **Exact text:**

```markdown
> **Current applicability (2026-10-02) — DR-G13, DR-G17, DR-G26:** The [applied gate map](../../coop/design-corrections/qualification-gates.applied.v1.json) (SHA-256 `33b8d13c…`) owns current gate standing under D-372 condition 4.
>
> - **DR-G17:** "dropped / inapplicable (D-077 SARIF drop; D-086). not required-now" is the historical preview disposition. [D-372](../../coop/COORDINATOR-DECISIONS.md#d-372--complete-intended-product-design-correction-and-application) ("Explicit product and output re-entry acts") re-enters authoritative SARIF for default, analyze, audit and repair-verify. It also reactivates G17 as a required product gate, not yet performed (gate map `items[16]`, `harness.DR-G17.product-v1`). The DR-123 row's "G17 inapplicable (D-077)" likewise applies only to the preview.
> - **DR-G26:** "D-077 drop stands" and "G17 remains inapplicable" apply only to the historical preview. Gate map `items[25]` (`harness.DR-G26.product-v1`) requires exact declared command/format applicability and loss disclosure under G17, with no broad SARIF drop.
> - **DR-G13:** "cold/warm p95" and "Product thresholds DECIDED by D-369" describe the preview harness. For product cells, [admission-and-qualification §3](../contracts/product-v1/admission-and-qualification.md#3-full-product-matrix-and-report-schema) governs. It requires 3 warmups then 7 measured runs, median elapsed time and maximum RSS, and limits of 1.20× median time and 1.25× peak RSS against a reviewed baseline, plus absolute bounds. Gate map `items[12]` repeats the preview wording; this is recorded as a finding for a later gate successor ([record-hygiene item 5](../../implementation/m3/record-hygiene/PROPOSAL.md)).
>
> No gate is QUALIFIED or DEMONSTRATED, and no threshold changes.
```

### Item 5 — QG items[12] (DR-G13 product-v1) contradicts AQ §3 (finding only)

`qualification-gates.applied.v1.json` `items[12]` keeps the preview wording: `requiredEvidence` "cold/warm p95 and process-tree RSS", `thresholdDisposition` "Product thresholds DECIDED by D-369". The register's DR-G13 row (`docs/v2/architecture/08-decision-and-readiness-register.md:358`) repeats it verbatim. The preview numbers come from `quality-corpus-manifest.v1.json` `performance` (30 cold + 30 warm samples, 5 warmups, cold p95 10000 ms, warm p95 5000 ms, RSS 1 GiB). `admission-and-qualification.md` §3 (`:267-286`, contract SHA-256 `69cd6ba3cb41ed191e0a4e5cc20b191f4b8761625843b585426157873dbee6b3`) specifies something different for product cells:

- 3 warmups, then 7 measured runs;
- median elapsed time and maximum RSS;
- 1.20× median time and 1.25× peak RSS against an existing baseline, plus reviewed absolute bounds;
- a reviewed initial baseline for new cells.

**Finding RH-5 (for a later gate successor):** QG `items[12]` and the register's DR-G13 row cite the preview p95 regime for `harness.DR-G13.product-v1`. **AQ §3 governs product cells.** The applied QG JSON is not edited. The register note in item 4 states this at the DR-G13 row. A future gate-map successor should replace `items[12].requiredEvidence` and `thresholdDisposition` with an AQ §3 citation. It should keep the D-369 preview thresholds as `inheritedHarness` history.

### Item 6 — Implementation authorization

`docs/v2/architecture/08-decision-and-readiness-register.md:402`: condition 5 "NOT MET. The user authorized architecture/design/reference work only." Verified. **Same-kind additions:** the register header `:9-10`, the readiness heading `:381` ("implementation is not authorized"), `12-architecture-completion-goal.md:8` ("Condition 5 remains NOT MET"), and root `README.md:5` ("Implementation is not authorized").

**What I found.** The owner's direction to implement is recorded only in implementation records:

- `docs/implementation/m1/progress-checkpoint-before-interruption02.md:5-7` (also `…-before-owner04.md`): "The user authorized the entire implementation with actual Claude verifying the work, and asked us to continue until complete." Introduced in `13e3d8701` (2026-09-16).
- `docs/implementation/ACTIVE-WORK.md:5`: "User authorizes continuous full-project implementation …" (`13e3d8701`). Also `:390`: "User reauthorized continuous autonomous implementation through fullprojectcompletion" (`efb1dc1e5`, 2026-09-16).
- `docs/implementation/README.md:3`: "Local commits in both repositories are authorized. The user will push" (`671609e4d`, 2026-09-21).

**What I did not find.** No `COORDINATOR-DECISIONS.md` entry after D-372 exists; the file ends at D-372. No register successor and no `docs/coop` record mark condition 5 MET. D-371 and D-372 both say they grant no implementation authorization. I did not invent one. The notes point to the implementation records and say the condition 5 record is **pending owner record**. Condition 5 itself stays as written.

- **Insert:** a new blockquote paragraph after `docs/v2/architecture/08-decision-and-readiness-register.md:402`, separated by blank lines. STAGED in `staged-notes.patch` (not applied; see §2).
- **Exact text:**

```markdown
> **Current applicability (2026-10-02) — implementation authorization:** Product implementation (M1, M2) is under way at the owner's direction. That direction is recorded in the implementation records, not in this register or in a coordinator decision. The records are the [M1 checkpoint](../../implementation/m1/progress-checkpoint-before-interruption02.md) ("The user authorized the entire implementation …"), the [active-work log](../../implementation/ACTIVE-WORK.md) (opening direction, and the later "User reauthorized continuous autonomous implementation through fullprojectcompletion" entry) and the [implementation overview](../../implementation/README.md) (local commits authorized, no push). The earliest of these entries was committed in `13e3d8701` (2026-09-16). No COORDINATOR-DECISIONS entry or register successor records condition 5 as MET; that record is **pending owner record**. This note changes no condition, grade or gate.
```

The register header gets a pointer note (after line 10):

- **Insert:** a new blockquote paragraph after `docs/v2/architecture/08-decision-and-readiness-register.md:10`, separated by blank lines. STAGED in `staged-notes.patch` (not applied; see §2).
- **Exact text:**

```markdown
> **Current applicability (2026-10-02) — implementation authorization:** See the note after the [condition table](#unified-product-design-readiness). Condition 5's standing here is unchanged.
```

`12-architecture-completion-goal.md` (after line 9):

- **Insert:** a new blockquote paragraph after `docs/v2/architecture/12-architecture-completion-goal.md:9`, separated by blank lines. STAGED in `staged-notes.patch` (not applied; see §2).
- **Exact text:**

```markdown
> **Current applicability (2026-10-02) — implementation authorization:** See the register's note after the [condition table](08-decision-and-readiness-register.md#unified-product-design-readiness). M1/M2 implementation proceeds at the owner's direction recorded in the implementation records; the condition 5 record is pending owner record.
```

Root `README.md` (after line 5):

- **Insert:** a new blockquote paragraph after `README.md:5`, separated by blank lines. STAGED in `staged-notes.patch` (not applied; see §2).
- **Exact text:**

```markdown
> **Current applicability (2026-10-02) — implementation authorization:** Product implementation (M1, M2) proceeds at the owner's direction, recorded in [docs/implementation](docs/implementation/README.md). The register's condition 5 record is pending owner record; see the note after its [condition table](docs/v2/architecture/08-decision-and-readiness-register.md#unified-product-design-readiness).
```

Not annotated: `docs/v2/architecture/08-decision-and-readiness-register.md:484` (inside the "Blueprint-readiness decision" historical D-369 entry record) and `10-mvp-and-future-scope.md:127` (D-370-era paragraph inside the historical scope map). Both are historical in context; the item 6 notes cover the current reading path.

## 4. Other same-kind text checked, left unannotated

- `07-review-record.md:192`: "quality/parity claims stay OPEN until backed by a digest-pinned corpus". This is a
  historical review checklist under the chapter's D-372 banner ("The findings and scope below are historical").
- `12-architecture-completion-goal.md:76`: "SARIF drops". This is inside "Historical preview completion target".
- `08…:541`: "G17 is inapplicable (D-077)". This is inside "Historical preview position — measured snapshot, 2026-09-05".

## 5. Chapter 11 (non-binding synthesis): listed only

`11-three-reviewer-direction-synthesis.md` has an "Authority: None" banner and no current-applicability notes, so
it gets no notes. Superseded points:

| Line | Text | Superseded by |
|---|---|---|
| 276 | "There is no gate for analyze latency on a representative TypeScript repository—only help/version RSS." | DR-G13 product-v1 performance cells: AQ §3 (`admission-and-qualification.md:267-286`); QG `items[12]` |
| 314 | "Keep Rust depth deferred and marketplace scope excluded unless an explicit successor says otherwise." | Rust half: D-371 selects Rust depth (`10-mvp-and-future-scope.md:40`). The marketplace exclusion still stands (`10…:152`). |
| 122 | "Rust depth deferred not abandoned" (a successor-shape suggestion) | D-371; AQ §5 (the DR-117 seven-item successor applied by D-372) |
| 300 | "a corpus that DR-118/G13 confirm does not exist" | DR-118 SATISFIED (D-369) with `quality-corpus-manifest.v1.json` (TS preview); JS/Rust executable corpus OPEN under DR-G13 product-v1 |

## 6. Self-check

Working tree after this batch, at base `fb8472da8`:

- `git diff --stat`: this batch's only tracked change is `docs/v2/architecture/prototype-evidence-reference.md | 2 ++`.
  `git diff --stat` also shows `docs/implementation/m3/analysis-quality/PLAN.md` modified, and
  `analysis-quality/PLAN-r1.md` is untracked. Both appeared during this session from concurrent work, not from
  this batch, and were not touched. This file is untracked and new, as is `staged-notes.patch`
  (SHA-256 `03e030a6b62581150e1be9d10901485f30978a8ae6738d07fb37205d1b587880`; 6 files, 28 insertions;
  `git apply --check` passes).
- No file under `docs/v2/contracts/` changed. `docs/coop/COORDINATOR-DECISIONS.md` is unchanged. The applied
  QG JSON is unchanged. `docs/implementation/m2/` and the product repository are untouched. The product
  verifier was run from a copy in a scratch directory.
- **Checkers, run read-only:**
  - `docs/operations/check-catalog-links.py`: PASS 1463 catalog links.
  - `docs/operations/generate-current-design-catalog.py --check`: PASS.
  - `docs/operations/check_repository_file_inventory.py --check`: PASS (198 paths).
  - `docs/operations/check-document-custody.py`: `FAIL 858 missing references`. This is pre-existing, and the
    output is byte-identical before and after the edit. The script exits 0.
  - Product `tools/verify_design.py --architecture <arch>` (copied; uses the product `design-lock.json`): exit 0.
  - D-372 application manifest: all 197 applied files still match.
- **Not regenerated.** `docs/operations/document-inventory.v1.json`, `document-classification.v1.json`,
  `design-corrections/task-opening.json` and the `historical-preservation-report.v*.json` series still carry
  the prototype reference's old SHA-256 `69a71aac…`. They are accounting and historical-baseline records. No
  checker reads that hash, and none requires regeneration.
- **Not run.** `check_implementation_planning.py` needs a materialized product `--source` snapshot.
  `check-integration.py` and `check-architecture-application.v1.py` always write a report, and neither reads
  these chapters. `check_native_evidence.v2.py` writes its report on every run. Its pins include chapter 10,
  which is unchanged.

## Lead decision (2026-10-03): an errata record now, in-place notes with the next successor

The pinned files above cannot take in-place notes without changing D-372's activation subject, or, for the register, the product `design-lock.json`. A successor whose only purpose is notes would be an application-manifest review plus a design-lock unit for no change in meaning. The lead therefore decides:
1. **This batch is committed as the errata record.** It holds this PROPOSAL (every stale passage, its current authority and its exact note text), `staged-notes.patch`, and the one applied note in the unpinned `prototype-evidence-reference.md`. `docs/implementation/README.md`, which is unpinned, points readers here.
2. **The 12 staged notes land with the next successor that re-pins their files.** That means the next application-manifest successor, or the next product design-lock change that touches the register. That successor applies `staged-notes.patch` and records the new hashes.
3. **RH-5** (QG items[12] versus AQ §3) goes to the next DR-G13 gate successor. The M3 analysis-quality plan's D1 and D13 already cover it.

**Rejected:** a note-only manifest and design-lock successor now. It costs a full review cycle and moves D-372's activation subject for no change in meaning.
