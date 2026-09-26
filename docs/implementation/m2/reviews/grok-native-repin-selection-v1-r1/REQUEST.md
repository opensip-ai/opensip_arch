Grok, please review the design unit native-repin-selection-v1, r1. Claude Opus 5.5 leads, and you are the single reviewer. Do not edit either repository, commit, push or delegate. Write only under /tmp/opensip-implementation/reviews/grok-native-repin-selection-v1-r1. The host is macOS 27.0 (26A428) on an Apple M5 Max. Do not run cargo in the product. You may run the generator and design tools read-only against copies. Do not read or print the private 413 UUID fixture.

Subject: docs/implementation/m2/native-repin-selection-v1-subject.json, 14663 B, sha256 1d1552bebd641098d5dcefcc11a63634e3af2a2dc25e213c08912a36a2d4b624. It has 66 members. Record: native-repin-selection-v1/successor.json, 16660 B, sha256 412f05247138f6ed6a03f2cedfe8651ac959a7135c2c3ee9242fb4a89f891ac3. It has 8 parents, 65 candidates and passageOverrides []. Product HEAD is 0a3af77. The unit is not yet in design-lock.json.

## What it is

The owner authorised re-pinning native tool hashes after the reimage from macOS 26.6.2 to macOS 27.0: "change the hashes, we have no other choice". The unit changes 8 product files (see materialization-map.json):

- The 3 Python and confinement profiles and toolchain.json: new sha256 and bytes only. The toolchain `standing` now names the macOS 27 rebuild instead of rebuild403.
- build-receipt.json: the bytes of the offline generator rebuild on macOS 27.
- generator-closure.json: 5 rows and the toolchain object. Its new sha256 is 023208cfb04d318fbf36ca8c76f45aa5d37f6db13139bee61843348d12c8fa82.
- registry.json: recipe `generatorClosureSha256`. Its new sha256 is 2c434d3db7414401a091d600d20f651bbd3b9dea37e0242e3210d091ae05e644.
- report.ts: header lines 2–3 regenerated with `--write`. Its new sha256 is 3f264d755d2c3a567b5039a19600be25133c1d48cff7c5641e94fba4102cb792.

The README must justify why this is not the case tools/README.md forbids ("do not change hashes just to admit a different installed tool").

## Lead's replay on this host

- Scratch generation with `--write` changed only report.ts lines 2–3. Drift checks at a28cbeb and at 0a3af77 then reported `changed: []`. The in-memory approval (B2) used for those runs is disclosed in the README and logged in evidence/generation/bypass-log-*.json.
- In a scratch architecture clone, a provisional scratch-only review.json and unit.json were written, and this entry was appended as contractSuccessors[65] of a scratch design-lock.json. The unmodified `verify_design.py --implementation` then passed with 66 contract units, 40 generation sources and 48 admission sources. The unmodified `generate_contracts.py`, in drift mode with no bypass, passed with `changed: []`. The same run without the entry refused with "generator closure is not selected by an accepted design unit". Those provisional files are not part of this unit, and your review replaces them.

## Decide

- Are the 8 parents the currently selected paths, with bytes identical to product 0a3af77? Are the candidates sorted, and do they cover the subject exactly? Is every materialization-map before and after pin correct?
- Does evidence/sigequiv.json, with its script, support "same pinned versions, only the OS code signature changed" for all 28 Homebrew Mach-O files? That includes the cargo `__LINKEDIT` vmsize-only difference. Is the stated limitation (comparison with the bottle, not with the old signed bytes) acceptable?
- Is it correct that no confined result changed on macOS 27? Check the positive and negative re-probe runs and the system.sb and dyld-support.sb diffs, including the removal of the espd lookup and the Rosetta cryptex read/map.
- Is the generator rebuild acceptable? It has the same sources, dependencies, builder and Rust 1.95.0, but a new digest, and the embedded temp build path is the stated cause. Is the disclosed unpinned libgit2 1.9.2→1.9.7 change acceptable, or does it need a pin or a finding?
- Is every other generator output byte-identical, and does report.ts change only in its provenance header?
- Is anything overclaimed, or missing from the "Not claimed" list?

review.json must contain the top-level fields "verdict" (ACCEPT-DESIGN-UNIT or REQUIRED-FINDINGS), "requiredFindings" (id, title, failureScenario) and "subjectManifestSha256" (1d1552bebd641098d5dcefcc11a63634e3af2a2dc25e213c08912a36a2d4b624). Write REVIEW.md and review.json. Do not commit.

## Lead note

Before commit, the lead replaced the host name with `<dev-host>` and the session scratch path with `/Users/sb/opensip-deps/native-repin-01/evidence-inputs` in 7 evidence files, then re-pinned the record and subject. The scratch validation pair was rebuilt from the committed unit: verify_design passed with 66 contract units, and generate_contracts in drift mode, with no bypass, reported generatorClosureSelected true and changed [].
