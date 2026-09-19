# Independent bounded review — clock reference follow-ups 138

Reviewer: Claude (actual independent reviewer; Codex remains implementation/decision owner). 2026-09-19.
Request: `clock138-20260918-REQUEST.md`. Scope: the delta of frozen `clock-followups-reference-checkpoint-138` over
frozen 137 — the corrections of my clock133 review: T-1(a–d), N-1, N-2, and the reference half of clock134 T-2.
**Reference only**: no adapter, renderer, storage or Rust claim (Rust regressions are 139). No frozen/selected edit;
scratch copies only (`-I -B`, 0 stray `.pyc`); no commit, push or delegation; no cumulative approval.

## 1. Subject verification (before use)

| Item | Value |
|---|---|
| `subject.tar.xz` | 2,177,348 bytes, SHA-256 `4029b7f0b87f6a51b96a1ef9848f956c5f5b05d28f99e3830fe974c150948cf1` = request and `archive-pin.json` |
| Members | 1,458/1,458 regular, length + SHA-256 equal to the manifest, from the tar before extraction; 0 unsafe/extra; re-verified clean at the end |
| Candidate pins | 1,287/1,287 equal; none unpinned |
| Parent | `parent-inputs.json` equals **my own** verified 137 extraction and its `frozen-candidate.json` |
| Changed | **12**, none added: model, `clock_range_checks`, both workflow `common` schemas, `check-integration.py`, contract, six pin files. The lifecycle schema file is byte-identical to 137 |

## 2. Owner checks, fresh scratch, required order
envelope → integration 423/0 → security 581 + 24 sweeps (range sweep now **264** checked, 43 cases) → carrier 435/0 →
workflows 2,159/2,159 → foundation 231/231. All exit 0.

## 3. What changed (complete diffs read)
One module-level map `CLOCK_RANGE_REMEDIES` now supplies the kernel's remedies, and `CLOCK_RANGE_SUBJECTS` is derived
from its keys — so the public subject set is exactly the three clock operands. `public_details` additionally refuses
a remedy that is not the map's entry for the tag (`CLOCK_RANGE_REMEDY`). Both workflow schemas bind, for this one
code, subject ∈ the three tags and remedy = the literal text per tag. The kernel's range logic is untouched.

## 4. Evidence

**No behavioural drift.** My 133 randomised probe re-pointed at 138 (120,000 evaluations): the outcome table is
**identical to 133** (22,173 proceed / 49,200 ordinary refusals / 48,627 range refusals), 0 violations against my
oracle and the counterfactual rule; the 16 edge/priority cases and the 9 recovery-guard cases are identical too.

**Schema binding, both majors** (`schema_probe.py`): the three lawful (tag, remedy) pairs validate; `recovery-result`,
a timestamp subject, a missing subject, a retained subject carrying the *presented* remedy, the right remedy plus one
space, and a free-form remedy are all **invalid** in legacy and in evaluator3; another code keeps its free-form remedy.
The three literal remedies occur in both schema files. `enums == registry` still holds (321).

**My 133 mutant set re-run unchanged against 138's mandatory checker** (+3 new; first attempt died on a quoting error
of mine, log kept): **17/17 distinct mutants killed** (8 by a named failing check, 8 because the mutated model raised or its output was refused by a schema inside the checker, 1 — the mis-anchored one — run separately; my old remedy mutant and its replacement turned out to be the same mutation and count once).
In particular the four 133 survivors are now killed by named checks:

| 133 survivor | 138 |
|---|---|
| T-1(a) recovery guard tests the wall instead of `issuedAt` | killed — `recovery-issued-not-wall-range-operand` (straddles in both directions) |
| T-1(b) wrong remedy for the retained tag | killed — schema `const` refuses the model's own output |
| T-1(c) `public_details` accepts any subject | killed |
| T-1(d) `iso()` clamps | killed — `iso-no-clamp-…` direct assertions outside both endpoints |
| new: projector stops checking remedy-belongs-to-tag | killed |
| new: `recovery-result` re-admitted as a public subject | killed |
| new: one remedy loses "Nothing was written." | killed |

## 5. Closure of clock133

| Item | Status |
|---|---|
| **T-1(a)–(d)** | **Closed** — each property now has a named check, and each of my four mutants dies |
| **N-1** public subject set one wider than the clock | **Closed** — three subjects in model, projector and both schemas; `recovery-result` refused by projector and schemas; the contract now calls it a descriptive Rust-internal label |
| **N-2** projection did not tie remedy to tag | **Closed** — projector check plus per-tag schema constants |
| clock134 **T-2** (reference half: inclusive continuity maximum) | covered — symmetric exact-inclusive case in both report modes; my exclusive-maximum mutant was already killed on 133 and still is |

## 6. Findings
- **N-1 (note) — three copies of each remedy string.** The text now lives in the model map and as a `const` in each
  workflow schema. Drift is *detected* (changing the model text makes the model's own output schema-invalid — that is
  how two of my mutants died), which is the important property; it is not *prevented*. If the generated Rust/TypeScript
  consumers will carry the strings as well, generate all copies from one source at selection time.
- **N-2 (note)** The owner's disclosed harness correction (the first inclusive-continuity case expected the wrong
  outcome for a 2026 wall with a 9999 anchor) is consistent with what I measured on 133: that state is an ordinary
  in-session excursion, and the inclusive edge needs the wall at the maximum. Production logic was not changed —
  confirmed by the identical 120,000-row table.

No defect found.

## 7. Bounded verdict
**138: reviewed, no finding against the delta. All four unpinned properties of clock133 T-1 and both notes are closed:
the kernel behaves identically to 133 on 120,000 randomised evaluations, the public subject set is exactly the three
clock operands, subject and remedy are bound per tag in the projector and in both schema majors, and 17/17 of my
mutants — including the four that survived 133 — are killed by named checks.** Reference only; not approval of an
adapter, renderer, storage, Rust, OS, release or any cumulative standing.

Evidence: `claude-out/pin-verification.json`, `candidate-pins.json`, `diffs/`, `owner/`,
`probes/{range_probe.py,range-probe.json,range-probe.log,route_probe.py,route-probe.json,route-probe.log,schema_probe.py,schema-probe.json,mutation.py,mutation.failed-r1.py,mutation.FAILED-r1.log,extra138.py,mutation.json,mutation.log}`, `hashes.txt`.
