"""Reachable format names in bundled 2020-12 meta-schema used by check_schema.
Also compare default FORMAT_CHECKER vs format_checker=None.
"""
from __future__ import annotations

import importlib.metadata
import json
import sys

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
from jsonschema_specifications import REGISTRY as SPECIFICATIONS


def walk_formats(node, path, acc):
    if isinstance(node, dict):
        if isinstance(node.get("format"), str):
            acc.append({"path": path, "format": node["format"], "type": node.get("type")})
        for k, v in node.items():
            walk_formats(v, path + "/" + str(k).replace("/", "~1"), acc)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk_formats(v, path + f"/{i}", acc)


def result(fn):
    try:
        fn()
        return {"ok": True}
    except SchemaError as e:
        return {"ok": False, "kind": "SchemaError", "message": str(e)[:200]}
    except Exception as e:
        return {"ok": False, "kind": type(e).__name__, "message": str(e)[:200]}


def check_default(doc):
    return result(lambda: Draft202012Validator.check_schema(doc))


def check_none(doc):
    return result(lambda: Draft202012Validator.check_schema(doc, format_checker=None))


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
    graph = []
    for uri in sorted(SPECIFICATIONS):
        u = str(uri)
        if "/draft/2020-12" not in u:
            continue
        contents = SPECIFICATIONS.contents(uri)
        acc = []
        walk_formats(contents, "$", acc)
        voc = contents.get("$vocabulary") if isinstance(contents, dict) else None
        graph.append({"id": u, "vocabulary": voc, "formats": acc})

    reachable = sorted({f["format"] for g in graph for f in g["formats"]})
    meta_voc = Draft202012Validator.META_SCHEMA.get("$vocabulary")
    included = Draft202012Validator.META_SCHEMA.get("allOf")

    cases = []
    docs = [
        ("invalid-pattern-unclosed", base(pattern="(")),
        ("python-named-group-pattern", base(pattern="(?P<name>.)")),
        ("patternProperties-invalid-key", base(patternProperties={"(": {"type": "string"}})),
        ("patternProperties-valid-key", base(patternProperties={"^foo$": {"type": "string"}})),
        ("id-not-uri", base(**{"$id": "not a uri"})),
        ("id-fragment-extra", base(**{"$id": "https://example.invalid/x#foo"})),
        ("id-empty-fragment-ok-pattern", base(**{"$id": "https://example.invalid/x#"})),
        ("schema-not-uri", {**base(), "$schema": "https://json-schema.org/draft/2020-12/schema"}),
        ("ref-remote", base(**{"$ref": "https://example.invalid/schema.json"})),
        ("format-email-on-string", base(type="string", format="email")),
        ("unknown-keyword", base(fooBar=1)),
        ("nested-bool", base(additionalProperties=False)),
    ]
    for name, doc in docs:
        cases.append(
            {
                "name": name,
                "defaultFormatChecker": check_default(doc),
                "formatCheckerNone": check_none(doc),
            }
        )

    out = {
        "python": sys.version.split()[0],
        "jsonschema": importlib.metadata.version("jsonschema"),
        "jsonschema_specifications": importlib.metadata.version("jsonschema-specifications"),
        "metaSchemaId": Draft202012Validator.META_SCHEMA.get("$id"),
        "metaSchemaVocabulary": meta_voc,
        "formatAssertionVocabularyIncluded": bool(
            meta_voc and meta_voc.get("https://json-schema.org/draft/2020-12/vocab/format-assertion")
        ),
        "formatAnnotationVocabularyIncluded": bool(
            meta_voc and meta_voc.get("https://json-schema.org/draft/2020-12/vocab/format-annotation")
        ),
        "allOf": included,
        "defaultFormatCheckerNames": sorted(Draft202012Validator.FORMAT_CHECKER.checkers),
        "formatsInBundled2020_12Graph": reachable,
        "graph": graph,
        "formatKeywordNoopsWhenCheckerNone": True,
        "cases": cases,
        "scope": "Bundled 2020-12 meta-schema format reachability and format_checker=None vs default; no network; not identity schema.rs.",
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
