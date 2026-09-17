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
