"""Owner-joined public route checks (candidate 03, RF-1).

Every public field of every new refusal is DERIVED, never compared literal-to-literal: the published rows of
public-route-successor.v1.json are applied in memory to the pinned native_evidence_model.v2 route registry and remedy
table, and termination, envelope errors and exit come from the owner public_termination_for, failure_envelope_errors and
CLASS_TO_EXIT. Terminations and details are validated against the pinned workflows common StepTermination and
DomainDetail schemas (DomainDetailCode extended by exactly the published members). The owner request-precondition row
family is executed (owner D9_MAP, owner prepared_output_set_admit refusal, owner release-declaration route)."""
import copy
import inspect
import json

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

import public_routes as PR
import representability as REP

TIMING_PHRASES = {"before-plan-id": "before PlanId", "before-plan-construction": "before Plan construction", "plan-time-no-spawn": "Plan time (no spawn)"}


class Routes:
    def __init__(self, ref):
        self.r, self.s, self.NE = ref, ref.s, ref.NE
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
        self.add("route-rule-references", not bad and set(refs) == set(keys) and selectors == {k: sorted(refs.get(k, [])) for k in keys},
                 {"bad": bad, "references": refs})

    def join(self):
        NE = self.NE
        st_v, dd_v = self.validator("StepTermination"), self.validator("DomainDetail")
        owner = self.doc["joinedOwnerRows"]["routeRegistry"]
        owner_term = NE.public_termination_for(owner["key"], owner["origin"])
        codes = {m["code"]: m["remedy"] for m in self.doc["addDomainDetailCodes"]}
        with PR.Overlay(NE, self.doc) as ov:
            for key, row in self.doc["addKeys"].items():
                try:
                    d = ov.derive(key + ":probe-subject")
                    term, errors = d["termination"], d["errors"]
                    schema_errors = [e.message for e in st_v.iter_errors(term)] + [e.message for err in errors for e in dd_v.iter_errors(err)]
                    ok = (not schema_errors and self.doc["publicForm"] == "internal-key-domainDetail-absent"
                          and set(term) == set(owner_term) and "domainDetail" not in term
                          and term["class"] == owner_term["class"] and term["errorCode"] == owner_term["errorCode"]
                          and d["exitCode"] == NE.CLASS_TO_EXIT[owner_term["class"]]
                          and len(errors) == 1 and errors[0]["code"] == row["route"]["envelopeDetail"] and errors[0]["code"] in codes
                          and errors[0]["remedy"] == codes[errors[0]["code"]] and errors[0]["subject"] == key + ":probe-subject")
                    detail = {"termination": term, "exitCode": d["exitCode"], "errors": errors, "schemaErrors": schema_errors[:3], "ownerRow": owner_term}
                except Exception as exc:  # noqa: BLE001
                    ok, detail = False, type(exc).__name__ + ": " + str(exc)[:240]
                self.add("route-join:" + key, ok, detail)

    def owner_family(self):
        NE, fx = self.NE, self.r.fx
        d9 = NE.D9_MAP[self.doc["joinedOwnerRows"]["modelD9Map"]]
        executed = NE.prepared_output_set_admit(copy.deepcopy(fx["prepDylib"]), fx["ctx"], True)["d9"]
        results = []
        with PR.Overlay(NE, self.doc) as ov:
            for row in self.doc["routeTableRows"]:
                d = ov.derive(row["routeKey"])
                line = self.s.lines(row["target"]["pin"])[row["target"]["line"] - 1]
                results.append(row["class"] == d["termination"]["class"] == d9["class"] == executed["class"]
                               and row["errorCode"] == d["termination"]["errorCode"] == d9["code"] == executed["code"]
                               and int(row["exitCode"]) == d["exitCode"] == d9["exitCode"] == executed["exitCode"]
                               and row["target"]["rowNeedle"] in line and "`REQUEST.PRECONDITION_FAILED`" in line and "`request-rejected` (2)" in line
                               and row["routeKey"] in row["carrier"] and self.doc["addKeys"][row["routeKey"]]["route"]["envelopeDetail"] in row["carrier"])
        self.add("route-join-owner-family", bool(results) and all(results) and {r["routeKey"] for r in self.doc["routeTableRows"]} == set(self.doc["addKeys"]),
                 {"rows": results, "ownerD9Row": d9, "executedOwnerRefusal": executed})

    def origins(self):
        NE = self.NE
        existing = sorted({o for r in NE.PUBLIC_ROUTE_REGISTRY["keys"].values() for o in r.get("possibleOrigins", [])})
        try:
            NE.public_termination_for(next(iter(self.doc["addKeys"])), self.doc["newOrigin"]["id"])
            unregistered_refused = False
        except NE.AdmissionError:
            unregistered_refused = True
        per_key = {}
        with PR.Overlay(NE, self.doc):
            for key, row in self.doc["addKeys"].items():
                refused = []
                for origin in existing:
                    try:
                        NE.public_termination_for(key, origin)
                        refused.append(False)
                    except NE.AdmissionError:
                        refused.append(True)
                per_key[key] = all(refused) and row["possibleOrigins"] == [self.doc["newOrigin"]["id"]] and row["originDependent"] is False
        self.add("route-origin-closed", unregistered_refused and all(per_key.values()) and self.doc["newOrigin"]["id"] not in existing,
                 {"existingOrigins": existing, "perKey": per_key, "withoutSuccessorRefused": unregistered_refused})

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
        NE, fx, doc = self.NE, self.r.fx, self.s.wire
        for key, sel in self.doc["selectors"].items():
            try:
                a = sel["timingAnchor"]
                line = self.s.lines(a["pin"])[a["line"] - 1]
                phrase = TIMING_PHRASES.get(sel["timing"])
                ok = sel["timing"] in self.doc["preSpawnTimings"] and phrase is not None and a["needle"] in line and phrase in a["needle"]
                behaviour = "no executable boundary (pure planner over Plan-bound inputs)"
                if key == PR.DEP_KEY:
                    lock, provided, activated = self.r.depsrc_case({"files": ["Cargo.toml", "C:x"]})
                    out = REP.dependency_source_set_admit_successor(NE, doc, lock, provided, activated)
                    behaviour = {"admitted": out["admitted"], "dependencySourceSetIdMinted": out["identity"] is not None}
                    ok = ok and out["admitted"] is False and out["identity"] is None and out["successorRefusal"]["key"] == key
                elif key == PR.PREP_KEY:
                    prep, explicit = self.r.prepared_case({"fixture": "prepInert", "rows": 257})
                    out = REP.prepared_output_set_admit_successor(NE, doc, prep, fx["ctx"], explicit)
                    behaviour = {"outcome": out["outcome"]}
                    ok = ok and out["outcome"] == "rejected" and out["successorRefusal"]["key"] == key
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
            if PR.function_source_sha256(text, name) != sel.get("ownerFunctionSourceSha256"):
                bad.append(key + ": owner source digest")
            wrapper = getattr(REP, sel["successorFunction"].split("#")[1])
            if "NE." + name + "(" not in inspect.getsource(wrapper):
                bad.append(key + ": wrapper does not call the owner")
        self.add("route-selectors-owner-source", not bad, bad)

    def run(self):
        for step in (self.rule_references, self.join, self.owner_family, self.origins, self.remedies, self.timing, self.selectors):
            try:
                step()
            except Exception as exc:  # noqa: BLE001
                self.add("step:routes." + step.__name__, False, type(exc).__name__ + ": " + str(exc)[:300])
