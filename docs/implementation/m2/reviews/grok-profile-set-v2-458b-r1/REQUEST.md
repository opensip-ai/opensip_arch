Grok review unit 458b, r1: code, contract successor and inventory successor together. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-profile-set-v2-458b-r1. You own the serial native lane until your report is written. Host macOS 27.0. Rust is /opt/homebrew/Cellar/rust/1.95.0/bin. Use cargo --locked --offline. Do not read or print the private 413 UUID fixture.

Law: docs/implementation/m2/profile-set-acl-omission-458b/PROPOSAL.md r2 (accepted).

## Subjects

1. **Product code** (uncommitted on 6f39619; pins in hashes.txt):
   - root_payload.rs:
     - `mac_profile(value, schema)`: a V2 macOS measured row may carry `installAclOmission` == "no-acl-stored";
     - `profile_shape` stays V1, with new `profile_shape_v2` and `profile_shape_version`;
     - `PlatformDecision.matched_acl_omission` is set only on the selected last-duplicate row when there are no refusals and the body is `profileSetSchema` 2;
     - the `install_acl_omission()` accessor also requires ExactMeasured, a lane and no refusals;
     - a test-only `unsigned_fixture_v2`.
   - admitted_profiles.rs: `ProfileReader { V1Only, V1OrV2 }` and `verify_profile_set_with`. `verify_profile_set` is the V1Only wrapper and is unchanged for every caller.
   - profile_tests.rs and platform_tests.rs: three tests over the V2 fixtures.
   - The three new fixture files.

   **The working tree also has uncommitted 463b changes** (tools/security/*, the generated shape nodes, core_inventory.rs). They are out of scope and will be reviewed next; treat them only as the environment.
2. **Contract successor** docs/implementation/m2/profile-set-acl-omission-selection-v1/ (subject pin in subjects.txt). It contains:
   - the V2 schema, made by make_schema.py and asserted to differ from V1 in exactly two ways;
   - a reference model that imports the pinned V1 model by hash;
   - pure-Python RFC 8032 Ed25519 and public-seed signing;
   - the three case files, byte-identical to the product fixtures;
   - check_cases.py and check-results.json;
   - passage overrides for security-and-lifecycle.md lines 685, 711 and 845.

   Parents are the canonicalization source, the schema bundle, the V1 model and security-and-lifecycle.md. The reference model normalizes one refusal spelling (INSTALL_ROOT_FS without the fs suffix) to the selected product corpus, and the README says so.
3. **Inventory successor** docs/implementation/m2/profile-set-v2-inventory-v68/ (subject pin in subjects.txt). It is v67 plus the three fixture rows, in sorted order (718 files), with the byte-identical v64–67 projection helper; its verification passed with 5 rows and 28 corruptions refused.

## Lead's replay

The security lib passes 455/0 with both uncommitted units present, and 452/0 before 463b. The three V2 tests pass. Workspace clippy `-D warnings` and fmt pass. In a scratch clone pair with provisional review and assent files for both 458b records and both lock entries appended, `verify_design --implementation` passed with 67 contract units, 43 inventory successors and v68 selected.

## Decide

Code: does it implement 458b exactly? Specifically:
- the V1 path is unchanged;
- the V2 member is const;
- the accessor reads only the selected row;
- the opt-in reader admits V1 or V2;
- V2 is never admitted by default.

Contract successor: are the schema, reference, cases, parents and passage overrides right, and are the Python signatures genuine against profile-roots.json? Inventory: is v68 exactly v67 plus three rows with a correct projection?

review.json must contain:
- "verdict" (ACCEPT-UNIT or REQUIRED-FINDINGS), covering all three subjects;
- "requiredFindings";
- "subjectManifestSha256", an object mapping each subject manifest path to its sha256;
- "inventoryCandidateAssessment" as in your 463a reviews, for v68: verdict, requiredFindings, the candidate path, bytes and sha256, the parent, and the successorRecord.

Write REVIEW.md and review.json. Do not commit.
