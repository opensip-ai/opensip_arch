I agree with root's direction and have fixed it. An incoming dependency covering only some source subjects can no longer make incoming answers complete, while all the partial evidence is kept. This is authorship only; the independent assessment and root's reconciliation remain.

**The defect.** Each dependency relation gets one slot in the sufficiency view, filled by whatever matching dependency partitions exist.
- **Outgoing** checks a single subject, so a filled slot always covers it.
- **Incoming, per scope,** checks the whole primary scope, so f's calls partition alone filled the slot for {f, g}.
- **The whole-source attestation route** did the same, which I measured (f only → `true`).

On the previous model, merged {f, g} with only f's dependency answered `none=true`, `count≤1=true` and `all-covered=true`. Splitting the same subjects into {f} and {g} gave unknown, so grouping alone changed the truth.

**The rule, published in §4 as "Dependency totality":**
- **Owed subjects of a view:**
  - outgoing: the current subject;
  - incoming per scope: that scope's subjects;
  - attestation view: the subjects of the provider's owned scopes.
- **Covered:** a subject is covered when an exact dependency scope contains it and pairs at least one Coverage at the exact target.
- **When any owed subject is uncovered:** the actual view is kept as is. Native sufficiency runs on it and again on the same view with that dependency slot removed, which answers `required-relation-missing`. Both answers are kept, and the view is satisfied only if both are.
- **Nothing is invented:** no Coverage, scope or cause is created for the missing subject, and `coverage-unknown` keeps the actual view's `nativeCause`.

I rejected three other ways to represent the gap:
- **Dropping the slot** would lose f's real deficiency and carrier.
- **Forcing the folded entry to unknown** would rewrite real evidence.
- **One view per subject** multiplies evaluations and causes for no gain.

Two choices could reasonably go the other way:
- **Attestation owed set:** I used the owned scopes' subjects rather than the inventory population.
- **Different-kind dependencies (clones→declares):** these stay whole-source and unchecked, because file and symbol subjects need a containment map this layer doesn't have.

**Results (synthetic atom API only; no Run reachability claimed):**
- **Now unknown with `required-relation-missing`:** all six ways of leaving g uncovered (including a scope without Coverage, the wrong target or universe, or only an unrelated partition). f's Coverage stays cited.
- **Still true:** full covers.
- **Merged vs split:** now give the same value and causes.
- **Outgoing:** every row unchanged.
- **Partial carrier:** `input-closure-incomplete` and `lockfile-missing` survive, with `required-relation-missing` added.
- **Known facts:** `exists`, `none` and `count≤0` keep their results; `count≤1` and `all-covered` now need totality.
- **Attestation f-only and synthetic depth-2:** now unknown.
- **Order independence:** 48 insertion orders give one result.
- **Empty-subject scope:** unchanged.
- **Previous-model vs corrected-model diff:** 47 changed cells across the probe matrix, listed in `review.json`.

**Checks.** 101 of 101 pass. The original 95 passed on the corrected model before I added anything, and none of their expected results, fixtures or assertions changed. All six new checks fail on the previous model and pass on the corrected one: regrouping, missing subject plus full cover, partial carrier, known facts and bounds, attestation route plus ordering, and synthetic depth-2. The seven downstream checkers exit 0 with identical output on both trees. I did not run the integrated groups or pin sealing.

**My changes** (dependency-scope successor → this tree):

| File | Change | Lines |
|---|---|---|
| `atom_model.v1.py` `2c5fdabb…` → `4477285c…` | new `_dependency_totality_gaps`; `run_suff` checks the reduced view; three call sites | +56/−6 |
| `atom-evaluation-contract.v1.md` `72986bd3…` → `2d399ec9…` | §4 totality rule and §9 case | +32/−1 |
| `check-atoms.v1.py` `67d8c656…` → `ebb9da8c…` | 6 new checks, no existing line changed | +173/−0 |

Against frozen35, cumulatively with my earlier dependency-scope delta, the changes are +33/−2, +68/−18 and +364/−0.

**For root.**
- **Pins:** reseal the 15 stale pin rows; no new pin is needed.
- **Other owners:** no change is required from any other owner.
- **Planned prose alignments:** I did not implement `historySubjectOrder` or the runtime-polarity wording.
- **Your preparation runtime:** you added five files to `root-source36-preparation.v1` while I worked; I didn't read them.

My first probe run was contaminated because I inventoried h without any scope containing it. That run is kept as a receipt and the probe was rerun.

Files are in `/tmp/opensip-design-corrections/claude-dependency-totality-author.v1/`:
- review.md
- review.json
