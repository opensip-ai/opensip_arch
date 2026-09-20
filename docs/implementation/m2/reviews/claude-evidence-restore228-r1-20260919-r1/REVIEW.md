# Bounded review — frozen INCOMPLETE evidence-restore owner 228 r1

Reviewer: Claude. Date 2026-09-19. **228 only; directional owner plus a conditional model; not cumulative or implementation approval; no candidate/product/repo edit, commit or push.** I supplied source analysis that this proposal follows; that is not acceptance, and I checked the frozen text against the pinned sources independently. My 227 author draft is not discussed. Named unmet format obligations are not repeated as findings.

## 1. Identity and what I ran
- `subject.tar.xz` SHA-256 `6bfaae15444f774feee62aa1798417b4f500e4e4a4f52e128cf7de25a6c99310`, 256,592 bytes, 46 members — equals the request; **all member pins verified from the tar before extraction**; 0 non-regular/unsafe/extra; end pass `re-verified`.
- Pinned copies `kernel201.py`, `identity-and-evidence.md`, `security-and-lifecycle.md`, `workflows-and-surfaces.md` are byte-equal to my own verified 201 extraction; the 201 pins equal the repo trial; the kernel the model imports from the T path hashes to the pinned `df45c9c5…2299`.
- `restore_model.py` re-run = `restore-model-r2.json` (**32 cases**); `mutants-r1/baseline.py` = model; **report-named variants only** (guarded runner): 9/9 rejected with exact predeclared labels, baseline passes. Five variants of my own (`claude-out/probes/my_variants.py`).

## 2. My source recommendations as adopted — checked
| Topic | RESTORE.md | Verdict |
|---|---|---|
| Guarded maintenance, no SEAL | "must not call prepare_commit, mint a PublishedCommit, append an authoritative Run manifest/commit-receipt/SEAL, or give the mutation step an authoritative invocation Run link … result type must not be convertible to a committed Run capability" | consistent with workflows §1 (only analysis/verify seal or link) and build plan l.84–90 |
| Per-admission provenance | imported record keyed by RunId + origin bundle + **the actual local admission ExecutionId**; no RunId-global bit; local commit neither demoted nor strengthened | correct, and **better than my (RunId, originSeal) key** — two independently authorized admissions of one bundle are distinct acts |
| Replay-scope idempotence | "Same-scope completed receipt replay follows workflow mutation idempotence and creates no second effect" | consistent with `MutationReplayScopeV1`; model: completed scope returns `delivery-replay`, a changed input under the same execution is `scope-conflict` |
| Retention root / GC / budgets | explicit new root, counted in budgets and census; "imported-only presence is not a sealed Run availability row" | correct |
| Purge | releases every imported root for the RunId in the project with the local Run's evidence, keeps provenance/tombstone, respects independent pins and shared objects; imported-only must be purgeable | coherent; it **goes beyond my note deliberately** (I had left it unowned) |
| Re-export | closed `inventorySource` union covering local-commit **and** imported-only; "do not quietly omit" | correct; supersedes my "initially local only" |
| Clock non-interference | no bundle-supplied time source; F/anchor and clock-driven role events allowed; compare "at the SAME reached admission boundary" | correct and sharper than my wording: an earlier parse refusal lawfully reaches no clock evaluation |
| Inert receipts | inventory includes stage receipts / import2 wrappers / provenance when they are replay dependencies; exclusions "by admitted record role, not filename" | correct |
| Barrier class | "any present active transition, including a coherent terminal slot, prevents the mutation" | matches S9.2.1's row for "every other mutating entry … including coherent `DONE`/`ABORTED`", and that section's rule that a new command needs an explicit category |
| S9.3 clarification, project identity, no fresh-S | as reconciled | consistent |

## 3. Findings

### E-1 (Medium) — imported-evidence publication has no revocation linearization; the commit facade it bypasses is where that lives
**[E]** build plan, commit sequence step 5: "Under the journal checkpoint, security checks current custody, relevant trust epoch, observer freshness, grants and operation cancellation. **The final SEAL/commit sequence must linearize with REV: no new SEAL or commit after REV.**" Path B (correctly) never calls `prepare_commit`, so it inherits none of this. Replay of a bundle can be long; the fence is not held across it (S7: a lease holder cannot wait for or hold the fence), and a concurrent fence-only `trust import` can revoke the producing closure meanwhile. As written, RESTORE requires "its own admitted installation/project/store/session/fence/lease" but names no **publication-time** recheck, so evidence verified "under current trust" can be published after that trust was revoked. **[P]:** the maintenance publication (objects already staged; record + retention root) takes the same short final checkpoint: re-check custody, trust epoch/observer freshness for every closure the replay relied on, and cancellation; "no imported-evidence publication after REV" joins the existing rule. Say also which journal record, if any, the maintenance operation appends, because REV linearization is defined through the journal checkpoint.

### E-2 (Low–Medium) — S7 ordering of the host-owned trust writes is not stated
**[E]** S7 laws: "no lease without the fence; no waiting for a lease; no waiting for the fence while holding a lease …; **trust state is written only under the fence and never under a lease**". RESTORE says "Global fence precedes project locks" and that S4 write-ahead and clock-driven role events may occur, but not *when*. They must complete — including 222's successor check, durability reconfirmation and the clock revision — **before** the APPEND-WRITE (export pins, restore) or EXCLUSIVE (purge) lease is acquired; nothing under `I/trust` may be written while the lease is held, so a trust change needed mid-operation is a refusal, not a late write. One sentence; the model's single `host_clock()` call is already in that position.

### E-3 (Low–Medium) — model: four meaningful variants survive
`io/my-variants.json` (a fifth, `v7`, was a no-op of mine and is discounted):
- `v5` **hash-only restore when a local commit exists** — RESTORE: "only after full matching replay"; the replay-refusal case uses a fresh store only.
- `v6` **purge releases only the first imported admission's root** — every purge case has a single admission; RESTORE requires "all applicable imported evidence retention roots".
- `v4` **export still lists purged imported roots** — export is asserted only before any purge.
- `v3` **delivery replay re-runs the S4 evaluation** — survives because the model's wall is constant; with a later wall it would write F on a path RESTORE says "creates no second effect". Use two observations.
Add one case each; all four are one-line assertions.

### E-4 (Low) — restoring a purged local Run revives authority; say so
Model `restore-local-availability`: after `purge --revoke-pins`, a later restore returns the Run to `retained` and `authority()` becomes true again (pins stay revoked). That follows inherited law (identity l.1748–1752: availability states include `purged` and "may improve through verified restoration"), but purge's disclosed consequence `dependent-evidence-replay-unavailable` is thereby reversible by an explicit restore. State it in RESTORE.md so it is a rule, not a model artefact — and note that for an **imported-only** RunId a post-purge restore creates a new admission record rather than "un-purging" the old one (the model already does this).

## 4. Source/project boundary and grant/commit law — no contradiction found
Origin ProjectId must equal the admitted target; adoption is separate request data with its own first-registration law; no bundle member reaches trust, journals, witnesses, selection, lineage or registry (model: six foreign operational roles refused with nothing written, while `semantic-grant-projection` — a semantic identity input — travels inertly, which is the right line against identity l.536–540). Local commitment stays exclusively with analysis/verify attempts; the model's `seal-boundary` case and `permit-restore-seal` variant hold it.

## 5. Limits
Prose and one conditional model in which replay validity, current trust, sessions, leases and atomic record+root publication are asserted strings/booleans; the S4 arithmetic alone is real (pinned kernel). I executed the model, the nine report-named variants and five of my own, inside my review directory. No bundle, record, registry, adoption, retention, pin-disclosure or native transaction format exists to review. Nothing here approves 228.

## 6. Result
**The direction is consistent with the pinned sources and with the original grant/commit law. One Medium gap (E-1: publication-time revocation linearization for the path that bypasses the commit facade), one ordering sentence owed (E-2), four model coverage gaps (E-3), one consequence to state (E-4).**
