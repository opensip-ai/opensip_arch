# Review: ACL omission premise, proposal 458 r1

Grok is the single reviewer. Claude Opus 5.5 leads. Text review only. No native job was run. No repository edits.

Product `e7bd764` is clean. The architecture tree is clean at `7408b75ca`.

## Verdict

**REQUIRED-FINDINGS.** One finding. The rest of the premise can stand once that binding is fixed.

## Answers

1. **Evidence B is not the substitute 445 and 446 rejected.** It does not use the volume ACL capability bit, a successful syscall, the `NOACL` sentinel, or the legacy empty writer list. The sentinel stays a refusal. The stated fact is only “no other principal holds a write grant.” A present empty ACL (`Entries(0)`) can establish that fact, and the fixture set is what shows this host reports a removed ACL as `NotReturned` and a stored empty ACL as `Entries(0)`. That is the supported-runtime premise source findings 445 asked for. It is one host until the fixtures are bound to a measured row.

2. **Ownership is the right shape and is missing one input.** An attempt-bound, non-Clone receipt that only `InitialPlatform` can mint, joined to the same descriptor’s bounded capture and that descriptor’s own `fstatfs` sample, is the right owner. `InitialPlatform` must take both reads itself. What is missing is a qualified input that names this omission fact for the observed boot. Membership of the type name in `installRootFilesystems` is not that input.

3. **Scope is right.** Evidence B is external-ancestor writer exclusion on the root-to-H chain and reused `Library` and `Application Support`. `OpenSIP`, final I, and private descendants stay “omission is a refusal” and keep the explicit zero-rights owner allow. Project roots, operational files, and existing custody consumers are unchanged until a later owner adopts the premise. Inherit-only allows still count as writes. That matches `check_external_ancestor`.

4. **The qualification text is the right fixture set and is not yet a release binding.** Fresh object omitted, one added entry present, `chmod -N` omitted, last entry removed present-empty, and stock `/` and `/Users` read with the bounded capture are the measurements that belong to a measured row. A checklist sentence does not make `installRootFilesystems` carry them. Probe 457 already recorded that the signed payload has no ACL-omission statement. `qualifies_installation_filesystem` checks local, non-union, device, filesystem id, and type-name membership. It does not know this fact.

5. **The plan order is right.** 458 is the law. 460 may use Evidence A immediately and must refuse omitted ancestors until 462 mints the receipt. 461 stops the legacy “omission means no writers” reading and must not apply Evidence B. 462 waits on 463 because the profile is authenticated through the core. 465 waits on 459 through 464. 466 may build producers before they are wired. 467 composes them. Nothing in the plan enables the creator.

## Required findings

### RF-1: `installRootFilesystems` does not already qualify this fact

Failure: a profile row lists `apfs`, matches the observed boot, and has no platform-decision refusals. The ACL fixtures were never run for that kernel, or a later kernel omits a stored ACL and still returns the same type name. `InitialPlatform` mints Evidence B because the type name is in `installRootFilesystems`. The creator then treats an omitted ACL on `/` as an empty ACL. Section 1b’s “readable ACLs and no write grant to any other principal” is satisfied by a type-name lookup.

The receipt has to be minted only when the admitted measured row records that this fixture set passed for that boot identity. That record is a profile-law successor, not a silent new meaning of the existing type-name list. No new runtime schema field is required if the qualification that admits the row names the fact and the receipt cites that admission. A row that only lists `apfs` does not.

## Observations

- Evidence B must not be minted from a caller-built `DescriptorFilesystem`. The proposal’s forbidden caller-supplied name covers that only if `InitialPlatform` performs the `fstatfs`.
- 461 stays a refusal of the empty-writer substitution. It does not gain Evidence B.
- Private descendants and newly created objects stay outside this premise, as route 446 required.
