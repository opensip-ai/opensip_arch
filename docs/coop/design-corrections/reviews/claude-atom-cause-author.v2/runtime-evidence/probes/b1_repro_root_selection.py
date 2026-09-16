"""Reproduce root's retained helper-only counterexample against the current source bytes.

Root's construction: TWO scopes for the SAME subject and the SAME source kind, with `coverageScopes`
mapping the HIGHER coverage id to the LOWER scope id. `_coverages_for_current_source` and
`_select_dep_coverages` walk scopes in ascending SCOPE order and concatenate each scope's matches,
so the combined Coverage list comes out in DESCENDING coverage-id order and the first-wins typed
carrier is the opposite of the published ascending-Coverage-ID fold.

Synthetic helper-only inputs. NOT a native-schema-admitted Coverage, not a proof, not a retained
Run. AUTHOR/REFERENCE evidence.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

F = Path("/tmp/opensip-design-corrections/atom-cause-successor.v1/source/"
         "docs/coop/design-corrections/foundation")
P = F / "atom_model.v1.py"
spec = importlib.util.spec_from_file_location("A", P)
A = importlib.util.module_from_spec(spec)
spec.loader.exec_module(A)

U = "a" * 64
N = "symbol"
LO_S, HI_S = "scope2:" + "1" * 64, "scope2:" + "2" * 64
LO_C, HI_C = "coverage2:" + "1" * 64, "coverage2:" + "2" * 64


def sc():
    return {"relation": "declares", "resolution": "syntactic", "sourceUniverse": U,
            "targetUniverse": U, "subjects": [N]}


def cov(d, nc):
    return {"key": {"relation": "declares", "resolution": "syntactic", "sourceUniverse": U,
                    "targetUniverse": U},
            "entry": {"coverage": "unknown", "deficiency": d, "nativeCause": nc}}


def build(mapping):
    return {"scopes": {LO_S: sc(), HI_S: sc()},
            "coverages": {LO_C: cov("budget-exhausted", None),
                          HI_C: cov("input-closure-incomplete", "lockfile-missing")},
            "coverageScopes": mapping}


rows = []
for label, mapping in (
        ("reversed  (HI coverage -> LO scope)", {HI_C: LO_S, LO_C: HI_S}),
        ("aligned   (LO coverage -> LO scope)", {LO_C: LO_S, HI_C: HI_S})):
    inp = build(mapping)
    selected = A._select_dep_coverages("declares", "syntactic", U, U, inp, {N}, "symbol")
    fold, refs = A._conservative_entry("declares", selected)
    paired, sids, unpaired = A._coverages_for_current_source(inp, "declares", "syntactic", U, N)
    rows.append({
        "case": label,
        "depSelected": [c for c, _ in selected],
        "depAscending": [c for c, _ in selected] == sorted(c for c, _ in selected),
        "foldedCarrier": [fold.get("deficiency"), fold.get("nativeCause")],
        "outgoingPaired": [c for c, _ in paired],
        "outgoingAscending": [c for c, _ in paired] == sorted(c for c, _ in paired),
        "scopes": sids,
        "cited": refs,
    })

print(json.dumps({
    "standing": "Synthetic helper-only inputs; not native-schema admitted, not a proof, not a "
                "retained Run. Reproduces root's stated selection-order mismatch only.",
    "sourceSha256": hashlib.sha256(P.read_bytes()).hexdigest(),
    "ascendingExpected": sorted([LO_C, HI_C]),
    "carrierIfAscending": ["budget-exhausted", None],
    "cases": rows,
    "MISMATCH_PRESENT": any(not r["depAscending"] or not r["outgoingAscending"] for r in rows),
}, indent=2, default=str))
