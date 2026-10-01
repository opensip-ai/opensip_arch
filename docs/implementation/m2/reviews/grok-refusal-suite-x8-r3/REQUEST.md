Grok review: law X8 r3, the opaque API refusal suite (`crates/host/tests/admission_tests.rs`). Claude Opus 5.5 leads, and you are the single reviewer.

**Ground rules.**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/grok-refusal-suite-x8-r3`.
- This is a law review. Run no cargo in the product checkout. A harness-flag probe in a scratch crate under `/tmp` is fine.
- The product baseline pin is `f1b8321`. The arch repo is `/Users/sb/code/opensip-ai/opensip_arch`.

**Subject.** `docs/implementation/m2/refusal-suite-x8/PROPOSAL.md` r3. The first row of `hashes.txt` pins it: sha256 `1dc6b71fa4e5ec064fc409abf1164a968ddaa6ca1d635f363080128d2bbbf385`, 44288 bytes.
- r2 is preserved as `PROPOSAL-r2.md` (sha256 `829a70e5…afd`, the bytes you reviewed).
- Your r2 review is in `docs/implementation/m2/reviews/grok-refusal-suite-x8-r2/`.
- X9 r1 is `crash-matrix-x9/PROPOSAL.md`.

## What r3 changes

The header's r3 note lists the changes. r3 changes only these parts:
- **Item 4b:** the fenced `state.v1` publisher is a function beside the trust owner's publication code, placed on the joint-predicate list by X9-1, not an item of `crash_matrix_support`. Both support modules call it.
- **Item 4c:** two new `scenario` functions:
  - `publish_revocation_fenced(home, subjects)`, compiled under `scenario-fixtures` alone, which refuses in a process holding an operation lease that `operation` handed out;
  - the read-only `revocation_version(home)`.
- **Item 5a:**
  - the entry is an ordinary `#[test]` in X9 item 3's shape, gated by `OPENSIP_X8_HELPER`, not `#[ignore]`d;
  - the exact command line and environment;
  - the self-checks: success exit, exactly one `X8|published|<before>|<after>` record, `after > before`, and `revocation_version` after the exit equal to `after`;
  - only then `prepare_commit` and `publish`, with no sleep.
- **Rejected alternatives** and one new **forbidden substitute**.

Everything else is unchanged from r2.

## Decide

1. **Does r3 close r2 RF-1?**
   - Does the re-executed process run the fenced publisher before it exits 0, in a process that never ran `operation` and holds no operation lease?
   - Is the publisher callable from the host test under `scenario-fixtures` alone, through `scenario`, with `crash-matrix` off?
   - Does a no-op exit (an ignored entry, a filter matching nothing, an unset variable) now fail the case?
   - Does the test thread wait without sleeping before `prepare_commit` and `publish`?
2. Is placing the publisher outside `crash_matrix_support` consistent with X9 r1 items 2 and 6, and with item 4b's rule that only sites both surfaces call are on the list? Does it need anything beyond X9-1 placing it?
3. Did r3 introduce anything inconsistent elsewhere?

## Output

Write `REVIEW.md` and `review.json`. `review.json` must contain these top-level keys:
- `"verdict"`: `ACCEPT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: an array, empty on ACCEPT;
- `"subjectSha256"`: `1dc6b71fa4e5ec064fc409abf1164a968ddaa6ca1d635f363080128d2bbbf385`.

Do not commit.
