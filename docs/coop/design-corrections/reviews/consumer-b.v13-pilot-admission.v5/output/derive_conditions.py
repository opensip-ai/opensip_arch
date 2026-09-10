#!/usr/bin/env python3
"""Condition-level inventory (not keyword-level) from selected kit tables.

No whitelist of nested container names. Documents are selected from the TS
graph's owning schemas and followed $ref/document pointers, not from helper imports.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v5/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v13/subject")
sys.path.insert(0, str(OUT))

from helpers import kit_schemas, store, admit_graph, xsites, admit  # noqa: E402
from helpers.store import load_export  # noqa: E402

METADATA = {
    "standing": "table/document provenance; not an instance comparison",
    "why": "explanatory rationale",
    "whyItIsNeeded": "explanatory rationale",
    "whyThisWasNeeded": "explanatory rationale",
    "whyNotMoreEnumMembers": "explanatory rationale",
    "whyExactAndNotThePrefixConvention": "explanatory rationale",
    "whyNotRekeyByDocumentAndSelector": "explanatory rationale",
    "note": "non-normative commentary unless a sibling structured field is the predicate",
    "description": "JSON Schema description text",
    "enforcedAt": "names the boundary; the sibling structured fields are the predicates",
    "notARecognitionRule": "scope comment",
    "notAGrammarQuestion": "scope comment",
    "notAProofOfAbsence": "scope comment",
    "notASubstituteForAdmission": "scope comment",
    "notAStageSpecDuplicate": "scope comment",
    "examples": "illustrations, not oracle",
    "corpusCases": "illustrations",
    "limitations": "declared limitation list",
    "thisIsDeclarationSupportNotAnObligation": "limits what the sibling predicate implies",
    "selectedScalarCauseLimitation": "stated limitation",
    "perRequirementConsumerBoundary": "consumer routing, not this Run's native admission unless a repair is selected",
    "hostInvariantSuccessor": "declared future D9 owner",
    "helperDoesNotGuessOrigin": "boundary comment",
    "aliasMapIsContextFree": "boundary comment",
}

SCHEMA_NOISE = {
    "$schema",
    "$id",
    "$ref",
    "$defs",
    "title",
    "description",
    "type",
    "properties",
    "required",
    "additionalProperties",
    "items",
    "oneOf",
    "anyOf",
    "allOf",
    "if",
    "then",
    "else",
    "not",
    "const",
    "enum",
    "pattern",
    "minLength",
    "maxLength",
    "minItems",
    "maxItems",
    "uniqueItems",
    "minimum",
    "maximum",
    "default",
}


def pointer(parts: list) -> str:
    out = ""
    for p in parts:
        s = str(p).replace("~", "~0").replace("/", "~1")
        out += "/" + s
    return out or "/"


def walk_x(obj, parts, under_x, kit_path, sid, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = parts + [k]
            is_x = str(k).startswith("x-opensip-")
            if is_x:
                out.append(
                    {
                        "kitPath": kit_path,
                        "schemaId": sid,
                        "pointer": pointer(p),
                        "kind": "annotation",
                        "keyword": k,
                        "valueType": type(v).__name__,
                    }
                )
                walk_x(v, p, True, kit_path, sid, out)
            elif under_x:
                if k in METADATA:
                    out.append(
                        {
                            "kitPath": kit_path,
                            "schemaId": sid,
                            "pointer": pointer(p),
                            "kind": "metadata",
                            "key": k,
                            "reason": METADATA[k],
                        }
                    )
                    # still recurse: nested predicates may sit under a metadata wrapper
                    walk_x(v, p, True, kit_path, sid, out)
                else:
                    out.append(
                        {
                            "kitPath": kit_path,
                            "schemaId": sid,
                            "pointer": pointer(p),
                            "kind": "predicate-entry",
                            "key": k,
                            "valueType": type(v).__name__,
                            "scalar": v if isinstance(v, (str, int, bool)) or v is None else None,
                            "n": len(v) if isinstance(v, (dict, list)) else None,
                        }
                    )
                    walk_x(v, p, True, kit_path, sid, out)
            else:
                if k not in SCHEMA_NOISE or k in ("allOf", "if", "then", "oneOf", "anyOf", "properties", "items", "$defs"):
                    walk_x(v, p, False, kit_path, sid, out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            p = parts + [i]
            if under_x:
                out.append(
                    {
                        "kitPath": kit_path,
                        "schemaId": sid,
                        "pointer": pointer(p),
                        "kind": "predicate-entry",
                        "key": str(i),
                        "valueType": type(v).__name__,
                        "listIndex": i,
                    }
                )
            walk_x(v, p, under_x, kit_path, sid, out)


def classify_object(ident: str, obj) -> tuple[str, str] | None:
    if not isinstance(obj, dict):
        return None
    canon = admit_graph.classify_canonical_object(ident, obj)
    if canon:
        return canon
    bare_hex = len(ident) == 64 and all(c in "0123456789abcdef" for c in ident)
    if ident.startswith("sha256:") or bare_hex:
        cls = admit_graph.classify_sha256_object(obj)
        if cls:
            return cls
        if obj.get("schemaVersion") == 1 and "entries" in obj and obj.get("entries") and "packageName" in (obj["entries"][0] or {}):
            return ("urn:opensip:product-v1:native:evidence-schemas:v2", "ResolvedNodeModulesLayoutV1")
        if obj.get("schemaVersion") == 1 and "entryConfigPath" in obj and "nodes" in obj:
            return ("urn:opensip:product-v1:native:evidence-schemas:v2", "TypeScriptConfigGraphV1")
        if obj.get("schemaVersion") == 1 and "units" in obj and "rows" in obj and "erasedFiles" in obj:
            return ("urn:opensip:product-v1:native:evidence-schemas:v2", "UnitMembershipV1")
        if obj.get("schemaVersion") == 1 and "cells" in obj and "membershipDigest" in obj:
            return ("opensip.product.enumeration-plan.1", None)
        if obj.get("schemaVersion") == 1 and "rules" in obj and "detectorClosure" in ((obj.get("rules") or [{}])[0] or {}):
            return ("urn:opensip:product-v1:evaluator-emission-plan:1", None)
        if obj.get("schemaVersion") == 1 and "selectedRefs" in obj and "cellOutcomes" in obj:
            return ("opensip.product.execution-inputs.1", None)
        if obj.get("schemaVersion") == 1 and "cellOrdinal" in obj and "rows" in obj and "kind" in obj:
            return ("opensip.product.subject-inventory.1", None)
        if obj.get("schemaVersion") == 2 and "occupancy" in obj and "sourceFactId" in obj:
            return ("opensip.product.target-attribution.2", None)
        if obj.get("schemaFamily") == "opensip.product.policy":
            return ("urn:opensip:product-v1:policy-document:2", "PolicyDocumentV2")
        if obj.get("schemaFamily") == "opensip.product.waivers":
            return ("urn:opensip:product-v1:workflows:policy-document", "WaiverSetV1")
        if obj.get("schemaFamily") == "opensip.product.scope":
            return ("urn:opensip:product-v1:workflows:policy-document", "ScopeDocumentV1")
        if obj.get("payloadDomain") == "workflow.import-payload.runtime.v1":
            return ("urn:opensip:product-v1:workflows:imported-evidence", "RuntimePayloadV1")
        if obj.get("schemaVersion") == 2 and "requestedCapabilities" in obj:
            return ("urn:opensip:product-v1:identity:v3", "analysis-spec")
        if obj.get("schemaVersion") == 2 and "analysis" in obj and "capabilities" in (obj.get("analysis") or {}):
            return ("urn:opensip:product-configuration:2", None)
        if obj.get("schemaVersion") == 3 and "entry" in obj and "key" in obj:
            return ("urn:opensip:product-v1:native:evidence-schemas:v2", "CoverageResultV3")
        if obj.get("schemaVersion") == 1 and "authority" in obj and obj.get("authority") == "candidate-only":
            return ("opensip.product.execution-inputs.1", "CandidateProducerResultV1")
        return None
    pref = ident.split(":")[0]
    defn = kit_schemas.PREFIX_TO_IDENTITY_DEF.get(pref)
    if defn:
        return ("urn:opensip:product-v1:identity:v3", defn)
    return None


def collect_selected_docs(st: store.Store) -> dict[str, Path]:
    """Documents selected by the graph, then $ref / record.document follow."""
    selected: dict[str, Path] = {}

    def add_id(sid: str):
        p = kit_schemas.SCHEMA_PATHS.get(sid)
        if p:
            selected[sid] = p

    def add_rel(rel: str):
        p = KIT / rel
        if p.exists():
            try:
                d = json.loads(p.read_text())
            except Exception:
                return
            sid = d.get("$id") or rel
            selected[sid] = p

    for ident, obj in st.objects.items():
        cls = classify_object(ident, obj)
        if not cls:
            continue
        sid, _defn = cls
        add_id(sid)

    # always the identity/native/relation owners when those records exist
    add_rel("docs/coop/design-corrections/foundation/identity-schemas.v3.json")
    add_rel("docs/coop/design-corrections/native/native-evidence.schemas.v2.json")
    add_rel("docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json")
    add_rel("docs/coop/design-corrections/native/native-capability-matrix.v2.json")
    add_rel("docs/coop/design-corrections/native/capability-manifest-domains.v2.json")
    add_rel("docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json")

    # follow record.document and $ref document paths inside selected
    changed = True
    while changed:
        changed = False
        for sid, p in list(selected.items()):
            try:
                data = json.loads(p.read_text())
            except Exception:
                continue
            blob = json.dumps(data)

            def consider(doc: str):
                nonlocal changed
                if not isinstance(doc, str):
                    return
                for cand in (
                    doc,
                    "docs/coop/design-corrections/" + doc,
                    "docs/coop/design-corrections/foundation/" + doc.split("/")[-1],
                    "docs/coop/design-corrections/native/" + doc.split("/")[-1],
                    "docs/coop/design-corrections/workflows/schemas/" + doc.split("/")[-1],
                ):
                    fp = KIT / cand
                    if fp.exists() and fp.suffix == ".json":
                        try:
                            d = json.loads(fp.read_text())
                        except Exception:
                            continue
                        ns = d.get("$id") or cand
                        if ns not in selected:
                            selected[ns] = fp
                            changed = True
                        return

            def hunt(o):
                if isinstance(o, dict):
                    if "document" in o and isinstance(o["document"], str):
                        consider(o["document"])
                    if "$ref" in o and isinstance(o["$ref"], str) and not o["$ref"].startswith("#"):
                        consider(o["$ref"].split("#", 1)[0])
                    if "authority" in o and isinstance(o["authority"], str) and o["authority"].endswith(".json") or (
                        isinstance(o.get("authority"), str) and ".json#" in o.get("authority", "")
                    ):
                        consider(str(o["authority"]).split("#", 1)[0])
                    for v in o.values():
                        hunt(v)
                elif isinstance(o, list):
                    for v in o:
                        hunt(v)

            hunt(data)
    return selected


def bind_occurrences(st: store.Store, conditions: list[dict]) -> list[dict]:
    """Required (condition, instance, field) from kit+graph, not from handler cases."""
    classified = []
    for ident, obj in st.objects.items():
        cls = classify_object(ident, obj)
        classified.append((ident, obj, cls))

    facts = [(i, o) for i, o, c in classified if i.startswith("fact2:")]
    covs = [(i, o) for i, o, c in classified if i.startswith("coverage2:")]
    ctxs = [(i, o) for i, o, c in classified if c and c[1] == "TypeScriptNativeContextV2"]
    unis = [(i, o) for i, o, c in classified if c and c[1] == "TypeScriptUniverseV2ResolvedInputs"]
    plans = [(i, o) for i, o, c in classified if i.startswith("plan2:")]
    views = [(i, o) for i, o, c in classified if i.startswith("view2:")]
    findings = [(i, o) for i, o, c in classified if i.startswith("finding3:")]
    proofs = [(i, o) for i, o, c in classified if i.startswith("proof3:")]
    seals = [(i, o) for i, o, c in classified if i.startswith("seal3:")]
    imports = [(i, o) for i, o, c in classified if i.startswith("import2:")]
    scopes = [(i, o) for i, o, c in classified if i.startswith("scope2:")]
    specs = [(i, o, c) for i, o, c in classified if c and c[1] == "analysis-spec"]
    enums = [(i, o, c) for i, o, c in classified if c and c[0] == "opensip.product.enumeration-plan.1" and c[1] is None]
    invs = [(i, o, c) for i, o, c in classified if c and c[0] == "opensip.product.subject-inventory.1"]
    attrs = [(i, o, c) for i, o, c in classified if c and c[0] == "opensip.product.target-attribution.2"]
    eis = [(i, o, c) for i, o, c in classified if c and c[0] == "opensip.product.execution-inputs.1" and c[1] is None]
    mems = [(i, o, c) for i, o, c in classified if c and c[1] == "UnitMembershipV1"]
    graphs = [(i, o, c) for i, o, c in classified if c and c[1] == "TypeScriptConfigGraphV1"]
    layouts = [(i, o, c) for i, o, c in classified if c and c[1] == "ResolvedNodeModulesLayoutV1"]
    policies = [(i, o, c) for i, o, c in classified if c and c[1] == "PolicyDocumentV2"]
    emissions = [(i, o, c) for i, o, c in classified if c and c[0] == "urn:opensip:product-v1:evaluator-emission-plan:1"]
    cands = [(i, o, c) for i, o, c in classified if c and c[1] == "CandidateProducerResultV1"]

    occ = []

    def add(cond, instance, field, why):
        occ.append(
            {
                "condition": cond["pointer"] if isinstance(cond, dict) else cond,
                "kitPath": cond.get("kitPath") if isinstance(cond, dict) else None,
                "instance": instance,
                "field": field,
                "bindWhy": why,
                "kind": cond.get("kind") if isinstance(cond, dict) else None,
            }
        )

    # Schema×instance walk: every published field annotation on a retained record.
    # Independent of handler cases. Successor identity v3 wraps prefix-mapped records.
    for ident, obj, cls in classified:
        if not cls or not isinstance(obj, dict):
            continue
        sid, defn = cls
        try:
            schema = kit_schemas.wrap_def(sid, defn)
        except Exception:
            continue
        for site in xsites.iter_x_sites(obj, schema, sid, ident):
            kw = site["keyword"]
            if kw in {"x-opensip-ownership-attribute", "x-opensip-mirror"}:
                continue
            if kw == "x-opensip-uniqueness" and not isinstance(site["value"], list):
                if not (isinstance(site["value"], dict) and isinstance(site["value"].get("rules"), list)):
                    continue
            occ.append(
                {
                    "condition": site["schema_ptr"],
                    "kitPath": site.get("kitPath"),
                    "instance": ident,
                    "field": site["field"],
                    "bindWhy": "schema-walk",
                    "kind": "annotation",
                    "keyword": kw,
                }
            )
            if kw == "x-opensip-digest" and isinstance(site["annot"], dict) and site["annot"].get("representation") == "by-domain":
                dname = site["parent"].get("domain") if isinstance(site["parent"], dict) else None
                if dname:
                    occ.append(
                        {
                            "condition": f"/x-opensip-digest-domains/byDomain/{dname}",
                            "kitPath": site.get("kitPath"),
                            "instance": ident,
                            "field": site["field"],
                            "bindWhy": f"by-domain sibling {dname}",
                            "kind": "predicate-entry",
                        }
                    )

    # Relation payloads under owning facts (same instance id, payload schema pointers)
    for ident, obj in facts:
        rel = obj.get("relation")
        defn = kit_schemas.REL_TO_PAYLOAD_DEF.get(rel)
        if not defn:
            continue
        try:
            payload = admit_graph._load_c(st, obj["payloadDigest"])
        except Exception:
            continue
        schema = kit_schemas.wrap_def("opensip.product.relation-payload.2", defn)
        for site in xsites.iter_x_sites(payload, schema, "opensip.product.relation-payload.2", ident):
            if site["keyword"] in {"x-opensip-ownership-attribute", "x-opensip-mirror"}:
                continue
            occ.append(
                {
                    "condition": site["schema_ptr"],
                    "kitPath": site.get("kitPath"),
                    "instance": ident,
                    "field": site["field"],
                    "bindWhy": f"payload schema {defn}",
                    "kind": "annotation",
                    "keyword": site["keyword"],
                }
            )

    for cond in conditions:
        if cond.get("kind") == "metadata":
            continue
        # Join operand field names are not independent conditions. Dispatch scalars
        # (representation, nativeCause, form, class) are.
        OPERAND_KEYS = {
            "path", "pathField", "digestField", "lengthField", "retainedBlob", "nullable",
            "document", "selector", "bundle", "artifact", "derivedFrom", "resolvedThrough",
            "payloadClass", "authority", "schema", "admittedBy", "implementation",
            "semanticJoin", "anchorPathField", "retainedAs", "owner", "source",
        }
        if (
            cond.get("kind") == "predicate-entry"
            and cond.get("valueType") not in ("dict", "list")
            and cond.get("listIndex") is None
            and cond.get("key") in OPERAND_KEYS
        ):
            continue
        ptr = cond["pointer"]
        kit = cond.get("kitPath") or ""
        # Current identity owner is identity-schemas.v3. Historical v2 tables are
        # not applicable to v3-admitted records. Do not alias v2 to v3.
        if "identity-schemas.v2.json" in kit:
            continue

        # Field annotations are bound by schema-walk above, not by def-name matching
        # (which previously applied identity-schemas.v2 $defs to v3 instances).
        if "/$defs/" in ptr and "/properties/" in ptr and (
            ptr.endswith("/x-opensip-digest")
            or ptr.endswith("/x-opensip-order")
            or "/x-opensip-uniqueness" in ptr
            or "/x-opensip-vocabulary" in ptr
        ):
            continue

        if "x-opensip-relation-registry/relations/" in ptr.replace("~1", "/"):
            rest = ptr.split("relations/", 1)[1]
            rel = rest.split("/")[0]
            tail = rest[len(rel) :]
            if tail in ("", "/"):
                field = "relation"
            elif "universeRule" in tail:
                field = "sourceUniverse"
            elif "coverageTotality" in tail:
                field = "relation"
            elif "bodyIdentityJoin" in tail:
                field = "anchors"
            elif "snapshotJoins/" in tail:
                field = "retainedBlob" if rel == "file" else "path"
            elif "ladder" in tail:
                field = "resolution"
            elif "/rungs/" in tail:
                field = "resolvedTarget" if rel == "imports" else "resolution"
            elif "anchorLaw" in tail:
                field = "anchors"
            else:
                field = "relation"
            if "/snapshotJoins/" in tail and rel == "package":
                field = "manifestPath"
            for ident, obj in facts:
                if obj.get("relation") != rel:
                    continue
                f = field
                if "/rungs/" in tail:
                    rung = tail.split("rungs/", 1)[1].split("/")[0]
                    if obj.get("resolution") != rung:
                        f = "resolution"
                if "universeRule" in tail and rel == "imports":
                    f = "targetUniverse"
                add(cond, ident, f, f"fact.relation={rel}")
            continue

        if "/x-opensip-digest-domains/byDomain/" in ptr:
            # Bound from actual Ref.domain siblings during schema-walk; do not
            # attach every byDomain row to every prefixed identity.
            continue

        if "/domainSets/native-context/native.context.typescript.v2/" in ptr:
            if "/closureJoins/" in ptr:
                fld = "kind"
            elif "/snapshotJoins/0" in ptr:
                fld = "path"
            elif "/snapshotJoins/1" in ptr:
                fld = "contentSha256"
            elif "/nestedRecords/" in ptr:
                fld = "nodeModulesLayoutDigest"
            else:
                fld = ptr.rsplit("/", 1)[-1]
            for ident, obj in ctxs:
                add(cond, ident, fld, "TS native context domainSet entry")
            continue
        if "/domainSets/native-semantic-universe/native.semantic-universe.typescript.v2/" in ptr:
            if "/dialect/table/" in ptr:
                fld = "dialect"
            elif "/nestedRecords/" in ptr:
                fld = str(ptr.rsplit("/", 1)[-1])
            else:
                fld = ptr.rsplit("/", 1)[-1]
            for ident, obj in unis:
                add(cond, ident, fld, "TS universe domainSet entry")
            continue

        if "/closureKinds/byField/" in ptr:
            fld = ptr.split("byField/", 1)[1]
            if fld.startswith("fact."):
                f = fld.split(".", 1)[1]
                for ident, obj in facts:
                    add(cond, ident, f, "closureKinds.byField")
            elif fld.startswith("view."):
                f = fld.split(".", 1)[1]
                for ident, obj in views:
                    add(cond, ident, f, "closureKinds.byField")
            elif fld.startswith("finding."):
                f = fld.split(".", 1)[1]
                for ident, obj in findings:
                    add(cond, ident, f, "closureKinds.byField")
            elif fld.startswith("proof-bundle."):
                f = fld.split(".", 1)[1]
                for ident, obj in proofs:
                    add(cond, ident, f, "closureKinds.byField")
            elif fld.startswith("evaluation-seal."):
                f = fld.split(".", 1)[1]
                for ident, obj in seals:
                    add(cond, ident, f, "closureKinds.byField")
            elif fld.startswith("import."):
                f = fld.split(".", 1)[1]
                for ident, obj in imports:
                    add(cond, ident, f, "closureKinds.byField")
            elif fld.startswith("subject-scope."):
                f = fld.split(".", 1)[1]
                for ident, obj in scopes:
                    add(cond, ident, f, "closureKinds.byField")
            elif "TypeScriptToolClosureV1" in fld:
                for ident, obj in ctxs:
                    add(cond, ident, "toolClosure.closureId", "closureKinds.byField")
            elif "typescriptStdlibMerkleRoot" in fld:
                for ident, obj in ctxs:
                    add(cond, ident, "toolchain.typescriptStdlibMerkleRoot", "closureKinds.byField")
            continue

        if ptr.rstrip("/").endswith("noDeficiencyNoCause") or ptr.endswith("/noDeficiencyNoCause"):
            from helpers import law_admit as _la
            for ident, obj in covs:
                try:
                    pl = _la._c(st, obj["payloadDigest"])
                except Exception:
                    continue
                entry = pl.get("entry") or {}
                if entry.get("deficiency") is None:
                    add(cond, ident, "entry.nativeCause", "noDeficiencyNoCause")
            continue
        if "/x-opensip-deficiency-cause-registry/deficiencies/" in ptr:
            name = ptr.split("deficiencies/", 1)[1].split("/")[0]
            # sibling-dependent: this row applies only when entry.deficiency equals the row key
            from helpers import law_admit as _la
            for ident, obj in covs:
                try:
                    pl = _la._c(st, obj["payloadDigest"])
                except Exception:
                    continue
                d = (pl.get("entry") or {}).get("deficiency")
                if d == name:
                    add(cond, ident, "entry.deficiency", f"deficiency row {name} applies")
            continue

        if "/x-opensip-kind-derivation/" in ptr:
            cap = ptr.split("x-opensip-kind-derivation/", 1)[1].split("/")[0]
            for ident, obj, c in enums:
                for i, cell in enumerate(obj.get("cells") or []):
                    if cell.get("capabilityId") == cap:
                        add(cond, ident, f"cells[{i}].kinds", f"kind-derivation {cap}")
            continue

        if "/x-opensip-subject-language-table/members/" in ptr:
            rest = ptr.split("members/", 1)[1]
            try:
                mi = int(rest.split("/")[0])
            except Exception:
                continue
            members = LANG_TABLE["members"] if False else None
            try:
                from helpers.law_admit import LANG_TABLE as _LT, subject_language_from_table as _slt
                mem = (_LT.get("members") or [])[mi]
            except Exception:
                continue
            lid = mem.get("languageId")
            for ident, obj, c in invs:
                applies = False
                for row in (obj.get("rows") or []):
                    path = row.get("path") or ""
                    if _slt(path) == lid:
                        applies = True
                        break
                if applies:
                    add(cond, ident, "subjectLanguage", "subject-language-table member applies")
            continue

        if "/x-opensip-join-law/" in ptr:
            for ident, obj, c in attrs:
                add(cond, ident, ptr.rsplit("/", 1)[-1], "TargetAttributionV2 join-law")
            continue

        if "native-capability-matrix" in kit and "/capabilities/" in ptr:
            # bind to analysis-spec requestedCapabilities
            for ident, obj, c in specs:
                add(cond, ident, "requestedCapabilities", "matrix capability")
            continue

        if "/x-opensip-config-node-kind-law/" in ptr:
            for ident, obj, c in graphs:
                add(cond, ident, "nodes[].kind", "config-node-kind-law")
            continue

        if "/languageModes/map/" in ptr:
            mode = ptr.split("map/", 1)[1].split("/")[0]
            for ident, obj, c in specs:
                used = {r.get("languageMode") for r in (obj.get("requestedCapabilities") or [])}
                if mode in used:
                    add(cond, ident, "requestedCapabilities[].languageMode", f"mode {mode}")
            continue

        if "/x-opensip-file-membership-extent-law/" in ptr:
            for ident, obj, c in mems:
                add(cond, ident, "rows", "extent-law")
            for ident, obj, c in enums:
                add(cond, ident, "cells[].programBindings[].extents", "extent-law")
            continue

        if "/x-opensip-payload-registry/classes/" in ptr:
            cls = ptr.split("classes/", 1)[1].split("/")[0]
            if cls == "relation":
                for ident, obj in facts:
                    add(cond, ident, "payloadSchemaDigest", "payload-registry relation class")
            elif cls == "coverage":
                for ident, obj in covs:
                    add(cond, ident, "payloadSchemaDigest", "payload-registry coverage class")
            elif cls == "import":
                for ident, obj in imports:
                    add(cond, ident, "payloadSchemaDigest", "payload-registry import class")
            elif cls == "parameter":
                for ident, obj, c in specs:
                    add(cond, ident, "payloadSchemaDigest", "payload-registry parameter class")
            continue

        if "/x-opensip-evaluator-profile/" in ptr:
            for ident, obj in proofs + seals + [(i, o) for i, o, c in classified if i.startswith("run3:")]:
                add(cond, ident, "identity-prefix", "evaluator-profile")
            continue

        if "/x-opensip-evidence-relation-registry/" in ptr:
            for ident, obj, c in policies:
                add(cond, ident, "rules[].emitWhen", "evidence-relation-registry")
            continue

        if "/x-opensip-uniqueness" in ptr and "enumeration-plan" in kit:
            continue
        if "/x-opensip-uniqueness" in ptr and "emission" in kit:
            continue

        if "execution-inputs" in kit and cond.get("kind") == "annotation":
            continue

    return occ


def main():
    st = load_export(json.loads((OUT / "runs" / "ts.store.json").read_text()))
    docs = collect_selected_docs(st)
    conditions = []
    for sid, p in sorted(docs.items(), key=lambda kv: str(kv[1])):
        rel = p.as_posix().split("/subject/", 1)[-1] if "/subject/" in p.as_posix() else str(p)
        data = json.loads(p.read_text())
        walk_x(data, [], False, rel, data.get("$id") or sid, conditions)

    predicates = [c for c in conditions if c.get("kind") == "predicate-entry"]
    annotations = [c for c in conditions if c.get("kind") == "annotation"]
    metadata = [c for c in conditions if c.get("kind") == "metadata"]
    occ = bind_occurrences(st, conditions)
    occ = [o for o in occ if o.get("kind") != "metadata"]

    def keep_pointer(ptr: str) -> bool:
        """Keep annotations, named table rows, and indexed joins; drop nested operand dicts."""
        if ptr.endswith("x-opensip-digest") or ptr.endswith("x-opensip-order"):
            return True
        if ptr.rstrip("/").endswith("x-opensip-uniqueness") or ptr.rstrip("/").endswith("x-opensip-vocabulary"):
            return True
        segs = [s.replace("~1", "/") for s in ptr.split("/") if s]
        # indexed join row itself, not operand children (form/path/kind)
        for i, s in enumerate(segs):
            if s in {"closureJoins", "snapshotJoins", "nestedRecords", "blobJoins", "nestedIdentities", "rungs", "members", "joins"} and i + 1 < len(segs):
                return len(segs) == i + 2
        if "relations" in segs:
            j = segs.index("relations")
            if len(segs) == j + 2:
                return True
            if len(segs) == j + 3 and segs[j + 2] in {
                "ladder", "anchorLaw", "coverageTotality", "bodyIdentityJoin", "universeRule",
            }:
                return True
            if len(segs) == j + 4 and segs[j + 2] in {"rungs", "snapshotJoins"}:
                return True
            return False
        for marker in ("byDomain", "byField", "deficiencies", "classes", "map", "table"):
            if marker in segs:
                j = segs.index(marker)
                return j + 1 < len(segs) and len(segs) == j + 2
        if "kind-derivation" in ptr:
            return len(segs) == 2
        if ptr.rstrip("/").endswith("noDeficiencyNoCause"):
            return True
        if segs and segs[0] in {
            "x-opensip-join-law",
            "x-opensip-config-node-kind-law",
            "x-opensip-file-membership-extent-law",
            "x-opensip-subject-language-table",
            "x-opensip-evidence-relation-registry",
            "x-opensip-deficiency-cause-registry",
        } and len(segs) <= 1:
            return True
        if segs and segs[0] == "x-opensip-evaluator-profile":
            return len(segs) == 2 and segs[1] == "changedIdentifierMajors"
        if "capabilities" in segs and "native-capability-matrix" in ptr:
            j = segs.index("capabilities")
            return len(segs) == j + 2 or (len(segs) == j + 1)
        if "schema-walk" in ptr:
            return True
        return False

    occ = [
        o
        for o in occ
        if o.get("bindWhy") == "schema-walk"
        or str(o.get("bindWhy") or "").startswith("by-domain sibling")
        or str(o.get("bindWhy") or "").startswith("payload schema")
        or keep_pointer(o["condition"])
    ]
    # unique
    seen = set()
    uniq = []
    for o in occ:
        k = (o["condition"], o["instance"], o["field"])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(o)
    occ = uniq

    dest = OUT / "condition-inventory.json"
    dest.write_text(
        json.dumps(
            {
                "standing": "Condition inventory: every nested key/list index under x-opensip-* without container whitelist. Metadata keys classified with reasons.",
                "selectedDocuments": {k: str(v) for k, v in docs.items()},
                "counts": {
                    "documents": len(docs),
                    "conditions": len(conditions),
                    "annotations": len(annotations),
                    "predicateEntries": len(predicates),
                    "metadata": len(metadata),
                },
                "conditions": conditions,
            },
            indent=2,
        )
        + "\n"
    )
    (OUT / "required-occurrences.json").write_text(
        json.dumps(
            {
                "standing": "Required (condition,instance,field) from kit tables × this TS graph. Not from handler cases.",
                "count": len(occ),
                "occurrences": occ,
            },
            indent=2,
        )
        + "\n"
    )
    print("docs", len(docs))
    print("conditions", len(conditions), "pred", len(predicates), "ann", len(annotations), "meta", len(metadata))
    print("required occurrences", len(occ))
    print("selected", sorted(docs))


if __name__ == "__main__":
    main()
