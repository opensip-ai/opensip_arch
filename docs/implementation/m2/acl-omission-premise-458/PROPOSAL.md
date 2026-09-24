# ACL omission premise for external ancestors — proposal 458 r2

2026-09-23. Claude Opus 5.5, implementation lead. r2 answers Grok r1 RF-1: a filesystem type name does not qualify this fact; the matched measured row must carry it. r1 bytes are preserved in PROPOSAL-r1.md. Proposed owner amendment to initial-root-binding owner §1a step 4 and §1b. Not selected until an ACCEPT from the reviewer; not code; not creator authority.

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
   - `InitialPlatform` itself took the same descriptor's filesystem sample (`fstatfs` on that descriptor). It is local, not union, and its type name is in the admitted platform entry's `installRootFilesystems`. A caller-built `DescriptorFilesystem` is never an input.
   - The admitted platform entry comes from an `InitialPlatform` receipt of the same `InitialInstallationAttempt`, and the measured profile row that matches the observed boot (build, kernel UUID, dyld cdhash) has no platform-decision refusals.
   - That matched row carries the explicit qualification member `installAclOmission` with the value `"no-acl-stored"`. The release signs that member only after the row passed the fixture set in item 6 for that boot identity. A row without the member, or with any other value, refuses Evidence B. Membership of the type name in `installRootFilesystems` is never enough.
   - The premise is consumed through a private, non-Clone receipt minted only by that `InitialPlatform` owner, bound to the attempt, and citing the matched row. A caller cannot construct it.
4. **Forbidden substitutes.** The NOACL sentinel stays a refusal. A volume capability bit, a successful syscall, the legacy writer list, a caller-supplied filesystem name or sample, an unsigned profile fixture, a type name in `installRootFilesystems` alone, and omission on a filesystem or boot whose row lacks the qualification member do not establish the fact.
5. **Scope.** Evidence B applies only to external-ancestor writer exclusion (§1b first sentence), on the root-to-H chain and the reused `Library` and `Application Support`. It does not apply to `OpenSIP`, final I, or any private descendant. Those keep "omission is a refusal" and the creator's explicit zero-rights owner allow. It does not apply to project roots, operational files or any existing custody consumer. Unit 461, which stops the legacy "omission means no writers" reading, does not gain Evidence B.
6. **Qualification obligation.** Before a release signs `installAclOmission: "no-acl-stored"` on a measured macOS row, that row's boot identity must pass, with the bounded capture: fresh object omitted; one added entry present; `chmod -N` omitted; last entry removed present-empty; and root-owned `/` and `/Users` captured. A failing or unmeasured row carries no member. Linux remains unavailable for creation as the owner already says.
7. **Profile-law successor.** The member is new signed profile law. The macOS measured-row shape (`build`, `kernUuid`, `dyldCdhash`, `lane`) is closed today, so adding `installAclOmission` needs a reviewed profile-set schema successor with its decoder, shape cases and signature fixtures. Until that successor is selected and a signed row carries the member, Evidence B cannot be minted and omitted ancestors refuse. The existing rows and schema bytes are preserved.

## What this changes and does not change

It adds one admissible evidence path, owned by `InitialPlatform`, for one fact, and names the profile-schema successor it needs. It does not change the existing profile schema bytes, the platform decision, the private-descendant rule, the NOACL treatment, or any existing custody consumer. The legacy writer-list reader still reads omission as no writers; replacing it in the existing custody chain is separate owed work.
