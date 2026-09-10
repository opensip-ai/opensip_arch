# bv5-corrections-author.v2 — substantive assessment of the root feedback

**Timing, stated accurately.** The prompt asked for this assessment *before* edits. It was not
written before edits: I read the three root inputs, reproduced the root full-Run probe, and began
correcting, and I am writing this after those corrections were made and measured. The
`CODEX-PUBLIC-NOTE.md` in this directory records the same observation and asks me to record the
actual timing rather than claim it preceded the edits. I am recording it. Nothing below is
back-dated; every judgement here is the one the corrected bytes implement.

**Standing.** Coauthor assessment. Not independent review, not blind acceptance, not readiness, not
product qualification.

---

## The eight initial root points

| # | Root point | My assessment | Disposition |
|---|---|---|---|
| 1 | `fold` is not simple lowercase | **Agree, fully.** Measured on UCD 15.0.0: `U+0130` → `U+0069 U+0307`; `ΟΣ` → `ος` but `ΣΟ` → `σο`; `ß` unchanged where casefold gives `ss`. My v1 wording was wrong in a way that would change an admission outcome. | CORRECTED, and the binding made **effective** |
| 2 | Schema stage and origin routing overstated | **Agree.** Step 1 refuses only an actual over-bound array, so missing/null/boolean/number/string/object all reach schema; and §10 routes a host-generated invalid spec to `operational-failed` (4), which my "both routes are request-rejected / exit2" flattened. | CORRECTED in prose **and** docstring |
| 3 | Repair guard narrowed; dynamicDispatch veto | **Agree.** `UNSAFE_ACTIONS = {delete, replace}` unqualified; my "replace of an exported subject" narrowed a live guard. And §4.5 `affected_targets` makes dynamic-edge effects target-relative. | CORRECTED |
| 4 | Contradictory not-applicable coverage closes a Run | **Agree, and reproduced.** | CORRECTED **in the admission**, both boundaries |
| 5 | Fingerprint path enforcement invents a join | **Agree.** Only anchors join the inventory; `finding-fingerprint.subjectKey.logicalPath` is checked by `identity-model.ordered`, which enforces no per-segment 255 bound. | CORRECTED |
| 6 | Windows citation wrong | **Agree.** The owning selection is security S8 + the native matrix. | CORRECTED |
| 7 | "One observation" exceeds the evidence | **Agree.** `complete` and `not-attempted` necessarily differ in `attempted` too; it is a determinacy gap, not a digest collision. | CORRECTED |
| 8 | Cross-relation pair closes a Run; my cross-rung probe was too weak | **Agree on both halves.** My `unresolved-edge@resolved-binding` probe only exercised the resolved-rung NA refusal and could not establish relation-specific membership. | CORRECTED at four sites |

### Where I disagreed with nothing, and where I qualified

I found no root point where the evidence supports disagreement. Two qualifications, both recorded
in the source rather than only here:

* **Point 1 has a cost I will not hide.** Making the version binding effective means this reference
  derivation now *refuses to run* where the declared Unicode case data is absent. That is a real
  portability restriction. I judged it correct anyway, because the alternative — a declared version
  that nothing consults, beside a `.lower()` that silently uses whatever the runtime ships — is a
  determinism claim with no mechanism behind it. The refusal is a `ReferenceEnvironmentError`,
  deliberately **not** an `AdmissionError`, so it can never be mistaken for a refusal about a
  caller's `lib` selection.
* **Point 4/8's fix moves reference Run identities**, and I traced that rather than asserting it was
  harmless (see below).

---

## The two additional findings in `CODEX-PUBLIC-NOTE.md`

* **CX-BV5-09 (SHOULD).** Agree and reproduced: the `complete` branch checked the zero count but not
  the class list, so `complete` + count 0 + `["computed-member-access"]` closed a Run. Corrected,
  with the analogous `not-attempted` law. I did **not** touch `incomplete`/`partial`: both already
  require exact count *and* class equality, and both are honest observations that legitimately carry
  classes. Nothing here converts an honest partial observation into a completeness claim, and
  `stageTerminal`/`examinedExhaustive` remain independent.
* **CX-BV5-08 completion (retained scopes with no Coverage wrapper).** Agree and reproduced: my
  constructor guard could not see retained bytes that never went through the constructor, and a
  scope with no Coverage reaches no other membership check. Corrected at retained closure, over
  `view.scopeIds`, independent of whether a Coverage wrapper or a fact exists. This adds no
  requirement that every scope must have Coverage — the valid `unresolved-edge@observed` scope with
  no wrapper still closes.

---

## My own v1 new findings, individually

* **BV5A-NEW-1** — I had left it open as "a behaviour change outside minimal scope". Root's full-Run
  counterexample makes that scoping wrong: a contradictory Coverage entry closing a sealed Run is
  not an advisory. **Fixed**, at the producer boundary, at retained closure, at scope construction
  and over retained scopes.
* **BV5A-NEW-2** — Addressed proportionately, as root directed, and I accept the distinction: a
  workflow helper that consumes an already-admitted native record is **not** thereby a product host
  failure, so I did not add a re-validation call on that basis. What *was* a genuine contradiction
  is that the reference fixture carried a six-member record while the normative record is closed at
  seven; a limitation note would have hidden it. Both fixture records now carry `dynamicDispatch`,
  and the helper docstring states the admitted-input assumption explicitly.
* **BV5A-NEW-3** — Corroboration only, and root is right that it substantiates the *mapping* and
  says nothing about simple-versus-full conversion. Restated with that limit.

---

## The one thing I want a reviewer to look at hardest

The reference **Run identities moved**: the shared fixture's baseline goes
`4e83d795…` (frozen v15) → `e7abd2f4…` (released v1) → `ca67ad74…` (this turn). I did not want to
assert that this was benign, so I attributed it by experiment: taking the final v2 tree and
reverting **only** `native-evidence.schemas.v2.json` to its v1 bytes restores the v1 baseline
exactly (`e7abd2f4…`, and `c3117646…` for the no-match graph) while every behavioural edit stays in
place. So the movement is entirely the digest law working as designed — a Coverage
`payloadSchemaDigest` is the raw SHA-256 of that schema document's bytes, so any edit to it, even a
description, moves every `coverage2` and therefore the Run — and **none** of it comes from the
admission or closure changes. Evidence: `evidence/run-identity-attribution.json`,
`disposable/identity-attribution.v1/`.

---

## What I did not do

* No change to `incomplete`/`partial` semantics, to the five resolved rungs, to RC-2's preconditions,
  to `stageTerminal`/`examinedExhaustive` independence, or to any registered pair — all 17 still
  admit, swept through the producer boundary.
* No ASCII narrowing of `libSelection`, no locale parameter, no casefold substitution.
* No published pin, generated report, readiness record or crosswalk touched in `work/`. Every repin
  and checker run is in a named disposable copy.
