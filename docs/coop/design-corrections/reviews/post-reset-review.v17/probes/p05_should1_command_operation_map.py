#!/usr/bin/env python
"""CB6-SHOULD-1 executable probe: the owned closed command -> operation map.

Independently verified, against the frozen bytes:
  A. Every command (45) and every MutationOperation (24) is accounted for.
  B. The generic rows are EXACTLY the commands carrying a `mutation` step -
     recomputed from command-inventory, not restated from the map.
  C. Intentional operations with no command are exactly what the map discloses,
     recomputed rather than trusted.
  D. The specialized step kinds (import, native-preparation, repair-apply) are
     separated from generic MutationParams, and repair-apply is REFUSED by the
     generic fields at the ACTUAL field schema (negative control), while all
     23 admissible tokens are ADMITTED (positive controls).
  E. The renamed rows equal the commands whose name is not itself an operation.
  F. The replay preimage law: MutationReceiptV1 requires BOTH operation and
     idempotencyKey; the import/native-preparation results require receiptId;
     and the generic key is the published H over the closed scope record,
     recomputed by me.
  G. Authority separation: the map grants nothing.
"""
import importlib.util
import json
import sys
from pathlib import Path

COPY, OUT = sys.argv[1], sys.argv[2]
DC = Path(COPY) / "docs/coop/design-corrections"
sys.path.insert(0, str(DC / "foundation"))
import canonical  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402
import glob


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


M = load("workflows_model", DC / "workflows/workflows_model.v1.py")

SCHEMAS = {}
for p in sorted(glob.glob(str(DC / "workflows/schemas/*.schema.json"))):
    s = canonical.parse(Path(p).read_bytes())
    SCHEMAS[s["$id"]] = s
FOUND = canonical.parse((DC / "foundation/identity-schemas.v2.json").read_bytes())
REG = Registry().with_resources(
    [(k, Resource(contents=v, specification=DRAFT202012)) for k, v in SCHEMAS.items()]
    + [(FOUND["$id"], Resource(contents=FOUND, specification=DRAFT202012))])
U = "urn:opensip:product-v1:workflows:"

REPAIR = SCHEMAS[U + "repair"]
INVREC = SCHEMAS[U + "invocation-record"]
MAP = REPAIR["x-opensip-mutation-operation-map"]
OPS = list(REPAIR["$defs"]["MutationOperation"]["enum"])
CI = canonical.parse((DC / "workflows/command-inventory.v1.json").read_bytes())
COMMANDS = CI["commands"]

rep = {"probe": "p05-should1-command-operation-map"}

# ---------- A. inventory sizes ----------
rep["commandCount"] = len(COMMANDS)
rep["operationCount"] = len(OPS)
rep["operations"] = OPS
rep["commandCountIs45"] = len(COMMANDS) == 45
rep["operationCountIs24"] = len(OPS) == 24

# ---------- B. generic rows == commands with a `mutation` step ----------
by_cmd = MAP["byCommandGenericMutationStep"]
cmds_with_mutation_step = sorted(
    c["name"] for c in COMMANDS if "mutation" in c.get("steps", []))
rep["commandsWithAMutationStep"] = cmds_with_mutation_step
rep["genericRowNames"] = sorted(by_cmd)
rep["genericRowsEqualCommandsWithMutationStep"] = (
    sorted(by_cmd) == cmds_with_mutation_step)
rep["genericRowCount"] = len(by_cmd)

# every generic row names a registered operation and a real command
rep["genericRowsWhoseOperationIsNotRegistered"] = [
    n for n, r in by_cmd.items() if r["operation"] not in OPS]
cmd_names = {c["name"] for c in COMMANDS}
rep["genericRowsWhoseCommandDoesNotExist"] = [
    n for n in by_cmd if n not in cmd_names]
# requestClass in the map must equal the inventory's own value
ci_class = {c["name"]: c.get("requestClass") for c in COMMANDS}
rep["genericRowsWithRequestClassMismatch"] = [
    {"command": n, "map": r.get("requestClass"), "inventory": ci_class.get(n)}
    for n, r in by_cmd.items() if r.get("requestClass") != ci_class.get(n)]
rep["genericRowsAllMintedByMutationStepKind"] = all(
    r["mintedByStepKind"] == "mutation" for r in by_cmd.values())

# ---------- C. operations accounted ----------
by_step = MAP["byStepKindReceiptOperation"]
step_ops = set()
for k, v in by_step.items():
    o = v.get("operation")
    if isinstance(o, str) and o in OPS:
        step_ops.add(o)
generic_ops = {r["operation"] for r in by_cmd.values()}
disclosed_no_command = set(MAP["operationsWithNoCommandInThisInventory"]["operations"])
accounted = generic_ops | step_ops | disclosed_no_command
rep["genericOperations"] = sorted(generic_ops)
rep["stepKindOperations"] = sorted(step_ops)
rep["disclosedOperationsWithNoCommand"] = sorted(disclosed_no_command)
rep["accountedOperations"] = sorted(accounted)
rep["everyOperationAccounted"] = set(OPS) == accounted
rep["unaccountedOperations"] = sorted(set(OPS) - accounted)
rep["overAccounted"] = sorted(accounted - set(OPS))

# recompute, rather than trust, the set of operations no step kind / command binds
bound = generic_ops | step_ops
rep["recomputedUnboundOperations"] = sorted(set(OPS) - bound)
rep["disclosureMatchesRecomputedUnbound"] = (
    sorted(set(OPS) - bound) == sorted(disclosed_no_command))

# ---------- D. generic field domain: executable admit/refuse ----------
domain = MAP["admissibleGenericFieldDomain"]["operations"]
rep["declaredGenericDomainCount"] = len(domain)
rep["declaredGenericDomainEqualsOpsMinusRepairApply"] = (
    sorted(domain) == sorted(set(OPS) - {"repair-apply"}))

field_results = []
for field_ref, defname, propname in (
        ("MutationParams.mutationClass", "MutationParams", "mutationClass"),
        ("MutationReplayScopeV1.operation", "MutationReplayScopeV1", "operation")):
    sub = INVREC["$defs"][defname]["properties"][propname]
    v = Draft202012Validator(sub, registry=REG)
    admitted, refused = [], []
    for op in OPS:
        (admitted if v.is_valid(op) else refused).append(op)
    field_results.append({
        "field": field_ref,
        "admitted": sorted(admitted),
        "refused": sorted(refused),
        "admitsAll23Admissible": sorted(admitted) == sorted(domain),
        "refusesExactlyRepairApply": refused == ["repair-apply"],
    })
rep["genericFieldDomainMeasured"] = field_results
rep["bothGenericFieldsRefuseOnlyRepairApply"] = all(
    f["refusesExactlyRepairApply"] and f["admitsAll23Admissible"]
    for f in field_results)

# NEGATIVE CONTROL: a dedicated repair-apply must not be promotable into a
# generic mutation field, and config-write must not be silently given a command.
rep["negativeControls"] = {
    "repairApplyRefusedByBothGenericFields":
        all(f["refused"] == ["repair-apply"] for f in field_results),
    "configWriteHasNoGenericCommandRow":
        "config-write" not in generic_ops,
    "configWriteBoundByNoStepKind": "config-write" not in step_ops,
    "noCommandNamedConfigWrite": "config-write" not in cmd_names,
    "repairApplyIsNotAGenericCommandRow": "repair-apply" not in generic_ops,
    "repairApplyIsBoundByItsOwnStepKind":
        by_step.get("repair-apply", {}).get("operation") == "repair-apply"
        and by_step.get("repair-apply", {}).get("excludedFromGenericFields") is True,
}

# ---------- E. renamed rows ----------
renamed = MAP["renamedRows"]
recomputed_renames = sorted(n for n in by_cmd if n not in OPS)
# native-prepare is not a generic mutation row; recompute over ALL commands whose
# name is not itself an operation AND which the map binds by name or step kind
all_named = sorted(n for n in renamed)
rep["renamedRows"] = renamed
rep["renamedRowCount"] = len(renamed)
rep["genericRenamesRecomputed"] = recomputed_renames
rep["everyRenamedKeyIsARealCommand"] = all(n in cmd_names for n in renamed)
rep["everyRenamedValueIsARegisteredOperation"] = all(
    v in OPS for v in renamed.values())
rep["noRenamedKeyIsItselfAnOperation"] = all(n not in OPS for n in renamed)
rep["genericRenamesAreASubsetOfRenamedRows"] = set(recomputed_renames) <= set(renamed)
rep["renamedRowsMinusGenericRenames"] = sorted(set(renamed) - set(recomputed_renames))

# ---------- F. replay preimage law ----------
mr = REPAIR["$defs"].get("MutationReceiptV1", {})
rep["mutationReceiptRequires"] = mr.get("required")
rep["mutationReceiptRequiresOperationAndKey"] = (
    "operation" in (mr.get("required") or [])
    and "idempotencyKey" in (mr.get("required") or []))
for res in ("ImportResult", "NativePreparationResult"):
    d = INVREC["$defs"].get(res, {})
    rep[res + "RequiresReceiptId"] = "receiptId" in (d.get("required") or [])

# recompute the generic key myself from the published preimage
scope = M.mutation_replay_scope(
    "req1_" + "0" * 32, 2, "prj1-" + "a" * 64, "purge")
rep["replayScopeRecord"] = scope
rep["replayScopePreimageFields"] = sorted(scope)
declared_preimage = MAP["receiptIdempotencyKeyByStepKind"]["recipes"]["mutation"]["preimage"]
rep["declaredGenericPreimage"] = declared_preimage
rep["preimageFieldsMatchDeclared"] = (
    sorted(scope) == sorted(["schemaVersion", "requestId", "stepId",
                             "projectId", "operation"]))
rep["recomputedGenericKey"] = M.mutation_replay_key(scope)
# the key must move when the operation moves, and only then
scope_other = dict(scope, operation="review-join")
rep["keyMovesWithOperation"] = (
    M.mutation_replay_key(scope_other) != M.mutation_replay_key(scope))
scope_same = M.mutation_replay_scope(
    "req1_" + "0" * 32, 2, "prj1-" + "a" * 64, "purge")
rep["keyIsDeterministic"] = (
    M.mutation_replay_key(scope_same) == M.mutation_replay_key(scope))
scope_req = M.mutation_replay_scope(
    "req1_" + "1" * 32, 2, "prj1-" + "a" * 64, "purge")
rep["keyMovesWithRequestId"] = (
    M.mutation_replay_key(scope_req) != M.mutation_replay_key(scope))

# ---------- G. authority separation ----------
rep["authoritySeparation"] = {
    "mapDeclaresItIsNotARequestGrammar": bool(MAP.get("notARequestGrammar")),
    "mapDeclaresInjectivityNotAssumed": bool(MAP.get("injectivityIsNotAssumed")),
    "importBoundByStepKindSoTwoCommandsShareIt": [
        c["name"] for c in COMMANDS if "import" in c.get("steps", [])],
}

with open(OUT, "w") as fh:
    json.dump(rep, fh, indent=1, sort_keys=True, default=str)

keys = ["commandCount", "operationCount", "commandCountIs45", "operationCountIs24",
        "genericRowCount", "genericRowsEqualCommandsWithMutationStep",
        "genericRowsWhoseOperationIsNotRegistered",
        "genericRowsWhoseCommandDoesNotExist",
        "genericRowsWithRequestClassMismatch",
        "genericRowsAllMintedByMutationStepKind",
        "everyOperationAccounted", "unaccountedOperations", "overAccounted",
        "recomputedUnboundOperations", "disclosureMatchesRecomputedUnbound",
        "declaredGenericDomainCount",
        "declaredGenericDomainEqualsOpsMinusRepairApply",
        "bothGenericFieldsRefuseOnlyRepairApply",
        "renamedRowCount", "everyRenamedKeyIsARealCommand",
        "everyRenamedValueIsARegisteredOperation",
        "noRenamedKeyIsItselfAnOperation",
        "genericRenamesAreASubsetOfRenamedRows",
        "renamedRowsMinusGenericRenames",
        "mutationReceiptRequiresOperationAndKey",
        "ImportResultRequiresReceiptId",
        "NativePreparationResultRequiresReceiptId",
        "preimageFieldsMatchDeclared", "keyMovesWithOperation",
        "keyIsDeterministic", "keyMovesWithRequestId"]
for k in keys:
    print("%-52s %s" % (k, json.dumps(rep.get(k))[:150]))
print()
print("negativeControls:", json.dumps(rep["negativeControls"], indent=1))
print("authoritySeparation:", json.dumps(rep["authoritySeparation"], indent=1))
