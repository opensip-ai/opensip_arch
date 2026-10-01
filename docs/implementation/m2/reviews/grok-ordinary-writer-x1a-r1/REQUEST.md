Grok review: X1a, the purpose-sealed platform receipt and `admit_ordinary_writer`, and inventory v81. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-ordinary-writer-x1a-r1.

Law: `docs/implementation/m2/ordinary-platform-x1/PROPOSAL.md` r1 (accepted).

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x1a`, based on fdbedf4. Save `git -C <worktree> diff` (new files are intent-to-add) as product.diff in your output directory and report its sha256.
- **Arch:** v81, `ordinary-writer-inventory-v81-subject.json`, and `ordinary-writer-inventory-v81/`.

## What it does

- **`PlatformReceipt<P: Purpose>`** with sealed `Read` and `Write` purposes, and one composition, `produce_for::<P>`.
  - `ReadPremiseReceipt` = `<Read>`, unchanged.
  - `WritePlatformReceipt` = `<Write>`.
  - `qualification()` exists only on the two concrete impls: Read lends `ReadPremiseQualification`, and Write lends `DurableBarrierQualification`. Each impl is gated by the marker trait `LendsReadPremise` or `LendsBarrier`.
  - There are no conversions, and only `InitialPlatform` implements the sealed traits.
- **`admit_ordinary_writer()`**, in this order:
  1. receipt recheck;
  2. `DurableWriteGate::begin`;
  3. `admit`;
  4. receipt recheck while the fence is held. On failure, the fence is released and the recheck's row is returned.

  The result is `OrdinaryWriteAdmission { installation, receipt }`, with `installation()`, `recheck()` and `release()`. There are two ledgers, and 468c rows only.
- **Inventory v81.** It adds `ordinary_writer.rs` and its tests, and carries 461b's 8 overrides as inherited rows, so the projection has 16 rows.

## Judgment calls: please rule on each

1. **The receipt-type separation pin.** It uses marker-trait probes plus a source pin (exactly two `fn qualification(`, each naming only its own trait; no From or Into), not compile_fail doctests, because rustdoc cannot name `pub(crate)` items. The lending types are opaque `impl Trait`, and the session takes the concrete `PlatformReceipt<Read>`. Is the separation actually compiler-enforced?
2. On a failed second recheck, the recheck stays the reported cause and a release error is dropped.
3. The step 4 refusal test uses a scripted recheck seam.
4. **Known follow-up (X1b).** `read_premise.rs`'s description is a 461b override carried unchanged into v81, and it now understates the file because it doesn't mention the Write receipt. X1 item 8 anticipates a description-only successor for this. Is deferring it to X1b acceptable?

## Checks

- Workspace: 1153/0, on two runs. 11 new tests. The 458c tests are unchanged.
- Clippy and fmt are clean.
- `check_package_edges --lane host` passes.
- `verify_scratch` passes with v81 selected and 16 inheritance rows. `verify_projection`: 16 rows, 83 corruptions refused.

## Decide

- Does it implement X1 r1 items 1 to 7 exactly?
- Can a Read receipt reach the gate, or a Write receipt reach the session?
- Is v81 right, including the 16-row projection?
- Rule on the judgment calls.
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": a single string, the sha256 of ordinary-writer-inventory-v81-subject.json;
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of v81, parent (the v80 pin), successorRecord (the pin of ordinary-writer-inventory-v81/successor.json)}.

Write REVIEW.md and review.json. Do not commit.
