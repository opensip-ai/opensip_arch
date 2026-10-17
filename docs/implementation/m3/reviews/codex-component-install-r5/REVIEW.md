# Component release installation and tree custody — CI r5 review

Verdict: **ACCEPT** — no required findings; three non-blocking observations. This accepts the law proposal, not implementation code, binding or qualification.

## Subject and verification

Manifest: 1,343 bytes, SHA-256 `ad9c4c55d774a0673ad7f098b300db7f9a10eb1da25bd8632bc4a641c7291db4`. All six members match their lengths and hashes. PROPOSAL-r5.md is 63,707 bytes, SHA-256 `efdbf7e70ab48522fec855bbb74f144a5c695c27eefc194b2de000e8e3a54333`; the four historical proposals and input memo are unchanged.

The manifest names product `3742822e2823c3a7624aca3fea11220a46cffa16` and architecture `d89779089a9132de7b089e05c295581bd23b8963`, matching live HEADs. These are newer than the request’s b7538549/a87c1234 shorthand. The eleven inspected publication/barrier/traversal/ledger/custody/capture/snapshot/termination authority files are byte-equal to b7538549, so the advancement does not alter the reviewed primitives.

Reviewed the r5 text, its changes against r4, the prior findings, and the cited primitive charge/operation definitions. Only reading, hashing, JSON parsing and Git queries were used. No Cargo, rustc, builds, tests, lanes, shared lane lock, network, private fixtures, installation directory, keys/private test keys, held trees, T2/cache/held-out material, other panes or delegation were used. Neither repository was edited.

## Requested dispositions

**CI-R4-RF-1 resolved.** B_open explicitly funds and retains the verified tree/ base via desc(4), once. RetainedTree now holds that handle, the generation and pin handles, the shared buffer and borrowed evidence. Blob paths are explicitly relative to tree/, with k equal to their component count. Transfer begins at that retained base, resolves its k-1 parent components individually without following links, then opens the file. A root-level Blob therefore needs zero parent descents; a nested Blob needs exactly its stated parent count. B_transfer and item 6 agree. CI-T22 records root and nested paths, bans a multi-component openat substitute, and preserves sink commit only after final length/digest verification.

**CI-R4-NBO-1 resolved.** cust now equals the actual public descriptor_acl_capture_cost. Source confirms admit_custody_directory calls observe_private_directory, which calls capture_descriptor_acl_accounted and charges that cost once. No legacy descriptor-observation allowance is substituted or added. P-7 is limited to exposing status_read_cost or an equal published price. CI-T22 identifies the actual custody chain and the one charge.

**Final re-derivation accepted.** The recipes now cover the selected execution strategy’s operation categories. There is no remaining required pricing omission at law level. In particular:

- **Installation admission/acquisition:** bounded existence/name observation, store custody, archive path/open/kind check and identity samples are named. The stage’s retained handles and worst-case creation attempts are included by its existing primitive; stage custody and tree/ creation are separate. Borrowed trust/candidate/fence inputs do not acquire duplicate charges.
- **Population:** each archive member’s parent-chain descent is charged independently, followed by the selected exclusive file/directory or symlink creation. Chunk writes and the archive read buffer/attempt envelope are explicit. Handles are released per member rather than accumulated for all entries.
- **V1:** root and committed-directory descents, complete bounded listing, status reads, link-text buffers, file opens and file read attempts are priced. It verifies staging permissions and bytes without constructing an admitted retained capability.
- **Finalization:** root and directory descents plus each file’s newly opened handle, chmod and barrier are explicit. The record’s create/owned bytes/write/mode/barrier, pin create/barrier, each final directory mode/barrier and the stage barrier are separate terms. This count is implementable by post-order driven from borrowed TreeCommitment paths while retaining the current traversal stack; it does not fund another filesystem listing pass (NBO-1). It also does not fund reopening every ancestor independently for every file during finalization. The actual CI-2 implementation must obey that distinction.
- **V2 and publication:** independent full structural enumeration/link checks, expected-record bounded read/byte comparison and pin state checks are priced. effect=0 and postchecks=exclusive_publication_cost+dbar reserve exactly the rename and required parent durability work before rename, without double charging; the publication primitive already prices its binding rechecks.
- **Opening/no-op:** B_open covers custody, retained generation/pin/tree base, expected record, one retained shared buffer, full traversal and file/link verification, and the capability’s compile-time CAP representation. The ordinary preexisting-generation no-op uses this recipe and never continues a failed publication attempt.
- **Transfer:** only component descents below the retained base, the file open/status and its read-attempt envelope are new costs. The buffer is retained from B_open. Sink-side work belongs to its existing owner, and no sink commit precedes verification.

The uniform fopen price and explicit finite buffers/attempt counts make the choices auditable. desc prices stream/stack/name setup separately from listing reads; implementation cannot silently add listings, metadata buffers or extra retained representations and still claim the published bound. Checked arithmetic, actual pre-operation charges, a single caller scope and the independent CI-T22 enumerator remain mandatory. Exact allocator/RSS measurements are not required. Native implementations and CI-T22/CI-T26 are future acceptance evidence, not tests executed by this review.

The handle discipline bounds simultaneous entry handles by path depth rather than entry count. It covers the store/stage/tree base, current directory stack and current entry, alongside the fixed archive/primitive-owned resources already priced by their rows. The 100,000-entry control should verify that bounded pattern, rather than interpret its shorthand as excluding those fixed handles. A supported filesystem may still refuse an open; its real I/O cause remains owned by the existing route.

**P-3 access mode:** selecting an appropriate regular-file handle before final chmod is compatible with the selected single fopen price and the required chmod-before-barrier order. The allowance is not permission for a failed readonly barrier to be retried through another handle; NBO-3 makes this implementation boundary explicit. The native barrier algorithm remains F_FULLFSYNC on macOS or fsync on Linux, without a new durability fallback.

## Non-blocking observations

### CI-R5-NBO-1 — Make the finalization walk’s source explicit

`docs/implementation/m3/component-install/PROPOSAL-r5.md:168`.

Step 4 prices a descent into tree/, one descent per committed directory, and each file open/mode/barrier, but it has no separate readdir row. This is implementable by driving post-order from the borrowed authenticated TreeCommitment while retaining the current parent stack. A fresh filesystem enumeration would instead require additional listing charges; descend_cost covers stream setup, not readdir calls. V1 and V2 already price their independent full filesystem enumeration.

Suggested change: State that step 4 is manifest-driven and performs no additional unpriced listing or per-entry parent-chain restart. If native enumeration is chosen instead, add its bounded rd term. In CI-T22, distinguish V1/V2 listing calls from finalization and verify the chosen traversal has exactly the priced descents.

### CI-R5-NBO-2 — Restore the standalone definition of record length R

`docs/implementation/m3/component-install/PROPOSAL-r5.md:124`.

The r5 edit removes r4’s paragraph defining R, although the arithmetic paragraph still points to its definition below and both recipes use R. The closed generation.json schema and authenticated association fields remain present, so the intended quantity is clear, but the explicit pre-acquisition canonical-length derivation should remain in the current operative text rather than only in superseded history.

Suggested change: Restore R as the exact canonical byte length of item 5’s closed record derived from authenticated release/candidate fields, with escaped UTF-8 payload lengths and checked arithmetic computed before acquisition/allocation. Preserve the single owned expected record and bounded byte comparison.

### CI-R5-NBO-3 — Select the finalization handle access mode before the charged open

`docs/implementation/m3/component-install/PROPOSAL-r5.md:216`.

P-3 allows opening read-write where a read-only handle cannot support the selected metadata/barrier operation. This is compatible with the one-open fopen price when access mode is selected by the qualified platform behavior before opening the staging file. Trying read-only, failing after chmod, and then reopening read-write would add unfunded calls, violate the failure latch/no-retry discipline, and may fail because the file is already 0400/0500.

Suggested change: Describe this as advance platform-specific access-mode selection for regular files, before their final chmod, with the chosen handle retained through the barrier. Keep directory handles on the supported directory-open path. A native chmod/barrier failure ends the act; it does not trigger a retry or a durability fallback. Have CI-2’s native controls record the selected mode and one-open sequence.

## No-regression disposition

No further regression identified in rounds 1–4’s accepted selections. Same-parent sibling staging, exact generation-name exclusion and bounded fenced GC of inert stages remain intact. V1/V2 stay distinct from the strict production retained-tree constructor. Final metadata precedes its own barriers, bottom-up, and the store’s publication barrier stays under the fence. LostRace/NotPerformed end the act; uncertain publication remains uncertain and is resolved by full later verification, never rollback, automatic replacement or retry. The installer performs no cleanup on a latched ledger.

Full authenticated TreeCommitment verification still covers paths, types, symlink text, installed modes and regular-file lengths/digests, with association metadata carrying no independent authority. Owner-only usable modes, no symlink chmod, no-follow offline archive input, the same-octet profile-1 digests, the closed host-token lookup and pinned narrow archive-profile adoption remain unchanged. The borrowed candidate is not admitted authority; pins span fenced admission and handoff, ephemeral reads create nothing, and missing/invalid pin.lock refuses rather than recreating it. Run retention owns every required preimage before origin release; replay remains separate from current-trust pivot resolution.

Pre-acquisition bound excess/overflow retains the admission route; in-operation charge/reservation failure retains law 468’s operational Budget route before rename. RTC committed-Run and X-8 required-cell gates, no dropped cells/placeholders or ephemeral detail, fixture predicate and existing trust/signing authority remain preserved. Interim snapshot-profile selection remains finite policy under the owned X-CI-1 disposition, not release-census coverage or qualification. No new public code, root/key, network acquisition, update/migration policy or qualification is accepted here.
