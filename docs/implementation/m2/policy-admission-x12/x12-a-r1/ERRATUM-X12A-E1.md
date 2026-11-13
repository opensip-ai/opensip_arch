# Erratum X12A-E1: the empty-population exemption names four lawful base evaluations, not one (author draft, 2026-11-13)

Status: **PROPOSED.** It records the lead's ruling on `LC/x12d-ts/fix-1/QUESTIONS.md`, section Q-RF2 (`LC` =
`/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25`), and answers the cross-vendor code review's required
finding RF-2 (`LC/x12d-ts/review-codex-code/VERDICT.md`, point 5). It is **additive**: the bound bytes stay frozen. It
decides the points below and nothing else. It also records the lead's corrected ruling on the same file's section
Q-RF2-GOLDEN, option (c): the two indeterminate cycle cases stay replayed and are named bases too.

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

**Item 1. Selector 3 and A7: four named lawful base evaluations.** This **widens the amendment of MC8:1101 from one Run to
four named lawful base evaluations, and to no other lawful base evaluation:** the (iii) fail Run, the (iii-p) pass Run
`retained-typescript-acyclic`, and the two indeterminate cycle cases `retained-typescript-file-partial` (iii-f) and
`retained-typescript-symbol-partial-optional` (iii-s) (items 3 and 5). MC8:1101's requirement, "with an empty `typescript`
file population", stands for every other lawful base evaluation. Only those four may have a live population.
The required forged-output negatives (README:101-107) are not further exemptions and are not further bases: each reuses
exactly one base's retained Plan, population and other evaluation inputs, changing only the specified claimed output and
its dependent identities and carriers (a changed claimed output re-identifies the evidence, seal and Run). Its base is
either one of the named live-population lawful base evaluations or a disposition (i) empty-population Run, as
README:101-107 assigns each forging kind; it keeps that base's population, so only the four named bases, and negatives
reusing exactly their inputs, have a live `typescript` population. Each negative is compared with its base (item 4). No
additional lawful base, input shape or population edit is authorized. This applies to all retained forged-output kinds
(README:101-107), not only the two verdict cases. Of the kinds README:101-104 names: the forged verdict on the pass Run
sits on the (iii-p) base; the forged verdict on the fail Run and the forged finding on the fail Run sit on the (iii) base;
forged deficiencies sit on an (i) empty-population Run (Q8 measured `packet-2-original` as `indeterminate` with a rule
deficiency); any further expressible kind sits on whichever of those base classes the coverage map assigns it.

README:33-34, old:

> 3. MC8:1101 (item 19 part 4), "with an empty `typescript` file population, so the rule evaluates nothing", for the one
>    disposition (iii) Run only (A7).

read as:

> 3. MC8:1101 (item 19 part 4), "with an empty `typescript` file population, so the rule evaluates nothing", for four
>    named lawful base evaluations only: the disposition (iii) fail Run, the disposition (iii-p) pass Run
>    `retained-typescript-acyclic` (live `typescript` file population, pass, seven predicate proofs), and the disposition
>    (iii-f) and (iii-s) indeterminate Runs `retained-typescript-file-partial` and
>    `retained-typescript-symbol-partial-optional` (A7; erratum X12A-E1).

README:93-94, old: "Selector 3 amends MC8:1101 for this Run only, because a Run that exists to carry a finding cannot carry
one with an empty population." Read as: "Selector 3 amends MC8:1101 for this Run and for the (iii-p), (iii-f) and (iii-s) Runs only, as
lawful base evaluations (erratum X12A-E1), because a Run that exists to carry a finding cannot carry one with an empty
population."

**Item 2. A9's enumerated edits.** The population edit names the populations of the four named bases, and nothing else.

README:140, old: "For the (iii) Run the population is also covered." Read as: "For the (iii), (iii-p), (iii-f) and
(iii-s) Runs the population is also covered."

README:142-143, old: "and the per-disposition population edits (the (iii) Run's population)". Read as: "and the
per-disposition population edits (the populations of the (iii), (iii-p), (iii-f) and (iii-s) Runs)".

The rest of README:137-146 (identity-normalized comparison, preserved budget, capability, configuration and grant values)
is unchanged.

**Item 3. The two indeterminate cycle cases are named bases, each with a disposition of its own; they are not (iv).**
`retained-typescript-file-partial` and `retained-typescript-symbol-partial-optional` stay replayed, as at product `1ba880cf`
(lead ruling on Q-RF2-GOLDEN, option (c)). Disposition (iv) cannot meet README:96-100 for them, because no stored outputs
exist: the cycle fixture stores inputs only, and replay checks outputs it builds in memory. Disposition (i) would drop
the populations whose indeterminate reasons they exist to show. This is the cross-vendor reviewer's first alternative for
RF-2 (`review-codex-code/VERDICT.md`, point 5: "explicitly amend/adopt the named pass/partial exceptions").

Two bullets follow the (iii-p) bullet of item 5:

> - **(iii-f) The file-partial Run:** the indeterminate Run `retained-typescript-file-partial`, with its live `typescript`
>   population, moved onto the release pack. Its Plan carries what the (iii) Plan carries (README:127). *Control:* on
>   replay its indeterminate outcome, with the rule deficiency cause `incomplete-inventory`, is produced by the release
>   rule over its retained facts, not typed into a fixture.
> - **(iii-s) The symbol-partial-optional Run:** the indeterminate Run `retained-typescript-symbol-partial-optional`, with
>   its live `typescript` population, moved onto the release pack. Its Plan carries what the (iii) Plan carries
>   (README:127). *Control:* on replay its indeterminate outcome, with the rule deficiency cause `population-unknown`, is
>   produced by the release rule over its retained facts, not typed into a fixture.

The reasons are those the evaluator's cycle test asserts for the two labels (`crates/evaluator/src/atoms.rs` at `1ba880cf`,
:4296-4312 for `file-partial`, `incomplete-inventory`; :4313-4329 for `symbol-partial-optional`, `population-unknown`),
and the unit's handoff pairs them the same way. Nothing is lost at replay level, so the record's disclosed limit
(README:115-117) gains no sentence for these cases.

**Item 4. Controls.** README:172-174 ends "also A4's pin, the reviewed coverage map, the (iii) control and A9's diff
control." Two controls are added to that list:
- The corpus check covers every regenerated fixture that reaches `replay_run` (the host corpus, the seal corpus, the cycle
  fixture and `run_candidate.rs`). It pins the four named lawful base evaluations by label and by regenerated RunId, fails if
  one of the four is missing, and refuses any other lawful base evaluation with a live `typescript` population. A forged-output negative passes the check
  only if it reuses exactly one base's retained Plan, population and other evaluation inputs, the base being either a
  named lawful base evaluation or a disposition (i) empty-population Run, and differs from that base only in the specified
  claimed output and its dependent identities and carriers. A negative on an (i) base keeps that base's empty population.
- A forged-verdict case exists on the pass base and on the fail base (README:101-104). Every retained forged-output negative (README:101-107) is
  compared with its base under the identity-normalized comparison, so that only the one forged claimed output and
  its dependents differ (README:101-103: "built by forging one claimed output of a release-pack Run, so the mismatch is
  the only thing wrong"), and asserts its exact mismatch diagnostic (README:105-106: "`evidence.regeneration-mismatch`").

**Item 5. "The pass base" and its disposition: an amendment, not a note.** README:87-89 says: "**(i) Structure:**
regenerated onto the release pack with an empty `typescript` population (MC8:1101). This covers the seal-corpus Run, the
synthetic's source, the pass base, and cases whose test checks replay, admission, commit, bounds or member removal." It
cannot be read as a note without contradiction: the sentence gives (i) an empty population and lists the pass base under
it, while the pass base is the named Run `retained-typescript-acyclic`, which has a live population and is exempt under item
1. No empty-population pass Run exists (lead ruling Q8, measured: `packet-2-original` comes out `indeterminate`,
`no-covering-program`). So (i) covers the structure Runs that are not pass. README:85-86 says "Each case of the three
corpora gets exactly one disposition", so the pass Run takes a named disposition of its own, (iii-p), and not (iii), which
README:90 defines as "one fail Run".

README:87-89, old text as quoted above. Read as:

> - **(i) Structure:** regenerated onto the release pack with an empty `typescript` population (MC8:1101). This covers
>   the seal-corpus Run, the synthetic's source, and cases whose test checks replay, admission, commit, bounds or member
>   removal. The pass base is not an (i) Run: it is the (iii-p) Run below.

A new bullet follows README:95 (the end of the (iii) bullet):

> - **(iii-p) The pass Run:** the one pass Run with a live `typescript` population, `retained-typescript-acyclic` (seven
>   predicate proofs), moved onto the release pack. It is the pass base, and the base of the forged verdict on the pass
>   Run. Selector 3, as widened by erratum X12A-E1, amends MC8:1101 for this Run. *Control:* on replay its pass verdict is
>   produced by the release rule over its retained facts, not typed into a fixture.

A8 (README:127), old: "- **The (iii) Plan** carries item 18's enumeration and `imports` request (MAP §5)." Read as:
"- **The (iii), (iii-p), (iii-f) and (iii-s) Plans** carry item 18's enumeration and `imports` request (MAP §5)."

## X12A-E1.3 What this does not change

- MC8:1101 itself, and its requirement for every lawful base evaluation other than the four named.
- The (iii) Run, its control ("its finding is produced by the release rule over its retained facts, not typed into a
  fixture", README:95) and the other dispositions apart from item 5, the boundary (README:111-114), A8's pack provenance, the forged-case
  rule (README:101-107) apart from what item 1 says a negative may reuse, and the RF-1 text of A9 apart from the population
  words above.
- The existing disclosed limit about `selected-nongating-live-findings` (README:115-117), which stays as written.
- The coverage map `COVERAGE-MAP-C1.md` (not in this record).
- No product code, fixture, test, lane or qualification is accepted here.

## X12A-E1.4 Open points

None. The point raised by the first draft (README:87-89) is closed by item 5.

## X12A-E1.5 Review and binding owed

- **Review: two independent reviewers** (the lead's ruling).
- **Code resting on it (at risk until this binds):** on product branch `x12d-ts-r1`, the replay of the four named
  bases (the fail, pass and two indeterminate cycle cases, kept in `CYCLE_CASES` and the regenerated cycle fixture) and the
  forged-verdict-on-pass case, marked `[AT RISK: X12A-E1]`.
- **Binding owed:** the lead's receipt `ADOPTION-X12A-E1.md` pinning this file's sha256. No design-lock entry.
