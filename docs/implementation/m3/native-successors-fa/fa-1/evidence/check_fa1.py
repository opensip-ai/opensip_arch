"""Read-only content checks of native contract successor FA-1. Run with python3 -I -B; it writes nothing.
It reads the architecture repository only. It never imports or executes a reference model: the two native
model files are parsed with `ast`.

1. Shape and pins: one parent (NE at its accepted bytes), exactly the overrides NE:3529, NE:3849 and NE:3850,
   each `before` the exact parent line; candidates equal the subject members other than the record.
2. NE:3529 is insert-only and keeps the row's five cells; the new internal key occurs once in the
   effective NE and nowhere in the registered native bundle or the public detail registry (it is an
   internal key on an existing row, not a public code).
3. The effective fault-law paragraph no longer admits "facts before the terminal", names each retained
   selector, and every quoted selector resolves in delivery.v2 / rust-provider-protocol.v2 to the value the
   text gives. Only Complete carries factStreamCommitment in either protocol. NE never names those
   dispositions anywhere, so section 0 supersedes none of them.
4. StageAuthorityV1.factsAdmitted admits `none`, and the reference stage_authority (the B-S9 selected copy and
   the frozen v2 model) still returns `before-terminal` for the two terminals: the text's defect statement
   is accurate and its stated value is schema-valid.
5. The section 4.5 record laws quoted at NE:3529 are NE:2221-2222 and NE:2237-2239.
6. The source: M3-H r3's accepted bytes carry X-H2 and the FA-1 row exactly as README cites them."""
import ast, hashlib, json
from pathlib import Path

A = Path(__file__).resolve().parents[6]
B = 'docs/implementation/m3/native-successors-fa/'
D = B + 'fa-1/'
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
NES = 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
REG = 'docs/coop/design-corrections/public-detail-registry.v1.json'
DLV = 'docs/coop/artifacts/delivery.v2.json'
RPP = 'docs/coop/artifacts/rust-provider-protocol.v2.json'
MODELS = ['docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.py',
          'docs/coop/design-corrections/native/native_evidence_model.v2.py']
H3 = 'docs/implementation/m3/fact-admission-h/PROPOSAL-r3.md'
KEY = '`native.coverage-closed-world-mismatch`'


def raw(p):
    return (A / p).read_bytes()


def pin(p):
    b = raw(p)
    return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def at(doc, path):
    for k in path.split('.'):
        doc = doc[k]
    return doc


checks = []

# 1. shape and pins
record = json.loads(raw(D + 'successor.json'))
subject = json.loads(raw(B + 'fa-1-subject.json'))
assert set(record) == {'schemaVersion', 'standing', 'parents', 'passageOverrides', 'candidates'}
assert record['parents'] == [pin(NE)] and pin(NE)['sha256'].startswith('83b99783')
for row in record['candidates'] + subject['files']:
    assert pin(row['path']) == row, row['path']
assert {r['path'] for r in record['candidates']} == {r['path'] for r in subject['files']} - {D + 'successor.json'}
assert [r['path'] for r in subject['files']] == sorted(r['path'] for r in subject['files'])
lines = raw(NE).decode('utf-8').splitlines()
ov = {o['selector']['line']: o for o in record['passageOverrides']}
assert sorted(ov) == [3529, 3849, 3850] and len(record['passageOverrides']) == 3
for n, o in ov.items():
    assert o['parent'] == pin(NE) and o['selector'] == {'line': n} and o['before'] == lines[n - 1]
    assert '\n' not in o['after']
checks.append('shape: 1 parent, 3 line overrides (3529, 3849, 3850), befores exact, candidates = subject - record')

# 2. NE:3529 insert-only, cells kept, key new
b, a = ov[3529]['before'], ov[3529]['after']
assert len(a) > len(b) and a.count('|') == b.count('|') == 6
i = next(k for k in range(len(b)) if b[k] != a[k])
assert a[:i] == b[:i] and a[i + len(a) - len(b):] == b[i:], 'NE:3529 is not a pure insertion'
assert a.endswith('| | `operational-failed` (4) | `PROVIDER.PROTOCOL_VIOLATION` | operational record |')
effective = list(lines)
for n, o in ov.items():
    effective[n - 1] = o['after']
eff = '\n'.join(effective)
assert lines and KEY not in '\n'.join(lines) and eff.count(KEY) == 1
assert 'coverage-closed-world-mismatch' not in raw(NES).decode('utf-8')
reg = json.loads(raw(REG))
assert all('closed-world' not in r['code'] for r in reg['records'])
assert all('closed-world' not in r['internalCode'] for r in reg['internalAliases'])
checks.append('NE:3529 insert-only (one contiguous insertion, 6 pipes kept, row route unchanged); key new in NE, '
              'not in the registered bundle, not a DomainDetailCode or alias')

# 3. the fault-law paragraph and the retained selectors
para_before = ' '.join(lines[3836:3855])
para_after = ' '.join(effective[3836:3855])
assert 'facts before the terminal are admitted' in para_before
assert 'facts before the terminal are admitted' not in para_after and 'admitted and the Run' not in para_after
dlv, rpp = json.loads(raw(DLV)), json.loads(raw(RPP))
sup = 'typescriptSemanticSubstrate.supervision.'
for path in ('factBatchAtomicity.onUnavailable', 'factBatchAtomicity.onBudgetExhausted',
             'cleanUnavailable.candidateDisposition', 'deterministicBudget.candidateDisposition'):
    assert at(dlv, sup + path) == 'DISCARD_ALL_CANDIDATES', path
    assert ('`$.' + sup + path + '`' in para_after) or ('`.' + path.split('.')[-1] + '`' in para_after), path
assert at(rpp, 'candidateAtomicity.discardAllOn').startswith('every other terminal')
assert at(rpp, 'candidateAtomicity.unavailableAndBudgetCoverage').endswith('candidates remain discarded.')
for p in ('`$.candidateAtomicity.discardAllOn`', '`$.candidateAtomicity.unavailableAndBudgetCoverage`',
          '"candidates remain discarded"', '`DISCARD_ALL_CANDIDATES`', '`StageAuthorityV1.factsAdmitted`',
          'is `none`', '`before-terminal`', 'contract successor FA-1', 'host conversion of §9.7',
          'The Run is authoritative with the stage `partial`.'):
    assert p in para_after, p
dps = at(dlv, 'typescriptSemanticSubstrate.providerProtocol.wireSchema.payloadSchemas')
rps = rpp['wireSchema']['payloadSchemas']
assert 'factStreamCommitment' in dps['CompleteV1']['required'] and 'factStreamCommitment' in rps['CompleteV2']['required']
for t in (dps['BudgetExhaustedV1'], dps['UnavailableV1'], rps['BudgetExhaustedV2'], rps['UnavailableV2']):
    assert 'coverageCommitment' in t['required'] and 'factStreamCommitment' not in t['required']
for s in ('candidateAtomicity', 'factBatchAtomicity', 'candidateDisposition', 'DISCARD_ALL_CANDIDATES'):
    assert s not in '\n'.join(lines), s
checks.append('fault law: "facts before the terminal are admitted" withdrawn; 4 delivery.v2 and 2 '
              'rust-provider-protocol.v2 selectors resolve to the quoted values; only CompleteV1/CompleteV2 carry '
              'factStreamCommitment; NE (section 0 included) names none of the dispositions')

# 4. StageAuthorityV1 and the reference stage_authority
nes = json.loads(raw(NES))
enum = nes['$defs']['StageAuthorityV1']['properties']['factsAdmitted']['enum']
assert enum == ['all', 'before-terminal', 'none']
for m in MODELS:
    tree = ast.parse(raw(m).decode('utf-8'))
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'stage_authority')
    found = {}
    for node in ast.walk(fn):
        if isinstance(node, ast.If) and isinstance(node.test, ast.Compare) and \
                isinstance(node.test.comparators[0], ast.Constant):
            kind = node.test.comparators[0].value
            for st in node.body:
                if isinstance(st, ast.Assign) and isinstance(st.value, ast.Dict):
                    d = {k.value: v for k, v in zip(st.value.keys, st.value.values) if isinstance(k, ast.Constant)}
                    found[kind] = d['factsAdmitted'].value
    assert found.get('budget-exhausted') == 'before-terminal' and found.get('unavailable') == 'before-terminal', m
    assert found.get('complete') == 'all', m
checks.append('StageAuthorityV1.factsAdmitted enum %s admits none; stage_authority returns before-terminal for '
              'budget-exhausted and unavailable in both models (finding FA1-F1 accurate)' % enum)

# 5. the section 4.5 laws
assert lines[2220] == '3. `nonliteralLoading=none` (no `require-nonliteral`, `dynamic-import-nonliteral`,'
assert lines[2221].strip() == '`reflective-access`, `indirect-eval` edges in the universe);'
assert lines[2236].endswith('`deadCodeRepairEligible` is')
assert lines[2237] == 'true only with `exportsClosed=closed`, `entryPointsRecognized=all` and no'
checks.append('section 4.5 laws at NE:2221-2222 and NE:2237-2239 match the NE:3529 key text')

# 6. the source law
h3 = raw(H3)
assert hashlib.sha256(h3).hexdigest().startswith('7a562720')
h = h3.decode('utf-8')
for s in ('- **X-H2. Clean non-Complete terminals.** It is for the **native owner (FA-1)**.',
          '| **FA-1** | NE §10 fault-law passage, NE:3849-3850.',
          'It also adds `native.coverage-closed-world-mismatch` to NE:3529\'s producer-boundary row (item 13).',
          '### 4. Clean non-Complete terminals: candidates discarded, terminal Coverage admitted (lead decision; X-H2)'):
    assert s in h, s
checks.append('M3-H r3 (7a562720) carries X-H2, the FA-1 row and item 4 as cited')
print(json.dumps({'passed': True, 'checks': checks}, indent=1, ensure_ascii=False))
