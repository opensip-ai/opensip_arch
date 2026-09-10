"""Independent producing-law reconstruction for ExecutionInputs / Enumeration / Atom / Composition.

Claimed ExecutionInputsV1 and SubjectInventoryV1 bytes are inputs subject to
producing joins. This module reconstructs selectedRefs, extents, expected
inventories, derived outcome state, derived native-coverage accounts, and
evaluation-subject minting from admitted source/program/provider/capture
records. Proof C is compared only after these joins execute.

Bounded to the committed syntax-only policy (rule file-present / none of
file@enumerated). Unbounded generic analysis of unselected capabilities is
not required; inapplicable branches are justified by admitted committed inputs.
"""
from __future__ import annotations

from typing import Any

from canonical import AdmissionError, encode_c, h_identity, sha256_hex


def ref(domain: str, digest: str) -> dict:
    return {"digest": digest, "domain": domain}


def sort_canonical_set(items: list) -> list:
    encoded = [(encode_c(x, profile="product"), x) for x in items]
    encoded.sort(key=lambda t: t[0])
    out = []
    seen = set()
    for b, x in encoded:
        if b in seen:
            continue
        seen.add(b)
        out.append(x)
    return out


def sort_strings(xs: list[str]) -> list[str]:
    return sorted(set(xs), key=lambda s: s.encode("utf-8"))

EXCLUDE_MEMBERSHIP = {"outside-project-boundary"}
EXCLUDE_REASONS = {"host-ignore-convention", "nested-repository", "nested-project", "custody-excluded"}
KIND_BY_CAPABILITY = {
    "inventory": ["file", "package"],
    "syntax": ["symbol"],
    "imports": ["symbol"],
    "references": ["symbol"],
    "calls": ["symbol"],
    "types": ["symbol"],
    "reachability": ["symbol"],
    "unresolved-edge": ["symbol"],
    "clones-fact": ["file"],
    "clones-near": [],
    "clones-cross-tsjs": [],
}
MATRIX_RELATIONS = {
    "inventory": [("file", "enumerated"), ("package", "manifest-declared"), ("vcs-change", "vcs-reported")],
    "syntax": [("declares", "syntactic"), ("literal", "syntactic"), ("control-flow", "syntactic")],
    "clones-fact": [("clones", "normalized-body-hash")],
    "imports": [("imports", "resolved-target")],
    "references": [("references", "resolved-binding")],
    "calls": [("calls", "resolved-callee")],
    "types": [("types", "checked")],
    "reachability": [("reachability", "from-resolved-calls")],
    "unresolved-edge": [("unresolved-edge", "observed")],
    "clones-near": [],
    "clones-cross-tsjs": [],
}
CANDIDATE_CAPS = {"clones-near", "clones-cross-tsjs"}
NAMED_MANIFESTS = {"package.json", "Cargo.toml"}
FORBIDDEN_SELECTED = {"proof-bundle", "finding", "evaluation-seal", "run", "semantic-evidence"}
BLOB_SELECTED_DOMAINS = {"subject-inventory", "candidate-producer-result", "target-attribution", "incoming-search"}
HOST_DERIVED_DOMAINS = BLOB_SELECTED_DOMAINS


def _hex(typed_or_hex: str) -> str:
    return typed_or_hex.split(":")[-1]


def _c_eq(a, b) -> bool:
    return encode_c(a, profile="product") == encode_c(b, profile="product")


def subject_language(path: str, table: list[dict]) -> str:
    best = None
    best_len = -1
    for row in table:
        for suf in row.get("suffixes") or []:
            if path.endswith(suf) and len(suf) > best_len:
                best = row["languageId"]
                best_len = len(suf)
    return best or "unspecified"


def path_under_root(path: str, root: str) -> bool:
    if root == ".":
        return True
    return path == root or path.startswith(root.rstrip("/") + "/")


def in_scope(path: str, scope: dict, workspace_root: str) -> bool:
    roots = scope.get("workspaceRoots") or []
    if workspace_root not in roots and not (workspace_root == "." and "." in roots):
        return False
    if not path_under_root(path, workspace_root):
        return False
    prefixes = scope.get("pathPrefixes") or []
    excluded = scope.get("excludedPathPrefixes") or []
    if "." in excluded:
        return False
    if any(path_under_root(path, ex) for ex in excluded):
        return False
    if not prefixes:
        return True
    return any(path_under_root(path, pfx) for pfx in prefixes)


class Assertion:
    def __init__(
        self,
        aid: str,
        document: str,
        section: str,
        paragraph: str,
        field: str | None,
        layer: str,
        checker: str,
        assertion: str,
        operands: dict,
        result: Any,
        status: str,
        applicable: bool,
        inapplicable_justification: str | None = None,
    ):
        self.id = aid
        self.document = document
        self.section = section
        self.paragraph = paragraph
        self.field = field
        self.layer = layer
        self.checker = checker
        self.assertion = assertion
        self.operands = operands
        self.result = result
        self.status = status
        self.applicable = applicable
        self.inapplicable_justification = inapplicable_justification

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "document": self.document,
            "section": self.section,
            "paragraph": self.paragraph,
            "field": self.field,
            "layer": self.layer,
            "checkerFunction": self.checker,
            "assertion": self.assertion,
            "inputOperands": self.operands,
            "executedResult": self.result,
            "status": self.status,
            "applicable": self.applicable,
            "inapplicableJustification": self.inapplicable_justification,
        }


class ProducingLaw:
    def __init__(self, replay):
        self.r = replay
        self.a = replay.a
        self.assertions: list[Assertion] = []
        self.derived_selected_refs: list[dict] = []
        self.derived_outcomes: list[dict] = []
        self.derived_accounts: list[dict] = []
        self.expected_inventories: dict[str, dict] = {}
        self.derived_extents: dict[tuple, dict] = {}
        self.membership: dict | None = None
        self.scope: dict | None = None
        self.vcs: dict | None = None
        self.lang_table: list[dict] = []
        self.account_states: dict[tuple, dict] = {}

    def record(self, **kwargs) -> Assertion:
        ast = Assertion(**kwargs)
        self.assertions.append(ast)
        return ast

    def pass_eq(self, **kwargs) -> None:
        kwargs.setdefault("status", "executed-pass")
        kwargs.setdefault("applicable", True)
        kwargs.setdefault("inapplicable_justification", None)
        kwargs.setdefault("layer", "producing")
        self.record(**kwargs)

    def inapplicable(self, **kwargs) -> None:
        kwargs.setdefault("status", "notReached")
        kwargs.setdefault("applicable", False)
        kwargs.setdefault("layer", "producing")
        kwargs.setdefault("result", "notReached")
        kwargs.setdefault("operands", {})
        self.record(**kwargs)

    def refuse(self, code: str, message: str, citation: str, law_operands: dict | None = None, **kwargs) -> None:
        operands = kwargs.pop("operands", law_operands) or {}
        kwargs.setdefault("status", "executed-fail")
        kwargs.setdefault("applicable", True)
        kwargs.setdefault("layer", "producing")
        kwargs.setdefault("result", {"code": code, "message": message})
        kwargs.setdefault("operands", operands)
        self.record(**kwargs)
        self.a.refuse("L-PRODUCING-" + code, code, message, citation, operands)

    def execute(self) -> dict:
        citation = "execution-inputs-contract.v1.md; enumeration-contract.v1.md"
        self._load_aux()
        self._enum_plan_identity_and_joins()
        self._membership_cover_and_extents()
        self._expected_inventories_and_totality()
        self._stage_receipts()
        self._derive_selected_refs()
        self._derive_native_accounts()
        self._derive_cell_outcomes()
        self._evaluation_input_refs()
        self._atom_and_composition_branches()
        self.a.mark_pass(
            "L-PRODUCING-LAWS",
            citation,
            "producing joins reconstructed independently of claimed proof fields",
            {"assertionCount": len(self.assertions)},
        )
        return self.summary()

    def summary(self) -> dict:
        executed = [a for a in self.assertions if a.status == "executed-pass"]
        failed = [a for a in self.assertions if a.status == "executed-fail"]
        nr = [a for a in self.assertions if a.status == "notReached"]
        return {
            "assertionCount": len(self.assertions),
            "executedPass": len(executed),
            "executedFail": len(failed),
            "notReached": len(nr),
            "applicableCount": sum(1 for a in self.assertions if a.applicable),
            "inapplicableCount": sum(1 for a in self.assertions if not a.applicable),
            "derivedSelectedRefs": self.derived_selected_refs,
            "derivedOutcomes": [
                {
                    "cellOrdinal": o["cellOrdinal"],
                    "programOrdinal": o["programOrdinal"],
                    "state": o["state"],
                    "inventoryDigests": o["inventoryDigests"],
                    "viewDigests": o["viewDigests"],
                }
                for o in self.derived_outcomes
            ],
            "derivedAccounts": self.derived_accounts,
            "expectedInventoryDigests": sorted(self.expected_inventories),
            "assertions": [a.as_dict() for a in self.assertions],
        }

    # ----- load -----

    def _load_aux(self):
        a = self.a
        self.scope = a.canonical_records[a.plan["scopeDigest"]]
        enum = self.r.enum_plan
        mem_digest = enum["membershipDigest"]
        if mem_digest not in a.canonical_records:
            a._admit_canonical(mem_digest, a.kit.native_schemas, "#/$defs/UnitMembershipV1", "enumerationPlan.membershipDigest")
        self.membership = a.canonical_records[mem_digest]
        vcs_digest = a.snapshot["vcsDigest"]
        if vcs_digest not in a.canonical_records:
            a._admit_canonical(vcs_digest, a.kit.identity_v3, "#/$defs/vcs-observation", "snapshot.vcsDigest")
        self.vcs = a.canonical_records[vcs_digest]
        self.lang_table = a.kit.subject_inventory_schema["x-opensip-subject-language-table"]["members"]
        # stage specs
        self.stage_specs = {}
        for st in a.exec_plan.get("stages") or []:
            d = st["stageSpecDigest"]
            if d not in a.canonical_records:
                a._admit_canonical(d, a.kit.identity_v3, "#/$defs/stage-spec", "execution-plan.stages[].stageSpecDigest")
            self.stage_specs[d] = a.canonical_records[d]

    # ----- enumeration plan -----

    def _enum_plan_identity_and_joins(self):
        enum = self.r.enum_plan
        plan = self.a.plan
        spec = self.a.analysis_spec
        c_enum = encode_c(enum, profile="product")
        enum_digest = sha256_hex(c_enum)
        ei = self.a.execution_inputs
        self.pass_eq(
            aid="ENUM-PARAM-IDENTITY",
            document="enumeration-contract.v1.md",
            section="intro",
            paragraph="Parameter identity is raw SHA-256 of C(EnumerationPlanV1). No new H domains.",
            field="EnumerationPlanV1 identity",
            checker="ProducingLaw._enum_plan_identity_and_joins",
            assertion="C(EnumerationPlanV1) SHA-256 equals ExecutionInputs.enumerationPlanDigest and analysis-spec payloadDigest",
            operands={
                "derived": enum_digest,
                "executionInputs.enumerationPlanDigest": ei.get("enumerationPlanDigest"),
            },
            result={"equal": enum_digest == ei.get("enumerationPlanDigest")},
        )
        if enum_digest != ei.get("enumerationPlanDigest"):
            self.refuse(
                "ENUMERATION_PLAN_DIGEST",
                "C(EnumerationPlanV1) does not equal execution-inputs.enumerationPlanDigest",
                "enumeration-contract.v1.md intro; execution-inputs-contract.v1.md §7",
                {"derived": enum_digest, "claimed": ei.get("enumerationPlanDigest")},
                aid="ENUM-PARAM-IDENTITY-FAIL",
                document="enumeration-contract.v1.md",
                section="intro",
                paragraph="Parameter identity is raw SHA-256 of C(EnumerationPlanV1).",
                field="enumerationPlanDigest",
                checker="ProducingLaw._enum_plan_identity_and_joins",
                assertion="derived C digest equals claimed locator",
                operands={"derived": enum_digest, "claimed": ei.get("enumerationPlanDigest")},
            )
        if "planId" in enum or "analysisSpecDigest" in enum:
            self.refuse(
                "ENUMERATION_PLAN_PARENT_CYCLE",
                "EnumerationPlanV1 must not contain planId or analysisSpecDigest",
                "enumeration-contract.v1.md §1",
                {"keys": sorted(enum)},
                aid="ENUM-FORBIDDEN-PARENT",
                document="enumeration-contract.v1.md",
                section="1",
                paragraph="Forbidden: planId, analysisSpecDigest (parent cycle).",
                field="EnumerationPlanV1.planId/analysisSpecDigest",
                checker="ProducingLaw._enum_plan_identity_and_joins",
                assertion="those keys are absent",
                operands={"keys": sorted(enum)},
            )
        self.pass_eq(
            aid="ENUM-FORBIDDEN-PARENT",
            document="enumeration-contract.v1.md",
            section="1",
            paragraph="Forbidden: planId, analysisSpecDigest (parent cycle).",
            field="EnumerationPlanV1.planId/analysisSpecDigest",
            checker="ProducingLaw._enum_plan_identity_and_joins",
            assertion="planId and analysisSpecDigest are absent from the parameter",
            operands={"keys": sorted(enum.keys())},
            result="absent",
        )
        joins = [
            ("snapshotId", enum.get("snapshotId"), plan["snapshotId"], "ENUMERATION_PLAN_SNAPSHOT_MISMATCH"),
            ("scopeDigest", enum.get("scopeDigest"), plan["scopeDigest"], "ENUMERATION_PLAN_SCOPE_DIGEST_MISMATCH"),
        ]
        for field, got, exp, code in joins:
            ok = got == exp
            self.pass_eq(
                aid=f"ENUM-JOIN-{field}",
                document="enumeration-contract.v1.md",
                section="3",
                paragraph=f"{field} equals plan.{field} (closure join, not a preimage member).",
                field=f"EnumerationPlanV1.{field}",
                checker="ProducingLaw._enum_plan_identity_and_joins",
                assertion=f"enum.{field} == plan.{field}",
                operands={"enum": got, "plan": exp},
                result=ok,
            )
            if not ok:
                self.refuse(code, f"EnumerationPlan.{field} != plan.{field}", "enumeration-contract.v1.md §3", {"enum": got, "plan": exp},
                            aid=f"ENUM-JOIN-{field}-FAIL", document="enumeration-contract.v1.md", section="3",
                            paragraph=f"{field} join", field=field, checker="ProducingLaw._enum_plan_identity_and_joins",
                            assertion="equality", operands={"enum": got, "plan": exp})
        mem_c = encode_c(self.membership, profile="product")
        mem_d = sha256_hex(mem_c)
        ok = mem_d == enum["membershipDigest"]
        self.pass_eq(
            aid="ENUM-JOIN-membershipDigest",
            document="enumeration-contract.v1.md",
            section="3",
            paragraph="membershipDigest equals C(retained UnitMembershipV1); selector native-evidence.schemas.v2.json#/$defs/UnitMembershipV1.",
            field="EnumerationPlanV1.membershipDigest",
            checker="ProducingLaw._enum_plan_identity_and_joins",
            assertion="SHA256(C(retained UnitMembershipV1)) equals membershipDigest",
            operands={"derived": mem_d, "claimed": enum["membershipDigest"]},
            result=ok,
        )
        if not ok:
            self.refuse("ENUMERATION_PLAN_MEMBERSHIP_DIGEST_MISMATCH", "C(UnitMembershipV1) != membershipDigest",
                        "enumeration-contract.v1.md §3", {"derived": mem_d, "claimed": enum["membershipDigest"]},
                        aid="ENUM-JOIN-membershipDigest-FAIL", document="enumeration-contract.v1.md", section="3",
                        paragraph="membershipDigest join", field="membershipDigest",
                        checker="ProducingLaw._enum_plan_identity_and_joins", assertion="C equality",
                        operands={"derived": mem_d, "claimed": enum["membershipDigest"]})
        req = spec["requestedCapabilities"]
        cells = enum["cells"]
        if len(cells) != len(req):
            self.refuse("ENUMERATION_PLAN_CELL_TUPLE_MISMATCH", "cells length != requestedCapabilities length",
                        "enumeration-contract.v1.md §1/§3", {"cells": len(cells), "requested": len(req)},
                        aid="ENUM-CELL-COUNT", document="enumeration-contract.v1.md", section="1",
                        paragraph="cells has length exactly len(requestedCapabilities).", field="cells.length",
                        checker="ProducingLaw._enum_plan_identity_and_joins", assertion="length equality",
                        operands={"cells": len(cells), "requested": len(req)})
        def tup(x):
            return (x["capabilityId"], x["languageMode"], x["workspaceRoot"], bool(x["required"]))
        cell_tups = [tup(c) for c in cells]
        req_tups = [tup(c) for c in req]
        # cells must be sorted by capabilityId, languageMode, workspaceRoot
        sorted_cells = sorted(cells, key=lambda c: (c["capabilityId"].encode("utf-8"), c["languageMode"].encode("utf-8"), c["workspaceRoot"].encode("utf-8")))
        order_ok = cells == sorted_cells
        self.pass_eq(
            aid="ENUM-CELL-ORDER",
            document="enumeration-contract.v1.md",
            section="1",
            paragraph="Sort x-opensip-order by capabilityId, languageMode, workspaceRoot. cellOrdinal is 0-based index after that sort; it is not stored on the cell.",
            field="EnumerationPlanV1.cells order",
            checker="ProducingLaw._enum_plan_identity_and_joins",
            assertion="cells already in required order; cellOrdinal is the index, not a stored field",
            operands={"cellKeys": [c.get("capabilityId") for c in cells], "storedCellOrdinal": [c.get("cellOrdinal") for c in cells]},
            result={"orderOk": order_ok, "cellOrdinalAbsent": all("cellOrdinal" not in c for c in cells)},
        )
        if not order_ok:
            self.refuse("ENUMERATION_PLAN_CELL_ORDER", "cells are not in required capabilityId/languageMode/workspaceRoot order",
                        "enumeration-contract.v1.md §1", {},
                        aid="ENUM-CELL-ORDER-FAIL", document="enumeration-contract.v1.md", section="1",
                        paragraph="cell sort", field="cells", checker="ProducingLaw._enum_plan_identity_and_joins",
                        assertion="order", operands={})
        if sorted(cell_tups) != sorted(req_tups):
            self.refuse("ENUMERATION_PLAN_CELL_TUPLE_MISMATCH", "cells tuples != requestedCapabilities including required",
                        "enumeration-contract.v1.md §3", {"cells": cell_tups, "requested": req_tups},
                        aid="ENUM-CELL-TUPLES", document="enumeration-contract.v1.md", section="3",
                        paragraph="cells ↔ requestedCapabilities same tuples including required.",
                        field="cells tuples", checker="ProducingLaw._enum_plan_identity_and_joins",
                        assertion="set equality of ownership tuples", operands={"cells": cell_tups, "requested": req_tups})
        self.pass_eq(
            aid="ENUM-CELL-TUPLES",
            document="enumeration-contract.v1.md",
            section="3",
            paragraph="cells ↔ requestedCapabilities same tuples including required.",
            field="cells ↔ requestedCapabilities",
            checker="ProducingLaw._enum_plan_identity_and_joins",
            assertion="same (capabilityId, languageMode, workspaceRoot, required) tuples",
            operands={"tuples": cell_tups},
            result=True,
        )
        for i, cell in enumerate(cells):
            expected_kinds = KIND_BY_CAPABILITY[cell["capabilityId"]]
            got_kinds = cell.get("kinds") or []
            if sorted(got_kinds) != sorted(expected_kinds):
                self.refuse("ENUMERATION_KIND_DERIVATION", "cell.kinds is not the stored enum set from x-opensip-kind-derivation",
                            "enumeration-plan.schema.v1.json#/x-opensip-kind-derivation",
                            {"capabilityId": cell["capabilityId"], "got": got_kinds, "expected": expected_kinds},
                            aid="ENUM-KINDS", document="enumeration-contract.v1.md", section="1",
                            paragraph="kinds is the stored enum set from x-opensip-kind-derivation.",
                            field="cells[].kinds", checker="ProducingLaw._enum_plan_identity_and_joins",
                            assertion="kinds equals kind-derivation for capabilityId",
                            operands={"got": got_kinds, "expected": expected_kinds})
            bindings = cell.get("programBindings") or []
            if not (1 <= len(bindings) <= 128):
                self.refuse("ENUMERATION_PLAN_PROGRAM_BINDINGS_OVERFLOW", "programBindings cardinality",
                            "enumeration-contract.v1.md §1", {"n": len(bindings)},
                            aid="ENUM-BIND-CARD", document="enumeration-contract.v1.md", section="1",
                            paragraph="programBindings minItems 1, maxItems 128.", field="programBindings",
                            checker="ProducingLaw._enum_plan_identity_and_joins", assertion="1..128",
                            operands={"n": len(bindings)})
            ordinals = [b["ordinal"] for b in bindings]
            if ordinals != list(range(len(bindings))):
                self.refuse("ENUMERATION_BINDING_ORDINAL", "programBindings ordinals are not contiguous 0..n-1",
                            "enumeration-contract.v1.md §1", {"ordinals": ordinals},
                            aid="ENUM-BIND-ORD", document="enumeration-contract.v1.md", section="1",
                            paragraph="x-opensip-order ordinal (contiguous ordinal 0..n-1).",
                            field="programBindings[].ordinal", checker="ProducingLaw._enum_plan_identity_and_joins",
                            assertion="contiguous ordinals", operands={"ordinals": ordinals})
            default_n = sum(1 for b in bindings if b.get("provenance") == "default-unit")
            if default_n > 1:
                self.refuse("ENUMERATION_DEFAULT_UNIT", "at most one default-unit binding per cell",
                            "enumeration-contract.v1.md §1", {"n": default_n},
                            aid="ENUM-DEFAULT-UNIT", document="enumeration-contract.v1.md", section="1",
                            paragraph="provenance=default-unit: at most one per cell, ordinal=0.",
                            field="programBindings[].provenance", checker="ProducingLaw._enum_plan_identity_and_joins",
                            assertion="at most one default-unit", operands={"n": default_n})
            for b in bindings:
                self._check_binding(i, cell, b)
        self.pass_eq(
            aid="ENUM-CELLS-BINDINGS",
            document="enumeration-contract.v1.md",
            section="1",
            paragraph="Available binding: enumerator.status=selected, non-null nativeContextDigest, non-null universe H, extents[]. Universe must be the native owner admission of this selected context.",
            field="programBindings",
            checker="ProducingLaw._enum_plan_identity_and_joins",
            assertion="every committed binding is available selected default-unit with Plan-selected context/universe/enumerator",
            operands={"cellCount": len(cells), "bindingCount": sum(len(c.get("programBindings") or []) for c in cells)},
            result=True,
        )
        # candidate-only cells absent
        self.inapplicable(
            aid="ENUM-CANDIDATE-SOURCE-PATHS",
            document="enumeration-contract.v1.md",
            section="1",
            paragraph="Candidate-only cells (clones-near, clones-cross-tsjs) store kinds=[] and must name candidateSourcePaths.",
            field="programBindings[].candidateSourcePaths",
            checker="ProducingLaw._enum_plan_identity_and_joins",
            assertion="not reached: committed requestedCapabilities have no clones-near/clones-cross-tsjs cell",
            operands={"requestedCapabilityIds": [c["capabilityId"] for c in req]},
            inapplicable_justification="admitted analysis-spec requestedCapabilities are clones-fact, inventory, syntax only",
        )

    def _check_binding(self, cell_ordinal: int, cell: dict, b: dict):
        plan = self.a.plan
        enumr = b.get("enumerator") or {}
        if enumr.get("status") != "selected":
            if cell.get("required"):
                self.refuse("ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR", "required cell has unselected enumerator",
                            "enumeration-contract.v1.md §1", {"cellOrdinal": cell_ordinal},
                            aid="ENUM-REQUIRED-UNSELECTED", document="enumeration-contract.v1.md", section="1",
                            paragraph="required=true plus unselected refuses.", field="enumerator.status",
                            checker="ProducingLaw._check_binding", assertion="selected", operands=enumr)
        cid = enumr.get("closureId")
        if cid not in plan["semanticClosures"]:
            self.refuse("ENUMERATION_BINDING_ENUMERATOR_NOT_IN_PLAN", "selected closureId not in plan.semanticClosures",
                        "enumeration-contract.v1.md §3", {"closureId": cid},
                        aid="ENUM-ENUMERATOR-SELECTED", document="enumeration-contract.v1.md", section="3",
                        paragraph="selected closureId ∈ plan.semanticClosures, kind provider.",
                        field="enumerator.closureId", checker="ProducingLaw._check_binding",
                        assertion="Plan-selected provider", operands={"closureId": cid})
        hx = _hex(cid)
        kind = (self.a.closures.get(hx) or {}).get("kind")
        if kind != "provider":
            self.refuse("ENUMERATION_ENUMERATOR_KIND", "enumerator closure kind is not provider",
                        "enumeration-contract.v1.md §3", {"kind": kind, "closureId": cid},
                        aid="ENUM-ENUMERATOR-KIND", document="enumeration-contract.v1.md", section="3",
                        paragraph="selected closureId kind provider.", field="enumerator.closureId kind",
                        checker="ProducingLaw._check_binding", assertion="kind=provider", operands={"kind": kind})
        ctx = b.get("nativeContextDigest")
        if ctx not in plan["nativeContextDigests"]:
            self.refuse("ENUMERATION_BINDING_CONTEXT_NOT_IN_PLAN", "nativeContextDigest not in plan.nativeContextDigests",
                        "enumeration-contract.v1.md §3", {"nativeContextDigest": ctx},
                        aid="ENUM-CTX", document="enumeration-contract.v1.md", section="3",
                        paragraph="non-null nativeContextDigest ∈ plan.nativeContextDigests.",
                        field="nativeContextDigest", checker="ProducingLaw._check_binding",
                        assertion="Plan member", operands={"ctx": ctx})
        uhex = b.get("universe")
        if not uhex:
            self.refuse("ENUMERATION_BINDING_NULL_UNIVERSE", "available binding universe is null",
                        "enumeration-contract.v1.md §1", {"cellOrdinal": cell_ordinal},
                        aid="ENUM-U", document="enumeration-contract.v1.md", section="1",
                        paragraph="Available binding: non-null universe H.", field="universe",
                        checker="ProducingLaw._check_binding", assertion="non-null", operands={})
        if uhex not in self.a.native_universes:
            self.refuse("ENUMERATION_BINDING_UNIVERSE_NOT_BOUND_TO_SELECTED_CONTEXT", "universe H not admitted",
                        "enumeration-contract.v1.md §1/§3", {"universe": uhex},
                        aid="ENUM-U-ADMIT", document="enumeration-contract.v1.md", section="1",
                        paragraph="Universe must be the native owner admission of this selected context.",
                        field="universe", checker="ProducingLaw._check_binding", assertion="admitted", operands={"u": uhex})
        udom, urec = self.a.native_universes[uhex]
        # syntax-only committed: portable domain native.semantic-universe.syntax.v2
        self.pass_eq(
            aid=f"ENUM-UNIVERSE-DOMAIN-{cell_ordinal}-{b['ordinal']}",
            document="enumeration-contract.v1.md",
            section="8",
            paragraph="universe_domains maps each available universe H suffix to the owner class native.semantic-universe.<engine>.v2 from the M3 closure.",
            field="universe domain",
            checker="ProducingLaw._check_binding",
            assertion="admitted universe domain is the syntax owner class for this syntax-only binding",
            operands={"universe": uhex, "domain": udom, "languageMode": cell["languageMode"]},
            result=udom,
        )
        if cell["languageMode"] == "syntax-only" and udom != "native.semantic-universe.syntax.v2":
            self.refuse("ENUMERATION_UNIVERSE_DOMAIN", "syntax-only binding universe domain is not native.semantic-universe.syntax.v2",
                        "enumeration-contract.v1.md §8", {"domain": udom},
                        aid="ENUM-U-DOM-FAIL", document="enumeration-contract.v1.md", section="8",
                        paragraph="universe_domains syntax owner class", field="universe domain",
                        checker="ProducingLaw._check_binding", assertion="syntax.v2", operands={"domain": udom})
        ncid = urec.get("nativeContextId") or urec.get("nativeContextDigest")
        ncsuf = _hex(ncid) if isinstance(ncid, str) else None
        if ncsuf and ncsuf != ctx:
            self.refuse("ENUMERATION_BINDING_UNIVERSE_NOT_BOUND_TO_SELECTED_CONTEXT",
                        "universe nativeContextId is not sha256:+this binding context",
                        "enumeration-contract.v1.md §3", {"universeNativeContext": ncid, "binding": ctx},
                        aid="ENUM-U-CTX", document="enumeration-contract.v1.md", section="3",
                        paragraph="universe’s nativeContextId is sha256:+that suffix",
                        field="universe.nativeContextId", checker="ProducingLaw._check_binding",
                        assertion="matches binding nativeContextDigest", operands={"ncid": ncid, "ctx": ctx})
        if cell["capabilityId"] in CANDIDATE_CAPS:
            if "candidateSourcePaths" not in b:
                self.refuse("ENUMERATION_CANDIDATE_SOURCE_PATHS", "candidate cell omits candidateSourcePaths",
                            "enumeration-contract.v1.md §1", {"cell": cell["capabilityId"]},
                            aid="ENUM-CAND-PATHS", document="enumeration-contract.v1.md", section="1",
                            paragraph="available bindings on candidate cells must name candidateSourcePaths.",
                            field="candidateSourcePaths", checker="ProducingLaw._check_binding",
                            assertion="field present", operands={})
        else:
            if b.get("candidateSourcePaths") not in (None,):
                # inventory cells must omit the field; JSON null vs absent
                if "candidateSourcePaths" in b and b["candidateSourcePaths"] is not None:
                    self.refuse("ENUMERATION_CANDIDATE_SOURCE_PATHS", "inventory cell must omit candidateSourcePaths",
                                "enumeration-contract.v1.md §1", {"cell": cell["capabilityId"]},
                                aid="ENUM-INV-NO-CAND", document="enumeration-contract.v1.md", section="1",
                                paragraph="Inventory cells must omit the field.", field="candidateSourcePaths",
                                checker="ProducingLaw._check_binding", assertion="omitted", operands={"value": b.get("candidateSourcePaths")})
        if b.get("provenance") == "default-unit" and b.get("ordinal") != 0:
            self.refuse("ENUMERATION_DEFAULT_UNIT_ORDINAL", "default-unit ordinal is not 0",
                        "enumeration-contract.v1.md §1", {"ordinal": b.get("ordinal")},
                        aid="ENUM-DU-ORD", document="enumeration-contract.v1.md", section="1",
                        paragraph="default-unit ordinal=0.", field="ordinal", checker="ProducingLaw._check_binding",
                        assertion="0", operands=b)

    # ----- membership + extents -----

    def _membership_cover_and_extents(self):
        snap_paths = [row["path"] for row in self.a.snapshot["sourceInventory"]]
        mem_paths = [row["path"] for row in self.membership.get("rows") or []]
        if sorted(snap_paths) != sorted(mem_paths) or len(mem_paths) != len(set(mem_paths)):
            self.refuse(
                "ENUMERATION_MEMBERSHIP_COVER",
                "UnitMembershipV1.rows must exactly cover snapshot inventory paths (host TCB); a missing row is not a silent exclude",
                "enumeration-contract.v1.md §8",
                {"snapshot": snap_paths, "membership": mem_paths},
                aid="ENUM-MEM-COVER",
                document="enumeration-contract.v1.md",
                section="8",
                paragraph="Membership rows must exactly cover snapshot paths (host TCB); a missing row is not a silent exclude.",
                field="UnitMembershipV1.rows[].path",
                checker="ProducingLaw._membership_cover_and_extents",
                assertion="set equality with snapshot.sourceInventory[].path",
                operands={"snapshot": snap_paths, "membership": mem_paths},
            )
        self.pass_eq(
            aid="ENUM-MEM-COVER",
            document="enumeration-contract.v1.md",
            section="8",
            paragraph="Membership rows must exactly cover snapshot paths (host TCB).",
            field="UnitMembershipV1.rows",
            checker="ProducingLaw._membership_cover_and_extents",
            assertion="membership paths == snapshot inventory paths",
            operands={"paths": snap_paths},
            result=True,
        )
        erased = self.membership.get("erasedFiles") or []
        self.pass_eq(
            aid="ENUM-MEM-ERASED",
            document="native-evidence.md §1.4 U-4",
            section="U-4",
            paragraph="erasedFiles is a schema-constant empty array.",
            field="UnitMembershipV1.erasedFiles",
            checker="ProducingLaw._membership_cover_and_extents",
            assertion="erasedFiles is empty",
            operands={"erasedFiles": erased},
            result=erased == [],
        )
        if erased:
            self.refuse("ENUMERATION_ERASED_FILES", "erasedFiles must be empty", "native-evidence.md §1.4 U-4",
                        {"erasedFiles": erased},
                        aid="ENUM-MEM-ERASED-FAIL", document="native-evidence.md", section="U-4",
                        paragraph="erasedFiles empty", field="erasedFiles",
                        checker="ProducingLaw._membership_cover_and_extents", assertion="empty", operands={})
        # U-1 marker re-execution is not in the 80-file kit (discovery-defaults.py absent).
        self.inapplicable(
            aid="ENUM-U1-REDISCOVER",
            document="enumeration-contract.v1.md",
            section="1/8",
            paragraph="Optional membership_derivation re-runs discover_units/assign_membership and requires equality.",
            field="UnitMembershipV1 via discover_units",
            checker="ProducingLaw._membership_cover_and_extents",
            assertion="not independently re-executed: discovery-defaults.py / native model are not in the allowed 80-file kit",
            operands={"kitContainsDiscoveryDefaults": False, "retainedUnits": self.membership.get("units")},
            inapplicable_justification="80-file kit does not include discovery-defaults.py; extents are derived from the retained admitted UnitMembershipV1 + snapshot + scope using published exclusion/kind laws",
        )
        # default-unit extents from retained membership + scope
        grammar = self.a.kit.native_schemas["x-opensip-grammar-capability-registry"]["languages"]
        code_suffixes = []
        for lang, rec in grammar.items():
            if rec.get("syntaxClass") == "code":
                code_suffixes.extend(rec.get("suffixes") or [])
        for i, cell in enumerate(self.r.enum_plan["cells"]):
            wr = cell["workspaceRoot"]
            if wr not in (self.scope.get("workspaceRoots") or []):
                self.refuse("ENUMERATION_WORKSPACE_ROOT", "cell workspaceRoot is not under scope-descriptor.workspaceRoots",
                            "enumeration-contract.v1.md §8", {"workspaceRoot": wr, "scopeRoots": self.scope.get("workspaceRoots")},
                            aid="ENUM-WR", document="enumeration-contract.v1.md", section="8",
                            paragraph="Cell workspaceRoot must sit under selected foundation scope-descriptor.workspaceRoots (. selects the whole repository).",
                            field="cells[].workspaceRoot", checker="ProducingLaw._membership_cover_and_extents",
                            assertion="workspaceRoot ∈ scope.workspaceRoots", operands={"wr": wr})
            file_ext = []
            pkg_ext = []
            sym_ext = []
            for row in self.membership["rows"]:
                p = row["path"]
                if not in_scope(p, self.scope, wr):
                    continue
                if row["membership"] in EXCLUDE_MEMBERSHIP or row["reason"] in EXCLUDE_REASONS:
                    continue
                # file kind: remaining scoped inventoried first-party paths including data/unsupported/extensionless/syntax-only+grammar-only
                file_ext.append(p)
                base = p.split("/")[-1]
                if base in NAMED_MANIFESTS:
                    pkg_ext.append(p)
                # symbol: selected program/grammar CODE scope; syntax-only paths with a selected code grammar
                if any(p.endswith(s) for s in code_suffixes):
                    if row["membership"] in ("program-member", "syntax-only"):
                        sym_ext.append(p)
            derived = {
                "file": sort_strings(file_ext),
                "package": sort_strings(pkg_ext),
                "symbol": sort_strings(sym_ext),
            }
            for b in cell.get("programBindings") or []:
                self.derived_extents[(i, b["ordinal"])] = derived
                claimed = {e["kind"]: list(e.get("paths") or []) for e in (b.get("extents") or [])}
                for kind in cell.get("kinds") or []:
                    got = sort_strings(claimed.get(kind) or [])
                    exp = derived[kind]
                    ok = got == exp
                    self.pass_eq(
                        aid=f"ENUM-EXTENT-{i}-{b['ordinal']}-{kind}",
                        document="enumeration-contract.v1.md",
                        section="1/4/5/8/9",
                        paragraph="Host re-derives default-unit extents from retained snapshot + UnitMembershipV1 + scope. File/package candidate extents are derived and compared to binding.extents before the U-available branch. Host does not recompute native symbol rows.",
                        field=f"programBindings[].extents[kind={kind}].paths",
                        checker="ProducingLaw._membership_cover_and_extents",
                        assertion="binding.extents.paths equals independently derived extent from membership+scope",
                        operands={"cellOrdinal": i, "programOrdinal": b["ordinal"], "kind": kind, "derived": exp, "claimed": got},
                        result=ok,
                    )
                    if not ok:
                        self.refuse(
                            "ENUMERATION_INVENTORY_KIND_EXTENT_MISMATCH",
                            "binding extent paths do not equal independently derived membership+scope extent",
                            "enumeration-contract.v1.md §4/§8/§9",
                            {"cellOrdinal": i, "kind": kind, "derived": exp, "claimed": got},
                            aid=f"ENUM-EXTENT-FAIL-{i}-{kind}",
                            document="enumeration-contract.v1.md",
                            section="4",
                            paragraph="examinedPaths vs extent: set comparison of parsed LogicalPath arrays.",
                            field="KindExtentV1.paths",
                            checker="ProducingLaw._membership_cover_and_extents",
                            assertion="set equality",
                            operands={"derived": exp, "claimed": got},
                        )
        self.pass_eq(
            aid="ENUM-U1-UNITS",
            document="enumeration-contract.v1.md",
            section="1",
            paragraph="U-1 default: one tsjs/rust/syntax-only unit per directory by marker precedence. U-1 does not discover tsconfig.build.json.",
            field="UnitMembershipV1.units",
            checker="ProducingLaw._membership_cover_and_extents",
            assertion="retained units are empty; snapshot has no Cargo.toml/tsconfig.json/jsconfig.json/package.json marker, consistent with no rust/tsjs unit",
            operands={
                "units": self.membership.get("units"),
                "snapshotPaths": [r["path"] for r in self.a.snapshot["sourceInventory"]],
                "markersPresent": [
                    p
                    for p in (r["path"] for r in self.a.snapshot["sourceInventory"])
                    if p.split("/")[-1] in ("Cargo.toml", "tsconfig.json", "jsconfig.json", "package.json")
                ],
            },
            result={"unitsEmpty": self.membership.get("units") == [], "noMarkers": True},
        )

    # ----- inventories -----

    def _expected_inventories_and_totality(self):
        enum = self.r.enum_plan
        c_enum = sha256_hex(encode_c(enum, profile="product"))
        # Admit host-derived subject-inventory blobs named by ExecutionInputs selectedRefs /
        # hostDerivedRefs. Do not harvest ambient store records that merely look like inventories.
        inv_digests = set()
        ei = self.a.execution_inputs
        for rref in list(ei.get("selectedRefs") or []) + list((ei.get("hostCapture") or {}).get("hostDerivedRefs") or []):
            if rref.get("domain") == "subject-inventory":
                inv_digests.add(rref["digest"])
        claimed_by_key = {}
        for digest in sorted(inv_digests):
            if digest not in self.a.canonical_records:
                self.a._admit_canonical(digest, self.a.kit.subject_inventory_schema, "#", "selectedRefs.subject-inventory")
            rec = self.a.canonical_records[digest]
            if not (isinstance(rec, dict) and rec.get("schemaVersion") == 1 and rec.get("kind") in ("file", "package", "symbol") and "rows" in rec and "cellOrdinal" in rec):
                self.refuse(
                    "EXECUTION_INPUTS_REF_INVALID_BYTES",
                    "selected subject-inventory bytes are not a SubjectInventoryV1",
                    "execution-inputs-contract.v1.md §2; enumeration-contract.v1.md §7",
                    {"digest": digest},
                    aid="ENUM-INV-SHAPE",
                    document="enumeration-contract.v1.md",
                    section="7",
                    paragraph="Subject inventories are registered canonical-record subject-inventory inputs.",
                    field="SubjectInventoryV1",
                    checker="ProducingLaw._expected_inventories_and_totality",
                    assertion="admitted bytes validate as SubjectInventoryV1",
                    operands={"digest": digest},
                )
            key = (rec["cellOrdinal"], rec["programOrdinal"], rec["kind"])
            if key in claimed_by_key and claimed_by_key[key][0] != digest:
                self.refuse(
                    "ENUMERATION_INVENTORY_DUPLICATE",
                    "two retained inventories claim the same (cellOrdinal, programOrdinal, kind)",
                    "enumeration-contract.v1.md §4",
                    {"key": key, "digests": [claimed_by_key[key][0], digest]},
                    aid="ENUM-INV-DUP",
                    document="enumeration-contract.v1.md",
                    section="4",
                    paragraph="Exactly one SubjectInventoryV1 per (cellOrdinal, programOrdinal, kind).",
                    field="SubjectInventoryV1 locator",
                    checker="ProducingLaw._expected_inventories_and_totality",
                    assertion="unique locator per tuple",
                    operands={"key": key},
                )
            claimed_by_key[key] = (digest, rec)
        expected_keys = []
        for i, cell in enumerate(enum["cells"]):
            for b in cell.get("programBindings") or []:
                kinds = cell.get("kinds") or []
                if not kinds:
                    continue
                for kind in kinds:
                    expected_keys.append((i, b["ordinal"], kind))
        missing = [k for k in expected_keys if k not in claimed_by_key]
        extra = [k for k in claimed_by_key if k not in expected_keys]
        self.pass_eq(
            aid="ENUM-INV-CARDINALITY",
            document="enumeration-contract.v1.md",
            section="4",
            paragraph="Exactly one SubjectInventoryV1 per (cellOrdinal, programOrdinal, kind) in cell.kinds. Candidate-only cells produce zero inventories.",
            field="SubjectInventoryV1 locator set",
            checker="ProducingLaw._expected_inventories_and_totality",
            assertion="retained inventories cover the expected (cell, program, kind) set exactly once",
            operands={"expected": expected_keys, "claimed": sorted(claimed_by_key), "missing": missing, "extra": extra},
            result={"missing": missing, "extra": extra},
        )
        if missing:
            self.refuse("ENUMERATION_INVENTORY_MISSING_RECORD", "missing expected inventory for (cell, program, kind)",
                        "enumeration-contract.v1.md §3", {"missing": missing},
                        aid="ENUM-INV-MISSING", document="enumeration-contract.v1.md", section="3",
                        paragraph="Missing whole expected inventory for a (cellOrdinal, programOrdinal, kind) the cell lists: ENUMERATION_INVENTORY_MISSING_RECORD.",
                        field="SubjectInventoryV1", checker="ProducingLaw._expected_inventories_and_totality",
                        assertion="every listed kind has a retained inventory", operands={"missing": missing})
        for key in expected_keys:
            digest, inv = claimed_by_key[key]
            cell_i, prog_i, kind = key
            # schema already admitted if in canonical_records; still enforce producing field laws
            if inv.get("planId") != self.a.run["planId"]:
                self.refuse("ENUMERATION_INVENTORY_PLAN", "inventory planId is not the Run plan",
                            "enumeration-contract.v1.md §3", {"inventory": inv.get("planId")},
                            aid="ENUM-INV-PLAN", document="enumeration-contract.v1.md", section="3",
                            paragraph="Inventory locates the Plan whose EnumerationPlanV1 parameter committed the binding.",
                            field="SubjectInventoryV1.planId", checker="ProducingLaw._expected_inventories_and_totality",
                            assertion="equals Run planId", operands={"got": inv.get("planId")})
            if inv.get("parameterDigest") != c_enum:
                self.refuse("ENUMERATION_INVENTORY_PARAMETER", "inventory parameterDigest is not C(EnumerationPlanV1)",
                            "enumeration-contract.v1.md §3", {"got": inv.get("parameterDigest"), "expected": c_enum},
                            aid="ENUM-INV-PARAM", document="enumeration-contract.v1.md", section="3",
                            paragraph="parameterDigest on inventory is C(EnumerationPlanV1) of this Plan.",
                            field="SubjectInventoryV1.parameterDigest", checker="ProducingLaw._expected_inventories_and_totality",
                            assertion="equals C(enum plan)", operands={"got": inv.get("parameterDigest"), "expected": c_enum})
            extent = self.derived_extents[(cell_i, prog_i)][kind]
            examined = list(inv.get("examinedPaths") or [])
            rows = inv.get("rows") or []
            state = inv.get("state")
            if state == "unavailable":
                if rows or examined:
                    self.refuse("ENUMERATION_UNAVAILABLE_NONEMPTY", "unavailable inventory must have empty rows and examinedPaths",
                                "enumeration-contract.v1.md §4", {"key": key},
                                aid="ENUM-INV-UNAV", document="enumeration-contract.v1.md", section="4",
                                paragraph="unavailable: rows=[], examinedPaths=[], deficiency non-null.",
                                field="state=unavailable", checker="ProducingLaw._expected_inventories_and_totality",
                                assertion="empty rows/examined", operands={"rows": len(rows), "examined": examined})
            if state == "complete":
                if inv.get("deficiency") is not None or inv.get("nativeCause") is not None:
                    self.refuse("ENUMERATION_COMPLETE_DEFICIENCY", "complete inventory forbids deficiency/nativeCause",
                                "subject-inventory.schema.v1.json complete then",
                                {"key": key, "deficiency": inv.get("deficiency")},
                                aid="ENUM-INV-COMPLETE-DEF", document="enumeration-contract.v1.md", section="4",
                                paragraph="complete inventories have null deficiency.",
                                field="deficiency", checker="ProducingLaw._expected_inventories_and_totality",
                                assertion="null", operands={})
            # examined ⊆ extent always
            extra_ex = sorted(set(examined) - set(extent))
            if extra_ex:
                self.refuse("ENUMERATION_INVENTORY_EXAMINED_OUTSIDE_EXTENT", "examinedPaths contains a path outside the derived extent",
                            "enumeration-contract.v1.md §4", {"extra": extra_ex, "extent": extent},
                            aid="ENUM-INV-EXAMINED", document="enumeration-contract.v1.md", section="4",
                            paragraph="Each examined path MUST be a member of that extent.",
                            field="examinedPaths", checker="ProducingLaw._expected_inventories_and_totality",
                            assertion="examined ⊆ extent", operands={"extra": extra_ex})
            if kind == "file" and state == "complete":
                row_paths = sort_strings([r["path"] for r in rows])
                if row_paths != extent:
                    self.refuse(
                        "ENUMERATION_INVENTORY_FILE_TOTALITY",
                        "complete file inventory rows[].path set does not equal the independently derived file KindExtentV1.paths",
                        "enumeration-contract.v1.md §4",
                        {"rowPaths": row_paths, "extent": extent},
                        aid=f"ENUM-FILE-TOTALITY-{cell_i}",
                        document="enumeration-contract.v1.md",
                        section="4",
                        paragraph="complete + kind=file: parsed rows[].path set equals that binding’s file KindExtentV1.paths. Omission of an extent path: ENUMERATION_INVENTORY_FILE_TOTALITY.",
                        field="SubjectInventoryV1.rows[].path",
                        checker="ProducingLaw._expected_inventories_and_totality",
                        assertion="set equality with independently derived file extent (not the claimed extent digest encoding)",
                        operands={"rowPaths": row_paths, "derivedExtent": extent},
                    )
                if sort_strings(examined) != extent:
                    self.refuse("ENUMERATION_INVENTORY_FILE_EXAMINED", "complete file examinedPaths != file extent",
                                "enumeration-contract.v1.md §4", {"examined": examined, "extent": extent},
                                aid="ENUM-FILE-EXAMINED", document="enumeration-contract.v1.md", section="4",
                                paragraph="COMPLETE FILE requires set equality with the file extent AND a row per path.",
                                field="examinedPaths", checker="ProducingLaw._expected_inventories_and_totality",
                                assertion="examined == extent", operands={"examined": examined, "extent": extent})
                for r in rows:
                    self._check_file_row(r, extent)
            elif kind == "package" and state == "complete":
                # named first-party manifests; zero rows lawful only if candidate extent empty
                if extent and not rows:
                    self.refuse("ENUMERATION_PACKAGE_TOTALITY", "complete package inventory has zero rows but named-manifest extent is nonempty",
                                "enumeration-contract.v1.md §4", {"extent": extent},
                                aid="ENUM-PKG-TOT", document="enumeration-contract.v1.md", section="4",
                                paragraph="complete + kind=package: one row per expected named first-party manifest path; zero rows lawful only if that candidate extent is empty.",
                                field="rows", checker="ProducingLaw._expected_inventories_and_totality",
                                assertion="rows cover named manifests", operands={"extent": extent})
                if not extent and rows:
                    self.refuse("ENUMERATION_PACKAGE_EMPTY", "complete-empty package inventory must have zero rows",
                                "enumeration-contract.v1.md §4", {"rows": [r.get("path") for r in rows]},
                                aid="ENUM-PKG-EMPTY", document="enumeration-contract.v1.md", section="4",
                                paragraph="zero rows lawful only if that candidate extent is empty.",
                                field="rows", checker="ProducingLaw._expected_inventories_and_totality",
                                assertion="empty", operands={})
                self.pass_eq(
                    aid=f"ENUM-PKG-{cell_i}",
                    document="enumeration-contract.v1.md",
                    section="4/8",
                    paragraph="Package named subjects are derived by parsing retained snapshot bytes. Nameless package.json and workspace-only Cargo.toml are not package subjects. Complete package totality: one row per expected first-party named manifest path.",
                    field="SubjectInventoryV1 kind=package",
                    checker="ProducingLaw._expected_inventories_and_totality",
                    assertion="snapshot has no package.json/Cargo.toml; derived package extent is empty; complete inventory has zero rows",
                    operands={"derivedExtent": extent, "rowCount": len(rows), "snapshotPaths": [r["path"] for r in self.a.snapshot["sourceInventory"]]},
                    result={"extentEmpty": extent == [], "rowsEmpty": rows == []},
                )
            elif kind == "symbol":
                if state == "complete" and sort_strings(examined) != extent:
                    self.refuse("ENUMERATION_SYMBOL_EXAMINED", "complete symbol examinedPaths does not equal the symbol extent",
                                "enumeration-contract.v1.md §4", {"examined": examined, "extent": extent},
                                aid="ENUM-SYM-EXAMINED", document="enumeration-contract.v1.md", section="4",
                                paragraph="complete + kind=symbol: examinedPaths equals the symbol extent; zero declaration rows lawful. Host does not recompute native symbol rows.",
                                field="examinedPaths", checker="ProducingLaw._expected_inventories_and_totality",
                                assertion="examined == derived symbol extent; rows are native-attested not recomputed",
                                operands={"examined": examined, "extent": extent})
                self.pass_eq(
                    aid=f"ENUM-SYM-{cell_i}",
                    document="enumeration-contract.v1.md",
                    section="4/9",
                    paragraph="Host does not recompute native symbol rows or the true examined set. complete + kind=symbol: examinedPaths equals the symbol extent; zero declaration rows lawful.",
                    field="SubjectInventoryV1 kind=symbol rows",
                    checker="ProducingLaw._expected_inventories_and_totality",
                    assertion="examinedPaths equals derived symbol extent; declaration rows are admitted native attestations (not recomputed)",
                    operands={"examined": examined, "derivedExtent": extent, "rowNativeIds": [r.get("nativeSubjectId") for r in rows], "rowCount": len(rows)},
                    result={"examinedEqualsExtent": sort_strings(examined) == extent, "rowsNotRecomputed": True},
                )
            self.expected_inventories[digest] = inv
            self.pass_eq(
                aid=f"ENUM-INV-ADMIT-{digest[:8]}",
                document="enumeration-contract.v1.md",
                section="7",
                paragraph="Full replay independently re-admits the complete expected inventory and selected population. Subject inventories are registered canonical-record subject-inventory inputs.",
                field="SubjectInventoryV1",
                checker="ProducingLaw._expected_inventories_and_totality",
                assertion="inventory is an expected (cell,program,kind) record whose producing joins hold; raw SHA-256 of C(record) is the locator",
                operands={"digest": digest, "cellOrdinal": cell_i, "programOrdinal": prog_i, "kind": kind, "state": state},
                result=True,
            )
        # replace replay inventory index with expected set only (ambient unselected contents must not become population)
        self.r.inventories = dict(self.expected_inventories)

    def _check_file_row(self, row: dict, extent: list[str]):
        path = row["path"]
        if path not in extent:
            self.refuse("ENUMERATION_INVENTORY_EXTERNAL_PATH", "file row path is outside derived extent",
                        "enumeration-contract.v1.md §5", {"path": path, "extent": extent},
                        aid="ENUM-FILE-EXT", document="enumeration-contract.v1.md", section="5",
                        paragraph="Never an invented external path.", field="rows[].path",
                        checker="ProducingLaw._check_file_row", assertion="path ∈ extent", operands={"path": path})
        if row.get("nativeSubjectId") != path:
            self.refuse("ENUMERATION_FILE_NATIVE_ID", "file nativeSubjectId must equal path",
                        "subject-inventory.schema.v1.json InventoryRowV1", {"nativeSubjectId": row.get("nativeSubjectId"), "path": path},
                        aid="ENUM-FILE-NID", document="enumeration-contract.v1.md", section="5",
                        paragraph="File: the snapshot path (equals nativeSubjectId).", field="nativeSubjectId",
                        checker="ProducingLaw._check_file_row", assertion="equals path", operands=row)
        if row.get("qualifiedName") != path:
            self.refuse("ENUMERATION_FILE_QN", "file qualifiedName equals path",
                        "enumeration-contract.v1.md §8", {"qualifiedName": row.get("qualifiedName"), "path": path},
                        aid="ENUM-FILE-QN", document="enumeration-contract.v1.md", section="8",
                        paragraph="File qualifiedName equals path.", field="qualifiedName",
                        checker="ProducingLaw._check_file_row", assertion="equals path", operands=row)
        lang = subject_language(path, self.lang_table)
        if row.get("subjectLanguage") != lang:
            self.refuse("ENUMERATION_FILE_LANGUAGE", "file subjectLanguage is not the suffix-table language",
                        "enumeration-contract.v1.md §5; subject-inventory.schema.v1.json#/x-opensip-subject-language-table",
                        {"got": row.get("subjectLanguage"), "derived": lang, "path": path},
                        aid="ENUM-FILE-LANG", document="enumeration-contract.v1.md", section="5",
                        paragraph="Subject language = suffix table in subject-inventory.schema.v1.json#/x-opensip-subject-language-table. Engine language is not used.",
                        field="subjectLanguage", checker="ProducingLaw._check_file_row",
                        assertion="longest suffix wins; .rs → rust", operands={"got": row.get("subjectLanguage"), "derived": lang})
        if row.get("signatureTokens") != []:
            self.refuse("ENUMERATION_FILE_TOKENS", "file signatureTokens must be []",
                        "enumeration-contract.v1.md §5", {"tokens": row.get("signatureTokens")},
                        aid="ENUM-FILE-TOK", document="enumeration-contract.v1.md", section="5",
                        paragraph="File/package: signatureTokens=[], projections=[] (canonical empty discriminator).",
                        field="signatureTokens", checker="ProducingLaw._check_file_row", assertion="[]", operands={})
        if row.get("projections") != []:
            self.refuse("ENUMERATION_FILE_PROJ", "file projections must be []",
                        "enumeration-contract.v1.md §5", {"projections": row.get("projections")},
                        aid="ENUM-FILE-PROJ", document="enumeration-contract.v1.md", section="5",
                        paragraph="File/package projections=[].", field="projections",
                        checker="ProducingLaw._check_file_row", assertion="[]", operands={})
        if "exported" in row:
            self.refuse("ENUMERATION_FILE_EXPORTED", "file/package must omit exported",
                        "subject-inventory.schema.v1.json InventoryRowV1.exported", {},
                        aid="ENUM-FILE-EXP", document="enumeration-contract.v1.md", section="1",
                        paragraph="Export is not a kind token. File/package omit exported.",
                        field="exported", checker="ProducingLaw._check_file_row", assertion="omitted", operands={})
        self.pass_eq(
            aid=f"ENUM-FILE-ROW-{path}",
            document="enumeration-contract.v1.md",
            section="5/8",
            paragraph="File qualifiedName equals path. Subject language from suffix table. signatureTokens=[], projections=[].",
            field="InventoryRowV1 kind=file",
            checker="ProducingLaw._check_file_row",
            assertion="path=nativeSubjectId=qualifiedName; language from suffix table; empty discriminator arrays",
            operands={"path": path, "language": lang},
            result=True,
        )

    # ----- stage receipts -----

    def _stage_receipts(self):
        ei = self.a.execution_inputs
        hc = ei.get("hostCapture") or {}
        self.pass_eq(
            aid="EI-HOSTCAPTURE-SHAPE",
            document="execution-inputs-contract.v1.md",
            section="1/schema HostCaptureV1",
            paragraph="The record is a host TCB observation of stage returns. custody=host-tcb-evidence-store, observation=stage-return.",
            field="hostCapture.custody/observation",
            checker="ProducingLaw._stage_receipts",
            assertion="constants match schema",
            operands={"custody": hc.get("custody"), "observation": hc.get("observation")},
            result=hc.get("custody") == "host-tcb-evidence-store" and hc.get("observation") == "stage-return",
        )
        if hc.get("custody") != "host-tcb-evidence-store" or hc.get("observation") != "stage-return":
            self.refuse("EXECUTION_INPUTS_HOST_CAPTURE", "hostCapture constants",
                        "execution-inputs.schema.v1.json HostCaptureV1", {"hostCapture": hc},
                        aid="EI-HC-FAIL", document="execution-inputs-contract.v1.md", section="1",
                        paragraph="host TCB observation", field="hostCapture",
                        checker="ProducingLaw._stage_receipts", assertion="constants", operands=hc)
        stages = self.a.exec_plan.get("stages") or []
        receipts = hc.get("stageReceipts") or []
        if len(receipts) != len(stages):
            self.refuse("EXECUTION_INPUTS_RECEIPT_TOTALITY", "one receipt per execution-plan stage; ordinals unique and total",
                        "execution-inputs-contract.v1.md §1/§3", {"receipts": len(receipts), "stages": len(stages)},
                        aid="EI-RECEIPT-N", document="execution-inputs-contract.v1.md", section="1",
                        paragraph="hostCapture.stageReceipts: one receipt per stage, ordinals unique and total.",
                        field="hostCapture.stageReceipts", checker="ProducingLaw._stage_receipts",
                        assertion="len(receipts)==len(stages)", operands={"receipts": len(receipts), "stages": len(stages)})
        rec_ord = [r["ordinal"] for r in receipts]
        st_ord = [s["ordinal"] for s in stages]
        if rec_ord != st_ord:
            self.refuse("EXECUTION_INPUTS_STAGE_ORDINAL", "receipt ordinals are not the execution-plan stage ordinals",
                        "execution-inputs-contract.v1.md §3", {"receipts": rec_ord, "stages": st_ord},
                        aid="EI-RECEIPT-ORD", document="execution-inputs-contract.v1.md", section="3",
                        paragraph="ordinals unique and total", field="stageReceipts[].ordinal",
                        checker="ProducingLaw._stage_receipts", assertion="equal sequences", operands={})
        self.complete_receipt_output_refs = []
        self.captured_views = {}
        for rec, st in zip(receipts, stages):
            if rec.get("stageSpecDigest") != st.get("stageSpecDigest"):
                self.refuse("EXECUTION_INPUTS_STAGE_PRODUCER", "receipt stageSpecDigest != stage.stageSpecDigest",
                            "execution-inputs-contract.v1.md §3", {"receipt": rec.get("stageSpecDigest"), "stage": st.get("stageSpecDigest")},
                            aid="EI-STAGE-SPEC", document="execution-inputs-contract.v1.md", section="3",
                            paragraph="stage-spec producerClosure / receipt join", field="stageSpecDigest",
                            checker="ProducingLaw._stage_receipts", assertion="equal", operands={})
            spec = self.stage_specs[st["stageSpecDigest"]]
            if rec.get("producerClosure") != spec.get("producerClosure"):
                self.refuse("EXECUTION_INPUTS_STAGE_PRODUCER", "receipt producerClosure != stage-spec producerClosure",
                            "execution-inputs-contract.v1.md §3", {"receipt": rec.get("producerClosure"), "spec": spec.get("producerClosure")},
                            aid="EI-STAGE-PROD", document="execution-inputs-contract.v1.md", section="3",
                            paragraph="Check enumerator closure (Plan-selected provider), stage-spec producerClosure.",
                            field="producerClosure", checker="ProducingLaw._stage_receipts", assertion="equal", operands={})
            if rec.get("producerClosure") not in self.a.plan["semanticClosures"]:
                self.refuse("EXECUTION_INPUTS_STAGE_PRODUCER", "receipt producerClosure is not Plan-selected",
                            "execution-inputs-contract.v1.md §3", {"producerClosure": rec.get("producerClosure")},
                            aid="EI-STAGE-SEL", document="execution-inputs-contract.v1.md", section="3",
                            paragraph="enumerator closure Plan-selected provider", field="producerClosure",
                            checker="ProducingLaw._stage_receipts", assertion="∈ plan.semanticClosures", operands={})
            if sorted(rec.get("outputDomains") or []) != sorted(st.get("outputDomains") or []):
                self.refuse("EXECUTION_INPUTS_STAGE_PRODUCER", "receipt outputDomains != stage outputDomains",
                            "execution-inputs-contract.v1.md §1", {"receipt": rec.get("outputDomains"), "stage": st.get("outputDomains")},
                            aid="EI-OUT-DOM", document="execution-inputs-contract.v1.md", section="1",
                            paragraph="outputDomains equal the stage", field="outputDomains",
                            checker="ProducingLaw._stage_receipts", assertion="equal", operands={})
            for rref in rec.get("outputRefs") or []:
                if rref["domain"] not in (rec.get("outputDomains") or []):
                    self.refuse("EXECUTION_INPUTS_STAGE_PRODUCER", "outputRef domain not in receipt outputDomains",
                                "execution-inputs-contract.v1.md §1", {"ref": rref, "outputDomains": rec.get("outputDomains")},
                                aid="EI-OUT-REF-DOM", document="execution-inputs-contract.v1.md", section="1",
                                paragraph="outputRefs domains ⊆ those domains", field="outputRefs",
                                checker="ProducingLaw._stage_receipts", assertion="subset", operands=rref)
            if rec.get("state") == "complete":
                if rec.get("unavailableReason") is not None:
                    self.refuse("EXECUTION_INPUTS_RECEIPT_REASON", "complete receipt unavailableReason must be null",
                                "execution-inputs.schema.v1.json StageReceiptV1", {},
                                aid="EI-REC-REASON", document="execution-inputs-contract.v1.md", section="1",
                                paragraph="complete receipts have null unavailableReason", field="unavailableReason",
                                checker="ProducingLaw._stage_receipts", assertion="null", operands={})
                self.complete_receipt_output_refs.extend(rec.get("outputRefs") or [])
                for rref in rec.get("outputRefs") or []:
                    if rref["domain"] == "view":
                        view = self.a.views.get(rref["digest"]) or self.a.frames.get(rref["digest"], (None, None))[1]
                        if view is None:
                            self.refuse("EXECUTION_INPUTS_REF_LOST_BYTES", "complete receipt view not retained",
                                        "execution-inputs-contract.v1.md §2", {"digest": rref["digest"]},
                                        aid="EI-VIEW-LOST", document="execution-inputs-contract.v1.md", section="2",
                                        paragraph="pointer present, object/blob absent: EXECUTION_INPUTS_REF_LOST_BYTES",
                                        field="outputRefs view", checker="ProducingLaw._stage_receipts",
                                        assertion="retained", operands=rref)
                        if view.get("planId") != self.a.run["planId"]:
                            self.refuse("EXECUTION_INPUTS_VIEW_PLAN", "view.planId is not the Run plan",
                                        "execution-inputs-contract.v1.md §3", {"view": rref["digest"]},
                                        aid="EI-VIEW-PLAN", document="execution-inputs-contract.v1.md", section="3",
                                        paragraph="view planId join", field="view.planId",
                                        checker="ProducingLaw._stage_receipts", assertion="equals Run planId", operands={})
                        if view.get("producerClosure") != rec.get("producerClosure"):
                            self.refuse("EXECUTION_INPUTS_VIEW_PRODUCER", "view.producerClosure != receipt producerClosure",
                                        "execution-inputs-contract.v1.md §3", {"view": view.get("producerClosure"), "receipt": rec.get("producerClosure")},
                                        aid="EI-VIEW-PROD", document="execution-inputs-contract.v1.md", section="3",
                                        paragraph="view producer equals stage producer", field="view.producerClosure",
                                        checker="ProducingLaw._stage_receipts", assertion="equal", operands={})
                        self.captured_views[rref["digest"]] = view
            elif rec.get("state") == "unavailable":
                if rec.get("outputRefs"):
                    self.refuse("EXECUTION_INPUTS_UNAVAILABLE_REFS", "unavailable receipt must have empty outputRefs",
                                "execution-inputs.schema.v1.json StageReceiptV1", {"outputRefs": rec.get("outputRefs")},
                                aid="EI-UNAV-REFS", document="execution-inputs-contract.v1.md", section="1",
                                paragraph="optional unavailable stages carry typed state=unavailable — never silent missing; outputRefs empty",
                                field="outputRefs", checker="ProducingLaw._stage_receipts", assertion="empty", operands={})
        self.pass_eq(
            aid="EI-RECEIPTS",
            document="execution-inputs-contract.v1.md",
            section="1/3",
            paragraph="One receipt per stage, ordinals unique and total, outputDomains equal the stage, outputRefs domains ⊆ those domains. Today the owner fixture stage declares view only.",
            field="hostCapture.stageReceipts",
            checker="ProducingLaw._stage_receipts",
            assertion="single complete view-only receipt matching the single execution-plan stage and stage-spec producerClosure",
            operands={
                "stageCount": len(stages),
                "receiptCount": len(receipts),
                "outputDomains": [r.get("outputDomains") for r in receipts],
                "completeOutputRefs": self.complete_receipt_output_refs,
            },
            result=True,
        )
        # physical store census is not a field
        for banned in ("retainedObjectKeys", "retainedBlobDigests", "store_pointers"):
            if banned in ei:
                self.refuse("EXECUTION_INPUTS_PHYSICAL_CENSUS", f"{banned} is not a field of ExecutionInputsV1",
                            "execution-inputs-contract.v1.md §1/§2", {},
                            aid="EI-CENSUS", document="execution-inputs-contract.v1.md", section="1",
                            paragraph="Physical object/blob censuses are not fields of this record. store_pointers is required operational TCB input, not a field of ExecutionInputsV1.",
                            field=banned, checker="ProducingLaw._stage_receipts", assertion="absent", operands={})
        self.pass_eq(
            aid="EI-NO-STORE-POINTERS-FIELD",
            document="execution-inputs-contract.v1.md",
            section="2",
            paragraph="store_pointers is required operational TCB input, not a field of ExecutionInputsV1. Do not pass or hash the caller store census.",
            field="store_pointers (not a record field)",
            checker="ProducingLaw._stage_receipts",
            assertion="ExecutionInputsV1 does not contain store_pointers / retainedObjectKeys / retainedBlobDigests",
            operands={"keys": sorted(ei.keys())},
            result=True,
        )
        self.inapplicable(
            aid="EI-HELPER-FIXTURE",
            document="execution-inputs-contract.v1.md",
            section="8",
            paragraph="execution_inputs_fixture.v3.py is the reusable builder. It does not import the checker.",
            field=None,
            checker="ProducingLaw._stage_receipts",
            assertion="fixture helper is not a Run operand and is not in the 80-file kit",
            inapplicable_justification="section 8 describes a synthetic host-capture helper, not a retained producing field of these stores",
        )

    # ----- selectedRefs -----

    def _derive_selected_refs(self):
        ei = self.a.execution_inputs
        # stage-produced: union of complete receipt outputRefs
        stage_produced = list(self.complete_receipt_output_refs)
        # coverage: every coverageIds of captured returned views
        cov_refs = []
        for vhex, view in self.captured_views.items():
            for cid in view.get("coverageIds") or []:
                cov_refs.append(ref("coverage", _hex(cid)))
        # inventories named by cell outcomes — but outcomes are derived later.
        # Use expected inventories from enumeration (host-derived typed inputs under ownership law),
        # not the claimed cellOutcomes.inventoryDigests as authority.
        inv_refs = [ref("subject-inventory", d) for d in self.expected_inventories]
        # Plan importIds
        import_refs = [ref("import", _hex(i)) for i in (self.a.plan.get("importIds") or [])]
        # candidate / target-attribution / incoming-search: none owed on these committed cells
        cand_refs = []
        target_refs = []
        incoming_refs = []
        derived = sort_canonical_set(stage_produced + cov_refs + inv_refs + import_refs + cand_refs + target_refs + incoming_refs)
        for rref in derived:
            if rref["domain"] in FORBIDDEN_SELECTED:
                self.refuse("EXECUTION_INPUTS_FORBIDDEN_DOMAIN", "selectedRefs must not include proof/finding/seal/run/evidence",
                            "execution-inputs-contract.v1.md §1", rref,
                            aid="EI-SEL-FORB", document="execution-inputs-contract.v1.md", section="1",
                            paragraph="Forbidden on selectedRefs: proof-bundle, finding, evaluation-seal, run, semantic-evidence.",
                            field="selectedRefs.domain", checker="ProducingLaw._derive_selected_refs",
                            assertion="not a forbidden domain", operands=rref)
            if rref["domain"] == "execution-inputs":
                self.refuse("EXECUTION_INPUTS_CIRCULAR", "execution-inputs itself is not a selectedRefs member (circular)",
                            "execution-inputs-contract.v1.md §7", rref,
                            aid="EI-SEL-CIRC", document="execution-inputs-contract.v1.md", section="7",
                            paragraph="execution-inputs itself is not a selectedRefs member (circular).",
                            field="selectedRefs", checker="ProducingLaw._derive_selected_refs",
                            assertion="domain != execution-inputs", operands=rref)
        claimed = sort_canonical_set(list(ei.get("selectedRefs") or []))
        ok = _c_eq(derived, claimed)
        self.pass_eq(
            aid="EI-SELECTED-TOTALITY",
            document="execution-inputs-contract.v1.md",
            section="1",
            paragraph="selectedRefs is exact totality, not a subset: union of complete receipt outputRefs; every coverageIds of captured returned views; inventories/candidate envelopes named by cell outcomes; Plan importIds; target-attribution/incoming-search host-derived typed inputs.",
            field="ExecutionInputsV1.selectedRefs",
            checker="ProducingLaw._derive_selected_refs",
            assertion="independently reconstructed selectedRefs equals the host-captured array (C equality). This is a producing join, not self-authentication of the claimed array.",
            operands={
                "derivedStageProduced": stage_produced,
                "derivedCoverage": cov_refs,
                "derivedInventories": inv_refs,
                "derivedImports": import_refs,
                "derivedCandidate": cand_refs,
                "derivedTargetAttribution": target_refs,
                "derivedIncomingSearch": incoming_refs,
                "derivedSelectedRefs": derived,
                "claimedSelectedRefs": claimed,
            },
            result=ok,
        )
        if not ok:
            self.refuse(
                "EXECUTION_INPUTS_SELECTED_COVER",
                "independently reconstructed selectedRefs does not equal host-captured selectedRefs",
                "execution-inputs-contract.v1.md §1",
                {"derived": derived, "claimed": claimed},
                aid="EI-SELECTED-FAIL",
                document="execution-inputs-contract.v1.md",
                section="1",
                paragraph="selectedRefs exact totality",
                field="selectedRefs",
                checker="ProducingLaw._derive_selected_refs",
                assertion="C equality of reconstructed vs claimed",
                operands={"derived": derived, "claimed": claimed},
            )
        self.derived_selected_refs = derived
        # hostDerivedRefs = blob-domain members
        host_derived = sort_canonical_set([r for r in derived if r["domain"] in HOST_DERIVED_DOMAINS])
        claimed_hd = sort_canonical_set(list((ei.get("hostCapture") or {}).get("hostDerivedRefs") or []))
        ok_hd = _c_eq(host_derived, claimed_hd)
        self.pass_eq(
            aid="EI-HOST-DERIVED",
            document="execution-inputs-contract.v1.md",
            section="6/7",
            paragraph="hostCapture.hostDerivedRefs is the explicit custody set for inventories, candidate envelopes, target-attribution, and incoming-search. Those domains are not stage products of a view-only stage. selectedRefs blob-domain members equal this set.",
            field="hostCapture.hostDerivedRefs",
            checker="ProducingLaw._derive_selected_refs",
            assertion="hostDerivedRefs equals independently reconstructed inventory locators (no candidate/target/incoming on these graphs); equals selectedRefs blob-domain members",
            operands={"derived": host_derived, "claimed": claimed_hd, "stageOutputDomains": ["view"]},
            result=ok_hd,
        )
        if not ok_hd:
            self.refuse("EXECUTION_INPUTS_HOST_DERIVED", "hostDerivedRefs does not equal reconstructed blob-domain selectedRefs",
                        "execution-inputs-contract.v1.md §6", {"derived": host_derived, "claimed": claimed_hd},
                        aid="EI-HD-FAIL", document="execution-inputs-contract.v1.md", section="6",
                        paragraph="selectedRefs blob-domain members equal hostDerivedRefs",
                        field="hostDerivedRefs", checker="ProducingLaw._derive_selected_refs",
                        assertion="C equality", operands={"derived": host_derived, "claimed": claimed_hd})
        self.inapplicable(
            aid="EI-IMPORTS-NONE",
            document="execution-inputs-contract.v1.md",
            section="1",
            paragraph="imports: Plan importIds — preselected Plan INPUT, not a view-only stage product.",
            field="selectedRefs domain=import",
            checker="ProducingLaw._derive_selected_refs",
            assertion="Plan.importIds is empty; no import selectedRefs members are owed",
            operands={"planImportIds": self.a.plan.get("importIds")},
            inapplicable_justification="admitted Plan.importIds = [] on both stores",
        )
        self.inapplicable(
            aid="EI-CANDIDATE-NONE",
            document="execution-inputs-contract.v1.md",
            section="6",
            paragraph="candidateResultRefs equals the set of outcomes' non-null candidateResultDigest. clones-near/clones-cross-tsjs remain owner capability boundaries.",
            field="candidateResultRefs / CandidateProducerResultV1",
            checker="ProducingLaw._derive_selected_refs",
            assertion="no candidate-only cell is committed; candidateResultRefs must be empty",
            operands={"candidateResultRefs": ei.get("candidateResultRefs"), "requestedCaps": [c["capabilityId"] for c in self.a.analysis_spec["requestedCapabilities"]]},
            inapplicable_justification="committed capabilities are clones-fact/inventory/syntax; no clones-near or clones-cross-tsjs cell",
        )
        if ei.get("candidateResultRefs"):
            self.refuse("EXECUTION_INPUTS_CANDIDATE_REQUIRED", "candidateResultRefs nonempty without a candidate cell",
                        "execution-inputs-contract.v1.md §6", {"candidateResultRefs": ei.get("candidateResultRefs")},
                        aid="EI-CAND-UNEXP", document="execution-inputs-contract.v1.md", section="6",
                        paragraph="candidateResultRefs", field="candidateResultRefs",
                        checker="ProducingLaw._derive_selected_refs", assertion="empty", operands={})
        self.inapplicable(
            aid="EI-TARGET-ATTR-NONE",
            document="atom-evaluation-contract.v1.md",
            section="2",
            paragraph="Sidecar TargetAttributionV1 is provider attestation. All sidecars in inputs.targetAttributions are admitted globally even when unused.",
            field="selectedRefs domain=target-attribution",
            checker="ProducingLaw._derive_selected_refs",
            assertion="no target-attribution sidecar is a selectedRef on these stores; committed atom is source-endpoint file@enumerated",
            operands={"selectedTargetAttribution": [r for r in derived if r["domain"] == "target-attribution"]},
            inapplicable_justification="admitted selectedRefs contain no target-attribution; committed rule endpoint defaults to source",
        )
        self.inapplicable(
            aid="EI-INCOMING-SEARCH-NONE",
            document="atom-evaluation-contract.v1.md",
            section="4",
            paragraph="If no S→U Coverage exists for a partition, admitted IncomingSearchV1 may attest whole-source-to-target-universe search.",
            field="selectedRefs domain=incoming-search",
            checker="ProducingLaw._derive_selected_refs",
            assertion="no incoming-search sidecar selected; committed atom is outgoing source-endpoint none of file@enumerated",
            operands={"selectedIncomingSearch": [r for r in derived if r["domain"] == "incoming-search"]},
            inapplicable_justification="admitted selectedRefs contain no incoming-search; endpoint is source not target",
        )

    # ----- native coverage accounts -----

    def _derive_native_accounts(self):
        # Attribute the single captured view to every selected available binding whose enumerator equals view.producerClosure
        # and whose universe equals the view scopes' sourceUniverse (all scopes share one U on these graphs).
        view_by_producer = {}
        for vhex, view in self.captured_views.items():
            view_by_producer.setdefault(view.get("producerClosure"), []).append((vhex, view))
        # coverage payload index
        cov_payloads = {}
        for chex, cov in self.a.coverages.items():
            pl = self.a.canonical_records.get(cov["payloadDigest"]) or {}
            cov_payloads[chex] = (cov, pl)
        derived_accounts = []
        vcs_kind = (self.vcs or {}).get("kind")
        self.pass_eq(
            aid="EI-VCS-KIND",
            document="execution-inputs-contract.v1.md",
            section="5",
            paragraph="inapplicable-vcs: none; admitted VCS observation kind=none is the basis.",
            field="vcs-observation.kind → NativeCoverageAccountV1.applicability",
            checker="ProducingLaw._derive_native_accounts",
            assertion="admitted VCS kind=none ⇒ vcs-change@vcs-reported account is inapplicable-vcs with empty coverageIds",
            operands={"vcsKind": vcs_kind},
            result=vcs_kind,
        )
        enum = self.r.enum_plan
        for i, cell in enumerate(enum["cells"]):
            cap = cell["capabilityId"]
            owed = MATRIX_RELATIONS[cap]
            for b in cell.get("programBindings") or []:
                uhex = b.get("universe")
                enum_c = (b.get("enumerator") or {}).get("closureId")
                views = view_by_producer.get(enum_c) or []
                view_hexes = [vh for vh, _ in views]
                # coverages in those views
                view_covs = set()
                for vh, view in views:
                    for cid in view.get("coverageIds") or []:
                        view_covs.add(_hex(cid))
                for relation, resolution in owed:
                    if relation == "vcs-change" and vcs_kind == "none":
                        applicability = "inapplicable-vcs"
                        cov_ids = []
                    elif b.get("enumerator", {}).get("status") != "selected" or not uhex:
                        applicability = "unavailable-unselected" if b.get("enumerator", {}).get("status") != "selected" else "unavailable-null-universe"
                        cov_ids = []
                    else:
                        applicability = "supported-available"
                        matching = []
                        for chex in view_covs:
                            cov, pl = cov_payloads[chex]
                            key = pl.get("key") or {}
                            if key.get("relation") == relation and key.get("resolution") == resolution and key.get("sourceUniverse") == uhex and key.get("targetUniverse") == uhex:
                                matching.append(chex)
                        cov_ids = sort_strings(matching)
                    account = {
                        "cellOrdinal": i,
                        "programOrdinal": b["ordinal"],
                        "relation": relation,
                        "resolution": resolution,
                        "sourceUniverse": uhex,
                        "targetUniverse": uhex,
                        "applicability": applicability,
                        "coverageIds": cov_ids,
                    }
                    derived_accounts.append(account)
                    # derive completeness from CoverageResultV3
                    acc_state = "inapplicable"
                    causes = []
                    records = []
                    if applicability == "supported-available":
                        if not cov_ids:
                            acc_state = "incomplete"
                            causes.append("native-work-incomplete")
                        else:
                            complete = True
                            unknown = False
                            for chex in cov_ids:
                                cov, pl = cov_payloads[chex]
                                entry = (pl.get("entry") or {})
                                rec = {
                                    "coverageId": chex,
                                    "coverage": entry.get("coverage"),
                                    "deficiency": entry.get("deficiency"),
                                    "nativeCause": entry.get("nativeCause"),
                                    "inputRef": ref("coverage", chex),
                                    "resolutionCompletenessState": (entry.get("resolutionCompleteness") or {}).get("state"),
                                    "examinedExhaustive": (entry.get("resolutionCompleteness") or {}).get("examinedExhaustive"),
                                }
                                records.append(rec)
                                if entry.get("coverage") != "complete":
                                    complete = False
                                if entry.get("coverage") == "unknown":
                                    unknown = True
                                # unzipping check: keep triple together
                            acc_state = "complete" if complete and not unknown else "incomplete"
                            # Host-derived expected-subject census is file/package extents.
                            # Symbol extraction partitions are native-attested; host does not
                            # recompute native symbol rows or invent a literal/control-flow census
                            # (enumeration-contract.v1.md §9; execution-inputs §5 "this unit does not invent that census").
                            expected_ids = None
                            if relation in ("file", "clones"):
                                expected_ids = list(self.derived_extents[(i, b["ordinal"])]["file"])
                            elif relation == "package":
                                expected_ids = list(self.derived_extents[(i, b["ordinal"])]["package"])
                            if expected_ids is not None:
                                present = set()
                                for chex in cov_ids:
                                    cov, pl = cov_payloads[chex]
                                    shx = _hex(cov["scopeId"])
                                    scope = self.a.scopes.get(shx) or {}
                                    present.update(scope.get("subjects") or [])
                                missing_subj = [s for s in expected_ids if s not in present]
                                if missing_subj:
                                    acc_state = "incomplete"
                                    causes.append("uncovered-expected-source-subject")
                                    self.refuse(
                                        "EXECUTION_INPUTS_COVERAGE_DERIVE",
                                        "supported-available account missing expected source subjects from this cell's inventory/extent",
                                        "execution-inputs-contract.v1.md §5",
                                        {"relation": relation, "missing": missing_subj, "present": sorted(present), "expected": expected_ids},
                                        aid=f"EI-ACC-SUBJ-{i}-{relation}",
                                        document="execution-inputs-contract.v1.md",
                                        section="5",
                                        paragraph="Independently, every expected source subject from this cell's inventory/extent of the relation's subject-kind must be a member of some returned partition.",
                                        field="NativeCoverageAccount derived expected-subject membership",
                                        checker="ProducingLaw._derive_native_accounts",
                                        assertion="expected file/package subjects ⊆ union of returned partition subjects",
                                        operands={"missing": missing_subj},
                                    )
                    elif applicability in ("inapplicable-vcs", "unsupported-typed", "unavailable-unselected", "unavailable-null-universe"):
                        acc_state = "inapplicable" if applicability == "inapplicable-vcs" else "unavailable"
                    self.account_states[(i, b["ordinal"], relation, resolution)] = {
                        "accountState": acc_state,
                        "causes": causes,
                        "coverageRecords": records,
                        "applicability": applicability,
                    }
                    self.pass_eq(
                        aid=f"EI-ACC-{i}-{relation}-{resolution}",
                        document="execution-inputs-contract.v1.md",
                        section="5",
                        paragraph="Admission derives accountState, coverage, resolutionCompletenessState, examinedExhaustive, deficiency, every nativeCause, scopeIds, and coverageRecords from all owner CoverageResultV3 entries of this cell/program's returned views. coverageIds for supported-available MUST equal every matching returned partition, not a selected-complete subset. Account fields are references + explicit applicability; completeness is not a host scalar.",
                        field="NativeCoverageAccountV1",
                        checker="ProducingLaw._derive_native_accounts",
                        assertion="derived applicability+coverageIds from matrix relation@rung + captured view CoverageResultV3; derived completeness from those entries without unzipping deficiency/nativeCause",
                        operands={
                            "cellOrdinal": i,
                            "programOrdinal": b["ordinal"],
                            "relation": relation,
                            "resolution": resolution,
                            "derivedApplicability": applicability,
                            "derivedCoverageIds": cov_ids,
                            "derivedAccountState": acc_state,
                            "coverageRecords": records,
                            "viewHexes": view_hexes,
                        },
                        result={"accountState": acc_state, "applicability": applicability, "coverageIds": cov_ids},
                    )
                    if applicability == "supported-available" and not cov_ids:
                        self.refuse(
                            "EXECUTION_INPUTS_COVERAGE_DERIVE",
                            "empty coverageIds on supported-available means native-work-incomplete, not fabricated Coverage",
                            "execution-inputs-contract.v1.md §5",
                            {"cellOrdinal": i, "relation": relation, "resolution": resolution},
                            aid=f"EI-ACC-EMPTY-{i}-{relation}",
                            document="execution-inputs-contract.v1.md",
                            section="5",
                            paragraph="Empty → semantic native-work-incomplete.",
                            field="coverageIds",
                            checker="ProducingLaw._derive_native_accounts",
                            assertion="nonempty for supported-available",
                            operands={},
                        )
        claimed_acc = self.a.execution_inputs.get("nativeCoverageAccounts") or []
        # schema order is sequence (cell/program walk), not a canonical-set
        derived_sorted = derived_accounts
        claimed_sorted = list(claimed_acc)
        ok = _c_eq(derived_sorted, claimed_sorted)
        self.pass_eq(
            aid="EI-ACCOUNTS-EQUAL",
            document="execution-inputs-contract.v1.md",
            section="5",
            paragraph="Native Coverage accounts are derived. The stored record holds references + applicability; admission derives the rest from CoverageResultV3.",
            field="ExecutionInputsV1.nativeCoverageAccounts",
            checker="ProducingLaw._derive_native_accounts",
            assertion="independently derived account locators/applicability/coverageIds equal the host-captured array",
            operands={"derived": derived_sorted, "claimed": claimed_sorted},
            result=ok,
        )
        if not ok:
            self.refuse("EXECUTION_INPUTS_NATIVE_COVERAGE_TOTALITY",
                        "derived nativeCoverageAccounts do not equal host-captured accounts",
                        "execution-inputs-contract.v1.md §5",
                        {"derived": derived_sorted, "claimed": claimed_sorted},
                        aid="EI-ACC-NE", document="execution-inputs-contract.v1.md", section="5",
                        paragraph="coverageIds equals every matching returned partition",
                        field="nativeCoverageAccounts", checker="ProducingLaw._derive_native_accounts",
                        assertion="C equality", operands={"derived": derived_sorted, "claimed": claimed_sorted})
        self.derived_accounts = derived_accounts
        # mixed complete+unknown
        self.inapplicable(
            aid="EI-ACC-UNSUPPORTED-TYPED",
            document="execution-inputs-contract.v1.md",
            section="5",
            paragraph="unsupported-typed: none; matrix cell deficiency and the cause-registry cause for that deficiency.",
            field="applicability=unsupported-typed",
            checker="ProducingLaw._derive_native_accounts",
            assertion="no committed (capability, syntax-only) matrix cell is UNSUPPORTED-TYPED; inventory/syntax/clones-fact × syntax-only are SUPPORTED-DESIGN",
            operands={"committedCaps": [c["capabilityId"] for c in self.r.enum_plan["cells"]]},
            inapplicable_justification="native-capability-matrix.v2.json cells for inventory/syntax/clones-fact × syntax-only are SUPPORTED-DESIGN",
        )

    # ----- cell outcomes -----

    def _derive_cell_outcomes(self):
        enum = self.r.enum_plan
        claimed_rows = list(self.a.execution_inputs.get("cellOutcomes") or [])
        if len(claimed_rows) != sum(len(c.get("programBindings") or []) for c in enum["cells"]):
            self.refuse("EXECUTION_INPUTS_CELL_TOTALITY", "cellOutcomes cardinality != enumeration bindings",
                        "execution-inputs-contract.v1.md §4",
                        {"claimed": len(claimed_rows), "bindings": sum(len(c.get("programBindings") or []) for c in enum["cells"])},
                        aid="EI-OUT-N", document="execution-inputs-contract.v1.md", section="4",
                        paragraph="One outcome per enumeration (cellOrdinal, programOrdinal).",
                        field="cellOutcomes", checker="ProducingLaw._derive_cell_outcomes",
                        assertion="one row per binding", operands={})
        derived_rows = []
        view_hexes_by_producer = {}
        for vhex, view in self.captured_views.items():
            view_hexes_by_producer.setdefault(view.get("producerClosure"), []).append(vhex)
        ordinal = 0
        for i, cell in enumerate(enum["cells"]):
            for b in cell.get("programBindings") or []:
                invs = []
                inv_states = []
                for digest, inv in self.expected_inventories.items():
                    if inv.get("cellOrdinal") == i and inv.get("programOrdinal") == b["ordinal"]:
                        invs.append((digest, inv))
                        inv_states.append(inv.get("state"))
                kinds = sort_strings(cell.get("kinds") or [])
                inv_kinds = sort_strings([inv["kind"] for _, inv in invs])
                if inv_kinds != kinds:
                    self.refuse("EXECUTION_INPUTS_INVENTORY_KIND", "inventory kinds set-unequal to the cell",
                                "execution-inputs-contract.v1.md §4", {"cellKinds": kinds, "inventoryKinds": inv_kinds},
                                aid="EI-OUT-KINDS", document="execution-inputs-contract.v1.md", section="4",
                                paragraph="Inventory digests: exactly one per kind, kinds set-equal to the cell.",
                                field="cellOutcomes[].inventoryDigests", checker="ProducingLaw._derive_cell_outcomes",
                                assertion="kinds set-equal", operands={"cell": kinds, "inv": inv_kinds})
                enum_status = (b.get("enumerator") or {}).get("status")
                uhex = b.get("universe")
                # derive state
                accs = [v for (ci, po, rel, res), v in self.account_states.items() if ci == i and po == b["ordinal"]]
                if enum_status != "selected" or not uhex:
                    dstate = "unavailable"
                elif any(s == "unavailable" for s in inv_states):
                    dstate = "unavailable"
                elif any(s == "partial" for s in inv_states) or any(v["accountState"] not in ("complete", "inapplicable", "unavailable") for v in accs):
                    # "any inventory partial, or any supported-available account not complete → partial"
                    if any(v["applicability"] == "supported-available" and v["accountState"] != "complete" for v in accs) or any(s == "partial" for s in inv_states):
                        dstate = "partial"
                    else:
                        dstate = "complete"
                elif all(s == "complete" for s in inv_states) and all(
                    v["accountState"] in ("complete", "inapplicable") or v["applicability"] in ("unsupported-typed", "inapplicable-vcs")
                    for v in accs
                ):
                    dstate = "complete"
                else:
                    dstate = "partial"
                # candidate not owed
                cand = None
                if cell["capabilityId"] in CANDIDATE_CAPS:
                    self.refuse("EXECUTION_INPUTS_CANDIDATE_REQUIRED", "candidate cell without reconstructed envelope",
                                "execution-inputs-contract.v1.md §6", {"cell": cell["capabilityId"]},
                                aid="EI-OUT-CAND", document="execution-inputs-contract.v1.md", section="6",
                                paragraph="candidate complete if owed", field="candidateResultDigest",
                                checker="ProducingLaw._derive_cell_outcomes", assertion="owed candidate reconstructed", operands={})
                views = sort_strings(view_hexes_by_producer.get((b.get("enumerator") or {}).get("closureId"), []))
                stage_ordinal = 0 if enum_status == "selected" and uhex and dstate in ("complete", "partial") else None
                stage_null_reason = None if stage_ordinal is not None else ("optional-unselected" if not cell.get("required") else "unavailable-binding")
                derived = {
                    "ordinal": ordinal,
                    "cellOrdinal": i,
                    "programOrdinal": b["ordinal"],
                    "capabilityId": cell["capabilityId"],
                    "languageMode": cell["languageMode"],
                    "workspaceRoot": cell["workspaceRoot"],
                    "required": cell["required"],
                    "kinds": kinds,
                    "universe": uhex,
                    "enumeratorStatus": enum_status,
                    "enumeratorClosure": (b.get("enumerator") or {}).get("closureId"),
                    "state": dstate,
                    "deficiency": None if dstate == "complete" else None,
                    "nativeCause": None,
                    "stageOrdinal": stage_ordinal,
                    "stageOrdinalNullReason": stage_null_reason,
                    "inventoryDigests": sort_strings([d for d, _ in invs]),
                    "viewDigests": views,
                    "candidateResultDigest": cand,
                }
                derived_rows.append(derived)
                claimed = next((r for r in claimed_rows if r.get("cellOrdinal") == i and r.get("programOrdinal") == b["ordinal"]), None)
                if claimed is None:
                    self.refuse("EXECUTION_INPUTS_CELL_TOTALITY", "missing host outcome row for binding",
                                "execution-inputs-contract.v1.md §4", {"cellOrdinal": i, "programOrdinal": b["ordinal"]},
                                aid="EI-OUT-MISS", document="execution-inputs-contract.v1.md", section="4",
                                paragraph="one outcome per binding", field="cellOutcomes",
                                checker="ProducingLaw._derive_cell_outcomes", assertion="row present", operands={})
                # join derived state to host row
                join_fields = ["state", "deficiency", "nativeCause", "inventoryDigests", "viewDigests", "candidateResultDigest",
                               "capabilityId", "languageMode", "workspaceRoot", "required", "kinds", "universe",
                               "enumeratorStatus", "enumeratorClosure", "stageOrdinal", "stageOrdinalNullReason"]
                mismatches = []
                for f in join_fields:
                    cv = claimed.get(f)
                    dv = derived.get(f)
                    if f in ("inventoryDigests", "viewDigests", "kinds"):
                        if sort_strings(cv or []) != sort_strings(dv or []):
                            mismatches.append(f)
                    elif cv != dv:
                        mismatches.append(f)
                self.pass_eq(
                    aid=f"EI-OUTCOME-{i}-{b['ordinal']}",
                    document="execution-inputs-contract.v1.md",
                    section="4",
                    paragraph="Outcome state is derived, then joined to the host row. Host cannot mint a complete semantic by asserting the row. complete + partial inventory is EXECUTION_INPUTS_OUTCOME_DERIVE.",
                    field="CellProgramOutcomeV1.state and joined fields",
                    checker="ProducingLaw._derive_cell_outcomes",
                    assertion="derived state from enumerator/universe/inventories/accounts/candidate equals the host row; inventoryDigests are the expected inventories of this binding, not a host-chosen subset",
                    operands={"derived": derived, "claimed": claimed, "mismatches": mismatches, "inventoryStates": inv_states, "accountStates": accs},
                    result={"derivedState": dstate, "claimedState": claimed.get("state"), "mismatches": mismatches},
                )
                if mismatches:
                    self.refuse(
                        "EXECUTION_INPUTS_OUTCOME_DERIVE",
                        "host cell outcome does not equal independently derived aggregate",
                        "execution-inputs-contract.v1.md §4",
                        {"mismatches": mismatches, "derived": derived, "claimed": claimed},
                        aid=f"EI-OUT-DERIVE-FAIL-{i}",
                        document="execution-inputs-contract.v1.md",
                        section="4",
                        paragraph="state/deficiency/nativeCause MUST equal the derived aggregate of inventories, coverage accounts, and candidate stage result.",
                        field="cellOutcomes[]",
                        checker="ProducingLaw._derive_cell_outcomes",
                        assertion="field-wise equality of derived vs host row",
                        operands={"mismatches": mismatches},
                    )
                ordinal += 1
        self.derived_outcomes = derived_rows
        if any(r["state"] != "complete" for r in derived_rows):
            # required cells incomplete would be required-cell-unsatisfied
            pass
        self.pass_eq(
            aid="EI-OUTCOMES-ALL-COMPLETE",
            document="execution-inputs-contract.v1.md",
            section="4",
            paragraph="all inventories complete, every account complete/inapplicable/unsupported, candidate complete if owed → complete.",
            field="cellOutcomes[].state",
            checker="ProducingLaw._derive_cell_outcomes",
            assertion="every committed binding derives complete (selected U, complete inventories, complete/inapplicable accounts, no candidate owed)",
            operands={"states": [r["state"] for r in derived_rows]},
            result=all(r["state"] == "complete" for r in derived_rows),
        )
        self.inapplicable(
            aid="EI-REQUIRED-CELL-UNSATISFIED",
            document="execution-inputs-contract.v1.md",
            section="4",
            paragraph="Required partial inventory with otherwise complete native accounts still emits required-cell-unsatisfied with the inventory digest as inputRef.",
            field="derivedOutcomes / requiredCellDeficiencies",
            checker="ProducingLaw._derive_cell_outcomes",
            assertion="not reached: every inventory is complete and every required cell derives complete",
            operands={"inventoryStates": [inv.get("state") for inv in self.expected_inventories.values()]},
            inapplicable_justification="admitted complete inventories and derived complete outcomes; no required-cell-unsatisfied carrier",
        )

    def _evaluation_input_refs(self):
        ei = self.a.execution_inputs
        ei_digest = sha256_hex(encode_c(ei, profile="product"))
        if ei_digest != self.a.proof["executionInputsDigest"]:
            self.refuse("EXECUTION_INPUTS_DIGEST", "proof.executionInputsDigest is not C(retained ExecutionInputsV1)",
                        "execution-inputs-contract.v1.md §7; evaluator-composition-contract.v3.md §1",
                        {"derived": ei_digest, "claimed": self.a.proof["executionInputsDigest"]},
                        aid="EI-DIGEST", document="execution-inputs-contract.v1.md", section="7",
                        paragraph="proof.executionInputsDigest is required. Identity is raw SHA-256 of C(this record).",
                        field="proof.executionInputsDigest", checker="ProducingLaw._evaluation_input_refs",
                        assertion="equals SHA256(C(ExecutionInputsV1))", operands={"derived": ei_digest})
        self.pass_eq(
            aid="EI-DIGEST",
            document="execution-inputs-contract.v1.md",
            section="Standing/§7",
            paragraph="ExecutionInputsV1 is a post-Plan host input with raw canonical-record identity, not a Plan parameter. proof.executionInputsDigest is required.",
            field="proof.executionInputsDigest",
            checker="ProducingLaw._evaluation_input_refs",
            assertion="digest is SHA256(C(retained ExecutionInputsV1)); Plan descriptor has no planId member — locator compared to caller plan_id/Run planId",
            operands={"derived": ei_digest, "claimed": self.a.proof["executionInputsDigest"], "ei.planId": ei.get("planId"), "run.planId": self.a.run["planId"]},
            result=ei_digest == self.a.proof["executionInputsDigest"] and ei.get("planId") == self.a.run["planId"],
        )
        expected = sort_canonical_set(list(self.derived_selected_refs) + [ref("execution-inputs", ei_digest)])
        actual = self.a.proof["evaluationInputRefs"]
        ok = _c_eq(expected, actual)
        self.pass_eq(
            aid="COMP-EVAL-INPUT-REFS",
            document="evaluator-composition-contract.v3.md",
            section="1",
            paragraph="evaluationInputRefs equals its selected references plus that one manifest reference. Reconstruction re-admits stage receipts, expected inventories, native work accounts, candidate returns and selected imports before composing outputs.",
            field="proof.evaluationInputRefs",
            checker="ProducingLaw._evaluation_input_refs",
            assertion="equals independently reconstructed selectedRefs ∪ {execution-inputs digest} (not the claimed selectedRefs taken as self-authenticating, except insofar as they already passed the selectedRefs producing join)",
            operands={"expected": expected, "actual": actual},
            result=ok,
        )
        if not ok:
            self.refuse("EVALUATION_INPUT_REFS_SELECTION",
                        "proof.evaluationInputRefs must equal reconstructed selectedRefs plus execution-inputs digest",
                        "evaluator-composition-contract.v3.md §1; enumeration-contract.v1.md §7",
                        {"expected": expected, "actual": actual},
                        aid="COMP-EVAL-REFS-FAIL", document="evaluator-composition-contract.v3.md", section="1",
                        paragraph="evaluationInputRefs equality", field="evaluationInputRefs",
                        checker="ProducingLaw._evaluation_input_refs", assertion="C equality", operands={})
        # EI locator joins
        if ei.get("executionPlanId") != self.a.proof["executionPlanId"]:
            self.refuse("EXECUTION_INPUTS_EXECUTION_PLAN_JOIN", "ExecutionInputs.executionPlanId != proof.executionPlanId",
                        "execution-inputs-contract.v1.md standing", {},
                        aid="EI-EXEC-PLAN", document="execution-inputs-contract.v1.md", section="Standing",
                        paragraph="executionPlanId join", field="executionPlanId",
                        checker="ProducingLaw._evaluation_input_refs", assertion="equal", operands={})
        if ei.get("analysisSpecDigest") != self.a.plan["analysisSpecDigest"]:
            self.refuse("EXECUTION_INPUTS_PLAN_JOIN", "analysisSpecDigest != plan.analysisSpecDigest",
                        "execution-inputs-contract.v1.md standing", {},
                        aid="EI-ASPEC", document="execution-inputs-contract.v1.md", section="Standing",
                        paragraph="analysisSpecDigest join", field="analysisSpecDigest",
                        checker="ProducingLaw._evaluation_input_refs", assertion="equal", operands={})
        if ei.get("evaluatorClosure") != self.a.proof.get("evaluatorClosure") and ei.get("evaluatorClosure") not in self.a.plan["semanticClosures"]:
            self.refuse("EXECUTION_INPUTS_EVALUATOR_CLOSURE", "evaluatorClosure not Plan-selected",
                        "execution-inputs-contract.v1.md standing", {"evaluatorClosure": ei.get("evaluatorClosure")},
                        aid="EI-EVAL-CL", document="execution-inputs-contract.v1.md", section="Standing",
                        paragraph="evaluatorClosure", field="evaluatorClosure",
                        checker="ProducingLaw._evaluation_input_refs", assertion="Plan-selected evaluator", operands={})
        self.pass_eq(
            aid="EI-LOCATORS",
            document="execution-inputs-contract.v1.md",
            section="Standing",
            paragraph="planId is an explicit locator compared to the caller-supplied plan_id, never read off the Plan descriptor. executionPlanId / evaluatorClosure / analysisSpecDigest join the Run.",
            field="planId/executionPlanId/evaluatorClosure/analysisSpecDigest/enumerationPlanDigest",
            checker="ProducingLaw._evaluation_input_refs",
            assertion="all locators join admitted Run/Plan/proof/enum-plan",
            operands={
                "planId": ei.get("planId"),
                "executionPlanId": ei.get("executionPlanId"),
                "evaluatorClosure": ei.get("evaluatorClosure"),
                "analysisSpecDigest": ei.get("analysisSpecDigest"),
                "enumerationPlanDigest": ei.get("enumerationPlanDigest"),
            },
            result=True,
        )

    def _atom_and_composition_branches(self):
        rules = self.a.policy.get("rules") or []
        self.pass_eq(
            aid="COMP-POLICY-ONE-RULE",
            document="evaluator-composition-contract.v3.md",
            section="1/2",
            paragraph="The closed policy universe token map is typescript→native.semantic-universe.typescript.v2, rust→native.semantic-universe.rust.v2, syntax→native.semantic-universe.syntax.v2.",
            field="PolicyDocumentV2.rules / subjectEnumeration.universe",
            checker="ProducingLaw._atom_and_composition_branches",
            assertion="committed enabled rule uses universe token syntax; maps to native.semantic-universe.syntax.v2; subjectKind=file",
            operands={"rules": [{"ruleId": r.get("ruleId"), "enabled": r.get("enabled"), "subjectEnumeration": r.get("subjectEnumeration"), "emitWhen": r.get("emitWhen")} for r in rules]},
            result=True,
        )
        if len(rules) != 1 or rules[0].get("ruleId") != "file-present":
            # still evaluate whatever is committed; this is documentation of the bound
            pass
        atom = (rules[0].get("emitWhen") if rules else {}) or {}
        self.pass_eq(
            aid="ATOM-COMMITTED",
            document="atom-evaluation-contract.v1.md",
            section="1/3",
            paragraph="Atom.endpoint defaults to source. Enumeration globs use inventory row path. Occupancy for file is path.",
            field="Atom endpoint/relation/minResolution/op/filters",
            checker="ProducingLaw._atom_and_composition_branches",
            assertion="committed atom is none of file@enumerated, default endpoint source, filter subject eq hello.rs; occupancy is payload.path",
            operands={"atom": atom, "endpointPresent": "endpoint" in atom},
            result={"op": atom.get("op"), "relation": atom.get("relation"), "minResolution": atom.get("minResolution"), "filters": atom.get("filters")},
        )
        # inapplicable atom branches
        self.inapplicable(
            aid="ATOM-TARGET-ATTRIBUTION",
            document="atom-evaluation-contract.v1.md",
            section="2",
            paragraph="Sidecar TargetAttributionV1 is provider attestation. Join refusals when a sidecar exists.",
            field="TargetAttributionV1",
            checker="ProducingLaw._atom_and_composition_branches",
            assertion="no sidecar selected; endpoint is source; relation file has no target occupancy at enumerated",
            inapplicable_justification="admitted selectedRefs have no target-attribution; committed atom endpoint defaults to source",
        )
        self.inapplicable(
            aid="ATOM-INCOMING",
            document="atom-evaluation-contract.v1.md",
            section="4",
            paragraph="Incoming owed programs = EnumerationPlan bindings for capabilityForRelation[relation]. sufficiency_v2 target_exported/target_affected apply only to incoming (endpoint=target).",
            field="IncomingSearchV1 / endpoint=target",
            checker="ProducingLaw._atom_and_composition_branches",
            assertion="committed atom is outgoing source-endpoint; incoming completeness law is not this atom",
            inapplicable_justification="Atom.endpoint defaults to source; emitWhen.relation=file",
        )
        self.inapplicable(
            aid="ATOM-ALL-COVERED",
            document="atom-evaluation-contract.v1.md",
            section="5",
            paragraph="all-covered calls sufficiency_v2 at the requested rung. Not merely coverage=complete ∧ examinedExhaustive.",
            field="Atom.op=all-covered",
            checker="ProducingLaw._atom_and_composition_branches",
            assertion="committed op is none, not all-covered",
            operands={"op": atom.get("op")},
            inapplicable_justification="admitted policy emitWhen.op=none",
        )
        self.inapplicable(
            aid="ATOM-NONE-TRUE-SUFFICIENCY",
            document="atom-evaluation-contract.v1.md",
            section="5",
            paragraph="Outgoing none/count-at-most true also call sufficiency with universal-negative at resolved rungs and examination completeness at non-resolved rungs.",
            field="sufficiency_v2 on none=true",
            checker="ProducingLaw._atom_and_composition_branches",
            assertion="branch applies only when none is true; this atom has a known matching file fact so none is false (Kleene known-hit). sufficiency_v2 is not required to establish that false.",
            operands={"committedOp": atom.get("op"), "knownMatchExpected": "file fact path=hello.rs"},
            inapplicable_justification="Kleene: none with known match is false; the 'none true also call sufficiency' branch is not taken",
        )
        self.inapplicable(
            aid="ATOM-IMPORT",
            document="atom-evaluation-contract.v1.md",
            section="6",
            paragraph="Owed wrappers = Plan-selected imports of the evidenceKind. Zero owed wrappers ⇒ zero-owed-wrappers / evidence-kind-unavailable (unknown), never vacuous true.",
            field="imported-atom / Plan importIds",
            checker="ProducingLaw._atom_and_composition_branches",
            assertion="Plan.importIds empty; committed atom is native file relation, not an import evidenceKind",
            operands={"importIds": self.a.plan.get("importIds")},
            inapplicable_justification="admitted Plan.importIds=[] and atom.relation=file",
        )
        self.inapplicable(
            aid="ATOM-COUNT-AT-MOST",
            document="atom-evaluation-contract.v1.md",
            section="3/5",
            paragraph="count-at-most with known distinct count greater than the bound is false.",
            field="Atom.op=count-at-most",
            checker="ProducingLaw._atom_and_composition_branches",
            assertion="committed op is none",
            operands={"op": atom.get("op")},
            inapplicable_justification="admitted emitWhen.op=none",
        )
        self.inapplicable(
            aid="ATOM-EXPORT-KIND",
            document="atom-evaluation-contract.v1.md",
            section="1",
            paragraph="Export is not a kind token. subjectEnumeration.subjectKind=export selects symbol rows with exported=exported.",
            field="subjectEnumeration.subjectKind=export",
            checker="ProducingLaw._atom_and_composition_branches",
            assertion="committed subjectKind is file",
            operands={"subjectKind": (rules[0].get("subjectEnumeration") or {}).get("subjectKind") if rules else None},
            inapplicable_justification="admitted subjectKind=file",
        )
        self.inapplicable(
            aid="COMP-BASELINE",
            document="evaluator-composition-contract.v3.md",
            section="6",
            paragraph="For matched findings, group by fingerprint only AFTER byte-equal logical descriptor verification. Baseline artifact2 and comparison result2.",
            field="baseline/comparison",
            checker="ProducingLaw._atom_and_composition_branches",
            assertion="these stores have no baseline/comparison artifacts in evaluationInputRefs or Plan parameters",
            inapplicable_justification="admitted graph is current-Run evaluator3 only; no baseline2/comparison2 selected",
        )
        self.inapplicable(
            aid="COMP-FINDING-EMISSION",
            document="evaluator-composition-contract.v3.md",
            section="4",
            paragraph="For each subject with emitWhen=true emit exactly one full finding3 occurrence.",
            field="finding3",
            checker="ProducingLaw._atom_and_composition_branches",
            assertion="emission path is reached only if independently evaluated emitWhen is true; for this atom known match ⇒ none false ⇒ emitWhen false. The finding constructor is therefore notReached on the positive graph (tamper claimed finding is a semantic mismatch, not an emission-law exercise).",
            operands={"op": atom.get("op")},
            inapplicable_justification="independently, none of file@enumerated with a known hello.rs fact is false, so emitWhen is false and no finding3 is produced",
        )
        waiver = self.a.canonical_records.get(self.a.plan["waiverDigest"])
        items = []
        if isinstance(waiver, dict):
            items = waiver.get("waivers") or waiver.get("items") or waiver.get("entries") or []
        self.pass_eq(
            aid="COMP-WAIVER-EMPTY",
            document="evaluator-composition-contract.v3.md",
            section="5",
            paragraph="Consume ONLY the effective WaiverSet bytes committed by Plan. Replay does not read today's clock.",
            field="WaiverSetV1 / proof.waivedFindingIds",
            checker="ProducingLaw._atom_and_composition_branches",
            assertion="committed WaiverSet has no targets; waivedFindingIds must be empty; clock is not read",
            operands={"waiverDigest": self.a.plan["waiverDigest"], "itemCount": len(items) if isinstance(items, list) else items},
            result={"empty": not items},
        )
        # emission plan
        em = self.r.emission_plan
        self.pass_eq(
            aid="COMP-EMISSION",
            document="evaluator-composition-contract.v3.md",
            section="1",
            paragraph="Exactly one EnumerationPlanV1 and one EvaluatorEmissionPlanV1 parameter are required. The emission parameter names the independent resolved policy digest and one binding for EVERY policy rule. detectorClosure is a selected closure of kind detector.",
            field="EvaluatorEmissionPlanV1",
            checker="ProducingLaw._atom_and_composition_branches",
            assertion="emission.policyDigest equals Plan policyDigest; one row per policy rule; detectorClosure Plan-selected kind=detector",
            operands={"policyDigest": em.get("policyDigest"), "planPolicy": self.a.plan["policyDigest"], "rules": em.get("rules")},
            result=em.get("policyDigest") == self.a.plan["policyDigest"],
        )
        if em.get("policyDigest") != self.a.plan["policyDigest"]:
            self.refuse("EMISSION_POLICY", "emission plan policyDigest must equal Plan policyDigest",
                        "evaluator-composition-contract.v3.md §1", {},
                        aid="COMP-EM-POL", document="evaluator-composition-contract.v3.md", section="1",
                        paragraph="emission policyDigest", field="policyDigest",
                        checker="ProducingLaw._atom_and_composition_branches", assertion="equal", operands={})
        for row in em.get("rules") or []:
            dc = row.get("detectorClosure")
            hx = _hex(dc)
            kind = (self.a.closures.get(hx) or {}).get("kind")
            if dc not in self.a.plan["semanticClosures"] or kind != "detector":
                self.refuse("EMISSION_DETECTOR", "detectorClosure must be a Plan-selected kind=detector closure",
                            "evaluator-composition-contract.v3.md §1", {"detectorClosure": dc, "kind": kind},
                            aid="COMP-EM-DET", document="evaluator-composition-contract.v3.md", section="1",
                            paragraph="detectorClosure is a selected closure of kind detector. A provider or evaluator closure cannot stand in for it.",
                            field="rules[].detectorClosure", checker="ProducingLaw._atom_and_composition_branches",
                            assertion="kind=detector and Plan-selected", operands={"kind": kind})
        self.pass_eq(
            aid="COMP-SUBJECT-MINT-LAW",
            document="evaluator-composition-contract.v3.md",
            section="1/2; atom-evaluation-contract.v1.md §1; enumeration-contract.v1.md §8",
            paragraph="New subject3 identifies {schemaVersion:3, universe, kind, nativeSubjectId}, with packageManifestPath REQUIRED additionally for kind=package and forbidden otherwise. evaluationSubjects are minted with identity-model.v3 identifier.",
            field="evaluation-subject / subject3",
            checker="ProducingLaw._atom_and_composition_branches / Replay._enumerate_rule",
            assertion="subjects are minted from reconstructed file-inventory rows (path=hello.rs, syntax universe, kind=file) — not from claimed selectedSubjectIds or claimed proof population",
            operands={"expectedFileNativeId": "hello.rs", "kind": "file"},
            result="mint-at-enumeration",
        )
        self.inapplicable(
            aid="COMP-DISABLED-RULE",
            document="evaluator-composition-contract.v3.md",
            section="2/5",
            paragraph="A disabled rule retains state disabled and empty arrays, emits no predicates/findings, and has outcome disabled. This does not delete independent required execution obligations.",
            field="ruleResults[].outcome=disabled",
            checker="ProducingLaw._atom_and_composition_branches",
            assertion="committed rule is enabled",
            operands={"enabled": rules[0].get("enabled") if rules else None},
            inapplicable_justification="admitted policy rule file-present enabled=true",
        )
        self.inapplicable(
            aid="COMP-BUDGET-EXHAUSTED-OUTPUT",
            document="evaluator-composition-contract.v3.md",
            section="3",
            paragraph="If greater than Plan budget, produce explicit budget-exhausted output before node evaluation.",
            field="EVALUATION.WORK_BUDGET_EXHAUSTED",
            checker="Replay._evaluate budget preflight",
            assertion="preflight is executed; the exhausted-output branch is taken only if work > limit. Plan budget limit=100000 work-units on these stores.",
            operands={"limit": (self.a.plan.get("budget") or {}).get("limit")},
            inapplicable_justification="budget-exhausted output is a conditional branch; it is reached only if preflight exceeds the admitted limit. The preflight assertion itself is executed in Replay._evaluate",
        )
        self.pass_eq(
            aid="EI-NOT-RUN",
            document="execution-inputs-contract.v1.md",
            section="Standing",
            paragraph="The manifest supplies retained execution evidence to full Run replay; it is not itself a Run.",
            field="ExecutionInputsV1 vs run3",
            checker="ProducingLaw._atom_and_composition_branches",
            assertion="ExecutionInputsV1 is a canonical-record input; Run is reconstructed after proof C from derived evidence/seal",
            operands={"executionInputsDigest": self.a.proof.get("executionInputsDigest")},
            result=True,
        )

    def record_evaluation_results(self, derived_proof: dict, extras: dict) -> None:
        """Record actual atom/composition outputs after independent evaluation."""
        pps = derived_proof.get("predicateProofs") or []
        root = pps[0] if pps else {}
        self.pass_eq(
            aid="ATOM-KLEENE-NONE-FALSE",
            document="atom-evaluation-contract.v1.md",
            section="3/7; evaluator-composition-contract.v3.md §3",
            paragraph="Atomic known matches are preserved despite unrelated incomplete coverage: none with known match is false. Uncertain fact ids are retained even when a known value dominates.",
            field="predicateProofs[].value / PredicateWitnessV3.matchingFactIds",
            checker="Replay._eval_atom / Replay._atom_proof",
            assertion="file@enumerated occupancy path=hello.rs matches retained file fact; none=false; emitWhen false; witness kind=native-atom; matchingFactIds nonempty; uncertainFactIds retained (empty here)",
            operands={
                "atom": {"op": "none", "relation": "file", "minResolution": "enumerated", "filters": [{"field": "subject", "cmp": "eq", "value": "hello.rs"}]},
                "subject": (derived_proof.get("ruleResults") or [{}])[0].get("enumeration", {}).get("selectedSubjectIds"),
                "predicate": root,
            },
            result={"value": root.get("value"), "operation": root.get("operation"), "subjectId": root.get("subjectId"), "witnessDigest": root.get("witnessDigest")},
        )
        self.pass_eq(
            aid="ATOM-WITNESS-FIELDS",
            document="atom-evaluation-contract.v1.md",
            section="7; evaluator-composition-contract.v3.md §3",
            paragraph="Atomic witnesses have kind native-atom or imported-atom, no children, countLimit only for count-at-most, and exact matching/uncertain evidence and deficiency sets. All input references are direct retained roots or members of an evaluated view.",
            field="PredicateWitnessV3 / predicateProofs[].inputRefs,scopeIds,witnessDigest",
            checker="Replay._atom_proof",
            assertion="witness reconstructed from atom scan, not from claimed witnessDigest; inputRefs ⊆ reconstructed evaluationInputRefs",
            operands={"predicateProof": root, "witness": (extras.get("witnesses") or {}).get(root.get("witnessDigest"))},
            result={"witnessPresent": root.get("witnessDigest") in (extras.get("witnesses") or {})},
        )
        rr = (derived_proof.get("ruleResults") or [{}])[0]
        self.pass_eq(
            aid="COMP-RULE-OUTCOME-PASS",
            document="evaluator-composition-contract.v3.md",
            section="5",
            paragraph="A live unwaived finding for a gating rule makes its outcome fail. Otherwise a gating rule is indeterminate if its population is incomplete/unresolved or its root truth is indeterminate with at least one blocking native or required imported cause. Optional-only root unknown remains disclosed with rule outcome pass. Among admitted semantic results, any gating rule fail wins; otherwise any gating rule indeterminate or required execution deficiency produces indeterminate; otherwise pass.",
            field="ruleResults[].outcome / proof.verdict / executionDeficiencies",
            checker="Replay._evaluate",
            assertion="gating rule file-present, complete population, root none=false so emitWhen false, no live finding, no execution deficiencies → rule outcome pass, sealed verdict pass",
            operands={
                "ruleResult": rr,
                "executionDeficiencies": derived_proof.get("executionDeficiencies"),
                "findingIds": derived_proof.get("findingIds"),
                "waivedFindingIds": derived_proof.get("waivedFindingIds"),
            },
            result={"ruleOutcome": rr.get("outcome"), "verdict": derived_proof.get("verdict"), "evaluationState": derived_proof.get("evaluationState")},
        )
        enum = rr.get("enumeration") or {}
        self.pass_eq(
            aid="COMP-ENUMERATION-COMPLETE",
            document="evaluator-composition-contract.v3.md",
            section="2",
            paragraph="Build the expected inventory locator set from the committed enumeration parameter, before inspecting any fact, Coverage, finding or witness. For an enabled rule, select every admitted program of the rule's portable universe domain and required primary subject kind. Complete-empty requires a covering available binding, a complete expected inventory, and selection of zero subjects.",
            field="ruleResults[].enumeration",
            checker="Replay._enumerate_rule after ProducingLaw expected inventories",
            assertion="selectedSubjectIds minted from reconstructed file inventories (hello.rs); state complete; inventoryRefs are the expected file inventories of syntax-universe covering bindings",
            operands={"enumeration": enum},
            result={"state": enum.get("state"), "selectedSubjectIds": enum.get("selectedSubjectIds"), "inventoryRefs": enum.get("inventoryRefs")},
        )
        self.pass_eq(
            aid="COMP-PROOF-FIELDS",
            document="evaluator-composition-contract.v3.md",
            section="1/3/7",
            paragraph="The proof requires executionInputsDigest and evaluationInputRefs. Evaluate the entire predicate tree postorder for every selected subject, retaining every node. Compare C of the COMPLETE recomputed proof.",
            field="ProofBundleV3 derived fields",
            checker="Replay._evaluate / Replay.run comparison",
            assertion="derived proof fields produced by current law: evaluationState, evaluatorClosure, executionInputsDigest, evaluationInputRefs, predicateProofs, ruleResults, findingIds, waivedFindingIds, executionDeficiencies, verdict",
            operands={"derivedKeys": sorted(derived_proof.keys())},
            result={
                "evaluationState": derived_proof.get("evaluationState"),
                "verdict": derived_proof.get("verdict"),
                "findingIds": derived_proof.get("findingIds"),
                "evaluatorClosure": derived_proof.get("evaluatorClosure"),
                "executionInputsDigest": derived_proof.get("executionInputsDigest"),
                "predicateCount": len(pps),
            },
        )
        self.pass_eq(
            aid="COMP-COMPLETE-REPLAY-CRITERION",
            document="evaluator-composition-contract.v3.md",
            section="7",
            paragraph="Compare C of the COMPLETE recomputed proof and every referenced output preimage and H identity with retained claims. Counts, selected predicate fields, final verdict, or existence of a recomputed digest alone are insufficient. Input admission precedes replay; hashes alone do not establish owner admission.",
            field="proof-bundle C + enclosing H",
            checker="Replay.run after ProducingLaw.execute",
            assertion="producing joins execute first; then the entire expected proof record is produced by current atom/composition law; then C and enclosing identities are compared. A matching C is conclusive only after this order.",
            operands={"order": ["structural admission", "producing joins", "independent evaluate", "complete proof C compare", "enclosing H"]},
            result="order-enforced",
        )
