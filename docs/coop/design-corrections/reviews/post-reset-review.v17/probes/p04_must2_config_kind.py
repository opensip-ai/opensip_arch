#!/usr/bin/env python
"""CB6-MUST-2 executable probe: TypeScript config node `kind` derivation.

Independently authored controls at the changed boundary:
  A. EXACT all-node derivation from the admitted logical path - entry, non-entry,
     custom-named, case variants, near-miss basenames, and paths designed to
     separate the exact-basename rule from the tsconfig*.json PREFIX convention
     and from case folding.
  B. The normative recipe (the published table + the prose) equals the ACTUAL
     derivation the model performs, and the model READS the table.
  C. Valid retained contexts remain USABLE (positive controls admit) and a wrong
     declared kind REFUSES at real admission (negative controls).
  D. The identity consequence is real: two readings of one repository mint two
     different tsconfigGraphHash values.

All expectations below are authored from the published law, not from the
candidate's own case file.
"""
import importlib.util
import json
import sys
from pathlib import Path

COPY, OUT = sys.argv[1], sys.argv[2]
DC = Path(COPY) / "docs/coop/design-corrections"
sys.path.insert(0, str(DC / "foundation"))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


N = load("native_model", DC / "native/native_evidence_model.v2.py")
LAW = json.loads((DC / "native/native-evidence.schemas.v2.json").read_bytes()
                 )["x-opensip-config-node-kind-law"]

rep = {"probe": "p04-must2-config-kind"}

# ---------- A. derivation table, independently expected ----------
# My expectation: kind = basename exact-match against {tsconfig.json, jsconfig.json}
# else "other". Case-sensitive. No prefix/stem/extension inference. Depth-blind.
CASES = [
    # (path, my expectation, why this path is discriminating)
    ("tsconfig.json", "tsconfig", "ordinary entry"),
    ("jsconfig.json", "jsconfig", "jsconfig entry"),
    ("packages/web/tsconfig.json", "tsconfig", "NON-ENTRY, depth must not matter"),
    ("a/b/c/d/e/jsconfig.json", "jsconfig", "deep non-entry jsconfig"),
    ("tsconfig.build.json", "other", "DISCRIMINATES exact vs tsconfig*.json prefix"),
    ("tsconfig.base.json", "other", "same, the shared-base spelling"),
    ("tsconfig.jsonc", "other", "prefix rule would have to decide this"),
    ("jsconfig.build.json", "other", "prefix rule would have to decide this too"),
    ("tsconfig", "other", "extensionless; a stem rule would say tsconfig"),
    ("TSConfig.json", "other", "CASE: folding would say tsconfig"),
    ("TSCONFIG.JSON", "other", "CASE: upper"),
    ("Tsconfig.json", "other", "CASE: title"),
    ("JSConfig.json", "other", "CASE: jsconfig variant"),
    (".tsconfig.json", "other", "leading dot is part of the basename"),
    ("tsconfig.json.bak", "other", "suffix rule would mis-fire"),
    ("mytsconfig.json", "other", "substring/endswith rule would mis-fire"),
    ("configs/app.build.json", "other", "explicitly selected CUSTOM-named config"),
    ("dir.tsconfig.json/tsconfig.json", "tsconfig",
     "final segment decides even when a parent dir contains the name"),
    ("packages/tsconfig.json/x.json", "other",
     "a parent segment named tsconfig.json must not leak into the basename"),
    ("tsconfig.json ", "other", "trailing space is a different basename"),
    (" tsconfig.json", "other", "leading space is a different basename"),
    ("node_modules/@scope/pkg/tsconfig.json", "tsconfig", "vendored non-entry"),
]
rows = []
for path, expect, why in CASES:
    got = N.config_node_kind(path)
    rows.append({"path": path, "myExpectation": expect, "derived": got,
                 "agrees": got == expect, "why": why})
rep["derivationRows"] = rows
rep["derivationCaseCount"] = len(rows)
rep["derivationDisagreements"] = [r for r in rows if not r["agrees"]]
rep["derivationAllAgree"] = not rep["derivationDisagreements"]

# ---------- B. the model READS the published table ----------
rep["modelReadsPublishedTable"] = {
    "modelTableIsTheSchemaObject":
        N.CONFIG_NODE_KIND_LAW is not None
        and N.CONFIG_NODE_KIND_LAW["basenames"] == LAW["basenames"]
        and N.CONFIG_NODE_KIND_LAW["otherwise"] == LAW["otherwise"],
    "publishedBasenames": LAW["basenames"],
    "publishedOtherwise": LAW["otherwise"],
    "tableIsClosedTwoMembers": sorted(LAW["basenames"]) ==
        ["jsconfig.json", "tsconfig.json"],
}
# The law's own published examples must equal the model's derivation.
rep["publishedExamplesAgreeWithModel"] = [
    {"path": e["path"], "lawSays": e["kind"],
     "modelDerives": N.config_node_kind(e["path"]),
     "agrees": N.config_node_kind(e["path"]) == e["kind"]}
    for e in LAW["examples"]
]
rep["allPublishedExamplesAgree"] = all(
    x["agrees"] for x in rep["publishedExamplesAgreeWithModel"])

# ---------- C. admission: valid contexts usable, wrong kind refuses ----------
def graph(nodes, entry):
    # nodes carries x-opensip-order {"by":["path"]} - strict unique ascending.
    # My first attempt passed them unsorted; typescript_config_graph_digest
    # validates the record and refused. Sorting here is fixture hygiene and
    # changes no kind derivation (the fault checker does not read order).
    return {"schemaVersion": 1, "entryConfigPath": entry,
            "nodes": sorted(nodes, key=lambda n: n["path"])}


def node(path, kind, extends=None):
    # contentSha256 is a required retained preimage digest; its VALUE is
    # irrelevant to the kind law, so a distinct deterministic filler per path
    # keeps the record schema-valid without smuggling meaning into the control.
    import hashlib
    return {"path": path, "kind": kind,
            "contentSha256": hashlib.sha256(path.encode()).hexdigest(),
            "extendsResolved": extends or []}


admission = []


def adm(cid, g, expect_faults, why):
    faults = N.typescript_config_graph_faults(g)
    kind_faults = [f for f in faults
                   if f.startswith("native.config-graph-kind-contradicts-path")]
    admission.append({
        "id": cid, "graph": g, "allFaults": faults,
        "kindFaults": kind_faults,
        "myExpectation": expect_faults,
        "agrees": (len(kind_faults) > 0) == expect_faults,
        "why": why,
    })


# POSITIVE CONTROLS - valid retained contexts must remain usable
adm("POS-plain-entry",
    graph([node("tsconfig.json", "tsconfig")], "tsconfig.json"),
    False, "POSITIVE: ordinary entry admits with no kind fault")
adm("POS-jsconfig-entry",
    graph([node("jsconfig.json", "jsconfig")], "jsconfig.json"),
    False, "POSITIVE: jsconfig entry admits")
adm("POS-entry-with-nonentry-base",
    graph([node("tsconfig.json", "tsconfig", ["packages/web/tsconfig.json"]),
           node("packages/web/tsconfig.json", "tsconfig")], "tsconfig.json"),
    False, "POSITIVE: correctly labelled non-entry base admits")
adm("POS-custom-named-entry-is-other",
    graph([node("configs/app.build.json", "other")], "configs/app.build.json"),
    False,
    "POSITIVE and load-bearing: an explicitly selected CUSTOM-named config is a "
    "usable entry whose kind is `other`; `other` must not be a refusal")
adm("POS-custom-base-labelled-other",
    graph([node("tsconfig.json", "tsconfig", ["tsconfig.base.json"]),
           node("tsconfig.base.json", "other")], "tsconfig.json"),
    False, "POSITIVE: tsconfig.base.json correctly labelled `other` admits")
adm("POS-jsconfig-entry-with-other-base",
    graph([node("jsconfig.json", "jsconfig", ["tsconfig.base.json"]),
           node("tsconfig.base.json", "other")], "jsconfig.json"),
    False, "POSITIVE: a jsconfig entry extending a shared base stays lawful")

# NEGATIVE CONTROLS - a wrong declared kind must refuse
adm("NEG-entry-relabelled-other",
    graph([node("tsconfig.json", "other")], "tsconfig.json"),
    True, "NEGATIVE: the entry cannot be relabelled")
adm("NEG-prefix-convention-on-entry",
    graph([node("tsconfig.build.json", "tsconfig")], "tsconfig.build.json"),
    True, "NEGATIVE: the tsconfig*.json PREFIX reading is refused")
adm("NEG-prefix-convention-on-base",
    graph([node("tsconfig.json", "tsconfig", ["tsconfig.base.json"]),
           node("tsconfig.base.json", "tsconfig")], "tsconfig.json"),
    True, "NEGATIVE: a NON-ENTRY base cannot be relabelled either")
adm("NEG-case-folded-entry",
    graph([node("TSConfig.json", "tsconfig")], "TSConfig.json"),
    True, "NEGATIVE: case folding is refused")
adm("NEG-jsconfig-claimed-on-tsconfig",
    graph([node("tsconfig.json", "jsconfig")], "tsconfig.json"),
    True, "NEGATIVE: wrong recognized kind refuses")
adm("NEG-custom-claimed-tsconfig",
    graph([node("configs/app.build.json", "tsconfig")], "configs/app.build.json"),
    True, "NEGATIVE: a custom-named config cannot assert tsconfig")
adm("NEG-deep-base-relabelled",
    graph([node("tsconfig.json", "tsconfig", ["packages/web/tsconfig.json"]),
           node("packages/web/tsconfig.json", "other")], "tsconfig.json"),
    True, "NEGATIVE: a depth-reached recognized base cannot be downgraded")

rep["admissionControls"] = admission
rep["admissionDisagreements"] = [a for a in admission if not a["agrees"]]
rep["admissionAllAgree"] = not rep["admissionDisagreements"]
rep["positiveControlCount"] = sum(1 for a in admission if a["id"].startswith("POS"))
rep["negativeControlCount"] = sum(1 for a in admission if a["id"].startswith("NEG"))

# ---------- D. the identity consequence is real ----------
g_exact = graph([node("tsconfig.json", "tsconfig", ["tsconfig.build.json"]),
                 node("tsconfig.build.json", "other")], "tsconfig.json")
g_prefix = graph([node("tsconfig.json", "tsconfig", ["tsconfig.build.json"]),
                  node("tsconfig.build.json", "tsconfig")], "tsconfig.json")
try:
    h_exact = N.typescript_config_graph_digest(g_exact)
    h_prefix = N.typescript_config_graph_digest(g_prefix)
    rep["identityConsequence"] = {
        "exactReadingHash": h_exact,
        "prefixReadingHash": h_prefix,
        "twoReadingsMintTwoHashes": h_exact != h_prefix,
        "onlyTheExactReadingAdmits": (
            not [f for f in N.typescript_config_graph_faults(g_exact)
                 if "kind-contradicts" in f]
            and bool([f for f in N.typescript_config_graph_faults(g_prefix)
                      if "kind-contradicts" in f])),
        "note": "This is the defect the law closes: before publication both "
                "readings were conforming and minted different RunIds. Now only "
                "one admits, so the ambiguity is removed at admission, not "
                "merely described.",
    }
except Exception as e:
    rep["identityConsequence"] = {"error": type(e).__name__ + ": " + str(e)}

with open(OUT, "w") as fh:
    json.dump(rep, fh, indent=1, sort_keys=True, default=str)

print("derivation cases:", rep["derivationCaseCount"],
      "disagreements:", len(rep["derivationDisagreements"]))
for r in rep["derivationDisagreements"]:
    print("   DISAGREE", r)
print("published examples agree:", rep["allPublishedExamplesAgree"])
print("model reads published table:",
      rep["modelReadsPublishedTable"]["modelTableIsTheSchemaObject"],
      "| table:", rep["modelReadsPublishedTable"]["publishedBasenames"],
      "otherwise:", rep["modelReadsPublishedTable"]["publishedOtherwise"])
print()
print("admission controls: %d positive, %d negative, disagreements: %d"
      % (rep["positiveControlCount"], rep["negativeControlCount"],
         len(rep["admissionDisagreements"])))
for a in admission:
    print("  %-34s kindFaults=%d expectFault=%s agrees=%s"
          % (a["id"], len(a["kindFaults"]), a["myExpectation"], a["agrees"]))
print()
print("identity consequence:", json.dumps(rep["identityConsequence"], indent=1)[:700])
