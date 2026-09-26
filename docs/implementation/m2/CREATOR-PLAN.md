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
| 461 | Replace the legacy writer-list reader in existing custody consumers | 462, 458c | REORDERED 2026-09-26 (owner agreed): `/` and `/Users` omit the ACL, so refusing omission before an admissible premise exists makes every read-side consumer (installation fence, trust reads, census, store marker) refuse at `/` on stock macOS. 462 mints the receipt first; 458c extends a receipt-bound premise to the read fence's root-to-H prefix; then 461 maps omission to unreadable at the single custody choke point |
| 458c | Law: extend the receipt-bound omission premise to the existing read fence's root-to-H prefix (not project roots, operational files, `OpenSIP`, I or private descendants) | 458, 462 | 458 §5 currently withholds Evidence B from existing consumers |
| 462 | `InitialPlatform` without a fence (it takes the per-descriptor `fstatfs` itself; mints Evidence B only from a row carrying `installAclOmission`): boot, process, loader and per-descriptor filesystem samples joined to an authenticated profile | 463, 458b | Existing factory requires a fence; profile verification takes a caller revoked set |
| 469 | Law: macOS 27 in the supported population (owner decision 2026-09-26); then the synthetic test profile350 successor with `supportedMajors."26"` floor 26A428 | — | DONE (469 r1; code 469 code r1 at product aed5e08) |
| 348a | DONE (law 348a r1; code 348a code r1 at product 0a3af77): select the fat slice whose full cputype/cpusubtype equals the header the kernel mapped for that image in this process. Loader observation works on macOS 27 | — | macOS 27 dyld has two arm64e slices; 348 refuses |
| 463 | LAW ACCEPTED (463 r3; initial-core-launch-463/PROPOSAL.md). 463a DONE (Grok 463a r3: the running image's kernel CodeDirectory hash joined to its retained file, `macos_image.rs`). Code still owes the image layout, flags, `authenticate` revocation change, K record successor (463b) and signed fixtures. `InitialCore`: executing core identity from the loader TCB, open-then-verify of executed members, core-rooted profile authentication, K from writer capability | — | No producer exists; needs a signed core release format and fixtures |
| 464 | LAW ACCEPTED (464 r2; creation-ingress-464/PROPOSAL.md; code under review; classifier UNKNOWN-first, stderr disclosure before effects, no CLI wiring until 467). `CreationIntent`: durable ingress, command eligibility, first-write disclosure with the storage root, backup classification and `--allow-backup-custody`, `INSTALLATION.NOT_INITIALIZED` | — | CLI has only metadata ingress |
| 465 | Parent preparation and permit: H barrier, create-or-admit each fixed ancestor with own and parent barriers, no-follow absence of `preview-v1` | 459–464 | — |
| 466 | PARTLY DONE (466 r1: the trust publication, verified in memory; host composition of the non-trust files waits for 467): P0 producers: fence file, registry v2, marker, node, pair, CreationInput, OperationInput, creation event, descriptor, state.v1 | 463 | Only decoders and verifiers exist |
| 467 | Stage, validate, publish, final barrier, loser and indeterminate routes, ordinary handoff | 465, 466 | Primitive exists; composition does not |
| 468 | §5 observation versus durable write, doctor informational note, formal diagnostic successors | 467 | Needs schema/generation successor |

The M2 exit (pure replay, live guards, storage facade, carrier recovery join, refusal suite and crash/lock/revocation matrix) follows and is planned separately. All 32 release gates remain unqualified.

## Reviewer budget

Grok's pane showed 3% of its weekly limit after 457. Units are sized to use each review well. If Grok cannot review, implemented bytes stay uncommitted and are recorded as unreviewed; no second reviewer is used.
