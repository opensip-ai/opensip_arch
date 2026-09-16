This is a real gap. The schema that defines the public termination record (StepTermination) accepts cause and code combinations that the retained D9 law forbids. No other check rejects them, and nothing in the owner docs says the schema was meant to check shape only. Every piece of code that builds terminations today builds lawful ones; the gap is that the published admission rule is weaker than the law it claims to keep.

**What I found in candidate37**
- **Root's result reproduces, and the gap is wider.** 13 combinations break the retained D9 law. All 13 are accepted at all seven places that reference StepTermination: both common schemas, both command-envelope majors, the graph-query response, and both invocation-record step results.
- **No other gate enforces the law:**
  - `exit_code` only looks at the class.
  - `validate_envelope` only checks that the envelope matches its evaluator-fault route.
  - `validate_pinned_purge_refusal` only checks purge fields.
  - `render` only projects fields.
  - The §8 query rule only requires the response termination to equal the enclosing one.
  - No import kind or retained Run record carries a termination.
- **Why it isn't intentional:**
  - Workflows line 66 says StepTermination replaces the D9 union's field rules ("no undeclared D9 field is admitted") and that "Class/code/exit legality remains retained". It names no other place that enforces it.
  - §9 calls the branch rules "(schema-enforced)".
  - The D9 union being replaced refused reasonCodes on every class except indeterminate. The current schema accepts them.
- **Producers are lawful:** `terminate`, the evaluator-fault routes, native `public_termination_for` and the host `public_termination` emit no illegal termination.
- **One host observation:** `public_termination` silently drops a code supplied with a success outcome. It also passes request-rejected with fault-family codes.

**Dispositions**
- **R1, required:** faultCause may appear only on operational-failed, and reasonCodes only on indeterminate. The law is D9 codeDerivation plus cross-axis invariants X1, X3 and X4.
- **R2, required:** on operational-failed, faultCause must match errorCode through the 11-entry fault map, including host-invariant → `SYSTEM.OUTCOME.ILLEGAL_STATE`. Only the new carrier publishes both fields, so a mismatch contradicts itself under the D9 code maps.
- **A1, advisory:** limit request-rejected errorCode to the D9 rejection codes. This was always the host finalizer's derivation job, so I left it out of the diff.
- **A2, advisory:** `public_termination` should refuse a class/code the law forbids instead of dropping or passing it.
- **A3, advisory:** add a check that the workflows and evaluator3 StepTermination definitions stay identical.

**Proposed edit** (`proposed-edits.diff`, applied only to my disposable copy)
- **Schemas:** the same branch constraints for R1 and R2 in both common schemas, plus one sentence in the description.
- **Controls:** 12 new reject vectors in `workflow-cases.v1.json`, and a `check_workflows` check that the schema's fault pairs equal `FAULT_TO_ERROR`.
- **Prose:** one sentence in workflows §9. Native §10 is unchanged.

**Checks on the edited copy:** all 12 gates passed.
- All 13 illegal combinations are now refused at all seven sites, while every lawful control still passes.
- What the producers emit is byte-identical to before and lawful.
- The termination and envelope vectors behave as intended.
- None of the 52 termination-shaped fixture objects changes result.

**Digest consequence**
- The raw digests of both common schemas change, so owners would need to regenerate:
  - the five source-pins ledgers;
  - `workflows-report.v1.json`;
  - any rebound package manifest.
- Pins for the other three changed files would also move; I didn't locate those.
- The registered payload schema digests don't change: no registered payload document references StepTermination.
- Nothing retained in exports changes either: no retained Run or import payload contains a termination.

**Limits**
- I ran no group or global suites. The new control and vectors were reproduced in my own probe, not run inside `check_workflows`.
- I regenerated no pins.
- The legality predicate is my own transcription of D9, always reported beside the actual result.
- The fixture scan covers JSON files only.
- I didn't assess signal on operational-failed.
- The frozen source is unchanged, and no background process was started.

**Kept failures**
- **p00:** exited 1 because it matched manifest pins by path suffix, which caught copies under `reviews/`. p00b redid the match by exact path and passed.
- **p01, first run:** exited 1 on a type error in my fixture scan. I fixed the guard and the rerun passed.

Files are in /tmp/opensip-design-corrections/claude-source37-termination-boundary-assessment.v1/ (probes and receipts are in the same folder):
- assessment.md — SHA-256 7ad6095a…
- assessment.json — SHA-256 cb98d2c9…
- proposed-edits.diff — SHA-256 a2e3a27a…
