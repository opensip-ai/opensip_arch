import json
import sys

sys.path.insert(0, "/tmp/opensip-design-corrections/consumer-b.v8/output/work")
import closure as CL
import run_syntax

results = []


def check(name, shape="mixed", selected=None, mutate=None, expect=None):
    fx, A, run_id = run_syntax.build_run(shape, selected, mutate)
    c = CL.Closure(fx.s)
    rep = c.close_run(run_id)
    first = rep["firstFault"]
    ok = (first == expect) if expect else (first is None)
    results.append({"vector": name, "shape": shape, "selected": selected,
                    "expectedFirstRefusal": expect, "observedFirstRefusal": first,
                    "checks": rep["checks"], "faultCount": len(rep["faults"]),
                    "faults": rep["faults"][:6], "runId": run_id,
                    "bodyIdentity": A.extra["bodyIdentity"]})
    print(("PASS " if ok else "FAIL ") + name, "->", first,
          (rep["faults"][0]["detail"][:130] if rep["faults"] else ""))
    return A


a = check("CB-SX-POS1 mixed grammar-only repository, no TS and no Rust unit")
print("  bodyLanguageVersion:", json.dumps(a.extra["bodyLanguageVersion"],
                                           sort_keys=True))
print("  selected grammars:", a.extra["selectedGrammarIds"],
      "of bundled", a.extra["bundledLanguages"])
b = check("CB-SX-POS2 data/document-only repository: inventory complete, "
          "code capabilities unavailable", "data-only")

check("CB-SX-N1 false complete empty declares over a data-only repository",
      "data-only", None, {"false_complete_empty_declares": True},
      "SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE")
check("CB-SX-N2 false complete clones over a data-document path", "mixed", None,
      {"false_complete_data_clone": True}, "COVERAGE_SOURCE_VARIANT_UNSUPPORTED_SCOPE")
check("CB-SX-N3 false complete for a semantic capability no grammar bears",
      "mixed", None, {"false_complete_references": True},
      "SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE")
check("CB-SX-N4 a Markdown-anchored code fact", "mixed", None,
      {"markdown_anchored_code_fact": True}, "SYNTAX_CAPABILITY_UNSUPPORTED_FACT")
check("CB-SX-N5 a data grammar declaring syntaxClass code", "mixed", None,
      {"data_grammar_claims_code": True}, "native.syntax-grammar-class-mismatch")
check("CB-SX-N6 parserVersion not the grammar closure manifest's", "mixed", None,
      {"parser_version_not_from_manifest": True},
      "native.syntax-grammar-version-not-from-manifest")
check("CB-SX-N7 selecting a grammar the bundle does not contain", "mixed",
      ["g-javascript", "g-python"], None, "native.syntax-grammar-not-in-bundle")
check("CB-SX-N8 an UNSELECTED code grammar lends no capability: clones over a "
      ".js path with only data grammars selected", "mixed",
      ["g-markdown", "g-yaml"], None, "SYNTAX_CAPABILITY_UNSUPPORTED_FACT")

with open("/tmp/opensip-design-corrections/consumer-b.v8/output/vectors-syntax-run.json",
          "w") as f:
    json.dump(results, f, indent=1, sort_keys=True)


# ---- one refused hidden input for the syntax universe ---------------------
def hidden_syntax_context(fx, A, run_id):
    desc = json.loads(json.dumps(A.contexts[A.extra["contextHex"]][1]))
    desc["grammarBundle"]["parserName"] = "opensip-grammars-alt"
    fx.s.put_h("native.context.syntax.v2", desc)
    return "a second hash-valid syntax context no Plan selected"


fx, A, run_id = run_syntax.build_run("mixed")
note = hidden_syntax_context(fx, A, run_id)
rep = CL.Closure(fx.s).close_run(run_id)
first = rep["firstFault"]
good = first == "PLAN_CONTEXT_SET_MISMATCH"
print(("PASS " if good else "FAIL ")
      + "CB-SX-N9 hidden hash-valid syntax context outside "
        "plan.nativeContextDigests ->", first)
results.append({"vector": "CB-SX-N9 hidden hash-valid syntax context",
                "expectedFirstRefusal": "PLAN_CONTEXT_SET_MISMATCH",
                "observedFirstRefusal": first, "note": note,
                "faults": rep["faults"][:3]})
with open("/tmp/opensip-design-corrections/consumer-b.v8/output/vectors-syntax-run.json",
          "w") as f:
    json.dump(results, f, indent=1, sort_keys=True)
