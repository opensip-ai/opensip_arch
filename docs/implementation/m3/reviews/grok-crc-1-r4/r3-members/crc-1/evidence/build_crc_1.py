"""Build CRC-1, the core role closures contract successor of law M3-C (item 9; r6's X-C1), with
its test vector, PASSAGES.md, the subject manifest and the lead's draft unit record.

Usage: build_crc_1.py [--product PATH] [--rev REV] [--check]
- PATH is the product checkout (default /Users/sb/code/opensip-ai/opensip), read only. REV
  (default cd5958b, product main for r2) names the product commit whose design-lock.json and security fixture are
  read with read-only `git show`.
- Without --check every generated file is written. With --check nothing is written: each
  generated file is rebuilt in memory and compared with the bytes on disk.

Deterministic: two runs give identical bytes. Run with python3 -I -B at nice -n 19. It needs
the hand-written README.md to exist, because the record and the subject pin it.

Generated: crc-1/PASSAGES.md, crc-1/successor.json, crc-1/evidence/vector.json,
../crc-1-subject.json and ../crc-1-unit.json (the unit record is not part of the subject).
"""
import difflib, hashlib, json, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[6]
args = list(sys.argv[1:])


def opt(name, default):
    if name in args:
        i = args.index(name)
        value = args[i + 1]
        del args[i:i + 2]
        return value
    return default


W = Path(opt('--product', '/Users/sb/code/opensip-ai/opensip'))
REV = opt('--rev', 'cd5958b')
CHECK = '--check' in args
M = 'docs/implementation/m3/snapshot-plan-c/'
D = M + 'crc-1/'

IE = 'docs/v2/contracts/product-v1/identity-and-evidence.md'
IDS = 'docs/implementation/m3/preview-pack-i1/i1-l/design/foundation/identity-schemas.v3.json'
COMP = 'docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md'
WS = 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
WSE = 'docs/implementation/m1/source-selection-v2/reference/effective-workflows-and-surfaces.md'
DMS = 'docs/coop/design-corrections/workflows/schemas/evaluator3/detector-manifest.schema.json'
FIXTURE = 'crates/security/tests/fixtures/core-inventory318.ndjson'
LABEL = 'baseline-macos'
EC1_VECTOR = 'docs/implementation/m2/core-evaluator-closure-ec1/evidence/vector.json'


def git_show(path):
    return subprocess.run(['git', '-C', str(W), 'show', '%s:%s' % (REV, path)], check=True,
                          capture_output=True).stdout


def pin_bytes(path, raw):
    return {'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def pin(path):
    return pin_bytes(path, (A / path).read_bytes())


def read_pinned(row):
    raw = (A / row['path']).read_bytes()
    assert pin_bytes(row['path'], raw) == {k: row[k] for k in ('path', 'bytes', 'sha256')}, row['path']
    return raw


def C(x):
    # Identity canonical form for these values (sorted keys, no whitespace, small integers,
    # ASCII paths), checked below against the product fixture's own expected core closure.
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def H(domain, x):
    c = C(x)
    return hashlib.sha256(b'opensip.product.v1\x00' + domain.encode() + b'\x00'
                          + len(c).to_bytes(8, 'big') + c).hexdigest()


def resolve(doc, pointer):
    for token in pointer[1:].split('/'):
        doc = doc[token.replace('~1', '/').replace('~0', '~')]
    return doc


def insert_only(before, after):
    ops = difflib.SequenceMatcher(None, before, after, autojunk=False).get_opcodes()
    return before != after and all(tag in ('equal', 'insert') for tag, *_ in ops)


# --- The lock at REV: the accepted set and every bound override key. -------------------------
lock = json.loads(git_show('design-lock.json'))
accepted, bound = {}, {}
for key in ('sourceManifest', 'applicationManifest'):
    for row in json.loads(read_pinned(lock['approvals'][key]))['files']:
        accepted[row['path']] = row
for binding in lock['contractSuccessors']:
    record = json.loads(read_pinned(binding['record']))
    accepted[binding['record']['path']] = binding['record']
    for row in record['candidates']:
        accepted[row['path']] = row
    for entry in record.get('passageOverrides', []) + record.get('passageSupersessions', []):
        bound[(entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True))] = binding['record']['path']
CONTRACT_SUCCESSORS = len(lock['contractSuccessors'])

# --- The overrides. ----------------------------------------------------------------------------
IE285_ADD = '\n\n' + (
    '**Core role closures (contract successor CRC-1, 2026-10-04).** The core evaluator closure\'s rule (EC1, above)'
    ' has three more projections. For one core release, the **core detector closure**, the **core provider closure**'
    ' and the **core adapter closure** are each `closure2:` + H("closure", D), where D is the authenticated core'
    ' inventory\'s selected-platform closure descriptor that security projects for the core closure, with `kind` set to'
    ' `"detector"`, `"provider"` or `"adapter"` respectively and every other member unchanged. The core closure and the'
    ' four core role closures of one release (evaluator, detector, provider and adapter) therefore differ only by'
    ' `kind`. For every core role closure, `manifestDigest` is raw SHA256 of the TR-CORE-signed core inventory body'
    ' (`opensip.metadata.inventory.1`), excluding its signature envelope, and `tree` is the projection of that'
    ' platform\'s regular files. The `closure.manifestDigest` sentence above and the `raw-artifact` row of the'
    ' representation table name the kind-`evaluator` case; they hold equally for every core role closure. No core role'
    ' closure is a component-manifest closure: none is admitted through a component manifest, a catalog release or'
    ' security\'s role-to-kind table (security §S1, contract successor CR-1), and `core` is never an identity closure'
    ' kind. A closure is a core role closure of a Plan exactly when its descriptor equals, except for `kind`, the'
    ' descriptor of the core evaluator closure that the Plan selects and its evaluation seal names.'
    ' `closureKinds.byField` is unchanged. Each core role closure is admitted only in the fields below; in any other'
    ' field, `cache-key.producerClosure` included, it refuses.\n'
    '\n'
    '- **The core detector closure** is the `detectorClosure` of each `EvaluatorEmissionPlanV1` row whose rule\'s'
    ' policy came from a pack of the core\'s bundled pack registry, and so the `finding.ruleClosure` of those rules\''
    ' findings. **The detector join**, checked at Run closure: every emission row of a bundled pack names a retained'
    ' kind-`detector` closure that is the Plan\'s core detector closure, and the row\'s `contributionId` is a member of'
    ' that pack\'s registry-row `contributions`. An evaluator or provider closure, or another core\'s detector closure,'
    ' cannot stand in (composition §1).\n'
    '- **The core adapter closure** is only the `import.adapterClosure` of an import whose `kind` is `dependency` or'
    ' `prepared`. It is never a `plan.semanticClosures` member.\n'
    '- **The core provider closure** has exactly two admitted uses under the one provider identity: (1) the'
    ' `import.producerClosure` of an import whose `kind` is `dependency` or `prepared`; (2) the producer of'
    ' syntax-universe work, only where the record\'s, stage\'s or binding\'s universe is a'
    ' `native.semantic-universe.syntax.v2` identity: `subject-scope.enumeratorClosure`, `view.producerClosure` and so'
    ' `fact.producerClosure`, `stage-spec.producerClosure`, an enumeration binding\'s `enumerator.closureId`, and'
    ' `CandidateProducerResultV1.producerClosure`. It is a `plan.semanticClosures` member exactly when the Plan selects'
    ' a syntax universe, and is never selected otherwise, not even explicitly. It is never the producer of a TypeScript'
    ' or Rust record. The grammar'
    ' closure keeps kind `grammar` and is never a producer, and a TypeScript or Rust provider closure is never the'
    ' producer of a syntax record. As every stage producer does, the core provider closure registers each syntax'
    ' stage\'s output schema as a core platform tree member at `opensip-interface/stage-output/<operation>.schema.json`'
    ' (below).\n'
    '\n'
    'Security derives every core role closure from the one authenticated inventory it already holds; none is read from'
    ' a Run, a worker claim or a build-time string, and no new signed data, release format or trust change is needed.'
    ' As for every closure, the inventory body and every tree member are retained preimages of a Run that names one,'
    ' stored once per store by raw SHA256. A new core release is a new detector, provider and adapter closure, so the'
    ' Plans and Runs that select them have new identities. Historical closures, Plans and Runs keep their bytes and'
    ' are not re-read under this law.')
IE1377_ADD = (
    ' **The core role closures are the exception (contract successor CRC-1, above).** The core provider closure is a'
    ' direct `semanticClosures` member exactly when the Plan selects a `native.semantic-universe.syntax.v2` universe,'
    ' and is never selected otherwise, not even explicitly; the core adapter closure is never a `semanticClosures`'
    ' member. A Plan that breaks either rule refuses.')
ART_ADD = ('; for the core detector, provider and adapter closures, the same TR-CORE-signed core inventory body bytes'
           ' (contract successor CRC-1, the core role closures)')
NOTE_ADD = (
    ' Contract successor CRC-1 adds the other core role closures: the core detector, provider and adapter closures are'
    ' the same projection with kind set to "detector", "provider" and "adapter", so the four core role closures of one'
    ' release differ only by kind, and none is a component-manifest closure. A closure is a core role closure of a Plan'
    ' when its descriptor equals, except for kind, that of the core evaluator closure the Plan selects. Each is'
    ' confined to named fields. The core detector closure is the detectorClosure, and so the finding.ruleClosure, of'
    ' the rules of the core\'s bundled packs. The core adapter closure is only the import.adapterClosure of a'
    ' dependency or prepared import. The core provider closure has exactly two uses under one identity: the'
    ' import.producerClosure of a dependency or prepared import, and the producer of syntax-universe work'
    ' (subject-scope.enumeratorClosure, view.producerClosure and so fact.producerClosure, stage-spec.producerClosure,'
    ' the enumeration binding\'s enumerator.closureId and CandidateProducerResultV1.producerClosure) only where the'
    ' universe is a native.semantic-universe.syntax.v2 identity; it never produces a TypeScript or Rust record. A core'
    ' role closure in any other field, cache-key.producerClosure included, refuses. byField is unchanged.')
SELECTION_ADD = (
    ' The core role closures are the exception (contract successor CRC-1): the core provider closure is a direct'
    ' member exactly when the Plan selects a native.semantic-universe.syntax.v2 universe, and is never selected'
    ' otherwise, not even explicitly; the core adapter closure is never a member.')
COMP9_ANCHOR = 'A provider or evaluator closure cannot stand in for it.'
COMP9_ADD = (
    ' For a rule whose policy came from a pack of the core\'s bundled pack registry, detectorClosure is the core'
    ' detector closure (identity-and-evidence §3, contract successor CRC-1): its descriptor equals the seal\'s'
    ' evaluator-closure descriptor except for kind, and the row\'s contributionId is a member of that pack\'s'
    ' registry-row contributions. It is a distinct closure of kind detector, not the evaluator closure, although both'
    ' project one core release; another core\'s detector closure cannot stand in either.')
WS_ADD = (
    ' For a core role closure (identity-and-evidence §3, contract successors EC1 and CRC-1), such as a bundled pack\'s'
    ' core detector closure, `closure.manifestDigest` identifies the TR-CORE-signed core inventory body instead, and the'
    ' listing is the reserved file of the core platform tree.')
DMS_ANCHOR = 'never this three-field listing.'
DMS_ADD = (
    ' For a core role closure (identity-and-evidence §3, contract successors EC1 and CRC-1), such as a bundled pack\'s'
    ' core detector closure, closure.manifestDigest is the TR-CORE-signed core inventory body instead, and this listing'
    ' is the reserved file of the core platform tree.')


def insert_after(anchor, addition):
    def apply(before):
        assert before.count(anchor) == 1, anchor
        return before.replace(anchor, anchor + addition)
    return apply


SPEC = [
    (IE, {'line': 285}, lambda b: b + IE285_ADD),
    (IE, {'line': 1377}, lambda b: b + IE1377_ADD),
    (IDS, {'jsonPointer': '/$defs/closure/properties/manifestDigest/x-opensip-digest/artifact'}, lambda b: b + ART_ADD),
    (IDS, {'jsonPointer': '/x-opensip-digest-domains/closureKinds/note'}, lambda b: b + NOTE_ADD),
    (IDS, {'jsonPointer': '/x-opensip-digest-domains/closureMembership/selectionLaw'}, lambda b: b + SELECTION_ADD),
    (COMP, {'line': 9}, insert_after(COMP9_ANCHOR, COMP9_ADD)),
    (WS, {'line': 308}, lambda b: b + WS_ADD),
    (WSE, {'line': 312}, lambda b: b + WS_ADD),
    (DMS, {'jsonPointer': '/description'}, insert_after(DMS_ANCHOR, DMS_ADD)),
]

parents, overrides = {}, []
for path, selector, make in SPEC:
    parent = accepted.get(path)
    assert parent is not None, 'parent is not accepted at %s: %s' % (REV, path)
    parent = {k: parent[k] for k in ('path', 'bytes', 'sha256')}
    raw = read_pinned(parent)
    parents[path] = parent
    if 'line' in selector:
        try:
            json.loads(raw)
        except ValueError:
            pass
        else:
            raise AssertionError('line selector on a JSON parent: ' + path)
        before = raw.decode('utf-8').splitlines()[selector['line'] - 1]
    else:
        before = resolve(json.loads(raw), selector['jsonPointer'])
    assert isinstance(before, str) and before
    key = (path, json.dumps(selector, sort_keys=True))
    assert key not in bound, 'already overridden by %s: %s %s' % (bound[key], path, selector)
    after = make(before)
    assert insert_only(before, after) and 'CRC-1' in after, (path, selector)
    overrides.append({'parent': parent, 'selector': selector, 'before': before, 'after': after})

# --- The vector. -------------------------------------------------------------------------------
fixture_raw = git_show(FIXTURE)
cases = [json.loads(line) for line in fixture_raw.decode('utf-8').splitlines()]
case = [q for q in cases if q['label'] == LABEL][0]
assert case['expected']['ok'] is True
body = bytes.fromhex(case['raw'])
core = case['expected']['descriptor']
assert core['kind'] == 'core' and core['manifestDigest'] == hashlib.sha256(body).hexdigest()
assert 'closure2:' + H('closure', core) == case['expected']['closure']
KINDS = ['core', 'evaluator', 'detector', 'provider', 'adapter']
closures = {}
for kind in KINDS:
    d = dict(core, kind=kind)
    closures[kind] = {'kind': kind, 'closure': 'closure2:' + H('closure', d),
                      'descriptorCanonicalSha256': hashlib.sha256(C(d)).hexdigest()}
assert len({c['closure'] for c in closures.values()}) == 5
ec1 = json.loads((A / EC1_VECTOR).read_bytes())
assert ec1['coreClosure'] == closures['core']['closure'] and ec1['evaluatorClosure'] == closures['evaluator']['closure']
assert ec1['coreDescriptor'] == core
accepted_cases = 0
for q in cases:
    if q['expected'].get('ok') is True:
        d = q['expected']['descriptor']
        assert 'closure2:' + H('closure', d) == q['expected']['closure']
        assert len({H('closure', dict(d, kind=k)) for k in KINDS}) == 5
        accepted_cases += 1
assert accepted_cases == 53, accepted_cases
vector = {
    'schemaVersion': 1,
    'standing': 'CRC-1 test vector. The core closure and the four core role closures (evaluator, detector, provider,'
                ' adapter) of one authenticated core inventory: the five descriptors differ only by kind, and the five'
                ' ids are pairwise distinct. The core and evaluator values equal EC1\'s vector. C2a reproduces it byte'
                ' for byte in a Rust test of core_inventory.',
    'source': {'product': REV, 'fixture': pin_bytes(FIXTURE, fixture_raw), 'label': LABEL,
               'platform': case['platform'], 'ec1Vector': pin(EC1_VECTOR)},
    'inventoryBody': {'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(), 'hex': body.hex()},
    'coreDescriptor': core,
    'closures': [closures[k] for k in KINDS],
    'fixtureCases': {'accepted': accepted_cases, 'idsPerCasePairwiseDistinct': 5},
}
outputs = {D + 'evidence/vector.json': (json.dumps(vector, indent=2, sort_keys=True) + '\n').encode()}


# --- PASSAGES.md. ------------------------------------------------------------------------------
def selector_text(selector):
    return 'line %d' % selector['line'] if 'line' in selector else 'pointer `%s`' % selector['jsonPointer']


def fence(text):
    return '~~~text\n' + text + '\n~~~\n'


parts = ['# CRC-1 passages (generated)\n',
         'Generated by `evidence/build_crc_1.py` from the same data as `successor.json`; do not edit by hand. Each'
         ' entry gives the parent, the selector, the exact accepted `before` and the candidate `after`. Every `after`'
         ' keeps its `before` and only inserts text. Product lock: `%s`, %d contract successors.\n' % (REV, CONTRACT_SUCCESSORS),
         '## Passage overrides\n']
for n, o in enumerate(overrides, 1):
    parts.append('### %d. `%s` %s\n' % (n, o['parent']['path'], selector_text(o['selector'])))
    parts.append('Before:\n')
    parts.append(fence(o['before']))
    parts.append('After:\n')
    parts.append(fence(o['after']))
outputs[D + 'PASSAGES.md'] = '\n'.join(parts).encode()


def current(path):
    return outputs[path] if path in outputs else (A / path).read_bytes()


HAND = [D + 'README.md', D + 'evidence/build_crc_1.py', D + 'evidence/check_crc_1.py', D + 'evidence/verify_scratch.py']
GENERATED = [D + 'PASSAGES.md', D + 'evidence/vector.json']
candidates = sorted([pin_bytes(p, current(p)) for p in HAND + GENERATED], key=lambda r: r['path'])
for row in candidates:
    assert row['path'] not in accepted, 'candidate reuses an accepted path: ' + row['path']
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED CRC-1 identity contract successor (law M3-C r7 item 9, with r6\'s X-C1; the EC1 pattern): the'
                ' core detector, provider and adapter closures are closure2: + H("closure", the authenticated core'
                ' descriptor with kind "detector", "provider" or "adapter"), and their manifestDigest is the raw SHA-256'
                ' of the TR-CORE-signed inventory body. Each is confined to named fields: the detector to bundled-pack'
                ' emission rows (with the detector join); the adapter to import.adapterClosure of dependency and'
                ' prepared imports; the provider to import.producerClosure of those imports and to syntax-universe work,'
                ' a plan.semanticClosures member exactly when a syntax universe is selected. Text-only overrides of the'
                ' identity contract, the selected identity schema bundle (I1-L\'s copy), the composition contract,'
                ' workflows-and-surfaces and its selected effective copy, and the detector-manifest schema'
                ' description; no schema shape, kind, domain, recipe, registry, generated code, inventory or product'
                ' change. Exact frozen candidate requires actual independent review and root assent.',
    'parents': sorted(parents.values(), key=lambda r: r['path']),
    'passageOverrides': overrides,
    'candidates': candidates,
}
outputs[D + 'successor.json'] = (json.dumps(record, indent=2, ensure_ascii=False) + '\n').encode()
record_pin = pin_bytes(D + 'successor.json', outputs[D + 'successor.json'])
subject = {'schemaVersion': 1, 'files': sorted(candidates + [record_pin], key=lambda r: r['path'])}
outputs[M + 'crc-1-subject.json'] = (json.dumps(subject, indent=2) + '\n').encode()
subject_pin = pin_bytes(M + 'crc-1-subject.json', outputs[M + 'crc-1-subject.json'])
unit = {
    'schemaVersion': 1,
    'unit': 'snapshot-plan-c-crc-1',
    'status': 'DRAFT-PENDING-REVIEW',
    'subjectManifest': subject_pin,
    'independentReview': {'path': 'docs/implementation/m3/reviews/grok-crc-1-r3/review.json', 'bytes': None,
                          'sha256': None},
    'rootSubstantiveAssent': False,
    'requiredUnitFindings': [],
    'acceptedSuccessor': record_pin,
    'rootAssessment': 'DRAFT (r3, after GROK2\'s r1 RF-1 and Grok\'s r2 RF-1). Completed by the lead after Grok\'s r3 review: status'
                      ' ACCEPTED-DESIGN-UNIT, the review pin, rootSubstantiveAssent true. CRC-1 is nine insert-only passage overrides (IE 285 and 1377; three'
                      ' JSON Pointer strings of I1-L\'s identity schema copy; COMP 9; WS 308 and WSE 312; the'
                      ' detector-manifest description) and a vector on EC1\'s baseline-macos fixture. It binds on the'
                      ' verify_design at product %s on top of %d contract successors. X-H3 (M3-H r1) is left to'
                      ' M3-C\'s next revision and a follow-on identity successor (README LD-8).' % (REV, CONTRACT_SUCCESSORS),
    'fullM2Complete': False,
    'productQualification': False,
}
outputs[M + 'crc-1-unit.json'] = (json.dumps(unit, indent=2) + '\n').encode()

if CHECK:
    stale = [p for p, b in outputs.items() if not (A / p).exists() or (A / p).read_bytes() != b]
    print(json.dumps({'check': 'identical' if not stale else 'DIFFERS', 'differs': stale}, indent=1))
    sys.exit(1 if stale else 0)
for path, raw in outputs.items():
    (A / path).write_bytes(raw)
print(json.dumps({'rev': REV, 'contractSuccessors': CONTRACT_SUCCESSORS, 'overrides': len(overrides),
                  'parents': len(parents), 'candidates': len(candidates), 'subject': subject_pin,
                  'successor': record_pin, 'closures': {k: closures[k]['closure'] for k in KINDS},
                  'fixtureCases': accepted_cases}, indent=1))
