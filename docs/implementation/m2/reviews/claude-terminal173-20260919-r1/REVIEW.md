# Independent bounded review — terminal-journal admission, active-slot retirement and the pure reader observer, 173 (reference)

Reviewer: Claude (actual independent reviewer; Codex remains owner). 2026-09-19.
Request: `terminal173-20260919-REQUEST.md` (bytes as read: `claude-out/REQUEST-as-read.md`); README, `owner-decision.md`
and the full delta read. My earlier proposal assistance is not approval of these bytes; I review what is frozen,
including the owner choices that go beyond it. Scope: the delta of frozen
`terminal-admission-reference-checkpoint-173` over frozen 171. No physical retirement, host reader, mapper or selection
is claimed, and I infer none. Scratch only, `-I -B`; no frozen/selected/product edit, commit, push or delegation; no
cumulative approval.

## 1. Subject verification (before use)
| Item | Value |
|---|---|
| `subject.tar.xz` | 2,149,068 bytes, SHA-256 `2717e3ca784724c3628b29653db8ce3abcec4813cb6797c6abba190a7d7ab027` = request = `archive-pin.json` |
| Members | 1,393/1,393 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified after all runs |
| Candidate pins | 1,289/1,289; nothing unpinned |
| Parent | `parent-inputs.json` = **my own** verified 171 extraction (1,287/1,287) |
| Changed / added | exactly the declared 12: three owner documents, five manifests, `check-security-lifecycle.v1.py`, `generation_reference.py`; added `readonly_transition_reference.py`, `readonly_transition_checks.v1.py` |
| Python | 86 files: 82 byte-identical to 171, 2 changed, 2 added. **`security_lifecycle_model_v1.py` and `transition-journal-cases.v1.json` are byte-identical to 171** — the writer model and its 43 vectors did not move |
| Lanes, fresh scratch | all seven exit 0; counts unchanged except the security sweep list, now 25 with `readonly-active-transition-admission` (61 checks, `physicalRetirementQualified: false`) |
| 167 W-1 | docstring now "`quarantine_present` (from admitted markers only)" — **closed** |

## 2. The observer, examined independently (`probes/observer_probe.py` → `io/observer-probe.txt`)
- **Own oracle.** I wrote the four numbered steps of `commit-recovery-readonly.v3.md` §2 as a separate function (using
  only the model's canonical/hash helper and `admit_transition_intent`, never `observe`). Corpus: every lawful fixture
  journal × six states × {registry equal / grew / shrank}; every bound field × ten junk values **both with the digest
  left stale and with the digest repaired** (so one rule is violated); every envelope field × thirteen values; missing
  and extra members; reversed frozen registry (same set ⇒ same digest and same derived lease set — isolates the
  sortedness rule); reversed `leaseSet`; duplicate registry with repaired digest; observation/context envelopes.
  **30,515 cases: 0 mismatches, 0 uncaught exceptions, inputs never mutated, the only key ever returned is
  `standing`** (330 permit / 628 busy / 29,557 unknown-custody).
- **Totality.** 40,000 random corruptions (wrong types, lone surrogates, NaN, bytes, huge ints, nested junk, foreign
  keys, junk contexts): no exception, always one of the three standings.
- **Relation to the unchanged writer recovery** on the same journal and registry: writer `RELEASE-ONLY` ↔ reader
  `permit`; writer `QUARANTINE` (registry grew) on a terminal journal ↔ reader `unknown-custody` (never corruption);
  every nonterminal writer action (`ABORT`, `RESUME-COMMIT`, `QUARANTINE`) ↔ reader `unavailable-busy`. Every lawful
  fixture journal is busy or permit; only the two deliberately bad fixtures are `unknown-custody`
  (`io/fixture-journals.txt`).
- **Mutants of the observer (15).** Owner's checker kills 13 (one by an uncaught `AttributeError` in the mutant rather
  than an assertion — a kill, but it shows `_registry` is also what keeps `registry_digest` total). Two survive it:
  one is equivalent (terminal registries compared as sets — both sides are already proven sorted-unique); one is T-1.

## 3. The owner choices, against the other owners
- **Option A is coherent with the writer law it leaves untouched.** The new S9.2 paragraph states the invariant that
  was implicit: terminal durability, then durable active-slot absence **under the same fence, before releasing the
  journaled leases/fence or admitting a registration**; failed or uncertain retirement fails closed; history is never a
  fallback; PS-01 lineage completes before retirement. With that, the writer's `registry == frozen` and exact
  re-acquisition are sound for terminal states too (my 173-proposal probe showed they were *not* without it), which is
  why the model and its eleven recovery vectors can stay byte-identical. Retirement is correctly described as a host
  postcondition that the pure action does not perform or prove.
- **The reader law is fully defined now** — nothing like "terminal footprint" remains; every predicate is an existing
  selector, the state is declared custody-conditional, and "initial-`LEASED` admission is not proof of terminal state"
  is said in all three owners. Not importing current-generation or deadline equality is the right call and is stated
  as a decision, not an omission.

## 4. Findings
- **F-1 (low–medium) — the two rule sites still name a narrower exception than the paragraph beneath them.** S7
  core-transition item 4: "before any admission, **except for read-only commit recovery's admission** described above";
  S9.2 heading rule: "before any project admission **other than the narrow read-only commit-recovery exception**". The
  new S9.2 text then excepts a whole class: "Any entry promising no durable writes — including read-only commit
  recovery, **ordinary `SHARED-READ` operations, and report-only `doctor`, `trust doctor` and `store status`** — must
  not execute crash recovery or retirement." A reader of either rule sentence concludes that `query` still runs crash
  recovery under its fence; a reader of the paragraph concludes it must not. This is the same two-sites problem 171
  fixed for the narrower case; both sentences need the class, not the instance.
- **F-2 (low–medium) — the executor set is a predicate with no extension.** "entries whose existing contract and
  authority permit the required S9.2 mutations" is never enumerated, and the lease-by-command table is unchanged. The
  decisive undefined case is **`APPEND-WRITE`** (`analyze`, `import`, the default command): it promises durable
  *project* writes, but nothing gives it authority to abort or resume a **core/store transition** and take `EXCLUSIVE`
  on every registered namespace. If it is eligible, an ordinary analysis run performs installation recovery (the old
  unconditional rule — but then say so); if it is not, the text gives it **no barrier at all** ("Project reader
  admission uses the same … barrier" covers readers only), and "no dedicated command is required" becomes doubtful,
  because after a crashed transition only core-transition commands might clear it. Either way the public behaviour of
  many commands now depends on a set nobody can read off the contract. One column in the lease table (executes S9.2
  recovery / observes and refuses / report-only diagnostic) would settle it, and would also make visible that this
  candidate **changes the behaviour of every ordinary `SHARED-READ` command** during a crashed transition (busy or
  unknown-custody instead of recovering) — a deliberate and defensible choice, but a wider one than "terminal-journal
  admission", and no workflow-surface owner was touched.
- **T-1 (low) — the intent-law step is unpinned by the owner's 61 checks.** Removing
  `admit_transition_intent(intent)` from the observer passes the checker: its three intent negatives
  (`fromStateSchema: True`, `operation: 'unknown'`, `rollbackDeadline: 'invalid'`) also break `intentDigest`, which
  refuses first. With the digest **repaired** the mutant is caught 6,654 times in my corpus. One repaired-digest
  negative (e.g. a same-closure `core-update`, which the fixture `…_wrongField` already models) pins it. Same masking
  pattern as 144/152/172.
- **N-1 (note)** `_registry` requires `1 ≤ len(s) ≤ 4096` per namespace string. The lower bound matches "admitted
  namespace strings"; I could not find the 4,096 upper bound for a locator in S7 or the model (`_registry_sorted` has
  none; the contract's 4096 is the workspace-unit cap). Harmless in a projection, but it is a constant the observer
  introduces — cite its owner or drop it, so the future host reader does not inherit an unowned limit.
- **N-2 (note)** The checker loads the observer and shares its fixture with it; its independence is in the
  hand-written expectations. That is adequate for a projection (and it correctly asserts no `action`, `reacquire`,
  `journalStateAfter` or `MIGRATION.CORRUPT` key can appear), and my oracle agrees on 30,515 cases; I note it because
  the README calls the checker "independent".
- Stated and still owed, correctly: physical atomic retirement, directory barriers, crash/idempotence qualification;
  the host custody reader; the mapper (150 F-2); writer disposition (165).

## 5. Closure
| My item | Status |
|---|---|
| admission171 **F-1** undefined "terminal footprint" | **Closed** — explicit four-step law in existing selectors, executable projection, custody caveat; generic writer recovery unchanged and made sound by the retirement law |
| admission171 **W-1** "writer-class entry" | **Replaced by an owner choice** — see F-1/F-2 above for what that choice still leaves inconsistent or undefined |
| marker-routes167 **W-1** docstring | **Closed** |

## 6. Bounded verdict
**173: reviewed, no blocking finding in the mechanism. The pure observer equals an independently written oracle of the
contract's four steps on 30,515 cases with isolating negatives and is total over 40,000 random corruptions; it returns
only an internal standing, never an action, lease set or corruption code; it relates to the byte-identical writer
recovery exactly as intended (release-only ↔ permit, registry-grew ↔ unknown-custody, every nonterminal action ↔ busy).
Option A is stated as a same-fence, fail-closed retirement postcondition that makes the unchanged writer checks sound
and is honestly marked unqualified in the host. Two findings concern the owner's wider executor-scope choice, not the
mechanism: F-1 — both next-fence rule sentences still except only read-only commit recovery while the paragraph below
excepts every no-write entry including ordinary `SHARED-READ`; F-2 — the set of entries that *do* execute recovery is
a predicate without an extension, leaving `APPEND-WRITE` with neither authority nor barrier and changing the behaviour
of every `SHARED-READ` command without a table that says so. T-1: the intent-law step is masked in the owner's
checker.** Not approval of physical retirement, a host reader or mapper (none exists), or any cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `candidate-pins.json`, `diffs/` (five),
`owner/` (seven lanes + `exits.txt`), `probes/{lanes.sh, observer_probe.py}`,
`io/{observer-probe.txt, observer-probe.json, fixture-journals.txt}`, `hashes.txt`.
