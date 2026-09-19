# Independent bounded review — recovery admission reference 169 (prose only)

Reviewer: Claude (actual independent reviewer; Codex remains owner). 2026-09-19.
Request: `admission169-20260919-REQUEST.md` (bytes as read: `claude-out/REQUEST-as-read.md`); README read. Scope: the
delta of frozen `recovery-admission-reference-checkpoint-169` over frozen 167 — three owner documents and five manifest
rebindings. My earlier opinion on the *proposal* is not acceptance of these bytes; this review reads the frozen text.
No runtime source, mapper or selection is claimed. Scratch only, `-I -B`; no frozen/selected/product edit, commit, push
or delegation; no cumulative approval. No cryptographic corpus repeated.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 2,117,588 bytes, SHA-256 `8c77846b1069fd9f308769df1bc5011e69b4bc1ae3ca139d92e60031daf749bf` = request = `archive-pin.json` |
| Members | 1,361/1,361 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified after the lanes |
| Candidate pins | 1,287/1,287; nothing unpinned |
| Parent | `parent-inputs.json` = **my own** verified 167 extraction (1,287/1,287) |
| Changed | exactly eight = the declared list: `commit-recovery-readonly.v3.md`, `identity-and-evidence.md`, `security-and-lifecycle.md` + five manifests (every changed manifest line is a SHA-256 value); all three before-images equal my 167 bytes |
| Python | 84/84 byte-identical to 167 (hence 145) |
| Lanes, fresh scratch | all seven exit 0, counts unchanged — as the README says, they show compatibility of unchanged projected models, not that an admission owner exists |

## 2. The eight clarifications, against the frozen text
| # | Asked in my adjudication | 169 text | |
|---|---|---|---|
| 1 | retry budget normative; wait bound printed | "once, nonblocking … never takes the 30-second project-lease retry path … may wait up to 5 seconds for its admission fence; the reader below waits on no lock or writer. This is a lock-wait bound, not a bound on the total time" — same in all three owners | ✔ |
| 2 | existing projection for admission failure, zero reads | "`unavailable-busy` using §1's existing `operational-failed` / exit 4 / `LEDGER.BUSY_TIMEOUT` / `ledger-busy` / `PROJECT.BUSY`" — equals §1's row; "starts no recovery ledger or journal snapshot and performs no recovery witness or floor read; registry and custody reads needed by admission are separate" | ✔ busy; see W-2 for the refusal |
| 3 | keep "no liveness probe"; busyness ≠ liveness | kept verbatim in Step 0; "never attempt liveness or evidence for `unknown-attempt-open` or noncommitment" | ✔ |
| 4 | sealed, host-composed context; match, don't re-read | "private-field admitted read context, constructible only from successful S7 fence-to-`SHARED-READ` admission … matching its admitted mode, namespace and binding to the request, not re-reading the registry outside the fence … the security crate gains no dependency" | ✔ |
| 5 | both lifetimes | "The lease outlives the read **and consumption/projection** … Owned … evidence may survive lease release, but then carries only historical observations" | ✔ |
| 6 | third owner | `identity-and-evidence.md` rewritten consistently | ✔ |
| 7 | scope of §2's prohibition | "govern **only the §2 reader**, starting at Step 0, not its prior ordinary admission or the separately authorized §4 settlement sweep" | ✔ — and this is what exposes F-1 |
| 8 | incompatible holder → existing end handoff | "the ordinary S7 end handoff releases the existing lease **before** taking the fence … No upgrade or fence acquisition while holding a lease … A latched committing session starts no new phase" | ✔ |

The exclusion argument is stated and correctly limited: "cooperating protocol exclusion, not proof against arbitrary
external filesystem mutation, path replacement or ABA; physical custody checks remain required." No overclaim there.

## 3. Findings
- **F-1 (medium) — by scoping the prohibitions to "Step 0 onward", 169 leaves the admission phase with no statement
  that it writes nothing, while S7 attaches writes to exactly that kind of boundary.** Before 169, lease-taking sat
  *inside* "Read-only throughout", so every prohibition (no `INSERT/UPDATE/DELETE`, no witness write, "any SC-TRUST
  high-water raise or copy", no marker write, no repair) covered it. Now the prohibitions "govern only the §2 reader …
  not its prior ordinary admission", and what 169 says about admission is only "allocates no binding, registers no
  namespace, and grants no execution authority". Two existing S7 rules speak about *ordinary* fence acquisitions:
  1. contract, core-transition lock set, item 4: "**Crash recovery runs as the first act under the next fence
     acquisition, before any admission**, over the S9.2 recovery table … and re-acquires exactly the journaled
     [EXCLUSIVE] set." Read with "ordinary S7 admission", a `recover(ExecutionId)` that finds a pending installation
     transition journal would *perform installation crash recovery* — writes, `EXCLUSIVE` leases, unbounded work —
     before its "read-only" reader starts; or, if it must not, the text has to say what it does instead.
  2. contract l. 866–868: "Operation start retains fence→nonblocking project lease order … **At either boundary,
     copy** only the generation the admitted witness names" (the SC-TRUST floor copy). Line 876 does say "Read-only
     recovery and migration/rollback do not raise final floors", which settles the floor copy — but it is the *only*
     write that is settled, and it sits far from the new paragraph.
  The public consequences differ: a command documented as read-only that may run a transition recovery has a different
  wait/time disclosure ("not a bound on total admission I/O" does not cover *writes*), different failure projections
  (`MIGRATION.CORRUPT` from the S9.2 table), and a different authority class. Needed, in the owner of your choice: one
  sentence that recovery admission **performs no write of any kind** — no boundary floor copy (cite l. 876), no witness
  or marker write, no trust-state write, no transition-journal action — and a rule for a pending installation
  transition journal observed under its fence: either it refuses with a named existing projection (I would expect
  `unavailable-busy`: the install is mid-transition and a writer-class entry must finish it) without starting the
  reader, or the contract explicitly says any fence acquirer, including this one, runs that recovery and the command is
  then not read-only end to end. Silence is the one option that is not safe, because "ordinary" now imports the rule.
- **W-1 (low) — "must get a busy probe and retain/skip as their owners require"** is right for GC and the settlement
  sweep (busy = retain / skip) but not for the others it lists: a core transition is all-or-nothing — "the first busy
  namespace releases every acquired lease … releases the fence, reports `PROJECT.BUSY`" — and purge / repair-apply are
  `EXCLUSIVE` requests that get `PROJECT.BUSY` "at once". "as their owners require" rescues the sentence formally; "is
  refused busy (GC and the sweep retain or skip; purge, repair-apply, migration and core transitions report
  `PROJECT.BUSY`)" would say it. The protection claim itself is unaffected: none of them proceeds.
- **W-2 (low) — the public projection of "an unregistered namespace refuses" is still not named.** It was not named
  before either, and I did not insist on it in the adjudication; but this request asks about public projection, and
  the busy outcome is now spelled out to the last field while its sibling is "under the existing S7 rule" — an internal
  lock-model rule (`lease-on-an-unregistered-namespace-is-refused-negative`) with no D9 row. §1's closed table has
  `binding-unusable` (`request-rejected` / 2 / `EXTENSION.ADMISSION_REJECTED` / `RECOVERY.REFUSED`) as the only
  refusal; if that is the intended row, say so; if not, the mapper has nothing to map to.
- **N-1 (note)** "A nested caller already holding the matching admitted `SHARED-READ` context reuses it" — then that
  invocation's fence wait is 0 and its registry validation is as old as the outer admission. Correct under the
  exclusion argument; worth remembering when the wait bound is quoted as "up to 5 seconds" for *every* invocation.
- Unchanged and disclosed: 167 W-1 (Python docstring), 151 N-2 (three of seven lanes enforce document hashes), no
  executable admission owner, no mapper (150 F-2), writer disposition (165).

## 4. Bounded verdict
**169: reviewed; one finding of substance. All eight clarifications from my adjudication are present and mutually
consistent across the three owners: admission first (≤ 5 s fence wait, registry/binding validation under the fence, one
non-blocking `SHARED-READ`, no project retry), the existing `unavailable-busy` projection with zero recovery reads,
busyness never liveness, a sealed host-composed context matched rather than re-admitted, both lifetimes, nested reuse
versus the ordinary end handoff, and §2's prohibitions scoped to the reader and away from the §4 sweep; the exclusion
claim is correctly limited to the cooperating protocol. F-1: that very scoping removes every "no write" prohibition
from the admission phase, while S7 says crash recovery of a pending installation transition "runs as the first act
under the next fence acquisition, before any admission" and attaches a floor copy to operation boundaries — 169 must
state that recovery admission writes nothing and what it does when it meets a pending transition journal. W-1/W-2 are
wording.** Not acceptance of the proposal as implemented, not approval of any host admission owner (none exists), and
not any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `candidate-pins.json`, `diffs/` (three documents),
`owner/` (seven lanes + `exits.txt`), `probes/lanes.sh`, `hashes.txt`. Owner passages cited are in my verified 169
extraction: contract S7 (lock table, laws, core-transition lock set item 4, boundary paragraph l. 866–876, new
"Read-only recovery admission" paragraph); `commit-recovery-readonly.v3.md` §1 table and new §2; identity
"Read-only recovery selectors".
