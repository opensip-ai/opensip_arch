# Independent review — authenticated command composition 251 r1

**Standing:** bounded code review of frozen `authenticated-command-reference-wip-251-r1`. **Not** cumulative approval, installed source, current root/revocation/time, whole-image effect, publication, 51-command completion, or M2 close. Archived 250 (`35576c02…c75f`), 248/249 (`c407f4f4…b15c`), and 247 (`d5a7d732…4984`) reports were not edited.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Nested 248/249/250 archives pin-verified; remaining fixture siblings reused from those already-verified extracts. Frozen check/variant output directories were not overwritten. Hardcoded `/tmp/opensip-implementation/m2-authenticated-command-reference-251` and 249 paths were redirected in the review copy.

This is **resource-context relocation**: signature checking and replay/delivery share one `Operation` budget and fail-stop. It is not a semantic join of the command payload to the authenticated pair.

---

## Verification

Frozen archive: **14041284 B, 1558 members, SHA256 `edc0125f70d52966b8407052455dff773bbb0ae36f6cb052240aaf155e5dc64b`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed 1558/1558. Standing: Incomplete WIP, not approval or source selection.

Included predecessor tars match reviewed pins: 248 r1 `08105445…9396`, 249 r1 `3298e2b7…2c54`, 250 r2 `dbf1aa27…cf85`.

Candidate: **1361** files, **11** SHA deltas vs 248 r1, **34** pin updates. New/changed subjects: `trust_authorization_reference.py`, `Operation.authorization`, `workflows/current/replay_reference.py`, pin inventories, and `trust-authentication-composition.v1.md`.

Included keys are **TEST ONLY**.

---

## What 251 composes

`security/trust_authorization_reference.py` is the 250 algorithm as an **internal helper**. Independent AST dump: `require`, `root_binding`, and `_authenticated` are byte-equal to 250 r2. `read_doc` uses lower `I.shape` instead of `M.I.shape`. There is **no** public `authenticated()` wrapper. The helper imports `trust_input_reference` and `envelope_reference` only — not `trust_operation_reference` and not `workflows/`.

`Operation.authorization` owns the outer `budget.guard` and calls `A._authenticated(self, ...)`. Failures latch the same budget; a later producer cannot reset it.

`workflows/current/replay_reference.py` has **function/class ASTs equal** to 249 (4 defs). It loads local `delivery_reference.py` and uses **that module’s `M`**. One operation created in this replay/delivery context can call `op.authorization` and `prepare`/`replay` without independently imported `Operation` class mismatch.

Current and historical command schemas/inventory are unchanged (38+5 composition: 49=45+4, 26 historical schema files byte-identical, no `/tmp`/`m2-` in the six 248 current modules plus replay). Isolated candidate import still works; local pin tamper still fails.

Shared-command tests use **separate** authorization and replay fixture sets and assert both `full-payload-closure-and-bundle-quorum` and `full-metadata-authentication-and-requested-effects` remain pending. Shared context is not proof that the command’s payload is that authenticated pair.

---

## Reproduction

Fresh output directories. Frozen `authorization-check-r1/`, `shared-fixtures-r1/`, `integration-variants-r1/` were not overwritten.

| Corpus | Result |
|---|---|
| Relocated 250 authorization | **42/42**, source `dfff1a05…7653` (helper) |
| Relocated 249 replay | **41/41**, counters 9 / 22 / 6723, source `da097238…fd8e` |
| Relocated 247 delivery + 248 integration | **38 + 5**, counters 9 / 17 / 6723 |
| Shared-command | **13/13**, combined counters **13 / 26 / 16903** |
| Integration omission controls | **2/2** core-equal frozen results |

Shared 13: both producer orders; exact/short combined budget; signature failure then closed replay; replay failure then closed authorization; repeated auth **edges +4** with objects/bytes unchanged (reference recapture, not raw-byte dedup); explicit pending semantic-join case; 250 bodies unchanged / no import cycle.

Two controls: omit outer fail-stop (`return A._authenticated(...)`) or reset signature context (`A._authenticated(Operation(), ...)`). Baseline refuses subsequent replay (`operation-budget-closed` / `operation-object-budget`); mutant wrongly prepares it. Test-only module wiring (`R.M=m` etc.) is **identical** for baseline and mutant so Python class mismatch is not counted as a killed guard.

Initial shared driver (`check_shared_command-before-syntax.py`) has a SyntaxError (`bad(...,'operation-budget-closed'and lambda: ...)`); `shared-command-r1.stderr` retains it. Corrected r2 passes; **production** helper/Operation/replay were not relaxed to fix the driver.

Root suites **inspected, not rerun**: foundation 231, native 477, workflows 2193, security 580, carrier 479, integration 1787; envelope 1803 historical / 47 explicit differential / 55 actual replay-crypto (qualification also records 168/147/6000 as in 248). Those receipts do not qualify native effects.

---

## Independent probes

| Probe | Result |
|---|---|
| 250 `require` / `root_binding` / `_authenticated` AST | equal |
| Helper public `authenticated` / Operation import / workflows import | absent |
| `read_doc` | `I.shape`, not `M.I.shape` |
| 249 replay AST | equal; `M=D.M` |
| `Operation.authorization` | `self.budget.guard(lambda: A._authenticated(self, ...))` |
| Current module temporary paths | none |
| Combined counters / pending join case | 13/26/16903; explicit non-join case present |
| r1 driver typo | retained in beforeimage + r1 stderr |

The helper’s “no security→workflow import” claim holds for `trust_authorization_reference.py` and `trust_operation_reference.py`. Historical security **check** scripts still mention workflow paths as they did in 248; that is not a new circular import from this helper.

---

## Remaining (do not count closed)

Semantic command-to-authenticated-closure join; complete payload/member/BUNDLE validation; current revocation union; held-root custody; S4/tEval; ancestry/floors; role/batch effects; live publication; original-scope replay readmission; receipt retention; actual delivery. GC, two evidence commands, mutating transport, native writers, source selection, M3–M6. 251 is not installed runtime source.

---

## Verdict

- [x] Archive/pins/members verified. Nested 248/249/250 pins match. **42 / 41 / 38+5 / 13 / 2** reproduced. 1361 files, 11 deltas, 34 pin updates.
- [x] 250 algorithm relocated as an internal helper under `Operation.authorization` fail-stop; 249 replay AST-equal under delivery’s `M`. One budget and fail-stop across both producer orders. Isolated import and pin tamper still hold.
- [x] Shared tests assert pending full-metadata/effect owners and use separate fixtures. r1 shared-driver syntax failure retained; production not weakened.
- [ ] **Not** semantic command authorization, current authority, native custody, installed source, or M2 completion.
