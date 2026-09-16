"""Independent reviewer-02 probes: adapter reproduction, adapter mutations, successor/override negatives.

Read-only against the frozen subject and architecture. Temporary copies are created only
under this review directory.
"""
import copy
import importlib.util
import json
import shutil
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, validators
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

REVIEW = Path("/tmp/opensip-implementation/m1-metadata-review-02")
SUBJECT = Path("/tmp/opensip-implementation/m1-metadata-subject-02/docs/implementation/m1/metadata-v2")
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
EID = "urn:opensip:product-v1:workflows:evaluator3:command-envelope:4"
MID = "urn:opensip:product-v1:workflows:metadata:1"

results = []


def probe(pid, got, expected, note=""):
    results.append({"id": pid, "expected": expected, "observed": got, "pass": got == expected, "note": note})


def import_checker(folder, name):
    spec = importlib.util.spec_from_file_location(name, folder / "check_metadata.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cm = import_checker(SUBJECT, "checker_v2")
reference, reg_adapter, documents = cm.load(ARCH)
fixture = json.loads((SUBJECT / "fixtures.json").read_bytes())
cases = {c["id"]: c for c in fixture["cases"]}
E4 = documents[EID]

# Registry reproducing metadata-v1 behaviour: full contents (with $schema), dialect inferred.
reg_raw = Registry().with_resources((k, Resource.from_contents(v)) for k, v in documents.items())

# Registry with $schema retained but explicit spec: isolates "contents keep $schema" as the trigger.
reg_raw_explicit = Registry().with_resources((k, Resource(contents=v, specification=DRAFT202012)) for k, v in documents.items())


def valid(schema, value, registry, cls=None):
    cls = cls or reference.ExactValidator
    return cls(schema, registry=registry).is_valid(value)


# ---- 1. Mechanism: count custom keyword calls reached through each registry
calls = {"order": 0, "const": 0}


def counting_order(v, order, instance, schema):
    calls["order"] += 1
    yield from reference.exact_order(v, order, instance, schema)


def counting_const(v, expected, instance, schema):
    calls["const"] += 1
    yield from reference.exact_const(v, expected, instance, schema)


Counting = validators.extend(
    Draft202012Validator,
    validators={"const": counting_const, "enum": reference.exact_enum, "x-opensip-order": counting_order},
    type_checker=Draft202012Validator.TYPE_CHECKER.redefine("integer", lambda c, v: type(v) is int),
)
help_ok = cases["help-top-level"]["value"]
for label, reg in (("raw", reg_raw), ("raw-explicit-spec", reg_raw_explicit), ("adapter", reg_adapter)):
    calls.update(order=0, const=0)
    Counting(E4, registry=reg).is_valid(help_ok)
    probe("mechanism-order-calls-through-envelope-" + label, calls["order"] > 0, label == "adapter",
          "x-opensip-order on meta.commands reached only if the validator class survives the external-root $ref")

# Direct $defs pointer bypass (why earlier direct probes did not see the loss)
calls.update(order=0)
Counting({"$ref": MID + "#/$defs/HelpMetadataV1"}, registry=reg_raw).is_valid(help_ok["meta"])
probe("mechanism-direct-defs-pointer-keeps-custom-validator-raw", calls["order"] > 0, True)
calls.update(order=0)
Counting({"$ref": MID}, registry=reg_raw).is_valid(help_ok["meta"])
probe("mechanism-root-ref-drops-custom-validator-raw", calls["order"] > 0, False)

# ---- 2. Behavioural reproduction of the 2 TS/Python disagreements and more
for cid in ("unsorted-help", "duplicate-help-name"):
    v = cases[cid]["value"]
    probe("repro-" + cid + "-schema-only-raw-accepts", valid(E4, v, reg_raw), True, "metadata-v1 registry behaviour (bug)")
    probe("repro-" + cid + "-schema-only-adapter-refuses", valid(E4, v, reg_adapter), False)

rev_rel = copy.deepcopy(help_ok)
rev_rel["meta"] = {"command": "version", "hostRelease": "1.0.0", "buildChannel": "release",
                   "closureIds": ["closure2:" + "2" * 64, "closure2:" + "1" * 64]}
probe("repro-release-closure-order-envelope-raw-accepts", valid(E4, rev_rel, reg_raw), True)
probe("repro-release-closure-order-envelope-adapter-refuses", valid(E4, rev_rel, reg_adapter), False)
dup_rel = copy.deepcopy(rev_rel)
dup_rel["meta"]["closureIds"] = ["closure2:" + "1" * 64] * 2
probe("repro-release-closure-duplicate-envelope-raw", valid(E4, dup_rel, reg_raw), False, "uniqueItems is standard, so still refused")
probe("repro-release-closure-duplicate-envelope-adapter", valid(E4, dup_rel, reg_adapter), False)

# Exact const/enum loss through external roots: bool vs int in common:3 referenced roots?
probe("standard-const-true-vs-1", Draft202012Validator({"const": 1}).is_valid(True), False,
      "jsonschema equal() distinguishes bool/int, so const loss matters mainly for order annotations")
probe("standard-enum-false-vs-0", Draft202012Validator({"enum": [0]}).is_valid(False), False)

# Invented development closure: schema-only through envelope
inv = cases["invented-development-closure"]["value"]
probe("dev-closure-schema-only-raw", valid(E4, inv, reg_raw), False, "maxItems/if-const are standard keywords; rule never depended on custom validator")
probe("dev-closure-schema-only-adapter", valid(E4, inv, reg_adapter), False)

# ---- 3. Full-fixture differential raw vs adapter (schema-only, no semantic admission)
diff = []
for c in fixture["cases"]:
    a, b = valid(E4, c["value"], reg_raw), valid(E4, c["value"], reg_adapter)
    if a != b:
        diff.append((c["id"], a, b))
probe("fixture-differential-raw-vs-adapter", sorted(d[0] for d in diff), ["duplicate-help-name", "unsorted-help"],
      "only the ordering cases may differ")
accepted_fail = [c["id"] for c in fixture["cases"] if c["accepted"] and not valid(E4, c["value"], reg_adapter)]
probe("adapter-accepts-all-accepted-cases-schema-only", accepted_fail, [])

# ---- 4. Adapter projection fidelity
fidelity = all(
    reg_adapter.contents(k) == {kk: vv for kk, vv in documents[k].items() if kk != "$schema"} for k in documents
)
probe("adapter-contents-equal-original-minus-schema", fidelity, True)
probe("adapter-specification-is-draft202012",
      all(reg_adapter.get_or_retrieve(k).value._specification is DRAFT202012 for k in documents), True)


def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield path + "/" + k, k, v
            yield from walk(v, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + "/" + str(i))


nested_schema, dynamic, embedded_ids, root_refs = [], [], [], set()
for doc_id, doc in documents.items():
    for p, k, v in walk(doc):
        if k == "$schema" and p != "/$schema":
            nested_schema.append((doc_id, p))
        if k in ("$dynamicRef", "$recursiveRef", "$dynamicAnchor", "$recursiveAnchor"):
            dynamic.append((doc_id, p))
        if k == "$id" and p != "/$id":
            embedded_ids.append((doc_id, p))
        if k == "$ref" and isinstance(v, str) and not v.startswith("#"):
            target, _, frag = v.partition("#")
            if frag in ("", "/"):
                root_refs.add((doc_id, target))
probe("no-nested-$schema-in-28-docs", nested_schema, [])
probe("no-dynamic-or-recursive-refs", dynamic, [])
probe("no-embedded-$id-resources", embedded_ids, [], "embedded resources would carry their own dialect selection")
Path(REVIEW / "root-refs.json").write_text(json.dumps(sorted(root_refs), indent=1))
probe("external-root-ref-edges-listed", len(root_refs) > 0, True, "blast radius written to root-refs.json")

# ---- 5. Mutations: does the new checker assertion detect loss?
def checker_schema_only_assertion(envelope, registry):
    for case_id in ("unsorted-help", "duplicate-help-name", "invented-development-closure"):
        if reference.ExactValidator(envelope, registry=registry).is_valid(cases[case_id]["value"]):
            return False
    return True


probe("mutation-revert-adapter-killed-by-new-assertion", checker_schema_only_assertion(E4, reg_raw), False)


def registry_with(mutate):
    docs = copy.deepcopy(documents)
    mutate(docs)
    reg = Registry().with_resources((k, Resource(contents={kk: vv for kk, vv in v.items() if kk != "$schema"}, specification=DRAFT202012)) for k, v in docs.items())
    return docs, reg


docs_m, reg_m = registry_with(lambda d: d[MID]["$defs"]["HelpMetadataV1"]["properties"]["commands"].pop("x-opensip-order"))
probe("mutation-drop-help-order-killed-by-new-assertion", checker_schema_only_assertion(docs_m[EID], reg_m), False)
docs_m, reg_m = registry_with(lambda d: d[MID]["$defs"]["VersionMetadataV1"].__setitem__("allOf", []))
probe("mutation-drop-dev-closure-rule-killed-by-new-assertion", checker_schema_only_assertion(docs_m[EID], reg_m), False)
docs_m, reg_m = registry_with(lambda d: d[MID]["$defs"]["VersionMetadataV1"]["properties"]["closureIds"].pop("x-opensip-order"))
probe("mutation-drop-closure-order-killed-by-new-assertion", checker_schema_only_assertion(docs_m[EID], reg_m), True,
      "not killed: no schema-only external-root case for release closure order (only direct $defs BuildMetadataV1 check)")
killed_direct = reference.ExactValidator({"$ref": MID + "#/$defs/BuildMetadataV1"}, registry=reg_m).is_valid(
    {"schemaVersion": 1, "hostRelease": "1.0.0", "buildChannel": "release", "closureIds": ["closure2:" + "2" * 64, "closure2:" + "1" * 64]})
probe("mutation-drop-version-closure-order-vs-direct-build-check", killed_direct, False,
      "BuildMetadataV1 order annotation is separate and untouched, so direct check still refuses; VersionMetadataV1 order mutant survives checker")

# Alternate subtle adapter mutation: keep $schema but explicit spec (does not fix)
probe("mutation-adapter-explicit-spec-only-insufficient", checker_schema_only_assertion(E4, reg_raw_explicit), False)

# ---- 6. admit_build negatives
def raises(fn):
    try:
        fn()
        return False
    except (AssertionError, Exception):
        return True


b = fixture["build"]
probe("admit-build-dev-dev", raises(lambda: cm.admit_build(reference, reg_adapter, b, "development")), False)
probe("admit-build-dev-release", raises(lambda: cm.admit_build(reference, reg_adapter, b, "release")), True)
rel = {**b, "buildChannel": "release", "closureIds": ["closure2:" + "1" * 64]}
probe("admit-build-release-dev-asset", raises(lambda: cm.admit_build(reference, reg_adapter, rel, "development")), True)
probe("admit-build-channel-case", raises(lambda: cm.admit_build(reference, reg_adapter, b, "Development")), True)
probe("admit-build-channel-none", raises(lambda: cm.admit_build(reference, reg_adapter, b, None)), True)
probe("admit-build-invalid-record", raises(lambda: cm.admit_build(reference, reg_adapter, {**b, "closureIds": ["closure2:" + "1" * 64]}, "development")), True)

# ---- 7. verify_successor negatives on temporary copies under the review dir
tmp = REVIEW / "tmp-successor-probe"
if tmp.exists():
    shutil.rmtree(tmp)
folder = tmp / "docs/implementation/m1/metadata-v2"
shutil.copytree(SUBJECT, folder)


def succ_fails(arch, prepare=None, name="copy"):
    if prepare:
        prepare()
    mod = import_checker(folder, name)
    try:
        mod.verify_successor(arch)
        return False
    except (AssertionError, KeyError, FileNotFoundError, IndexError):
        return True


probe("successor-copy-baseline-passes", succ_fails(ARCH, name="c0"), False)
(folder / "extra.txt").write_text("x")
probe("successor-unlisted-member-refused", succ_fails(ARCH, name="c1"), True)
(folder / "extra.txt").unlink()
readme = folder / "README.md"
orig = readme.read_bytes()
readme.write_bytes(orig + b"\n")
probe("successor-tampered-member-refused", succ_fails(ARCH, name="c2"), True)
readme.write_bytes(orig)

# Fake architecture: copy parents only, then tamper a passage (whitespace-preserving length change avoided -> hash catches)
record = json.loads((folder / "successor.json").read_bytes())
fake = tmp / "arch"
for pin in record["parents"]:
    dst = fake / pin["path"]
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ARCH / pin["path"], dst)
probe("successor-fake-arch-baseline-passes", succ_fails(fake, name="c3"), False)
plan = fake / "docs/v2/architecture/implementation-boundaries-and-build-plan.md"
plan_orig = plan.read_bytes()
plan.write_bytes(plan_orig.replace(b"signed release descriptor", b"signed release descriptoR", 1))
probe("successor-tampered-parent-refused", succ_fails(fake, name="c4"), True)
plan.write_bytes(plan_orig)

# Override-record tamper (after text) with matching member hash is not possible without editing successor.json itself;
# successor.json is excluded from its own pins, so test semantic override checks directly.
succ = folder / "successor.json"
succ_orig = succ.read_bytes()
rec = json.loads(succ_orig)
rec["passageOverrides"][0]["after"] = rec["passageOverrides"][0]["after"].replace("enclosing signed", "enclosing unsigned")
succ.write_text(json.dumps(rec))
probe("successor-override-after-tamper-refused", succ_fails(ARCH, name="c5"), True)
rec = json.loads(succ_orig)
rec["passageOverrides"][2]["selector"]["jsonPointer"] = "/files/8/description"
succ.write_text(json.dumps(rec))
probe("successor-override-wrong-pointer-refused", succ_fails(ARCH, name="c6"), True)
rec = json.loads(succ_orig)
rec["passageOverrides"] = rec["passageOverrides"][:3]
succ.write_text(json.dumps(rec))
probe("successor-override-dropped-refused", succ_fails(ARCH, name="c7"), True)
rec = json.loads(succ_orig)
rec["candidates"] = rec["candidates"][:-1]
succ.write_text(json.dumps(rec))
probe("successor-candidate-dropped-refused", succ_fails(ARCH, name="c8"), True)
succ.write_bytes(succ_orig)
shutil.rmtree(tmp)
probe("temporary-copies-removed", tmp.exists(), False)

out = {"summary": {"total": len(results), "failed": [r["id"] for r in results if not r["pass"]]}, "results": results}
(REVIEW / "probe-results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out["summary"], indent=1))
