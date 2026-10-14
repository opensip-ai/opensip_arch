# Review request: M3-L r7, the S-M delta round on M3-L r6

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-provider-protocol-l-r7/`).

## Boundaries

Do not edit either repository, the stage or control files. Do not run the compiler, Cargo, tests or the lane. No network. Do not read the private 413 fixture, the installation directory (`~/Library/Application Support/OpenSIP`), signing keys or held trees. Do not use other panes and do not delegate. Permitted: read-only hashing, JSON parsing, reading sources and read-only Git queries. You may re-run control L-C1 in the stage: `python3 -I -B /tmp/opensip-implementation/provider-protocol-l-r7-stage/docs/implementation/m3/provider-protocol-l/evidence/wire_identities.py --check`. It only reads.

## Lead note

You accepted r6 in review (`codex-provider-protocol-l-r6`). "Review and effect" sends a delta round to the same reviewer, so no substitution is needed. This is the **first trigger**: "filling every `⟨SM-n⟩` from S-M's report, with every outcome item 9 records, and any owner answer to O3 or O4 that those outcomes trigger". It also refreshes the gate rows.

**On acceptance, by r6's own text, L takes effect.** Every other gate item is met, and no other delta round is owed before effect. Check that claim with particular care.

## Subject

- Stage: `/tmp/opensip-implementation/provider-protocol-l-r7-stage`
- `subject.json`: 5024 bytes, SHA-256 `dc8747519c6e7fcf948a7a42631afa42e2ea38c53476e0afcbda12f6074c38c2`, 6 members plus 18 architecture context pins. Rehash every member, and the context pins in the architecture repo at HEAD `17049baf9a508fb69bd6c28394dcd8b5091ec79d`.
- **The law:** `docs/implementation/m3/provider-protocol-l/PROPOSAL.md`, which is r7 and byte-identical to `PROPOSAL-r7.md`. **The diff:** `r6-to-r7.diff` (`diff PROPOSAL-r6.md PROPOSAL.md`). Review it on the diff only, while reading enough of r6 to judge each change in context. `runners/make_l_r7.py` builds r7 from r6's exact bytes by asserted edits.

## What to review

1. **Item 9's values.** Does every filled value cell in item 9's table match S-M's accepted report and `sm-report-data.json`, under PLAN-r3's D-1 to D-9, with its labels? Labels to check include preliminary standing, synthetic SM-9, the one-span Rust SM-5, SM-7's fields with no conformance claimed, SM-4's partial coverage, and SM-11 to SM-14 as the S-M round's part.
2. **"(r7) Recorded".** Do the per-workload F and T match SMR §3? Is every holding outcome recorded with D-1 conditionality, and are the sensitivities stated rather than substituted? Is "items 1 and 2 stay one-shot" right?
3. **O3 and O4.** Are the owner's answers recorded verbatim from the owner records, with consequences faithful to the reviewed proposal and to L's O3 and O4 text? Are the protocol constants, items, D5 staging and budgets unchanged?
4. **SM-11 to SM-14.** Is only the S-M round's part entered? Do S_eff's other terms and the stage budget stay formulas, and is the completion round still the fifth trigger, after effect?
5. **The gate.** Check each refreshed row (L-G1 to L-G11) against its cited evidence: the owner records of 2026-10-09 and 2026-10-14, `M3-PLAN-r10.md:79-80`, and r6's header note and review. Is "no other delta round is owed before effect" true for triggers 2 to 4 (O7 decided as recommended; FA-2 and RUST3-LIM bound with no pending change)? Is "L takes effect when r7 is accepted" correct against "Review and effect" and "What dependents may rely on"?
6. **Scope.** Does r7 change only the following?
   - the header, history and r7 table;
   - item 9's preamble, value cells and "(r7) Recorded";
   - the O3/O4 answer line;
   - the gate status and "Before L takes effect";
   - "Not claimed".

   Item 13's generated block and L-C1 must be unchanged, and `l-c1-check.log` must show a pass.

Product, lock, inventory 187 and contracts 161 are unchanged. This is law text; the values are S-M's accepted ones.

## Output

`review.json` must carry:
- `verdict` (`ACCEPT` or `REQUIRED-FINDINGS`);
- `requiredFindings` (array);
- `nonBlockingObservations` (array);
- exactly these expected fields, with your independently checked values. Report the actual value, and raise a finding if any differs:

```json
{
  "verdict": "ACCEPT",
  "requiredFindings": [],
  "subjectManifestSha256": "dc8747519c6e7fcf948a7a42631afa42e2ea38c53476e0afcbda12f6074c38c2",
  "item9ValuesMatchSMReport": true,
  "everyOutcomeAndSensitivityRecorded": true,
  "ownerAnswersVerbatimAndFaithful": true,
  "sm11to14SMRoundPartOnly": true,
  "sEffAndStageBudgetStayFormulas": true,
  "gateRowsAccurate": true,
  "noOtherPreEffectDeltaRoundOwed": true,
  "LInEffectOnAcceptanceStatedCorrectly": true,
  "onlyRoundTextChanged": true,
  "item13AndLC1Unchanged": true,
  "protocolConstantsUnchanged": true,
  "outcomeRulesUnchanged": true,
  "completionRoundStillOwedAfterEffect": true,
  "budgetsOrStagingChanged": false,
  "productQualification": false
}
```

After an ACCEPT, the lead gives its own assent, runs fresh design verification and publishes r7 architecture-only, recording L in effect. Nothing is pushed.
