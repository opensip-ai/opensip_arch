# Independent review — frozen `binding-pairs-reference-checkpoint-192`

Reviewer: Claude (independent; Codex remains owner). Date 2026-09-19. Review dir: this directory only.
Scope: exactly the frozen 192 reference bytes — one test module widened to close my 190 T-1′. No fresh claim about production or reference algorithms is made by the owner, and none is reviewed beyond confirming they are unchanged. No host, product or cumulative approval.

## 1. Identity verified

| Item | Result |
|---|---|
| `subject.tar.xz` | SHA-256 `64f96711a4fbd7cac642f3e83f2e049b0bbf1bb813b0574a1d59a301f6af7fef`, 2,067,764 B = request = `archive-pin.json` |
| Members | 1,378, all regular/safe, verified from the tar before extraction; re-verified at end |
| Candidate pins | 1,299/1,299; none unpinned; declared change list equals computed |
| Parent | equals **my own verified 190 extraction**; 6 changed: `store_transition_checks.py` and five manifests; 90 of 91 Python files byte-identical; model, selector, observer, schemas, SQL and all owner prose among the unchanged pins |
| Behaviour unchanged | my `sweep`, `binding` and `phasec` probes re-run on the 192 tree are **byte-identical** to my 190 (and 188) outputs |

## 2. Owner checks re-run

Reference order, `-I -B`, fresh outputs: **all seven lanes exit 0**; integration 1,787 checks / 0 failed (my run). Focused modules through the loader: 1,361 checks, 0 failed.

## 3. The change

Three lines: the stale-revision loop iterates `itertools.permutations(S.TRANSITION_STATES, 2)` instead of one fixed earlier state per current state, and each check id carries both states (`…stale-revision.<operation>.<state>.bound-<other>`). The fixture is unchanged otherwise — still a healthy, fenced footprint, so nothing but the binding can refuse.

## 4. Coverage, enumerated (`claude-out/probes/coverage.py` → `io/coverage.txt`)

From the ids the module actually emits: **120 stale-revision checks, 120 distinct, all passed**; for each of `store-migrate`, `store-rollback`, `core-update`, `core-rollback` the pair set equals **all 30 ordered pairs of distinct states**, with no self-pair. Forward and ancestor selection are both represented, through a store command and a core command each.

## 5. Closure of 190 T-1′, by re-applying the faults (`claude-out/probes/mutation.{py,json,log}`)

Baseline 1,361 / 0 failed.

| Mutant | 190 | 192 |
|---|---|---|
| stale reference accepted when it names the `PREPARED` revision or later | survived all 1,265 | **KILLED** (80 failing checks) |
| immediately preceding revision accepted, `COMMITTED`/`DONE` journals only (the torn-write shape) | survived all 1,265 | **KILLED** (8) |
| eight **single-pair** mutants — accept exactly one (journal state, bound revision): `COMMITTED←PREPARED`, `DONE←COMMITTED`, `PREPARED←PREPARING`, `ABORTED←PREPARED`, `LEASED←DONE`, `PREPARING←ABORTED`, `DONE←ABORTED`, `ABORTED←DONE` | — | **all KILLED**, each by exactly 4 checks (one per family) |

The single-pair results are the sharpest statement of the coverage: the narrowest possible fault of this class — one pair — is caught, in every family.

## 6. Findings

None. 190 T-1′ is closed.

One observation, not a finding: the test now encodes the law as "no revision other than the current one", which is what the protocol says ("exact current journal reference"). It deliberately does not distinguish earlier from later revisions, and should not — a binding naming a *later* state than the journal is as incoherent as an earlier one, and both directions are covered (e.g. `LEASED←DONE`).

## 7. Limits

A test-only checkpoint over a pure reference. The atomic journal+binding publication that 190 made a host prerequisite is still asserted, not exercised. I ran 10 of the 120 possible single-pair mutants plus the two range mutants; the enumeration in §4 is what shows the remaining 110 are covered by construction.

## 8. Verdict (bounded)

**Complete: 120 of 120 ordered distinct-state pairs across the four changed-store families, both of my 190 survivors now killed, every single-pair fault I tried killed once per family, all lanes green, and recovery behaviour byte-identical to 190.** No host, product or cumulative approval.
