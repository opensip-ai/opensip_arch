Codex review: the D2b implementation plan r1 (M3-D r5 items 10 and 11: the provider codecs, `crates/components/src/provider_protocol.rs`). A **plan review**, round 1. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only `REVIEW.md` and `review.json` under /tmp/opensip-implementation/reviews/codex-d2b-plan-r1.

**Rules:**
- Read-only: no repository edits, commits, pushes or delegation.
- No product build, test or generator run. Reading, hashing and `git show` / `git diff` are fine.
- Never touch `~/Library/Application Support/OpenSIP`, the private 413 UUID fixture, signing keys or any held-out store or T2 cache.
- No network.

## Subject

- **Subject manifest:** `docs/implementation/m3/supervisor-d/d2b-plan-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted), 380 bytes, SHA-256 `b1f997d76f25ee5154c3b2e9bda09f3417573714bdf74b5f68fafb06b004414f`. It pins `d2b/PLAN-r1.md`.
- **Bases:** product `56d0eb53a888572dd0129fbc595d0c1be16eaf3a` (clean; inventory v214, 173 contract successors), architecture `2894884ef33b0434a7c09029d2f727cf5f7a2524`.

## Authority

- **Law M3-D r5,** `supervisor-d/PROPOSAL.md`: items 10 ("`provider_protocol.rs`: one codec per protocol, selected before spawn", with D2b-T1 to T5) and 11 ("no translation"), and the units table row D2b.
- **Protocol sources:**
  - NE §9 (`docs/v2/contracts/product-v1/native-evidence.md`:2781-3316), DLV (`docs/coop/artifacts/delivery.v2.json`) and RPP (`docs/coop/artifacts/rust-provider-protocol.v2.json`);
  - P3T (`docs/coop/design-corrections/native/protocol3-transitions.v1.json`), its overlay (`docs/implementation/m1/source-selection-v2/owners/native/p3-guard-successor.v1.json`) and T2O (`…/native/typescript-protocol2-order.v1.json`).
- **Product schemas and carriers:** `schemas/sources/handshake-v1.schema.json` (with RCA-1), `startup-v1.schema.json` and `fact-batch-v3.schema.json`, and `schemas/wire/native-carriers-v1.json`.
- **The bound successors** FA-2 and RUST3-LIM (`docs/implementation/m3/native-successors-fa/`) and their materialization maps.
- **The reference corpus:** native wire owner trial 07 (`docs/implementation/m1/trials/native-wire-owner-07/`).
- **The constraints:**
  - `crates/components/Cargo.toml`'s permitted dependencies;
  - the discovery census's binding of `tools/contracts/generator-closure.json` (`tools/security/discovery_census.py`, `REFERENCE_PRODUCT`).

## Decide

1. **Fidelity to items 10 and 11.** Check each of:
   - the framing;
   - the strict CBOR profiles;
   - dispatch fixed at construction;
   - schema-checked hand-written decoding into the carriers;
   - P3T and T2O read as data;
   - the echoes and limits;
   - reject before disclosure;
   - commitments from received bytes;
   - no fact admission or Coverage minting;
   - no common semantic type.
2. **The split (LD-D2B-1) and its order, and Q1.** D2b-0's materialization stales the B2-b4c blind receipt through the generator closure. Is it correctly followed at once by a reviewed blind refresh?
3. **Each lead decision LD-D2B-2 to LD-D2B-14, with Q2 and Q3:**
   - the computed depth bound;
   - received bytes primary;
   - the vendored tables;
   - TS2's phase-selected Unavailable;
   - the process-event input;
   - Cancel per table;
   - no invented TS2 aggregate bound;
   - the send-schedule ownership;
   - the cve1 anchor order;
   - the NFC predicate exported from identity;
   - the check order;
   - RCA-1 as the materialization base;
   - trial 07 as the replay corpus.
4. **What is missing.** Is any item 10 or 11 obligation, any control or any source the plan does not account for?

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D2BPLAN-R1-RF-n` / `D2BPLAN-R1-NBO-n`.
