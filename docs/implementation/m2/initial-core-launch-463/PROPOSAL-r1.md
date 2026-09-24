# Executing core identity for the initial creator — proposal 463 r1

2026-09-23. Claude Opus 5.5, implementation lead. Proposed owner amendment for initial-root-binding owner §1a step 3 (`InitialCore`). Not selected until the reviewer accepts it. Not code, not creator authority, and no change to any selected record shape.

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
- **Release records.** The anchor, inventory pair, bootstrap manifest and envelope are read from the core tree's embedded bootstrap directory, which the inventory names (`embeddedBootstrap`), through retained no-follow handles under the same tree. They are authenticated by the existing `core_anchor::capture` and `core_authentication::authenticate`, starting from the root binding embedded in the image at build time.
- **No circularity.** The image embeds only its root binding (schema, version, digest), not the anchor or inventory digest. The anchor commits to the inventory, which commits to the tree, which contains the image, so embedding the anchor digest would be circular. The kernel-hash and tree-commitment joins close the loop instead.
- **Revocation.** The revocation context is the embedded authenticated context delivered with the closure. `authenticate` must not take a caller-supplied empty revoked set. That signature change is part of the implementation unit.

## Forbidden substitutes

argv[0]; PATH; `std::env::current_exe()` as identity; a path reopen whose bytes are not joined to the kernel CodeDirectory hash; a record found by directory enumeration or by name "latest"; records inside I; a caller-supplied revoked set; an unsigned or test-signed release outside `#[cfg(test)]`; a build-time closure string without the authenticated inventory; the loader measurement of `/usr/lib/dyld` standing in for the core's identity.

## Development builds

A build without an embedded root binding and a signed release tree has no `InitialCore`. It refuses with a stable detail, and the creator stays unavailable. Tests use test-signed fixtures only under `#[cfg(test)]`. This keeps the owner's rule that a reference model's eligibility label is a premise, not its implementation.

## Qualification obligation

For each measured macOS row: `CS_OPS_CDHASH` equals the in-process parser's hash of the executed slice; a substituted file at the kernel path is refused; the required code-signing flags are present for a notarized release. Linux remains unavailable for creation until its own owner exists.

## Open questions for the reviewer

1. Is the kernel CodeDirectory hash plus the tree commitment an honest "loaded-image owner" for the entrypoint, given security-completion v8 §8.3 excludes Security.framework at launch?
2. Where must the core tree's custody chain be judged: by the external-ancestor rule of owner §1b (so it needs premise 458 for omitted ancestors) or by a separate core-tree custody rule?
3. No existing release record declares a state-schema writer capability: in the product trust-record schema, `stateSchema` appears only in store bindings and transition intents. K therefore needs a signed release-record successor (for example a core inventory member naming the writer schema) before `InitialCore` can derive it. Is that the right owner for it?
