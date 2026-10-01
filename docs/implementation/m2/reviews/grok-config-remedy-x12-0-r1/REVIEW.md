# Review: CONFIG.INVALID remedy text X12-0 r1

Verdict: ACCEPT-DESIGN-UNIT.

Subject manifest `docs/implementation/m2/config-remedy-x12-0-subject.json` is 1028 bytes, sha256 `7d4401110febd88b9a6740f3d48d09362db929c0550062f39e19786f460fd674`. Successor `docs/implementation/m2/config-remedy-x12-0/successor.json` is 3759 bytes, sha256 `469317223374f351bdecf24c9054f864a3249c6d23e613a605e637b72d4fd3c4`. README, `build_x12_0.py`, `check_remedy.py`, and `verify_scratch.py` match that manifest and hashes.txt. The product checkout is `b642c45a77cf38a0ab8ebf949548ce4eca1f410d`, with a clean work tree. `~/Library/Application Support/OpenSIP` is absent. No product cargo.

## The string

The widened remedy is 367 ASCII characters:

> the configured capability or policy selection is invalid: for capabilities, name a registered capability id from the native capability matrix, and state at most one row per (capabilityId, languageMode, workspaceRoot); for policy, name exactly one bundled policy pack id, written exactly as name:version, and supply no policy document of your own or from a third party

It stays true for each key that reaches `CONFIG.INVALID`:

- `native.requested-capability-unregistered`, `-mode-unregistered`, and `-duplicate-ownership-tuple` keep the published capability sentence: name a registered capability id from the native capability matrix, and state at most one row per `(capabilityId, languageMode, workspaceRoot)`. The policy instructions sit in the `for policy` clause.
- Row 1, an unregistered id (bare name, `:01`, uppercase, trailing whitespace, and, in M2, any named id): name exactly one bundled policy pack id, written exactly as `name:version`.
- Row 1, `count:<n>`: name exactly one.
- Row 2, a supplied pack of either provenance: supply no policy document of your own or from a third party.
- Row 3a, a supplied document that fails lexical or schema admission: the same sentence. A supplied document is refused whatever its bytes.

Item 7's three substance requirements are in the string: the capability sentence, exactly one bundled pack id, and no policy document of your own. The `name:version` form and the third-party limb are true additions. Row 3 keeps detail `POLICY.IMPERATIVE_KEY_REFUSED` and its own remedy. Row 4 is the host-invariant row. The public code stays `CONFIG.INVALID`.

The bytes stand.

## Copies

Both live table rows are overridden, both at line 1158, with the same before and after text:

- `docs/coop/design-corrections/native/native_evidence_model.v2.py`, 319376 bytes, sha256 `7d1c0acf2c7d74e52c6570bba66dcb846c03710f64cb61a2c83bd1c39abab8be`
- `docs/implementation/m2/capability-totality-reference-selection-v1/reference/native_evidence_model.py`, 319944 bytes, sha256 `e6784aa1a595222cfd5a3da55e2beaa3d0839c878d67d6821297682089bde2b9`

`check_remedy.py` applied both overrides in memory, parsed each result with `ast`, and passed: one changed line, the same table keys and other values, both copies equal, the two check-identity remedy predicates, the X12 phrases, no `POLICY.` or `PACK.` in the string, ASCII, length 367.

A walk of the architecture tree found 140 files containing the old sentence. 130 sit under review trees. The accepted law (`PROPOSAL.md` and the preserved r2 and r3 texts), this unit's README, builder, and successor `before` fields quote the published sentence. The product tree has no copy of that sentence. `schemas/sources/native-v2.schema.json` `remedyKeyingConstraint` names the three capability keys, says one string must stay true, and says `THIS IS CURRENTLY SATISFIED`. That prose stays true after the widening. Generated `report.ts` embeds those schema bytes.

Two further copies are byte-identical to the v2 parent and pinned as trial inputs: `docs/implementation/m1/trials/interruption-envelope-06/subject/inputs/native_evidence_model.v2.py` and the envelope-07 twin. Each subject manifest and `input-pins.json` records 319376 bytes and sha256 `7d1c0acf2c7d74e52c6570bba66dcb846c03710f64cb61a2c83bd1c39abab8be`, sourced from the v2 parent. They are the trial subjects' frozen inputs. The selected reference remains the capability-totality copy.

The comment above the table (v2 lines 1149–1156) records the ownership-tuple widening and stays true.

## Judgment calls

1. Conditional wording holds. Each instruction stays with the selection it governs, and the capability sentence keeps its published words, so both check-identity predicates still match.
2. `written exactly as name:version` holds. Item 3's spelling is that form, and the bare-name, `:01`, uppercase, and trailing-whitespace cases of row 1 get a usable next step.
3. `of your own or from a third party` holds. `SuppliedProvenance` is `User` or `ThirdParty`.
4. Leaving row 3 out of this string holds. Row 3's detail is `POLICY.IMPERATIVE_KEY_REFUSED`.
5. Overriding both live copies holds. The review-tree copies and the two pinned trial inputs are frozen records of the parent bytes.
6. Leaving the product unchanged holds. No product file carries the remedy table. X12b embeds the string.
7. Leaving the comment and the constraint prose unchanged holds. Both remain true.
8. Line selectors hold. `verify_design.py` keeps `{"line": n}` for a text parent and refuses it when the parent decodes as JSON. source-selection-v3 overrides `workflows_model.v1.py` line 380 the same way.
9. Leaving `check-identity.py` unrun holds. The native model refuses this interpreter's Unicode case data. `check_remedy.py` checks the two remedy predicates without importing the model.

## Selection

`verify_scratch.py` ran the product checkout's `tools/verify_design.py` with X12-0 appended over the real lock and a synthetic in-memory review and assent. It passed: inventory v104 selected, 72 contract successors, 16 inheritance rows, 40 generation sources, 48 admission sources, 15 aliases. X12-0 was selected with two passage overrides. The directory `/Users/sb/code/opensip-ai/opensip-x12-0` is absent on this machine; the product checkout at `b642c45` is clean, and that is the tree the script checked. The script writes nothing. `build_x12_0.py` was left unrun.

The successor is schemaVersion 1, standing PROPOSED, with two pinned parents, two line overrides whose `before` text is the live line, and candidates that are the subject manifest's other files.

Required findings: none.
