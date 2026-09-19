# Independent bounded review — purge joins reference 142

Reviewer: Claude (actual independent reviewer; Codex remains implementation/decision owner). 2026-09-19.
Request: `purge142-20260919-REQUEST.md`. Scope: the delta of frozen `purge-joins-reference-checkpoint-142` over frozen
138 — corrections of my purge137 review: F-1 (completed-termination route), T-1 (six unpinned joins), N-1 (flag name)
and the N-2 wording. **Pure model** over supplied observations with synthetic execution ids; host store, spool,
rendering, deletion and generated consumers are separate. No frozen/selected edit; scratch copies only (`-I -B`,
0 stray `.pyc`); no commit, push or delegation; no cumulative approval.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 2,146,140 bytes, SHA-256 `bd600afbc26b4d87c93f4bcb6f7db8930c161024b252ca59f90ab8ee1f559711` = request and `archive-pin.json` |
| Members | 1,438/1,438 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Candidate pins | 1,287/1,287 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 138 extraction and its `frozen-candidate.json` |
| Changed | **10**, none added: workflow model (2 lines), `pin_budget_reference.py` (flag rename + docstring), `purge_checks`, two contracts, five pin files |

## 2. Owner checks, fresh scratch, required order
envelope → integration 423/0 → security 581 + 24 sweeps → carrier 435/0 → workflows **2,181/2,181** → foundation
231/231. All exit 0.

## 3. Evidence

**The model change is two lines**: where `run_invocation` takes a caller-supplied `termination` on a `completed`
observation, a termination whose `domainDetail.code` is `evidence.pinned` is refused (`PINNED_PURGE_OBSERVATION`).

**My complete 137 recheck re-run unchanged on 142** (`recheck.py`, both majors, ~40 assertions each): the **only**
result that differs from 137 is the one that should — *completed event carrying a pinned termination override*:
`ACCEPTED` → `refused`. Everything else (F-1 remedy, F-3 order, T-1.1–1.5, maxima 4,179,744 / 4,180,431, fallback
majors, the twelve runner joins, gate/cancel/retry behaviour, schema-valid aggregates) is identical.

**Guard probe** (`guard_probe.py`, both majors): full **and** bare pinned terminations on `completed` are refused; the
older routes stay refused (bare code on `rejected`, the detail on `operational-fault`); the lawful observation route
still works; and three **controls still pass** — a completed mutation with no termination, with an ordinary success
termination, and with *another* rejected detail — so the guard is specific, as the owner says, and did not break the
general termination-override feature. One shape slips through: N-1 below.

**Mutants.** My whole purge set carried forward — 28 from 131, 12 from 137, 4 new for 142 — against 142's mandatory
checker (in memory, no pin gate): 44 total, 1 harness error (an anchor 137 rewrote; not counted), **39 killed**,
**4 survived, all four previously shown equivalent** (the implied `old <= ceiling` disjunct; attached invocation and
two-step record, refused by the schema; the constructor's remedy check, refused by the schema `const`).
In particular **all six 137 T-1 joins are now killed by named, isolated checks**:

| 137 T-1 | 142 check that kills my mutant |
|---|---|
| (a) `errors == [detail]` (the kill-power regression) | `errors-detail-identity-v2` |
| (b) UTF-8 vs UTF-16 order | killed — `PINNED_PURGE_ORDER` raised inside the checker on the U+FF41 / U+1F600 pair |
| (c) replay key, wrong step | `runner-isolated-replay-step-v2` |
| (d) step kind (`store-gc`) | `runner-isolated-mutation-class-v2` |
| (e) envelope `projectId` | `runner-isolated-envelope-project-v2` |
| (f) opposite major, other joins consistent | `runner-isolated-major-v2` |

and the four new ones: guard removed; guard refusing only terminations that carry a disclosure (the *bare* case);
flag `true` on a first-publication identical set; the old flag name emitted as an alias — all killed.

**Flag.** `receiptRequired` → `pinInventoryChangeAdmitted`; no alias (the only remaining occurrence of the old name in
the tree is the check asserting its absence). Ordinary change → `ADMIT, true`; ordinary identical → `NOOP, false`;
first-publication identical → `ADMIT, false` — and the docstring and contract say this is a *proposed* delta admitted
by the law, not a committed fact and not a waiver of any publication receipt. That resolves my naming note: the name
no longer invites the inference the contract had to forbid.

**N-2 wording** executed (ceilings shrunk by patching constants): over-**byte** only, a rename to a shorter name that
is still over the ceiling → `ADMIT`; a kind change that lengthens the disclosure → `REFUSE evidence.pin-byte-limit`;
and (from 131/137) an over-**count** rename alone → refused. The clarified sentence matches the law; no new law or
ceiling.

## 4. Closure of purge137

| Item | Status |
|---|---|
| **F-1** completed-termination route yields an unjoined pinned aggregate | **Closed** for every JSON-shaped observation, full and bare, both majors — see N-1 for the one non-JSON shape |
| **T-1 (a)–(f)** six unpinned joins | **Closed** — each mutant dies on an isolated named check |
| **N-1** flag name | **Closed** — renamed, no alias, meaning stated |
| **N-2**, **N-3**, **N-4** | text accepted in 137; N-2 sentence now precise and matches execution |

## 5. Findings
- **N-1 (low) — the guard tests `type(x) is dict`.** A termination (or its `domainDetail`) that is a `dict`
  *subclass* passes the guard, and the runner again returns exit 2 with an `evidence.pinned` aggregate on a `completed`
  step, in both majors. Observations parsed from JSON are always plain dicts, so no fixture or product-shaped input
  reaches this; it is reachable only from Python callers that build observations by hand. It matters slightly because
  the guard exists precisely to make the statement "no route but the joined observation produces this termination"
  true of the runner. Either use `isinstance(..., dict)` in the guard, or — better, and in keeping with
  "structure is admitted before indexing" elsewhere in this model — refuse any supplied termination that is not a
  plain JSON object before looking inside it.

No other finding.

## 6. Bounded verdict
**142: reviewed, no blocking finding. purge137 F-1 and all six T-1 joins are closed: my 137 recheck changes in exactly
one place (the bypass is now refused, full and bare, both majors, with the three legitimate completed-termination
controls intact); my 44-mutant purge set leaves only the four known-equivalent survivors; the flag is renamed without
alias and its meaning is stated; the N-2 sentence matches execution. N-1 is a narrow type-test gap in the new guard.**
Not approval of host store, spool, renderers, deletion ordering, generated consumers, OS, release or any cumulative
standing.

Evidence: `claude-out/pin-verification.json`, `candidate-pins.json`, `diffs/`, `owner/`,
`probes/{recheck.py,recheck.json,recheck.log,guard_probe.py,guard-probe.json,mutation131set.py,extra137.py,mutation131set.json,mutation131set.log}`, `hashes.txt`.
