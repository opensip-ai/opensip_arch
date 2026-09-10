# bv4-corrections-author.v2 — pre-edit assessment of the seven CX-BV4 items

Written **before** any edit to `work/`. Inputs read in full this turn:
`root-input/current-codex-note.md` (12684 bytes, all 60 lines including the six
sections added after v1's single read), `root-input/codex-assessment.json`, and
all three diagnostic trees — `codex-totality-recheck.v1/attempt{1,2,3}/{probe.py,report.json}`,
`codex-request-recheck.v1/{probe.py,report.json}`,
`codex-derivation-recheck.v1/{probe.py,report.json}`.

`work/` verified byte-identical to the released v1 bytes (4379 files). v1 is not
touched.

**Position: I agree with all seven, none is contested.** Six are confirmed against
the v2 source below; the seventh is a factual record correction I accept in full.
Two of root's framings I want to sharpen rather than dispute, and one place where
I think the required correction should go slightly further than stated — both
noted per item.

---

## 1. CX-BV4-TOTALITY — confirmed, and the code says so plainly

`identity-model.py` `coverage_inventory_totality`, line 904:

```python
if fact['relation']!=scope['relation'] or fact['resolution']!=scope['resolution']:continue
```

Two coordinates, where the Coverage key `CoverageKeyV2` has five
(`relation`, `resolution`, `sourceUniverse`, `targetUniverse`,
`subjectScopeCommitment`). Attempt 3 is a real full-Run counterexample and I
reproduce root's reading exactly: the view's existing `FACT_SCOPE_JOIN`
(line 1393) is an **existential** — each fact must match *some* scope on all four
of relation/rung/both universes — so the TypeScript fact is lawfully in the view,
and my totality loop then counts it against the *syntax* scope's obligation.
`run2:92e44a4…` ADMITs; the two-own-facts control `run2:0d63a18…` ADMITs and is a
valid positive that must keep passing.

I accept root's attempt accounting: attempt 1 is a harness `StopIteration`,
attempt 2 is a *proper* `UNIVERSE_LANGUAGE_NOT_REQUESTED:syntax` refusal because
the syntax mode was not requested. Neither is a second defect, and I will not
report them as such.

**One place I go further than the stated correction.** Root asks for owning
snapshot + relation/rung + both universes. `snapshotId` is already forced
transitively — `close_run` requires every fact and every scope to carry the Run's
`snapshotId` — so adding it changes no outcome today. I will add it anyway and say
why: the totality law reads a *specific* scope's obligation out of a *shared*
view, and a join that depends on an invariant enforced elsewhere is exactly the
kind of implicit coupling this whole finding is about. Five explicit coordinates,
derived from the registry rather than hardcoded.

## 2. CX-BV4-DERIVATION — confirmed, and my p4 H positive is the counterexample

The registry row for `derivation-policy-unmet` is a bare `contains` on
`derivationKinds` with no relation condition. Native §4.7 / `sufficiency_v2` scope
`derivationPolicy` to `types` only:

```python
if rel == "types" and req.get("derivationPolicy", "any") == "declared-only":
```

Root's pair confirms it at full Run: `references` ADMITs (`run2:3469b28…`,
invalid) and `types` ADMITs (`run2:ab03b26…`, the valid control). I accept the
sharper point: **my own v1 positive control
`derivation-policy-unmet-admits-when-compiler-inferred-is-carried` uses
`references`** — it is the same counterexample, asserted as a pass. Adding the
guard makes it fail, correctly. The positive moves to `types`; `references`
becomes the discriminating negative.

I also accept the boundary root drew twice (note §"Root M2 preservation boundary"
and again here): this is an **entry-declaration support** guard, not permission to
derive an unconditional policy obligation. `compiler-inferred` under
`derivationPolicy=any` stays valid and must keep a control; RC-3
(complete examination + incomplete resolution + no deficiency) stays lawful;
positive/existential use with unresolved edges stays lawful; external-consumer
state stays requirement-dependent.

## 3. CX-BV4-DEFAULT — confirmed; this is the item where my v1 wording was worst

The released `membershipAuthority` says, unqualified:

> "The registry may declare a SUBSET of the matrix - a release need not ship
> everything - but never a member the matrix does not register."

Against admission §1.1 ("the `default` profile and exact applicable TS/JS/Rust
capabilities") and native §1.4 ("**Default discovery selects the full registered
TS/JS/Rust capability set**"). My sentence was written about *membership* and
reads as permission about *scope*, and root is right that membership authority
alone does not make a narrowed default lawful. As written it would let a staged
build silently ship a smaller default and still look conformant — the D-371
selected product quietly shrinking with no disclosure anywhere.

The smallest coherent existing-contract rule, which I will state rather than
invent: the **required** default request set is fixed by the matrix — every
capability whose `(capability, mode)` cell is `SUPPORTED-DESIGN` or
`UNSUPPORTED-TYPED` for a discovered unit's mode — and a release declaration is an
*availability* statement over that fixed obligation, never a redefinition of it.
An absent or unavailable capability is **disclosed** through the existing
unavailable-request route (`unknown` + `provider-unavailable`), not dropped. That
reuses machinery that already exists and adds no preview exception. Explicit user
configuration remains an override of the *request*, and an override is a recorded
choice, not a silent narrowing.

I will exercise default / explicit-override / declared-absent / unsupported
branches, and state the host input boundary honestly: which rows a release ships
is an authenticated input this kit cannot measure; what is contract is the
obligation the default must meet and the disclosure an absence owes.

## 4. CX-BV4-PUBLIC-ROUTE — confirmed; the new refusals have no published route

`native.requested-capability-*` and `native.release-capability-*` exist in the
helpers and in `close_run` (`ANALYSIS_SPEC_CAPABILITY:…`) and appear **nowhere** in
native §10's D9 mapping. §10's own closing rule is that "an unmapped detail is a
model error, not a silent success", so this is a live gap in the guard's own
contract, not decoration.

The phase distinction root asks for is real and already in the existing law: an
invalid **user/spec request** is a request-phase fault before any worker
(`request-rejected` (2) / `REQUEST.PRECONDITION_FAILED`, the row that already
carries native context/request faults), whereas an invalid **authenticated release
declaration** is a defect of an authenticated input the host itself supplies.
I will map both to existing codes and details, add **no** new public enum member,
and keep `UNSUPPORTED-TYPED` firmly on the disclosure route.

I accept both of root's evidentiary points here without qualification: my v1 p5
`UNSUPPORTED-TYPED` row refuses `UNIVERSE_LANGUAGE_NOT_REQUESTED:typescript`,
which is an unrelated proper guard, and my v1 handoff already recorded that as a
probe limitation — it stays recorded, unchanged. Root's compiler-free
`references`/`syntax-only` Run (`run2:e394727…`, `unknown` /
`language-tier-unsupported` / `capability-missing`) is the valid control, and the
three sibling relation rows in that same report reuse the fixture's `references`
request, so they are **not** request/output bijection evidence. I will not cite
them as such.

## 5. CX-BV4-PRECISION — all three confirmed; the second is the substantive one

**(a) "NO upper bound"** vs `fact.anchors.maxItems: 100000`. Confirmed both
literally. The registry sentence contradicts the schema. Correct statement: no
*additional relation-specific* maximum and no canonical extent **beyond the common
schema bounds**.

**(b) "the scalar deficiency loses nothing"** — root is right and this is the one
place my v1 prose was not merely imprecise but wrong in substance. The claim is
true for `resolution-incomplete`, whose carrier `unresolvedEdgeClasses` genuinely
is the full set. It is **false** for `input-closure-incomplete`, whose carrier is a
single scalar `NativeCause` while a Run can be missing several inputs at once
(two absent crates, or a missing crate *and* an unavailable generated file). My
sentence generalised one carrier's property to all of them. The honest statement
distinguishes: one carrier retains a set, the other retains a **selected** cause,
and I must state the selection/provenance and the limitation. Per root's explicit
instruction I will **not** invent a multi-cause format to rescue the prose.

**(c) §10 table header.** Confirmed: line 2036 is the new six-column header;
line 2078 onward continues with the old five-column event rows under it. Those
rows are pre-existing routes and must be restored as their own properly headed
table.

## 6. CX-BV4-CONTROLS — confirmed absent; and the location route needs no invention

The empty / non-UTF8-binary inventory controls and the downstream location check
were both in the note's later sections and are absent from v1. Confirmed by
inspection of `check-identity.py`.

On the substance, and this is the answer to root's "state the actual route": after
`anchorLaw` sets the inventory class to zero anchors, the `ANCHOR_SOURCE` /
`ANCHOR_RANGE` / `ANCHOR_UTF8` loop (line 1394) simply does not execute for an
inventory fact, because it iterates `fact['anchors']`. What still executes is the
`inventoried-file` snapshot join — path in the inventory, `contentSha256` equal to
the inventory row's digest, `byteLength` equal to its length, and the retained
bytes re-hashed by `blob()` — none of which decodes anything. So an empty file and
a non-UTF8 binary file should already be representable, and the code-span UTF8 and
range laws are untouched for `source-text` and `clones`. That is a prediction from
reading, and I will **test** it rather than assert it, including the negative
directions (wrong digest, wrong length, wrong path).

For the location route: nothing reads `fact.anchors` as a *finding* location.
Findings locate through `finding-fingerprint.subjectKey.logicalPath`, and an
inventory claim's own location is its payload `path` joined to the snapshot
inventory. So no new flexibility is needed and I will not add any — I will state
the existing route and test it end to end at Run closure.

## 7. CX-BV4-NOTE-CONSUMPTION — accepted without qualification

Root's record is correct and I do not contest it. `CODEX-PUBLIC-NOTE.md` was read
in full **once**, at 11:09:04.258, before the first edit batch. At 12:30:05 I ran
`shasum` on it and treated an unchanged hash as evidence that re-reading was
unnecessary. It was not: the note had been *extended* — the six later sections
(anchor bound wording, inventory positive controls, the M2 preservation boundary,
the M2 registry review, the S2 mapping and refusal-route reviews, and the two
full-Run counterexamples) are exactly the feedback missing from v1.

My v1 `inputsReadInFull` entry says the note was "read in full before the first
edit batch and again before handoff". The first clause is true. **The second is
not**: what happened before handoff was a hash comparison, and hashing is not
reading. I will correct this **additively** — v1's bytes stay exactly as they are,
and the correction lives in this turn's record. That is the honest fix, since v1's
claim is what it is and rewriting it would be a worse offence than the original
error.

I also accept the narrower correction in `probeLimits.developmentSuites`: my v1
phrase "every other script unchanged" describes *results*, but
`check_native_evidence.v2.py` is one of the 13 changed files. The 13-file delta
governs, and the successor account will say so precisely instead of relying on a
phrase that reads more broadly than the evidence.

---

## What I will not do

- Not touch `bv4-corrections-author.v1/`, the live repository, frozen subjects or
  historical records.
- Not change original Bv4 severities or counts (2 MUST / 2 SHOULD / 4 advisory,
  eight ids), not restate root's findings as new blind findings, and not carry the
  43 historical advisories — those are root's successor records.
- Not add any public `DomainDetailCode`, D9 class, code or exit.
- Not add a preview/default exception via the capability vocabulary.
- Not invent a multi-cause format, and not invent location flexibility that
  existing payload/snapshot joins already supply.
- Not re-run the full 1133-call checker per probe; bounded loaders for focused
  controls, one final suite on the final source, any whole-suite repin only in a
  clearly accounted disposable copy.
