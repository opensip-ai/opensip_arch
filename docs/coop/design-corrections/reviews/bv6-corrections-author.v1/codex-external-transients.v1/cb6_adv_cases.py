import json, pathlib, collections

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work/'
                 'docs/coop/design-corrections/native/native-cases.v2.json')
d = json.loads(P.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
cases = d['cases']
ids = {c['id'] for c in cases}


def OD(*pairs):
    return collections.OrderedDict(pairs)


def case(cid, kind, feedback, note, steps, expect):
    assert cid not in ids, cid
    return OD(('id', cid), ('kind', kind), ('feedback', list(feedback)), ('note', note),
              ('steps', steps), ('expect', expect))


new = []

# ---------------------------------------------------------------------------- CB6-ADV-1
new.append(case(
    'units-bare-js-directory-without-a-marker-is-not-a-unit',
    'negative', ['R1'],
    'CB6-ADV-1. Section 1.2 selects a MODE inside a unit; it does not discover one. Read alone, the '
    'js-synthesized recognition cell ("package.json present OR any .js file under the unit") looked '
    'like an independent test and would have minted a unit for a directory of bare .js files, '
    'changing membership and therefore the Plan. U-1 governs: with no tsconfig.json, no '
    'jsconfig.json and no package.json there is no tsjs unit for a .js file to be "under", and each '
    'such file is syntax-only / no-program-unit-for-language rather than a program member.',
    [OD(('fn', 'discover_units'), ('bind', 'u'), ('args', OD(('markers', {})))),
     OD(('fn', 'assign_membership'), ('bind', 'm'),
        ('args', OD(('units', '$u.units'), ('files', ['app/main.js', 'app/util.mjs']))))],
    OD(('$u.units', []),
       ('$m.rows.0.path', 'app/main.js'),
       ('$m.rows.0.languageFamily', 'tsjs'),
       ('$m.rows.0.unitOrdinal', None),
       ('$m.rows.0.membership', 'syntax-only'),
       ('$m.rows.0.reason', 'no-program-unit-for-language'),
       ('$m.rows.1.membership', 'syntax-only'),
       ('$m.erasedFiles', []))))

new.append(case(
    'units-the-same-js-files-under-a-package-json-marker-are-a-js-synthesized-program',
    'positive', ['R1'],
    'The positive half of the same boundary, so the clarification is not read as removing the mode: '
    'add the U-1 marker and the identical files become program members of one js-synthesized unit. '
    'The marker makes the unit; the .js files never did.',
    [OD(('fn', 'discover_units'), ('bind', 'u'),
        ('args', OD(('markers', OD(('app/package.json', OD(('sha256', 'e' * 64)))))))),
     OD(('fn', 'assign_membership'), ('bind', 'm'),
        ('args', OD(('units', '$u.units'), ('files', ['app/main.js', 'app/util.mjs'])))),
     OD(('fn', 'typescript_mode'), ('bind', 't'),
        ('args', OD(('listing', ['app/main.js', 'app/util.mjs']), ('unit_root', 'app'),
                    ('package_json', {}), ('tsconfig', None), ('jsconfig', None),
                    ('lockfiles', []), ('node_modules_in_read_set', False))))],
    OD(('$u.units.0.languageMode', 'js-synthesized'),
       ('$u.units.0.unitKind', 'js-program'),
       ('$u.units.0.markerPath', 'app/package.json'),
       ('$m.rows.0.membership', 'program-member'),
       ('$m.rows.1.membership', 'program-member'),
       ('$t.languageMode', 'js-synthesized'),
       ('$t.configOrigin', 'synthesized'))))

# ---------------------------------------------------------------------------- CB6-ADV-2
new.append(case(
    'confidence-v1-is-a-provider-emission-law-and-the-floor-fixture-is-not-provider-emission',
    'positive', ['F12'],
    'CB6-ADV-2. The scope of section 4.8\'s second clause. It is NOT narrowed to types@checked - '
    'that reading would be a WEAKENING, permitting a native clones or references provider to emit a '
    'fabricated percentage, which is exactly what 4.8 removed. It is a provider-emission law over '
    'the bundle: TypeDerivationV1 pins confidenceMillionths to the constant 1000000 and is the only '
    'record carrying confidenceMethod. Section 4.6 step 3 stays reachable because it compares '
    'ViewEntryV3.confidenceMillionths, whose domain is deliberately the wider 0..1000000 and which '
    'carries NO method, so an imported, non-native or defective contribution is still judged. The '
    'named regression fixture at 100000 is a hand-built EVALUATOR input, not a ViewEntryV3 and not '
    'provider emission - it fails ViewEntryV3 admission here - so it is no counterexample to the '
    'emission law and this contract claims no product emission of such a value.',
    [OD(('fn', 'types_fact_derivation'), ('bind', 'td'),
        ('args', OD(('subject_language', 'typescript'), ('has_annotation', True),
                    ('has_jsdoc', False), ('check_js', False)))),
     OD(('fn', 'types_fact_derivation'), ('bind', 'ti'),
        ('args', OD(('subject_language', 'javascript'), ('has_annotation', False),
                    ('has_jsdoc', False), ('check_js', True)))),
     OD(('fn', 'validate'), ('bind', 'bad'), ('expectError', 'confidenceMillionths'),
        ('args', OD(('def', 'TypeDerivationV1'),
                    ('value', OD(('derivationKind', 'compiler-inferred'),
                                 ('confidenceMillionths', 900000),
                                 ('confidenceMethod', 'native.confidence.v1'),
                                 ('checkJs', False), ('limitations', [])))))),
     OD(('fn', 'validate'), ('bind', 'fixture'), ('expectError', 'required'),
        ('args', OD(('def', 'ViewEntryV3'),
                    ('value', OD(('relation', 'clones'), ('resolution', 'normalized-body-hash'),
                                 ('coverage', 'complete'), ('confidenceMillionths', 100000)))))),
     OD(('fn', 'sufficiency_v2'), ('bind', 'floor'),
        ('args', OD(('req', OD(('relation', 'clones'), ('minResolution', 'normalized-body-hash'),
                               ('completeness', 'partial-ok'), ('quantifier', 'existential'),
                               ('minConfidenceMillionths', 900000))),
                    ('view', OD(('clones', OD(('resolution', 'normalized-body-hash'),
                                              ('coverage', 'complete'),
                                              ('confidenceMillionths', 100000))),
                                ('declares', OD(('resolution', 'syntactic'),
                                                ('coverage', 'complete')))))))),
     ],
    OD(('$td.confidenceMillionths', 1000000),
       ('$td.confidenceMethod', 'native.confidence.v1'),
       ('$ti.derivationKind', 'compiler-inferred'),
       ('$ti.confidenceMillionths', 1000000),
       ('$floor.satisfied', False),
       ('$floor.deficiency', 'confidence-floor-unmet'))))

cases.extend(new)
P.write_text(json.dumps(d, indent=1, ensure_ascii=True) + '\n', encoding='utf-8')
print('cases now', len(cases))
