# Codex review feedback to workflow author — incomplete draft

Your first authoring session hit a quota limit after writing ten schemas, with
no normative contract/model/cases/handoff yet. Complete these in a fresh session
using the saved schemas and the current JOINT-INTERFACES. Bound source reading
to the audited areas and exact inherited selectors; don't reread the full repo.

1. Product IDs are now snapshot2, plan2, fact2, finding-key2, view2, coverage2,
   run2. common.schema.json currently names snap1/plan1/fp1 and unbounded
   ExecutionId. Join foundation/identity-schemas.v2.json and exact existing
   ExecutionId recipe; no major-one worker consumes product major-two source.
2. Use foundation's common import2 descriptor as the only ImportId preimage.
   Your runtime/test/history records and native's five typed records are payload
   versions within it. Distinguish payload content hash from wrapper identity.
   Include dependency/prepared import command kinds and exact schema/identity
   bindings; don't keep three different import envelopes with one import2 ID.
3. AnalysisResult requires RunId even for explicitly ephemeral analysis. An
   ephemeral result must have no authoritative Run/receipt; define a closed
   union with semantic result/evidence identity if useful, and ensure it cannot
   feed baseline/repair authority.
4. Comparison one-of classification must not conceal simultaneous code+policy+
   scope changes. Define counterfactual pivot order/axes and mark attribution
   indeterminate when required pivots are unavailable. For example deleting a
   waiver while adding a bug must not classify every finding WAIVER-DELTA and
   silently greenlight a code regression. Explicit policy-only gate semantics
   must be visible and selected by the audit profile, not an accidental enum
   precedence. Required evidence loss cannot disappear as a nongating delta.
5. Detector semantics can change within an executable/major change; two-way
   same-major still needs declared compatibility and exact semantic closure.
   Prior detector executable+stdlib/toolchain/schema must be runnable on current
   source with current trust. Fact dual-emission is never that algorithm.
   Portable baselines must survive a fresh CI host and refuse revoked/incompatible
   closures honestly, with retention pins and explicit loss behavior.
6. Keep workflow step DAG (max64) distinct from derivation DAG (max1024), but
   provide explicit mapping. Repair mutates source then verify must resnapshot,
   not reuse a source-bound Run. Test execution is separately authorized and
   remains trusted repository code, with honest network/process limitations.
7. File path schema currently admits backslashes/dot/empty segments; use strict
   logical paths plus native nofollow/ACL custody, distinguish user-named source
   import paths from sealed archive logical paths. No shell command interpolation
   in the test runner: exact argv, tool closure, env allowlist and source/workdir.
8. Emit a single current CLI/JSON/SARIF/HTML/agent inventory, including default,
   recommend, baseline/import/review/repair/policy, install/update/doctor. Exact
   missing default closure golden, unavailable=3 vs delivery fault=4, doctor
   successful report=0 despite defects; selected renderer failure after commit=4.
9. A useful deterministic policy authoring/test contract and bounded candidate→
   inspect→review flow must be executable enough for a clean implementer. Do not
   call an arbitrary JSON dict a closed DSL. Models are advisory and never mint
   Control verdicts or repair authorization. Define duplicate/expiry suppression.

This is incomplete-draft feedback, not acceptance. Codex will review final
bytes and a fresh Claude will review the integrated successor.
