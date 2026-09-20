# Bounded source assistance — event hash and exact role-image joins (draft owner 226)

Reviewer: Claude. Date 2026-09-19. **Incomplete-source assistance; not frozen-candidate approval; no candidate/repo/product edit, commit or push.** Work confined to this directory. **[E]** inherited (pinned 215/222/v14 text) · **[P]** my proposed correction.

## 1. Sources and hashes (`claude-out/io/source-hashes.txt`; `AUDIT-JOINS.md` copied as read)
| File | SHA-256 | Relation to what I have verified |
|---|---|---|
| `AUDIT-JOINS.md` (7,482 B) | `5cd836f00d366f89fa550f42905586f5184ca13291aed9de17495ac4c82445a6` | the subject |
| `logical215.md` | `d8165f14…f9fa` | = 215 draft "revision 14", which differs from my verified r13 only in its heading |
| `persistence222.md` | `f8ddaecc…092e` | = my verified 222 r6 `PERSISTENCE.md` |
| `machine14.json` | `039a5702…6715` | = the v14 contract I have used throughout |
| `authorization215.json` | `527f8552…412a` | 215 authorization schema (six role tokens) |
| `source-inputs.json` | `a68656c8…9ec5` | pins agree with the four hashes above |
No schema fragment or model was present when I read the directory; only `AUDIT-JOINS.md` and the pinned copies are considered. Nothing executed.

## 2. Answer in brief
**Acyclic: yes. Implementable: yes. Audit evidence weakened: no — with one property that should be stated because the whole argument rests on it.** The remaining problems are three missing owners at the edges (private reset closing a ceremony, continuity logical-before and cross-store chain link, the BeginBatch instant) and two exactness errors.

### 2.1 Why it is acyclic
`RoleRecord` carries `EventRef`s in `accepted.by`, `conditionEvidence.{revokedBy,quorumLostBy}`, `reset.by` and `ceremony.{batch,begin}` **[E, 222]**. An AFTER record generally names *this* event, so it cannot be inside the event; a BEFORE record names only earlier events. With the amendment the dependency order is: signed objects / admission nodes → event₁ … eventₖ (each holding BEFORE, from/to, inputs, `previous`) → `BeginBatch` (names the BEGIN events and the six-role image) → any later event of the same revision whose BEFORE already contains `ceremony.batch` → descriptor (entries with full before/after; `afterProjection`) → capsule. No edge points backwards; no record hashes itself; an event never names the descriptor, the capsule or a batch that names it.

### 2.2 Why audit evidence is not weakened — the property to state **[P]**
v14's audit record needs `{role, from, to, event, outcome, refusalReason?, payloadDigests, clockObservation}` **[E]**; the event keeps all of it plus the literal BEFORE. The full AFTER is *not lost* even though old descriptors are not reachable backwards (a descriptor names `previousCapsule` by hash and lives in a predecessor-keyed bucket; nothing points to the previous **descriptor**): because AUDIT-JOINS forbids any role change without an event, **AFTER(e) for role r is exactly BEFORE(next event on r), or the current capsule's record when e is the last** — and both of those are committed by hashes on the authoritative chain (next event's hash via `previous`; capsule). So the complete per-role history is reconstructible from the capsule and the event chain alone. Say this explicitly, and make "no role record changes without a role-mutating event in the same descriptor" a named invariant (step 6 implies it for no-event operations only).

## 3. Findings

### J-1 (Medium) — a private reset that closes a ceremony: which event mutates the role?
AUDIT: "role-event, standing-reset **and** per-role ceremony-termination require one non-null roleChange", and step 5 gives each kind its own law (reset: "set reset.by to THIS event"; termination: none stated). **[E, 215 C.4 / 222 r5]** a RESTORED/MIGRATED/ROOT_CHANGED reset (or restore-recovery) that closes a batch takes an established `RECOVERY` member to `REVOKED` (BEGIN source REVOKED; "takes no reset projection") or to `UNBOOTSTRAPPED` with a reset projection, and a never-established one to `UNBOOTSTRAPPED` without one. For the established non-revoked case two role-mutating kinds apply to one role in one revision, and the text does not say whether that is one event or two, nor what the record between them is.
**[P] bounded rule:** exactly two events, in this order, each single-purpose — (1) `ceremony-termination`: `RECOVERY → target state` decided only by the BEGIN-source/active-evidence rule, clears `ceremony`, touches nothing else; (2) `standing-reset` (only where a reset projection is due): state token unchanged, sets `reset.{cause,by}` to itself, BEFORE = the record produced by (1). The intermediate "established `UNBOOTSTRAPPED`, `reset` unchanged" record exists only inside that descriptor's ordered entries — the same shape r10 already accepted for a reset from `UNBOOTSTRAPPED`. State the termination kind's owner law in step 5 (target state from exact BEGIN preimage + active evidence; `ceremony` → null; no `accepted`/`condition`/`reset` rewrite).

### J-2 (Medium) — continuity: logical-before of the target and the cross-store chain link are unowned
Step 1: a transition "must use the operation-owned target logical-before image, not silently substitute source roles"; step 2: "previous EventRef is the preceding event globally … Sequence is previous.sequence+1 **in the same event store**, starting at 1".
- **Forward (new) target.** If its logical-before is the six *initial* records, every carried established role shows `before.accepted = null → after.accepted = <source's>`, which violates step 5's "a standing-reset must preserve accepted", and a carried `REVOKED` needs a mutation that no permitted kind can lawfully perform (`continuity` must have null roleChange). If instead it is the source's pre-fence records, replay and the preserve-laws work unchanged. The draft forbids *silent* substitution but never says what the image **is**.
- **Ancestor target.** Its own old records are the natural BEFORE; newly learned revocations arrive as `EV-REVOKE` role-events (**[E]** 215 C.1: "The same OLD-subject-before-reset law applies when ancestor continuity merges revocations") and the rest as resets — coherent, but unstated here.
- **Chain link.** In a new store the first event has no same-store predecessor, so `previous` must be the explicit initial null — which disconnects the target's audit chain from the source's unless something else binds it.
**[P]:** (i) forward target logical-before := the admitted **source BEFORE-fence** role records (same installation, same logical roles), named in the `continuity` event; ancestor target := its own admitted BEFORE capsule roles; (ii) `previous` stays strictly same-store (null for a store's first event), and the `continuity` event carries a distinct closed member `sourceEventHead: EventRef` (cross-store; 222 already keeps source stores retained) so the two chains are joined by an explicit edge rather than by a sequence that pretends to continue; (iii) `BEFORE` records may reference events of another store of the same installation — say so, since every `by`/`revokedBy` carried forward does.

### J-3 (Low–Medium) — `BeginBatch.beforeRoles`: which instant, and its join to the BEGIN events
The batch holds "the complete six-role BEFORE image"; each BEGIN event also holds its role's BEFORE. If a recovery PRESENT accompanies BEGIN (v14 permits; 222 commands), staging events precede the BEGIN events in the same revision, so "BEFORE" is ambiguous between the revision's logical-before and the vector immediately before the first BEGIN. **[P]:** `beforeRoles` = the six-role vector obtained by replaying the descriptor entries up to, not including, the first BEGIN entry; require `beforeRoles[r] ==` the BEGIN event's BEFORE for every selected r. This is also the preimage 215 r12/r13 key the revoked-source protection on, so it must be one unambiguous value.

### J-4 (Low–Medium) — publication order sentence vs mid-sequence dependencies
Step 2: "Publish exact dependencies, then events in order." Step 3 publishes `BeginBatch` *after* the BEGIN events, and 215 C.2 derives availability observations "on publication of a … begun ceremony binding … in the outcome revision": those later events' BEFORE already contains `ceremony.batch`, so they depend on a record that depends on earlier events. 222 r3 already says topological order with "NO universal documents-before-events order" **[E]**; align step 2 with it (event *sequence* is the chain order; *publication* is topological), and drop "No subsequent operation is interleaved" in favour of "no other **operation's** event" — same-operation events after the batch are lawful.

### J-5 (Low) — exactness
- "Descriptor's **nine** top-level members remain unchanged": pinned 222 l.59 lists **eight** (`publicationSchema, store, revision, previousCapsule, nativeBefore, operation, events, afterProjection`).
- "Refused role events have before==after": accepted *stay* events (v14 fallbacks for `EV-CLOCK`/`EV-QUORUM-OBSERVE`, the r12 protected stay) also have before==after; the entry must not be read as "refused" from equality — outcome comes from the event.
- The abort annotation is right in principle (**[E]** v14: ceremonyTermination is "Joined to the accepted abort event … not a refusalReason"): the ABORT `role-event` carries the single mutation `RECOVERY → toFunction result`, the annotation carries null. Name the two `ceremony-termination` variants distinctly in the union (mutating private termination vs abort annotation) so a decoder cannot accept a mutating one after an ABORT.
- restore-recovery: "Descriptor.events has no duplicates or gaps" is per descriptor; add that the chain walked from `eventHead` must pass through proven N's `eventHead`, and that same-sequence events of the lost branch (different hash, same store) are never on it.

## 4. Checked, no finding
Multiple changes to one role in a revision replay correctly (event₂'s BEFORE is event₁'s AFTER and may name event₁); refused-import T0 audits are before==after; a prior reset's `by` survives in the successor's BEFORE and in `roleChange.before` (consistent with 215 r10); structural replay is correctly declared insufficient without re-running each owner law; orphan events/batches/descriptors prove nothing; the size argument holds (two bounded records per entry, a handful of entries, ≤ 4 MiB with preflight-or-refuse).

## 5. Limits
Reading only; nothing executed; no schema fragment or model existed in the draft directory when read, so shapes are as described in prose. J-2's forward-target choice is a proposal with an alternative (a dedicated role-carry event kind); I prefer source-BEFORE as logical-before because it adds no kind and keeps every preserve-law checkable. Nothing here approves 215, 222 or 226.
