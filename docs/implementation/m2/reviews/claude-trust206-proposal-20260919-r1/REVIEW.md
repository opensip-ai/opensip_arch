# Bounded assessment — root's trust-layout decision (206) and the `active.slot` bound

Reviewer: Claude. Date 2026-09-19. **Assistance only**: not a frozen review, not approval; 205 not inspected. Sources: my verified 201 reference extraction and my verified 204 product extraction (read-only). Evidence in `claude-out/` (`io/role_vocabulary.txt`, `journal_size.py`, `journal_threshold.py` and outputs — executed against the frozen reference model and canonicalizer).

## 1. Placement `I/trust/stores/S/state.v1` instead of `stores/S/trust-state.v1` — I agree, and it is better than what I proposed

My note put the capsule inside the evidence store root and then had to argue about what a store restore drags along. Root's placement removes the argument:
- v8 §5.5 "Trust floors are excluded from lifecycle backups and generation rollback" and v1's design reason ("a separate file … precisely so lifecycle restore cannot carry trust state") hold **by location**, the same reasoning that moved the journal high-water files in 201 (my 199 F-1). A capsule inside `stores/S/` would have repeated that defect in a second place.
- The forward publication rename `stores/.staging/E → stores/S` cannot carry trust state "accidentally", as root says; the six-counter copy/max becomes an explicit fenced write of the target's entry. That matches STP's wording — the image is *applied*, never inherited by directory motion.
- State stays logically per instance because the key is S, and S is only ever an admitted marker value + full binding (PSL).

Consequences root should write down, each following from the separation:
1. **Two creations, no atomicity between them.** A store now has a root (marker) in one domain and a trust entry in another. Order by existing law: the trust entry must exist with `sourceFence: null` **before the store's first publication** (corr.188: "A new store initializes it to observed-none as part of its admitted creation"). For a forward target: create `trust/stores/S/state.v1` (floors copied, roles MIGRATED, anchor/challenge null) while the tree is still at `stores/.staging/E`; S is known then because the marker is written in staging (PSL). Crash leaves either no entry (target unpublished → ABORT rows still lawful; orphan entry cleanup = Q below) or an entry for a never-published S.
2. **A published store with no admissible trust entry is *unavailable*, never observed-none and never "fresh floors"** — it is now a reachable state (out-of-band deletion of `trust/stores/S`, or a restored `stores/` tree), and it must fail closed exactly like corr.188's "older carrier without an admitted attribution representation".
3. **Orphan entries** (`trust/stores/S` for an S that was never published or was reclaimed) are trust files: PSL's "this layout grants no deletion of retained trust files" should be extended to them; store GC reclaims `stores/S`, not its trust entry, unless a trust-owned rule says so. They are harmless: nothing addresses them without an admitted S.
4. **Detection bound, stated as 201 does:** restoring `stores/` alone cannot roll trust back; restoring `I/trust/` alone rolls floors back *under* a newer store — which the existing rule catches only where a comparison exists ("a trust store restored below any document still on disk", v8 §5.5). Coordinated/whole-install rollback stays outside the bound.
5. `I/trust/` now holds two collections (`journal-floors/N/…`, `stores/S/…`) plus documents: give the directory a PSL table row with the provisioning discipline (my 201 N-2).

## 2. Is there a better already-owned representation? Partly — name it, don't invent beside it

- **The record exists and is closed:** `TrustClockRecordV1`, eleven required members, all-or-nothing admission, calendar validation, and — S&L l.2484–2492 — "**A future private AdmittedTrustRecord must own this admitted state and expose only immutable projections.**" The capsule's clock member should be *the physical form of that already-named owner*, verbatim eleven members, not a parallel structure. The clock kernel consumes six of them (`evalHighWater, lastAccepted, anchor, revocationIssuedAt, catalogExpiresAt, rootExpiresAt`); the six `FLOOR_KEYS` of the transition law are a different six (`rootVersion, indexSnapshotVersion, revocationVersion, evalHighWater, lastAccepted, recoveryEpochSerial`). Both subsets live in the one record; persist the record once.
- **The product has nothing to reuse for persistence**: `security/src/trust_time.rs` assesses and *proposes* writes (`floor_write`, `anchor_write`, `last_write`) and says it does not "persist a floor"; `trust.rs` holds metadata/signature/root codecs. 202's bounded reader is the read mechanism (with my 202 W-1 about the descriptor observation).
- **`trust.sqlite`** is named by v1 §5.1 and repeated by PSL's table row, implemented nowhere. Root's "explicit prospective supersession, not a bridge claim" is the right treatment and mirrors S2.1's and PSL's "no product writer has shipped" statements. It also dissolves the existing conflict I flagged (a WAL trust database read by fence-only `trust doctor` under a "write nothing" contract). **PSL's row must be changed in the same owner revision**, otherwise two current texts name different authoritative carriers.

## 3. The role vocabulary that actually exists — and what it implies should be persisted

Collected from current owners (`io/role_vocabulary.txt`):

| Token | Where defined | Nature |
|---|---|---|
| roles `TR-CORE, TR-INDEX, TR-COMPONENT, TR-BUNDLE, TR-PROFILE, TR-REPAIR` | root document `roles`; S9.1 | **document content**. Typed absence (`TR-REPAIR`/`TR-PROFILE`: keys `[]`, threshold 0, `typed-absence-DR-110`; "Missing/typed-absent roles never…", S&L l.1289, l.1327) is a property of the **accepted root**, not of local state |
| `ST-EXPIRED` | v1 §4.2: root expiry → every role; index expiry → `TR-INDEX` | **recomputed at `tEval`** from `rootExpiresAt`/`catalogExpiresAt` (v8 §4.2: expired iff `tEval >= expiresAt`). The reference kernel returns these as booleans (`rootExpired`, `catalogExpired`) on every call |
| `ST-STALE-REVOCATION` | v1 §4.2 | **recomputed** from `revocationIssuedAt` (`revocationStale`) |
| `ST-REVOKED`, `ST-QUORUM-LOST` | v1 §4.1–4.3 | **recomputable** from the accepted root + accepted revocation list (keys revoked, signers below threshold) |
| `ST-TRUSTED` | v1 §4.7 "every role `ST-TRUSTED`; counters set" after `EV-PRESENT-PAYLOAD` | **durable fact**: PRESENT happened over the currently accepted documents |
| `ST-UNBOOTSTRAPPED` + reason `RESTORED` \| `MIGRATED` (and the initial, reason-less form) | v8 §5.5; S&L l.1700; model l.2294/2317 | **durable fact**: PRESENT has *not* happened since the named resetting event |

Two things follow.
**(a) The full DR-112 state machine is not in this tree.** v8 §4 says "As v2 §4"; v2 is absent; v1 §4 carries numbers and worked transitions, not the closed state/event table. I can list the tokens that appear, not certify the set is complete. *Gap G1.*
**(b) What is genuinely durable is small.** Everything except "has PRESENT established standing since the last reset, and if not, why" is a function of (accepted documents, `TrustClockRecordV1`, `tEval`). Persisting `ST-EXPIRED`/`ST-STALE-*`/`ST-REVOKED` would be precisely the "duplicate cache posing as authority" root wants to avoid — and a stale one the moment the clock moves. So:

```
standing = { "kind": "established" }
         | { "kind": "unbootstrapped", "reason": "INITIAL" | "RESTORED" | "MIGRATED" }
```
one value for the store, not a per-role map, **if** the missing machine has no durable per-role event. The one candidate I can see for durable per-role state is v1's "per-role `snapshotVersion`" member (SC-TRUST list) — today's record has the single `indexSnapshotVersion`. If v2's machine really keeps per-role counters or a per-role established flag, the shape must be a closed map over the six role names; root needs the v2 text to decide. *Gap G2.* Either way: closed enum tokens, never the model's sentence (`'ST-UNBOOTSTRAPPED:MIGRATED (re-established by the PRESENT event …)'`). `INITIAL` is my placeholder for the reason-less first-install form — it needs the owner's spelling.

## 4. Accepted documents and the reference closure

v1 §5.1 SC-TRUST members, checked one by one against root's split:

| Member (v1 list) | Root's split | Assessment |
|---|---|---|
| accepted root documents (**all versions**) | immutable files under `I/trust` | required by S5 (chain N+1..M evaluated link by link against the *held* accepted root; recovery authority read from the accepted root, S&L l.478). Content-addressed, exclusive-create, never replaced ⇒ global storage is not a second authority: bytes are self-verifying and carry no standing |
| current index snapshot bytes; revocation list | same | same; "current" is a *reference*, which is per store (below) |
| `rootVersion`, `revocationVersion`, snapshot version, `lastAcceptedIssuedAt` | in the record | already `TrustClockRecordV1` members (`indexSnapshotVersion`, `lastAccepted`) |
| per-role state | capsule `standing` | §3 |
| `lastKnownRevocation` | — | **not in `TrustClockRecordV1`**; the record has `revocationVersion` + `revocationIssuedAt`. Either subsumed by those two or silently dropped since v1. *Gap G3* — root asked not to omit members silently; this one needs an explicit disposition |
| the pinned index-origin SPKI | — | today `indexOrigin` is a **root document** member (S9.1), so it is derivable from the accepted root; v1's separate pin may be historical. *Gap G4*: confirm nothing else pins it |
| grant-journal high-water witnesses | `trust/journal-floors/N/G.floor` | settled in 201 |

**Reference closure (new member, needed):** counters alone do not say *which bytes* were accepted. Per store: `accepted = { "root": <sha256 of the accepted root document bytes>, "catalog": <sha256|null>, "revocation": <sha256|null> }`, raw SHA-256 of exact file bytes (evidence locator style, like `receiptBytesSha256` — no new identity domain). Laws: a referenced document must be present and rehash equal, else the entry is **unavailable**; the referenced root's version must equal `clock.rootVersion` (and likewise catalog/revocation) else **contradictory ⇒ unavailable**, never "take the larger". Older root versions are retained as chain material without being referenced. This is what makes "no second global authoritative copy" true: the global directory holds bytes; only the per-store entry says which bytes count. Persisted expiry/issue timestamps in the record are then redundant with the referenced documents but are *required* members of the existing closed record — keep them and treat disagreement with the referenced document as unavailable, not as a tie to break.

## 5. Concrete minimal representation

```
I/trust/
  documents/<sha256>.json                 immutable accepted signed documents; exclusive create; never replaced/deleted by store ops
  stores/S/state.v1                       ONE replacement-published file = the AdmittedTrustRecord's physical form
  journal-floors/N/G.floor                (201, unchanged)

StoreTrustStateV1 (product-canonical, raw == canonical(decoded), bounded, read via the 202 mechanism):
{ "capsuleSchema": 1,
  "storeInstanceId": S,                   // == directory name == admitted marker; mismatch ⇒ unavailable
  "clock":    { …exactly the 11 TrustClockRecordV1 members… },
  "accepted": { "root": hex64, "catalog": hex64|null, "revocation": hex64|null },
  "standing": <§3>,
  "sourceFence": null | { "executionId": E, "intentDigest": D } }
```
Writers (all under the installation fence, which already owns floor writes): `publish_initial` (creation, `sourceFence: null`), `republish(prev, f)` where `f` can reach `clock`/`accepted`/`standing` but **not** `sourceFence` (floor write-ahead, PRESENT, image application), and `fence_source(prev, E, D)` — the only function that sets `sourceFence`, and it sets `standing → unbootstrapped/RESTORED` in the same revision. One rename = STP's "one recoverable commit boundary"; the observation is durable while the journal is still PREPARED (root's R3).
Note the **write frequency**: v8 §4.2 "A decision evaluation writes `evalHighWater = tEval` durably first (write-ahead)" — every decision evaluation replaces this file. Small file, one fsync pair; fine, but it means the `republish` invariant (sourceFence byte-identical across every republish) is exercised constantly and deserves a property test, not an example.
Report-only reads (`trust doctor`) are plain bounded reads: physically write-free, as root intends.

## 6. `active.slot` and the 4 MiB product bound — measured, and there is an existing incompatibility

Run against the frozen model and `foundation/canonical.py` (`io/journal_threshold.txt`), store-changing intent (all namespaces in both `registry` and `leaseSet`), UUIDv4 locators (PSL grammar), worst state spelling `PREPARING`:

| Object | Largest namespace count that canonicalizes |
|---|---|
| bare 20-member journal (the **existing** `journalRef` identity path) | **53,763** |
| `ActiveTransitionSlotV1` wrapper (my 203 sketch) | **53,760** |
| schema `NamespaceList.maxItems` | 65,536 |

≈78 bytes per namespace (it appears twice). Above the threshold `canonical()` raises `AdmissionError('BYTE_LIMIT')`. So:
1. **The incompatibility already exists without any wrapper**: a registry of 53,764–65,536 namespaces is schema-legal and *cannot have a `journalRef`*. Root's instinct (do not move to 8 MiB) is right — the bound belongs to the product parser, and the identity path hits it first.
2. **The schema is looser still**: `NamespaceList` items allow `maxLength` 4096; 65,536 × 4,096-char locators is ~512 MiB in the journal. PSL narrows N to 36 bytes, but the public journal schema does not know that. The preflight must be computed on **actual bytes**, not on a count.
3. **Root's two-sided rule is the right shape**, with these precisions:
   - *Transition admission*: build the actual journal from the frozen registry, take the longest state spelling (`PREPARING`, 9 bytes; wrapper sizes differ only by the state string, so "all six revisions" = one computation + a constant), add the wrapper overhead, compare with the bound **before jLEASED or any effect**. Refuse as a resource refusal with existing vocabulary.
   - *Registration*: refuse the namespace that would make the **worst legal** transition journal (all namespaces affected — a schema-changing or store-reselecting operation) exceed the bound. Otherwise an install can register itself into a state where `core update` with a schema change can never be journaled — and S9's ordered release *requires* that path. With UUID locators that is a cap of **53,760 namespaces**, not 65,536. Say the number is derived from the bound and the wrapper, and re-derive it if either changes.
   - The check must use the *wrapper* size (53,760), not the bare journal (53,763): the last three registrations would otherwise be admitted and then strand.
4. No new wire code: both are preconditions on the host's own state; existing resource/precondition refusals apply. No change to the 20 members.

Root's other choices — no `retired/E.slot` copies (retained invocation/history is independent), lineage nodes as exclusive-create files keyed by the full triple with guarded reconciliation, foreign/unattributable temp directories untouched — are consistent with my 203 note and with S&L l.1582 / the lineage owner's "absent → write, byte-identical → done, different → quarantine". Dropping `retired/` also removes the copy-then-unlink window I had to describe.

## 7. Gaps to record explicitly
- **G1** the closed DR-112 state/event machine is referenced ("As v2 §4") but not present in the current tree; the token list in §3 is what exists here.
- **G2** whether any per-role *durable* state exists (v1's "per-role `snapshotVersion`"); decides scalar vs map for `standing`.
- **G3** `lastKnownRevocation` disposition.
- **G4** index-origin pin: root-document member only, or also local state.
- **G5** the initial (reason-less) unbootstrapped spelling.
- **G6** `sourceFence` after an authorized *trust* restore: root says such a restore "follows its own RESTORED/floors laws". An attribution restored from a backup describes a fence act of an older timeline; I would make it **unavailable** until the next source-fencing, but it is an owner call.
- **G7** PSL table row `trust.sqlite` must be superseded in the same revision that introduces `trust/stores/S/state.v1`; and `I/trust/` needs its own row and provisioning rule.
- **G8** orphan `trust/stores/S` entries: retention/cleanup owner.

## 8. Limits
Reading and two executed measurements against the frozen reference; no product build; nothing here is implemented or qualified. The v2 completion document is not in my tree, so §3's completeness is bounded by G1. This is assistance for root to reconcile, author and freeze; I will review the frozen owner independently, and this note is not acceptance of it.
