# V1 product dispositions

**Status:** binding for the decided rows; retention remains blocked on Phase 1A  
**Binding artifact:**
[`artifacts/product-dispositions.v1.json`](artifacts/product-dispositions.v1.json)  
**Checker:**
[`artifacts/check-product-dispositions.py`](artifacts/check-product-dispositions.py)

These choices close the product-owned forks that are independent of the in-flight
V10/retention work.

| Decision | V1 disposition |
|---|---|
| P-1 ecosystem | Preserve a future-safe boundary; **no marketplace or ecosystem lifecycle depth for v1** |
| P-2 contributions | **Narrow producers and data-only rules/profiles**; no extension-owned commands, policy, persistence, rendering, termination, or lifecycle |
| CI layer 4 | **Ignore layer 4 entirely in CI/non-interactive mode**; local interactive use remains keyed and explained |
| Detector pivot | Only for an explicitly requested comparison when the detector major changes; optional for the first milestone; unavailable means `INDETERMINATE` |
| Public rule IR | **Do not freeze for v1** |
| Support windows | Keep provisional/GUESSED and consumer-labelled; they are not SLAs or demonstrated evidence |
| Substrate | Confirm DELIVERY v2: Rust host/core, bundled TypeScript provider, pinned `rustc_driver` sidecar, full default profile, finite platform matrix, offline assets |
| Retention default (`CD-RT-5`) | **Pending Phase 1A**; no implementer may choose it and no freeze may imply V10 is resolved |

The vertical-slice inclusion/exclusion boundary remains
[`v1-slice.md`](v1-slice.md). These dispositions narrow product behavior; they do
not weaken any binding contract and do not qualify a release.
