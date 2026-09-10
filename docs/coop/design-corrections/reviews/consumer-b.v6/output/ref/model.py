"""Independent reconstruction helpers: CAS store, identity minting, derived
relation/rung applicability table, syntax capability law, clones dialect law.

Derived only from the subject kit's normative text and machine-readable
registries. No author model was read.
"""
import hashlib, json, os, sys, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from osip import (C, H, raw, rawbytes, frame, Refuse, cve1, capability_manifest_id,
                  body_identity, l0_payload, token_stream_payload, longest_suffix,
                  check_order)

KIT = "/tmp/opensip-design-corrections/consumer-b.v6/subject"


def load(rel):
    with open(os.path.join(KIT, rel), "rb") as f:
        return f.read()


def loadj(rel):
    return json.loads(load(rel))


IDS = loadj("docs/coop/design-corrections/foundation/identity-schemas.v2.json")
NAT = loadj("docs/coop/design-corrections/native/native-evidence.schemas.v2.json")
RELDOC_BYTES = load("docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json")
RELDOC = json.loads(RELDOC_BYTES)
NATDOC_BYTES = load("docs/coop/design-corrections/native/native-evidence.schemas.v2.json")
POLDOC_BYTES = load("docs/coop/design-corrections/workflows/schemas/policy-document.schema.json")
CAPDOMAINS = loadj("docs/coop/design-corrections/native/capability-manifest-domains.v2.json")
MATRIX = loadj("docs/coop/design-corrections/native/native-capability-matrix.v2.json")

RELREG = RELDOC["x-opensip-relation-registry"]["relations"]
DIGDOM = IDS["x-opensip-digest-domains"]
UNIVROWS = DIGDOM["domainSets"]["native-semantic-universe"]
CTXROWS = DIGDOM["domainSets"]["native-context"]
GRAMREG = NAT["x-opensip-grammar-capability-registry"]
DEFCAUSE = NAT["x-opensip-deficiency-cause-registry"]

# The exact registered payload-schema document digests (payload registry law:
# raw SHA-256 of the EXACT FULL document bytes).
RELATION_SCHEMA_DIGEST = rawbytes(RELDOC_BYTES)
COVERAGE_SCHEMA_DIGEST = rawbytes(NATDOC_BYTES)     # CoverageResultV3 lives here
POLICY_DOC_DIGEST = rawbytes(POLDOC_BYTES)

# RC-1: the closed five-member RESOLVED rung set (native sec.4.3 RC-1)
RESOLVED_RUNGS = {"resolved-target", "resolved-binding", "resolved-callee",
                  "checked", "from-resolved-calls"}

PREFIX = {
    "snapshot": "snapshot2", "closure": "closure2", "import": "import2",
    "plan": "plan2", "subject-scope": "scope2", "fact": "fact2",
    "coverage": "coverage2", "view": "view2", "execution-plan": "exec-plan2",
    "finding-fingerprint": "finding-key2", "finding": "finding2",
    "proof-bundle": "proof2", "semantic-evidence": "evidence2",
    "evaluation-seal": "seal2", "run": "run2", "cache-key": "cache2",
    "regeneration-key": "regen2", "policy-derivation": "policy-derivation2",
}


# ---------------------------------------------------------------- derived table

def registered_pairs():
    """The complete registered (relation, rung) table with RC-1 applicability,
    coverage totality, anchor class and universe rule, derived from the single
    ladder authority."""
    rows = []
    for rel in sorted(RELREG):
        r = RELREG[rel]
        for idx, rung in enumerate(r["ladder"]):
            resolved = rung in RESOLVED_RUNGS
            rows.append({
                "relation": rel, "rung": rung, "ladderIndex": idx,
                "isResolvedRung": resolved,
                "rcState": ("one of complete|incomplete|partial|not-attempted"
                            if resolved else "not-applicable"),
                "attemptedMustBe": (None if resolved else False),
                "unresolvedEdgeCountMustBe": (None if resolved else 0),
                "unresolvedEdgeClassesMustBe": (None if resolved else []),
                "anchorClass": r["anchorLaw"]["class"],
                "anchorCardinality": (r["anchorLaw"].get("cardinality")
                                      if "cardinality" in r["anchorLaw"]
                                      else f">= {r['anchorLaw']['minimum']}"),
                "universeRule": r["universeRule"],
                "subjectKind": r["subjectKind"],
                "coverageTotality": bool(r.get("coverageTotality")),
                "rungRequiredFields": r["rungs"].get(rung, {}).get("required", []),
                "rungForbiddenFields": r["rungs"].get(rung, {}).get("forbidden", []),
                "selector": r["selector"],
            })
    return rows


def rc0(relation, rung):
    """RC-0: the pair must be REGISTERED - rung must be on THAT relation's ladder."""
    if relation not in RELREG:
        raise Refuse("RC0_RELATION_UNREGISTERED", relation)
    if rung not in RELREG[relation]["ladder"]:
        raise Refuse("RC0_PAIR_UNREGISTERED", f"{relation}@{rung}")
    return True


def rc1(relation, rung, entry):
    rc0(relation, rung)
    rcp = entry["resolutionCompleteness"]
    if rung in RESOLVED_RUNGS:
        if rcp["state"] == "not-applicable":
            raise Refuse("RC1_NOT_APPLICABLE_ON_RESOLVED_RUNG", f"{relation}@{rung}")
    else:
        if rcp["state"] != "not-applicable":
            raise Refuse("RC1_RESOLUTION_CLAIM_ON_NON_RESOLVED_RUNG", rcp["state"])
        if rcp["attempted"] is not False:
            raise Refuse("RC1_ATTEMPTED_MUST_BE_FALSE", f"{relation}@{rung}")
        if rcp["unresolvedEdgeCount"] != 0:
            raise Refuse("RC1_COUNT_MUST_BE_ZERO", f"{relation}@{rung}")
        if rcp["unresolvedEdgeClasses"] != []:
            raise Refuse("RC1_CLASSES_MUST_BE_EMPTY", f"{relation}@{rung}")
    return True


def rc2(entry, admitted_unresolved_edges_in_examined_set):
    """RC-2 as corrected by native sec.4.3."""
    rcp = entry["resolutionCompleteness"]
    st, att = rcp["state"], rcp["attempted"]
    ex, term = rcp["examinedExhaustive"], rcp["stageTerminal"]
    n = admitted_unresolved_edges_in_examined_set
    if st == "not-applicable":
        return True
    if st == "complete":
        ok = (att is True and ex is True and term == "complete" and n == 0)
        if not ok:
            raise Refuse("RC2_COMPLETE_PRECONDITION", json.dumps(rcp))
    elif st == "incomplete":
        if not (att is True and ex is True and term == "complete" and n >= 1):
            raise Refuse("RC2_INCOMPLETE_PRECONDITION", json.dumps(rcp))
    elif st == "partial":
        if not (att is True and (term in {"unavailable", "budget-exhausted",
                                          "provider-fault", "cancelled", "crash"}
                                 or ex is False)):
            raise Refuse("RC2_PARTIAL_PRECONDITION", json.dumps(rcp))
    elif st == "not-attempted":
        if not (att is False and rcp["unresolvedEdgeCount"] == 0):
            raise Refuse("RC2_NOT_ATTEMPTED_PRECONDITION", json.dumps(rcp))
    return True


# --------------------------------------------------- syntax capability law

def suffix_owner(bundle, selected_ids, path):
    """Path support decided by the SELECTED grammar ROWS and their own suffixes;
    longest match over the union of the selected rows' suffixes."""
    owned = {}
    for g in bundle["grammars"]:
        if g["grammarId"] in selected_ids:
            for s in g["suffixes"]:
                owned[s] = g
    s = longest_suffix(owned, path)
    return (owned[s] if s else None)


INVENTORY_CAPS = {"file@enumerated", "package@manifest-declared",
                  "vcs-change@vcs-reported"}


def syntax_fact_admissible(bundle, selected, relation, rung, anchor_paths):
    """Boundary (2): every anchor path read by a selected grammar bearing the
    relation@rung, EXCEPT inventory relations, which are exempt."""
    cap = f"{relation}@{rung}"
    if cap in INVENTORY_CAPS:
        return True, None
    for p in anchor_paths:
        g = suffix_owner(bundle, selected, p)
        if g is None or cap not in GRAMREG["languages"][g["languageId"]]["capabilities"]:
            return False, ("SYNTAX_CAPABILITY_UNSUPPORTED_FACT", p, cap)
    if not anchor_paths:
        return False, ("SYNTAX_CAPABILITY_UNSUPPORTED_FACT", "<unanchored>", cap)
    return True, None


def syntax_scope_available(bundle, selected, relation, rung, extent, subjects,
                           subject_kind):
    """Boundary (3): judged on the committed examined extent.
    Inventory capabilities are ALWAYS available. A source-path relation is judged
    on its own subjects; a symbol relation on the coarser extent question."""
    cap = f"{relation}@{rung}"
    if cap in INVENTORY_CAPS:
        return True, None
    if subject_kind == "source-path":
        for p in subjects:
            g = suffix_owner(bundle, selected, p)
            if g is None or cap not in GRAMREG["languages"][g["languageId"]]["capabilities"]:
                return False, ("SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE", p, cap)
        return True, None
    # symbol relation: does any selected grammar bear this capability over the extent
    for p in extent:
        g = suffix_owner(bundle, selected, p)
        if g and cap in GRAMREG["languages"][g["languageId"]]["capabilities"]:
            return True, None
    return False, ("SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE", "<extent>", cap)


UNAVAILABLE_PAIR = {"deficiency": "language-tier-unsupported",
                    "nativeCause": "capability-missing"}


# ------------------------------------------------------ clones dialect law

def rust_dialect(ownership, edition_map, anchor_path):
    """native sec.11 selection law, in its published order, each step its own cause."""
    if ownership is None:
        raise Refuse("BODY_LANGUAGE_OWNERSHIP_REQUIRED", anchor_path)
    if ownership["enumeration"] == "partial":
        raise Refuse("BODY_LANGUAGE_OWNER_UNENUMERATED", anchor_path)
    rows = [o for o in ownership["ownership"] if o["path"] == anchor_path]
    if not rows:
        raise Refuse("BODY_LANGUAGE_OWNER_NOT_COMPILED", anchor_path)
    units = {u["unitId"]: u for u in ownership["units"]}
    sel = set(ownership["selectedUnitIds"])
    owners = [units[o["unitId"]] for o in rows if o["unitId"] in sel]
    if not owners:
        raise Refuse("BODY_LANGUAGE_OWNER_NOT_SELECTED", anchor_path)
    eff = set()
    for u in owners:
        eff.add(u["targetEdition"] if u["targetEdition"] is not None
                else edition_map[u["crateName"]])
    if len(eff) != 1:
        raise Refuse("BODY_LANGUAGE_OWNER_AMBIGUOUS",
                     f"{anchor_path}:{sorted(eff)}")
    return {"edition": eff.pop()}


def unit_id(marker_path, target_kind, target_name):
    return "sha256:" + H("native.compilation-unit.v1",
                         {"schemaVersion": 1, "markerPath": marker_path,
                          "targetKind": target_kind, "targetName": target_name})


def ts_variant(path):
    tbl = UNIVROWS["native.semantic-universe.typescript.v2"]["languageVersionBinding"]["dialect"]["table"]
    s = longest_suffix(tbl, path)
    if s is None:
        raise Refuse("BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN", path)
    return tbl[s]


def syntax_variant(path):
    tbl = UNIVROWS["native.semantic-universe.syntax.v2"]["languageVersionBinding"]["dialect"]["table"]
    s = longest_suffix(tbl, path)
    if s is None:
        raise Refuse("BODY_LANGUAGE_GRAMMAR_VARIANT_UNKNOWN", path)
    return tbl[s]


def body_language_id(universe_domain, anchor_path):
    row = UNIVROWS[universe_domain]["languageVersionBinding"]
    d = row["dialect"]
    if d["form"] == "closed-suffix-table":
        s = longest_suffix(d["table"], anchor_path)
        if s is None:
            raise Refuse(d["onUnknown"], anchor_path)
        return row["bodyLanguageByVariant"][d["table"][s]]
    return row["bodyLanguage"]


def body_language_version(universe_domain, context, universe, anchor_path,
                          ownership=None):
    """The DERIVED body-language-version record, rebuilt per the domain row's
    languageVersionBinding. Never accepted from a producer."""
    row = UNIVROWS[universe_domain]["languageVersionBinding"]
    rec = {"schemaVersion": 1,
           "languageId": body_language_id(universe_domain, anchor_path)}
    for fld, spec in row["fields"].items():
        if "const" in spec:
            rec[fld] = spec["const"]
        else:
            assert spec["source"] == "native-context"
            v = context
            for p in spec["path"]:
                v = v[p]
            rec[fld] = v
    d = row["dialect"]
    if d["form"] == "closed-suffix-table":
        s = longest_suffix(d["table"], anchor_path)
        if s is None:
            raise Refuse(d["onUnknown"], anchor_path)
        rec["dialect"] = {d["key"]: d["table"][s]}
    elif d["form"] == "selected-compilation-target-edition":
        rec["dialect"] = rust_dialect(ownership, universe["edition"], anchor_path)
    else:
        raise Refuse("DIALECT_FORM_UNKNOWN", d["form"])
    return rec


# ------------------------------------------------------------------ CAS store

class Store:
    def __init__(self):
        self.cas = {}                # digest -> bytes
        self.kind = {}               # digest -> label

    def put_blob(self, b, label="blob"):
        d = rawbytes(b)
        self.cas[d] = b
        self.kind.setdefault(d, label)
        return d

    def put_record(self, rec, label="record"):
        """canonical-record retention: retain C(record) under raw SHA-256."""
        return self.put_blob(C(rec), label)

    def put_framed(self, domain, rec, label=None):
        """h-identity retention: retain the exact H PREIMAGE FRAME under H."""
        fr = frame(domain, rec)
        d = hashlib.sha256(fr).hexdigest()
        self.cas[d] = fr
        self.kind.setdefault(d, label or ("frame:" + domain))
        return d

    def mint(self, domain, rec, label=None):
        d = self.put_framed(domain, rec, label)
        return f"{PREFIX[domain]}:{d}" if domain in PREFIX else d

    def has(self, digest):
        return digest in self.cas

    def reframe_check(self, digest, domain, record_validator=None):
        """Frame admission is exact: literal prefix, domain member, declared
        length equal to the remainder, remainder byte-identical to C of its own
        parse, payload valid under the record the domain set registers."""
        if digest not in self.cas:
            raise Refuse("EVIDENCE_UNAVAILABLE", digest)
        b = self.cas[digest]
        pre = b"opensip.product.v1\x00"
        if not b.startswith(pre):
            raise Refuse("FRAME_PREFIX", digest)
        rest = b[len(pre):]
        i = rest.index(b"\x00")
        dom = rest[:i].decode("ascii")
        if dom != domain:
            raise Refuse("FRAME_DOMAIN", f"{dom}!={domain}")
        n = struct.unpack(">Q", rest[i + 1:i + 9])[0]
        payload = rest[i + 9:]
        if len(payload) != n:
            raise Refuse("FRAME_LENGTH", str(n))
        try:
            parsed = json.loads(payload.decode("utf-8"))
        except Exception as ex:
            raise Refuse("FRAME_PAYLOAD_NOT_PARSEABLE", type(ex).__name__)
        if C(parsed) != payload:
            raise Refuse("FRAME_NOT_CANONICAL", digest)
        if record_validator:
            record_validator(parsed)
        if hashlib.sha256(b).hexdigest() != digest:
            raise Refuse("FRAME_DIGEST", digest)
        return parsed
