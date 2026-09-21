# Independent source follow-through — time-admission proposal 317

**Standing:** bounded source review of frozen `time-admission-proposal-317`. Unselected successor of 315 that names the mixed equal-L policy, required old-T **locator** shape, recursive 222 no-GC retention, and whole-prerequisite-path scoping. Not a native consumer, wire change, tests, total discovery algorithm, 316 re-approval, or product installation. Installed product remains `fa72e50`. Native 316 remains exact 312 literal bindings. Native 318 (if any) is original 229 core-inventory projection, not this recovery consumer. 315 REVIEW and 316 REVIEW were not edited.

Python 3.12.13 `-I -B`. No native tests. No product/frozen edits.

Pins **before** extract: **433096 B, 210 members, SHA256 `8ccd47a0650c789247f1a38d704bf7c1953958291bc3ccf64427799ce3fb7292`**. Extract rehashed **210/210**. Parent 315 live tar SHA match `decb680d…25d8` (203 / 428756). Packet `OWNER315.md` byte-identical to 315 OWNER (`908877c4…1b0e`). `review315/REVIEW.md` byte-identical to live 315 REVIEW (`87e3cd2d…e0e8`). `review315/ROOT-DISPOSITION.md` byte-identical to `grok315-DISPOSITION.md` (`2d9812c5…4e82`). 316 REVIEW remains `1ef324da…d059`.

---

## What 317 changes relative to 315

315 REVIEW left three owner gaps: (1) ancestor equal-L mixed ordinary vs epoch T; (2) selected-L CapsuleImage reachability after `sourceFence` supersession; (3) fail-closed event-chain gaps; plus the circular-premise test that “current capsule standing” must not DFS `timeEvidence`. Root disposition accepted designated-base (target) even mixed, no epoch-priority, field-present P2 `timeEvidence`, recursive no-GC retention. 317 writes those into OWNER.

No schema/native/code in this packet.

---

## 1. Equal-L designated-base — does it close 315 Q1?

**Rule:** after **both** sides admit L and proof, copy the proof of strictly greater L. On equal L, keep the **full NodeRef** of the designated base: forward → source BEFORE; ancestor → **target** BEFORE; restore → proven **N**. Explicitly: ancestor keeps **target ordinary T** even when source holds S4.5 epoch T at the same L. If the base itself has epoch T, keep that epoch T. Two distinct epoch proofs at equal L use the **same base rule**, not `epochSerial` or hash order. Nonselected proof **remains** in that branch’s retained audit/proof dependencies. Selecting another already-admitted equal-L proof is **not** deleting or denying the recovery. Intra-store S4.5 new-T and ordinary Keep are unchanged. Restore still keeps N if n holds a distinct epoch. Both closures still required; missing competitor is unavailable.

**This is 315’s explicit tie policy**, not inherited 201/222 scalar copy/max (those name `max(L)`, not proof identity). 315 REVIEW already treated epoch-priority as an optional policy, not a security entailment. Disposition rejected implicit epoch-priority. 317 matches that.

**Security premise:** the surviving store’s floor T is the proof **already admitted on the designated base**. The nonselected epoch stays on the other image’s retained chain (continuity `sourceBeforeImage` / source capsule), not as the target’s `clock.timeEvidence`. That is coherent **if** §retention actually keeps that image live. It does not lower L, merge NodeRefs, or treat an orphan as a win.

Forward source and restore-N rules are unchanged from 315. **Hold.**

**Not closed:** a consumer that **drops** the nonselected branch’s images while carrying only the target NodeRef would convert “retain as history” into deletion. 317 forbids that in prose; it is a **producer/retention invariant**, not yet a test. Adversarial cases in OWNER (both ancestor directions, two epochs, restore n-vs-N epoch) remain **owed before a consumer**.

**Verdict Q1:** the named mixed ordinary/epoch case is closed as **explicit designated-base policy** without lost security premise **and without a delete claim**, provided recursive retention of the nonselected proof holds. Do not describe this as “already copy/max.”

---

## 2. Required locators vs out-of-scope **targets**

P2 `clock.timeEvidence` remains a **required** full NodeRef (hash **and** length). Missing field, null, malformed hash/length, or other closed-record defect **refuses**. Only the **referenced old-T bytes** are out of S4.5 recovery scope. Root/history `context.time` locators are likewise **shape-checked**; their **targets** are not loaded and must not change the result if present.

This is the 315 correction (field-present / target out of scope), not 314’s withdrawn optional-integrity rule. **Hold.**

Malformed required time **reference** still fails. That is not “waive time because the capsule looks valid.”

---

## 3. Recursive retention and discovery

317 states retention is recursive over **required typed dependencies**, not the latest live pointer: every retained event’s `previous` EventRef; continuity `sourceBeforeImage` and `targetBefore.image`; restore proof images and original direct terminal. Superseding the **live** `sourceFence` does **not** remove the earlier continuity event from the event chain or reclaim its image. 222 no-GC; no cleanup authority here.

Lawful carry **producer** must leave a full path from the resulting capsule through retained events **or** live fence to the image that supplied selected L. Reachability is a **publication invariant**. Readers fail **unavailable** on missing EventRef/image, malformed edge, cycle, or exhausted budget. No unrelated records scan; no silent switch to the other equal-L proof. No new wire member.

This **closes 315’s fence-supersession gap as existing-edge law**, not a new locator field. Missing references fail unavailable, as disposition required. Discovery remains a **candidate generator**, not durable consumption, and **not a proven total algorithm** (317 still says so).

**Still not total:** capsules produced **before** this publication invariant may lack a complete event path; those fail unavailable — no migration invented. Event-chain cycles/budget exhaustion are unavailable, not a reverse index.

---

## 4. Whole prerequisite path — circular premise

317’s new section is the important remaining owner statement: the S4.5 exception is **not** “omit two fields from a generic DFS.” Current/proven standing has its own constructor (native custody, 222 census, projection, independent original direct-terminal witness). That constructor **must not** eagerly follow `descriptor` → role-event `clock.by` → `clock-write.evaluation` and thereby **reload the missing old T**.

If a purportedly independent standing proof **in fact** requires that historical time input, that is an **unresolved dependency**, not success and not a “partial graph = complete proof.” 315 source text and 316 literal bindings **do not** settle the implementation plan.

**This does not silently waive time.** A capsule that is schema-valid with a dangling `timeEvidence` locator is **not** accepted standing by itself. Standing is the scoped 222/custody constructor. 317 correctly refuses arbitrary JSON as publication proof.

**Concrete remaining obligation (not closed):** enumerate **exact fields and predicates per constructor** (S4.5 authority-for-image; current-capsule census; floor discovery; continuity carry) **before** a native consumer. An omitted target must be **outside the requested predicate**, never a failed required read turned into skip. Adversarial tests of that consumer remain owed (OWNER list plus: standing constructor with `clock.by` present; census that must not decode evaluation raw; missing EventRef after fence replace).

**Circular-premise test:** if `AcceptedRecoveryAuthorityForImage` step 1 is implemented by “parse current capsule + walk its publication events,” it reintroduces T. Step 1 must stop at **physical current file + successor-bucket census + reconstructed AFTER projection** without loading `clock.timeEvidence` **targets** or `clock-write.evaluation` bytes. 317 names the obligation; it does **not** supply the field list. **Not an implementation approval.**

---

## Findings

| Item | Result |
|---|---|
| Mixed equal-L designated target T (even source epoch / target ordinary) | **Closes 315 Q1 as explicit policy**; nonselected proof retained, not deleted |
| Two epochs at equal L | Same base rule; no serial/hash priority — **hold** |
| Required P2 / `context.time` **locator** shape; targets out of S4.5 scope | **Closes** 315 locator-shape correction |
| Recursive EventRef / CapsuleImage retention under 222 no-GC | **Closes** fence-supersession gap **if** producers keep the path |
| Whole-path scoping vs two-field DFS | **Named remaining implementation obligation**; not waived |
| Wire / native 316 / 318 | Unchanged; 316 is not this consumer |
| Totality of discovery | **Still not claimed, still not proven** |

**Actionable encoding gap:** none. **Actionable owner gap:** per-constructor field/predicate plan and consumer tests **before** native 317 recovery work. Do not treat 317 prose as that plan.

---

## Remaining (do not count closed)

Native scoped constructors, 222 unique/durable publication as implemented product, 312 embedded resolver on S4.5 ancestry, 316 is only literal bind_context, 318 is not 317, M2–M6. Historical capsules without the new publication invariant stay unavailable.

---

## Verdicts

- [x] **317 as source follow-through of 315:** archive and 315 copies verified; mixed equal-L policy named without epoch-priority or delete; locator vs target split explicit; retention/reachability stated as existing typed edges; circular DFS named and forbidden in prose.
- [ ] **Not** a complete native traversal spec, total discovery algorithm, consumer implementation, or product installation.
