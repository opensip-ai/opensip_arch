"""P9: is there published law on whether an UNSUPPORTED-TYPED capability may be SELECTED and
mint Coverage? And does anything require unreferenced Coverage to be accounted?"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT32 = '/tmp/opensip-design-corrections/candidate-subject.v32'

TARGETS = [
    'docs/v2/contracts/product-v1/native-evidence.md',
    'docs/coop/design-corrections/native/native-capability-matrix.v2.json',
    'docs/coop/design-corrections/native/native-evidence.schemas.v2.json',
    'docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md',
    'docs/coop/design-corrections/foundation/enumeration-contract.v1.md',
    'docs/v2/contracts/product-v1/admission-and-qualification.md',
]

out = {'searches': []}


def show(label, pattern, files=TARGETS, window=2):
    rx = re.compile(pattern, re.I)
    hits = []
    print('\n=== %s' % label)
    for rel in files:
        p = os.path.join(ROOT32, rel)
        if not os.path.exists(p):
            continue
        text = open(p, encoding='utf-8', errors='ignore').read()
        lines = text.split('\n')
        for m in rx.finditer(text):
            ln = text[:m.start()].count('\n') + 1
            chunk = ' '.join(l.strip() for l in lines[max(0, ln - 1): ln + window])
            hits.append({'file': rel, 'line': ln, 'text': chunk[:700]})
            print('  %s:%d' % (rel, ln))
            print('     %s' % chunk[:560])
    out['searches'].append({'label': label, 'pattern': pattern, 'hits': hits})
    return hits


show('UNSUPPORTED-TYPED is answered / minted coverage',
     r'UNSUPPORTED-TYPED[^\n]{0,80}(admitted|answered|lawful|included|refuses)')
show('unsupportedTypedIsNotOnThisTable full text',
     r'unsupportedTypedIsNotOnThisTable')
show('may an unsupported capability be requested/selected',
     r'(request|selected|requestedCapabilit)[^\n]{0,120}UNSUPPORTED-TYPED')
show('NOT-SELECTED vs UNSUPPORTED distinction',
     r'NOT-SELECTED')

# the exact native sentence about what an UNSUPPORTED-TYPED cell yields
p = os.path.join(ROOT32, 'docs/v2/contracts/product-v1/native-evidence.md')
text = open(p, encoding='utf-8', errors='ignore').read().split('\n')
for ln in (155, 534, 830, 905, 3183):
    print('\n--- native-evidence.md:%d' % ln)
    print('\n'.join(text[ln - 2: ln + 6]))
    out.setdefault('nativeExcerpts', {})[str(ln)] = '\n'.join(text[ln - 2: ln + 6])

json.dump(out, open(os.path.join(HERE, 'p9-selection-law.json'), 'w'), indent=2)
print('\nWROTE p9-selection-law.json')
