# CRC-2: the core provider closure's third use (contract successor)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r1, PROPOSED, not accepted.** It is a design unit. It edits only arch, and changes no product file, code, class, exit code, route or public code. It needs CODEX2's `ACCEPT-DESIGN-UNIT`, with a review that lists `supersededPassages`, and the lead's root assent before it can be bound in the product's `design-lock.json`. It binds only after M3-C r8 is accepted.

**What it is.** M3-C r8 names successor **CRC-2** (MC8:519, MC8:1144): item 9's use 3, "the core provider closure as producer and enumerator of host-derived `inventory` records in every universe, its four fields, its bound, and its `semanticClosures` membership when an `inventory` cell is requested". That is M3-H r3's cross-law item **X-H3** (MH:860-866; its successor row, MH:811), which M3-PLAN r10 routes to "M3-C r8 and CRC-2" (M3P10:306, :361, :405). CRC-1 left it to this unit (CRC-1 README, LD-8). CRC-2 must be accepted before C4a (MC8:1172).

**Law standing.** MC8 is in review with CODEX2 in the same request (`reviews/codex2-snapshot-plan-c-r8`). CRC-2 carries MC8's item 9 text and nothing else. If that review changes item 9, CRC-2 is rebuilt to match.

**Product.** Main `21e428d` (REG v3's binding), read only. Its lock has 98 contract successors and 2 contract passage supersessions (SD-7's and REG v3's). CRC-1 is bound at `392499e` (lock index 82), and SYN-1F at `218465f` (index 90). The record is built and checked against `21e428d`'s lock, read with `git show`.

## Short names

| Name | Document | sha256 |
|---|---|---|
| **MC8** | `docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`, M3-C r8, in review in the same request | pinned in the request |
| **MC7** | `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r7.md`, M3-C r7, accepted in review by CODEX2 | `a1ee9386…` |
| **MH** | `docs/implementation/m3/fact-admission-h/PROPOSAL-r3.md`, M3-H r3, accepted by Grok | `7a562720…` |
| **M3P10** | `docs/implementation/m3/M3-PLAN-r10.md`, accepted by Codex | `ec8c38f8…` |
| **CRC1** | `docs/implementation/m3/snapshot-plan-c/crc-1/successor.json`, bound at `392499e` (21,493 bytes) | `29df5f5e…` |
| **SYN1F** | `docs/implementation/m3/syntax-e/syn-1f/successor.json`, bound at `218465f` (9,697 bytes) | `736f2fed…` |
| **IE** | `docs/v2/contracts/product-v1/identity-and-evidence.md` (135,448 bytes) | `c82404f3…` |
| **IDS** | `docs/implementation/m3/syntax-e/syn-1f/design/foundation/identity-schemas.v3.json`, SYN-1F's complete copy, the selected identity schema bundle (200,510 bytes) | `73645b76…` |
| **IDS-L** | `docs/implementation/m3/preview-pack-i1/i1-l/design/foundation/identity-schemas.v3.json`, I1-L's copy, which SYN-1F's copy succeeded (198,725 bytes) | `c9214f03…` |
| **VD** | `tools/verify_design.py` at product `21e428d` (43,946 bytes; VD2-a's bytes) | `7b313de6…` |
| **VD2** | `docs/implementation/m3/verify-design-vd2/PROPOSAL-r1.md`, the accepted law of contract passage supersession | `2e4f70b4…` |

The precedents for the form are SD-7 (`docs/implementation/m3/supervisor-d/sd-7/`) and REG v3 (`docs/implementation/m2/project-registry-owner-selection-v3/`).

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `PASSAGES.md` | generated: the two supersessions and the two overrides, each with its exact `before`, its `after` and the character-level changes |
| `successor.json` | the record: two parents, two `passageOverrides`, two `passageSupersessions`, five candidates |
| `evidence/build_crc_2.py` | builds the generated files, the record, the subject manifest and the draft unit record deterministically; `--check` compares instead of writing |
| `evidence/check_crc_2.py` | read-only, independent checks |
| `evidence/verify_scratch.py` | the real VD in a throwaway worktree, with the scratch review and assent served from memory, plus VD2's refusals |
| `../crc-2-subject.json` | the subject manifest (generated) |
| `../crc-2-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW`, naming `reviews/codex2-snapshot-plan-c-r8/crc-2/review.json`; not part of the subject |

## What changes

Four entries. `PASSAGES.md` has the full texts.

| # | Kind | Parent | Selector | Change |
|---|---|---|---|---|
| 1 | **supersession** of CRC-1's override | IE | line 285 | CRC-1's "Core role closures" paragraph. The heading names CRC-1 and CRC-2. The provider bullet's "exactly two admitted uses" becomes three. Use (3) names the three `inventory` relations, its four fields and what it never admits. Membership becomes "exactly when the Plan selects a syntax universe or requests an `inventory` cell". "It is never the producer of a TypeScript or Rust record" becomes "Apart from use (3), …". The mirror rule is added: no language provider closure produces or enumerates an `inventory` relation's record. Output-schema registration covers the host inventory stage too. The detector and adapter bullets and the closing paragraph are CRC-1's, verbatim. |
| 2 | **supersession** of CRC-1's override | IE | line 1377 | CRC-1's `semanticClosures` exception. It names CRC-1 and CRC-2, and adds "or requests an `inventory` cell". |
| 3 | override | IDS | `/x-opensip-digest-domains/closureKinds/note` | The string SYN-1F carries in place from CRC-1. The core provider closure's "exactly two uses" becomes three, with use (3)'s relations and fields; "it never produces a TypeScript or Rust record" becomes "Apart from that third use …", with the mirror rule. |
| 4 | override | IDS | `/x-opensip-digest-domains/closureMembership/selectionLaw` | The string SYN-1F carries in place from CRC-1. It names CRC-1 and CRC-2, and adds "or requests an inventory cell". |

Nothing else changes. `closureKinds.byField`, the closure kind list, every schema shape, H domain and recipe, the enumeration and execution-input schemas, every registry, generated file, product copy and inventory keep their bytes and meaning. The check script shows that the two IDS strings are the only change to that document.

## The rule

The texts say the following. This is MC8 item 9 (MC8:486-519) clause for clause.
- **Three uses under one identity.** The core provider closure keeps CRC-1's two uses: an import's `producerClosure`, and syntax-universe work. It gains **use (3): the producer and enumerator of host inventory records in every universe.** These are the records of `file@enumerated`, `package@manifest-declared` and `vcs-change@vcs-reported` that the host derives from retained records, and that no language provider produces (NCM:949; MH item 18).
- **Use (3)'s four fields:**
  - the `enumerator.closureId` of each enumeration binding of a requested `inventory` cell, available or not;
  - the `stage-spec.producerClosure` of each host inventory stage;
  - that stage's `view.producerClosure`, and so `fact.producerClosure`;
  - that stage's `subject-scope.enumeratorClosure`.
- **What use (3) never admits:** a record of another relation; a record a language provider returned; the enumerator of a binding that owes a symbol inventory; `CandidateProducerResultV1.producerClosure`. `cache-key.producerClosure` stays refused for every core role closure (CRC-1).
- **Membership.** It is a `plan.semanticClosures` member exactly when the Plan selects a syntax universe or requests an `inventory` cell, and never otherwise, not even explicitly. All three statements of membership (IE:285, IE:1377 and `selectionLaw`) carry the same clause.
- **The mirror.** No language provider closure is the producer or enumerator of an `inventory` relation's record.
- **Unchanged:** the three projections, `manifestDigest`, recognition, the detector join, the adapter's one field, retention and the identity consequence.

**The bound keeps MC7:458's principle,** "the provider did not produce the record", both ways. The core provider closure names an inventory record only where the host's own code derived it (MH item 25's H3, shipped in the core). A language provider is never named on one, because it never produces one.

## Why this form: the lock, selector by selector

`build_crc_2.py` reads the lock at `21e428d` and finds each key's current meaning.
- **IE:285 and IE:1377 are taken by CRC-1.** Both carry CRC-1's bound overrides, and no later record supersedes them. A second override of either refuses ("conflicting contract passage overrides", VD:409-411), and `verify_scratch.py`'s probe shows it. Law VD2 admits a **contract passage supersession** instead (VD:349-369): the entry names CRC-1's record by exact pin, with the same parent and selector, and its `before` is CRC-1's `after`. The review must list `supersededPassages`, equal to the record's `supersedes` list (VD:420-426).
- **The selected IDS is SYN-1F's copy.** It is the last complete identity-schema copy in the chain, and it carries CRC-1's three strings in place (SYN-1F README, LD-F3). No bound record overrides its pointers, so CRC-2's two pointers on it are fresh keys and take plain overrides. Each `before` equals CRC-1's `after` on IDS-L, which the checker asserts. The `manifestDigest` artifact string needs no change: it already names the core provider closure.
- **IDS-L keeps CRC-1's three bound overrides,** on a copy that is no longer selected, as the original IDS keeps EC1's (CRC-1 LD-1). CRC-2 does not touch them.
- **Untouched on purpose:** COMP:9, WS:308, WSE:312 and the detector-manifest description, which concern the detector only; NE, and NCM:949, which already says the host produces inventory records; ENC with its schema, and EXC with its schema, whose joins already admit a Plan-selected provider closure as enumerator and producer; and the product copies (CRC-1 LD-7).

## Lead decisions

Each decision is dated 2026-10-04 and made under the owner's standing direction to decide on the lead's recommendation. Each names the alternatives it rejects, and the owner may reverse any of them. MC8's LD8-6 is LD-1 and LD-2 here.

**LD-1. IE:285 and IE:1377 are superseded in VD2's form.**
- **Rejected: a new paragraph at a fresh line,** such as IE:286, which CRC-1 LD-8 advised before VD2 was integrated. It would leave CRC-1's "exactly two admitted uses", its membership clause and "It is never the producer of a TypeScript or Rust record" in force beside a paragraph that contradicts them.
- **Rejected: raw overrides of the two lines.** VD refuses them as conflicting (probe below).
- **Rejected: a complete IE copy.** It would move the selected IE for every successor in flight.

**LD-2. The IDS text goes on SYN-1F's copy, by plain overrides.**
- **Rejected: superseding CRC-1's IDS-L overrides.** IDS-L is no longer the selected copy, so a new meaning there would be read by nobody, and SYN-1F's copy would still say "exactly two uses".
- **Rejected: a new complete IDS copy.** No structure changes, so string overrides suffice, and a copy would fork the selected text.

**LD-3. The passages are rewritten, not appended to.** Appending "and a third use" after "exactly two admitted uses" would leave a false sentence in force. Every sentence of CRC-1's text that CRC-2 does not rewrite survives verbatim, and the checker proves it sentence by sentence.

**LD-4. No vector, no new code, no product copy change.** Use (3) names an existing closure, whose id CRC-1's vector already gives. A misused core provider closure refuses through the existing closure-kind and membership refusals (CRC-1 LD-5). Product copies are annotation prose that no code dispatches on (CRC-1 LD-7).

**LD-5. Binding.** After `ACCEPT-DESIGN-UNIT`, and only once MC8 is accepted, the lead appends CRC-2's entry in a binding-only product commit, before C4a.
- **Rejected:** binding before MC8 is accepted, which would put identity text in force ahead of its law (CRC-1 LD-8, reason 1); binding inside C4a's commit, which would mix review subjects.

## Cross-law items

1. **Later IDS copies.** VD does not enforce which copy is selected. Any later complete identity-schema copy must carry CRC-2's two strings in place, as SYN-1F's carried CRC-1's. Review must hold this.
2. **H and core packaging (MC8's X-9).** The host inventory stage's output schema must be a member of the core platform tree at `opensip-interface/stage-output/<operation>.schema.json` (IE:1303-1318). Otherwise C4a's stage spec refuses `STAGE_OUTPUT_SCHEMA_UNREGISTERED`.
3. **FA-2's enumerator ask (M3P10's C row).** The enumerator of a binding that owes a symbol inventory stays the universe's worker provider closure. Use (3)'s binding bound agrees with it.

## Points for the reviewer

- **R1 (faithfulness).** Is CRC-2 exactly MC8 item 9's use 3, its bound and its membership, neither wider nor narrower?
- **R2 (form).** Are the supersessions well formed under VD2, and are SYN-1F's copy and plain overrides the right IDS target (LD-1, LD-2)?
- **R3 (nothing else).** Does every sentence of CRC-1's text that CRC-2 does not rewrite survive, and do the three membership statements agree?
- **R4 (the bound).** Does use (3) keep MC7:458's principle both ways?
- **R5 (binding).** Does the record bind after main's chain with your review's `supersededPassages`, and does any selected passage still conflict?

## Binding

CRC-2 binds on VD at main `21e428d`, on top of all 98 contract successors. After `ACCEPT-DESIGN-UNIT` and MC8's acceptance:
1. copy the review into `docs/implementation/m3/reviews/codex2-snapshot-plan-c-r8/crc-2/review.json`;
2. complete `crc-2-unit.json`: status `ACCEPTED-DESIGN-UNIT`, the review pin, `rootSubstantiveAssent: true`;
3. append the four pins to the product lock;
4. run plain VD.

The review must carry this `supersededPassages` list, exactly:

```json
[{"record": {"path": "docs/implementation/m3/snapshot-plan-c/crc-1/successor.json", "bytes": 21493, "sha256": "29df5f5e2b145daf3c9b8e231ccac1d08c5b36d2eb006fbdc3bba543d7084166"}, "parent": {"path": "docs/v2/contracts/product-v1/identity-and-evidence.md", "bytes": 135448, "sha256": "c82404f3a0cf56fa6cc02e99cc3ebbd5356fedc3b36aeb38f9ef284077fbd31f"}, "selector": {"line": 285}}, {"record": {"path": "docs/implementation/m3/snapshot-plan-c/crc-1/successor.json", "bytes": 21493, "sha256": "29df5f5e2b145daf3c9b8e231ccac1d08c5b36d2eb006fbdc3bba543d7084166"}, "parent": {"path": "docs/v2/contracts/product-v1/identity-and-evidence.md", "bytes": 135448, "sha256": "c82404f3a0cf56fa6cc02e99cc3ebbd5356fedc3b36aeb38f9ef284077fbd31f"}, "selector": {"line": 1377}}]
```

## Evidence runs

Every run used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`. Nothing ran cargo or a test.
- **`evidence/build_crc_2.py`**, then `--check`, which reports identical bytes for every generated file, the unit draft included.
- **`evidence/check_crc_2.py`** passes at `21e428d`. It checks the parents, each supersession's target and current meaning, each override's key and carried text, the sentence-by-sentence survival, the rule's clauses, the three membership statements, MC8's agreement, and this README's naming of every passage.
- **`evidence/verify_scratch.py`** in a throwaway detached worktree of product main `21e428d`, with a private 0700 TMPDIR under `$(getconf DARWIN_USER_TEMP_DIR)`. Its output is pinned in the review request (`reviews/codex2-snapshot-plan-c-r8/evidence/local-binding-check.json`), and the worktree was then removed.
  - **Baseline:** the literal CLI on main's lock passes, with 98 contract successors and 2 contract passage supersessions. The overlay run agrees.
  - **With CRC-2 appended:** PASS, with the worktree as implementation and without it. There are 99 contract successors and 4 contract passage supersessions. The inventory chain, inheritance and supersessions, generation and admission sources, and verified inputs equal the baseline's.
  - **Refusals:** a review without `supersededPassages` ("contract passage supersession is not listed by its review"); a review with `[]` ("contract review superseded passages differ from the record"); CRC-2 with raw overrides of IE:285 and IE:1377 ("conflicting contract passage overrides"); after CRC-2, a second supersession of CRC-1's IE:285 ("double supersession: the named passage is not the current meaning"); after CRC-2, a second override of its `closureKinds/note` pointer ("conflicting contract passage overrides").
  - **The literal CLI on the appended lock** stops at the SCRATCH placeholder, as for earlier units. The overlay run is the binding result.

## Not changed, and noted

- **No refusal code, class, exit or route is added.**
- **No product file is touched.** No code, test or build was run, and the reference checkers were not run.
- **The closure's identity is unchanged.** Use (3) adds fields to an existing closure, so no Plan that does not select it moves.

## Owner flag

As with EC1 and CRC-1 (MC8 O-2; MH owner flag 4), every core release is also a new producer of every inventory record. Plans that request `inventory` already select the core evaluator closure, so their identity already moves with each release, and use (3) adds no new churn.
