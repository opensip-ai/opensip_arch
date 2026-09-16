I resolved both questions in a new copy of the capture's core docs. Seven files changed, and every focused check passes except the security owner launcher, which stops at its source-pin gate as expected. Your v2 runtime and the capture are both byte-unchanged; I re-hashed them at the end.

**1. Repair:2 constructor.**
- **Cause:** `workflows_model.v3.py` is the current workflow owner, but its `repair_preview` was just the historical v1 function, so it always built a major-1 plan. The projection model is a separate, pure module; it already owns the target-matching law and the evaluator3 schemas.
- **Historical path:** the v1 builder gains one keyword-only argument, `descriptor_major`, defaulting to 1. The historical tests and the integration host call it without the argument, and their check output is byte-identical to the unmodified capture.
- **New constructor** (`workflows_model.v3.repair_preview`): before building anything it checks, in order:
  - the evidence Run is authoritative (still first);
  - the retained Run exists and has the same `planId`;
  - the evidence Run is run3;
  - every target is a matched fingerprint of that retained Run with compatible metadata.
- **Output:** it builds the descriptor at major 2, then returns the plan only if `admit_repair_plan_v2` accepts it. A major-1 plan is refused with `EVALUATION.MIXED_OUTPUT_MAJOR`. A relabelled plan whose id wasn't recomputed is refused with `IMPORT.ARTIFACT_CORRUPT`.
- **Checker:** I removed the r2 relabel code and its check; the repair-preview control now carries the plan exactly as the owner returns it.
- **Controls:** new ones cover the positive plan, the historical path, and each refusal:
  - a target the Run doesn't match (the historical constructor would accept it);
  - a retained Run from another plan;
  - a run2 evidence Run;
  - the unreminted relabel.
- **Pinned ids:** the historical `repairplan2` values are unchanged. The current-profile plan ids were never pinned and do change, because major 2 is now part of the identity.

**2. CONFIG.INVALID for policy-test suite admission.**
- **Error code versus detail:** as an error code, `CONFIG.INVALID` is the D9 request-rejected code (exit 2). As a detail, it is a separate entry in the shared public detail registry. Security registered that entry, but nothing restricts use to security, and native and identity already use the same detail on their own routes. So using it for workflow suite admission is lawful, and no new code is needed.
- **Contradiction:** the sentence I wrote in v2 did conflict with the workflows owner's own rules, in two ways:
  - a policy key outside the closed grammar, or a string expression, must be `POLICY.IMPERATIVE_KEY_REFUSED`, not `CONFIG.INVALID`;
  - resolver refusals, such as a duplicate waiver, are request rejections according to the existing goldens, not "result data".
- **Correction, route:** workflows-and-surfaces §5, §8 and §9 now state the full route. Grammar violations get `POLICY.IMPERATIVE_KEY_REFUSED`, any other suite admission failure gets the shared `CONFIG.INVALID` detail, and resolver refusals keep their own details.
- **Correction, goldens and carrier:** a new inventory golden `policy-test-suite-inadmissible` records the residual route. The policy-test carrier now only accepts results where the resolver accepted the suite.
- **Correction, reference code:** `admit_policy_test_suite` is the owner's admission function. It has typed refusal controls that check the error code and detail separately, using the owner's existing workflow-cases fixtures. The registry itself is unchanged.

**Checks.**
- **Baseline:** on the unmodified copy, workflow-projection 766, query-projection 204, current-profile 38, workflows-v1 1816, integration 412.
- **Final tree, workflow-projection:** 795/795, with one check removed (the relabel) and 30 added.
- **Final tree, other checkers:** workflows-v1 1816, integration 412, query-projection 204, current-profile 38, comparison-knowledge 1, composition 30, semantic-replay 31, evaluator-faults 41, replay 73. The first four give output identical to the baseline. Those last five only have receipts after the edits, not before.
- **Security:** the owner launcher exits 1 on its pin gate (55 paths). Seven are this delta's files, 3 are review files excluded from the copy, and 45 already differed in the capture itself. With the gate bypassed, the security checks pass 464/464 with 11/11 sweeps, but that is not the owner launcher.
- **Failed attempts:** one run failed and is kept (`oc-1`). My grammar classifier misread conditional schema parts as allowing strings; I fixed it and reran. A later diff review found §5 wording narrower than the code, which I aligned (text only) before rerunning everything.

**Limitations.**
- Snapshot equality is still judged against the synthetic fixture tree, not the retained Run's real snapshot.
- The evidence Run is tied to the retained Run by `planId` and the run3 prefix; its run3 identity isn't re-derived.
- The metadata-ambiguity refusal is reachable but no full admitted Run exercises it.
- The policy-test suite is still the major-1 suite format.
- config2 roots-only proposals, zero registered recommendations and unmodelled HTML stay as previously reported.
- No pins, planning, packages or grades were updated, and I make no readiness claim.

**For your integration.**
- **Paragraphs to merge:** workflows-and-surfaces §5, §6, §8 and §9, plus projection-contract §5.
- **New module dependency:** `workflows_model.v3` now lazily loads `workflow_projection_model.v3`, with no import cycle.
- **Carrier schema:** `PolicyTestResultRecordV1` now requires `resolverAccepted` to be true.

Everything is in `/private/tmp/opensip-design-corrections/claude-workflow-owner-completion.v1`:
- review.md — sha e0912a82…
- review.json — sha b9c94433…
- diffs/capture-to-work.diff — 509 lines, sha 518c6a37…
