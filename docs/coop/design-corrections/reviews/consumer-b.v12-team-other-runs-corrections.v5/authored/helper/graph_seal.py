"""Shared sealing of a minimal complete Run graph around a language-specific context."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from helper.body_identity import body_identity, body_language_version, framed_token_stream, l0_payload, language_version_bytes
from helper.canonical import C
from helper.cap_manifest import capability_manifest_id
from helper.evaluator import flatten, walk_predicate
from helper.identity import parse_h_frame, typed_id
from helper.schema_admit import validate_against
from helper.store import Store

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-other-runs-corrections.v5/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-other-runs-corrections.v5/subject")
IDENT = "docs/coop/design-corrections/foundation/identity-schemas.v3.json"
NATIVE = "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
REL = "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"
POL2 = "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json"
POL1 = "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json"
ENUM = "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json"
EMIS = "docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json"
EXEC = "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json"
SINV = "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json"


def sort_set(xs):
    return sorted(xs, key=lambda x: C(x))


def make_closure(store: Store, kind: str, platform="macos-aarch64", extra_files=None):
    from helper.component_manifest import component_manifest_body, encode_manifest_body, stored_sha256

    stub = store.put_raw(b"stub-" + kind.encode(), label=f"bin-{kind}")
    tree = extra_files or []
    tree = sorted(
        tree + [{"path": f"bin/{kind}", "sha256": stub, "bytes": 5 + len(kind)}],
        key=lambda r: r["path"].encode(),
    )
    body_obj = component_manifest_body(
        closure_kind=kind,
        semantic_version="1.0.0",
        platform=platform,
        tree=tree,
    )
    body_bytes = encode_manifest_body(body_obj)
    man_d = store.put_raw(body_bytes, label=f"manifest-{kind}")
    assert man_d == stored_sha256(body_bytes)
    rec = {
        "schemaVersion": 2,
        "kind": kind,
        "manifestDigest": man_d,
        "tree": tree,
        "semanticVersion": "1.0.0",
        "protocolMajor": 1,
        "platform": platform,
    }
    return store.put_h("closure", rec, label=f"closure-{kind}"), rec
