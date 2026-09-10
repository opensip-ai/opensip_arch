# Command-inventory joins (v12)

- Historical: workflows/command-inventory.v1.json schemaMajor 1, json renderer version 2 / envelope major 2, golden pin schemaMajor 2
- Current: workflows/command-inventory.v3.json schemaMajor 3, json renderer version 3 / CommandEnvelope major 3, golden pin schemaMajor 3, validated against evaluator3 command-inventory:3

Remaining joins:
- v1 historical instance remains schemaMajor 1 and is not the evaluator3 inventory:3 instance
- v1 and v3 share command names; v3 renderer/envelope majors are the selected profile
- parityFields token 'findings' vs FindingSurface / sarif-adapter:2 still names the same analysis projection
- execution-inputs manifest is required on a public admitted Run; missing capture is EVALUATION.PROJECTION_INPUT_INCOMPLETE
- physical store pointer inventories are excluded from semantic execution-inputs identity (main Grok v6); this projector does not join retainedObjectKeys/retainedBlobDigests
- sidecar/candidate parent locators are stripped; incoming-search expectedInventoryRefs expand to stripped inventory bodies
