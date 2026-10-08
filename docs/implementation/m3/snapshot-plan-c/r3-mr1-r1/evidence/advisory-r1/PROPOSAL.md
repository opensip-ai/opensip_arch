# R3 owner file manifest: proposed selection and implementation gates

2026-10-08. Unaccepted lead proposal. No repository mutation, contract successor, product implementation, owner assent or gate closure follows from this packet. R3 remains open. Closed NIJ-1 and O1 units remain closed.

## Recommended membership

For an actually admitted snapshot-member owner, select the complete retained sealed snapshot sourceInventory as the conservative file dependency set. Each owner in that snapshot receives the same file-set digest. This asserts dependency sensitivity, not exclusive ownership of every file. It intentionally includes nested packages, workspace-shared configuration and unrelated retained files; an unrelated retained edit can invalidate prepared output. It neither expands the snapshot walk nor reads anything new. A symlink, special file, pruned tree or outside-snapshot input cannot be added to this set by a caller. Files in the already admitted TypeScript read set are included if and only if present in that snapshot sourceInventory. Rust dependency bytes remain with DependencySourceSetV1 and its separately checked inputBinding dependencySourceSetId.

For an actually admitted dependency-closure-member owner, select that one package's complete retained dependency file manifest, before virtual mount-prefix rewriting. Paths are the package manifest's admitted relative logical paths. Preserve all admitted members; a checksum metadata file is included exactly when the admitted manifest includes it. Do not independently read or reinterpret vendor metadata at this stage. An in-snapshot path package admitted as a dependency owner uses the dependency package manifest, not a heuristic snapshot subtree. Security chooses the admitted source; equal content cannot transfer an owner between sources.

Owner admission remains indispensable. A string key or equality to a claimed file digest never establishes source membership. The host must retain a unique admitted owner-to-snapshot-package or owner-to-dependency-package witness. This proposal does not invent that missing package/owner codec: its exact identity, mapping, source conflict disposition and failure routes must be published before implementation. An empty admitted map makes the requested owner unavailable; it does not silently select another owner or authorize dropping an activated package.

## Recommended byte recipe

Propose the canonical preimage to be the ordered array of closed rows `{path,contentSha256,byteLength}`, with no wrapper and no newline. `path` is the existing logical path, contentSha256 is lower-case raw SHA-256 of the exact retained file bytes, and byteLength is their exact uint64 length. Rows are strictly ascending by UTF-8 path bytes and unique by path. Admission checks ordering and uniqueness before hashing; canonical encoding never repairs them. Snapshot Blob rows map exactly path->path, sha256->contentSha256 and bytes->byteLength. Dependency manifest rows preserve all three values exactly.

Use the already published identity-and-evidence section3 canonical JSON encoder: UTF-8 key order, ordinary integer spelling, no Unicode normalization or whitespace, exact escaping and existing descriptor/depth limits. The raw SHA-256 of this exact array is the proposed ownerFileManifestSha256. Retain those exact canonical bytes and their byte count with security's admitted owner witness. No ProjectId, snapshotId, dependencySourceSetId, ownerKey, sourceId, timestamp, acquisition path, pid or RequestId enters this file-set preimage. Those membership and context joins stay in the owning records. Thus a fresh ephemeral ProjectId alone does not force a changed file-set digest.

The dependency file-manifest identity remains H(native.dependency-file-manifest.v1, this array). The owner digest is raw SHA-256 of the same array under this proposed selection: these are two explicitly different digest recipes over one preimage, not equal digest strings. ownerSourceDigest remains raw SHA-256 of the canonical sorted security owner-row array, a third preimage. The exact conversion is allowed only after verifying the retained canonical array; hashing a domain identity string is forbidden.

The existing snapshot and dependency population/count/byte bounds still apply. The canonical descriptor bound also applies to this independently retained preimage, including at exactly the cap; one byte over refuses without truncation. This may reject a source population whose own descriptor was admitted. The final successor must assess that additional capacity boundary against effective L and publish its actual existing failure composition; this packet grants no new budget or broad error code.

## Staleness and compatibility

An edited admitted row, inserted/deleted path or changed retained path spelling changes the preimage and invalidates a prior prepared inputBinding. Equal files under a newly admitted owner retain the file-set digest, but the owner key, source, dependency set, toolchain and cfg joins are still checked separately. A different sourceId with identical bytes does not reuse an owner admission. Historical owner manifest bytes and records retain their historical selected recipe/schema; they are never rewritten to this prospective preimage or automatically admitted to a new Plan.

## Why this selection

Selecting only a Cargo package subtree needs new precise rules for workspace-shared files, nested packages, declared paths outside the package and build-script reads. Hashing Cargo metadata alone misses source bytes. Compiler-traced reads launch code before the M3 Plan and O7 decision. Whole admitted snapshot membership avoids guessing those rules and preserves conservative staleness. Its cost is more false stale results and a possibly stricter descriptor capacity boundary. If that cost is unacceptable, a tighter dependency-membership contract is required before choosing a smaller set.

## Required publication and owning controls

The complete R3 successor must publish this membership/recipe selection, a closed retained preimage schema and exact authority/passage selectors, the single security-owned library function and harness call, owner admission/PackageKey codecs, real provenance-aware failure routes and capacity consequences. R3/C3c do not unblock from this packet alone.

Controls owed: identical snapshot file sets with different ProjectIds preserve the file-set digest; unrelated retained edits make prepared output stale; package siblings and shared configuration edits are included; excluded symlink and target bytes remain excluded; equal package bytes under conflicting sources do not confer admission; snapshot/dependency row projection is exact; raw and domain hash confusion refuses; missing/corrupt retained witnesses keep their more specific owners; reverse order/duplicate paths/bad lengths reject before hashing; exact and one-over descriptor bounds; a caller's subset and injected outside file both reject; actual library/harness parity and current prepared inputBinding stale refusals. These are proposed control requirements, not passing product results.

O7/D3/D13 owner packets, effective L/S-M, mount/source collision and virtual OUT_DIR codecs remain separate pending gates. No execution, measurement, qualification or project completion is asserted.
