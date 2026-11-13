# Adoption receipt: ERRATUM X12A-E1 (the empty-population exemption names four lawful base evaluations)

**Prepared by the records clerk on the lead coordinator's binding instruction (OD-LEAD-1); the lead's merge of this branch is its adoption.** This is an erratum to the bound record X12-A r7 (`README.md` of this directory, 17,858 bytes, sha256 `e4f44496b1cc45b2fd103cbea636124289e87b62f9338cf1c900803f8e7b8a2e`, bound on architecture main with its unit `../x12-a-r1-unit.json`). X12-A r7's bytes are NOT edited; the erratum is read with it.

**Adopted:** the exact bytes `docs/implementation/m2/policy-admission-x12/x12-a-r1/ERRATUM-X12A-E1.md` (13,304 bytes), sha256 `1cffb1bfc32948eb88ed85dc64e8c4a4b9b706223ce2c6349ffff7f9bc4cf9e6`, at head `016061dba38113ec29aa40996ea91b03e418f872`, the bytes both reviewers accepted.

**Substance (the erratum controls):** it amends MC8:1101's empty-population exemption (MC8 item 19 part 4: the replay corpus moves onto the release pack "with an empty `typescript` file population") for exactly four named lawful base evaluations, and for no other: the disposition (iii) fail Run `retained-typescript-self-cycle`, the (iii-p) pass Run `retained-typescript-acyclic`, and the two indeterminate cycle cases `retained-typescript-file-partial` (iii-f) and `retained-typescript-symbol-partial-optional` (iii-s). MC8:1101's requirement stands for every other lawful base evaluation. Forged-output negatives are not further exemptions: each reuses exactly one base's inputs and is compared with that base. Where r7 and this erratum differ, the erratum controls; where it is silent, r7 stands.

**Code resting on it:** product branch `x12d-ts-r1` (the replay of the four named bases and the forged-verdict-on-pass case, marked `[AT RISK: X12A-E1]`). That mark resolves at the lead's merge of this branch. No code is accepted by this receipt, and the cross-vendor reviewer's acceptance is conditional on the code retaining or restoring the replay coverage of the two partial cycle cases.

**Basis, bound by value:** Codex gpt-6.1-sol/high (`reviews/codex-x12a-e1-r1/review.json`): ACCEPT at the final head. Claude claude-opus-5-5/medium (`reviews/claude-x12a-e1-r1/review.json`): ACCEPT at the same head; its one wording advisory is not applied and stays open. Earlier verdicts on earlier heads are history.

**Not established here:** no implementation, integration, lane or qualification. No design-lock entry and no contract successor: the product's `design-lock.json` names no X12-A path, and the erratum says so.
