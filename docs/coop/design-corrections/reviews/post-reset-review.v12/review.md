# Independent design/reference review — frozen candidate v12

**Verdict: ACCEPT.**

- Subject: `/tmp/opensip-design-corrections/candidate-subject.v12`
- Manifest SHA256: `fc124cc7d487f7f6fcc97665255574273b03fe1f09e6b70c3246feedf1678beb`
- Reviewer: actual Claude, fresh independent session. I authored none of these bytes and am neither the coauthor session `5dec928a-6357-4726-9ea8-49a3079fb726` nor the prior reviewer session `cd236691-03ef-4863-b612-e7d8cdf0d3ad`.
- Scope: independent **design and reference acceptance only**. Not reconstructability, not readiness, not application, not product qualification.

Under the strict gate — any unresolved MUST or SHOULD forces CHANGES_REQUIRED, and ACCEPT is never granted with a non-blocking SHOULD — this candidate passes. Both completed v11 required findings are resolved and independently reproduced from the frozen bytes; I raise no new MUST and no new SHOULD. `newMustIssues` and `newShouldIssues` are both present and empty in `review.json`. Two explicitly non-blocking advisories are recorded separately and do not bear on the verdict.

---

## 1. Custody

I verified every declared file digest and length, plus an undeclared-file inventory, **before and after** all work.

| | Before | After |
|---|---|---|
| Files declared / verified | 2981 / 2981 | 2981 / 2981 |
| Total bytes declared / computed | 82,723,140 / 82,723,140 | identical |
| Digest or length mismatches | 0 | 0 |
| Undeclared files | 0 | 0 |
| Missing files | 0 | 0 |

The before and after reports are byte-identical, aggregate tree digest `e9fc5561…`. The manifest file itself hashes to the pin I was given. The declared `predecessorManifestSha256` equals the stated frozen v11 pin `a03b7fe9…`, and the retained prior review JSON hashes to `ea93b92d…` — both as stated. I re-verified the frozen v11 snapshot independently (2786 files, 0 mismatches) since I use it as a comparison basis throughout.

All my writes were confined to `/tmp/opensip-design-corrections/post-reset-review.v12`, including every disposable copy and probe. I regenerated reports only inside disposable copies — never inside the frozen subject, never inside the original repository. Both were re-verified unmodified afterwards.

## 2. The exact delta, recomputed

16 changed, 195 added, 0 removed, 2770 unchanged.

Only **three** files matter semantically:

- `foundation/identity-model.py` (+960) and `foundation/check-identity.py` (+7045) — the coauthor two-file delta.
- `docs/v2/contracts/product-v1/identity-and-evidence.md` (+82) — the one normative prose insertion.

The remaining thirteen are bookkeeping. Seven of them are **same-length substitutions**, which I inspected individually rather than trusting the byte count: four pin ledgers and `integration-fixtures.py` carry updated 64-hex digests; `validation-summary.v1.json` advances counts and two review-version labels; two report files carry updated nested report digests. No prose or logic changed in any of them.

**Zero registered schema or registry bytes changed.** I confirmed this positively rather than by absence from a diff list: all five foundation schema JSONs, the registered relation document, the digest law, the relation registry, all 13 relation closure rows and the coverage sweep are canonically byte-identical across the delta.

## 3. Prior finding v11-M1 (MUST) — RESOLVED

The v11 finding was that two of six declared reference commands did not pass on the frozen v11 bytes, because the security and workflows pin ledgers carried the *v10* digest of `correction-crosswalk.proposed.json`, which the final recording step rewrote after pins were refreshed and after the commands ran.

I was instructed not to accept the root's sequencing assertion as evidence, and I did not. Instead I tested the outcome, which is the stronger and order-independent property: **do the frozen bytes reproduce their own declared evidence?**

**Pin audit.** All 1,308 pins across the four ledgers, against the frozen v12 bytes: **0 stale, 0 missing** (foundation 1099, security 73, workflows 65, native 71). The two formerly stale entries now read `556879f7…`, which is the actual frozen digest of the crosswalk.

**Six commands.** Re-executed in a disposable full-subject copy. All six exit 0, and every deterministic report *and* log is **byte-identical** to the frozen one:

| Command | Exit | Report | Observed |
|---|---|---|---|
| foundation | 0 | identical | pins valid, 1099 sources, passed |
| security | 0 | identical | 456/456 cases, 10 sweeps true |
| native | 0 | identical | 151/151, 60 matrix cells, 0 open |
| workflows | 0 | identical | pins valid, 65 sources, passed |
| workflow-surface | 0 | identical | 1290/1290 |
| integration | 0 | identical | 363 passed, 0 failed |

These match `validation-summary.v1.json` exactly: foundation 1115 = 231+767+24+28+65, security 456 + 10 sweeps, native 151, workflows 1290, integration 363.

**Both tools proven discriminating.** A clean result is worthless if the instrument cannot detect failure, so I ran both against frozen v11. My pin auditor reproduced *exactly* the two stale pins with exact hashes (`9560a51e…` pinned vs `ae78c7e6…` observed). My command harness reproduced *exactly* the two failures — security and workflows exit 1, `sourcePinsValid: false`, `checksExecuted: false`. So the zero-stale, all-pass result on v12 is not vacuous.

Independently, a field-level comparison of all 16 crosswalk rows across v11→v12 shows the **only** differing fields are `historicalReviews` and `latestCompletedReview`. No status, obligation, owner or routing field changed; AR-15 remains `PROPOSED-SOURCE-MAP-PENDING-REVIEW-AND-APPLICATION` and still routes DR-201..205.

The earlier PASS reports remain in the tree as historical records of an earlier working state, and the root's own error account is disclosed separately in `post-freeze-pin-drift.v11/account.json` with a read-only recheck showing 2 mismatches of 1,308 — which I reproduced.

## 4. Prior finding v11-S1 (SHOULD) — RESOLVED

`validation-summary.v1.json` now reads `claudeFinalReview: "PENDING-FROZEN-V12"`, with `claudePriorReview` advanced to `reviews/post-reset-review.v11/review.json` and `priorReviewLimitation` rewritten to the v11 outcome. The label correctly names the candidate this review is against, and advancing V10→V12 rather than to a stale V11 is right, because the v11 review is complete.

## 5. Prior advisory v11-A1 — corrected, and confirmed beyond its author's matrix

The defect: early annotation collection and inheritance used Python membership, so `ordinal=1` and `ordinal=true` were collapsed before typed conflict checking, although canonical JSON distinguishes them.

I wrote my own probe — my own document shapes, my own pair table, my own oracle — and ran it against **both** frozen models. **7 location classes × 6 typed-distinct pairs × 2 orientations = 84 cases.**

| | frozen v11 | frozen v12 |
|---|---|---|
| Refuse with `RELATION_DIGEST_ANNOTATION_CONFLICT` | 36 | **84** |
| Wrongly ADMIT | **48** | 0 |
| Surviving annotations at the probe path | 1 in the 48 failures | **2 in all 84** |
| Identical-annotation positive controls admitting | — | **42 / 42** |

So under v12 typed-unequal annotations conflict in **either order** at every location, both survive collection so the conflict limb can see them, and typed-equal controls remain usable. Under v11, 48 cases across four location classes silently collapsed. One of those four — `array-items-container` — is a class **I** invented that is not in the authored matrix, so the correction generalises beyond what its author tested. The authored 35-case / 9-discriminating recheck is consistent with my measurement on the overlapping shapes.

**Source completeness.** All four comparison sites now route through one helper, `annotation_already_collected` = `C.equal_typed`: the same-path merge, the inherited collection, the `$ref`-chain contribution filter, and the conflict limb's distinct list. `governed_form` only concatenates and performs no equality comparison, so it cannot collapse a pair. No residual Python-equality annotation comparison remains.

This implements the already-agreed v11 normative typed-equality rule. It adds no annotation schema restriction and no normative feature — the registered documents are canonically unchanged. And it is a hypothetical schema/reference consistency matter, not an attack on current closed Run payloads: no annotation value in the registered document is numeric or boolean, so no such pair can be written today.

**Provenance.** The two applied source files are byte-identical to the retained released coauthor images (`ed38f172…`, `f9b427a8…`), and the retained before-images are byte-identical to frozen v11 (`de3ae06b…`, `90a3b590…`). Handoff `74de34c5…` verified.

## 6. Prior advisory v11-A3 — the cycle sentence

One sentence was added: *"Following local references must terminate even when a local definition is cyclic."* — exactly 81 bytes, sha256 `7375c210…`, matching the declared value.

I inspected the actual insertion and custody rather than substring similarity with earlier drafts. Recomputing from the frozen bytes: the replaced v11 block is 409 bytes hashing to `c6c61d28…` and the v12 replacement is 491 bytes hashing to `79c94849…` — **both byte-exactly** the blocks recorded in the bounded Claude assessment (`2ed0b757…`) and the root custody. A whitespace-normalised comparison of the whole 83 KB contract proves the rest of the document is identical after removing that one sentence, so the only other effect is the explicitly assessed local rewrap including the pre-existing 105-column line.

The coauthor read Codex's 52-byte proposal and offered a clearer alternative; the applied text is byte-identical to that assessed refinement, not a paraphrase. The assessment records `agrees: true`, `refinementIsBlocking: false`, `sourcesEdited: []`, `suitesRun: []`, and states it did not claim to read a completed independent verdict.

It states existing robustness, not a new feature. I confirmed behaviourally that a self-referential container terminates and refuses when unannotated and admits when annotated, and that mutually recursive defs and an alias-only cycle both terminate. No admission outcome depends on the wording.

## 7. Prior advisory v11-A2 — measured, not corrected

Recounted independently: frozen v12 has **767 passing calls / 757 distinct ids / 10 extra instances** from exactly two parameterised ids (`closed-closure` ×6, `exact-version-closure` ×6); frozen v11 has 673/663/10 with the same two ids. All instances agree, so nothing is masked, and **zero historic ids were renamed or dropped** — v12's id set is a strict superset of v11's, adding 94.

The duplication itself was not corrected; it was measured and disclosed in a dedicated artifact. That is a legitimate response to a non-blocking advisory and I do not escalate it. It stays a carried open advisory, and I raise a related non-blocking advisory (v12-A1) about where that disclosure lives.

## 8. Normative prose — assessed as a blind input

I treated each normative sentence as a falsifiable claim and tested it against the reference with my own constructed documents. **All 14 cases hold.** Highlights:

- **All six refusal causes are derivable from the prose** — missing annotations, conflicting annotations, undeclared retention, unaddressable claimed joins, missing joins, and joins naming absent fields — and the closing sentence enumerates them explicitly.
- **Terminal scalar exclusion** — annotating the shared terminal `DigestHex` def does *not* blanket-exempt; an unannotated governed occurrence still refuses.
- **Branch isolation** — an annotated alternative does not cover an unannotated one, in *both* branch orders; a parent annotation does cover each alternative it encloses.
- **Monotonic missingness** — a third *annotated* sighting arriving after a missing one still refuses, in both visit orders. The previous v11 same-path missingness fix is intact.
- **Order independence** — all six key permutations of a probe node yield one identical outcome.
- **Top-level join addressing** — a nested member cannot be joined and must declare `not-joined`; a scalar alternative of a top-level property preserves the address and admits.
- **Direct non-governed annotations** — the prose refers explicitly to top-level *selector properties*, and that is exactly what the code does: `file.byteLength` refs `UInt64` and is non-governed, yet as a directly annotated top-level property an invalid retention on it refuses and a joined retention without its join refuses — while an annotated non-top-level non-governed member is correctly not dragged in.
- **Exemption reasons are an authoring disclosure obligation** — admission validates the *declared retention*, not the presence or content of the reason prose. An annotation with the `reason` key absent, and one with an empty reason, both admit. No new reason key is invented; the vocabulary is exactly `{not-joined, preimage, provider-output-retained, snapshot-inventoried}`.

A blind implementer can derive the traversal surface, the effective-annotation rule, the three limbs, typed equality, order independence, monotonic missingness, join addressability and every refusal condition **without reading the author's Python**. I found no silent gap in the claimed language, and I demand no schema-language feature beyond declared support.

## 9. The three law limbs and the 39 injections

All three limbs use the **same effective annotations**, confirmed for field, alias-definition *and* nullable-branch placements:

| Limb | Injection | Cause |
|---|---|---|
| 1 | unannotated governed field | `RELATION_DIGEST_UNANNOTATED` |
| 2 | annotated field without join | `RELATION_DIGEST_LAW_RESIDUE` |
| 3 | join naming a missing field | `RELATION_JOIN_FIELD_UNKNOWN` |

Invalid retention refuses with `RELATION_DIGEST_RETENTION`. The intended cause carries its exact selector: `RELATION_DIGEST_UNANNOTATED:file:file.strayGoverned:DigestHex`.

**39 injections across 13 selectors** — 13 relations × 3 governed forms — all refuse, none admits; and the **positive control** shows all 39 admit once annotated, so the refusal is caused by the missing annotation and by nothing else about injecting a field. All eight shapes (ref, inline, nullable, aliased, nested, array, container-ref, cyclic-container-ref) refuse unannotated and admit annotated, preserving the earlier Codex traversal/alias/inherited-limb counterexamples.

**The byteLength distinction, as required.** `file.byteLength` is annotated but refs `UInt64` and is non-governed, appearing as an ungoverned sighting with `form: None`. **Removing its annotation ADMITS** — it does not require third-limb refusal — whereas removing the annotation from any of the seven governed digest/path fields refuses with `RELATION_DIGEST_UNANNOTATED`. The coverage sweep counts exactly 7 governed fields (file 2, package 1, vcs-change 2, clones 2) and does not count `byteLength`.

The `vcs-change.previousPath` **not-joined exemption is preserved** verbatim, with its stated reason about naming a state before the analysed snapshot. All 13 registered relations admit and remain coherent.

## 10. No unintended change; identities stable

Beyond the canonical byte-identity of the registered artifacts, I harvested the identities the suite actually computes, by source-instrumenting `identifier()` inside disposable copies of *each* frozen tree:

- **21,562 identity computations, 5,370 distinct, across 17 domains** — under both v11 and v12.
- The multiset digests are **identical** (`252d4f6c…`).
- Both suites exit 0 (673 and 767 passing, 0 failed).

So the delta added 94 checks and changed **zero** computed identities. Combined with the strict-superset check-id set, this is the basis on which I carry forward the previously confirmed behaviours — owning-snapshot joins and memo owner context, `file@enumerated` coverage, the 13 registered relations and typed arrays, CVE1's four gates, nativeCoverage producer admission, Plan enumerator membership, the complete TypeScript+Rust Run closure, the TS config/layout surface, raw32 clone body version, JS body language via the TS engine, L0 recomputation versus L1–L3 custody, the Rust target/edition/marker/bounds surface, stable body IDs under unrelated ownership, the partial/absent-ownership and honest-partial controls, cache lookup versus validated hit, mutation versus repair replay, public purge disclosure, required-output failure and committed-Run preservation, and leased pin ledger comparison versus pure projection. I did **not** re-derive each from first principles, and I say so plainly.

The 723-byte canonical wrapped edition record (bare map 711), conservative suffix choices, the fixture-level spec not being a qualified FACT-IDENTITY asset, "no clone facts" not exempting Coverage prerequisites, and multiple contexts per language with owning-universe joins are all carried on the byte-identity of their governing files.

## 11. Preserved failure evidence

The v11 review's failed p12 attempt is preserved **literally**: `logs/p12-reachability.json` is a **zero-byte file** — exactly what "no result" should look like — with its driver and probe retained. The v11 review records that it exceeded the 600-second foreground wait, was moved to the background, and was terminated by its reviewer with **exit 144 and no result**. The subsequent explicit disposable instrumentation `p12b` independently produced completed reachability evidence (16 mergeBranch executions in v11 versus zero in v10, 1355 record calls), and the technical review restates that distinction rather than presenting the incomplete trace as passing evidence.

The v11 review's four honest self-corrections are retained verbatim. I independently re-checked the DR-012 one: `inherited-residuals.proposed.md` contains `DR-012` only in the sentence "DR-012 remains release qualification", confirming the 27-row register and the correctness of that self-correction.

## 12. Registers

- **16 AR** dispositions, individually keyed. The nine that were `CHANGES_REQUIRED` in v11 were *all* linked to v11-M1 — every one in the security or workflows unit, whose reference command exited 1 before any check ran. That cause is resolved, so all nine become ACCEPT on reproduced evidence. AR-15 stays ACCEPT_SCOPED.
- **15 FW** dispositions, ACCEPT_SCOPED. `current-source-map.proposed.md` is byte-identical across the delta, so no FW row's statement changed. No FW obligation is demonstrated or graded.
- **27 inherited residuals** (DR-001..011 + DR-011-R01..R16), carried unchanged; DR-012 is release qualification, not a 28th row.
- **30 evaluation subresiduals**, carried unchanged on byte-identity.
- **5 scoped review owners** DR-201..205, ACCEPT_SCOPED — routing preserved as AR-15 ownerRows, with no re-review outcome, no SATISFIED grade and no re-opening of historical acceptance.
- **32 qualification gates**, all false on all three boolean fields (`demonstrated`, `qualified`, `implementationHarnessAuthored`). None is demonstrated here and no historical preview grade is extended.
- **31 carried advisories** (v5..v11) present with original ids and original severities — none upgraded, downgraded, merged or dropped. v11-A1 correctly retains ADVISORY severity despite being substantively corrected.

D-371/D-372 describe one complete intended product implemented in stages — TS/JS/Rust on exactly four macOS/Linux machine IDs, with no implicit execution, untrusted ecosystem, bundled semantic model or full Map app. Central readiness and application remain intentionally unapplied.

## 13. New advisories (explicitly non-blocking)

**v12-A1** — `validation-summary.v1.json` reports the identity component as 767 without cross-referencing the distinct-id figure (757) that the subject itself records in `identity-check-counts.v12.json`. Nothing is misstated — 767 is the honest count of passing calls — and the subject does disclose the distinction in a dedicated file. A reader of the summary alone simply doesn't see the link. Continues the standing caution of v10-A3 and v11-A2 that a check count is not a coverage measure.

**v12-A2** — `reference-checks.json` records each command with an absolute *live-repository* script path, so the command as literally written would execute the live checker rather than the frozen one; reproducing against the frozen snapshot requires substituting the copy's paths. This did not impede reproduction — the checkers resolve their root from `__file__`, so running the copy's own scripts is fully self-contained, and each command's `sourceSha256` pins the intended checker unambiguously. Worth tidying before the blind and application gates, which consume frozen kits.

Neither affects the verdict. No patch text is proposed and no source edit was made.

## 14. Harness mistakes I made, corrected

Recorded as my errors, not subject defects:

1. **Exception identity.** My first law-limb run caught `AdmissionError` from a canonical module I had injected, but `identity-model.py` binds its *own* instance, so the class didn't match and the probe crashed instead of classifying the refusal. Re-bound to the model's own `C`. The model raised exactly the right error; my catch was wrong.
2. **Invented vocabulary.** Four of my cases used `retention='retained-blob'`, a value I made up. They refused with `RELATION_DIGEST_RETENTION` before reaching the limb under test — the model behaving correctly. Re-ran with the lawful `preimage`; all 18 then passed.
3. **A vacuous "identical" result.** My first identity harvest monkeypatched `identifier()` on a model object I had loaded, but `check-identity.py` loads its own instance, so nothing was captured. It reported 0 identities with the sha256 of the empty string for *both* candidates — a trivially "identical" result that proved nothing. I discarded it rather than reporting it as stability evidence, and replaced it with source-level instrumentation that captured 21,562 real computations per candidate. The vacuous result is used as evidence nowhere in this review.

## 15. Limitations

- Independent **design and reference** acceptance only — not reconstructability, readiness, application or product qualification.
- No implementation, commit, push, source edit, reset or clean. All writes confined to my output directory.
- All native, OS, compiler, crypto and storage observations remain **synthetic TCB assumptions**. Nothing was measured on real toolchains; no platform is qualified.
- The integration fixture's synthetic shared construction is **not an independent oracle**. I verified only that its declared source hash equals the applied checker (`f9b427a8…`) and that it is transitively pinned identically in all four ledgers. Agreement between fixture and checker is shared construction, not corroboration.
- I verified that applied bytes equal the released coauthor images and before-images equal frozen v11. I cannot verify from bytes alone the wall-clock **order** in which the root performed its steps, and my verdict does not depend on that narrative.
- Termination of local-reference traversal is confirmed; **no work-complexity bound** is claimed.
- The root's prospective `/tmp` application and finalizer tooling is outside this frozen design and was not reviewed. Final application review is a later separate gate.
- No subagents. No Codex assent, no blind consumer pass, no application review is performed or implied.

## 16. Required next acts

1. Actual Codex assent to these exact frozen bytes, carrying all 31 prior advisories plus v12-A1 and v12-A2.
2. A **new** fresh blind consumer B v3 on the accepted normative subset.
3. A complete, independently reviewed application, then readiness verification.

Readiness unchanged. Implementation not authorized. No product qualification. No application or blind acceptance.
