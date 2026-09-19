# Addendum 1 to the reference122 review — case count corrected

Reviewer: Claude. 2026-09-18. `REVIEW.md` is left byte-unchanged (SHA-256
`13d2699aa18ddd8d07b6f0da52061cf6e6da689524544f959c9ad2ea8151852e`).

The review says the boundary probe has "32 cases". `probes/osrelease.py` executes and
`probes/osrelease.json` records **31**: 12 padded (3 components × 255/256/257/5,000), 11 Unicode/grammar
strings, 5 non-string types, 2 EXACT-MEASURED tier cases and 1 precedence case. The owner noticed the
discrepancy when porting them. No result, finding or verdict changes.
