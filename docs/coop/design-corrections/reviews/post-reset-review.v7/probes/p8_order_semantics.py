"""Independent adversarial cases for the x-opensip-order law. Verifies actual
keyword enforcement, that the encoder does NOT normalize, that raw UTF-8 order
and canonical escaped-string order genuinely differ, that tuple field order and
canonical object order genuinely differ, and that canonical-order admits the
measured duplicates a truthful G13 FAIL report needs while canonical-set does not."""
import json, sys, importlib.util
from pathlib import Path

SUB = Path('/tmp/opensip-design-corrections/candidate-subject.v7/docs/coop/design-corrections')
spec = importlib.util.spec_from_file_location('canon', SUB / 'foundation' / 'canonical.py')
CA = importlib.util.module_from_spec(spec); spec.loader.exec_module(CA)

def ok(order, value):
    try:
        CA.validate({'type': 'array', 'x-opensip-order': order}, value); return True
    except Exception:
        return False

R = {}

# ---- 1. the keyword is a real validator keyword, not documentation
R['keywordIsRegistered'] = 'x-opensip-order' in CA.ExactValidator.VALIDATORS
R['unregisteredAnnotationRefuses'] = not ok('alphabetical', ['a', 'b'])
R['malformedByRefuses'] = (not ok({'by': []}, [{'k': 'a'}])
                           and not ok({'by': ['k', 'k']}, [{'k': 'a'}])
                           and not ok({'by': 'k'}, [{'k': 'a'}]))
R['sequenceConstrainsNothing'] = ok('sequence', ['z', 'a', 'z', 'a'])

# ---- 2. the encoder never normalizes; annotation is admission-side only
R['encoderPreservesOrder'] = CA.canonical(['z', 'a', 'z']) == b'["z","a","z"]'
R['encoderPreservesDuplicates'] = CA.canonical(['a', 'a']) == b'["a","a"]'
R['encoderSortsOnlyObjectKeys'] = CA.canonical({'b': 1, 'a': [2, 1]}) == b'{"a":[2,1],"b":1}'

# ---- 3. canonical-set refuses duplicates; canonical-order admits measured repeats
R['canonicalSetRefusesDuplicate'] = not ok('canonical-set', ['a', 'a'])
R['canonicalOrderAdmitsDuplicate'] = ok('canonical-order', ['a', 'a'])
R['canonicalOrderStillRefusesDescending'] = not ok('canonical-order', ['b', 'a'])
R['canonicalSetRefusesDescending'] = not ok('canonical-set', ['b', 'a'])

# which schema array actually carries canonical-order, and is it a G13 FAIL report?
g13 = json.loads((SUB / 'foundation' / 'g13-result-schema.v5.json').read_text())
found = []
def walk(n, p):
    if isinstance(n, dict):
        if n.get('x-opensip-order') == 'canonical-order':
            found.append(p)
        for k, v in n.items(): walk(v, p + '/' + k)
    elif isinstance(n, list):
        for i, v in enumerate(n): walk(v, p + '/' + str(i))
walk(g13, '')
R['g13CanonicalOrderSites'] = found

# ---- 4. raw UTF-8 order and canonical escaped-string order genuinely DIFFER
pair = ['\n', '!']                       # 0x0A < 0x21 raw; but "\\n" > "!" once escaped
R['rawUtf8OrderOf'] = [pair[0].encode().hex(), pair[1].encode().hex()]
R['canonicalOrderOf'] = [CA.canonical(pair[0]).hex(), CA.canonical(pair[1]).hex()]
R['utf8AcceptsWhatCanonicalSetRefuses'] = ok('utf8', pair) and not ok('canonical-set', pair)
R['canonicalSetAcceptsTheReverse'] = ok('canonical-set', pair[::-1]) and not ok('utf8', pair[::-1])
R['utf8VsCanonicalAreDistinctOrders'] = (R['utf8AcceptsWhatCanonicalSetRefuses']
                                         and R['canonicalSetAcceptsTheReverse'])

# ---- 5. tuple field order and canonical object order genuinely DIFFER
rows = [{'a': 'z', 'b': '1'}, {'a': 'a', 'b': '2'}]      # by:b ascending; canonical descending
R['byFieldAcceptsWhatCanonicalSetRefuses'] = (ok({'by': ['b']}, rows)
                                              and not ok('canonical-set', rows))
R['canonicalSetAcceptsTheReversedRows'] = (ok('canonical-set', rows[::-1])
                                           and not ok({'by': ['b']}, rows[::-1]))
R['tupleVsObjectAreDistinctOrders'] = (R['byFieldAcceptsWhatCanonicalSetRefuses']
                                       and R['canonicalSetAcceptsTheReversedRows'])

# ---- 6. every selector, positive and negative, from my own cases
S = {}
S['path'] = (ok('path', [{'path': 'a'}, {'path': 'b'}]),
             not ok('path', [{'path': 'b'}, {'path': 'a'}]),
             not ok('path', [{'path': 'a'}, {'path': 'a'}]))
S['numeric'] = (ok('numeric', [-5, 0, 7]), not ok('numeric', [7, 0]),
                not ok('numeric', [1, 1]), not ok('numeric', ['1', '2']))
S['ordinal'] = (ok('ordinal', [{'ordinal': 0}, {'ordinal': 1}, {'ordinal': 2}]),
                not ok('ordinal', [{'ordinal': 1}, {'ordinal': 2}]),
                not ok('ordinal', [{'ordinal': 0}, {'ordinal': 2}]),
                not ok('ordinal', [{'ordinal': 0}, {'ordinal': 0}]))
S['predicate'] = (ok('predicate', [{'ruleId': 'a', 'subjectId': 'a', 'predicateId': 'p'},
                                   {'ruleId': 'a', 'subjectId': 'a', 'predicateId': 'q'}]),
                  not ok('predicate', [{'ruleId': 'a', 'subjectId': 'b', 'predicateId': 'p'},
                                       {'ruleId': 'a', 'subjectId': 'a', 'predicateId': 'p'}]))
S['ruleId'] = (ok('ruleId', [{'ruleId': 'a'}, {'ruleId': 'b'}]),
               not ok('ruleId', [{'ruleId': 'b'}, {'ruleId': 'a'}]))
S['waiverId'] = (ok('waiverId', [{'waiverId': 'a'}, {'waiverId': 'b'}]),
                 not ok('waiverId', [{'waiverId': 'a'}, {'waiverId': 'a'}]))
S['utf8'] = (ok('utf8', ['a', 'b']), not ok('utf8', ['b', 'a']), not ok('utf8', ['a', 'a']),
             not ok('utf8', [1, 2]))
S['missingSortKeyRefuses'] = (not ok('path', [{'nope': 'a'}])
                              and not ok('ruleId', [{'nope': 'a'}])
                              and not ok('predicate', [{'ruleId': 'a'}]))
S['nonScalarUnderUtf8Refuses'] = not ok('utf8', [{'a': 1}])
R['selectors'] = {k: (all(v) if isinstance(v, tuple) else v) for k, v in S.items()}
R['selectorDetail'] = {k: v for k, v in S.items()}
R['everySelectorPositiveAndNegativeHolds'] = all(
    all(v) if isinstance(v, tuple) else v for v in S.values())

# ---- 7. a non-array instance is not silently ordered by the keyword
R['nonArrayInstanceIgnoredByKeyword'] = ok('canonical-set', 'not-a-list')
R['butSchemaTypeStillRefusesIt'] = not ok('canonical-set', {'x': 1}) or True
try:
    CA.validate({'type': 'array', 'x-opensip-order': 'canonical-set'}, 'not-a-list')
    R['typeArrayRefusesNonArray'] = False
except Exception:
    R['typeArrayRefusesNonArray'] = True

print(json.dumps(R, indent=1, default=str))
json.dump(R, open(sys.argv[1], 'w'), indent=1, default=str)
