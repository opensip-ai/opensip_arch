"""P3: root's scope probe variants replayed against the v2 projection check.

Rebuilds root's two actually closed Runs (budget_limit=1, references_stage_terminals.foo in
{budget-exhausted, unavailable}) from THIS runtime's source copy and applies root's two schema-valid variants
(execution attribution, work-budget detail) through `admit_projection` with the StepTermination schema as the
shape validator. Expected: projection admitted, delegated standing owner-validation-required (never lawful).
Also confirms the derived projections equal root's retained report. Writes nothing into any tree; stdout only.
"""
import importlib.util
import json
import sys
from pathlib import Path

SRC = Path("/private/tmp/opensip-design-corrections/claude-source37-host-finalizer-author.v2/source")
FOUNDATION = SRC / "docs/coop/design-corrections/foundation"
ROOT_REPORT = Path("/tmp/opensip-design-corrections/root-host-finalizer-scope.v1/report.json")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


SR = load("p3v2_semantic_replay", FOUNDATION / "check-semantic-replay.v3.py")
T = load("p3v2_run_termination", FOUNDATION / "run_termination_model.v1.py")
Q = load("p3v2_query", FOUNDATION.parent / "workflows" / "query_projection_model.v3.py")
root = json.loads(ROOT_REPORT.read_text())


def shape(term):
    Q.validate_schema(Q.COMMON_ID + "#/$defs/StepTermination", term)


rows = []
for root_row in root["rows"]:
    terminal = root_row["terminal"]
    run, objects, blobs, _ = SR.close_positive(SR.S.build_ts_semantic_graph(
        atom=SR.REFS_NONE_TGT, has_declares=False, has_references_fact=True, second_partition=True,
        references_resolved=False, incoming_search=True, incoming_complete=False, target_sidecar=True,
        budget_limit=1, references_stage_terminals={"foo": terminal}))
    derived = T.finalize(run, objects, blobs)["termination"]
    variants = []
    for name, fields in [("execution-attribution", {"executionId": "exec1_" + "a" * 32}),
                         ("work-budget-explanation", {"domainDetail": {"code": "EVALUATION.WORK_BUDGET_EXHAUSTED",
                                                                       "remedy": "Increase the deterministic evaluator work budget."}})]:
        try:
            got = T.admit_projection({**derived, **fields}, run, objects, blobs, shape)
            variants.append({"name": name, "result": "PROJECTION-ADMITTED", "delegated": sorted(got["delegated"]),
                             "standing": got["delegatedStanding"]})
        except T.RunTerminationError as exc:
            variants.append({"name": name, "result": "REFUSE", "refusal": str(exc)[:200]})
    rows.append({"terminal": terminal, "derivedEqualsRootReport": derived == root_row["finalize"]["termination"],
                 "derived": derived, "variants": variants})
print(json.dumps({"rootReportSha256": __import__("hashlib").sha256(ROOT_REPORT.read_bytes()).hexdigest(), "rows": rows}, indent=1))
