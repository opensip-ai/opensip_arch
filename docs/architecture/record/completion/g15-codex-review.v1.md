# Conditional G15 independent review

OBJECT:1MUST-FIX,0SHOULD-FIX.3208/3208replay byte-identical;reviewer authored none of15unit files.

G15-M1: a ROOT-signed revocation list issued2026-10-02 is accepted at2027-03-01 with valid current catalog/root. The resolver checks version floor and future time but not the chosen90day freshness bound. Full repro/input paths and repair are in the companion JSON. No partial resolved lock may result from stale revocation. Other concrete custody, archive, canonicalization, scoped view and960slot joins are supported within their stated design scope. No register edit or production qualification.
