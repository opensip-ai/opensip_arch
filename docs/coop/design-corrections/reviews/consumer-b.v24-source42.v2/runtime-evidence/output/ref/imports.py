"""Plan-selected import admission at Run closure (workflows-and-surfaces s4; identity-and-evidence s3 import record and
s6 lifecycle joins; atom-evaluation s6 import scope membership and flags; composition 'Retained input selection').

The import2 wrapper object is admitted by the caller (closure.obj). This module admits everything the wrapper names:
registered (kind, payloadDomain) row and exact schema-document bytes, canonical validated payload, SourceCorrespondence,
BuildIdentityV1, scope-descriptor, ImportObservationV1 (kind join, inapplicable members null, owner-field equality),
retained artifact blobs, producer/adapter closure kinds, and the closed StalenessRule table. It derives the
{consumable, staleness} flags; nothing is caller-supplied.
"""
import canonical as K
import schemas
import native_ctx as NC

KIT = schemas.kit()
ID = "foundation/identity-schemas.v3.json"
IE = "workflows/schemas/imported-evidence.schema.json"
CM = "workflows/schemas/common.schema.json"
ROWS = KIT.doc(ID)["x-opensip-payload-registry"]["classes"]["import"]["rows"]
INAPPLICABLE = {"runtime": ("selection", "revisionRange"), "history": ("window", "population", "selection"),
                "test": ("window", "population", "revisionRange"), "dependency": ("window", "population", "selection", "revisionRange"),
                "prepared": ("window", "population", "selection", "revisionRange")}


def _record(store, hx, doc, sel, label, faults, admitted):
    if hx not in store.blobs:
        faults.append(f"EVIDENCE_UNAVAILABLE:{label}")
        return None
    try:
        v = store.get_record(hx)
    except K.AdmissionError as exc:
        faults.append(f"IMPORT.ARTIFACT_CORRUPT:{label}:{exc.boundary}")
        return None
    r = KIT.admit(v, doc, sel)
    if not r["ok"]:
        faults.append(f"cb24.IMPORT_RECORD_SCHEMA:{label}:{r['typed']}{r['stock'][:1]}{r['order'][:1]}")
        return None
    admitted.append((label, v, doc, sel))
    return v


def staleness(correspondence, plan):
    """Closed StalenessRule table (workflows s4). Only exact-snapshot is reconstructed here; vcs-revision needs the
    SourceMappingV1 + expected-build join and is refused rather than guessed."""
    if correspondence["kind"] == "exact-snapshot":
        if correspondence["snapshotId"] == plan["snapshotId"]:
            return "current", "consumable", "snapshot-equal"
        return "stale", "unmapped-only", "snapshot-differs"
    return None, None, "cb24.IMPORT_VCS_REVISION_NOT_RECONSTRUCTED"


def admit_import(store, import_id, wrapper, plan):
    faults, admitted = [], []
    kind = wrapper["kind"]
    payload = None
    if wrapper["payloadDigest"] not in store.blobs:
        faults.append("EVIDENCE_UNAVAILABLE:import-payload")
    else:
        try:
            payload = store.get_record(wrapper["payloadDigest"])
        except K.AdmissionError as exc:
            faults.append(f"IMPORT.ARTIFACT_CORRUPT:payload:{exc.boundary}")
    row = None
    if payload is not None:
        domain = payload.get("payloadDomain") if isinstance(payload, dict) else None
        row = ROWS.get(f"{kind}|{domain}")
        if row is None:
            known = any(k.split("|", 1)[1] == domain for k in ROWS)
            faults.append("IMPORT.KIND_PAYLOAD_MISMATCH" if known else "IMPORT.PAYLOAD_SCHEMA_UNREGISTERED")
        else:
            if wrapper["payloadSchemaDigest"] != KIT.digest(row["document"]):
                faults.append("IMPORT.PAYLOAD_SCHEMA_UNREGISTERED")
            if store.blobs.get(wrapper["payloadSchemaDigest"]) != KIT.raw[schemas.norm_rel(row["document"])]:
                faults.append("EVIDENCE_UNAVAILABLE:import-payload-schema-document")
            r = KIT.admit(payload, row["document"], row["selector"])
            if not r["ok"]:
                faults.append(f"cb24.IMPORT_PAYLOAD_SCHEMA:{r['typed']}{r['stock'][:1]}{r['order'][:1]}")
            else:
                admitted.append((f"import-payload:{import_id}", payload, row["document"], row["selector"]))
            if kind == "runtime":
                keys = [(s["path"].encode(), s.get("symbol", "").encode(), "symbol" in s) for s in payload["subjects"]]
                for a, b in zip(keys, keys[1:]):
                    if (a[0], a[2], a[1]) == (b[0], b[2], b[1]):
                        faults.append("RUNTIME_SUBJECT_DUPLICATE_KEY")
                    elif (a[0], a[1]) >= (b[0], b[1]):
                        faults.append("cb24.RUNTIME_SUBJECT_ORDER")
    corr = _record(store, wrapper["sourceCorrespondenceDigest"], CM, "#/$defs/SourceCorrespondence", "source-correspondence", faults, admitted)
    build = _record(store, wrapper["buildDigest"], IE, "#/$defs/BuildIdentityV1", "build-identity", faults, admitted)
    scope = _record(store, wrapper["scopeDigest"], ID, "#/$defs/scope-descriptor", "import-scope", faults, admitted)
    obs = _record(store, wrapper["observationDigest"], IE, "#/$defs/ImportObservationV1", "import-observation", faults, admitted)
    if obs is not None:
        if obs["kind"] != kind:
            faults.append("ATOM_IMPORT_OBSERVATION_PAYLOAD_JOIN:kind")
        for member in INAPPLICABLE.get(kind, ()):
            if obs.get(member) is not None:
                faults.append(f"ATOM_IMPORT_OBSERVATION_PAYLOAD_JOIN:inapplicable-{member}")
        if payload is not None and row is not None and kind == "runtime":
            if obs["window"] is not None and obs["window"] != payload["observationWindow"]:
                faults.append("ATOM_IMPORT_OBSERVATION_PAYLOAD_JOIN:window")
            if obs["population"] is not None and obs["population"] != payload["observedPopulation"]:
                faults.append("ATOM_IMPORT_OBSERVATION_PAYLOAD_JOIN:population")
        if payload is not None and row is not None and kind == "history" and obs["revisionRange"] is not None:
            rr = payload["revisionRange"]
            if obs["revisionRange"]["from"] != rr["from"] or obs["revisionRange"]["to"] != rr["to"]:
                faults.append("ATOM_IMPORT_OBSERVATION_PAYLOAD_JOIN:revisionRange")
    for b in wrapper["blobs"]:
        data = store.blobs.get(b["sha256"])
        if data is None:
            faults.append(f"EVIDENCE_UNAVAILABLE:import-blob:{b['path']}")
        elif len(data) != b["bytes"]:
            faults.append(f"BLOB_LENGTH:import-blob:{b['path']}")
    for field, want in (("producerClosure", "provider"), ("adapterClosure", "adapter")):
        try:
            NC.admit_closure(store, wrapper[field], want, refusal_prefix=f"cb24.import-{field}")
        except NC.Refusal as exc:
            faults.append(f"{exc.key}:{exc.detail}")
    flags = None
    if corr is not None:
        st, usable, condition = staleness(corr, plan)
        if st is None:
            faults.append(condition)
        else:
            flags = {"consumable": usable == "consumable", "staleness": st}
            if st != "current":
                faults.append(f"IMPORT.STALE_FOR_PLAN:{condition}")
    return {"importId": import_id, "wrapper": wrapper, "payload": payload, "observation": obs, "scope": scope,
            "correspondence": corr, "build": build, "flags": flags, "faults": faults, "admitted": admitted}
