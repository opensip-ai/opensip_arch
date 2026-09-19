# Independent bounded review — population contract clarification 151 (reference, prose only)

Reviewer: Claude (actual independent reviewer; Codex remains owner). 2026-09-19.
Request: `population151-20260919-REQUEST.md` (bytes as read: `claude-out/REQUEST-as-read.md`).
Scope: the delta of frozen `population-contract-reference-checkpoint-151` over frozen reference 145 — one paragraph
added to `security-and-lifecycle.md` plus five rebound source-pin manifests. No executable behaviour, no product
installation, no Rust. Scratch only, `-I -B`; no frozen/selected/product edit, commit, push or delegation; no
cumulative approval. As invited, I did not repeat cryptographic corpora: no byte they exercise changed.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 2,066,564 bytes, SHA-256 `2b8e8cab5ffc6bf478ad1c59e5ffba9bf1949c8efebe4ab7ecf9657a31a45e50` = request = `archive-pin.json` |
| Members | 1,358/1,358 regular, length + SHA-256 equal to `subject.json`, checked from the tar before extraction; 0 unsafe, 0 extra; re-verified clean after all runs |
| Candidate pins | 1,287/1,287 equal; nothing under `candidate/` unpinned |
| Parent | `parent-inputs.json` = the 145 candidate pins = **my own** verified 145 extraction, 1,287/1,287 |
| Changed | exactly six, equal to the declared list: the contract (`a2db56b9…16af7` → `25acd5b8…17bfc`) and five manifests; 0 added, 0 removed; the before-image equals my 145 bytes |
| Python | 84/84 byte-identical to 145; the equivalence list is exactly the set of `.py` files |
| Manifests | every changed line is a SHA-256 value: the contract hash (6 places) and the four re-bound sibling manifests inside `evaluator3-source-pins`; all 6,370 path/hash entries across the five manifests equal the bytes on disk |

## 2. Owner lanes, re-run in fresh scratch output (reference order)
envelope 168 + 145 + 6,000 + 1,803 · integration 423 · security 581 · carrier 435 · workflows 2,193 · foundation 231 ·
native 477 + 66 — all exit 0, equal to the owner's counts. (The native lane writes its report beside itself; it wrote
identical bytes — the extraction re-verifies.)

**The new contract bytes are really bound** (`probes/pin-binding.txt`, scratch copy, one byte appended to the
contract): security, native and integration refuse (`sourcePinsValid: false` / `sha256 mismatch` /
`standalone-envelope-check-current-source-receipt`). Foundation, workflows and carrier still pass on their own — they
do not hash this file themselves. That is unchanged 145 behaviour and outside this delta, but it means "five binding
manifests" are enforced by three of the seven lanes, not by each lane that owns a manifest (N-2).

## 3. The paragraph against the executable law
I ran the unchanged `generation_dispatch_reference.dispatch` over a complete small grid
(`probes/dispatch_grid.py` → `dispatch-grid.txt/.json`): predecessor tail {open, `grantGenerationClosure`,
`projectPurge`} × predecessor marker {none, `uncertainTailLoss`, `witnesslessRestore`} × next generation {no rows,
populated} × witness {names 1 at its tail, names 2 COMMITTED, names 2 PENDING1, absent} = 72 cells.

| Sentence in 151 | Executable law | Result |
|---|---|---|
| "the admitted marker is independent of the terminal cause" | line 72: `_closed(predecessor rows) or predecessor in markers` — the marker arm never looks at rows | **exact**: all 16 marked cell-groups are identical across open / closure / purge |
| "a generation ending in … `projectPurge` may therefore satisfy the predecessor condition through its admitted marker" | purge + marker, empty generation 2, witness names 2 → `OK` / `REVERT` (bound), not `REFUSE` | **exact** |
| "without such a marker, the purged generation cannot justify an immediate-next generation" | unmarked purge equals unmarked *open* in all 8 cells and differs from closure in exactly the two empty-next cells, both `REFUSE`; this is the existing owner case `predecessor-projectPurge-is-not-closure` | **exact** for the empty next generation. For a *populated* next generation `dispatch` answers `OK` for every tail and leaves the question to S7.1 admission, as the contract already says (ll. 946–950); the new sentence is that S7.1 rule, and it is the rule frozen Rust 148 implements (my 6,561 real-SQL scenarios: unmarked purged predecessor refused with all eight successor kinds; marked purged behaves as any marked predecessor) |
| "a purged final generation remains readable" | purge, no successor, witness at its tail → `OK`; Rust 148 admits it and reports `ProjectPurge` | consistent — wording, see W-1 |
| "not permission to recreate a purged project, continue a writer, repair history or bypass … witness, custody, lease and execution-authority" | `dispatch` is documented as inert; l. 833 "it grants no new permission"; l. 877 "eligibility to continue never grants an execution permission" | **does not overstate** — every clause is a negation; see W-2 for what it leaves unowned |

The paragraph sits directly after the population-admission paragraph it qualifies and before the
not-migratable rule, which it does not disturb (that rule is about the *highest inherited* marked generation and act
A/C; nothing here lets a marker substitute for a witnessed TERMINAL).

## 4. Findings
No defect and no overstatement of authority. Two wording points and two notes, none blocking.

- **W-1 (low, wording) — "remains readable" is the only undefined term in the paragraph.** Everything else is phrased
  as population admission; "readable" can be read as a promise that a read of a purged project succeeds, which also
  depends on witness, floor, custody and on what purge removed. "remains admissible as the final generation of the
  historical population" says what the law and Rust 148 actually establish.
- **W-2 (low, honest limit) — the disclaimer names a prohibition that has no owner in this contract.** "recreate" occurs
  nowhere else in `security-and-lifecycle.md`, and the executable dispatch is *more* permissive than a reader of the
  new paragraph might assume: for a purged **and marked** generation it returns `continuation-eligible` (witness names
  it, or absent with `witnesslessRestore`) and `OK` for a bound empty generation 2 — identical to a non-purged marked
  generation, because it is cause-blind. Those are inert dispositions, so the paragraph is right that they grant
  nothing; but after 151 the contract says what this state does *not* permit without saying where "may a purged
  project ever be continued" is decided. One clause — naming the owning law, or stating that this profile defines no
  continuation of a purged project — would keep a future writer owner from reading `continuation-eligible` as the
  answer. This is the writer-side twin of Rust 148 T-1 (append stop after a purge terminal), which you report as
  regressed in draft 150; I have not reviewed 150.
- **N-1 (note)** The clarification is prose only, and the reference has no Python population-admission function: the
  sentence about a *populated* successor is executable only in Rust (148). That is a fair division, but it means the
  reference lanes cannot notice if this paragraph and the Rust predicate drift; the 148 owner cases are the binding
  tests for it.
- **N-2 (note, pre-existing)** See §2: foundation, workflows and carrier lanes pass with a modified contract.

## 5. Closure of my earlier item
| Item | Status |
|---|---|
| closure148 **N-1** — "purged + marked may have a successor" deserved a sentence in the contract paragraph itself | **Closed.** The sentence is in the S7.1 population paragraph, states both directions (marked may, unmarked may not), and carries the no-authority rider. No law changed: 84/84 Python identical and the 72-cell grid agrees with every clause. |

## 6. Bounded verdict
**151: reviewed, no blocking finding. The delta is exactly one contract paragraph and its five manifest rebindings;
all executable reference bytes are identical to 145; all seven lanes pass in fresh scratch and the amended contract is
hash-bound by three of them. Each sentence of the paragraph agrees with the unchanged dispatch law over a complete
72-cell grid and with the frozen Rust 148 population predicate, and the paragraph confers no authority — it is written
entirely as admission rules plus negations. W-1 ("readable") and W-2 (no named owner for the purged-project
continuation question, while dispatch stays cause-blind and answers `continuation-eligible`/`OK`) are wording
improvements, not defects.** Not approval of 145's other content, of any Rust candidate, of draft 150, or of any
writer, custody, lease, OS, release or cumulative standing.

Evidence (`claude-out/`): `pin-verification.json`, `pins.py` → `candidate-pins.json`, `diffs/` (six),
`owner/` (seven lanes + `exits.txt`), `probes/{dispatch_grid.py,dispatch-grid.txt,dispatch-grid.json,cause-blindness.txt,pin-binding.txt,pin-binding-FAILED-r1.txt}`
(the FAILED file is my own shell word-splitting slip, preserved), `hashes.txt`.
