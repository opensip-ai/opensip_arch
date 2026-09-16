"""Independent reviewer probes for the RF-01 metadata candidate. Read-only against subject/architecture."""
import copy
import hashlib
import json
import sys
from pathlib import Path

SUBJECT = Path("/tmp/opensip-implementation/m1-metadata-subject-01/docs/implementation/m1/metadata-v1")
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
sys.path.insert(0, str(SUBJECT))
import check_metadata as cm  # noqa: E402  (module import only; main() not run)

reference, registry, documents = cm.load(ARCH)
E4 = documents["urn:opensip:product-v1:workflows:evaluator3:command-envelope:4"]
E3 = documents["urn:opensip:product-v1:workflows:evaluator3:command-envelope:3"]
MID = "urn:opensip:product-v1:workflows:metadata:1"
fixture = json.loads((SUBJECT / "fixtures.json").read_bytes())
cases = {c["id"]: c["value"] for c in fixture["cases"]}
catalogue, build = fixture["catalogue"], fixture["build"]

results = []


def schema_ok(schema, value):
    try:
        reference.typed(value)
    except reference.AdmissionError:
        return False
    return reference.ExactValidator(schema, registry=registry).is_valid(value)


def admitted(value, cat=catalogue, bld=build):
    try:
        cm.admit(reference, registry, E4, value, cat, bld)
        return True
    except Exception as exc:  # noqa: BLE001
        from jsonschema import ValidationError
        if not isinstance(exc, (ValidationError, AssertionError, reference.AdmissionError, KeyError)):
            raise
        return False


def probe(pid, got, expected, note=""):
    results.append({"id": pid, "expected": expected, "observed": got, "pass": got == expected, "note": note})


def with_(base, **kw):
    v = copy.deepcopy(base)
    for k, val in kw.items():
        if val is DEL:
            v.pop(k, None)
        else:
            v[k] = val
    return v


DEL = object()
ver = cases["development-version"]
hlp = cases["help-top-level"]
pr = cases["parser-refusal-no-invented-detail"]
fmt = cases["completion-format-refusal"]

# --- meta exclusivity / termination / exit exactness
probe("meta-kind-run-with-meta", schema_ok(E4, with_(ver, kind="run")), False)
probe("meta-on-failure-kind", schema_ok(E4, with_(fmt, meta=ver["meta"])), False)
probe("meta-termination-request-rejected", schema_ok(E4, with_(ver, termination={"class": "request-rejected", "errorCode": "REQUEST.UNKNOWN_OPTION"}, exitCode=2)), False)
probe("meta-exit-bool-false", schema_ok(E4, with_(ver, exitCode=False)), False)
probe("meta-schemaMajor-float-parse", (lambda: (reference.parse(json.dumps(with_(ver, schemaMajor=4)).replace('"schemaMajor": 4', '"schemaMajor": 4.0').encode()), True))() if False else None, None, "see lexical probes")
probe("meta-errors-empty", schema_ok(E4, with_(ver, errors=[])), False)
probe("meta-invocation-field", schema_ok(E4, with_(ver, invocation={})), False)
probe("meta-querySurface-field", schema_ok(E4, with_(ver, querySurface="review-brief")), False)
probe("meta-schemaFamily-wrong", schema_ok(E4, with_(ver, schemaFamily="opensip.product.meta")), False)
probe("meta-correlation-129", schema_ok(E4, with_(ver, clientCorrelationId="x" * 129)), False)
probe("meta-requestId-upper", schema_ok(E4, with_(ver, requestId="req1_" + "A" * 32)), False)
probe("envelope3-rejects-kind-meta-with-major3", schema_ok(E3, with_(ver, schemaMajor=3)), False)
probe("envelope4-rejects-major4-meta-nonsense-command", schema_ok(E4, with_(ver, meta={**ver["meta"], "command": "doctor"})), False)
probe("meta-both-variants-mixed", schema_ok(E4, with_(ver, meta={**ver["meta"], "topic": None, "commands": catalogue})), False)

# --- parser-refusal narrow rule
probe("pr-accepted-baseline", schema_ok(E4, pr), True)
probe("pr-with-domainDetail", schema_ok(E4, with_(pr, termination={**pr["termination"], "domainDetail": {"code": "OUTPUT.FORMAT_NOT_APPLICABLE", "remedy": "x"}})), False)
probe("pr-with-runId", schema_ok(E4, with_(pr, termination={**pr["termination"], "runId": "run3:" + "b" * 64})), False)
probe("pr-with-projectId", schema_ok(E4, with_(pr, projectId="prj1-" + "b" * 64)), True, "base failure branch permits projectId; parser refusal pre-admission would not know a project; not constrained")
probe("pr-with-agentHints", schema_ok(E4, with_(pr, agentHints=[])), True, "not constrained by narrow rule")
probe("pr-schema-major-unsupported-empty", schema_ok(E4, with_(pr, termination={"class": "request-rejected", "errorCode": "REQUEST.SCHEMA_MAJOR_UNSUPPORTED"})), False)
probe("pr-precondition-empty", schema_ok(E4, with_(pr, termination={"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED"})), False)
probe("pr-kind-query-empty-errors", schema_ok(E4, with_(pr, kind="query")), False)
probe("pr-empty-string-diagnostic", schema_ok(E4, with_(pr, diagnostics=[""])), True, "nonempty list but empty text admitted")
probe("pr-diagnostic-1025", schema_ok(E4, with_(pr, diagnostics=["x" * 1025])), False)
probe("pr-diagnostic-257-items", schema_ok(E4, with_(pr, diagnostics=["x"] * 257)), False)
probe("pr-diagnostic-control-escape", schema_ok(E4, with_(pr, diagnostics=["" + chr(27) + "[31mUnknown --" + chr(0) + "x"])), True, "BoundedText has no control-character restriction (inherited)")
probe("pr-exit-derivation-3", admitted(with_(pr, exitCode=3)), False)
probe("pr-unknown-option-with-registered-detail-still-valid", schema_ok(E4, with_(pr, errors=[{"code": "OUTPUT.FORMAT_NOT_APPLICABLE", "remedy": "x"}], diagnostics=DEL)), True, "nonempty-detail form preserved")
probe("fmt-refusal-major3-still-valid", schema_ok(E3, with_(fmt, schemaMajor=3)), True)
probe("pr-major3-rejected", schema_ok(E3, with_(pr, schemaMajor=3)), False, "old reader cannot receive the parser refusal")

# --- metadata payload: version
bs = {"$ref": MID + "#/$defs/BuildMetadataV1"}
vs = {"$ref": MID + "#/$defs/VersionMetadataV1"}
hs = {"$ref": MID + "#/$defs/HelpMetadataV1"}
cid = lambda n: "closure2:" + format(n, "064x")  # noqa: E731
rel = {"command": "version", "hostRelease": "1.0.0", "buildChannel": "release", "closureIds": [cid(i) for i in range(256)]}
probe("rel-256-closures", schema_ok(vs, rel), True)
probe("rel-257-closures", schema_ok(vs, {**rel, "closureIds": [cid(i) for i in range(257)]}), False)
probe("rel-empty-closures-schema", schema_ok(vs, {**rel, "closureIds": []}), True, "schema admits release with no closures; only semantic build comparison refuses")
probe("rel-uppercase-closure", schema_ok(vs, {**rel, "closureIds": ["closure2:" + "A" * 64]}), False)
probe("rel-closure1-prefix", schema_ok(vs, {**rel, "closureIds": ["closure1:" + "a" * 64]}), False)
probe("rel-closure-trailing-newline", schema_ok(vs, {**rel, "closureIds": ["closure2:" + "a" * 64 + "\n"]}), False)
probe("dev-closure-null", schema_ok(vs, {**ver["meta"], "closureIds": None}), False)
probe("version-channel-case", schema_ok(vs, {**ver["meta"], "buildChannel": "Development"}), False)
probe("version-channel-missing", schema_ok(vs, {k: v for k, v in ver["meta"].items() if k != "buildChannel"}), False)
probe("semver-128", schema_ok(vs, {**ver["meta"], "hostRelease": "1.0.0-" + "a" * 122}), True)
probe("semver-129", schema_ok(vs, {**ver["meta"], "hostRelease": "1.0.0-" + "a" * 123}), False)
probe("semver-leading-zero-minor", schema_ok(vs, {**ver["meta"], "hostRelease": "1.02.3"}), False)
probe("semver-empty-prerelease-ident", schema_ok(vs, {**ver["meta"], "hostRelease": "1.2.3-a..b"}), False)
probe("semver-build-leading-zero-ok", schema_ok(vs, {**ver["meta"], "hostRelease": "1.2.3+001"}), True)
probe("semver-unicode-digit", schema_ok(vs, {**ver["meta"], "hostRelease": "1.2.٣"}), False, "Python re [0-9] is ASCII; ok")
probe("semver-space", schema_ok(vs, {**ver["meta"], "hostRelease": " 1.2.3"}), False)
probe("build-schemaVersion-2", schema_ok(bs, {**build, "schemaVersion": 2}), False)
probe("build-command-field", schema_ok(bs, {**build, "command": "version"}), False)
probe("build-assetPin-digest-smuggle", schema_ok(bs, {**build, "hostDigest": "a" * 64}), False)
probe("meta-payload-has-no-schemaVersion", schema_ok(vs, {**ver["meta"], "schemaVersion": 1}), False)

# --- help payload
probe("help-topic-alias-noncanonical", schema_ok(hs, {"command": "help", "topic": "--help", "commands": catalogue}), False)
probe("help-empty-commands", schema_ok(hs, {"command": "help", "topic": None, "commands": []}), False)
probe("help-usage-empty", schema_ok(hs, {"command": "help", "topic": None, "commands": [{**catalogue[0], "usage": ""}]}), False)
probe("help-usage-257", schema_ok(hs, {"command": "help", "topic": None, "commands": [{**catalogue[0], "usage": "u" * 257}]}), False)
probe("help-summary-2048-astral", schema_ok(hs, {"command": "help", "topic": None, "commands": [{**catalogue[0], "summary": "\U0001F600" * 2048}]}), True, "length counted in scalars, not UTF-16 units or bytes")
probe("help-summary-2049-astral", schema_ok(hs, {"command": "help", "topic": None, "commands": [{**catalogue[0], "summary": "\U0001F600" * 2049}]}), False)
probe("help-lone-surrogate", schema_ok(hs, {"command": "help", "topic": None, "commands": [{**catalogue[0], "summary": "\ud800"}]}), False)
probe("help-topic-omitted", schema_ok(hs, {"command": "help", "commands": catalogue}), False)
probe("help-row-extra-field", schema_ok(hs, {"command": "help", "topic": None, "commands": [{**catalogue[0], "aliases": []}]}), False)
probe("help-name-not-in-enum", schema_ok(hs, {"command": "help", "topic": None, "commands": [{**catalogue[0], "name": "Help"}]}), False)
probe("help-topic-no-row-in-catalogue-semantic", admitted(with_(hlp, meta={"command": "help", "topic": "analyze", "commands": [{"name": "analyze", "usage": "opensip analyze", "summary": "x"}]})), False)
probe("help-null-topic-single-row-semantic", admitted(with_(hlp, meta={"command": "help", "topic": None, "commands": [catalogue[1]]})), False)
probe("help-topic-correct-but-topic-help", admitted(with_(hlp, meta={"command": "help", "topic": "help", "commands": [catalogue[1]]})), True)
probe("help-summary-controls-schema", schema_ok(hs, {"command": "help", "topic": None, "commands": [{**catalogue[0], "summary": "a" + chr(27) + "[2Jb\nc"}]}), True, "no control-char law; trusted catalogue only")

# --- version semantic admission
probe("version-release-build-accepts-release", admitted(with_(ver, meta={"command": "version", "hostRelease": "1.0.0", "buildChannel": "release", "closureIds": [cid(1)]}), bld={"schemaVersion": 1, "hostRelease": "1.0.0", "buildChannel": "release", "closureIds": [cid(1)]}), True, "reference admits release when trusted build selection says release")
probe("version-closure-order-semantic", admitted(with_(ver, meta={"command": "version", "hostRelease": "1.0.0", "buildChannel": "release", "closureIds": [cid(2), cid(1)]}), bld={"schemaVersion": 1, "hostRelease": "1.0.0", "buildChannel": "release", "closureIds": [cid(1), cid(2)]}), False)

# --- inventory: selectors & name enum
inv = json.loads((SUBJECT / "command-inventory.v4.json").read_bytes())
inv_names = [c["name"] for c in inv["commands"]]
meta_names = documents[MID]["$defs"]["CommandName"]["enum"]
probe("command-name-enum-equals-inventory", sorted(meta_names) == sorted(inv_names) and len(inv_names) == 45 and len(set(inv_names)) == 45, True)
isch = documents["urn:opensip:product-v1:workflows:evaluator3:command-inventory:4"]
bad = copy.deepcopy(inv)
h = next(c for c in bad["commands"] if c["name"] == "help")
h["metaDispatch"]["paritySelectors"]["command-names"] = "$.meta.commands[0].name"
probe("inventory-altered-help-selector", schema_ok(isch, bad), False)
bad = copy.deepcopy(inv)
next(c for c in bad["commands"] if c["name"] == "completion")["metaDispatch"] = next(c for c in inv["commands"] if c["name"] == "help")["metaDispatch"]
probe("inventory-metaDispatch-on-completion", schema_ok(isch, bad), False)
bad = copy.deepcopy(inv)
next(c for c in bad["commands"] if c["name"] == "version").pop("metaDispatch")
probe("inventory-version-missing-metaDispatch", schema_ok(isch, bad), False)
bad = copy.deepcopy(inv)
v = next(c for c in bad["commands"] if c["name"] == "version")
v["parityFields"].remove("build-channel")
probe("inventory-version-parityField-dropped-schema", schema_ok(isch, bad), True, "schema does not bind parityFields to selector keys; only checker equality does")
bad = copy.deepcopy(inv)
next(c for c in bad["commands"] if c["name"] == "help")["metaDispatch"] = next(c for c in inv["commands"] if c["name"] == "version")["metaDispatch"]
probe("inventory-swapped-metaDispatch", schema_ok(isch, bad), False)
probe("inventory-schemaMajor-3", schema_ok(isch, {**inv, "schemaMajor": 3}), False)
renderer_json = inv["renderers"][1]
probe("json-renderer-version-4", renderer_json.get("version"), 4)
for c in inv["commands"]:
    if c["name"] in ("help", "version"):
        # each selector must resolve in the fixture envelope to a present value
        val = cases["help-top-level"] if c["name"] == "help" else cases["development-version"]
        for field, sel in c["metaDispatch"]["paritySelectors"].items():
            path = sel[2:].replace("[*]", "").split(".")
            cur = val
            ok = True
            for i, part in enumerate(path):
                if isinstance(cur, list):
                    cur = [x[part] for x in cur]
                elif isinstance(cur, dict) and part in cur:
                    cur = cur[part]
                else:
                    ok = False
                    break
            probe("selector-resolves-" + c["name"] + "-" + field, ok, True)

# --- coverage routing text
cov = json.loads((SUBJECT / "implementation-coverage.v2.json").read_bytes())
raw_cov = (SUBJECT / "implementation-coverage.v2.json").read_text()
probe("coverage-mentions-envelope-major-3", "CommandEnvelope-major-3" in raw_cov, False, "successor routing should not direct help/version to envelope major3")
probe("coverage-mentions-release-descriptor", "build-embedded release descriptor" in raw_cov, False, "phrase the README says is corrected")
probe("coverage-mentions-metadata-schema", "metadata:1" in raw_cov or "metadata.schema" in raw_cov or "BuildMetadataV1" in raw_cov, True)
probe("coverage-mentions-UNKNOWN_OPTION-empty-errors", "UNKNOWN_OPTION" in raw_cov, True)

# --- successor binding completeness
succ = json.loads((SUBJECT / "successor.json").read_bytes())
bound = {c["path"] for c in succ["candidates"]}
for name in ("README.md", "fixtures.json", "check_metadata.py", "sources.json"):
    probe("successor-binds-" + name, "docs/implementation/m1/metadata-v1/" + name in bound, True)
probe("successor-parents-include-canonical-or-registry", any("public-detail-registry" in p["path"] or "report-asset-binding" in p["path"] or "implementation-boundaries" in p["path"] for p in succ["parents"]), True, "parents whose text is corrected/relied on")

# --- lexical probes on an envelope byte form
lex = {
    "float-exit": b'{"exitCode":0.0}', "exp-exit": b'{"exitCode":0e0}', "neg-zero": b'{"exitCode":-0}',
    "dup-kind": b'{"kind":"meta","kind":"failure"}', "lone-surrogate": b'{"d":"\\udfff"}', "nan": b'{"x":NaN}',
    "bom": b'\xef\xbb\xbf{}', "int-2^64": b'{"x":18446744073709551616}', "overlong-utf8": b'{"x":"\xc0\xaf"}',
}
for k, raw in lex.items():
    try:
        reference.parse(raw)
        got = True
    except reference.AdmissionError:
        got = False
    probe("lexical-" + k, got, False)

# --- mutation probes against schema files (in-memory only)
def mutated_registry(mutate_id, fn):
    from referencing import Registry, Resource
    docs = copy.deepcopy(documents)
    fn(docs[mutate_id])
    return docs, Registry().with_resources((k, Resource.from_contents(v)) for k, v in docs.items())

def m_drop_meta_exclusion(s):
    s["allOf"][-2]["then"]["not"]["anyOf"] = [r for r in s["allOf"][-2]["then"]["not"]["anyOf"] if r["required"] != ["diagnostics"]]
docs2, reg2 = mutated_registry("urn:opensip:product-v1:workflows:evaluator3:command-envelope:4", m_drop_meta_exclusion)
try:
    cm.compatibility(ARCH, docs2["urn:opensip:product-v1:workflows:evaluator3:command-envelope:4"])
    killed = False
except AssertionError:
    killed = True
probe("mutation-drop-diagnostics-exclusion-killed-by-checker", killed, True)

def m_widen_empty_errors(s):
    s["allOf"][-1]["then"]["properties"]["termination"] = {"properties": {"class": {"const": "request-rejected"}}}
docs3, reg3 = mutated_registry("urn:opensip:product-v1:workflows:evaluator3:command-envelope:4", m_widen_empty_errors)
e_mut = docs3["urn:opensip:product-v1:workflows:evaluator3:command-envelope:4"]
killed_by_fixtures = any(
    reference.ExactValidator(e_mut, registry=reg3).is_valid(c["value"]) != c["accepted"] and c["value"].get("errors") == []
    for c in fixture["cases"] if not c["value"].get("kind") == "meta"
)
probe("mutation-widen-empty-errors-killed-by-fixtures", killed_by_fixtures, True)
try:
    cm.compatibility(ARCH, e_mut)
    ck = False
except AssertionError:
    ck = True
probe("mutation-widen-empty-errors-killed-by-compatibility", ck, False, "compatibility deliberately strips last two allOf entries")

def m_drop_dev_rule(s):
    s["$defs"]["VersionMetadataV1"]["allOf"] = []
docs4, reg4 = mutated_registry(MID, m_drop_dev_rule)
probe("mutation-drop-dev-empty-closures-schema-rule-detected-at-schema", reference.ExactValidator({"$ref": MID + "#/$defs/VersionMetadataV1"}, registry=reg4).is_valid(cases["invented-development-closure"]["meta"]), True, "mutant admits; fixture still refuses via semantic build comparison, so the schema rule is masked for envelope cases")
killed_env = not reference.ExactValidator(docs4["urn:opensip:product-v1:workflows:evaluator3:command-envelope:4"], registry=reg4).is_valid(cases["invented-development-closure"])
probe("mutation-drop-dev-rule-killed-by-envelope-schema", killed_env, False, "envelope-level schema check no longer refuses; checker still refuses via semantic admit()")

def m_drop_order(s):
    del s["$defs"]["HelpMetadataV1"]["properties"]["commands"]["x-opensip-order"]
docs5, reg5 = mutated_registry(MID, m_drop_order)
probe("mutation-drop-help-order-schema-level", reference.ExactValidator(docs5["urn:opensip:product-v1:workflows:evaluator3:command-envelope:4"], registry=reg5).is_valid(cases["unsorted-help"]), True, "fixture 'unsorted-help' would still be refused only by semantic catalogue equality, masking the schema order law")

summary = {"total": len(results), "failed": [r for r in results if not r["pass"]]}
out = {"summary": {"total": summary["total"], "failedCount": len(summary["failed"])}, "results": results}
Path("/tmp/opensip-implementation/m1-metadata-review-01/probe-results.json").write_text(json.dumps(out, indent=1))
print(json.dumps({"total": summary["total"], "failed": [(r["id"], r["observed"], r["expected"]) for r in summary["failed"]]}, indent=1))
