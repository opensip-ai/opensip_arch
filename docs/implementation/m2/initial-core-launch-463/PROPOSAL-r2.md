# Executing core identity for the initial creator — proposal 463 r2

2026-09-23. Claude Opus 5.5, implementation lead. r2 answers Grok r1 RF-1 (the bootstrap directory was located through the inventory inside it) and adopts the r1 answers on custody and K. r1 bytes are preserved in PROPOSAL-r1.md. Proposed owner amendment for initial-root-binding owner §1a step 3 (`InitialCore`). Not selected until the reviewer accepts it. Not code, not creator authority, and no change to any selected record shape.

## Problem

Owner §1a step 3 requires the executing core's identity and closure "through the existing native launch/loaded-image owner and OS loader TCB, not argv[0], PATH, a later path reopen, caller descriptors or records found inside I", then open-then-verify of every executed member (security-completion v8 §3.3). The product has no such owner. It has verifiers for the signed release records (`core_anchor::capture`, `core_authentication::authenticate`, `core_inventory::project`) that read a supplied record store, and it embeds no release data. `opensip version` prints empty closure IDs. So there is no native producer, and the owner's word "existing" names nothing. This proposal states the facts the producer must establish, its evidence, and the forbidden substitutes. It ends at facts; the byte-level layout is left to the implementation unit and its tests.

## Required facts

1. **Executed image.** The process's main executable image, as the kernel validated and mapped it, is the entrypoint member of one platform entry in an authenticated core inventory.
2. **Authenticated release.** That inventory, its anchor, bootstrap manifest and profile binding are authenticated from the root embedded in the executed image, along the release-declared ordered root chain, never by choosing a "latest" file.
3. **Closure and K.** The core closure is the inventory's closure identity. K is derived from the release's declared state-schema writer capability (owner step 3), never from a decoder capability or a default.
4. **Every executed member.** Each other member the invocation executes or loads is verified on its own opened descriptor against the same inventory before use. The creator launches no helper, so for the creator this is the entrypoint alone.

## Evidence (macOS)

- **Kernel identity of the running image.** `csops(getpid(), CS_OPS_STATUS)` must report the code-signing flags the admitted release profile requires (at least CS_VALID; a notarized release also requires hardened runtime and kill-on-invalid). `csops(getpid(), CS_OPS_CDHASH)` gives the 20-byte CodeDirectory hash of the main executable as the kernel validated it. These are kernel observations of the executed image. No path, argument or environment value contributes.
- **Byte owner, open-then-verify.** The kernel's executable path for this process (`proc_pidpath`) is used only to open a descriptor, with no-follow on each component and custody checks on the containing tree. From that descriptor: bound and read the file; locate the slice for the running architecture; compute its CodeDirectory hash with the same parser the loader measurement already uses; require equality with the kernel hash; and require the file's SHA-256 and length to equal the inventory's committed entrypoint bytes. A renamed or substituted file fails either the kernel-hash equality or the inventory commitment. The path is a locator, never an identity.
- **Release records, located without the records.** The image embeds, at build time, two values: the root binding (schema, version, digest) and the logical path of the core tree's embedded bootstrap directory, relative to the tree root that contains the entrypoint. A path is not a digest, so the digest cycle stays closed. From the retained tree handle the producer opens only that relative directory, then only its fixed `payload.json` and `payload.sig.json`, then only the paths the authenticated bootstrap manifest's root chain declares, each with no-follow opens. It never lists a directory and never selects a file by name order or "latest". The anchor, inventory pair, manifest and envelope are then authenticated by the existing `core_anchor::capture` and `core_authentication::authenticate`, starting from the embedded root binding. The authenticated inventory's `embeddedBootstrap.directory` must equal the embedded path.
- **One platform row.** The platform row is the single row whose platform id equals the authenticated profile's platform id for this boot (`InitialPlatform`). The opened entrypoint's relative path, SHA-256 and length must equal that row's entrypoint commitment. Rows are never scanned for a matching file.
- **No circularity.** The image embeds only the root binding and the bootstrap path, not the anchor or inventory digest. The anchor commits to the inventory, which commits to the tree, which contains the image. The kernel-hash and tree-commitment joins close the loop.
- **Core tree custody.** The core tree is the executing core, not an external ancestor of I. Owner §1b and premise 458 do not apply to it, and `installAclOmission` is not reused. Every directory the entrypoint and bootstrap opens traverse, and every opened file, must be no-follow, have no group or other write, and grant no ACL write to any principal except the owner or root, judged from the bounded capture. An omitted ACL on that path refuses until a separate signed qualification for the core path exists. A symlink component on the kernel path refuses; there is no fallback to `current_exe` or to following the link.
- **Revocation.** The revocation context is the embedded authenticated context delivered with the closure. `authenticate` must not take a caller-supplied empty revoked set. That signature change is part of the implementation unit.

## Forbidden substitutes

argv[0]; PATH; `std::env::current_exe()` as identity; a path reopen whose bytes are not joined to the kernel CodeDirectory hash; a record found by directory enumeration or by name "latest"; records inside I; a caller-supplied revoked set; an unsigned or test-signed release outside `#[cfg(test)]`; a build-time closure string without the authenticated inventory; the loader measurement of `/usr/lib/dyld` standing in for the core's identity.

## Development builds

A build without an embedded root binding and a signed release tree has no `InitialCore`. It refuses with a stable detail, and the creator stays unavailable. Tests use test-signed fixtures only under `#[cfg(test)]`. This keeps the owner's rule that a reference model's eligibility label is a premise, not its implementation.

## K

K comes from a signed core-inventory member, or a record that member commits, naming the state-schema writer. No such member exists today: `stateSchema` appears only in store bindings and transition intents, and a decoder capability does not declare it. A release-record successor must add it. `InitialCore` then derives K=2 only when the admitted member names the stage-2 writer, K=1 only when it names the stage-1 writer, and refuses any other or missing value. There is no default.

## Qualification obligation

For each measured macOS row: `CS_OPS_CDHASH` equals the in-process parser's hash of the executed slice; a substituted file at the kernel path is refused; a file whose cdhash matches but whose SHA-256 differs from the committed entrypoint is refused; the code-signing flags the profile requires are present for a notarized release. Linux remains unavailable for creation until its own owner exists.

## Still owed by the implementation unit

The build-time layout of the embedded root binding and bootstrap path in the image; the exact code-signing flag set per profile; `authenticate` taking its revocation set from the embedded chain and refusing an empty caller set; the release-record successor for K; and a signed release tree and fixtures. Security.framework stays the qualification-only helper of security-completion v8 §8.3; the launch path uses only libSystem.
