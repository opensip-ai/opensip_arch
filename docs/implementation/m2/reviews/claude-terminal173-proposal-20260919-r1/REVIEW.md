# Proposal assistance — terminal installation-journal admission (towards a 173 correction)

Author: Claude (independent reviewer). 2026-09-19. **This is proposal assistance, not approval and not a review of
frozen bytes.** Codex authors, tests and freezes any correction; I then review those bytes. I edited nothing. Request:
`terminal173-proposal-REQUEST.md` (bytes as read: `claude-out/REQUEST-as-read.md`).

Sources, all from my verified extraction of frozen **171** (`812ad674…731d`):
`security_lifecycle_model_v1.py` `3c23b428…fb8f` (`TRANSITION_JOURNAL_KEYS`, `TRANSITION_STATES`,
`TRANSITION_RECOVERY_TABLE`, `registry_digest`, `core_transition_affected_namespaces`, `admit_transition_journal`,
`recover_transition_journal`); `transition-journal-cases.v1.json` (43 vectors; recovery vectors 31–41);
`security-and-lifecycle.md` S7 / S9.2; `commit-recovery-readonly.v3.md` §2. Executable evidence:
`claude-out/terminal_probe.py` → `terminal-probe.txt`.

## 1. What the unchanged reference actually does (executed, not read)
| Input to `recover_transition_journal` | Result |
|---|---|
| `DONE` / `ABORTED`, live registry == frozen, journaled lease set re-acquired | `RELEASE-ONLY` |
| same, **one namespace lawfully registered after completion** | **`QUARANTINE` / `MIGRATION.CORRUPT`** |
| same, leases not re-acquired (what a read-only entry must not do) | `BUSY` / `PROJECT.BUSY` |
| same, one journaled namespace busy (e.g. a reader holds `SHARED-READ`) | `BUSY` / `PROJECT.BUSY` |
| `admit_transition_journal` on a `DONE`/`ABORTED` journal | `REFUSE TRANSITION.INITIAL_STATE:<state>` — **no function admits a terminal journal** |

So your investigation is right, and it is wider than 171's phrase: the fence, live-registry equality and exact
re-acquisition all precede the state dispatch, for terminal states too. Two consequences:
1. There is no selector today that could back 171's "admitted `DONE` or `ABORTED` journal"; admission exists only for
   the *initial* `LEASED` record with a live context, and I agree it must not be stretched into proof of a later state.
2. **Whether the writer law is defective depends on one fact the reference never states: how long a terminal journal
   stays in the slot the next-fence rule consults.** The model's own rationale for the registry check is "a namespace
   registered or deregistered **while a transition was journaled** is impossible without the fence". That sentence is
   true only if a completed transition stops being "journaled". If a terminal journal is *retained in the active slot*,
   the first lawful registration afterwards turns every later fence acquisition into `MIGRATION.CORRUPT` (row 2) — a
   general defect, not a reader problem.

## 2. The owner choice that decides everything
- **Option A — retirement (recommended).** The journal consulted by the next-fence rule is an *active slot*. Completing
  a transition — normally, or through `RELEASE-ONLY` — ends by **retiring** the journal from that slot (its
  `journalRef` and bytes may be retained as history; the slot becomes *confirmed absent*). A terminal journal is then
  observable in the active slot **only in the crash window** between the terminal state write and retirement.
- **Option B — retention.** A terminal journal stays in the active slot until the next transition replaces it.

Why A:
1. It makes the model's existing rationale true instead of weakening checks: in the crash window no registration can
   have happened (registration needs the fence; every fence acquirer other than the read-only reader runs recovery —
   hence retirement — first; the reader registers nothing). So `registry == frozen` and exact re-acquisition remain
   *sound* for terminal journals, and **`recover_transition_journal` and all eleven recovery vectors (31–41, including
   40 `done-journal-only-releases`) stay byte-identical.**
2. It removes the general `MIGRATION.CORRUPT`-after-registration defect by lifecycle, where B must remove a fail-closed
   check from the writer path.
3. It gives the reader's "terminal footprint" a meaning made only of existing selectors (§3), so nothing is invented.
4. Retirement is idempotent under crash: a terminal journal seen again yields `RELEASE-ONLY` again.
Cost of A: one new normative act ("retire") in S9.2 whose physical form (rename/unlink/slot marker) is the host's to
implement under the fence; the pure model needs no change because it already ends at `journalStateAfter`.

If you choose **B** instead, the generic reference *must* change: dispatch `DONE`/`ABORTED` before the registry and
lease checks (internal consistency only), rewrite the docstring sentence quoted above, amend S9.2's order ("then by
state") and the `MIGRATION.CORRUPT` registry row in the S12 table, keep vectors 37/38 for nonterminal states, and add
`done-after-later-registration-releases-only` / `aborted-…` / `done-without-reacquisition-…` vectors. That is a larger
and riskier edit to a writer path for the sake of a reader.

## 3. Minimum safe reader law (Option A), using only existing selectors
Under the reader's fence, before any project lease, over the **active slot** read through retained custody:
1. **Custody and shape.** Unreadable / unavailable custody, or anything failing the closed shape —
   `set(journal) == TRANSITION_JOURNAL_KEYS`, `journalSchema == 1`, `kind == 'installation-transition'`,
   `fenceHeld is True`, `writtenAfterAllLeasesHeld is True`, `state ∈ TRANSITION_STATES` — → `unknown-custody`.
   (Same predicates the model already uses: `TRANSITION.JOURNAL_SHAPE`, `TRANSITION.JOURNAL_LAW_CONSTANTS`.)
2. **Internal consistency, from the journal alone.** `registryDigest == registry_digest(journal.registry)` and
   `journal.registry` already in `_registry_sorted` order; `(affects, leaseSet) ==
   core_transition_affected_namespaces(<the journal's own bound fields>, journal.registry)` — that function reads only
   `operation`, `from/toStateSchema`, `from/toStoreGeneration`, all of which are `INTENT_BOUND_FIELDS` carried in the
   journal. Failure → `unknown-custody` (`TRANSITION.REGISTRY_DIGEST_MISMATCH` / `TRANSITION.SCOPE_MISMATCH` are the
   existing names for these defects; the *reader* never reports them as `MIGRATION.CORRUPT`).
3. **State.** Nonterminal → `unavailable-busy` (171, unchanged). Terminal → step 4.
4. **Terminal, Option A only:** live registry observed under this fence `==` the frozen registry (the existing
   `registry != journal['registry']` predicate). Equal → **permit**; unequal → `unknown-custody` (under A this is an
   impossible state, so it must not be read as absence or busy; and the reader still may not call it corruption).
   **No lease re-acquisition**, no release, no retirement — the reader writes nothing; retirement is left to the next
   ordinary fence acquirer. Ordinary registry/store-binding admission of the *requested* namespace then follows as in
   169/171.
What this deliberately does **not** claim: that the terminal *state value* is authenticated. It is read under retained
custody like every other byte here; the initial-`LEASED` admission is not evidence for it, and no digest chains the
state progression. Say so in the text.
Not in the minimum: `intentDigest` against the admitted intent record (only checkable if the host retains that record —
**owner choice 1**: require it when retained, or leave it to the writer); equality of current schema/store/core
generation with the journal's `to*` (DONE) / `from*` (ABORTED) values (**owner choice 2** — attractive as a real
"footprint", but fence-only `update`/`install` change generations without a journal, so it risks re-creating a
permanent `unknown-custody`; I would leave it out and track it).

## 4. "Writer-class" versus "next fence" (171 W-1) without authorizing report-only writes
The unqualified S9.2 rule ("first act under the next fence, before any project admission") has the same latent
collision for the lease table's **report-only, no write** fence-only entries (`doctor`, `trust doctor`, `store status`)
as it had for `recover`. Suggested wording, reusing that table rather than a new class:
> Transition crash recovery is executed by the next fence acquisition of an entry that is permitted to mutate
> installation or project state. Entries the lease table marks report-only, and read-only commit recovery, never
> execute it: under their fence they observe the active journal and refuse or report as their owners specify.
and in the reader's paragraph replace "a separately authorized writer-class entry must execute S9.2 recovery first" by
"recovery is executed by the next such entry, per S9.2; repeating `recover` alone does not clear the condition."
**Owner choice 3:** whether an ordinary `SHARED-READ` `query` counts as such an entry. Existing law says yes ("before
any project admission"); I would not change that here, only stop the sentence from implying a dedicated command.

## 5. Exact things that must change (Option A)
| Artifact | Change |
|---|---|
| contract S9.2 | define the active slot; completion and `RELEASE-ONLY` end by retiring the journal; steady state is confirmed absence; a terminal journal is observable only in the crash window; §4's executor sentence |
| contract S7 "Read-only recovery admission", `commit-recovery-readonly.v3.md` §2, identity "Read-only recovery selectors" | replace "its read-only S9.2 checks establish the terminal footprint with no remaining recovery action" by the explicit list of §3 (steps 1, 2, 4), the no-re-acquisition / no-retirement sentence, the custody-conditional caveat, and §4's wording |
| `security_lifecycle_model_v1.py`, `transition-journal-cases.v1.json` | **none required** for A. *Optional and better:* add a pure selector (e.g. `observe_transition_journal_readonly(journal, ctx={namespaceRegistry, fenceHeld})` → `permit` / `unavailable-busy` / `unknown-custody`) with vectors: absent; four nonterminal states; `DONE`/`ABORTED` permit; terminal with registry changed; bad digest; scope mismatch; bad law constants; unknown state; and **a mandatory negative that it never returns `MIGRATION.CORRUPT`, `reacquire` or a `journalStateAfter`**. That would be the first real executable change since 145, so 167 W-1's docstring rides along |
| five source-pin manifests | rebind |
| tracked, not fixed here | owner choices 1–3; the physical retirement act and its crash-safety test in the host; S9.3's lineage companion, which keys on "`RELEASE-ONLY` reaching `DONE`" and should be read once against retirement |

## 6. Recommendation and what stays open
**Recommend Option A with the §3 law and the §4 wording.** It is the smallest correction that (i) defines the
terminal check entirely in existing selectors, (ii) leaves the generic writer recovery function and its eleven vectors
untouched while making its own stated rationale true, (iii) closes the general retained-journal defect the probe
demonstrates, and (iv) keeps the reader write-free, lease-free and unable to call anything corrupt. Unresolved and
yours to decide: A versus B (everything else follows from it), owner choices 1–3, and whether to make the reader
observation executable now. Nothing here is acceptance; I will review whatever bytes are frozen.
