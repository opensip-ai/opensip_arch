# Bounded critique — incomplete WIP215 revision 7 (closure of my r6 G-1..G-6)

Reviewer: Claude. Date 2026-09-19. **Assistance on an incomplete owner; no approval, no protocol acceptance, no root-source edit, commit or push.** Known 222/creator/schema/model-integration omissions are not re-listed.

## 1. Identity and what I ran
- `subject.tar.xz` SHA-256 `0ebd29971f9d626a722d4831df9365e82a568185ed0b64ebd9d29bd38052a9e5`, 112,192 bytes, 105 members — equals the request; all members hashed from the tar before extraction; 0 non-regular/unsafe/extra; end pass `re-verified`.
- `beforeimages-r7/OWNER.md` is byte-equal to the r6 `OWNER.md` I reviewed; both schemas byte-equal to r6. `OWNER.md` stays 135 lines; I diffed it at sentence level and read every changed sentence (C BEGIN/COMMIT amendment, C.3 inert members / completeness / success dispatch / genesis, D missing-`T` and P1→P2).
- Model: my re-run of `ordinary_batch_model.py` is byte-equal to `ordinary-batch-model-r4.json` (6272 / 4096 with 1024 accepted / 9594 states, 34002 edges, 5340 closed). `coordination-mutants-r2/baseline.py` equals the model; all **eight** owner variants fail when I run them, with semantic messages (`wrong exact role outcome`, `stale barrier blocks head`, `live ceremony barrier bypassed`, …).

## 2. Closure of r6 findings
| r6 | r7 | Status |
|---|---|---|
| G-1 batch BEGIN/COMMIT atomicity vs v14 | explicit `batchCompleteness` on both; on a dispatched failure **every** member gets the existing `RECOVERY-BEGIN-REFUSED`/`RECOVERY-COMMIT-REFUSED`, state unchanged; `whenInactive` precedence kept; pre-dispatch boundary kept | **closed in prose**; not represented in the model — M-2 |
| G-2 model survivors / definitional edges | exact literal outcome tables; stateful sequences with a separately stored binding exercised by real subsequent `begin`/`advance_head`; the 4010 edges explicitly superseded | **my three survivors are killed; tautology removed** — but see M-1 |
| G-3 genesis reachability | permissive sentence replaced by the theorem (accepted ordinary genesis ⇒ BUNDLE and INDEX TRUSTED; shared signers never leave T0 by key loss; post-genesis counters imply no trusted role); P1→P2 wording aligned; 4096-cell check with shared-signer constraint | **closed** |
| G-4 exactness (all T0; T0∖T1 on success; inactive precedence) | all three written | **closed** (my variant `n7` — PRESENT dispatched to removed targets — is rejected) |
| G-5 inert members vs DR-103 | envelope present, well-formed, non-empty signatures, digest-joined still mandatory; only the DR-112 authority half is scoped away; "required envelopes never become optional" | **closed** |
| G-6 missing-`T` ABORT | "safe" removed; root **declines** my `max(wall,F,L)` shorthand and keeps the existing S4 decision with its range/continuity/plausibility guards, no new witness, may advance F/anchor, never L or `T` | **closed — root's version is the correct one**; my shorthand would have bypassed S4's guards. One consequence: N-1 |

## 3. New findings

### M-1 (Medium) — the model rewrite dropped assertions r6 had: four variants that r6 **rejected** now **survive**
My r7 variant run (`claude-out/probes/model_mutants_r7.py`, `io/model-mutants-r7.json`): 16 variants, 9 rejected, **7 survive**. Four of the survivors are regressions against the r6 model, where the identical edits were rejected:
| Variant | r6 | r7 | What is no longer asserted |
|---|---|---|---|
| `f2` shared guards ignored entirely | (f) rejected | **survives** | that `shared_guards=False` ⇒ refusal — i.e. "an older catalog refuses the whole import" and "empty T1 cannot waive shared guards". In the 6272 cells an accepting mutant simply takes the `else` branch, where its outcome matches the tables |
| `f` shared guards waived when no targets remain | rejected | **survives** | same |
| `d` guard-failure refusal writes no clock | rejected | **survives** | that a post-S4 refusal has `clock_written=True` (only the *authentication*-failure side is still asserted, in genesis) |
| `j` abort defaults to `TRUSTED` | rejected | **survives** | "no abort restores TRUSTED": `batch_abort` always passes all-false causes and nothing asserts the result |
New, never covered: `j2` abort priority reversed (the `REVOKED > QUORUM-LOST > EXPIRED > STALE` order is unexercised because only all-false is supplied); `n5` BEGIN selects a `TRUSTED` role (sequences start from all-`EXPIRED`, so "TRUSTED is excluded, never silently changed to RECOVERY" is never reachable in the exploration); `n6` observation events dropped (on success only the PRESENT set is asserted; the REVOKE/QUORUM event list is free).
**[P] bounded correction:** (i) in the 6272 cells assert the **acceptance decision itself** against a literal rule — `accepted ⇔ shared ∧ ∀ i∈T1: guard[i]` with T1 computed from the literal state lists — and `clock_written` on both refusal kinds; (ii) restore the abort table: enumerate the four cause bits per recovering member, assert the exact v14 priority result and `TRUSTED ∉ after`; (iii) seed the sequence exploration from mixed initial vectors including `TRUSTED` and assert BEGIN's selected set against the literal source-state list; (iv) assert the full expected event list (kinds, order REVOKE → QUORUM → PRESENT, from/to), not only the PRESENT index set. A retained variant corpus run on every model revision would have caught the regression; the owner's eight plus these seven is a reasonable start.

### M-2 (Low–Medium) — COMMIT is absent from the lifecycle model, so G-1's closure has no model evidence
The sequence exploration has BEGIN, interruption, same-head ordinary import, ABORT and head-advance; there is no COMMIT action and no refused-BEGIN/COMMIT outcome. Unexercised r7 rules: an interrupted batch cannot commit; a successful COMMIT clears binding and staging and advances the head once in the same step; a failing member refuses **all** members with state unchanged and one refused event each. The limits string says only that "complete crypto guards" are outside the model; the *coordination* of COMMIT is outside too. **[P]:** add `commit(world, member_pass)` with exactly those three assertions and a per-member refused-event check; it needs no crypto.

### N-1 (Low–Medium) — with S4 kept in ABORT, an S4 preflight refusal can hold a batch open where no S4.5 remedy exists
r7: "An S4 preflight refusal leaves the batch unchanged; retained-phase S4.5 is the separately authorized remedy where applicable." In P0/P1 S4.5 is refused by r7's own rule, yet a pre-genesis batch can be begun and, while it is, BEGIN and first-head publication are barred. But such a batch's members are never-established: by C.2 their revoked/quorum/expired/stale causes are "not established as true" whatever the clock says — **their abort result does not depend on a time evaluation at all**. **[P] one rule:** ABORT evaluates S4 only when at least one still-recovering member has retained accepted-document times (a decidable time-dependent cause); otherwise it performs no S4 decision and cannot be refused by one. This confines the stuck case to phase `retained`, where the S4.5 remedy exists.

## 4. Independent check of the stated model claims
- *Exact outcome cells against literal tables* — true: `EXPECTED_HEALTHY/BELOW` are literal and independent of `ENTRY`; refusal audiences are checked against a literal state list. Gap: the accept/refuse **decision** is not (M-1).
- *4096 genesis cells / 1024 accepted with shared-signer constraints* — reproduced; refusal ⇒ `below[BUNDLE] ∨ below[INDEX]`, with no clock and no events, as the pre-dispatch boundary requires. Entry guards are all-true there, which is fine because the completeness path is the same code as the 6272 cells — once M-1(i) is asserted.
- *Subsequent BEGIN and head-advance exercised against a separately stored binding* — true and non-definitional: `check_barrier` calls the real `begin`/`advance_head`, which read `binding`; the owner's two barrier variants and my `n1`–`n4` are rejected.
- *Two generic-role cells are non-shared roles* — stated in code and limits; accurate.
- The exploration also (correctly) lets a same-head import heal an already-interrupted `QUORUM-LOST` member to `TRUSTED` while the batch stays begun for its remaining members; that matches r7 prose (the member left `RECOVERY`, is an ordinary target, and ABORT later leaves it alone).

## 5. Cross-rule checks with no finding
`batchCompleteness` and `importCompleteness` are both "another active conjunct" behind `whenInactive`; refusal publications (S4, audits) are kept distinct from role/head commitment; inert-member wording now matches v1/v2 `UNSIGNED` and v14's "DR-103 … pass"; genesis statements are mutually consistent with D's P1→P2 sentence and with the head-publication barrier.

## 6. Limits
Prose plus one conditional model; I executed only that model, the owner's eight variants and my sixteen. Variant survival shows missing assertions, not defects in the modelled rule — in every surviving case the unmodified model behaves as the prose requires. Nothing here approves r7.
