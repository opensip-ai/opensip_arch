# Independent source review — scoped time-admission proposal 315

**Standing:** bounded source review of frozen `time-admission-proposal-315`. Unselected **new** completion of 314 ADDENDUM’s two unresolved policy questions, plus a replacement for the withdrawn same-store `previous` walk. Not native implementation, schema change, 313 codec approval, 316 literal-context capture, publication qualification, or product installation. Installed product remains `fa72e50`. 313 REVIEW/ADDENDUM and 314 REVIEW/ADDENDUM were not edited.

Python 3.12.13 `-I -B`. No native tests. No product/frozen edits.

Pins **before** extract: **428756 B, 203 members, SHA256 `decb680d01ab517081b675e2652b23780d457f19069e44f793ffd3208a2b25d8`**. Extract rehashed **203/203**. Copied 314 REVIEW/ADDENDUM byte-identical to live (`d54342fd…daca` / `02a3a0bc…c8ee`). Nested 310 archive pin `120c4046…dd9d`; 312 copies `f04b5b42…6e5b`. OWNER.md SHA256 `908877c4…1b0e`.

314 REVIEW’s tEval vs floor split **stands**. 314’s same-store `previous` algorithm is **withdrawn** (already in 314 ADDENDUM; 315 replaces it). Native 316 is 312 literal-context binding only and does not implement 315.

---

## 1. Equal-L different T

**Rule as written:** after **both** relied-on sides have admitted L and its proof, copy the proof of the **strictly greater** L. On equal L, keep the full NodeRef from the designated base image: forward → source BEFORE; ancestor → target BEFORE; restore → proven N. Tie choice is not permission to skip a missing competing proof. No hash order, no late-load preference, no merge of proof records.

**Copy/max of the scalar L** is preserved (`selected L = max`). F remains a **separate** copy/max (222 restore may raise F toward n; S4.5 is the only lowerer). Ordinary Keep (never replace T when L unchanged **within** a store) and S4.5-apply (always new T, even equal L **within** a store) are not rewritten by this carry rule.

**Not a metadata identity fork.** T NodeRefs are evaluation/epoch records, not signed catalog/root bodies. 222 fork language stays on equal-version **signed metadata** identities.

**Not orphan acceptance.** Both closures must admit before the choice; a missing competitor is unavailable, not a win for the present side.

### Named tension (not a silent reject)

Ancestor or restore at **equal L** with **distinct T**, where one side’s T is an **S4.5 epoch** and the other’s is ordinary S4: the designated-base rule keeps target / N, which can **drop** an admitted epoch provenance that 225 treats as the replacement proof of that L **on the non-base store**.

- **Restore:** keeping N at equal L is coherent with “proven branch,” not observed n. n’s later S4.5 at the same L is outside the proven chain. **Hold** for restore.
- **Ancestor:** both sides are admitted live stores. Preferring target ordinary T over source epoch T at equal L is an **explicit new policy**, not inherited 201/222 copy/max (those name the scalar max, not proof identity). If the owner wants epoch provenance to dominate at equal L, that rule is **missing**. If designated-base stability is the intent, state that dropped non-base epoch T is accepted.

Forward has no target L; source T (Keep or S4.5) is carried. **Hold.**

Identical NodeRefs: no choice. Misleading digest order: rejected by construction.

**Verdict Q1:** the rule is a lawful explicit completion of 314 ADDENDUM’s unresolved equal-L datum **if** both proofs are required and Keep/S4.5 intra-store rules stay put. **Correction:** name the ancestor equal-L / mixed epoch-vs-ordinary case as designated-base (drop non-base epoch T) or add “epoch T wins at equal L.” Do not treat it as already settled copy/max.

---

## 2. `AcceptedRecoveryAuthorityForImage` (S4.5 only)

**Intent:** make 215/227’s missing-**old-T** exception executable when `acceptedAuthority.context.time` **is** that same missing T, without recursive `AdmitTEval` / `AdmitFloor`.

### Exact non-time accepted-standing proof

Standing is **not** derived from the RootAdmission’s original tEval. It is:

1. **This before-image is the native current capsule** under fence/custody **or** an independently 222-proven historical image (direct terminal witness + complete successor census). Caller bytes, orphan descriptor, version number, or cached boolean are insufficient.
2. **Closed P2 head identity:** `acceptedAuthority == beforeImage.heads.root.admission` (hash **and** length), plus root DocRef, `RootBinding`, `rootVersion` (312 P2 literals).
3. **Time-free authenticity** of that head’s retained ancestry: CoreAnchor TCB / complete embedded chain, ordinary old/new quorums, recovery authorization edges, original edge revocation contexts, raw body/envelope. Missing any of those bytes → unavailable.
4. **Current** complete revocation fact-set (union, admitting-root ancestry, finite work profile). Apply **current** filtering only to held RECOVERY keys for the **epoch** application.

`OriginalContext.time` **targets** (and historical activation windows) are **out of scope**: field remains required on the admission **record**; this proof **must not load** the target and **must not** change the result if the target happens to be present. That matches 314 ADDENDUM’s withdrawal of optional-integrity, and it is **narrower** than “skip all `context.time`.”

### First root whose `context.time` equals missing T

Genesis ordinary admission: `context.time` often **is** the L-establishing evaluation (T == evaluation == `context.time`). Loading that target **is** old-T admission and would erase the exception.

This capability **does not** follow that edge. The standing premise is step 1 (current/proven **capsule**), not re-derivation of the publication that first wrote the head. 222: a RootAdmission is an authentication edge; **acceptance** is capsule/outcome + head joins. S4.5 is already **not** dependent on old T (215 D). 222 successor census for S4.5 does not resolve `clock.timeEvidence`.

**Circular-premise test:** admitting “current capsule” for S4.5 must **not** DFS `timeEvidence` or `context.time`. If a generic walker still does, the exception is not executable — that is an **admitter-scope** defect, not a missing wire field. 315 correctly forbids opportunistic load.

**History / parent admissions** also carry `context.time`. Step 3–4 load those **records** and list DocRefs; they must not load **time targets**. Missing **parent/authorization/list** bytes still fail (not old T).

### What this does not grant

- No role/head change, no ordinary/BEGIN/COMMIT/continuity/restore reuse.
- No orphan head (must equal this BEFORE admission).
- No self-supporting proof from the epoch input or admission node alone (step 1 is independent 222 current/proven).
- Subsequent metadata tEval remains **S4**, not the epoch (314 ADDENDUM Q3). 315 restates that. **Hold.**

**Rolled-back capsule:** 222 successor census → behind/fork/unavailable blocks S4.5 publication. **Hold** if step 1 is actually that census, not a shape-only image.

**Verdict Q2:** this is an explicit, executable completion of 314 ADDENDUM’s unresolved `AdmitTEval(acceptedAuthority.context.time)` datum **for S4.5 only**, provided step 1 is independent of T. **No broader schema change is required.** **Correction:** state that P2 `clock.timeEvidence` **locator** must remain field-present (shape) while its **target** is out of scope; a missing **locator** (malformed required time reference) still refuses. Do not weaken step 3 if ancestry bytes are missing.

---

## 3. Candidate discovery (314 walk withdrawn)

**Path:** admitted capsule `eventHead` → `previous` EventRefs (same store, budgeted) → typed `clock-write` with `{kind:new, proof:T}` and `evaluation == proof`. Load `evaluation.beforeImage` NodeRef. That image’s **raw digest** is 222 `previousCapsule` **H**; enumerate the **bounded** `publications/by-predecessor/H` bucket (≤64). Exact consuming D: same store, adjacent revision/nativeBefore, this event, reconstructed AFTER = `afterProjection` + full PublicationRef, after clock T matches. Durability: native current file **or** independent direct-terminal proof — **not** D alone. Continuity/restore: retained CapsuleImage NodeRefs + §1 L-choice. Empty-event: `eventHead` may predate this revision; still walk that chain. No `records/<bare previous SHA>`, no global reverse index.

**Discovery ≠ proof.** Event presence is not durable consumption.

### Is it total for lawful current/proven states?

**Sufficient starting roots:** native `state.v1`; 222-proven reconstructed N; continuity `sourceBeforeImage` / ancestor `targetBefore.image` (full NodeRefs). From T alone: still **unavailable** (acyclicity). **Hold.**

**beforeImage digest → by-predecessor bucket** is the correct **forward** 222 locator, not a lifetime reverse index. Fork/behind/capacity stay mandatory. **Hold.**

**Not proven total.** Named gaps:

1. **Event-chain retention.** 222 says events of a retained capsule/clock witness remain live and there is no GC in that proposal. If an implementation drops intermediate `previous` EventRefs, discovery cannot reach the establishing clock-write and **must fail unavailable**, not search records. **Missing product-retention datum**, not a new wire field.
2. **Continuity after `sourceFence` is superseded.** Target-side continuity event holds `sourceBeforeImage`. That event must remain on the **target** event previous-chain (or the selected-L image must still be a retained CapsuleImage). If both are gone, there is **no** encoded jump to the source establishing write. **Correction:** require that the selected-L CapsuleImage NodeRef still be reachable from the starting capsule (event chain or live fence `by`); else unavailable.
3. **New-store revision 1 / `previous: null`.** Must not walk target `previous`; must use source BEFORE image. 315 states this. **Hold** if implementers do not fall back to target eventHead-only search for source T.
4. **Abandoned clock descriptor.** Matching bytes in a bucket must not win without step-1 current/proven standing. 315 states this. **Hold.**
5. **Circular durability.** Starting from current native file avoids circularity. Historical start must already be a proven image (continuity/restore). Candidate D cannot prove itself. **Hold.**

**Correction to 314:** do not `load(records, capsule.previous)`. 315’s EventRef + PublicationRef + CapsuleImage strategy is the right owner set. Treat it as **bounded discovery with fail-closed gaps**, not a proven covering algorithm.

---

## Findings

| Item | Result |
|---|---|
| Three capabilities distinguished (tEval / floor / S4.5 accepted-authority-for-image) | **Hold** — needed; no generic boolean |
| Equal-L designated-base choice | **Hold** with ancestor mixed epoch/ordinary tension named |
| S4.5 authority-for-image without loading `context.time` targets | **Hold** if step 1 is 222 current/proven without T DFS |
| Epoch as metadata tEval | **Still forbidden** |
| Event/publication discovery | **Plausible, not total**; fail closed on event-chain / image-retention gaps |
| Wire change | **None required** for these three |
| Native 313/316 | **Do not implement 315** |

**Actionable encoding gap:** none. **Actionable owner gaps:** (1) ancestor equal-L epoch vs ordinary T; (2) require selected-L CapsuleImage to remain reachable after fence supersession; (3) fail unavailable on event-chain gaps — no records search.

---

## Remaining (do not count closed)

Native 222 unique/durable publication, fences/custody, actual crypto/TCB, 312 embedded resolver on the S4.5 ancestry step, 313 P0/P1 producer, 316 is not this, M2–M6. Adversarial fixtures listed in OWNER §validation are **owed before a consumer**.

---

## Verdicts

- [x] **315 as unselected source completion:** archive verified; 314 copies match; equal-L rule is an explicit policy (one named tension); S4.5 accepted-authority-for-image can be independent of old T if capsule standing is 222-without-T-walk; discovery via EventRef/PublicationRef/CapsuleImage replaces the invalid `previous` SHA load.
- [ ] **Not** a total algorithm, native admitter, schema freeze, 313 re-approval, or product installation.
