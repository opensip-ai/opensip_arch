# FX-PLAN-1 round 2 independent review

Reviewer: GROK2. Verdict: REQUIRED-FINDINGS. Reviewed at 2026-10-06T04:08:49Z.

Subject `docs/implementation/fallow-expansion/plan-r2/subject.json` is 1171 bytes, SHA-256 `985ae695df6b98177c3905e5fd95aaab6f847b8e66ee756cb4bef6d303e52068`. All six members match the manifest. The record has an empty `passageOverrides` list and no passage supersession. It selects a planning overlay. It does not change a contract passage, widen a schema, or qualify a capability.

Plan r1 was frozen and was not dispatched. This is the first independent review of the programme's plan subject. The r2 prerequisite text names components-r2 manifest `0afd515a2c19f9a466a6f409d0b815942b50f59e3b25d3c5835463f05e2a3aa4`.

## Required finding

### FX-PLAN-1-RF-01 (P1). The overlay leaves the accepted M3 planning record unresolved and calls r10 a draft

`IMPLEMENTATION.md` says the current M3 r10 record is explicitly a draft, uses r10 for navigation only, and tells the lead to resolve the exact accepted plan revision before publishing this amendment. `PLAN-AMENDMENT-r2.md` never names that revision.

The independent review `docs/implementation/m3/reviews/codex-m3-plan-r10/review.json` records verdict ACCEPT and `requiredFindings: []`. Its subject hash is `ec8c38f8c6ac8d522989ea6226363817a1b77c5b37560e72e2520088601bb964`, 226011 bytes. Those bytes are the current `docs/implementation/m3/M3-PLAN-r10.md`. The review names `M3-PLAN-r9.md` only as `diffBase` (150586 bytes, SHA-256 `72bc7a135014072fd06b84211f0535a0fece8b14280d0dc16059e6240de54a17`). Live `M3-PLAN.md` is 226459 bytes, SHA-256 `af4f835c969887ffd1aebbd3046791efb7bd9dcb4c3e24f5e320918781692e36`, because an acceptance note was prepended; that noted copy is not the reviewed subject.

r10's own text says the record is not law, not code, and not a contract successor. That limitation stands. The defect is the overlay's draft label and missing pin, which leave integration without the accepted planning record Codex reviewed.

Required correction: in `PLAN-AMENDMENT-r2.md` and `IMPLEMENTATION.md`, name `docs/implementation/m3/M3-PLAN-r10.md` with 226011 bytes and SHA-256 `ec8c38f8c6ac8d522989ea6226363817a1b77c5b37560e72e2520088601bb964`, and cite `docs/implementation/m3/reviews/codex-m3-plan-r10/review.json`. State that the record is planning and is not contract law, that its cutoff is earlier than product `f5f5b4d20eca34ab2312b3ffc141c378da326afe`, and that this amendment preserves r10's unit scopes, durations, and later accepted unit laws. Remove the unresolved "resolve before publishing" instruction and the claim that r10 is only a draft. Pin `M3-PLAN-r10.md`, not the noted `M3-PLAN.md`.

## What was checked and holds

Parents are sorted and match the foundational candidate pins exactly:

- `docs/implementation/fallow-expansion/capacity-r2/CONTRACT.md`, 7523 bytes, SHA-256 `f12adb1955fc9d4be179b7f6cba6fa01ceca02b5387b621a161f104832b105ff`
- `docs/implementation/fallow-expansion/components-r2/CONTRACT.md`, 9900 bytes, SHA-256 `f316c5c7adfab657593a1d7eb666aa3f1a76bd6c875198c05bc685184e235610`

Those pins equal the corresponding rows inside the capacity-r2 and components-r2 manifests. The amendment's prerequisite manifests are capacity-r2 `2148a4824286f0046fef02e070e3b0fe51c19a34fc6bd191820c6d3bf04e557d` and components-r2 `0afd515a2c19f9a466a6f409d0b815942b50f59e3b25d3c5835463f05e2a3aa4`. Both files on disk match. Neither parent path is already in the product lock. Binding this overlay waits until FX-CAP-1 and FX-COMP-1 are bound, so those CONTRACT candidates are accepted pins. FX-CAP-1 round 2 is already ACCEPT-DESIGN-UNIT. FX-COMP-1 round 2 is ACCEPT-DESIGN-UNIT in this same review session. Neither acceptance binds either unit. This plan verdict does not become acceptance by that condition.

The nine gap families are FX-CAP, FX-FR, FX-COMP, FX-STYLE, FX-METRIC, FX-API, FX-SEC, FX-EDITOR, and FX-QUEUE. They map to packages FX-P1 through FX-P6 and to the amendment's downstream rows. Each downstream family is a requirement to write a later exact law. The overlay claims no grammar pin, recognizer id, metric, public capability, editor authority, or ranking permission. HSR-1 stays the historical-reader law. HSR-a and E2s are the named materialization lanes so an older same-family schema generation cannot overwrite the widened capacity meanings. S-R and S-B stay separate owners. In-flight review subjects stay frozen. The seven-language grammar bundle cited by the adapter row is the existing M3-E bundle, and the foundation does not widen it.

`DECISIONS.md` records owner selections FX-D1 A and FX-D2 A. Its statement that the bound identity schema still limits `requestedCapabilities` to 1024 is the f5f5b4d baseline. Numeric authority for the expansion is the parent FX-CAP-1 contract, which this overlay does not restate as a passage change. Analysis-quality `PLAN-r6.md` is 65304 bytes, SHA-256 `8aed6eb8461592f68575b672d4f79248cded9c869a4ff124964aaffbc9a2f9f1`, and `docs/implementation/m3/analysis-quality/reviews/codex2-analysis-quality-plan-r6/review.json` records ACCEPT for that hash. The gap register uses that plan's qualified-versus-exploratory distinction and still withholds qualification from an advisory label. That reading is consistent with PLAN-r6's own statement that it is not a qualification threshold.

## Non-blocking observation

`IMPLEMENTATION.md` records architecture `2a5157d314ccfa9e37c0e1901391b2386c517369` as the drafting baseline. That commit exists and is an ancestor of live architecture HEAD `a9f6557eeb924d3163d7494e83adbd69106e41fb`. The amendment's product baseline `f5f5b4d20eca34ab2312b3ffc141c378da326afe` still matches this worktree, whose tree is clean. Recheck the live architecture head when the corrected amendment is bound. That baseline sentence is not the required finding.

## Methods and limitations

Every subject member and both parent pins were hashed and compared with the capacity-r2 and components-r2 manifest rows. Candidate coverage, sort, and the empty override list were checked against the pinned `verify_design.py` contract-successor rules (SHA-256 `7b313de629f2c958a1e62538b909d6f01545be2519238ba9b3d86ab7e7ba3326`). The M3 plan hashes were computed from the files and compared with `reviews/codex-m3-plan-r10/review.json`. A full baseline `verify_design` was not re-run. No repository file was edited. No product cargo, test lane, or lane lock was used. This verdict does not accept the overlay, does not bind it, and does not qualify a 1024-unit analysis or a component adapter.
