import sys
sys.path.insert(0, "/tmp/opensip-design-corrections/consumer-b.v8/output/work")
import schemas

print(schemas.validate({"schemaVersion": 2, "kind": "none", "commitId": None,
                        "dirty": False, "sourceInventoryDigest": "0" * 64},
                       "identity", "#/$defs/vcs-observation"))
# exact typed: True must not satisfy const 2
print(schemas.validate({"schemaVersion": True, "kind": "none", "commitId": None,
                        "dirty": False, "sourceInventoryDigest": "0" * 64},
                       "identity", "#/$defs/vcs-observation"))
# cross-bundle URN ref
print(schemas.validate({"schemaFamily": "opensip.product.scope", "schemaMajor": 1,
                        "include": ["src/**"], "exclude": []},
                       "policy-document", "#/$defs/ScopeDocumentV1"))
print(schemas.validate({"schemaVersion": 3, "key": {}, "entry": {}},
                       "native", "#/$defs/CoverageResultV3")[:3])
