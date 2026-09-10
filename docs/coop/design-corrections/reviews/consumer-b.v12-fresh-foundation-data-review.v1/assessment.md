I'll start from the original charter, requirements, and exact file hashes, then independently recompute the retained foundation identities and joins without treating JSON claims as oracles.Hashes and the 80-file kit are next; I'll keep the review inside phases 0–4 plus the imported-observation boundary.I'll verify every declared hash, then pull the identity, canonical, and capability norms the foundation vectors have to satisfy.Hashes match. Next I’ll extract C/H/CVE1 and admission recipes from the kit and inspect each foundation exhibit.I’ll read the remaining exhibits and the identity/admission schemas so the checker can recompute C, H, and CVE1 independently.I’ll pull the remaining traces, import-boundary exhibit, relation registry, and schema defs needed to recompute independently.I have the schemas and store shape. Next I’ll write an independent checker that recomputes C/H/CVE1, admission, traces, and the cited store joins.I'll write an independent checker from the kit recipes, then run it against every retained exhibit.Four trace IDs failed. I'll inspect the independent mismatches before deciding whether that's an exhibit error or a checker bug.The identity-before-source miss is a checker bug: frame updates must apply only after a successful match. The unavailable/fault `stageCount` claims are separate exhibit errors I’ll record without treating them as oracles.Independent checks passed. I’ll write the review artifacts, ID map, hash verification, and reproduction notes next.**Verdict: `FOUNDATION_DATA_ADMITS`**

This is a bounded technical review of original phases 0–4 plus `R-IMPORTED-OBSERVATION-BOUNDARY`. It is not a full consumer ACCEPT and not implementation readiness.

Kit, data, charter, and requirements hashes all match (80 kit files, 30 evidence files). Claimed identities and `stockOk` flags were recomputed, not trusted.

Independently matching retained identities include:

| Record | Typed id |
|---|---|
| snapshot-A | `snapshot2:3324a39a…806a97` |
| plan → view → proof → evidence → seal → run | `plan2:61c9dfbb…` through `run3:393213e5…6b05` |
| capability manifest | `6e6f63c79285d280…72652b` |
| import wrapper | `import2:e52a8464…044af8` |

Source → Plan → View → Proof → Evidence → Seal → Run joins hold on the standalone chain. Missing plan nested preimages were not accepted by substitution and were not upgraded into a full Run. Capability first-gates/masking, protocol traces (including identity-before-source with `sourceBytesSent=false` on P3-34), relation/rung/count/matrix laws, and import nested SHA256(C) joins all independently hold. Frozen stores were used only for cited file-rung and import membership.

S-\* author-process / fresh-origin / oracle custody cannot be authenticated from these JSON bytes; those IDs are marked `external-root-custody-required`.

One should-issue: unavailable/fault exhibits claim `final.stageCount=1` on traces that never send Analyze. The published machine leaves `stageCount=0`. Discriminating P3 ids and terminals still match.

Reproduce with:

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-fresh-foundation-data-review.v1/output/independent-checker.py
```

Deliverables: `foundation-data-review.md`, `foundation-data-review.json`, `input-hash-verification.json`, `original-id-map.json`, `independent-checker.py`, `independent-results.json`, `first-refusals.json`, `reproduction.md`.
