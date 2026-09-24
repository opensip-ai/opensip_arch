# ACL omission premise for external ancestors — proposal 458

2026-09-23. Claude Opus 5.5, implementation lead. Proposed owner amendment to initial-root-binding owner §1a step 4 and §1b. Not selected until an ACCEPT from the reviewer; not code; not creator authority.

## Problem

Owner §1b requires, for H and every external ancestor, "readable ACLs and no ACL write grant to any other principal". §1a step 5 admits the whole root-to-H chain. The bounded capture keeps three states apart: omitted, NOACL sentinel, and present. Omission is not evidence of absence (root source findings 445; route 446). Probe 457 shows `/` and `/Users` omit the ACL on a stock Mac. Without a stated premise the creator can never admit the chain. Refusing forever is not product completion (source findings 445: "conservative refusal alone is not product completion").

## Measurements on this host

Probe 457 and its follow-up (docs/implementation/m2/ancestor-acl-probe-457/RESULT.md) on APFS:

| Object | Capture state |
|---|---|
| `/`, `/Users`, `/private`, `/private/var`, fresh directories | NotReturned |
| H, Library, Application Support (stock deny-delete) | Entries(1) |
| Fixture with one entry added | Entries(1) |
| Same after `chmod -N` (ACL removed) | NotReturned |
| Same after `chmod -a` of its only entry | Entries(0) |

So on this APFS host, omission follows "no ACL stored", and a stored empty ACL is reported separately as Entries(0). This is one host and one kernel build. It is not qualification.

## Proposed law

1. **Required fact.** For each external ancestor, no principal other than the invoking user or root holds an ACL grant of any right outside list, search, read attributes, read extended attributes, read security and synchronize. Inherit-only allows count.
2. **Evidence A (unchanged).** A present ACL from the bounded capture of the original retained descriptor, judged by `check_external_ancestor`.
3. **Evidence B (new).** An omitted ACL from the bounded capture of the original retained descriptor counts as a present empty ACL only when all of the following hold:
   - the same descriptor's filesystem sample (the existing `DescriptorFilesystem` from `fstatfs` on that descriptor) is local, not union, and its type name is in the admitted platform entry's `installRootFilesystems`;
   - that platform entry comes from an `InitialPlatform` receipt of the same `InitialInstallationAttempt`, under a measured profile row that matches the observed boot (build, kernel UUID, dyld cdhash) with no platform-decision refusals;
   - the omission premise is consumed through a private, non-Clone receipt minted only by that `InitialPlatform` owner and bound to the attempt. A caller cannot construct it.
4. **Forbidden substitutes.** The NOACL sentinel stays a refusal. A volume capability bit, a successful syscall, the legacy writer list, a caller-supplied filesystem name, an unsigned profile fixture, and omission on a filesystem outside `installRootFilesystems` do not establish the fact.
5. **Scope.** Evidence B applies only to external-ancestor writer exclusion (§1b first sentence), on the root-to-H chain and the reused `Library` and `Application Support`. It does not apply to `OpenSIP`, final I, or any private descendant. Those keep "omission is a refusal" and the creator's explicit zero-rights owner allow. It does not apply to project roots, operational files or any existing custody consumer until that owner adopts it separately.
6. **Qualification obligation.** Each measured macOS profile row that lists `apfs` in `installRootFilesystems` owes, at release qualification, the fixture set above: fresh object omitted; one added entry present; `chmod -N` omitted; last entry removed present-empty; and root-owned `/` and `/Users` read with the bounded capture. A row that fails refuses Evidence B. No schema member is added: the premise is part of what `installRootFilesystems` already qualifies. Linux remains unavailable for creation as the owner already says.

## What this changes and does not change

It adds one admissible evidence path, owned by `InitialPlatform`, for one fact. It does not change the profile schema, the platform decision, the private-descendant rule, the NOACL treatment, or any existing custody consumer. The legacy writer-list reader still reads omission as no writers; replacing it in the existing custody chain is separate owed work.
