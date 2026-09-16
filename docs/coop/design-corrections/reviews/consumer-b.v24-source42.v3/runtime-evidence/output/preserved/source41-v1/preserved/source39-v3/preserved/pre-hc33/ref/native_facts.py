"""Relation-registry laws, fact admission (incl. clones body identity), subject-scope admission,
native Coverage producer admission, view admission, and sufficiency_v2.

Sources: relation-payload-schemas.v2.json#/x-opensip-relation-registry (ladder, rungs, universeRule, anchorLaw,
snapshotJoins, bodyIdentityJoin, coverageTotalityLaw, coveragePartitionLaw), identity s3 (fact2/coverage2 joins),
native-evidence s1.2 (syntax capability law), s4.1a (commitment), s4.3 (RC-0..RC-6), s4.6 (sufficiency_v2),
s10 (cause registry, dialect disclosure), fact-identity-policy.v2 (#/canonicalisationSchema byteGrammar),
identity-schemas.v3 #/x-opensip-digest-domains (languageVersionBinding, scopeCapabilityLaw),
native-evidence.schemas.v2.json (#/x-opensip-deficiency-cause-registry, #/x-opensip-grammar-capability-registry),
fact-plane.v1.json#/relationRegistry/dependsOn (dependency table consumed by s4.6 step 8).
"""
import hashlib
import unicodedata

import canonical as K
import schemas
import source39 as S39
from native_ctx import Refusal, body_language_version, suffix_select, rust_dialect, inv_map

KIT = schemas.kit()
REL_DOC = "foundation/relation-payload-schemas.v2.json"
NE = "native/native-evidence.schemas.v2.json"
ID = "foundation/identity-schemas.v3.json"
REG = KIT.doc(REL_DOC)["x-opensip-relation-registry"]
RELS = REG["relations"]
CAUSES = KIT.doc(NE)["x-opensip-deficiency-cause-registry"]["deficiencies"]
GRAMMARS = KIT.doc(NE)["x-opensip-grammar-capability-registry"]["languages"]
SCL = KIT.doc(ID)["x-opensip-digest-domains"]["scopeCapabilityLaw"]
DEPENDS_ON = KIT.doc("coop/artifacts/fact-plane.v1.json")["relationRegistry"]["dependsOn"]
RESOLVED = {"resolved-target", "resolved-binding", "resolved-callee", "checked", "from-resolved-calls"}
INVENTORY_CAPS = {"file@enumerated", "package@manifest-declared", "vcs-change@vcs-reported"}
PRECEDENCE = ["language-tier-unsupported", "provider-unavailable", "input-closure-incomplete", "budget-exhausted",
              "confidence-floor-unmet", "derivation-policy-unmet", "resolution-incomplete", "external-consumers-unknown",
              "required-relation-missing"]
FACT_ID_TAG = "opensip.fact-identity.v1"


def rel_doc_digest():
    return KIT.digest(REL_DOC)


def ne_doc_digest():
    return KIT.digest(NE)


def ladder_ok(relation, rung):
    row = RELS.get(relation)
    return row is not None and rung in row["ladder"]


def ladder_index(relation, rung):
    return RELS[relation]["ladder"].index(rung)


def is_nfc_everywhere(v):
    if isinstance(v, str):
        return unicodedata.is_normalized("NFC", v)
    if isinstance(v, dict):
        return all(is_nfc_everywhere(k) and is_nfc_everywhere(x) for k, x in v.items())
    if isinstance(v, list):
        return all(is_nfc_everywhere(x) for x in v)
    return True


# ------------------------------------------------------------------ fact admission
def admit_fact_payload(store, fact):
    faults = []
    rel = fact["relation"]
    row = RELS.get(rel)
    if row is None:
        return None, ["RELATION_UNREGISTERED:" + rel]
    if fact["payloadSchemaDigest"] != rel_doc_digest():
        faults.append("FACT_PAYLOAD_SCHEMA_NOT_REGISTERED")
    if fact["payloadDigest"] not in store.blobs:
        return None, faults + ["EVIDENCE_UNAVAILABLE:fact-payload"]
    payload = store.get_record(fact["payloadDigest"])
    r = KIT.admit(payload, REL_DOC, row["selector"])
    if not r["ok"]:
        faults.append(f"FACT_PAYLOAD_SCHEMA:{r['stock'][:1]}{r['order'][:1]}{r['typed']}")
    if not is_nfc_everywhere(payload):
        faults.append("FACT_PAYLOAD_TEXT_NOT_NFC")
    return payload, faults


def body_frame_parse(frame):
    pos = 0

    def u8comp():
        nonlocal pos
        n = frame[pos]
        pos += 1
        v = frame[pos:pos + n]
        if len(v) != n:
            raise ValueError("short component")
        pos += n
        return v
    tag = u8comp()
    level = u8comp()
    level_version = u8comp()
    lang = u8comp()
    lang_version = u8comp()
    n = int.from_bytes(frame[pos:pos + 4], "big")
    pos += 4
    payload = frame[pos:pos + n]
    if len(payload) != n:
        raise ValueError("short payload")
    pos += n
    if pos != len(frame):
        raise ValueError("trailing bytes")
    return {"tag": tag, "level": level, "levelVersion": level_version, "languageId": lang,
            "languageVersion": lang_version, "payload": payload}


def token_stream_parse(payload):
    pos = 0
    count = int.from_bytes(payload[0:4], "big")
    pos = 4
    toks = []
    for _ in range(count):
        kl = int.from_bytes(payload[pos:pos + 2], "big")
        pos += 2
        kind = payload[pos:pos + kl]
        pos += kl
        vl = int.from_bytes(payload[pos:pos + 4], "big")
        pos += 4
        val = payload[pos:pos + vl]
        pos += vl
        if len(kind) != kl or len(val) != vl or kl == 0:
            raise ValueError("token framing")
        kind.decode("utf-8")
        toks.append((kind, val))
    if pos != len(payload):
        raise ValueError("token stream trailing bytes")
    return toks


def build_body_frame(level_id, level_version_hex, language_id, blv_record, payload):
    lv = bytes.fromhex(level_version_hex)
    lang_v = hashlib.sha256(K.C(blv_record)).digest()
    parts = [bytes([len(FACT_ID_TAG)]), FACT_ID_TAG.encode(), bytes([len(level_id)]), level_id.encode(),
             bytes([len(lv)]), lv, bytes([len(language_id)]), language_id.encode(), bytes([len(lang_v)]), lang_v,
             len(payload).to_bytes(4, "big"), payload]
    return b"".join(parts)


def l0_payload(span):
    return len(span).to_bytes(4, "big") + span


def l1_payload(tokens):
    out = [len(tokens).to_bytes(4, "big")]
    for kind, val in tokens:
        kb = kind.encode()
        out += [len(kb).to_bytes(2, "big"), kb, len(val).to_bytes(4, "big"), val]
    return b"".join(out)


def clones_join_faults(store, fact, payload, bound):
    faults = []
    join = RELS["clones"]["bodyIdentityJoin"]
    if join["anchorCardinality"] != RELS["clones"]["anchorLaw"]["cardinality"]:
        faults.append("RELATION_ANCHOR_LAW_DRIFT")
    if len(fact["anchors"]) != 1:
        return faults
    anchor = fact["anchors"][0]
    spec = payload["normalisationVersion"]
    # HC-16: normalizationSpecificationLaw - the interpreting closure's map selects the level specification (five ordered joins)
    faults += S39.normalization_map_faults(store, payload, bound)
    hx = payload["bodyIdentity"][7:]
    if hx not in store.blobs:
        return faults + ["EVIDENCE_UNAVAILABLE:body-identity-frame"]
    frame = store.get_bytes(hx)
    try:
        parts = body_frame_parse(frame)
    except (ValueError, IndexError):
        return faults + ["CLONE_BODY_FRAME_MALFORMED"]
    if parts["tag"] != join["domainTag"].encode():
        faults.append("CLONE_BODY_FRAME_DOMAIN_TAG")
    if parts["level"] != payload["normalisationLevel"].encode():
        faults.append("CLONE_BODY_FRAME_LEVEL")
    if parts["levelVersion"] != bytes.fromhex(spec):
        faults.append("CLONE_BODY_FRAME_LEVEL_VERSION")
    rec, lang, refusal = body_language_version(bound, anchor["path"])
    if refusal:
        return faults + [refusal]
    if parts["languageId"] != lang.encode():
        faults.append("CLONE_BODY_FRAME_LANGUAGE_ID")
    if lang not in bound["row"]["languageVersionBinding"]["bodyLanguages"]:
        faults.append("CLONE_BODY_LANGUAGE_NOT_OF_UNIVERSE")
    if parts["languageVersion"] != hashlib.sha256(K.C(rec)).digest():
        faults.append("CLONE_BODY_FRAME_LANGUAGE_VERSION")
    src = store.blobs.get(anchor["blobDigest"])
    if payload["normalisationLevel"] == "L0-verbatim":
        if src is None or parts["payload"] != l0_payload(src[anchor["startByte"]:anchor["endByte"]]):
            faults.append("CLONE_L0_PAYLOAD_NOT_ANCHOR_SPAN")
    else:
        try:
            token_stream_parse(parts["payload"])
        except (ValueError, UnicodeDecodeError):
            faults.append("CLONE_TOKEN_STREAM_FRAMING")
    return faults


def syntax_selected_rows(bound):
    ctx = bound["contextAdmission"]["context"]
    sel = set(bound["universe"]["selectedGrammarIds"])
    return [g for g in ctx["grammarBundle"]["grammars"] if g["grammarId"] in sel]


def syntax_path_capabilities(bound, path):
    rows = syntax_selected_rows(bound)
    suffixes = {s: g for g in rows for s in g["suffixes"]}
    suf = suffix_select(list(suffixes.keys()), path)
    if suf is None:
        return None, set()
    g = suffixes[suf]
    return g, set(GRAMMARS[g["languageId"]]["capabilities"]) if g["syntaxClass"] == GRAMMARS[g["languageId"]]["syntaxClass"] else set()


def fact_faults(store, fact, snapshot_id, inventory, bound_by_hex):
    """Run-closure admission of one fact2 descriptor. Returns (faults, payload)."""
    faults = []
    r = KIT.admit(fact, ID, "#/$defs/fact")
    if not r["ok"]:
        return [f"FACT_SCHEMA:{r['stock'][:1]}{r['order'][:1]}{r['typed']}"], None
    if fact["snapshotId"] != snapshot_id:
        faults.append("REFERENCE_SOURCE_JOIN")
    rel, rung = fact["relation"], fact["resolution"]
    if rel not in RELS:
        return faults + ["RELATION_UNREGISTERED"], None
    row = RELS[rel]
    if rung not in row["ladder"]:
        faults.append("FACT_RUNG_NOT_IN_RELATION_LADDER")
    payload, pf = admit_fact_payload(store, fact)
    faults += pf
    if payload is None:
        return faults, None
    rules = row["rungs"].get(rung, {"required": [], "forbidden": []})
    for f in rules["required"]:
        if f not in payload:
            faults.append(f"FACT_RUNG_FIELD_REQUIRED:{f}")
    for f in rules["forbidden"]:
        if f in payload:
            faults.append(f"FACT_RUNG_FIELD_FORBIDDEN:{f}")
    if row["universeRule"] == "same-only" and fact["sourceUniverse"] != fact["targetUniverse"]:
        faults.append("FACT_UNIVERSE_RULE")
    for u in (fact["sourceUniverse"], fact["targetUniverse"]):
        if u not in bound_by_hex:
            faults.append("FACT_UNIVERSE_NOT_PLAN_SELECTED")
    law = row["anchorLaw"]
    n = len(fact["anchors"])
    if (law["class"] == "source-text" and n < 1) or (law["class"] in ("body-identity", "inventory") and n != law["cardinality"]):
        return faults + ["FACT_ANCHOR_CARDINALITY"], payload
    inv = inv_map(inventory)
    for a in fact["anchors"]:
        irow = inv.get(a["path"])
        if irow is None or irow["sha256"] != a["blobDigest"]:
            faults.append("ANCHOR_SOURCE")
            continue
        b = store.blobs.get(a["blobDigest"])
        if b is None:
            faults.append("EVIDENCE_UNAVAILABLE:anchor-blob")
            continue
        if not (0 <= a["startByte"] <= a["endByte"] <= len(b)):
            faults.append("ANCHOR_RANGE")
            continue
        try:
            b[a["startByte"]:a["endByte"]].decode("utf-8")
            if a["startByte"] < len(b) and (b[a["startByte"]] & 0xC0) == 0x80:
                raise UnicodeDecodeError("utf-8", b, a["startByte"], a["startByte"] + 1, "split")
        except UnicodeDecodeError:
            faults.append("ANCHOR_UTF8")
    for j in row["snapshotJoins"]:
        if j.get("unless") and payload.get(j["unless"]["field"]) == j["unless"]["equals"]:
            continue
        p = payload.get(j["pathField"])
        irow = inv.get(p)
        if irow is None:
            faults.append(f"SNAPSHOT_JOIN_PATH:{rel}")
            continue
        if j["form"] == "inventoried-file":
            if payload[j["digestField"]] != irow["sha256"]:
                faults.append("SNAPSHOT_JOIN_DIGEST")
            if payload[j["lengthField"]] != irow["bytes"]:
                faults.append("SNAPSHOT_JOIN_LENGTH")
            b = store.blobs.get(irow["sha256"])
            if b is None:
                faults.append("EVIDENCE_UNAVAILABLE:inventoried-file")
            elif hashlib.sha256(b).hexdigest() != irow["sha256"] or len(b) != irow["bytes"]:
                faults.append("SNAPSHOT_JOIN_RETAINED_BYTES")
    bound = bound_by_hex.get(fact["sourceUniverse"])
    if bound is not None:
        cap = f"{rel}@{rung}"
        if bound["domain"] == "native.semantic-universe.syntax.v2" and cap not in INVENTORY_CAPS:
            for a in fact["anchors"]:
                g, caps = syntax_path_capabilities(bound, a["path"])
                if cap not in caps:
                    faults.append("SYNTAX_CAPABILITY_UNSUPPORTED_FACT")
        if rel == "clones":
            faults += clones_join_faults(store, fact, payload, bound)
    if fact["confidenceMillionths"] != 1000000:
        faults.append("cb24.NATIVE_CONFIDENCE_EMISSION_LAW")
    return faults, payload


# ------------------------------------------------------------------ scope and Coverage
def scope_faults(scope, snapshot_id, bound_by_hex, closures):
    faults = []
    r = KIT.admit(scope, ID, "#/$defs/subject-scope")
    if not r["ok"]:
        return [f"SCOPE_SCHEMA:{r['stock'][:1]}{r['order'][:1]}{r['typed']}"]
    if scope["snapshotId"] != snapshot_id:
        faults.append("SCOPE_SOURCE_JOIN")
    if not ladder_ok(scope["relation"], scope["resolution"]):
        faults.append("SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER")
    c = closures.get(scope["enumeratorClosure"])
    if c is None:
        faults.append("UNSELECTED_ENUMERATOR")
    elif c["kind"] != "provider":
        faults.append("ENUMERATOR_CLOSURE_KIND")
    for u in (scope["sourceUniverse"], scope["targetUniverse"]):
        if u not in bound_by_hex:
            faults.append("SCOPE_UNIVERSE_NOT_PLAN_SELECTED")
    if scope["relation"] in RELS and RELS[scope["relation"]]["universeRule"] == "same-only" and scope["sourceUniverse"] != scope["targetUniverse"]:
        faults.append("SCOPE_UNIVERSE_RULE")
    return faults


def cause_registry_faults(entry, relation):
    d, c = entry["deficiency"], entry["nativeCause"]
    if d is None:
        return [] if c is None else ["native.coverage-cause-without-deficiency"]
    row = CAUSES.get(d)
    if row is None:
        return ["native.coverage-cause-registry-row-missing"]
    out = []
    if "relations" in row and relation not in row["relations"]:
        out.append("native.coverage-cause-relation-not-in-scope")
    if row["nativeCause"] == "required" and c is None:
        out.append("native.coverage-cause-required")
    if row["nativeCause"] == "must-be-null" and c is not None:
        out.append("native.coverage-cause-must-be-null")
    if c is not None and "allowedCauses" in row and c not in row["allowedCauses"]:
        out.append("native.coverage-cause-not-for-deficiency")
    if "requires" in row:
        cur = entry
        for p in row["requires"]["path"]:
            cur = cur[p]
        if cur != row["requires"]["equals"]:
            out.append("native.coverage-cause-carrier-unsupported")
    if "oneOf" in row:
        cur = entry
        for p in row["oneOf"]["path"]:
            cur = cur[p]
        if cur not in row["oneOf"]["members"]:
            out.append("native.coverage-cause-carrier-unsupported")
    if "contains" in row and row["contains"]["member"] not in entry[row["contains"]["path"][0]]:
        out.append("native.coverage-cause-carrier-unsupported")
    return out


def owed_disclosure(scope, bound, inventory):
    """Returns ((deficiency, nativeCause), refusalName) owed for a scope, or None when a determinate answer is lawful.

    HC-17: scopeCapabilityLaw.guardOrder at Run closure - the compilation-ownership axis, then the syntax grammar-capability
    registry, then this law as the backstop for EVERY universe through languageVersionBinding.bodyEligibility
    (appliesToBodyEligibility; Rust closed-suffix-set). The original order and closed-suffix-table-only gate are preserved in
    preserved/s39-original/ref/native_facts.py."""
    rel, rung = scope["relation"], scope["resolution"]
    cap = f"{rel}@{rung}"
    lts = ("language-tier-unsupported", "capability-missing")
    dom = bound["domain"]
    if dom == "native.semantic-universe.rust.v2" and rel == "clones":
        own = bound["sourceUnitOwnership"]
        if own is None:
            return ("input-closure-incomplete", "body-language-ownership-missing"), "COVERAGE_DIALECT_PREREQUISITE"
        if own["enumeration"] == "partial":
            return ("input-closure-incomplete", "body-language-owner-unenumerated"), "COVERAGE_DIALECT_PREREQUISITE"
        for s in scope["subjects"]:
            _, refusal = rust_dialect(bound, s)
            if refusal == "BODY_LANGUAGE_OWNER_AMBIGUOUS":
                return ("input-closure-incomplete", "body-language-owner-ambiguous"), "COVERAGE_DIALECT_PREREQUISITE"
    if dom == "native.semantic-universe.syntax.v2" and cap not in INVENTORY_CAPS:
        if RELS[rel]["subjectKind"] == "source-path":
            if not scope["subjects"]:
                return lts, "SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE"
            for s in scope["subjects"]:
                g, caps = syntax_path_capabilities(bound, s)
                if cap not in caps:
                    return lts, "SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE"
        else:
            if not any(cap in syntax_path_capabilities(bound, row["path"])[1] for row in inventory):
                return lts, "SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE"
    if "bodyIdentityJoin" in RELS[rel] and cap not in INVENTORY_CAPS:
        if RELS[rel]["subjectKind"] == "source-path":
            if not scope["subjects"] or any(not S39.body_eligible(dom, s) for s in scope["subjects"]):
                return lts, "COVERAGE_SOURCE_VARIANT_UNSUPPORTED_SCOPE"
        elif not any(S39.body_eligible(dom, row["path"]) for row in inventory):
            return lts, "COVERAGE_SOURCE_VARIANT_UNSUPPORTED_SCOPE"
    return None


def coverage_faults(store, coverage, scope, scope_id, view_facts_payloads, bound, inventory):
    """admit_coverage_result_v3 over retained bytes (producer boundary re-run at closure)."""
    faults = []
    r = KIT.admit(coverage, ID, "#/$defs/coverage")
    if not r["ok"]:
        return ["COVERAGE_SCHEMA"], None
    if coverage["scopeId"] != scope_id:
        faults.append("native.coverage-subject-scope-outside-view")
    if coverage["payloadSchemaDigest"] != ne_doc_digest():
        faults.append("native.coverage-payload-schema-not-registered")
    if coverage["payloadDigest"] not in store.blobs:
        return faults + ["EVIDENCE_UNAVAILABLE:coverage-payload"], None
    payload = store.get_record(coverage["payloadDigest"])
    pr = KIT.admit(payload, NE, "#/$defs/CoverageResultV3")
    if not pr["ok"]:
        return faults + [f"COVERAGE_PAYLOAD_SCHEMA:{pr['stock'][:1]}{pr['order'][:1]}"], payload
    key, entry = payload["key"], payload["entry"]
    for f in ("relation", "resolution", "sourceUniverse", "targetUniverse"):
        if key[f] != scope[f]:
            faults.append(f"native.coverage-key-scope-mismatch:{f}")
    if key["subjectScopeCommitment"] != "sha256:" + scope_id.split(":", 1)[1]:
        faults.append("native.subject-scope-commitment-mismatch")
    if entry["examinedUniverse"]["subjectScopeCommitment"] != key["subjectScopeCommitment"]:
        faults.append("native.examined-universe-commitment-mismatch")
    if entry["examinedUniverse"]["subjectCount"] != len(scope["subjects"]):
        faults.append("native.examined-universe-subject-count-mismatch")
    if entry["relation"] != key["relation"] or entry["resolution"] != key["resolution"]:
        faults.append("native.coverage-entry-key-mismatch")
    rel, rung = key["relation"], key["resolution"]
    if not ladder_ok(rel, rung):
        return faults + ["native.coverage-bijection-mismatch:RC-0"], payload
    rc = entry["resolutionCompleteness"]
    if rung in RESOLVED:
        subjects = set(scope["subjects"])
        edges = [p for (f, p) in view_facts_payloads if f["relation"] == "unresolved-edge" and p["relation"] == rel and p["referrer"] in subjects]
        st = rc["state"]
        classes = sorted({p["edgeKind"] for p in edges})
        if st == "not-applicable":
            faults.append("native.coverage-bijection-mismatch:RC-1-resolved-not-applicable")
        elif st == "complete":
            if not (rc["attempted"] and rc["examinedExhaustive"] and rc["stageTerminal"] == "complete" and not edges):
                faults.append("native.coverage-bijection-mismatch:RC-2-complete")
        elif st == "incomplete":
            if not (edges and rc["stageTerminal"] == "complete" and rc["examinedExhaustive"]):
                faults.append("native.coverage-bijection-mismatch:RC-2-incomplete")
        elif st == "partial":
            if not (rc["attempted"] and (rc["stageTerminal"] in ("unavailable", "budget-exhausted", "provider-fault", "cancelled", "crash") or not rc["examinedExhaustive"])):
                faults.append("native.coverage-bijection-mismatch:RC-2-partial")
        elif st == "not-attempted":
            if rc["attempted"] or rc["unresolvedEdgeCount"] != 0:
                faults.append("native.coverage-bijection-mismatch:RC-2-not-attempted")
        if st in ("complete", "incomplete") and (rc["unresolvedEdgeCount"] != len(edges) or rc["unresolvedEdgeClasses"] != classes):
            faults.append("native.coverage-bijection-mismatch:RC-2-edge-account")
    else:
        if rc["state"] != "not-applicable" or rc["attempted"] or rc["unresolvedEdgeCount"] != 0 or rc["unresolvedEdgeClasses"]:
            faults.append("native.coverage-bijection-mismatch:RC-1-non-resolved")
    if entry["coverage"] == "complete" and not rc["examinedExhaustive"]:
        faults.append("native.coverage-bijection-mismatch:RC-6")
    faults += cause_registry_faults(entry, rel)
    owed = owed_disclosure(scope, bound, inventory)
    if owed is not None:
        # Published complete keys (native s1.2 line 442, s10 lines 3300-3326): SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE,
        # COVERAGE_SOURCE_VARIANT_UNSUPPORTED_SCOPE, COVERAGE_DIALECT_PREREQUISITE / _DEFICIENCY_MISMATCH / _CAUSE_MISMATCH.
        # The syntax/source-variant mismatch and every "undisclosed" variant are NOT spelled out by the kit; this
        # reconstruction names them under cb24. (helper correction HC-KEYNAMES; see notes/02 advisory).
        # HC-17 (source39 names): COVERAGE_DIALECT_{PREREQUISITE,UNDISCLOSED,DEFICIENCY_MISMATCH,CAUSE_MISMATCH} (native s10 lines
        # 3454-3457); COVERAGE_SOURCE_VARIANT_{UNSUPPORTED_SCOPE,DEFICIENCY_MISMATCH,CAUSE_MISMATCH} (s10 lines 3479-3482,
        # scopeCapabilityLaw.refusals), where a null deficiency is a wrong deficiency. SYNTAX_CAPABILITY publishes only its
        # false-complete name, so its mismatch variants keep cb24 names.
        (od, oc), name = owed
        family = {"SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE": "SYNTAX_CAPABILITY", "COVERAGE_SOURCE_VARIANT_UNSUPPORTED_SCOPE": "COVERAGE_SOURCE_VARIANT",
                  "COVERAGE_DIALECT_PREREQUISITE": "COVERAGE_DIALECT"}[name]
        local = "cb24." if family == "SYNTAX_CAPABILITY" else ""
        if entry["coverage"] == "complete":
            faults.append(name)
        elif entry["deficiency"] is None:
            faults.append({"COVERAGE_DIALECT": "COVERAGE_DIALECT_UNDISCLOSED",
                           "COVERAGE_SOURCE_VARIANT": "COVERAGE_SOURCE_VARIANT_DEFICIENCY_MISMATCH"}.get(family, f"cb24.{family}_UNDISCLOSED"))
        elif entry["deficiency"] != od:
            faults.append(f"{local}{family}_DEFICIENCY_MISMATCH")
        elif entry["nativeCause"] != oc:
            faults.append(f"{local}{family}_CAUSE_MISMATCH")
    return faults, payload


def view_faults(view, plan_id, scopes_by_id, coverages_by_id, facts_by_id, schema_doc_digests):
    faults = []
    r = KIT.admit(view, ID, "#/$defs/view")
    if not r["ok"]:
        return ["VIEW_SCHEMA"]
    if view["planId"] != plan_id:
        faults.append("VIEW_PLAN_JOIN")
    for d in view["schemaDigests"]:
        if d not in schema_doc_digests:
            faults.append("SCHEMA_DOCUMENT_UNREGISTERED")
    for cid in view["coverageIds"]:
        cov = coverages_by_id[cid]
        if cov["scopeId"] not in view["scopeIds"]:
            faults.append("native.coverage-subject-scope-outside-view")
    for fid in view["facts"]:
        f = facts_by_id[fid]
        if f["producerClosure"] != view["producerClosure"]:
            faults.append("VIEW_FACT_PRODUCER_JOIN")
        if not any(s["snapshotId"] == f["snapshotId"] and s["relation"] == f["relation"] and s["resolution"] == f["resolution"]
                   and s["sourceUniverse"] == f["sourceUniverse"] and s["targetUniverse"] == f["targetUniverse"]
                   for s in (scopes_by_id[x] for x in view["scopeIds"])):
            faults.append("VIEW_FACT_SCOPE_JOIN")
    # coveragePartitionLaw (per view, every scope, including scopes with no Coverage)
    key = REG["coveragePartitionLaw"]["partitionKey"]
    parts = {}
    for sid in view["scopeIds"]:
        s = scopes_by_id[sid]
        k = tuple(s[x] for x in key)
        for subj in s["subjects"]:
            parts.setdefault(k, {}).setdefault(subj, []).append(sid)
    for k, subjects in parts.items():
        overl = sorted((subj for subj, sids in subjects.items() if len(sids) > 1), key=lambda x: x.encode())
        if overl:
            faults.append(f"SUBJECT_SCOPE_PARTITION_OVERLAP:{k[1]}@{k[2]}:{overl[0]}")
    return faults


def totality_faults(view, scopes_by_id, coverages_by_id, facts_by_id, payloads_by_fact, inventory, coverage_payloads):
    faults = []
    inv = inv_map(inventory)
    tot = RELS["file"]["coverageTotality"]
    for cid in view["coverageIds"]:
        cov = coverages_by_id[cid]
        s = scopes_by_id[cov["scopeId"]]
        if s["relation"] != "file" or s["resolution"] != tot["rung"]:
            continue
        if coverage_payloads[cid]["entry"]["coverage"] != "complete":
            continue
        for subj in s["subjects"]:
            if subj not in inv:
                continue
            ok = any(all(facts_by_id[fid][m] == s[m] for m in tot["matchOn"]) and payloads_by_fact[fid][tot["pathField"]] == subj
                     for fid in view["facts"])
            if not ok:
                faults.append(f"{tot['refusal']}:{subj}")
    return faults


# ------------------------------------------------------------------ sufficiency_v2 (native s4.6)
def sufficiency_v2(req, view, depth=0):
    """req: RequirementV2 dict. view: {relation: [entry,...] positions folded per atom contract}, each entry a ViewEntryV3
    plus optional 'affected'/'exported' target flags supplied by the caller. Returns {satisfied, deficiency, causes, disclosures}."""
    causes, disclosures = [], []
    rel, minr = req["relation"], req["minResolution"]
    entry = view.get(rel)
    if entry is None:
        causes.append("required-relation-missing")
    else:
        if not ladder_ok(rel, minr) or not ladder_ok(rel, entry["resolution"]) or ladder_index(rel, entry["resolution"]) < ladder_index(rel, minr):
            if entry.get("rungUnavailableBecause") in ("language-tier-unsupported", "provider-unavailable", "input-closure-incomplete", "budget-exhausted"):
                causes.append(entry["rungUnavailableBecause"])
            else:
                causes.append("required-relation-missing")
        if entry["confidenceMillionths"] < req.get("minConfidenceMillionths", 0):
            causes.append("confidence-floor-unmet")
        if rel == "types" and req.get("derivationPolicy", "any") == "declared-only" and "compiler-inferred" in entry["derivationKinds"]:
            causes.append("derivation-policy-unmet")
        if req["completeness"] == "complete" and entry["coverage"] != "complete":
            causes.append(entry["deficiency"] if entry["deficiency"] else "required-relation-missing")
        if req["quantifier"] == "universal-negative":
            st = entry["resolutionCompleteness"]["state"]
            if st in ("partial", "not-attempted"):
                causes.append("resolution-incomplete")
            elif st == "incomplete" or entry.get("targetAffected"):
                if req["unresolvedEdgePolicy"] == "forbid":
                    causes.append("resolution-incomplete")
                else:
                    disclosures.append({"unresolved-edges": entry["resolutionCompleteness"]["unresolvedEdgeCount"],
                                        "classes": entry["resolutionCompleteness"]["unresolvedEdgeClasses"]})
            if entry.get("targetExported") and entry["closedWorld"]["exportsClosed"] != "closed":
                if req["externalConsumerPolicy"] == "forbid":
                    causes.append("external-consumers-unknown")
                else:
                    disclosures.append({"external-consumers": entry["closedWorld"]["exportsClosed"]})
    if depth < 4:
        for dep in DEPENDS_ON.get(rel, []):
            sub = dict(req, relation=dep["relation"], minResolution=dep["minResolution"])
            if req["quantifier"] == "existential":
                sub["completeness"] = "partial-ok"
            r = sufficiency_v2(sub, view, depth + 1)
            causes += r["causes"]
            disclosures += r["disclosures"]
    uniq = []
    for c in causes:
        if c not in uniq:
            uniq.append(c)
    if uniq:
        best = min(uniq, key=lambda c: PRECEDENCE.index(c) if c in PRECEDENCE else len(PRECEDENCE))
        return {"satisfied": False, "deficiency": best, "causes": uniq, "disclosures": disclosures}
    return {"satisfied": True, "deficiency": None, "causes": [], "disclosures": disclosures}
