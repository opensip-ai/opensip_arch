"""MUST-2 reference control: the published libSelection -> component join.

Driven through the HOST admission `admit_native_context` on the retained closure trees, plus a
positive universe binding, so this exercises the enforced admission join and not a helper.

The corrected §2.4 / schema descriptions publish:
    fold(n)        = Unicode simple lowercase of n (the SAME fold the honoredOptions.lib
                     agreement uses; no NFC/NFKC, no trimming, no alias, no prefix match)
    component(n)   = "lib." + fold(n) + ".d.ts"
    membership     = component(n) must be in the declared component set, else
                     native.native-context-lib-not-retained:<n>
    equality       = folded libSelection set == folded honoredOptions.lib set
    order          = libSelection sorted by raw UTF-8 bytes of the RETAINED (unfolded) names;
                     standardLibraryComponentDigests sorted by component bytes
    custody        = the component rows are the COMPLETE .d.ts inventory of the retained tree,
                     selected or not; selection never narrows it, folding never rewrites it

Usage: /tmp/opensip-architecture-review-env/bin/python -I -B probe_ts_lib_component_mapping.py <work-root>
"""
from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

WORK = Path(sys.argv[1]).resolve()
NATIVE = WORK / "docs/coop/design-corrections/native"

spec = importlib.util.spec_from_file_location("nm", NATIVE / "native_evidence_model.v2.py")
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)

CASES = json.loads((NATIVE / "native-cases.v2.json").read_text(encoding="utf-8"))
FX = CASES["fixtures"]
SCHEMAS = json.loads((NATIVE / "native-evidence.schemas.v2.json").read_text(encoding="utf-8"))

out = {"probe": "typescript-lib-name-to-stdlib-component-join",
       "host_entry_point": "native_evidence_model.v2.admit_native_context (+ bind_typescript_universe)",
       "publishedMapping": 'component(n) = "lib." + fold(n) + ".d.ts", fold = Unicode simple lowercase',
       "checks": [], "failures": []}


def admit(descriptor, trees=None):
    return N.admit_native_context("typescript", descriptor, trees or FX["tsClosureTrees"])


def check(name, condition, **detail):
    out["checks"].append({"check": name, "ok": bool(condition), **detail})
    if not condition:
        out["failures"].append(name)


# --- 1. POSITIVE: the admitted context of the accepted case, and the mapping read off it -----
base = copy.deepcopy(FX["tsNativeContext"])
a = admit(base)
components = [r["component"] for r in base["toolchain"]["standardLibraryComponentDigests"]]
selection = list(base["toolchain"]["libSelection"])
mapped = {n: "lib." + n.lower() + ".d.ts" for n in selection}
check("admitted positive TypeScript context has no refusals", a["refusals"] == [],
      nativeContextId=a["nativeContextId"], refusals=a["refusals"])
check("every selected lib name maps into the retained component set under the published mapping",
      all(v in components for v in mapped.values()),
      libSelection=selection, mapping=mapped, components=components)
check("the mapping is one-directional: no component name is itself a selected lib name",
      not (set(components) & set(selection)))
check("the component rows are the COMPLETE .d.ts inventory of the retained tree, not just the selection",
      sorted(components) == sorted(b["path"].rpartition("/")[2]
                                   for b in FX["tsStdlibClosure"]["tree"] if b["path"].endswith(".d.ts"))
      and len(components) > len(selection),
      componentCount=len(components), selectedCount=len(selection))

u = N.bind_typescript_universe(FX["tsUniverse"], a, base, FX["tsRetainedUniverseInputs"],
                               FX["tsSnapshotInventory"])
check("the admitted context binds a positive universe (graph, not a schema-only check)",
      u["result"] == "ADMIT", universeResult=u["result"], universeId=u.get("universeId"))

# --- 2. CASE: the accepted fixture itself is the evidence the join was never publishable ----
# The retained fixture selects DOM / ES2022 while the retained components are lib.dom.d.ts /
# lib.es2022.d.ts, so the admitted graph ALREADY depends on the fold + mapping this correction
# publishes. Re-spelling the selection in lower case must admit through the SAME fold, and must
# move the identity, because folding is a comparison and never a rewrite of retained bytes.
check("the accepted fixture already depends on the fold: selection is cased, components are not",
      selection == ["DOM", "ES2022"] and components == sorted(components)
      and all(c == c.lower() for c in components),
      libSelection=selection, components=components)
cased = copy.deepcopy(base)
cased["toolchain"]["libSelection"] = ["dom", "es2022"]      # in raw UTF-8 byte order
cased_admission = admit(cased)
check("a lower-case libSelection admits against an upper-case honoredOptions.lib: one fold "
      "serves the equality AND the component join",
      cased_admission["refusals"] == [], refusals=cased_admission["refusals"],
      libSelection=cased["toolchain"]["libSelection"],
      honoredLib=cased["configProjection"]["honoredOptions"]["lib"])
check("folding is a COMPARISON, not a rewrite: the retained bytes differ so the identity moves",
      cased_admission["nativeContextId"] != a["nativeContextId"],
      cased=cased_admission["nativeContextId"], base=a["nativeContextId"])

# --- 3. NEGATIVE: a selected name whose component is not retained ----------------------------
missing = copy.deepcopy(base)
missing["toolchain"]["libSelection"] = sorted(selection + ["es2023"], key=lambda x: x.encode())
missing["configProjection"]["honoredOptions"]["lib"] = list(missing["toolchain"]["libSelection"])
missing_admission = admit(missing)
check("a selected lib whose component(n) is absent refuses native.native-context-lib-not-retained",
      missing_admission["refusals"] == ["native.native-context-lib-not-retained:es2023"],
      refusals=missing_admission["refusals"],
      note="honoredOptions.lib was widened in step with the selection so ONLY the join fires")

# --- 4. NEGATIVE: case-only difference against the honored options ---------------------------
disagree = copy.deepcopy(base)
disagree["configProjection"]["honoredOptions"]["lib"] = ["dom", "es2021"]
disagree_admission = admit(disagree)
check("a folded-set disagreement with honoredOptions.lib still refuses (the rule is not dropped)",
      "native.native-context-field-mismatch:libSelection" in disagree_admission["refusals"],
      refusals=disagree_admission["refusals"])

dup = copy.deepcopy(base)
dup["toolchain"]["libSelection"] = ["DOM", "dom", "es2022"]
dup_admission = admit(dup)
check("two entries equal under fold refuse duplicate-lib-selection",
      any(r.startswith("native.native-context-field-mismatch:duplicate-lib-selection")
          or r.startswith("native.native-context-field-mismatch:lib-selection-order")
          for r in dup_admission["refusals"]),
      refusals=dup_admission["refusals"])

# --- 5. NEGATIVE: order is over the RETAINED names, not the folded ones ----------------------
unsorted_sel = copy.deepcopy(base)
unsorted_sel["toolchain"]["libSelection"] = ["es2022", "dom"]
unsorted_admission = admit(unsorted_sel)
check("an unsorted libSelection refuses on order",
      any("lib-selection-order" in r for r in unsorted_admission["refusals"]),
      refusals=unsorted_admission["refusals"])

# --- 6. NEGATIVE: the two custody refusals the corrected prose names (existing fixtures) -----
dropped = admit(FX["tsDroppedLibContext"])
check("[reproduction of an existing accepted case] an incomplete declaration inventory refuses",
      dropped["refusals"] == ["native.native-context-stdlib-inventory-incomplete:lib.decorators.d.ts"],
      refusals=dropped["refusals"])
ambiguous = admit(FX["tsAmbiguousStdlibContext"], FX["tsAmbiguousStdlibTrees"])
check("[reproduction of an existing accepted case] two tree paths sharing a basename refuse",
      ambiguous["refusals"] == ["native.native-context-stdlib-tree-ambiguous-basename:lib.dom.d.ts"],
      refusals=ambiguous["refusals"])

# --- 7. the published schema descriptions actually carry the mapping ------------------------
lib_desc = SCHEMAS["$defs"]["TypeScriptToolchainIdentityV1"]["properties"]["libSelection"]["description"]
comp_desc = SCHEMAS["$defs"]["TypeScriptLibComponentV1"]["properties"]["component"]["description"]
check("the schema descriptions publish the exact mapping expression",
      '"lib." + fold(n) + ".d.ts"' in lib_desc and '"lib." + fold(n) + ".d.ts"' in comp_desc)
check("libSelection is still typed as names, not rewritten into file names",
      SCHEMAS["$defs"]["TypeScriptToolchainIdentityV1"]["properties"]["libSelection"]["items"]["type"]
      == "string" and "$ref" not in
      SCHEMAS["$defs"]["TypeScriptToolchainIdentityV1"]["properties"]["libSelection"]["items"])

out["ok"] = not out["failures"]
print(json.dumps(out, indent=1))
sys.exit(0 if out["ok"] else 1)
