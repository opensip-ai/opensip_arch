# LEAD-CORRECTION-REVIEW 2 — security v7

**OBJECT: 0 MUST-FIX, 1 SHOULD-FIX.** The frozen subject is [security-freeze.v7.json](security-freeze.v7.json), SHA-256 `b289fb968d8958c99d22990547ee0e1cb3faab939f33013a20ac0c5931752efd`, containing 72 frozen files. I authored none of its bytes. Dispatch is [security-lead-review-dispatch.v2.md](security-lead-review-dispatch.v2.md), SHA-256 `15d6d1f54cf1e41a6aaa77e1ac39d096f5c9ecdb14b22a3d93a174274930b1bf`.

The independent replay of `check-security-unit.v7.py` passed **864 checks, 0 failures**. Replay report: `/tmp/security-lead-review-v2-replay.json`, SHA-256 `d01c96d45ba26a2cd85284fce99cc34e1ff8586cc4d7a1c4dcade51bcf5c57e9`; frozen report SHA-256 remains `a02c92c2e41410d80d262aa148108b10e3876ccd3d22c2275d99893b6cf661c3` and was not modified. The exact v6→v7 composition is 6 changed paths and 66 byte-identical paths; no files were added or removed.

Lead review 1 findings are resolved in security outcome. Full envelope canonicalization rejects float `envelopeSchema: 2.0` before schema/signature use; policy stateClass cannot be introduced by a project layer and any refusal yields zero effective grants; and the normative courier context now uses `scratchDirSt`/`fileSt`. Prior v5 root, traversal, broker/courier, witness/recovery, policy duplicate, journal and malformed-record controls remain in the replay and mutation suite.

One exact contract defect remains:

1. **SEC7-LR2-S1 — SHOULD: canonical envelope mutations use the wrong refusal class.** Changing only the valid envelope's `envelopeSchema` from `2` to `2.0` returns `RJ-4 ENVELOPE_MISMATCH` through the outer `boundary exception Reject` path. Section 2.2 (v7 lines 144–147, incorporating v2 §2.2 lines 124–133) assigns malformed envelope input to `RJ-4 UNSIGNED`, and canonical-profile rejection occurs before routing, digest, and signature use. Unknown-member and missing-member controls already return the expected malformed class. Catch `Reject` with `SchemaError` in step 1 and return the fixed canonical-profile malformed-envelope token. The boundary fails closed, so this is an exact refusal-precedence contract issue rather than an authority bypass.

History is retained exactly: three ordinary exchanges, one UPHOLD, two failed bounded confirmations, and lead review 1 OBJECT (2 MUST/1 SHOULD). There is no reset and no third confirmation. This OBJECT is the required user notification before another repair round; it grants no implementation permission, register edit, platform qualification, or adoption.
