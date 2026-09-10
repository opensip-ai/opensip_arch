# v19 native coauthor — handoff

**Role.** Actual Claude, source **coauthor** with Codex. I am not the independent reviewer of these
changes. No grade is minted, no acceptance is claimed, and a fresh successor freeze, independent
source review and NEW blind review remain required. `technicalAssent.value` in `handoff.json` is
`true` and is an author's assent to his own exact bytes, nothing more.

**Custody.** The before-copy at `/tmp/opensip-design-corrections/v19-native-coauthor.v1/work`
verified 7864/7864 files, 544 831 302 bytes against manifest
`cd6e828c…c25a44` — 0 missing, 0 mismatched, 0 undeclared. It now holds 7865 files. A full
tree diff against the live repository shows exactly my six changed files plus one new artifact, and
one further path — `reviews/NEXT-REVIEW.md` — where **live has moved since the freeze**; the copy in
`work` is byte-identical to the frozen subject and I never wrote to `reviews/`. Six canonical checks
run at root after pin sealing; no pin in `work` was edited and **no pin match is claimed**.

---

## CB7-MUST-1 — closed, with one refinement to root's framing

The gap reproduces exactly as measured. `coverage_dialect_prerequisite` returns early unless the
universe dialect carries an `ownership` key — only Rust does — so a `clones` scope over
`package.json` under the TypeScript universe reached **no classification at all** and sealed a Run
with `coverage: complete`, `deficiency: null`, zero facts. `body_language_version` does refuse an
unlisted suffix, but only while a body is being derived, and a scope with no facts derives none.

**Root's preferred semantics is sound, and I can substantiate it rather than accept it.** The
alternative — treat an unlisted suffix like `BODY_LANGUAGE_OWNER_NOT_COMPILED` and leave `complete`
lawful — is right for Rust and wrong here, substantively. `OWNER_NOT_COMPILED` describes a path that
**is** a Rust source file which no selected target compiles: the universe examined a known-language
file and correctly produced no fact. A suffix outside the closed table is not a body of that universe
in any dialect, so `complete` asserts a negative from an absent capability — precisely what the syntax
universe's grammar law already refuses. Existing vocabulary suffices:
`language-tier-unsupported` / `capability-missing`. No new deficiency, `nativeCause` or
`DomainDetailCode`, and no schema enum changed.

**The refinement, which matters.** The law is **not** TypeScript-specific and must not be written as
if it were. The **syntax** universe's dialect form is *also* `closed-suffix-table`, so the correct
gate is the dialect **form**, not a universe id. For the syntax universe the new condition is
strictly implied by its own grammar registry — the published `data-document` classLaw states that no
data-grammar suffix appears in the syntax dialect table — so `syntax_capability_prerequisite` runs
**first** at closure and keeps its own refusal names, and the source-variant guard is the **backstop**
that makes the set of published universes total. All three universes then have a total scope
interpretation, and syntax's `onUnknown` remains defensive-only because its scope guard refuses before
a body is created. No compiler or grammar authority is invented anywhere.

**Both boundaries.** At retained Run closure, `coverage_source_variant_prerequisite` is
**unconditional** and depends on no caller passing anything (`COVERAGE_SOURCE_VARIANT_{UNSUPPORTED_SCOPE,
DEFICIENCY_MISMATCH,CAUSE_MISMATCH}`). At producer admission, `admit_coverage_result_v3` gains an
optional `universe_dialect` supplied by the caller holding the retained universe record — the
reference producer and `close_run` both do — refusing `native.coverage-source-variant-*` under
`PROVIDER.PROTOCOL_VIOLATION`. **Honest limit:** that boundary judges one record and never sees the
snapshot, so it applies the law only where the scope carries its own paths, and a caller supplying no
dialect gets today's behaviour there. The fact boundary was already total and is not duplicated.

Gated on `bodyIdentityJoin` (today, `clones` alone), so nothing claims a suffix table decides symbol
capability. `clones` is `source-path`, so **all** subjects must have a registered variant: a mixed
`src/a.ts` + `package.json` scope discloses instead of hiding, and an empty subject list is
unsupported rather than vacuously complete. `INVENTORY_CAPABILITIES` stay ungated on every inventoried
path. The classification is derived from the owning universe record and the scope's subjects — a
control feeds the identical payload and scope under a dialect that *does* register the suffix and
shows it then admits.

Measured: `package.json` goes `complete` → `unknown / language-tier-unsupported / capability-missing`;
`a.py` likewise; `a.ts`, `a.d.ts`, `a.tsx` with **no clone body** stay `complete`; Rust and syntax
unchanged. Projection: `run_termination` now yields indeterminate exit 3 with the typed detail, where
before the same request projected a silent exit 0.

**One existing control legitimately moved.** `injected-false-complete-for-a-markdown-scoped-clone-refuses`
now dies at the producer boundary naming the source variant instead of at closure naming
`SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE`, because `.md` is in no dialect table. The claim still dies and
the entry content is identical; only the diagnostic name changed. I did not weaken it: it asserts the
exact earlier refusal, a companion asserts *which* boundary refused, and two new controls prove the
grammar guard still solely owns the case the dialect table provably cannot see (`.tsx` in the table,
its grammar row dropped). **Disclosed risk:** a reviewer may prefer the more specific syntax refusal
to survive at the producer boundary. I judged that the earliest boundary able to see a provider's
false claim should refuse it. If root or the reviewer disagrees, conditioning the producer hook so it
makes no claim for a universe owned by a more specific law is a small contained change and I do not
object.

## CB7-SHOULD-2 — closed

All three arrays are reachable by ordinary valid selections every earlier bound admits.
`nativeContextDigests` (128) carries one member per **distinct** admitted context and units collapse
only on identical closure/stdlib/options, while `workspaceRoots` admits 1024 and a narrow capability
selection keeps `requestedCapabilities` far under its own 1024 — so 129 such units pass every earlier
gate. `importIds` (256) is selected by `evidence.importIds`, which admits 1024. `semanticClosures`
(128) is reached by 128 admitted policy packs that need not share closures. The only prior outcome was
a generic `maxItems` error naming no field, count, limit or route.

`admit_plan_selection_cardinality` is a **pre-Plan** boundary on the prospective Plan, raising the
existing field-generic `ScopeRefusal`: `PROJECT.SCOPE_LIMIT`, subject `field:count>limit`,
request-rejected exit 2 `REQUEST.UNSATISFIABLE`, and a **field-specific** narrowing remedy. No bound
widened, nothing truncated, no analysis silently reduced. It is wired into the **real** construction
path in both reference producers immediately before `add('plan', …)` — `add` builds the identical
value, so no Plan identity moves — and inside `plan_native_context_digests`, where that field's
deduplicated count first exists. Controls drive `build()` itself, so an oversized selection provably
mints no Plan and no Run.

Deliberately **not** added to retained closure: a retained Plan over its bound is a corrupt record and
keeps its schema-first refusal and origin-dependent routing; two controls assert it still refuses and
that the refusal is **not** a `ScopeRefusal`. Only an actual array over bound refuses — missing, null,
booleans, numbers, strings, objects, nested lists, wrong-typed members and a non-object Plan all reach
the schema untouched, and a 300-character string is never reported as 300 members. Multi-overflow
order is the published `$defs/plan` declaration order, drift-checked against the document.

Adjacent bounds audited: `policyPackIds` 128 = `policy.packIds` 128; `analysis.capabilities` 128 is
the *smaller* selecting field; `discovery.workspaceRoots` 1024 = `scope-descriptor.workspaceRoots`
1024, already accounted; `waiverIds` projects to a digest. `analysis-spec.parameters` 128 was checked
and is **not** an unaccounted selection — it carries one row per schema kind, not one per import.
Recorded as an observation; no resource-policy redesign.

## Advisories

**ADV-1, ADV-2, ADV-3, ADV-5 — accounted, no source change, limits preserved.** ADV-1's successor adds
exactly one fault cause (`host-invariant` → `SYSTEM.OUTCOME.ILLEGAL_STATE`) with class/exit and
`reasonCodes` unchanged; the artifact obligation is implementation plus root's application record.
ADV-2's 93-unit arithmetic is stated in the very S14 paragraph I widened and the limit is untouched;
its resolution is a product decision. ADV-3's 8-member encoding domain against 4 selected platforms is
disclosed with its reason and read as a support claim by no surface; implementation must not widen
support by widening encoding. ADV-5's UCD 15.0.0 pin and byte-exact fold are unchanged, and I
explicitly preserve rather than convert the blind's limitation: the ASCII vector set shows agreement
**on ASCII only** and establishes nothing about U+0130, Final_Sigma or U+00DF.

**ADV-4 — closed.** Existing normative inputs did **not** determine the 34 rows: S9.2 published the
phases, the frame table and three sentences, but not the rows, guards, wildcard vocabulary, terminal
law, or — decisively — the stage-dependent `ANALYZING_OR_READY_COMPLETE` transition, without which a
multi-stage exchange cannot be interpreted at all. `native/protocol3-transitions.v1.json` is
**generated from the exact existing rows**, and the model now **reads** it (the same idiom this file
already uses for `LADDERS`), so there is one authority and no transcription. The four existing
protocol traces run off it and pass unchanged. Prose-owned logic is listed explicitly: frame payloads,
the identity token set, the terminal→D9/exit mapping, custody obligations, and the stage count itself.

**I corrected myself here.** My first artifact text and control claimed the declared **order** is
load-bearing. That is false of this table: the rows are pairwise disjoint on (phase, frame, guard), a
reversed table reproduces the trace, and the competing rows are separated by mutually exclusive
guards. The artifact and controls now assert the true, stronger property, plus a control proving the
disjointness check would catch an overlapping row.

## CB7-SHOULD-1 — initial disposition only, source untouched

I did not read or interfere with the active clarification directory, changed no per-requirement
vocabulary, and invented no codes. I lean to root's reading, supported by shipped bytes rather than
argument alone: `workflows_model.v1.py` already emits, per unsatisfied requirement,
`{'code': 'REPAIR.EVIDENCE_RUN_UNAVAILABLE', 'remedy': 'evidence requirement unsatisfied:
<relation>@<minResolution> (<plane>: <deficiency>)'}`. S6 mandates remedy **distinctness**, not code
equality, and since `unmetPreconditions` is in the `repairPlanId` preimage that distinction is
identity-bearing — the property the blind's own `whyShouldNotMust` turns on. What would change my
mind: if the reviewer maintains a consumer is entitled to **branch on the code**, a shared code
under-determines a machine consumer even with differing remedies, and the fix is a statement of which
field is the machine-readable carrier — neither 11 codes nor silence. A one-sentence S6 mapping is
drafted in `handoff.json` and is **not** proposed, **not** written to source, and must not be
auto-accepted.

## Results, failures, limitations

`check-identity` 1346→**1431 / 0 failed** (+85 controls); `check-integration` **392/0** unchanged;
`check-foundation` **231/231**; `check-array-orders` **65/65**; `check-product-configuration`
**28/0**; `check-product-quality` **24/0**; `check_native_evidence.v2` **355/355** and
`check-security-lifecycle.v1` **456/456** — the last two only in a **disposable repinned copy outside
`work`**, because they refuse before running when pins differ. No pin in `work` was edited.

Four failures I hit and fixed are recorded in `handoff.json`, including two that were my own errors:
a prose replacement that silently did nothing because my assertion covered only the sentence prefix,
and the false order-dependence claim above.

Limitations: everything is a reference-model admission boundary over synthetic trusted observations —
no compiler, grammar, provider, OS or filesystem is executed or qualified, and nothing here is
evidence of host enforcement. The producer-side source-variant guard is total only for callers
supplying the dialect and only for `source-path` subject kinds. The symbol branch is unreachable today
and is stated as parity, not a live guard. `coverage_result` remains **duplicated** between
`integration-fixtures.py` and `check-identity.py`; I mirrored it and *proved* the mirror by asserting
the patched copies are byte-equal, but unifying them would move unrelated fixture identities and
deserves its own scoped change.

**Root owns:** a pin row for the new artifact, its addition to the next blind kit selector, and the
resealing of all five ledgers (`V19-ROOT-1/2/3`).
