# Command-inventory cross-schema joins

- Historical instance: workflows/command-inventory.v1.json schemaMajor 1, $id urn:opensip:product-v1:workflows:command-inventory, json renderer version 2 / CommandEnvelope major 2, golden envelope-major-unsupported remedy pin schemaMajor 2
- Isolated schema: workflows/schemas/evaluator3/command-inventory.schema.json $id urn:opensip:product-v1:workflows:evaluator3:command-inventory:3 schemaMajor 3, findings parity FindingSurface
- Root will mint: version-3 inventory from unchanged commands plus selected JSON renderer 3 / envelope 3; do not edit the v1 instance

Remaining joins:
- v1 instance json renderer version 2 vs isolated envelope schemaMajor 3
- v1 golden envelope-major-unsupported remedy 'pin schemaMajor 2' vs command-envelope:3
- v1 parityFields token 'findings' vs evaluator3 FindingSurface / sarif-adapter:2
- checker loads evaluator3 command-inventory:3 schema but does not validate command-inventory.v1.json against it
