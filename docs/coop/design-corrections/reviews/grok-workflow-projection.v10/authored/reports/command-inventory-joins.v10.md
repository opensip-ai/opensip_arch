# Command-inventory joins (v10)

- Historical: workflows/command-inventory.v1.json schemaMajor 1, json renderer version 2 / envelope major 2, golden pin schemaMajor 2
- Current: workflows/command-inventory.v3.json schemaMajor 3, json renderer version 3 / CommandEnvelope major 3, golden pin schemaMajor 3, validated against evaluator3 command-inventory:3

Remaining joins:
- v1 historical instance remains schemaMajor 1 and is not the evaluator3 inventory:3 instance
- v1 and v3 share command names; v3 renderer/envelope majors are the selected profile
- parityFields token 'findings' vs FindingSurface / sarif-adapter:2 still names the same analysis projection
- proof.executionInputsDigest / execution-inputs domain: root is activating fixture capture; pivot join compares captured records minus Plan locators when both sides have the ref, and does not rewrite foundation to paper over a missing digest
- physical store pointer inventories are excluded from semantic execution-inputs identity (main Grok v6); this projector does not join retainedObjectKeys/retainedBlobDigests
