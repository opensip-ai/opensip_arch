# Independent review — frozen candidate v19

**Subject manifest SHA-256** `312db9d904d0ec1f9c91d84137feb3277490b79b07bf3a6d5efc0380caa0f24b`
**Verdict: ACCEPT** — of the frozen v19 **source bytes only**.
**Reviewer:** actual Claude, fresh and independent. Not a source coauthor (`4b48ccdd`, `f8404b42`), not the prior independent review (`87a6bcea`), not the blind (`e6448709`).

This is not a blind review, not an application, not a readiness reconciliation and not product qualification. A **new blind consumer** on these bytes and a **complete, separately independently reviewed application** remain required. I do not claim their agreement.

## Custody

I rehashed the manifest and got the declared value. I verified all **8,653 files / 628,224,694 bytes** before and after my work: zero missing, zero hash mismatches, zero length mismatches, zero extras. I verified **60 declared references** — the `final-source-account.v19` files, four coauthor handoffs, four root coauthor assessments, the prior independent review, prior root assessment, predecessor manifest, latest blind clarification, the withdrawal evidence and its root assessment, and every `sourceDelta` after-hash plus each source proposal's byte-equality with the final. Zero mismatched.

All four pin ledgers verify: foundation 1100, security 74, **native 72 including the new `protocol3-transitions.v1.json` runtime table**, workflows 66 — 1,312 rows, zero mismatches. All writes are confined to my own directory.

## Reference checks

I reproduced the six canonical commands in a **disposable full exact copy**, without repinning. All six exit 0, matching their declared exits, with source hashes matching. The **actual source-copy delta is zero, before and after every probe I ran**: the six commands regenerate every report byte-identically, so the retained report bytes are exactly what the retained sources produce.

The declared 11-path `sourceDelta` is a subset of the 23 changed paths I computed from the two manifests. I accounted for the other twelve: six generated reports (which my own runs reproduce), the four pin ledgers, the crosswalk (routing only), `README.md` (a prepended v19 header preserving prior text as history), and `NEXT-REVIEW.md`. Of 789 additions, 786 are retained evidence under `reviews/`; the three outside are the historical-preservation report, the v19 dispositions, and the new normative table. Two product contracts changed — `native-evidence.md` and `workflows-and-surfaces.md`; the other four and the index are byte-identical.

## My own controls

**192 controls across eight sets, zero failures**, authored fresh for this review and run against these bytes.

### 1. TS closed-suffix clone scope (CB7-MUST-1) — resolved

The law is **read from its owning registry**, not restated: the module value equals `scopeCapabilityLaw`, and no suffix→`sourceVariant` pair appears anywhere in either executable model. Longest-match selection is right, including `.d.ts → ts-declaration` (never `ts`).

The counterexample that opened the finding — a `clones` scope over `package.json` under the TypeScript universe — now yields the **existing** `language-tier-unsupported` / `capability-missing` pair: no new deficiency, cause, or public detail code. Empty `source-path` scopes are unsupported rather than vacuously complete; mixed scopes disclose in either order; every supported TS/JS variant including declaration suffixes stays eligible for `complete`; all three inventory capabilities are ungated even on unlisted suffixes and empty scopes. Rust's ownership form has no suffix table, so this law does not own it and `BODY_LANGUAGE_OWNER_NOT_COMPILED` is untouched.

**Optional context cannot bypass the final authority.** The producer-boundary application is conditional on the caller supplying `universe_dialect` — disclosed in both the code and the published `guardOrder`. The final authority is not conditional: `coverage_source_variant_prerequisite` is called unconditionally at `identity-model.py:1560` inside `close_run`, and the dialect it reads comes from the **retained universe record** (`:1545-1546`), never from the payload. A provider cannot switch its own capability on by asserting a flag.

**Actual first refusal and precedence.** I read the control flow rather than the prose. `close_run` runs producer admission at `:1547` *before* its own prerequisites, so a false `complete` refuses there as `native.coverage-source-variant-unsupported-complete`. Among closure's prerequisites the order is ownership → syntax grammar capability → this backstop, so a syntax violation keeps its own name. That is an intentional, published precedence change, and the grammar law is neither weakened nor reordered.

### 2. Prospective Plan cardinality (CB7-SHOULD-2) — resolved

Bounds are read from the schema (128/128/256) and `PLAN_SELECTION_FIELDS` equals the `$defs/plan` declaration order. At limit+1 each field reaches `PROJECT.SCOPE_LIMIT` with subject `{field,count,limit}`, `request-rejected` / `REQUEST.UNSATISFIABLE` / exit 2, and its **own** narrowing remedy — three distinct sentences. Exactly-at-limit, below-limit and empty arrays are admitted.

**Array-only cardinality holds.** A 500-character string, a 500-key dict, `null`, bool, int, float and a tuple all pass through as the *same object*; length-of-a-string is never reported as a member count. An in-bound array of wrong element types is the schema's; an over-bound one still refuses on cardinality.

**Precedence** is the fixed declaration order: all three oversized → `semanticClosures`; closures in bound → `nativeContextDigests`; Python insertion order is irrelevant; an earlier field of the *wrong type* does not mask a later breach.

**This is actual invocation wiring, not an orphan helper.** The guard sits inline in the prospective Plan construction at `integration-fixtures.py:725` and `check-identity.py:770`, immediately before `add('plan',…)`, so a refusal structurally precedes minting. Driving the owning checker's real `build()` with 257 `importIds` refuses `importIds:257>256`, exit 2, returning **no Plan and no Run**; 256 still closes a Run. The producer boundary refuses 129 *distinct* contexts before any prospective Plan exists, admits exactly 128, and collapses 129 identical descriptors to one. An ordinary invocation before and after the refusal is **byte-identical** — earlier committed outcomes are preserved. A retained oversized Plan refuses on the **schema** route; the pre-Plan boundary appears nowhere in `identity-model.py`, so retained closure cannot take the request route.

### 3. Published provider transition table — resolved

The discriminating test of "directly consumable" is whether the document alone suffices. **I wrote an independent interpreter from the published laws only** — `initializationAndUpdateOrder`, `matchLaw`, `preMatchLaw`, `noMatchLaw`, `guardLaw`, `stateUpdates`, `stageDependentTransitions`, `terminalLaw` — and it reproduces `protocol3_run` **exactly on all 423 cases**: four mode combinations, multi-stage `CoverageV3` resolution and one-stage-short, all five terminal kinds, every process fault, FAULT absorption, post-terminal frames, unknown and out-of-order frames, and 400 seeded fuzz sequences.

34 ordered rows `P3-01..P3-34`, 22 phases, the exact nine-field `initialState`, `*PRE_COMPLETE` equal to its published derivation `phases[1:17]`. The model **reads** the artifact — no `P3-xx` row literal remains in it. I proved pairwise disjointness myself (zero overlapping pairs), and 25 random row permutations preserve every outcome, confirming that position resolves no ambiguity today while first-match remains the declared normative rule.

**No silently altered transition behaviour:** I exec'd the pre-v19 inline table out of `source-before-v19` — rows, phases, the `[1:17]` derivation, the process-fault set and the now-derived `_SOURCE_FRAMES` are all byte-equal to the pre-v19 values.

One honest limit: my interpreter takes `IDENTITY_TOKENS` from the model, because the document declares the identity token set prose-owned. That is a declared division, not a gap — but a kit reader needs the contract prose as well as the table.

### 4. Workflow S6 repair projection — resolved

The decisive fact is that the repair preview emission body is **byte-identical to pre-v19**; the only v19 change to the workflow model is a five-line subject copy. The S6 paragraph therefore **broadens published meaning to match unchanged model behaviour** and asserts no new behaviour.

Per-requirement emission is **mandatory** — `if not req['satisfied']` emits unconditionally, no flag and no option — so schema-only permissiveness is *not* normative optionality: an unsatisfied requirement with empty `unmetPreconditions` is decided non-conforming at admission. Exactly two routes reach the one **existing** `REPAIR.EVIDENCE_RUN_UNAVAILABLE` code, and the emitted code set is identical to pre-v19; no per-deficiency code is minted, and `EvidenceRequirement.deficiency` remains the typed cause carrier. The **retention** remedy names Run-level restoration and carries no `relation`, `minResolution`, plane or deficiency; the **per-requirement** remedy names all four — cause fields are required only on that entry. Authoritative applicability and the exact authorization binding are preserved: any edit mints a different `repairPlanId` that no authorization names.

The subject projection copies by **presence**, not truthiness: absent yields byte-identical pre-v19 output, an explicit empty string is preserved, and I confirmed the root's correction over the narrower coauthor claim — `False`, `0`, `[]`, `{}` are preserved too. The subject is copied, never admitted; a 2000-character subject and each falsey shape are refused by the schema.

**CB7-SHOULD-1 is withdrawn**, retracted in full by the original reviewer. I confirmed the premise unfounded against the bytes: the deficiency is admitted separately and projected into the *remedy*; no deficiency value is ever minted as a code. This is **not** original blind acceptance of v19 and **not** a revival of the eleven-new-code premise; the clarification itself says it cannot accept a future source fix.

## Advisories, re-measured independently

I measured all five myself rather than accepting their numbers. **ADV-1**: the inherited enum has 11 members and the successor 12 — exactly one addition, `host-invariant`, no removals. This confirms the 11→12 comparison the blind's own clarification had already corrected to; the original "10→12" mixed a non-`none` count with a total. **ADV-2**: 93×11 = 1023 (one row *under* 1024, not at it), 94×11 = 1034; the typed refusal is real. **ADV-3**: 8 registry members, four selected, disclosed as deliberately broader, bound only at `ProviderCapability.platformIds[]`. **ADV-4** is the one v19 acts on. **ADV-5**: pinned at UCD 15.0.0, with the contract stating the limitation itself.

## New advisories (no new MUST or SHOULD)

**CX-CL19-ADV-1 — the table is kit-shaped, but nothing binds it into the next kit.** The artifact is a self-contained `.json` in `native/`, the same class the retained blind kit already carries, and my interpreter proves it sufficient. But kits are assembled per pass and no v19 record declares the composition rule. Not a finding — no byte is wrong — but blind 8's kit must include it or ADV-4 recurs verbatim.

**CX-CL19-ADV-2 — the `_SOURCE_FRAMES` drift control is tautological.** The model derives the set as the union of `stateUpdates[].onFrames`, and the published control asserts that same expression equals the model value. Today's derived set is provably correct (byte-equal to the pre-v19 literal), but "plural `onFrames` means `sourceBytesSent`" is a convention, not an asserted law: a future entry using the plural form for another purpose would silently widen the observable that proves no source byte preceded negotiation, while the control still passed. Advisory, not a finding — no counterexample exists in these bytes.

## Governance groups — routing only

For all **16 AR**, **15 FW**, **27 inherited residual**, **30 evaluation** and **5 scoped-owner** rows I assessed routing and byte-preservation only. `appliedByThisReview` and `finalApplicationOutcomeGranted` are **false on every row, including all five DR-201..205**. Carry-forward and routing are not a fresh substantive readiness grade.

The owning documents for FW, inherited, evaluation, the scoped-owner register and the gates are all **byte-identical v18→v19**. The crosswalk did change, so I diffed it leaf-by-leaf: 64 changed leaves are exactly the 16 rows' review pointers, 96 added leaves are appended history, zero removals, and **zero structural leaves** — obligation, selector, owner, unit, contract, status, id and `ownerRows` are all unchanged.

**All 32 gates remain unperformed**: I read the file directly — every row carries `demonstrated=false`, `qualified=false`, `implementationHarnessAuthored=false`. I performed none. **D-372 is unapplied and Condition 5 is NOT MET**: the README still states it, the register is byte-identical with its Condition 5 sentence intact, and nothing in v19 or in this review applies it.

## What I executed, and what I did not

I executed the reference models and checkers in a disposable copy. I executed **no** compiler, parser, provider, cargo, OS, repository or product host. Every TCB and provider observation in these suites remains an explicit synthetic trusted input. I do not report my literal and schema observations as executed security, host or compiler enforcement, nor as fully admitted product Runs. All counts here are calls or cases executed — never qualification.

Nine defects in **my own controls** are retained. Three were matcher errors (object identity across module instances, a `jsx` collision with the tsconfig option name, a wrong accessor form), two were shape or path errors, two were fragile string tests, and one — F1/F3 — measured *empty* because I searched the wrong files, which would have been a false negative of my own making. The most consequential is FA-9: my first reading of the producer-boundary call sites would have raised an advisory about a docstring, until I found `check-identity.py:2677`, the owning unit's own producer-boundary control, which *does* supply the dialect. I withdrew the observation rather than publish it.

## Judgment

The four changed laws hold on these exact bytes, and they hold under controls I designed to break them rather than to confirm them. The clone-scope gap that blind 7 found is closed at a boundary a caller cannot bypass, using vocabulary that already existed, with the Rust and syntax universes' own laws left intact. The Plan limits reach a real typed refusal at real invocation, mint nothing for the refused step, and leave earlier outcomes untouched — and the array-only rule keeps cardinality from stealing shapes the schema describes better. The transition table is genuinely reconstructable from its own document, and byte-for-byte the same machine as before. The repair paragraph documents behaviour that did not change, which is exactly what a meaning-broadening correction should look like.

The corrections that impressed me most are the ones that made claims *weaker*: retracting "names no field, count or limit" once jsonschema's structured fields were checked, and narrowing the context-identity claim from a compiler closure to the whole descriptor. Those are the moves of authors testing themselves. I found no MUST and no SHOULD. My two advisories are about a control's discriminating power and a future assembly act, not about anything wrong in these bytes.

I accept these source bytes. I accept nothing else: no readiness, no qualification, no implementation authorization, and neither the blind's nor the application's agreement, which do not exist yet and are not mine to give.
