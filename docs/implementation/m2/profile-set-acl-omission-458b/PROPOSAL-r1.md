# Profile-set successor carrying `installAclOmission` — proposal 458b r1

2026-09-26. Claude Opus 5.5, implementation lead. Law for unit 458b, the profile-schema successor that law 458 names (acl-omission-premise-458/PROPOSAL.md §3, §7; accepted via grok-attempt-actor459-r1/premise458.json). It settles the choices 458 leaves open. The contract successor, reference, cases and decoder are the implementation units that follow. Not code. It does not mint Evidence B; that stays with 462.

## Problem

458 requires a signed, measured macOS row member `installAclOmission` with the value `"no-acl-stored"`. Today's `PlatformProfileSetV1` is closed at every level (`additionalProperties:false`; Rust `closed(...)`), and `profileSetSchema` is the constant 1. So any row carrying the member refuses. The V1 schema bundle and reference model are pinned by the design lock and cannot be edited. The existing corpora (1963 shape rows, 237 signed rows, 1084 platform cases) pin V1 behaviour, including that `profileSetSchema: 2` refuses.

## Decisions

1. **A new version, not a widened V1.** `PlatformProfileSetV2` is a new closed schema, identical to V1 except for two things:
   - `profileSetSchema` is the constant `2`;
   - each **macOS `measuredProfiles` row** gains one optional member, `installAclOmission: {"const": "no-acl-stored"}`.

   Nothing else changes. Linux rows, `supportedMajors`, the platform object and the top level gain nothing. A V1 body carrying the member keeps refusing as an unknown member. V1 schema bytes and V1 behaviour are preserved.
2. **Shape const, not a decision value.** A V2 row whose `installAclOmission` is present with any other value or type fails shape, so the whole profile set refuses. It does not merely refuse Evidence B. An absent member means only that the row does not qualify for Evidence B.
3. **Reader opt-in.** `profile_shape` and `verify_profile_set` stay the V1 path for every existing caller, and they keep refusing `profileSetSchema: 2`. A separate V2 shape check and verifier are used only by a caller that opts in, as the payload-2 reader capability does today. The only such caller will be `InitialPlatform` (462). The existing signed wrong-schema rows, the `type:profileSetSchema:2` shape row, the platform corpus and the `native_census` test profiles therefore keep their results.
4. **Digest domain unchanged.** The domain stays `opensip.metadata.platform-profile-set.1`. The canonical body's `profileSetSchema` value separates V1 and V2 digests, and `CoreProfileBindingV2` pins only the digest, so no trust-record schema changes.
5. **The matched row is exposed.** The platform decision records which measured row matched: the same last-duplicate row that `platform_admit` selects today, by (build, kernUuid, dyldCdhash). An accessor returns that row's `installAclOmission` only when:
   - the decision is ADMIT;
   - the tier is EXACT-MEASURED;
   - there are no refusals;
   - the profile set is V2.

   Evidence B may read only that accessor. It can never scan rows, and never read a different duplicate.
6. **Qualification stays external.** Signing `"no-acl-stored"` for a boot identity requires that identity's 458 §6 fixture measurements. SYNTHETIC test profiles may carry the member only with `standing: "SYNTHETIC"`, and they are never qualification. A BASELINE-ATTESTED identity, such as this macOS 27 host under 469, has no measured row and so cannot yield Evidence B. Live-host tests of 462 build a synthetic signed V2 profile at run time from the observed identity, with the public test-only seeds, and never check in a measured row for a development host.
7. **Reference and cases in the successor unit.** The V1 model and schema bundle are not edited. The contract successor carries its own:
   - V2 schema;
   - a reference `profile_set_v2_model.py` that imports the pinned V1 model by hash and adds V2 admission and the matched-row accessor;
   - new shape cases: the member absent, wrong value, wrong type, on a Linux row, on `supportedMajors`, on the platform object, and in a V1 body;
   - new signed V2 cases produced with the public quorum62 seeds.

   New product fixture files carry their own counts. The V1 fixture files and their assertions are unchanged.

## Forbidden substitutes

Accepting V2 through the default verifier; an optional member in V1; reading `installAclOmission` from any row other than the matched one, or at BASELINE-ATTESTED; a type name in `installRootFilesystems` as the qualification; a checked-in measured row for a development host; re-signing or re-projecting the existing 237 signed cases.

## Not claimed

No boot identity is qualified. No Evidence B is minted. 461 and 458c are unchanged.
