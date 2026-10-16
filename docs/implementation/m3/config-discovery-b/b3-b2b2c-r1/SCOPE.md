# B3-b2b2c r1: the T2 link-map controls and the joint sweep (M3-B unit B3-b, sub-unit B3-b2b2c)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 1.**

It implements B3-b2b2c of the B3-b plan r2 as amendment A3 states it (`../b3-b/PLAN-r2-A3.md`; Codex `codex-b3b-plan-a3-r1`, ACCEPT). That is plan r2 section 3's two T2 link-map controls and its joint sweep, unchanged, under law M3-B r9 item 20's first control and item 22's control.

**Base:**
- product main `c0a9761`: B3-b2b2b bound, inventory v206, 170 contract successors;
- architecture `51d91621`.

No product source outside tests and one developer tool changes. No closure file changes, so the census is unchanged.

## What it delivers

### (a) `vcs: none`: declarations and links, with the members supplied

- **The tool** (`tools/security/t2_link_controls.py`, new) covers each lead-readable T2 workspace whose ecosystem has a D15 reader. Those are the four Cargo and npm workspaces. Python has no reader at M3 (law item 20), so `mr-py-medium-boto` keeps its pinned map and is not run. For each workspace it:
  - re-verifies every member store against its pinned `gitTree` and QD-22 `treeDigest`, no-follow, through the census tool's own `verified_tree` and `store_path`. A held-out entry is refused before any filesystem call;
  - verifies the workspace's overlay through the census's `verified_workspace`. The record must be canonical, its SHA-256 must be the manifest's `overlayDigest`, and it must equal the cache's and the archived acquisition copy;
  - requires the manifest to be the one the bound census was taken over (its SHA-256 in `discovery_census.json`).

  Then it writes a minimal `vcs: none` reconstruction:
  - each overlay link's provider manifest, with its exact verified bytes, at `<mount>/<package directory>/`;
  - the reader carrier rendered from the overlay. For Cargo, that is FETCH-SPEC §6's `.cargo/config.toml`, which must equal the cache's rendered file byte for byte. For npm, it is law item 20's `package.json`, `{"private": true, "workspaces": [<link directories, sorted>]}`.

  **It writes only under the lane's private temporary directory** (`--out` must lie outside both checkouts). The lane removes the reconstruction after each run. No corpus byte is a repository fixture (FETCH-SPEC: "never in any repository").
- **The control** (`t2_vcs_none_reconstructions_give_the_overlay_link_maps_with_supplied_members`, in the new `workspace_t2_link_tests.rs`) copies each reconstruction into a scratch W, the invoking user's own, with directories 0755 and files 0644. It then runs the decision core over the native observation. A test-only wrapper, `Supplied`, supplies only two things at the link stage:
  - the members' placement, a `.git` marker at each overlay member mount;
  - item 6b's admission.

  Every other observation is native: the carrier read and its custody, placement lookups, and the provider manifests' custody and reads. This is plan r2 NBO-1's seam: test-only, never a production placement bypass. **Checked:**
  - every providing member is declared;
  - the carrier is read with nothing unresolved;
  - the derived links are exactly the overlay's link map, each link of the workspace's ecosystem and inside its provider;
  - each overlay record is checked against its pinned digest. The four `(id, overlayDigest)` pairs are constants in the test.

### (b) Conventional Git: integration through the unchanged discovery

`t2_reconstructions_with_conventional_git_members_link_through_discovery` uses the same reconstructions. Each member mount is given a synthetic conventional `.git` (`git init`, then `git read-tree --empty` for an empty valid index), and the test runs `discover_with_members`, the unchanged product discovery, with no seam. **Checked:**
- the result is accepted;
- item 6b admits every declared member, each declared by its reader;
- the links are the overlay's map;
- one carrier is read with nothing unresolved;
- the V3 record is complete: `memberRepositories` and both `workspaceDeclarations` rows;
- an undeclared, consumer-only member mount stays a nested repository (LD-B3B2B2C-2).

### The joint sweep (item 22's control)

`the_p3_sweep_with_members_joins_security_discovery_and_the_native_unit_instrument` is in the host's `discovery_flag_tests.rs`, through security's scenario seam. It places the P3 fixture under a W that is in no repository, with two members, `repos/a` and `repos/b`, declared by `W/package.json` and made real repositories with `git init`. Member `a` holds P3's nested repository (`vendor/lib`, with an installed dependency tree) and its nested project (`apps/site`, with a `sub` crate). **Over one marker inventory:**
- security's admitted inventory (`records.inventory`, with `memberRepositories`), passed to B2-c1's native unit instrument (`discover_units`), gives exactly security's unit set: W and both members;
- the inventory records the nested repository and the nested project, and the native instrument excludes every marker unit below them, by reason. Security's walker enters neither, so it records no excluded unit inside them (LD-B3B2B2C-3);
- **the inventory with `repos/b` removed from `memberRepositories`** refuses `native.boundary-inventory-mismatch`, with the anchor `repos/b/.git` (B-S1 U-8, `member-not-admitted`).

## What changes

| Path | Change |
| --- | --- |
| `tools/security/t2_link_controls.py` | **New.** The reconstruction tool, as above. |
| `crates/security/src/custody/workspace_t2_link_tests.rs` | **New.** The two T2 controls, both `#[ignore]`d and run by the check lane, and the `Supplied` wrapper. |
| `crates/security/src/custody/workspace_discovery.rs` | One `include!` of the new tests in its test module. |
| `crates/security/src/custody/workspace_discovery_tests.rs` | `run_with`'s discovery half is extracted as `discover_at`, which the T2 control (b) shares. The composition and race controls are unchanged. |
| `crates/host/src/discovery_flag_tests.rs` | The joint sweep, with its `git_in` and `marker_inventory` helpers. |

## Lead decisions

- **LD-B3B2B2C-1. The reconstruction reaches the controls through the lane's temporary directory.** M3-B r5 item 9 closes the environment reads to its enumerated list, and the T2 bytes may live in no repository. So the controls are `#[ignore]`d, as the existing lane-run probes are (`project_admission_legacy_probe_tests.rs`). They read `std::env::temp_dir()/opensip-t2-link-controls`, which the lane's tool has just written in its private 0700 `TMPDIR`, and they assert they found exactly the four pinned workspaces. `temp_dir` is not one of the audited reads, and the environment-exceptions pin passes unchanged. **Rejected:**
  - a new environment variable, which would need law;
  - committing the manifests, which FETCH-SPEC forbids.
- **LD-B3B2B2C-2. The declared members are the providing mounts.** A member exists only when a reader entry declares it (law item 20). The carrier rendered from the overlay names each link's directory, so it declares exactly the mounts that provide a linked package. `mr-rs-large-aws-lambda-tokio`'s `rs-medium-aws-lambda-rust-runtime` only consumes, so it is not declared. In (b) it stays a nested repository. The controls assert this, rather than every overlay mount being a member.
- **LD-B3B2B2C-3. The joint sweep compares what each instrument can observe.** SLM's P3 sweep compares excluded units because its synthetic fs holds every marker. The product walker never lists inside a boundary, so security records the boundaries (`nestedRepositories`, `nestedProjects`), not units inside them. The sweep therefore compares unit sets for equality and the boundary records, and it checks the native instrument's excluded units against those boundaries.
- **LD-B3B2B2C-4. Cargo carrier keys are quoted.** FETCH-SPEC §6's example writes `tokio = { path = ... }`. The acquisition rendered the cache's file with quoted keys (`"tokio" = { path = ... }`), which parse to the same table. The tool renders the cache's exact bytes and cross-checks them.

## Checks

Lane r1, `evidence/b3b2b2c-checks-r1/`. A first, fully passing attempt (`b3b2b2c-checks-r1-attempt1/`) showed that `carrier-drops-a-link` was caught by the tool's cache cross-check, not by the controls. So `cargo-carrier-written-short` was added, and the lane was run again:
- the security and host suites at base and candidate, with equal failure sets: no new security test is counted, because the two T2 controls are lane-run, and one new host test;
- the census unchanged (no closure file changes);
- rustfmt;
- the T2 run: the tool, then both lane-run controls, which must report two passed, then the reconstruction removed;
- Clippy on security (with and without `scenario-fixtures`) and on host;
- the host's scenario discovery tests;
- every vector check;
- FW-01, walk storage, the census controls and the census;
- environment, operability and verify_design.

**Mutations (seven), each with its gate:**
- `carrier-drops-a-link` (Cargo): the T2 run, caught by the tool's own cross-check against the cache's rendered carrier;
- `cargo-carrier-written-short`, a Cargo carrier written without one link after that cross-check, and `npm-carrier-drops-a-link`: the T2 run, caught by both controls;
- `provider-manifest-swapped`, which renames the provided package in one reconstructed manifest: the T2 run;
- `npm-links-not-npm`, in the decision core: the T2 run;
- `inventory-members-dropped`, which empties the inventory's `memberRepositories`: the joint sweep;
- `host-member-check-dropped`, which disables U-8's member check: the joint sweep.

## Not claimed

- That `vcs: none` product discovery admits members: (a) supplies them.
- That S8's `git-conventional` assembly exists: (b)'s `.git` is synthetic.
- No held-out workspace is read. Their margins are B3-b3b's blind run.
- No member-observation bound (B3-b3a).
- No CLI composition (J1).
- No qualification.

## Inventory

New paths for the inventory after acceptance:
- `tools/security/t2_link_controls.py`;
- `crates/security/src/custody/workspace_t2_link_tests.rs`.
