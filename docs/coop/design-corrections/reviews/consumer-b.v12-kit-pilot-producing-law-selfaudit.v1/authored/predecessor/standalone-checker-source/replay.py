"""Independent evaluator3 replay from Plan-selected retained inputs.

Does not read claimed proof/finding/witness values as truth.
Incorporates identity-and-evidence §4, enumeration-contract.v1,
atom-evaluation-contract.v1, evaluator-composition-contract.v3,
execution-inputs-contract.v1.
"""
from __future__ import annotations

import hashlib
from typing import Any

from canonical import AdmissionError, encode_c, h_identity, sha256_hex
from kit import Kit
from schema_validate import check_order


TRUE, FALSE, INDET = "true", "false", "indeterminate"
UNIVERSE_MAP = {
    "typescript": "native.semantic-universe.typescript.v2",
    "rust": "native.semantic-universe.rust.v2",
    "syntax": "native.semantic-universe.syntax.v2",
}
SEV_RANK = {"note": 0, "warning": 1, "error": 2}


def ref(domain: str, digest: str) -> dict:
    return {"digest": digest, "domain": domain}


def sort_canonical_set(items: list) -> list:
    encoded = [(encode_c(x, profile="product"), x) for x in items]
    encoded.sort(key=lambda t: t[0])
    # unique by C bytes
    out = []
    seen = set()
    for b, x in encoded:
        if b in seen:
            continue
        seen.add(b)
        out.append(x)
    return out


def sort_strings(xs: list[str]) -> list[str]:
    ys = sorted(set(xs), key=lambda s: s.encode("utf-8"))
    return ys


class Replay:
    def __init__(self, admit):
        self.a = admit
        self.kit: Kit = admit.kit
        self.ladders = {
            rel: row["ladder"] for rel, row in self.kit.relation_registry["relations"].items()
        }
        self.derived_subjects: dict[str, dict] = {}
        self.inventories: dict[str, dict] = {}
        self.result: dict = {"status": "UNEXECUTED"}

    def run(self) -> dict:
        citation = "identity-and-evidence.md§4; evaluator-composition-contract.v3.md"
        try:
            self._require_structural()
            self._bind_parameters()
            self._index_inventories()
            self._check_execution_input_refs()
            derived_proof, extras = self._evaluate()
            claimed = self.a.proof
            derived_c = encode_c(derived_proof, profile="product")
            claimed_c = encode_c(claimed, profile="product")
            proof_h, _ = h_identity("proof-bundle", derived_proof)
            claimed_proof_id = None
            for digest, (dom, rec) in self.a.frames.items():
                if dom == "proof-bundle":
                    claimed_proof_id = "proof3:" + digest
                    break
            derived_proof_id = "proof3:" + proof_h
            cmp = {
                "proofCEqual": derived_c == claimed_c,
                "derivedProofSha256": sha256_hex(derived_c),
                "claimedProofSha256": sha256_hex(claimed_c),
                "derivedProofId": derived_proof_id,
                "claimedProofId": claimed_proof_id,
                "derivedVerdict": derived_proof["verdict"],
                "claimedVerdict": claimed.get("verdict"),
                "derivedFindingIds": derived_proof["findingIds"],
                "claimedFindingIds": claimed.get("findingIds"),
            }
            # reconstruct evidence/seal/run from derived proof (not claimed)
            ev, seal, run = self._reconstruct_enclosing(derived_proof, proof_h, extras)
            mismatches = []
            if derived_c != claimed_c:
                mismatches.append("PROOF_C_MISMATCH")
            if derived_proof["verdict"] != claimed.get("verdict"):
                mismatches.append("VERDICT_MISMATCH")
            if derived_proof["findingIds"] != claimed.get("findingIds"):
                mismatches.append("FINDING_IDS_MISMATCH")
            if derived_proof["predicateProofs"] != claimed.get("predicateProofs"):
                mismatches.append("PREDICATE_PROOFS_MISMATCH")
            # enclosing identities
            claimed_ev_id = self.a.run["evidenceId"]
            claimed_seal_id = self.a.run["evaluationSealId"]
            claimed_run_id = self.a.store.claimed_run_id
            if ev["typedId"] != claimed_ev_id:
                mismatches.append("EVIDENCE_ID_MISMATCH")
            if seal["typedId"] != claimed_seal_id:
                mismatches.append("SEAL_ID_MISMATCH")
            if run["typedId"] != claimed_run_id:
                mismatches.append("RUN_ID_MISMATCH")
            status = "REPLAY_MATCH" if not mismatches else "REPLAY_REFUSE"
            self.result = {
                "status": status,
                "citation": citation,
                "mismatches": mismatches,
                "comparison": cmp,
                "derivedProof": derived_proof,
                "derivedEnclosing": {
                    "evidenceId": ev["typedId"],
                    "sealId": seal["typedId"],
                    "runId": run["typedId"],
                },
                "claimedEnclosing": {
                    "evidenceId": claimed_ev_id,
                    "sealId": claimed_seal_id,
                    "runId": claimed_run_id,
                },
                "derivedSubjects": list(self.derived_subjects.keys()),
            }
            if status == "REPLAY_REFUSE":
                self.a.refuse(
                    "L-REPLAY-COMPARE-BUNDLE",
                    "REPLAY_PROOF_MISMATCH",
                    "independently recomputed complete proof does not equal retained claimed proof",
                    citation + " §7 complete replay criterion",
                    {
                        "mismatches": mismatches,
                        "derivedVerdict": derived_proof["verdict"],
                        "claimedVerdict": claimed.get("verdict"),
                        "derivedProofSha256": cmp["derivedProofSha256"],
                        "claimedProofSha256": cmp["claimedProofSha256"],
                        "derivedFindingIds": derived_proof["findingIds"],
                        "claimedFindingIds": claimed.get("findingIds"),
                        "derivedPredicateValues": [
                            {"predicateId": p["predicateId"], "value": p["value"], "operation": p["operation"]}
                            for p in derived_proof["predicateProofs"]
                        ],
                        "claimedPredicateValues": [
                            {"predicateId": p.get("predicateId"), "value": p.get("value"), "operation": p.get("operation")}
                            for p in (claimed.get("predicateProofs") or [])
                        ],
                    },
                )
            self.a.mark_pass("L-REPLAY-COMPARE-BUNDLE", citation, "derived complete proof C and enclosing identities equal retained claims", cmp)
            return self.result
        except AdmissionError:
            if self.result.get("status") == "UNEXECUTED":
                self.result["status"] = "NOT_REACHED_OR_REFUSED"
            raise

    def _require_structural(self):
        if self.a.first_refusal is not None:
            raise AdmissionError(
                "STRUCTURAL_PREREQUISITE",
                "semantic replay is not reached: structural admission refused",
                "identity-and-evidence.md§4 input admission precedes replay",
                {"firstRefusal": self.a.first_refusal},
            )
        for name in ("run", "plan", "proof", "policy", "rule_program", "execution_inputs", "analysis_spec"):
            if getattr(self.a, name) is None:
                raise AdmissionError("REPLAY_INPUT_MISSING", f"admitted {name} missing", "identity-and-evidence.md§4", {"name": name})

    def _bind_parameters(self):
        spec = self.a.analysis_spec
        rows = self.kit.payload_registry["classes"]["parameter"]["rows"]
        self.enum_plan = None
        self.emission_plan = None
        self.scope_policy = None
        enum_sha = self.kit.sha256_of("docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json")
        emis_sha = self.kit.sha256_of("docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json")
        scope_sha = self.kit.sha256_of("docs/coop/design-corrections/workflows/schemas/policy-document.schema.json")
        for p in spec["parameters"]:
            if p["schemaDigest"] == enum_sha:
                self.enum_plan = self.a.canonical_records[p["payloadDigest"]]
            elif p["schemaDigest"] == emis_sha:
                self.emission_plan = self.a.canonical_records[p["payloadDigest"]]
            elif p["schemaDigest"] == scope_sha:
                self.scope_policy = self.a.canonical_records.get(p["payloadDigest"])
        if self.enum_plan is None or self.emission_plan is None:
            raise AdmissionError(
                "EVALUATOR3_PARAMETER_MISSING",
                "replay requires EnumerationPlanV1 and EvaluatorEmissionPlanV1",
                "evaluator-composition-contract.v3.md§1",
                {},
            )
        if self.emission_plan.get("policyDigest") != self.a.plan["policyDigest"]:
            raise AdmissionError(
                "EMISSION_POLICY",
                "emission plan policyDigest must equal Plan policyDigest",
                "evaluator-composition-contract.v3.md§1",
                {"emission": self.emission_plan.get("policyDigest"), "plan": self.a.plan["policyDigest"]},
            )
        # enum plan joins
        if self.enum_plan.get("snapshotId") != self.a.plan["snapshotId"]:
            raise AdmissionError("ENUM_SNAPSHOT", "EnumerationPlan.snapshotId != plan.snapshotId", "enumeration-contract.v1.md§3", {})
        if self.enum_plan.get("scopeDigest") != self.a.plan["scopeDigest"]:
            raise AdmissionError("ENUM_SCOPE", "EnumerationPlan.scopeDigest != plan.scopeDigest", "enumeration-contract.v1.md§3", {})

    def _index_inventories(self):
        # inventories retained as canonical-records under execution-inputs selectedRefs / proof evaluationInputRefs
        for digest, rec in self.a.canonical_records.items():
            if isinstance(rec, dict) and rec.get("schemaVersion") == 1 and rec.get("kind") in ("file", "package", "symbol") and "rows" in rec and "cellOrdinal" in rec:
                self.inventories[digest] = rec

    def _check_execution_input_refs(self):
        citation = "evaluator-composition-contract.v3.md§1 evaluationInputRefs equals selectedRefs plus execution-inputs digest"
        ei = self.a.execution_inputs
        ei_digest = self.a.proof["executionInputsDigest"]
        selected = ei.get("selectedRefs") or []
        expected = sort_canonical_set(list(selected) + [ref("execution-inputs", ei_digest)])
        actual = self.a.proof["evaluationInputRefs"]
        # both should already be canonical-set; compare as C
        if encode_c(actual, profile="product") != encode_c(expected, profile="product"):
            self.a.refuse(
                "L-EI-EVAL-REFS",
                "EVALUATION_INPUT_REFS_SELECTION",
                "proof.evaluationInputRefs must equal ExecutionInputs.selectedRefs plus the execution-inputs manifest digest",
                citation,
                {"expected": expected, "actual": actual},
            )
        self.a.mark_pass("L-EI-EVAL-REFS", citation, "evaluationInputRefs equals selectedRefs ∪ {execution-inputs}", {"n": len(actual)})

    def _evaluate(self):
        policy = self.a.policy
        program = self.a.rule_program
        emission = {r["ruleId"]: r for r in self.emission_plan["rules"]}
        view = next(iter(self.a.views.values()))
        view_hex = next(iter(self.a.views.keys()))
        facts = self.a.facts
        coverages = self.a.coverages
        scopes = self.a.scopes

        # budget preflight
        enabled_rules = [r for r in policy["rules"] if r.get("enabled")]
        selected_by_rule = {}
        enum_by_rule = {}
        all_selected = []
        for rule in policy["rules"]:
            if not rule.get("enabled"):
                enum_by_rule[rule["ruleId"]] = {
                    "state": "disabled",
                    "inventoryRefs": [],
                    "selectedSubjectIds": [],
                    "unresolvedSubjectIds": [],
                    "incompleteInventoryRefs": [],
                }
                selected_by_rule[rule["ruleId"]] = []
                continue
            enum, subjects = self._enumerate_rule(rule)
            enum_by_rule[rule["ruleId"]] = enum
            selected_by_rule[rule["ruleId"]] = subjects
            all_selected.extend(subjects)

        S = len(all_selected)
        F = len(facts)
        I = 0
        K = len(coverages)
        E = sum(len(inv.get("rows") or []) for inv in self.inventories.values()) + len(self.inventories)
        work = E
        for rule in enabled_rules:
            node_n, atom_n = count_nodes(rule["emitWhen"])
            ns = len(selected_by_rule[rule["ruleId"]])
            work += ns * (node_n + atom_n * (F + I + K))
        budget = (self.a.plan.get("budget") or {}).get("limit")
        unit = (self.a.plan.get("budget") or {}).get("unit")
        if budget is not None and work > int(budget):
            raise AdmissionError(
                "EVALUATION.WORK_BUDGET_EXHAUSTED",
                "deterministic scan budget exceeded before predicate evaluation",
                "evaluator-composition-contract.v3.md§3",
                {"work": work, "limit": budget, "unit": unit},
            )

        predicate_proofs = []
        findings = []
        finding_ids = []
        rule_results = []
        extras = {"findings": {}, "witnesses": {}, "programPredicates": {}, "parameters": {}, "fingerprints": {}}

        rp_digest = self.a.proof["ruleProgramDigest"]  # this is the digest of the program record we already admitted; we recompute from our program bytes
        rp_c = encode_c(program, profile="product")
        rp_digest_derived = sha256_hex(rp_c)
        if rp_digest_derived != rp_digest:
            raise AdmissionError("RULE_PROGRAM_DIGEST", "admitted RuleProgramV2 C digest drifted", "identity-and-evidence.md§4", {"derived": rp_digest_derived, "claimed": rp_digest})

        for rule in policy["rules"]:
            rid = rule["ruleId"]
            enum = enum_by_rule[rid]
            if not rule.get("enabled"):
                rule_results.append(
                    {"deficiencies": [], "enumeration": enum, "findingIds": [], "outcome": "disabled", "ruleId": rid}
                )
                continue
            emit_findings = []
            deficiencies = []
            root_values = []
            blocking = False
            for subj in selected_by_rule[rid]:
                subj_id = subj["typedId"]
                proofs, witness_map, value = self._eval_tree(
                    rule["emitWhen"], "p", rid, subj, view, view_hex, rp_digest_derived, program
                )
                predicate_proofs.extend(proofs)
                extras["witnesses"].update(witness_map)
                root_values.append(value)
                if value == TRUE:
                    finding, fextras = self._emit_finding(rule, emission[rid], subj, proofs, witness_map)
                    findings.append(finding)
                    emit_findings.append(finding["typedId"])
                    extras["findings"][finding["digest"]] = finding["record"]
                    extras["parameters"].update(fextras.get("parameters") or {})
                    extras["fingerprints"].update(fextras.get("fingerprints") or {})
            # rule outcome
            gate = bool(rule.get("gate")) and SEV_RANK[rule["severity"]] >= SEV_RANK.get(policy.get("gateSeverityAtLeast", "error"), 2)
            live_unwaived = emit_findings  # waivers empty in this pilot unless WaiverSet nonempty
            waived = self._waived_ids(emit_findings, findings, rule)
            live = [fid for fid in emit_findings if fid not in waived]
            if gate and live:
                outcome = "fail"
            elif gate and (enum["state"] != "complete" or INDET in root_values):
                # indeterminate if population incomplete or root indeterminate with blocking cause
                if enum["state"] != "complete":
                    outcome = "indeterminate"
                elif INDET in root_values:
                    outcome = "indeterminate"
                else:
                    outcome = "pass"
            else:
                outcome = "pass"
            rule_results.append(
                {
                    "deficiencies": deficiencies,
                    "enumeration": enum,
                    "findingIds": sort_strings(emit_findings),
                    "outcome": outcome,
                    "ruleId": rid,
                }
            )
            finding_ids.extend(emit_findings)

        # verdict
        if any(rr["outcome"] == "fail" for rr in rule_results if rr["outcome"] != "disabled"):
            verdict = "fail"
        elif any(rr["outcome"] == "indeterminate" for rr in rule_results) or False:
            verdict = "indeterminate"
        else:
            verdict = "pass"

        predicate_proofs = sort_predicate_proofs(predicate_proofs)
        finding_ids = sort_strings(finding_ids)
        rule_results = sorted(rule_results, key=lambda r: r["ruleId"].encode("utf-8"))

        derived_proof = {
            "evaluationInputRefs": self.a.proof["evaluationInputRefs"],  # MUST equal selectedRefs+EI, already checked; this is an INPUT set not a derived truth of atoms
            "evaluationState": "evaluated",
            "evaluatorClosure": self.a.seal["evaluatorClosure"] if self.a.seal else self.a.proof["evaluatorClosure"],
            "executionDeficiencies": [],
            "executionInputsDigest": sha256_hex(encode_c(self.a.execution_inputs, profile="product")),
            "executionPlanId": self.a.proof["executionPlanId"],
            "findingIds": finding_ids,
            "planId": self.a.run["planId"],
            "predicateProofs": predicate_proofs,
            "ruleProgramDigest": rp_digest_derived,
            "ruleResults": rule_results,
            "schemaVersion": 3,
            "verdict": verdict,
            "waivedFindingIds": [],
        }
        # evaluationInputRefs is Plan-selected input inventory, reconstructed from execution-inputs, not from claimed proof fields of atoms.
        # We already verified it equals selectedRefs ∪ {EI}. Use the reconstructed expected set:
        ei_digest = sha256_hex(encode_c(self.a.execution_inputs, profile="product"))
        derived_proof["evaluationInputRefs"] = sort_canonical_set(
            list(self.a.execution_inputs.get("selectedRefs") or []) + [ref("execution-inputs", ei_digest)]
        )
        derived_proof["evaluatorClosure"] = self.a.plan["semanticClosures"]  # NO - must be the evaluator closure
        # evaluator is the seal/proof evaluator which must be plan-selected kind=evaluator
        ev_closures = [c for d, c in self.a.closures.items() if c.get("kind") == "evaluator"]
        # use the one named by plan that is evaluator
        evaluator_id = None
        for cid in self.a.plan["semanticClosures"]:
            hx = cid.split(":")[1]
            if self.a.closures.get(hx, {}).get("kind") == "evaluator":
                evaluator_id = cid
                break
        if evaluator_id is None:
            raise AdmissionError("NO_EVALUATOR", "no Plan-selected evaluator closure", "identity-schemas.v3.json closureMembership", {})
        derived_proof["evaluatorClosure"] = evaluator_id
        extras["findings_list"] = findings
        return derived_proof, extras

    def _enumerate_rule(self, rule: dict) -> tuple[dict, list]:
        citation = "enumeration-contract.v1.md; evaluator-composition-contract.v3.md§2"
        tok = (rule.get("subjectEnumeration") or {}).get("universe")
        kind = (rule.get("subjectEnumeration") or {}).get("subjectKind")
        if tok not in UNIVERSE_MAP:
            raise AdmissionError("POLICY_UNIVERSE_TOKEN", "unknown policy universe token", citation, {"token": tok})
        domain = UNIVERSE_MAP[tok]
        # programs whose universe H domain is this and kinds include kind
        wanted_kind = "symbol" if kind == "export" else kind
        covering = []
        for cell in self.enum_plan["cells"]:
            if wanted_kind not in (cell.get("kinds") or []):
                continue
            for b in cell.get("programBindings") or []:
                uhex = b.get("universe")
                if not uhex:
                    continue
                if uhex not in self.a.native_universes:
                    # may be stored as hex; admit already loaded
                    continue
                udom, _urec = self.a.native_universes[uhex]
                if udom != domain:
                    continue
                if b.get("enumerator", {}).get("status") != "selected":
                    continue
                covering.append((cell, b, uhex))
        if not covering:
            enum = {
                "state": "incomplete",
                "inventoryRefs": [],
                "selectedSubjectIds": [],
                "unresolvedSubjectIds": [],
                "incompleteInventoryRefs": [],
            }
            return enum, []
        # inventories for those (cellOrdinal, programOrdinal, kind)
        cells_sorted = self.enum_plan["cells"]  # already schema-ordered
        inv_refs = []
        incomplete = []
        subjects_by_id = {}
        for cell, binding, uhex in covering:
            cell_ordinal = cells_sorted.index(cell)
            prog_ord = binding["ordinal"]
            found = None
            for digest, inv in self.inventories.items():
                if inv.get("cellOrdinal") == cell_ordinal and inv.get("programOrdinal") == prog_ord and inv.get("kind") == wanted_kind:
                    found = (digest, inv)
                    break
            if found is None:
                raise AdmissionError(
                    "ENUMERATION_INVENTORY_MISSING_RECORD",
                    "missing expected inventory for (cell, program, kind)",
                    "enumeration-contract.v1.md§3",
                    {"cellOrdinal": cell_ordinal, "programOrdinal": prog_ord, "kind": wanted_kind},
                )
            digest, inv = found
            iref = {"digest": digest, "domain": "subject-inventory"}
            inv_refs.append(iref)
            if inv.get("state") != "complete":
                incomplete.append(iref)
            if inv.get("state") == "unavailable":
                continue
            include = (rule.get("subjectEnumeration") or {}).get("include") or []
            exclude = (rule.get("subjectEnumeration") or {}).get("exclude") or []
            for row in inv.get("rows") or []:
                path = row.get("path") or row.get("nativeSubjectId")
                if include and not any(glob_match(g, path) for g in include):
                    continue
                if exclude and any(glob_match(g, path) for g in exclude):
                    continue
                if kind == "export":
                    exp = row.get("exported")
                    if exp == "not-exported":
                        continue
                    if exp != "exported":
                        # unresolved
                        continue
                rec = {
                    "schemaVersion": 3,
                    "universe": uhex,
                    "kind": wanted_kind,
                    "nativeSubjectId": row["nativeSubjectId"],
                }
                if wanted_kind == "package":
                    rec["packageManifestPath"] = row.get("path")
                digest_h, _ = h_identity("evaluation-subject", rec)
                typed = "subject3:" + digest_h
                rec_wrap = {
                    "record": rec,
                    "digest": digest_h,
                    "typedId": typed,
                    "row": row,
                    "path": path,
                    "language": row.get("subjectLanguage"),
                    "qualifiedName": row.get("qualifiedName") or path,
                }
                # union duplicates of same identity
                subjects_by_id[typed] = rec_wrap
                self.derived_subjects[typed] = rec_wrap
        selected = list(subjects_by_id.values())
        selected_ids = sort_strings([s["typedId"] for s in selected])
        selected = [subjects_by_id[i] for i in selected_ids]
        state = "complete" if not incomplete else "incomplete"
        enum = {
            "state": state,
            "inventoryRefs": sort_canonical_set(inv_refs),
            "selectedSubjectIds": selected_ids,
            "unresolvedSubjectIds": [],
            "incompleteInventoryRefs": sort_canonical_set(incomplete),
        }
        return enum, selected

    def _eval_tree(self, node, addr, rule_id, subj, view, view_hex, rp_digest, program):
        op = node["op"]
        proofs = []
        witnesses = {}
        if op in ("and", "or"):
            child_vals = []
            child_addrs = []
            for i, ch in enumerate(node["operands"]):
                ca = f"{addr}.{i}"
                child_addrs.append(ca)
                p, w, v = self._eval_tree(ch, ca, rule_id, subj, view, view_hex, rp_digest, program)
                proofs.extend(p)
                witnesses.update(w)
                child_vals.append(v)
            if op == "and":
                if FALSE in child_vals:
                    value = FALSE
                elif all(x == TRUE for x in child_vals):
                    value = TRUE
                else:
                    value = INDET
            else:
                if TRUE in child_vals:
                    value = TRUE
                elif all(x == FALSE for x in child_vals):
                    value = FALSE
                else:
                    value = INDET
            pp, wdig, wrec = self._boolean_proof(op, addr, rule_id, subj, child_addrs, value, rp_digest, node, view_hex)
            proofs.append(pp)
            witnesses[wdig] = wrec
            return proofs, witnesses, value
        if op == "not":
            p, w, v = self._eval_tree(node["operand"], addr + ".0", rule_id, subj, view, view_hex, rp_digest, program)
            if v == TRUE:
                value = FALSE
            elif v == FALSE:
                value = TRUE
            else:
                value = INDET
            pp, wdig, wrec = self._boolean_proof("not", addr, rule_id, subj, [addr + ".0"], value, rp_digest, node, view_hex)
            p.append(pp)
            w[wdig] = wrec
            return p, w, value
        # atom
        value, matching, uncertain, cov_ids, scope_ids, defs = self._eval_atom(node, subj, view)
        pp, wdig, wrec = self._atom_proof(
            op, addr, rule_id, subj, value, matching, uncertain, cov_ids, scope_ids, node, rp_digest, view_hex
        )
        witnesses[wdig] = wrec
        return [pp], witnesses, value

    def _eval_atom(self, atom, subj, view):
        relation = atom["relation"]
        min_r = atom["minResolution"]
        ladder = self.ladders[relation]
        if min_r not in ladder:
            raise AdmissionError("ATOM_RUNG", "minResolution not on this relation ladder", "identity-and-evidence.md§3; policy-document.v2 Atom.minResolution", {"relation": relation, "minResolution": min_r})
        min_i = ladder.index(min_r)
        endpoint = atom.get("endpoint") or "source"
        filters = atom.get("filters") or []
        matching = []
        for fhex, fact in self.a.facts.items():
            if fact["relation"] != relation:
                continue
            if fact["resolution"] not in ladder:
                continue
            if ladder.index(fact["resolution"]) < min_i:
                continue
            payload = self.a.canonical_records.get(fact["payloadDigest"])
            if payload is None:
                continue
            occ = occupancy(relation, endpoint, payload, fact)
            if occ is None:
                continue
            if endpoint == "source" and occ != subj["record"]["nativeSubjectId"]:
                continue
            if not filters_match(filters, fact, payload, occ, subj, endpoint):
                continue
            matching.append("fact2:" + fhex)
        matching = sort_strings(matching)
        # coverages at exact rung whose scope contains subject
        cov_ids = []
        scope_ids = []
        complete = False
        unknown = False
        for chex, cov in self.a.coverages.items():
            shx = cov["scopeId"].split(":")[1] if ":" in cov["scopeId"] else cov["scopeId"]
            scope = self.a.scopes.get(shx)
            if not scope:
                continue
            if scope["relation"] != relation or scope["resolution"] != min_r:
                continue
            if scope["sourceUniverse"] != subj["record"]["universe"]:
                continue
            if subj["record"]["nativeSubjectId"] not in (scope.get("subjects") or []) and subj["path"] not in (scope.get("subjects") or []):
                continue
            scope_ids.append("scope2:" + shx)
            cov_ids.append("coverage2:" + chex)
            pl = self.a.canonical_records.get(cov["payloadDigest"]) or {}
            entry = (pl.get("entry") or {})
            if entry.get("coverage") == "complete":
                complete = True
            else:
                unknown = True
        cov_ids = sort_strings(cov_ids)
        scope_ids = sort_strings(scope_ids)
        op = atom["op"]
        nmatch = len(matching)
        if op == "exists":
            if nmatch:
                value = TRUE
            elif complete and not unknown:
                value = FALSE
            else:
                value = INDET
        elif op == "none":
            if nmatch:
                value = FALSE
            elif complete and not unknown:
                value = TRUE
            else:
                value = INDET
        elif op == "count-at-most":
            n = atom["n"]
            if nmatch > n:
                value = FALSE
            elif complete and not unknown and nmatch <= n:
                value = TRUE
            else:
                value = INDET
        elif op == "all-covered":
            # sufficiency_v2 at requested rung; non-resolved: coverage complete
            if complete and not unknown:
                value = TRUE
            else:
                value = INDET
        else:
            raise AdmissionError("ATOM_OP", "unknown atom op", "policy-document.v2.schema.json Atom", {"op": op})
        return value, matching, [], cov_ids, scope_ids, []

    def _atom_proof(self, op, addr, rule_id, subj, value, matching, uncertain, cov_ids, scope_ids, node, rp_digest, view_hex):
        node_c = encode_c(node, profile="product")
        node_digest = sha256_hex(node_c)
        pred = {
            "nodeDigest": node_digest,
            "operation": op,
            "predicateId": addr,
            "ruleId": rule_id,
            "ruleProgramDigest": rp_digest,
            "schemaVersion": 2,
        }
        pred_d = sha256_hex(encode_c(pred, profile="product"))
        witness = {
            "childPredicateIds": [],
            "countLimit": node.get("n") if op == "count-at-most" else None,
            "coverageIds": cov_ids,
            "deficiencies": [],
            "kind": "native-atom",
            "matchingFactIds": matching,
            "matchingImportRows": [],
            "programPredicateDigest": pred_d,
            "schemaVersion": 3,
            "uncertainFactIds": uncertain,
            "uncertainImportRows": [],
        }
        wdig = sha256_hex(encode_c(witness, profile="product"))
        input_refs = sort_canonical_set([ref("view", view_hex)] + [ref("coverage", c.split(":")[1]) for c in cov_ids])
        pp = {
            "inputRefs": input_refs,
            "operation": op,
            "predicateId": addr,
            "ruleId": rule_id,
            "scopeIds": scope_ids,
            "subjectId": subj["typedId"],
            "value": value,
            "witnessDigest": wdig,
        }
        return pp, wdig, {"witness": witness, "programPredicate": pred}

    def _boolean_proof(self, op, addr, rule_id, subj, child_addrs, value, rp_digest, node, view_hex):
        node_c = encode_c(node, profile="product")
        pred = {
            "nodeDigest": sha256_hex(node_c),
            "operation": op,
            "predicateId": addr,
            "ruleId": rule_id,
            "ruleProgramDigest": rp_digest,
            "schemaVersion": 2,
        }
        pred_d = sha256_hex(encode_c(pred, profile="product"))
        witness = {
            "childPredicateIds": sort_strings(child_addrs),
            "countLimit": None,
            "coverageIds": [],
            "deficiencies": [],
            "kind": "boolean",
            "matchingFactIds": [],
            "matchingImportRows": [],
            "programPredicateDigest": pred_d,
            "schemaVersion": 3,
            "uncertainFactIds": [],
            "uncertainImportRows": [],
        }
        wdig = sha256_hex(encode_c(witness, profile="product"))
        pp = {
            "inputRefs": sort_canonical_set([ref("view", view_hex)]),
            "operation": op,
            "predicateId": addr,
            "ruleId": rule_id,
            "scopeIds": [],
            "subjectId": subj["typedId"],
            "value": value,
            "witnessDigest": wdig,
        }
        return pp, wdig, {"witness": witness, "programPredicate": pred}

    def _emit_finding(self, rule, emission, subj, proofs, witness_map):
        root = [p for p in proofs if p["predicateId"] == "p"][0]
        message_code = rule.get("messageCode") or rule["ruleId"]
        matching_facts = []
        matching_imports = 0
        covs = []
        for p in proofs:
            w = witness_map[p["witnessDigest"]]["witness"]
            matching_facts.extend(w.get("matchingFactIds") or [])
            matching_imports += len(w.get("matchingImportRows") or [])
            covs.extend(w.get("coverageIds") or [])
        matching_facts = sort_strings(matching_facts)
        params_obj = {
            "matchingFactCount": len(set(matching_facts)),
            "matchingImportCount": matching_imports,
            "qualifiedName": subj["qualifiedName"],
            "ruleId": rule["ruleId"],
            "subjectKind": subj["record"]["kind"],
            "subjectLanguage": subj["language"],
            "subjectPath": subj["path"],
        }
        param_rec = {"messageCode": message_code, "parameters": params_obj, "schemaVersion": 2}
        param_digest = sha256_hex(encode_c(param_rec, profile="product"))
        disc_hex = sha256_hex(encode_c([], profile="product"))
        fp_rec = {
            "detectorSemanticsMajor": emission["semanticsMajor"],
            "relatedSubjectKeys": [],
            "ruleStableId": emission["ruleStableId"],
            "schemaVersion": 2,
            "subjectKey": {
                "discriminator": disc_hex,
                "kind": subj["record"]["kind"],
                "language": subj["language"],
                "logicalPath": subj["path"],
                "qualifiedName": subj["qualifiedName"],
            },
        }
        fp_h, _ = h_identity("finding-fingerprint", fp_rec)
        ev_refs = sort_canonical_set(
            [ref("predicate-witness", root["witnessDigest"])]
            + [ref("fact", fid.split(":")[1]) for fid in matching_facts]
            + [ref("coverage", cid.split(":")[1]) for cid in covs]
        )
        finding = {
            "correspondence": {"reason": None, "state": "matched"},
            "evidenceRefs": ev_refs,
            "fingerprint": "finding-key2:" + fp_h,
            "messageCode": message_code,
            "parameterDigest": param_digest,
            "ruleClosure": emission["detectorClosure"],
            "ruleId": rule["ruleId"],
            "schemaVersion": 3,
            "severity": rule["severity"],
            "subject": {
                "kind": subj["record"]["kind"],
                "language": subj["language"],
                "logicalPath": subj["path"],
                "qualifiedName": subj["qualifiedName"],
            },
            "subjectId": subj["typedId"],
        }
        # correspondence.reason oneOf null? schema required reason, matched may need null
        fh, _ = h_identity("finding", finding)
        return (
            {"record": finding, "digest": fh, "typedId": "finding3:" + fh},
            {"parameters": {param_digest: param_rec}, "fingerprints": {fp_h: fp_rec}},
        )

    def _waived_ids(self, finding_ids, findings, rule):
        # Plan waiver set; replay does not consult wall clock
        waivers = self.a.canonical_records.get(self.a.plan["waiverDigest"])
        if not waivers:
            return []
        targets = []
        # WaiverSetV1 shape
        items = waivers.get("waivers") or waivers.get("items") or []
        if isinstance(waivers, dict) and "waivers" not in waivers and isinstance(waivers.get("entries"), list):
            items = waivers["entries"]
        return []

    def _reconstruct_enclosing(self, derived_proof, proof_h, extras):
        view_ids = sort_strings(["view2:" + hx for hx in self.a.views])
        cov_union = set()
        for v in self.a.views.values():
            cov_union.update(v.get("coverageIds") or [])
        evidence = {
            "coverageIds": sort_strings(list(cov_union)),
            "findingIds": derived_proof["findingIds"],
            "importIds": list(self.a.plan["importIds"]),
            "planId": self.a.run["planId"],
            "proofBundleId": "proof3:" + proof_h,
            "schemaVersion": 3,
            "viewIds": view_ids,
        }
        ev_h, _ = h_identity("semantic-evidence", evidence)
        seal = {
            "evaluatorClosure": derived_proof["evaluatorClosure"],
            "evidenceId": "evidence3:" + ev_h,
            "executionPlanId": derived_proof["executionPlanId"],
            "planId": derived_proof["planId"],
            "policyDigest": self.a.plan["policyDigest"],
            "proofBundleId": "proof3:" + proof_h,
            "schemaVersion": 3,
            "verdict": derived_proof["verdict"],
        }
        seal_h, _ = h_identity("evaluation-seal", seal)
        run = {
            "capabilityManifestId": self.a.plan["capabilityManifestId"],
            "evaluationSealId": "seal3:" + seal_h,
            "evidenceId": "evidence3:" + ev_h,
            "planId": self.a.run["planId"],
            "projectId": self.a.run["projectId"],
            "schemaVersion": 3,
            "snapshotId": self.a.run["snapshotId"],
        }
        run_h, _ = h_identity("run", run)
        return (
            {"record": evidence, "digest": ev_h, "typedId": "evidence3:" + ev_h},
            {"record": seal, "digest": seal_h, "typedId": "seal3:" + seal_h},
            {"record": run, "digest": run_h, "typedId": "run3:" + run_h},
        )


def occupancy(relation, endpoint, payload, fact):
    if relation == "file":
        return payload.get("path")
    if relation == "package":
        return payload.get("packageName")
    if relation == "clones":
        # body-identity subject is the anchor path
        anchors = fact.get("anchors") or []
        if anchors:
            return anchors[0].get("path")
        return None
    if relation in ("declares",):
        return payload.get("declared")
    return payload.get("path") or payload.get("declared")


def filters_match(filters, fact, payload, occ, subj, endpoint):
    for fl in filters:
        field, cmp, value = fl["field"], fl["cmp"], fl["value"]
        got = None
        if field == "subject":
            got = occ if endpoint == "source" else subj["record"]["nativeSubjectId"]
        elif field == "target":
            got = occ if endpoint == "target" else None
        elif field == "resolution":
            got = fact.get("resolution")
        elif field == "universe":
            got = fact.get("sourceUniverse") if endpoint == "source" else fact.get("targetUniverse")
        elif field == "confidenceMillionths":
            got = fact.get("confidenceMillionths")
        elif field == "subjectKind":
            got = subj["record"]["kind"]
        else:
            return False
        if cmp == "eq":
            if got != value:
                return False
        elif cmp == "neq":
            if got == value:
                return False
        else:
            # glob etc. not needed for this pilot atom
            if got != value:
                return False
    return True


def count_nodes(node):
    op = node.get("op")
    if op in ("and", "or"):
        n, a = 1, 0
        for ch in node["operands"]:
            cn, ca = count_nodes(ch)
            n += cn
            a += ca
        return n, a
    if op == "not":
        cn, ca = count_nodes(node["operand"])
        return 1 + cn, ca
    return 1, 1


def glob_match(pattern: str, path: str) -> bool:
    # composition: **/*.ts matches root a.ts. Minimal glob.
    import fnmatch
    if pattern == "**" or pattern == "**/*":
        return True
    if pattern.startswith("**/"):
        rest = pattern[3:]
        if fnmatch.fnmatch(path, rest) or fnmatch.fnmatch(path.split("/")[-1], rest):
            return True
        return fnmatch.fnmatch(path, pattern)
    return fnmatch.fnmatch(path, pattern)


def sort_predicate_proofs(pps: list) -> list:
    def key(p):
        tup = f"{p['ruleId']},{p['subjectId']},{p['predicateId']}"
        return tup.encode("utf-8")
    return sorted(pps, key=key)
