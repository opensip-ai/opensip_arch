Perform a fresh independent review of the OpenSIP developer design-lock v2 implementation. Use your own reasoning and executable adversarial probes. You are actual Claude; do not delegate or use prior session memory. Product qualification and full M1 are out of scope.

Frozen subject: /tmp/opensip-implementation/m1-successor-subject-01
Manifest: /tmp/opensip-implementation/m1-successor-subject-01.json
Manifest SHA256: 3fabfe4759fb6555813a05d54e9f99e5f2e8d3a7ed54a5806a5dd9f1c0ea4caa
Verify every subject file before and after review. The changes relative to /tmp/opensip-implementation/m1-canonical-subject-04 are only design-lock.json, tools/verify_design.py and tools/tests/test_design_binding.py. Rust bytes are unchanged; no reason to repeat crypto qualification.

Read design proposal /Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/design-lock-v2.proposed.md; accepted base architecture and existing inventory acceptance evidence are at /Users/sb/code/opensip-ai/opensip_arch. In particular docs/implementation/m1/canonical-unit.v1.json and reviews/canonical-03/review.json under that folder are historical actual acceptance, not acceptance of this new code. The live architecture checkout has many user-authorized changes: preserve all.

Assess closed lock shapes, authenticated pins and joins, invalid/malformed input refusal, reviewed candidate selection, unchanged inherited rows/package edges, backward compatibility with lock1. Distinguish trusted lock provenance checking from a runtime authorization or cryptographic identity service. Run 17 Python test groups and the real design verification command against the explicit arch checkout. Add independent probes for realistic mistakes. Assess whether the bounded profile is proportionate and correct, including whether additional schema/generalization is truly required now.

Permitted: read frozen subject and architecture/reference files; execute local tests, Python, diff/hash tools; create your independent probes/logs only under /tmp/opensip-implementation/m1-successor-review-01. Do not modify frozen subjects, live product, architecture, global settings; no commit/push/network writes/messages. Do not inspect private session/hidden reasoning logs or dump environment/secrets.

Write review.md and review.json in /tmp/opensip-implementation/m1-successor-review-01. JSON: verdict ACCEPT-UNIT or CHANGES-REQUIRED or INCOMPLETE, subjectManifestSha256 exact above, requiredFindings [], advisories [], executedChecks [], limitations []. State execution failures honestly. A substantive acceptance requires executed tests and independent review, not just static reading. Do not manufacture a full M1/product approval.
