Codex review: X10a (the `opensip doctor` command) with inventory v82, and X10b (golden text overrides). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/codex-read-cli-x10a-r1.

Law: `docs/implementation/m2/read-cli-x10/PROPOSAL.md` r3 (accepted by Codex).

## Subjects (pins are in hashes.txt)

1. **X10a.**
   - Product: the worktree `/Users/sb/code/opensip-ai/opensip-x10a`, based on f7acb6d. Save `git -C <worktree> diff` (new files are intent-to-add) as product.diff and report its sha256.
   - Arch: `repository-file-inventory.v82.json`, `read-cli-inventory-v82-subject.json` and `read-cli-inventory-v82/`. v82 is on v81 and carries its 16 projection rows.
2. **X10b.** A contract successor with six overrides of the `doctor-report-not-producible` golden situation and remedy, across the three command inventories: `read-cli-x10b-subject.json` and `read-cli-x10b/`.

## What X10a does

- `opensip doctor [--format human|json]`, via a doctor method on `MetadataHost` (`doctor_ingress.rs`) with exactly one producer call, `observe_installation_for_doctor()`.
- The CLI parses into `Request::{Metadata, Doctor}`. Off macOS, `doctor` stays an unknown command.
- The envelope follows law item 3:
  - `kind: doctor` for a produced report, and for a not-producible report with the nested `kind`;
  - `kind: failure` with 468 item 6 rows. The host I/O row's `errors` entry is `HOST.IO_FAILURE`.
- Remedies:
  - `DOCTOR.DEFECTS_FOUND` now uses the selected golden's text, which changes 458c-c's constant;
  - the backup row uses 468a's golden text;
  - every other row has one fixed text in `doctor_ingress.rs`;
  - `row_remedy` matches only details 468c can produce.
- A shared termination renderer shows the Fault cause. A failure may omit `diagnostics` only when `errors` is non-empty; metadata rejections keep their old rule. The metadata delivery-failure envelope now also shows the Fault cause.
- The catalogue row, plus help and completion.
- Source pin:
  - it covers `apps/cli/src/*`, `doctor_ingress.rs`, `outcomes.rs` and `request.rs`, with comment lines stripped;
  - it forbids env reads, `home_dir`, `cfg(feature`, `cfg(test)` and `cfg(debug_assertions)`;
  - it requires exactly one producer call, and no other producer or session entry;
  - it refuses a `[features]` table on cli, host, security and reporting.
- Tests in three layers (law item 5):
  - security: 11, including new chain, account, no-premise, budget and not-initialized cases. `Store` cannot be produced from real bytes;
  - host: 19, covering native-shaped and labelled-synthetic report bounds, parity and schema validation, including the negative `doctor.kind` test;
  - CLI binary: 6. In a dev build it ends with `CORE.NO_EMBEDDED_RELEASE`, exit 2, a schema-valid envelope, and the real installation untouched.

## Known follow-up

`doctor_report.rs`'s description still says "nothing emits it yet". It needs a later description-only successor on v82, like 461b.

## Checks

- Workspace: 1172/0, on two runs. Clippy and fmt are clean.
- `check_package_edges --lane host` passes.
- verify_scratch passes for X10b alone and for X10b plus v82.

## Decide

- Does X10a implement law X10 r3 items 1 to 7 exactly?
- Rule on the ingress shape, the remedy choices (including changing 458c-c's `DEFECTS_FOUND` text to the golden), the renderer change, and the pin's completeness.
- Can any release-build path select another home, profile or release?
- Are v82 and the 16-row projection right?
- Are X10b's six overrides exact and true?

## Write two verdict files

- `/tmp/opensip-implementation/reviews/codex-read-cli-x10a-r1/x10a/review.json`, with:
  - "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
  - "requiredFindings";
  - "subjectManifestSha256" (the sha256 of read-cli-inventory-v82-subject.json);
  - "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v82, parent (the v81 pin), successorRecord}.
- `/tmp/opensip-implementation/reviews/codex-read-cli-x10a-r1/x10b/review.json`, with:
  - "verdict": `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
  - "requiredFindings";
  - "subjectManifestSha256" (the sha256 of read-cli-x10b-subject.json).

Write one REVIEW.md at the top level. Do not commit.
