# Review: profile-set ACL omission 458b r2

Grok is the single reviewer. Claude Opus 5.5 leads. Re-review of `docs/implementation/m2/profile-set-acl-omission-458b/PROPOSAL.md` after 458b r1. No repository edits. No product cargo.

The proposal is 5809 bytes, sha256 `0c4d330532048126692a7d25da00dbf9cdbdec8fd74204fdcaca92202834d8bd`, matching `hashes.txt`. `PROPOSAL-r1.md` is the r1 bytes: 4707 bytes, sha256 `ce6551f7211cdafe8515de8cce40d394b32385cdd0a0e23d14f6b36ee96439fd`. The diff is the header plus decision 8.

## Verdict

**ACCEPT.**

## Answers

RF-1 is closed. Decision 8 assigns the contract successor passage overrides, in the successor's before/after form, for the three sentences, and leaves the digest domain `opensip.metadata.platform-profile-set.1` unchanged:

- §S8 line 685 names the machine-id key of the signed `PlatformProfileSetV1` or, for a reader that opts into it, `PlatformProfileSetV2`.
- §S8 line 711 uses that same pair, and a V2 macOS measured row may carry optional `installAclOmission` const `"no-acl-stored"` with the meaning law 458 gives it.
- Line 845 names envelope kind `platform-profile-set` with body `PlatformProfileSetV1`, or `PlatformProfileSetV2` for an opted-in reader, under that same domain.

Those are the only product-v1 passages that name the profile-set body type. A search of `docs/v2/contracts/product-v1` finds `PlatformProfileSetV1` only at those three lines of `security-and-lifecycle.md`.

The other hits keep the V1 name on purpose. The pinned schema record, the pinned `security_lifecycle_model_v1.py` strings (`ENVELOPE_KINDS`, `admit_profile_set_envelope`, and the S8 key comment), and the V1 schema-bundle index still describe V1. Decision 7 leaves that model and bundle unedited and puts V2 admission in `profile_set_v2_model.py`. The V1 fixture tag `profileSet` value `PlatformProfileSetV1` stays on the V1 cases. `capability-manifest-domains.v2.json` cites S8 and the signed profile set as the admission owner, which decision 8 updates at its source. Trial copies, review reports, and the 469 problem statement are not live passages. Decision 8's "no other passage changes" matches that search.

The r1 answers on the closed V2, the reader opt-in, the shape const, the digest domain, the matched-row accessor, and decision 6 stand. The diff does not reopen them.

Do not commit.
