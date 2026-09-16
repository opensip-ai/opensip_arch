"""Phase B: the TS/JS unitKind law in its normative owner, the owner projection in the native model, and the closure check
in enumeration admission (existing internal key ENUMERATION_MEMBERSHIP_ORDER). No schema document bytes change.
usage: python -I -B apply_fix.py"""
import json, sys
sys.path.insert(0, '/private/tmp/opensip-design-corrections/claude-tsjs-unitkind-author.v1/tools')
from textedit import apply_all  # noqa: E402

MD = 'docs/v2/contracts/product-v1/native-evidence.md'
NVM = 'docs/coop/design-corrections/native/native_evidence_model.v2.py'
ENUM = 'docs/coop/design-corrections/foundation/enumeration_model.v1.py'

rows = apply_all('phase B: TS/JS unitKind law, owner projection and closure check', [
    (MD, [
        ('''whose mode is U-1's, and whose `recognizerId` is''',
         '''whose mode is U-1's, whose `unitKind` is `ts-program`
     exactly when that mode is `ts-tsconfig` and `js-program` when it is `js-allowjs` or
     `js-synthesized` (so a `tsconfig.json` marker with effective `allowJs=true` is a
     `js-program` unit; the kind follows the mode, never the marker file name), and whose
     `recognizerId` is'''),
        ('''out-of-order, duplicated or mis-numbered units or rows and mismatched
     projections refuse `ENUMERATION_MEMBERSHIP_ORDER`''',
         '''out-of-order, duplicated or mis-numbered units or rows, mismatched
     projections, a `tsjs` unit whose `unitKind` is not the projection of its mode in 2
     above, and a `ts-program`/`js-program` kind on a unit of another family refuse
     `ENUMERATION_MEMBERSHIP_ORDER`'''),
    ]),
    (NVM, [
        ('''FAMILY_MARKERS = {"rust": ["Cargo.toml"], "tsjs": ["tsconfig.json", "jsconfig.json", "package.json"]}
''', '''FAMILY_MARKERS = {"rust": ["Cargo.toml"], "tsjs": ["tsconfig.json", "jsconfig.json", "package.json"]}
# native-evidence section 1.4 U-4b.2: a tsjs unit's unitKind is a function of its languageMode alone. It enters PlanId
# through UnitMembershipV1.membershipDigest; enumeration admission re-derives it (ENUMERATION_MEMBERSHIP_ORDER).
TSJS_UNIT_KIND = {"ts-tsconfig": "ts-program", "js-allowjs": "js-program", "js-synthesized": "js-program"}
'''),
        ('''                              "unitKind": "ts-program" if mode == "ts-tsconfig" else "js-program",
''', '''                              "unitKind": TSJS_UNIT_KIND[mode],
'''),
    ]),
    (ENUM, [
        ('''      path (so no duplicate); unsupportedFiles and outsideBoundaryFiles exactly the row-order projections.
''', '''      path (so no duplicate); unsupportedFiles and outsideBoundaryFiles exactly the row-order projections; every tsjs
      unit's unitKind the U-4b.2 projection of its languageMode (NV.TSJS_UNIT_KIND) and no TS/JS kind on another family.
'''),
        ('''        for u in units:
            roots = [r.encode("utf-8") for r in u["memberPackageRoots"]]
            if any(not a < b for a, b in zip(roots, roots[1:])):
                _add(faults, "ENUMERATION_MEMBERSHIP_ORDER")
''', '''        for u in units:
            roots = [r.encode("utf-8") for r in u["memberPackageRoots"]]
            if any(not a < b for a, b in zip(roots, roots[1:])):
                _add(faults, "ENUMERATION_MEMBERSHIP_ORDER")
            if u["languageFamily"] == "tsjs":
                if u["unitKind"] != NV.TSJS_UNIT_KIND.get(u["languageMode"]):
                    _add(faults, "ENUMERATION_MEMBERSHIP_ORDER")
            elif u["unitKind"] in NV.TSJS_UNIT_KIND.values():
                _add(faults, "ENUMERATION_MEMBERSHIP_ORDER")
'''),
    ]),
])
print(json.dumps(rows, indent=1))
