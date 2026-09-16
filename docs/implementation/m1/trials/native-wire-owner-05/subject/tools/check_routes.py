"""Owner-joined public route checks (candidate 05; review-02 RF-1, review-03 RF-3, A-1, A-2, A-3, A-9, review-04 RF-1, A-1).

Every public field is DERIVED, never compared literal-to-literal: the published rows of public-route-successor.v1.json are
applied in memory to the pinned owner model; termination, envelope errors and exit come from the owner
public_termination_for, failure_envelope_errors and CLASS_TO_EXIT, validated against the pinned common StepTermination
and DomainDetail schemas. Route SEMANTICS are bound by execution:
  route-remedy-keying      every (key, fault kind) the admission vectors produce derives an envelope remedy that states
                           that fault's condition and not the other condition class (remedyKeyingConstraint executed);
  route-join-owner-family  each key's condition class selects its owner family (errorCode, D9_MAP row, route-table row);
  route-origin-closed      the new origin's actor derives the expected class under the owner originatingBoundaryLaw;
  route-timing-anchored    timing follows the wrapped owner function and its pinned owner text, plus executed behaviour;
  route-prepared-modes     the prepared mode actions follow the owner PO-1 mode law and execute in both modes;
  route-selectors-owner-source  owner function and callee-closure source digests (A-9).
"""
import copy
import inspect
import json

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

import owner_successor as OS
import public_routes as PR
import representability as REP

TIMING_PHRASES = {"before-plan-id": "before PlanId", "before-plan-construction": "before Plan construction", "plan-time-no-spawn": "Plan time (no spawn)"}
OWNER_FUNCTION_TIMING = {"dependency_source_set_admit": "before-plan-id", "prepared_output_set_admit": "before-plan-construction", None: "plan-time-no-spawn"}
ACTOR_LAW = {"external-input": ("Invalid external input is an admission rejection", "request-rejected"),
             "host-generated-internal-layer": ("an invalid host-generated internal layer is a host invariant fault", "operational-failed")}
REPRESENTABILITY_MARK, BOUND_MARK = "cannot be carried", "limits"


def remedy_requirements(kind):
    """(phrases the remedy must contain, phrase it must not contain) for one fault kind; the checker's own reading of the
    fault's condition, independent of the published successor."""
    if kind.startswith("non-nfc"):
        return ["non-NFC", REPRESENTABILITY_MARK], BOUND_MARK
    if kind.startswith("name-or-version-scalar-at-or-below"):
        return ["U+0020", REPRESENTABILITY_MARK], BOUND_MARK
    if kind.startswith("package-key-over"):
        return ["package key", REPRESENTABILITY_MARK], BOUND_MARK
    if kind == "generated-logical-path-owner-schema":
        return ["generated-file logical path", "'..'", REPRESENTABILITY_MARK], BOUND_MARK
    if kind == "site-path-owner-schema":
        return ["prepared output site path", "'..'", REPRESENTABILITY_MARK], BOUND_MARK
    if "path" in kind:
        return ["dependency source file path", "'..'", REPRESENTABILITY_MARK], BOUND_MARK
    if kind.startswith("entries:"):
        return ["entry", BOUND_MARK], REPRESENTABILITY_MARK
    if kind in ("entries", "blob-bytes"):
        return ["prepared outputs", BOUND_MARK], REPRESENTABILITY_MARK
    if kind.startswith("frame:"):
        return ["frame", BOUND_MARK], REPRESENTABILITY_MARK
    if kind in ("request-bytes", "request-frames"):
        return ["request limits"], REPRESENTABILITY_MARK
    return None, None


class Routes:
    def __init__(self, ref):
        self.r, self.s, self.NE, self.NE_S = ref, ref.s, ref.NE, ref.NE_S
        self.doc = json.loads((self.s.out / "public-route-successor.v1.json").read_text())
        self.common = json.loads(self.s.raw["workflowCommon"])
        self.registry_doc = json.loads(self.s.raw["publicDetailRegistry"])

    def add(self, *a):
        self.r.add(*a)

    def validator(self, defname):
        schema = PR.common_schema_with_members(self.common, self.doc)
        cid = schema["$id"]
        reg = Registry().with_resource(cid, Resource(contents=schema, specification=DRAFT202012))
        return Draft202012Validator({"$ref": cid + "#/$defs/" + defname}, registry=reg)

    def family(self, key):
        return self.doc["conditionClasses"][self.doc["addKeys"][key]["conditionClass"]]["ownerFamily"]

    # ------------------------------------------------------------------
    def rule_references(self):
        keys = self.doc["addKeys"]
        refs, bad = {}, []
        for rule in self.s.wire["admission"]:
            p = rule.get("params", {})
            if "refusal" in p:
                bad.append(rule["id"] + ": literal refusal")
            rt = p.get("route")
            if rt is None:
                continue
            if rt["routeKey"] not in keys or rt["successor"] != "public-route-successor.v1.json#/addKeys/" + rt["routeKey"]:
                bad.append(rule["id"] + ": " + rt["routeKey"])
            refs.setdefault(rt["routeKey"], []).append(rule["id"])
        selectors = {k: sorted(self.doc["selectors"].get(k, {}).get("rules", [])) for k in keys}
        refs_sorted = {k: sorted(v) for k, v in refs.items()}
        self.add("route-rule-references", not bad and set(refs) == set(keys) and all(set(refs_sorted.get(k, [])) <= set(selectors[k]) and refs_sorted.get(k) for k in keys),
                 {"bad": bad, "references": refs_sorted})

    def join(self):
        NE = self.NE
        st_v, dd_v = self.validator("StepTermination"), self.validator("DomainDetail")
        codes = {m["code"]: m["remedy"] for m in self.doc["addDomainDetailCodes"]}
        with PR.Overlay(NE, self.doc) as ov:
            for key, row in self.doc["addKeys"].items():
                try:
                    fam = self.family(key)["routeRegistry"]
                    owner = NE.PUBLIC_ROUTE_REGISTRY["keys"][fam["key"]]
                    owner_route = owner["byOriginatingBoundary"][fam["origin"]] if owner["originDependent"] else owner["route"]
                    d = ov.derive(key + ":probe-subject")
                    term, errors = d["termination"], d["errors"]
                    schema_errors = [e.message for e in st_v.iter_errors(term)] + [e.message for err in errors for e in dd_v.iter_errors(err)]
                    ok = (not schema_errors and self.doc["publicForm"] == "internal-key-domainDetail-absent"
                          and set(term) == {"class", "errorCode"} and term["class"] == owner_route["class"] and term["errorCode"] == owner_route["errorCode"]
                          and d["exitCode"] == NE.CLASS_TO_EXIT[owner_route["class"]]
                          and len(errors) == 1 and errors[0]["code"] in codes and errors[0]["remedy"] == codes[errors[0]["code"]]
                          and errors[0]["subject"] == key + ":probe-subject")
                    detail = {"termination": term, "exitCode": d["exitCode"], "envelope": errors[0]["code"] if errors else None, "schemaErrors": schema_errors[:3],
                              "ownerFamilyRoute": {"key": fam["key"], "class": owner_route["class"], "errorCode": owner_route["errorCode"]}}
                except Exception as exc:  # noqa: BLE001
                    ok, detail = False, type(exc).__name__ + ": " + str(exc)[:240]
                self.add("route-join:" + key, ok, detail)

    def owner_family(self):
        NE, fx = self.NE, self.r.fx
        executed = NE.prepared_output_set_admit(copy.deepcopy(fx["prepDylib"]), fx["ctx"], True)["d9"]
        results = {}
        with PR.Overlay(NE, self.doc) as ov:
            for row in self.doc["routeTableRows"]:
                fam = self.family(row["routeKey"])
                d9 = NE.D9_MAP[fam["modelD9Map"]]
                d = ov.derive(row["routeKey"])
                target = fam["routeTable"]
                line = self.s.lines(target["pin"])[target["line"] - 1]
                ok = (row["target"] == target and row["class"] == d["termination"]["class"] == d9["class"]
                      and row["errorCode"] == d["termination"]["errorCode"] == d9["code"] and int(row["exitCode"]) == d["exitCode"] == d9["exitCode"]
                      and target["rowNeedle"] in line and "`%s`" % d9["code"] in line and "`request-rejected` (2)" in line
                      and row["routeKey"] in row["carrier"] and self.doc["addKeys"][row["routeKey"]]["route"]["envelopeDetail"] in row["carrier"])
                if self.doc["addKeys"][row["routeKey"]]["conditionClass"] == "representability":
                    ok = ok and executed["code"] == d9["code"] and executed["exitCode"] == d9["exitCode"]
                results[row["routeKey"]] = ok
        self.add("route-join-owner-family", bool(results) and all(results.values()) and set(results) == set(self.doc["addKeys"]),
                 {"rows": results, "executedOwnerRepresentabilityRefusal": executed})

    def remedy_keying(self):
        codes = {m["code"]: m["remedy"] for m in self.doc["addDomainDetailCodes"]}
        pairs = set()
        for vecs in self.s.vectors["vectors"].values():
            for vec in vecs:
                exp = vec.get("expect") or ""
                if vec["kind"] == "refuse" and exp.startswith("ROUTE:"):
                    parts = exp.split(":", 2)
                    if len(parts) == 3:
                        pairs.add((parts[1], parts[2]))
        bad, checked = [], 0
        with PR.Overlay(self.NE, self.doc) as ov:
            for key, kind in sorted(pairs):
                need, forbid = remedy_requirements(kind)
                if need is None or key not in self.doc["addKeys"]:
                    bad.append([key, kind, "unclassified"])
                    continue
                try:
                    remedy = ov.derive(key + ":" + kind)["errors"][0]["remedy"]
                except Exception as exc:  # noqa: BLE001
                    bad.append([key, kind, type(exc).__name__])
                    continue
                checked += 1
                if any(p not in remedy for p in need) or forbid in remedy:
                    bad.append([key, kind, "remedy does not state this condition"])
        keys_with_faults = {k for k, _ in pairs}
        self.add("route-remedy-keying", not bad and checked >= 10 and keys_with_faults == set(self.doc["addKeys"]) and len(codes) == 2,
                 {"pairsChecked": checked, "bad": bad[:6]})

    def origins(self):
        NE = self.NE
        existing = sorted({o for r in NE.PUBLIC_ROUTE_REGISTRY["keys"].values() for o in r.get("possibleOrigins", [])})
        try:
            NE.public_termination_for(next(iter(self.doc["addKeys"])), self.doc["newOrigin"]["id"])
            unregistered_refused = False
        except NE.AdmissionError:
            unregistered_refused = True
        law = NE.PUBLIC_ROUTE_REGISTRY["originatingBoundaryLaw"]
        actor = self.doc["newOrigin"].get("actor")
        phrase, expected_class = ACTOR_LAW.get(actor, (None, None))
        per_key = {}
        with PR.Overlay(NE, self.doc) as ov:
            for key, row in self.doc["addKeys"].items():
                refused = []
                for origin in existing:
                    try:
                        NE.public_termination_for(key, origin)
                        refused.append(False)
                    except NE.AdmissionError:
                        refused.append(True)
                derived_class = ov.derive(key)["termination"]["class"]
                per_key[key] = all(refused) and row["possibleOrigins"] == [self.doc["newOrigin"]["id"]] and row["originDependent"] is False and derived_class == expected_class
        self.add("route-origin-closed", unregistered_refused and phrase is not None and phrase in law and all(per_key.values()) and self.doc["newOrigin"]["id"] not in existing,
                 {"existingOrigins": existing, "actor": actor, "lawClass": expected_class, "perKey": per_key, "withoutSuccessorRefused": unregistered_refused})

    def remedies(self):
        NE = self.NE
        codes = [r["code"] for r in self.registry_doc["records"]]
        enum = self.common["$defs"]["DomainDetailCode"]["enum"]
        new = [m["code"] for m in self.doc["addDomainDetailCodes"]]
        used = {row["route"]["envelopeDetail"] for row in self.doc["addKeys"].values()}
        aliases = json.dumps(self.registry_doc.get("internalAliases", {}))
        ok = (sorted(codes) == sorted(enum) and not set(new) & set(codes) and not set(new) & set(NE.PUBLIC_ROUTE_REMEDIES)
              and set(new) == used and len(new) == len(set(new))
              and all(m["remedy"] not in set(NE.PUBLIC_ROUTE_REMEDIES.values()) for m in self.doc["addDomainDetailCodes"])
              and not any(k in aliases for k in list(self.doc["addKeys"]) + new))
        self.add("route-remedy-not-reused", ok, {"registryRecords": len(codes), "commonEnum": len(enum), "added": new, "usedAsEnvelopeDetail": sorted(used)})

    def timing(self):
        NE_S, fx, doc = self.NE_S, self.r.fx, self.s.wire
        for key, sel in self.doc["selectors"].items():
            try:
                a = sel["timingAnchor"]
                line = self.s.lines(a["pin"])[a["line"] - 1]
                phrase = TIMING_PHRASES.get(sel["timing"])
                fn = sel["ownerFunction"].split("#")[1] if sel["ownerFunction"] else None
                ok = (sel["timing"] in self.doc["preSpawnTimings"] and phrase is not None and a["needle"] in line and phrase in a["needle"]
                      and OWNER_FUNCTION_TIMING.get(fn) == sel["timing"])
                behaviour = None
                if key == PR.DEP_KEY:
                    lock, provided, activated = self.r.depsrc_case({"files": ["Cargo.toml", "C:x"]})
                    out = REP.dependency_source_set_admit_successor(NE_S, doc, lock, provided, activated)
                    behaviour = {"admitted": out["admitted"], "dependencySourceSetIdMinted": out["identity"] is not None}
                    ok = ok and out["admitted"] is False and out["identity"] is None and out["successorRefusal"]["key"] == key
                elif key == PR.PREP_PATH_KEY:
                    prep, explicit = self.r.prepared_path_case({"generatedLogicalPath": "x" + chr(10) + "/../y.rs"})
                    out = REP.prepared_output_set_admit_successor(NE_S, doc, prep, fx["ctx"], explicit)
                    behaviour = {"outcome": out["outcome"], "ownerRan": out["ownerRan"]}
                    ok = ok and out["outcome"] == "rejected" and out["successorRefusal"]["key"] == key
                elif key == PR.PREP_KEY:
                    prep, explicit = self.r.prepared_case({"fixture": "prepInert", "rows": 257})
                    out = REP.prepared_output_set_admit_successor(NE_S, doc, prep, fx["ctx"], explicit)
                    behaviour = {"outcome": out["outcome"]}
                    ok = ok and out["outcome"] == "rejected" and out["successorRefusal"]["key"] == key
                else:
                    fate = sel.get("planIdFate", "")
                    with PR.Overlay(self.NE, self.doc) as ov:
                        term = ov.derive(key)["termination"]
                    behaviour = {"terminationMembers": sorted(term), "planIdFate": bool(fate)}
                    ok = ok and all(w in fate for w in ("plan2", "run3", "Coverage", "no worker")) and not ({"runId", "coverageId", "executionId"} & set(term)) \
                        and "timing only" in sel.get("anchorScope", "")
                detail = {"timing": sel["timing"], "line": line.strip()[:120], "behaviour": behaviour}
            except Exception as exc:  # noqa: BLE001
                ok, detail = False, type(exc).__name__ + ": " + str(exc)[:240]
            self.add("route-timing-anchored:" + key, ok, detail)

    def selectors(self):
        text = self.s.raw["nativeModel"].decode("utf-8")
        bad = []
        for key, sel in self.doc["selectors"].items():
            if sel["ownerFunction"] is None:
                continue
            name = sel["ownerFunction"].split("#")[1]
            closure = OS.source_closure(text, [name])
            if closure.get(name) != sel.get("ownerFunctionSourceSha256"):
                bad.append(key + ": owner source digest")
            if closure != sel.get("calleeClosureSha256"):
                bad.append(key + ": callee closure digests")
            wrapper = getattr(REP, sel["successorFunction"].split("#")[1])
            if "NE." + name + "(" not in inspect.getsource(wrapper):
                bad.append(key + ": wrapper does not call the owner")
        self.add("route-selectors-owner-source", not bad, bad)

    def prepared_modes(self):
        NE_S, fx, doc = self.NE_S, self.r.fx, self.s.wire
        md = " ".join(x.strip() for x in self.s.lines("nativeMd")[1849:1858])
        derived = {}
        if "refused before Plan construction" in md and "when prepared mode was selected explicitly" in md:
            derived["explicit"] = "refuse"
        if "non-prepared fallback when prepared mode was defaulted" in md:
            derived["defaulted"] = "fallback-non-prepared-with-disclosure"
        params = next(r for r in doc["admission"] if r["id"] == "PREPARED-V3-WIRE-LIMIT")["params"]["modes"]
        sel = self.doc["selectors"][PR.PREP_KEY]
        row = next(r for r in self.doc["routeTableRows"] if r["routeKey"] == PR.PREP_KEY)
        runs = {}
        for name, case, explicit in (("explicit-257", {"fixture": "prepInert", "rows": 257}, True), ("defaulted-257", {"fixture": "prepInert", "rows": 257}, False),
                                     ("defaulted-256", {"fixture": "prepInert", "rows": 256}, False),
                                     ("defaulted-257-one-stale", {"fixture": "prepInert", "rows": 257, "stale": [0]}, False),
                                     ("defaulted-10-one-stale", {"fixture": "prepInert", "rows": 10, "stale": [0]}, False)):
            prep, _ = self.r.prepared_case(case)
            out = REP.prepared_output_set_admit_successor(NE_S, doc, prep, fx["ctx"], explicit)
            runs[name] = {"outcome": out["outcome"], "refusal": (out.get("successorRefusal") or {}).get("key"),
                          "disclosure": [f["kind"] for f in out.get("wireLimitDisclosure") or []], "usableRows": len(out.get("usableRows", []))}
        executed = (runs["explicit-257"]["outcome"] == "rejected" and runs["explicit-257"]["refusal"] == PR.PREP_KEY
                    and runs["defaulted-257"] == {"outcome": "fallback-non-prepared", "refusal": None, "disclosure": ["entries"], "usableRows": 0}
                    and runs["defaulted-256"]["outcome"] == "admitted"
                    and runs["defaulted-257-one-stale"] == {"outcome": "fallback-non-prepared", "refusal": None, "disclosure": ["entries"], "usableRows": 0}
                    and runs["defaulted-10-one-stale"] == {"outcome": "fallback-non-prepared", "refusal": None, "disclosure": [], "usableRows": 9})
        ok = (len(derived) == 2 and params == derived and sel.get("modes") == derived and executed
              and "selected explicitly" in row["condition"] and "defaulted" in row["condition"] and "no refusal" in row["condition"] and "partially stale" in row["condition"])
        self.add("route-prepared-modes", ok, {"ownerDerived": derived, "params": params, "runs": runs})

    def run(self):
        for step in (self.rule_references, self.join, self.owner_family, self.remedy_keying, self.origins, self.remedies, self.timing, self.selectors, self.prepared_modes):
            try:
                step()
            except Exception as exc:  # noqa: BLE001
                self.add("step:routes." + step.__name__, False, type(exc).__name__ + ": " + str(exc)[:300])
