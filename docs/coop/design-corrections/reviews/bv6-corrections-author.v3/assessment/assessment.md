# bv6-corrections-author.v3 — initial assessment (pre-correction)

Assessment of the five remaining root items against the **actual final v2 bytes**,
written before any v3 edit. No assent, no integration, no readiness.

**Custody.** `work/` verified byte-exact against
`root-input/final-v2-source-inventory.json` — 6839 declared, 0 missing, 0
mismatched, 0 undeclared. Frozen manifest recomputed `ca5f36d4…44042ee9`. Final v2
differs from frozen v16 in 17 files. All four final-v2 root probes read with source
and results, and `final-v2-public-note.md` read in full — including the 22:54 and
22:57 UTC sections I had **not** seen at my v2 read.

**I agree with all five.** Three are MUST and all three are real defects in bytes I
authored; the two SHOULD items include several false claims in my v2 handoff. I
have no disagreement to record on any of the five.

---

## BV6-V3-RECEIPT (SHOULD, parent CX-BV6-04)

**Two distinct errors of mine, both confirmed.**

1. `MutationReceiptV1` requires **`idempotencyKey`** as well as `operation`. My v2
   law bound the operation and then said the other three step kinds "mint no
   `H("workflow.mutation-intent")` key", leaving a **required field
   underdetermined** for `import` and `native-preparation`. Supplying the operation
   and alluding to "their own idempotency law" is not a law.
2. §10 lists **two** `receipt2:` domains — `workflow.mutation-receipt` **and**
   `workflow.verification-link`. My "exactly one receipt domain" is false.

**What I will publish.** The owning domain for these result branches is
`workflow.mutation-receipt` (named as the *mutation* receipt domain, not as the
only one). For the key, the exact existing owner already fits and I will cite it
rather than invent a domain: `MutationReplayScopeV1` is
`{schemaVersion, requestId, stepId, projectId, operation}`, and its `operation`
domain **already admits** `import` and `native-preparation` — they are two of the
23 tokens. So the deterministic preimage is the existing
`H("workflow.mutation-intent", scope)` over immutable admitted request/step inputs,
and this is a further reason the 23-token domain must stay wider than the current
emitters.

**Sharing a key recipe is not sharing replay authority**, and I will state the
lookup/delivery meaning per step kind: `mutation` — delivery replay with no second
effect; `repair-apply` — its existing content-derived key; `import` —
delivery-only within the same retained invocation, with custody, correspondence
and staleness joins re-checked and never a cross-request dedupe;
`native-preparation` — **not replay at all**: the key identifies that attempt's
receipt, a fresh preparation is a **new authorized execution** under a fresh grant
set, and no completed receipt ever suppresses one. This also corrects my v2
sentence that those steps mint no such key.

## BV6-V3-IMPORT-BINDING (MUST, parent CX-BV6-03)

**Agreed; this is the most substantive of the five.** `RepairPlanDescriptor.targets`
are `Fingerprint` = `finding-key2:<64hex>`. `RuntimeSubject` keys on
`{path, symbol?}` and `HistorySubject` on `{path}`. My producer read observability
and presence maps **keyed directly by the target string**, and my prose called the
targets the payload subjects. That silently equates a finding-key identity with a
LogicalPath and skips a real join.

**The join exists in retained records and I will publish it.** A `finding-key2`
identity is the H identity of the retained `finding-fingerprint` descriptor, whose
retention is `preimage`, so its bytes are retained and re-hashable at closure. That
descriptor carries
`subjectKey = {language, kind, logicalPath, qualifiedName, discriminator}`. The
deterministic projection is therefore: target fingerprint → the evidence Run's
retained finding carrying it (`repair_preview` already requires every target to be
in that Run) → its `finding-fingerprint` descriptor → `subjectKey`. Runtime matches
on `logicalPath` and, where the payload row carries `symbol`, on `qualifiedName`;
history has no symbol field, so a symbol-granularity target projects to its **file**
and that widening is **disclosed** rather than hidden. **Ambiguity refuses** — more
than one matching payload subject is not a deterministic projection and must not be
silently resolved — and unmatched targets are unsupported, not satisfied.

I will publish the projection law *and* implement it as a reference projection
joined to the caller, so the helper consumes an explicitly already-admitted
projection rather than pretending fingerprints are paths.

**The window demand has no wire field, and I claimed one.** `RecipeRef` carries only
`contributionId`, `recipeId`, `recipeVersion`, `closureId`. I will state the actual
owner: the demand is a property of the **admitted recipe closure** named by
`recipe.closureId` — content-addressed, admitted under current trust, and revoked
trust already invalidates apply — projected by the host into the typed input the
reference consumes. No field is claimed that does not exist.

## BV6-V3-IMPORT-CAUSE (MUST, parent CX-BV6-03)

**Agreed; root's probe proves it.** `admit_evidence_requirement` admits
`runtime-observation` with `history-range-insufficient` and `history-change` with
`subject-not-observable`, although the published `perKindApplicability` excludes
both. The producer checks per-kind applicability; the consumer checks only the
broad imported plane. The consumer will check the **per-kind** law, keeping typed
presence and `CONFIG.INVALID` routing, and both lawful kind/cause pairs must keep
admitting.

## BV6-V3-IMPORT-SEMANTICS (MUST, parent CX-BV6-03)

**Three separate defects, all agreed.**

1. My law says `partial-acceptable` needs at least one supported target, but the
   producer vetoes on **any** unobservable runtime target or **any** uncovered
   history target *before* the ANY test — so root's partial fixtures with one
   supported and one such target refuse. I will make the support test depend on
   `completeness` and let the not-observable / not-covered condition only **name the
   cause more precisely when the support test fails**, so valid partial cases
   survive and `complete` still requires every target.
2. `required=None` and `required=0` currently become optional success while the text
   claims unknown declarations are required. I will **enforce the typed boundary**:
   `required` must be an actual `bool`, matching the discipline I applied to
   `satisfied` under CX-BV6-02, and I will **remove the contradictory "unknown"
   claim** — at this boundary there is no unknown state, only a typed input from the
   owning declaration projection.
3. My v2 text said the existing `completeness` enum "already means exactly this".
   That is a historical overclaim: the enum exists, but the **imported ALL/ANY
   target interpretation is being selected now**. I will mark it as a selected
   clarification with its provenance, and relate the optional projection explicitly
   to the owning recipe/rule declaration rather than equating it with policy
   predicate truth.

## BV6-V3-PRECISION (SHOULD, parents CX-BV6-07/08)

All agreed; every item is a claim of mine to correct.

* **"Not decidable by this schema because relation is not an enum" is false.** JSON
  Schema can branch on a property's `const`/`enum` even when the base type is a
  broader string. The accurate statement is that this schema **deliberately leaves
  the authoritative registry lookup to admission** and cannot itself fetch registry
  rows. I will remove the false rationale and keep the deliberate choice.
* **`D9Deficiency`:** its **enum** is preserved; its definition bytes changed when I
  added a description. The v2 handoff must say enum, not definition bytes.
* **The v2 "FULL RETAINED-RUN" claim is false for the `repair_preview` cases** —
  those are synthetic workflow helper calls. Only the CX-BV6-01 partition controls
  reach an actual `close_run` closure, and even that is distinct from ledger or
  evaluator execution.
* **The four renames are 3 generic + 1 dedicated native-preparation**, not 4 generic
  rows.
* **v2 wrote outside its output directory** — `/tmp/hb.log`, `/tmp/hd.py`,
  `/tmp/delta-table.md` — so the all-writes-inside claim is repeated in error and is
  corrected. In v3 every script, log and temp file is under the v3 root.
* **The v2 public note was read once at 22:51 UTC**; the 22:54 and 22:57 additions
  arrived during or after my handoff and were not substantively covered. I will not
  claim every note point was agreed at v2.

---

**Preserved and not re-opened:** the CX-BV6-01 partition law and its controls; the
plane split and its disjoint vocabularies; supported runtime and history relations;
symbol-versus-file granularity; native safety and recipe authority; all 23 generic
operation tokens and the dedicated `repair-apply` exclusion; no D9 widening; and all
original severities. The new laws are recorded as **selected design clarifications**,
not as historical facts I failed to find.
