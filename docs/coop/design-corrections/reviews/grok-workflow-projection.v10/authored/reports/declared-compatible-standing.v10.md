# declared-compatible standing (v10)

- Normative: workflows-and-surfaces.md §2: current detector signed manifest lists baseline closure2 as exactly semantically compatible at the same major; fresh host resolves pivot closures from retained generation, installed signed release with the same closure2, or signed closureBundle, all under current trust.
- Implemented: DetectorManifestV1 is the unsigned body hashed as closure.manifestDigest. compare_admitted fills compatibleWith only from that body when host.closures[id].trust==admitted. Caller compatibleWith maps are refused. This helper does not verify signatures (host TCB already admitted the closure).
- Security-owned remainder: Signature envelope, release catalog, and closureBundle verification remain security/identity. Workflows consume the admitted body plus host trust receipt only.
- Standing: Typed owner schema under workflows/evaluator3; current-trust receipt is host.closures[].trust. Not a cryptographic verifier.
