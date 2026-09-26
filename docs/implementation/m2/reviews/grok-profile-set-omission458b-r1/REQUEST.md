Grok review law proposal 458b r1. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-profile-set-omission458b-r1. Law review; no product cargo. Do not read or print the private 413 UUID fixture.

Subject: docs/implementation/m2/profile-set-acl-omission-458b/PROPOSAL.md (pin in hashes.txt). It settles the choices law 458 leaves to its named profile-schema successor for `installAclOmission`.

Context:
- 458: acl-omission-premise-458/PROPOSAL.md, accepted via reviews/grok-attempt-actor459-r1/premise458.json.
- V1 schema: docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json `PlatformProfileSetV1` (about lines 2209–2330, pinned by the design lock).
- Rust decoder: crates/security/src/trust/root_payload.rs:
  - `closed()` around line 66
  - `mac_profile` around 940–989
  - `profile_shape` around 1045–1062
  - the decision around 1087–1094 and 1217–1269
  - the payload-2 reader capability precedent around 345–356
- Verifier: admitted_profiles.rs:14–80.
- Corpora: profile_tests.rs (1963 shape rows, 237 signed rows) and platform-admission-cases.ndjson (1084).
- Existing premise type: custody/installation_root.rs:206–236 `AclOmissionPremise` (test-only constructor).

## Decide

- Is a new closed V2 with a reader opt-in the right successor, rather than an optional V1 member? Does it keep every existing corpus result? Check the signed wrong-schema rows, the `type:profileSetSchema:2` shape row, and the native_census 350/469 test profiles.
- Is the shape-const choice (wrong value refuses the whole set) right against 458's "any other value refuses Evidence B"?
- Is keeping the digest domain `.1` sound?
- Does the matched-row accessor close duplicate-row borrowing, with the same last-duplicate selection and only at ADMIT, EXACT-MEASURED and no refusals?
- Is decision 6 honest: development hosts at BASELINE-ATTESTED cannot yield Evidence B, and only synthetic runtime-signed V2 profiles are used in tests?
- Is anything missing for the contract successor unit: schema, reference, cases, passage overrides for §S8's "PlatformProfileSetV1" mentions?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" (id, title, failureScenario) and "subjectSha256". Write REVIEW.md and review.json. Do not commit.
