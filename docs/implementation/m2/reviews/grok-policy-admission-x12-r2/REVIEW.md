# Law X12 r2 — configuration and policy-pack admission

Law review only. No product cargo. The OpenSIP support directory is absent. Subject `policy-admission-x12/PROPOSAL.md` is 26394 bytes, sha256 `62bcdab188cdb8d67a7c2cef8d8715829d7fbc2d913433fda38d67458d2ad3bc`, matching `hashes.txt`. Preserved r1 is `PROPOSAL-r1.md`, 23279 bytes, sha256 `f1d5c19cdf94d2d69493b160d53c67cb4916ec0329afc87e281c5df6c0f362a6`, the reviewed r1. Live product HEAD is `66bdd05ea71f8293ae104da697dbcf96f7d52f44`.

The diff from r1 is the title, the r2 provenance sentence, the Named-source failure paragraph in item 6, rows 3 and 4, the RF-1 and RF-2 remedy paragraphs, the rejected-alternative paragraph, the NT-2 and bundled-defect tests, the remedy byte test, the X12-0 unit, X12b's dependency and emission, the EXIT-PLAN row text, and two new forbidden bullets.

## What holds

r1 RF-1 is closed on the rows. Item 6 says a `Named` source failing step 1, 2, 3, 5, 6, or 7 is a signed-core defect, and only a step 4 failure is the caller's. Row 3 is a `Supplied` document failing item 6.2, detail `POLICY.IMPERATIVE_KEY_REFUSED`, subject the member's pointer. Row 4 includes a bundled item 6.2 failure and keeps subject `pack:<packId>`, class operational-failed, exit 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, fault `host-invariant`, detail `HOST.INVARIANT_VIOLATED`. Item 10 expects a bundled `exec` key to give row 4. The release self-check still refuses to ship that row. The caller-document NT-2 cases stay on row 3.

r1 RF-2 is closed. The claim that the registered `CONFIG.INVALID` detail already states the pack condition is gone. The law quotes `PUBLIC_ROUTE_REMEDIES["CONFIG.INVALID"]` from `native/native_evidence_model.v2.py`: "the configured capability selection is invalid: name a registered capability id from the native capability matrix, and state at most one row per (capabilityId, languageMode, workspaceRoot)". That quote matches the published string. The remedy-keying constraint keys the table by public code, and the three external-configuration keys that reach `CONFIG.INVALID` are `native.requested-capability-unregistered`, `native.requested-capability-mode-unregistered`, and `native.requested-capability-duplicate-ownership-tuple`. X12-0 widens that one string so it stays true for those keys and for rows 1, 2, and 3a. The widened text must say, in substance, the capability-selection sentence, exactly one bundled pack id, and no caller-supplied policy document. Exact bytes stay with X12-0's own review. X12-0 depends on nothing, precedes X12b, and X12b depends on X12a and X12-0. No row 1, 2, or 3a is emitted before X12-0 lands. The public code stays `CONFIG.INVALID`. Minting `POLICY.PACK_UNREGISTERED` or `PACK.NOT_BUNDLED` stays rejected. `CONFIG.INVALID`, `HOST.INVARIANT_VIOLATED`, and `POLICY.IMPERATIVE_KEY_REFUSED` remain rows in `public-detail-registry.v1.json`.

The r1 holdings on the zero-row registry, `name:version`, the pure order, and the X12d replay deferral stay in force.

## RF-1

The Declarativeness prohibition still forbids an imperative member or a string expression from surfacing as any detail other than `POLICY.IMPERATIVE_KEY_REFUSED`.

Row 4 requires a bundled imperative member to surface as `HOST.INVARIANT_VIOLATED`. The new types-and-codes bullet forbids that member from surfacing as row 3, and row 3 is the row whose detail is `POLICY.IMPERATIVE_KEY_REFUSED`. Item 10 requires the bundled `exec` key to give row 4. The public result the row requires is a result the declarativeness bullet forbids, so a bundled `exec` key has no result that satisfies both.

Required: scope that declarativeness bullet to a document the caller presents, so the document surfaces as row 3 with detail `POLICY.IMPERATIVE_KEY_REFUSED` and the member's pointer. A bundled imperative member surfaces as row 4.

## Verdict

REQUIRED-FINDINGS. RF-1.
