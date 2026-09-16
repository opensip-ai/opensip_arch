"""Probe: the exact BEFORE vs AFTER behavioural delta of the model corrections.

Loads the preserved BEFORE image of execution_inputs_model.v1.py in-memory (with __file__ set to
its original location so its sibling loads resolve) and compares it to the edited module. Writes
nothing into the source.
"""
import importlib.util
import json
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SRC = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source/docs/coop/design-corrections/foundation")
BEFORE_IMAGE = HERE / "before" / "docs__coop__design-corrections__foundation__execution_inputs_model.v1.py"


def load_after():
    spec = importlib.util.spec_from_file_location("after_model", SRC / "execution_inputs_model.v1.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_before():
    path = SRC / "execution_inputs_model.v1.py"
    mod = types.ModuleType("before_model")
    mod.__file__ = str(path)
    mod.__name__ = "before_model"
    exec(compile(BEFORE_IMAGE.read_text(), str(path), "exec"), mod.__dict__)
    return mod


A = load_after()
B = load_before()
out = {"beforeImage": str(BEFORE_IMAGE)}

# 1. Applicability over the full cross-product, with lawfulness marked.
U = "a" * 64
deltas = []
same = 0
for rel in ("vcs-change", "file", "references"):
    for uni in (None, U):
        for en in ("selected", "unselected"):
            for matrix in ("SUPPORTED-DESIGN", "UNSUPPORTED-TYPED", None):
                for vcs in ("none", "git"):
                    b = B.derived_applicability(rel, uni, en, matrix, vcs)
                    a = A.derived_applicability(rel, uni, en, matrix, vcs)
                    lawful = not (en == "unselected" and uni is not None)
                    if a != b:
                        deltas.append({"relation": rel, "universe": "U" if uni else None,
                                       "enumerator": en, "matrix": matrix, "vcsKind": vcs,
                                       "lawfulBindingShape": lawful, "before": b, "after": a})
                    else:
                        same += 1
out["applicability"] = {"unchangedCombinations": same, "changed": deltas}

# 2. want_u: old rule vs new rule over the REACHABLE domain.
def want_u_before(app, uni):
    return None if app in ("unavailable-unselected", "unavailable-null-universe") else uni


def want_u_after(app, uni):
    return uni


u_rows = []
for rel in ("vcs-change", "file", "references"):
    for uni in (None, U):
        for en in ("selected", "unselected"):
            for matrix in ("SUPPORTED-DESIGN", "UNSUPPORTED-TYPED"):
                for vcs in ("none", "git"):
                    if en == "unselected" and uni is not None:
                        continue  # enumeration owner refuses this shape
                    app = A.derived_applicability(rel, uni, en, matrix, vcs)
                    wb, wa = want_u_before(app, uni), want_u_after(app, uni)
                    if wb != wa:
                        u_rows.append({"applicability": app, "universe": "U" if uni else None,
                                       "before": wb, "after": wa})
out["sourceUniverseRuleDeltaOverLawfulShapes"] = u_rows
out["sourceUniverseRuleNote"] = (
    "Empty list means the published law ('sourceUniverse IS the binding universe, always') and "
    "the old reference expression agree on every LAWFUL shape, so publishing it changes no "
    "admitted Run. It removes the trap, and the refusal blind19 hit was that the host emitted "
    "null for inapplicable-vcs while the unpublished reference rule already wanted the binding U."
)

# 3. Carrier derivation.
def recs(*triples):
    return [
        {"id": chr(97 + i) * 64, "entry": {
            "coverage": cov, "deficiency": d, "nativeCause": c,
            "resolutionCompleteness": {"state": "not-applicable", "examinedExhaustive": cov == "complete"},
        }}
        for i, (cov, d, c) in enumerate(triples)
    ]


scenarios = {
    "no-returned-partitions": ([], {"a.ts"}, set()),
    "no-returned-partitions-no-census": ([], set(), set()),
    "complete-partition-missing-expected-subjects": (
        recs(("complete", None, None)), {"a.ts", "b.ts"}, {"a.ts"}),
    "typed-partition-missing-expected-subjects": (
        recs(("unknown", "budget-exhausted", None)), {"a.ts", "b.ts"}, {"a.ts"}),
    "untyped-then-typed-partitions": (
        recs(("complete", None, None), ("unknown", "input-closure-incomplete", "lockfile-missing")),
        {"a.ts"}, {"a.ts"}),
    "typed-then-untyped-partitions": (
        recs(("unknown", "input-closure-incomplete", "lockfile-missing"), ("complete", None, None)),
        {"a.ts"}, {"a.ts"}),
    "fully-complete": (recs(("complete", None, None)), {"a.ts"}, {"a.ts"}),
}
carrier = {}
for name, (r, expected, covered) in scenarios.items():
    sb = B._summarize_coverage_records(list(r), set(expected), set(covered))
    sa = A._summarize_coverage_records(list(r), set(expected), set(covered))
    keys = ("accountState", "deficiency", "nativeCause", "deficiencies", "censusMissing")
    carrier[name] = {
        "before": {k: sb.get(k) for k in keys},
        "after": {k: sa.get(k) for k in keys},
        "changed": {k: (sb.get(k), sa.get(k)) for k in keys if sb.get(k) != sa.get(k)},
    }
out["carrier"] = carrier

print(json.dumps(out, indent=2, default=str))
