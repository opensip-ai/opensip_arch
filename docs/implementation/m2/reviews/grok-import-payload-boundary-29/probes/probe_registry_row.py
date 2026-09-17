"""Independent probes of selected workflows registry_row + identity import branch."""
from __future__ import annotations

import ast
import hashlib
import json
import traceback
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
WF = (
    ARCH
    / "docs/implementation/m2/predicate-matching-reference-selection-v1/reference/workflows_model.v1.py"
)
ID = (
    ARCH
    / "docs/implementation/m2/stage-meta-reference-selection-v1/reference/identity_model.py"
)
SCHEMA = ARCH / "docs/coop/design-corrections/foundation/identity-schemas.v3.json"
OUT = Path("/tmp/opensip-implementation/m2-grok-import-payload-boundary-29/review/probes")


def load_selected_registry():
    tree = ast.parse(WF.read_bytes())
    names = {"PAYLOAD_REGISTRY", "registry_row"}
    body = [
        n
        for n in tree.body
        if (isinstance(n, ast.Assign) and any(getattr(t, "id", None) in names for t in n.targets))
        or (isinstance(n, ast.FunctionDef) and n.name in names)
    ]
    env = {}
    exec(compile(ast.Module(body=body, type_ignores=[]), str(WF), "exec"), env)
    return env["PAYLOAD_REGISTRY"], env["registry_row"]


def identity_import_rows():
    schema = json.loads(SCHEMA.read_bytes())
    return schema["x-opensip-payload-registry"]["classes"]["import"]["rows"]


def call(fn, kind, domain):
    try:
        value = fn(kind, domain)
        return {"result": "ok", "value": None if value is None else "row", "owner": None if value is None else value.get("owner")}
    except Exception as exc:
        return {
            "result": type(exc).__name__,
            "message": str(exc),
            "unhashable": "unhashable" in str(exc),
        }


def identity_branch(registry_row, rows, kind, domain):
    try:
        owner = registry_row(kind, domain)
        declared = rows.get(str(kind) + "|" + str(domain))
        if owner is None or declared is None:
            return {"result": "PAYLOAD_IMPORT_UNREGISTERED", "reprKey": str([kind, domain])}
        if owner["schemaDocument"] != declared["document"] or owner["selector"] != declared["selector"]:
            return {"result": "PAYLOAD_IMPORT_REGISTRY_DRIFT", "reprKey": str([kind, domain])}
        return {"result": "row", "owner": owner["owner"]}
    except Exception as exc:
        return {"result": type(exc).__name__, "message": str(exc), "unhashable": "unhashable" in str(exc)}


def guarded(registry):
    def registry_row(kind, payload_domain):
        if type(kind) is not str or type(payload_domain) is not str:
            return None
        return registry.get((kind, payload_domain))

    return registry_row


def main():
    registry, registry_row = load_selected_registry()
    rows = identity_import_rows()
    assert len(registry) == 5 and len(rows) == 5
    cases = [
        ("valid-runtime", "runtime", "workflow.import-payload.runtime.v1"),
        ("valid-test", "test", "workflow.import-payload.test.v1"),
        ("valid-history", "history", "workflow.import-payload.history.v1"),
        ("valid-dependency", "dependency", "native.import-payload.dependency-source.v1"),
        ("valid-prepared", "prepared", "native.import-payload.prepared-output.v1"),
        ("unknown-strings", "runtime", "workflow.import-payload.nope.v1"),
        ("domain-list", "runtime", []),
        ("domain-object", "runtime", {}),
        ("domain-nested-list", "runtime", [[]]),
        ("kind-list", [], "workflow.import-payload.runtime.v1"),
        ("kind-object", {}, "workflow.import-payload.runtime.v1"),
        ("both-list", [], []),
        ("domain-none", "runtime", None),
        ("kind-none", None, "workflow.import-payload.runtime.v1"),
        ("domain-true", "runtime", True),
        ("domain-false", "runtime", False),
        ("domain-int-1", "runtime", 1),
        ("domain-int-0", "runtime", 0),
        ("kind-true", True, "workflow.import-payload.runtime.v1"),
        ("kind-int-1", 1, "workflow.import-payload.runtime.v1"),
        ("bool-pair", True, True),
        ("int-pair", 1, 1),
        ("empty-strings", "", ""),
        ("domain-missing-via-none-kind-runtime", "runtime", None),
    ]
    current = []
    proposed = []
    identity_now = []
    identity_after = []
    g = guarded(registry)
    for name, kind, domain in cases:
        current.append({"name": name, "kindType": type(kind).__name__, "domainType": type(domain).__name__, **call(registry_row, kind, domain)})
        proposed.append({"name": name, **call(g, kind, domain)})
        identity_now.append({"name": name, **identity_branch(registry_row, rows, kind, domain)})
        identity_after.append({"name": name, **identity_branch(g, rows, kind, domain)})

    # bool/int cannot admit any of the five string-string rows
    admit = []
    for kind in (True, False, 0, 1, None):
        for domain in (True, False, 0, 1, None):
            got = registry.get((kind, domain))
            if got is not None:
                admit.append({"kind": repr(kind), "domain": repr(domain), "owner": got["owner"]})

    # str() declared-key collision
    collisions = []
    for sample in ([], {}, True, False, 1, 0, None, [[]]):
        key = str("runtime") + "|" + str(sample)
        if key in rows:
            collisions.append(key)
        key2 = str(sample) + "|" + str("workflow.import-payload.runtime.v1")
        if key2 in rows:
            collisions.append(key2)

    # build_import residual: after None, string concat
    build_concat = []
    for domain in ([], {}, True, "missing"):
        try:
            if g("runtime", domain) is None:
                if not any(pd == domain for _, pd in registry):
                    _ = "no registered schema for " + domain
            build_concat.append({"domainType": type(domain).__name__, "result": "named"})
        except Exception as exc:
            build_concat.append({"domainType": type(domain).__name__, "result": type(exc).__name__, "message": str(exc)})

    report = {
        "selectedWorkflows": {"path": str(WF.relative_to(ARCH)), "bytes": WF.stat().st_size, "sha256": hashlib.sha256(WF.read_bytes()).hexdigest()},
        "selectedIdentity": {"path": str(ID.relative_to(ARCH)), "bytes": ID.stat().st_size, "sha256": hashlib.sha256(ID.read_bytes()).hexdigest()},
        "identitySchema": {"path": str(SCHEMA.relative_to(ARCH)), "bytes": SCHEMA.stat().st_size, "sha256": hashlib.sha256(SCHEMA.read_bytes()).hexdigest()},
        "registryRows": 5,
        "identityImportRows": 5,
        "currentRegistryRow": current,
        "proposedRegistryRow": proposed,
        "identityBranchCurrent": identity_now,
        "identityBranchAfterGuard": identity_after,
        "boolIntAdmittedRows": admit,
        "strDeclaredKeyCollisions": collisions,
        "buildImportConcatAfterGuard": build_concat,
        "validStillRowsAfterGuard": [c["name"] for c in proposed if c["name"].startswith("valid-") and c.get("value") == "row"],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "probe-results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("registryRows", "boolIntAdmittedRows", "strDeclaredKeyCollisions", "validStillRowsAfterGuard")}, indent=2))
    print("unhashable current", [c["name"] for c in current if c.get("unhashable")])
    print("identity current unhashable", [c["name"] for c in identity_now if c.get("unhashable")])
    print("identity after named", [(c["name"], c["result"]) for c in identity_after if not c["name"].startswith("valid-")])


if __name__ == "__main__":
    main()
