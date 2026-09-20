# Bounded critique — incomplete WIP215 revision 6 (closure of my r5 F-1..F-7)

Reviewer: Claude. Date 2026-09-19. **Assistance on an incomplete owner; no approval, no protocol acceptance, no source edits, commit or push.** Root remains owner. Known owed work (capsule, commands, creator, restore, complete model, the separate 222 supplement) is not rediscovered.

## 1. Identity
- `subject.tar.xz` SHA-256 `29e27c4bbb5dfc4fe13766216b0013001243b047641ebbba758906487ec22757`, 106,720 bytes, 58 members — equals the request; all members hashed from the tar before extraction; 0 non-regular/unsafe/extra; end pass `re-verified`.
- `beforeimages-r6/OWNER.md` is byte-equal to the r5 `OWNER.md` I reviewed; `schema.json` and `payload-schema.v2.json` are byte-equal to r5. `OWNER.md` 129 → 135 lines; I read every changed paragraph (C BEGIN/ABORT/acceptedUnder, C.1, C.2, all of C.3, D evaluated-phase and P-transitions).
- Model: `ordinary_batch_model.py` re-run by me reproduces `ordinary-batch-model-r2.json` exactly (6272 / 966 / 4010); `coordination-mutants-r1/baseline.py` is byte-equal to the model; the three owner variants each fail an assertion when I run them. Retained law re-read: v14 `039a5702…`, v1 §3.1/§4.1, v1/v2 DR-103 rows.

## 2. Closure of r5 findings
| r5 | r6 text | Status |
|---|---|---|
| F-1 uncloseable all-interrupted batch | last RECOVERY exit publishes private `INTERRUPTED` batch-termination in the same revision, clears staging; operator ABORT also carries one; no fabricated per-role ABORT | **closed in prose**; model evidence is definitional — see G-2 |
| F-2 key loss vetoes its own list | tentative REVOKE then availability; below-threshold leaves T0 with its actual v14 outcome (QUORUM-LOST transition/stay, or UNBOOTSTRAPPED accepted stay); "not every role trusted" | **closed** |
| F-3 relied-on scope / signer-role state | shared members authenticate in the prospective frame regardless of signer state; revoked prospective shared subjects or insufficient shared keys veto; excluded-role members inert | **closed**, one precision (G-5) |
| F-4 v14 outcome/audit conflict | explicit `importCompleteness` conjunct; refused PRESENT per T0; tentative observations never dispatched on failure | **closed for ordinary import**; the same conflict remains for batch BEGIN/COMMIT — **G-1** |
| F-5 REVOKE frame in RECOVERY | OLD subjects only; prospective hits block COMMIT; never-established REVOKED declared unreachable with a must-refuse fixture | **closed** |
| F-6 batch born interrupted | BEGIN availability guard, `RECOVERY-BEGIN-REFUSED` | **closed** (subject to G-1) |
| F-7 missing-proof exit | dependent defined; diagnostics, ABORT/termination and retained-phase S4.5 not dependent; refused-import witness closure retained and bounded; proof-only roots never heads | **closed**, one wording item (G-6) |

## 3. New findings

### G-1 (Medium) — batch BEGIN and COMMIT have the conflict F-4 had; only ordinary import received the conjunct
**[E]** v14: `EV-RECOVER-BEGIN` fires for a role when "ceremony inputs are present" and the state is allowed; `EV-RECOVER-COMMIT` fires when `recoveryTrustedEntry` holds, "Else stay RECOVERY and refuse"; every attempted event is audited; a member whose guard holds is `accepted`.
r6: BEGIN refuses the whole derived batch if **any** member's prospective availability is below threshold (it "cannot omit an applicable listed role"); COMMIT: "Any refusal commits no role/head". A sibling whose own guard holds is therefore refused — without a guard conjunct that makes that refusal lawful, and r6 does not say which batch members receive the refused `RECOVERY-BEGIN-REFUSED` / `RECOVERY-COMMIT-REFUSED` audit.
**[P] one rule:** add `batchCompleteness` to the `EV-RECOVER-BEGIN` and `EV-RECOVER-COMMIT` members — *every member of the derived (BEGIN) / bound (COMMIT) batch satisfies its remaining conjuncts for this exact binding* — and state, as C.3 now does, that on failure **every** batch member is dispatched, refused with the existing fallback reason, state unchanged, audited; nothing else is published. v14's `whenInactive` still precedes it (see G-4).

### G-2 (Medium) — the model does not yet test three of the invariants it is cited for
My eleven variants of the frozen model (`claude-out/probes/model_mutants.py`, results `io/model-mutants.json`): 8 rejected, **3 survive**:
- `h` — **an ordinary import heals a `RECOVERY` member to `TRUSTED`** (`ENTRY` no longer excludes RECOVERY). This is the half-updated-ceremony case the text forbids; no assertion covers it (the matching `REVOKED` variant `g` is rejected only because of the explicit `REVOKED` stays assertion).
- `a` — on success **no target becomes `TRUSTED`**. The success branch asserts only `REVOKED` preservation and `below ⇒ not TRUSTED`.
- `b` — key loss moves only `TRUSTED` to `QUORUM-LOST`; `EXPIRED`/`STALE-REVOCATION` stay put. The single F-2 case uses `TRUSTED`.
Separately, the **4010 interruption edges assert a definition against itself**: `terminated = 'RECOVERY' not in after` is checked with `terminated == all(s != 'RECOVERY' …)`, and the follow-up assertion restates it. The owner variant `all-interrupted-batch-remains-live` is rejected only because it edits that one expression. This is the same kind of row as the 126 BEGIN tautologies root already removed; the count should not be cited as verification of F-1.
**[P] bounded correction:** (i) replace the success assertions with an **exact expected final state per role** from an independent table of v14 rows (state × hit × below × in-T1 → state), so every cell is compared, not three properties; (ii) give the batch model a separate `barrier` flag updated by the *producer rule* and check, over event **sequences** (interrupt / abort / same-head import), the invariant `barrier ⇔ some member in RECOVERY` and "barrier cleared ⇒ BEGIN and head-advance applicable"; (iii) encode `below[BUNDLE] or below[INDEX] ⇒ not authenticated` so the enumerated cells are reachable ones (G-3).

### G-3 (Low–Medium) — "P1→P2 without any TRUSTED role" is unreachable under r6's own rules; the permissive sentence should become a tested theorem
r6: "Metadata bootstrap can reach P2 even if no role enters TRUSTED". But before any accepted head nothing is established, so OLD-subject REVOKE removes no one; T0 empty would need every active role in `RECOVERY`, where the barrier refuses; and **TR-BUNDLE and TR-INDEX cannot leave T0 by key loss**, because availability below threshold makes the manifest/catalog signature threshold unmeetable, which r6 (correctly) makes a shared veto. Hence every *accepted* genesis import has BUNDLE and INDEX in T1, and they become `TRUSTED` or the import refuses. (A genesis by recovery COMMIT makes its selected roles `TRUSTED`.) The true general statements are: *post-genesis, positive counters do not imply a trusted role* (all targets may be revoked later), and *a shared-signer role leaves T0 only by OLD-subject REVOKE, never by key loss*. **[P]:** replace the sentence with those two, and add "accepted P1→P2 ⇒ BUNDLE and INDEX TRUSTED" as a model assertion, so no implementation grows an untested head-without-any-role genesis path.

### G-4 (Low) — three exactness points in the `importCompleteness` paragraph
- "every T0 ordinary PRESENT **that is dispatched**" hedges; the model dispatches all of T0. Say *all T0*.
- T0∖T1 on **success** is unstated: those roles take their named REVOKE/QUORUM event and **no** PRESENT (their exclusion is a producer applicability decision made before dispatch, like roles outside T0). On failure they are ordinary T0 members with a false guard. Both are coherent; write both.
- **[E]** v14 `evaluationOrder` puts `whenInactive` (`ENVELOPE-INACTIVE`) before any active branch. `importCompleteness` is "a required conjunct other than envelope standing"; it must not turn an inactive-entry refusal into `PAYLOAD-NOT-ADMISSIBLE`.

### G-5 (Low) — inert members versus v14's "Payload complete; DR-103 UNSIGNED/DIGEST_MISMATCH pass"
Checked against retained sources: **[E]** v1 "Envelope absent where policy requires one → `RJ-4 UNSIGNED`"; v2 "`envelope-malformed` | empty `signatures`; step 1 → UNSIGNED"; v14 keeps these byte-level checks distinct from DR-112 envelope verification. So there is no conflict **if** inert members still pass both byte-level checks: envelope present, well-formed, non-empty `signatures`, digest joined. What role-scoping may waive is only the DR-112 half (key/threshold/namespace verification). r6's "present, shape-valid and byte/digest-bound" should say this in those terms, so that "inert" can never be implemented as "envelope optional".

### G-6 (Low) — missing-T operations
"safe ABORT" has no definition; delete "safe" or define it. State that ABORT under a missing `T` evaluates still-true causes with `tEval = max(wall, F, L)` using F/L **as numbers**, may advance F, and never writes L or `T`. S4.5's operation-scoped inputs (R, pending challenge, current accepted head's recovery authority via its retained admission chain, retained revocation history) are complete as listed and need no full trust grant.

## 4. Requested cross-rule checks with no finding
- **Discarded tentative observations vs refused PRESENT audits:** consistent. On failure nothing tentative is recorded, so an about-to-be-revoked T0 role is truthfully a target whose guard was false; the next successful import dispatches its REVOKE. The S4 revision stands in both cases; shared *authentication* failure stays pre-dispatch/no-write, shared *guard* failure at `tEval` is post-write with T0 audits (the model agrees: no clock/no events vs clock + T0 events; T0-empty gives no role events).
- **Never-established key loss does not fabricate REVOKED:** text and model agree (my variant `c` is rejected); QUORUM-LOST from `RECOVERY` via the prospective context and UNBOOTSTRAPPED accepted stay are the only outcomes.
- **Last interruption terminates automatically:** prose is complete, including the same-head import path ("any required reset or batch termination in ONE outcome revision"). Evidence: G-2.
- **Typed-absent:** no availability observation; REVOKED never reset. Consistent.

## 5. Retained-law amendments now on the table
`importCompleteness` (r6, explicit) · `batchCompleteness` for BEGIN/COMMIT (**G-1, new**) · BEGIN availability guard (r6) · prospective availability in RECOVERY (v1 §4.1) · `EV-REVOKE` from established-reset UNBOOTSTRAPPED (kernel/reference successor) · audit dispatch boundary (v14 `auditAndWaiver`). Producer-only, no v14 change: OLD-only REVOKE frame in RECOVERY, tentative ordering, inert-member scope (reference **reader** change), private batch termination and standing reset.

## 6. Limits
Prose and a small conditional model; I executed only that model, its three owner variants and my eleven. Reachability arguments (G-3) are from r6's stated rules and v14's named rows, not from a complete machine. Corrections are single bounded rules, not the only lawful ones. Nothing here approves r6.
