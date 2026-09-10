# bv6-corrections-author.v3 — correction coauthor handoff

**Role.** Correction **coauthor** working with Codex. Not an independent reviewer,
not an accepting reviewer. No product implementation, agents, subagents, commit,
push or publication. **Every** v3 script, log, probe, report and temporary file is
under `/tmp/opensip-design-corrections/bv6-corrections-author.v3` — nothing was
written to bare `/tmp` this turn.

**Technical assent: TRUE** to the exact bytes in §3 as a correct, minimal and
mutually consistent disposition of the five remaining root items and every point in
the v3 `CODEX-PUBLIC-NOTE.md`, on top of the earlier corrections, which are
preserved. It asserts **no agreement by root**, no independence, no acceptance and
no readiness.

---

## 1. Custody

`work/` verified byte-exact against `root-input/final-v2-source-inventory.json`
before any edit — 6839 declared, 0 missing, 0 mismatched, 0 undeclared. Frozen
manifest recomputed `ca5f36d4…44042ee9`. After all edits: 0 missing, 0 undeclared,
**12 changed this turn**, **17 aggregate vs frozen v16**, and **0** generated
reports, pins, readiness records or review files touched.

`root-input/final-v2-public-note.md` was read **in full before any edit**,
including the 22:54 and 22:57 UTC sections I had not seen at my v2 read. A further
`CODEX-PUBLIC-NOTE.md` appeared in the v3 root and was read before this handoff; it
added eleven more precision items, all dispositioned in §2b.

---

## 2. The five root items — all agreed, all corrected

### BV6-V3-RECEIPT (SHOULD) — the required receipt was still underdetermined

Two errors of mine. `MutationReceiptV1` requires **`idempotencyKey`** as well as
`operation`, and my v2 law bound only the operation while saying the non-generic
step kinds mint no key at all. And §10 lists **two** `receipt2:` domains, so
"exactly one receipt domain" was false.

Published: `workflow.mutation-receipt` as the owning **mutation** receipt domain,
and `receiptIdempotencyKeyByStepKind` giving the exact recipe, preimage, binding and
**lookup meaning** for all four step kinds. No new H domain was invented — the
existing owner fits, because `MutationReplayScopeV1.operation` **already admits**
`import` and `native-preparation` as two of the 23 tokens. That is a further reason
the generic domain must stay wider than today's emitters.

Sharing a recipe is **not** sharing replay authority, and the meanings are stated
separately: `import` is **delivery only** within the same retained invocation, never
a cross-request dedupe, with custody, mandatory correspondence and staleness
unchanged and re-checked; `native-preparation` is **not replay at all** — a fresh
preparation is a new explicit authorized execution under its own grant set, with no
automatic retry, and no completed receipt ever suppresses one.

### BV6-V3-IMPORT-BINDING (MUST) — fingerprints are not paths

`targets` are `finding-key2:` fingerprints; `RuntimeSubject` keys on
`{path, symbol?}` and `HistorySubject` on `{path}`. My producer read the payload
maps **directly by the target string**. The join exists in retained records and is
now published and implemented: target → the evidence Run's finding → the retained
`finding-fingerprint` descriptor (retention `preimage`, re-hashed at closure) →
`subjectKey`. Runtime matches on `logicalPath` and, where the row carries `symbol`,
on `qualifiedName`; **ambiguity refuses**; an unmatched target is unsupported.

After the v3 note the granularity handling was made explicit rather than assumed:
`subjectKey.kind` has **no closed vocabulary**, so the projection does not classify
the *target* — it reports the granularity of the **answer**. A path-only runtime row
is a **file-level** answer to a keyed subject and is flagged, so it never silently
passes as symbol-level; history, having no symbol field at all, is always file-level
and says so.

The window demand has **no wire field** and I claimed one. It is owned by the
**admitted recipe closure** named by `recipe.closureId`, projected into a typed
input.

### BV6-V3-IMPORT-CAUSE (MUST) — consumer checked the plane, not the kind

Root's probe proves `admit_evidence_requirement` admitted a history cause on a
runtime relation and the reverse. The consumer now decides the **per-kind** law from
the published `perKindApplicability`, with typed presence and `CONFIG.INVALID`
routing unchanged, and both lawful pairs still admit.

### BV6-V3-IMPORT-SEMANTICS (MUST) — three defects

**Partial:** the support test now depends on `completeness`, and the
not-observable / not-covered condition only names the cause **when that test fails**
— so root's partial fixtures with one supported target now satisfy, while `complete`
still names the specific cause. **Bounds** (window, revision range) are a property of
the observation, not of the target count, and apply in both modes; that is stated.
**Typed `required`:** `None`, `0`, `1` and `"yes"` now all refuse; the contradictory
"unknown declarations are required" claim is **withdrawn**, since there is no unknown
state at a typed boundary. **Provenance:** the `completeness` enum existed, but the
imported ALL/ANY reading is **selected here** and is recorded as such, and the
optional projection is related to the owning `evidenceUse` declaration rather than
equated with policy predicate truth.

### BV6-V3-PRECISION (SHOULD) — six claims of mine

The "because relation is not an enum" rationale is **false** and is removed — a
schema *can* branch on `const`/`enum` under a broader string type; the accurate
statement is a deliberate choice to leave registry lookup to admission.
`D9Deficiency`'s **enum** is preserved; its definition bytes changed when I added a
description. The v2 **FULL RETAINED-RUN** claim for the `repair_preview` cases is
**false** — those are synthetic helper calls. The four renames are **3 generic + 1
dedicated**. v2 wrote `/tmp/hb.log`, `/tmp/hd.py` and `/tmp/delta-table.md` outside
its output. And the v2 note was read once at 22:51 UTC, so its later additions were
not covered by that handoff.

## 2b. The eleven v3 public-note follow-ups

All corrected: the UTF-16/code-point ordering rationale; both leftover partition
comments; the builtin-plus-substring ordering control **replaced** by a full Run
with two scopes overlapping on two competing subjects; the closed-world case note
gaining **BY ITSELF**; the HistoryPayload "only fields" claim; the
causes/disclosures carrier claim in all four places; the remaining prose-substring
controls replaced by structural ones; the duplicated control id; the **dangling
`byCommand` pointer** plus a scan for others and a new control that every such
pointer resolves; the `native-preparation` `boundTo` rationale; and the runtime
matching/coarsening treatment.

---

## 3. Changed source — 17 vs frozen v16, 12 this turn

Abbreviated to eight hex characters; untruncated values and per-file edit lists are
in `handoff.json#/changedSource/files`.

| Path | frozen16 | final v2 | v3 | this turn |
|---|---|---|---|---|
| `docs/coop/design-corrections/check-integration.py` | `df9fbb2e…` | `e07b29ae…` | `4422ec24…` | yes |
| `docs/coop/design-corrections/foundation/check-identity.py` | `2724276f…` | `00a6c146…` | `1982e2b6…` | yes |
| `docs/coop/design-corrections/foundation/identity-model.py` | `66d8bd5a…` | `64e38f01…` | `650d7942…` | yes |
| `docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json` | `ef0c244e…` | `53380a24…` | `53380a24…` | no |
| `docs/coop/design-corrections/native/native-cases.v2.json` | `5740aed5…` | `07d990e2…` | `07d990e2…` | no |
| `docs/coop/design-corrections/native/native-evidence.schemas.v2.json` | `2a5fc493…` | `800eee09…` | `19eeba46…` | yes |
| `docs/coop/design-corrections/native/native_evidence_model.v2.py` | `8301e8e3…` | `01b517d3…` | `01b517d3…` | no |
| `docs/coop/design-corrections/workflows/check_workflows.v1.py` | `0af791d5…` | `1ead9c63…` | `29abcb85…` | yes |
| `docs/coop/design-corrections/workflows/schemas/common.schema.json` | `3f84dff2…` | `98690131…` | `16ff6419…` | yes |
| `docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json` | `8acfd72f…` | `a70345dc…` | `e6c997aa…` | yes |
| `docs/coop/design-corrections/workflows/schemas/invocation-record.schema.json` | `3b89b739…` | `6c5ed3f3…` | `6c5ed3f3…` | no |
| `docs/coop/design-corrections/workflows/schemas/repair.schema.json` | `b8fe3464…` | `a6481f98…` | `c577eda9…` | yes |
| `docs/coop/design-corrections/workflows/workflow-cases.v1.json` | `688506e6…` | `5a3c6966…` | `22b74430…` | yes |
| `docs/coop/design-corrections/workflows/workflows_model.v1.py` | `8d45d115…` | `6831c211…` | `6fa97479…` | yes |
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | `64a2a019…` | `3d7ca24e…` | `3d7ca24e…` | no |
| `docs/v2/contracts/product-v1/native-evidence.md` | `b50c814c…` | `1ca71365…` | `fafc4abc…` | yes |
| `docs/v2/contracts/product-v1/workflows-and-surfaces.md` | `4a5f0c4e…` | `11d98406…` | `f7735807…` | yes |

---

## 4. Controls and commands

Run **once** after coherent final source, in the separately inventoried disposable
repinned copy `disposable/checker-run.v1`. `work/` was never repinned — its pins are
stale by design. `run-suites.sh` sets `pipefail` and is **not** the canonical six;
root runs those after final source, records and pins.

| Suite | Result | v2 → v3 |
|---|---|---|
| `check-foundation.py` | PASS 231/231 | 231 → 231 |
| `check-identity.py` | 1346 passed, 0 failed | 1344 → 1346 |
| `check-security-lifecycle.v1.py` | 456/456, 10 sweeps | 456 → 456 |
| `check_native_evidence.v2.py` | PASS 355/355 cases | 355 → 355 |
| `run-reference-checks.py` | pins valid, 1788/1788 | 1761 → 1788 |
| `check-integration.py` | 392 passed, `failed: []` | 378 → 392 |

Counts are check **rows**, not distinct named properties; several ids are
parameterised over a vocabulary.

**What these controls are.** Schema-level validation; helper-level calls over
synthetic already-admitted inputs; and **full retained-Run `close_run` closure for
the partition controls only**. The `repair_preview` cases are synthetic workflow
helper calls — the v2 FULL RETAINED-RUN claim is withdrawn — and even `close_run` is
distinct from ledger, evaluator or provider execution. **Host enforcement: none.**
No control in this delta proves a claim by matching prose, and none is
self-mirroring.

**Root probes re-run against v3.** Overlap and no-Coverage: unchanged and correct.
Requirement shapes: helper and schema agree on all five. The final-v2 **imported
probe cannot run unmodified** — it passes plain strings as targets and omits
`required`, which are exactly the two defects it exposed; its failure is retained,
and `probes/probe_v3_imported.py` answers all of its questions against the corrected
structure, matching on all 20 cases including its four cross-kind consumer cases,
its `None`/`0` cases and both partial fixtures.

**Preserved failures:** my first replacement ordering control (the overlapping set
had one member) and a workflows report with a stale projection field name.

---

## 5. Limitations

* Design reference evidence over synthetic trusted inputs; no product execution.
* The reference model emits a receipt only for `repair-apply`. Stated as a
  qualification limit and deliberately distinct from the design law, which is now
  complete for both required receipt fields.
* The imported projection and outcome are **pure reads** over already-admitted
  inputs with stated preconditions; they admit no payload, observation scope or
  polarity and validate no opaque Run.
* The imported repair path is exercised through `repair_preview` and direct producer
  calls, **not** through a `close_run` closure.
* Pins in the proposed copy are stale by design.
* **Final full exact-byte root review, a fresh independent Claude review, a NEW
  blind consumer and an application review all remain owed.** This is coauthor
  assent to exact bytes — not agreement, acceptance or readiness — and root does not
  assent.
