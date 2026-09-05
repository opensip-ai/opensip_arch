# Review prompts — v1.9 and v7

Two independent reviews. Dispatch them to **separate agents**; neither may review both.
Both subjects were quiescent and unwritten-to when these digests were taken.

Working directory for both: `/Users/sb/code/opensip-ai/opensip/docs/coop`

---

## PROMPT 1 — `r1-lifetime-neutrality.conformance.v1.9`

You are an INDEPENDENT REVIEWER. You did not author the subject and you owe it nothing. Work in `/Users/sb/code/opensip-ai/opensip/docs/coop`.

**SUBJECT, FROZEN AT DISPATCH:** `artifacts/r1-lifetime-neutrality.conformance.v1.9.json`, sha256 `37897be0cca011e8…` (verify the full digest yourself). Measure it at start AND at end. If it moved, record that and bind your verdict to the START bytes — do NOT re-baseline. Subject drift has happened three times in this corpus.

**WRITE YOUR VERDICT TO:** `artifacts/r1-lifetime-neutrality.conformance.v1.9.review-independent.json`. Write NOTHING else. Never edit an existing file.

**WHAT v1.9 IS.** A 1-operation derivation clearing the three blockers raised against `v1.8`. Chain: `v1.9 → v1.8 → v1.7 → v1.6`. **`v1.6` is the full-text standalone and the resolution TERMINUS.** v1.9, v1.8 and v1.7 are DELTAS; their own bytes are not the artifact.

**THE SINGLE MOST IMPORTANT INSTRUCTION.** Resolve FULL-CHAIN before measuring anything (freeze §7.3 / `CMP-IR-01`). This corpus has committed the flat-read error five times, including three times by competent parties who knew the rule:
- A coordinator grepped `retention-tiers.v28`'s bytes for `PURGED`, got 0, and concluded the applied head lacked purge semantics. Resolved, it has 62.
- A reviewer counted `driftDisclosure` in a DELTA file (0), concluded the successor had dropped a protection block, and raised an advisory. Resolved, it is present at 2 — identical to the predecessor. The advisory was withdrawn in full.
- A flat grep of `v1.8` for `OPEN-DEP-FI-02` returns 0 because the delta writes the range form `…-01..07`; resolved, it is present at 2 leaves.

Detect derivations by **VALUE SHAPE at any depth** (an operations array of `{op,path}` records plus a sibling `sha256` pin), NEVER by key name: a key-name search for `derivedFrom` in v1.6 returns a FALSE hit at `$.policyDerivationIdentity.orderingRuling.planStageIds.derivedFrom`, a string-valued provenance citation. Publish a negative control proving your detector fires where it should.

**WHAT THE THREE BLOCKERS WERE, AND WHAT TO TEST.**

**Blocker 1 — `classSize: 59` was unrecomputable.** v1.8's predicate turned on "a WORD-numeral" with no published vocabulary; six defensible readings gave 62–70, never 59. v1.9 publishes the vocabulary: exactly twelve tokens `one two three four five six seven eight nine ten eleven twelve`, case-insensitive, word-bounded, `bool` tested before `int`. **Test whether the published rule is now sufficient to recompute every figure v1.9 states.** If any figure still cannot be reproduced from the published definition, that is a blocker — the freeze's standing rule is *"a figure without its definition is not a measurement, however true it is."*

**Blocker 2 — the derived class missed the class it exists to derive.** v1.8's key-name predicate caught 5 of 41 leaves in `$.measuredSelfReport`, and — the sharpest instance — MISSED `componentFrameOccurrencesInEP8` while CATCHING its misnamed twin, because that key contains "Measured". **Renaming a leaf honestly removed it from the class.**

v1.9 changes the BASIS to value shape + structural position, with key name ADDITIVE ONLY. It publishes: stage 1 (shape+position) = 867, excluded as DATA = 481, added back by key name = 31, CLASS = 898; `measuredSelfReport` coverage 37 of 41, with the four exclusions named as two type-name lists and one prose line.

**Recompute all of it.** Then attack it: find a self-measurement in the resolved value that the new basis still misses. v1.9 states its own honest bound — 898 members are derived and recomputable but NOT individually verified. Judge whether that bound is stated honestly or used as cover.

**Blocker 3 — a self-invalidating measurement.** v1.8 published *"this artifact's own bytes contain `componentFrame` 8 times"*: true of the resolved predecessor (8), false of the resolved successor (11), because the sentence itself names the token 3 more times. `11 − 8 = 3`. v1.9's single operation WITHDRAWS the self-count rather than restating it, arguing no value survives its own publication. **Judge whether withdrawal is correct or an evasion** — the alternative was a fixed point recomputed with itself included. Freeze §7.2.2.1(a) item 4 records the rule: when the measurer is inside the measured, publish the boundary.

**WHAT MUST NOT HAVE MOVED.** v1.9 claims `digestsMoved: 0` and that no design decision changed. The v1.8 review confirmed 209 digest leaves with 0 changed and that B-R17-01 is genuinely repaired (5 distinct `findingId` literals at 79 bytes, 57 Digests at 71, 4096/79 = 51.8481, superseded "about 57x" = 4096/71 exactly). Verify none of that regressed. `OPEN-DEP-FI-01..07` must still be open and stated.

**TRAPS THIS CORPUS HAS ACTUALLY SPRUNG.**
- **ENCODING**: word-numerals. A digit-only sweep misses "seventeen", "thirty". Roughly 4× more word-numerals than integer leaves in some artifacts.
- **SCOPING**: key name versus referent — the exact subject of blocker 2.
- **AUTHORSHIP**: carried versus authored; a measurement inherited unchanged through a delta is blind to a repair promised and not made.
- **The vacuous caveat** (freeze §7.2.2.1): a DISCLOSED LIMITATION can be false. Reviewers hunt overclaims and pass over concessions — one false caveat survived FOUR independent reviews. **Recompute limitations, not just claims, including v1.9's own.**
- **The self-invalidating measurement** (freeze §7.2.2.1(a) item 4) — check v1.9 does not commit it while repairing it.
- Test `bool` before `int` (`bool` subclasses `int`). Parse with a duplicate-key-rejecting `object_pairs_hook`. Invoke corpus checkers as `python3 -I -B`.
- §7.7: FOLD markdown before concluding a quotation ABSENT — seven freeze phrases return ABSENT byte-literally and FOUND only after folding.
- §7.8: a green checker run is AUTHOR-SIDE evidence only. `check-r1-v1.7.py` is the retained checker for **v1.6**, not for this lineage — the version number is the checker's own. This candidate has no retained instrument.

**ENVIRONMENT** (§7.2 — your verdict binds bytes AND an environment). Measure `IMPLEMENTATION-FREEZE.md` and `artifacts/claim-register.v1.json` yourself at review time and record both digests. The freeze moved repeatedly on 2026-08-12; resolve any freeze-dependent claim at the digest you measured and disclose it. §7.8.1: an input that moved after authoring must NEVER present as a finding about the artifact.

**OUTPUT:** strict JSON — `verdict`, `blockers`, `advisories`, `whatIDidNotCheck` (specific and honest; prior reviewers' candour here was their most useful output), `recordedInputs` with digests, `environment`. Score by FINDING-SET DELTA, never exit code. Final message: a concise summary for the coordinator, not the JSON.

---

## PROMPT 2 — `evidence-identity-recipes.v7`

You are an INDEPENDENT REVIEWER. You did not author the subject and you owe it nothing. Work in `/Users/sb/code/opensip-ai/opensip/docs/coop`.

**SUBJECT, FROZEN AT DISPATCH:** `artifacts/evidence-identity-recipes.v7.json`, sha256 `81b67bfeed69485b…` (verify the full digest yourself). Measure at start AND end; on drift, bind to the START bytes.

**WRITE YOUR VERDICT TO:** `artifacts/evidence-identity-recipes.v7.review-independent.json`. Nothing else. Never edit an existing file.

**WHAT v7 IS.** A 1-operation derivation from `evidence-identity-recipes.v6.json` (APPLIED 2026-08-12, `bed154dce8b49c1c…`). Chain `v7 → v6 → v5`; **`v5` is the standalone TERMINUS.** Resolve FULL-CHAIN before measuring (freeze §7.3 / `CMP-IR-01`). Detect derivations by value shape, never key name.

**WHY v7 EXISTS — and it is the interesting part.** Blocker `B-EIR5-02` instructed *"strike 'which differ above the BMP' at both sites"* — scoped to the false CLAUSE. But the defect is the VACUITY: naming two spellings of ONE total order as though they could differ. `v5` carries **three** vacuity-bearing sites and **two** clause-bearing ones. `v6` repaired exactly the two and was APPLIED still carrying the third. Two independent reviewers disagreed on whether v6 was complete and **both were right** — one counted clause-bearing sites, the other vacuity-bearing sites.

v7 repairs the third, `$.declaredUnresolvedDependencies.entries[4].reproductionStatusInV5`, and claims to have scoped the repair by deriving the vacuity class over the RESOLVED v6 rather than grepping the clause.

**VERIFY THE CENTRAL FACT YOURSELF, EXHAUSTIVELY.** Over all valid Unicode scalars (0x0000–0x10FFFF excluding surrogates D800–DFFF, = 1,112,064), does UTF-8 byte order ever disagree with scalar-value order? Adjacent pairs settle order equality on a totally ordered set. Repeat at the string level with mixed-plane strings, and repeat for UTF-16. v7 claims 0 UTF-8 inversions and exactly 1 UTF-16 adjacent inversion at U+FFFF/U+10000. Reproduce the settling vector: keys U+E000 and U+10000 — scalar/UTF-8 emit U+E000 first, UTF-16 emits U+10000 first because the surrogate pair opens 0xD800 < 0xE000.

**THEN TEST THE SCOPING CLAIM, which is what v7 is really asserting.** v7 publishes its predicate and claims exactly 1 vacuity-bearing leaf was live in the applied head and 0 remain after the repair. **Derive the class yourself, by your own predicate, and see whether you find a fourth site.** A reviewer who greps for the clause will certify a repair that left the defect standing — that is precisely how v6 shipped incomplete. This is the highest-value thing you can do.

**WHAT MUST NOT HAVE MOVED.** v7 claims `digestsMoved: 0` and `recipesChanged: 0`. v5's cryptography survived 275 independent assertions with 0 failures — all four commissioned pins reproduced from first principles, `outcomeSetCommitment == outcomeSetDigest` confirmed on three measured legs, and F-1 survived chosen-sibling non-membership, fabricated promoted-leaf path, extra step, cross-tree and internal-node impersonation attacks. Verify v7 broke none of it. Any change to a recipe, commissioned pin or golden vector is a blocker.

**SCOPE — judge both directions.** v7 states it does NOT repair v1–v4 or v2's review (reviewed bytes keep the sentence permanently, §7.2/§7.6), does NOT close `UR-1` (it belongs to the canonical-JSON profile's owning surface, §6 law 19), does NOT reach `evidence-identity-recipes.v1.review-independent.json` — which carries the claim in a VARIANT SPELLING containing `above the BMP` **zero** times and uniquely ENDORSES it (*"is correct and I did not narrow it"*) — and does NOT confirm RFC 8785's UTF-16 ordering against a primary source. **Verify each disclaimer is honest and that v7 does not overreach**: it binds nothing, so any language that decides, seals or closes something is a blocker.

**One open item you may be able to close:** nobody in this corpus has yet confirmed RFC 8785 JCS's UTF-16 key ordering against a primary source. It is load-bearing for the exposure argument against applied `delivery.v4`, whose release-manifest canonicalisation is defined as sha256 over JCS. If you can confirm or refute it from the RFC text, say so explicitly.

**TRAPS.** The vacuous caveat (a false disclosed limitation reads as candour and survived four reviews — recompute limitations, including v7's own); SCOPING (a file MENTIONING scalar order is not one CARRYING the claim — classify by reading sentences; nine spelling variants exist); ENCODING (word-numerals defeat digit-only sweeps); the flat read. Test `bool` before `int`; duplicate-key-rejecting `object_pairs_hook`; checkers as `python3 -I -B`; §7.7 folding before concluding ABSENT.

**ENVIRONMENT** (§7.2). Measure `IMPLEMENTATION-FREEZE.md` and `artifacts/claim-register.v1.json` yourself and record both. Freeze §7.2.2.1 and §7.2.2.1(a)–(b) contain the coordinator's own record of this defect — **do not check the artifact against that record; recompute independently and then compare artifact, freeze and your own measurement, reporting any disagreement as a finding.** Two reviewers have already produced different totals from the same tree, both correct under different scopings. §7.8.1: an input that moved after authoring must never present as a finding about the artifact.

**OUTPUT:** strict JSON — `verdict`, `blockers`, `advisories`, `whatIDidNotCheck`, `recordedInputs` with digests, `environment`. Score by FINDING-SET DELTA, never exit code. Final message: a concise summary for the coordinator, not the JSON.
