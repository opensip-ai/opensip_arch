# Broker integration independent review v2

**OBJECT — 1 MUST-FIX, 0 SHOULD-FIX.** Reviewer: Codex `/root/integration_reviewer`; authored none of the seven frozen subject bytes.

The exact frozen subject is `broker-bootstrap.freeze.v5.json`, SHA-256 `e5155b3681c55e2685671e4631f6b059177ffb99f7ccdf9682c5e0f0855e4191`. All seven subject pins are recorded in the companion JSON. The v5 checker replayed 93/93 bootstrap checks and its embedded courier/security replay reports 273/273 checks, with exit 0 in an isolated environment.

The reviewed joins cover the security rebind host path, complete effectRequest/effectResult bodies and correlation, commit and journal ordering, strict scope joins, and HE-1/HE-2 exact snapshot and bounded custody rules. No subject bytes were edited.

One blocking integration finding remains. Broker v5 explicitly binds security v7 (`security-freeze.v7.json`, SHA-256 `b289fb…`), while the application manifest pins independently accepted security v8 (`security-freeze.v8.json`, SHA-256 `33dad5ec1692ccbee859ead54d17d9730999a2d61012e2e48cbd1d2ad27e44ca`). A bounded broker successor must rebind the security receipt, host join and courier/security checks to v8 and receive independent replay/review. No qualification or register change is claimed.
