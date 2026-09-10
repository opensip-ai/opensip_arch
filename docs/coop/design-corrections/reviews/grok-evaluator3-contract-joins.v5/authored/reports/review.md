# Native/security chapter reconciliation and detector-compatibility owner assessment — v5

**Standing.** Actual Grok architecture/reference. Isolated `evaluator-successor.v1`. v4 source/report retained. Not independent acceptance. Workflow files read only. Official suites not run (root pin-seal pending). SEAL adapter 8 not re-run (no defect).

**Verdict.** `OWNER_CLOSURE_WORDING_CORRECTED_AND_DETECTOR_COMPAT_PROJECTION_PROPOSED`.

## 1. Three-chapter wording

`identity-model.py.close_run` was called “hash-only”. That is false. It is `open_run_closure`: exact schema, identity, and native owner joins over retained descriptors. It lacks evaluator3 semantic replay. Current minting remains `identity-model.v3.close_run`.

Amended:

- `native-evidence.md` joint interfaces
- `security-and-lifecycle.md` cache/regeneration paragraph
- `admission-and-qualification.md` `check-identity.py` description

Also removed two narration fragments from current law: native H-1 “Codex-owned”; admission “this design turn does not implement that host Plan builder” → later-stage Plan construction, this section does not author the builder. Chapter standing/review histories (S13, native standing) stay as review record, not current dispatch.

Qualification limits unchanged: synthetic graphs do not qualify compilers; linearize is not product SEAL; prefix dispatch is not close_run.

## 2. Detector compatibility (proposal only)

Workflows-and-surfaces §2 already names `declared-compatible`. No security-owned listing existed after trust admission. Workflow v3 already published `DetectorManifestV1` (`compatibleClosures: [{closureId, semanticsMajor}]`) and refuses caller `compatibleWith`. Do **not** fork that schema.

Proposal (full text: `detector-compatibility-proposal.md`): after existing trust-trio admission of the detector `closure2`, project `DetectorCompatibilityProjectionV1` from `blobs[closure.manifestDigest]`. Trust trio already owns verification. No `signatureVerified` flag. `ruleStableId` joins through emission bindings, not extra listing fields. W v1 caller `compatibleWith` remains historical.

## Checks

- Official native/security suites: **not run**
- Pin bypass: **not run**
- SEAL adapter: **not re-run** (v4 8/8 stands; no defect)

## Hashes (sha256)

| file | bytes | sha256 |
|---|---|---|
| `native-evidence.md` | 263011 | `23eb41bedfe528dfcaa0c437d5664bf8990676d356338d043525e8c470b78ff7` |
| `security-and-lifecycle.md` | 90842 | `3c5ab26382dbbc5954c17aff3ca2d8b67e3152ab5fc5109ada0a63bb390ff94d` |
| `admission-and-qualification.md` | 27249 | `c51f012028bd2a7a5febd89930d4838b7e6e056eff270635ce5c739e1c43a136` |

Read-only W: detector-manifest schema `ce54903a8806ae5e3d3dcbb3b1a787719af252a802128826b54597ae1f00bd58` (1853); `workflow_projection_model.v3.py` `482a312a2d0eaaf7f2e0226d828191d1f3270a29351e2dfd187a26c6f015ba76` (100470); `workflows_model.v1.py` `b83f910f107a6e7aba886dc5a07ce738eb73beec72c124ba03a34e5ae9b60156` (139660).
