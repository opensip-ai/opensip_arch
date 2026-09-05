#!/usr/bin/env python3
"""Retained executable checker for the fact-identity contract.

Three of the nine v1 findings were critical, and two of them are recurrences of
errors this exercise has already made once:

  B-FI-05  the artifact listed what the Rule API does not hand you and called that
           an absence of ambient authority. A narrow handle does not confine LINKED
           code, which reaches the same capabilities through its own imports,
           transitive dependencies, module globals or an injected collaborator.
           Third occurrence of Error 2. FI-CAP-CLAIM refuses the absence wording.
  B-FI-01  "the ladder is reversible because levels are additive". Additivity
           avoids false net-new findings; it does not preserve the user's ratchet.
           FI-CT enforces the transition protocol that replaced the claim.
  B-FI-09  levels were named but no byte-level construction was published, so two
           producers could implement different hashes and both claim conformance.

  FI-CAP        a level a language cannot implement reports a FACT-PLANE deficiency
  FI-CAP-CLAIM  no absence-of-authority wording survives; FI-07 stays unimplementable
  FI-CT         custody transitions require dual-emit, acceptance, and a witness or
                an INDETERMINATE comparison
  FI-CANON      canonicalisation is published with framing, domain separation and a
                golden-corpus requirement per language in the matrix
  FI-RECORD     normalized body identity and generic FACT-ID-V1 are exact, distinct,
                host-joined contracts rather than aliases
  FI-ANCHOR     the host validates anchors; the claim is "cannot MINT", not
                "cannot influence"
  FI-BUDGET     only deterministic budgets define outcomes; exhaustion is transactional
  FI-TM         every threatModelRef resolves in the live threat model
  FI-DIS        no sealed property is discharged by a non-implementable test
  FI-FREEZE     byte grammar is fixed; corpora are evidence; imperative authority excluded

Usage: python3 artifacts/check-fact-identity.py [contract]   ·   --selftest
Exit:  0 clean · 1 findings · 2 IO error
"""
from __future__ import annotations
import copy, json, re, sys, pathlib

BINDING = "fact-identity-policy.v2.json"
CLOSURE = "fact-identity-policy.freeze-closure-coordinator.v1.json"
PRODUCT = "product-dispositions.v1.json"
FP = "fact-plane.v1.json"
TM = "threat-model.v3.json"
HERE = pathlib.Path(__file__).resolve().parent
TOTALITY_ROOT_CASES = (
    ("string", "hostile-root"),
    ("null", None),
    ("list", []),
    ("empty-object", {}),
)
MALFORMED_SHAPE_EXCEPTIONS = (
    AttributeError, IndexError, KeyError, StopIteration, TypeError, ValueError,
)

# Wording that asserts a capability BOUNDARY rather than an API surface.
ABSENCE_WORDING = re.compile(
    r"\b(no reachable|has no ambient|absence of ambient|cannot reach|denied at runtime)\b", re.I)


class DuplicateKeyError(ValueError):
    """A JSON object carried the same key twice. Named, never silently kept."""


def _no_duplicate_keys(pairs):
    """object_pairs_hook that refuses duplicates and NAMES the key.

    json.loads keeps the LAST of a duplicated key, so a contract can read one way
    to a human and another to every FI-* gate below while the parsed object stays
    byte-identical to the honest one — a digest check cannot see it, because the
    bytes really are what they claim to be. The gates run on the parsed value.
    The key is named so an operator learns not just that a file is bad but where.
    """
    seen = {}
    for k, v in pairs:
        if k in seen:
            raise DuplicateKeyError(f"duplicate JSON key {k!r}")
        seen[k] = v
    return seen


def loads_strict(text):
    """The only JSON entry point in this file. One place to keep hooked."""
    return json.loads(text, object_pairs_hook=_no_duplicate_keys)


def load(n):
    p = HERE / n
    return loads_strict(p.read_text()) if p.exists() else None


def tm_ids(tm: dict) -> set[str]:
    ids = set()
    for k in ("assets", "primaryRisks", "findings", "requiredProperties",
              "conditionalAdversaries", "nonGoals", "trustBoundaries", "residualRisks"):
        v = tm.get(k)
        if isinstance(v, list):
            ids |= {x["id"] for x in v if isinstance(x, dict) and "id" in x}
    return ids


def validate_level(fx: dict, c: dict, fp_defs: set[str]) -> list[tuple[str, str]]:
    """A declared capability plus its Coverage consequence -> violations."""
    errs = []
    cap, defc = fx["capability"], fx.get("expectDeficiency")
    if cap == "unavailable":
        if not defc:
            errs.append(("FI-CAP", f"{fx['language']}/{fx['level']} is unavailable but "
                                   f"reports no deficiency — silent approximation"))
        elif fp_defs and defc not in fp_defs:
            errs.append(("FI-CAP", f"deficiency '{defc}' is not in the fact-plane "
                                   f"vocabulary — a Coverage state with no way to terminate"))
    elif defc:
        errs.append(("FI-CAP", f"{fx['language']}/{fx['level']} is '{cap}' yet reports "
                               f"deficiency '{defc}'"))
    return errs


def validate_transition(fx: dict) -> list[tuple[str, str]]:
    """A custody transition -> violations. B-FI-01 / B-FI-02."""
    errs = []
    if fx["change"] == "add-level":
        if fx.get("comparison") != "unaffected":
            errs.append(("FI-CT", "an additive level must leave comparison unaffected"))
        return errs
    if not fx.get("dualEmit"):
        errs.append(("FI-CT", "algorithm change without a dual-emit window"))
    if not fx.get("userAcceptance"):
        errs.append(("FI-CT", "algorithm change without explicit user acceptance"))
    if not fx.get("witness") and fx.get("comparison") != "indeterminate":
        errs.append(("FI-CT", f"algorithm change with no migration witness claims a "
                              f"'{fx.get('comparison')}' comparison — nothing supports a "
                              f"mapping, so the honest outcome is indeterminate"))
    return errs


def _check(c: dict, fp: dict | None, tm: dict | None,
           closure: dict | None = None, product: dict | None = None) -> list[str]:
    f: list[str] = []
    fp_defs = set(fp["deficiencyVocabulary"]["values"]) if fp else set()
    if fp is None:
        f.append(f"FI-CAP: could not load {FP} — deficiency vocabulary unverified")

    # ---- FI-CAP-CLAIM: the absence claim must stay retracted (B-FI-05) ----
    blob = json.dumps(c)
    fi07 = next((t for t in c["conformanceTests"] if t["id"] == "FI-07"), None)
    if fi07 is None:
        f.append("FI-CAP-CLAIM: FI-07 is absent — the capability question cannot silently "
                 "disappear")
    else:
        if fi07.get("implementable"):
            f.append("FI-CAP-CLAIM: FI-07 is marked implementable, but no capability-"
                     "restricted runtime exists (ARCH.PROBE-CONTRACT is REOPENED). For "
                     "LINKED code a dependency audit is an integrity control, not a "
                     "boundary — this is Error 2")
        if not (fi07.get("requiresMechanism") or fi07.get("requiresHarness")):
            f.append("FI-CAP-CLAIM: FI-07 is unimplementable and names no blocker")
    tc = c.get("theCapabilityClaim", {})
    if "accurateClaim" not in tc:
        f.append("FI-CAP-CLAIM: no accurate capability claim is stated to replace the "
                 "retracted absence claim")
    elif ABSENCE_WORDING.search(tc.get("accurateClaim", "")):
        f.append("FI-CAP-CLAIM: the 'accurate' claim still uses absence wording")

    # ---- FI-DIS: no paper seals, and the capability property must not be discharged ----
    impl = {t["id"]: t.get("implementable", False) for t in c["conformanceTests"]}
    for prop in c["dischargeStatus"]["properties"]:
        for tid in prop["dischargedBy"]:
            if tid not in impl:
                f.append(f"FI-DIS: '{prop['property']}' names unknown test '{tid}'")
            elif not impl[tid]:
                f.append(f"FI-DIS: '{prop['property']}' is discharged by '{tid}', which is "
                         f"not implementable — a paper seal")
        if prop["status"] == "DISCHARGED" and not prop["dischargedBy"]:
            f.append(f"FI-DIS: '{prop['property']}' claims DISCHARGED with no tests")

    # ---- FI-CAP: language matrix and its fixtures ----
    matrix = {m["language"]: m for m in c["languageCapability"]["matrix"]}
    for fx in c["levelFixtures"]:
        if fx["language"] not in matrix:
            f.append(f"{fx['id']}: language '{fx['language']}' is not in the matrix")
            continue
        errs = validate_level(fx, c, fp_defs)
        codes = {code for code, _ in errs}
        if fx["valid"] and errs:
            f.append(f"{fx['id']}: expected valid but got — {errs[0][1]}")
        elif not fx["valid"]:
            want = fx.get("violates")
            if not errs:
                f.append(f"{fx['id']}: expected REJECTION by {want} but it validated")
            elif want not in codes:
                f.append(f"{fx['id']}: rejected by {sorted(codes)}, not the named {want}")
    if not any(m[l] == "unavailable" for m in matrix.values() for l in ("L1", "L2", "L3")):
        f.append("FI-CAP: no language declares an unavailable level — the capability "
                 "tier is never exercised")

    # ---- FI-CT: custody transition fixtures ----
    for fx in c["transitionFixtures"]:
        errs = validate_transition(fx)
        codes = {code for code, _ in errs}
        if fx["valid"] and errs:
            f.append(f"{fx['id']}: expected valid but got — {errs[0][1]}")
        elif not fx["valid"]:
            want = fx.get("violates")
            if not errs:
                f.append(f"{fx['id']}: expected REJECTION by {want} but it validated")
            elif want not in codes:
                f.append(f"{fx['id']}: rejected by {sorted(codes)}, not the named {want}")
    ct = c["custodyTransition"]
    if "reversible" in json.dumps(ct).lower() and "not custody-reversible" not in json.dumps(ct).lower():
        f.append("FI-CT: the reversibility claim B-FI-01 falsified has reappeared")
    if ct["protocol"]["groupTransitionModel"].split(".")[0].strip().upper() != "MANY-TO-MANY":
        f.append("FI-CT: group transitions are not modelled many-to-many (B-FI-02)")

    # ---- FI-CANON: a published construction, not just level names ----
    canon = c.get("canonicalisationSchema", {})
    cblob = json.dumps(canon).lower()
    for need, why in (("length-prefixed", "framing must make distinct streams distinct"),
                      ("domain separation", "levels/languages must not collide"),
                      ("collisionpolicy", "a collision must be a declared host defect")):
        if need.replace(" ", "") not in cblob.replace(" ", ""):
            f.append(f"FI-CANON: canonicalisation omits '{need}' — {why}")
    if "goldenCorpusRequirement" not in canon:
        f.append("FI-CANON: no golden corpus is required, so two producers can differ and "
                 "both claim conformance (B-FI-09)")

    # ---- FI-RECORD: normalized body identity is not generic fact-record identity ----
    boundary = c.get("factRecordIdentityBoundaryV1") or {}
    body = boundary.get("normalizedBodyIdentity") or {}
    generic = boundary.get("genericFactRecordIdentity") or {}
    expected_profiles = [
        {"providerId": "rust-semantic", "language": "rust"},
        {"providerId": "typescript-semantic", "language": "typescript"},
    ]
    fp_record = (fp or {}).get("factRecordContractV1") or {}
    fp_fact_id = fp_record.get("factIdContract") or {}
    fp_registry = fp_record.get("relationPayloadSchemaRegistryV1") or {}
    fp_mapping = fp_record.get("candidateToAdmittedMapping") or {}
    if boundary.get("id") != "opensip.fact-record-identity-boundary.v1" or \
            body.get("contractId") != "opensip.normalized-body-identity.v1" or \
            generic.get("contractId") != "opensip.fact-id.v1" or \
            body.get("source") != "fact-identity-policy.v2.json#canonicalisationSchema" or \
            generic.get("source") != \
            "fact-plane.v1.json#factRecordContractV1.factIdContract" or \
            generic.get("relationRegistrySource") != \
            "fact-plane.v1.json#factRecordContractV1.relationPayloadSchemaRegistryV1" or \
            generic.get("candidateMappingSource") != \
            "fact-plane.v1.json#factRecordContractV1.candidateToAdmittedMapping":
        f.append("FI-RECORD: fact-record/body-identity boundary identifiers or joins drifted")
    if canon.get("contractId") != body.get("contractId") or \
            canon.get("byteGrammar", {}).get("domainTag") != body.get("domainTag") or \
            canon.get("outputRepresentation") != body.get("outputRepresentation"):
        f.append("FI-RECORD: normalized body identity does not join its live byte grammar")
    if fp_fact_id.get("id") != generic.get("contractId") or \
            fp_fact_id.get("owner") != generic.get("owner") or \
            fp_registry.get("id") != "opensip.relation-payload-registry.v1" or \
            fp_mapping.get("id") != "opensip.fact-candidate-admission.v1" or \
            generic.get("domainTag") != "opensip.fact-id\0":
        f.append("FI-RECORD: generic FACT-ID-V1 does not join the live host-owned contract")
    if body.get("contractId") == generic.get("contractId") or \
            body.get("domainTag") == generic.get("domainTag"):
        f.append("FI-RECORD: normalized body identity and generic FACT-ID-V1 are aliased")
    clone = boundary.get("clonePayloadJoin") or {}
    clone_schema = (fp_registry.get("schemas") or {}).get("clones") or {}
    if clone != {
        "relation": "clones",
        "schemaId": "opensip.relation.clones.v1",
        "field": "bodyIdentity",
        "fieldType": "Sha256Text",
        "rule": "The normalized body identity is payload data inside a clones fact. FACT-ID-V1 wraps the complete clone fact and can never equal or substitute for bodyIdentity by type or domain.",
    } or clone_schema.get("schemaId") != clone.get("schemaId") or \
            (clone_schema.get("fields") or {}).get("bodyIdentity") != clone.get("fieldType"):
        f.append("FI-RECORD: clones payload does not carry body identity as typed nested data")
    if boundary.get("providerProfiles") != expected_profiles or \
            fp_record.get("providerProfiles") != expected_profiles:
        f.append("FI-RECORD: canonical TypeScript/Rust provider profile join drifted")
    preimage_names = {x.get("name") for x in fp_fact_id.get("preimageFields", [])}
    if "canonicalRelationPayload" not in preimage_names or "requestId" in preimage_names or \
            "RequestId" in preimage_names:
        f.append("FI-RECORD: generic FactId omits admitted payload or admits RequestId")

    # ---- FI-ANCHOR: cannot MINT, and the host validates ----
    av = c.get("anchorValidation", {})
    # Check the CLAIM field, not the whole blob: the v1Defect narrative also contains
    # the phrase "cannot MINT", so a blob search passed while the claim itself had been
    # widened back to the overclaim. A checker must read the field that binds.
    claim = av.get("accurateClaim", "").lower()
    if "cannot mint" not in claim:
        f.append("FI-ANCHOR: accurateClaim is not narrowed to 'cannot mint' (B-FI-06)")
    if re.search(r"cannot (compute or )?influence", claim):
        f.append("FI-ANCHOR: accurateClaim re-asserts 'cannot influence' — a rule chooses "
                 "its anchors and can destabilise its own identities (B-FI-06)")
    if len(av.get("hostObligations", [])) < 3:
        f.append("FI-ANCHOR: too few host obligations to make anchor validation real")
    if "residual" not in av:
        f.append("FI-ANCHOR: the residual instability a rule can still cause is not stated")

    # ---- FI-BUDGET: deterministic budgets define semantics ----
    bm = c["budgetModel"]
    if "transactionality" not in bm:
        f.append("FI-BUDGET: exhaustion is not transactional — different scheduling would "
                 "authorise different partial prefixes (B-FI-07)")
    wall = [d for d in bm["dimensions"] if d["budget"] == "wallClock"]
    if not wall:
        f.append("FI-BUDGET: no wall-clock dimension declared")
    elif wall[0]["class"] != "host-safety-backstop-only":
        f.append("FI-BUDGET: wall clock is treated as a semantic limit; it varies by "
                 "machine and cannot define a valid result")
    if not any(d["class"] == "deterministic" for d in bm["dimensions"]):
        f.append("FI-BUDGET: no deterministic budget defines outcomes")

    # ---- FI-TM: citations resolve in the live model ----
    if tm is None:
        f.append(f"FI-TM: could not load {TM} — citations unverified")
    else:
        live = tm_ids(tm)
        refs = [(d.get("claim", "?"), r) for d in c["decisionDependencies"]
                for r in d.get("refs", [])]
        refs += [(k, v["threatModelRef"]) for k, v in c.items()
                 if isinstance(v, dict) and "threatModelRef" in v]
        refs += [(d["budget"], d["threatModelRef"]) for d in bm["dimensions"]
                 if "threatModelRef" in d]
        for where, ref in refs:
            if ref not in live:
                f.append(f"FI-TM: {where} cites threat-model id '{ref}', absent from the "
                         f"live model — paper compliance (B-FI-08)")

    # ---- FI-CAP matrix binding (R2-FI-02) ----
    supported = c["languageCapability"].get("supportedLanguages")
    if not supported:
        f.append("FI-CAP: supportedLanguages is absent — matrix is not a binding input (R2-FI-02)")
    else:
        if set(supported) != set(matrix):
            f.append(f"FI-CAP: supportedLanguages {sorted(supported)} != matrix languages "
                     f"{sorted(matrix)} (R2-FI-02)")
        shipping = c["languageCapability"].get("v1ShippingLanguages")
        if shipping != ["typescript", "rust"]:
            f.append("FI-CAP: v1ShippingLanguages must be exactly TypeScript and Rust; "
                     "matrix breadth is not product admission")
        elif not set(shipping).issubset(set(supported)):
            f.append("FI-CAP: v1ShippingLanguages is not a subset of supportedLanguages")
        # every matrix language/level needs a fixture
        fx_index = {(fx["language"], fx["level"]): fx
                    for fx in c["levelFixtures"] if fx.get("valid", True)}
        for lang, row in matrix.items():
            for level in ("L1", "L2", "L3"):
                if (lang, level) not in fx_index:
                    f.append(f"FI-CAP: no positive levelFixture for matrix cell "
                             f"{lang}/{level} (R2-FI-02)")
                else:
                    mcap = row[level]
                    fcap = fx_index[(lang, level)]["capability"]
                    if mcap == "full-provisional":
                        if fcap not in ("restricted", "full-provisional"):
                            f.append(f"FI-CAP: {lang}/{level} matrix is full-provisional but "
                                     f"fixture capability is '{fcap}'")
                    elif mcap != fcap:
                        f.append(f"FI-CAP: {lang}/{level} matrix '{mcap}' != fixture '{fcap}'")

    # ---- FI-DIS grades: DISCHARGED requires demonstration (R2-FI-01) ----
    rule = c["dischargeStatus"].get("rule", "")
    if "implementable:true alone is NOT discharge" not in rule and "DEMONSTRATED" not in rule:
        f.append("FI-DIS: discharge rule still equates implementable:true with discharge "
                 "(R2-FI-01)")
    for prop in c["dischargeStatus"]["properties"]:
        if prop["status"] == "DISCHARGED":
            if prop.get("evidenceGrade") != "DEMONSTRATED":
                f.append(f"FI-DIS: '{prop['property']}' is DISCHARGED without "
                         f"DEMONSTRATED evidenceGrade (R2-FI-01 / R2-FINAL-02)")
            if not prop.get("demonstrationEvidenceIds"):
                f.append(f"FI-DIS: '{prop['property']}' is DISCHARGED without retained "
                         f"demonstrationEvidenceIds (R2-FINAL-02)")

    # ---- FI-CANON framed preimage (R2-FI-03) ----
    bg = canon.get("byteGrammar") or {}
    if not bg:
        f.append("FI-CANON: byteGrammar is absent — domain components may be unframed (R2-FI-03)")
    else:
        pre = json.dumps(bg.get("domainSeparatedPreimage", [])).lower()
        if "len" not in pre and "length" not in pre and "u8" not in pre:
            f.append("FI-CANON: domainSeparatedPreimage is not length-prefixed (R2-FI-03)")
        if "forbidden" in bg and "concatenation" not in json.dumps(bg["forbidden"]).lower():
            f.append("FI-CANON: byteGrammar.forbidden does not ban unframed concatenation")
        for need in ("bodySpanBoundary", "levelVersionDefinition", "identifierEncoding",
                     "payloadEncodingByLevel", "tokenKindDefinition",
                     "tokenValueDefinition", "tokenEncoding",
                     "languageVersionDefinition"):
            if need not in bg:
                f.append(f"FI-CANON: byteGrammar omits '{need}' (R2-FI-03)")
        payloads = bg.get("payloadEncodingByLevel") or {}
        levels = {item.get("level") for item in c.get("normalisationLadder", {}).get(
            "levels", [])}
        if set(payloads) != levels:
            f.append("FI-CANON: payloadEncodingByLevel does not cover exactly the ladder")
        l0 = str(payloads.get("L0-verbatim", "")).lower()
        if "exact" not in l0 or "tokenisation is forbidden" not in l0:
            f.append("FI-CANON: L0 payload is not exact raw bytes with tokenisation forbidden")
        for level in ("L1-lexical", "L2-comment-insensitive",
                      "L3-identifier-insensitive"):
            if payloads.get(level) != "framedTokenStream":
                f.append(f"FI-CANON: {level} payload is not framedTokenStream")
        kind_def = bg.get("tokenKindDefinition", "").lower()
        if "registry" not in kind_def or "numeric enum ordinals are forbidden" not in kind_def:
            f.append("FI-CANON: token kinds are not bound to the level-version registry")
        level_version = bg.get("levelVersionDefinition", "").lower()
        if "raw 32-byte sha-256" not in level_version or "token-kind registry" not in level_version:
            f.append("FI-CANON: levelVersion does not commit the token-kind/transform spec")
        identifiers = bg.get("identifierEncoding") or {}
        if set(identifiers) != {"domainTag", "levelId", "levelVersion", "languageId",
                                "languageVersion"}:
            f.append("FI-CANON: identifierEncoding does not define every preimage component")
        elif "not hexadecimal" not in identifiers["levelVersion"]:
            f.append("FI-CANON: levelVersion bytes are ambiguous between raw and display form")
    # construction steps must exist and be non-empty
    steps = (canon.get("construction") or {})
    if not steps or any(not str(v).strip() for v in steps.values()):
        f.append("FI-CANON: construction steps missing or empty (R2-FI-03)")

    # ---- FI-CT witness minimum non-empty (R2-FI-06) ----
    wit = ct["protocol"].get("migrationWitness") or {}
    minimum = wit.get("minimum") or []
    if len(minimum) < 5:
        f.append("FI-CT: migrationWitness.minimum too thin for many-to-many transitions "
                 "(R2-FI-06)")
    need_fields = ["oldGroupIds", "newGroupIds", "edges", "acceptanceId"]
    blob = json.dumps(minimum).lower()
    for nf in need_fields:
        if nf.lower() not in blob:
            f.append(f"FI-CT: migrationWitness.minimum omits '{nf}' (R2-FI-06)")

    # ---- third-party exclusion (R2-FI-04) ----
    tc2 = c.get("theCapabilityClaim", {})
    if "thirdPartyImperativeRules" not in tc2:
        f.append("FI-CAP-CLAIM: third-party imperative rules not explicitly excluded until "
                 "restricted runtime (R2-FI-04)")
    elif "EXCLUDED" not in json.dumps(tc2["thirdPartyImperativeRules"]).upper():
        f.append("FI-CAP-CLAIM: thirdPartyImperativeRules does not say EXCLUDED")

    # ---- FI-FREEZE: the Phase 1B closure is a checked scope decision ----
    if closure is None:
        f.append(f"FI-FREEZE: could not load {CLOSURE} — seal scope/exclusions unverified")
    else:
        if closure.get("sealRecommendation", {}).get("verdict") != "SEAL-WITH-CHANGES":
            f.append("FI-FREEZE: coordinator verdict is not SEAL-WITH-CHANGES")
        arch = closure.get("v1Architecture") or {}
        ladder = arch.get("normalisationLadder") or {}
        contract_levels = [item.get("level") for item in c.get("normalisationLadder", {}).get(
            "levels", [])]
        if ladder.get("levels") != contract_levels:
            f.append("FI-FREEZE: closure level list differs from the binding ladder")
        if ladder.get("default") != c.get("normalisationLadder", {}).get("defaultLevel"):
            f.append("FI-FREEZE: closure default level differs from the binding ladder")
        if ladder.get("v1ShippingLanguages") != c.get("languageCapability", {}).get(
                "v1ShippingLanguages"):
            f.append("FI-FREEZE: closure v1 language set differs from the binding policy")
        closure_bytes = arch.get("canonicalBytes") or {}
        if closure_bytes.get("algorithm") != bg.get("algorithm"):
            f.append("FI-FREEZE: closure hash algorithm differs from byteGrammar")
        if closure_bytes.get("domainTag") != bg.get("domainTag"):
            f.append("FI-FREEZE: closure domainTag differs from byteGrammar")
        payload_rule = closure_bytes.get("payloadRule", "").lower()
        if "l0 payload is exact raw" not in payload_rule or "never tokenised" not in payload_rule:
            f.append("FI-FREEZE: closure does not preserve verbatim L0 payload bytes")
        exclusions = {item.get("id"): item for item in closure.get("v1Exclusions", [])}
        imperative = exclusions.get("FI-PARK-IMPERATIVE-AUTHORITY") or {}
        if imperative.get("status") != "EXCLUDED-UNTIL-RESTRICTED-RUNTIME":
            f.append("FI-FREEZE: imperative authority is not excluded until a runtime exists")
        if imperative.get("blockedOn") != "ARCH.PROBE-CONTRACT":
            f.append("FI-FREEZE: imperative authority is not parked on ARCH.PROBE-CONTRACT")
        narrow = imperative.get("narrowTruth", "")
        if not all(term in narrow for term in ("TCB", "integrity control", "not confinement")):
            f.append("FI-FREEZE: closure does not state the linked-first-party TCB narrow truth")
        impl = closure.get("implementationEvidence") or {}
        if impl.get("status") != "SPECIFIED-NOT-DEMONSTRATED":
            f.append("FI-FREEZE: corpus evidence is not SPECIFIED-NOT-DEMONSTRATED")
        if "not a remaining choice" not in impl.get("freezeRule", ""):
            f.append("FI-FREEZE: closure does not separate corpus evidence from byte-grammar choice")
        patch = closure.get("claimRegisterPatch") or {}
        if patch.get("claimId") != "FACT-IDENTITY":
            f.append("FI-FREEZE: closure does not target claim-register FACT-IDENTITY")
        patch_set = patch.get("set") or {}
        if patch_set.get("sealBlockers") != []:
            f.append("FI-FREEZE: closure does not clear architecture sealBlockers")
        if len(patch_set.get("nonBlockingResiduals", [])) != 2:
            f.append("FI-FREEZE: closure must name exactly corpus and imperative residuals")
        if "UNREVIEWED" in c.get("status", "").upper() or "NOT REVIEWED" in c.get(
                "reviewStatus", "").upper():
            f.append("FI-FREEZE: binding metadata still says unreviewed")
        if c.get("peerReviewRequired"):
            f.append("FI-FREEZE: binding still carries unresolved peerReviewRequired entries")

    if product is None:
        f.append(f"FI-FREEZE: could not load {PRODUCT} — product exclusion posture unverified")
    else:
        decisions = product.get("decisions") or {}
        required_choices = {
            "P-1": "NO_ECOSYSTEM_DEPTH_FOR_V1",
            "P-2": "NARROW_CONTRIBUTION_ONTOLOGY",
            "PUBLIC-RULE-IR": "DO_NOT_FREEZE_FOR_V1",
            "G3-SUBSTRATE": "DELIVERY_V2_BINDING",
        }
        for decision, choice in required_choices.items():
            if (decisions.get(decision) or {}).get("choice") != choice:
                f.append(f"FI-FREEZE: product decision {decision} is not '{choice}'")

    return f


def check(c: object, fp: dict | None, tm: dict | None,
          closure: dict | None = None, product: dict | None = None) -> list[str]:
    """Total contract boundary for malformed but successfully parsed JSON."""
    if not isinstance(c, dict) or not c:
        return ["FI-TOTALITY-ROOT: contract root must be a non-empty object"]
    if not isinstance(c.get("conformanceTests"), list):
        return ["FI-TOTALITY-SHAPE: conformanceTests must be an array"]
    try:
        return _check(c, fp, tm, closure, product)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [f"FI-TOTALITY-EXCEPTION: malformed contract shape "
                f"({type(exc).__name__})"]


# --------------------------------------------------------------------------
def _m_reassert_absence(c):
    for t in c["conformanceTests"]:
        if t["id"] == "FI-07":
            t["implementable"] = True

def _m_discharge_capability(c):
    for p in c["dischargeStatus"]["properties"]:
        if p["property"].startswith("imperative rules hold no"):
            p["dischargedBy"] = ["FI-07"]
            p["status"] = "DISCHARGED"

def _m_silent_unavailable(c):
    for fx in c["levelFixtures"]:
        if fx["id"] == "reject-unavailable-without-deficiency":
            fx["valid"] = True

def _m_deficiency_outside_factplane(c):
    for fx in c["levelFixtures"]:
        if fx["id"] == "reject-deficiency-outside-factplane":
            fx["valid"] = True

def _m_transition_without_acceptance(c):
    for fx in c["transitionFixtures"]:
        if fx["id"] == "reject-algorithm-change-without-acceptance":
            fx["valid"] = True

def _m_claim_mapping_without_witness(c):
    for fx in c["transitionFixtures"]:
        if fx["id"] == "reject-silent-reidentification":
            fx["valid"] = True

def _m_one_to_one_groups(c):
    c["custodyTransition"]["protocol"]["groupTransitionModel"] = "ONE-TO-ONE."

def _m_drop_domain_separation(c):
    c["canonicalisationSchema"]["construction"]["step4"] = "Hash the framed token stream."

def _m_wall_clock_semantic(c):
    for d in c["budgetModel"]["dimensions"]:
        if d["budget"] == "wallClock":
            d["class"] = "deterministic"

def _m_stale_tm(c):
    c["budgetModel"]["dimensions"][4]["threatModelRef"] = "F3"

def _m_widen_anchor_claim(c):
    c["anchorValidation"]["accurateClaim"] = "A rule cannot compute or influence a fingerprint."

def _m_paper_discharge(c):
    for p in c["dischargeStatus"]["properties"]:
        if p["status"] == "SPECIFIED":
            p["status"] = "DISCHARGED"
            p["evidenceGrade"] = "IMPLEMENTABLE_UNEXECUTED"
            break

def _m_demonstrated_without_evidence(c):
    for p in c["dischargeStatus"]["properties"]:
        if p["status"] == "SPECIFIED":
            p["status"] = "DISCHARGED"
            p["evidenceGrade"] = "DEMONSTRATED"
            p["demonstrationEvidenceIds"] = []
            break

def _m_desync_matrix_fixture(c):
    for m in c["languageCapability"]["matrix"]:
        if m["language"] == "typescript":
            m["L3"] = "unavailable"

def _m_delete_rust_row(c):
    c["languageCapability"]["matrix"] = [
        m for m in c["languageCapability"]["matrix"] if m["language"] != "rust"]
    # leave supportedLanguages stale intentionally? better delete from supported too to test row absence
    # actually: delete row but keep supportedLanguages listing rust
    c["languageCapability"]["supportedLanguages"] = ["typescript", "rust", "python", "go"]

def _m_admit_python_in_v1(c):
    c["languageCapability"]["v1ShippingLanguages"].append("python")

def _m_destroy_construction(c):
    c["canonicalisationSchema"]["construction"]["step1"] = ""

def _m_empty_witness_min(c):
    c["custodyTransition"]["protocol"]["migrationWitness"]["minimum"] = []

def _m_drop_byte_grammar(c):
    del c["canonicalisationSchema"]["byteGrammar"]

def _m_tokenise_l0(c):
    c["canonicalisationSchema"]["byteGrammar"]["payloadEncodingByLevel"][
        "L0-verbatim"] = "framedTokenStream"

def _m_numeric_token_kinds(c):
    c["canonicalisationSchema"]["byteGrammar"]["tokenKindDefinition"] = (
        "kind_id is the producer's u32 compiler enum ordinal")

def _m_drop_identifier_encoding(c):
    del c["canonicalisationSchema"]["byteGrammar"]["identifierEncoding"]


def _m_alias_generic_fact_id_to_body(c):
    boundary = c["factRecordIdentityBoundaryV1"]
    boundary["genericFactRecordIdentity"]["contractId"] = \
        boundary["normalizedBodyIdentity"]["contractId"]


def _m_alias_generic_fact_domain_to_body(c):
    boundary = c["factRecordIdentityBoundaryV1"]
    boundary["genericFactRecordIdentity"]["domainTag"] = \
        boundary["normalizedBodyIdentity"]["domainTag"]


def _m_drop_fact_record_identity_join(c):
    del c["factRecordIdentityBoundaryV1"]["genericFactRecordIdentity"][
        "candidateMappingSource"]


def _m_prefix_fact_record_provider(c):
    c["factRecordIdentityBoundaryV1"]["providerProfiles"][1]["providerId"] = \
        "provider.typescript-semantic"

MUTATIONS = [
    ("re-assert the absence-of-authority claim (B-FI-05 / Error 2)", _m_reassert_absence),
    ("discharge the capability property with an unbuilt test (FI-DIS)", _m_discharge_capability),
    ("let an unavailable level approximate silently (FI-CAP)", _m_silent_unavailable),
    ("emit a deficiency the fact plane cannot express (FI-CAP)", _m_deficiency_outside_factplane),
    ("change an algorithm without user acceptance (B-FI-01 / FI-CT)", _m_transition_without_acceptance),
    ("claim a group mapping with no witness (B-FI-02 / FI-CT)", _m_claim_mapping_without_witness),
    ("model group transitions one-to-one (B-FI-02)", _m_one_to_one_groups),
    ("drop domain separation from the hash (B-FI-09 / FI-CANON)", _m_drop_domain_separation),
    ("make wall clock a semantic limit (B-FI-07 / FI-BUDGET)", _m_wall_clock_semantic),
    ("cite a superseded threat-model id (B-FI-08 / FI-TM)", _m_stale_tm),
    ("widen 'cannot mint' back to 'cannot influence' (B-FI-06)", _m_widen_anchor_claim),
    ("paper-discharge unexecuted property (R2-FI-01)", _m_paper_discharge),
    ("claim DEMONSTRATED discharge without retained evidence (R2-FINAL-02)",
     _m_demonstrated_without_evidence),
    ("desync matrix cell from fixture (R2-FI-02)", _m_desync_matrix_fixture),
    ("delete rust matrix row (R2-FI-02)", _m_delete_rust_row),
    ("admit a non-v1 language from the capability matrix (FI-CAP)", _m_admit_python_in_v1),
    ("destroy construction step (R2-FI-03)", _m_destroy_construction),
    ("empty migration witness minimum (R2-FI-06)", _m_empty_witness_min),
    ("drop byteGrammar (R2-FI-03)", _m_drop_byte_grammar),
    ("tokenise the verbatim L0 payload (FI-CANON)", _m_tokenise_l0),
    ("use producer-local numeric token kinds (FI-CANON)", _m_numeric_token_kinds),
    ("drop identifier byte encodings (FI-CANON)", _m_drop_identifier_encoding),
    ("alias generic FACT-ID-V1 to normalized body identity (R5R-DLTS-02)",
     _m_alias_generic_fact_id_to_body),
    ("reuse the normalized-body domain for FACT-ID-V1 (R5R-DLTS-02)",
     _m_alias_generic_fact_domain_to_body),
    ("drop the exact candidate-to-fact identity join (R5R-DLTS-02)",
     _m_drop_fact_record_identity_join),
    ("alias a fact-record provider with provider.* (R5R-DLTS-05)",
     _m_prefix_fact_record_provider),
]


def _m_closure_changes_domain(c):
    c["v1Architecture"]["canonicalBytes"]["domainTag"] = "opensip.bodyhash.alternate"

def _m_closure_tokenises_l0(c):
    c["v1Architecture"]["canonicalBytes"]["payloadRule"] = (
        "Every level uses a producer token stream.")

def _m_closure_admits_imperative(c):
    c["v1Exclusions"][0]["status"] = "AVAILABLE-IN-V1"

def _m_closure_papers_corpus(c):
    c["implementationEvidence"]["status"] = "DEMONSTRATED"

def _m_closure_keeps_blocker(c):
    c["claimRegisterPatch"]["set"]["sealBlockers"] = ["golden corpus not run"]

CLOSURE_MUTATIONS = [
    ("change the sealed domain tag in closure (FI-FREEZE)", _m_closure_changes_domain),
    ("tokenise L0 in the freeze closure (FI-FREEZE)", _m_closure_tokenises_l0),
    ("admit imperative authority without a runtime (FI-FREEZE)",
     _m_closure_admits_imperative),
    ("paper-demonstrate absent corpus evidence (FI-FREEZE)", _m_closure_papers_corpus),
    ("leave implementation evidence as architecture blocker (FI-FREEZE)",
     _m_closure_keeps_blocker),
]


def _m_product_freezes_public_ir(p):
    p["decisions"]["PUBLIC-RULE-IR"]["choice"] = "FREEZE_PUBLIC_IR_FOR_V1"

PRODUCT_MUTATIONS = [
    ("freeze a public rule IR despite product exclusion (FI-FREEZE)",
     _m_product_freezes_public_ir),
]


def selftest(base, fp, tm, closure, product) -> int:
    pre = check(base, fp, tm, closure, product)
    if pre:
        print(f"REFUSING to self-test: the base contract has {len(pre)} finding(s), so "
              f"every mutation would be masked by them.")
        for x in pre[:5]:
            print("  -", x)
        return 1
    print("mutation self-test — each row must be REJECTED\n")
    escaped = 0
    for name, root in TOTALITY_ROOT_CASES:
        findings = check(copy.deepcopy(root), fp, tm, closure, product)
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  parsed-JSON root {name}")
        print(f"          {findings[0] if findings else 'NO FINDING — root survived'}")
    for name, mut in MUTATIONS:
        c = copy.deepcopy(base)
        mut(c)
        findings = check(c, fp, tm, closure, product)
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  {name}")
        print(f"          {findings[0] if findings else 'NO FINDING — mutation survived'}")
    for name, mut in CLOSURE_MUTATIONS:
        candidate = copy.deepcopy(closure)
        mut(candidate)
        findings = check(base, fp, tm, candidate, product)
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  {name}")
        print(f"          {findings[0] if findings else 'NO FINDING — mutation survived'}")
    for name, mut in PRODUCT_MUTATIONS:
        candidate = copy.deepcopy(product)
        mut(candidate)
        findings = check(base, fp, tm, closure, candidate)
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  {name}")
        print(f"          {findings[0] if findings else 'NO FINDING — mutation survived'}")
    print()
    if escaped:
        print(f"{escaped}/{len(MUTATIONS) + len(CLOSURE_MUTATIONS) + len(PRODUCT_MUTATIONS) + len(TOTALITY_ROOT_CASES)} "
              f"retained cases ESCAPED — the proof path is optional")
        return 1
    print(f"all {len(MUTATIONS) + len(CLOSURE_MUTATIONS) + len(PRODUCT_MUTATIONS)} "
          f"semantic mutations and {len(TOTALITY_ROOT_CASES)} root-shape cases rejected "
          f"— the proof path is load-bearing")
    return 0


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--selftest"]
    p = pathlib.Path(args[0]) if args else HERE / BINDING
    if not p.exists():
        print(f"missing contract: {p}", file=sys.stderr)
        return 2
    c = loads_strict(p.read_text())
    fp, tm, closure, product = load(FP), load(TM), load(CLOSURE), load(PRODUCT)
    if "--selftest" in sys.argv:
        return selftest(c, fp, tm, closure, product)
    f = check(c, fp, tm, closure, product)
    if not f:
        impl = sum(1 for t in c["conformanceTests"] if t.get("implementable"))
        tot = len(c["conformanceTests"])
        print(f"fact-identity OK — {p.name}, {len(c['levelFixtures'])} level + "
              f"{len(c['transitionFixtures'])} transition fixtures, FI-CAP / FI-CAP-CLAIM / "
              f"FI-CT / FI-CANON / FI-RECORD / FI-ANCHOR / FI-BUDGET / FI-TM / FI-DIS / "
              f"FI-FREEZE clean")
        print(f"  cross-checked against {FP}, {TM}, {CLOSURE}, and {PRODUCT}")
        print(f"  {impl}/{tot} conformance tests implementable; the capability property is "
              f"NOT DISCHARGED; corpora remain implementation evidence and imperative "
              f"authority is excluded")
        return 0
    print(f"{len(f)} finding(s) in {p.name}:")
    for x in f:
        print("  -", x)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
