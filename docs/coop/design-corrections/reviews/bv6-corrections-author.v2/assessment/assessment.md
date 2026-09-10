# bv6-corrections-author.v2 — initial assessment (pre-correction)

Coauthor assessment of the eight root points against the **actual final v1 bytes**,
written before any v2 edit. No assent, no integration, no readiness claim.

**Custody.** `work/` verified byte-exact against
`root-input/final-v1-source-inventory.json` — 6839 declared, 0 missing, 0
mismatched, 0 undeclared. Frozen manifest SHA-256 recomputed as
`ca5f36d4…44042ee9`, matching. Final v1 differs from frozen v16 in exactly 14
files. All four root probes read with source and results. No
`CODEX-PUBLIC-NOTE.md` present at assessment time; re-checked before final handoff.

**Headline: I agree with all eight points.** Two are MUST and both are real
defects in bytes I authored. On CX-BV6-01 I withdraw my CB6-NEW-3 deferral
outright. I disagree with root only on *two implementation choices* inside
CX-BV6-01, both of which make the fix stricter or better attributed, not weaker.

---

## CX-BV6-01 (MUST) — overlapping scopes admit at retained Run closure

**Agree in full. My CB6-NEW-3 deferral was wrong and I withdraw it.**

Root's v3 probe case `overlap` ADMITs at `close_run`
(`run2:5d333c16…`) while frozen identity §3 already requires non-overlap. I
re-read `close_run`: the per-view scope loop checks `SCOPE_SOURCE_JOIN`,
`UNSELECTED_ENUMERATOR` and `ENUMERATOR_CLOSURE_KIND`, and nothing compares two
scopes to each other.

**Why the deferral was wrong.** This is an admitted violation of *existing
published law*, not a new product feature, and it is decidable from retained bytes
at the authoritative boundary. Worse, my v1 §3 reconciliation made the text *more*
specific about a property the closure does not decide — so deferring left the
contract asserting more than before while enforcing the same nothing. Root is
right to reject it.

**Assessment of the root proposal, boundary by boundary** — read as a reference,
not authority:

| Choice | My assessment |
|---|---|
| Grouping `(snapshotId, relation, resolution, sourceUniverse, targetUniverse)` | **Accept.** Equals the registry's `file@enumerated` `matchOn` and equals the tuple I published in §3, so the enforced key and the stated key become one object. |
| Per-view isolation | **Accept.** Rebuilt per view, so cross-view reuse of one scope stays lawful — required, since two views of one Run legitimately share a scope. |
| Applies to scopes without Coverage | **Accept, and important.** Iterating `view['scopeIds']` reaches scopes that have no Coverage entry and therefore reach no other membership check — exactly the case a single-Coverage producer cannot see. |
| Single-producer limit | **Accept.** `admit_coverage_result_v3` sees one scope and cannot decide a between-scopes property. Retained Run closure is the only correct boundary, and no host effect or protocol call is added. |
| **Placement before `SCOPE_SOURCE_JOIN`** | **Do not adopt as proposed.** I run the per-scope well-formedness checks for every scope *first*, then compute the partition, so a foreign-snapshot or unselected-enumerator scope refuses as **itself**. This follows the discipline the codebase already states for the anchor law. |
| **Tuple hardcoded in `identity-model`** | **Do not adopt as proposed.** I publish it as `coveragePartitionLaw` in the relation registry beside `coverageTotalityLaw` and have `identity-model` **read** it — matching how `coverageTotality` and the ladder are already handled, so the enforced key cannot drift from the published one. |
| Refusal name | Extend with the offending `relation@rung` and subject, matching `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH`. Internal `AdmissionError` only — no public detail code, no D9 change. |

Planned controls: full-Run disjoint ADMIT; full-Run overlap REFUSE with the exact
cause; different-relation same-subject ADMIT; the same tuple across two **views**
ADMIT; a scope with **no Coverage** still partitioned; and lawful partial/unknown
coverage unaffected.

## CX-BV6-02 (SHOULD) — helper admits what its own schema refuses

**Agree; reproduced exactly.** `admit_evidence_requirement` admits
`{satisfied: true, deficiency: null}` and `{satisfied: 1}`, both of which the
owning schema refuses. The cause is mine: `req.get('deficiency')` conflates an
explicit null with absence, and `if req['satisfied']` is a truthiness test.

Fix: distinguish presence (`'deficiency' in req`) from value so an explicit null
refuses in **both** branches exactly as the schema does; require an actual `bool`
so `1` refuses; and route shape violations to **`CONFIG.INVALID`**, matching
`validate_import_record` and `admit_atom`, instead of
`REQUEST.PRECONDITION_FAILED`, which is for a well-formed request whose
preconditions are unmet. No new public detail code.

The checker comment claiming the boundary holds "even when a host skips schema
validation" is replaced with the accurate statement: the boundary re-decides the
same law over its own typed preconditions and is held **equal** to the schema on
an enumerated shape table. Root is right that the five-case comparison is not a
whole-product exploit claim — `repair_preview` is reached through a request the
host validates; what is wrong is that two boundaries claiming to decide one law
disagreed.

## CX-BV6-03 (MUST) — imported-evidence requirement ownership is missing

**Agree; my v1 answer was off-target.** `repair_preview` admits requirements over
`runtime-observation` and `history-change` through `admit_atom` (13 native + 2
imported relations), but `sufficiency_v2` ranges only over the native view and
returns `required-relation-missing` for both. My v1 text calling `sufficiency_v2`
"the only defined producer" is false for those two relations.

**Why I missed it.** My `importSemanticsPreserved` paragraph answered about
`evidenceOrigin: imported-prepared-*` — native Runs whose *facts* came from an
imported prepared expansion. That is the **native** plane.
`runtime-observation` and `history-change` are the **imported-evidence** plane:
they mint no `fact2`, carry no `sourceUniverse`/`targetUniverse`, and are
deliberately outside the native registry. Root is right that these are distinct,
and right that the helper contrast proves different domains rather than that two
functions must agree.

Plan: publish an owning imported-requirement outcome law in
`imported-evidence.schema.json`; add a **distinct** vocabulary whose members are
each grounded in an already-published import condition (evidence-kind
availability, required-vs-optional `evidenceUse`, unmapped-only staleness,
observation window/population, `unobservable`/`unmapped` observability) rather
than invented; make `EvidenceRequirement.deficiency` a plane-tagged union with the
plane decided **at admission** by relation-registry membership, which is where the
two planes are already separated.

**Safety invariant to preserve and control, not assume:** an imported requirement
can never by itself support a universal negative or an unsafe delete/replace. One
window never establishes universal non-use, `observable-unhit` is not unused, and
the closed-world gate stays native and separate. Not doing: removing a supported
imported relation, widening D9, adding a rung, or inferring universal non-use from
cold observations.

## CX-BV6-04 (SHOULD) — command names conflated with operation tokens

**Agree; the count is worse than I published.** `genericMutationClasses` holds 20
**command names** while my `invocation-record` annotation calls it the exact
admissible operation set. Property-schema admits 23 **operation tokens** (24 minus
`repair-apply`). Three listed names refuse; six admitted tokens are absent. My own
checker validated operations looked up *through* `byCommand`, so the control
passed while the published list and the annotation were wrong.

**On `analyze`:** `ImportParams` and `NativePreparationParams` carry **no**
operation field, and the only model emitter of `MutationReceiptV1.operation` sets
`repair-apply`. So no import step — in `import` *or* `analyze` — is shown to emit a
`MutationOperation` anywhere in this kit. The checker's `analyze` exception
therefore disappears: the real rule is that only `mutation` steps and the
dedicated `repair-apply` step carry an operation here, which makes totality
*derivable* instead of patched.

**This widens my own CB6-NEW-2** from one orphan operation to **three**:
`config-write`, `import` and `native-preparation` have no published emitter in
this kit. My v1 "receipt-only" claim for the latter two was an inference with no
citation, exactly as root says.

Fix: separate three published things — `byCommandGenericMutationStep`,
`dedicatedStepOperations` (`repair-apply`, with its citation), and
`admissibleGenericFieldDomain` (the actual 23-token schema domain, explicitly
**not** narrowed to current emitters); disclose the three orphans; drop injectivity
as a law and keep it only as an observation over the current rows, since multiple
commands could emit one operation.

## CX-BV6-05 (SHOULD) — "every row" contradicts compiler-free syntax-only

**Agree.** `discover_units(markers={})` returns no units, yet syntax-only is a
supported compiler-free path over exactly such a repository;
`assign_membership` classifies those files `syntax-only`/`grammar-only` with
`unitOrdinal: null`. `unitKind: syntax-only` exists in `WorkspaceUnitV2` but
`discover_units` never mints one. I will scope the unit prerequisite to the rows
naming a **compilation** universe and state explicitly that `syntax-only` needs no
unit. The bare-JS clarification stands without the over-general claim.

## CX-BV6-06 (SHOULD) — the "closed total shape" wording

**Agree.** `sufficiency_v2` returns `causes` on **both** branches (empty on
success) and can return non-empty `disclosures` on the **failing** branch. I will
restate it as a **projection** law: the requirement record carries the
satisfaction/deficiency projection; `causes` and `disclosures` stay with the
producer and the retained Coverage and are not carried by this field. Per-requirement
cause, retained Coverage cause and public D9 detail stay distinct.

## CX-BV6-07 (SHOULD) — four precision items

1. **Remove** the unverified claim about what TypeScript itself recognizes. The
   internal rationale is sufficient.
2. **Correct** "refuses before the graph digest is used": the digest *is* computed
   and compared (line 2573) before `typescript_config_graph_faults` (line 2582).
   The accurate statement is that the universe is never **admitted** and no
   identity accepted.
3. **Correct** "the three cannot drift": model↔table cannot drift because the model
   reads the table; prose agreement is not established by assertion and is not
   claimed.
4. **Correct** the ADV-2 examples: imports are a separate plane and I will not
   invent a lawful imported native `ViewEntryV3` path. The defensive synthetic
   evaluator input and a non-conforming provider justify the wider domain. Root
   accepts the global native provider exact-confidence scope as defensible; that
   reading is retained.

## CX-BV6-08 (SHOULD) — evidence overclaims in my v1 handoff

**Agree; every listed item is mine.** The v1 handoff and all original reports stay
verbatim; corrections are recorded in the v2 handoff. Notably: v1 claimed every
write was inside the v1 output directory (false — `/tmp/cb6_*.py`, `/tmp/bl-*`,
`/tmp/w*`, `/tmp/i*`, `/tmp/id2-3.json`, `/tmp/probe-cw.json`,
`/tmp/cb6-delta*.json`); claimed `D9Deficiency` was byte-unchanged (false — only
its **enum** is; I added a description); overstated the `config-write` search
scope; called `byCommand` keyed both ways when it is not an inverse map; and said
"no filesystem was executed" when Python read, wrote and hashed throughout — what
was not performed is product execution or host durability qualification.
`run-six.sh` lacked `pipefail` and is not the canonical six. The disposable copy
excluded most of `reviews/` and reused report filenames, so not every intermediate
version is retained. I will also remove the prose-substring and wrapping controls
I added in v1 and replace them with structural and full-Run controls.

---

**Original severities preserved.** The four blind v6 required findings and three
advisories keep their own severities and ownership; the root points above are
root's. My CB6-NEW-1 and CB6-NEW-2 remain mine (NEW-2 widened to three orphans);
**CB6-NEW-3's deferral is withdrawn** and is corrected under CX-BV6-01.
