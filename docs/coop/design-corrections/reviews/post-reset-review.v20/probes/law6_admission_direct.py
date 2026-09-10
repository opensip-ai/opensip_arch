"""Isolate law 6's admission path, away from the pinned native fixture.

The earlier fixture mutation could not separate the LAW from the fixture drift guard
(`v20-native-view-fixture-declares-current-registered-schemas`) and the source pins:
every edit tripped those first. This drives the admission helper directly.

Requirement 6 says empty / subset / registered-extra declarations stay LEGAL
declarations, arbitrary retained bytes REFUSE, and missing bytes retain UNAVAILABLE.
"""
import hashlib
import importlib.util
import json
import os
import sys

ROOT = sys.argv[1]
F = os.path.join(ROOT, "docs/coop/design-corrections/foundation")
spec = importlib.util.spec_from_file_location(
    "identity_model", os.path.join(F, "identity-model.py"))
M = importlib.util.module_from_spec(spec)
sys.modules["identity_model"] = M
spec.loader.exec_module(M)

registered = sorted(M.registered_schema_documents())
ANN = {"representation": "raw-artifact",
       "artifactClass": "registered-schema-document"}

# a blob store that retains exactly what we put in it
store = {}


def put(b):
    d = hashlib.sha256(b).hexdigest()
    store[d] = b
    return d


native_doc = open(os.path.join(
    ROOT,
    "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"),
    "rb").read()
# a GENUINELY registered second document (identity-schemas.v2.json is NOT on the
# payload-registry list, so it would refuse as unregistered and prove nothing here)
id_doc = open(os.path.join(
    ROOT,
    "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json"),
    "rb").read()
native_d, id_d = put(native_doc), put(id_doc)
arbitrary_d = put(b"retained bytes that are not a registered schema document")
missing_d = hashlib.sha256(b"never retained").hexdigest()   # deliberately not put


def admit(digests):
    """Run the model's own raw-artifact/registered-schema-document branch."""
    def blob(d):
        if d not in store:
            raise M.C.AdmissionError("BLOB_UNAVAILABLE:" + d)
        return store[d]
    results = []
    for d in digests:
        try:
            blob(d)
            if ANN.get("artifactClass") == "registered-schema-document" and \
                    d not in M.registered_schema_documents():
                raise M.C.AdmissionError("SCHEMA_DOCUMENT_UNREGISTERED:" + d)
            results.append(("ADMITTED", d[:12]))
        except M.C.AdmissionError as exc:
            results.append(("REFUSED", str(exc).split(":")[0], d[:12]))
    return results


cases = {
    "empty-declaration": [],
    "single-registered": [native_d],
    "subset-of-registered": [native_d],
    "registered-extra-unused": [native_d, id_d],
    "arbitrary-retained-bytes": [arbitrary_d],
    "missing-bytes": [missing_d],
    "mixed-registered-plus-arbitrary": [native_d, arbitrary_d],
}
out = {"registeredDocumentCount": len(registered), "cases": {}}
for name, ds in cases.items():
    r = admit(ds)
    out["cases"][name] = {
        "declared": len(ds),
        "results": r,
        "allAdmitted": all(x[0] == "ADMITTED" for x in r),
        "anyRefused": any(x[0] == "REFUSED" for x in r),
        "refusalKinds": sorted({x[1] for x in r if x[0] == "REFUSED"}),
    }

out["law6Verdict"] = {
    "emptyStaysLegal": out["cases"]["empty-declaration"]["allAdmitted"],
    "subsetStaysLegal": out["cases"]["subset-of-registered"]["allAdmitted"],
    "registeredExtraStaysLegal":
        out["cases"]["registered-extra-unused"]["allAdmitted"],
    "arbitraryRefuses":
        out["cases"]["arbitrary-retained-bytes"]["refusalKinds"] ==
        ["SCHEMA_DOCUMENT_UNREGISTERED"],
    "missingRetainsUnavailable":
        out["cases"]["missing-bytes"]["refusalKinds"] == ["BLOB_UNAVAILABLE"],
}
print(json.dumps(out, indent=2))
