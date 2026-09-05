# Independent review — preview-product-boundary-successor.v14

Independent, refute not confirm. **New subject after three Stage A rejections.**

**SUBJECT:** `docs/coop/artifacts/preview-product-boundary-successor.v14.json`
Expected sha256:
`93a8e421234b7cd3f349953e37ba4f6fdaf51cb73706c5f3ceaa420033308ad1`
Mode 0444. If the subject moves, OBJECT / REJECT.

Three frozen, unrecorded, rejected predecessors stand between the current recording and this subject: `v11` `d25a7f29148b41e1e1991876c0f2ba549ef2d15834c2776feb52aeac97caf881`, `v12` `2f31ca88e263cd93fd7b3bb97b18d6cecab87df87e661ac90575cfddca4643f9`, `v13` `fd571584e1d8596b279e26977b2dbf708dd900a069a5cc9b3151e6dfb0622f8f` — each REJECT / REJECT. `preview-product-boundary-successor.v10` (`8f34c92ef4fb835ce31945bfc73e1442b38dada1d483380231a53d1d93a03483`, **D-295**) remains the current recorded DR-117 leftover remasurement.

**What changed, and why this is not another patch.** The v11, v12 and v13 rejections all had the same shape: a hand-written universal claim about the predecessor record that the bytes did not satisfy. v14 inverts that. `basedOn` is generated from a **census of every frozen version of this lineage on disk** — all thirteen — with each recording measured from COORD rather than assumed, and `basedOn.predecessorPinningShape` is **generated from the pinned objects**, so the description cannot outrun what is pinned. Every Stage A finding identifier discoverable on disk across the lineage (fifty-nine) is disposed, and the generator aborts if any is missing or carries empty disposition text.

**Findings this subject must land.** All thirteen from v13: PPBSV13-B1, PPBSV13-B2, PPBSV13-B3, PPBSV13-B4, PPBSV13-S1, PPBSV13-S2, CLAUDE-PPBS-V13-B1, CLAUDE-PPBS-V13-B2, CLAUDE-PPBS-V13-SF1, CLAUDE-PPBS-V13-ADV-1, CLAUDE-PPBS-V13-ADV-2, CLAUDE-PPBS-V13-ADV-3, CLAUDE-PPBS-V13-ADV-4 — plus the seventeen from v11 and v12, and the eight earlier identifiers v13 omitted. Check each against these bytes, not against its disposition sentence.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/preview-product-boundary-successor.v14.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/preview-product-boundary-successor.v14.review-independent.codex.json`

Do not edit the subject. Do not commit. Do not edit file 08 or COORD.
Do not mark SATISFIED. Do not SATISFY DR-117. Do not perform D-056 Eligibility gate 4 or gate 5.
Do not re-perform, widen or re-open the D-316 Class A opening.
Do not reopen leftover-design of unnamed EE classes. Do not steal another row's leftover-design.
Do not name G13 into required-now. Do not invent fixture bytes or the DR-131 pack.
Do not change live required-now 28. Do not authorize implementation. Do not read the other reviewer.

HEAD `f7a98a70e650d0ed2639f815fa932bff21a99b83` (D-362 ADOPTED). Last heading D-362. Required-now 28.
COORD `bae06532b8417800414ee4fbdcd980135365185ce88b2244f92f6767412f264f`; file 08 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`; file 02 `1811c682cf293e1e0b255be82c62f7ed3c439f0873eb7922bfb0ad965b43f7db`.

**Why this subject exists.** D-294 Decision 2 trigger (b) fires on live bytes: of the twelve leftover-joins `preview-product-boundary-successor.v10` cites as current, four are superseded and two of those changed their `leftoverDesign` partition. D-294 Decision 3 requires the refresh. This subject performs it, records the measured D-316 Class A standing, and carries the predecessor record.

**Heading spellings.** Forward `## D-NNN — Record <lineage>[- ]leftover-join.vN as …` and inverted `## D-NNN — Record leftover-join.vN of <GATE> as …`. A forward-only search silently returns a stale version for G21, G29, G30. Current: g29 v7 (D-343) `leftoverDesign` **[]**; g30 v10 (D-340) **[]**; g21 v45 (D-359); distribution-core v10 (D-308); g09 v12, language-runtime v7, g16 v5, g23 v8, permission v12, monorepo v4, language-quality v5, doctor-actor v12 unchanged.

**The grade question (D-005 form; top-level `gradeRuling`):** is this subject, as bytes, acceptable at application grade — T2-02's "application-grade acceptance with no express reservation"? Answer `"ruling"`, `"reservationSweep"`, `"reasons"`. A later SATISFIED-GRADE cycle is intended to rest on these bytes.

Attack:
- any of the thirteen v13 findings, or any earlier finding, is not landed, or a repair introduced a new defect
- **the generated pin-shape sentence is still false at any object it describes** — walk all thirteen predecessor objects against it
- a frozen version of this lineage on disk that is not pinned; a recording pinned that COORD does not state, or omitted where COORD states one
- a reviewer finding identifier on disk that `findingDisposition` omits, or a disposition claiming a landing the bytes do not show
- more than one version described as the immediate predecessor, or the wrong one
- an identifier minted by this subject impersonating a reviewer finding
- **walk all fourteen classes**: any `leftoverDesign` assertion the named join's live bytes do not carry
- currency and partition site counts disagree per lineage, or `siteCount` disagrees with `sitesByReason`
- the `doesNot` union is not exactly the union of the twelve current joins' `leftoverDesign` arrays; the do-not-record enumeration omits an unrecorded frozen version
- `classEqualityAssertion` false under canonical JSON comparison of the normalized arrays
- a present-tense currency sentence names a superseded version, or a superseded version is unlabelled
- D-316 overstated (gate 4, gate 5, SATISFIED, this subject opening Class A) or understated
- the fourteen classes, seven dispositions or p1p2g3Mapping differ from v10's beyond the enumerated refresh
- carried text speaks in an earlier version's voice, or asserts as current something true only at an earlier dispatch
- `recordedInputs` pins a digest not matching live bytes, or omits a cited path
- deictic "This vN", bare version tokens, "byte-identical" claims about rewritten content, number/word disagreement
- SATISFIES DR-117, changes required-now 28, names G13, or authorizes docs/v2/implementation/

REJECT / OBJECT unless zero MUST-FIX and zero SHOULD-FIX.
Final chat: ACCEPT or REJECT.
