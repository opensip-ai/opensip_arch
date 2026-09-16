"""Bounded graph query admission, projection, traversal, cursor, and failure envelopes.

Public execute_graph_query always requires a retained Run and identity-model.v3
close_run. host.standing, host.cache, host.targetAttributions and
host.evaluationDeficiencies cannot replace that admission or its retained
records. Occupancy identity for projected targets uses the same
atom_model._reconcile_attribution / _ephemeral_target law as atom matching,
fed only from the admitted Run's selected evaluationInputRefs (inventories,
sidecars) plus the plan enumeration binding and named producer closures.
Caller-supplied census is not retained authority. Algorithm goldens over
already-projected edges use traverse_projected_graph, which is not a public
query and does not admit a Run.

Does not seal a Run, invoke a provider, change storage generations, or mint
negative proof. Public bound constants are schema Bounds; host.testBounds may
only lower visited/produced caps for reference controls.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
import sys
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "foundation"))
import canonical  # noqa: E402
from jsonschema import ValidationError  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402

PUBLIC_BOUNDS = {
    "maxPageSize": 1000,
    "defaultPageSize": 100,
    "maxItemsPerOperation": 100000,
    "maxTraversalDepth": 64,
    "maxVisitedNodes": 1000000,
}
GRAPH_OPS = frozenset({"graph.neighbors", "graph.path", "graph.reach"})
STORED_KINDS = frozenset({"file", "symbol", "package"})
DEFICIENCY_SOURCES = frozenset({"enumeration", "native", "import", "execution", "correspondence"})
CURSOR_RE = re.compile(r"^q3\.([0-9a-f]{64})\.([0-9a-f]{64})\.([0-9]+)$")
SCHEMA_ID = "urn:opensip:product-v1:workflows:evaluator3:graph-query:3"
COMMON_ID = "urn:opensip:product-v1:workflows:evaluator3:common:3"
ENVELOPE_ID = "urn:opensip:product-v1:workflows:evaluator3:command-envelope:3"
ENUM_PLAN_ROW = "foundation/enumeration-plan.schema.v1.json"
CLASS_EXIT = {
    "success": 0,
    "policy-failed": 1,
    "request-rejected": 2,
    "indeterminate": 3,
    "operational-failed": 4,
    "interrupted": 130,
}
_ID3 = None
_REG = None
_TABLE = None
_AM = None


class ReferenceCallPrecondition(Exception):
    """Reference-harness missing trusted host metadata. Not a public request refusal."""

    def __init__(self, missing, remedy="supply an already reserved host.requestId observation; RequestId is never hashed from the request"):
        super().__init__(missing)
        self.missing = missing
        self.remedy = remedy


class QueryRefusal(Exception):
    """Public graph-query refusal. envelope() is the admitted CommandEnvelope kind=failure.

    `diagnostic` retains the exact owner decision text privately. It never selects the route and is not an
    envelope field.
    """

    def __init__(
        self,
        error_code,
        detail=None,
        remedy="see query-projection-contract.v3.md",
        subject=None,
        *,
        klass="request-rejected",
        fault_cause=None,
        run_id=None,
        request=None,
        host=None,
        diagnostic=None,
    ):
        super().__init__(error_code)
        self.error_code = error_code
        self.detail = detail
        self.remedy = remedy
        self.subject = subject
        self.klass = klass
        self.fault_cause = fault_cause
        self.run_id = run_id
        self.request = request
        self.host = host
        self.diagnostic = diagnostic

    def termination(self):
        term = {"class": self.klass}
        if self.klass in ("request-rejected", "operational-failed"):
            term["errorCode"] = self.error_code
        if self.klass == "operational-failed":
            term["faultCause"] = self.fault_cause or "host-io"
        if self.klass == "indeterminate":
            term["reasonCodes"] = [self.error_code]
        if self.detail:
            body = {"code": self.detail, "remedy": str(self.remedy)[:1024]}
            if self.subject is not None:
                body["subject"] = str(self.subject)[:1024]
            term["domainDetail"] = body
        if self.run_id and self.klass in ("indeterminate", "operational-failed", "policy-failed"):
            term["runId"] = self.run_id
        return term

    def envelope(self, host=None):
        return failure_envelope(self, self.request, host if host is not None else self.host)


def identity3():
    global _ID3
    if _ID3 is None:
        spec = importlib.util.spec_from_file_location(
            "query_identity3", HERE.parent / "foundation" / "identity-model.v3.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _ID3 = mod
    return _ID3


def atom_model():
    """Share atom occupancy reconciliation. Do not parse SubjectIdV1 namespaces here.

    M2 identity-contradiction work should preserve _reconcile_attribution(fact, spec, inputs)
    and _ephemeral_target(fact, spec, inputs). Query does not overwrite atom_model.
    """
    global _AM
    if _AM is None:
        spec = importlib.util.spec_from_file_location(
            "query_atom_model_v1", HERE.parent / "foundation" / "atom_model.v1.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _AM = mod
    return _AM


def schema_registry():
    global _REG
    if _REG is None:
        schemas = {}
        e3 = HERE / "schemas" / "evaluator3"
        for path in sorted(e3.glob("*.schema.json")):
            doc = json.loads(path.read_text())
            schemas[doc["$id"]] = doc
        wf = HERE / "schemas"
        for name in (
            "common.schema.json",
            "imported-evidence.schema.json",
            "policy-document.schema.json",
            "policy-document.v2.schema.json",
            "test-execution.schema.json",
        ):
            path = wf / name
            if path.exists():
                doc = json.loads(path.read_text())
                schemas[doc["$id"]] = doc
        _REG = Registry().with_resources(
            [(k, Resource(contents=v, specification=DRAFT202012)) for k, v in schemas.items()]
        )
    return _REG


def validate_schema(ref, value):
    canonical.typed(value)
    canonical.ExactValidator({"$ref": ref}, registry=schema_registry()).validate(value)
    return value


def projection_table():
    """Binary native-id rungs from the existing evaluator projection registry. No invented edges."""
    global _TABLE
    if _TABLE is None:
        path = HERE.parent / "foundation" / "evaluator-projection-registry.v1.json"
        doc = json.loads(path.read_text())
        table = {}
        for name, spec in doc["relations"].items():
            et = spec.get("endpointTarget")
            if et == "forbidden" or not spec.get("targetNativeIdField"):
                continue
            source_kind = spec.get("sourceSubjectKind")
            if source_kind not in STORED_KINDS:
                continue
            target_kinds = tuple(k for k in (spec.get("targetKinds") or []) if k in STORED_KINDS)
            if not target_kinds:
                continue
            if et == "admitted":
                rungs = list(spec.get("ladder") or [])
            elif et == "admitted-at-rung":
                rungs = list(spec.get("endpointTargetRungs") or [])
            else:
                continue
            target_field = spec.get("targetField") or spec.get("targetNativeIdField")
            for rung in rungs:
                table[(name, rung)] = {
                    "relation": name,
                    "minResolution": rung,
                    "sourceField": spec["sourceField"],
                    "targetField": target_field,
                    "sourceKind": source_kind,
                    "targetKinds": target_kinds,
                    "universeRule": spec.get("universeRule"),
                }
        if not table:
            raise RuntimeError("projection table empty")
        _TABLE = table
    return _TABLE


def endpoint_tuple(ep):
    return (
        ep["universe"],
        ep["kind"],
        ep["nativeSubjectId"],
        ep.get("packageManifestPath") or "",
    )


def endpoint_key(ep):
    """Normative order key: utf-8 bytes of (universe, kind, nativeSubjectId, packageManifestPath or empty)."""
    return (
        ep["universe"].encode("utf-8"),
        ep["kind"].encode("utf-8"),
        ep["nativeSubjectId"].encode("utf-8"),
        (ep.get("packageManifestPath") or "").encode("utf-8"),
    )


def canonical_endpoint(ep):
    out = {
        "kind": ep["kind"],
        "nativeSubjectId": ep["nativeSubjectId"],
        "universe": ep["universe"],
    }
    if ep["kind"] == "package":
        path = ep.get("packageManifestPath")
        if not path:
            return None
        out["packageManifestPath"] = path
    return out


def endpoints_equal(a, b):
    return endpoint_tuple(a) == endpoint_tuple(b)


def reserved_request_id(host):
    """Preserve an already reserved host RequestId. Never hash request bytes; never mint entropy."""
    supplied = (host or {}).get("requestId")
    if type(supplied) is str and re.fullmatch(r"req1_[0-9a-f]{32}", supplied):
        return supplied
    raise ReferenceCallPrecondition(
        "host.requestId",
        "failure envelopes require an explicit already-reserved host.requestId (req1_ + 32 hex); RequestId is independent 16-byte host CSPRNG reserved before admission",
    )


def domain_detail(code, remedy, subject=None):
    body = {"code": code, "remedy": str(remedy)[:1024]}
    if subject is not None:
        body["subject"] = str(subject)[:1024]
    return body


def _admitted_project_id(value):
    return type(value) is str and re.fullmatch(r"prj1-[0-9a-f]{64}", value)


def failure_envelope(refusal, request=None, host=None):
    """Admitted CommandEnvelope kind=failure. Never carries a Run. errors is nonempty.

    RequestId is a trusted host observation already reserved before admission.
    Malformed projectId is omitted; it is not copied into the envelope.
    """
    term = refusal.termination()
    detail = term.get("domainDetail")
    if detail is None:
        if refusal.detail:
            detail = domain_detail(refusal.detail, refusal.remedy, refusal.subject)
        else:
            raise RuntimeError("failure envelope requires a registered DomainDetail")
    envelope = {
        "schemaFamily": "opensip.product.envelope",
        "schemaMajor": 3,
        "kind": "failure",
        "requestId": reserved_request_id(host),
        "termination": term,
        "exitCode": CLASS_EXIT[refusal.klass],
        "errors": [detail],
    }
    if type(request) is dict and _admitted_project_id(request.get("projectId")):
        envelope["projectId"] = request["projectId"]
    validate_schema(ENVELOPE_ID, envelope)
    validate_schema(COMMON_ID + "#/$defs/StepTermination", term)
    return envelope


def work_bounds(host):
    bounds = dict(PUBLIC_BOUNDS)
    injected = (host or {}).get("testBounds") or {}
    for key in ("maxVisitedNodes", "maxItemsPerOperation"):
        if key in injected:
            value = injected[key]
            if type(value) is not int or value < 1 or value > bounds[key]:
                raise QueryRefusal(
                    "REQUEST.PRECONDITION_FAILED",
                    "QUERY.PARAMS_MALFORMED",
                    "testBounds may only lower public visited/produced caps",
                    key,
                )
            bounds[key] = value
    return bounds


def selection_hash(project_id, run_id, fact_view_digests, operation, effective_params):
    record = {
        "factViewDigests": sorted(fact_view_digests),
        "operation": operation,
        "params": effective_params,
        "projectId": project_id,
        "runId": run_id,
    }
    return hashlib.sha256(canonical.canonical(record)).hexdigest()


def encode_cursor(run_id, digest, position):
    token = "q3.%s.%s.%d" % (run_id.split(":", 1)[1], digest, position)
    if len(token) > 256:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.CURSOR_MISMATCH",
            "cursor exceeds 256 characters",
        )
    return token


def decode_cursor(token):
    match = CURSOR_RE.fullmatch(token)
    if not match:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.CURSOR_MISMATCH",
            "cursor is not a bound q3 token",
        )
    return {
        "runId": "run3:" + match.group(1),
        "selectionHash": match.group(2),
        "position": int(match.group(3)),
    }


def parse_endpoint_syntax(ep, label):
    """Malformed or incomplete endpoint syntax, both QUERY.PARAMS_MALFORMED (contract section 2, schema-first).

    Agrees with GraphEndpoint: a package endpoint without a non-empty packageManifestPath is an incomplete
    request, never QUERY.ENDPOINT_AMBIGUOUS. Does not test vertex membership.
    """
    if type(ep) is not dict:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.PARAMS_MALFORMED",
            "graph endpoint must be an object {universe,kind,nativeSubjectId}",
            label,
        )
    extra = set(ep) - {"universe", "kind", "nativeSubjectId", "packageManifestPath"}
    if extra:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.PARAMS_MALFORMED",
            "graph endpoint has unknown properties",
            label,
        )
    universe, kind, native = ep.get("universe"), ep.get("kind"), ep.get("nativeSubjectId")
    if type(universe) is not str or not re.fullmatch(r"[0-9a-f]{64}", universe):
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.PARAMS_MALFORMED",
            "endpoint.universe must be a 64-hex native universe H-identity",
            label,
        )
    if kind not in STORED_KINDS:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.PARAMS_MALFORMED",
            "endpoint kind is file|symbol|package",
            label,
        )
    if type(native) is not str or not native or len(native) > 4096:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.PARAMS_MALFORMED",
            "endpoint.nativeSubjectId is required text",
            label,
        )
    if kind == "package":
        path = ep.get("packageManifestPath")
        if type(path) is not str or not path:
            raise QueryRefusal(
                "REQUEST.PRECONDITION_FAILED",
                "QUERY.PARAMS_MALFORMED",
                "package endpoints require a non-empty packageManifestPath coordinate",
                label,
            )
    elif ep.get("packageManifestPath"):
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.PARAMS_MALFORMED",
            "packageManifestPath is only lawful on kind=package",
            label,
        )
    got = canonical_endpoint(ep)
    if got is None:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.PARAMS_MALFORMED",
            "endpoint could not be canonically named",
            label,
        )
    return got


def effective_params(operation, params):
    p = copy.deepcopy(params)
    out = {
        "direction": p["direction"],
        "minResolution": p["minResolution"],
        "relation": p["relation"],
    }
    if operation == "graph.neighbors":
        out["endpoint"] = parse_endpoint_syntax(p["endpoint"], "endpoint")
    elif operation == "graph.path":
        out["start"] = parse_endpoint_syntax(p["start"], "start")
        out["target"] = parse_endpoint_syntax(p["target"], "target")
        out["maxDepth"] = p["maxDepth"]
    elif operation == "graph.reach":
        out["start"] = parse_endpoint_syntax(p["start"], "start")
        out["maxDepth"] = p["maxDepth"]
        out["includeStart"] = bool(p["includeStart"]) if "includeStart" in p else False
    return out


def _blob_payload(blobs, digest, label):
    raw = blobs.get(digest)
    if raw is None:
        raise QueryRefusal(
            "HOST.IO_FAILURE",
            "evidence.missing",
            "restore the exact retained payload bytes",
            label,
            klass="operational-failed",
            fault_cause="host-io",
        )
    if type(raw) is not bytes:
        raise QueryRefusal(
            "HOST.IO_FAILURE",
            "evidence.corrupt",
            "retained payload is not raw bytes",
            label,
            klass="operational-failed",
            fault_cause="host-io",
        )
    if hashlib.sha256(raw).hexdigest() != digest:
        raise QueryRefusal(
            "HOST.IO_FAILURE",
            "evidence.corrupt",
            "retained payload digest mismatch",
            label,
            klass="operational-failed",
            fault_cause="host-io",
        )
    try:
        return canonical.parse(raw)
    except canonical.AdmissionError as exc:
        raise QueryRefusal(
            "HOST.IO_FAILURE",
            "evidence.corrupt",
            "retained payload is not exact JSON",
            label,
            klass="operational-failed",
            fault_cause="host-io",
        ) from exc


def _object(objects, key, domain, detail="QUERY.FACT_VIEW_UNAVAILABLE"):
    if key not in objects:
        if detail.startswith("evidence."):
            raise QueryRefusal(
                "HOST.IO_FAILURE",
                detail,
                "restore the exact retained closure bytes",
                key,
                klass="operational-failed",
                fault_cause="host-io",
            )
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            detail,
            "selected fact-view or fact is not admitted on this Run",
            key,
        )
    actual, value = objects[key]
    if actual != domain:
        raise QueryRefusal(
            "HOST.IO_FAILURE",
            "evidence.corrupt",
            "retained object domain mismatch",
            key,
            klass="operational-failed",
            fault_cause="host-io",
        )
    return value


# evaluator-fault-observation.schema.v3.json host-internal remedy for an invalid host-generated internal layer.
HOST_INVARIANT_REMEDY = "Report the host defect with the retained diagnostic."


def owner_carrier_refusal(carrier, diagnostic):
    """Project an identity owner termination carrier verbatim; the query does not restate its route."""
    term = carrier.termination
    detail = term["domainDetail"]
    return QueryRefusal(
        term["errorCode"],
        detail["code"],
        detail["remedy"],
        detail.get("subject"),
        klass=term["class"],
        fault_cause=term["faultCause"],
        diagnostic=diagnostic,
    )


def host_invariant_refusal(boundary, diagnostic):
    """A host-owned step failed without an owner decision. Existing host-internal invariant route; no evidence is blamed."""
    return QueryRefusal(
        "SYSTEM.OUTCOME.ILLEGAL_STATE",
        "HOST.INVARIANT_VIOLATED",
        HOST_INVARIANT_REMEDY,
        boundary,
        klass="operational-failed",
        fault_cause="host-invariant",
        diagnostic=diagnostic,
    )


def close_retained_run(run, objects, blobs):
    """Contract section 7. Route by the exact typed outcome of this module's identity copy, never by message text.

    The graph query is a retained read, so complete replay disagreement is the retained-regeneration boundary.
    """
    M = identity3()
    try:
        return M.close_run(run, objects, blobs)
    except M.EvidenceUnavailable as exc:
        raise QueryRefusal(
            "HOST.IO_FAILURE",
            "evidence.missing",
            "restore the exact retained closure bytes or report their unavailability",
            exc.reference,
            klass="operational-failed",
            fault_cause="host-io",
            diagnostic=str(exc),
        ) from exc
    except M.CompleteReplayMismatch as exc:
        raise owner_carrier_refusal(M.RegenerationMismatch(M.identifier("run", run)), exc.diagnostic) from exc
    except M.C.AdmissionError as exc:
        raise QueryRefusal(
            "HOST.IO_FAILURE",
            "evidence.corrupt",
            "retained Run failed closed fact-view admission",
            str(exc)[:200],
            klass="operational-failed",
            fault_cause="host-io",
            diagnostic=str(exc),
        ) from exc
    except Exception as exc:
        raise host_invariant_refusal("close_run", type(exc).__name__ + ": " + str(exc)) from exc


def join_request_view(request, run, run_id, host, cursor_bind):
    """Admitted Run is authority. Host snapshot indexes are not. latest is a trusted observation."""
    view = request["view"]
    if cursor_bind is not None:
        if "runId" not in view or view["runId"] != cursor_bind["runId"] or view["runId"] != run_id:
            raise QueryRefusal(
                "REQUEST.PRECONDITION_FAILED",
                "QUERY.CURSOR_MISMATCH",
                "continuation must reuse the bound runId and must not re-resolve latest or snapshot",
            )
        return run_id
    if "runId" in view:
        if view["runId"] != run_id:
            raise QueryRefusal(
                "IDENTITY.UNKNOWN",
                "QUERY.VIEW_UNKNOWN",
                "request runId is not the admitted Run",
                view["runId"],
            )
        return run_id
    if view.get("latest") is True:
        latest = (host or {}).get("latestRunId")
        if not latest:
            raise QueryRefusal(
                "IDENTITY.UNKNOWN",
                "QUERY.VIEW_UNKNOWN",
                "latest requires an explicit trusted host observation of the current runId",
            )
        if latest != run_id:
            raise QueryRefusal(
                "IDENTITY.UNKNOWN",
                "QUERY.VIEW_UNKNOWN",
                "admitted Run is not the host-observed latest",
                latest,
            )
        return run_id
    snap = view.get("snapshotId")
    if snap != run["snapshotId"]:
        raise QueryRefusal(
            "IDENTITY.UNKNOWN",
            "QUERY.VIEW_UNKNOWN",
            "request snapshotId is not the admitted Run snapshot; a host index is not authority",
            snap,
        )
    observed = (host or {}).get("runsForSnapshot")
    if type(observed) is not dict or snap not in observed:
        raise QueryRefusal(
            "IDENTITY.UNKNOWN",
            "QUERY.VIEW_UNKNOWN",
            "snapshot selection requires an explicit complete trusted host resolver observation for that snapshot",
            snap,
        )
    listed = observed.get(snap)
    if type(listed) is not list or len(listed) == 0:
        raise QueryRefusal(
            "IDENTITY.UNKNOWN",
            "QUERY.VIEW_UNKNOWN",
            "host snapshot resolver observation is empty; a single admitted Run does not prove uniqueness",
            snap,
        )
    unique = []
    for item in listed:
        if item not in unique:
            unique.append(item)
    if len(unique) > 1:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.VIEW_AMBIGUOUS",
            "host snapshot resolver names more than one Run; name runId",
            snap,
        )
    if unique[0] != run_id:
        raise QueryRefusal(
            "IDENTITY.UNKNOWN",
            "QUERY.VIEW_UNKNOWN",
            "unique host snapshot observation does not name the admitted Run",
            snap,
        )
    return run_id


def view_matches_relation(view, objects, relation, min_resolution):
    for sid in view.get("scopeIds") or []:
        if sid not in objects:
            continue
        domain, scope = objects[sid]
        if domain != "subject-scope":
            continue
        if scope.get("relation") == relation and scope.get("resolution") == min_resolution:
            return True
    return False


def select_views(evidence_view_ids, objects, params, requested):
    admitted = list(evidence_view_ids)
    if requested:
        missing = [v for v in requested if v not in admitted]
        if missing:
            raise QueryRefusal(
                "REQUEST.PRECONDITION_FAILED",
                "QUERY.FACT_VIEW_UNAVAILABLE",
                "selected view2 is not admitted on this Run",
                missing[0],
            )
        return sorted(set(requested))
    selected = []
    for vid in admitted:
        view = _object(objects, vid, "view")
        if view_matches_relation(view, objects, params["relation"], params["minResolution"]):
            selected.append(vid)
    return sorted(set(selected))


def load_enumeration_plan(plan, blobs):
    spec = _blob_payload(blobs, plan["analysisSpecDigest"], "analysisSpec")
    M = identity3()
    for parameter in spec.get("parameters") or []:
        digest = parameter.get("schemaDigest")
        if type(digest) is not str:
            continue
        if M.parameter_row_of(digest) == ENUM_PLAN_ROW:
            return _blob_payload(blobs, parameter["payloadDigest"], "enumeration-plan")
    return None


def inventory_universe(enum_plan, inventory):
    if enum_plan is None:
        return None
    cells = enum_plan.get("cells") or []
    ordinal = inventory.get("cellOrdinal")
    if type(ordinal) is not int or ordinal < 0 or ordinal >= len(cells):
        return None
    for binding in cells[ordinal].get("programBindings") or []:
        if binding.get("ordinal") == inventory.get("programOrdinal"):
            universe = binding.get("universe")
            return universe if type(universe) is str else None
    return None


def inventory_vertices(proof, plan, blobs):
    enum_plan = load_enumeration_plan(plan, blobs)
    vertices = {}
    ambiguous = set()
    for ref in proof.get("evaluationInputRefs") or []:
        if ref.get("domain") != "subject-inventory":
            continue
        inv = _blob_payload(blobs, ref["digest"], ref["digest"])
        universe = inventory_universe(enum_plan, inv)
        if not universe:
            continue
        kind = inv.get("kind")
        for row in inv.get("rows") or []:
            ep = {
                "universe": universe,
                "kind": kind,
                "nativeSubjectId": row["nativeSubjectId"],
            }
            if kind == "package":
                ep["packageManifestPath"] = row.get("path") or row.get("packageManifestPath")
                if not ep.get("packageManifestPath"):
                    continue
            named = canonical_endpoint(ep)
            if named is None:
                continue
            key = endpoint_tuple(named)
            if key in vertices and vertices[key] != named:
                ambiguous.add(key)
            vertices[key] = named
    return vertices, ambiguous


def retained_attributions(proof, blobs):
    out = {}
    for ref in proof.get("evaluationInputRefs") or []:
        if ref.get("domain") != "target-attribution":
            continue
        value = _blob_payload(blobs, ref["digest"], ref["digest"])
        fid = value.get("sourceFactId")
        if fid:
            out[fid] = value
    return out


def occupancy_inputs_from_retained(proof, plan, objects, blobs, producer_closures=None):
    """Atom-shaped occupancy inputs from the admitted Run closure only.

    Inventories and sidecars are the selected evaluationInputRefs. Enumeration
    is the plan's registered enumeration-plan parameter. Closures are named
    producer records already in the retained objects map. Host targetAttributions
    and ambient unselected blobs are not consulted.
    """
    inventories = []
    attributions = {}
    needed = set(producer_closures or ())
    for ref in proof.get("evaluationInputRefs") or []:
        domain = ref.get("domain")
        digest = ref.get("digest")
        if domain == "subject-inventory":
            inventories.append(_blob_payload(blobs, digest, digest))
        elif domain == "target-attribution":
            value = _blob_payload(blobs, digest, digest)
            fid = value.get("sourceFactId")
            if fid:
                attributions[fid] = value
            pc = value.get("producerClosure")
            if pc:
                needed.add(pc)
    closures = {}
    for cid in needed:
        rec = objects.get(cid)
        if rec and rec[0] == "closure":
            closures[cid] = rec[1]
    return {
        "enumerationPlan": load_enumeration_plan(plan, blobs),
        "inventories": inventories,
        "targetAttributions": attributions,
        "closures": closures,
    }


def retained_incoming_search(proof, blobs, relation, min_resolution):
    rows = []
    for ref in proof.get("evaluationInputRefs") or []:
        if ref.get("domain") != "incoming-search":
            continue
        value = _blob_payload(blobs, ref["digest"], ref["digest"])
        if value.get("relation") == relation and value.get("minResolution") == min_resolution:
            rows.append((ref["digest"], value))
    return rows


def project_fact(fact_id, fact, payload, table, occupancy=None):
    """Project one fact using reconciled occupancy, not raw sidecar fields.

    occupancy is atom_model._reconcile_attribution output (or None).
    Multi-kind relations need a known occupancy kind. Single-kind relations
    keep payload native id for external/unknown occupancy.
    """
    src_field, tgt_field = table["sourceField"], table["targetField"]
    if type(payload) is not dict or src_field not in payload or tgt_field not in payload:
        return None, {"kind": "unprojectable-fact", "factId": fact_id, "note": "payload lacks native endpoint fields"}
    if payload[src_field] in (None, "") or payload[tgt_field] in (None, ""):
        return None, {"kind": "unprojectable-fact", "factId": fact_id, "note": "native endpoint id empty"}
    source = {
        "universe": fact["sourceUniverse"],
        "kind": table["sourceKind"],
        "nativeSubjectId": payload[src_field],
    }
    if table["universeRule"] == "admitted-target":
        target_universe = fact["targetUniverse"]
    else:
        target_universe = fact["sourceUniverse"]
    kinds = table["targetKinds"]
    occ = occupancy or {}
    occ_state = occ.get("occupancy") or "unknown"
    occ_kind = occ.get("kind") or "unknown"
    package_path = occ.get("packageManifestPath")
    if len(kinds) == 1:
        tkind = kinds[0]
        if occ_kind in STORED_KINDS and occ_kind != tkind:
            return None, {
                "kind": "unprojectable-fact",
                "factId": fact_id,
                "note": "target attribution kind disagrees with table",
            }
        if occ_state == "first-party":
            native = occ.get("nativeId")
            if not native:
                return None, {
                    "kind": "unprojectable-fact",
                    "factId": fact_id,
                    "note": "first-party occupancy missing occupancy identity",
                }
        else:
            native = payload[tgt_field]
            if tkind != "package":
                package_path = None
    else:
        if occ_state == "unknown":
            return None, {
                "kind": "unprojectable-fact",
                "factId": fact_id,
                "note": "missing occupancy mapping with no unique exact-id identity",
            }
        if occ_kind not in kinds:
            return None, {
                "kind": "unprojectable-fact",
                "factId": fact_id,
                "note": "reconciled occupancy kind is not an imports target kind",
            }
        tkind = occ_kind
        if occ_state == "first-party":
            native = occ.get("nativeId")
            if not native:
                return None, {
                    "kind": "unprojectable-fact",
                    "factId": fact_id,
                    "note": "first-party occupancy missing occupancy identity",
                }
        else:
            native = occ.get("payloadNativeId") or payload[tgt_field]
    target = {
        "universe": target_universe,
        "kind": tkind,
        "nativeSubjectId": native,
    }
    if tkind == "package":
        if not package_path:
            return None, {
                "kind": "unprojectable-fact",
                "factId": fact_id,
                "note": "package target missing packageManifestPath",
            }
        target["packageManifestPath"] = package_path
    src = canonical_endpoint(source)
    tgt = canonical_endpoint(target)
    if src is None or tgt is None:
        return None, {"kind": "unprojectable-fact", "factId": fact_id}
    row = {
        "confidenceMillionths": fact["confidenceMillionths"],
        "factId": fact_id,
        "producerClosure": fact["producerClosure"],
        "relation": fact["relation"],
        "resolution": fact["resolution"],
        "source": src,
        "target": tgt,
    }
    return row, None


def _reconcile_fact_occupancy(fact, occupancy_inputs):
    AM = atom_model()
    spec = AM.REGISTRY["relations"].get(fact.get("relation")) or {}
    sidecar = (occupancy_inputs.get("targetAttributions") or {}).get(fact.get("factId"))
    if sidecar is not None and sidecar.get("schemaVersion") == 1:
        raise AM.AtomAdmissionError("TARGET_ATTRIBUTION_SCHEMA_VERSION")
    return AM._reconcile_attribution(fact, spec, occupancy_inputs)


def collect_projected_edges(selected_views, objects, blobs, table, occupancy_inputs):
    facts = {}
    limitations = []
    coverage_ids = []
    scope_ids = []
    for vid in selected_views:
        view = _object(objects, vid, "view")
        coverage_ids.extend(view.get("coverageIds") or [])
        scope_ids.extend(view.get("scopeIds") or [])
        for fid in view.get("facts") or []:
            if fid not in facts:
                facts[fid] = vid
    projected = []
    AM = atom_model()
    for fid in sorted(facts):
        fact = _object(objects, fid, "fact", "evidence.missing")
        payload = _blob_payload(blobs, fact["payloadDigest"], fid)
        key = (fact.get("relation"), fact.get("resolution"))
        if key != (table["relation"], table["minResolution"]):
            if fact.get("relation") == table["relation"]:
                limitations.append({"kind": "unsupported-rung-omitted", "factId": fid})
            continue
        fact_for_occ = dict(fact)
        fact_for_occ["payload"] = payload
        fact_for_occ["factId"] = fid
        try:
            occupancy = _reconcile_fact_occupancy(fact_for_occ, occupancy_inputs)
        except AM.AtomAdmissionError as exc:
            limitations.append({
                "kind": "unprojectable-fact",
                "factId": fid,
                "note": "occupancy admission " + exc.key,
            })
            continue
        row, limitation = project_fact(fid, fact_for_occ, payload, table, occupancy)
        if limitation:
            limitations.append(limitation)
            continue
        projected.append(row)
    return projected, limitations, sorted(set(coverage_ids)), sorted(set(scope_ids))


def coverage_entry(payload):
    if type(payload) is not dict:
        return {}
    entry = payload.get("entry")
    return entry if type(entry) is dict else payload


def relevant_resolution_limitations(evidence, objects, blobs, relation, selected_scope_ids, incoming):
    out = []
    seen_cov = set()
    for cid in evidence.get("coverageIds") or []:
        if cid not in objects or objects[cid][0] != "coverage":
            continue
        cov = objects[cid][1]
        payload = _blob_payload(blobs, cov["payloadDigest"], cid)
        entry = coverage_entry(payload)
        key = payload.get("key") if type(payload) is dict else {}
        same_relation = (entry.get("relation") == relation) or (type(key) is dict and key.get("relation") == relation)
        if not same_relation:
            continue
        seen_cov.add(cid)
        rc = entry.get("resolutionCompleteness") if type(entry.get("resolutionCompleteness")) is dict else {}
        state = rc.get("state")
        token = entry.get("coverage")
        row = {"coverageId": cid}
        if type(rc.get("unresolvedEdgeCount")) is int:
            row["unresolvedEdgeCount"] = rc["unresolvedEdgeCount"]
        if type(rc.get("examinedExhaustive")) is bool:
            row["examinedExhaustive"] = rc["examinedExhaustive"]
        if type(rc.get("attempted")) is bool:
            row["attempted"] = rc["attempted"]
        if state in ("not-attempted", "partial", "complete", "not-applicable", "incomplete"):
            row["resolutionState"] = state
        if token in ("complete", "partial", "unknown"):
            row["coverage"] = token
        if state == "not-attempted":
            row["kind"] = "resolution-not-attempted"
        elif state == "partial":
            row["kind"] = "resolution-partial"
        elif state == "incomplete" or entry.get("deficiency") == "resolution-incomplete":
            row["kind"] = "resolution-incomplete"
        elif token == "unknown":
            row["kind"] = "coverage-unknown"
        elif token == "partial":
            row["kind"] = "coverage-partial"
        elif rc.get("examinedExhaustive") is False and state not in ("not-applicable", None):
            row["kind"] = "examined-not-exhaustive"
        else:
            continue
        out.append(row)
    for vid in evidence.get("viewIds") or []:
        if vid not in objects or objects[vid][0] != "view":
            continue
        view = objects[vid][1]
        for fid in view.get("facts") or []:
            if fid not in objects or objects[fid][0] != "fact":
                continue
            fact = objects[fid][1]
            if fact.get("relation") == "unresolved-edge":
                out.append({"kind": "unresolved-edge-present", "factId": fid})
    for digest, att in incoming:
        rc = att.get("resolutionCompleteness") if type(att.get("resolutionCompleteness")) is dict else {}
        row = {
            "kind": "incoming-search-incomplete",
            "incomingSearchDigest": digest,
            "coverage": att.get("coverage") if att.get("coverage") in ("complete", "partial", "unknown") else "unknown",
        }
        if type(rc.get("unresolvedEdgeCount")) is int:
            row["unresolvedEdgeCount"] = rc["unresolvedEdgeCount"]
        if type(rc.get("examinedExhaustive")) is bool:
            row["examinedExhaustive"] = rc["examinedExhaustive"]
        if type(rc.get("attempted")) is bool:
            row["attempted"] = rc["attempted"]
        if rc.get("state") in ("not-attempted", "partial", "complete", "not-applicable", "incomplete"):
            row["resolutionState"] = rc["state"]
        if att.get("completeSearch") is True and att.get("coverage") == "complete":
            continue
        out.append(row)
    return out, selected_scope_ids, sorted(seen_cov)


def deficiency_citations(proof):
    rows = []
    for item in proof.get("executionDeficiencies") or []:
        if type(item) is not dict:
            continue
        source = item.get("source")
        cause = item.get("cause")
        if source not in DEFICIENCY_SOURCES or type(cause) is not str:
            continue
        refs = item.get("inputRefs")
        if type(refs) is not list:
            refs = []
        cleaned = []
        for ref in refs:
            if type(ref) is dict and type(ref.get("domain")) is str and type(ref.get("digest")) is str:
                cleaned.append({"digest": ref["digest"], "domain": ref["domain"]})
        cleaned = sorted(cleaned, key=lambda r: canonical.canonical(r))
        row = {"cause": cause[:128], "inputRefs": cleaned, "source": source}
        if "subjectId" in item:
            row["subjectId"] = item["subjectId"]
        if "predicateId" in item:
            row["predicateId"] = item["predicateId"]
        if item.get("nativeCause") is not None:
            row["nativeCause"] = item["nativeCause"]
        rows.append(row)
    return rows


class VisitBudget:
    """Distinct canonical-endpoint visits. Check before entering an unvisited vertex."""

    def __init__(self, maximum):
        self.maximum = maximum
        self.seen = set()
        self.truncated = False

    def enter(self, ep):
        key = endpoint_tuple(ep)
        if key in self.seen:
            return True
        if len(self.seen) >= self.maximum:
            self.truncated = True
            return False
        self.seen.add(key)
        return True

    @property
    def count(self):
        return len(self.seen)


def directed_hops(projected, direction):
    hops = []
    for edge in projected:
        if direction in ("outgoing", "both"):
            hops.append((endpoint_tuple(edge["source"]), endpoint_tuple(edge["target"]), edge, edge["source"], edge["target"]))
        if direction in ("incoming", "both"):
            hops.append((endpoint_tuple(edge["target"]), endpoint_tuple(edge["source"]), edge, edge["target"], edge["source"]))
    adj = {}
    for src_k, dst_k, edge, src_ep, dst_ep in hops:
        adj.setdefault(src_k, []).append((edge["factId"], dst_k, edge, src_ep, dst_ep))
    for key in adj:
        adj[key].sort(key=lambda row: row[0].encode("utf-8"))
    return adj


def neighbor_units(projected, endpoint, direction):
    rows = []
    seen = set()
    for edge in projected:
        hit = False
        if direction in ("outgoing", "both") and endpoints_equal(edge["source"], endpoint):
            hit = True
        if direction in ("incoming", "both") and endpoints_equal(edge["target"], endpoint):
            hit = True
        if hit and edge["factId"] not in seen:
            seen.add(edge["factId"])
            rows.append(edge)
    rows.sort(key=lambda r: endpoint_key(r["source"]) + endpoint_key(r["target"]) + (r["factId"].encode("utf-8"),))
    return rows


def path_unit(projected, start, target, direction, max_depth, budget):
    """Canonical BFS path. Adjacency is fact2-id order. First reach of the target
    is the selected shortest hop-count path and the lex-least fact2 sequence among
    those shortest paths, so search stops there. Unfinished extra branches are
    not owed and must not truncate a proven witness. If the cap hits before the
    target is reached, no path is claimed.
    """
    start = canonical_endpoint(start)
    target = canonical_endpoint(target)
    if not budget.enter(start):
        return [], budget
    if endpoints_equal(start, target):
        return (
            [{"edges": [], "hopCount": 0, "nodes": [start], "start": start, "target": target}],
            budget,
        )
    adj = directed_hops(projected, direction)
    start_k, target_k = endpoint_tuple(start), endpoint_tuple(target)
    seen = {start_k}
    queue = deque([(start_k, 0, tuple(), [start], [])])
    while queue:
        node_k, depth, seq, nodes, edges = queue.popleft()
        if depth >= max_depth:
            continue
        for fact_id, dst_k, edge, src_ep, dst_ep in adj.get(node_k, []):
            if dst_k in seen:
                continue
            if any(endpoint_tuple(n) == dst_k for n in nodes):
                continue
            if not budget.enter(dst_ep):
                return [], budget
            seen.add(dst_k)
            hop = {"factId": fact_id, "source": canonical_endpoint(src_ep), "target": canonical_endpoint(dst_ep)}
            new_nodes = nodes + [canonical_endpoint(dst_ep)]
            new_edges = edges + [hop]
            new_seq = seq + (fact_id,)
            new_depth = depth + 1
            if dst_k == target_k:
                return (
                    [{
                        "edges": new_edges,
                        "hopCount": new_depth,
                        "nodes": new_nodes,
                        "start": start,
                        "target": target,
                    }],
                    budget,
                )
            queue.append((dst_k, new_depth, new_seq, new_nodes, new_edges))
    return [], budget


def reach_units(projected, start, direction, max_depth, include_start, budget):
    start = canonical_endpoint(start)
    if not budget.enter(start):
        return [], budget
    adj = directed_hops(projected, direction)
    start_k = endpoint_tuple(start)
    rows = []
    if include_start:
        rows.append({"depth": 0, "endpoint": start})
    seen = {start_k}
    queue = deque([(start_k, 0)])
    while queue:
        node_k, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for fact_id, dst_k, edge, src_ep, dst_ep in adj.get(node_k, []):
            if dst_k in seen:
                continue
            if not budget.enter(dst_ep):
                break
            seen.add(dst_k)
            rows.append({"depth": depth + 1, "endpoint": canonical_endpoint(dst_ep), "viaFactId": fact_id})
            queue.append((dst_k, depth + 1))
        if budget.truncated:
            break
    rows.sort(key=lambda r: endpoint_key(r["endpoint"]))
    return rows, budget


def apply_produced_cap(units, max_produced, already_truncated):
    if len(units) > max_produced:
        return units[:max_produced], True
    return units, already_truncated


def admit_vertices(requested, vertices, ambiguous):
    """requested is list of (label, endpoint). vertices maps tuple -> endpoint.

    A fully specified unknown tuple is QUERY.ENDPOINT_UNKNOWN. Other-universe
    same native ids do not make it ambiguous. A package endpoint without its
    coordinate never reaches here: it is QUERY.PARAMS_MALFORMED at schema
    admission and at parse_endpoint_syntax. QUERY.ENDPOINT_AMBIGUOUS is only a
    complete tuple marked as resolving to more than one distinct admitted vertex;
    inventory_vertices keys vertices by the complete tuple, so the public wrapper
    does not produce that mark from one retained Run.
    """
    for label, ep in requested:
        key = endpoint_tuple(ep)
        if key not in vertices:
            raise QueryRefusal(
                "REQUEST.PRECONDITION_FAILED",
                "QUERY.ENDPOINT_UNKNOWN",
                "endpoint is not an admitted inventory vertex or projected fact endpoint",
                label,
            )
        if key in ambiguous:
            raise QueryRefusal(
                "REQUEST.PRECONDITION_FAILED",
                "QUERY.ENDPOINT_AMBIGUOUS",
                "endpoint matches more than one admitted vertex",
                label,
            )


def _validate_request(request):
    if type(request) is not dict:
        raise QueryRefusal("REQUEST.PRECONDITION_FAILED", "QUERY.PARAMS_MALFORMED", "request must be an object")
    if request.get("schemaMajor") != 3:
        raise QueryRefusal(
            "REQUEST.SCHEMA_MAJOR_UNSUPPORTED",
            "QUERY.SCHEMA_MAJOR_UNSUPPORTED",
            "graph-query schemaMajor 3 required",
        )
    if request.get("schemaFamily") != "opensip.product.query":
        raise QueryRefusal("REQUEST.PRECONDITION_FAILED", "QUERY.PARAMS_MALFORMED", "schemaFamily opensip.product.query")
    try:
        validate_schema(SCHEMA_ID + "#/$defs/GraphQueryRequestV1", request)
    except (ValidationError, canonical.AdmissionError) as exc:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.PARAMS_MALFORMED",
            "graph request failed closed schema admission",
            str(exc).splitlines()[0][:200],
        ) from exc
    if request["operation"] not in GRAPH_OPS:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.PARAMS_MALFORMED",
            "this projection owner implements graph.neighbors|path|reach only",
            request["operation"],
        )


def _attach(refusal, request, host):
    refusal.request = request
    refusal.host = host
    return refusal


def traverse_projected_graph(operation, params, edges, *, vertices=None, bounds=None, completeness="required", page=None, project_id=None, run_id=None, fact_view_digests=None):
    """Internal algorithm helper over already-projected edges. Not close_run and not a public query."""
    table = projection_table()
    key = (params["relation"], params["minResolution"])
    if key not in table:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.RELATION_UNSUPPORTED",
            "relation@minResolution is not a binary native-id graph projection",
            "%s@%s" % (params["relation"], params["minResolution"]),
        )
    projected = []
    for edge in edges:
        if edge.get("relation") == params["relation"] and edge.get("resolution") == params["minResolution"]:
            projected.append(copy.deepcopy(edge))
    vertex_map = {}
    if vertices is None:
        for edge in projected:
            vertex_map[endpoint_tuple(edge["source"])] = edge["source"]
            vertex_map[endpoint_tuple(edge["target"])] = edge["target"]
        for field in ("endpoint", "start", "target"):
            if field in params:
                vertex_map[endpoint_tuple(params[field])] = params[field]
    else:
        for ep in vertices:
            vertex_map[endpoint_tuple(ep)] = canonical_endpoint(ep)
    requested = []
    if operation == "graph.neighbors":
        requested.append(("endpoint", params["endpoint"]))
    elif operation == "graph.path":
        requested.append(("start", params["start"]))
        requested.append(("target", params["target"]))
    else:
        requested.append(("start", params["start"]))
    admit_vertices(requested, vertex_map, set())
    bounds = bounds or dict(PUBLIC_BOUNDS)
    page = page or {"size": bounds["defaultPageSize"]}
    cursor_bind = decode_cursor(page["cursor"]) if page.get("cursor") else None
    return finish_operation(
        operation,
        params,
        projected,
        bounds,
        completeness,
        page,
        project_id or "prj1-" + ("0" * 64),
        run_id or ("run3:" + ("0" * 64)),
        fact_view_digests or [],
        "retained",
        [],
        [],
        [],
        [],
        cursor_bind,
    )


def finish_operation(
    operation,
    params,
    projected,
    bounds,
    completeness,
    page,
    project_id,
    run_id,
    selected_views,
    availability,
    cites,
    limitations,
    coverage_ids,
    scope_ids,
    cursor_bind=None,
):
    budget = VisitBudget(bounds["maxVisitedNodes"])
    if operation == "graph.neighbors":
        if not budget.enter(params["endpoint"]):
            units = []
        else:
            units = neighbor_units(projected, params["endpoint"], params["direction"])
    elif operation == "graph.path":
        units, budget = path_unit(
            projected, params["start"], params["target"], params["direction"], params["maxDepth"], budget
        )
    else:
        units, budget = reach_units(
            projected,
            params["start"],
            params["direction"],
            params["maxDepth"],
            params["includeStart"],
            budget,
        )
    visit_truncated = budget.truncated
    units, prod_trunc = apply_produced_cap(units, bounds["maxItemsPerOperation"], visit_truncated)
    walk_truncated = visit_truncated or prod_trunc
    bind = selection_hash(project_id, run_id, selected_views, operation, params)
    if cursor_bind is not None and cursor_bind["selectionHash"] != bind:
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.CURSOR_MISMATCH",
            "cursor does not bind this project+Run+fact-views+operation+effective params",
        )
    position = cursor_bind["position"] if cursor_bind is not None else 0
    if not (position == 0 and len(units) == 0) and not (0 <= position < len(units)):
        raise QueryRefusal(
            "REQUEST.PRECONDITION_FAILED",
            "QUERY.CURSOR_MISMATCH",
            "cursor page position is outside the bound produced prefix; continuation cannot pass work caps",
        )
    page_size = page["size"]
    items = units[position : position + page_size]
    more_prefix = position + len(items) < len(units)
    if more_prefix:
        traversal = "truncated-page"
        truncated = False
        next_cursor = encode_cursor(run_id, bind, position + len(items))
    elif walk_truncated:
        traversal = "truncated-bound"
        truncated = True
        next_cursor = None
    else:
        traversal = "complete"
        truncated = False
        next_cursor = None
    if walk_truncated:
        count_basis = "lower-bound"
        total_items = len(units)
        if not any(x.get("kind") == "unexamined-work-bound" for x in limitations):
            limitations = list(limitations) + [{"kind": "unexamined-work-bound", "note": "visited or produced cap with owed unexamined work"}]
    else:
        count_basis = "exact"
        total_items = len(units)
    evidence = {
        "coverageIds": coverage_ids,
        "deficiencyCitations": cites,
        "resolutionLimitations": limitations,
        "scopeIds": scope_ids,
    }
    context = {
        "advisory": False,
        "availability": availability,
        "countBasis": count_basis,
        "evidence": evidence,
        "factViewDigests": selected_views,
        "producedItems": len(units),
        "projectId": project_id,
        "resolvedView": {"runId": run_id},
        "totalItems": total_items,
        "traversalCoverage": traversal,
        "truncated": truncated,
        "visitedNodes": budget.count,
    }
    if next_cursor is not None:
        context["nextCursor"] = next_cursor
    termination = {"class": "success"}
    if completeness == "required" and walk_truncated:
        termination = {"class": "indeterminate", "reasonCodes": ["QUERY.COMPLETENESS_UNMET"], "runId": run_id}
    result = {
        "context": context,
        "items": items,
        "operation": operation,
        "schemaFamily": "opensip.product.query",
        "schemaMajor": 3,
        "termination": termination,
    }
    validate_schema(SCHEMA_ID + "#/$defs/GraphQueryResponseV1", result)
    validate_schema(COMMON_ID + "#/$defs/StepTermination", termination)
    return result


# Contract section 7. The identity availability.state values purged/expired/corrupt/unavailable refuse with these
# registered details; `unavailable` routes to evidence.missing, the identity owner's missing-evidence carrier. The
# states `retained` and `partial` are absent on purpose: they neither refuse nor grant, and close_run decides.
# `missing` is not an identity availability state; it is the same missing-bytes refusal a host may report directly.
AVAIL_REFUSE = {
    "purged": "evidence.purged",
    "expired": "evidence.expired",
    "corrupt": "evidence.corrupt",
    "unavailable": "evidence.missing",
    "missing": "evidence.missing",
}


def observe_availability(host):
    """Identity availability is a trusted current host observation.

    It may refuse access. It cannot grant retained authority; close_run remains
    the positive admission. Owner: foundation EvidenceStore / identity availability.
    """
    if "availability" not in (host or {}):
        return "retained"
    avail = host["availability"]
    if type(avail) is not str or avail not in (*AVAIL_REFUSE, "retained", "partial"):
        raise ReferenceCallPrecondition(
            "host.availability",
            "supply a typed availability observation or omit it; an unknown value is not evidence availability",
        )
    if avail in AVAIL_REFUSE:
        raise QueryRefusal(
            "HOST.IO_FAILURE",
            AVAIL_REFUSE[avail],
            "current host availability observation refuses access to retained evidence; it cannot be treated as an empty graph",
            avail,
            klass="operational-failed",
            fault_cause="host-io",
        )
    return "retained"


def host_adapter_refusal(precondition, request=None, host=None):
    """Contract section 7 product host adapter law for its OWN invalid trusted observation.

    The reference entry raises ReferenceCallPrecondition because the observation is a call argument. An adapter
    that produced an out-of-vocabulary observation violated a host invariant: with a valid reserved RequestId it
    terminates by the existing host-internal route. A RequestId precondition, or no valid RequestId, has no
    envelope and is re-raised.
    """
    if type(precondition) is not ReferenceCallPrecondition or precondition.missing == "host.requestId":
        raise precondition
    reserved_request_id(host)
    return _attach(
        host_invariant_refusal(precondition.missing, "ReferenceCallPrecondition: " + precondition.missing),
        request,
        host,
    )


def observe_retained_availability(raw, run_id):
    """Adapter read of a RETAINED identity availability record, not a host observation.

    A record failing identity availability admission is corrupt retained evidence, never an adapter invariant
    fault or an omitted observation. An admitted record supplies its state as the host observation.
    """
    M = identity3()
    try:
        record = M.C.parse(raw)
        schema = copy.deepcopy(M.SCHEMA)
        schema["$ref"] = "#/$defs/availability"
        M.C.validate(schema, record)
        if record["runId"] != run_id:
            raise M.C.AdmissionError("AVAILABILITY_RUN_JOIN")
    except (M.C.AdmissionError, M.C.ValidationError) as exc:
        raise QueryRefusal(
            "HOST.IO_FAILURE",
            "evidence.corrupt",
            "retained availability record failed identity availability admission",
            run_id,
            klass="operational-failed",
            fault_cause="host-io",
            diagnostic=str(exc),
        ) from exc
    return record["state"]


def execute_graph_query(request, run=None, objects=None, blobs=None, host=None):
    """Strong public graph query. Always close_run. host.standing cannot bypass admission."""
    host = {} if host is None else host
    try:
        _validate_request(request)
        if run is None or objects is None or blobs is None:
            raise QueryRefusal(
                "IDENTITY.UNKNOWN",
                "QUERY.VIEW_UNKNOWN",
                "graph query requires a retained Run and closed fact-view admission",
            )
        observe_availability(host)
        operation = request["operation"]
        params = effective_params(operation, request["params"])
        table = projection_table().get((params["relation"], params["minResolution"]))
        if table is None:
            raise QueryRefusal(
                "REQUEST.PRECONDITION_FAILED",
                "QUERY.RELATION_UNSUPPORTED",
                "unsupported relation@rung is refused; individual unprojectable facts are omitted with disclosure",
                "%s@%s" % (params["relation"], params["minResolution"]),
            )
        bounds = work_bounds(host)
        page = request["page"]
        cursor_bind = decode_cursor(page["cursor"]) if page.get("cursor") else None
        if run.get("projectId") != request["projectId"]:
            raise QueryRefusal(
                "REQUEST.PRECONDITION_FAILED",
                "QUERY.PARAMS_MALFORMED",
                "projectId does not match the admitted Run",
            )
        admitted_id = close_retained_run(run, objects, blobs)
        join_request_view(request, run, admitted_id, host, cursor_bind)
        evidence = _object(objects, run["evidenceId"], "semantic-evidence", "evidence.missing")
        proof = _object(
            objects,
            _object(objects, run["evaluationSealId"], "evaluation-seal", "evidence.missing")["proofBundleId"],
            "proof-bundle",
            "evidence.missing",
        )
        plan = _object(objects, run["planId"], "plan", "evidence.missing")
        selected_views = select_views(
            evidence.get("viewIds") or [], objects, params, request["params"].get("factViewDigests")
        )
        matching_selected = [
            vid
            for vid in selected_views
            if view_matches_relation(
                _object(objects, vid, "view"), objects, params["relation"], params["minResolution"]
            )
        ]
        missing_selection = []
        if not matching_selected:
            missing_selection = [{
                "kind": "native-evidence-unavailable",
                "minResolution": params["minResolution"],
                "note": "no retained selected fact-view of the declared relation@rung; not an absence claim",
                "relation": params["relation"],
            }]
        producer_closures = set()
        for vid in selected_views:
            view = _object(objects, vid, "view")
            for fid in view.get("facts") or []:
                frec = objects.get(fid)
                if frec and frec[0] == "fact" and frec[1].get("producerClosure"):
                    producer_closures.add(frec[1]["producerClosure"])
        occupancy_inputs = occupancy_inputs_from_retained(
            proof, plan, objects, blobs, producer_closures
        )
        projected, proj_limits, sel_cov, sel_scope = collect_projected_edges(
            selected_views, objects, blobs, table, occupancy_inputs
        )
        inv_vertices, ambiguous = inventory_vertices(proof, plan, blobs)
        for edge in projected:
            inv_vertices[endpoint_tuple(edge["source"])] = edge["source"]
            inv_vertices[endpoint_tuple(edge["target"])] = edge["target"]
        requested = []
        if operation == "graph.neighbors":
            requested.append(("endpoint", params["endpoint"]))
        elif operation == "graph.path":
            requested.append(("start", params["start"]))
            requested.append(("target", params["target"]))
        else:
            requested.append(("start", params["start"]))
        admit_vertices(requested, inv_vertices, ambiguous)
        incoming = retained_incoming_search(proof, blobs, params["relation"], params["minResolution"])
        rel_limits, scope_ids, coverage_ids = relevant_resolution_limitations(
            evidence, objects, blobs, params["relation"], sel_scope, incoming
        )
        coverage_ids = sorted(set(list(sel_cov) + list(coverage_ids)))
        cites = deficiency_citations(proof)
        limitations = missing_selection + proj_limits + rel_limits
        return finish_operation(
            operation,
            params,
            projected,
            bounds,
            request["completeness"],
            page,
            request["projectId"],
            admitted_id,
            selected_views,
            "retained",
            cites,
            limitations,
            coverage_ids,
            scope_ids,
            cursor_bind,
        )
    except QueryRefusal as exc:
        _attach(exc, request, host)
        raise
