"""The static subject file list (candidate 05; review-02 A-2).

INPUTS is the complete execution closure of build, check, selftest and isolation: isolation.py copies exactly these
files and nothing else (subject-files.json is an OUTPUT and is never read by check.py or selftest.py). OUTPUTS are run
results. HARNESS files belong to the session. Everything under prior/ is preserved evidence; check.py reads only
prior/review-02/probe_ecma_compare.json, prior/review-03/probe_canon_newline.out.json and
prior/review-04/probe_dialect_scope.out.json (independent reviewer outputs that the checker replays), which are therefore
inputs.
"""

INPUTS = [
    "contract.md", "successor.json", "wire-carriers.v1.json", "wire-carriers.meta.schema.json", "field-coverage.json",
    "admission-vectors.json", "p3-guard-successor.v1.json", "public-route-successor.v1.json", "owner-pattern-successor.v1.json",
    "reference-environment.json", "check.py", "selftest.py",
    "tools/common.py", "tools/filelist.py", "tools/records_ts2.py", "tools/records_rust3.py", "tools/rules.py", "tools/succ.py",
    "tools/build.py", "tools/vectors.py", "tools/wirecodec.py", "tools/patterns.py", "tools/public_routes.py",
    "tools/owner_successor.py", "tools/representability.py", "tools/sender_ref.py", "tools/ecma_probe.js", "tools/admission_ref.py",
    "tools/check_static.py", "tools/check_reference.py", "tools/check_routes.py", "tools/manifest.py", "tools/isolation.py", "tools/outcome.py",
    "inputs/ts2-fields.json", "inputs/rust3-fields.json", "inputs/generator-candidate03-options.json",
    "prior/review-02/probe_ecma_compare.json", "prior/review-03/probe_canon_newline.out.json", "prior/review-04/probe_dialect_scope.out.json",
]
OUTPUTS = ["check-result.json", "selftest-result.json", "isolation-result.json", "outcome.json", "subject-files.json"]
HARNESS = {"launch-public.py", "process.json", "prompt.md", "public-events.jsonl"}
