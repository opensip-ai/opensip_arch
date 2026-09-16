"""Selected Draft202012Validator.check_schema corner cases.
Python 3.12 / jsonschema 4.25.1. Not identity schema.rs. No network.
"""
from __future__ import annotations

import importlib.metadata
import json
import sys
import traceback
import types
import unicodedata

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


def outcome(fn):
    try:
        fn()
        return {"ok": True}
    except SchemaError as e:
        msg = str(e)
        return {"ok": False, "kind": "SchemaError", "message": msg[:240]}
    except Exception as e:
        return {"ok": False, "kind": type(e).__name__, "message": str(e)[:240]}


def check(doc):
    return outcome(lambda: Draft202012Validator.check_schema(doc))


def base(**extra):
    d = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "x-opensip-stage-output": {
            "schemaVersion": 1,
            "operation": "analyze",
            "outputDomains": [],
        },
    }
    d.update(extra)
    return d


def main() -> None:
    checker = Draft202012Validator.FORMAT_CHECKER
    names = sorted(checker.checkers)
    optional = {}
    for pkg in [
        "rfc3987",
        "rfc3986_validator",
        "rfc3987_syntax",
        "fqdn",
        "idna",
        "rfc3339_validator",
        "jsonpointer",
        "uri_template",
        "isoduration",
        "webcolors",
    ]:
        try:
            __import__(pkg)
            optional[pkg] = True
        except ImportError:
            optional[pkg] = False

    rows = []

    def add(name, doc, **meta):
        r = {"name": name, "result": check(doc)}
        r.update(meta)
        rows.append(r)

    add("unknown-x-opensip-stage-output", base())
    add("unknown-keyword-fooBar", base(fooBar={"hello": 1}))
    add("remote-http-ref", base(**{"$ref": "https://example.invalid/schema.json"}))
    add("remote-http-ref-in-properties", base(properties={"x": {"$ref": "https://example.invalid/x"}}))
    add("invalid-pattern-unclosed", base(pattern="("))
    add("valid-pattern-literal", base(pattern="^foo$"))
    add("python-named-group-pattern", base(pattern="(?P<name>.)"))
    add("id-not-uri-reference-looking", base(**{"$id": "not-an-email"}))
    add("id-spaces", base(**{"$id": "not a uri"}))
    add("nested-bool-additionalProperties-false", base(additionalProperties=False))
    add("nested-bool-items-true", base(type="array", items=True))
    add("nested-bool-defs-false", base(**{"$defs": {"deny": False}}))
    add("root-bool-true", True)
    add("root-bool-false", False)
    add("format-email-on-string-schema", base(type="string", format="email"))
    add("format-unknown-name", base(type="string", format="not-a-registered-format"))
    add("exclusiveMaximum-number", {**base(), "type": "number", "exclusiveMaximum": 3})
    add("multipleOf", {**base(), "type": "number", "multipleOf": 2})
    add("unevaluatedProperties", base(unevaluatedProperties=False))
    add("dependentRequired", base(dependentRequired={"a": ["b"]}))
    add("comment-keyword", base(**{"$comment": "hello"}))
    add("draft07-schema-url", {**base(), "$schema": "http://json-schema.org/draft-07/schema#"})
    add("missing-schema-url", {k: v for k, v in base().items() if k != "$schema"})

    pretty = json.dumps(base(), indent=2)
    rows.append(
        {
            "name": "pretty-json-loads-then-check_schema",
            "prettyBytes": len(pretty.encode()),
            "canonicalEq": json.dumps(json.loads(pretty), separators=(",", ":")) == pretty,
            "result": outcome(lambda: Draft202012Validator.check_schema(json.loads(pretty))),
        }
    )

    # format: regex uses Python re, not ECMA-262. Nested in meta-schema via pattern.
    rows.append(
        {
            "name": "pattern-python-only-lookbehind",
            "result": check(base(pattern="(?<=a)b")),
        }
    )

    out = {
        "python": sys.version.split()[0],
        "unicode": unicodedata.unidata_version,
        "jsonschema": importlib.metadata.version("jsonschema"),
        "jsonschema_specifications": importlib.metadata.version("jsonschema-specifications"),
        "referencing": importlib.metadata.version("referencing"),
        "formatCheckers": names,
        "optionalFormatPackagesPresent": optional,
        "uriFormatRegistered": "uri" in names,
        "uriReferenceFormatRegistered": "uri-reference" in names,
        "hostnameFormatRegistered": "hostname" in names,
        "cases": rows,
        "scope": "Local jsonschema 4.25.1 Draft202012Validator.check_schema; no network; not identity schema.rs; not admit_stage_output_schema tree/digest joins.",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
