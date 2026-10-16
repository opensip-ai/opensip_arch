# B3-B3C inventory v209 review

Verdict: **ACCEPT-UNIT**. Inventory candidate assessment: **ACCEPT**.

Required findings: none. Non-blocking observations: none.

The subject manifest independently matches 701 bytes and SHA-256 `ce97b3694e84bf8e465e8cb8e2b4a3a8c7b793a698dddc38c3ce7c1a6a5a6d3a`. All three members match their declared sizes and hashes. Product main is clean at `a91e96c311dc3b300b25704a02dda2ba12396e15`; architecture is at `1d90ed57f06ec79aa8fa0688c10847b0571c7633`. The integrated files match the accepted B3-b3c product map. This is an inventory review, not a code re-review.

## Added rows

Exactly three rows are added; none had an inherited planned row.

| Path | Package / role | Generated | Assessment |
| --- | --- | --- | --- |
| `crates/security/src/custody/discovery_workspace_ledger.json` | `opensip-security` / `fixture` | true | Accurately describes the generated per-branch costs, members, inputs, pins, verdicts and caps; explicitly design evidence without corpus bytes or qualification. |
| `tools/security/discovery_workspace_ledger.py` | `tooling` / `builder` | false | Accurately describes the unchanged imported model, verified D15 shapes, rendered carriers, both branches and joint failure/caps rule. |
| `tools/tests/test_discovery_workspace_ledger.py` | `tooling` / `test` | false | Accurately describes the hermetic synthetic shape, accounting, refusal, lifecycle and held-out-access controls. |

The descriptions claim no capability beyond the accepted unit. Only the generated record is marked generated.

## Inheritance and coverage

The candidate contains 1285 sorted, unique rows, a strict superset of the parent's 1282 rows. Every inherited row is equal by value. All other top-level content is unchanged, including the 20 packages and nine pending decisions. Every one of the 1187 tracked product paths is covered. The other 98 rows are exactly the still-absent inherited planned paths, retained unchanged without implementation claims.

The successor's addedFiles and inheritedPlannedFilesRetained lists equal the independently computed sets exactly. The inherited discovery_census_tests.rs description remains true: the existing walker soundness, compiled closure and census-classification controls remain. It omits the new companion workspace-ledger classification, making it incomplete rather than false. No description override is required for this unit.

## Census and bindings

The expressly permitted source operability command passed with 114 rows and no findings. The exceptions file contains 439 mint-audit rows. Both checker and exceptions match their integration-census pins and are byte-identical to the accepted code base `fb63a93adb77f7ef50663be41241edba4c3f966d`. The source check includes the mint-audit comparison. No mint authority is added; lexical audit evidence is not authority.

Independently verified successor bindings:

- Parent v208: 706443 bytes, `3ba67e2d955c7c2a89e6d2cbfb12d69a322fbc865f1327cbbbc75b9742350a31`.
- Candidate v209: 708851 bytes, `c20976abdf1003c42091ea8b27e2814749975e6cf5a4909c63ffebf9cf5a9deb`.
- Successor record: 5542 bytes, `037415b4cc23895252ad9143324e87d29afd225a91b1307dd68600b997e5bb2f`.
- Accepted code review: 185 bytes, `9cb17a6dc02425186c2997fa39d4f2cee503242ab9e0ef94f308ff1785dae875`, verdict ACCEPT-UNIT with no required findings.
- Accepted code subject: 7948 bytes, `91b0ea21228cf12812dded61de03c8c428a2a6b2ce4b554c86749167aef3b313`, matching the accepted review's subject binding.
- Integration census: 741 bytes, `74313ca60e06344699c150343d001acb372787054cb46be541080f848a0aa75d`, with the correct integrated product commit, source result and mint count.

No qualification is claimed. Lead assent, architecture publication, the separate inventory lock binding and fresh verify_design remain integration work.

Only REVIEW.md and review.json are written. Neither repository, stage nor control files were edited. No compiler, Cargo, tests, lane, network, private fixture, installation directory, signing keys, held trees, other panes or delegation was used. Nothing was pushed.
