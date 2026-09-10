#!/usr/bin/env python3
"""Specification-first law inventory for the selected TS Run.

Does not exclude description/note/standing by key name. Classifies textual
clauses by CONTENT. Follows $ref (including sibling keywords), applicators,
and nested object/array shapes. Dedup key includes document identity.
Unrecognized applicable predicates are kept, never dropped by a family list.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v7/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v13/subject")
sys.path.insert(0, str(OUT))

from derive_conditions import classify_object, collect_selected_docs  # noqa: E402
from helpers.store import load_export  # noqa: E402
from helpers import kit_schemas  # noqa: E402

MUST_RE = re.compile(
    r"\b(MUST(?:\s+NOT)?|REQUIRED|REQUIRES|refuses?|forbidden|never |always |"
    r"equals |IMPLICATION|shall |total over|not-applicable|closed and|"
    r"exactly (?:the|one|one item)|canonical set)\b",
    re.I,
)
EXPLAIN_RE = re.compile(
    r"\b(illustration|example encoding|historical bytes|provenance only|"
    r"review narrative|not an oracle|advisory A-|standing is governed)\b",
    re.I,
)
TEXT_KEYS = {
    "description",
    "note",
    "standing",
    "why",
    "whyItIsNeeded",
    "whyThisWasNeeded",
    "comment",
    "law",
    "rule",
    "classLaw",
}


def pointer(parts: list) -> str:
    out = ""
    for p in parts:
        s = str(p).replace("~", "~0").replace("/", "~1")
        out += "/" + s
    return out or "/"


def kit_rel(p: Path) -> str:
    s = p.as_posix()
    return s.split("/subject/", 1)[-1] if "/subject/" in s else s


def classify_text(key: str, text: str) -> str:
    """Content-based, not key-name-based. JSON Schema 'description' may still be mandatory."""
    t = str(text or "")
    if not t.strip():
        return "empty"
    has_must = bool(MUST_RE.search(t))
    has_explain = bool(EXPLAIN_RE.search(t))
    if has_must and not has_explain:
        return "mandatory-candidate"
    if has_must and has_explain:
        return "mixed-mandatory-and-explanatory"
    if has_explain:
        return "explanatory"
    if key in {"standing", "law", "rule"} and len(t) > 80:
        return "mandatory-candidate"
    if key in {"why", "whyItIsNeeded", "whyThisWasNeeded", "examples"}:
        return "explanatory"
    return "annotation-text"


def walk_schema(obj, parts, kit_path, sid, out, seen_refs: set):
    if isinstance(obj, dict):
        # $ref with or without sibling keywords
        ref = obj.get("$ref")
        if isinstance(ref, str):
            out.append(
                {
                    "document": kit_path,
                    "schemaId": sid,
                    "pointer": pointer(parts + ["$ref"]),
                    "kind": "ref",
                    "ref": ref,
                    "siblingKeywords": sorted(k for k in obj if k != "$ref"),
                }
            )
        for k, v in obj.items():
            p = parts + [k]
            ptr = pointer(p)
            if str(k).startswith("x-opensip-"):
                out.append(
                    {
                        "document": kit_path,
                        "schemaId": sid,
                        "pointer": ptr,
                        "kind": "annotation",
                        "keyword": k,
                        "valueType": type(v).__name__,
                    }
                )
            if k in TEXT_KEYS and isinstance(v, str):
                cls = classify_text(k, v)
                out.append(
                    {
                        "document": kit_path,
                        "schemaId": sid,
                        "pointer": ptr,
                        "kind": "textual-clause",
                        "textKey": k,
                        "classification": cls,
                        "text": v if len(v) < 4000 else v[:4000] + "…",
                    }
                )
            if k in {"allOf", "oneOf", "anyOf", "if", "then", "else", "not", "properties", "items", "$defs", "dependentSchemas", "prefixItems"}:
                out.append(
                    {
                        "document": kit_path,
                        "schemaId": sid,
                        "pointer": ptr,
                        "kind": "applicator",
                        "keyword": k,
                    }
                )
            walk_schema(v, p, kit_path, sid, out, seen_refs)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk_schema(v, parts + [i], kit_path, sid, out, seen_refs)


def bind_def_to_instances(st, defn: str) -> list[str]:
    out = []
    for ident, obj in st.objects.items():
        cls = classify_object(ident, obj)
        if not cls:
            continue
        sid, d = cls
        if d == defn:
            out.append(ident)
        elif d is None and defn is None:
            out.append(ident)
    # prefix map
    for pref, name in kit_schemas.PREFIX_TO_IDENTITY_DEF.items():
        if name == defn:
            out.extend([i for i in st.objects if i.startswith(pref + ":")])
    # unique
    seen = set()
    uniq = []
    for i in out:
        if i not in seen:
            seen.add(i)
            uniq.append(i)
    return uniq


def defn_from_pointer(ptr: str) -> tuple[str | None, str | None]:
    """Extract $defs/NAME and properties/FIELD from a pointer."""
    segs = [s.replace("~1", "/") for s in ptr.split("/") if s]
    defn = None
    field = None
    if "$defs" in segs:
        j = segs.index("$defs")
        if j + 1 < len(segs):
            defn = segs[j + 1]
    if "properties" in segs:
        j = segs.index("properties")
        if j + 1 < len(segs):
            field = segs[j + 1]
    return defn, field


PROSE_DOCS = [
    ("docs/v2/contracts/product-v1/native-evidence.md", "native-evidence.md"),
    ("docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md", "composition-v3"),
    ("docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md", "atom-v1"),
    ("docs/coop/design-corrections/foundation/enumeration-contract.v1.md", "enumeration-v1"),
    ("docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md", "execution-inputs-v1"),
]


def walk_prose(rel: str, label: str, out: list) -> None:
    p = KIT / rel
    if not p.exists():
        out.append(
            {
                "document": rel,
                "pointer": "/",
                "kind": "input-custody-missing",
                "classification": "mandatory-candidate",
                "text": f"missing kit file {rel}",
            }
        )
        return
    text = p.read_text()
    # section headings as clause anchors; keep the following paragraph
    lines = text.splitlines()
    buf = []
    heading = "/"
    for i, line in enumerate(lines):
        if line.startswith("#"):
            if buf:
                block = "\n".join(buf).strip()
                if block:
                    cls = classify_text("prose", block)
                    out.append(
                        {
                            "document": rel,
                            "schemaId": label,
                            "pointer": heading,
                            "kind": "prose-clause",
                            "classification": cls,
                            "text": block if len(block) < 4000 else block[:4000] + "…",
                        }
                    )
            heading = "/" + re.sub(r"^#+\s*", "", line).strip()[:120]
            buf = []
        else:
            buf.append(line)
    if buf:
        block = "\n".join(buf).strip()
        if block:
            cls = classify_text("prose", block)
            out.append(
                {
                    "document": rel,
                    "schemaId": label,
                    "pointer": heading,
                    "kind": "prose-clause",
                    "classification": cls,
                    "text": block if len(block) < 4000 else block[:4000] + "…",
                }
            )


def main() -> int:
    st = load_export(json.loads((OUT / "runs" / "ts.store.json").read_text()))
    docs = collect_selected_docs(st)
    # incorporated prose is part of the selected closure, not optional
    clauses = []
    for sid, p in sorted(docs.items(), key=lambda kv: str(kv[1])):
        rel = kit_rel(p)
        data = json.loads(p.read_text())
        walk_schema(data, [], rel, data.get("$id") or sid, clauses, set())
    for rel, label in PROSE_DOCS:
        walk_prose(rel, label, clauses)

    # Bind to instances. Unbound mandatory clauses remain required with instance UNBOUND (OPEN).
    occ = []
    classified = [(i, o, classify_object(i, o)) for i, o in st.objects.items()]

    def add_occ(clause, instance, field, why):
        occ.append(
            {
                "document": clause.get("document"),
                "condition": clause.get("pointer"),
                "instance": instance,
                "field": field,
                "kind": clause.get("kind"),
                "classification": clause.get("classification"),
                "bindWhy": why,
                "keyword": clause.get("keyword") or clause.get("textKey"),
            }
        )

    for clause in clauses:
        kind = clause.get("kind")
        cls = clause.get("classification")
        ptr = clause.get("pointer") or "/"
        doc = clause.get("document")
        if kind == "textual-clause":
            defn, field = defn_from_pointer(ptr)
            field = field or (ptr.rsplit("/", 1)[-1] if ptr else "/")
            insts = bind_def_to_instances(st, defn) if defn else []
            if insts:
                for ident in insts:
                    add_occ(clause, ident, field, f"schema $defs/{defn} × retained instance")
            else:
                add_occ(clause, "UNBOUND", field, "no retained instance of this $defs name")
            continue
        if kind == "prose-clause":
            # bind mandatory prose to the selected Run; explanatory stays documented
            add_occ(clause, st.meta.get("runId") or "UNBOUND", "/", "selected Run as prose subject")
            continue
        if kind == "annotation":
            defn, field = defn_from_pointer(ptr)
            field = field or clause.get("keyword") or "/"
            insts = bind_def_to_instances(st, defn) if defn else []
            if insts:
                for ident in insts:
                    add_occ(clause, ident, field, "x-opensip annotation on retained def")
            else:
                # document-level registries: keep one occurrence per selected Run
                add_occ(clause, st.meta.get("runId") or "UNBOUND", field, "document-level or unbound annotation")
            continue
        if kind in {"ref", "applicator"}:
            # structure of the selected schema; not an instance comparison unless mandatory text
            add_occ(clause, "SCHEMA", ptr.rsplit("/", 1)[-1], "schema structure of selected document")
            continue

    # Dedup WITH document identity
    seen = set()
    uniq = []
    for o in occ:
        k = (o.get("document") or "", o.get("condition") or "", str(o.get("instance")), str(o.get("field")))
        if k in seen:
            continue
        seen.add(k)
        uniq.append(o)

    mandatory = [
        o
        for o in uniq
        if o.get("classification") in {"mandatory-candidate", "mixed-mandatory-and-explanatory"}
        or o.get("kind") in {"annotation", "textual-clause", "prose-clause"}
    ]

    dest = OUT / "inventory" / "specification-inventory.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        json.dumps(
            {
                "standing": (
                    "Specification-first inventory. Descriptions are not excluded by key name. "
                    "Dedup is (document, pointer, instance, field). Unrecognized clauses are kept."
                ),
                "selectedDocuments": {k: str(v) for k, v in docs.items()},
                "proseDocuments": [rel for rel, _ in PROSE_DOCS],
                "clauseCount": len(clauses),
                "occurrenceCount": len(uniq),
                "mandatoryOccurrenceCount": len(mandatory),
                "unboundMandatory": sum(
                    1
                    for o in mandatory
                    if o.get("instance") in {"UNBOUND", "SCHEMA"}
                    and o.get("classification") in {"mandatory-candidate", "mixed-mandatory-and-explanatory"}
                ),
                "clauses": clauses,
                "occurrences": uniq,
            },
            indent=2,
        )
        + "\n"
    )
    (OUT / "required-occurrences.json").write_text(
        json.dumps(
            {
                "standing": "Required (document, pointer, instance, field) from specification inventory. Document identity is part of the key.",
                "count": len(uniq),
                "occurrences": [
                    {
                        "kitPath": o.get("document"),
                        "document": o.get("document"),
                        "condition": o.get("condition"),
                        "instance": o.get("instance"),
                        "field": o.get("field"),
                        "kind": o.get("kind"),
                        "classification": o.get("classification"),
                        "bindWhy": o.get("bindWhy"),
                    }
                    for o in uniq
                ],
            },
            indent=2,
        )
        + "\n"
    )
    print("docs", len(docs), "clauses", len(clauses), "occ", len(uniq), "mandatory", len(mandatory))
    return 0


if __name__ == "__main__":
    sys.exit(main())
