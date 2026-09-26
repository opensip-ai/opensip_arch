# Review: profile-set ACL omission 458b r1

Grok is the single reviewer. Claude Opus 5.5 leads. Law review of `docs/implementation/m2/profile-set-acl-omission-458b/PROPOSAL.md`. No repository edits. No product cargo.

The proposal is 4707 bytes, sha256 `ce6551f7211cdafe8515de8cce40d394b32385cdd0a0e23d14f6b36ee96439fd`, matching `hashes.txt`. It is the profile-schema successor named by accepted law 458 §7. Evidence B stays with 462.

## Verdict

**REQUIRED-FINDINGS.**

## Answers

A new closed V2 with a reader opt-in is the right successor. `PlatformProfileSetV1` is closed at every level, `profileSetSchema` is const 1, and the design lock pins that schema bundle. An optional V1 member would edit those bytes and move the corpora. V2 copies V1 and changes two things: `profileSetSchema` const 2, and an optional `installAclOmission` const `"no-acl-stored"` on each macOS `measuredProfiles` row. Linux rows, `supportedMajors`, the platform object, and the top level stay closed. A V1 body that carries the member still fails `closed`.

The existing callers stay on the V1 path. `profile_shape` requires integer 1. `verify_profile_set` calls that check and digests domain `opensip.metadata.platform-profile-set.1`. That is the same opt-in shape as `CURRENT_ENVELOPE_READER`, whose `payload_schemas` are `[true, false]` and whose comment says existing callers do not opt into payload 2. The only V2 caller named here is `InitialPlatform` (462).

Those corpora keep their results on that path:

- `profile-shape-cases.ndjson` is 1963 rows. `type:profileSetSchema:2` is `valid: false`. `type:profileSetSchema:1` is the true row.
- `profile-signature-cases.ndjson` is 237 rows, all `standing: SYNTHETIC`. 234 are schema 1. The three schema-2 rows are the `signed-invalid-shape:wrong-schema` cases, and their expected object is `error`, not `admit`. The first admitted row is schema 1 and has no `installAclOmission`.
- `platform-admission-cases.ndjson` is 1084 rows, every `profileSetSchema` is 1, and none mention `installAclOmission`.
- `signed_profile350` and `signed_profile469` do not write `profileSetSchema`. They remain the schema-1 synthetic payload, with 469 adding supported major `"26"`.

The shape-const choice is right against 458's sentence. Absence of the member leaves the row a normal measured row and withholds Evidence B. A present member with any other value or type fails shape, so the whole set refuses. That set then has no admitted matched row, which refuses Evidence B. The same discipline already refuses `profileSetSchema: 2` as a document, rather than as a partial platform decision. A wrong const is not a second qualification value. 458's "any other value refuses Evidence B" is met. The absent-member case stays the one that can still admit the platform.

Keeping digest domain `.1` is sound. The canonical body contains `profileSetSchema`, so a V2 body and a V1 body do not share a digest. `CoreProfileBindingV2` has `schemaVersion` const 2 and `platformProfileSetBodyDigest` only. The V1 verifier still rejects a V2 body at `profile_shape` before that digest can satisfy a V1 pin. No trust-record field is added.

The matched-row accessor closes duplicate borrowing. `platform_admit` builds `{build: row}` in order, so the last row for a build wins, which is the same row `root_payload` selects with `rev().find` on `build`. Identity mismatch on `kernUuid` or `dyldCdhash` returns `REFUSE` with tier `EXACT-MEASURED`. A clean match returns `ADMIT`, tier `EXACT-MEASURED`, and that row's lane. Baseline returns `ADMIT` at `BASELINE-ATTESTED` with no measured row. The accessor may return `installAclOmission` only for a V2 set at `ADMIT`, `EXACT-MEASURED`, and no refusals, and only from that selected row. Evidence B cannot scan an earlier duplicate.

Decision 6 is honest. 458 §6 puts the member only on a measured row whose boot identity passed the fixture set. A baseline identity has no such row. This macOS 27 host under 469 is `BASELINE-ATTESTED`: the synthetic measured builds are `25G83`, and the host build `26A428` does not match them. Live-host tests of 462 sign a synthetic V2 profile at run time from the observed identity, with `standing: SYNTHETIC` and the public test seeds. They do not check in a measured development-host row. `AclOmissionPremise` still has only the test constructor, so production omission still refuses until 462.

## Required findings

**RF-1.** The contract successor's obligations omit the passage overrides for the sentences that name only `PlatformProfileSetV1`. Decision 7 lists a V2 schema, a reference that imports the pinned V1 model by hash, shape cases, and signed V2 cases. It does not amend:

- §S8 line 685, the machine-id key of the signed `PlatformProfileSetV1`
- §S8 line 711, what that signed set carries
- the envelope-kind sentence at line 845, body `PlatformProfileSetV1`, domain `opensip.metadata.platform-profile-set.1`

A successor that adds V2 and a reader opt-in leaves those sentences as the selected description of the profile-set body. A reader that follows them treats a V2 body as the wrong type. The same unit needs passage overrides so those sentences cover V2 under the unchanged domain, with the optional macOS measured-row member.

Do not commit.
