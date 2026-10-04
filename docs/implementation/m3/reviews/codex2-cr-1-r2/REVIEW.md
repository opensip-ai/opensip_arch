# CODEX2 review: CR-1 r2

**Verdict: REQUIRED-FINDINGS.** RF-CR1-1 and NB-CR1-1 are resolved. One new required finding, **RF-CR1-2**, concerns the C2a materialization instructions. No new non-blocking observations.

The reviewed subject is `docs/implementation/m3/snapshot-plan-c/cr-1-subject.json`, SHA-256 `4e1b169b241212b5b6b250de0fdd85888c9a390168f766ba9a7d33968426484c` (11 members). The successor is `docs/implementation/m3/snapshot-plan-c/cr-1/successor.json`, 10694 bytes, SHA-256 `5ee9beace59c0c45b13fafe5e60cdd74afa7cbf281c3901cc7dfa3693f2365af`. The excluded lead unit draft is not part of this verdict.

## RF-CR1-2: preserve name admission when removing command trees

The instructions at `materialization-map.json:45` (`/alsoChangedByC2a/2/change`), `README.md:179,221`, and `evidence/build_cr_1.py:331-333` say to run the existing `command_checks` function only when `commands` is present. This avoids its unconditional indexing at product `component_manifest.rs:171`, but the function contains more than command-tree validation.

At pinned product `cd5958b`, lines 257-276 build the component name and alias set, add mounted-root aliases, reject duplicate keys and reserved-name collisions, and check live names for a different `(stableId, provenance)`. Both host admission and inventory-body validation reach this function through `validate_inner` (395-414). Gating its whole call would bypass these component-name rules for all four closure-only roles.

DR103 `/manifestSchema/fields/3` and `/manifestSchema/fields/5` retain name/alias admission, and `/rejectionRules/rules/1` retains RJ-2. CR-1 expressly preserves every other DR-103 rule for every role. The completed schema cannot check supplied reserved/live context or compare an alias with the primary component name. Thus a commandless grammar manifest whose name or alias collides with the supplied reserved/live set would receive no such check from this owner if C2a implemented the stated whole-function gate. This is a static finding about the proposed instructions; no runtime regression was executed.

Make command-tree validation conditional and preserve component-name/alias admission for every role, including the existing coexistence exception. The required exact replacements are:

At `materialization-map.json /alsoChangedByC2a/2/change`, replace the complete string with:

~~~text
The command-tree-specific checks run only when commands is present, which the schema makes exactly role analyzer. Component-name and manifest-alias admission currently colocated at component_manifest.rs:257-276 remains mandatory for every role: form the name/alias set without reading commands for closure-only roles, reject duplicate keys and reserved-list collisions, and check live-name collisions against a different (stableId, provenance); analyzer also includes its mounted-root aliases as before. The executable-entrypoint check (line 337) applies to role analyzer only, while a closure-only entrypoint must name a regular-file entry directly (no symlink resolution); the closure-only roles require capabilities [] and permissions [].
~~~

At `README.md:179`, replace the complete bullet with:

~~~text
- separates component-name and manifest-alias admission from command-tree validation. The name/alias checks currently at `component_manifest.rs:257-276` remain mandatory for every role, including reserved-list refusal and the existing different-`(stableId, provenance)` live-name collision rule. Only command-tree validation requires `commands`, which the schema guarantees exactly for `analyzer`; analyzer retains mounted-root alias checks;
~~~

At `README.md:221`, replace the complete indented sentence with:

~~~text
  Command-tree validation never runs on a manifest without `commands`. Component-name and manifest-alias admission still runs for every role without reading an absent tree.
~~~

Immediately after CR-T8, add:

~~~text
- **CR-T9.** For every role, component-name and manifest-alias admission remains enforced independently of command-tree presence. A component name or alias colliding with the reserved list refuses RJ-2; an alias duplicating the component name refuses RJ-2; a name or alias colliding with a live entry of a different `(stableId, provenance)` refuses RJ-2. The same-`(stableId, provenance)` coexistence control still admits when all other rules pass. Closure-only controls have no `commands`; analyzer controls retain their required tree and mounted-root alias checks.
~~~

Emit the exact map string from `evidence/build_cr_1.py` and rebuild/repin the affected subject members. No schema amendment or extra parent override is required. C2a must demonstrate the separation in full host admission and inventory-body validation; these are future implementation controls, not a request to execute product code in this round.

## Resolution of the r1 items

**RF-CR1-1: RESOLVED.** LD-8 is a sound alternative to the offered inert-metadata repair. The selected schema, SL:70 and DR103 fields/8 semantics all require `commands` absent for closure-only roles. A complete lawful grammar manifest has no mandatory root-command claim. A declared tree remains refused through RJ-6 and the stated D4 route. The semantics override explicitly qualifies the inherited `required: true` boolean; the executable copy implements that exception.

The analyzer branch retains its existing tree requirements. The prior M3-D EE-3b/EE-5a issue is disclosed in the cross-law paragraph and remains M3-D's to resolve. CR-1 does not newly change analyzer admission on that point.

**NB-CR1-1: RESOLVED.** LD-9, SL:70 and CR-T4 correctly distinguish direct regular-file entrypoints for closure-only roles from the existing analyzer in-tree resolution and executable-target check.

## Other requested judgments

The `oneOf` shape is sound. Required role makes the two branches disjoint. Analyzer requires its non-empty array, with the root preserving the 4,096 maximum and CommandSpec constraints. For a closure-only role, a present `commands` must simultaneously be an array under the root and null under its branch; no value satisfies both. Absence is the only valid spelling. This is a minimal expression within the generator's supported keyword subset.

The supplied independent audit reproduced all 11,010 parent-fixture verdicts, found no copy/parent flips, and reproduced all 100 role variants on five valid bases. This is sufficient evidence for the stated existing-case result, supported by the schema reasoning. It does not validate semantic admission or generated Rust execution.

Static generator inspection confirms optional-property `is_none_or`, exactly-one counting for `oneOf`, and the null-type predicate. The recorded root/role/branch changes are consistent with that generator. The materialization instructions need RF-CR1-2's correction because command-tree absence does not remove component-name custody.

The full nine-member r1-to-r2 diff was reviewed; the two new evidence members were read. Changes match the declared amendments, evidence/control additions, base and reviewer-path refresh, and both-order verifier support. The role-to-kind table and remaining rules are preserved.

Initial product HEAD was `cd5958b3608f44a0035566c9d4500e5005c62e91`. Seven schema/input/generator/generated-shape/owner/fixture files were independently byte-compared between `9c11c53` and `cd5958b` and are identical. The prior accepted mechanics remain valid at the newer base. The incomplete new presence-gate instruction is the substantive issue.

## Evidence and limits

Initially all 50 supplied pins, all 11 subject members and all nine frozen r1 members matched. CR-1's subject bytes remained unchanged at final validation. Local evidence is in `pin-audit.json`, `diff-summary.json` and `r1-r2.diff`.

Each of the eight initial allowed evidence checks was run once. Three verifier checks were refreshed only after external bytes changed:

| Check | Result | Local log |
|---|---|---|
| Independent schema audit | Identical; 11,010 cases, 100 variants | `schema-audit.log` |
| Builder with `--check` | Identical, including excluded unit draft | `build-check.log` |
| Content checker, current base | Pass | `content-check-current.log` |
| Content checker, `9c11c53` | Pass | `content-check-r1-base.log` |
| Scratch verifier, `cd5958b` | Pass; 82 to 83 successors | `verify-base.log` |
| Scratch verifier, CRC-1 then CR-1 | Pass; 82 to 84 | `verify-after-crc.log` |
| Scratch verifier, CR-1 then CRC-1 | Pass; 82 to 84 | `verify-before-crc.log` |
| Scratch verifier, checkout | Pass; 40 generation sources, 48 admission sources, 15 aliases | `verify-checkout.log` |
| Refreshed CRC-1 then CR-1, frozen base | Pass; 82 to 84 | `verify-after-crc-refresh.log` |
| Refreshed CR-1 then CRC-1, frozen base | Pass; 82 to 84 | `verify-before-crc-refresh.log` |
| Refreshed checkout after CRC-1 binding | Pass; 83 to 84; 40/48 sources, 15 aliases | `verify-checkout-refresh.log` |

The verifier kept inventory v134 and 55 inheritance rows unchanged, with four CR-1 passage overrides and no supersessions. Initial joint runs used CRC-1 subject `e030a1cf5031c7ece420b54663415cae69a7db1a55937130be91281408437728`. At final validation that explicitly mutable sibling subject had advanced to `ec89680137ed0ad29af1d2b3b955eff763a184c5314387f2fa83b67da14433bc`, with successor `29df5f5e2b145daf3c9b8e231ccac1d08c5b36d2eb006fbdc3bba543d7084166`, and product HEAD advanced to `392499e3a42ab9f45d517b8c267a83031abf3863` in the CRC-1 binding commit (83 successors). Both frozen-base joint-order checks and the checkout check were refreshed and pass. `refresh-context.json` records these external pins. The lead-only harness against frozen CRC-1 r2 bytes was not rerun. Synthetic reviews and assents establish verifier well-formedness, not actual acceptance or root assent.

Repositories remained read-only. No delegation, cargo, builds, tests, generator execution, crash-matrix commands or commits occurred. Commands used `nice -n 19`; evidence Python used the requested interpreter with `-I -B`. Offline jsonschema dependencies and every write are confined to this review directory. Neither the protected OpenSIP home nor the private 413 fixture was accessed.
