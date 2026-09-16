Candidate 05 is written and fixes all four review-04 required findings and all five advisories.
- **Check:** 567 checks, 0 failed.
- **Selftest:** all 132 controls caught with a clean baseline, including the 4 review-04 mutants that previously went uncaught.
- **Isolation:** copying only the 40 inputs, the check reran with identical results and the selftest caught all 132 controls again.
- **Outcome:** `outcome.json` marks RF-1..RF-4 and A-1..A-5 as resolved against named checks. This is author readiness for review, not approval.

## Candidate paths

Everything is in `/tmp/opensip-implementation/m1-native-wire-owner-author-05/`. The execution closure in `tools/filelist.py` has 40 inputs.
- **Built outputs:** `wire-carriers.v1.json`, `owner-pattern-successor.v1.json`, `public-route-successor.v1.json`, `successor.json`, `admission-vectors.json` (333 vectors in 30 groups), `p3-guard-successor.v1.json`, `field-coverage.json`.
- **Changed code:** `check.py`, `selftest.py`, and in `tools/`: `owner_successor.py`, `representability.py`, `sender_ref.py`, `check_static.py`, `check_reference.py`, `check_routes.py`, `rules.py`, `public_routes.py`, `succ.py`, `vectors.py`, `build.py`, `common.py`, `filelist.py`, `outcome.py`, `isolation.py`, `manifest.py`.
- **New input:** `prior/review-04/probe_dialect_scope.out.json`, which the checker replays.
- **Pins:** 8 new architecture pins, 44 in total. They are the foundation documents that identity-model.v3 loads for its relation-payload admission.
- **Contract:** `contract.md` holds the per-finding dispositions.
- **Results:** `check-result.json`, `selftest-result.json`, `isolation-result.json`, `outcome.json`.
- **Manifest:** `subject-files.json` (sha256 `40a79ffe…6b46735`).

## What changed per finding

- **RF-1 (defaulted, partially stale prepared sets).** The prepared-set wire limit now applies to every outcome the owner doesn't reject, including the defaulted partial-stale fallback.
  - **The owner stays first:** its non-inert and stale refusals are checked before the wire limit. The path refusal, which runs before the owner over every row, outranks both, and this is now stated.
  - **Changed from what you asked:** you asked for the check on the usable rows. The manifest has to carry every row of the set, stale and failed rows included, because each entry answers a row and the set identity is recomputed over all of them. So the limit is counted over the carried rows, which include every usable row.
  - **Why it matters:** counting only usable rows would admit one stale row plus 256 usable rows, and the carrier would refuse the resulting 257-entry manifest, as in review-04.
  - **Defaulted and over the limit:** the set is not selected. The outcome is a fallback with zero usable rows, the stale rows kept and a disclosure.
  - **Planner:** it now also refuses snapshot, dependency and prepared manifests over their entry bounds, including the review's 299-entry plan.
  - **Coverage:** vectors cover stale, non-inert, failed, invalid-path and over-limit rows in both modes.
- **RF-2 (ECMA scope).** No shared validator is patched any more.
  - **Scope:** in each of four declared modules only the module's own validator reference is replaced by a scoped view. It uses ECMA only for pattern nodes in these scoped documents:
    - the evidence schema, in the native and startup models;
    - the occupancy schema, in the wire model;
    - the relation-payload schema, in identity-model.v3 `validate_registered_record`.
  - **No-change checks:** one per non-parent document review-04 named: identity v2, identity v3, workflows common, c2v3 and rust2. Each runs the review's own changed examples through the real consumers, pinned against successor, and requires equal results.
  - **Proof they bite:** every example is a real ECMA/Python difference, and controls that widen or narrow the scope both fail.
  - **Fact-plane owner:** `check-fact-plane.py _is_path` needs no change. It has no lookahead and refuses control characters.
- **RF-3 (relation-payload paths).**
  - **Correction:** the relation-payload `CanonicalPath` now has a correction row.
  - **Vectors:** all four sites (`FilePayloadV1.path`, `PackagePayloadV1.manifestPath`, `VcsChangePayloadV1.path` and `previousPath`) get 24 vectors.
  - **Execution:** they run through `validate_registered_record`, which is the call retained fact admission makes. The check confirms that call in the pinned source.
  - **Results:** `x<LF>/../y.rs` is refused and `a/..<LF>` is admitted, and the pinned model is shown to do the opposite at every site.
  - **Not driven:** a full retained-bundle `admit_frame` run, because no retained bundle is available.
- **RF-4 (sender Cancel law).** The plan now carries the expected Cancel echo, and the sender refuses a Cancel before Hello and any Cancel that isn't the exact echo for its position.
  - **Vectors:** they cover wrong or early execution IDs, ordinals and reasons (both protocol majors) and payload-byte divergence with the same frame type and the same chunk coordinates.
  - **Cross-check:** the sender's echo agrees with `CANCEL-NULLABILITY` at all 17 positions of two plans.
  - **Defensive branches, stated as such:** the over-reserve check and the per-frame limit re-checks can only fire when a plan is consumed under different limits. Vectors exercise exactly that.
- **Advisories.**
  - **A-1:** every (key, fault) remedy phrase is bound, including "generated-file logical path"; the remedy wording itself is unchanged.
  - **A-2:** covered under RF-4.
  - **A-3:** the precedence is stated.
  - **A-4:** the eight integration duties are declared and checked.
  - **A-5:** the pins and the Node trust boundary are kept.

## Other findings

- **Fact-plane path law is stricter than the corrected schema.** It still refuses legitimate newline names such as `a/..<LF>`. That is the fact-plane unit's law; I recorded it and didn't change it.
- **Pinned occupancy `LogicalPath` had a different defect.** Python's `$` matches before a final newline, so it refused both the bad and the legitimate path. It did not have the lookahead defect.
- **Identity `LogicalPath` is deliberately left as pinned.** Any change there belongs to the identity unit.
- **Worker duty for partial-stale fallbacks.** A fallback set within the limit still carries its stale and failed rows, so the worker must never read them. This is listed as a duty.

## Disclosed and not claimed

- **Corrections this round:**
  - an editing slip in `succ.py` broke parsing; the build caught it and I fixed it;
  - one check failed on the first full run (567 checks, 1 failed) because a source probe searched too short a window. After the fix it passes (567/0).
- **Evidence preserved:** review-04 and root-validation-04 evidence is kept as byte-identical copies under `prior/`. Nothing was imported from a frozen subject, and there is no bytecode outside `tmp/`.
- **Not claimed:** approval, product integration, promotion of the owner source files, production codec, admission, sender or generator, M2/M3 or platform qualification, a clean git state, general confinement, or the Node system libraries.
