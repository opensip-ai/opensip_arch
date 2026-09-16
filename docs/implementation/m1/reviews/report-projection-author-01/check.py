"""Reference check of the report-projection author candidate; no product qualification.

Run: /tmp/opensip-implementation/metadata-reference-env/bin/python -I -B check.py --architecture ARCH
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import re
import sys
import time
from pathlib import Path

from referencing import Resource
from referencing.jsonschema import DRAFT202012
from jsonschema import Draft202012Validator, ValidationError

HERE = Path(__file__).resolve().parent
RID = "urn:opensip:product-v1:workflows:evaluator3:report-projection:1"
ENV = "urn:opensip:product-v1:workflows:evaluator3:command-envelope:4"
C = "urn:opensip:product-v1:workflows:evaluator3:common:3#/$defs/"
G = "urn:opensip:product-v1:workflows:evaluator3:graph-query:3#/$defs/"
EXIT = {"success": 0, "policy-failed": 1, "request-rejected": 2, "indeterminate": 3, "operational-failed": 4, "interrupted": 130}
ANALYSIS = {"default", "analyze", "fit", "audit"}


class Refused(Exception):
    def __init__(self, code, text=""):
        super().__init__(code + (": " + text if text else ""))
        self.code = code


def need(condition, code, text=""):
    if not condition:
        raise Refused(code, text)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def typed_report(reference, value, max_depth, depth=0):
    """Report-profile exact-codec value check: canonical.typed with a larger depth parameter."""
    if type(value) in (dict, list) and depth >= max_depth:
        raise Refused("CODEC-DEPTH")
    if type(value) is dict:
        for key, child in value.items():
            need(type(key) is str, "CODEC-TYPE")
            typed_report(reference, child, max_depth, depth + 1)
    elif type(value) is list:
        for child in value:
            typed_report(reference, child, max_depth, depth + 1)
    else:
        reference.typed(value)


def pointer_get(doc, pointer):
    value = doc
    for token in [t.replace("~1", "/").replace("~0", "~") for t in pointer.strip("/").split("/")] if pointer else []:
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def apply_ops(doc, ops, fixture, schema):
    doc = copy.deepcopy(doc)
    for op in ops:
        kind = op["op"]
        if kind in ("set", "remove"):
            *parent, last = op["path"].strip("/").split("/")
            target = pointer_get(doc, "/" + "/".join(parent)) if parent else doc
            key = int(last) if isinstance(target, list) else last
            if kind == "set":
                target[key] = copy.deepcopy(op["value"])
            else:
                del target[key]
        elif kind == "x-append-copy":
            array = pointer_get(doc, op["path"])
            array.append(copy.deepcopy(array[0]))
        elif kind == "x-inflate-findings":
            base = doc["envelope"]["findings"][0]
            rows = []
            for i in range(op["count"]):
                row = copy.deepcopy(base)
                row["findingId"] = "finding3:" + sha(b"finding-%d" % i)
                rows.append(row)
            doc["envelope"]["findings"] = sorted(rows, key=lambda r: r["findingId"].encode())
        elif kind == "x-inflate-evidence":
            base = doc["panels"]["evidence"]["data"]["entries"][0]
            rows = []
            for i in range(op["count"]):
                row = copy.deepcopy(base)
                row["key"]["subjectScopeCommitment"] = "sha256:" + sha(b"scope-%d" % i)
                rows.append(row)
            doc["panels"]["evidence"]["data"]["entries"] = rows
            doc["panels"]["evidence"]["data"]["entriesProjection"] = {"total": op["count"], "omitted": 0, "omissionCause": "none"}
        elif kind == "x-graph-slots":
            slots = doc["panels"]["graph"]["data"]["slots"]
            while len(slots) < op["count"]:
                extra = copy.deepcopy(slots[0])
                extra["ordinal"] = len(slots)
                slots.append(extra)
        elif kind == "x-deep-rule-predicate":
            rule = doc["panels"]["catalog"]["data"]["rules"]["data"]["rules"][0]
            atom = rule["emitWhen"]
            for _ in range(op["notChain"]):
                atom = {"op": "not", "operand": atom}
            rule["emitWhen"] = atom
        else:
            raise AssertionError("unknown fixture op " + kind)
    return doc


def subject_run(env, command):
    """Concrete run3 anchor for exploration joins, or None. Never resolves latest or snapshot views."""
    if env["kind"] == "run":
        return env["run"]["runId"] if env["run"]["authority"] == "authoritative" else None
    if env["kind"] != "query":
        return None
    record = env["queryRecord"]
    if command == "candidates":
        return record["context"]["resolvedView"].get("runId")
    if command == "inspect":
        return record["inspection"]["runId"]
    if command == "review-brief":
        return record["brief"]["runId"]
    return None


def admit(reference, registry, schema, inventory, doc):
    """Full reference admission; raises Refused with a stable code."""
    budget = schema["$defs"]["BudgetProfileV1"]["properties"]
    typed_report(reference, doc, budget["maxJsonDepth"]["const"])
    need(len(canonical(doc)) <= budget["documentMaxCanonicalBytes"]["const"], "J-BUDGET-BYTES", "document")
    try:
        reference.ExactValidator(schema, registry=registry).validate(doc)
    except ValidationError as exc:
        raise Refused("SCHEMA", exc.message[:160])
    env, command, panels = doc["envelope"], doc["command"], doc["panels"]
    row = next(c for c in inventory["commands"] if c["name"] == command)
    html = next(r for r in inventory["renderers"] if r["format"] == "html")
    need("html" in row["formats"] and row["requestClass"] in html["applicability"], "J-RENDERER")
    need(doc["renderer"] == {"format": "html", "version": html["version"]}, "J-RENDERER")
    need(env["exitCode"] == EXIT[env["termination"]["class"]], "J-EXIT")
    if env["kind"] == "query":
        need(env["querySurface"] == row["queryDispatch"]["surface"], "J-SURFACE")
    anchor = subject_run(env, command)
    run = env.get("run", {})

    def present(value):
        return value.get("state") == "present"

    def states():
        for name, value in panels.items():
            yield name, value
            if name == "catalog" and present(value):
                for section, inner in value["data"].items():
                    yield name + "." + section, inner

    for name, value in states():
        if present(value):
            continue
        reason = value["reason"]
        if env["kind"] == "failure":
            need(reason == "no-admitted-result", "J-FAILURE-PANELS", name)
            continue
        need(reason != "no-admitted-result", "J-STATE-REASON", name)
        if reason == "no-run-identity":
            need(anchor is None and name in ("graph", "history"), "J-STATE-REASON", name)
        if reason == "not-selected":
            need(name == "comparison" and "comparisonResultId" not in run, "J-NOT-SELECTED", name)
    if env["kind"] == "run" and "comparison" in panels and "comparisonResultId" not in run:
        need(panels["comparison"] == {"state": "omitted", "reason": "not-selected"}, "J-COMPARISON-ID", "no selected comparison")

    order = budget["budgetOmissionOrder"]["const"]
    for i, name in enumerate(order):
        value = panels.get(name)
        budget_omitted = value is not None and (value.get("reason") == "exploration-budget-exceeded" or
                                                 (name == "catalog" and present(value) and any(s.get("reason") == "exploration-budget-exceeded" for s in value["data"].values())))
        if budget_omitted:
            need(not any(present(panels[p]) for p in order[:i] if p in panels), "J-BUDGET-ORDER", name)

    graph = panels.get("graph")
    if graph and present(graph):
        need(anchor is not None, "J-ANCHOR", "graph requires a concrete run3 subject")
        for slot in graph["data"]["slots"]:
            request, response = slot["request"], slot["response"]
            ctx, params, items = response["context"], request["params"], response["items"]
            need(ctx["resolvedView"]["runId"] == anchor and request["view"]["runId"] == anchor, "J-GRAPH-RUN")
            need(request["projectId"] == ctx["projectId"] == env["projectId"], "J-GRAPH-PROJECT")
            need(request["operation"] == response["operation"], "J-GRAPH-OPERATION")
            need(len(items) <= request["page"]["size"], "J-GRAPH-PAGE")
            need(("nextCursor" in ctx) == (slot["hostProjection"]["continuation"] == "not-embedded"), "J-GRAPH-CONTINUATION")
            if "factViewDigests" in params:
                need(params["factViewDigests"] == ctx["factViewDigests"], "J-GRAPH-VIEWS")
            op = response["operation"]
            if op == "graph.neighbors":
                for item in items:
                    need(item["relation"] == params["relation"], "J-GRAPH-RELATION")
                    touches = {"outgoing": [item["source"]], "incoming": [item["target"]], "both": [item["source"], item["target"]]}[params["direction"]]
                    need(any(reference.equal_typed(e, params["endpoint"]) for e in touches), "J-GRAPH-ENDPOINT")
                    if slot["purpose"] == "package-coupling":
                        need(item["source"]["kind"] == item["target"]["kind"] == "package", "J-GRAPH-COUPLING")
            elif op == "graph.path":
                for item in items:
                    need(reference.equal_typed(item["start"], params["start"]) and reference.equal_typed(item["target"], params["target"]), "J-GRAPH-ENDPOINT")
                    need(item["hopCount"] <= params["maxDepth"], "J-GRAPH-ENDPOINT")
            else:
                for item in items:
                    need(item["depth"] <= params["maxDepth"], "J-GRAPH-ENDPOINT")
                    if item["depth"] == 0:
                        need(params.get("includeStart") is True and reference.equal_typed(item["endpoint"], params["start"]), "J-GRAPH-ENDPOINT")

    evidence = panels.get("evidence")
    if evidence and present(evidence):
        data = evidence["data"]
        need(env["kind"] == "run" and run.get("coverageId") == data["coverageId"], "J-EVIDENCE-COVERAGE")
        projection = data["entriesProjection"]
        need(projection["total"] == len(data["entries"]) + projection["omitted"], "J-EVIDENCE-COUNTS")
        need((projection["omissionCause"] == "item-limit") == (projection["omitted"] > 0), "J-EVIDENCE-COUNTS")
        if projection["omissionCause"] == "item-limit":
            need(len(data["entries"]) == budget["maxEvidenceEntries"]["const"], "J-EVIDENCE-COUNTS")
        keys = [canonical(e["key"]) for e in data["entries"]]
        need(len(keys) == len(set(keys)), "J-EVIDENCE-KEYS")

    comparison = panels.get("comparison")
    if comparison and present(comparison):
        result = comparison["data"]["comparison"]
        need(run.get("comparisonResultId") == result["comparisonResultId"], "J-COMPARISON-ID")
        need(result["descriptor"]["currentRunId"] == run["runId"], "J-COMPARISON-RUN")

    history = panels.get("history")
    if history and present(history):
        need(anchor is not None, "J-ANCHOR", "history requires an authoritative current Run")
        data = history["data"]
        selection = data["selection"]
        if comparison and present(comparison):
            need(selection["baselineId"] == comparison["data"]["comparison"]["descriptor"]["baselineId"], "J-HISTORY-BASELINE")
        need([r["runId"] for r in data["runs"]] == selection["requestedRunIds"], "J-HISTORY-SELECTION")
        need(anchor not in selection["requestedRunIds"], "J-HISTORY-CURRENT")
        for entry in data["runs"]:
            if present(entry):
                need(entry["run"]["runId"] == entry["runId"], "J-HISTORY-RUN")
                projection = entry["findingsProjection"]
                need(projection["total"] == len(entry["findings"]) + projection["omitted"], "J-HISTORY-COUNTS")
                need((projection["omissionCause"] == "item-limit") == (projection["omitted"] > 0), "J-HISTORY-COUNTS")

    catalog = panels.get("catalog")
    if catalog and present(catalog):
        rules = catalog["data"]["rules"]
        if present(rules):
            need(env["kind"] == "run" and rules["data"]["source"]["planId"] == run["planId"], "J-CATALOG-PLAN")
            listed = {r["ruleId"] for r in rules["data"]["rules"]}
            need({f["ruleId"] for f in env.get("findings", [])} <= listed, "J-CATALOG-RULES")
        capabilities = catalog["data"]["capabilities"]
        if present(capabilities):
            need(capabilities["data"]["source"]["registrySha256"] == sha(canonical(capabilities["data"]["declarations"])), "J-CATALOG-DIGEST")

    need(len(canonical(env)) <= budget["envelopeMaxCanonicalBytes"]["const"], "J-BUDGET-BYTES", "envelope")
    need(len(canonical(panels)) <= budget["explorationMaxCanonicalBytes"]["const"], "J-BUDGET-BYTES", "exploration")
    return True


def resolve_schema_pointer(schema, pointer):
    try:
        pointer_get(schema, pointer)
        return True
    except (KeyError, IndexError, ValueError):
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--architecture", required=True, type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    arch = args.architecture
    report = {"standing": "AUTHOR CANDIDATE reference check; not approval, not measured performance, not product or release qualification"}

    # 1. Successor record: exact parent/candidate pins and passage-override before text.
    successor = json.loads((HERE / "successor.json").read_bytes())
    for pin in successor["parents"]:
        path = Path(pin["path"]) if pin["path"].startswith("/") else arch / pin["path"]
        raw = path.read_bytes()
        assert len(raw) == pin["bytes"] and sha(raw) == pin["sha256"], pin["path"]
    for pin in successor["candidates"]:
        raw = (HERE / pin["path"]).read_bytes()
        assert len(raw) == pin["bytes"] and sha(raw) == pin["sha256"], pin["path"]
    for override in successor["passageOverrides"]:
        lines = (arch / override["parent"]["path"]).read_text().splitlines()
        assert lines[override["selector"]["line"] - 1] == override["before"], override["selector"]
    report["pinsVerified"] = len(successor["parents"]) + len(successor["candidates"])

    # 2. Owner registry from the pinned metadata-v2 loader; candidate registered beside it, no retrieval.
    spec = importlib.util.spec_from_file_location("check_metadata", arch / "docs/implementation/m1/metadata-v2/check_metadata.py")
    check_metadata = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(check_metadata)
    reference, registry, documents = check_metadata.load(arch)
    schema_raw = (HERE / "report-projection.schema.json").read_bytes()
    schema = reference.parse(schema_raw)
    Draft202012Validator.check_schema(schema)
    assert schema["$id"] == RID and RID not in documents
    registry = registry.with_resource(RID, Resource(contents={k: v for k, v in schema.items() if k != "$schema"}, specification=DRAFT202012))
    report["projectionSchemaSha256"] = sha(schema_raw)
    for ref in re.findall(r'"\$ref":\s*"([^"#]+)', schema_raw.decode()):
        assert ref in documents, "unregistered external owner " + ref

    # 3. Renderer gating against inventory4 and the prototype inventory's exact HTML set.
    inventory = json.loads((arch / "docs/implementation/m1/metadata-v2/command-inventory.v4.json").read_bytes())
    html_commands = sorted(c["name"] for c in inventory["commands"] if "html" in c["formats"])
    assert html_commands == sorted(schema["$defs"]["ReportCommand"]["enum"]), html_commands
    inventory_text = (arch / "docs/v2/architecture/prototype-report-inventory.md").read_text()
    advertised = re.search(r"HTML is advertised by exactly (.*?)\. Graph", inventory_text, re.S).group(1)
    assert sorted(re.findall(r"`([a-z-]+)`", advertised)) == html_commands
    html = [r for r in inventory["renderers"] if r["format"] == "html"]
    assert len(html) == 1 and html[0]["version"] == schema["properties"]["renderer"]["properties"]["version"]["const"]
    per_command = {}
    for block in schema["allOf"]:
        cmd = block.get("if", {}).get("properties", {}).get("command", {}).get("const")
        if cmd:
            per_command[cmd] = block["then"]["properties"]
    assert set(per_command) == set(html_commands)
    for cmd in html_commands:
        row = next(c for c in inventory["commands"] if c["name"] == cmd)
        surface = per_command[cmd]["envelope"]["properties"].get("querySurface", {}).get("const")
        assert surface == row.get("queryDispatch", {}).get("surface"), cmd
        assert (cmd in ANALYSIS) == (row["requestClass"] == "analysis")
    fit = next(c for c in inventory["commands"] if c["name"] == "fit")
    assert "queryDispatch" not in fit and {"candidates", "evidence-levels"} <= set(fit["parityFields"])
    report["rendererGating"] = {"htmlCommands": html_commands, "htmlRendererVersion": html[0]["version"], "fitCandidateCarrierAbsentInEnvelope4": True}

    # 4. Envelope4 stays closed and unmodified; exploration members are absent from it.
    envelope = documents[ENV]
    assert envelope["additionalProperties"] is False
    assert not {"panels", "history", "catalog", "graph", "evidence", "comparison"} & set(envelope["properties"])
    report["envelope4Closed"] = True

    # 5. All 24 R rows mapped; every pointer resolves; every view used and sourced.
    fixture = json.loads((HERE / "fixtures.json").read_bytes())
    rows = re.findall(r"^### (R\d\d) — ", inventory_text, re.M)
    assert rows == ["R%02d" % i for i in range(1, 25)] and sorted(fixture["featureMap"]) == rows
    for rid, mapping in fixture["featureMap"].items():
        assert mapping["report"] or mapping["envelope"] or mapping["presentationalOnly"], rid
        for pointer in mapping["report"]:
            assert resolve_schema_pointer(schema, pointer), (rid, pointer)
        for pointer in mapping["envelope"]:
            assert resolve_schema_pointer(envelope, pointer), (rid, pointer)
    used = {v for props in per_command.values() for v in props["supportedReportViews"]["const"]}
    assert used == set(schema["$defs"]["ReportViewId"]["enum"]) == set(fixture["viewSources"])
    for view, sources in fixture["viewSources"].items():
        assert sources["report"] or sources["envelope"], view
        assert all(resolve_schema_pointer(schema, p) for p in sources["report"]), view
        assert all(resolve_schema_pointer(envelope, p) for p in sources["envelope"]), view

    # 6. Fixture regeneration is byte-identical.
    spec = importlib.util.spec_from_file_location("build_fixtures", HERE / "build_fixtures.py")
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    assert json.dumps(builder.build(), indent=1, ensure_ascii=False).encode("utf-8") + b"\n" == (HERE / "fixtures.json").read_bytes(), "fixtures drift"

    # 7. Budget derivation from labelled construction measurements (not performance measurement).
    budget = {k: v.get("const") for k, v in schema["$defs"]["BudgetProfileV1"]["properties"].items()}
    samples = fixture["measurementSamples"]
    reference.validate({"$ref": G + "GraphNeighborRow"}, samples["neighborRow"], registry)
    reference.validate({"$ref": C + "FindingSurface"}, samples["finding"], registry)
    reference.validate({"$ref": "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CoverageResultV3"}, samples["coverage"], registry)
    row_b, finding_b, coverage_b = (len(canonical(samples[k])) for k in ("neighborRow", "finding", "coverage"))
    codec_bytes, codec_depth = reference.MAX_BYTES, reference.MAX_DEPTH
    graph_bounds = documents["urn:opensip:product-v1:workflows:evaluator3:graph-query:3"]["$defs"]["Bounds"]["properties"]
    envelope_findings_max = envelope["properties"]["findings"]["maxItems"]
    mib16 = 16 * 1024 * 1024
    derived = {
        "explorationMaxCanonicalBytes": codec_bytes,
        "maxGraphItemsPerSlot": graph_bounds["maxPageSize"]["const"],
        "maxGraphSlots": codec_bytes // (graph_bounds["maxPageSize"]["const"] * row_b),
        "maxEvidenceEntries": codec_bytes // coverage_b,
        "maxHistoryFindingsPerRun": codec_bytes // finding_b,
        "envelopeMaxCanonicalBytes": -(-envelope_findings_max * finding_b // mib16) * mib16,
        "maxCatalogRules": documents["urn:opensip:product-v1:policy-document:2"]["$defs"]["PolicyDocumentV2"]["properties"]["rules"]["maxItems"],
        "maxCapabilityDeclarations": documents["urn:opensip:product-v1:native:evidence-schemas:v2"]["$defs"]["ReleaseCapabilityRegistryV1"]["maxItems"],
    }
    derived["documentMaxCanonicalBytes"] = derived["envelopeMaxCanonicalBytes"] + codec_bytes + 65536
    # Depth: (offset in report) - (offset in the document the record was admitted in) + accepted codec depth.
    embeddings = [
        ("envelope", ["envelope"], 0, ENV),
        ("graph request", ["panels", "graph", "data", "slots", 0, "request"], 0, G + "GraphQueryRequestV1"),
        ("graph response", ["panels", "graph", "data", "slots", 0, "response"], 0, G + "GraphQueryResponseV1"),
        ("coverage entry", ["panels", "evidence", "data", "entries", 0], 0, "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/CoverageResultV3"),
        ("comparison", ["panels", "comparison", "data", "comparison"], 0, "urn:opensip:product-v1:workflows:evaluator3:comparison:2"),
        ("history run (envelope.run)", ["panels", "history", "data", "runs", 0, "run"], 1, "urn:opensip:product-v1:workflows:evaluator3:invocation:3#/$defs/AnalysisResult"),
        ("policy rule (policy.rules[i])", ["panels", "catalog", "data", "rules", "data", "rules", 0], 2, "urn:opensip:product-v1:policy-document:2#/$defs/Rule"),
        ("capability registry", ["panels", "catalog", "data", "capabilities", "data", "declarations"], 0, "urn:opensip:product-v1:native:evidence-schemas:v2#/$defs/ReleaseCapabilityRegistryV1"),
    ]
    full = fixture["bases"]["audit-full"]
    gains = {}
    for name, path, native, ref in embeddings:
        value = full
        for token in path:
            value = value[token]
        reference.validate({"$ref": ref}, value, registry)
        gains[name] = len(path) - native
    # history findings sit at findings[j] (native envelope offset 2); checked structurally.
    gains["history finding (envelope.findings[j])"] = len(["panels", "history", "data", "runs", 0, "findings", 0]) - 2
    derived["maxJsonDepth"] = codec_depth + max(gains.values())
    for key, value in derived.items():
        assert budget[key] == value, (key, budget[key], value)
    report["budgetDerivation"] = {"label": "schema/reference construction measurement over constructed values; not browser performance",
                                  "acceptedExactCodec": {"maxBytes": codec_bytes, "maxDepth": codec_depth},
                                  "constructedBytes": {"GraphNeighborRow": row_b, "FindingSurface": finding_b, "CoverageResultV3": coverage_b},
                                  "findingsFittingAcceptedCodec": codec_bytes // finding_b, "envelope4FindingsMaxItems": envelope_findings_max,
                                  "embeddingDepthGains": gains, "derived": derived}

    # 8. Cases: exact expected result code, so a refusal for the wrong reason fails the check.
    results = []
    for case in fixture["cases"]:
        doc = apply_ops(fixture["bases"][case["base"]], case["ops"], fixture, schema)
        started = time.perf_counter()
        try:
            admit(reference, registry, schema, inventory, doc)
            outcome = "accept"
        except Refused as exc:
            outcome = exc.code
            detail = str(exc)
        assert outcome == case["expect"], (case["id"], outcome, case["expect"], None if outcome == "accept" else detail)
        results.append({"id": case["id"], "result": outcome, "canonicalBytes": len(canonical(doc)), "referenceSeconds": round(time.perf_counter() - started, 3)})
    report["cases"] = results

    # 9. Why the report profile is larger than the accepted 4 MiB / 32 codec (evidence, not a performance claim).
    large = apply_ops(fixture["bases"]["audit-full"], [{"op": "x-inflate-findings", "count": 8000}], fixture, schema)
    try:
        reference.canonical(large["envelope"])
        raise AssertionError("8000-finding envelope unexpectedly fits the accepted codec")
    except reference.AdmissionError as exc:
        assert "BYTE_LIMIT" in str(exc)
    deep = apply_ops(fixture["bases"]["audit-full"], [{"op": "x-deep-rule-predicate", "notChain": 27}], fixture, schema)
    rule = deep["panels"]["catalog"]["data"]["rules"]["data"]["rules"][0]
    policy = {"schemaFamily": "opensip.product.policy", "schemaMajor": 2, "gateSeverityAtLeast": "warning", "rules": [rule]}
    reference.validate({"$ref": "urn:opensip:product-v1:policy-document:2#/$defs/PolicyDocumentV2"}, policy, registry)
    try:
        reference.typed(deep)
        raise AssertionError("deep report unexpectedly within accepted depth 32")
    except reference.AdmissionError as exc:
        assert "DEPTH_LIMIT" in str(exc)
    report["largerProfileEvidence"] = {"envelope8000FindingsBytes":len(canonical(large["envelope"])), "acceptedCodecRefusesEnvelope": True,
                                       "policyDocumentAdmittedAtDepth32": True, "sameRuleInReportRefusedAtDepth32": True}

    # 10. No retrieval: unknown refs refuse offline.
    for target in ("https://example.invalid/report.json", "urn:opensip:product-v1:workflows:evaluator3:report-projection:2"):
        try:
            reference.validate({"$ref": target}, {}, registry)
            raise AssertionError("unregistered reference accepted")
        except AssertionError:
            raise
        except Exception:
            pass

    report["passed"] = True
    report["openObligations"] = [o["id"] for o in fixture["openObligations"]]
    report["productQualification"] = False
    text = json.dumps(report, indent=1)
    if args.out:
        args.out.write_text(text + "\n")
    print(json.dumps({k: report[k] for k in ("passed", "pinsVerified", "projectionSchemaSha256", "rendererGating", "largerProfileEvidence", "openObligations", "productQualification")}, indent=1))
    print("cases:", len(results), "accepted:", sum(r["result"] == "accept" for r in results))


if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    main()
