Codex review: the D2a implementation plan r1 (M3-D r5 item 9: the common control codec, `crates/components/src/control_protocol.rs`). A **plan review**, round 1. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only `REVIEW.md` and `review.json` under /tmp/opensip-implementation/reviews/codex-d2a-plan-r1.

**Rules:**
- Read-only: no repository edits, commits, pushes or delegation.
- No product build, test or generator run. Reading, hashing and `git show` / `git diff` are fine.
- Never touch `~/Library/Application Support/OpenSIP`, the private 413 UUID fixture, signing keys or any held-out store or T2 cache.
- No network.

## Subject

- **Subject manifest:** `docs/implementation/m3/supervisor-d/d2a-plan-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted), 380 bytes, SHA-256 `326ad737a5e29a7343b07a1cefd05dceefff038b95dd00693964bd94b4768359`. It pins `d2a/PLAN-r1.md`.
- **Bases:** product `56d0eb53a888572dd0129fbc595d0c1be16eaf3a` (clean; inventory v214, 173 contract successors), architecture `cbcc436eb253a926775d3b19744ca93e504bc152`.

## Authority

- **Law M3-D r5,** `supervisor-d/PROPOSAL.md`:
  - section B, items 9 ("`control_protocol.rs`: CC v5 exactly, and the select tuple", with D2a-T1 to T4) and 11 ("no translation");
  - the units table row D2a and its gates.
- **CC v5** and its retained reference, in `docs/coop/completion/`: the contract `control-completion.contract.v5.md`, `.check.v5.py`, `.cases.v5.json`, `.rf5-proof.v2.json`, `.report.v5.json` and `.freeze.v5.json`.
- **CPC** (`docs/coop/artifacts/control-protocol-contract.v2.json`).
- **The product schema** `schemas/sources/control-v3.schema.json`, and its generated `Control3Root` (`crates/contracts/src/generated/protocol.rs`).
- **`crates/components/Cargo.toml`'s permitted dependencies.**

## Context

A candidate implementation exists in `/Users/sb/code/opensip-ai/opensip-d2a`, as context only: in it, all 480 corpus cases replay exactly. This round reviews the plan.

## Decide

1. **Fidelity to item 9.** Does the plan implement CC v5 exactly? Check:
   - the sixteen closed messages against the product schema;
   - the framing and the 65,536 host offer;
   - the integer-lexeme reader;
   - the states and the 256 cells;
   - RF precedence with both repairs (CCR-1, CCR4-1);
   - the select tuple, confirm-only, from the admitted manifest;
   - hello's fields from the admitted selection only.
2. **Each lead decision,** and the three questions:
   - **LD-D2A-1:** the context-parameterized classifier, with the 65,536 policy in the production constructor (Q1);
   - **LD-D2A-2:** the arena reader, and unpaired surrogates kept until the UTF-8 walk (Q3);
   - **LD-D2A-3:** the product schema evaluated by a closed interpreter of exactly its keywords, refusing any other keyword or pattern at load;
   - **LD-D2A-4:** precedence, with the two recorded corpus readings (hello in CLOSED and FAULTED is RF8; over-offer is RF2 after RF3 and RF4);
   - **LD-D2A-5:** direction stopping in the session driver;
   - **LD-D2A-6:** stream framing;
   - **LD-D2A-7:** the vendored corpus, with the 484 checks split as 482 native and 2 architecture-side source pins (Q2);
   - **LD-D2A-8:** the select tuple;
   - **LD-D2A-9:** one dependency edge, `opensip-contracts`, and no serde on wire bytes.
3. **Item 11.** Is anything in the plan a translation, normalization or a seventeenth message?
4. **The controls and lane.** Are D2a-T1 to T4 and the supplementary controls sufficient, and does each listed mutation prove a rule?

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D2APLAN-R1-RF-n` / `D2APLAN-R1-NBO-n`.
