**Verdict: ACCEPT-UNIT** for the narrow delta02, with no required findings and 4 new advisories. The guard is sound as a limited, cautious check, not a proof about how Typify names types. Nothing here is promotion, integration or qualification. The review is in `m1-control-generation-review-02/review.json` and `review.md`, and my scripts and results are under `work/`.

**A correction to review01:** it overstated the malformed-bound results. My first TS probe left out `$schema`, like the author's `check.cjs`, so those schemas were refused for the wrong reason (unsupported dialect). My later direct probe only tested `-1n`, `'0'`, `1.5` and the number `0` properly. `true`, `null`, `{}` and `[]` were never tested properly in review01. The new in-tree test now covers them with the dialect set and checks the exact `x-maxUtf8Bytes` error, and it passes. review.json records this correction.

**What I checked:**
- **Subject:** 88/88 files matched before and after, with no symlinks, and no `__pycache__` appeared in any frozen dir. I ran all imports and mutations on copies with `-B` and my own TMPDIR.
- **Outputs and projections:** all 8 output bodies match subject 01 except the header lines, which carry registry `abe989a7…`. The Rust and TS projections are identical for all 587 definitions. Naming changes only the 16 control body titles, and the new guard refuses the projection without them.
- **Workspace:** the 140 pinned TypeScript files are regular files with matching hashes and no symlinks. The node, generator and Python hashes match the closure.
- **Tests and drift:** all 82 tests pass with the pinned Python 3.14 (`-I -B`) and native node, including the UTF‑8 runtime test. Fresh generation shows 8 outputs and no drift.
- **Preflight:** a copy of the live `verify_design.py` refuses subject 02 with "generation source is not selected by accepted design", matching the root's refusal record.
- **Guard probes (39):** differing array properties under `oneOf` or `anyOf` are refused at all 10 schema positions I tried, as are const, enum and title misuse. A private title that clashes with an existing definition or title is also refused. Differing plain strings or integer ranges, `$ref` children and distinct titles pass correctly.
- **Test sensitivity:** 9 of the 10 mutations were caught by their target test. These covered disabling the guard, dropping arrays from the check, removing the reserved-title check, disabling the namer, and four ways of breaking the UTF‑8 rule.

**One mistake of mine:** my first test, mutation and generation runs used the system `python3`, because I had cut PATH down to `/usr/bin:/bin`. Generation refused, discovery errored, and every mutation baseline failed. I threw those results out and reran everything with the pinned interpreter. review.json records this too.

**Advisories:**
1. **D2A1:** one mutation survived. Letting the same title stand on different shapes isn't covered by any test, although the real guard does refuse it.
2. **D2A2:** four cases get past the guard.
   - A title that differs from a definition name only by case.
   - A private title that matches a name Typify would derive for an untitled property elsewhere.
   - Differing `allOf` siblings.
   - Properties nested inside a branch `allOf`.

   None of these occur in the current 587 roots.
3. **D2A3:** the runtime test finds `node` through PATH rather than using the pinned node.
4. **D2A4:** the documented test command should name the exact Python interpreter, since both a missing `-I` and the wrong `python3` make the run refuse.

From review01, CA1 (preflight binding and promotion), CA4 (the Rust carrier is inert and looser than the schema) and CA5 (stale obligation, untracked route) still apply. CA2 and CA3 are mostly addressed, apart from D2A1 and D2A2.

**Not covered:** I didn't rebuild or re-roundtrip Rust, because the carrier bodies are byte-identical to review01's. The adapter04 confinement algorithms, control/native/report semantics, source promotion and integration were also out of scope.
