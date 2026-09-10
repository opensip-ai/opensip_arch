#!/usr/bin/env python
"""Structural (prose-stripped) diff of every changed schema/registry document,
v16 -> v17, to separate genuine normative change from wording.

Reports, per document:
  - the full set of JSON pointers whose STRUCTURAL value changed
  - every enum that gained or lost a member (vocabulary growth/shrink)
  - every change to type / required / additionalProperties / const / pattern
    / bounds / $ref  (the widening-relevant keywords)

Prose keys stripped: description, title, $comment, summary, note, rationale,
examples, and the x-opensip-* annotation blocks are kept STRUCTURAL because in
this contract set they carry normative law (they are cited as authorities), but
their own description strings are stripped.
"""
import json
import os
import sys

V16 = "/tmp/opensip-design-corrections/post-reset-review.v17/copies/v16-extract"
V17 = "/tmp/opensip-design-corrections/candidate-subject.v17"

PROSE = {"description", "title", "$comment", "summary", "note", "rationale",
         "examples", "example", "readOn", "claim", "standing", "purpose"}

WIDENING_KEYS = {"type", "required", "additionalProperties", "const", "enum",
                 "pattern", "minimum", "maximum", "minItems", "maxItems",
                 "minLength", "maxLength", "$ref", "oneOf", "anyOf", "allOf",
                 "not", "uniqueItems", "format", "multipleOf",
                 "exclusiveMinimum", "exclusiveMaximum", "propertyNames",
                 "patternProperties", "dependentRequired", "if", "then",
                 "else", "prefixItems", "items", "contains"}

DOCS = [
    "docs/coop/design-corrections/workflows/schemas/common.schema.json",
    "docs/coop/design-corrections/workflows/schemas/repair.schema.json",
    "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json",
    "docs/coop/design-corrections/workflows/schemas/invocation-record.schema.json",
    "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
    "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json",
]


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k not in PROSE}
    if isinstance(o, list):
        return [strip(x) for x in o]
    return o


def flatten(o, p="", acc=None):
    if acc is None:
        acc = {}
    if isinstance(o, dict):
        for k, v in o.items():
            flatten(v, p + "/" + str(k), acc)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            flatten(v, p + "/" + str(i), acc)
    else:
        acc[p] = o
    return acc


def collect_enums(o, p="", acc=None):
    if acc is None:
        acc = {}
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "enum" and isinstance(v, list):
                acc[p + "/enum"] = v
            collect_enums(v, p + "/" + str(k), acc)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            collect_enums(v, p + "/" + str(i), acc)
    return acc


def main():
    out = sys.argv[1]
    rep = {"documents": []}
    any_widening = False
    for rel in DOCS:
        a_path, b_path = os.path.join(V16, rel), os.path.join(V17, rel)
        if not os.path.isfile(a_path):
            rep["documents"].append({"path": rel, "v16Present": False})
            continue
        a = json.load(open(a_path))
        b = json.load(open(b_path))
        sa, sb = strip(a), strip(b)

        fa, fb = flatten(sa), flatten(sb)
        changed = sorted(set(fa) & set(fb))
        changed = [p for p in changed if fa[p] != fb[p]]
        onlya = sorted(set(fa) - set(fb))
        onlyb = sorted(set(fb) - set(fa))

        ea, eb = collect_enums(sa), collect_enums(sb)
        enum_delta = []
        for p in sorted(set(ea) | set(eb)):
            va, vb = ea.get(p), eb.get(p)
            if va != vb:
                enum_delta.append({
                    "pointer": p,
                    "v16": va, "v17": vb,
                    "added": sorted(set(vb or []) - set(va or [])),
                    "removed": sorted(set(va or []) - set(vb or [])),
                    "memberSetEqual": set(va or []) == set(vb or []),
                    "orderOnlyChange": (set(va or []) == set(vb or [])
                                        and va != vb),
                })

        def widening_relevant(ptr):
            return any(("/" + k) in ptr for k in WIDENING_KEYS)

        wchanged = [p for p in changed if widening_relevant(p)]
        wonlya = [p for p in onlya if widening_relevant(p)]
        wonlyb = [p for p in onlyb if widening_relevant(p)]

        doc = {
            "path": rel,
            "structuralPointersChanged": len(changed),
            "structuralPointersOnlyInV16": len(onlya),
            "structuralPointersOnlyInV17": len(onlyb),
            "proseStrippedStructurallyIdentical":
                not changed and not onlya and not onlyb,
            "enumDeltas": enum_delta,
            "enumsThatGrew": [e for e in enum_delta if e["added"]],
            "enumsThatShrank": [e for e in enum_delta if e["removed"]],
            "wideningKeyPointersChanged": wchanged[:200],
            "wideningKeyPointersChangedCount": len(wchanged),
            "wideningKeyPointersRemoved": wonlya[:200],
            "wideningKeyPointersAdded": wonlyb[:200],
            "sampleChanged": [
                {"pointer": p, "v16": fa[p], "v17": fb[p]}
                for p in changed[:25]
            ],
            "sampleOnlyV17": [{"pointer": p, "v17": fb[p]} for p in onlyb[:40]],
            "sampleOnlyV16": [{"pointer": p, "v16": fa[p]} for p in onlya[:40]],
        }
        if doc["enumsThatGrew"] or doc["enumsThatShrank"]:
            any_widening = True
        rep["documents"].append(doc)

    rep["anyEnumVocabularyChanged"] = any_widening
    with open(out, "w") as fh:
        json.dump(rep, fh, indent=1, sort_keys=True)

    for d in rep["documents"]:
        print("=" * 78)
        print(d["path"])
        if not d.get("v16Present", True):
            print("  (not present in v16)")
            continue
        print("  prose-stripped identical:",
              d["proseStrippedStructurallyIdentical"])
        print("  structural pointers changed/onlyV16/onlyV17: %d / %d / %d"
              % (d["structuralPointersChanged"],
                 d["structuralPointersOnlyInV16"],
                 d["structuralPointersOnlyInV17"]))
        print("  widening-key pointers changed:",
              d["wideningKeyPointersChangedCount"])
        for e in d["enumDeltas"]:
            print("  ENUM DELTA", e["pointer"],
                  "added=", e["added"], "removed=", e["removed"],
                  "orderOnly=", e["orderOnlyChange"])
        for s in d["sampleChanged"][:12]:
            print("   CH", s["pointer"], "|", json.dumps(s["v16"])[:70],
                  "->", json.dumps(s["v17"])[:70])
        for s in d["sampleOnlyV17"][:20]:
            print("   +V17", s["pointer"], "=", json.dumps(s["v17"])[:80])
        for s in d["sampleOnlyV16"][:20]:
            print("   -V16", s["pointer"], "=", json.dumps(s["v16"])[:80])


if __name__ == "__main__":
    main()
