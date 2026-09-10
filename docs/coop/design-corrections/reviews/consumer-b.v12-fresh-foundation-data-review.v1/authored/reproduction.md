# Reproduction

Independent checker, kit-only, no author models:

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-fresh-foundation-data-review.v1/output/independent-checker.py
```

The checker:

- verifies control, 80-file kit, and 30 evidence hashes
- implements C, H, CVE1, raw lexical JSON, CAP-MANIFEST-ID-V1 gates, and protocol3 from the kit
- recomputes every retained C/H/frame in the H, semantic, acyclic, capability, and import exhibits
- executes named negatives and first-gate/masking
- joins cited frozen-store file facts and one TS import id as membership only

It writes `independent-results.json` beside itself. Claimed JSON fields are comparison targets, not oracles.
