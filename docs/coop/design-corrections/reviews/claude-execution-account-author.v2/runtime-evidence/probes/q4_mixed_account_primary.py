"""Probe: the DRAFT-P1 counterexample on an ADMITTED fixture and through a full Run.

Shape: file account incomplete with NO typed pair (census-short returned partition), followed in
the owed matrix-relations order by a package account that DOES carry a real typed pair. Under
items[0] the row carrier was masked to null/null; under first-actually-typed it is the real pair.

Also replays root's exact synthetic unit counterexample against the edited model.
"""
import importlib.util
import json
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
F = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source/docs/coop/design-corrections/foundation")
BEFORE_MODEL = HERE / "before" / "docs__coop__design-corrections__foundation__execution_inputs_model.v1.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_before_model():
    path = F / "execution_inputs_model.v1.py"
    mod = types.ModuleType("before_model")
    mod.__file__ = str(path)
    mod.__name__ = "before_model"
    exec(compile(BEFORE_MODEL.read_text(), str(path), "exec"), mod.__dict__)
    return mod


M = load("q4_model", F / "execution_inputs_model.v1.py")
B = load_before_model()
Fx = load("q4_graph", F / "evaluator_graph_fixture.v3.py")
H = load("q4_capture", F / "execution_inputs_fixture.v3.py")
R = load("q4_replay", F / "evaluator_replay_model.v3.py")
S = load("q4_semantic", F / "evaluator_semantic_fixture.v3.py")
IDENT = R.M

out = {}

# --- 1. Root's exact synthetic unit counterexample, before vs after -----------------------
root_inputs = [
    {"accountState": "incomplete", "relation": "file", "resolution": "enumerated",
     "deficiency": None, "nativeCause": None, "coverageRecords": [], "inputRefs": []},
    {"accountState": "incomplete", "relation": "package", "resolution": "manifest-declared",
     "deficiency": "budget-exhausted", "nativeCause": None,
     "coverageRecords": [{"deficiency": "budget-exhausted", "nativeCause": None,
                          "inputRef": {"domain": "coverage", "digest": "a" * 64},
                          "coverageId": "a" * 64}],
     "inputRefs": [{"domain": "coverage", "digest": "a" * 64}]},
]
kw = dict(enumerator_status="selected", universe="c" * 64, required=True, inventories=[],
          candidate_rec=None, candidate_digest=None, candidate_cap=False,
          binding={"ordinal": 0, "universe": "c" * 64, "extents": []})
rb = B.derive_outcome(account_summaries=json.loads(json.dumps(root_inputs)), **kw)
ra = M.derive_outcome(account_summaries=json.loads(json.dumps(root_inputs)), **kw)
out["rootUnitCounterexample"] = {
    "standing": "root's probe inputs replayed; synthetic internal summaries, NOT a full Run",
    "before": {"state": rb["state"], "pair": [rb["deficiency"], rb["nativeCause"]],
               "sourceCount": len(rb["sources"]),
               "sourcePairs": [[s.get("deficiency"), s.get("nativeCause")] for s in rb["sources"]]},
    "after": {"state": ra["state"], "pair": [ra["deficiency"], ra["nativeCause"]],
              "sourceCount": len(ra["sources"]),
              "sourcePairs": [[s.get("deficiency"), s.get("nativeCause")] for s in ra["sources"]]},
    "allSourcesRetainedUnchanged": rb["sources"] == ra["sources"],
    "inputRefsUnchanged": rb["inputRefs"] == ra["inputRefs"],
    "nativeCausesUnchanged": rb["nativeCauses"] == ra["nativeCauses"],
}

# --- 2. The same shape on an ADMITTED owner fixture ---------------------------------------
MIXED = dict(file_coverage_subjects=["README.md"], package_coverage_unknown=True)
g = Fx.build_file_inputs(**MIXED)
kwargs = H.admission_kwargs(g)
adm = M.admit_execution_inputs(**kwargs)
accounts = [a for a in adm["derivedAccounts"] if a["cellOrdinal"] == 0 and a["programOrdinal"] == 0]
row = adm["derivedOutcomes"][0]
out["admittedMixedAccountFixture"] = {
    "result": adm["result"], "refusals": adm["refusals"],
    "accountOrder": [(a["relation"], a["resolution"], a["accountState"],
                      a.get("deficiency"), a.get("nativeCause"),
                      a.get("censusMissing")) for a in accounts],
    "rowState": row["state"],
    "rowPair": [row["deficiency"], row["nativeCause"]],
    "sourceOrder": [(s.get("source"), s.get("relation"), s.get("deficiency"), s.get("nativeCause"))
                    for s in row["sources"]],
    "rowInputRefs": row["inputRefs"],
    "requiredCellDeficiencies": [(d.get("cause"), d.get("relation"), d.get("deficiency"),
                                  d.get("nativeCause"),
                                  [r["domain"] for r in d.get("inputRefs") or []])
                                 for d in adm["requiredCellDeficiencies"]],
}
# The BEFORE model's derivation of the SAME account summaries, to show the masking removed.
# NOTE ON STANDING: this is not "the before model refuses this graph". The host rows here are
# built by the shared host-capture builder, which imports the EDITED model, so feeding them to
# the BEFORE model compares a new builder against an old admission and its refusal is an
# artifact of that mix, not a pre-existing refusal. The meaningful comparison is the derivation
# itself, below: same inputs, same sources, different row carrier.
before_row = B.derive_outcome(
    enumerator_status="selected",
    universe=g["enumerationPlan"]["cells"][0]["programBindings"][0]["universe"], required=True,
    inventories=[], account_summaries=json.loads(json.dumps(accounts)),
    candidate_rec=None, candidate_digest=None, candidate_cap=False,
    binding=g["enumerationPlan"]["cells"][0]["programBindings"][0],
)
out["admittedMixedAccountFixture"]["beforeModelDerivationOfTheseAccounts"] = {
    "standing": "BEFORE model re-deriving the SAME admitted account summaries; not a claim about "
                "how the before model treated any previously admitted graph.",
    "rowPair": [before_row["deficiency"], before_row["nativeCause"]],
    "sourceOrder": [(s.get("source"), s.get("relation"), s.get("deficiency"), s.get("nativeCause"))
                    for s in before_row["sources"]],
    "sourcesIdenticalToAfter": (
        [(s.get("source"), s.get("relation"), s.get("deficiency"), s.get("nativeCause"))
         for s in before_row["sources"]]
        == [(s.get("source"), s.get("relation"), s.get("deficiency"), s.get("nativeCause"))
            for s in row["sources"]]),
}

# --- 3. The same shape through a FULL Run (M.close_run) -----------------------------------
NONE_ATOM = {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": []}
try:
    gr = Fx.build_file_inputs(atom_override=NONE_ATOM, **MIXED)
    seed, objects, blobs, _ = Fx.seal_fixture(gr)
    _, owner = IDENT.open_run_closure(seed, objects, blobs)
    i = gr["inputs"]
    o = R.derive(i["planId"], i["executionPlanId"], i["evaluatorClosure"],
                 i["evaluationInputRefs"], objects, blobs, owner)
    run, objects, blobs = S.seal_derived(gr, o, objects, blobs)
    result = R.replay(run, objects, blobs)
    closed = IDENT.close_run(run, objects, blobs)
    out["fullRun"] = {
        "closeRunMatchesReplay": closed == result["runId"],
        "runId": result["runId"], "verdict": result["verdict"],
        "executionDeficiencies": o["proof"]["executionDeficiencies"],
    }
except Exception as exc:  # noqa: BLE001
    out["fullRun"] = {"error": f"{type(exc).__name__}: {exc}"}

print(json.dumps(out, indent=2, default=str))
