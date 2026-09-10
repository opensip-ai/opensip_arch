I’ll amend the three chapters’ owner-closure wording first, then read workflow/security admission as-is and write a v5 detector-compatibility proposal without touching workflow files.I’ll correct the three chapters’ owner-closure wording, then write a v5 detector-compatibility proposal that joins the existing workflow schema instead of forking it.v5 is at `/tmp/opensip-design-corrections/grok-evaluator3-contract-joins.v5/`. Official suites were not run. SEAL adapter was not re-run. Workflow files were not edited.

**Chapters.** `identity-model.py.close_run` is no longer called hash-only. It is historical **owner-closure admission**: exact schema, identity, and native owner joins. It is not evaluator3 semantic replay. Current minting stays `identity-model.v3.close_run`. Two narration fragments were removed from current law (native H-1 “Codex-owned”; admission “this design turn”). Qualification limits are unchanged.

**Detector compatibility.** Workflows-and-surfaces §2 already requires `declared-compatible`. Workflow v3 already has `DetectorManifestV1` (`compatibleClosures: [{closureId, semanticsMajor}]`) and refuses caller `compatibleWith`. Do not fork that schema.

Proposal: after the existing trust trio admits the detector `closure2` (retained generation / installed signed release / signed bundle), project `DetectorCompatibilityProjectionV1` from `blobs[closure.manifestDigest]`. No `signatureVerified` flag. `ruleStableId` joins through emission bindings, not extra listing rows. Envelope `verify_envelope` remains TCB; closure identity is not release authority. Workflow v1 caller `compatibleWith` stays historical.

Full proposal: `detector-compatibility-proposal.md`. Root can attach that to workflow v10 delivery.
