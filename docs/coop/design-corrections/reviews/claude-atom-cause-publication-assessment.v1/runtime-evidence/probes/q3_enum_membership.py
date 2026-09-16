"""Test the published discriminator: 'Native deficiencies from sufficiency_v2 stay in
nativeDeficiencies and use DeficiencyV2 membership; they are NOT overloaded here [AtomCauseCodeV1]'.

If a code is in BOTH DeficiencyV2 and AtomCauseCodeV1, the discriminator does not partition it.
READ-ONLY, normative JSON only.
"""
import json
from pathlib import Path

S = Path("/tmp/opensip-design-corrections/candidate-subject.v33/docs/coop/design-corrections")

proj = json.loads((S / "foundation/evaluator-projection-registry.v1.json").read_text())
nat = json.loads((S / "native/native-evidence.schemas.v2.json").read_text())
ident = json.loads((S / "foundation/identity-schemas.v3.json").read_text())

atom_enum = proj["$defs"]["AtomCauseCodeV1"]["enum"]
atom_desc = proj["$defs"]["AtomCauseCodeV1"].get("description")
defv2 = nat["$defs"]["DeficiencyV2"]["enum"]
nativecause = nat["$defs"]["NativeCause"]["enum"]
reg = ident["x-opensip-evaluator-deficiency-registry"]["sources"]

both = sorted(set(atom_enum) & set(defv2))
atom_only = sorted(set(atom_enum) - set(defv2))
def_only = sorted(set(defv2) - set(atom_enum))

focus = ["missing-relation-coverage", "selector-unbound", "coverage-unknown",
         "uncovered-expected-source-subject", "scope-without-coverage",
         "unavailable-program-binding", "population-unknown", "required-relation-missing",
         "language-tier-unsupported", "input-closure-incomplete", "budget-exhausted"]

out = {
    "standing": "READ-ONLY enum membership test of the published causes/nativeDeficiencies "
                "discriminator. Normative JSON only; no reference Python consulted.",
    "atomCauseCodeV1Description": atom_desc,
    "atomCauseCodeV1Size": len(atom_enum),
    "deficiencyV2Size": len(defv2),
    "inBothEnums": both,
    "inBothCount": len(both),
    "atomCauseOnly": atom_only,
    "deficiencyV2Only": def_only,
    "discriminatorPartitionsCleanly": not both,
    "perCode": {
        c: {
            "inAtomCauseCodeV1": c in atom_enum,
            "inDeficiencyV2": c in defv2,
            "inEvaluatorRegistryNative": c in (reg.get("native") or []),
            "inNativeCauseEnum": c in nativecause,
        } for c in focus
    },
}
print(json.dumps(out, indent=2, default=str))
