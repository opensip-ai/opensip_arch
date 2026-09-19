# Independent bounded review — purge subclass reference 145

Reviewer: Claude (actual independent reviewer; Codex remains implementation/decision owner). 2026-09-19.
Request: `purge145-20260919-REQUEST.md`. Scope: the delta of frozen `purge-subclass-reference-checkpoint-145` over
frozen 142 — the correction of my purge142 N-1 (the completed-termination guard tested `type(x) is dict`). The owner
states this is **not** admission of arbitrary Python behaviour or full observation-shape validation; normal JSON stays
the same. Host pin store, spool, render, deletion and generated consumers remain separate. No frozen/selected edit;
scratch only, `-I -B`, 0 stray `.pyc`; no commit, push or delegation; no cumulative approval.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 2,061,588 bytes, SHA-256 `88558098c030aaefee3bd5afb2ca247e1f4f357d245cbbd63cc7881472891e59` = request and `archive-pin.json` |
| Members | 1,365/1,365 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Candidate pins | 1,287/1,287 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 142 extraction and its `frozen-candidate.json` |
| Changed | **7**: `workflows_model.v1.py` (one line), `purge_checks.v1.py` (nine lines), five source-pin files |

## 2. Owner checks — all seven lanes, fresh scratch
envelope → integration 423/0 → security 581 + 24 sweeps → carrier 435/0 → workflows **2,193/2,193** → foundation
231/231 → native 477 + 66. All exit 0.

## 3. Evidence
**The model change is one expression:** `type(term) is dict and type(term.get('domainDetail')) is dict` →
`isinstance(term, dict) and isinstance(term.get('domainDetail'), dict)`.

**My 142 guard probe re-run on 145** (`guard_probe.py`, both majors): the two rows that slipped through 142 — a
`dict` **subclass** termination, and a subclass `domainDetail` — are now **refused** (`PINNED_PURGE_OBSERVATION`), as
is an `OrderedDict`; full and bare plain-dict terminations stay refused; the three legitimate completed-termination
controls still pass; the older `rejected` and `operational-fault` routes stay refused; the lawful observation route
works.

**No other behaviour moved:** my complete 137/142 recheck (both majors, ~40 assertions each, including maxima and
every runner join) produces a result file **identical to 142's**.

**Regression kill power.** My whole purge mutant set carried forward (28 + 12 + 4) plus two for 145 — each half of the
type test reverted separately. Against 145's mandatory checker (377 purge checks): both reverted-type mutants are
**killed by the new subclass checks** (`…-termTrue-detailFalse`, `…-termFalse-detailTrue`), so each half is pinned
independently, as the owner says; guard-removed is killed (re-run separately — its anchor in my carried-forward file
was stale, recorded as a harness error and not counted); 40 of the remaining 44 are killed; the 4 survivors are the
same four shown equivalent in 137/142 (implied disjunct; two refused by the schema; constructor remedy refused by the
schema `const`).

## 4. Closure
| Item | Status |
|---|---|
| purge142 **N-1** — guard tested `type(x) is dict`, so a dict subclass slipped through | **Closed as stated**: subclasses of `dict` at either level, and both, full and bare, both majors |

## 5. Note
- **N-1 (low, residual of the same narrow class).** In 142 I offered two fixes: `isinstance`, or — "better" — refusing
  any supplied termination that is not a plain JSON object before looking inside it. 145 takes the first. A mapping
  that is **not** a `dict` still passes the guard: `collections.UserDict` (at either level) and
  `types.MappingProxyType` each make `run_invocation` return exit 2 with an `evidence.pinned` aggregate on a
  `completed` step, in both majors (`guard-probe.json`). This is reachable only from hand-built Python observations,
  never from parsed JSON, and the owner explicitly disclaims arbitrary Python behaviour — so I record it as the
  boundary of the claim, not as a failure of 145. If the sentence "no route but the joined observation produces this
  termination" is ever meant literally of the runner, the structural check (exact `dict` of JSON scalars/containers,
  refused otherwise) is what makes it true; the type test can only ever enumerate.

## 6. Bounded verdict
**145: reviewed, no finding against the delta. purge142 N-1 is closed as stated — dict subclasses at the termination
level, the detail level and both are refused, full and bare, in both majors; each half of the type test is pinned by
its own regression; nothing else moved (my full recheck is identical to 142; all seven owner lanes pass). The residual
is non-`dict` mappings from hand-built Python observations, which the owner places outside the claim.** Not approval of
host pin store, spool, renderers, deletion ordering, generated consumers, OS, release or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `candidate-pins.json`, `diffs/`, `owner/`,
`probes/{guard_probe.py,guard-probe.json,guard-probe.log,recheck.py,recheck.json,mutation131set.py,extra137.py,mutation131set.json,mutation131set.log,guard-removed-rerun.json}`, `hashes.txt`.
