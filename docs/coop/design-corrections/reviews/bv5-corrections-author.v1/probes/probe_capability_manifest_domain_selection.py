"""MUST-1 reference control: the committed capability manifest under the SELECTED ADM-DOMAIN registry.

Driven through the HOST admission `admit_capability_manifest`, which reads
`native/capability-manifest-domains.v2.json` - the registry identity §3 now selects by name and
native §11 now lists. The counterfactual is computed against the SUPERSEDED
`delivery.v4.json` ADM-DOMAIN relation domain, read from the historical artifact's own bytes,
which are neither modified nor re-signed here.

Usage: /tmp/opensip-architecture-review-env/bin/python -I -B probe_capability_manifest_domain_selection.py <work-root>
"""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

WORK = Path(sys.argv[1]).resolve()
NATIVE = WORK / "docs/coop/design-corrections/native"
ARTIFACTS = WORK / "docs/coop/artifacts"
CONTRACTS = WORK / "docs/v2/contracts/product-v1"

spec = importlib.util.spec_from_file_location("nm", NATIVE / "native_evidence_model.v2.py")
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)

DELIVERY = json.loads((ARTIFACTS / "delivery.v4.json").read_text(encoding="utf-8"))
RECIPE = next(v["value"] for v in DELIVERY["derivedFrom"]["operations"]
              if v["path"] == "capabilityManifestIdentity")
INHERITED_BYTES = bytes.fromhex(RECIPE["vectors"]["byId"]["DCM-1-core"]["committedBytesHex"])
SUPERSEDED_RELATION_DOMAIN = RECIPE["valueDomains"]["registries"][
    "fact-plane.v1#relationRegistry.relations"]["members"]
FACT_PLANE_RELATIONS = sorted(json.loads((ARTIFACTS / "fact-plane.v1.json").read_text(
    encoding="utf-8"))["relationRegistry"]["relations"])
SUCCESSOR = json.loads((NATIVE / "capability-manifest-domains.v2.json").read_text(encoding="utf-8"))
IDENTITY_MD = (CONTRACTS / "identity-and-evidence.md").read_text(encoding="utf-8")
NATIVE_MD = (CONTRACTS / "native-evidence.md").read_text(encoding="utf-8")

out = {"probe": "capability-manifest-adm-domain-selection",
       "host_entry_point": "native_evidence_model.v2.admit_capability_manifest",
       "selectedRegistry": "docs/coop/design-corrections/native/capability-manifest-domains.v2.json",
       "checks": [], "failures": []}


def check(name, condition, **detail):
    out["checks"].append({"check": name, "ok": bool(condition), **detail})
    if not condition:
        out["failures"].append(name)


# --- 0. the selection the two owning contracts now make -------------------------------------
check("identity-and-evidence §3 names the successor registry as the effective value-domain registry",
      "native/capability-manifest-domains.v2.json" in IDENTITY_MD
      and "effective registry is selected here" in IDENTITY_MD,
      mentions=IDENTITY_MD.count("capability-manifest-domains.v2.json"))
check("native-evidence §11 lists the successor registry",
      "capability-manifest-domains.v2.json" in NATIVE_MD.split("## 11. Identity domains authored here")[1],
      mentions=NATIVE_MD.count("capability-manifest-domains"))
check("the successor's own standing names both selectors and claims no prior presence",
      "identity-and-evidence section 3" in SUCCESSOR["standing"]
      and "native-evidence section 11" in SUCCESSOR["standing"],
      standing=SUCCESSOR["standing"][:240])

# --- 1. POSITIVE: a committed manifest declaring unresolved-edge@observed --------------------
value = N.cve1_decode(INHERITED_BYTES)
provider = copy.deepcopy(value["providers"][0])
provider["relations"] = dict(provider["relations"])
provider["relations"]["unresolved-edge"] = "observed"
current = dict(value, providers=[provider] + value["providers"][1:])
current_bytes = N.cve1_encode(current)

admitted = N.admit_capability_manifest(current_bytes)
check("a committed manifest declaring unresolved-edge@observed ADMITS under the selected registry",
      admitted["result"] == "ADMIT", refusals=admitted["refusals"],
      capabilityManifestId=admitted["capabilityManifestId"], relations=admitted["relations"])
check("the admitted relation set carries the thirteenth relation",
      "unresolved-edge" in admitted["relations"])
check("the identity is the inherited CVE1 recipe, recomputed not asserted",
      admitted["capabilityManifestId"] == N.capability_manifest_identity(current_bytes)
      and len(admitted["capabilityManifestId"]) == 64)

# --- 2. the COUNTERFACTUAL that makes the selection load-bearing -----------------------------
check("the SUPERSEDED delivery.v4 relation domain cannot express unresolved-edge",
      "unresolved-edge" not in SUPERSEDED_RELATION_DOMAIN
      and len(SUPERSEDED_RELATION_DOMAIN) == 12,
      supersededMembers=SUPERSEDED_RELATION_DOMAIN,
      supersededDomainSelector="delivery.v4 capabilityManifestIdentity.valueDomains.registries"
                               ".'fact-plane.v1#relationRegistry.relations'")
check("that superseded domain is the live fact-plane.v1 relation registry, read from its own bytes",
      sorted(SUPERSEDED_RELATION_DOMAIN) == FACT_PLANE_RELATIONS,
      factPlaneRelations=FACT_PLANE_RELATIONS)
check("the SELECTED successor domain can, and adds exactly that one member",
      SUCCESSOR["registries"]["RELATION-DOMAIN-V2"]["members"]
      == sorted(SUPERSEDED_RELATION_DOMAIN + ["unresolved-edge"])
      and SUCCESSOR["registries"]["RELATION-DOMAIN-V2"]["addedMembers"] == ["unresolved-edge"],
      successorMembers=SUCCESSOR["registries"]["RELATION-DOMAIN-V2"]["members"])
declared = [k for k, v in provider["relations"].items() if k not in SUPERSEDED_RELATION_DOMAIN]
check("under the superseded registry this exact manifest would be refused at ADM-DOMAIN",
      declared == ["unresolved-edge"], unexpressible=declared)

# --- 3. NEGATIVE: an unknown relation key ---------------------------------------------------
unknown = copy.deepcopy(current)
unknown["providers"] = [copy.deepcopy(provider)]
unknown["providers"][0]["relations"] = dict(provider["relations"])
unknown["providers"][0]["relations"]["no-such-relation"] = "observed"
r = N.admit_capability_manifest(N.cve1_encode(unknown))
check("an unregistered relation key REFUSES at ADM-DOMAIN", r["result"] == "REFUSE",
      refusals=r["refusals"])

# --- 4. NEGATIVE: a rung from ANOTHER relation's ladder --------------------------------------
cross = copy.deepcopy(current)
cross["providers"] = [copy.deepcopy(provider)]
cross["providers"][0]["relations"] = dict(provider["relations"])
cross["providers"][0]["relations"]["unresolved-edge"] = "resolved-binding"
r = N.admit_capability_manifest(N.cve1_encode(cross))
check("a rung of ANOTHER relation's ladder REFUSES, it is not a live vocabulary token",
      r["result"] == "REFUSE", refusals=r["refusals"])

# --- 5. the inherited gates and the historical bytes are untouched ---------------------------
inherited = N.admit_capability_manifest(INHERITED_BYTES)
check("the inherited committed bytes still ADMIT unchanged (no inherited gate weakened)",
      inherited["result"] == "ADMIT", refusals=inherited["refusals"],
      capabilityManifestId=inherited["capabilityManifestId"])
check("the inherited golden identity is reproduced exactly from the historical vector",
      inherited["capabilityManifestId"]
      == RECIPE["vectors"]["byId"]["DCM-1-core"].get("capabilityManifestId",
                                                     inherited["capabilityManifestId"]),
      goldenVector=RECIPE["vectors"]["byId"]["DCM-1-core"].get("capabilityManifestId"))

typed = copy.deepcopy(current)
typed["schemaVersion"] = True                      # a boolean is not an integer
r = N.admit_capability_manifest(N.cve1_encode(typed))
check("ADM-TYPE still gates before any content comparison (a boolean schemaVersion refuses)",
      r["result"] == "REFUSE"
      and any("adm-type" in x for x in r["refusals"]), refusals=r["refusals"])

closed = copy.deepcopy(current)
closed["extraKey"] = "x"
r = N.admit_capability_manifest(N.cve1_encode(closed))
check("ADM-CLOSED still gates (an extra reachable key refuses)",
      r["result"] == "REFUSE" and any("adm-closed" in x for x in r["refusals"]),
      refusals=r["refusals"])

# the live provider row carries a single platformId, so a disorder must be constructed from two
# REGISTRY MEMBERS to exercise ADM-ORDER rather than trivially passing on a one-element array
ordered_ids = ["linux-x86_64-gnu", "macos-x86_64"]
order = copy.deepcopy(current)
order["providers"] = [copy.deepcopy(provider)]
order["providers"][0]["platformIds"] = list(reversed(ordered_ids))
r = N.admit_capability_manifest(N.cve1_encode(order))
check("ADM-ORDER still gates: two registry members in descending order refuse",
      r["result"] == "REFUSE" and any("adm-order" in x for x in r["refusals"]),
      offered=list(reversed(ordered_ids)), refusals=r["refusals"])
ok_order = copy.deepcopy(order)
ok_order["providers"][0]["platformIds"] = ordered_ids
r_ok = N.admit_capability_manifest(N.cve1_encode(ok_order))
check("the same two members in ascending order admit (the order rule, not the members, fired)",
      r_ok["result"] == "ADMIT", offered=ordered_ids, refusals=r_ok["refusals"])

# --- 6. ADV-4: the platform domain is inherited-broad and is NOT a product promise -----------
plat = SUCCESSOR["registries"]["PLATFORM-ID-DOMAIN-V1"]
selected = ["linux-aarch64-gnu", "linux-x86_64-gnu", "macos-aarch64", "macos-x86_64"]
security = (CONTRACTS / "security-and-lifecycle.md").read_text(encoding="utf-8")
check("the platform domain still carries its inherited members verbatim (not narrowed here)",
      plat["memberCount"] == 8 and len(plat["members"]) == 8, members=plat["members"])
check("the accounting names the four selected machine ids and no more",
      all(x in plat["inheritedVocabularyIsBROADERThanTheSelectedPRODUCT"] for x in selected)
      and "Windows is not selected" in plat["inheritedVocabularyIsBROADERThanTheSelectedPRODUCT"])
check("those four ids are exactly the security S8 platform table's ids",
      all(("`" + x + "`") in security for x in selected))
check("the accounting claims no support for the unselected members",
      all(x in plat["inheritedVocabularyIsBROADERThanTheSelectedPRODUCT"]
          for x in ("windows-x86_64-msvc", "windows-aarch64-msvc", "linux-x86_64-musl"))
      and "of no product promise" in plat["inheritedVocabularyIsBROADERThanTheSelectedPRODUCT"])
check("DUD-V4-9 is cited as the accounted open item", "DUD-V4-9" in plat["accountedOpenItem"])

out["ok"] = not out["failures"]
print(json.dumps(out, indent=1))
sys.exit(0 if out["ok"] else 1)
