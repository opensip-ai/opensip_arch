I accept candidate02 at unit scope with no required fixes; this is not product approval. This is a resumed delta review in the same session as assembly review01, not a fresh blind one. Review01's required issue RQ-A1 is resolved, and the three behavior changes do what they are meant to. The earlier separate coverage acceptance is unchanged; I didn't reopen it, and its file is byte-identical. `review.json` and `review.md` are in `/tmp/opensip-implementation/m1-report-asset-assembly-review-02`.

**Custody**
- **Subject:** the manifest hash `8ddf5ebe…` matches, and all 49 files matched in set, size and hash before and after.
- **Pins:** the 14 unchanged owner/verifier pins, the 8 tool pins and both test-origins pins all match.
- **Root evidence:** the 17 `root-validation/` logs are identical to the external root-validation-02 directory, and the tool hash they record matches the frozen tool.
- **Isolation:** I worked on my own exact copy with Python `-I -B` and an empty private pycache prefix, which stayed empty. Scratch was a short private directory. The deep fixture was only created and removed through descriptor-relative operations, and scratch is now empty.

**Reproduction (following `UNIT.md`)**
- 11 unit tests pass, including with a 215-character TMPDIR, so the socket fix works.
- All 7 adopted regression groups pass. The p02 read count is exactly 33554432 bytes against the tightened limit; the old wording in that log is just a stale label.
- Regenerated fixtures are byte-identical.
- The consumer passes both of its tests, including all 19 bundle/projection pairs, plus Clippy with `-D warnings` and fmt.

**The three changes, checked with my own probes (all pass)**
- **Typed filesystem errors:** symlink swaps, removed files, `EACCES` and a closed root descriptor each refuse with exactly `ASSET_FILESYSTEM`, with the original error kept as the cause and no descriptor leak. Other refusal codes, retries after interrupted reads, and `TypeError` are left alone.
- **Aggregate check before reading:** with three 16 MiB members, the first two are read and the third is never read. The exact limit boundaries behave correctly. A member that grows between the check and the read is still refused by the retained post-read check.
- **Windows device names:** all 88 reserved variants are refused, including `.tar.gz`-style names, on disk and in the root, manifest and role paths. Near-miss names are admitted.
- **Final byte count:** a short read with unchanged metadata refuses `ASSET_CHANGED`, and zero-byte members are not falsely refused.

**Mutation evidence (48 mutants: review01's 36 plus 12 for the new code)**
- 43 are killed by the permanent tests, including every earlier meaningful survivor (T02, T04–T08, T12–T20, T26, T30).
- 2 are killed only by my probes: N06 changes how much is read but not the outcome, and N09 checks only the last extension, which admits `con.tar.gz`.
- 3 survive, all equivalent: T03 no longer changes any outcome now that the pre-read check exists, and T24 and T25 were already equivalent.

**Advisories (non-blocking)**
- **Windows name vectors:** add a multi-extension vector like `con.tar.gz` to the permanent tests. Also record why `com0`/`lpt0` are admitted; current Microsoft guidance may list them. There's no Windows target, so this isn't required.
- **Refusal code for large members:** a member over both caps now reports `ASSET_BUNDLE_LIMIT` instead of `ASSET_MEMBER_LIMIT`. Both refuse before reading, so only the diagnostic changes.
- **Stale prose:** the p02 log label and the adopted regressions' docstring still have old wording.
- **Typed error coverage:** only the unit test requires `ASSET_FILESYSTEM`; the adopted regressions still accept a bare `OSError`.
- **Root evidence:** the root log recorded no private pycache prefix, and `root-validation.json` uses a placeholder interpreter name. I reproduced both with the pinned interpreter and got identical results.
- **Carried over from review01:** change detection relies on timestamps and the runtime doesn't recheck completeness, so publication must lock the tree. The verifier's filesystem tests still aren't carried, and `jsonschema` still isn't byte-pinned.

**Remaining integration duties**
- D9 delivery mapping.
- The compiled-pin-only route: a private compiled `HostAssetPinV1` and a single build channel.
- The actual browser bundle and licenses, with real sizing.
- Binding the renderer schema to `projection_sha256`.
- Bootstrap and tool closure.
- Immutable publication and the TR-CORE release inventory.
- Host/platform `AssetSource` integration and Linux qualification.

All fixtures remain synthetic, and passing tests don't prove atomic snapshots under concurrent malicious writers.
