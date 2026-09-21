# Independent review — corrected initial-root owner 401

Reviewer: Claude Opus 5 (1M context), `claude-opus-5[1m]`. Capacity available; substantive review
performed. Bounded owner/reference review, document and model only; no native work needed or done.

**Top verdict: ACCEPT-DESIGN-UNIT**, with **one required finding** (non-blocking, and listed because
the request asks for remaining findings even when non-blocking).

Both required findings from my owner399 review are closed, root's own additional EEXIST gap is closed,
and my two non-required observations are answered by a supplement whose central claims I re-derived
independently. One documentation inconsistency remains inside the unit.

---

## 1. Verification

| Artefact | Declared | Match |
|---|---|---|
| `…/trials/initial-root-binding-proposal-401/subject.tar.xz` | 91 504 B, `6e2fd71d8a4954ca4760649378474a1fa3eb84717a19d54f3461812258a1b833` | ✓ |
| `…/trials/initial-root-binding-proposal-401/subject.json` | 7 680 B, `b00b694892aa00d1ef4da6fa2665b22fb18efe3aa7ae457e4b92c473afcffa0d` | ✓ |

Both verified **before** extraction; extraction only into this review directory. **49 / 49** members
verified byte-for-byte and by sha256: 0 missing, 0 extra, 0 mismatched, 0 unsafe.

**47 anchors; 46 match live; all 16 product anchors match at `cd5af4d`.** The single live mismatch is
the declared historical `crates/platform/src/filesystem.rs` (73 907 B / `9a02dcbb…` at `cd5af4d`, live
81 671 B after the runtime32 integration). No pin is stale and none was edited.

**Models unchanged from 399, verified against my own retained 399 copies:** `preinstallation_model.py`,
`publication_model.py`, `check_preinstallation.py`, `check_publication.py`,
`check_digest_compatibility.py`, `surface_model.py`, `check_surfaces.py`, `lineage_probe.rs`,
`run_lineage_probe.py` — all **byte-identical**.

Replay: the 39 surface checks PASS and regenerate `surface-checks.json` **byte-identically to 399's**;
the 22 new diagnostic composition checks PASS and regenerate `diagnostic-checks.json` byte-identically.
The 392/390 historical counts (54 / 36 / 7 / 9 / 7 lineage) are carried and correctly **not** claimed as
rerun for 401.

---

## 2. Closure of the required findings

### RF-1 — the reconciliation list — **CLOSED**, with three root corrections I verified

§9 now names `check_workflows` and `workflow-cases` explicitly, and adds schema-first coordinated
activation: register the enum and bindings coherently **before** emission.

Three corrections came from root, and each is right:

1. **The function is `doctor(store_openable, defects)`, not `doctor_report`.** 399's text said
   `doctor_report`, and I repeated that phrasing in my finding's summary even though the body cited
   `M.doctor(True, [two defects])` correctly. 401 uses the real name throughout.
2. **The helper need not append the notice.** *"the assembler owns that observation and one reserved
   notice; the helper receives the already assembled admitted detail list and computes the one agreed
   count."* This is the right shape and it dissolves the concrete hazard behind my finding: an
   unconditional append inside `doctor()` would have changed the existing two-defect fixture. 401 keeps
   that case and adds complete-root cases beside it.
3. **"The latest selected workflow reference"** is the `import-totality-reference-selection-v1`
   reference copy, not the older `docs/coop/design-corrections/workflows` file — see §4, where getting
   this wrong nearly cost me a false finding.

### RF-2 — the capacity change — **CLOSED**

> …256 actual defects to **255 actual defects plus one informational entry**. … 255 actual defects are
> admitted; 256 actual defects cannot produce this bounded complete-root report and must refuse and
> latch the report session, never truncate.

with the goldens required explicitly — *"including 255 actual defects admitted and 256 actual defects
refused-and-latched"* — and the **256-entry bound retained** where no note applies. That is exactly the
statement and the boundary golden I asked for.

### Root's own additional gap — EEXIST — **CLOSED**

Root found a cross-unit inconsistency I had not: §4's raw-EEXIST "clean loss" language did not match
source396/400's typed classification. 401 now requires both:

> AlreadyExists AND target visibility Unchanged is the no-publication loser route. … EEXIST/AlreadyExists
> error alone is insufficient: a failed original-stage postcheck makes the outcome Indeterminate even
> when the primary syscall error is preserved.

and adds that the parent-barrier association uses the publication's duplicate handle. Both statements
match the source400 behaviour I verified in the companion review, so the owner and the primitive now
agree.

---

## 3. The diagnostic supplement — claims re-derived, not accepted

My O-1 said neither new code is emittable under the selected 317-code enum, and O-2 said no model in
the unit could express that. The supplement answers both. I checked its three load-bearing claims
myself.

**(a) 317 → 319, order preserved, same identity.** Comparing the draft `common.schema.json` with the
selected `common-v4.schema.json`:

| Check | Result |
|---|---|
| Selected enum size | **317** |
| Candidate enum size | **319** |
| First 317 entries preserve the selected order exactly | **yes** |
| Appended | `INSTALLATION.DURABILITY_NOT_CHECKED`, `INSTALLATION.NOT_INITIALIZED` |
| `$id` unchanged | **yes** — `urn:opensip:product-v1:workflows:evaluator3:common:4` |
| Candidate enum unique | yes |
| Every other `$def` byte-identical | **yes** (0 differing) |

So "preserve old schema enum order, append two, same unreleased ID, not a new public major" is exact.
The `public-detail-registry.json` carries **319 distinct codes** whose set equals the candidate enum.

**(b) The 22 composition cases cover the boundary.** The count table is the evidence:

| Case | entries | `defectsFound` | termination detail |
|---|---|---|---|
| `complete-root-0` | 1 | **0** | **none** — no `DOCTOR.DEFECTS_FOUND` |
| `complete-root-1` | 2 | 1 | `DOCTOR.DEFECTS_FOUND` |
| `complete-root-254` | 255 | 254 | `DOCTOR.DEFECTS_FOUND` |
| `complete-root-255` | **256** | **255** | `DOCTOR.DEFECTS_FOUND` |
| `complete-root-256`, `-257` | — | refuse | — |

plus `no-informational-notice-{0,1,2,256}` proving the 256 bound survives where no note applies, the
`trust-doctor` and `store-status` no-note cases, both new codes against old and candidate schemas, and
refusals for `unknown-code`, `boolean-count`, `new-envelope-field`, `oversized-detail-array`,
`new-detail-field` and `informational-code-in-actual-defect-input`. `complete-root-255` is precisely the
RF-2 boundary at the schema cap.

**(c) The preparation-guard account is accurate.** The first guard compared registry and schema
enumeration **order**; the 317 sets agree but historical ordering differs, so it refused **before
writing the candidate schema**. The corrected comparison uses unique set equality and preserves the
original 317 positions. My own check confirms the positions are preserved and no selected byte changed.

---

## 4. A near-miss worth recording

My first AST comparison used `docs/coop/design-corrections/workflows/workflows_model.v1.py` and found
**four** changed top-level functions — `run_invocation`, `registry_row`, `glob_match` and `doctor` —
which would have contradicted the "doctor only" claim.

That baseline was wrong. The latest **selected** workflows model is the reference copy inside
`import-totality-reference-selection-v1` (locked at `/contractSuccessors/29`, `ACCEPTED-DESIGN-UNIT`,
`rootSubstantiveAssent: true`, zero required findings), sha `60dc11e2…`. Against that baseline:

| Baseline | Top-level statements | Changed nodes |
|---|---|---|
| **selected import-totality reference** | 118 / 118 | **`doctor` only** (117 others unchanged) |
| older coop copy | 118 / 118 | `run_invocation`, `registry_row`, `glob_match`, `doctor` |

The extra three are exactly the import-totality fixes the draft correctly preserves, which is what root
meant by "latest import-totality reference preserves prior fixes". My corrected count of 117 unchanged
statements agrees with the supplement's own reported figure. `check_diagnostics.py` itself sets
`BASE` to that selected reference, so it targets the right baseline by construction.

I record this because it is the third time a stale or wrong baseline has nearly produced a false
finding in this series, and because the fix is now mechanical: resolve "latest selected" through the
lock, never through a familiar path.

---

## 5. Required finding

### RF-1 (non-blocking) — the supplement's README contradicts the owner draft it ships with

`diagnostic-draft/README.md` ends:

> Other owner399 issues and **root EEXIST concern remain unresolved**.

The owner draft in the same frozen archive resolves that concern — "AlreadyExists AND target visibility
Unchanged is the no-publication loser route… EEXIST/AlreadyExists error alone is insufficient…". A
reader taking the unit as a whole gets two answers, and the reconciliation reviewer may carry the stale
one forward.

*Required:* update the supplement README to match the owner draft, or scope the sentence to what the
supplement itself does not cover.

---

## 6. Observations

- **O-1.** `check_diagnostics.py` reads its baseline and schemas **by path** from the live trees, not by
  pinned digest. Its PASS therefore attests the composition against today's live bytes; if the selected
  reference or schema moves, the frozen result is stale. The same scope note applied to the inventory
  v59-r2 helper, and root already qualified that one. The README's "A formal successor must bind the
  exact current schema and source maps" is the right forward statement.
- **O-2.** The supplement is explicitly mutable, not frozen, not a formal successor, and not generated
  bindings or a public renderer. Accepting this unit accepts the owner reasoning and the reference
  evidence, not a schema change.
- **O-3.** The five composition gaps remain open and are still correctly labelled. The carried
  publication model is disclosed as idealized state rather than native errno/post-check classification —
  an honest limit, and the reason the EEXIST reconciliation had to be made in prose rather than found by
  that model.
- **O-4.** `INSTALLATION.NOT_INITIALIZED` and `INSTALLATION.DURABILITY_NOT_CHECKED` remain
  **unemittable** against the selected schema until the enum successor lands. 401's schema-first
  ordering makes that a stated precondition rather than an implicit one.

---

## 7. Limits

- **Level:** document and model reading, archive/anchor verification, model replay, and independent
  re-derivation of the supplement's schema, registry and AST claims.
- **No native work**, as instructed. Source400/formal34 is reviewed separately; neither review depends
  on the other, and this one grants it nothing.
- **Not qualified:** native eligibility producers, actor/custody/profile qualification, P0 construction,
  shared budgets, crash and power-loss behaviour, GC, Linux, release.
- **Not rerun:** the 392 preinstallation/publication/canonical counts and the 390 lineage checks.
- **Unselected references remain unselected:** this owner, S9.3, `store-instance-lineage.v1.json`,
  `host-foundation-completion.v2.md`, 215. 401 is **not** a formal passage successor; selection requires
  a separately reviewed formal passage/schema/reference unit and root assent.
- `M/initial-root-binding-reconciliation` is root's working area outside this frozen unit and carries no
  authority here; I did not review it.

---

## 8. Context HEADs — as of 2026-09-21T16:31:53-07:00

| Repository | HEAD | Subject |
|---|---|---|
| architecture | `35bb623b76bb6ec259946c25092f20fa71aa9328` | "Clarify publication receipts and freeze initialization reconciliation corrections" |
| product | `4b298dae44e553e8317cf68350f5201cd3fc6771` | (clean) |

Stated as of that sample only; the byte pins above are the authority.

---

## 9. Attestation

Read-only against live, frozen, history, product and lock. No byte edited, no pin edited, no select
script run, no native build, no commits, no pushes. All writing went into this review directory;
extraction went only there.

This grants no root assent, no formal selection, no passage reconciliation, no native owner or writer
permission, no current authority, no S9.3 or 215 adoption, no whole-M2 approval and no release
qualification. Every earlier report — including owner397, its fact addendum, owner399 and the companion
source400/formal34 review — is untouched and keeps its own standing.

Reviewer: Claude Opus 5 (1M context).
