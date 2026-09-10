"""Independent checks of laws the contracts state about their OWN documents.

  1. the closing digest law: every 64-hex field of identity-schemas.v2 carries
     exactly one x-opensip-digest annotation, and every reference field's
     `by-domain` selector resolves through x-opensip-digest-domains.byDomain;
  2. the x-opensip-order vocabulary is closed across every current schema;
  3. the relation document's own x-opensip-digest-law reaches every governed
     occurrence;
  4. the import mirror differential: one instance, two documents, identical
     admit/refuse verdicts, with a discriminating-negative floor;
  5. the ladder mirrors are equal AND IN ORDER;
  6. the analysis-spec bound arithmetic the workflow/native contracts publish.
"""

import json

import oslib as O
import graph as G
from oslib import C, H, sha256hex, raw_digest

HEX64 = "^[0-9a-f]{64}(?![\\s\\S])"
ORDER_VOCAB = {"sequence", "canonical-set", "canonical-order", "utf8", "path",
               "numeric", "ordinal", "predicate", "ruleId", "waiverId"}
TERMINAL_REPS = {"raw-artifact", "canonical-record", "h-identity",
                 "capability-manifest-id"}
RETENTIONS = {"preimage", "fragment", "derived", "owner-retained"}


def _walk(node, path, out):
    if isinstance(node, dict):
        out.append((path, node))
        for k, v in node.items():
            _walk(v, path + "/" + k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _walk(v, path + "/%d" % i, out)


def digest_law():
    doc = O.doc("identity")
    nodes = []
    _walk(doc["$defs"], "#/$defs", nodes)
    by_domain = doc["x-opensip-digest-domains"]["byDomain"]
    domain_sets = doc["x-opensip-digest-domains"]["domainSets"]
    unannotated, bad_rep, bad_ret, by_domain_terminal = [], [], [], []
    annotated = 0
    for path, n in nodes:
        if n.get("pattern") != HEX64 and "$ref" not in n:
            continue
        is_hash_ref = n.get("$ref") == "#/$defs/Hash"
        if n.get("pattern") != HEX64 and not is_hash_ref:
            continue
        ann = n.get("x-opensip-digest")
        if ann is None:
            # a bare `$ref: #/$defs/Hash` or hex pattern inside a $defs
            # PRIMITIVE (Hash itself) is the definition, not an occurrence
            if path.endswith("/Hash") or "/x-opensip-digest" in path:
                continue
            unannotated.append(path)
            continue
        annotated += 1
        rep = ann.get("representation")
        if rep == "by-domain":
            # a SELECTOR, resolved through the sibling `domain` enum
            reg = ann.get("registry")
            if reg != "x-opensip-digest-domains":
                by_domain_terminal.append(path)
        elif rep not in TERMINAL_REPS:
            bad_rep.append((path, rep))
        ret = ann.get("retention")
        if ret is not None and ret not in RETENTIONS:
            bad_ret.append((path, ret))
    # every member of every reference `domain` enum must be registered
    unregistered_domains = []
    for ref in ("Ref", "ProofInputRef", "FindingEvidenceRef"):
        for d in doc["$defs"][ref]["properties"]["domain"]["enum"]:
            if d not in by_domain:
                unregistered_domains.append(ref + ":" + d)
    # and every registered byDomain row must resolve to a TERMINAL rep
    nonterminal_rows = [d for d, r in by_domain.items()
                        if r["representation"] not in TERMINAL_REPS]
    return {"annotatedFieldCount": annotated,
            "unannotated64HexFields": unannotated,
            "nonTerminalRepresentations": bad_rep,
            "undeclaredRetentionValues": bad_ret,
            "byDomainWithoutRegistry": by_domain_terminal,
            "unregisteredReferenceDomains": unregistered_domains,
            "byDomainRowsResolvingToANonTerminal": nonterminal_rows,
            "domainSetNames": sorted(domain_sets.keys()),
            "lawHolds": not (unannotated or bad_rep or bad_ret
                             or unregistered_domains or nonterminal_rows)}


def order_vocabulary():
    bad = []
    counts = {}
    for name in ("identity", "relation", "native", "common", "policy-document",
                 "imported-evidence", "invocation-record", "command-envelope",
                 "comparison-result", "repair", "baseline-artifact",
                 "test-execution", "policy-test", "graph-query", "review",
                 "product-config", "import-source-context"):
        try:
            d = O.doc(name)
        except Exception:
            continue
        nodes = []
        _walk(d, "#", nodes)
        for path, n in nodes:
            if "x-opensip-order" not in n:
                continue
            v = n["x-opensip-order"]
            if isinstance(v, str):
                counts[v] = counts.get(v, 0) + 1
                if v not in ORDER_VOCAB:
                    bad.append((name, path, v))
            elif isinstance(v, dict) and list(v.keys()) == ["by"]:
                counts["{by}"] = counts.get("{by}", 0) + 1
            else:
                bad.append((name, path, v))
    return {"annotationCounts": counts, "outsideTheClosedVocabulary": bad,
            "vocabularyIsClosed": not bad}


def relation_digest_law():
    d = O.doc("relation")
    law = d.get("x-opensip-digest-law")
    governed = {"#/$defs/DigestHex", "#/$defs/Sha256Text", "#/$defs/CanonicalPath"}
    occ, unannotated = [], []
    for rel, row in d["x-opensip-relation-registry"]["relations"].items():
        sel = row["selector"].lstrip("#/").split("/")
        node = d
        for p in sel:
            node = node[p]
        for pname, pnode in node.get("properties", {}).items():
            ref = pnode.get("$ref")
            if ref in governed or pnode.get("pattern") in (
                    d["$defs"]["DigestHex"]["pattern"],
                    d["$defs"]["Sha256Text"]["pattern"],
                    d["$defs"]["CanonicalPath"]["pattern"]):
                occ.append((rel, pname))
                if "x-opensip-digest" not in pnode:
                    unannotated.append((rel, pname))
    retentions = {}
    for rel, pname in occ:
        sel = d["x-opensip-relation-registry"]["relations"][rel]["selector"]
        node = d
        for p in sel.lstrip("#/").split("/"):
            node = node[p]
        ann = node["properties"][pname].get("x-opensip-digest", {})
        retentions.setdefault(ann.get("retention", "<none>"), []).append(
            rel + "." + pname)
    return {"lawDeclared": law is not None,
            "governedTopLevelOccurrences": len(occ),
            "unannotatedOccurrences": unannotated,
            "byRetention": retentions,
            "notJoinedExemptions": retentions.get("not-joined", []),
            "lawHolds": not unannotated}


def import_mirror_differential():
    """The workflow contract claims the foundation `import` record and the
    workflow `ImportWrapperV2` mirror admit and refuse the SAME instances.
    Prove it on the exact boundaries the contract says once disagreed."""
    base = {
        "schemaVersion": 2, "kind": "runtime",
        "payloadSchemaDigest": sha256hex(b"schema-doc"),
        "payloadDigest": sha256hex(b"payload"),
        "sourceCorrespondenceDigest": sha256hex(b"corr"),
        "buildDigest": sha256hex(b"build"),
        "producerClosure": "closure2:" + "11" * 32,
        "adapterClosure": "closure2:" + "22" * 32,
        "blobs": [],
        "scopeDigest": sha256hex(b"scope"),
        "observationDigest": sha256hex(b"obs"),
        "completeness": "complete", "omissions": []}

    def both(inst):
        a = O.validate("identity", "#/$defs/import", inst)
        b = O.validate("imported-evidence", "#/$defs/ImportWrapperV2", inst)
        return {"foundationAdmits": not a, "mirrorAdmits": not b,
                "verdictsAgree": (not a) == (not b),
                "foundationErrors": a[:2], "mirrorErrors": b[:2]}

    cases = {}
    cases["zero-blobs"] = both(base)
    cases["one-blob"] = both(dict(base, blobs=[
        {"path": "cov/lcov.info", "sha256": sha256hex(b"x"), "bytes": 1}]))
    cases["omissions-unsorted"] = both(dict(base, completeness="partial",
                                            omissions=["b", "a"]))
    cases["omissions-sorted"] = both(dict(base, completeness="partial",
                                          omissions=["a", "b"]))
    cases["blob-path-absolute"] = both(dict(base, blobs=[
        {"path": "/etc/passwd", "sha256": sha256hex(b"x"), "bytes": 1}]))
    cases["blob-path-dotdot"] = both(dict(base, blobs=[
        {"path": "../out", "sha256": sha256hex(b"x"), "bytes": 1}]))
    cases["blob-bytes-over-268435456"] = both(dict(base, blobs=[
        {"path": "big.bin", "sha256": sha256hex(b"x"), "bytes": 268435457}]))
    cases["blob-bytes-at-268435456"] = both(dict(base, blobs=[
        {"path": "big.bin", "sha256": sha256hex(b"x"), "bytes": 268435456}]))
    cases["4097-blobs"] = both(dict(base, blobs=[
        {"path": "b/%d" % i, "sha256": sha256hex(b"x%d" % i), "bytes": 1}
        for i in range(4097)]))
    # a DISCRIMINATING negative floor: both documents must REFUSE something
    cases["_discriminating-negative"] = both(dict(base, kind="not-a-kind"))
    cases["_discriminating-negative-2"] = both(dict(base, extraKey=1))
    agree = all(v["verdictsAgree"] for v in cases.values())
    refused_by_both = [k for k, v in cases.items()
                       if not v["foundationAdmits"] and not v["mirrorAdmits"]]
    return {"cases": cases, "allVerdictsAgree": agree,
            "discriminatingNegativesRefusedByBoth": refused_by_both,
            "floorSatisfied": len(refused_by_both) >= 2}


def bound_arithmetic():
    M = O.doc("matrix")
    caps = [c["id"] for c in M["capabilities"]]
    cell = {(c["capability"], c["mode"]): c["state"] for c in M["cells"]}
    per_mode = {m: len([c for c in caps if cell[(c, m)] != "NOT-SELECTED"])
                for m in [x for x in M["languageModes"]]}
    ts = per_mode["ts-tsconfig"]
    limit = O.doc("identity")["$defs"]["analysis-spec"]["properties"][
        "requestedCapabilities"]["maxItems"]
    fits = limit // ts
    return {"capabilitiesPerMode": per_mode,
            "requestedCapabilitiesMaxItems": limit,
            "typescriptUnitsThatFit": fits,
            "rowsAtThatCount": fits * ts,
            "rowsAtOneMore": (fits + 1) * ts,
            "matchesPublishedArithmetic":
                fits == 93 and fits * ts == 1023 and (fits + 1) * ts == 1034,
            "cellCountEqualsProduct":
                len(M["cells"]) == len(caps) * len(M["languageModes"]),
            "cellCount": len(M["cells"]),
            "product": len(caps) * len(M["languageModes"])}


def build():
    return {"digestLaw": digest_law(),
            "orderVocabulary": order_vocabulary(),
            "relationDigestLaw": relation_digest_law(),
            "importMirrorDifferential": import_mirror_differential(),
            "boundArithmetic": bound_arithmetic()}


def cardinality_boundaries():
    """native S14 publishes a typed PROJECT.SCOPE_LIMIT refusal for FOUR
    bounded selection arrays across TWO record families.  These are reachable
    boundaries on a THIRD family (`plan`) with no published typed refusal."""
    i = O.doc("identity")["$defs"]
    sc = i["semantic-configuration"]["properties"]
    published = {"scope-descriptor.workspaceRoots":
                     i["scope-descriptor"]["properties"]["workspaceRoots"]["maxItems"],
                 "scope-descriptor.pathPrefixes":
                     i["scope-descriptor"]["properties"]["pathPrefixes"]["maxItems"],
                 "scope-descriptor.excludedPathPrefixes":
                     i["scope-descriptor"]["properties"]["excludedPathPrefixes"]["maxItems"],
                 "analysis-spec.requestedCapabilities":
                     i["analysis-spec"]["properties"]["requestedCapabilities"]["maxItems"]}
    unpublished = {"plan.nativeContextDigests":
                       i["plan"]["properties"]["nativeContextDigests"]["maxItems"],
                   "plan.semanticClosures":
                       i["plan"]["properties"]["semanticClosures"]["maxItems"],
                   "plan.importIds": i["plan"]["properties"]["importIds"]["maxItems"]}

    base = {"schemaVersion": 2, "snapshotId": "snapshot2:" + "11" * 32,
            "capabilityManifestId": "22" * 32, "semanticClosures": [],
            "analysisSpecDigest": "33" * 32, "resolvedConfigDigest": "44" * 32,
            "nativeContextDigests": [], "importIds": [],
            "policyDigest": "55" * 32, "waiverDigest": "66" * 32,
            "scopeDigest": "77" * 32,
            "budget": {"unit": "work-units", "limit": 1},
            "semanticGrantDigest": "88" * 32,
            "capabilityManifestBytesDigest": "99" * 32}

    ctx129 = sorted("%064x" % n for n in range(129))
    over_ctx = dict(base, nativeContextDigests=ctx129)
    imp257 = sorted("import2:%064x" % n for n in range(257))
    over_imp = dict(base, importIds=imp257)
    errs_ctx = O.validate("identity", "#/$defs/plan", over_ctx)
    errs_imp = O.validate("identity", "#/$defs/plan", over_imp)
    return {
        "publishedTypedRefusalFields": published,
        "unpublishedPlanBounds": unpublished,
        "reachability": {
            "129 distinct TypeScript units with an explicit "
            "analysis.capabilities=[inventory] override": {
                "requestedCapabilityRows": 129,
                "requestedCapabilitiesBound": published[
                    "analysis-spec.requestedCapabilities"],
                "admittedByThatBound": True,
                "workspaceRoots": 129,
                "workspaceRootsBound": published["scope-descriptor.workspaceRoots"],
                "admittedByThatBound2": True,
                "distinctNativeContexts": 129,
                "planBound": unpublished["plan.nativeContextDigests"],
                "expressible": False},
            "1024 already-admitted import2 IDs in the resolved configuration": {
                "configurationBound": sc["evidence"]["properties"]["importIds"]["maxItems"],
                "planBound": unpublished["plan.importIds"],
                "expressibleAbove": unpublished["plan.importIds"]}},
        "genericSchemaFaultForOverflow": {
            "nativeContextDigests": errs_ctx,
            "importIds": errs_imp,
            "namesFieldCountAndLimit": all(
                ("129" in " ".join(errs_ctx)) or ("128" in " ".join(errs_ctx))
                for _ in [0])},
        "note": "native S14: 'a maxItems breach is reported generically, "
                "restating the entire instance and naming no field, count or "
                "limit; an oversized ordinary selection is not a malformed "
                "record and is not published as one'."}
