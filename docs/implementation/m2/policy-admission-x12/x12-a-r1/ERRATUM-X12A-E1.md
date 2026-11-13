# Erratum X12A-E1: the empty-population exemption names two Runs, not one (author draft, 2026-11-13)

Status: **PROPOSED.** It records the lead's ruling on `LC/x12d-ts/fix-1/QUESTIONS.md`, section Q-RF2 (`LC` =
`/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`), and answers the cross-vendor code review's required
finding RF-2 (`LC/x12d-ts/review-codex-code/VERDICT.md`, point 5). It is **additive**: the bound bytes stay frozen. It
decides the points below and nothing else.

Corrects one bound record: **X12-A r7** (`docs/implementation/m2/policy-admission-x12/x12-a-r1/README.md`, 17,858 bytes,
sha256 `e4f44496b1cc45b2fd103cbea636124289e87b62f9338cf1c900803f8e7b8a2e`, architecture head `9687fd21b831ad5059d917d80f5ad92dc5426e42`,
bound on architecture main `8b09ee24935c623de9639ea74055fa2f7993de62`; subject manifest `x12-a-r1-subject.json`). Line
numbers below are those bytes' lines. The record it amends cites MC8 as `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r8.md`
(MC8; the accepted bytes, 183,744 bytes, sha256 `578c186ec9fc239f42d88713b8c31ec7085ab507251691f6cbba01e49b6607e1`).

## X12A-E1.1 The conflict (verified)

The code unit's four cycle replays (`LC/x12d-ts/fix-1/QUESTIONS.md`, Q-RF2) include `retained-typescript-acyclic`: a pass
Run with a live `typescript` file population and seven predicate proofs (the code review confirms it: "the committed
acyclic host Run is pass with seven predicate proofs", `review-codex-code/VERDICT.md`, point 5). r7 contradicts itself
about it:

- r7 needs a pass Run replayed. README:101-104: "The kinds the rulings name are a forged verdict on the pass Run and on
  the fail Run". README:87-89 lists "the pass base" among the cases of the replayed corpus.
- r7 forbids that Run as built. MC8:1101 (item 19 part 4): "The synthetic replay corpus ... moves onto
  `opensip.preview.typescript.pack:1`, with an empty `typescript` file population, so the rule evaluates nothing (I1:219)".
  r7 amends that line for one Run only: README:33-34 "for the one disposition (iii) Run only (A7)"; README:93-94
  "Selector 3 amends MC8:1101 for this Run only".
- The measurement that makes the two incompatible is the lead's ruling Q8 (`LC/x12d-ts/QUESTIONS.md`, "Lead rulings
  2026-11-12 on Q8-Q11"): "no empty-population release Run passes: `packet-2-original` comes out `indeterminate`,
  `no-covering-program`". So the pass Run that README:101-104 requires can only have a live population, and r7 did not
  carry Q8 into selector 3.

## X12A-E1.2 The amendments

**Item 1. Selector 3 and A7: two named Runs.** This **widens the amendment of MC8:1101 from one Run to two named Runs,
and to no other.** MC8:1101's requirement, "with an empty `typescript` file population", stands for every other Run.

README:33-34, old:

> 3. MC8:1101 (item 19 part 4), "with an empty `typescript` file population, so the rule evaluates nothing", for the one
>    disposition (iii) Run only (A7).

read as:

> 3. MC8:1101 (item 19 part 4), "with an empty `typescript` file population, so the rule evaluates nothing", for two
>    named Runs only: the disposition (iii) fail Run and the pass Run `retained-typescript-acyclic` (live `typescript`
>    file population, pass, seven predicate proofs) (A7; erratum X12A-E1).

README:93-94, old: "Selector 3 amends MC8:1101 for this Run only, because a Run that exists to carry a finding cannot carry
one with an empty population." Read as: "Selector 3 amends MC8:1101 for this Run and for the pass Run
`retained-typescript-acyclic` only (erratum X12A-E1), because a Run that exists to carry a finding cannot carry one with an
empty population."

**Item 2. A9's enumerated edits.** The population edit names the pass Run's population beside the (iii) Run's, and nothing
else.

README:140, old: "For the (iii) Run the population is also covered." Read as: "For the (iii) Run and for
`retained-typescript-acyclic` the population is also covered."

README:142-143, old: "and the per-disposition population edits (the (iii) Run's population)". Read as: "and the
per-disposition population edits (the population of the (iii) Run and of `retained-typescript-acyclic`)".

The rest of README:137-146 (identity-normalized comparison, preserved budget, capability, configuration and grant values)
is unchanged.

**Item 3. The two indeterminate cycle cases take (iv), with no exemption.** `retained-typescript-file-partial` and
`retained-typescript-symbol-partial-optional` are not exempted from MC8:1101. They take disposition (iv) (README:96-100):
a named derive-level test asserts their evaluation content against the stored outputs, as COMP does, and they leave the
replayed corpus. The record's disclosed limit (README:115-117) gains this sentence after its current text:

> The two indeterminate cycle cases `retained-typescript-file-partial` and `retained-typescript-symbol-partial-optional`
> are covered at the derive level only (disposition (iv)). Replay no longer shows the `incomplete-inventory` and
> `population-unknown` indeterminate reasons through the evaluator's own replay, and the unit's handoff and the milestone
> disclosure state this.

**Item 4. Controls.** README:172-174 ends "also A4's pin, the reviewed coverage map, the (iii) control and A9's diff
control." Two controls are added to that list:
- The corpus check refuses any replayed Run with a live `typescript` population other than the two named Runs.
- The forged-verdict cases exist on both named Runs. Each is compared with its base Run so that only the one forged
  claimed output differs (README:101-103: "built by forging one claimed output of a release-pack Run, so the mismatch is the
  only thing wrong").

**Item 5. "The pass base" in disposition (i): an amendment, not a note.** README:87-89 says: "**(i) Structure:**
regenerated onto the release pack with an empty `typescript` population (MC8:1101). This covers the seal-corpus Run, the
synthetic's source, the pass base, and cases whose test checks replay, admission, commit, bounds or member removal." It
cannot be read as a note without contradiction: the sentence gives (i) an empty population and lists the pass base under
it, while the pass base is the named Run `retained-typescript-acyclic`, which has a live population and is exempt under item
1. No empty-population pass Run exists (lead ruling Q8, measured: `packet-2-original` comes out `indeterminate`,
`no-covering-program`). So (i) covers the structure Runs that are not pass.

README:87-89, old text as quoted above. Read as:

> - **(i) Structure:** regenerated onto the release pack with an empty `typescript` population (MC8:1101). This covers
>   the seal-corpus Run, the synthetic's source, and cases whose test checks replay, admission, commit, bounds or member
>   removal. The pass base is not an (i) Run: it is `retained-typescript-acyclic`, with its live population, exempt under
>   selector 3 as widened by erratum X12A-E1.

## X12A-E1.3 What this does not change

- MC8:1101 itself, and its requirement for every Run other than the two named.
- The (iii) Run, its control ("its finding is produced by the release rule over its retained facts, not typed into a
  fixture", README:95) and the other dispositions, the boundary (README:111-114), A8's pack provenance, the forged-case
  rule (README:101-107), and the RF-1 text of A9 apart from the population words above.
- The existing disclosed limit about `selected-nongating-live-findings` (README:115-117), which stays as written.
- The coverage map `COVERAGE-MAP-C1.md` (not in this record).
- No product code, fixture, test, lane or qualification is accepted here.

## X12A-E1.4 Open points

None. The point raised by the first draft (README:87-89) is closed by item 5.

## X12A-E1.5 Review and binding owed

- **Review: two independent reviewers** (the lead's ruling).
- **Code resting on it (at risk until this binds):** on product branch `x12d-ts-r1`, the pass replay and the
  forged-verdict-on-pass case, marked `[AT RISK: X12A-E1]`; and the removal of the two indeterminate cycle cases from
  `CYCLE_CASES` and the regenerated cycle fixture under (iv).
- **Binding owed:** the lead's receipt `ADOPTION-X12A-E1.md` pinning this file's sha256. No design-lock entry.
