# Ordinary root-chain and T1/DR-103 vs DR-112 adapter law

This is **not** a 285/286 bounded verdict and is **not** an implementation request. Sources: nested 265 candidate (`73c3b3f5…86df`) `security-completion.v1.md`, `core-distribution-binding.v1.md`, `trust-capsule-persistence.v1.md`, `trust-signed-time-inputs.v1.md`, `trust-state-continuity.v1.md` C.3, existing `verified_root_chains::verify_root_chain`, and 284–286 as frozen.

---

## What already exists

`verify_root_chain(anchor, chain, context, budget)` takes an **externally admitted** `ValidatedRootPayload` plus a **proper-successor** `WireRootLink` array. It does **not** take or re-authenticate a delivered first-root envelope. Empty `chain` still checks the admitted anchor's current expiry. Each successor is dual-threshold authenticated (old-root and new-root thresholds, completion §3.1 / TUF §6.1), `previousRootVersion` +1, nondecreasing `issuedAt`, then final validity/future bound. `ChainContext` root/revocations/time are **supplied**, not qualified current authority.

Bootstrap **anchor** is a different object: `core-distribution-binding` C.1 says the anchor is always embedded-bootstrap `rootChain[0]`. C.3 forbids inferring that TR-CORE signed the inventory therefore the root is trustworthy (circular: TR-CORE keys are delegated by a root). Anchor admission takes **no** signature verdict. Why the anchor is trusted is a 229/core-closure + install-channel premise, not an ordinary payload fact.

Capsule persistence: first accepted root is a **DocRef**; identity is domain-separated signed **body**, not raw locator. Alternate envelope spelling of the same body is not a fork. Signed-time-inputs: re-presenting an already-accepted root is still an **explicit presented-root input**; it normally adds nothing above L.

Continuity C.3 (lines 91–101, 109): an ordinary payload is one complete signed inventory. Shared authentication is **root chain, BUNDLE, catalog, list** under prospective contexts and retained∪incoming filtering. Excluding a role from T1 **cannot waive** shared signatures. Relied-on role-specific members use DR-112. Members owned solely by excluded roles still need DR-103: envelope present, well-formed, **nonempty signatures**, exact digest join, member present/shape/byte-bound — but remain **inert**. Shared members are never made inert. Authenticate relied-on members with the finite second-pass union **before** using the payload as signed time evidence.

284–286 currently prepare the **complete component set** and require every component quorum. They are full-set **conditional preparation helpers**, not the complete ordinary-import gate.

---

## Adapter law for payload `rootChain` that begins with an already-accepted root

**Do not:** treat 282/283 supplied-root shape as current-root admission; skip the first envelope silently; invent a self-signature the accepted-anchor rules do not require; use payload `rootChain[0]` as a bootstrap anchor (that is C.1 embedded-bootstrap only); claim circular TR-CORE justification.

**Bind, without circular bootstrap:**

1. **First accepted body.** The first retained ordinary `rootChain` DocRef **body identity** must equal the already-accepted head document (signed-body identity). Keep that DocRef. Envelope spelling may differ; that is not a fork and must not drop the first accepted DocRef.
2. **Presented first-root envelope as shared input.** Continuity C.3 says shared ROOT signatures cannot be waived, and re-presentation is an explicit presented-root input. The adapter **should** authenticate that envelope under the **current filtered ROOT quorum** (finite union including incoming list/chain reports) as a **shared DR-112 input**. That check does **not** admit a new current root, does **not** replace 229 bootstrap-anchor proof, and does **not** treat TR-CORE inventory signatures as the reason the accepted identity is trusted. `verify_root_chain` today does not perform this envelope step: that is the **genuine design gap**. The adapter/reference must state it explicitly rather than leaving a silent skip.
3. **Proper successors.** Remaining ordered `rootChain` members after that first identity. Each is a `WireRootLink` into existing `verify_root_chain` (dual threshold, +1/previous, nondecreasing issue).
4. **Final signing root.** Last chain member's captured body equals the 283 supplied signing-root context (already membership-bound, still not current-head admission by itself).
5. **Finite union.** Successor and presented-first-root ROOT quorums use retained∪incoming keyIds, including chain reports, **before** signed-time use (C.3 line 101). 284 currently leaves all roots unresolved, so this composition does not exist yet.
6. **Same-head / empty successors.** If the payload only re-presents the accepted root, `verify_root_chain` empty-chain expiry still applies to the admitted anchor.

Current population/history/custody of the accepted root remain separate. Store source membership/time/writer context remain pending.

---

## C.3 T1 vs 284–286

284–286 **cannot** be used unchanged as the final ordinary-import gate when T1 excludes COMPONENT:

| Member class | Required now (284–286) | Ordinary-import T1 law |
|---|---|---|
| Root chain, BUNDLE, catalog, list | 284 authenticates catalog/list/BUNDLE; **roots unresolved** | Always shared authentication; cannot become inert |
| Relied-on T1 role-specific | 285 requires **all** component quorums | DR-112 on T1 members only |
| Excluded-role members | still fully quorum-checked | DR-103 presence/shape/nonempty signatures/digest/byte inventory; **inert**; failed DR-112 does not veto |

A later **derived-target** owner must keep shared signatures, keep DR-103 on excluded members, and scope DR-112 to T1 — without an untrusted `authenticated` flag or unsigned executable authority.

---

## Concrete scoped next steps (planning only)

1. Reference composition: retained first-root **body** = accepted DocRef; ordered proper successors; final = supplied signing-root body; union including chain reports.
2. Explicit case: re-presented first-root **envelope** under current filtered ROOT quorum as shared input, owning the first DocRef, not claiming bootstrap or current-head selection.
3. Cases: empty successors (same-head refresh + expiry); one successor; invalid first-root envelope that still matches accepted body identity (must refuse shared auth); T1 excluding COMPONENT (DR-103 inert vs 285 full quorum).
4. Do **not** fold this into 285/286 production; they correctly leave roots unresolved.

**Gap (real, not invented authority):** shared-ROOT-cannot-be-waived vs `verify_root_chain`'s "anchor envelope is not an input" vs 284 "all roots unresolved" is an **unstated adapter law**, not a missing crypto primitive. Bootstrap remains 229. Ordinary import remains unimplemented.
