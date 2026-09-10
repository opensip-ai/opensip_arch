#!/usr/bin/env python3
"""P04: whole-graph digest-field sweep.

The closing digest law says every BARE 64-hex field in identity-schemas.v2
carries exactly one `x-opensip-digest` annotation, and that an unannotated one
is inadmissible. A PREFIXED identity (`plan2:<64hex>`) is a typed identity, not
a bare digest field, so the two must be separated before the law is checked.

Also verifies:
  - every annotation's `representation` is one of the four closed values;
  - every annotation's `retention` is one of the four closed modes;
  - the non-default retention modes are closed to exactly the fields the
    contract names;
  - every `domain` enum member is registered in x-opensip-digest-domains;
  - the same sweep over the native bundle, where the law is claimed to reach.
"""
import json, re, sys
from pathlib import Path

SUBJ = Path("/tmp/opensip-design-corrections/candidate-subject.v8")
F = SUBJ / "docs/coop/design-corrections/foundation"
NAT = SUBJ / "docs/coop/design-corrections/native"

BARE = re.compile(r"^\^\[0-9a-f\]\{64\}\(\?!\[\\s\\S\]\)\$?$")
PREFIXED = re.compile(r"^\^[a-z0-9\-]+2?:\[0-9a-f\]\{64\}")

REPRESENTATIONS = {"raw-artifact", "canonical-record", "h-identity",
                   "capability-manifest-id"}
RETENTIONS = {"preimage", "fragment", "derived", "owner-retained"}

out = {}


def sweep(doc, label):
    bare, prefixed, other = [], [], []
    reps, rets = {}, {}
    bad_rep, bad_ret, unannotated = [], [], []

    def walk(node, path):
        if isinstance(node, dict):
            pat = node.get("pattern")
            if isinstance(pat, str) and "[0-9a-f]{64}" in pat:
                ann = node.get("x-opensip-digest")
                entry = {"path": path, "pattern": pat, "annotation": ann}
                if BARE.match(pat):
                    bare.append(entry)
                    if ann is None:
                        unannotated.append(path)
                    else:
                        rep = ann.get("representation") if isinstance(ann, dict) else ann
                        ret = (ann.get("retention", "preimage")
                               if isinstance(ann, dict) else "preimage")
                        reps[rep] = reps.get(rep, 0) + 1
                        rets[ret] = rets.get(ret, 0) + 1
                        if rep not in REPRESENTATIONS:
                            bad_rep.append({"path": path, "representation": rep})
                        if ret not in RETENTIONS:
                            bad_ret.append({"path": path, "retention": ret})
                elif PREFIXED.match(pat):
                    prefixed.append(entry)
                else:
                    other.append(entry)
            for k, v in node.items():
                walk(v, path + "/" + str(k))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + "/" + str(i))

    walk(doc, "#")
    return {
        "bare64HexFields": len(bare),
        "bare64HexAnnotated": len(bare) - len(unannotated),
        "bare64HexUnannotated": unannotated,
        "prefixedTypedIdentityFields": len(prefixed),
        "otherHexBearingPatterns": [e["path"] for e in other],
        "representationHistogram": reps,
        "retentionHistogram": rets,
        "invalidRepresentations": bad_rep,
        "invalidRetentions": bad_ret,
        "LAW_HOLDS": not unannotated and not bad_rep and not bad_ret,
        "_bare": bare,
    }


def main():
    ids = json.loads((F / "identity-schemas.v2.json").read_bytes())
    nat = json.loads((NAT / "native-evidence.schemas.v2.json").read_bytes())
    rel = json.loads((F / "relation-payload-schemas.v2.json").read_bytes())
    cfg = json.loads((F / "product-configuration.schema.v2.json").read_bytes())

    s_id = sweep(ids, "identity")
    s_nat = sweep(nat, "native")
    s_rel = sweep(rel, "relation")
    s_cfg = sweep(cfg, "configuration")

    # ---- non-default retention modes are closed to the named fields -------
    closed_expect = {
        "fragment": ["program-predicate", "nodeDigest"],
        "derived": ["capabilityManifestId"],
        "owner-retained": ["ownerFileManifestSha256"],
    }
    actual = {"fragment": [], "derived": [], "owner-retained": []}
    for e in s_id["_bare"]:
        ann = e["annotation"]
        if isinstance(ann, dict):
            r = ann.get("retention", "preimage")
            if r in actual:
                actual[r].append(e["path"])
    out["nonDefaultRetentionModes"] = {
        "actual": actual,
        "contractClosesThemTo": closed_expect,
        "fragmentClosedToNodeDigest": all("nodeDigest" in p for p in actual["fragment"]),
        "derivedClosedToCapabilityManifestId": all(
            "capabilityManifestId" in p for p in actual["derived"]),
        "ownerRetainedClosedToOwnerFileManifest": all(
            "ownerFileManifestSha256" in p for p in actual["owner-retained"]),
    }

    # ---- every `domain` enum member is registered -------------------------
    domains_reg = ids["x-opensip-digest-domains"]
    by_domain = domains_reg.get("byDomain", {})
    domain_sets = domains_reg.get("domainSets", {})
    enum_members = set()

    def collect(node, path):
        if isinstance(node, dict):
            if "properties" in node and "domain" in node.get("properties", {}):
                d = node["properties"]["domain"]
                if "enum" in d:
                    enum_members.update(d["enum"])
            for k, v in node.items():
                collect(v, path + "/" + str(k))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                collect(v, path + "/" + str(i))
    collect(ids, "#")
    out["refDomainRegistry"] = {
        "domainEnumMembers": sorted(enum_members),
        "registeredInByDomain": sorted(by_domain),
        "unregisteredEnumMembers": sorted(enum_members - set(by_domain)),
        "everyEnumMemberRegistered": not (enum_members - set(by_domain)),
        "domainSets": {k: sorted(v.get("domains", v)) if isinstance(v, dict) else v
                       for k, v in domain_sets.items()},
    }

    # ---- payload reference domains excluded from proof input vocabulary ---
    payload_domains = {"coverage-payload", "import-payload", "fact-payload"}
    proof_input = None

    def find_proof_inputs(node, path):
        nonlocal proof_input
        if isinstance(node, dict):
            if path.endswith("ProofInputRef/properties/domain") and "enum" in node:
                proof_input = node["enum"]
            for k, v in node.items():
                find_proof_inputs(v, path + "/" + str(k))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                find_proof_inputs(v, path + "/" + str(i))
    find_proof_inputs(ids, "#")
    out["proofInputVocabulary"] = {
        "members": proof_input,
        "excludesPayloadDomains": (proof_input is not None
                                   and not (set(proof_input) & payload_domains)),
    }

    for k in ("_bare",):
        for s in (s_id, s_nat, s_rel, s_cfg):
            s.pop(k, None)
    out["identity"] = s_id
    out["native"] = s_nat
    out["relationPayloads"] = s_rel
    out["configuration"] = s_cfg

    json.dump(out, sys.stdout, indent=1)
    print()


if __name__ == "__main__":
    main()
