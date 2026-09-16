"""Private probe: selected admit/commitment vs descriptor-construction. Not product code."""
from pathlib import Path
import hashlib, json, types, traceback

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
SELECTED_NATIVE = (
    ARCH
    / "docs/implementation/m2/capability-totality-reference-selection-v1/reference/native_evidence_model.py"
)
HISTORICAL = (
    ARCH / "docs/coop/design-corrections/native/native_evidence_model.v2.py"
)
HEX = "0" * 64
SNAP = "snapshot2:" + HEX
CLOS = "closure2:" + HEX


def load_native():
    src = SELECTED_NATIVE.read_bytes()
    m = types.ModuleType("native_commitment_probe")
    m.__file__ = str(HISTORICAL)
    exec(compile(src, str(SELECTED_NATIVE), "exec"), m.__dict__)
    return m


def scope(relation, resolution, subjects):
    return {
        "schemaVersion": 2,
        "snapshotId": SNAP,
        "sourceUniverse": HEX,
        "targetUniverse": HEX,
        "relation": relation,
        "resolution": resolution,
        "enumeratorClosure": CLOS,
        "subjects": subjects,
    }


def closed_world():
    return {
        "deadCodeRepairEligible": False,
        "dynamicDispatch": "not-applicable",
        "entryPointsRecognized": "none",
        "exportsClosed": "unknown",
        "externalConsumers": "unknown",
        "nonliteralLoading": "none",
        "reasons": [],
    }


def payload(relation, resolution, commitment, count):
    return {
        "schemaVersion": 3,
        "key": {
            "relation": relation,
            "resolution": resolution,
            "sourceUniverse": HEX,
            "targetUniverse": HEX,
            "subjectScopeCommitment": commitment,
        },
        "entry": {
            "relation": relation,
            "resolution": resolution,
            "coverage": "unknown",
            "deficiency": None,
            "nativeCause": None,
            "derivationKinds": [],
            "confidenceMillionths": 0,
            "examinedUniverse": {
                "subjectScopeCommitment": commitment,
                "subjectCount": count,
            },
            "resolutionCompleteness": {
                "state": "not-applicable",
                "attempted": False,
                "examinedExhaustive": False,
                "stageTerminal": None,
                "unresolvedEdgeCount": 0,
                "unresolvedEdgeClasses": [],
            },
            "closedWorld": closed_world(),
        },
    }


def catch(fn):
    try:
        return {"ok": True, "value": fn()}
    except Exception as e:
        return {"ok": False, "type": type(e).__name__, "msg": str(e)}


def main():
    N = load_native()
    print("ladder_unresolved_edge", N.LADDERS.get("unresolved-edge"))
    print(
        "rung_index enumerated",
        N._rung_index("unresolved-edge", "enumerated"),
    )
    print("rung_index observed", N._rung_index("unresolved-edge", "observed"))

    desc = scope("unresolved-edge", "enumerated", ["a.ts"])
    ctor = catch(
        lambda: N.subject_scope_descriptor(
            SNAP, "unresolved-edge", "enumerated", HEX, HEX, CLOS, ["a.ts"]
        )
    )
    ident = catch(lambda: N.subject_scope_identity(desc))
    commit = catch(lambda: N.subject_scope_commitment(desc))
    print("descriptor_ctor", json.dumps(ctor, default=str))
    print("identity", json.dumps(ident, default=str))
    print("commitment", json.dumps(commit, default=str))

    if commit["ok"]:
        c = commit["value"]
        pl = payload(
            "unresolved-edge",
            "enumerated",
            c["subjectScopeCommitment"],
            c["subjectCount"],
        )
        admitted = catch(lambda: N.admit_coverage_result_v3(pl, desc, []))
        print("admit", json.dumps(admitted, default=str)[:2000])

    dup = scope("unresolved-edge", "enumerated", ["a.ts", "a.ts"])
    print("dup_identity", json.dumps(catch(lambda: N.subject_scope_identity(dup)), default=str))
    print(
        "dup_ctor",
        json.dumps(
            catch(
                lambda: N.subject_scope_descriptor(
                    SNAP, "unresolved-edge", "enumerated", HEX, HEX, CLOS, ["a.ts", "a.ts"]
                )
            ),
            default=str,
        ),
    )
    unordered = scope("unresolved-edge", "enumerated", ["b.ts", "a.ts"])
    print(
        "unordered_identity",
        json.dumps(catch(lambda: N.subject_scope_identity(unordered)), default=str),
    )
    print(
        "unordered_ctor",
        json.dumps(
            catch(
                lambda: N.subject_scope_descriptor(
                    SNAP, "unresolved-edge", "enumerated", HEX, HEX, CLOS, ["b.ts", "a.ts"]
                )
            ),
            default=str,
        ),
    )


if __name__ == "__main__":
    main()
