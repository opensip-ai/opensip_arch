**Verdict: CHANGES-REQUIRED.** The schemas are sound; my probes found no schema-behaviour defect. The unit still can't be accepted, for three reasons that stay within RF-01. Nothing is accepted by this review. Once the three fixes are made and accepted, only this design/reference correction would be accepted; product implementation, successor binding and the M1/runtime/release gates still remain.

**What held up**
- **Hashes:** all 10 subject files matched the manifest (`bccfda51…`) before and after the review.
- **Checker:** exit 0, 28 schemas, all 43 cases as expected.
- **Pins:** all 25 non-candidate pins match the v45/v46 overlay (the after-image where v46 also records a before-image) and the live bytes.
- **Compatibility:** remove the metadata branch and the parser-refusal rule, and envelope4 is exactly envelope3. Inventory4 changes only the help/version dispatch, the added `build-channel` field and the JSON renderer version.
- **Probes:** 102 of my own. 93 behaved as expected, covering meta exclusivity, exact integers, Unicode scalar lengths, SemVer and closure-ID limits, strict ordering, strict JSON parsing and inventory mutations. The other 9 are all about coverage routing and successor binding (below).
- **Signing direction** has no cycle. **No-effects bootstrap** is stated clearly but is prose only; no product code was run.

**Parser refusal with `errors=[]`:** sound, D9-compatible and complete, needing no different correction.
- None of the 319 registry detail codes is a general argument/option detail.
- D9 already maps all malformed invocation to `REQUEST.UNKNOWN_OPTION` (exit 2).
- The D9 v1.14 golden `pre-admission-unknown-option` expects exactly `{request-rejected, REQUEST.UNKNOWN_OPTION}` with no detail, which is the termination the candidate fixes.
- Probes confirm empty errors are refused for every other code, kind, exit, detail, `runId` and missing diagnostics.
- Optional hardening only: `diagnostics:[""]` and control characters in echoed argv are allowed, and `projectId` isn't forbidden on this branch.

**Required findings**
1. **RF-A, coverage routing:** `implementation-coverage.v2.json` L1177/L1209 still say "CommandEnvelope-major-3" and "build-embedded release descriptor". No coverage row routes the parser-refusal rule, the build metadata record or the M1 development-only negative.
2. **RF-B, successor binding:** `successor.json` doesn't bind `README.md`, the only place the catalogue, trusted-build, bootstrap and signing rules are written. It also doesn't list the accepted passages that still say "signed release descriptor": build plan L885, ch14 L325, and repository-file-inventory v1 and M1 v3, both L279.
3. **RF-C, second build channel:** the accepted plan compiles `HostAssetPinV1` with its `buildChannel` and says "No second untrusted self-declaration is introduced". The candidate adds `BuildMetadataV1.buildChannel` without saying the two come from one build selection. Nothing tests them disagreeing.

The review also has 8 advisories. One: the checker's semantic comparison hides some schema rules, so deleting the development empty-closure rule or the help ordering rule goes unnoticed by the envelope fixtures. Limitations recorded: whole-corpus closure wasn't evaluated (the RF-03 Atom issue is not counted as a pass), and only one validator version was used.

Everything is in `/tmp/opensip-implementation/m1-metadata-review-01`:
- review.md
- review.json
- checker-output.json
- probes.py
- probe-results.json
