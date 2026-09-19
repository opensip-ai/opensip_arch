# Independent bounded review — read-only recovery admission 171 (reference, prose only)

Reviewer: Claude (actual independent reviewer; Codex remains owner). 2026-09-19.
Request: `admission171-20260919-REQUEST.md` (bytes as read: `claude-out/REQUEST-as-read.md`); README and the full delta
read against my verified 169. Scope: the delta of frozen `readonly-admission-reference-checkpoint-171` over frozen 169
— three owner documents and five manifest rebindings, answering my 169 F-1 / W-1 / W-2. I was asked to check whether
the exception is *coherent*, not whether it follows my recommendation. No runtime source, producer or mapper exists
and none is claimed. Scratch only, `-I -B`; no frozen/selected/product edit, commit, push or delegation; no cumulative
approval. No cryptographic corpus repeated.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 2,118,312 bytes, SHA-256 `812ad6744401d78b237d04254fa0dfdc043a8aa3705d55686e4edd1f4d0a731d` = request = `archive-pin.json` |
| Members | 1,360/1,360 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified after the lanes |
| Candidate pins | 1,287/1,287; nothing unpinned |
| Parent | `parent-inputs.json` = **my own** verified 169 extraction (1,287/1,287) |
| Changed | exactly eight = the declared list (three owners + five manifests); all three before-images equal my 169 bytes |
| Python | 84/84 byte-identical to 169 (hence 145) |
| Lanes, fresh scratch | all seven exit 0, counts unchanged — compatibility of unchanged projected models only, as the README says |

## 2. Is the exception coherent? (checked against the unchanged law, not against my wish list)
- **It is made where the rule lives, at both sites.** S7's core-transition item 4 ("Crash recovery runs as the first act
  under the next fence acquisition, before any admission") and S9.2's heading rule each now carry the same narrow
  exception and point to the bounded owner; the third owner (identity) restates it. No site still states the
  unqualified rule.
- **It is an exception to the *action*, not to the lock order.** "not an exception to the fence-to-lease lock order":
  the journal is observed **under the fence, before any project lease**, which is exactly where S9.2 places its own
  decision. Because a core transition holds the fence for its whole duration, a nonterminal journal seen *under our
  fence* can only be a crashed transition, never a live one — so refusing it is not a race.
- **The busy projection has a precedent of the same shape.** §1 already routes a lawful `{A}` / `{A,B}` migration prefix
  to `unavailable-busy`: a state that needs a *separately admitted* maintenance attempt before a reader can proceed.
  A pending installation journal is the same kind of state, one level up. It is not a new meaning for the row.
- **`unknown-custody` for an unreadable/unadmittable journal is the right neighbour.** It is neither absence (would
  admit a reader into a possibly half-transitioned install), nor busy (nothing says a retry helps), nor the *writer's*
  `MIGRATION.CORRUPT` (a reader has not established corruption) — consistent with how 165/167 route evidence that
  cannot be admitted.
- **No write is left unstated.** "creates or mutates no durable file, row, registry, binding, lease carrier, trust
  state, witness, floor or quarantine marker; performs no boundary floor copy …; starts no repair or
  installation-transition recovery action. Acquiring/releasing locks on existing admitted carriers is allowed; creating
  missing carriers … is not", and a missing fence/lease carrier is `unknown-custody`. That closes the hole 169's
  scoping opened, and it also answers a case I had not raised (a reader must not create `lifecycle.fence` or
  `readers.lease`).
- **Zero-read claim is kept honest:** "zero recovery ledger, journal-carrier, witness and floor reads; the necessary
  install-journal/registry admission observations are distinct."

## 3. Findings
- **F-1 (low–medium) — the *permit* branch for `DONE`/`ABORTED` relies on checks S9.2 does not define.** 171: "An
  admitted `DONE` or `ABORTED` journal permits continuation only when **its read-only S9.2 checks establish the
  terminal footprint** with no remaining recovery action". S9.2's whole rule for these states is "`DONE`/`ABORTED` →
  release only"; its footprint table is for `PREPARED` store operations, and "terminal footprint" occurs nowhere else
  in the contract. The only S9.2 checks that precede the state dispatch are (i) the fence, (ii) "a registry that
  differs from the frozen one → `QUARANTINE` / `MIGRATION.CORRUPT`", (iii) exact re-acquisition of the journaled lease
  set — and (iii) is forbidden to this reader. So an implementer cannot tell what must be verified:
  - if it means (ii), then every namespace lawfully registered *after* a completed transition makes the registry
    "differ from the frozen one", and — if a terminal journal is retained — `recover` would answer `unknown-custody`
    on every installation that has ever completed a transition and then registered a project;
  - if it means nothing beyond an admitted terminal journal (because "release only" is a no-op for a new process:
    "flock leases die with the process"), the sentence should say exactly that.
  The request already lists "terminal-footprint admission" as an implementation obligation; my point is that the
  *reference* does not yet say what that admission is, and the two readings give opposite public results
  (`unknown-custody` vs proceed). Define the check (or state that an admitted terminal journal alone permits), and say
  whether the registry-versus-frozen comparison applies to terminal journals at all.
- **W-1 (low) — "a separately authorized writer-class entry must execute S9.2 recovery first".** Under the unchanged
  S9.2 rule, recovery is "the first act under the next fence" of **any** other entry — including an ordinary
  `SHARED-READ` `query`. "Writer-class" suggests a dedicated command and could be read as "no ordinary command will
  clear this"; "any other fence acquisition, per S9.2" is what the law says. This also matters for the user-facing
  meaning of the busy answer: `PROJECT.BUSY` normally invites a retry, and here a retry of `recover` alone never
  succeeds until some other entry has run the recovery — the same is already true of the `{A,B}` prefix, so it is
  consistent, but worth one clause.
- **Closed:** 169 **W-1** (per-owner busy behaviour: "GC and the settlement sweep retain/skip …; purge, repair-apply,
  migration and core transitions report `PROJECT.BUSY`") and 169 **W-2** (unregistered namespace = `binding-unusable`,
  `request-rejected` / 2 / `EXTENSION.ADMISSION_REJECTED`, typed `RECOVERY.REFUSED` naming the namespace — identical
  in all three owners and equal to §1's existing row).
- Unchanged and disclosed: no executable admission owner or journal producer; 150 F-2 mapper; 165 writer disposition;
  167 W-1 docstring; 151 N-2 lane enforcement.

## 4. Closure
| My item | Status |
|---|---|
| admission169 **F-1** admission phase left without a no-write statement; next-fence crash recovery imported by "ordinary" | **Closed** — explicit no-write list, exception stated at both rule sites, pending journal refused without acquiring the journaled set; one residual definition gap (F-1 above) in the terminal-permit branch |
| admission169 **W-1**, **W-2** | **Closed** |

## 5. Bounded verdict
**171: reviewed, no blocking finding. The read-only exception is coherent on its own terms: it is stated at both S7
and S9.2, it excepts the recovery *action* while keeping the fence-to-lease order, the journal is observed under the
fence where a nonterminal state can only be a crashed transition, the busy and unknown-custody routes reuse existing
rows with an existing precedent of the same shape, and admission now writes nothing and creates no carrier. F-1: the
branch that *permits* admission past a `DONE`/`ABORTED` journal depends on "read-only S9.2 checks" of a "terminal
footprint" that S9.2 does not define — under one reading a retained terminal journal plus any later registration
makes `recover` permanently `unknown-custody`, under the other the journal's admitted state alone suffices; say which.
W-1: "writer-class entry" is narrower than S9.2's "next fence".** Not approval of any host admission owner, journal
producer or mapper (none exists), and not any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `candidate-pins.json`, `diffs/` (three documents),
`owner/` (seven lanes + `exits.txt`), `probes/lanes.sh`, `hashes.txt`. Owner passages are in my verified 171
extraction: contract S7 "Read-only recovery admission" and core-transition item 4; S9.2 states and crash-recovery
rule; `commit-recovery-readonly.v3.md` §1 table and §2 admission; identity "Read-only recovery selectors".
