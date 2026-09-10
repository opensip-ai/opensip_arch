# Fresh independent review — frozen candidate v9

**Verdict: CHANGES_REQUIRED**

**Subject manifest SHA-256 `288ac21453b635115b833935386ca5d65dbb6f482f51e078b118ffefb3ac1249`** —
2288 files, 57,852,259 bytes, snapshot root `/tmp/opensip-design-corrections/candidate-subject.v9`.

I am actual Claude in a fresh independent review. I authored none of these bytes. I am not coauthor
session `5dec928a-6357-4726-9ea8-49a3079fb726` and not v8 reviewer
`c48b2df7-1e29-4c97-9b91-f236e9b51e94`. I wrote only under
`/tmp/opensip-design-corrections/post-reset-review.v9`, including the disposable copy, and never
executed anything inside the frozen subject in place — so no shipped report could be overwritten,
which is the failure mode the v4 session recorded honestly and which I deliberately avoided
repeating.

**No MUST-level defect exists in these bytes, and both v8 SHOULD findings are independently
verified as fully closed**, as are all six v9 correction classes. The verdict is CHANGES_REQUIRED
because I found **one new SHOULD**. The gate is strict: any unresolved MUST or SHOULD means
CHANGES_REQUIRED, and I do not invoke the reasoning that a SHOULD is not required. That is the same
gate under which Codex correctly declined to promote v8's headline ACCEPT.

---

## 1. Custody

The manifest hashes to exactly the declared value. Every one of the 2288 declared files matches its
declared digest and length; the recomputed total is 57,852,259 bytes; there are **zero** undeclared
files on disk and **zero** declared files missing. I re-ran the entire verification — manifest
digest, every file digest and length, and the undeclared-file scan — **after** all probing, and it
is unchanged (`work/final-custody.json`).

The v8→v9 delta is **25 changed, 264 added, 0 removed**. Two changes deserved checking rather than
assuming:

- `NEXT-REVIEW.md` shrank from 69,498 to 3,987 bytes. I checked every substantive line of the v8
  file against the v9 file plus the three `resume-history-*` documents: **0 lines lost**.
- `native-evidence-report.v2.json` differs from the image the v4/v5/v6 handoffs declared. That is
  legitimate — Codex regenerated it in the final in-tree run — and the frozen report is a genuine
  `PASS` at 151/151 with `pins.verified: true`, not a `PIN-MISMATCH` residue of the kind the v4
  handoff disclosed.

All nine coauthor-owned files declared in the v6 handoff match the frozen v9 bytes exactly, and
every hash claimed inside `post-reset-dispositions.v9.proposed.json` — the v8 review, the v8
dispositions, and the v4/v5/v6 handoffs — verifies.

## 2. What I did, and what that is worth

I reproduced all six reference commands against a verified disposable copy. All six logs are
**byte-identical** to the retained images, and all six regenerated in-tree reports are
**byte-identical** to the frozen subject: foundation 950 (231+602+24+28+65), security 456 + 10
sweeps, native 151 with 60 matrix cells and **0 qualified**, workflow surface 1290, integration
363, with pin sets 1099/73/71/65. That agrees exactly with `validation-summary.v1.json`.

That establishes determinism and the authors' own claims. **It is not acceptance.** My harness
loads `check-identity.py` truncated at the end of `graph_with_import`, so none of the authored
`check()` assertions run at all; every finding below rests on probes I wrote. v9-S1 is a direct
demonstration of why this matters — an authored check passes while the property its *name* asserts
is false.

## 3. The two v8 SHOULD findings — both closed

### v8-S1 (Plan/configuration budget equality) — closed

`identity-and-evidence.md` §3 now states the rule normatively: the Plan's deterministic `budget`
must equal, **exactly and by type**, the `analysis.budget` of the committed resolved semantic
configuration the same Plan names; a legitimate override enters the **resolved semantic
configuration first** so neither committed place silently wins; a contradicting Plan is refused
before any evaluation; and it is stated that no identity, replay or determinism property changes,
because both values already enter PlanId. Both schema descriptions cross-reference the rule and the
enforcement at `identity-model.py:825` is unchanged.

**This is not a schema-closure fix, and G8's retraction stands.** I compared the two budget schemas
structurally with descriptions stripped: `plan.budget` and
`semantic-configuration.analysis.budget` are shape-identical between v8 and v9 — both were already
closed `{unit, limit}` objects with `additionalProperties: false`. The v9 change is
description-only. The blind reviewer's own retraction of G8 therefore remains intact and is not
reopened.

### v8-S2 (a file payload's content claim joined to nothing) — closed, end to end

v8 recorded that it *could not* drive a file Run to a seal, because its fixture Coverage for
`file@enumerated` was refused first by RC-1, and asked a future reviewer to confirm end to end. I
supply that confirmation independently.

I built a lawful **complete** file Run straight from the shipped builder with no monkeypatching. It
closes, prepares, replays and **commits**, and the file fact is genuinely *reachable* — named by
the predicate witness's `matchingFactIds`, not merely present in the view. Five negatives each
reach their intended join, with the witness and proof refs resynced after mutation so that no
refusal can be an artifact of a stale witness:

| mutation | cause reached |
|---|---|
| false `contentSha256` | `RELATION_FILE_CONTENT_JOIN:a.ts` |
| `contentSha256` of a *different inventoried* file | `RELATION_FILE_CONTENT_JOIN:a.ts` |
| false `byteLength` | `RELATION_FILE_LENGTH_JOIN:a.ts` |
| `byteLength` of a *different inventoried* file | `RELATION_FILE_LENGTH_JOIN:a.ts` |
| uninventoried `path` | `RELATION_PATH_NOT_INVENTORIED:file:absent.ts` |

**The memoised-decode case is proven in both directions**, which is the part that actually matters.
I built two facts carrying one byte-identical payload digest, so payload decode is a cache *hit* on
the second. The foreign-anchor second owner refuses at `RELATION_ANCHOR_FOREIGN_PATH`; the lawful
same-file second owner **admits and commits**. The positive control is what makes this evidence
rather than noise: the rule is doing owner-specific joins outside the memo, not refusing all second
owners.

**RC-1 is untouched and no rung was invented.** Measured on the sealing Run: `enumerated` is *not*
in `RESOLVED_RUNGS`; `resolutionCompleteness` is `not-applicable` with `attempted: false` and
`unresolvedEdgeCount: 0`; and the *separate* examined-partition claim `entry.coverage` is
`complete` with `deficiency: null`. That is exactly the shape v8 predicted, reached by deriving the
claim from the rung through the native producer's own helper instead of asserting it.

## 4. The v9 correction classes — all verified

**The relation payload digest/path boundary is fully governed.** Enumerating by `$ref` rather than
by pattern guessing, there are exactly seven governed fields across the 13 relations. Six are
joined; `vcs-change.previousPath` declares `retention: not-joined` with its reason stated. **Zero
ungoverned.** `package.manifestPath` and `vcs-change.path` are joined to the snapshot inventory,
and a manifest inside the pruned `node_modules/` tree is refused as uninventoried — the package
path semantics match the declared source scope. Historical VCS paths keep their distinct meaning:
the *same* uninventoried path `gone.ts` refuses under `changeKind: modified` and is **exempt** under
`deleted`, and an uninventoried `previousPath` on a rename is not joined and commits.

**The normalized-body identity reconstructs exactly.** I rebuilt the inherited domain-separated
preimage from `fact-identity-policy.v2#/canonicalisationSchema/byteGrammar` with my own code and
reproduced every frame **byte for byte** across five complete clone Runs, all of which commit. Per
Run: five `u8`-prefixed components then `u32be` payload with zero trailing bytes; lengths
`[24,11,32,10,32]` for TS/JS and `[24,11,32,4,32]` for Rust, all inside the `u8` bound; `domainTag`
equal to the inherited literal; `levelId` equal to the payload's `normalisationLevel`;
`levelVersion` carried as **raw 32 digest bytes and not hex text**; `normalisationVersion` equal to
the raw SHA-256 of the **retained** level-specification bytes; and at L0 the payload `u32be`-framed
and equal to the **exact anchor span read from the enclosing fact's own snapshot blob** — a real
source join, recomputed rather than asserted. This is custody and framing evidence. It qualifies no
normalizer and grades no tokenisation, and I do not confuse the two.

**The 723-byte objection reconciles.** I measured the 21-entry Rust edition map independently: 711
bytes bare, 723 wrapped as an `edition` member. Codex reported 723. Both exceed the inherited
255-byte `u8` maximum, so the conclusion holds; only the wrapping differs, which I record as an
advisory so a future reader can reproduce the number. The final projection is fixed at raw 32 bytes
for both the small and the 21-entry map, the large-map Run commits, and unrelated crate growth
leaves the body identity unchanged while the universe identity moves.

**Version sensitivity is real, on the right fields.** `rustcVersion` and `rustCommitHash` each move
the language-version component; the declared exclusions `targetTriple`, `cargoVersion` and
`sysrootDigest` each leave it unchanged. Compiler identity is reachable through the universe's own
`nativeContextId`, so the earlier coauthor assertion that it was absent is correctly withdrawn — I
verified the reachability rather than accepting either the assertion or its withdrawal.

**Mixed-edition Rust provenance holds.** All five refusal causes are distinct and intended, driven
directly through the model: `BODY_LANGUAGE_OWNERSHIP_REQUIRED`, `BODY_LANGUAGE_OWNER_UNENUMERATED`,
`BODY_LANGUAGE_OWNER_NOT_COMPILED`, `BODY_LANGUAGE_OWNER_NOT_SELECTED`,
`BODY_LANGUAGE_OWNER_AMBIGUOUS`, plus `BODY_LANGUAGE_DIALECT_ABSENT` on an empty map. Partial
enumeration refuses **before any row is read** — I confirmed this by planting a conflicting owner
under `partial` and observing the identical enumeration cause — so partial discovery cannot act as
hidden selection. The **same physical `src/lib.rs` under two explicitly selected target editions**
(lib 2021, bin 2015) both commit with **different** body identities, in a workspace where the
package default map alone could not have distinguished them; selecting both at once refuses as
ambiguous. No path, crate name, unit id or selection enters the record — selection establishes the
join only.

**Body language is not provider language.** A complete JavaScript clone Run through the TypeScript
*engine* universe closes and commits carrying body `languageId: javascript`, as native §6.3–6.4
requires, while a **byte-identical** `.ts` body has a different `bodyIdentity`. All nine registered
suffixes map to distinct variants; `.vue`, a suffixless path and an uppercase `.TS` each refuse
rather than being folded into a neighbour.

**Unit identity is derived, not opaque.** I recomputed `H(native.compilation-unit.v1,
UnitIdentityV1)` from the published projection with my own code and agreed on all six vectors —
ordinary paths, a marker path containing `#`, two `#` segments, a 4096-character `markerPath` and a
256-character `targetName` — all fixed width and all distinct, with one-over-bound values refusing.
A **complete Run** whose owning unit marker path contains `#` closes and commits.

**Body identity stability is measured, not assumed.** With compiler, dialect, source and level
inputs unchanged, enlarging the units table and adding an unrelated crate changes
`sourceUnitOwnershipId` and `sourceUniverse` while leaving `bodyIdentity` **identical**; changing
the selected effective edition does move it. This confirms the coauthor's withdrawal of the
opposite assumption.

**The partial-Coverage bypass is closed without over-refusing.** Driven through the owning Run
rather than by a producer choosing a flag: with partial ownership and an empty view, a
contradictory `complete` claim refuses at
`COVERAGE_DIALECT_PREREQUISITE:clones:enumeration-partial`, while the honest
`unknown`/indeterminate control still closes, replays and **commits**. The boundary is genuinely
universe-level: under a **healthy** universe whose anchor path is simply unowned, an honest empty
view still claims `complete` and commits. That is the right line — the rule checks universe-wide
availability, not the truth of a producer's observations, and it does not prohibit honest empty
findings.

**Transitive pins are authenticated, not merely present.** All four artifacts are pinned in all
four suites at the claimed counts with zero digest mismatches. Because presence is not
authentication, I tampered each of the 16 suite/artifact pairs in throwaway copies: **every one
refuses with a pin fault**, each against a passing untampered control. (My first attempt at this
was invalid — see §6.)

**Workflow §8 and §12 are exact.** `DELIVERY.REQUIRED_FAILED` is an **existing** classification,
present in v8 too, not invented; `terminate()` retains a committed RunId and invents none when
uncommitted; the projection is a total comprehension over `parityFields`; and a pure `KeyError` from
the reference helper is explicitly not itself a public termination, with host wiring left as a
DR-G17/G20 obligation — an honest boundary rather than a gap. `validate_pinned_purge_refusal`
consults no ledger, lease, observation or inventory, returns the envelope only, and grants no
effect authority, which is precisely what §12 now says.

**v8's major corrections are preserved.** The relation registry is closed at 13 (12 inherited plus
`unresolved-edge`), every row resolving to a selector present in the registered document under one
declared CJSON codec. All four inherited CVE1 gates fire with exact causes — `capability.adm-type`,
`adm-closed`, `adm-domain` (relation, rung and platform) and `adm-order` (duplicate platform,
duplicate provider, and unsorted platform against a sorted positive control) — and I recomputed the
CVE1 identity independently, agreeing exactly with the committed `508f24c7…`. The native Coverage
producer boundary is real: it admits the honest payload and refuses a contradictory completeness
claim. The enumerator is a Plan member and a foreign one refuses. The canonical encoder does not
sort arrays.

## 5. The new finding

### v9-S1 (SHOULD) — the relation digest law has three limbs and only two are consumed

`relation-payload-schemas.v2.json#/x-opensip-digest-law/residueRule` states that *"An annotated
field with no join, a join naming a field the selector does not have, and an unannotated digest/path
field are each inadmissible"*, and the law's standing states *"There is no default and no residue: a
new such field added without an annotation is inadmissible."*

Limbs 1 and 2 are genuinely consumed — I reproduced `RELATION_DIGEST_LAW_RESIDUE`,
`RELATION_JOIN_FIELD_UNKNOWN` (in isolation, so the residue check could not fire first) and
`RELATION_DIGEST_RETENTION`, with the shipped document passing as a positive control for all 13
relations.

**Limb 3 is enforced nowhere.** `relation_annotation_closure` iterates only fields that *already*
carry `x-opensip-digest`, so an unannotated field is invisible to it by construction. I injected an
unannotated `DigestHex`, `Sha256Text` or `CanonicalPath` field into every one of the 13 relation
selectors — **39 injections, 39 admitted.** A grep of every shipped `.py` outside `reviews/` finds
no other consumer.

Worse, `check-identity.py` ships a check named
`every-relation-payload-digest-and-path-field-is-annotated-and-joined`, but its assertion only
checks that the closure returns non-`None` per relation and that the join-bearing set equals
`{file, package, vcs-change, clones}`. I reproduced that exact assertion against a document carrying
an unannotated `CanonicalPath` field: **it still evaluates `True`.** The suite passes while the
property its name asserts is false.

This is not a deliberate scope boundary. The **native bundle implements exactly this sweep** —
`native_digest_annotation_coverage()`, which walks for `DigestHex`/`Sha256Text` sites and requires
an annotation, with the docstring *"A new field without one is inadmissible"* — and it **is
consumed**, asserted at `check-identity.py:2070-2071` with `unannotated == []` and `annotated >=
68`. The relation bundle declares the same rule, ships no equivalent, and declares no exemption for
it.

**Why it matters.** This is the guard that keeps the v8-S2 class closed under future editing.
v8-S2 was exactly a payload field joined to nothing; the residue rule is the mechanism that makes
that unrepresentable, and a third of it is inert. An implementer building from the law would
implement all three limbs and the reference implements two, so two conforming implementations would
disagree on whether a document is admissible — the identical rationale that made **v8-S1** a SHOULD
and was accepted and fixed.

**Why not a MUST.** No admissible payload can exercise it today: the relation payload schemas are
closed, and the shipped document has **zero** unannotated governed fields across all 13 selectors.
There is no current defect in these bytes and no runtime attack surface; adding such a field
requires a reviewed design-time edit to a registered document. Identity, replay and determinism are
unaffected, since any such value still enters `payloadDigest` and hence fact2 — the same reason
v8-S2 itself was graded SHOULD.

**The counter-argument, stated plainly.** The law's standing says coverage is asserted *"by
consumed CHECKS in the Run closure, not by counting annotations"*, which can be read as
deliberately declining a native-style counting sweep. If that is the intent, then the design has
stated a rule its chosen mechanism cannot deliver, because an unannotated field is by construction
invisible to a consumed join check. Either way the law and the enforcement disagree; only the
remedy changes.

**Remedy.** Either (a) add the native-style annotation-coverage sweep over the relation document
and consume it, and fix the check whose name already claims it; or (b) scope the third limb
explicitly as a design-time authoring rule rather than an admissibility rule, and rename the check
to what it actually asserts. Either is small. What is not acceptable is a normative inadmissibility
claim with no consumer plus a test name that asserts it.

## 6. My own harness errors — corrected, and not counted as product defects

Twelve of my probes initially measured the wrong thing. Each is corrected in a successor probe and
every superseded probe is retained. None is a product defect, and I state them because a review
that hides its own misfires is not usable evidence:

- p01 classified `bodyIdentity` as unjoined (`bodyIdentityJoin` binds under key `field`, not
  `*Field`) and `previousPath` as reasonless (its reason is under `join`). Both were my classifier
  bugs; p02 finds **zero** ungoverned fields.
- p02 mutated `FilePayloadV1` but asked the *per-relation* closure about `clones`, so nothing raised.
- p03's limb-2 test renamed an existing join role, which made a real field unjoined so the residue
  check fired first — an ordering artifact, fixed in p04 by *adding* a bogus join field.
- p05 expected a `RELATION_FILE*` token for the borrowed-anchor owner (the intended join is
  `RELATION_ANCHOR_FOREIGN_PATH`) and for a dropped blob (`EVIDENCE_UNAVAILABLE` is correct and
  earlier).
- p08 edited the *first* `semanticVersion` literal — the rust-dev-llvm closure, a **deliberately
  excluded** field — so its negative version result measured nothing; and its refusals were masked
  by the fixture's own `FIXTURE_NO_ADMISSIBLE_PAYLOAD` guard.
- p10 tested the healthy-universe empty view by owning an *uninventoried* path, refusing earlier at
  `NATIVE_NESTED_PATH_NOT_INVENTORIED`.
- p12 omitted the required `--report` argument for three runners, so its "refusals" were argparse
  usage errors. **This one mattered**: only `native` had genuinely detected the tamper. p13 redid it
  properly with untampered controls, and all 16 then refuse with real pin faults.
- p14 string-matched a line-wrapped contract sentence; confirmed present with whitespace normalised.
- p15 compared the registry's `payloadSchemaDigest` *description* to a hash (no self-hash cycle
  exists or is wanted), matched `POST-CONSTRUCTION` in the wrong case, and counted typed order
  annotations in a document that legitimately carries none.
- p16 assumed the capability manifest was JSON; CVE1 is a binary encoding.
- p16b tested "unsorted platform" on a provider with a *single* `platformId`, where no disorder is
  constructible; p16c redid it with two registered platforms and a sorted control.
- p17 moved the vcs-change payload path without moving the rule atom filtering on it, so the fact
  stopped matching and refused at `PROOF_REPLAY_MISMATCH`.

## 7. Dispositions

All 16 AR rows, all 15 FW rows, all 27 inherited residuals (DR-001..011 and DR-011-R01..R16), and
the five scoped DR-201..205 rows are dispositioned individually in `review.json` with exact bases
and selectors.

- **AR**: 15 ACCEPT; **AR-15 CHANGES_REQUIRED** — not because the crosswalk is wrong. Its routing is
  correct and honest: every item retains `AUTHOR-CORRECTED-PENDING-INDEPENDENT-REVIEW`,
  `currentReviewBinding` stays `PENDING-INDEPENDENT-REVIEW` with no embedded future digest, and the
  only v8→v9 change is appending review history that explicitly records that v8's headline ACCEPT
  retained two unresolved SHOULDs. AR-15 is graded CHANGES_REQUIRED solely because this review
  carries an unresolved SHOULD the integration narrative must absorb.
- **FW**: 15 ACCEPT. FW-14's real configuration corpus correctly remains an implementation
  obligation and is not claimed.
- **Inherited residuals**: 26 ACCEPT; **DR-011-R10 CHANGES_REQUIRED** — the blind consumer row can
  only be closed by an actual fresh blind litmus on accepted bytes. No Bv3 exists; the completed Bv2
  is CHANGES_REQUIRED against a predecessor manifest. The row says it cannot be closed by the
  proposed table, and I do not close it.
- **Scoped DR-201..205**: ACCEPT, strictly scoped to routing. No architecture file changed between
  v8 and v9, so each row's 2026-08-13 ACCEPTED grade is preserved as history, neither extended nor
  re-litigated.
- **Product qualification gates**: all **32** carry `demonstrated: false` across the four canonical
  platform families. I demonstrate none and grant none.
- **Evaluation subresiduals**: all **30** (19 RES, 7 NB, 4 measured escapes) carry individual
  dispositions under DR-011-R12.

## 8. What this review does not do

It grants no blind, application, readiness or qualification standing. It performs no OS, compiler,
cargo, crypto, storage, clock or end-to-end measurement, and it claims none — every native and
toolchain observation here is an explicit synthetic trusted input, and "commits" means the reference
custody model accepted a transition, not that any real store is durable. It does not demand a real
OS, compiler, crypto or store implementation from a design/reference exercise, and it does not
convert synthetic TCB inputs into qualification. Readiness remains unapplied and **condition 5
remains NOT MET**, as do conditions 1, 2 and 3. Frozen v8 remains exact historical evidence, its
headline ACCEPT with two retained SHOULDs recorded as it stands rather than rewritten. Application
acceptance is scoped separately and is not granted; a fresh blind consumer and a complete
independent application review remain later acts.

I read the Codex technical review, the v9 dispositions, the v4/v5/v6 handoffs and the Codex
counterexamples as **assertions to test**, not as evidence. Where I agree with them, it is on the
strength of my own probes.

## 9. Path to ACCEPT

One finding stands between this candidate and a clean gate, and its remedy is a few lines plus a
test rename. Close v9-S1, freeze, and obtain a fresh independent review at zero unresolved MUST and
SHOULD; then the blind Bv3; then application and readiness as separate reviewed acts.

---

*Probes, results, positive controls, intended refusal causes, custody records and the report
reproduction are retained under `/tmp/opensip-design-corrections/post-reset-review.v9/`
(`probes/`, `work/`, `runs/final-v9/`).*
