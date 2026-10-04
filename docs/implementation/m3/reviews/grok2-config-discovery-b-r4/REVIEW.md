# M3-B r4 — ACCEPT

Subject: `docs/implementation/m3/config-discovery-b/PROPOSAL.md`, 107025 bytes, sha256 `8e0803a8045bf4c47ac0340a4d47f7d733e710432cea17c1e78a90f7d53d19c7`. Diff base: `PROPOSAL-r3.md`, 106199 bytes, sha256 `06ac4d915c1fcdcdb22e342b33f8b90b2ae738a1fd3b838d5861c14bfbd8109f`. The four pins in `hashes.txt` match. Read-only. No cargo. `~/Library/Application Support/OpenSIP` was absent.

r4 answers the r3 review (`reviews/grok2-config-discovery-b-r3/`). The diff is the title, the new r4 changes section (its standing sentence and the two-row table), the item 13 producer cell, and the item 24 directory-custody code cell. Those two body edits are the two rows of that table.

## RF-1

Resolved. Item 24's directory-custody row (`PROPOSAL.md:785`) states row 2's pair: `PROJECT.ROOT_CUSTODY_REFUSED` / `CONFIG.INVALID` (X2:250-270). The subject cell remains "the existing custody subjects".

Row 2 is the layout row at line 783, which states that pair with subjects `member-vcs-unsupported:<reason>` and `member-outside-volume`. Row 1 (line 782) stays `PROJECT.EXPLICIT_PATH_INVALID` / `CONFIG.INVALID` for a grammar failure and for a crossing. The in-repository row (line 784) still names row 1's pair with `JOIN_CROSSES_NESTED_REPOSITORY` (RBS1 R2).

That is the r3 fix. B-S1's refusals paragraph keeps a member directory's custody failure on its existing custody subject, and keeps `JOIN_CROSSES_NESTED_REPOSITORY` for a crossing into a repository that cannot become a member. `X2:250-270` is `project-root-x2/PROPOSAL-r8.md` lines 250–270, item 8's refusal rows; line 251 pairs `PROJECT.ROOT_CUSTODY_REFUSED` with `CONFIG.INVALID`. Both codes are in `public-detail-registry.json`. The row adds no code.

## NBO-1

Handled. Item 13's producer cell (`PROPOSAL.md:405`) says `boundary_inventory(result)` produces `AdmittedBoundaryInventoryV3` for every project, because B-S1 LD-4 makes version 3 the current discovery record (the SX-1 anchor is on every project). The citation names SLS `schemas.AdmittedBoundaryInventoryV3`, the `schemas` member at `b-s1/schemas/security-lifecycle.schemas.v1.b-s1-additions.json:729`. The SL:286 override and the NE:4135 override in `b-s1/PASSAGES.md` both name `AdmittedBoundaryInventoryV3`. F9 at `PROPOSAL.md:829` already said that and is unchanged.

## Non-blocking

NBO-1. Line 9 still reads "Draft r3, not accepted. Not code." The title and the r4 changes section identify this file as r4.

NBO-2. Line 409 still says the closed `DiscoveryProvenanceV2`, or V3 under D15. B-S1 LD-4 and the S3 records paragraph make `DiscoveryProvenanceV3` the current provenance for every project. The producer row at line 405 already names the V3 inventory for every project.

NBO-3. The parentheticals at lines 405 and 785 say "RBS3". The r3 changes glossary defines RBS1 as GROK2's review of B-S1. The r4 changes section names `reviews/grok2-config-discovery-b-r3/`. The cells state the r3 fix.
