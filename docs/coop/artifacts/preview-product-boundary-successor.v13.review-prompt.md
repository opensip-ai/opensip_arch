# Independent review — preview-product-boundary-successor.v13

Independent, refute not confirm. **New subject after two Stage A rejections.**

**SUBJECT:** `docs/coop/artifacts/preview-product-boundary-successor.v13.json`
Expected sha256:
`fd571584e1d8596b279e26977b2dbf708dd900a069a5cc9b3151e6dfb0622f8f`
Mode 0444. If the subject moves, OBJECT / REJECT.

Two frozen, unrecorded, rejected predecessors stand between the current recording and this subject:
- `preview-product-boundary-successor.v11` `d25a7f29148b41e1e1991876c0f2ba549ef2d15834c2776feb52aeac97caf881` — REJECT / REJECT
- `preview-product-boundary-successor.v12` `2f31ca88e263cd93fd7b3bb97b18d6cecab87df87e661ac90575cfddca4643f9` — REJECT / REJECT

`preview-product-boundary-successor.v10` (`8f34c92ef4fb835ce31945bfc73e1442b38dada1d483380231a53d1d93a03483`, **D-295**) remains the current recorded DR-117 leftover remasurement. Do not treat any of the three as this subject.

**Findings this subject must land — all seventeen.** From v11: PPBSV11-B1, PPBSV11-B2, PPBSV11-B3, CLAUDE-PPBS-V11-B1, CLAUDE-PPBS-V11-B2, CLAUDE-PPBS-V11-SF1, CLAUDE-PPBS-V11-SF2, CLAUDE-PPBS-V11-ADV-1, CLAUDE-PPBS-V11-ADV-2, CLAUDE-PPBS-V11-ADV-3. From v12: PPBSV12-B1, CLAUDE-PPBS-V12-B1, CLAUDE-PPBS-V12-SF1, CLAUDE-PPBS-V12-ADV-1, CLAUDE-PPBS-V12-ADV-2, CLAUDE-PPBS-V12-ADV-3, CLAUDE-PPBS-V12-ADV-4. Each is disposed in `findingDisposition` with severity LANDED; check every one against these bytes rather than against its disposition sentence.

The v12 rejection was a single shared blocker: v12 pinned no predecessor record for v11 and disposed none of v11's findings, while claiming to pin every predecessor. This subject rebuilds the predecessor record from the frozen files on disk.

**WRITE ONLY:**
- Claude 2: `docs/coop/artifacts/preview-product-boundary-successor.v13.review-independent.claude2.json`
- Codex: `docs/coop/artifacts/preview-product-boundary-successor.v13.review-independent.codex.json`

Do not edit the subject. Do not commit. Do not edit file 08 or COORD.
Do not mark SATISFIED. Do not SATISFY DR-117. Do not perform D-056 Eligibility gate 4 or gate 5.
Do not re-perform, widen or re-open the D-316 Class A opening.
Do not reopen leftover-design of unnamed EE classes. Do not steal another row's leftover-design.
Do not name G13 into required-now. Do not invent fixture bytes or the DR-131 pack.
Do not change live required-now 28. Do not authorize implementation. Do not read the other reviewer.

HEAD `f7a98a70e650d0ed2639f815fa932bff21a99b83` (D-362 ADOPTED). Last heading D-362. Required-now 28.
COORD `bae06532b8417800414ee4fbdcd980135365185ce88b2244f92f6767412f264f`; file 08 `e503b75b5599444ee4d77c0c7d7c82a74026b2c1848ad214e0ac738c0aa40c3e`; file 02 `1811c682cf293e1e0b255be82c62f7ed3c439f0873eb7922bfb0ad965b43f7db`.

**Why this subject exists.** D-294 Decision 2 trigger (b) fires on live bytes: of the twelve leftover-joins `preview-product-boundary-successor.v10` cites as current, four are superseded and two of those changed their `leftoverDesign` partition. D-294 Decision 3 requires the refresh. This subject performs it, records the measured D-316 Class A standing, and carries the predecessor record for the two rejected intermediates.

**Heading spellings.** Forward `## D-NNN — Record <lineage>[- ]leftover-join.vN as …` and inverted `## D-NNN — Record leftover-join.vN of <GATE> as …`. A forward-only search silently returns a stale version for G21, G29, G30. Current: g29 v7 (D-343) `leftoverDesign` **[]**; g30 v10 (D-340) **[]**; g21 v45 (D-359); distribution-core v10 (D-308); g09 v12 (D-288), language-runtime v7 (D-274), g16 v5 (D-278), g23 v8 (D-240), permission v12 (D-283), monorepo v4 (D-277), language-quality v5 (D-273), doctor-actor v12 (D-285) unchanged.

**The grade question (D-005 form; top-level `gradeRuling`):** is this subject, as bytes, acceptable at application grade — T2-02's "application-grade acceptance with no express reservation"? Answer `"ruling"`, `"reservationSweep"`, `"reasons"`. A later SATISFIED-GRADE cycle is intended to rest on these bytes.

Attack:
- any of the seventeen findings is not fully landed, or a repair introduced a new defect
- the predecessor record is incomplete again: a frozen version of this lineage that exists on disk and is not pinned, or a reviewer finding identifier on disk that `findingDisposition` omits
- an identifier minted by this subject impersonates a reviewer finding, or a disposition claims a landing the bytes do not show
- **walk all fourteen classes**: any `leftoverDesign` assertion the named join's live bytes do not carry
- currency and partition site counts disagree per lineage, or `siteCount` disagrees with `sitesByReason`
- the `doesNot` union is not exactly the union of the twelve current joins' `leftoverDesign` arrays
- `classEqualityAssertion` is false under canonical JSON comparison of the normalized arrays
- a present-tense currency sentence names a superseded version, or a superseded version is unlabelled
- `basedOn.predecessorPinningShape` is contradicted by any object it describes
- any predecessor role sentence attributes to a frozen file content that file does not contain
- D-316 overstated (gate 4, gate 5, SATISFIED, this subject opening Class A) or understated
- the fourteen classes, seven dispositions or p1p2g3Mapping differ from v10's beyond the enumerated refresh
- carried text speaks in an earlier version's voice, or asserts as current something true only at an earlier dispatch
- `recordedInputs` pins a digest not matching live bytes, or omits a cited path
- deictic "This vN", bare version tokens, "byte-identical" claims about rewritten content, number/word disagreement
- SATISFIES DR-117, changes required-now 28, names G13, or authorizes docs/v2/implementation/

REJECT / OBJECT unless zero MUST-FIX and zero SHOULD-FIX.
Final chat: ACCEPT or REJECT.
