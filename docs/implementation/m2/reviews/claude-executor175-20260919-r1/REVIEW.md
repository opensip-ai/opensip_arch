# Independent bounded review — closed transition-executor set and non-executor barriers, 175 (reference)

Reviewer: Claude (actual independent reviewer; Codex remains owner). 2026-09-19.
Request: `executor175-20260919-REQUEST.md` (bytes as read: `claude-out/REQUEST-as-read.md`); README and the full delta
read against my verified 173. Scope: the delta of frozen `transition-executor-reference-checkpoint-175` over frozen 173
— four owner documents, five manifests, the pure observer and its checker. Host classification, custody, physical
retirement and the mapper remain owed; I infer none. Scratch only, `-I -B`; no frozen/selected/product edit, commit,
push or delegation; no cumulative approval. This report is scoped to 175 only (174 has its own report and NOTES).

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 2,177,368 bytes, SHA-256 `fdf18bff87664c5aa52d2ac7692ec6030ff5d8174267fe442f64ea42a3a9a569` = request = `archive-pin.json` |
| Members | 1,456/1,456 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified after all runs |
| Candidate pins | 1,289/1,289; nothing unpinned |
| Parent | `parent-inputs.json` = **my own** verified 173 extraction (1,289/1,289) |
| Changed | exactly the declared 11: `security-and-lifecycle.md`, `workflows-and-surfaces.md`, `commit-recovery-readonly.v3.md`, `identity-and-evidence.md`, five manifests, `readonly_transition_reference.py`, `readonly_transition_checks.v1.py`; 0 added |
| Python | 86 files, 84 byte-identical to 173; **`security_lifecycle_model_v1.py` and the 43 transition vectors byte-identical** |
| Lanes, fresh scratch | all seven exit 0; security 581 + 25 sweeps, `readonly-active-transition-admission` now 71 checks |

## 2. The mechanism (`probes/observer_probe.py` → `io/observer-probe.txt`)
My 173 oracle and corpus, unchanged, plus the new lane (`oracle_nonexec` = my oracle, with a *present* permit turned
into busy): **30,515 cases × both selectors: 0 mismatches, 0 exceptions, inputs never mutated, only `standing`
returned**; 40,000-case totality fuzz clean. `observe_for_nonexecuting_mutation` is a four-line delegate and is total
(it indexes the observation only after `observe` has proved it a 2-tuple).
Mutants (19): the owner's checker now kills **18** — including my 173 T-1 survivor (*intent laws not applied*, killed
by the new repaired-digest same-closure negative) and four new non-executor mutants (terminal still permits;
absence also blocked; unknown flattened to busy; only `DONE` blocks). The one survivor is the equivalent
set-comparison mutant. The 4,096 cap is gone (`not s` only) and a 4,097-scalar locator is pinned as admissible.
**173 T-1 and N-1: closed.**

## 3. Classification exhaustiveness, against the command owners (`probes/classify.py`)
I classified all 45 entries of `workflows/command-inventory.v3.json` and every name in the S7 lease table:
- **Executors.** The five commands are exactly the inventory's `authorizationClass: core-transition-leases` set and
  exactly the lease table's core-transition row. So "ordinary required authority" has an existing, closed owner, and
  any one of the five carries the same class — I had worried that authority for command X might not cover recovering
  a crashed operation Y; with one shared class that concern does not arise, but the text should say it (W-2).
- **Row 2 (other mutators).** `default`, `analyze`, `fit`, `audit`, `repair-verify`, `import`, the six
  `user-consent` mutations, `test-run`, `native-prepare`, `purge`, `store-gc` (hence the §4 settlement sweep),
  `repair-apply`, `repair-recover --apply-recovery`, component `install`/`update`, and the four mutating trust
  commands all fall here by the stated rule. No incidental installation mutation remains for any of them.
- **Row 3 / 4.** The nine query commands, `agent-serve` reads and `repair-recover` inspection are readers; `doctor`,
  `trust-doctor`, `store-status` are report-only, and the sentence "classified by that guarantee, even when its
  diagnostic implementation uses a project `SHARED-READ` lease" correctly settles `doctor`'s project checks.
- **Rule sites.** S7 item 4, the S9.2 heading rule, the S7 reader paragraph, the recovery owner, identity and the new
  workflows section now all state the five-command class; none of the 173 phrasings survives in the four changed
  owners. **173 F-1 (within those owners) and F-2: closed**, and the behaviour change for ordinary readers is now
  stated as deliberate in both the security and the workflow owner.

## 4. Findings
- **F-1 (low–medium) — a fifth owner still states the unconditional rule.**
  `docs/v2/architecture/store-instance-lineage.v1.json` l. 89 (unchanged, pinned): "`recover_transition_journal` is
  **the first act under the next fence, before any project admission**, from the durable footprint only." It is a
  normative architecture document for the very PS-01 lineage that 173/175 order *before retirement*. The same sentence
  also lives in the byte-identical model — comments, and the **emitted** `'recovery'` string of every
  `admit_transition_journal` result ("first act under the next fence acquisition, before any project admission"),
  which is an executable output a host could surface. The model being frozen is a fair reason to defer *that*; the
  lineage JSON is prose-class and should have moved with the other four. Same two-sites pattern as 169→171→173.
- **F-2 (low–medium, owner decision to make explicit) — row 2 also blocks SC-TRUST-only operations, which the
  retirement invariant does not need, and one class of executor depends on them.** The stated reason for the terminal
  barrier is that "a subsequent project **registration or mutation** must not leave the terminal active slot behind".
  `trust refresh|import|recovery-challenge|recovery-import` register nothing and touch no project store (contract:
  "Trust recovery deliberately takes no project lease: it mutates SC-TRUST only"), yet after a crashed transition they
  are refused until someone runs a core/store transition command. Two consequences worth stating: (i) **security
  freshness** — revocation/trust refresh is delayed behind an installation remedy; (ii) **partial circularity** — the
  two rollback executors need an S4 admitted time (`TRANSITION.NO_ADMITTED_TIME_CONTEXT`), and the operations that can
  restore one are exactly the blocked trust commands. It is not a deadlock: `core update` and `core repair` need no
  admitted time in the model, and `core repair` (same closure, affects no namespace) is always applicable, so the slot
  can always be cleared. But nothing says so. Either exempt SC-TRUST-only fence operations (at least past a coherent
  *terminal* journal), or keep the conservative rule and name `core repair` as the universal remedy and the freshness
  cost as accepted. I do not prefer one; the journal binds `platformProfileSetBodyDigest`, so there is an argument for
  keeping trust still while a nonterminal transition is pending.
- **W-1 (low) — "exhaustive" omits entries that take no fence.** `help`, `version`, `completion` (inventory
  `requestClass: meta`) fit none of the four rows. One clause — entries that acquire neither fence nor lease are outside
  the table — makes the word true.
- **W-2 (low)** Say that the five executors share one authorization class (`core-transition-leases`) and that an
  invocation admitted for its own operation executes recovery of *whatever* operation was journaled; "a missing or
  mismatched authorization refuses under its existing owner" otherwise invites the reading that a `core repair`
  cannot clear a crashed `store migrate`.
- **W-3 (low)** Two inventoried commands change row with their mode (`repair-recover` with/without
  `--apply-recovery`; `doctor` with/without project checks). The text handles `doctor`; add that classification is per
  invocation mode, so "the user cannot select a role flag" is not read as contradicting `--apply-recovery` (which
  selects mutator versus reader, never executor).
- **N-1 (note)** Remedy ergonomics: with no dedicated command, clearing a crashed transition means *running a
  transition*. `core repair` is the least invasive; "blocked output may identify that existing remedy" is the right
  hook, and the workflow owner could name it.
- **N-2 (note)** As the request says, the checker is hand expectations over a shared fixture, not an independent
  oracle; mine agrees with it on every case.

## 5. Closure
| My 173 item | Status |
|---|---|
| **F-1** rule sites narrower than the paragraph | **Closed in the four changed owners**; one further site found (F-1 above) |
| **F-2** executor set a predicate without extension; `APPEND-WRITE` unclassified | **Closed** — closed five-command set equal to an existing authorization class; explicit barrier for every other mutator |
| **T-1** intent-law step masked | **Closed** — repaired-digest negative; my mutant killed |
| **N-1** unowned 4,096 locator cap | **Closed** — removed and pinned |

## 6. Bounded verdict
**175: reviewed, no blocking finding. The executor set is now closed, identical to the inventory's existing
`core-transition-leases` authorization class and to the lease table's core-transition row; all 45 inventoried commands
classify into exactly one row (three meta commands take no fence and should be named as outside); every other mutator
requires active-slot absence, every project reader uses the reader barrier, report-only surfaces write nothing, and
the change for ordinary readers is stated as deliberate in the security and workflow owners. The pure selectors equal
my independent oracle on 30,515 cases in both lanes, are total, and the owner's checker now kills 18 of my 19 mutants
(the other is equivalent), including the 173 survivor. F-1: `store-instance-lineage.v1.json` — and the frozen model's
emitted `recovery` string — still state the unconditional next-fence rule. F-2: blocking SC-TRUST-only operations is
not required by the stated invariant, delays trust refresh behind an installation remedy, and leaves the rollback
executors dependent on operations the barrier blocks; `core repair` always remains available, which the text should
say, or the trust operations should be exempted.** Not approval of host classification, custody, physical retirement,
a mapper (none exists), or any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `candidate-pins.json`, `diffs/` (six),
`owner/` (seven lanes + `exits.txt`), `probes/{lanes.sh, observer_probe.py, classify.py}`,
`io/{observer-probe.txt, observer-probe.json}`, `hashes.txt`.
