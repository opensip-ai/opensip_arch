import json, pathlib

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work/'
                 'docs/coop/design-corrections/workflows/schemas/repair.schema.json')
s = P.read_text(encoding='utf-8')

OLD = '''    "EvidenceRequirement": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "relation",
        "minResolution",
        "completeness",
        "satisfied"
      ],
      "properties": {
        "relation": {
          "$ref": "urn:opensip:product-v1:workflows:common#/$defs/CanonicalIdentifier"
        },
        "minResolution": {
          "$ref": "urn:opensip:product-v1:workflows:policy-document#/$defs/Rung"
        },
        "completeness": {
          "type": "string",
          "enum": [
            "complete",
            "partial-acceptable"
          ]
        },
        "satisfied": {
          "type": "boolean"
        },
        "deficiency": {
          "$ref": "urn:opensip:product-v1:workflows:common#/$defs/D9Deficiency"
        }
      }
    },
'''

DEF_DESC = (
    "The reason THIS requirement is unsatisfied, in the native per-requirement sufficiency "
    "vocabulary. OWNERSHIP: the value is produced by native-evidence.md section 4.6 "
    "`sufficiency_v2` for this requirement against the evidence Run named by "
    "RepairPlanDescriptor.evidenceRunId, and repair CONSUMES it; preview mints no sufficiency "
    "verdict of its own and never re-derives one from the descriptor. PRESENCE IS NOT OPTIONAL AND "
    "IS NOT FREE: the field is REQUIRED exactly when satisfied is false and FORBIDDEN when "
    "satisfied is true, enforced by the allOf below, because sufficiency_v2 is total - it returns "
    "{satisfied:true, disclosures} with no deficiency, or {satisfied:false, deficiency} with "
    "exactly one member of this vocabulary. Omitting it under satisfied=false previously dropped "
    "the only disclosure of WHY a repair is inapplicable while leaving the record schema-valid. "
    "WHY NOT D9Deficiency, which this field previously named: four of the nine outcomes "
    "sufficiency_v2 emits - derivation-policy-unmet, external-consumers-unknown, "
    "input-closure-incomplete, resolution-incomplete - are not members of it, so the field could "
    "not express its own producer's result; the only conforming alternatives were to write the "
    "D9-mapped `verdict-indeterminate` for all four (destroying the distinction, and in particular "
    "conflating `resolution-incomplete` - the outcome that decides a destructive unused-code "
    "repair - with three unrelated ones), or to omit the field. Retyping this ONE per-requirement "
    "field is the repair; D9Deficiency itself is unchanged and still carries every whole-Run and "
    "comparison-step termination. THIS FIELD IS NOT AN AUTHORIZATION: the sealed Run named by "
    "evidenceRunId remains the authority, `applicable` is still false whenever any requirement is "
    "unsatisfied, and apply still requires a security authorization bound to the exact "
    "repairPlanId. Editing or deleting it cannot make a plan applicable - it mints a different "
    "repairPlanId, which no authorization names."
)

NEW = '''    "EvidenceRequirement": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "relation",
        "minResolution",
        "completeness",
        "satisfied"
      ],
      "properties": {
        "relation": {
          "$ref": "urn:opensip:product-v1:workflows:common#/$defs/CanonicalIdentifier"
        },
        "minResolution": {
          "$ref": "urn:opensip:product-v1:workflows:policy-document#/$defs/Rung"
        },
        "completeness": {
          "type": "string",
          "enum": [
            "complete",
            "partial-acceptable"
          ]
        },
        "satisfied": {
          "type": "boolean"
        },
        "deficiency": {
          "$ref": "urn:opensip:product-v1:workflows:common#/$defs/NativeSufficiencyDeficiency",
          "description": %s,
          "x-opensip-vocabulary": {
            "authority": "native/native-evidence.schemas.v2.json#/$defs/DeficiencyV2",
            "mirroredAs": "urn:opensip:product-v1:workflows:common#/$defs/NativeSufficiencyDeficiency",
            "law": "native/native-evidence.schemas.v2.json#/x-opensip-deficiency-cause-registry/perRequirementConsumerBoundary",
            "producer": "native-evidence.md section 4.6 sufficiency_v2, per requirement",
            "admittedBy": "workflows_model.admit_evidence_requirement, called by repair_preview before any descriptor exists"
          }
        }
      },
      "allOf": [
        {
          "if": {
            "properties": {
              "satisfied": {
                "const": false
              }
            },
            "required": [
              "satisfied"
            ]
          },
          "then": {
            "required": [
              "deficiency"
            ]
          },
          "else": {
            "not": {
              "required": [
                "deficiency"
              ]
            }
          }
        }
      ]
    },
''' % json.dumps(DEF_DESC)

assert s.count(OLD) == 1, s.count(OLD)
P.write_text(s.replace(OLD, NEW), encoding='utf-8')
print('ok')
