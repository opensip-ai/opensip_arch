# Independent review: coverage source binding

You are Grok, the user's explicitly authorized independent reviewer. Codex
remains implementation lead and will reproduce your findings. Prior requirements
to wait for Claude do not block this authorized Grok review. Attribute your own
work accurately; do not claim a Claude review or whole-product acceptance.

Review the frozen subject in
`/tmp/opensip-implementation/m1-grok-coverage-review-01/subject` against its
adjacent `subject-manifest.json`. Verify its manifest hash and every file before
review, and again at completion. The caller supplies the exact manifest hash in
the task message. Do not modify the subject, historical evidence, either repo,
or external pinned owner sources. You may write tests/results and a runnable copy
under `/tmp/opensip-implementation/m1-grok-coverage-review-01/review/` only. The
subject's existing check script writes files beside itself, so execute it only
from a private copy. Use Python `-I -B`; compile source bytes directly instead of
trusting bytecode caches. Do not run save_checkpoint.py.

Product repository: /Users/sb/code/opensip-ai/opensip
Architecture/evidence: /Users/sb/code/opensip-ai/opensip_arch
Python: /tmp/opensip-implementation/metadata-reference-env/bin/python

This bounded review concerns the executable reference correction and its
standalone schema, source identity/admission boundaries, selection/prefix rules,
refusals and conditional budget estimates. It is not product storage, final
Report1 integration, a browser adapter, release qualification or final source
selection. Those explicit pending duties are not defects merely because they
are pending. Flag a scope limitation if it makes a claim in this subject false.

Read README.md, correction.json, coverage_source.py, the standalone schema,
prepare.py, check.py and measure_integration.py. Inspect the actual pinned native,
identity and report owners needed to judge the change. Do not trust comments or
supplied pass counts as proof. Run the reference checks in a private copy and
construct your own meaningful counterexamples, particularly wrong source joins,
self-consistent wrong identities, lost/corrupt records, non-prefix selections,
source mutation, shape-vs-native authority and misleading empty results. Check
the conditional byte/depth estimates against the actual estimator and schema.

Provide a substantive verdict (ACCEPT WITHIN STATED REFERENCE SCOPE, or
CHANGES REQUIRED). Separate must-fix defects, justified should-fix findings and
advisories. For each actionable finding include exact file/line, trigger,
reproducer, observed/expected result and reason. Include commands executed,
limitations and verification of frozen bytes. Do not change the implementation
yourself or start other agents. Save review.md and any reproducer/test results
under the review directory, then summarize your verdict in this terminal.

Start now; no further user confirmation is needed for this read-only review and
its isolated tests.
