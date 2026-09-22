# Addendum to integration audit 405 — four corrections and the manifest-precedence answer

Auditor: Claude Opus 5 (1M context), `claude-opus-5[1m]`. **Separate note. `NOTES.md` and
`evidence/source-pins.json` are unchanged and remain the audit of record** — their digests
(`40096db0995e7744…`, `6850f2c6d867aeab…`) are unaltered, and this addendum is deliberately listed
separately in `hashes.txt`. Read-only; no native jobs; nothing edited; no commits or pushes. Still
advice, not acceptance. Evidence: `evidence/addendum-pins.json`.

Root raised four concrete points. I checked each mechanically rather than accepting it. **Three of my
405 statements were wrong, one attribution was wrong, and the precedence question has a definite
answer that changes the practical recommendation.**

---

## 1. "Maps need no edit" — **wrong**. Three pinned bindings move.

I checked only whether the *mappings* (schemaId → path → namespace) changed. They do not. But every
one of these rows carries a **digest pin**, and those move with the bytes:

| Binding | Carries | Current common-v4 pin |
|---|---|---|
| `schemas/source-map.json` → common:4 row → `architectureSource` | `{path, sha256, bytes}` | 64 866 / `6af81f35…` |
| `schemas/admission-source-map.json` → common:4 row → `architectureSource` | `{path, sha256, bytes}` | 64 866 / `6af81f35…` |
| `admission-registry.json` → `sources[]` common:4 row | `{schemaId, sourcePath, bytes, sha256}` | 64 866 / `6af81f35…` |

So a 317→319 extension requires updating **both maps and the admission registry**, not just the schema,
the closure pin and the bindings. `admission-source-map.json` additionally pins
`registryArchitectureSource` → `…/admission-runtime-selection-v1/schemas/admission-registry.json`
(17 170 / `59cbb0cd…`), so changing the registry moves that pin too — a second-order edit my 405 also
missed.

The registry holds **48 sources and 15 aliases**. The `common:1` alias row
(`workflows/schemas/common.schema.json` → `common-v1.schema.json`, 55 042 B) is the historical alias
root says stays unchanged; nothing in the common:4 extension touches it. The 48 sources match the
"48 reference inputs" root reports pinned in private 406.

**Correction to 405 §D:** delete "Maps need no edit". The consumer set is schema → both maps →
admission registry → `registryArchitectureSource` → generator closure → generated bindings.

## 2. "No architecture-side common:4 carrier" — **wrong**.

The carrier exists at
`docs/implementation/m1/source-selection-v2/schemas/sources/common.v4.schema.json`, **64 866 B /
`6af81f35c53ce74acbb0609d50524ab9d0b0ae1c2b772e9581dfb9f8535eaed9`** — **byte-identical to the product
copy**, and named explicitly by `architectureSource` in *both* product maps. It is one of the 136
candidates of `docs/implementation/m1/source-selection-v2/successor.json`.

My error was scope: I searched `docs/coop/design-corrections/workflows/schemas/` for arch carriers,
found `:common` (315) and `:common:3` (315), and concluded there was no common:4 anywhere in the
architecture. I never looked under `docs/implementation/m1/`.

One precision I owe, stated as a limit rather than a dispute: I did **not** find that successor or the
carrier in `design-lock.json` or in `approvals.sourceManifest` by the queries I ran. Its authority for
this purpose does not depend on that — the product maps bind the path *and digest* directly, so the
arch and product copies must move together regardless. Root's new current path
`…/initial-root-binding-owner-selection-v1/schemas/common.v4.schema.json` is a working draft and is not
reviewed here.

**Correction to 405 §D:** the extension is *not* product-only. It is a paired arch+product byte change
that both maps pin.

## 3. Manifest precedence — root is right, and it settles the question

`tools/verify_design.py` lines 515-522:

```python
manifest = approvals["applicationManifest"]          # line 495
...
effective = {}
for document in (approvals["sourceManifest"], manifest):
    ...
    effective[row["path"]] = row                     # plain assignment: last write wins
```

`effective` then feeds the `lock["inputs"]` check (533-536) and, for schemaVersion 4,
`successor_chain(architecture, lock, effective)` (544) — **the accepted-parent set**.

So for any path present in both manifests, the **applicationManifest row is the effective accepted
parent**, regardless of which pin the live file matches:

| Path | Effective (application) | sourceManifest | Live matches |
|---|---|---|---|
| `workflows/check_workflows.v1.py` | 114 055 / `5c64b593…` | 115 217 / `88edad11…` | sourceManifest |
| `workflows/workflow-cases.v1.json` | 243 554 / `22b74430…` | 245 182 / `f67d22f1…` | sourceManifest |
| `workflows/workflows_model.v1.py` | 139 660 / `b83f910f…` | 142 811 / `be37023f…` | sourceManifest |

**The exact mechanical constraint.** A successor that named the live coop files as accepted parents
would fail `same_reference` against `effective`, which holds the *older* application pins. And the
applicationManifest cannot simply be amended: lines 499-506 bind it to `activation`,
`applicationReview` (`verdict == "ACCEPT"`, matching `subjectManifestSha256`) and `rootAssent`
(`rootApplicationAssent is True`, matching `subjectManifestSha256`). Editing it would invalidate the
accepted application-46 chain — i.e. rewrite prior history.

**Answer to root's question: yes, adopting new copies as a new candidate is necessary, not merely
tidier.** It is the only route that leaves prior history intact. The successor should:

- carry **new copies** of the checker and vectors, derived from the newer `sourceManifest` bytes, at
  new paths under the new unit;
- record **provenance explicitly** — source path, the `sourceManifest` pin they were taken from, and
  the fact that the older `applicationManifest` pin remains the historical accepted parent for the old
  paths;
- ship **focused replacement checks** that exercise only the doctor behaviours, rather than re-running
  or re-freezing the whole workflow model;
- **not** rewrite, relabel or re-pin any application-46 artefact.

**The distinction to state in the successor, in these words:** *historically reviewed source* (the
newer `sourceManifest` bytes the live files match) is not the same as *effective accepted parent* (the
older `applicationManifest` pin that `verify_design.py` resolves). Both are selected; only the second
is what a contract successor may name as a parent.

This supersedes 405 §B-2, which said only "name which manifest governs". The mechanism already
governs, and it governs against the live files.

**Unchanged:** the latest selected reference successor remains current for workflow *behaviours* — it
is reached through `/contractSuccessors/29`, not through either approvals manifest, so none of the
above affects it.

## 4. The three-function delta — **accumulated, not all import-totality**

Measured along the chain:

| Step | Bytes | sha256 | Changed vs previous |
|---|---|---|---|
| coop (`approvals.sourceManifest`) | 142 811 | `be37023f…` | — |
| `predicate-matching-reference-selection-v1/reference` | 142 828 | `1d5212d5…` | **`run_invocation`, `glob_match`** |
| `import-totality-reference-selection-v1/reference` (latest) | 142 991 | `60dc11e2…` | **`registry_row`** only |

This matches the import-totality unit's own `evidence/draft-account.json`, which names
`predicate-matching-reference-selection-v1` as predecessor and states *"Only `registry_row` adds exact
string type guard … All other top-level AST unchanged."*

So 405 §B-1's phrase "the import-totality fixes" is wrong: import-totality contributed **one** function.
`M` holds **eleven** `*reference-selection*` unit directories, so the chain may extend further upstream
than the two steps I measured. **Correction:** call them *accumulated reference corrections across the
successor chain*, and preserve per-unit provenance rather than collapsing them under the latest unit's
name.

---

## What stands from 405

Unaffected by the above, and re-confirmed while checking it:

- **§A** — the checker and vectors are selected via `approvals.sourceManifest`, not `/inputs/*`. §3
  above sharpens *which pin* governs but does not change the channel finding.
- **§B-3** — `check-workflow-projection.v3.py` asserts the doctor golden mapping at lines 4355-4356 and
  was omitted from the reconciliation list. Root has accepted this.
- **§C** — the `DOCTOR.REPORT_NOT_PRODUCIBLE` divergence is pre-existing: the selected golden and the
  projection checker declare it; the selected reference model's `doctor-report` false branch does not
  emit it. Root's plan to amend that branch narrowly to the existing golden detail, changing `doctor`
  and `terminate` only and preserving the other 116 top-level statements, is exactly the minimal act
  §C described, and it replaces the adapter-only detail composition. It adds no owner law.
- **§D's Common1/Common3 protection** — `evidence.rs` carries all three enums in one file; the
  regeneration diff must add exactly two variants inside `Common4DomainDetailCode` and leave
  `Common1DomainDetailCode` and `Common3DomainDetailCode` at 315 in unchanged order. Root keeping the
  common:1 historical alias unchanged is consistent with this.
- **§E/§F** — the test table and the trusted-input-versus-renderer distinction are unchanged. Root's
  private 406 (8 complete/partial healthy/mixed/boundary/overflow/no-note-two-defect/unproducible
  goldens plus 5 malformed-schema cases) covers the table's rows; the two-defect no-note case being
  retained is the regression guard §E asked for.

## Limits

Read-only; no native jobs; no live, frozen, history or lock edits; no commits or pushes. Advice only —
not acceptance, not an owner-body review, and it grants nothing. Private 404 and 406, the 403 generator
rebuild, `initial-root-binding-owner-selection-v1` and `M/initial-root-binding-reconciliation` are
context and were not reviewed; I make no claim about the ten mapped files, the 581 unchanged files or
the native compile. Selection routes were determined from `design-lock.json` and the approvals
manifests it names; where I could not find a route I have said so rather than inferred one. Full
digests in `evidence/addendum-pins.json`.

Auditor: Claude Opus 5 (1M context).
