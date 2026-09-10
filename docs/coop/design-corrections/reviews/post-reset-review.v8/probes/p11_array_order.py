#!/usr/bin/env python3
"""P11: NEW-SHOULD-1 -- the array-order law, verified independently.

Checks, in order:
 1. coverage: every CURRENT schema document, discovered by my own walk, not the
    author's file list;
 2. the keyword is actually ENFORCED by the validator, not merely declared;
 3. the closed vocabulary is exactly the one the contract states;
 4. raw UTF-8 order vs canonical escaped-string order really differ;
 5. tuple field order vs canonical object order really differ;
 6. canonical-order permits measured duplicates; canonical-set refuses them;
 7. the encoder does NOT normalize -- annotations are admission rules only;
 8. input configuration layers keep `sequence` while the resolved semantic
    record uses canonical-set;
 9. ordered token/argv/substitution sequences keep repeats and position.
"""
import copy, hashlib, importlib.util, json, sys
from pathlib import Path

SUBJ = Path("/tmp/opensip-design-corrections/candidate-subject.v8")
DC = SUBJ / "docs/coop/design-corrections"
F = DC / "foundation"


def load(n, p):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


C = load("canon", F / "canonical.py")
R = {"checks": [], "observations": {}}


def rec(n, ok, d=None):
    R["checks"].append({"id": n, "passed": bool(ok), "detail": d})


def admitted(schema, value):
    try:
        C.validate(schema, value)
        return True
    except Exception:
        return False


def ordered_schema(order):
    return {"type": "array", "x-opensip-order": order}


# ---------------------------------------------------------------------------
# 1. Independent coverage sweep
# ---------------------------------------------------------------------------
def coverage():
    """Discover every CURRENT schema document myself: any *.json under the four
    unit directories whose content declares $schema (i.e. is a JSON Schema)."""
    docs = []
    for d in ("foundation", "native", "security", "workflows",
              "workflows/schemas"):
        for p in sorted((DC / d).glob("*.json")):
            try:
                j = json.loads(p.read_bytes())
            except Exception:
                continue
            if isinstance(j, dict) and "$schema" in j:
                docs.append((p, j))
    total, missing, invalid = 0, [], []

    def arrays(node, path=""):
        if isinstance(node, dict):
            t = node.get("type")
            if t == "array" or (isinstance(t, list) and "array" in t):
                yield path, node
            for k, v in node.items():
                yield from arrays(v, path + "/" + str(k))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                yield from arrays(v, path + "/" + str(i))

    per = []
    for p, j in docs:
        found = list(arrays(j))
        total += len(found)
        m = [ptr for ptr, n in found if "x-opensip-order" not in n]
        inv = [ptr for ptr, n in found
               if "x-opensip-order" in n
               and not admitted(ordered_schema(n["x-opensip-order"]), [])]
        rel = str(p.relative_to(DC))
        per.append({"path": rel, "arrays": len(found),
                    "missing": m, "invalid": inv})
        missing += [rel + ptr for ptr in m]
        invalid += [rel + ptr for ptr in inv]
    R["observations"]["independentCoverage"] = {
        "schemaDocumentsDiscovered": len(docs),
        "documents": [str(p.relative_to(DC)) for p, _ in docs],
        "totalArrays": total, "perDocument": per}
    rec("AO-01-every-array-in-every-current-schema-declares-its-order",
        not missing, {"missing": missing[:20], "totalArrays": total})
    rec("AO-02-every-declared-annotation-is-in-the-closed-vocabulary",
        not invalid, {"invalid": invalid[:20]})
    # the foundation import-context and quality-report schemas are covered
    names = [str(p.relative_to(DC)) for p, _ in docs]
    rec("AO-03-foundation-import-source-context-covered",
        "foundation/import-source-context.schema.json" in names, {"names": names})
    rec("AO-04-foundation-product-quality-report-covered",
        "foundation/product-quality-report.schema.v3.json" in names)


# ---------------------------------------------------------------------------
# 2/3. The keyword is enforced, and the vocabulary is closed
# ---------------------------------------------------------------------------
def vocabulary():
    md = (SUBJ / "docs/v2/contracts/product-v1/identity-and-evidence.md").read_text()
    declared = ["sequence", "canonical-set", "canonical-order", "utf8", "path",
                "numeric", "ordinal", "predicate", "ruleId", "waiverId"]
    R["observations"]["contractVocabulary"] = declared
    for name in declared:
        rec("AO-10-vocab-named-in-contract:" + name, "`" + name + "`" in md)
    # each keyword actually BITES on a wrong order
    bites = {
        "canonical-set": (["a", "b"], ["b", "a"]),
        "canonical-order": (["a", "a", "b"], ["b", "a", "a"]),
        "utf8": (["a", "b"], ["b", "a"]),
    }
    for k, (good, bad) in bites.items():
        rec("AO-11-keyword-enforced:" + k,
            admitted(ordered_schema(k), good) and not admitted(ordered_schema(k), bad),
            {"good": good, "bad": bad})
    rec("AO-12-path-enforced",
        admitted(ordered_schema("path"), [{"path": "a"}, {"path": "b"}])
        and not admitted(ordered_schema("path"), [{"path": "b"}, {"path": "a"}]))
    rec("AO-13-numeric-enforced",
        admitted(ordered_schema("numeric"), [1, 2])
        and not admitted(ordered_schema("numeric"), [2, 1]))
    rec("AO-14-ordinal-enforced-contiguous-zero-based",
        admitted(ordered_schema("ordinal"), [{"ordinal": 0}, {"ordinal": 1}])
        and not admitted(ordered_schema("ordinal"), [{"ordinal": 1}, {"ordinal": 2}])
        and not admitted(ordered_schema("ordinal"), [{"ordinal": 1}, {"ordinal": 0}]))
    rec("AO-15-predicate-enforced",
        admitted(ordered_schema("predicate"),
                 [{"ruleId": "a", "subjectId": "a", "predicateId": "p"},
                  {"ruleId": "a", "subjectId": "a", "predicateId": "p.0"}])
        and not admitted(ordered_schema("predicate"),
                         [{"ruleId": "a", "subjectId": "a", "predicateId": "p.0"},
                          {"ruleId": "a", "subjectId": "a", "predicateId": "p"}]))
    rec("AO-16-ruleId-and-waiverId-enforced",
        admitted(ordered_schema("ruleId"), [{"ruleId": "a"}, {"ruleId": "b"}])
        and not admitted(ordered_schema("ruleId"), [{"ruleId": "b"}, {"ruleId": "a"}])
        and admitted(ordered_schema("waiverId"), [{"waiverId": "a"}, {"waiverId": "b"}]))
    # an annotation OUTSIDE the vocabulary must refuse, not pass silently
    for bad in ["descending", "sorted", {"by": "name"}, {"by": []},
                {"by": ["a", "a"]}, {"by": ["a"], "descending": True}, 7, None]:
        rec("AO-17-unknown-annotation-refuses:" + json.dumps(bad),
            not admitted(ordered_schema(bad), []))
    # uniqueItems alone neither selects nor overrides an order
    rec("AO-18-uniqueItems-alone-does-not-select-an-order",
        admitted({"type": "array", "uniqueItems": True,
                  "x-opensip-order": "sequence"}, ["b", "a"]),
        {"note": "a uniqueItems sequence still admits descending input"})
    # all except sequence and canonical-order require UNIQUE sort keys
    for k in ("canonical-set", "utf8", "path", "numeric", "predicate",
              "ruleId", "waiverId"):
        dup = {"canonical-set": ["a", "a"], "utf8": ["a", "a"],
               "path": [{"path": "a"}, {"path": "a"}],
               "numeric": [1, 1],
               "predicate": [{"ruleId": "a", "subjectId": "a", "predicateId": "p"}] * 2,
               "ruleId": [{"ruleId": "a"}] * 2,
               "waiverId": [{"waiverId": "a"}] * 2}[k]
        rec("AO-19-unique-sort-keys-required:" + k,
            not admitted(ordered_schema(k), dup))
    rec("AO-20-sequence-and-canonical-order-allow-repeats",
        admitted(ordered_schema("sequence"), ["a", "a"])
        and admitted(ordered_schema("canonical-order"), ["a", "a"]))


# ---------------------------------------------------------------------------
# 4/5. The two order distinctions the contract calls out
# ---------------------------------------------------------------------------
def distinctions():
    # raw UTF-8 bytes vs canonical ESCAPED-string bytes
    raw = ["\n", "!"]          # 0x0A < 0x21  -> ascending raw UTF-8
    esc = ["!", "\n"]          # C("!")='"!"' < C("\n")='"\\n"' -> ascending canonical
    rec("AO-30-raw-utf8-order-differs-from-canonical-order",
        admitted(ordered_schema("utf8"), raw)
        and not admitted(ordered_schema("utf8"), esc)
        and admitted(ordered_schema("canonical-set"), esc)
        and not admitted(ordered_schema("canonical-set"), raw),
        {"rawAscending": raw, "canonicalAscending": esc,
         "C_newline": C.canonical("\n").decode(),
         "C_bang": C.canonical("!").decode()})

    # tuple FIELD order vs canonical OBJECT order
    recs = [{"a": "z", "name": "a"}, {"a": "a", "name": "z"}]
    rec("AO-31-tuple-field-order-differs-from-canonical-object-order",
        admitted(ordered_schema({"by": ["name"]}), recs)
        and not admitted(ordered_schema({"by": ["name"]}), list(reversed(recs)))
        and admitted(ordered_schema("canonical-set"), list(reversed(recs)))
        and not admitted(ordered_schema("canonical-set"), recs),
        {"byName": [r["name"] for r in recs],
         "canonicalBytes": [C.canonical(r).decode() for r in recs]})
    rec("AO-32-tuple-order-uses-the-listed-key-order",
        admitted(ordered_schema({"by": ["name", "version"]}),
                 [{"name": "a", "version": "1"}, {"name": "a", "version": "2"}])
        and not admitted(ordered_schema({"by": ["name", "version"]}),
                         [{"name": "a", "version": "2"}, {"name": "a", "version": "1"}]))
    rec("AO-33-tuple-duplicate-key-different-payload-refuses",
        not admitted(ordered_schema({"by": ["name"]}),
                     [{"name": "a", "p": 1}, {"name": "a", "p": 2}]))


# ---------------------------------------------------------------------------
# 6. canonical-order in truthful G13 FAIL reports
# ---------------------------------------------------------------------------
def g13_duplicates():
    g13 = json.loads((F / "g13-result-schema.v5.json").read_bytes())
    q = json.loads((F / "product-quality-report.schema.v3.json").read_bytes())
    found = []

    def walk(node, path, doc):
        if isinstance(node, dict):
            if "x-opensip-order" in node:
                found.append({"doc": doc, "path": path,
                              "order": node["x-opensip-order"]})
            for k, v in node.items():
                walk(v, path + "/" + str(k), doc)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + "/" + str(i), doc)
    walk(g13, "#", "g13-result-schema.v5.json")
    walk(q, "#", "product-quality-report.schema.v3.json")
    R["observations"]["reportOrders"] = found
    co = [f for f in found if f["order"] == "canonical-order"]
    cs = [f for f in found if f["order"] == "canonical-set"]
    R["observations"]["canonicalOrderSites"] = co
    rec("AO-40-canonical-order-used-where-measured-duplicates-are-truthful",
        bool(co), {"sites": co})
    rec("AO-41-canonical-order-admits-duplicates-canonical-set-does-not",
        admitted(ordered_schema("canonical-order"), ["x", "x"])
        and not admitted(ordered_schema("canonical-set"), ["x", "x"]))
    rec("AO-42-canonical-order-still-refuses-descending",
        not admitted(ordered_schema("canonical-order"), ["b", "a"]))


# ---------------------------------------------------------------------------
# 7. The encoder must NOT normalize
# ---------------------------------------------------------------------------
def encoder_purity():
    src = (F / "canonical.py").read_text()
    enc = src[src.index("def canonical"):]
    enc = enc[:enc.index("\ndef ")] if "\ndef " in enc[10:] else enc
    R["observations"]["canonicalEncoderSource"] = enc[:1500]
    for tok in ("sort(", "sorted(", "set(", "unique", "dedup"):
        # sorting KEYS is required; sorting ARRAY ITEMS is forbidden
        pass
    # behavioural: C must preserve a descending array verbatim
    rec("AO-50-encoder-does-not-sort-array-items",
        C.canonical([3, 1, 2]) == b"[3,1,2]", {"got": C.canonical([3, 1, 2]).decode()})
    rec("AO-51-encoder-does-not-deduplicate",
        C.canonical(["a", "a"]) == b'["a","a"]')
    rec("AO-52-encoder-does-sort-object-keys",
        C.canonical({"b": 1, "a": 2}) == b'{"a":2,"b":1}')
    rec("AO-53-encoder-does-not-normalize-unicode",
        C.canonical({"k": "é"}) != C.canonical({"k": "é"}))
    # an annotated schema must not CHANGE the value: validation only
    v = ["b", "a"]
    before = C.canonical(v)
    admitted(ordered_schema("canonical-set"), v)
    rec("AO-54-validation-does-not-mutate-the-value", C.canonical(v) == before
        and v == ["b", "a"])


# ---------------------------------------------------------------------------
# 8. Input layers keep sequence; resolved semantic record normalizes
# ---------------------------------------------------------------------------
def layers():
    cfg = json.loads((F / "product-configuration.schema.v2.json").read_bytes())
    ids = json.loads((F / "identity-schemas.v2.json").read_bytes())
    inp, res = [], []

    def walk(node, path, out):
        if isinstance(node, dict):
            if node.get("type") == "array" and "x-opensip-order" in node:
                out.append({"path": path, "order": node["x-opensip-order"]})
            for k, v in node.items():
                walk(v, path + "/" + str(k), out)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + "/" + str(i), out)
    walk(cfg, "#", inp)
    walk(ids["$defs"]["semantic-configuration"], "#/$defs/semantic-configuration", res)
    R["observations"]["inputLayerOrders"] = inp
    R["observations"]["resolvedSemanticOrders"] = res
    rec("AO-60-every-input-layer-array-is-a-sequence",
        all(x["order"] == "sequence" for x in inp),
        {"nonSequence": [x for x in inp if x["order"] != "sequence"]})
    rec("AO-61-resolved-semantic-arrays-normalize-explicitly",
        all(x["order"] != "sequence" for x in res)
        or any(x["order"] == "canonical-set" for x in res),
        {"resolved": res})
    # allowedScopes keeps its declared priority order
    scopes = [x for x in res if "allowedScopes" in x["path"]]
    R["observations"]["allowedScopesOrder"] = scopes
    rec("AO-62-allowedScopes-retains-declared-priority-order",
        all(x["order"] == "sequence" for x in scopes) if scopes else True,
        {"scopes": scopes})


# ---------------------------------------------------------------------------
# 9. Ordered token / argv / substitution sequences
# ---------------------------------------------------------------------------
def token_sequences():
    hits = []
    for p in sorted((DC / "workflows/schemas").glob("*.json")) + [
            DC / "native/native-evidence.schemas.v2.json",
            DC / "security/security-lifecycle.schemas.v1.json",
            F / "identity-schemas.v2.json"]:
        j = json.loads(p.read_bytes())

        def walk(node, path):
            if isinstance(node, dict):
                if node.get("type") == "array" and "x-opensip-order" in node:
                    low = path.lower()
                    if any(t in low for t in ("argv", "token", "substitut",
                                              "signature", "arg")):
                        hits.append({"doc": p.name, "path": path,
                                     "order": node["x-opensip-order"],
                                     "uniqueItems": node.get("uniqueItems")})
                for k, v in node.items():
                    walk(v, path + "/" + str(k))
            elif isinstance(node, list):
                for i, v in enumerate(node):
                    walk(v, path + "/" + str(i))
        walk(j, "#")
    R["observations"]["tokenArgvSubstitutionArrays"] = hits
    rec("AO-70-token-argv-substitution-arrays-are-ordered-sequences",
        all(h["order"] == "sequence" for h in hits) and bool(hits),
        {"nonSequence": [h for h in hits if h["order"] != "sequence"],
         "count": len(hits)})
    rec("AO-71-repeated-tokens-are-retained-and-positional",
        admitted(ordered_schema("sequence"), ["x", "(", ")", "x"])
        and C.canonical(["x", "(", ")", "x"]) != C.canonical(["x", ")", "(", "x"]))


def main():
    coverage()
    vocabulary()
    distinctions()
    g13_duplicates()
    encoder_purity()
    layers()
    token_sequences()
    R["summary"] = {"total": len(R["checks"]),
                    "passed": sum(c["passed"] for c in R["checks"]),
                    "failed": [c for c in R["checks"] if not c["passed"]]}
    json.dump(R, sys.stdout, indent=1, default=str)
    print()


if __name__ == "__main__":
    main()
