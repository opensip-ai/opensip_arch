"""Probes for stage20 correction. Not product code."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import traceback
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
C_PATH = (
    ARCH
    / "docs/implementation/m2/exact-schema-profile-selection-v1/reference/canonical.py"
)
ID_PATH = (
    ARCH
    / "docs/implementation/m2/recognition-derived-reference-selection-v1/reference/identity_model.py"
)
SCHEMA = Path("/Users/sb/code/opensip-ai/opensip/schemas/sources/identity-v3.schema.json")
HEX = "0" * 64


def load_c():
    spec = importlib.util.spec_from_file_location("canon_probe", C_PATH)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def catch(fn):
    try:
        v = fn()
        return {"ok": True, "value": v if not isinstance(v, (bytes, bytearray)) else v.decode()}
    except Exception as e:
        return {"ok": False, "type": type(e).__name__, "msg": str(e)[:300]}


def schema_doc(pretty=False, extra=None):
    doc = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "x-opensip-stage-output": {
            "schemaVersion": 1,
            "operation": "analyze",
            "outputDomains": [],
        },
    }
    if extra:
        doc.update(extra)
    if pretty:
        return json.dumps(doc, indent=2).encode()
    C = load_c()
    return C.canonical(doc)


def admit(C, spec, producer, raw):
    # local copy of selected 735-761 using this C
    import re
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError

    STAGE_OUTPUT_INTERFACE_DIRECTORY = "opensip-interface/stage-output/"
    STAGE_OUTPUT_DECLARATION = "x-opensip-stage-output"
    _STAGE_OPERATION_SEGMENT = re.compile(r"[a-z0-9][a-z0-9._-]{0,127}")

    def stage_output_schema_member_path(operation):
        if type(operation) is not str or _STAGE_OPERATION_SEGMENT.fullmatch(operation) is None:
            raise C.AdmissionError("STAGE_OUTPUT_SCHEMA_OPERATION_NOT_A_PATH_SEGMENT:" + repr(operation))
        return STAGE_OUTPUT_INTERFACE_DIRECTORY + operation + ".schema.json"

    path = stage_output_schema_member_path(spec["operation"])
    members = [row for row in producer["tree"] if row["path"] == path]
    if not members:
        raise C.AdmissionError("STAGE_OUTPUT_SCHEMA_UNREGISTERED:" + path)
    if members[0]["sha256"] != spec["outputSchemaDigest"]:
        raise C.AdmissionError("STAGE_OUTPUT_SCHEMA_REGISTRATION_MISMATCH:" + path)
    if type(raw) is not bytes or hashlib.sha256(raw).hexdigest() != spec["outputSchemaDigest"]:
        raise C.AdmissionError("BLOB_DIGEST")
    try:
        document = C.parse(raw)
    except (C.AdmissionError, ValueError) as exc:
        raise C.AdmissionError("STAGE_OUTPUT_SCHEMA_DOCUMENT_INVALID:" + path) from exc
    if type(document) is not dict or document.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise C.AdmissionError("STAGE_OUTPUT_SCHEMA_DOCUMENT_INVALID:" + path)
    try:
        Draft202012Validator.check_schema(document)
    except SchemaError as exc:
        raise C.AdmissionError("STAGE_OUTPUT_SCHEMA_DOCUMENT_INVALID:" + path) from exc
    declared = {
        "schemaVersion": 1,
        "operation": spec["operation"],
        "outputDomains": spec["outputDomains"],
    }
    if not C.equal_typed(document.get(STAGE_OUTPUT_DECLARATION), declared):
        raise C.AdmissionError("STAGE_OUTPUT_SCHEMA_DECLARATION_MISMATCH:" + path)
    return document


def main():
    C = load_c()
    out = {}

    pretty = schema_doc(pretty=True)
    compact = C.canonical(json.loads(pretty))
    out["pretty_ne_canonical"] = pretty != compact
    out["pretty_parse_ok"] = catch(lambda: C.parse(pretty))["ok"]
    out["pretty_canonical_eq_raw"] = catch(lambda: C.canonical(C.parse(pretty)) == pretty)["value"]
    spec = {
        "operation": "analyze",
        "outputDomains": [],
        "outputSchemaDigest": hashlib.sha256(pretty).hexdigest(),
    }
    producer = {
        "tree": [
            {
                "path": "opensip-interface/stage-output/analyze.schema.json",
                "sha256": spec["outputSchemaDigest"],
                "bytes": len(pretty),
            }
        ]
    }
    out["pretty_admit"] = catch(lambda: admit(C, spec, producer, pretty))
    compact_spec = dict(spec, outputSchemaDigest=hashlib.sha256(compact).hexdigest())
    compact_prod = {
        "tree": [
            {
                "path": "opensip-interface/stage-output/analyze.schema.json",
                "sha256": compact_spec["outputSchemaDigest"],
                "bytes": len(compact),
            }
        ]
    }
    out["compact_admit"] = catch(lambda: admit(C, compact_spec, compact_prod, compact))
    padded_int = b'{ "$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "x-opensip-stage-output": { "schemaVersion": 01, "operation": "analyze", "outputDomains": [] } }'
    out["leading_zero_int_parse"] = catch(lambda: C.parse(padded_int))
    float_raw = b'{ "$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "x-opensip-stage-output": { "schemaVersion": 1.0, "operation": "analyze", "outputDomains": [] } }'
    out["float_parse"] = catch(lambda: C.parse(float_raw))

    # (2) ordered uniqueness vs helper members[0]
    spec_src = ID_PATH.read_text()
    g = {"C": C}
    start = spec_src.index("def ordered(value,path=()):")
    end = spec_src.index("ROOT_ORDER_PATH=")
    exec(spec_src[start:end], g)
    ordered = g["ordered"]

    dup_tree = {
        "tree": [
            {"path": "opensip-interface/stage-output/analyze.schema.json", "sha256": "a" * 64, "bytes": 1},
            {"path": "opensip-interface/stage-output/analyze.schema.json", "sha256": "b" * 64, "bytes": 1},
        ]
    }
    out["ordered_dup_tree"] = catch(lambda: ordered(dup_tree, ("tree",)))
    # identifier: validate + ordered on full closure
    schema = json.loads(SCHEMA.read_text())
    # uniqueItems allows different objects with same path
    from jsonschema import Draft202012Validator

    blob = {"path": "opensip-interface/stage-output/analyze.schema.json", "sha256": HEX, "bytes": 1}

    def closure(tree):
        return {
            "schemaVersion": 2,
            "kind": "provider",
            "manifestDigest": HEX,
            "tree": tree,
            "semanticVersion": "1.0.0",
            "protocolMajor": 3,
            "platform": "any",
        }

    # two same path different sha - uniqueItems?
    t1 = [
        {"path": "a.json", "sha256": "a" * 64, "bytes": 1},
        {"path": "a.json", "sha256": "b" * 64, "bytes": 1},
    ]
    # identity Blob may need more fields - skip full schema if fail
    out["schema_uniqueItems_same_path_diff_sha"] = catch(
        lambda: Draft202012Validator(schema["$defs"]["closure"]["properties"]["tree"]).validate(t1)
    )
    out["ordered_same_path_diff_sha"] = catch(lambda: ordered({"tree": t1}, ("tree",)))

    # helper members[0] with dup tree: first sha wins
    spec_d = {
        "operation": "analyze",
        "outputDomains": [],
        "outputSchemaDigest": "a" * 64,
    }
    raw_dummy = b"{}"  # will fail later if we get past members[0]
    prod_dup = {"tree": t1}
    # path won't match a.json vs analyze.schema.json
    prod_dup2 = {
        "tree": [
            {
                "path": "opensip-interface/stage-output/analyze.schema.json",
                "sha256": "a" * 64,
                "bytes": 1,
            },
            {
                "path": "opensip-interface/stage-output/analyze.schema.json",
                "sha256": "b" * 64,
                "bytes": 1,
            },
        ]
    }
    out["helper_members0_first_sha"] = catch(lambda: admit(C, spec_d, prod_dup2, b"not-the-digest"))
    spec_b = dict(spec_d, outputSchemaDigest="b" * 64)
    out["helper_members0_second_sha_unreached"] = catch(
        lambda: admit(C, spec_b, prod_dup2, b"not-the-digest")
    )

    # (4) check_schema
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError

    def cs(doc):
        Draft202012Validator.check_schema(doc)
        return True

    base = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "x-opensip-stage-output": {"schemaVersion": 1, "operation": "analyze", "outputDomains": []},
    }
    out["unknown_keyword"] = catch(lambda: cs(base))
    out["remote_ref"] = catch(
        lambda: cs({**base, "$ref": "https://example.invalid/schema.json"})
    )
    out["bad_regex"] = catch(lambda: cs({**base, "type": "string", "pattern": "("}))
    out["bad_email_format_on_schema_id"] = catch(
        lambda: cs({**base, "$id": "not-an-email"})
    )
    # $id format uri-reference typically
    out["format_checker_names"] = sorted(Draft202012Validator.FORMAT_CHECKER.checkers)
    out["uri_in_format_checker"] = "uri" in Draft202012Validator.FORMAT_CHECKER.checkers
    out["regex_in_format_checker"] = "regex" in Draft202012Validator.FORMAT_CHECKER.checkers

    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
