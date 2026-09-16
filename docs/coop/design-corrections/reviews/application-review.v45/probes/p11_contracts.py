import re, os
C = '/tmp/opensip-design-corrections/candidate-subject.v45/'
O = '/private/tmp/opensip-design-corrections/application-review.v45/probes/sections/'
os.makedirs(O, exist_ok=True)
docs = {
 'adm': 'docs/v2/contracts/product-v1/admission-and-qualification.md',
 'sec': 'docs/v2/contracts/product-v1/security-and-lifecycle.md',
 'ide': 'docs/v2/contracts/product-v1/identity-and-evidence.md',
 'nat': 'docs/v2/contracts/product-v1/native-evidence.md',
 'wf': 'docs/v2/contracts/product-v1/workflows-and-surfaces.md',
 'f02': 'docs/v2/architecture/02-distribution-and-components.md',
 'f05': 'docs/v2/architecture/05-v1-to-v2-relationship.md',
}
for k, p in docs.items():
    lines = open(C + p, encoding='utf-8').read().splitlines()
    heads = [(i, l) for i, l in enumerate(lines) if re.match(r'^#{1,4} ', l)]
    with open(O + k + '.headings.txt', 'w') as f:
        for i, l in heads: f.write('%d\t%s\n' % (i + 1, l))
    print(k, p, 'lines', len(lines), 'headings', len(heads))
def section(k, pattern, out):
    lines = open(C + docs[k], encoding='utf-8').read().splitlines()
    start = None; level = None
    for i, l in enumerate(lines):
        mm = re.match(r'^(#{1,6}) ', l)
        if start is None and mm and re.search(pattern, l):
            start = i; level = len(mm.group(1)); continue
        if start is not None and mm and len(mm.group(1)) <= level:
            open(O + out, 'w').write('\n'.join('%d: %s' % (j + 1, lines[j]) for j in range(start, i)))
            print('section', k, pattern, start + 1, i); return
    if start is not None:
        open(O + out, 'w').write('\n'.join('%d: %s' % (j + 1, lines[j]) for j in range(start, len(lines))))
        print('section', k, pattern, start + 1, 'EOF')
    else:
        print('NOT FOUND', k, pattern)
section('adm', r'^#+ (§\s*)?5\b|^#+ 5\.', 'adm5.txt')
section('sec', r'S16\b', 'secS16.txt')
section('sec', r'S9\.1\b', 'secS9.1.txt')
section('f05', r'[Mm]igration constraints', 'f05migration.txt')
section('f02', r'[Cc]urrent V1 product boundary', 'f02boundary.txt')
section('adm', r'^#+ (§\s*)?2\b|^#+ 2\.', 'adm2.txt')
section('adm', r'^#+ (§\s*)?3\b|^#+ 3\.', 'adm3.txt')
