# Resume actual independent review after the quota reset

This is a navigation aid for the existing review queue, not a new approval policy or an acceptance record. Read [ACTIVE-WORK](../ACTIVE-WORK.md) and [PENDING-REVIEW](PENDING-REVIEW.md) first. Their latest entries govern any later candidates. The user reported on September 17 that both Grok and Claude would reset in roughly 24 hours; that estimate is not confirmation that either is available.

The installed product remains runtime24 on design30/44. Private drafts contain substantial additional implementation and tests, but no unavailable reviewer has approved them. Do not substitute a GPT subagent, reuse an old assent for changed bytes, or install a cumulative draft simply because its tests pass. Preserve each historical archive and failure record. The user pushes; do not push.

## Questions to put in front of the returning reviewer

1. Adjudicate the pending reference corrections before approving dependent implementations. Reference60, 66, 69 and 73 form the relevant security correction chain; publication reference78 is a separate physical-error correction. Their evidence and dependencies are indexed in PENDING-REVIEW. Resolve the Unicode15/16 metadata bridge with reference63/source64 without silently changing identity's Unicode16 profile.
2. Resolve [draft97's integration questions](trials/witness-floor-draft-checkpoint-97/README.md). Its archive includes REVIEW-QUESTIONS.md: witness/floor file decoder selection (including negative zero) and the read-only diagnostic rule for malformed/foreign witnesses. Value constructors and proposed reconciliation actions do not decide either question.
3. Review the [reproduced purge-disclosure size gap99](trials/purge-disclosure-bound-checkpoint-99/README.md) before pin persistence or purge installation. The required complete envelope can exceed 4 MiB with names/counts admitted by the current schemas. Decide aggregate byte admission, both disclosure copies, optional/wrapper accounting, error/projection ownership and treatment of pre-existing over-budget state. Truncation and destructive fallback are not acceptable resolutions.

## Review the cumulative code in coherent groups

Use the exact source manifest of the latest frozen candidate and its verified parent chain. The groups below describe related changes, not independent accepted baselines. A review must bind every source actually examined and state which inherited dependencies remain conditional.

| Group | Drafts / evidence | Main questions |
| --- | --- | --- |
| Evaluation and replay | composition50, replay52, inventories33/34 | Complete retained-input derivation; non-forgeable owned replay output; source/runtime selection |
| Signed security records | 54,57,59–75 and related reference/inventory successors | Exact canonical profiles, signatures, shape/semantic ordering, trust context, revocation and conditional authority |
| Native custody and lifecycle | platform55,76–86; reference78; probes82/83 | Native ABI/ownership, ACL interpretation, lock lifetime/order, deadline clocks, publication uncertainty and final gate |
| Journal | 87,95–97 | Owned SEAL binding, selected physical schema, prefix/row checks, weak-chain assurance limit, witness/floor admission and unresolved integration questions |
| Storage | 88–94,98,100 | Immutable blob publication, SQLite configuration, single snapshots, attempt/receipt joins, paired transactions, availability generation checks and failure poison |
| Representation correction | probe99 | Complete pin disclosure must remain representable before durable admission, across required surfaces |

No claim is made that these groups can be approved from summaries. Every archive has a subject manifest and archive pin. Verify archive bytes and all members, inspect complete changed source and required context, and run the appropriate retained evidence. Do not execute preparers/freezers against an existing trial directory: many intentionally refuse reuse. Use an explicitly new review workspace and preserve any failed attempt.

After substantive findings, correct an editable successor, run the relevant checks, freeze new exact bytes and obtain review of those bytes. Update selected references, inventory/source/runtime manifests, readiness and accepted-design records only through the existing formal selection process. Availability of a reviewer alone does not complete those steps. Linux, suspend/reboot, power-loss and release qualification remain distinct from the observed macOS development tests.


## September18: actual112/113/D2r3 retained; frozen111 and114

Architecture predecessor8f6349346. Actual Claude remains primary in Herdr wF:p1 session de59b975-4f82-4aff-9252-ad6d68d6fb79; no quota error. Grok wN:p1 idle fallback. Product fa72e50 remains clean and unchanged; no pushes. Commit authority persists; user pushes.

Actual112 review archived (28members347056B, all rehashed): no blocker;106S1a/S1b/T1/T2/T3 closed.15611platform/855recovery differential cases had no admission disagreements;12of14compiledmutantskilled. NonblockingN1nonstringfsType typed-error divergence,N2multibyte/overflow test gaps,N3exactcount,N4class-leveldiagnosticmapping addressed in114, awaiting actualreview. Actual113 review archived (9members4936B): no findings,110N1closed;29platformtests4compiledmutants. ActualD2r3 adjudication archived (8members9988B): G1-G4 resolved choices; H1/H2explicittext required; no111text/modelacceptance. Reviewer withdrew multigeneration end-copy suggestion in favor of anchored final floors.

111 FROZEN at m2/trials/readonly-generation-reference-checkpoint-111:1284candidatefiles14changed/added versus108;1429members2026352B SHA050104a287797487bc833bb85c630119fc3e8f4e87d5b5b3149a4be334009a55. Prospective generation/floor/read-only/migration/marker law plus two pure kernels/fournewreferencefiles. Explicit requested-generation tails, immutable historical floors once witness leaves, closure/marker checks, witnessed TERMINAL/new append, no quarantine repair, carrier-before-witness dispatch including inherited rows, COMMITTED0 floor choice, no clock recovery lowering journal floors. External carrier/schema/custody/authorization and counter-exhaustion checks remain preconditions; no SQL/IO/marker writer implemented. H4chosen historical scope ignores witness decrease between two generations BOTH later than the requested historical association; actualadjudication requested, not claimed agreed.

111final checks PASS:231foundation1816workflow477native/66matrix581security/18sweeps406carrier423integration, freshsignature168+145+6000+1803receipt.29anchorcases/49checks;49dispatch+5floorcontrols;167codecchecks.14compiledkernel/dispatchmutantskilled. Boundedr2/r3lawful schedules0falsequarantine; r3negative unwitnessedTERMINAL-only224/48diagnoses. r2negative additionallyunanchoredcopy; r1rejectedmultigenerationcopy evidence preserved/notqualification. All49pinupdates andbeforeimages retained. Freeze script finish_reference111_checkpoint.py completed; neverrerun. Actualfrozen111 review queued after currentmonotone113 via reference111-20260918-REQUEST.md, expected claude-reference111-20260918-r1/REVIEW.md.

114 FROZEN at m2/trials/security-followups-checkpoint-114:330productpins327unchangedfrom113;379members4078392B SHAe9f44223b0462321ce50203c83f3d054b076a780def2f1c135ccd5ffc6040359. Only trust.rs and2existingfixturecorpora;6platform+2recoverycase append, oldbytespreserved.64security/strictworkspaceClippy/3compiledmutants pass;freshhost67 210sources51archives272workspace+2docs/build/metadata/version/help, HOMEabsent. NoLinux/OS/dependency/releasequalification. Actual114scopedreviewqueuedafter111 via security114-20260918-REQUEST.md. prepare_security_followups114.py/freeze_security114.py completed; neverrerun. Exactdraft /tmp/opensip-implementation/m2-security-followups-114.

Currentactualreview: monotone-security113 (trust_time.rs full/assess, observe_revocation, revocation.rs full); expected claude-monotone-security113-20260918-r1/REVIEW.md. No verdict yet. Independent probes running. Linuxarm/profile_shape/linux_profile; signed106R1/R2/R3; inheritedjournal/storage/native/evaluator andD3-D6 remain pending, not covered by recent approvals. Need formal selection/integration after coherent reviewed units. M2 andM3-M6 remain open. Preserve frozen/evidence/workingtreebytes; no GPT substitute.
