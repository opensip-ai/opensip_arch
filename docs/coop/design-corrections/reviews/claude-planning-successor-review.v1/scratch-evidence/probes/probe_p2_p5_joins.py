import json, pathlib, sys
INPUTS = pathlib.Path(sys.argv[1])
C25 = pathlib.Path(sys.argv[2])
ARCH = INPUTS / "docs/v2/architecture"
DEFS = "$defs"
out = {}
sec = json.loads((C25 / "docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json").read_text())
rec = json.loads((ARCH / "commit-recovery-plan.v1.json").read_text())
b = rec["storeGenerationBindingSchema"]
intent = sec["schemas"]["InstallationTransitionIntentV1"]
journal = sec["schemas"]["InstallationTransitionJournalV1"]
out["P2_store_instance_id_owner_support"] = {
  "bindingRequired": b["required"],
  "substringStoreInstanceInWholeOwnerBundle": "storeInstance" in json.dumps(sec),
  "intentProperties": sorted(intent["properties"]),
  "intentAdditionalProperties": intent["additionalProperties"],
  "journalProperties": sorted(journal["properties"]),
  "journalAdditionalProperties": journal["additionalProperties"],
  "storeGenerationEqualsOwnerI64NonNegative": b["properties"]["storeGeneration"] == sec[DEFS]["I64NonNegative"],
  "stateSchemaEnumEqualsOwner": b["properties"]["stateSchema"]["enum"] == sec[DEFS]["StateSchema"]["enum"],
  "ownerStateSchemaHasNoTypeKeyword": "type" not in sec[DEFS]["StateSchema"],
  "executionIdPatternEqualsOwner": rec["recordSchema"]["properties"]["executionId"]["pattern"] == sec[DEFS]["ExecutionId"]["pattern"],
  "grantGenerationEqualsOwnerI64Positive": {k: v for k, v in rec["recordSchema"]["properties"]["grantGeneration"].items() if k != "description"} == sec[DEFS]["I64Positive"]}
invf = json.loads((ARCH / "repository-file-inventory.v1.json").read_text())
gen = [x for x in invf["files"] if x["generated"]]
out["P3_generated_outputs_vs_closed_registry_role_enum"] = {
  "registryOutputRoleEnum": ["carrier", "shape-validator"],
  "registryOutputLanguageEnum": ["rust", "typescript"],
  "generatedFiles": [{"path": x["path"], "inventoryRole": x["role"], "description": x["description"]} for x in gen]}
ch14 = (ARCH / "14-repository-and-module-layout.md").read_text()
fence = chr(96) * 3 + "text"
tree = ch14[ch14.index(fence): ch14.index(chr(96) * 3, ch14.index(fence) + 7)]
crate_dirs = sorted({p["path"].split("/")[1] for p in invf["packages"] if p["path"].startswith("crates/")})
out["P4_chapter14_handwritten_tree"] = {"crateDirsInInventory": crate_dirs,
  "missingFromHandwrittenTree": [d for d in crate_dirs if (d + "/") not in tree]}
plan = (ARCH / "implementation-boundaries-and-build-plan.md").read_text()
out["P5_author_verification_counts"] = {"inventoryFilesActual": len(invf["files"]),
  "recoveryCasesActual": len(rec["cases"]),
  "planClaims186UniquePaths": "186 unique paths" in plan,
  "planClaims190InventoryPaths": ("190" + chr(10) + "inventory paths") in plan,
  "planClaims36PlannedFaultCases": "36 planned fault cases" in plan,
  "chapter14MissingSpaceDefects": [s for s in ("has198", "and38") if s in ch14]}
print(json.dumps(out, indent=1))
