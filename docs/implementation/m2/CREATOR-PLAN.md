# Initial creator implementation plan

2026-09-23. Claude Opus 5.5 leads; Grok is the single reviewer. Working plan, not selected law. It orders the owner's creator obligations into reviewable units. Each unit is one decision, reviewed after its tests. Nothing here enables the creator; the owner keeps it disabled until the launch, actor and profile receipts exist and one shared budget covers staging, publication and the final rename.

## Installed (product e7bd764)

Bounded ACL capture; private-descendant and external-ancestor predicates; private file and directory creation through a retained parent; directory observation; parent-gated file creation; `WorkLedger` with the owner's caps; stage directory and exclusive rename with typed visibility; directory barrier with receipt; bounded account observation; read-only root walk (legacy chain); installation fence on an existing root; read-side record decoders and trust verifiers.

## Units, in dependency order

| # | Unit | Depends on | Blocker or note |
|---|---|---|---|
| 458 | Law: ACL omission premise for external ancestors | — | ACCEPTED r2 (459 r1 premise458.json) |
| 458b | Profile-set schema successor: measured macOS row member `installAclOmission` | 458 | Contract successor with decoder, shape and signature cases; until selected, omitted ancestors refuse |
| 459 | DONE (product, 459 r1): Attempt and actor: `InitialInstallationAttempt` owning one ledger; `InitialActor` from the charged account observation (equal real and effective UID, home 1..4096 bytes, at most 256 components) | — | New host file needs an inventory successor |
| 460 | DONE (460 r2): Root-to-H chain and fixed suffix on the bounded capture, charged, using Evidence A or B; `OpenSIP` judged private | 458, 459 | Evidence B needs 462's receipt; until then the chain refuses omitted ancestors |
| 461 | Replace the legacy writer-list reader in existing custody consumers | 458 | Omission must stop reading as no writers everywhere; existing callers change behavior |
| 462 | `InitialPlatform` without a fence (it takes the per-descriptor `fstatfs` itself; mints Evidence B only from a row carrying `installAclOmission`): boot, process, loader and per-descriptor filesystem samples joined to an authenticated profile | 463, 458b | Existing factory requires a fence; profile verification takes a caller revoked set |
| 463 | `InitialCore`: executing core identity from the loader TCB, open-then-verify of executed members, core-rooted profile authentication, K from writer capability | — | No producer exists; needs a signed core release format and fixtures |
| 464 | `CreationIntent`: durable ingress, command eligibility, first-write disclosure with the storage root, backup classification and `--allow-backup-custody`, `INSTALLATION.NOT_INITIALIZED` | — | CLI has only metadata ingress |
| 465 | Parent preparation and permit: H barrier, create-or-admit each fixed ancestor with own and parent barriers, no-follow absence of `preview-v1` | 459–464 | — |
| 466 | P0 producers: fence file, registry v2, marker, node, pair, CreationInput, OperationInput, creation event, descriptor, state.v1 | 463 | Only decoders and verifiers exist |
| 467 | Stage, validate, publish, final barrier, loser and indeterminate routes, ordinary handoff | 465, 466 | Primitive exists; composition does not |
| 468 | §5 observation versus durable write, doctor informational note, formal diagnostic successors | 467 | Needs schema/generation successor |

The M2 exit (pure replay, live guards, storage facade, carrier recovery join, refusal suite and crash/lock/revocation matrix) follows and is planned separately. All 32 release gates remain unqualified.

## Reviewer budget

Grok's pane showed 3% of its weekly limit after 457. Units are sized to use each review well. If Grok cannot review, implemented bytes stay uncommitted and are recorded as unreviewed; no second reviewer is used.
