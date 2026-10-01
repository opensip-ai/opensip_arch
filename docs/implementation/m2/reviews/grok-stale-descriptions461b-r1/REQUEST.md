Grok review: 461b, a description-only contract successor that refreshes stale inventory v80 descriptions. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-stale-descriptions461b-r1.

## Subject

Pins are in hashes.txt:
- `docs/implementation/m2/stale-descriptions-461b-subject.json` (the subject manifest);
- `docs/implementation/m2/stale-descriptions-461b/`, which holds `successor.json`, `README.md` and `evidence/verify_scratch.py`.

The parent is inventory v80. There is no schema, registry, generated-code or product change. The product is main at d4239a5, read-only.

## What it does

It makes eight JSON Pointer description overrides on v80. None of the eight rows is an inherited row:
- `installation_fence.rs` (236)
- `installation_publication_tests.rs` (240)
- `installation_session.rs` (247)
- `read_premise.rs` (250)
- `installation_observation.rs` (259)
- `native_census.rs` (316)
- `native_read_session.rs` (320)
- `native_record_capture.rs` (321)

Each replaces text made stale by 458c-b1, b2 and c, for example "no consumer uses it yet", "under a native installation fence" or "borrowed native fence". The README gives each row's before and after text.

Both the scratch verify and the live verify_design pass. 461a (under separate review) changes no description, so 461b does not depend on it.

## Decide

- Is every new description true of the committed code at d4239a5? Read the files.
- Is any other v80 row for a file changed since v74 still stale?
- Is the successor well-formed, so the next inventory successor can carry these rows by value?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": a single string, the sha256 of stale-descriptions-461b-subject.json.

Write REVIEW.md and review.json. Do not commit.
