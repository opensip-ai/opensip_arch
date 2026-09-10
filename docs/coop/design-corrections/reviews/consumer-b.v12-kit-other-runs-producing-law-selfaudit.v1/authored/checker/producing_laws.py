"""Successor producing-law checks the original FULL_ADMIT did not execute.

Owners: enumeration-contract.v1.md, execution-inputs-contract.v1.md,
atom-evaluation-contract.v1.md, evaluator-composition-contract.v3.md,
plus incorporated schemas/annotations. Claimed extents, selectedRefs,
outcomes, and proof fields are comparison targets, never producing oracles.
"""
from __future__ import annotations

import json
import tomllib
from typing import Any

from .canonical import encode_c, LexicalRefusal, lexical_scan_raw
from .identity import H, sha256, typed_id


EXCLUDE_MEMBERSHIP = {"outside-project-boundary"}
EXCLUDE_REASON = {
    "host-ignore-convention",
    "nested-repository",
    "nested-project",
    "custody-excluded",
}

CAPABILITY_RELATIONS = {
    "inventory": [("file", "enumerated"), ("package", "manifest-declared"), ("vcs-change", "vcs-reported")],
    "syntax": [("declares", "syntactic"), ("literal", "syntactic"), ("control-flow", "syntactic")],
    "clones-fact": [("clones", "normalized-body-hash")],
    "imports": [("imports", "resolved-target")],
    "references": [("references", "resolved-binding")],
    "calls": [("calls", "resolved-callee")],
    "types": [("types", "checked")],
    "reachability": [("reachability", "from-resolved-calls")],
    "unresolved-edge": [("unresolved-edge", "observed")],
}


def ref_key(r: dict) -> tuple[str, str]:
    return (r.get("domain") or "", r.get("digest") or "")


def canonical_ref_set(refs: list[dict]) -> list[dict]:
    uniq = {}
    for r in refs:
        if not r.get("digest"):
            continue
        item = {"digest": r["digest"], "domain": r.get("domain") or ""}
        uniq[ref_key(item)] = item
    items = list(uniq.values())
    items.sort(key=lambda it: encode_c(it))
    return items


class ProducingLawAudit:
    def __init__(self, replay):
        self.R = replay
        self.coverage_rows: list[dict[str, Any]] = []
        self.derived: dict[str, Any] = {}

    def record(self, law_id: str, owner: str, field: str, fn: str, status: str, operand=None, note=""):
        self.coverage_rows.append(
            {
                "lawId": law_id,
                "owner": owner,
                "derivedField": field,
                "function": fn,
                "status": status,
                "operand": operand,
                "note": note,
            }
        )

    def check_prerequisites(self, L) -> None:
        """Must hold before semantic proof comparison."""
        self._membership(L)
        self._extents_and_inventories(L)
        self._packages(L)
        self._execution_capture(L)
        self._selected_refs(L)
        self._outcome_derive(L)
        self._native_accounts(L)

    def complete_bundle_compare(self, L, computed_proof: dict, claimed_proof: dict) -> None:
        """C of complete proof plus reminted evidence/seal/run. Not a field projection."""
        self._independently_fill_proof_locators(L, computed_proof)
        # Compare every required proof field by C, not selected projections.
        required = self.R.owners.identity_v3["$defs"]["proof-bundle"]["required"]
        missing_derived = []
        for field in required:
            if field not in computed_proof:
                missing_derived.append(field)
                L.refuse("FULLREPLAY_FIELD_NOT_DERIVED", field)
                self.record(
                    "composition.v3§7",
                    "evaluator-composition-contract.v3.md §7",
                    f"proof.{field}",
                    "complete_bundle_compare",
                    "not-derived",
                    note="lawful output field not independently derived",
                )
        if missing_derived:
            L.operands["fullReplayIncompleteFields"] = missing_derived
            return
        c_comp = encode_c(computed_proof)
        c_claim = encode_c(claimed_proof)
        L.operands["computedProofC"] = sha256(c_comp)
        L.operands["claimedProofC"] = sha256(c_claim)
        L.operands["proofCEquality"] = c_comp == c_claim
        self.record(
            "composition.v3§7-C",
            "evaluator-composition-contract.v3.md §7 Compare C of COMPLETE recomputed proof",
            "proof-bundle",
            "encode_c(computed_proof)==encode_c(claimed_proof)",
            "PASS" if c_comp == c_claim else "REFUSED",
            operand={"computedC": sha256(c_comp), "claimedC": sha256(c_claim)},
        )
        if c_comp != c_claim:
            # field-level C diffs for diagnosis (still a complete compare, not a substitute)
            diffs = []
            for field in required:
                a = encode_c(computed_proof.get(field))
                b = encode_c(claimed_proof.get(field))
                if a != b:
                    diffs.append({"field": field, "computedSha": sha256(a), "claimedSha": sha256(b)})
            L.operands["proofFieldCDiffs"] = diffs
            L.refuse(
                "PROOF_C_MISMATCH",
                "complete C(proof) inequality; selected-field/witnessDigest match is not admission",
                diffs=diffs[:20],
            )

        # remint enclosing IDs from independently computed proof
        self._remint_enclosing(L, computed_proof)

    def _independently_fill_proof_locators(self, L, computed: dict) -> None:
        """Do not copy claimed proof locators. Derive from admitted Plan/program/EI."""
        plan_id = self.R.claimed_run["planId"]
        plan = self.R.by_typed[plan_id]["payload"]
        proof_claimed = self.R.claimed_proof
        # execution plan from graph
        ep_keys = [k for k in self.R.store.object_table if k.startswith("exec-plan2:")]
        if len(ep_keys) == 1:
            computed["executionPlanId"] = ep_keys[0]
            self.record("identity.exec-plan", "identity-schemas.v3 execution-plan", "proof.executionPlanId", "typed exec-plan2 from store", "executed", ep_keys[0])
        else:
            computed.pop("executionPlanId", None)
            L.refuse("EXEC_PLAN_NOT_UNIQUE", str(ep_keys))
        # evaluator closure: seal/proof field must be plan-selected kind=evaluator
        kinds = getattr(self.R, "closure_kinds", None) or L.operands.get("closureKinds") or {}
        ev = None
        for cid, kind in kinds.items():
            if kind == "evaluator":
                ev = cid
                break
        if ev:
            computed["evaluatorClosure"] = ev
            self.record("composition.v3§1-eval", "closureKinds evaluation-seal.evaluatorClosure=evaluator", "proof.evaluatorClosure", "plan-selected evaluator closure", "executed", ev)
        else:
            computed.pop("evaluatorClosure", None)
        # rule program digest = C(program)
        rp = computed.get("ruleProgramDigest")
        # replace with independently hashed program bytes
        for d, obj in self.R.canonical_by_digest.items():
            if isinstance(obj, dict) and obj.get("schemaVersion") == 2 and "rules" in obj and "policyDigest" in obj and "ruleId" not in obj:
                # RuleProgramV2
                computed["ruleProgramDigest"] = sha256(encode_c(obj))
                self.record("composition.v3§3-program", "proof.ruleProgramDigest = SHA256(C(RuleProgramV2))", "proof.ruleProgramDigest", "sha256(encode_c(program))", "executed", computed["ruleProgramDigest"])
                break
        ei_digest = proof_claimed.get("executionInputsDigest")
        ei = self.R.canonical_by_digest.get(ei_digest)
        if ei is not None:
            # independently hash EI
            computed["executionInputsDigest"] = sha256(encode_c(ei))
            selected = ei.get("selectedRefs") or []
            computed["evaluationInputRefs"] = canonical_ref_set(
                list(selected) + [{"domain": "execution-inputs", "digest": computed["executionInputsDigest"]}]
            )
            self.record(
                "execution-inputs.v1§7",
                "evaluationInputRefs = selectedRefs + {execution-inputs,digest}",
                "proof.evaluationInputRefs",
                "canonical_ref_set(selected+ei)",
                "executed",
                operand={"n": len(computed["evaluationInputRefs"])},
            )

    def _membership(self, L) -> None:
        plan_id = self.R.claimed_run["planId"]
        plan = self.R.by_typed[plan_id]["payload"]
        aspec = self.R.canonical_by_digest.get(plan["analysisSpecDigest"])
        enum_digest = None
        for p in (aspec or {}).get("parameters") or []:
            if p.get("schemaDigest") == self.R.owners.file_sha["docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json"]:
                enum_digest = p.get("payloadDigest")
        enum_plan = self.R.canonical_by_digest.get(enum_digest) if enum_digest else None
        if not enum_plan:
            L.refuse("PRODUCING_ENUM_MISSING", str(enum_digest))
            return
        self.derived["enum_plan"] = enum_plan
        memb = None
        memb_digest = None
        for d, obj in self.R.canonical_by_digest.items():
            if isinstance(obj, dict) and obj.get("schemaVersion") == 1 and "units" in obj and "rows" in obj and "unsupportedFiles" in obj:
                memb = obj
                memb_digest = d
                break
        if memb is None:
            L.refuse("MEMBERSHIP_RECORD_MISSING", "no UnitMembershipV1 retained")
            self.record("enum.v1§3-membershipDigest", "enumeration-contract.v1.md §3 membershipDigest=C(UnitMembershipV1)", "enumerationPlan.membershipDigest", "find UnitMembershipV1", "REFUSED")
            return
        got = sha256(encode_c(memb))
        want = enum_plan.get("membershipDigest")
        self.derived["membership"] = memb
        self.derived["membershipDigest"] = got
        ok = got == want
        self.record(
            "enum.v1§3-membershipDigest",
            "enumeration-contract.v1.md §3; ENUMERATION_PLAN_MEMBERSHIP_DIGEST_MISMATCH",
            "enumerationPlan.membershipDigest",
            "sha256(C(UnitMembershipV1))",
            "PASS" if ok else "REFUSED",
            operand={"computed": got, "claimed": want},
        )
        if not ok:
            L.refuse("ENUMERATION_PLAN_MEMBERSHIP_DIGEST_MISMATCH", f"computed {got} claimed {want}")
        # rows must exactly cover snapshot paths
        snap_paths = set(self.R.snapshot_paths)
        row_paths = {r.get("path") for r in memb.get("rows") or [] if r.get("path")}
        extra_lists = set(memb.get("unsupportedFiles") or []) | set(memb.get("outsideBoundaryFiles") or []) | set(memb.get("erasedFiles") or [])
        covered = row_paths | extra_lists
        missing = sorted(snap_paths - covered)
        extra = sorted(covered - snap_paths)
        self.derived["snapshotPaths"] = sorted(snap_paths)
        self.derived["membershipRowPaths"] = sorted(row_paths)
        self.derived["membershipMissingSnapshotPaths"] = missing
        self.record(
            "enum.v1§8-membership-cover",
            "enumeration-contract.v1.md §8 Membership rows must exactly cover snapshot paths; a missing row is not a silent exclude",
            "UnitMembershipV1.rows.path",
            "set(membership.rows.path) vs snapshot Blob.path",
            "PASS" if not missing else "REFUSED",
            operand={"snapshot": sorted(snap_paths), "rows": sorted(row_paths), "missing": missing, "extra": extra},
        )
        if missing:
            L.refuse(
                "ENUMERATION_MEMBERSHIP_SNAPSHOT_COVER",
                "membership rows do not cover snapshot paths",
                missing=missing,
            )
        L.operands["membershipCover"] = {"missing": missing, "extra": extra, "digestOk": ok}

    def _extents_and_inventories(self, L) -> None:
        memb = self.derived.get("membership")
        enum_plan = self.derived.get("enum_plan")
        if not memb or not enum_plan:
            self.record("enum.v1§5-extent", "enumeration-contract.v1.md §5 / x-opensip-file-membership-extent-law", "binding.extents", "depends membership", "notReached")
            return
        remaining = []
        for p, row in self.R.snapshot_paths.items():
            # find membership
            mrow = next((r for r in (memb.get("rows") or []) if r.get("path") == p), None)
            if mrow:
                if mrow.get("membership") in EXCLUDE_MEMBERSHIP or mrow.get("reason") in EXCLUDE_REASON:
                    continue
            remaining.append(p)
        # file extent = remaining first-party snapshot paths (inventory is not grammar-gated)
        derived_file = sorted(remaining)
        self.derived["derivedFileExtent"] = derived_file
        self.record(
            "enum.v1§5-file-extent",
            "enumeration-contract.v1.md §5 file extent + enum-plan x-opensip-file-membership-extent-law.fileKind",
            "KindExtentV1.paths[kind=file]",
            "snapshot paths minus excludeAlways membership/reason",
            "executed",
            operand=derived_file,
        )
        # compare each file-kind binding.extents to derived (cell workspace .)
        for ci, cell in enumerate(enum_plan.get("cells") or []):
            wr = cell.get("workspaceRoot") or "."
            if wr not in (".",):
                # bounded: these exports use .
                pass
            for pb in cell.get("programBindings") or []:
                for e in pb.get("extents") or []:
                    if e.get("kind") != "file":
                        continue
                    claimed = sorted(e.get("paths") or [])
                    # claimed extents that are not a subset of derived, or omit derived members when cell is inventory
                    missing = sorted(set(derived_file) - set(claimed))
                    extra = sorted(set(claimed) - set(derived_file))
                    cap = cell.get("capabilityId")
                    # inventory file cell must list every remaining path; clones-fact file extent may be a program subset
                    # but enumeration §4 complete file rows must equal THAT binding's extent, AND
                    # binding extents for inventory fileKind must be the remaining set.
                    if cap == "inventory":
                        status = "PASS" if claimed == derived_file else "REFUSED"
                        self.record(
                            "enum.v1§5-inventory-file-extent-join",
                            "fileKind: every remaining inventoried first-party snapshot path; claimed binding.extents are not self-certifying",
                            f"cells[{ci}].programBindings.extents[file]",
                            "claimed extent vs independently derived remaining snapshot paths",
                            status,
                            operand={"claimed": claimed, "derived": derived_file, "missing": missing, "extra": extra},
                        )
                        if claimed != derived_file:
                            L.refuse(
                                "ENUMERATION_FILE_EXTENT_NOT_DERIVED",
                                "inventory file extent omits first-party snapshot paths; claimed KindExtentV1 is not producing-law",
                                cell=ci,
                                claimed=claimed,
                                derived=derived_file,
                            )
                    else:
                        # still require claimed ⊆ derived
                        if extra:
                            L.refuse("ENUMERATION_EXTENT_OUTSIDE_SNAPSHOT", extra, cell=ci, capability=cap)
                            self.record(
                                "enum.v1§5-extent-subset",
                                "every extent path must be a first-party scoped snapshot member",
                                f"cells[{ci}].extents[file]",
                                "claimed ⊆ derived remaining",
                                "REFUSED",
                                extra,
                            )
                        else:
                            self.record(
                                "enum.v1§5-extent-subset",
                                "every extent path must be a first-party scoped snapshot member",
                                f"cells[{ci}].extents[file]",
                                "claimed ⊆ derived remaining",
                                "PASS",
                                {"claimed": claimed, "derived": derived_file},
                            )

    def _packages(self, L) -> None:
        named = []
        workspace_only = []
        parse_fail = []
        for path, row in self.R.snapshot_paths.items():
            name = path.rsplit("/", 1)[-1]
            blob = self.R._blob_for_path(path)
            if blob is None:
                continue
            if name == "package.json":
                try:
                    obj = lexical_scan_raw(blob)
                except LexicalRefusal as e:
                    parse_fail.append({"path": path, "error": str(e)})
                    continue
                if isinstance(obj, dict):
                    n = obj.get("name")
                    if isinstance(n, str) and n:
                        named.append({"path": path, "name": n, "format": "json"})
                    else:
                        workspace_only.append(path)
            elif name == "Cargo.toml":
                try:
                    obj = tomllib.loads(blob.decode("utf-8"))
                except Exception as e:
                    parse_fail.append({"path": path, "error": str(e)})
                    continue
                pkg = obj.get("package") if isinstance(obj, dict) else None
                n = pkg.get("name") if isinstance(pkg, dict) else None
                if isinstance(n, str) and n:
                    named.append({"path": path, "name": n, "format": "toml"})
                else:
                    workspace_only.append(path)
        self.derived["namedPackages"] = named
        self.derived["workspaceOnlyManifests"] = workspace_only
        self.derived["packageParseFailures"] = parse_fail
        self.record(
            "enum.v1§8-package-parse",
            "enumeration-contract.v1.md §8 package named subjects from retained snapshot bytes; workspace-only Cargo.toml is not a package subject",
            "package inventory expected rows",
            "tomllib/canonical.parse of snapshot manifests",
            "executed",
            operand={"named": named, "workspaceOnly": workspace_only, "parseFail": parse_fail},
        )
        if parse_fail:
            L.refuse("ENUMERATION_PACKAGE_PARSE", parse_fail)
        # join complete package inventories
        enum_plan = self.derived.get("enum_plan")
        if not enum_plan:
            return
        expected_named_paths = {p["path"] for p in named}
        for d, obj in self.R.canonical_by_digest.items():
            if not (isinstance(obj, dict) and obj.get("kind") == "package" and "cellOrdinal" in obj):
                continue
            if obj.get("state") != "complete":
                continue
            rows = obj.get("rows") or []
            got_paths = {r.get("path") for r in rows}
            # complete package totality vs independently named manifests in this workspace
            # (cell workspace .)
            if got_paths != expected_named_paths:
                # if expected empty, complete-empty is lawful
                L.refuse(
                    "ENUMERATION_PACKAGE_TOTALITY",
                    "complete package rows != independently named first-party manifests",
                    inventory=d,
                    claimed=sorted(got_paths),
                    derived=sorted(expected_named_paths),
                )
                self.record(
                    "enum.v1§4-package-complete",
                    "complete+package: one row per expected named first-party manifest; workspace-only is not a subject",
                    "SubjectInventoryV1.rows[kind=package]",
                    "row.path set vs parsed named manifests",
                    "REFUSED",
                    {"claimed": sorted(got_paths), "derived": sorted(expected_named_paths)},
                )
            else:
                self.record(
                    "enum.v1§4-package-complete",
                    "complete+package totality",
                    "SubjectInventoryV1.rows[kind=package]",
                    "row.path set vs parsed named manifests",
                    "PASS",
                    {"paths": sorted(got_paths)},
                )
            for r in rows:
                if r.get("nativeSubjectId") != r.get("qualifiedName"):
                    L.refuse("PACKAGE_NAME_QN", r)
                if r.get("signatureTokens") != [] or r.get("projections") != []:
                    L.refuse("PACKAGE_EMPTY_DISCRIMINATOR", r)
                # attested name equals parsed name
                hit = next((p for p in named if p["path"] == r.get("path")), None)
                if hit and r.get("nativeSubjectId") != hit["name"]:
                    L.refuse("PACKAGE_NAME_ATTESTED", {"row": r.get("nativeSubjectId"), "parsed": hit["name"]})
                if r.get("subjectLanguage") not in ("json", "toml"):
                    L.refuse("PACKAGE_LANGUAGE_FORMAT", r.get("subjectLanguage"))

    def _execution_capture(self, L) -> None:
        proof = self.R.claimed_proof
        ei = self.R.canonical_by_digest.get(proof.get("executionInputsDigest") if proof else None)
        if not ei:
            L.refuse("EI_MISSING_FOR_PRODUCING", "no ExecutionInputsV1")
            return
        self.derived["ei"] = ei
        hc = ei.get("hostCapture") or {}
        if hc.get("custody") != "host-tcb-evidence-store" or hc.get("observation") != "stage-return":
            L.refuse("HOSTCAPTURE_CONST", hc)
        receipts = hc.get("stageReceipts") or []
        ordinals = [r.get("ordinal") for r in receipts]
        if ordinals != list(range(len(ordinals))):
            L.refuse("STAGE_RECEIPT_ORDINAL", ordinals)
            self.record("exec.v1§1-receipts", "one receipt per stage, ordinals unique and total", "hostCapture.stageReceipts.ordinal", "contiguous ordinals", "REFUSED", ordinals)
        else:
            self.record("exec.v1§1-receipts", "execution-inputs-contract.v1.md §1 stageReceipts", "hostCapture.stageReceipts", "ordinal unique+total; outputDomains vs outputRefs", "PASS", {"n": len(receipts)})
        for r in receipts:
            domains = set(r.get("outputDomains") or [])
            for ref in r.get("outputRefs") or []:
                if ref.get("domain") not in domains:
                    L.refuse("STAGE_OUTPUTREF_DOMAIN", ref)
            if r.get("state") != "unavailable" and not r.get("outputRefs"):
                # complete receipts should name outputs
                if r.get("state") == "complete" and "view" in domains:
                    pass
        # hostDerivedRefs must equal selectedRefs blob-domain members (inventories etc.)
        derived_refs = hc.get("hostDerivedRefs") or []
        selected = ei.get("selectedRefs") or []
        blob_domains = {"subject-inventory", "candidate-producer-result", "target-attribution", "incoming-search"}
        selected_blob = canonical_ref_set([r for r in selected if r.get("domain") in blob_domains])
        derived_c = canonical_ref_set(derived_refs)
        ok = encode_c(selected_blob) == encode_c(derived_c)
        self.record(
            "exec.v1§6-hostDerived",
            "selectedRefs blob-domain members equal hostCapture.hostDerivedRefs",
            "hostCapture.hostDerivedRefs",
            "C-set equality vs selectedRefs filtered to host-derived domains",
            "PASS" if ok else "REFUSED",
            operand={"selectedBlob": selected_blob, "hostDerived": derived_c},
        )
        if not ok:
            L.refuse("HOST_DERIVED_NE_SELECTED_BLOB", {"selectedBlob": selected_blob, "hostDerived": derived_c})
        forbidden = {"proof-bundle", "finding", "evaluation-seal", "run", "semantic-evidence"}
        for r in selected:
            if r.get("domain") in forbidden:
                L.refuse("EI_FORBIDDEN_REF", r)
        if any(r.get("domain") == "execution-inputs" for r in selected):
            L.refuse("EI_CIRCULAR_SELF_REF", "execution-inputs must not be a selectedRefs member")

    def _selected_refs(self, L) -> None:
        ei = self.derived.get("ei")
        if not ei:
            return
        receipts = ((ei.get("hostCapture") or {}).get("stageReceipts") or [])
        stage_produced = []
        for r in receipts:
            if r.get("state") == "complete":
                stage_produced.extend(r.get("outputRefs") or [])
        # coverage = every coverageIds of those views
        cov = []
        views = []
        for ref in stage_produced:
            if ref.get("domain") != "view":
                continue
            vid = "view2:" + ref["digest"]
            rec = self.R.by_typed.get(vid)
            if not rec:
                L.refuse("SELECTED_VIEW_MISSING", vid)
                continue
            views.append(vid)
            for cid in rec["payload"].get("coverageIds") or []:
                digest = cid.split(":", 1)[1] if cid.startswith("coverage2:") else cid
                cov.append({"domain": "coverage", "digest": digest})
        inventories = []
        for o in ei.get("cellOutcomes") or []:
            for d in o.get("inventoryDigests") or []:
                inventories.append({"domain": "subject-inventory", "digest": d})
        plan_id = self.R.claimed_run["planId"]
        plan = self.R.by_typed[plan_id]["payload"]
        imports = []
        for iid in plan.get("importIds") or []:
            digest = iid.split(":", 1)[1]
            imports.append({"domain": "import", "digest": digest})
        reconstructed = canonical_ref_set(
            [{"domain": "view", "digest": v.split(":", 1)[1]} for v in views] + cov + inventories + imports
        )
        claimed = canonical_ref_set(ei.get("selectedRefs") or [])
        self.derived["reconstructedSelectedRefs"] = reconstructed
        eq = encode_c(reconstructed) == encode_c(claimed)
        self.record(
            "exec.v1§1-selectedRefs-totality",
            "execution-inputs-contract.v1.md §1 selectedRefs is exact totality (views ∪ coverage ∪ inventories ∪ plan imports)",
            "ExecutionInputsV1.selectedRefs",
            "independently reconstruct then C-set compare",
            "PASS" if eq else "REFUSED",
            operand={"reconstructed": reconstructed, "claimed": claimed},
        )
        L.operands["selectedRefsCompare"] = {"equal": eq, "reconstructedN": len(reconstructed), "claimedN": len(claimed)}
        if not eq:
            L.refuse(
                "SELECTED_REFS_TOTALITY",
                "independently reconstructed selectedRefs C-set != claimed",
                reconstructed=reconstructed,
                claimed=claimed,
            )

    def _outcome_derive(self, L) -> None:
        ei = self.derived.get("ei")
        enum_plan = self.derived.get("enum_plan")
        if not ei or not enum_plan:
            return
        inv_by = {}
        for d, obj in self.R.canonical_by_digest.items():
            if isinstance(obj, dict) and "cellOrdinal" in obj and "kind" in obj and "rows" in obj and obj.get("schemaVersion") == 1:
                inv_by[(obj["cellOrdinal"], obj.get("programOrdinal"), obj["kind"])] = obj
        for o in ei.get("cellOutcomes") or []:
            ci, po = o.get("cellOrdinal"), o.get("programOrdinal")
            cell = (enum_plan.get("cells") or [None])[ci] if ci is not None and ci < len(enum_plan.get("cells") or []) else None
            kinds = set(o.get("kinds") or (cell.get("kinds") if cell else []) or [])
            invs = [inv_by.get((ci, po, k)) for k in kinds]
            invs = [x for x in invs if x]
            pb = None
            if cell:
                pb = next((b for b in (cell.get("programBindings") or []) if b.get("ordinal") == po), None)
            unselected = (o.get("enumeratorStatus") == "unselected") or (pb and pb.get("universe") is None and (pb.get("enumerator") or {}).get("status") != "selected")
            derived_state = None
            if unselected or o.get("universe") is None and o.get("enumeratorStatus") != "selected":
                derived_state = "unavailable"
            else:
                if any((x.get("state") == "partial") for x in invs):
                    derived_state = "partial"
                elif any((x.get("state") == "unavailable") for x in invs):
                    derived_state = "unavailable"
                else:
                    # accounts: any supported-available not complete → partial
                    accs = [
                        a
                        for a in (ei.get("nativeCoverageAccounts") or [])
                        if a.get("cellOrdinal") == ci and a.get("programOrdinal") == po
                    ]
                    account_blocks_complete = False
                    for a in accs:
                        if a.get("applicability") == "supported-available":
                            ids = a.get("coverageIds") or []
                            if not ids:
                                account_blocks_complete = True
                            for cid in ids:
                                typed = cid if str(cid).startswith("coverage2:") else "coverage2:" + cid
                                rec = self.R.by_typed.get(typed)
                                if not rec:
                                    account_blocks_complete = True
                                    continue
                                pd = rec["payload"].get("payloadDigest")
                                payload = self.R.canonical_by_digest.get(pd) or {}
                                entry = payload.get("entry") or {}
                                if entry.get("coverage") != "complete":
                                    account_blocks_complete = True
                        # unsupported/inapplicable do not block complete
                    if account_blocks_complete:
                        derived_state = "partial"
                    elif invs and all(x.get("state") == "complete" for x in invs):
                        derived_state = "complete"
            claimed = o.get("state")
            self.record(
                "exec.v1§4-outcome-state",
                "execution-inputs-contract.v1.md §4 outcome state is derived then joined to the host row; complete+partial inventory is EXECUTION_INPUTS_OUTCOME_DERIVE",
                f"cellOutcomes[{ci},{po}].state",
                "derive from enumerator/universe/inventory states",
                "PASS" if derived_state == claimed else "REFUSED",
                operand={"derived": derived_state, "claimed": claimed, "inventoryStates": [x.get("state") for x in invs]},
            )
            if derived_state and claimed != derived_state:
                L.refuse("EXECUTION_INPUTS_OUTCOME_DERIVE", f"cell {ci} derived {derived_state} claimed {claimed}")
            if claimed == "complete" and any(x.get("state") == "partial" for x in invs):
                L.refuse("EXECUTION_INPUTS_OUTCOME_DERIVE", "complete + partial inventory")

    def _native_accounts(self, L) -> None:
        ei = self.derived.get("ei")
        if not ei:
            return
        vcs = None
        for d, obj in self.R.canonical_by_digest.items():
            if isinstance(obj, dict) and "kind" in obj and "dirty" in obj and obj.get("schemaVersion") == 2:
                vcs = obj
                break
        vcs_none = bool(vcs and vcs.get("kind") == "none")
        self.derived["vcs"] = vcs
        self.record(
            "exec.v1§5-vcs",
            "inapplicable-vcs when admitted VCS observation kind=none",
            "nativeCoverageAccounts.applicability",
            "vcs-observation.kind",
            "executed",
            operand={"kind": None if not vcs else vcs.get("kind")},
        )
        # For each claimed account, independently collect matching coverage IDs from returned views
        view_cov = []
        for key, rec in self.R.by_typed.items():
            if key.startswith("view2:") and rec and rec.get("payload"):
                for cid in rec["payload"].get("coverageIds") or []:
                    view_cov.append(cid)
        accounts = ei.get("nativeCoverageAccounts") or []
        for acc in accounts:
            rel, rung = acc.get("relation"), acc.get("resolution")
            appl = acc.get("applicability")
            claimed_ids = acc.get("coverageIds") or []
            matching = []
            for cid in view_cov:
                rec = self.R.by_typed.get(cid)
                if not rec:
                    continue
                pd = rec["payload"].get("payloadDigest")
                payload = self.R.canonical_by_digest.get(pd)
                if not payload:
                    continue
                entry = payload.get("entry") or {}
                key = payload.get("key") or {}
                if (entry.get("relation") or key.get("relation")) == rel and (entry.get("resolution") or key.get("resolution")) == rung:
                    matching.append(cid.split(":", 1)[1] if cid.startswith("coverage2:") else cid)
            matching = sorted(set(matching))
            claimed_sorted = sorted(claimed_ids)
            if appl == "supported-available":
                eq = matching == claimed_sorted
                self.record(
                    "exec.v1§5-supported-available",
                    "coverageIds equals every matching returned partition, not a complete subset",
                    f"nativeCoverageAccounts[{rel}@{rung}].coverageIds",
                    "scan view coverage payloads for relation@rung",
                    "PASS" if eq else "REFUSED",
                    operand={"derived": matching, "claimed": claimed_sorted},
                )
                if not eq:
                    L.refuse("NATIVE_ACCOUNT_COVERAGE_IDS", f"{rel}@{rung}", derived=matching, claimed=claimed_sorted)
                if not matching:
                    L.refuse("NATIVE_WORK_INCOMPLETE", f"supported-available {rel}@{rung} has empty matching Coverage")
            elif appl == "inapplicable-vcs":
                if not vcs_none:
                    L.refuse("INAPPLICABLE_VCS_WITHOUT_NONE", rel)
                if claimed_ids:
                    L.refuse("INAPPLICABLE_VCS_HAS_COVERAGE", claimed_ids)
                self.record(
                    "exec.v1§5-inapplicable-vcs",
                    "inapplicable-vcs: none envelopes; VCS kind=none",
                    f"nativeCoverageAccounts[{rel}].coverageIds",
                    "empty iff vcs.kind=none",
                    "PASS" if vcs_none and not claimed_ids else "REFUSED",
                )
            elif appl == "unsupported-typed":
                if claimed_ids:
                    L.refuse("UNSUPPORTED_TYPED_HAS_COVERAGE", claimed_ids)
                cap = None
                # matrix deficiency for this cell
                self.record(
                    "exec.v1§5-unsupported-typed",
                    "unsupported-typed: no envelopes; matrix deficiency for that cell",
                    f"nativeCoverageAccounts[{rel}].applicability",
                    "empty coverageIds",
                    "PASS" if not claimed_ids else "REFUSED",
                )

    def _remint_enclosing(self, L, computed_proof: dict) -> None:
        if "PROOF_C_MISMATCH" in [f.get("code") for f in L.faults] or L.status == "REFUSED" and any(f.get("code") == "FULLREPLAY_FIELD_NOT_DERIVED" for f in L.faults):
            # still remint from computed for measurement
            pass
        try:
            proof_id = typed_id("proof-bundle", computed_proof)
        except Exception as e:
            L.refuse("PROOF_REMINT", str(e))
            return
        L.operands["computedProofId"] = proof_id
        claimed_proof_id = None
        for k in self.R.store.object_table:
            if k.startswith("proof3:"):
                claimed_proof_id = k
                break
        L.operands["claimedProofId"] = claimed_proof_id
        self.record(
            "composition.v3§7-proof-id",
            "H(proof-bundle, C(computed proof)) vs retained proof3",
            "proof3",
            "typed_id('proof-bundle', computed_proof)",
            "PASS" if proof_id == claimed_proof_id else "REFUSED",
            operand={"computed": proof_id, "claimed": claimed_proof_id},
        )
        if proof_id != claimed_proof_id:
            L.refuse("PROOF_ID_MISMATCH", f"computed {proof_id} claimed {claimed_proof_id}")

        evidence_claimed = None
        for k, rec in self.R.by_typed.items():
            if k.startswith("evidence3:"):
                evidence_claimed = rec["payload"]
                claimed_eid = k
                break
        else:
            return
        # independently compose evidence from selected views/coverage/imports + computed proof id
        ei = self.derived.get("ei") or {}
        view_ids = sorted({("view2:" + r["digest"]) for r in (ei.get("selectedRefs") or []) if r.get("domain") == "view"})
        cov_ids = sorted({("coverage2:" + r["digest"]) for r in (ei.get("selectedRefs") or []) if r.get("domain") == "coverage"})
        import_ids = sorted({("import2:" + r["digest"]) for r in (ei.get("selectedRefs") or []) if r.get("domain") == "import"})
        evidence = {
            "coverageIds": cov_ids,
            "findingIds": computed_proof.get("findingIds") or [],
            "importIds": import_ids,
            "planId": computed_proof.get("planId"),
            "proofBundleId": proof_id,
            "schemaVersion": 3,
            "viewIds": view_ids,
        }
        eid = typed_id("semantic-evidence", evidence)
        L.operands["computedEvidenceId"] = eid
        L.operands["claimedEvidenceId"] = claimed_eid
        L.operands["evidenceCEquality"] = encode_c(evidence) == encode_c(evidence_claimed)
        self.record(
            "composition.v3§7-evidence",
            "independently reconstruct semantic-evidence then H; C-equality vs retained",
            "evidence3",
            "typed_id + encode_c compare",
            "PASS" if eid == claimed_eid else "REFUSED",
            operand={"computed": eid, "claimed": claimed_eid, "cEqual": L.operands["evidenceCEquality"]},
        )
        if eid != claimed_eid:
            L.refuse("EVIDENCE_ID_MISMATCH", f"computed {eid} claimed {claimed_eid}")

        seal_claimed = None
        for k, rec in self.R.by_typed.items():
            if k.startswith("seal3:"):
                seal_claimed = rec["payload"]
                claimed_sid = k
                break
        else:
            return
        seal = {
            "evaluatorClosure": computed_proof.get("evaluatorClosure"),
            "evidenceId": eid,
            "executionPlanId": computed_proof.get("executionPlanId"),
            "planId": computed_proof.get("planId"),
            "policyDigest": self.R.by_typed[self.R.claimed_run["planId"]]["payload"]["policyDigest"],
            "proofBundleId": proof_id,
            "schemaVersion": 3,
            "verdict": computed_proof.get("verdict"),
        }
        sid = typed_id("evaluation-seal", seal)
        L.operands["computedSealId"] = sid
        L.operands["claimedSealId"] = claimed_sid
        self.record(
            "composition.v3§7-seal",
            "independently reconstruct evaluation-seal then H",
            "seal3",
            "typed_id('evaluation-seal', seal)",
            "PASS" if sid == claimed_sid else "REFUSED",
            operand={"computed": sid, "claimed": claimed_sid},
        )
        if sid != claimed_sid:
            L.refuse("SEAL_ID_MISMATCH", f"computed {sid} claimed {claimed_sid}")

        run = {
            "capabilityManifestId": self.R.claimed_run["capabilityManifestId"],
            "evaluationSealId": sid,
            "evidenceId": eid,
            "planId": self.R.claimed_run["planId"],
            "projectId": self.R.claimed_run["projectId"],
            "schemaVersion": 3,
            "snapshotId": self.R.claimed_run["snapshotId"],
        }
        rid = typed_id("run", run)
        claimed_rid = next(k for k in self.R.store.object_table if k.startswith("run3:"))
        L.operands["computedRunId"] = rid
        L.operands["claimedRunId"] = claimed_rid
        self.record(
            "composition.v3§7-run",
            "independently reconstruct run then H",
            "run3",
            "typed_id('run', run)",
            "PASS" if rid == claimed_rid else "REFUSED",
            operand={"computed": rid, "claimed": claimed_rid},
        )
        if rid != claimed_rid:
            L.refuse("RUN_ID_MISMATCH", f"computed {rid} claimed {claimed_rid}")
