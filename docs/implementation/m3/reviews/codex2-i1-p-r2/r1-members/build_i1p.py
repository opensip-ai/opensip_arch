"""Build contract successor I1-P deterministically: the pack contract of law M3-I1 r2 item 5.

Takes the bundled document's bytes from the accepted law's item 5.2 block, and recomputes the
item 5.3 digests with the design encoder `docs/coop/design-corrections/foundation/canonical.py`
(identity-and-evidence section 3). It cross-checks them with the exact-schema profile's encoder
(`exact-schema-profile-selection-v1/reference/canonical.py`), and validates the document and its
compiled RuleProgramV2 under I1-L's policy-document successor copies with that exact profile. Then
it writes the pack contract, the registry file, the materialization map, the digests, the
successor record and the subject manifest.

The parents are the law snapshot and I1-L's two policy-document copies, which are accepted once
I1-L is bound ahead of I1-P. The checks restate verify_design's contract_successor rules,
treating I1-L's subject members as accepted.

Usage (read-only on the product; git only reads the base blob):
    python3.14 -I -B evidence/build_i1p.py --product /path/to/opensip --deps DIR [--check]
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCH = HERE.parents[5]
BASE = 'docs/implementation/m3/preview-pack-i1'
UNIT = f'{BASE}/i1-p'
I1L = f'{BASE}/i1-l'
PRODUCT_HEAD = '3e64266aa8729160cd22509dcfff95a3bb09fcea'
LAW = f'{BASE}/PROPOSAL-r2.md'
LAW_SHA256 = '1eb47d1e292660b15cb0016a280899a384364f2c3d99ab61d18f12b133eba2c7'
ENCODER = 'docs/coop/design-corrections/foundation/canonical.py'
EXACT = 'docs/implementation/m2/exact-schema-profile-selection-v1/reference/canonical.py'
PDS_COPY = f'{I1L}/design/workflows/schemas/policy-document.v2.schema.json'
PPDS_COPY = f'{I1L}/product/schemas/sources/policy-v2.schema.json'
PDS = 'docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json'
PPDS = 'docs/implementation/m1/source-selection-v2/schemas/sources/policy.v2.schema.json'
COMMON = 'docs/coop/design-corrections/workflows/schemas/common.schema.json'
PCOMMON = 'docs/implementation/m1/source-selection-v2/schemas/sources/common.v1.schema.json'
I1L_COPIES = [f'{I1L}/design/foundation/identity-schemas.v3.json', PDS_COPY,
              f'{I1L}/product/schemas/sources/identity-v3.schema.json', PPDS_COPY]
POLICY_ID = 'urn:opensip:product-v1:policy-document:2'
DOC = f'{UNIT}/product/crates/evaluator/src/preview-typescript-pack.v1.policy.json'
REG = f'{UNIT}/product/crates/evaluator/src/pack-registry.json'
DOC_PRODUCT = 'crates/evaluator/src/preview-typescript-pack.v1.policy.json'
REG_PRODUCT = 'crates/evaluator/src/pack-registry.json'

# Law item 5.3's provisional values; a mismatch blocks acceptance (resolved in the encoder).
PROVISIONAL = {'programDigest': '8e8936af513ae93eeb8227fb991330b523761930d85d077b044f4312706a57de',
               'policySha256': '96675a5e20fcfd8ba6501f20b9017aa205e300b9f1984d7e74ad534996acdcd1',
               'policyBytes': 574,
               'ruleProgramDigest': 'e796f81764d0ee452c591c852e98f59647518a1894d4bd0fd5c70b674ecc3ecb',
               'ruleProgramBytes': 457}
# Law item 5.4's row, exactly as printed there.
ROW_TEXT = ('{"contributions":["opensip.preview.typescript"],"name":"opensip.preview.typescript.pack",'
            '"packId":"opensip.preview.typescript.pack:1","policyDocument":"preview-typescript-pack.v1.policy.json",'
            '"policySha256":"96675a5e20fcfd8ba6501f20b9017aa205e300b9f1984d7e74ad534996acdcd1","version":1}')
REGISTRY_STANDING = ('Bundled first-party policy packs compiled into the signed core (law X12 r3 items 2 to 4). '
                     'Admission is by exact packId against these rows only. One row (law M3-I1 r2 item 5, '
                     'contract successor I1-P): opensip.preview.typescript.pack:1, the DR-131 preview pack.')
SELF_CHECKS = [
    ('S1', 'The registry is self-consistent (policy.rs:930-1023) with exactly one row.'),
    ('S2', 'The document file\'s bytes equal canonical_bytes(parse_json(file)); its SHA-256 equals policySha256; '
           'there is no trailing newline.'),
    ('S3', 'X12 item 6\'s steps 6.1 to 6.7 pass for the release row (X12:87-101).'),
    ('S4', 'Each rule\'s programDigest equals SHA-256(C(emitWhen)).'),
    ('S5', 'The packId, policySha256, programDigest and compiled program digest equal the values this record pins '
           '(identity.packId, digests.policySha256.value, digests.programDigest.value, digests.ruleProgramDigest.value).'),
    ('S6', 'The source pin: the release build names one document and no test row; the include_bytes!( count goes '
           'from 7 to 8 (policy_pack_tests.rs:638); &RELEASE_PACKS still appears exactly twice.'),
    ('S7', 'NT-1: opensip.preview.typescript.pack:1 admits; :2, the bare name, :01, case variants, a trailing newline '
           'and other names stay row 1; Supplied with the release document\'s exact bytes stays row 2 (X12:92, X12:207).'),
    ('S8', 'check_plan_pack: a Plan naming the pack with the matching policyDigest admits; any other digest is '
           'refused (policy.rs:1403-1406).'),
    ('S9', 'Host admit_policy_selection(Named(pack:1)) returns the AdmittedPack, and every other host row is '
           'unchanged (X12b).'),
    ('S10', 'Over synthetic admitted inputs (unit I1-b2), the corpus golden sets hold: cycle has one finding on '
            'cycle/a.ts with members cycle/a.ts and cycle/b.ts; self has one finding on self/self.ts; acyclic, empty '
            'and shadow pass; unresolved, malformed and dynamic are indeterminate (QCM:7-124, LQM:232). I1-L\'s '
            'evidence/cases-report.json is the oracle\'s expectation for these.'),
]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pin(path, raw):
    return {'path': path, 'bytes': len(raw), 'sha256': sha(raw)}


def read(path):
    return (ARCH / path).read_bytes()


def dumps(value):
    return (json.dumps(value, indent=2, ensure_ascii=True) + '\n').encode('ascii')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ARCH / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def document_bytes():
    law = read(LAW)
    if sha(law) != LAW_SHA256:
        raise SystemExit('law bytes changed')
    text = law.decode('utf-8')
    start = text.index('**5.2 The bundled document.**')
    block = text[text.index('```\n', start) + 4:]
    raw = block[:block.index('\n```')].encode('utf-8')
    if text[start:].index('**5.3 Digest rules.**') < text[start:].index('```\n'):
        raise SystemExit('5.2 block not found')
    return raw


def digests(encoder, raw):
    value = encoder.parse(raw)
    canonical = encoder.canonical(value)
    rule_rows, program_digests = [], []
    for rule in value['rules']:
        program_digests.append(sha(encoder.canonical(rule['emitWhen'])))
        rule_rows.append({'ruleId': rule['ruleId'], 'ruleProgramRef': rule['ruleProgramRef'],
                          'emitWhen': rule['emitWhen']})
    program = {'schemaVersion': 2, 'policyDigest': sha(canonical), 'rules': rule_rows}
    program_raw = encoder.canonical(program)
    return value, canonical, program, program_raw, program_digests


def validation(exact, raw, program):
    """The exact profile admits the document under I1-L's copies; the parents refuse its op."""
    out = []
    value = exact.parse(raw)
    for policy, common, role in ((PDS_COPY, COMMON, 'I1-L design copy'), (PPDS_COPY, PCOMMON, 'I1-L product copy'),
                                 (PDS, COMMON, 'parent'), (PPDS, PCOMMON, 'parent')):
        documents = [exact.parse(read(common)), exact.parse(read(policy))]
        registry = exact.exact_registry(documents)
        result = {'schema': pin(policy, read(policy)), 'common': pin(common, read(common)), 'role': role}
        for selector, instance in (('PolicyDocumentV2', value), ('RuleProgramV2', program)):
            try:
                exact.validate({'$ref': f'{POLICY_ID}#/$defs/{selector}'}, instance, registry=registry)
                result[selector] = 'admitted'
            except Exception as exc:  # jsonschema.ValidationError or a profile AdmissionError
                result[selector] = 'refused: ' + str(getattr(exc, 'message', exc)).split('\n')[0][:160]
        out.append(result)
    return out


def metaschema(exact):
    from jsonschema import Draft202012Validator
    out = []
    for path in I1L_COPIES:
        Draft202012Validator.check_schema(exact.parse(read(path)))
        out.append({'copy': pin(path, read(path)), 'draft202012MetaSchema': 'valid'})
    return out


def accepted_set(product):
    lock = json.loads((product / 'design-lock.json').read_bytes())
    accepted = {}
    for name in ('sourceManifest', 'applicationManifest'):
        for row in json.loads(read(lock['approvals'][name]['path']))['files']:
            accepted[row['path']] = row
    for binding in lock['contractSuccessors']:
        accepted[binding['record']['path']] = binding['record']
        for row in json.loads(read(binding['record']['path']))['candidates']:
            accepted[row['path']] = row
    for binding in lock['inventorySuccessors']:
        accepted[binding['candidate']['path']] = binding['candidate']
    # I1-L is bound ahead of I1-P (LD-P4): its subject members are accepted at I1-P's selection.
    for row in json.loads(read(f'{BASE}/i1-l-subject.json'))['files']:
        assert row['path'] not in accepted, row['path']
        accepted[row['path']] = row
    return accepted


def build(product, deps):
    sys.path.insert(0, deps)
    design = load('opensip_design_canonical', ENCODER)
    exact = load('opensip_exact_canonical', EXACT)
    raw = document_bytes()
    value, canonical, program, program_raw, program_digests = digests(design, raw)
    again = digests(exact, raw)
    if (again[1], again[3], again[4]) != (canonical, program_raw, program_digests):
        raise SystemExit('the two encoders disagree')
    if canonical != raw or raw.endswith(b'\n'):
        raise SystemExit('S2: the document is not its own canonical bytes')
    recomputed = {'programDigest': program_digests[0], 'policySha256': sha(raw), 'policyBytes': len(raw),
                  'ruleProgramDigest': sha(program_raw), 'ruleProgramBytes': len(program_raw)}
    if recomputed != PROVISIONAL:
        raise SystemExit(f'digest mismatch with law item 5.3: {recomputed}')
    if value['rules'][0]['ruleProgramRef']['programDigest'] != program_digests[0]:
        raise SystemExit('S4: programDigest')
    row = json.loads(ROW_TEXT)
    if row['policySha256'] != recomputed['policySha256'] or row['packId'] != f"{row['name']}:{row['version']}":
        raise SystemExit('5.4 row disagrees')
    if set(row['contributions']) != {r['ruleProgramRef']['contributionId'] for r in value['rules']}:
        raise SystemExit('5.4 contributions disagree with the document')
    sys.path.insert(0, str(ARCH / I1L / 'evidence'))
    model = load('cycle_representative_model', f'{I1L}/evidence/cycle_representative_model.py')
    op_law = {r['ruleId']: model.admit_rule(r) for r in value['rules']}
    if any(op_law.values()):
        raise SystemExit(f'item 2.2 refuses the rule: {op_law}')
    checks = validation(exact, raw, program)
    expected = {'I1-L design copy': ('admitted', 'admitted'), 'I1-L product copy': ('admitted', 'admitted')}
    for result in checks:
        got = (result['PolicyDocumentV2'], result['RuleProgramV2'])
        if result['role'] in expected and got != expected[result['role']]:
            raise SystemExit(f'not admitted by {result["schema"]["path"]}: {got}')
        if result['role'] == 'parent' and not got[0].startswith('refused') :
            raise SystemExit('a parent schema admits the new op')
    meta = metaschema(exact)

    files = {DOC: raw}
    registry = {'schemaVersion': 1, 'standing': REGISTRY_STANDING, 'rows': [row]}
    files[REG] = (json.dumps(registry, indent=2, ensure_ascii=True) + '\n').encode('ascii')
    base_registry = subprocess.run(['git', '-C', str(product), 'show', f'{PRODUCT_HEAD}:{REG_PRODUCT}'],
                                   check=True, capture_output=True).stdout
    exists = subprocess.run(['git', '-C', str(product), 'cat-file', '-e', f'{PRODUCT_HEAD}:{DOC_PRODUCT}'],
                            capture_output=True).returncode == 0
    if exists:
        raise SystemExit('the pack document already exists in the product')
    parsed = json.loads(files[REG])
    if sorted(parsed) != ['rows', 'schemaVersion', 'standing'] or sorted(parsed['rows'][0]) != [
            'contributions', 'name', 'packId', 'policyDocument', 'policySha256', 'version']:
        raise SystemExit('registry key sets differ from policy.rs:953-965')
    files[f'{UNIT}/materialization-map.json'] = dumps({
        'schemaVersion': 1,
        'standing': ('Exact prospective materialization of the two data files unit I1-c ships. I1-c also edits '
                     'policy.rs (RELEASE_PACKS.documents) and the tests, which this map does not fix. Independent '
                     'review and root assent are required before selection.'),
        'baseProductHead': PRODUCT_HEAD,
        'files': [
            {'productPath': REG_PRODUCT, 'candidatePath': REG,
             'before': {'bytes': len(base_registry), 'sha256': sha(base_registry)},
             'after': {'bytes': len(files[REG]), 'sha256': sha(files[REG])}},
            {'productPath': DOC_PRODUCT, 'candidatePath': DOC, 'before': None,
             'after': {'bytes': len(raw), 'sha256': sha(raw)}}]})
    encoders = [pin(ENCODER, read(ENCODER)), pin(EXACT, read(EXACT))]
    files[f'{UNIT}/evidence/digests.json'] = dumps({
        'schemaVersion': 1, 'productHead': PRODUCT_HEAD, 'law': pin(LAW, read(LAW)),
        'designEncoder': encoders[0], 'crossCheckEncoder': encoders[1],
        'document': {'bytes': len(raw), 'sha256': sha(raw), 'canonical': True, 'trailingNewline': False},
        'recomputed': recomputed, 'provisional': PROVISIONAL, 'equal': True,
        'ruleProgramV2': program_raw.decode('ascii'),
        'opLaw': {k: 'admitted' for k in op_law},
        'schemaValidation': checks, 'i1lCopiesMetaSchema': meta})
    contract = {
        'schemaVersion': 1,
        'standing': ('PROPOSED I1-P pack contract successor for opensip.preview.typescript.pack:1 (law M3-I1 r2 '
                     'item 5; X12c). Exact frozen candidate requires actual independent review and root assent; '
                     'unit I1-c ships it, after I1-b1.'),
        'law': pin(LAW, read(LAW)),
        'identity': {'name': row['name'], 'version': row['version'], 'packId': row['packId'],
                     'matching': 'byte-exact, no normalization (X12:47-59; PAC:99-100)',
                     'planIdentity': 'name and version enter PlanId through analysisSpecDigest, content through '
                                     'policyDigest (X12:59; PAC:114-118)'},
        'document': {**pin(DOC, raw), 'productPath': DOC_PRODUCT, 'trailingNewline': False,
                     'canonical': True, 'source': 'law item 5.2, verbatim'},
        'registryRow': row,
        'registry': {**pin(REG, files[REG]), 'productPath': REG_PRODUCT, 'standing': REGISTRY_STANDING},
        'digests': {
            'programDigest': {'value': recomputed['programDigest'],
                              'recipe': 'raw SHA-256 of C(emitWhen); frozen for bundled packs only (law item 5.3)'},
            'policySha256': {'value': recomputed['policySha256'], 'bytes': recomputed['policyBytes'],
                             'recipe': 'raw SHA-256 of C(document), equal to the SHA-256 of the file bytes'},
            'ruleProgramDigest': {'value': recomputed['ruleProgramDigest'], 'bytes': recomputed['ruleProgramBytes'],
                                  'recipe': 'raw SHA-256 of C(RuleProgramV2) (COMP:103; AdmittedPack::program_digest)'},
            'encoder': encoders[0]},
        'schema': {'admittedUnder': [pin(PDS_COPY, read(PDS_COPY)), pin(PPDS_COPY, read(PPDS_COPY))],
                   'refusedUnderParents': [pin(PDS, read(PDS)), pin(PPDS, read(PPDS))]},
        'placement': {'document': DOC_PRODUCT, 'includedBy': 'include_bytes! as the sole RELEASE_PACKS.documents entry '
                      '(policy.rs:716-721), named by the row\'s policyDocument (policy.rs:1005-1011)',
                      'rows': 1, 'documents': 1, 'runtimeReads': 'none (X12:43)'},
        'selfChecks': [{'id': i, 'check': text} for i, text in SELF_CHECKS],
        'x12Amendments': ['item 4 "zero rows" (X12:67) becomes "exactly the one row of M3-I1 item 5"',
                          'item 10 NT-1 (X12:160): the ID admits and its variants stay row 1',
                          'item 10 "in M2 there are zero release rows" (X12:169) becomes "exactly one"'],
    }
    files[f'{UNIT}/pack-contract.json'] = dumps(contract)
    for path in (f'{UNIT}/README.md', f'{UNIT}/evidence/build_i1p.py'):
        files[path] = read(path)
    parents = sorted([LAW, PDS_COPY, PPDS_COPY])
    record = {
        'schemaVersion': 1,
        'standing': ('PROPOSED I1-P pack contract successor (law M3-I1 r2 item 5): the exact bundled document of '
                     'opensip.preview.typescript.pack:1, its registry row and file, and the recomputed digests, with '
                     'the self-checks S1 to S10 for unit I1-c. Parents are the law and I1-L\'s policy-document copies, '
                     'so I1-L is bound first. Exact frozen candidate requires actual independent review and root assent.'),
        'parents': [pin(p, read(p)) for p in parents],
        'passageOverrides': [],
        'candidates': [pin(p, files[p]) for p in sorted(files)],
    }
    files[f'{UNIT}/successor.json'] = dumps(record)
    subject = {'schemaVersion': 1, 'files': [pin(p, files[p]) for p in sorted(files)]}
    files[f'{BASE}/i1-p-subject.json'] = dumps(subject)
    check(record, subject, files, accepted_set(product))
    return files


def check(record, subject, files, accepted):
    paths = [row['path'] for row in subject['files']]
    assert paths == sorted(set(paths))
    assert {r['path'] for r in record['candidates']} == set(paths) - {f'{UNIT}/successor.json'}
    for row in subject['files']:
        assert pin(row['path'], files[row['path']]) == row
        assert row['path'] not in accepted, f'candidate reuses an accepted path: {row["path"]}'
    assert record['parents'] and [p['path'] for p in record['parents']] == sorted({p['path'] for p in record['parents']})
    for row in record['parents']:
        assert accepted.get(row['path'], {}).get('sha256') == row['sha256'], row['path']
        assert accepted[row['path']]['bytes'] == row['bytes'] and row['path'] not in paths


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--product', required=True, type=Path)
    parser.add_argument('--deps', required=True)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    files = build(args.product.resolve(), args.deps)
    for path in sorted(files):
        if path.endswith(('README.md', '.py')):
            continue
        target = ARCH / path
        if args.check:
            if target.read_bytes() != files[path]:
                raise SystemExit(f'differs: {path}')
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(files[path])
    print(json.dumps({'subject': pin(f'{BASE}/i1-p-subject.json', files[f'{BASE}/i1-p-subject.json']),
                      'successor': pin(f'{UNIT}/successor.json', files[f'{UNIT}/successor.json']),
                      'digests': json.loads(files[f'{UNIT}/evidence/digests.json'])['recomputed'],
                      'checked': args.check}))


if __name__ == '__main__':
    main()
