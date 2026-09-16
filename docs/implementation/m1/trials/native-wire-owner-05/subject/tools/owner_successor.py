"""Owner pattern-evaluation successor, SCOPED (candidate 05; review-03 RF-1/RF-2, review-04 RF-2/RF-3).

SELECTED FINAL OWNER, NOW WITH A CLOSED SCOPE. The declared JSON Schema 2020-12 dialect (ECMA-262 RegExp, flags u)
decides `pattern` for exactly the (document, consumer) pairs in SCOPE, and nowhere else:

  native-evidence-model   evidence schema held by native_evidence_model.v2 (SCHEMAS) and validated through its C
                          (validate_native, native_identity, file_manifest_identity, dependency and prepared set admission)
  provider-startup-model  the evidence schema copy held by provider_startup_model.v1 (BUNDLE, reached through REGISTRY by
                          validate_startup, e.g. OpenUniverseV3 crateRootPaths)
  provider-wire-model     the occupancy companion schema held by provider_wire_model.v1 (COMPANION, reached through REGISTRY
                          by validate_wire and admit_fact_batch)
  identity-model-v3-registered-records
                          the relation-payload schema in identity-model.v3 validate_registered_record's local registry: the
                          admission call retained fact admission makes for every relation payload (registered_payload)

The terminator-bounded lookahead `(?!.*(^|/)\\.\\.?(/|$))` is corrected to `(?![\\s\\S]*(^|/)\\.\\.?(/|$))` at every
occurrence in the ROW documents: the evidence schema (34) and the relation-payload schema (1: CanonicalPath, used by
FilePayloadV1.path, PackagePayloadV1.manifestPath, VcsChangePayloadV1.path and previousPath). Model regexes of the native
model that compile or mirror evidence schema patterns (_LOGICAL_RE, _UNIT_ROOT_RE, _MEMBER_ROOT_RE) evaluate the same ECMA
pattern.

HOW THE SCOPE IS ENFORCED. No canonical module is modified and no ExactValidator class is replaced. In each scoped module
instance only the module-level name `C` is rebound to a ScopedCanonical proxy whose validator evaluates a `pattern` as ECMA
iff its schema node carries NODE_MARK, and delegates every other node to the pinned Python evaluation of that very
canonical module; NODE_MARK is added only to pattern nodes of the scoped document object that module holds. Every other
document (identity v2/v3, workflows, c2v3, rust2, startup, handshake, fact-batch, import/enumeration schemas) and every
other canonical copy (identity-model.py v2 IM.C, nested NE.STARTUP/NE.WIRE copies, fact-plane FP) is evaluated exactly as
pinned; check.py executes no-change checks for each document review-04 named. Applied in memory to freshly loaded pinned
models only; never to source files.
"""
import ast
import copy
import hashlib
import importlib.util
import json
import re
from pathlib import Path

from jsonschema.exceptions import ValidationError
from jsonschema import validators
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

import wirecodec as W

MARK = "OPENSIP_OWNER_PATTERN_SUCCESSOR"
NODE_MARK = "x-opensip-successor-ecma-pattern"
DEFECT_TOKEN = "(?!.*("
CORRECT_TOKEN = "(?![\\s\\S]*("
FLAGS = "u"
ROW_DOC_KEYS = ["evidence", "relationRegistry2"]
EVALUATED_DOC_KEYS = ["evidence", "occupancy", "relationRegistry2"]
RELATION_DOC_PATH = "foundation/relation-payload-schemas.v2.json"
MODEL_FILES = {"nativeModel": "native_evidence_model.v2.py", "startupModel": "provider_startup_model.v1.py", "wireModel": "provider_wire_model.v1.py",
               "identityModel3": "identity-model.v3.py"}
WRAPPED_SELECTORS = ["dependency_source_set_admit", "prepared_output_set_admit", "generated_include_lookup", "file_manifest_identity", "_source_kind", "parse_cargo_lock"]
SCOPE = [
    {"id": "native-evidence-model", "documentKey": "evidence", "moduleKey": "nativeModel", "instance": "NE", "binding": "SCHEMAS", "registry": None,
     "consumers": ["validate_native", "native_identity", "file_manifest_identity", "dependency_source_set_admit", "prepared_output_set_admit"]},
    {"id": "provider-startup-model", "documentKey": "evidence", "moduleKey": "startupModel", "instance": "ST", "binding": "BUNDLE", "registry": "REGISTRY",
     "consumers": ["validate_startup"]},
    {"id": "provider-wire-model", "documentKey": "occupancy", "moduleKey": "wireModel", "instance": "WI", "binding": "COMPANION", "registry": "REGISTRY",
     "consumers": ["validate_wire", "admit_fact_batch"]},
    {"id": "identity-model-v3-registered-records", "documentKey": "relationRegistry2", "moduleKey": "identityModel3", "instance": "IM3",
     "binding": "_LOCAL_REGISTRY[" + RELATION_DOC_PATH + "]", "registry": "_LOCAL_REGISTRY", "consumers": ["validate_registered_record"]},
]
NO_CHANGE_DOC_KEYS = ["identitySchemas2", "identitySchemas3", "workflowCommon", "c2v3", "rust2"]


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


def mark_patterns(doc):
    count = 0

    def walk(o):
        nonlocal count
        if isinstance(o, dict):
            if isinstance(o.get("pattern"), str):
                o[NODE_MARK] = True
                count += 1
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(doc)
    return count


def marked_documents(obj, acc=None, seen=None):
    """$ids of every schema document (dict with $id) reachable in obj that carries at least one NODE_MARK."""
    acc = set() if acc is None else acc
    seen = set() if seen is None else seen

    def has_mark(o):
        if isinstance(o, dict):
            return o.get(NODE_MARK) is True or any(has_mark(v) for v in o.values())
        if isinstance(o, list):
            return any(has_mark(v) for v in o)
        return False
    if id(obj) in seen:
        return acc
    seen.add(id(obj))
    if isinstance(obj, dict) and isinstance(obj.get("$id"), str) and "$defs" in obj:
        if has_mark(obj):
            acc.add(obj["$id"])
        return acc
    if isinstance(obj, dict):
        for v in obj.values():
            marked_documents(v, acc, seen)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            marked_documents(v, acc, seen)
    return acc


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
    """Module-level functions that call canonical validation (C.validate or C.ExactValidator)."""
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
            literal = ast.literal_eval(arg) if arg[:2] in ('r"', "r'") else None
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
    docs = {key: json.loads(raw(key)) for key in set(ROW_DOC_KEYS + EVALUATED_DOC_KEYS)}
    rows = [r for key in ROW_DOC_KEYS for r in pattern_rows(docs[key])]
    effective_evidence = effective_docs({docs["evidence"]["$id"]: docs["evidence"]}, rows)[docs["evidence"]["$id"]]
    model_text = raw("nativeModel").decode("utf-8")
    inventory = regex_inventory(model_text, docs["evidence"])
    texts = {k: raw(k).decode("utf-8") for k in MODEL_FILES}
    pins = {r["key"]: r for r in pin_rows}
    scope = []
    for s in SCOPE:
        marked = copy.deepcopy(docs[s["documentKey"]])
        scope.append(dict(s, document=docs[s["documentKey"]]["$id"], module=MODEL_FILES[s["moduleKey"]], markedPatternNodes=mark_patterns(marked)))
    no_change = []
    for key in NO_CHANGE_DOC_KEYS:
        p = pins[key]
        no_change.append({"key": key, "path": p["path"], "sha256": p["sha256"],
                          "rule": "not a scoped document: evaluated exactly as pinned by every consumer, including the scoped module instances (unmarked nodes delegate to pinned Python evaluation)"})
    return {
        "artifact": "opensip.native-evidence.owner-pattern-evaluation.successor", "version": "2",
        "standing": "AUTHOR candidate 05 scoped successor to owner schema pattern evaluation for the closed (document, consumer) scope below, and to every occurrence of the terminator-bounded path lookahead in the evidence and relation-payload schema documents. Parent bytes unchanged; applied in memory by tools/owner_successor.py; not approval.",
        "parents": [pins[k] for k in ["evidence", "occupancy", "relationRegistry2", "canonical", "nativeModel", "startupModel", "wireModel", "identityModel3"]],
        "selectedOwner": {
            "law": "Within scope, an owner schema `pattern` is an ECMA-262 RegExp evaluated with flags u; the scoped model regexes evaluate the same ECMA pattern. Outside scope every pattern keeps its pinned evaluation.",
            "chosenOver": ["Python re evaluation of the scoped documents", "refusing every string on which ECMA and Python re disagree (a new restriction on POSIX file names)", "a global replacement of every canonical ExactValidator copy (review-04 RF-2: it changed identity, workflows, c2v3 and rust2 consumers outside the declared parents)"],
            "reason": "the scoped documents declare JSON Schema 2020-12 and carry the wire-reached and fact-payload path sites; the declared semantics are corrected there without changing unrelated owners"},
        "evaluator": {"keyword": "pattern", "engine": "ECMA-262 RegExp", "flags": FLAGS, "nodeMarker": NODE_MARK,
                      "mechanism": "per scoped module instance, module-level C is rebound to ScopedCanonical: validate() replicates canonical.validate (typed, then ExactValidator.validate) with a validator extending that module's ExactValidator by a pattern keyword that is ECMA for marked nodes and the pinned pattern evaluation otherwise; marks are added only to the scoped document object",
                      "translation": "tools/wirecodec.py ecma_to_python, differential-checked against the pinned ECMA-262 engine (ecma-owner-differential)",
                      "reference": "tools/owner_successor.py install"},
        "scope": scope,
        "noChangeDocuments": no_change,
        "patternCorrection": {"defectToken": DEFECT_TOKEN, "correctToken": CORRECT_TOKEN,
                              "why": "`.` excludes the four line terminators, so the lookahead never saw a `..` segment after a terminator; `[\\s\\S]` scans the complete string, while `(^|/)` and `(/|$)` keep exact segment boundaries (no m flag), so `..<LF>` stays a legitimate segment"},
        "schemaPatternRows": rows,
        "relationPayloadPathSites": relation_path_sites(docs["relationRegistry2"]),
        "modelRegexInventory": inventory,
        "modelRegexRows": regex_rows(inventory, effective_evidence),
        "selectorSources": {
            "canonical": source_closure(raw("canonical").decode("utf-8"), ["validate", "ExactValidator", "typed"]),
            "nativeModel": source_closure(model_text, WRAPPED_SELECTORS + validate_callers(model_text)),
            "startupModel": source_closure(texts["startupModel"], validate_callers(texts["startupModel"])),
            "wireModel": source_closure(texts["wireModel"], validate_callers(texts["wireModel"])),
            "identityModel3": source_closure(texts["identityModel3"], ["validate_registered_record"]),
        },
        "unchanged": ["every parent byte and every source file",
                      "every canonical module object and its ExactValidator class (no canonical copy is modified)",
                      "every document outside scope[*].document, as evaluated by every consumer including the scoped module instances",
                      "identity-model.py (v2, NE.IM) and every nested model copy (NE.STARTUP, NE.WIRE, WI.FP, identity-model.v3 lazy workflow/native copies)",
                      "the pinned module-level RELATION_DOCUMENT object of identity-model.v3 (only its local registry copy is scoped)",
                      "model-local Python regexes (modelRegexInventory kind model-local)",
                      "all non-pattern keywords and the canonical const/enum/order/integer semantics"],
    }


def relation_path_sites(relation_doc):
    """Every property in the relation-payload document whose schema is a $ref to #/$defs/CanonicalPath."""
    out = []
    for name, d in relation_doc["$defs"].items():
        for prop, sch in (d.get("properties") or {}).items():
            if isinstance(sch, dict) and sch.get("$ref") == "#/$defs/CanonicalPath":
                out.append("#/$defs/%s/properties/%s" % (name, prop))
    return sorted(out)


# ---------------------------------------------------------------- scoped reference installation
class ScopedCanonical:
    """A per-module view of one pinned canonical module: ECMA `pattern` for marked nodes, pinned evaluation otherwise."""

    def __init__(self, base, flags):
        self._base = base
        pinned_pattern = base.ExactValidator.VALIDATORS["pattern"]

        def pattern(validator, patrn, instance, schema):
            if isinstance(schema, dict) and schema.get(NODE_MARK) is True:
                if validator.is_type(instance, "string") and not W.ecma_test(patrn, flags, instance):
                    yield ValidationError("%r does not match ECMA-262 /%s/%s" % (instance, patrn, flags))
            else:
                yield from pinned_pattern(validator, patrn, instance, schema)
        self.ExactValidator = validators.extend(base.ExactValidator, {"pattern": pattern})

    def validate(self, schema, value, registry=None):
        self._base.typed(value)
        if registry is None:
            self.ExactValidator(schema).validate(value)
        else:
            self.ExactValidator(schema, registry=registry).validate(value)
        return value

    def __getattr__(self, name):
        return getattr(self._base, name)


def _registry(docs):
    return Registry().with_resources([(d["$id"], Resource(contents=d, specification=DRAFT202012)) for d in docs])


def install(mods, succ, only=None):
    """Install the scoped successor on the model instances {NE, ST, WI, IM3}; `only` restricts to listed scope ids."""
    flags = succ["evaluator"]["flags"]
    rows = succ["schemaPatternRows"]
    for s in succ["scope"]:
        if only is not None and s["id"] not in only:
            continue
        mod = mods[s["instance"]]
        if s["instance"] == "IM3":
            if mod._LOCAL_REGISTRY is None:
                mod.validate_registered_record(RELATION_DOC_PATH, "#/$defs/CanonicalPath", "a")
            _reg, by_path = mod._LOCAL_REGISTRY
            doc = by_path[RELATION_DOC_PATH]
            apply_rows(doc, rows)
            mark_patterns(doc)
            mod._LOCAL_REGISTRY = (_registry(by_path.values()), by_path)
        else:
            doc = getattr(mod, s["binding"])
            if doc.get("$id") != s["document"]:
                raise ValueError("scope binding does not hold the scoped document: " + s["id"])
            apply_rows(doc, rows)
            mark_patterns(doc)
            if s["registry"]:
                held = [v for v in vars(mod).values() if isinstance(v, dict) and isinstance(v.get("$id"), str) and "$defs" in v]
                setattr(mod, s["registry"], _registry(held))
        if not isinstance(mod.C, ScopedCanonical):
            mod.C = ScopedCanonical(mod.C, flags)
        if s["instance"] == "NE":
            for r in succ["modelRegexRows"]:
                setattr(mod, r["name"], re.compile(W.ecma_to_python(r["ecmaPattern"], flags)))
        setattr(mod, MARK, True)
    return mods


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_models(arch, succ, prefix, only=None):
    base = Path(arch) / "docs/coop/design-corrections"
    mods = {"NE": load(prefix + "ne", base / "native" / MODEL_FILES["nativeModel"]), "ST": load(prefix + "st", base / "native" / MODEL_FILES["startupModel"]),
            "WI": load(prefix + "wi", base / "native" / MODEL_FILES["wireModel"]), "IM3": load(prefix + "im3", base / "foundation" / MODEL_FILES["identityModel3"])}
    if succ is not None:
        install(mods, succ, only)
    return mods


def require_installed(mod):
    if not getattr(mod, MARK, False):
        raise RuntimeError("the owner pattern-evaluation successor is not installed on this owner model instance")
