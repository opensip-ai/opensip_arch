"""Owner pattern-evaluation successor (candidate 04; review-03 RF-1 and RF-2).

SELECTED FINAL OWNER. The declared JSON Schema 2020-12 dialect wins: every `pattern` keyword evaluated by the pinned
foundation/canonical.py ExactValidator (the validator behind native_evidence_model.v2 validate_native / native_identity,
provider_startup_model.v1 and provider_wire_model.v1 validation, and every other canonical.validate caller) is an
ECMA-262 RegExp with flags `u`, not a Python `re` expression. The owner path pattern whose negative lookahead
`(?!.*(^|/)\\.\\.?(/|$))` stops at the first line terminator is corrected to scan the COMPLETE string,
`(?![\\s\\S]*(^|/)\\.\\.?(/|$))`, at EVERY occurrence in the pinned owner schema documents. Model regular expressions
that compile or mirror owner schema patterns follow the same law.

Consequences: `a/..<LF>`, `..<LF>` and `a/.<LF>` are legitimate names (a segment `..<LF>` is not `..`) and are admitted
by the owner; `x<LF>/../y` and `a<U+2028>/../b` contain a real `..` segment and are refused. No spelling is normalized,
coerced or truncated. The alternative of refusing every string on which the two dialects disagree was not taken: it
would invent a restriction on POSIX file names instead of fixing the declared-schema semantics.

install() applies the successor in memory to freshly loaded instances of the PINNED models (never to source files):
it extends every loaded canonical.ExactValidator with the ECMA pattern keyword, applies schemaPatternRows to every
loaded owner schema document (verifying each `from` value), rebuilds module registries over those documents, and
recompiles modelRegexRows through the differential-checked translation tools/wirecodec.ecma_to_python.
"""
import ast
import copy
import hashlib
import importlib.util
import json
import re
from pathlib import Path

from jsonschema import validators
from jsonschema.exceptions import ValidationError
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

import wirecodec as W

MARK = "OPENSIP_OWNER_PATTERN_SUCCESSOR"
DEFECT_TOKEN = "(?!.*("
CORRECT_TOKEN = "(?![\\s\\S]*("
FLAGS = "u"
EVALUATED_DOC_KEYS = ["evidence", "startup", "handshake", "occupancy", "factBatch3"]
MODEL_FILES = {"nativeModel": "native_evidence_model.v2.py", "startupModel": "provider_startup_model.v1.py", "wireModel": "provider_wire_model.v1.py"}
WRAPPED_SELECTORS = ["dependency_source_set_admit", "prepared_output_set_admit", "generated_include_lookup", "file_manifest_identity", "_source_kind", "parse_cargo_lock"]


def _esc(k):
    return k.replace("~", "~0").replace("/", "~1")


def corrected(pattern):
    return pattern.replace(DEFECT_TOKEN, CORRECT_TOKEN)


def pattern_rows(doc):
    """Every `pattern` in the whole document containing the terminator-bounded lookahead, with its correction."""
    rows = []

    def walk(o, p):
        if isinstance(o, dict):
            for k, v in o.items():
                q = p + "/" + _esc(k)
                if k == "pattern" and isinstance(v, str) and DEFECT_TOKEN in v:
                    rows.append({"document": doc["$id"], "pointer": q, "from": v, "to": corrected(v)})
                walk(v, q)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, p + "/" + str(i))
    walk(doc, "#")
    return rows


def node_at(doc, pointer):
    node = doc
    for part in [x for x in pointer.lstrip("#").split("/") if x]:
        part = part.replace("~1", "/").replace("~0", "~")
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node


def apply_rows(doc, rows):
    for r in rows:
        if r["document"] != doc.get("$id"):
            continue
        parent_ptr, last = r["pointer"].rsplit("/", 1)
        parent = node_at(doc, parent_ptr)
        if parent.get(last) != r["from"]:
            raise ValueError("owner pattern successor row does not match the pinned value: " + r["pointer"])
        parent[last] = r["to"]


def effective_docs(docs, rows):
    out = {sid: copy.deepcopy(d) for sid, d in docs.items()}
    for d in out.values():
        apply_rows(d, rows)
    return out


# ---------------------------------------------------------------- source digests (review-03 A-9)
def _defs(text):
    tree = ast.parse(text)
    defs = {}
    for n in tree.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            defs[n.name] = n
        elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            defs[n.targets[0].id] = n
    return defs


def source_closure(text, roots):
    """sha256 of the exact source segment of every module-level definition transitively named by the roots."""
    defs = _defs(text)
    seen, stack = [], list(roots)
    while stack:
        name = stack.pop()
        if name in seen or name not in defs:
            continue
        seen.append(name)
        for x in ast.walk(defs[name]):
            if isinstance(x, ast.Name) and x.id in defs and x.id not in seen:
                stack.append(x.id)
    return {name: hashlib.sha256(ast.get_source_segment(text, defs[name]).encode("utf-8")).hexdigest() for name in sorted(seen)}


def validate_callers(text):
    """Module-level functions of a model that call canonical validation (C.validate or C.ExactValidator)."""
    out = []
    for name, node in _defs(text).items():
        if not isinstance(node, ast.FunctionDef):
            continue
        for x in ast.walk(node):
            if isinstance(x, ast.Attribute) and isinstance(x.value, ast.Name) and x.value.id == "C" and x.attr in ("validate", "ExactValidator"):
                out.append(name)
                break
    return sorted(out)


# ---------------------------------------------------------------- model regex inventory
def _normalize_python_regex(src):
    return src.replace("\\x00", "\\u0000")[:-1] + "(?![\\s\\S])" if src.endswith("$") else src.replace("\\x00", "\\u0000")


def regex_inventory(model_text, evidence_doc):
    """Every `re.<call>(...)` in the pinned native model, classified. schema-derived: compiles an owner schema pattern;
    mirrors-owner-schema-pattern: a Python literal whose ECMA normalization equals an owner schema pattern; model-local:
    an authored Python regex that is not a schema pattern (outside the declared-schema dialect law; unchanged)."""
    tree = ast.parse(model_text)
    names = {}
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            names[id(n.value)] = n.targets[0].id
    schema_patterns = {}

    def walk(o, p):
        if isinstance(o, dict):
            for k, v in o.items():
                if k == "pattern" and isinstance(v, str):
                    schema_patterns.setdefault(v, p + "/pattern")
                walk(v, p + "/" + _esc(k))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, p + "/" + str(i))
    walk(evidence_doc, "#")
    rows = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "re":
            arg = ast.get_source_segment(model_text, node.args[0]) if node.args else ""
            row = {"line": node.lineno, "call": "re." + node.func.attr, "name": names.get(id(node)), "argument": arg}
            m = re.fullmatch(r'SCHEMAS\["\$defs"\]\["([A-Za-z0-9]+)"\]\["pattern"\]', arg)
            literal = None
            if arg[:2] in ('r"', "r'"):
                literal = ast.literal_eval(arg)
            if m:
                row.update(kind="schema-derived", schemaPointer="#/$defs/" + m.group(1) + "/pattern")
            elif literal is not None and _normalize_python_regex(literal) in schema_patterns:
                row.update(kind="mirrors-owner-schema-pattern", schemaPointer=schema_patterns[_normalize_python_regex(literal)])
            else:
                row.update(kind="model-local")
            rows.append(row)
    return sorted(rows, key=lambda r: r["line"])


def regex_rows(inventory, effective_evidence):
    return [{"module": MODEL_FILES["nativeModel"], "name": r["name"], "kind": r["kind"], "schemaPointer": r["schemaPointer"],
             "ecmaPattern": node_at(effective_evidence, r["schemaPointer"].rsplit("/", 1)[0])["pattern"]}
            for r in inventory if r["kind"] != "model-local"]


def successor_document(raw, pin_rows):
    docs = {key: json.loads(raw(key)) for key in EVALUATED_DOC_KEYS}
    rows = [r for key in EVALUATED_DOC_KEYS for r in pattern_rows(docs[key])]
    effective_evidence = effective_docs({docs["evidence"]["$id"]: docs["evidence"]}, rows)[docs["evidence"]["$id"]]
    model_text = raw("nativeModel").decode("utf-8")
    inventory = regex_inventory(model_text, docs["evidence"])
    texts = {k: raw(k).decode("utf-8") for k in ("nativeModel", "startupModel", "wireModel")}
    pins = {r["key"]: r for r in pin_rows}
    return {
        "artifact": "opensip.native-evidence.owner-pattern-evaluation.successor", "version": "1",
        "standing": "AUTHOR candidate 04 scoped successor to the owner schema pattern evaluation of foundation/canonical.py ExactValidator and to every occurrence of the terminator-bounded path lookahead in the pinned owner schema documents. Parent bytes unchanged; applied in memory by tools/owner_successor.py; not approval.",
        "parents": [pins[k] for k in EVALUATED_DOC_KEYS + ["canonical", "nativeModel", "startupModel", "wireModel"]],
        "selectedOwner": {
            "law": "Every owner schema `pattern` is an ECMA-262 RegExp evaluated with flags u (JSON Schema 2020-12), by every loaded canonical ExactValidator instance; model regexes that compile or mirror owner schema patterns evaluate the same ECMA pattern.",
            "chosenOver": ["Python re evaluation by the pinned canonical ExactValidator", "refusing every string on which ECMA and Python re disagree (a new restriction on POSIX file names)"],
            "reason": "the schema documents declare JSON Schema 2020-12, whose pattern dialect is ECMA-262; the declared semantics are corrected rather than a file-name restriction invented"},
        "evaluator": {"keyword": "pattern", "engine": "ECMA-262 RegExp", "flags": FLAGS,
                      "validator": "foundation/canonical.py ExactValidator, extended in every loaded instance (native model C and IM.C, startup model C, wire model C)",
                      "translation": "tools/wirecodec.py ecma_to_python, differential-checked against the pinned ECMA-262 engine over every owner pattern (check ecma-owner-differential)",
                      "reference": "tools/owner_successor.py install"},
        "patternCorrection": {"defectToken": DEFECT_TOKEN, "correctToken": CORRECT_TOKEN,
                              "why": "`.` excludes the four line terminators, so the lookahead never saw a `..` segment after a terminator; `[\\s\\S]` scans the complete string, while `(^|/)` and `(/|$)` keep exact segment boundaries (no m flag), so `..<LF>` stays a legitimate segment"},
        "schemaPatternRows": rows,
        "modelRegexInventory": inventory,
        "modelRegexRows": regex_rows(inventory, effective_evidence),
        "selectorSources": {
            "canonical": source_closure(raw("canonical").decode("utf-8"), ["validate", "ExactValidator"]),
            "nativeModel": source_closure(model_text, WRAPPED_SELECTORS + validate_callers(model_text)),
            "startupModel": source_closure(texts["startupModel"], validate_callers(texts["startupModel"])),
            "wireModel": source_closure(texts["wireModel"], validate_callers(texts["wireModel"])),
        },
        "unchanged": ["every parent byte", "every pattern without the terminator-bounded lookahead", "model-local Python regexes (modelRegexInventory kind model-local)", "all non-pattern keywords and the canonical const/enum/order/integer semantics"],
    }


# ---------------------------------------------------------------- reference installation
def ecma_validator_class(base, flags):
    def pattern(validator, patrn, instance, schema):
        if validator.is_type(instance, "string") and not W.ecma_test(patrn, flags, instance):
            yield ValidationError("%r does not match ECMA-262 /%s/%s" % (instance, patrn, flags))
    return validators.extend(base, {"pattern": pattern})


def _canonical_modules(mod):
    out, frontier = [], [mod]
    for m in frontier:
        for v in list(vars(m).values()):
            if type(v).__name__ == "module" and hasattr(v, "__file__") and v not in frontier and "design-corrections" in str(getattr(v, "__file__", "")):
                frontier.append(v)
    for m in frontier:
        if hasattr(m, "ExactValidator") and hasattr(m, "validate") and m not in out:
            out.append(m)
    return out


def install(mod, succ):
    flags = succ["evaluator"]["flags"]
    for C in _canonical_modules(mod):
        if not getattr(C, MARK, False):
            C.ExactValidator = ecma_validator_class(C.ExactValidator, flags)
            setattr(C, MARK, True)
    docs = [v for v in vars(mod).values() if isinstance(v, dict) and isinstance(v.get("$id"), str) and "$defs" in v]
    for d in docs:
        apply_rows(d, succ["schemaPatternRows"])
    if isinstance(getattr(mod, "REGISTRY", None), Registry):
        mod.REGISTRY = Registry().with_resources([(d["$id"], Resource(contents=d, specification=DRAFT202012)) for d in docs])
    if Path(getattr(mod, "__file__", "")).name == MODEL_FILES["nativeModel"]:
        for r in succ["modelRegexRows"]:
            setattr(mod, r["name"], re.compile(W.ecma_to_python(r["ecmaPattern"], flags)))
    setattr(mod, MARK, True)
    return mod


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_models(arch, succ, prefix):
    native = Path(arch) / "docs/coop/design-corrections/native"
    mods = {"NE": load(prefix + "ne", native / MODEL_FILES["nativeModel"]), "ST": load(prefix + "st", native / MODEL_FILES["startupModel"]),
            "WI": load(prefix + "wi", native / MODEL_FILES["wireModel"])}
    if succ is not None:
        for m in mods.values():
            install(m, succ)
    return mods


def require_installed(mod):
    if not getattr(mod, MARK, False):
        raise RuntimeError("the owner pattern-evaluation successor is not installed on this owner model instance")
