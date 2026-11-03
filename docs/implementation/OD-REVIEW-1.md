# OD-REVIEW-1: additional same-vendor review strategy

Status: accepted owner decision; effective 2026-11-03 UTC (2026-11-02 PST).
Scope: OpenSIP's agent review process. This is not a product-law change or a
technical acceptance verdict for any pending subject.

## Owner instruction

> lets add this as an accepted and additional strategy, only allowing codex or claude to use same vendor

The instruction accepts the preceding proposal for separate author/reviewer
sessions, evidence-based review, additional scrutiny for consequential work,
and a measured initial rollout. The operational details below implement that
decision; they are not additional quotations from the owner.

## Two permitted strategies

- `CROSS-VENDOR`: retain the existing different-vendor review strategy and its
  capability requirements. It remains the default when no strategy is selected.
- `SAME-VENDOR-SEPARATE-REVIEW`: an additional, explicitly selected strategy,
  permitted only for Codex authors reviewed by Codex, or Claude authors reviewed
  by Claude. It can satisfy the required acceptance review when all conditions
  below are met. It is available by choice, not only during a credit outage.

No other provider may use this same-vendor option. It does not qualify DeepSeek,
Grok, or another provider, change their prior findings, or create a new route.
Using a different model within one vendor is optional and does not establish
vendor diversity. Record the remaining risk of shared blind spots.

## Conditions for same-vendor acceptance

1. **Separate authors and reviewers, observable sessions.** The author cannot
   accept their own subject. Use a fresh reviewer session that did not author or
   revise the subject and does not inherit the author's conversation. Record
   author and reviewer session IDs, provider, exact model, effort, route and
   successful route preflights. A second role prompt in the author session is
   insufficient. The coordinator may dispatch and reconcile reviews, but may not
   replace a required reviewer verdict on a subject it authored.
2. **Requirements before persuasion.** Give the reviewer accepted requirements,
   contracts, the exact candidate/base and relevant raw evidence. It records an
   initial assessment before receiving the author's justification, prior review
   verdicts or another reviewer's findings. Do not hide required specifications
   or adverse raw results to achieve this separation. Disclose unavoidable prior
   exposure; use a fresh reviewer if it defeats the initial independent pass.
3. **Evidence, not agreement.** Require concrete source/contract references,
   triggering inputs or counterexamples, examined failure paths, and reviewer-
   derived checks. Distinguish checks actually run from source inspection and
   supplied evidence. Architecture reviews challenge assumptions, compare viable
   alternatives and test invariants against scenarios. Do not require a reviewer
   to invent a defect or treat matching verdicts as proof.
4. **Additional review for consequential work.** Contract law, consequential
   architecture, security/custody/provenance, concurrency/cancellation, resource
   accounting, production composition and final qualification require two fresh
   reviewer sessions in addition to the author. One examines contract/invariant
   consistency; the other examines adversarial failure cases and evidence gaps.
   They form their initial findings separately. Both must issue the required
   favorable verdict on the final exact subject, or explicitly accepted carries
   where the unit already permits them. All required findings must be resolved;
   a majority vote or coordinator preference cannot waive a dissenting finding.
5. **Capability and execution gates stay.** Use the existing unit's minimum
   review route, escalation triggers and exceptional-effort rules. Routine scoped
   units require at least R1; the consequential scopes above require at least R2,
   and existing R3/R4 requirements remain. Source pins, author handoffs/assents,
   plan acceptance, binding, lane locks, exact-candidate validation, integration,
   data-access limits, publication and qualification criteria are unchanged.
   Reviewer access is not permission to run a lane or declare a unit complete.
6. **No retroactive acceptance.** Prior verdicts remain byte-identical. A new
   eligible review must be requested and recorded; an old advisory review does
   not become acceptance merely because this strategy now exists. Mixed-author
   subjects identify all authors, and reviewers must be separate from all of
   them. Eligibility is assessed for the full subject, not just its last editor.

The strategy may cover required reviews at any project stage, including design
and qualification, subject to the stronger conditions above. External review is
an additional assurance option when available, not a hidden prerequisite of
this strategy. No qualification criterion or substantive product gate is waived.

## Selection, records and initial rollout

The coordinator selects the strategy in the live execution handoff and each
review request. For a frozen plan, reference this decision as an additive
process overlay; never rewrite the accepted plan merely to change its vendor
requirement. Record at least:

```text
Review strategy: SAME-VENDOR-SEPARATE-REVIEW
Review authority: OD-REVIEW-1; <decision path and SHA-256>
Review subject: <base/head or exact manifest and SHA-256>
Author sessions: <IDs, providers, models, efforts and routes>
Reviewer sessions: <distinct IDs, providers, models, efforts and routes>
Review scope: <routine or consequential; rationale and required reviewer count>
Initial assessments: <separately recorded artifact paths and SHA-256s>
Review evidence: <checks, counterexamples, findings and dispositions>
Final reviews: <verdict artifacts and SHA-256s on the final subject>
```

The current route tool checks provider/model/effort only. `ROUTE-OK` does not
validate this review record or establish review separation. The coordinator must
check these conditions before accepting a same-vendor verdict; missing evidence
leaves the subject awaiting review.

Before the first same-vendor acceptance for a selected provider/reviewer route,
run fresh-context historical checks containing a representative known required
finding and a clean control, with prior verdicts withheld until assessment.
Record missed findings and false positives, and resolve any calibration failure
before relying on that reviewer configuration. Calibration is bounded evidence,
not proof of general reliability. The first three live subjects using this
strategy form the initial rollout: record findings, escapes, false positives,
review effort and correction rounds. The coordinator then records whether to
continue, narrow or strengthen the workflow. This is an accepted strategy with
measured rollout, not a proposal awaiting another owner approval.

## Relationship to earlier instructions

This decision supersedes only the blanket different-vendor-only restriction
where the eligible same-vendor strategy is explicitly selected. That includes
the corresponding restrictions in OD-AUTO-1, OD-PROC-1, the routing guidance and
existing unit/coordinator plans. Their other provisions remain in force.
Historical documents and verdicts are preserved as history; live controls point
to this additive decision. The existing cross-vendor strategy remains accepted.

Existing pauses caused solely by unavailable different-vendor review can now
proceed to reviewer selection and the checks above. This does not assert that
reviewers have been launched, calibration has passed, pending work is accepted,
or the end-to-end project goal has been achieved.
