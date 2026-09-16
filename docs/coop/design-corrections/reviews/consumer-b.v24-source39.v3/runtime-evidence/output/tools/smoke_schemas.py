import sys
sys.path.insert(0, '/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v3/output/ref')
import schemas

K = schemas.kit()
print("docs loaded", len(K.docs))
# 1. valid scope-descriptor
ok = K.admit({"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": [], "excludedPathPrefixes": ["node_modules"]},
             "foundation/identity-schemas.v3.json", "#/$defs/scope-descriptor")
print("scope ok", ok)
# 2. unsorted canonical-set
bad = K.admit({"schemaVersion": 2, "workspaceRoots": ["b", "a"], "pathPrefixes": [], "excludedPathPrefixes": []},
              "foundation/identity-schemas.v3.json", "#/$defs/scope-descriptor")
print("scope unsorted", bad)
# 3. float const
bad2 = K.admit({"schemaVersion": 2.0, "workspaceRoots": ["."], "pathPrefixes": [], "excludedPathPrefixes": []},
               "foundation/identity-schemas.v3.json", "#/$defs/scope-descriptor")
print("scope float", bad2)
# 4. cross-document $ref: command-envelope failure
env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "failure",
       "requestId": "req1_" + "0" * 32, "exitCode": 2,
       "termination": {"class": "request-rejected", "errorCode": "CONFIG.INVALID",
                       "domainDetail": {"code": "CONFIG.INVALID", "remedy": "fix"}},
       "errors": [{"code": "CONFIG.INVALID", "remedy": "fix"}]}
print("envelope", K.admit(env, "workflows/schemas/evaluator3/command-envelope.schema.json", "#"))
# 5. subject inventory with allOf-then order by nativeSubjectId (reversed rows)
inv = {"schemaVersion": 1, "planId": "plan2:" + "0" * 64, "parameterDigest": "0" * 64, "cellOrdinal": 0,
       "programOrdinal": 0, "kind": "file", "state": "complete", "deficiency": None, "nativeCause": None,
       "examinedPaths": ["a.ts", "b.ts"],
       "rows": [{"nativeSubjectId": "b.ts", "kind": "file", "path": "b.ts", "qualifiedName": "b.ts",
                 "subjectLanguage": "typescript", "signatureTokens": [], "projections": []},
                {"nativeSubjectId": "a.ts", "kind": "file", "path": "a.ts", "qualifiedName": "a.ts",
                 "subjectLanguage": "typescript", "signatureTokens": [], "projections": []}]}
print("inventory reversed", K.admit(inv, "foundation/subject-inventory.schema.v1.json", "#"))
for rel in ["foundation/identity-schemas.v3.json", "foundation/execution-inputs.schema.v1.json",
            "foundation/enumeration-plan.schema.v1.json", "foundation/subject-inventory.schema.v1.json",
            "native/native-evidence.schemas.v2.json", "foundation/relation-payload-schemas.v2.json",
            "foundation/incoming-search.schema.v1.json", "foundation/target-attribution.schema.v2.json"]:
    print("unannotated hex", rel, K.unannotated_hex_fields(rel))
