# PKG-ROWS-1-O1 r1: O1's package binding after inventory v245

Contract successor of the PKG-ROWS-1 unit (PLAN-r3 section 3.2, LD-Q-166 D2). Inventory v245 makes the
opensip-operability row and its three permissions (from opensip-host, opensip-components and opensip-storage) raw
inventory package rows by value, through VD3's reviewed package-successor profile. This record retires O1-PKG r1's
effective-policy route prospectively, without rewriting it:

- three VD2 supersessions of the meanings O1-PKG r1 published on docs/implementation/m3/operability/o1/PROPOSAL-r2.md
  lines 130, 149 and 558, keeping every other O1-C1 obligation;
- two ordinary overrides of O1-PKG r1's CONTRACT.md lines 3 and 7, which had no published meaning, qualifying them
  from v245.

Unchanged: package-policy.json (its Boolean rawInventoryPackagesMustRemainEqual and the fixed checker profile
opensip.o1a-package-admission.v1), CONTRACT.md lines 9, 11 and 13, and every other O1 passage. check_package_edges.py
--package-policy refuses v245 by design; the plain --inventory route is the binding check from v245.
No product code is accepted by this record, and it confers no qualification.
