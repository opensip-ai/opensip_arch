# Independent owner adjudication — retained trust-record admission at the recovery boundary

Reviewer: Claude (actual independent reviewer; Codex owns the decision). 2026-09-18. Request: `REQUEST.md`.
Question: my platform123 F-3 — recovery proposes/applies with deleted or malformed `rootExpiresAt`,
`revocationIssuedAt`, `catalogExpiresAt`, `anchor`. Adjudicated against frozen **reference 122** and
product **123**. Bounded owner adjudication, not code acceptance. No frozen/selected/product edit, commit,
push or delegation.

## 1. Owners read (exact bytes)

| Owner | SHA-256 | What it says |
|---|---|---|
| `security/security-lifecycle.schemas.v1.json` (122) | `79a1b38d335b53bedaca8c695518335028e5d102b9e229ec9ec470f1e2419e91` | **`TrustClockRecordV1`** (l.661): "SC-TRUST clock and floor fields (state, host-private)". Closed (`additionalProperties: false`), **all 11 members required**: `evalHighWater`, `lastAccepted`, `revocationIssuedAt`, `catalogExpiresAt`, `rootExpiresAt` (each `NullableTimestamp`), `anchor` (`Anchor` \| null), `rootVersion`, `indexSnapshotVersion`, `revocationVersion` (`I64Positive`), `recoveryEpochSerial` (`I64NonNegative`), `pendingRecoveryChallenge` (null \| `PendingRecoveryChallenge`) |
| `security/security_lifecycle_model_v1.py` (122) | `60b14495b38ec3c9927aea5272360d17081277463365f54d6ec71f134528939b` | `_recovery_challenge` (l.1146), `_recovery_apply` (l.1225), `RECOVERY_BOUND_FIELDS` (l.1122), `clock_decision` / `_states` (l.957, l.1105) |
| `security/check-security-lifecycle.v1.py` (122) | `cd039650018b372bd9e21b35235c9c4f5f422fc7a9f491b1dc2c318fdcd19b6a` | validates case *inputs* against `inputSchemas` (l.180) |
| product 123 `trust.rs` | `8f3b37357d8bb85d173281b68bf3078e6d13453b29ac03bfc8442d985f13d8a1` | `propose_recovery` (comment: "The record is an already-admitted storage projection, not a storage authority constructor") |
| product 123 `trust_time.rs` | `eed6873973a082a6a2f5e9a52f62bd12e364264c99c7e83ec860a355090e2dde` | `assess` takes a typed `Record`; nothing constructs one from stored state |

## 2. Findings of fact

1. **An owner exists: `TrustClockRecordV1`.** It is exactly the "well-shaped entire admitted trust state"
   you prefer, with owner-defined nullable/fresh states already in it.
2. **Nothing enforces it.** In the whole 122 candidate it is referenced only by the schema file, the
   README, and `trust-recovery-cases.v1.json` as an `inputSchemas` **declaration** — the checker uses that
   to confirm the *test inputs* are valid. Neither `_recovery_challenge`, `_recovery_apply` nor
   `clock_decision` calls `validate_input('TrustClockRecordV1', …)`. The challenge validates only the six
   `boundRecord` members (via `TrustRecoveryChallengeV1` plus `ts()` on the two times); apply checks the
   pending shape, the three counters and the two times.
3. **No caller invariant excludes it.** The Rust comment asserts prior admission, but no type, function or
   owner performs it: `propose_recovery` takes `record: &V`; the state decoder that would construct an
   admitted record does not exist yet; and `assess`'s typed `Record` has no production constructor. So this
   is an unowned precondition in both reference and product — the same shape as 119 I-1.

## 3. Executable cases (`claude-out/cases.py` → `cases.json`)
Every single-member deletion or replacement of the fixture's valid record (13-value pool), run through the
122 `recovery_apply`, the 122 schema, and — for those applied — through `clock_decision` on the record
*after* recovery's writes. Rust 123 agrees with the reference on all of them (my 123 probe, 280/280).

| Applied by recovery | Count | Owner schema | Clock after recovery |
|---|---|---|---|
| valid values (null, a valid timestamp, a valid serial, a valid pending) | 9 | valid | PROCEED |
| `anchor` replaced by `true`, `0`, `-1`, `""`, `[]`, `{}`, strings, … or deleted | 13 | **invalid** | PROCEED — recovery's write clears `anchor` |
| `revocationIssuedAt` / `catalogExpiresAt` / `rootExpiresAt` **deleted** | 3 | **invalid** (required) | PROCEED with that state reported expired/stale (fail-closed) |
| the same three members replaced by a non-timestamp | **33** | **invalid** | **`REJECT: TIMESTAMP_GRAMMAR`** |

So of 58 applied, **49 are schema-invalid**, and **33 end in a record the clock can never evaluate**:
recovery reports `APPLIED` — consuming the single-use pending challenge and an epoch serial — and leaves
the installation exactly as unusable as before. Everything touching a bound member, a counter or the
pending challenge was already refused.

**Compatibility with recovering a clock fault — it is compatible.** The fault recovery exists for is a
*poisoned* floor, not a malformed one: a record with `evalHighWater` decades ahead **validates**; a record
with every nullable member null **validates**; the fixture's own records validate. And the bound members
already have to be well-formed for a challenge to be issued at all, so complete-record admission adds no
new refusal for the members recovery actually repairs. What it newly refuses is recovery on a record whose
*unbound* members are corrupt — which is storage corruption, a different remedy (restore →
`ST-UNBOOTSTRAPPED:RESTORED`), and should be said so.

## 4. Classification

| Case | Verdict |
|---|---|
| Expiry member null | **Valid** owner-defined state (expired/stale, fail-closed) |
| Expiry member a well-formed timestamp, any value | **Valid**; irrelevant to recovery, re-evaluated at signed time |
| Expiry member a non-timestamp | **Defect** — successful recovery of an unevaluable record |
| Expiry member or `anchor` **absent** | **Defect** by the owner schema (all 11 required); benign today only because `.get()` reads absence as null. Do not let "absent" and "null" become two spellings of a state |
| `anchor` malformed | **Defect** by the schema; harmless in effect because the write clears it. I would still refuse: the alternative is a per-member rule about which corruption recovery may overwrite, and `anchor` is not digest-bound, so nothing would record that it was overwritten |
| Residual members beyond the 11 | **Refuse** (`additionalProperties: false`). The schema is a *projection* of the SC-TRUST state (the floor-migration shapes show that state also carries `roles`), so the admitted input is the projection of exactly these members, never the raw state |

## 5. Minimal correction

1. **Reference:** `validate_input('TrustClockRecordV1', record)` as part of "strict shapes first" in both
   `_recovery_challenge` and `_recovery_apply`, and at the head of `clock_decision`. One detail,
   `RECORD_SHAPE` — Rust already has it (`RecoveryError::Input("RECORD_SHAPE")`); today the reference has
   no such detail and falls back to `CONTEXT_SHAPE` through its exception wrapper.
2. **Precedence** (keeps every existing fixture expectation): epoch shape → observation shape →
   **pending shape (`PENDING_SHAPE`, unchanged)** → **complete record (`RECORD_SHAPE`)** → root admission →
   authority → freshness → binding → counters → time. Pending first, because a malformed pending also
   fails the record schema and its specific detail is already pinned by cases; record shape before any
   authority work, because a shape refusal must not depend on signatures.
3. **Typed input owner (Rust):** one private `AdmittedTrustRecord`, constructed only by the state decoder
   from the 11-member projection, consumed by `assess`, the challenge and `propose_recovery` in place of
   `record: &V` — and built in a child module with private fields, per my 123 F-1, so the guarantee is not
   again one assignment away. Until the decoder exists, `propose_recovery` should perform the complete
   shape check itself rather than cite an admission nobody performs.
4. **Cases to add:** the 33 malformed-expiry and 13 malformed-anchor inputs above (expected
   `RECORD_SHAPE`), the three deletions, an unknown extra member, and the three positives (all-null fresh
   record, poisoned floor, valid far-past expiries).

## 6. Bounded verdict
**The owner exists (`TrustClockRecordV1`) and is not applied; no caller invariant excludes the malformed
cases in either the reference or Rust. Complete-record admission at the recovery and clock boundaries is
sufficient, is compatible with recovering a poisoned floor, and needs one detail (`RECORD_SHAPE`), one
precedence slot and one typed Rust owner.** 49 of the 58 accepted mutations are defects by the owner
schema; 33 of them make a "successful" recovery useless. This adjudicates the owner question only; it
approves no schema, model or code.

Evidence: `claude-out/cases.py`, `cases.json`, `hashes.txt`; Rust outcomes from
`claude-platform123-20260918-r1/claude-out/probes/nv-still-proposed.txt` and `nv-recovery-vs-reference.json`.
