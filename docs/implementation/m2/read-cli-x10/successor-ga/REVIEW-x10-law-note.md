# Independent review: X10-SUCCESSOR-GA-r2

X10-LAW-NOTE: ACCEPT

Reviewed 2026-10-31. XL-1, XL-2 and XL-3 are closed for the exact r2 note. No new BLOCKING findings. This accepts the narrow law successor and its specified binding destinations; actual by-value binding and the final design-lock commit remain pending.

## Authority, route and custody

Request: `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25/c2b1/own-funding-r3/review/REQUEST-x10-law-note-c2b-NOTE-1.md`, SHA-256 `99f25d3780db1ac196506e121e43e083a94b6f54ded6b1fe25d99d2dee3f35f1`, matched. This is additive to the prior request and expressly selects r2 while preserving r1 as history.

Before substantive review, `python3 -I -B /Users/sb/code/opensip-ai/opensip_arch/tools/agent_model_route.py check --provider codex --route R3-FRONTIER` returned exit 0: `ROUTE-OK R3-FRONTIER codex gpt-6-astra/high`. Codex is independent of the Claude author. The previously read bootstrap orientation and routing guidance remain applicable; live control indirection, ACTIVE-PLAN and MAP top were rechecked. Live architecture HEAD is `9b0eb222816d03eb1db9ee75b6c4eecbfa53ea2d`; product main is `dd89db11a33e7b67d8ca7dce74368a56c4808231`. MAP's older architecture checkpoint is not used to override the exact request or note pins.

All twelve request-listed evidence hashes matched; all twelve files have no write permission bits. The r2 one-member SHA256SUMS matches the note. The earlier local review was confirmed byte-identical to the frozen historical copy `evidence/h6/REVIEW-x10-law-note-r1.md`, SHA-256 `3baa418775f7948866eacda3796e93a7c17c5625993a63aaf074dd7ea468a98e`, before updating this requested output path. That historical copy was not changed.

Accepted subject: `evidence/h5/guard-amend/guard-amend__X10-SUCCESSOR-GA-r2.md`, SHA-256 `15b8f63886162a4a5ffd9dfd9732d07fe43693a1f58327bd99b5d936a7a52ad5`. Its manifest SHA-256 is `53a8e04cea663765f4340439cfe4769a0ee9291ba0f72c19446643ab7772773d`.

References below: `R/` means `/Users/sb/code/.opensip-implementation-cache/lead-2026-10-25/c2b1/own-funding-r3/`; `NOTE` means `R/evidence/h5/guard-amend/guard-amend__X10-SUCCESSOR-GA-r2.md`. Product sites are at the exact H6 code commit recorded below.

## Answers to the three requested questions and finding closure

1. **Exact host feature list and GA-2 assertion — ACCEPT; XL-1 closed.** NOTE:28-35 states all four feature keys and every forwarding value, with no default. Independently parsed the quoted TOML and H6 host Cargo.toml: their feature maps are equal. The manifest is byte-identical at H5 and H6. NOTE:43-49 preserves no forwarding, no default, refusal of dependency activation in all three kinds, and compile-time refusal when the feature is enabled without debug assertions. The no-dev-exception restriction matches the previously accepted GA-2; it is stricter than the ruling's outside-host-dev minimum and adds no new activation permission. NOTE:71-75 pins the same doctor and creator files accepted in GA-r1; both match H6 Git bytes. This is the exact permitted map:

   ```toml
   [features]
   crash-matrix = ["opensip-storage/crash-matrix", "opensip-security/crash-matrix", "opensip-platform/crash-matrix"]
   operability-dev-sinks = ["opensip-operability/operability-dev-sinks"]
   harness-instrumentation = ["opensip-operability/harness-instrumentation"]
   profile-allocations = []
   ```

2. **Proper X10 successor, parent and unchanged scope — ACCEPT; XL-1 and XL-3 closed.** NOTE:13-15 supplies the complete architecture commit, parent path and SHA-256. Re-hashed the parent Git object and compared NOTE:17-20 with `docs/implementation/m2/read-cli-x10/PROPOSAL-r4.md:94`: the quotation is exact after line-wrap normalization. NOTE:26 and :56-59 replace only host's feature-list sentence, preserving security/storage, prior CLI/reporting widenings, and the other X10 clauses. No production feature is added. NOTE:48-49 removes the false exclusive-consumer assertion and explicitly includes library-test use of the controls. This matches H6 `crates/host/src/lib.rs:118-132` and the direct import in `crates/host/src/typescript_profile_tests.rs:6`. The feature-gated support module and the `any(test, feature)` controls are distinguished correctly. No product or guard edit is needed to close XL-3.

3. **Exact provenance and named by-value binding — ACCEPT as a binding specification; XL-2 closed.** NOTE:77-91 names the owning joint C2b contract 193 law-by-value set in `stage-joint-r3`, lists the four concrete architecture destinations, and gives complete hashes for both receipts and the earlier GA review. Re-hashed the supplied copies; additionally verified the receipt source paths named at NOTE:89. The table preserves v1 as historical and v2 as its binding-clause successor. The successor's own hash belongs in the external binding manifest, avoiding a circular self-hash; this note's eventual ACCEPT review joins the same directory. NOTE:91 explicitly leaves binding PENDING. This closes the missing-clause finding without claiming that the staging manifest or final lock has already been produced.

## Independently verified pins and H5-to-H6 transition

| Subject | Verified value |
| --- | --- |
| Parent architecture commit | `9b0eb222816d03eb1db9ee75b6c4eecbfa53ea2d` |
| Parent X10 `PROPOSAL-r4.md` SHA-256 | `33095e6c13c0e16a5e4fdc87832dbd2f048b01f126b432d49347cc2f116b386a` |
| H5 commit | `76ce532aa1191aa79791d4822c0855de9bf5e55a` |
| H6 code commit, direct child of H5 | `d2729979f0ff264711620f74b42fce84fb36e34c` |
| H5 and H6 `crates/host/Cargo.toml` SHA-256 | `0d9cf05ce826c07c29c41dea1da541cc13785272809d0fe2d400b10bcaebcbc9` |
| H6 `crates/host/src/lib.rs` SHA-256 | `7f949da827df1364aebd1e20cc4b89674d5d3334d02f51afa26267fb223f9298` |
| H6 doctor guard SHA-256 | `f50f76b81b637ed76d348518aca3046451e0917af22d7a9fa8f102e733ca92bc` |
| H6 creator guard SHA-256 | `9e73b5d790fd2cf7b85be99d943255fbc792ac0da905f710fea47eca1b919c4f` |

The complete H5-to-H6 diff changes only `crates/host/src/lib.rs`: the three-line `const _: () = { let _ = snapshot::btree_height; };` becomes `const _: fn(usize) -> usize = snapshot::btree_height;`. The profile-allocation blocks and both guard files are unchanged. Thus NOTE:63-66 accurately identifies the intervening code change. This is an identity check, not independent acceptance of the C2a census fix or a funding-transfer verdict.

The exact binding destinations specified by NOTE:84-87 share prefix `docs/implementation/m2/read-cli-x10/successor-ga/`:

| Member | Source SHA-256 |
| --- | --- |
| `X10-SUCCESSOR-GA-r2.md` | `15b8f63886162a4a5ffd9dfd9732d07fe43693a1f58327bd99b5d936a7a52ad5` |
| `ADOPTION-GUARD-AMENDMENT.md` | `e33e273a3adc7cbeeccba702f421393a20e2523a3b308a79e2208414dbf730a2` |
| `ADOPTION-GUARD-AMENDMENT-v2.md` | `375e410806556584901e66039a22a9488583f28f6e9570c4877c3248a7c01cb7` |
| `REVIEW-guard-amendment.md` | `243c5cce7bfc5dd564ecde2d1b28bc624ececf820bf5eca5ea0e7bf9dd3d2c89` |

The additive request still uses the older H6-final-lock description, but the r2 subject and author handoff explicitly identify H6 as the intervening code fix and H7 as the pending lock-only successor. This review accepts those exact code pins and the pending H7 requirement. NOTE:67's claim of source identity at H7 is a constraint to verify when H7 exists, not evidence about an already produced commit.

## Carried matters and evidence boundary

No new XL-n BLOCKING or CARRIED findings. The earlier GA review's two carried observations remain carried: the stale source forwarding comment and the non-fail-closed validation wrapper. NOTE:98 explicitly declines reliance on the separately carried `X10 r5` measurement citation. This review neither closes that item nor establishes a global absence claim about the law record.

The pinned `w28-identity-check-d2729979.txt` reports zero differing paths among 644 re-hashed manifest entries. Its bytes were verified, but this review did not re-run that 644-entry check or infer funding/sweep acceptance from it. Direct reviewer checks were limited to the parent, feature map, relevant product files, H5/H6 relationship, provenance hashes and correction semantics.

Only the requested review artifact was written. No frozen input, adoption receipt, historical review or source was edited. No Cargo tests, lane, staging, lock regeneration, adoption, integration or external messages were performed. This verdict accepts the exact law note and specified binding, closes XL-1 through XL-3, and leaves actual by-value staging, final manifest/lock verification and all remaining execution gates to their authorized owners. It does not itself establish completed binding, runtime enforcement, funding transfer, unit acceptance or product qualification.

X10-LAW-NOTE: ACCEPT
