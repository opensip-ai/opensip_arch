# RETAINED-MACHINE-NOTE — follow-up to my trust206 assessment

Separate note; `REVIEW.md` here is unchanged (its `hashes.txt` still verifies). **Assistance only, no frozen approval.** Sources read (read-only, repository working tree, *outside* my frozen 201 extraction): `docs/coop/artifacts/signed-index-trust-contract.v14.json` — SHA-256 verified `039a570244441709c8a773d2c92944fff7ad1b249718656ab2d87645feec6715`, equal to the pin tables in `security-completion.v1.md` l.22 and `security-completion.v2.md` l.23 — and `docs/coop/completion/security-completion.v2.md`. I read the incorporated clauses against the later supersessions I know (v8 §4.2/§4.8/§5.5, S&L S4/S4.5/S9/S9.1, STP); I do not adopt the historical candidate wholesale.

## 0. Retraction
My 206 §3(b) proposed a **scalar** `standing = established | unbootstrapped(reason)` on the argument that every other `ST-*` value is recomputable from (documents, clock record, `tEval`). **That is wrong, and root's rejection is correct.** I drew it from the fragments inside the 201 tree and flagged the missing machine as gap G1 instead of stopping there. The machine has durable, non-recomputable history:
- `machine.discipline`: "One machine per trust role. Roles do not share a single collapsed state. A CORE expiry is not an INDEX expiry."
- `ST-QUORUM-LOST` on `EV-QUORUM-OBSERVE`: "Still-below stays. **Restored quorum also stays**: leaving ST-QUORUM-LOST requires an ordinary payload refresh, not this event."
- `ST-REVOKED`: the ordinary-payload transition lists only `ST-EXPIRED, ST-STALE-REVOCATION, ST-QUORUM-LOST` as sources — REVOKED is not among them; its only named exit is `EV-RECOVER-BEGIN`. `monotonicStore.rule`: "No transition in this machine may decrease a counter or **forget a revocation observation** because an executable generation rolled back."
- `ST-RECOVERY`: "deliberately not EV-CLOCK-preempted"; abort goes to the "safety-dominant-still-true" candidate in order `REVOKED, QUORUM-LOST, EXPIRED, STALE-REVOCATION`, else `ST-UNBOOTSTRAPPED`, **never `ST-TRUSTED`** ("Does not restore prior TRUSTED by silence").

## 1. G1 — the closed machine (now located)
Seven states `ST-UNBOOTSTRAPPED, ST-TRUSTED, ST-EXPIRED, ST-STALE-REVOCATION, ST-QUORUM-LOST, ST-REVOKED, ST-RECOVERY`; nine events `EV-PRESENT-PAYLOAD, EV-CLOCK, EV-REVOKE, EV-QUORUM-OBSERVE, EV-RECOVER-BEGIN, EV-RECOVER-COMMIT, EV-INSTALL, EV-CONTINUE, EV-RECOVER-ABORT`; 19 named transitions; precedence `REVOKED > QUORUM-LOST > EXPIRED > STALE-REVOCATION > RECOVERY > TRUSTED > UNBOOTSTRAPPED`; fallback per event. **Closed for the text; open for standing**: neither file is in the 201/205 frozen candidates' pins, so the *current* candidate has no pinned owner for the machine its trust capsule would persist. If the capsule depends on it, the next reference checkpoint must pin/incorporate v14 (and the v2 clauses) explicitly. *(remaining gap R1)*

Durable vs derivable, per state — this is the part I got wrong:

| State | Entered by | Left by | Durable? |
|---|---|---|---|
| `UNBOOTSTRAPPED` | initial; v8 §5.5 declared restore (`RESTORED`); S9 migration (`MIGRATED`); recovery abort fallback | ordinary PRESENT; RECOVER-BEGIN | **yes**, with reason |
| `TRUSTED` | ordinary PRESENT from UNBOOTSTRAPPED/TRUSTED/EXPIRED/STALE/QUORUM-LOST; RECOVER-COMMIT | — | **yes**, but never usable without re-evaluation at `tEval` |
| `EXPIRED`, `STALE-REVOCATION` | `EV-CLOCK` guards | ordinary PRESENT; RECOVER-BEGIN | the *condition* is a monotone function of (accepted documents, `evalHighWater`) — v2 §4.7: clock reset ⇒ "nothing un-expires" because `evalHighWater` is write-ahead. Re-evaluating never heals; so these need no independent durable bit, **provided** the persisted `TRUSTED` is always re-evaluated before any effect (root's "reevaluate current freshness before effects") |
| `QUORUM-LOST` | `EV-QUORUM-OBSERVE` below threshold | ordinary PRESENT; RECOVER-BEGIN | **yes — not recomputable** |
| `REVOKED` | `EV-REVOKE` (from almost every state) | **only** RECOVER-BEGIN → RECOVER-COMMIT | **yes — must not be re-derived from "the current list" alone** (see G3) |
| `RECOVERY` | RECOVER-BEGIN with staged inputs | COMMIT → TRUSTED; ABORT → still-true condition / UNBOOTSTRAPPED; REVOKE / QUORUM-OBSERVE still leave it | **yes**, plus ceremony evidence |

**Consequence for the representation.** Persisting only the *visible* state token is also insufficient: abort from `ST-RECOVERY` must return to the safety-dominant condition that is *still true*, and a ceremony begun from `ST-REVOKED` must come back to `REVOKED`, not `UNBOOTSTRAPPED`. So what is durable is the set of **sticky conditions**, from which the visible state is computed by the owner's precedence — not a cache of the computed label:
```
"roles": { "<TR-*>": {
    "bootstrapped": true | false,
    "unbootstrappedReason": null | "RESTORED" | "MIGRATED",      // only when bootstrapped == false
    "revoked":    null | { "revocationVersion": n, "listSha256": hex64 },   // the accepted observation that set it
    "quorumLost": null | { "observedAt": <tEval>, … },           // evidence shape = owner's (R5)
    "recovery":   null | { "stagedPayload": [hex64…], … } } }     // ceremony evidence (R4)
visibleState(role) = precedence( revoked, quorumLost, expired(tEval), stale(tEval), recovery, bootstrapped )
```
Closed map over the role names; no free text. Whether root persists this or a token+history pair is an owner choice; what matters is that `revoked`/`quorumLost`/`recovery` survive independently of each other and of the clock.

**A conflict this exposes between current owners (R2, important):** v8 §5.5 "any declared restore marks **every role** `ST-UNBOOTSTRAPPED` with reason `RESTORED` … only an ordinary payload at or above the floors re-establishes trust", and S9/STP likewise set the source to `RESTORED` and the target to `MIGRATED`. In v14, `UNBOOTSTRAPPED --ordinary PRESENT--> TRUSTED` is a named transition. Composed literally, **a store migration, rollback or declared restore launders `ST-REVOKED` and `ST-QUORUM-LOST` into `TRUSTED` on the next ordinary payload** — exactly the silent heal v14 forbids. The counters are protected by the floor laws ("never lowers a floor"); nothing equivalent protects the sticky conditions. With the flag representation the fix is natural and mirrors the floors: *sticky conditions copy forward on migration and take the union (logical max) on rollback; a declared restore never clears them*; then precedence still shows `REVOKED` after the role is "unbootstrapped". That needs an explicit owner sentence in S9/STP and in the six-counter image law (the prepared image is "exactly FLOOR_KEYS" today — the sticky conditions are a second thing that must not be dropped at the same boundary).

## 2. G2 — per-role `snapshotVersion`
v1 §5.1 listed "per-role `snapshotVersion`". v2 §4.5 resolves it: "Signed TR-INDEX 2-of-3 at the release ceremony; immutable; **the machine's `TR-INDEX` role state is about this document**"; v2 §5.1 `trustEpoch` uses the single `catalogSnapshotVersion`; v2 §4.7 shows CORE/COMPONENT moved only by root and revocation conditions. So there is **one** snapshot counter — today's `indexSnapshotVersion` — and no per-role counters. **Closed**: counters stay in `TrustClockRecordV1`; per-role *state* is the durable thing, not per-role versions. Naming drift to record: v2 `catalogSnapshotVersion` ≡ v8/current `indexSnapshotVersion` ("`trustEpoch` member `indexSnapshotVersion` equal to the release catalog document's `snapshotVersion`", v8 §4).

## 3. G3 — `lastKnownRevocation`
It is more than `revocationVersion` + `revocationIssuedAt`. Three distinct things hide under the name: (i) the monotonic **version** (anti-rollback: `antiRollback`, `REVOKE-NOT-NEWER-OR-INVALID`); (ii) the **issue time** for `revocationFreshness` — both already record members; (iii) the **observations themselves**: v2 §4.5 "entries by `subjectKind` `keyId | namespace | release | catalogSnapshot`", and v14's "forget a revocation observation" prohibition. (iii) is not in the record and cannot be: it lives in the signed list. **Not fully closable from the sources**: nothing I read says whether a newer `opensip-revocation.1` list must be a superset of its predecessor. If lists are cumulative by rule, retaining the current accepted list suffices; if not, "no forget" requires retaining **every accepted list** (as roots are) and evaluating the union — and either way the per-role `revoked` condition above must be persisted when set, not recomputed from whichever list is current. *(remaining gap R3: state the cumulativeness rule or the union rule.)*

## 4. G4 — index-origin SPKI
**Closed: derived from the currently accepted root.** v2 §3.1: root document member "`indexOrigin {url, spkiSha256}`"; v1 l.311 "the pinned SPKI (§6.5) of the index origin" is listed among the root's contents, l.599 "verified against the SPKI pinned in the root document". v1 §5.1's separate "pinned index-origin SPKI" SC-TRUST member is therefore a projection of the accepted root; S9.1's current `indexOrigin` root member agrees. No separate state member — and it must not get one, or it becomes a second authority that can disagree with the root after a rotation.

## 5. G5 — the reason-less initial form
**Closed.** v14: `ST-UNBOOTSTRAPPED` = "No accepted root/index snapshot for this role", no reason member; v8 §5.5 adds the reason `RESTORED`; S9 adds `MIGRATED`. So `unbootstrappedReason: null | "RESTORED" | "MIGRATED"` — my placeholder `INITIAL` is withdrawn; absence of a reason *is* the initial form. Recovery abort's fallback to `UNBOOTSTRAPPED` also carries no reason.

## 6. Accepted roots "all versions" — explicit references, not a census
Agreed with root. The capsule's reference closure should carry an **ordered chain**, not a single hash: `"roots": [ { "version": n, "sha256": hex64 }, … ]` contiguous in `version`, last element's version == `clock.rootVersion`. S5 needs the held accepted root N to evaluate N+1..M, and recovery authority is read from the accepted root (S&L l.478); historical versions are audit/chain material. A document present under `I/trust/documents/` but not referenced is inert bytes; a referenced document missing or rehash-unequal makes the entry **unavailable**. Growth is unbounded in principle (one entry per root rotation — yearly by the 365-day floor), so it does not threaten the capsule bound, but say so.
`catalog` and `revocation` references stay single (current accepted) **unless** R3 resolves to the union rule, in which case `revocations` is a chain too.

## 7. Other member-mapping observations
- **Two different "recoveries"** — keep them in different members, as root says. *Root-recovery ceremony*: per-role `ST-RECOVERY`, `EV-RECOVER-*`, `recoveryAuthorityShape`, staged recovery-typed payload. *S4.5 clock-floor recovery*: `pendingRecoveryChallenge` + `recoveryEpochSerial` inside `TrustClockRecordV1`, a signed challenge that lowers an evaluation-time floor. They share a word and nothing else; the ceremony evidence must not be folded into `pendingRecoveryChallenge` (which a migration **drops** — model l.2293 — whereas an in-progress ceremony dropped by migration would be another silent state change: R2's rule should cover `recovery` too, or transitions must refuse while any role is in `ST-RECOVERY`).
- **`opensip-registry.1.trustMetadata`** (v2 §4.5: SC-OPS store "populated with the trust counters") is a *copy* of trust counters in an operations-class store. Under root's "no duplicate caches posing as authority" it needs an explicit standing: projection only, never read back as a floor.
- **`trustEpoch`**: v2 quadruple incl. `permissionPolicyDigest`; v8 triple. It is captured on the lifecycle side, not a capsule member; unaffected.
- **Roles**: v14 names five (`TR-CORE, TR-INDEX, TR-COMPONENT, TR-BUNDLE, TR-REPAIR` deferred). Current S9.1 has a sixth, `TR-PROFILE`, with typed absence. v14 has no machine row for it. *(remaining gap R6: does `TR-PROFILE` get its own machine instance, and do typed-absent roles have an entry at all? I would give typed-absent roles **no** entry — their absence is a property of the accepted root — but that is the owner's call.)*
- **Audit**: the ceremony requires "Record an audit event (role, from-state, to-state, payload digests, clock observation). EV-RECOVER-COMMIT only after those records exist." That is a durable ordering dependency on an audit carrier that no current layout places. *(R4)*

## 8. Remaining genuine gaps (carrier fields / protocol), none guessable from text
- **R1** pin/incorporate v14 + the v2 clauses in the current candidate; state which clauses later owners superseded (at least: clock rule → v8 §4.2 `tEval`; doctor → report-only; backup → v8 §5.5).
- **R2** sticky conditions and in-progress ceremonies across migration / rollback / declared restore (carry-forward / union / never cleared), including their relation to the "exactly FLOOR_KEYS" image.
- **R3** revocation-list cumulativeness vs retained union.
- **R4** ceremony evidence shape and the audit-record carrier and its write-before-COMMIT ordering.
- **R5** quorum-observation evidence: what is persisted when `quorumLost` is set (observed signer count, threshold, document ref).
- **R6** `TR-PROFILE` and typed-absent roles in the per-role map.
- **R7** `TRUSTED-entry ACTIVE/INACTIVE` (v14 `envelopeJoinStanding`): an activation standing that gates every TRUSTED entry. v2 §2.3 "Activation" presumably closes it; confirm it is not a durable local flag.

## 9. Limits
Two historical files read in the working tree, not from a frozen archive (hash of v14 verified; v2's hash recorded in `claude-out/io/` is my own measurement, not checked against a pin). I did not read the v14 `honestyRepairs*`, `offlineRunningPolicy` or fixture sections in full, nor the v2 schemas. Nothing executed. This note corrects my earlier assistance; it is not acceptance of any capsule root will freeze.
