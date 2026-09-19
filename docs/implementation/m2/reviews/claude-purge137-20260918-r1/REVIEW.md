# Independent bounded review — purge follow-ups reference 137

Reviewer: Claude (actual independent reviewer; Codex remains implementation/decision owner). 2026-09-18/19.
Request: `purge137-20260918-REQUEST.md`. Scope: the delta of frozen `purge-followups-reference-checkpoint-137` over
frozen 133 — the corrections of my purge131 review (F-1, T-1 ×5, F-2, F-3) and the contract clarifications N-1..N-4,
which the owner asks me to scrutinise rather than accept. **Pure model over supplied observations**: no storage,
spool, rendering, deletion or authority. Clock 133 findings are corrected separately (138). No frozen/selected edit;
scratch copies only (`-I -B`, 0 stray `.pyc`); no commit, push or delegation; no cumulative approval.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 2,157,024 bytes, SHA-256 `2877783b6817781380c86a7b0f27675fb1ceab3832e822244e5b9bb90f5609d1` = request and `archive-pin.json` |
| Members | 1,464/1,464 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Candidate pins | 1,287/1,287 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 133 extraction and its `frozen-candidate.json` (1,287/1,287) |
| Changed | **13**, none added: workflow model, `purge_checks`, four schemas (`common` and `command-inventory` × 2 majors), two contracts, five pin files |

## 2. Owner checks, fresh scratch, required order
envelope → integration 423/0 → security 581 + 24 sweeps → carrier 435/0 → workflows **2,159/2,159** → foundation
231/231. All exit 0. Owner mutants: r1 shows the disclosed survivor (`runner-request-join`), r2 shows all 13 detected.

## 3. Recheck of my 131 findings, both majors (`probes/recheck.py`; identical results in legacy 2/1 and evaluator3 3/3)

| 131 item | 137 | Evidence |
|---|---|---|
| **F-1** remedy of the pinned refusal not pinned | **Closed** | constructor refuses any other remedy; validator refuses a false remedy in both copies *and* the fixed remedy plus one trailing space (schema `const` in both majors); my 131 false-remedy mutant is now killed |
| **T-1.1** validator's own budget re-check | **Closed** | hand-built envelope one byte over the ceiling refused; owner mutant killed |
| **T-1.2** subject = RunId | **Closed** | refused; my mutant now killed |
| **T-1.3** aggregate = step termination | **Closed** | refused; my mutant now killed |
| **T-1.4** fallback major for a legacy invocation | **Closed** | invocation major 1 → fallback major 2; major 3 → 3; 996 bytes; my mutant now killed |
| **T-1.5** per-code pin-limit remedies | **Closed** | three distinct remedies; my mutant now killed |
| **F-3** declared order not enforced | **Closed, with one gap (T-1 below)** | identically unsorted copies refused `PINNED_PURGE_ORDER`; constructor orders non-ASCII correctly |
| **F-2** general runner could not produce the refusal | **Substantially closed; see F-1 and T-1 below** | through `run_invocation` the one-step record is **canonically byte-equal** to the closed constructor's record and passes the closed validator; observation and result are independent copies; bare code without an envelope, an envelope on a non-rejected event, an extra member, another request, another Run, another project context, no context at all, another replay key, a non-purge mutation step, the other major and a retry policy are each refused; with an explicit render step, gate `terminal` → render runs, `completed` → skipped, both aggregate to `request-rejected`/2 with the projection on the step, the records are **schema-valid** and serialise; SIGINT before render → 130 with a schema-valid record; SIGINT before purge → cancelled, no projection |
| N-5 aliasing; empty inventory label | **Closed** | `errors[0]` is no longer the same object as `termination.domainDetail`; empty inventory → `PIN_INVENTORY_EMPTY` |

New maxima with the fixed remedy, reproduced independently: **direct 4,179,744; one-step 4,180,431** with
`terminationEmitted:true` (the owner's 4,180,432 is the `false` spelling) — 14 KB of headroom against 4,194,304;
ceilings and reserve unchanged.

(My first run reported every two-step record schema-invalid: I had omitted three required render parameters, so a
*success* control was invalid too. Probe error; corrected, r1 output kept.)

## 4. Mutants
My 28 mutants of 131 re-run unchanged, plus 12 new ones for 137 (`mutation131set.py`, `extra137.py`; owner's mandatory
checker in memory, no pin gate; first attempt died on a quoting error of mine — log kept). 40 total: 1 harness error
(an anchor 137 rewrote; not counted), **29 killed**, **10 survived**. Every survivor then got an isolating
counterexample on original vs mutant (`survivors.py`; its first run aborted informatively — see T-1(b)):
4 are **equivalent** (the implied `old <= ceiling` disjunct; the constructor's remedy check, because the schema
`const` refuses the same input; the two-step record and the attached invocation, refused by the schema), and **6 are
unpinned** — T-1.

## 5. Findings

- **F-1 (low–medium) — "no bare code can produce that termination now" is not true of the runner.**
  `run_invocation` still honours a caller-supplied `termination` on a **`completed`** observation, and that path does
  not go through the new observation route. A `completed` event carrying a pinned termination — with the full
  disclosure, or with nothing but the bare `evidence.pinned` detail, subject and remedy — is **accepted**: the runner
  returns exit 2, a `completed` StepResult and an aggregate whose detail is `evidence.pinned`, with no projection and
  no join to request, Run, project or replay scope (`probes/debug-f2.json`). The resulting record is schema-invalid and
  the closed validator refuses it, so a consumer that validates is protected; but the runner itself neither refuses
  nor validates, and the claim in the README/contract is about the runner. One guard where `obs.get('termination')` is
  taken — refuse any termination whose detail is `evidence.pinned` outside the observation route — closes it.
- **T-1 (medium as a set) — six joins the mandatory checker does not pin** (`survivors.json`; original refuses,
  mutant accepts, 2,159 checks silent):
  (a) **`errors == [termination.domainDetail]`** in the direct validator — a *regression in kill power*: on 131 this
  mutant was killed (`error-detail-equality`); on 137 an envelope whose `errors` copy names another pin is accepted by
  the mutant and no check notices. Most likely the old check relied on the aliasing that 137 rightly removed.
  (b) **UTF-8 versus UTF-16 order.** The validator sorted by UTF-16 code units passes every check; it then accepts
  `[U+1F600, U+FF41]` (wrong by the contract) and — this is what aborted my first survivor run — *refuses the
  constructor's own correctly ordered output* for such names. The two orders differ exactly when a supplementary
  character meets U+E000–U+FFFF; one such pair in the order test pins it, and it matters for the Rust/TypeScript
  consumers, where UTF-16 order is the default mistake.
  (c)–(f) four of the runner's observation joins: **replay key** (right request, project and class, wrong step id),
  **step kind** (the observation offered to a `store-gc` mutation that keeps the purge key and target), **envelope
  `projectId`** versus the admitted context, and **major** (a major-3 record whose purge step targets a `run2:` id with
  a major-2 envelope). The owner's r1→r2 history shows the same effect for the request join — joins masking one
  another — and fixed that one; these four need the same treatment: each negative case must violate exactly one join.
- **N-1 (note, the owner asked for scrutiny of N-3) — agreed, with one request.** "`receiptRequired` describes only
  the pin-inventory delta; import/restore owe their own publication receipts; `ADMIT` on an identical source/result is
  not a publication no-op" is a sound separation, and the text now says what `before` may be on a first publication.
  The model still returns two spellings for one fact (`ADMIT, receiptRequired:false` with the flag, `NOOP` without).
  That is harmless given the text, but the name `receiptRequired` will be read by an executor author as "no receipt
  needed"; renaming it in the reference (e.g. `pinInventoryChanged`) would make the contract sentence unnecessary.
- **N-2 (note) — agreed.** The complete-result law is now stated as authoritative, including create-within-a-reducing
  batch; my 131 walk (9→8→7→6, each batch creating a pin) is lawful by text. The remaining consequence worth stating
  to users: an over-limit inventory can be *renamed into shape* only by pairing each rename with a release.
- **N-3 (note) — agreed.** Malformed inventory blocks ordinary mutation including release; restoration via the owner;
  "never delete or truncate malformed evidence to make the inventory appear valid" is the right sentence. It is a
  no-path state like 127 C-3; the restoration owner does not exist yet.
- **N-4 (note)** one-step purge rationale now sits in both `command-inventory` schemas — sufficient.

## 6. Unresolved limits
Pure functions over supplied observations. Execution ids are synthetic; delivery facts, atomic storage, spool, renderer
and deletion ordering are host obligations stated in text. Generated consumers are not refreshed. 133's clock findings
are unchanged in this tree.

## 7. Bounded verdict
**137: reviewed, no blocking finding. All eight items of my 131 review are corrected in both schema majors — the false
deletion remedy is refused by constructor, validator and schema; the five joins refuse; order is enforced; the general
runner now produces a record byte-equal to the closed form and obeys the gate, cancellation and no-retry laws with
schema-valid aggregates; the new maxima reproduce. Two things remain: F-1 (a `completed` observation with a supplied
termination still yields an unjoined `evidence.pinned` aggregate from the runner, contrary to the stated claim) and
T-1 (six unpinned joins, one of them a kill-power regression and one the UTF-8/UTF-16 order).** Not approval of
storage, spool, renderers, deletion ordering, generated consumers, OS, release or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `candidate-pins.json`, `diffs/`, `owner/`,
`probes/{recheck.py,recheck.json,recheck.r1-render-params-incomplete.json,recheck.log,debug_f2.py,debug-f2.json,mutation131set.py,mutation131set.failed-r1.py,mutation131set.FAILED-r1.log,extra137.py,mutation131set.json,mutation131set.log,survivors.py,survivors.json,survivors.log,survivors.FAILED-r1.log}`, `hashes.txt`.
