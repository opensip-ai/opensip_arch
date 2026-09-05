# G15 integration independent review v3

**OBJECT — 1 MUST-FIX, 0 SHOULD-FIX.** Reviewer: Codex `/root/integration_reviewer`; authored none of the 14 frozen subject bytes.

The exact frozen subject is `g15-final-security-freeze.v2.json`, SHA-256 `0c78e837ea5600e506573c4279742f012ffe141c522fa7a88a84b27fa10e102a`. All 14 subject pins are recorded in the companion JSON. `check_g15_final_security_v2.py` replayed 3425/3425 checks with exit 0 in an isolated environment.

The retained G15-PREFLIGHT-1 repair is present: the complete original envelope is structurally and canonically admitted before revoked-key filtering, preserving refusal for malformed revoked-key signatures. This covers the original filtering bypass concern; no subject bytes were edited.

One blocking integration finding remains. G15 v2 explicitly binds security v7 (`security-freeze.v7.json`, SHA-256 `b289fb…`), while the application manifest pins independently accepted security v8 (`security-freeze.v8.json`, SHA-256 `33dad5ec1692ccbee859ead54d17d9730999a2d61012e2e48cbd1d2ad27e44ca`). A bounded v3 rebind and replay against v8 is required before this unit can be accepted for the application. No qualification or register change is claimed.
