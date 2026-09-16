# Proposed additive schema inventory04

Extend accepted202-row inventory3 by44 owned source paths:40JSONschema documents, exact architecture source map, native wireIDL/metaschema and reportcodecprofile. All20packages, package edges, pending decisions and inherited rows remain exactly equal. No npm/tooling/frontend selection, package change, source approval, product file creation or milestone qualification is implied.

Product filename convention is name-vN.schema.json. Architecture source artifact filenames retain their historical names; only proposed implementation destinations change. Model is the existing role for inert schema/IDL declarations. The first draft's dot-vN/schema-role mismatch is preserved in docs/implementation/m1/audits/schema-inventory-names-01; it was never accepted or installed. Newly added rows use proposed standing. Accepted parent tooling refinements keep their original bytes/standing and are not reinterpreted through the original v1-only file checker.

Run python -I -B check.py in a private copy. input-pins.json binds copied parent/candidate/successor/maps back to architecture. Future product source selection must independently admit the exact schema bytes and generator. This inventory owns location/responsibility only.
