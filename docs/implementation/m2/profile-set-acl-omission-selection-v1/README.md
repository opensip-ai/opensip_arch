# PlatformProfileSetV2 contract successor (law 458b)

2026-09-26. Proposed contract successor that implements accepted law 458b r2 (docs/implementation/m2/profile-set-acl-omission-458b/PROPOSAL.md), the profile-set successor that law 458 §7 names (docs/implementation/m2/acl-omission-premise-458/PROPOSAL.md). No independent review or root assent of this unit is claimed. Not code, no qualification, and no Evidence B.

## What is selected

- **Schema.** `schema/platform-profile-set-v2.schema.json` is derived from the pinned `PlatformProfileSetV1` in security-lifecycle.schemas.v1.json by `reference/make_schema.py`. The script rewrites the bundle `$ref`s to document-local ones and carries `Hex64`. It then asserts that the only differences from V1 are these two:
  - `/properties/profileSetSchema/const` is 2;
  - there is an optional `/$defs/macos/properties/measuredProfiles/items/properties/installAclOmission` with `{"const":"no-acl-stored"}`.

  `required` is unchanged. Linux rows, `supportedMajors`, the platform objects and the top level gain nothing. The V1 bundle bytes are unchanged.
- **Digest domain.** The domain stays `opensip.metadata.platform-profile-set.1`, and the envelope and signing construction are unchanged. The canonical `profileSetSchema` value separates the V1 and V2 digests.
- **Reader opt-in.** The V1 path (`profile_shape`, `verify_profile_set`) still refuses `profileSetSchema: 2`. Only an opted-in reader admits V1 or V2, and 462 `InitialPlatform` is the only intended one. The existing corpora keep their results: 1963 shape rows, 237 signed rows and 1084 platform rows. The one V1 shape row that V2 would admit is `type:profileSetSchema:2`, and it stays `valid:false` under V1.
- **Matched-row accessor.** `matched_install_acl_omission(profile, observed)` returns `"no-acl-stored"` only when all of the following hold. Otherwise it returns None.
  - the profile set is V2;
  - the decision is ADMIT at EXACT-MEASURED with no refusals;
  - the row V1 `platform_admit` selects carries the member. That row is the last row whose `build` equals the observed `osversion`, and `kernUuid` and `dyldCdhash` are then compared against that row only.

  The accessor never scans the rows for the member.
- **Passage overrides** (decision 8) apply to security-and-lifecycle.md lines 685, 711 and 845, which cover §S8 and the envelope-kind list. No other passage changes.

## Reference

`reference/profile_set_v2_model.py` checks the sha256 of the pinned V1 model and bundle, then imports the V1 model. It adds the V1 and V2 shape checks, `admit_profile_set_shape(body, reader)`, `platform_admit_v2`, the accessor and a projection. V2 shape uses the same foundation exact validator and metadata `canon` as V1.

`reference/profile_envelope.py` reproduces `sign_synthetic_profile` and `envelope_message` from the product. It uses:
- the metadata-canonical stored bytes;
- the domain digest;
- the envelope message `SHA256("opensip.metadata.envelope.2"||0||canon(subject+role+namespace))`;
- the public test-only seeds `SHA256("opensip-public-test-only-quorum62-seed-"||i)`.

It also mirrors the verifier order: carrier, then stored digest, preimage, raw quorum, shape by reader, core pin, role and revocation.

`reference/ed25519_rfc8032.py` is a pure RFC 8032 implementation, because the reference interpreter has no `cryptography` package. It is self-tested on RFC 8032 TEST 1.

`reference/check_cases.py` re-checks everything from the committed bytes and writes `reference/check-results.json`:
- the schema equals the mechanical derivation, with exactly two differences;
- all 27 public keys and key IDs of root "2" in profile-roots.json are derived;
- the first V1 admit row is re-signed byte-identically;
- the model's V1 shape rule matches all 1963 V1 shape rows;
- the reference verifier order matches all 237 V1 signed rows;
- every V2 case row is recomputed, and every signature is verified: 33 of 37 verify, and the other 4 are deliberately corrupted.

Run it with `python3 -I -B` from `reference/`, passing `--product <opensip checkout> --packages <opensip>/tools/contracts/python-packages`. The development run used python 3.14.6. The product fixture inputs are read-only and sha256-pinned in `make_cases.py`.

## Cases (`cases/`, SYNTHETIC)

- `profile-shape-cases.v2.ndjson`: 43 rows `{label, hex, valid, validV1}`.
  - `valid` is the V2 shape; `validV1` is the unchanged V1 shape.
  - 4 rows are V2-valid: the base with the member, the member absent, the member on both macOS platforms, and a duplicate build where the last row carries the member.
  - 1 row is V1-valid: the V1 base.
  - The V2-invalid rows cover:
    - wrong values (7) and wrong types (9);
    - the member on a Linux row, on a Linux platform object, on a `supportedMajors` entry or map, on the macOS platform object, in the platforms map, or at the top level;
    - a V1 body with the member;
    - `profileSetSchema` 3, 0 or -1, or a non-integer;
    - a member row missing `lane`;
    - a duplicated member key.
- `profile-signature-cases.v2.ndjson`: 18 rows. Each has the V1 fields, with `expected` for the V1-only verifier, plus `expectedV2` for the opt-in reader. The rows cover:
  - V2 admits with and without the member;
  - a V2 envelope with three signers on the V1 path, which gives `Shape`;
  - a V1-body control that both readers admit;
  - three bad-signature cases, which give `SignatureThreshold`;
  - wrong value, wrong type, a Linux-row member, a V1 body with the member and schema 3, all of which give `Shape`;
  - three core-pin mismatches, which give `CorePin` under V2 and `Shape` under V1;
  - revocation below threshold;
  - a schema-1 root, which gives `Envelope`;
  - the member stripped from the stored bytes after signing, which gives `Envelope`.
- `platform-admission-cases.v2.ndjson`: 19 rows with the V1 expected fields plus `matchedInstallAclOmission`. The rows cover:
  - exact matches with and without the member, and on x86_64;
  - the member only on the other platform;
  - a duplicate build where the last row carries the member (yields) and the reverse (none);
  - a duplicate whose last row has another identity (refuses and yields none, even when the first row matches and carries the member);
  - BASELINE-ATTESTED (none);
  - kernUuid and dyldCdhash mismatches (none);
  - SIP, fs-type, unlisted-lane and out-of-population refusals (none);
  - V1 exact and baseline (none);
  - Linux EXACT-MEASURED on V2 (none).

The product V1 fixture files and their assertions are unchanged. The new product fixture files carry their own counts.

## Limits

- The expected product results come from the Python reference of the Rust verifier order. They are not a cargo run.
- The selected product corpus platform-admission-cases.ndjson decides refusal spellings; where it differs, the pinned V1 model is not followed. The model projects `NT-TCB-BOOT:INSTALL_ROOT_FS_<fsType>` as the plain `NT-TCB-BOOT:INSTALL_ROOT_FS` that the corpus (31 rows) and the Rust code use. `check_cases.py` checks two things:
  - this is the only spelling difference across all 1084 corpus rows;
  - every refusal string in the V2 platform cases appears in that corpus.

  The remaining 171 differences are behavioral, not spelling: on malformed identities the product refuses earlier. None of the V2 cases reaches them.
- The V2 no-member body is byte-identical to the body of the existing signed V1 row `123:signed-invalid-shape:wrong-schema` (digest 2e852a2d…). That row keeps `Shape` under V1, as decision 3 requires.
- No boot identity is qualified, and no measured row for a development host is checked in.
- Evidence B, 461 and 458c are unchanged.
