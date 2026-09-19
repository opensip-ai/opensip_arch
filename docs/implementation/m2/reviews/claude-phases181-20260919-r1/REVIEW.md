# Independent review — frozen `recovery-phases-reference-checkpoint-181`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: exactly the frozen 181 reference bytes. **My two 181 proposal assessments and `NOTES-D6.md` were assistance and are not acceptance of these bytes**; where the owner followed them I checked the bytes, and where the owner corrected me I say so. 184 (mechanism) is separate. No host, custody, retirement, mapper, product-adoption, cumulative or authority approval.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `083eb63517e231195f4f039b95543dac3791246387ec309c9a5fbfcb8a4279e0`, 2,207,232 B = request = `archive-pin.json` |
| Members | 1,398, all regular/safe, verified from the tar before extraction; re-verified at end |
| Candidate pins | 1,294/1,294; none unpinned; declared change list equals computed |
| Parent | equals **my own verified 182 extraction** (1,289 files); 14 changed + 5 added = 19 |
| Python | 89: 85 byte-identical to 182; `check-integration.py` changed; three new modules. Lifecycle writer model and the 43 transition vectors byte-identical |

## 2. Owner checks re-run

Reference order, `-I -B`, fresh outputs (`claude-out/owner/`): **all seven lanes exit 0** (integration includes the 108 new `phases181.*` checks; I also ran that module alone through the lane's loader: 108/108). No bytecode left.

## 3. What I read

All of `executor_phases_reference.py` (93 lines), `active_slot_reference.py` (114), `executor_phases_checks.v1.py` (167), the companion and its schema, the whole new S9.2.1 section, and every owner delta (`claude-out/diffs/`). Summary of my judgement of the text: **S9.2.1 is a clear, closed statement of the A/B/C order** and it deliberately dispositions every sentence I listed as D1–D6: S9.2 "must already authorize" is replaced by the closed Phase A gate; S15's commit recheck is qualified *in S15* to "first-pass commit of a newly admitted Phase C transition"; S6 epoch capture and S1/S4 evaluation are excluded from A/B by name; both inventory-schema descriptions and workflows l.1663 now derive the recovery set from the journaled intent. "No new consent" is stated and matches the inventory. The physical reason (floors live in the store whose selection is undecided) is recorded. The three points of `NOTES-D6.md` are each answered in the bytes: "no S4 **decision evaluation** or evaluation-driven floor/anchor write" (not "no S4 writes"); the `ST-UNBOOTSTRAPPED:MIGRATED` resting state is declared lawful with who performs PRESENT; structural refusal is placed before `RESTORED`.

## 4. My probes

`claude-out/probes/phase_probe.py` → `io/phase_probe.txt`; `footprint_grid.py` → `io/footprint_grid.txt`; `survivor_check.py` → `io/survivor_check.txt`. All through the real modules; retirement is an asserted tuple, as in the owner's model.

- **Every owner journal record × every state (90 pairs)** through the composition vs. the writer model called directly: 78 reach the same action. The 12 that differ are the owner's two deliberately malformed records (`…_smallerLeaseSet`, `…_wrongField`), which the composition refuses `unknown-custody` while the bare model would recover them — the composition is *stricter*, correctly (it goes through `recover_installation_transition`'s identity/intent/scope checks). No wedge from registry ordering: every record's frozen registry is sorted.
- Terminal `DONE` + live registry ≠ frozen → `MIGRATION.CORRUPT` (the observer-registry substitution in `historical` does not hide the mismatch). Fence not held, five malformed slot shapes → `unknown-custody`. BUSY with an asserted `absent` retirement → still `PROJECT.BUSY`.
- The D6 grid is §6 F-1.

## 5. Mutation (`claude-out/probes/mutation.{py,json,log}`)

Mutants applied to a scratch copy of the candidate; judged by the owner's phase-check module run through the lane's loader, **not** by the pinned lane (a pin refusal would not be semantic evidence). Baseline 108/108.

12 of 16 killed: retirement ignored; present-terminal accepted as retired; lease release skipped; QUARANTINE or BUSY treated as recovered; custody skipped; executor check dropped; freshness ignored; clock refusal ignored; stale generation in Phase C; clock evaluated before recovery; projection without `repositoryExecution`. The `Unreadable` spy is an effective control — it kills most ordering faults by construction.
4 survive — §6 T-1.

## 6. Findings

### F-1 (medium) — the D6 law "never ABORT after RESTORED / contradictory footprint is MIGRATION.CORRUPT" is contradicted by the unchanged writer model, and the new composition follows the model
S9.2.1 now says: "a proven contradictory store footprint retains S9's `MIGRATION.CORRUPT` refusal. Neither may be converted to ABORT after RESTORED". The writer model is byte-identical to 182, and for a `PREPARED` store-migrate journal with the old store **already fenced `RESTORED`** it answers (full 64-row grid in `io/footprint_grid.txt`):

| new-store footprint | model action |
|---|---|
| `migrating`, state `PREPARING` | **ABORT → ABORTED** |
| `migrating`, state `None` | **ABORT → ABORTED** |
| `migrating`, `PREPARED` | RESUME-COMMIT (correct) |
| `absent` / `both` | QUARANTINE `MIGRATION.CORRUPT` (correct) |

By the S9 protocol `RESTORED` is only written after `PREPARED` is durable, so *old=RESTORED with new=PREPARING* is precisely a contradictory footprint. `migration_recover` keys ABORT on the new-store state before it looks at the old store, and its rationale string says "old state untouched", which is false here: aborting deletes the migrating root while the old store is fenced — no usable store remains. Through `executor_phases_reference.sequence` that ABORT is accepted as a recovery action, an asserted retirement follows, and Phase C returns `journal-admitted-only` (`io/phase_probe.txt` case 2). Separately, for a **`COMMITTED`** journal the model never consults the footprint at all: `both` (which S9 itself calls ambiguous → quarantine), `absent`, or `PREPARING` all yield RESUME-COMMIT → DONE → retirement → Phase C (case 3).
The model behaviour is pre-existing; what is new in 181 is that the contract now legislates the opposite, the README says the writer predicates are unchanged, and none of the 108 checks exercises a contradictory footprint (the only footprint used is the healthy RESTORED/PREPARED one). So the most safety-relevant sentence of the D6 decision is prose-only and currently false of the reference. Remedy belongs in the writer model and its vectors (footprint consulted for `COMMITTED`; RESTORED dominates new-state in `PREPARED`), with the grid as vectors; "missing prepared evidence = unknown-custody" also needs a representable footprint value, which the closed footprint shape does not have today.

### F-2 (low-medium) — the floor image prepared "before RESTORED" has no stated freshness rule
S9.2.1 requires "the exact forward-only floor image … durably prepared before the old store is fenced `RESTORED`", and resumption "uses the … prepared floor image". `migrate_floors` in the model couples the copy and the `RESTORED` mark in one result, so there it is atomic. The prose opens an interval [image prepared, RESTORED] and does not say the image must equal the old store's floors *at the moment of fencing*. Any evaluation that advances `evalHighWater` in that interval (the transition's own first-pass checks are S4 evaluations with write-ahead floors) would make the copied image lower than the old store's final floor — a forward-only violation that no resumed step re-checks. One sentence closes it: the image is taken after the last floor write of the first pass and immediately before fencing, **or** resumption takes max(prepared image, fenced old-store floors) — the fenced store is still readable and rollback already uses max.

### T-1 (test strength) — four behaviour-changing faults pass the 108 checks
1. **Observer `unknown-custody` ignored** — not equivalent: with the slot **absent and the fence not held**, or absent with an unsorted/duplicate live registry, the mutant returns `phaseCEligible=True` (original: `unknown-custody`). No owner check has an absent slot without a fence. This is the path by which Phase C would run un-fenced.
2. **Requested operation need not match the new intent** — no check supplies a post-recovery intent for a different operation than the invoked command.
3. **Only one inventory lineage required** — `validate` is always called with two.
4. **Flag tokens matched by prefix** — the tokenised rule is never the deciding control, because `dispositions != expected_policy()` refuses first. Since the policy is fully pinned by that equality plus the projection digest, the structural rules in `validate` are secondary; that is a sound design (it is my R11 point taken to its conclusion), but then say so, or test the structural rules with the equality check bypassed.

### W-1 (low) — one more stale sentence, in unchanged Python
`integration-host-model.py` `installation_recovery_attempt` docstring: "Trusted host recovery step **before ordinary project admission**". Same old wording as the workflows paragraph 181 corrected. Also: this function is the existing owner of the Phase B attempt identity the new workflows text describes, yet `executor_phases_reference` does not compose it — the "distinct B/C identities" check only compares two strings the composition itself sets. `claude-out/io/residual-rule-scan.txt` (broader patterns than my 178 scan) shows every other site qualified.

### N-1 — disclosed limits are accurate
"journal-admitted-only", asserted custody/retirement/fresh inputs, no IO: the code matches. `post_recovery` is supplied up front and only lazily read — the model cannot show the host observed it *after* recovery; the README says so.

### N-2 — owner correction of my sketch, accepted
The owner-decision notes my proposal's projection omitted `steps` while claiming to detect a server gaining mutation. Correct: my sketch relied on `requestClass`/flags only. The frozen projection adds `steps` and `repositoryExecution`, and the `server-mutation`/`server-execution` drift checks exercise them. Better than what I proposed.

## 7. Closure of earlier findings (in these bytes)

| Finding | Status |
|---|---|
| 178 F-1 (undefined pre-recovery admission; class definition; circular wait) | **Closed in text**: closed Phase A; both schema descriptions + workflows; hostile-trust vectors show cleanup then `clock-refused`/`freshness-refused`, slot absent, trust-only selector `permit`. Subject to F-1 above for damaged footprints |
| 178 F-2 (forced order admits new transition first) | **Closed**: MUST name `core repair`, says it first completes/aborts the prior operation, "not a claim that repair is harmless", residual stated for all five |
| 178 W-1 / N-1 / N-2 | Closed: S7 row clarified; lineage selectors resolve headings/functions/JSON members and are checked; challenge expiry, reboot and non-copy across migration stated |
| 178 W-2 (prose-only classification) | **Closed at reference level**: companion + schema + selector join + generated table compared to the contract. Product adoption owed (disclosed) |
| my 178 NOTES residual paragraph (workflows l.1679) | Closed: conditioned on a Phase A executor; B/C identities stated |
| 182 F-1 (`carrier-dispatch` "or ledger") | Closed: sentence split; carrier tolerance untouched |
| 182 W-1 (`domainDetail`) | Closed: omitted, sweep "inaccessible" row cited |
| 183 F-1 (policy half) | Closed in identity + readonly: busy keeps its route "independently of which statement encountered" it; corruption error alone authorises nothing. Mechanism is 184 |

## 8. Limits

No executable encodes S9.2.1's Phase A custody, physical retirement, lease release or floor preparation; they are asserted inputs. I did not re-derive S5/S8/S9.1 admission, did not rebuild the owner's six compiled ordering mutants (I ran my own sixteen), and did not check product trees beyond reading the owner's name-check evidence.

## 9. Verdict (bounded)

**The A/B/C order, the no-consent decision, the resting state, the companion and every residual owner correction are coherent and, where executable, behave as written. The D6 "never ABORT after RESTORED" law is not true of the unchanged writer model that the new composition relies on (F-1), and the prepared floor image needs a freshness rule (F-2); T-1 lists four undetected faults, one of which lets Phase C become eligible without the fence.** No cumulative, product or implementation approval.
