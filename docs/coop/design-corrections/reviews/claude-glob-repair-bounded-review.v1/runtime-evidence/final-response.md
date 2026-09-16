Both tasks are complete. `review.md` and `review.json` are written; all inputs are byte-unchanged.

## Task 1 — Glob: **no semantic mismatch found**

Inputs bind cleanly: the successor tree is frozen31 plus exactly the five declared changes (1,346 files byte-identical), and every `beforeSha256` equals frozen31.

The decisive check was to test the stated goal directly. I implemented the predicate **from the contract prose alone** and differential-tested it against the unchanged `workflows_model.v1.glob_match`: **5,927,922 pairs, zero mismatches**, all 22 documented examples and all 28 named edge cases agreeing. The law is genuinely reconstructable without source code, and it preserves existing behaviour — no new dialect.

Both schema edits are annotation-only (`+0/−0` leaves, one changed description each), so admission is untouched; `matcherAlgorithmChanged: false` is structurally true. Everything you named checks out, including both directions of the scalar-vs-grapheme case and the astral-scalar case.

Two things worth your attention:

- **The callers genuinely differ** on absent/empty `include` — `in_scope` selects nothing, the enumeration filter treats it as no restriction. That is *not* a contract defect: the contract scopes its composition rule to ScopeDocument and explicitly defers absent/empty-list behaviour to other owners. That deferral is exactly what stops it becoming a second dialect.
- **The one apparent mismatch is not one.** `cmp: glob` dispatches as `glob_match(x, str(v))`, so the caller coerces. I validated every field in both policy-document schemas: `glob` is **inadmissible** on both integer-valued fields, so `str()` is a no-op under any admitted document and the contract's "neither coerces values" is accurate.

Atom checker: 70/70 in my runtime, with exactly 30 prescribed vectors all agreeing with the unchanged reference. I confirmed the declared pin-refresh item (20 ledger entries would refuse) and did **not** report the deferred workflow links as a gap.

## Task 2 — Repair ownership

**RRS-A1 is confirmed.** The frozen31 enumeration owner retains program-to-path ownership independently of source-path scopes — decisively at line 125: *"Symbol extent is owner-admitted `programRootFiles` / syntax code suffixes / rust `sourceUnitOwnership` selected paths… Unavailable-program symbol extent is the membership-fallback code extent"* — plus L24 `extents[]`, L26 `candidateSourcePaths`, and L28 where an **unavailable** binding keeps extents populated with `universe=null`.

The structural proof is blunt: the captured selector contains **zero** occurrences of `extents`, `candidateSourcePaths`, `EnumerationPlan` or `programBindings`. It reads only `subject_scopes()` filtered to `{clones, file, vcs-change}`. My unit-scoped probe shows universeB omitted in the asymmetric case, with controls both ways. **No full-Run counterexample was constructed and none is claimed** — the evidence class is static normative completeness plus that unit probe, matching root's own stated scope.

**RRS-A2: all five requests are well founded** — four unmet, one partial. Three I reproduced directly: the create-only paragraph says "fixed all-unknown value" while the sentinel is `entryPointsRecognized: none` / `nonliteralLoading: present` (wrong on 2 of 5 fields); module line 87 does call the display boolean "authoritative"; and two records differing in `targetUniverse`, `subjectScopeCommitment` *and* coverage identity produce **byte-identical** remedy text. The ordering point is a publication gap over already-correct behaviour — the code sorts by encoded bytes, but UTF-8 ordering is named nowhere in prose and the published key has five members, not the six requested.

This grants nothing: not architecture ready. Integrated freeze, final independent source review, blind reconstruction and application review all remain.
