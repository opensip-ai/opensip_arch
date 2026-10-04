"""Read-only content checks of contract successor SD-5. Run with python3 -I -B; it writes nothing. It reads
the architecture repository and, through read-only `git show`, the product's common-v4 schema at LOCK_REV.

1. Shape and pins: one parent (NE at its accepted bytes), exactly one override, NE:3540, whose `after` is the
   exact accepted line, a newline and one table row with the table's five columns; candidates equal the
   subject members other than the record.
2. Existing codes only: the class, error code and detail are members of the D9 v1.14 vocabulary, its
   extension-admission-rejected golden, the public detail registry, security S12's admission row and the
   product's DomainDetailCode enum. Every code-shaped token in the row is an existing member; nothing new.
3. Remedy and subject: ASCII, within BoundedText's 1024, the remedy names a next step true for every class.
4. Distinct from the not-installed golden: J1 r4 row 27 (indeterminate 3), WS:1374 and WSE:1447 carry
   COVERAGE.PROVIDER_UNAVAILABLE and COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED; the new row's class, error
   code and detail are all different, and its text states the boundary between the two.
5. The source: M3-D r3 item 24's four classes, as represented there, appear in the row; M3-D's SD-5 row and
   M3-J1 r4's R10a route and S20 read as README cites them."""
import hashlib, json, re, subprocess
from pathlib import Path

A = Path(__file__).resolve().parents[6]
PRODUCT = Path('/Users/sb/code/opensip-ai/opensip')
LOCK_REV = 'cd5958b'
B = 'docs/implementation/m3/supervisor-d/'
D = B + 'sd-5/'
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
SL = 'docs/v2/contracts/product-v1/security-and-lifecycle.md'
WS = 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
WSE = 'docs/implementation/m1/source-selection-v2/reference/effective-workflows-and-surfaces.md'
D9 = 'docs/coop/artifacts/d9-exit-contract.v1.14.json'
REG = 'docs/coop/design-corrections/public-detail-registry.v1.json'
MD = B + 'PROPOSAL-r3.md'
MJ = 'docs/implementation/m3/host-pipeline-j/PROPOSAL-r4.md'


def raw(p):
    return (A / p).read_bytes()


def pin(p):
    b = raw(p)
    return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def text(p):
    return raw(p).decode('utf-8')


checks = []

# 1. shape and pins
record = json.loads(raw(D + 'successor.json'))
subject = json.loads(raw(B + 'sd-5-subject.json'))
assert set(record) == {'schemaVersion', 'standing', 'parents', 'passageOverrides', 'candidates'}
assert record['parents'] == [pin(NE)] and pin(NE)['sha256'].startswith('83b99783')
for row in record['candidates'] + subject['files']:
    assert pin(row['path']) == row, row['path']
assert {r['path'] for r in record['candidates']} == {r['path'] for r in subject['files']} - {D + 'successor.json'}
[o] = record['passageOverrides']
lines = text(NE).splitlines()
assert o['parent'] == pin(NE) and o['selector'] == {'line': 3540} and o['before'] == lines[3539]
first, row = o['after'].split('\n')
assert first == o['before'] and row.startswith('| **component manifest that is an excluded form**') and row.endswith(' |')
assert row.count('|') == lines[3522].count('|') == 6 and lines[3522].startswith('| Condition |')
cells = [c.strip() for c in row.split('|')[1:-1]]
assert cells[1] == '' and cells[2] == '`request-rejected` (2)' and cells[3] == '`EXTENSION.ADMISSION_REJECTED`'
assert cells[4].startswith('`PAYLOAD-NOT-ADMISSIBLE`')
assert lines[3540].startswith('| **producer Coverage cause/carrier refusal**'), 'NE:3541 follows the new row unchanged'
checks.append('shape: 1 parent, 1 override (NE:3540): the accepted row, then one five-column row; '
              'class request-rejected (2), code EXTENSION.ADMISSION_REJECTED, detail PAYLOAD-NOT-ADMISSIBLE')

# 2. existing codes only
d9 = json.loads(raw(D9))
assert 'EXTENSION.ADMISSION_REJECTED' in d9['codeVocabulary']['errorCodes']
assert d9['codeMaps']['rejectionCauseToErrorCode']['extension-admission-rejected'] == 'EXTENSION.ADMISSION_REJECTED'
golden = next(g for g in d9['goldenCases'] if g['id'] == 'extension-admission-rejected')
assert golden['expectedTermination'] == {'class': 'request-rejected', 'errorCode': 'EXTENSION.ADMISSION_REJECTED'}
assert golden['scenario'] == 'extension signature, compatibility, or requested capability is rejected'
reg = json.loads(raw(REG))
codes = {r['code'] for r in reg['records']}
assert 'PAYLOAD-NOT-ADMISSIBLE' in codes and 'COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED' in codes
common4 = json.loads(subprocess.run(['git', '-C', str(PRODUCT), 'show', LOCK_REV + ':schemas/sources/common-v4.schema.json'],
                                    check=True, capture_output=True).stdout)
product_codes = set(common4['$defs']['DomainDetailCode']['enum'])
assert 'PAYLOAD-NOT-ADMISSIBLE' in product_codes
sl = text(SL).splitlines()
assert sl[1305].startswith('| `PAYLOAD-NOT-ADMISSIBLE` (incl. `ROOT.*`, `ENVELOPE.*`, `PROFILE_SET.*` details)')
assert sl[1305].endswith('| request-rejected / 2 / `EXTENSION.ADMISSION_REJECTED` |')
known = codes | product_codes | set(d9['codeVocabulary']['errorCodes']) | {'COVERAGE.PROVIDER_UNAVAILABLE'}
tokens = set(re.findall(r'`([A-Z][A-Z0-9_-]*(?:\.[A-Z0-9_]+)+|[A-Z][A-Z0-9]*(?:-[A-Z0-9]+){2,})`', row))
assert tokens and tokens <= known, tokens - known
assert 'COVERAGE.PROVIDER_UNAVAILABLE' in d9['codeVocabulary']['reasonCodes']
checks.append('existing codes only: %s are members of the D9 v1.14 vocabulary, the public detail registry or '
              'the product DomainDetailCode enum at %s; golden extension-admission-rejected is request-rejected / '
              'EXTENSION.ADMISSION_REJECTED; SL:1306 routes PAYLOAD-NOT-ADMISSIBLE there' % (sorted(tokens), LOCK_REV))

# 3. remedy and subject
remedy = re.search(r'remedy "([^"]*)"', row).group(1)
assert remedy.isascii() and len(remedy) <= 1024
for phrase in ('first-party or explicitly trusted', 'policy, persistence, rendering, termination or host-lifecycle '
               'authority', 'untrusted native or WASM code', 'project hook, root command or probe',
               'Remove the component, or install its first-party release.'):
    assert phrase in remedy, phrase
assert '`excluded-form:<class>:<manifestDigest>`' in row and len('excluded-form:EE-3b:') + 64 <= 1024
checks.append('remedy: %d ASCII characters, one next step per class (EE-1, EE-3b, EE-4, EE-5a); subject at most '
              '%d characters' % (len(remedy), len('excluded-form:EE-3b:') + 64))

# 4. distinct from row 27
mj = text(MJ).splitlines()
assert mj[672].startswith('| 27 | Required provider closure not installed, or not admissible (including ephemeral with no '
                          'trust, E-3) | indeterminate / 3 | — | `COVERAGE.PROVIDER_UNAVAILABLE`; '
                          '`COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` | runId if committed | WS:1374; NE:3370 |')
golden_row = ('| required provider closure not installed | indeterminate 3 | `COVERAGE.PROVIDER_UNAVAILABLE` | '
              '`COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` → `opensip install provider-typescript` |')
assert text(WS).splitlines()[1373] == golden_row and text(WSE).splitlines()[1446] == golden_row
assert 'indeterminate' not in cells[2] and 'COVERAGE.PROVIDER_UNAVAILABLE' not in (cells[3] + cells[4])
assert 'COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED' not in cells[4]
for phrase in ('never a `provider-unavailable` deficiency and never the not-installed golden of workflows §9',
               'is never an excluded form and keeps that golden', 'no runId and no executionId',
               'before any analysis attempt\'s `ExecutionId` is drawn or reserved, on the durable and the ephemeral path'):
    assert phrase in row, phrase
checks.append('distinct from J1 r4 row 27 (MJ:673) and its golden (WS:1374, WSE:1447): different class, code and '
              'detail, no runId, and the boundary is stated in the row')

# 5. the source laws
md = text(MD)
assert hashlib.sha256(raw(MD)).hexdigest().startswith('9679dbc4')
for s in ('a manifest whose authenticated publisher is neither first-party nor on the explicit-trust list',
          'a `commands` entry for role `analyzer`, or a capability outside the native capability matrix\'s provider capabilities',
          'a manifest requesting admission of untrusted native or WASM code',
          'a manifest claiming a project hook, root command or contribution-granted probe',
          '**Internal refusal:** `ExcludedForm {class, subject}`. **Public projection** is J1\'s, with existing codes (SD-5).',
          '| SD-5 | **J1\'s projections** | J1 law content (no new code) |'):
    assert s in md, s
for s in ('a `commands` entry for role `analyzer`, or a capability outside the native capability matrix\'s provider capabilities',
          'untrusted native or WASM code', 'project hook, root command or contribution-granted probe',
          'a publisher neither first-party nor explicitly trusted'):
    assert s in row, s
mjt = text(MJ)
assert hashlib.sha256(raw(MJ)).hexdigest().startswith('c18c0d3c')
for s in ('| S20 | **M3D\'s SD-5, for R10a\'s route (r4, record)** |',
          'Its public projection is J1\'s, with existing codes, under M3D\'s successor SD-5 (S20).',
          '- **Totality.** J2a\'s projection is an exhaustive match with no wildcard arm (X7 item 8).'):
    assert s in mjt, s
checks.append('M3-D r3 (9679dbc4) item 24 classes, SD-5 row; M3-J1 r4 (c18c0d3c) R10a route, S20 and totality, as cited')
print(json.dumps({'passed': True, 'checks': checks}, indent=1, ensure_ascii=False))
