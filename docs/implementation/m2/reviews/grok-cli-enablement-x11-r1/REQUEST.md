Grok review: law X11 r1, CLI enablement of the creator commands (`opensip`, `analyze`, `fit`, `audit`): the M2 scope. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-cli-enablement-x11-r1. This is a law review: run no product cargo. Product HEAD is bccb6b4; arch HEAD before this request is 14961daeb.

Subject: `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/cli-enablement-x11/PROPOSAL.md`, r1, sha256 b98debc9f8823f69ec95c84f7b4045ffbbaea990e69d7cc998f08328fbbe96e4 (19087 bytes; see hashes.txt).

Why: EXIT-PLAN's X11 row (`docs/implementation/m2/EXIT-PLAN.md`) says these are analysis commands. "Until M3 they can only create or admit the installation and then end on the existing not-implemented refusal", and "the X11 law must say whether that partial behavior ships before M3". Its planning carry-ins assign X11 three things: 464 item 7 (CLI enablement), the `RetentionDisclosure` backup-status field deferred by 468 item 7, and the doctor human label deferred by 458c r6 item 10.

Context (all under `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/` unless noted):
- **Laws:**
  - creation-ingress-464 (r2, items 2 to 5 and 7);
  - existing-root-admission-468 (r5, items 1, 6, 7 and 8) and its contract successor `existing-root-diagnostics-468a/README.md`;
  - read-premise-458c (r6, item 10);
  - read-cli-x10 (r4, items 1, 3, 4 and 5);
  - ordinary-platform-x1 (item 7);
  - project-root-x2 (r8, item 6);
  - store-admission-x3a (r5, item 2, "X11 decides only how the creator command ends after creation");
  - trust-bootstrap-x4b (r5, items 1 and 11, "required before X11");
  - replay-join-x5 (r3, "Not claimed": no analysis producer before M3);
  - finalization-x7 (r5);
  - policy-admission-x12 (r3, items 4, 8 and 9: pack admission runs first, before X1, X2 or any fence; the release registry has zero rows in M2).
- **Product** (`/Users/sb/code/opensip-ai/opensip`):
  - `apps/cli/src/arguments.rs` and `bootstrap.rs`;
  - `apps/cli/tests/startup_tests.rs` and `doctor_tests.rs`;
  - `crates/host/src/outcomes.rs` (the catalogue and `MetadataHost`), `doctor_ingress.rs`, `request.rs` (`installation_entry`), `configuration.rs` and `lib.rs`;
  - `crates/security/src/custody/installation_routing.rs` (`run_initial_creator`, `pub(crate)`) and `crates/security/src/initial_installation.rs` (`BackupClassification`, `deliver_disclosure`);
  - `schemas/sources/invocation-v5.schema.json` (`$defs/RetentionDisclosure`, closed) and `command-envelope-v7.schema.json`.

The lead decisions to check:
1. No creator command goes live in M2. The four commands keep their present refusals byte for byte. Four reasons are given:
   - X12 r3 item 8's order: pack admission comes first, and cannot pass in M2;
   - a false durable P0 record of an analysis step that cannot run;
   - X1, X3a and X4B leave the creator invocation nothing to do with I;
   - nothing observable on M2 builds.

   Rejected: the partial behavior; pack-admission-only wiring (`CONFIG.INVALID count:0`); a creator-only command; rewording now.
2. Item 2's end-to-end table, the claim that every build (dev, this BASELINE-ATTESTED host, a hypothetical release) behaves the same, and the stated limit on "in this development build".
3. There is no contract successor in M2. The backup-status field is deferred to M3 with its first emitter, with a recorded direction (`backupStatus`, the three `disclosed` spellings, present exactly when `firstUse`, never `not-backed-up` from a missing detector, the stderr notice kept).
4. The carry-ins: the doctor label is closed by X10a (84a8bfd); recovery, `store-gc`, finalization and commit are not enabled by X11 in M2.
5. The M3 obligations are recorded but not decided:
   - order;
   - the creator's public entry;
   - the creator-end termination (X3a's assignment);
   - one RequestId per invocation (the intent's RequestId versus the CLI's `RequestAuthority`);
   - terminations;
   - the backup-status successor;
   - the analysis producer and Run closure;
   - restated binary behavior.
6. The tests are in a new `apps/cli/tests/creator_commands_tests.rs`: refusal bytes in both formats with schema validation, zero effects, the catalogue, and a widened source pin.
7. The units: X11a (tests only, with an inventory successor), and an X11 successor law in M3.
8. An EXIT-PLAN record-only correction.

## Decide

- Is "nothing live in M2" lawful and the narrowest lawful scope? Check that no accepted law (464 item 7, 468 item 7, X3a r5 item 2, X4B r5 item 11, X10 r4) obliges X11 to ship creator behavior, the backup-status field or a creator-end decision in M2.
- Is item 1's reading of X12 r3 item 8 right, that the creator runs after pack admission in an analysis request? And is the rejection of pack-admission-only wiring sound?
- Is deferring the backup-status successor lawful, given 468 item 7's stated reason and 464 item 3's stderr carrier? Is the recorded direction consistent with 464 items 2 to 4?
- Is item 2's table accurate to bccb6b4's parser (`arguments.rs`) and `MetadataHost::execute`? Is the claim right that no producer, disclosure or file access occurs?
- Are item 5's M3 constraints faithful to the cited laws? In particular, is the one-RequestId gap (464 item 5 versus `RequestAuthority`) real, and is it correctly left to the M3 successor?
- Do item 6's tests and source pin prove item 2, without a seam and without weakening X10 r4 item 5's pin? At bccb6b4 the pinned files name none of the forbidden symbols.
- Is anything else wrong or missing?

review.json must contain top-level "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings" (an array; empty on ACCEPT) and "subjectSha256" (b98debc9f8823f69ec95c84f7b4045ffbbaea990e69d7cc998f08328fbbe96e4). Write REVIEW.md and review.json. Do not commit.
