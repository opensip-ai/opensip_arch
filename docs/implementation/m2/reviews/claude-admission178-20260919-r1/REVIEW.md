# Independent review — frozen `transition-scope-reference-checkpoint-178`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: exactly the frozen 178 reference bytes (policy text in five owners, model comments/one emitted literal, one schema title, manifests). Separate from my 176 and 177 reports. My 175 findings and my 173 proposal are not acceptance of these bytes. No host, custody, retirement, mapper, cumulative or authority approval. 179 is unfrozen and unread.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `2f979154eed887709c2e34d59957ef3d4dc299d7a7244c2035df35d31a0aaf14`, 2,243,036 B = request = `archive-pin.json` |
| Members | 1,436, all regular/safe, verified from the tar before extraction; re-verified at end (`claude-out/pin-verification.json`) |
| Candidate pins | 1,289/1,289 (hash and size); none unpinned; declared change list equals computed (`claude-out/candidate-pins.json`) |
| Parent | equals **my own verified 175 extraction**; 13 changed, 0 added/removed: four owner docs, `store-instance-lineage.v1.json`, lifecycle model, lifecycle schema, envelope model pin, five manifests |
| Python | 86; 85 unchanged; changed only `security_lifecycle_model_v1.py` |
| Observer / 43 vectors | `readonly_transition_reference.py` and `transition-journal-cases.v1.json` byte-identical to 175 |

## 2. Owner checks re-run (reference order, `-I -B`, fresh outputs, `claude-out/owner/`)

envelope (168 + 145 + 1803 + 61 crypto + 6000 fuzz) → integration 423 → security → carrier 435 → workflows 2193 → foundation 231 → native 477/66: **all seven exit 0**; no bytecode left in the tree.

## 3. "Action-equivalent model" claim — confirmed, by a stricter check than claimed

`claude-out/probes/ast_equiv.py` strips docstrings and normalises **nothing**, then diffs the full ASTs: **exactly one differing node**, the `'recovery'` string constant in `admit_transition_journal`'s base result (old/new text equal to the owner's `model-action-equivalence.json`). The schema's `recovery` property is an unconstrained string, so no consumer validates the old wording; no copy of the old literal remains in the tree. The owner's honesty note (output bytes do change) is accurate.

## 4. Closure of my 175 findings

| 175 | Status in these bytes |
|---|---|
| F-1 lineage A6 fact, model comments, emitted string, schema title | **Closed.** All four now say "admitted executor, journaled operation, before its new transition admission". Tree-wide scan for `first act under`, `next fence`, `every/all other/any mutating`: every remaining site is qualified (S7 step 4, S9.2 crash-recovery heading, readonly §, lineage A6) — `claude-out/io/residual-rule-scan.txt` |
| F-2 SC-TRUST-only operations blocked with no remedy | **Decided** (owner choice, assessed in §5) |
| W-1 meta commands | Closed: outside the table, stated in security and workflows owners |
| W-2 shared authorization class recovers foreign operation | Stated in S9.2 and workflows — **but see F-1 below: the class's own definition was not touched** |
| W-3 per-mode classification | Closed in prose: `repair recover` inspection = reader, `--apply-recovery` = nonexecuting mutator, `doctor` report-only in both modes |

Classification exhaustiveness (`claude-out/probes/classify178.py` → `io/classify178.txt`): all 45 inventoried commands land in exactly one of six dispositions using only rules the text states — 5 executors, 4 trust-only, 19 other mutators, 10 readers, 3 report-only, 3 meta; `repair-recover` is placed by the explicit per-mode sentence.

## 5. Policy assessment requested: does the trust exception preserve retirement without implying freshness or authority?

**Retirement invariant — preserved.** The invariant's purpose is that no registration/project mutation can leave a terminal journal behind, which is what makes the reader's "current registry == frozen registry" test sound. The four commands take the fence and no project lease (S7 row), write SC-TRUST only, and register nothing; terminal recovery by a later executor is release-only and reads registry + leases, never SC-TRUST. The amended soundness sentence in `commit-recovery-readonly.v3.md` step (terminal) now carries exactly this argument. I found no path by which a trust-only command changes an input of `recover_transition_journal` or of the reader's observer.

**No implied authority — preserved.** Every site says the barrier "permits only the command's ordinary SC-TRUST admission"; `recovery-authority-quorum`/consent classes are untouched in the inventory.

**No implied freshness — stated, and the rationale for the nonterminal block is real**, not arbitrary: S15 says trust refresh/import do not bypass "current-core profile-set admission", and a nonterminal core transition is precisely a pending profile/selection change. Because readers and all other mutators are also busy in that interval, stale trust cannot produce verdicts meanwhile; only report-only surfaces run.

So the choice is coherent on its own terms. The problem is at the other end of the remedy it relies on:

## 6. Findings

### F-1 (medium, policy coherence across owners) — what "admitted executor" means *before* recovery is undefined, and the class's owning definition contradicts the new order
178 introduces a two-step order: "Once admitted to that class, an executor recovers whatever operation is in the active journal, using its frozen affected set, **before admitting the requested new transition**." But:

1. The owner of the class — `workflows/schemas/command-inventory.schema.json` (and its `evaluator3` copy), unchanged — defines `core-transition-leases` as "installation fence plus the S7 affected namespace EXCLUSIVE set, **derived from the admitted intent** and installation registry; same-schema core update/repair require the fence alone". Workflows l.1663 says the same. Under that definition class admission *is downstream of* new-intent admission, and a `core repair` holds "the fence alone" — yet 178 has it re-acquire a journaled migration's every-namespace EXCLUSIVE set.
2. The new intent cannot be projected before recovery at all: `preconditionGeneration`, `from*Generation` are host-observed and recovery (`RESUME-COMMIT`/`ABORT`) changes them.
3. S9.2 still says "ordinary command/security admission must **already** authorize the required S9.2 recovery actions", and the table says recovery runs "only with the required ordinary authorization; then continue the requested command's admission" — admission on both sides of recovery, with no statement of which predicates sit where.

Why it matters for the 178 decision specifically: S15 resolves update/rollback VERSION "under current trust" and repair selects the "signed core closure"; trust documents expire and a floor ahead of the wall "heals only by S4.5" — i.e. by `trust recovery-challenge/import`, which 178 blocks on a nonterminal slot. If *any* SC-TRUST-dependent predicate is read as part of the pre-recovery "ordinary admission", then {nonterminal journal + expired/floor-ahead trust} is a circular wait: trust commands wait for an executor, the executor waits for trust. "`core repair` has no initial rollback-time predicate" answers the rollback-window dependency only, not this one. The README's "not unconditional success" disclaimer covers refusals, not a cycle.
Remedy (owner's to author; one rule, stated once in S9.2 and referenced by the class definition): the pre-recovery gate is closed and SC-TRUST/time independent — command ∈ the five, its explicit invocation/consent, fence held, registry equal to frozen, exact journaled lease set re-acquired; nothing derived from the new intent. The new intent is projected and admitted only after durable retirement, under the same fence, and its refusal leaves the slot absent (so trust recovery can then proceed). Then amend the class description: lease set derived from the *journaled* intent for recovery and from the *new admitted* intent afterwards. A reference vector pair (expired trust + `COMMITTED` journal → executor recovers, new admission refuses, slot absent) would make it executable.

### F-2 (low-medium) — the freshness cost is described as "delay", but the forced order admits a *new transition* ahead of the blocked trust update
Because the executor continues to its own admission under the same fence, a user holding a revocation cannot apply it before the remedy command's new transition is admitted: `trust import` is busy → `core update X` recovers, retires, **then admits update X against the pre-revocation trust state** → only then can the revocation be imported. The text promises "never silently claim freshness in the interval", but the interval includes that new admission. Naming `core repair` (same closure) as the entry to request is the right mitigation, yet it is "may identify", and nothing stops the other four. Options for the owner: state that blocked trust output MUST name `core repair` specifically and why; or state this residual explicitly next to the accepted cost. No new command is needed.

### W-1 (low) — S7's fence-only row lists "ordinary payload import" as an entry; the S9.2 table has no row by that name
From S4/S15 I read it as the trust payload carried by `trust refresh`/`trust import` (so: the trust-only row), not the APPEND-WRITE `import` command. With the table now claiming to classify "every invocation that acquires a fence", this S7 phrase is the one fence-acquiring entry a reader must interpret. One parenthesis in S7 fixes it.

### W-2 (low, carried from 175 W-3 in spirit) — the classification is still prose only
"A new command must have an explicit row/category before implementation" is unenforceable: the inventory schema has no active-slot disposition field, the observer has two selectors, and no checker joins command → selector. My probe had to reconstruct the mapping from markdown. A closed `activeSlotDisposition` enum per command (per mode where needed) in the inventory, checked for totality by the workflows lane, would make the four-vs-five-row question mechanical. Host classification is declared owed; this is the reference-side half of that debt.

### N-1 (note) — lineage A6 was re-worded but its `selector` still says "lines 755-789"
Those lines of `security-and-lifecycle.md` are now the read-only observation paragraph, not S9.2 journal/recovery (≈ l.1441–1570). All line selectors in that file appear stale (pre-existing), but A6 is the entry this checkpoint edited.

### N-2 (note) — `trust recovery-import` is boot- and monotonic-window-bound (S4.5)
A nonterminal block can outlast `expiresMono` or a reboot, forcing a fresh challenge round-trip with the recovery authority. This is a concrete instance of the accepted freshness cost worth one clause, since for an air-gapped quorum it is hours-to-days, not seconds.

## 7. Limits

This is a text/policy review plus re-execution of unchanged reference machinery; no executable artefact encodes the 178 decision (observer and vectors are byte-identical to 175), so nothing here can be differential-tested — I checked consistency across owners, the AST claim, classification totality and the lanes. I did not read 179. I did not re-derive the S4 trust-expiry laws beyond the cited sentences; F-1's circular wait is conditional on how "ordinary admission" is read, which is exactly the ambiguity reported.

## 8. Verdict (bounded)

**175 F-1, W-1, W-3 are closed in these bytes; the model-equivalence claim is exact; all seven lanes pass. The trust-only exception itself is coherent and preserves the retirement invariant without granting authority. It is not yet coherent with the executor remedy it depends on: F-1 (undefined pre-recovery admission, contradicted by the class's own definition, with a possible trust/executor circular wait) should be resolved before this policy is relied on; F-2 should be stated.** No cumulative or implementation approval.
