# Component installation law CI r1 review

**Verdict: REQUIRED-FINDINGS — six required findings, one non-blocking observation.** This review accepts no implementation, binding or qualification.

## Subject and scope

The 579-byte manifest hashes to `3a055f6d23ffc5b5580ec21d40261b1ff41213f874126aab624ae0c3942c42d8`. Both members match:

| Member | Bytes | SHA-256 |
| --- | ---: | --- |
| `component-install/PROPOSAL-r1.md` | 27330 | `286ebf5af6d443260211848417159c021dce817995df223b22ebf4aa372589ba` |
| `snapshot-plan-c/c2a/X-C2A-1-r1.md` (input memo only) | 6036 | `3f0cd8fd7f8c5ea59bf5795487f8785ca60e7d2e8428f75730bdb2bd043fedd3` |

Bases are product `b7538549b727e13013f36d3b7c2e2917e767f3f2` and architecture `a87c1234b26544e65cd2d36b613f218da41b4e86`. PKG's full SHA-256 independently matches `8321d527843c63592d8e4fd49c3df0ace690da0bcbcd1e268464e578fe30424c`.

Only read-only source/authority inspection, hashing and JSON parsing were used. No build, test, lane/lock, network, delegation, installation, private fixture/key, held tree/store, T2 cache or held-out material was accessed. Only REVIEW.md and review.json were written.

## Required findings

### CI-R1-RF-1: Verify the full committed filesystem tree, not only identity Blobs

`docs/implementation/m3/component-install/PROPOSAL-r1.md:100`

Item 5 promises refusal on extra/missing entries, but item 6 accepts only closure2 and the regular-file Blob list and only iterates those Blobs. That cannot detect an extra file, a missing empty directory, or a changed committed symlink target/type/mode. Directory and symlink metadata were deliberately excluded from identity Blobs; their authority remains the authenticated manifest TreeCommitment. A changed analyzer entrypoint symlink can therefore escape this proof even though every regular-file Blob still hashes correctly. TreeReadFailure also has no structural-tree mismatch case.

Required change: Carry the authenticated selected-platform TreeCommitment into the read capability and perform bounded no-follow enumeration/association of the complete installed tree. Check exact paths, types, symlink text and the selected installed-mode policy, rejecting extras and missing entries without trusting generation.json as authority. Verify record/candidate/manifest association explicitly. Add structural mismatch failures and controls for an extra regular file, a removed empty directory and a changed symlink target, including a symlinked analyzer entrypoint.

### CI-R1-RF-2: Define usable staged and published modes for every admitted entry type

`docs/implementation/m3/component-install/PROPOSAL-r1.md:28`

Clearing write bits alone does not ensure that the installer or retained-tree reader can access an admitted tree. CM permits 0000 modes and closure-only entrypoints need only be regular files. A file mode 0200 becomes unreadable 0000; a directory mode 0600 becomes untraversable 0400. Finalizing ordinary directories to 0555 before adding children also prevents staging writes. Further, symlink mode application/clearing is not a portable filesystem operation across the four selected platforms. Item 1 promises every row is applied this way without a refusal or representation rule for these cases.

Required change: Choose an explicit installed-mode policy by entry type, separate from the authenticated archive mode. Define temporary staging permissions and bottom-up finalization after population/verification. Either select lawful private read/traverse permissions or reject unmaterializable modes with an owned typed delivery refusal; do not silently grant execution. Specify the symlink-mode treatment without following its target. Keep generation/store custody directories 0700 as required by the cited primitive, and add unreadable-file, untraversable-directory and nested-staging controls.

### CI-R1-RF-3: Specify durable publication and crash recovery before claiming complete published generations

`docs/implementation/m3/component-install/PROPOSAL-r1.md:73`

The transaction specifies stream writes, verification and exclusive rename, but no file/directory barriers or recovery treatment for uncertain publication. Verification proves bytes seen in memory, and rename provides namespace atomicity; neither ensures file data and generation.json survive a crash with the published name. The assertion that a crash between publish and step completion is safe because verification preceded rename is therefore unsupported. Existing platform file/directory barrier and exclusive-publication primitives do not supply ordering unless this law selects it.

Required change: Define the durable sequence for payloads, metadata/modes, generation record, staging directories and the publication parent using the accepted native barrier/publication primitives. Define outcomes and recovery for failures before rename and after a rename whose durability is uncertain, preserving existing generations and forbidding automatic replacement/retry. Add crash-prefix controls through the post-rename barrier, not only before publication.

### CI-R1-RF-4: Make retained-byte transfer, pin lifetime and replay ownership concrete

`docs/implementation/m3/component-install/PROPOSAL-r1.md:101`

retained_tree hashes bytes and returns only an opaque list of verified Blobs. It provides no bounded transfer/stream/held-byte interface for C2a or the Run owner to retain those exact bytes. Its signature also carries no operation/pin capability or lifetime, although item 7 requires a generation to stay pinned from the pre-draw read until lease end; ephemeral use and the fence-to-lease transition are unspecified. Item 7 then mixes retained-Run replay with WS:293 pivot resolution and pivot-detector-unavailable, even though a complete Run must retain its own preimages under IE:1399-1412 and NE:1493-1499.

Required change: Define a retained capability or bounded verified-byte handoff, with custody/observation checks, through which the owning retention path copies/pins the complete descriptor, manifest body and file bytes. Define pin registration/acquisition under the fence, continuity through R11 and operation end, and ephemeral lifetime/release, so GC cannot remove a generation in a gap. A completed Run may release the installed origin only after its own complete retention is established. State that ordinary Run replay uses those retained preimages and keeps its evidence-missing/corrupt failure semantics; WS pivot discovery/current-trust execution is a separate operation. Never accept a historical hash-only proof as present retained bytes.

### CI-R1-RF-5: Preserve the required-cell and committed-Run gates on the not-installed route

`docs/implementation/m3/component-install/PROPOSAL-r1.md:135`

Item 8 labels its table retained reads at R10a, then unconditionally gives a durable NotInstalled result COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED. R10a precedes the analysis ExecutionId/Run. MC item 7:435 admits that durable detail through a committed Run and expressly records X-8 at :436: a required non-inventory cell currently has no lawful unavailable binding. CI cites item 7 but drops that gate. A pre-draw read result is not itself a committed durable analysis termination, and this law cannot invent the missing binding or detail authority.

Required change: Keep NotInstalled as a typed input to the existing availability/selection/composition owner. Explicitly carry X-8 and its successor gate before required-cell end-to-end composition; qualify the durable detail by RTC committed-Run authority. Specify the pre-draw propagation without minting a placeholder closure/context, silently dropping cells, or adding ephemeral detail. Retain the separate missing/corrupt promised-tree causes and the existing registered operational routes.

### CI-R1-RF-6: Bound installer work as well as signed archive length

`docs/implementation/m3/component-install/PROPOSAL-r1.md:60`

The signed entry/file limits and exact archive length bound accepted payload octets, but item 4 supplies no work scope/profile or charge discipline for archive acquisition, header processing, staging writes, directory/link creation, verification and failed-stage cleanup. Only the later retained reader has one. Signed size alone does not bound repeated interrupted/short I/O attempts, temporary allocation or cleanup work. Deferring R10a's reader profile to D4/J1 does not select a resource policy for the separate fence-only install command.

Required change: Give CI-1/CI-2 explicit finite caller work accounting and an owned installation profile selection, or a named gate before the installation implementation can be accepted. Price reads/writes/attempts, allocations, extraction and cleanup before each operation, propagate typed exhaustion without publishing a partial generation, and state the failure route. Keep signed capacities distinct from work limits and disk-space failure; no arbitrary archive-size constant is required to resolve this finding.

## Authority, scope and sound portions

The lead may propose this missing delivery law as DR-103's delivery owner; the input memo was a request for that work, not prior approval of its choices. One platform/release per transaction, no dependency resolution, no network acquisition, no update/migration implementation and no implicit repair are appropriately narrow. The design fills a real gap between signed metadata and installed bytes, but the incomplete reader/retention/publication rules above prevent it from closing that gap yet.

LD-CI-1 is a coherent explicit selection for this uncompressed profile: artifact octets equal archive octets, so both digests have the same raw-byte subject and a split refuses. The existing catalog shape supplies fields but not this new equality interpretation; implementation must treat it as this law's rule, not silently reinterpret another profile. Trust verification remains the ordinary reader's, with the body/envelope/catalog/preimage association intact.

The pinned PKG-AP selection is sufficiently exact for a pure codec: header octets, mask/checksum, types, ordering, field capacities, payload/padding, trailer and bijection are defined. Capacity refusals before acquisition correctly distinguish admissible metadata from deliverability by profile 1. The listed byte/path/entry bounds are supported by CM and PKG-AP. A hand-written fixed-profile parser can avoid a new third-party archive dependency. That does not by itself settle internal crate edges: lifecycle currently depends on platform and identity, while ClosureCandidate and the selected custody primitive belong to security; the implementing plan must name the lawful bridge/edge rather than assert an existing lifecycle/security API.

The local regular-file handoff, existing-generation preservation, non-generation staging namespace, exclusive publication intent and current-trust checks are correct directions. No-follow reads and private generation/store custody are also appropriate. The cited custody primitive specifically requires a 0700 directory owned by the invoking user and no foreign ACL grant; it explicitly does not exclude the invoking user's own processes or root. Clearing mode bits and a private directory should not be described as enforcing exclusive installer access against those processes. Retained-read verification remains necessary, including on reuse of an existing generation.

The registered vocabulary contains EXTENSION.ADMISSION_REJECTED, EXTENSION.INSTALL_IO_FAILED with extension-install-io, HOST.IO_FAILURE and the existing missing/corrupt delivery details. No new public code is needed for the proposed internal diagnostics. The implementation must still derive full schema-valid terminations/error details and preserve actual provenance; registration of a code is not proof of every proposed placement. RF-5 identifies the pre-draw unavailability problem.

The proposed unit order is sensible once the input/custody interface is complete: codec, store/transaction and reader, then C2a binding and command composition. The same installer/verifier for synthetic fixtures under exactly the joint fixture predicate is appropriate; no new root, key, feature or shortcut is authorized. Add the structural-tree, modes, crash-prefix, byte-transfer/pin and budget controls required above to CI-T1–T16.

## Question rulings

**Q1.** No additional total-byte constant is inherently required by the profile. Signed length/count capacities must be combined with finite installer work/allocation accounting and an owned profile/refusal gate (RF-6); ENOSPC alone is insufficient resource control.

**Q2.** Accept the closed S8 machine-id-to-existing-artifact-token lookup for artifact selection. The alias must never become an admitted machine platform/profile/grant id. This lookup alone needs no catalog schema successor; it does not authorize aliases in other admission records.

**Q3.** Accept an operator-supplied local regular-file input at the library boundary, leaving CLI spelling to J1. Keep no-follow descriptor capture, exact byte/digest checks and no network acquisition; select explicit bounded work and failure handling.

**Q4.** A completed Run need not pin the installed origin if it already owns every required preimage independently. Require a concrete protected transfer/pin handoff and preserve Run replay semantics; do not replace mandatory retention with future pivot-origin lookup or pivot-detector-unavailable (RF-4).

**Q5.** No new public code/detail is needed merely for profile/capacity/digest refusals; the existing rejection and installation-I/O families are appropriate. Publish exact derived carriers/remedies and a budget route, and preserve RTC/X-8 composition gates for NotInstalled (RF-5/RF-6).

**Q6.** Accept adoption of exactly the pinned archiveProfile algorithm by reference. That is an explicit new selection here, not evidence PKG or DR-120 was already applied. Preserve the exact dependency pin and leave all other PKG members, release/adapter qualification and DR-120 standing unchanged.

**Q7.** Do not accept write-bit clearing as the complete reconciliation. Separate authenticated archive metadata, staging permissions, installed read/traverse/execute requirements and symlink treatment; resolve unreadable/untraversable admitted modes explicitly (RF-2).

## Non-blocking observation

### CI-R1-NBO-1: Match the profile control list and distinguish codec limits from manifest admission

`docs/implementation/m3/component-install/PROPOSAL-r1.md:158`

The pinned PKG-AP goldenAndNegativeCases array has 15 entries, while CI-T1 calls it 17. Its mode-field maximum exceeds CM's admitted 0777 range, and some size-limit cases are explicitly metadata-only; they should not be presented as complete signed-installation positives.

Suggested change: Use the exact pinned case list and label pure codec/metadata-capacity controls separately from feasible manifest-valid installation controls. Also require an existing-generation no-op to validate custody and promised bytes before reporting a usable installed release; existence alone must not bypass LD-CI-8.

