# Independent source-owner review — current recovery standing 321

**Standing:** bounded review of frozen `scoped-current-proposal-321`. Root **option A** for **CURRENT retained-phase S4.5 only**: physical-current / projection / census standing, not retrospective empty-event effect proof. Not a native constructor, wire change, complete traversal, 318 TCB, 320 re-approval, or product installation. Installed product remains `fa72e50`. 318 is accepted only as the bounded declared-core projection already reviewed; it is not original-core authentication standing here.

Python 3.12.13 `-I -B`. No native tests. No product/frozen/history edits. No commit/push.

Pins **before** extract: **2637220 B, 620 members, SHA256 `dd80c72a0c2b0f88259de07b8efa58c13b1f7fa1ff62a474f60fe5897a73cdb1`**. Extract rehashed **620/620**. Nested 320 pin `44cf8592…b1b8f2` (612 / 2625124). Packet `review320/REVIEW.md` byte-identical to live 320 REVIEW (`897115e6…f713`). Field table / locator citations copied. 318 REVIEW remains `7748038b…77be`. 317 REVIEW `0740164f…2943`. OWNER.md SHA256 `25fd1360…6b05`.

---

## What 321 chooses

320 exhausted owned locators and refused to pick A vs B. 321 picks **A for CURRENT S4.5 only**. Exact grant: this fenced native `state.v1` file is the selected current capsule; D(current) matches C; live successor census of **hash(C)** is none/behind/fork/unavailable as 222 requires. It does **not** mean original empty-event clock/role/head effects were replayed. 279/306/`bind_events` stay unchanged and still need a real before image when proving that effect. No guessed `records/<previous SHA>`, no current roles as that before, no unavailable→skip.

Option B (durable before-image locator/retention) is left for a future owner that actually requires universally replayable empty-event effects from current C alone. This packet does not promise that audit capability.

---

## Challenge: does A contradict 222 / 215 / 227?

**No, if and only if** the implementation keeps the operation-specific split those sources already name. It **would** contradict them if current standing were treated as 279 effect proof, as 272 full DFS, or as a generic trust grant from a partial projection.

### 222 current file is sole per-store authority

Publication/crash law: hold fence/custody; read the **exact current capsule** and the successor check; a descriptor never proves its own acceptance; crash recovery observes the one surviving complete capsule, not the highest event or an orphan D. “Admit prerequisites for the exact requested operation, never issue a generic complete trust grant from a partially admitted projection.” Missing descriptor/event/identity evidence needed to determine **current outcome** is unavailable.

That supports selecting C as authority without reconstructing C’s predecessor. Reconstructing C from D(current).`afterProjection` + `PublicationRef` does **not** need the replaced file. `previous` / `nativeBefore` remain scalar pins. 320’s finding that those pins are not a full predecessor NodeRef is why A **drops the effect predicate**, not why it may skip census or D/C join.

### 215: S4.5 is not dependent on old T; empty-event effect is not in that list

215 r14 clock consumer: “Dependent means an operation publishing role/head trust admission or carrying L as authenticated time through continuity. Read-only diagnostics, ABORT/private batch termination and **S4.5 challenge/import in phase retained are NOT dependent on the old T.** Those operations still admit their actual **record/authority/custody** prerequisites and never claim a complete trust grant. S4.5 uses the admitted eleven-field R, exact pending challenge and recovery authority and publishes a new T on success; old T absence does not erase/lower L or bypass its epoch guards.”

222 cites that 215r6 exception in the same paragraph as “trust entry and continuity may not.”

So: missing **old T target** is an allowed S4.5 exception. Missing **predecessor capsule bytes** is a different predicate. 215 does **not** say empty-event unchanged-clock may be re-proven without before. 227 empty-event still “needs exact before image.” 321 is consistent only because it **does not add** that predicate to current standing.

### 227: old T vs beforeImage vs empty-event

`TIME-INPUT-JOINS.md`: S4.5 keeps exact `beforeImage` (the **current** capsule), `beforeRecord` equality to `beforeImage.clock.record`, acceptedAuthority **in that image**. “Old T need not be traversed solely because it appears in beforeImage.” Scope-sensitive admission: a generic walker must not require unavailable old T **here** or skip it on ordinary entry.

S4.5’s `beforeImage` is **current C**, which option A owns as the native file. It is **not** C’s predecessor. Empty-event 227 guards compare C to that predecessor; they are publisher/effect law. OWNER keeps publishers proving effects from the actual owned before before installing an empty-event update.

`PENDING-JOINS.md` item 1 already distinguishes cheap structural capsule/descriptor/successor joins from full authority admission. 321 is that distinction applied to CURRENT S4.5.

### 279 / 306 / 265 — not waived

Empty `D.events` plus 279/306/`bind_events` **still require** caller before bytes. 321 forbids invoking them for this capability and forbids using `C.roles` / `C.eventHead` as that before. That is the load-bearing anti-smuggling rule. If a later native helper calls them anyway, A becomes the unattainable path 320 warned about.

---

## Where A can still smuggle missing T or unavailable before

These are **unresolved constructor obligations**, not silent success.

### 1. Census “complete references” is still unsplit in 222

Successor check: admit `by-predecessor/H` with **H = hash(current C)**; for every canonical child, admit complete descriptor and reconstructed child (same store, revision+1); then that child’s own successor bucket. “Require complete private shape, **references** and projection/digest/adjacency joins.” Missing required dependencies → **unavailable**, not clean absence. Canonical names that cannot admit → unavailable.

Children of current reconstruct with **current C** as `previousCapsule`. That before **is** available. 279 on a **child** with `before = C` compares `timeEvidence` **locators**; it does not load T bytes.

If census child-admission instead follows `timeEvidence` / `clock.by` / `evaluation` **targets**, then a crash-orphan empty-event child that carries the same dangling T locator makes census **unavailable** under missing old T. A would then fail the motivating lawful empty-event current (or any current whose successor bucket is not empty of such Ds). OWNER says the CURRENT result must be independent of T **presence**. That scoping **must apply to child admission during census**, not only to C itself. 222 does not enumerate that field split. 272 full DFS is unsuitable (OWNER says so; 320 already did).

**Unresolved:** exact census child field/predicate list: locator-shape + projection/adjacency + optional locator-only T vs load of evaluation/T bytes. Until that list exists, do not claim census is T-independent.

### 2. Nonempty current `D.events` vs `bind_events`

EventRefs are full locators (store/sequence/sha256/bytes). Store/operation/sequence/`previous` chain and “final ref == `C.eventHead`” can be checked **without** the predecessor capsule.

`bind_events` cannot: `before_roles` / `before_head` must come from the owned logical **predecessor**, and the function cannot choose that base. Using **current** roles as before for **current** D is exactly the forgery OWNER forbids. For nonempty current events, that helper stays **unresolved**, not waived. S4.5 standing does not need role-effect replay (222: never regenerate proof from a role token; 317: do not follow `clock.by` → evaluation). An implementation that “completes” current standing by calling `bind_events` has reintroduced the 320 gap.

### 3. `D.operation`

Load typed `OperationInput` for declared action/identity only. Empty-event D’s operation is audit evidence for that revision, not D1’s clock-write evaluation. Walking `input.ref` into the missing S4 evaluation would reintroduce old T. Structural identity must stop at the operation node’s closed action/ref shape.

### 4. Physical premise is not supplied here

OWNER is explicit: fence, custody, marker, selected store, parent identity remain a **native qualification obligation**. Without that premise, signatures, recorded `priorRevocationHistory`, and a well-formed graph **cannot** manufacture current standing (215/227: schema-valid image / boolean never constructs native authority). That is not a defect in choosing A; it is why A is not yet a constructor.

### 5. `priorRevocationHistory` — honest non-claim, not resolved equality

Load the locator from the **admission record** if non-null; time-free ancestry of `admittingRoot`; current complete history separately filters new RECOVERY keys. **Do not** claim equality to omitted `context.time.beforeImage.history`. 320 left that unresolved; 321 names the non-claim. The association is a retained declaration pinned by independently current accepted state. That is enough for this scoped declared context **only if** the physical current premise holds. It is not replayed original-context time.

Time-free CoreAnchor / embedded-chain authentication remains 229/312 work. **318’s bounded inventory projection is not that TCB.**

### 6. Historical constructor not weakened

222 restore still admits N’s **complete** closure including **original time proof**. 321 does not give historical images the current-file premise or a weaker empty-event rule. Exact non-time predicate closure for historical epoch replay remains **open**, as OWNER says.

---

## Is native current standing enough for this scoped context?

Under the existing threat model, **yes for this declared S4.5-only capability**, provided:

- qualified fence/custody actually selects this C;
- D(current) reconstructs C;
- census of hash(C) is scoped so it cannot fail solely because old T bytes are absent;
- epoch still checks eleven-field R, pending challenge, recovery quorum, serial/window/range, L; challenge and ABORT stay on their own 215 guards;
- ordinary entry, BEGIN/COMMIT, continuity, and full restore still refuse missing T and missing required empty-effect befores.

**No** as a complete trust grant, publication permit, or substitute for 222 write barriers / 302 final age. A `CurrentRecoveryImage` value is not a durable-write permit (OWNER). Payload root, self-signed graph, orphan D, or numeric root version still fail.

---

## Remaining (do not count closed)

Exact event/census field lists and owed adversarial tests (OWNER list plus: census with T-dangling orphan child; nonempty current events without `bind_events`; `bind_events` fed current roles). Native fence/custody. Historical non-time closure. 317 discovery is still not a total algorithm and is **out of this standing constructor**. 318 projection, 320 investigation, and this disposition are not M2–M6 or product installation.

---

## Verdicts

- [x] **321 option A as CURRENT S4.5 disposition:** consistent with 222 current-file authority, 215 “S4.5 not dependent on old T,” and 227 scope-sensitive old-T exception; empty-event **effect** proof correctly left with 279/306; 320 locators not contradicted.
- [x] **Unresolved, not waived:** 222 census “complete references” field split (T-load on children would make A T-dependent); nonempty current `bind_events`/before_roles; physical premise; `priorRevHistory` vs omitted before-image history equality (named non-claim); historical constructor.
- [ ] **Not** a complete constructor, native implementation, wire change, 318 TCB, 320 standing approval beyond this scoped A, or product installation.
