"""Independent checker for witnesses.json; writes result.json and exits nonzero on any defect.

Re-verifies, from the original pinned sources only: every case is exact-codec valid
(typed/canonical/parse round trip) and valid under reference.validate and
ExactValidator(registry).is_valid for its ref; every selected target is either covered
or listed uncovered (never both); harvest-seed cases equal the retained source values.
"""
import collections
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # -I isolated mode omits the script directory
from witness_common import (ARCH, CHECK_METADATA, HARVEST, OUT, SOURCE_MAP, SOURCES,
                            check, load, no_float, pin, targets)


def main():
    defects = []
    reference, registry, documents = load()  # asserts all 28 schema pins and the canonical.py pin
    sources = json.loads(SOURCES.read_bytes())
    refs = list(targets())
    target_ids = json.loads(SOURCE_MAP.read_bytes())['selectedTargets']
    corpus = json.loads((OUT / 'witnesses.json').read_bytes(), parse_float=no_float)
    if corpus.get('schemaVersion') != 1 or set(corpus) != {'schemaVersion', 'cases', 'uncovered'}:
        defects.append('corpus envelope')
    by_ref = collections.defaultdict(list)
    for n, case in enumerate(corpus['cases']):
        if set(case) != {'ref', 'value', 'origin'}:
            defects.append('case %d keys' % n)
        if case['ref'] not in target_ids:
            defects.append('case %d ref not selected: %s' % (n, case['ref']))
        err = check(reference, registry, case['ref'], case['value'])
        if err is not None:
            defects.append('case %d %s invalid: %s' % (n, case['ref'], err))
        else:
            by_ref[case['ref']].append(case)
    uncovered = {u['ref']: u for u in corpus['uncovered']}
    for ref in refs:
        if by_ref.get(ref) and ref in uncovered:
            defects.append('covered and uncovered: ' + ref)
        if not by_ref.get(ref) and ref not in uncovered:
            defects.append('neither covered nor listed uncovered: ' + ref)
    proved = [r for r, u in uncovered.items() if u['reason'].get('classification') == 'proved-unsatisfiable']

    seed_index = json.loads((OUT / 'seed-index.json').read_bytes())
    harvest_pin = pin(HARVEST)
    seed_cases = [c for c in corpus['cases'] if c['origin']['kind'] == 'harvest-seed']
    if seed_index['source']['sha256'] != harvest_pin['sha256']:
        defects.append('harvest source changed since seeding')
    else:
        harvest = json.loads(HARVEST.read_bytes())
        true_rows = {(r, i) for r, i, ok in harvest['rows'] if ok is True}
        for case in seed_cases:
            i = case['origin']['valueIndex']
            if case['origin'].get('harvestSha256') != harvest_pin['sha256']:
                defects.append('seed provenance hash: ' + case['ref'])
            if not reference.equal_typed(harvest['values'][i], case['value']) or (case['ref'], i) not in true_rows:
                defects.append('seed value/row mismatch: %s #%d' % (case['ref'], i))
        del harvest

    report = json.loads((OUT / 'generation-report.json').read_bytes())
    generator_sha = hashlib.sha256((OUT / 'generate.py').read_bytes()).hexdigest()
    if report['generator']['sha256'] != generator_sha:
        defects.append('generate.py changed after generation')
    origins = collections.Counter(c['origin']['kind'] for c in corpus['cases'])
    seeded_refs = {c['ref'] for c in seed_cases}
    generated_refs = {c['ref'] for c in corpus['cases'] if c['origin']['kind'] == 'generated'}
    per_doc = collections.defaultdict(lambda: [0, 0])
    for ref in refs:
        per_doc[ref.split('#')[0]][0] += 1
        per_doc[ref.split('#')[0]][1] += bool(by_ref.get(ref))

    manifest = {
        'sourcesJson': pin(SOURCES), 'checkMetadata': pin(CHECK_METADATA),
        'lexicalReference': sources['lexicalReference'],
        'schemas': sources['schemas'],
        'sourceMap': pin(SOURCE_MAP),
        'sourceMapSourcesDifferFromSourcesJson': sorted({p['path'] for p in json.loads(SOURCE_MAP.read_bytes())['sources']} ^ {p['path'] for p in sources['schemas']}),
        'harvest': harvest_pin,
        'archGitHead': subprocess.run(['git', '-C', str(ARCH), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip(),
        'archNote': 'worktree may be dirty; authority is the sha256/bytes pins verified by check_metadata.load()',
        'refs': [{'ref': ref, 'targetId': target_ids[ref], 'documentId': ref.split('#')[0]} for ref in refs],
    }
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=1) + '\n')
    result = {
        'standing': 'POSITIVE SCHEMA WITNESS EVIDENCE ONLY; not semantic identity, not replay validity, no M1 or generator approval',
        'checkedWith': 'witness_common.check: reference.typed + canonical + parse round trip + reference.validate + ExactValidator(registry).is_valid',
        'totalTargets': len(refs),
        'covered': sum(1 for r in refs if by_ref.get(r)),
        'uncovered': len(uncovered),
        'provedUnsatisfiable': len(proved),
        'uncoveredNotProved': len(uncovered) - len(proved),
        'caseCount': len(corpus['cases']),
        'validCaseCount': sum(len(v) for v in by_ref.values()),
        'casesByOrigin': dict(origins),
        'refsCoveredBySeed': len(seeded_refs),
        'refsCoveredByGenerated': len(generated_refs),
        'refsCoveredOnlyBySeed': len(seeded_refs - generated_refs),
        'refsCoveredOnlyByGenerated': len(generated_refs - seeded_refs),
        'minCasesPerCoveredRef': min((len(v) for v in by_ref.values()), default=0),
        'perDocument': {d: {'targets': t, 'covered': c} for d, (t, c) in sorted(per_doc.items())},
        'exactCodecLimits': {'integer': ['-2^63', '2^64-1'], 'floats': 'forbidden', 'strings': 'Unicode scalar values',
                             'maxCanonicalBytes': 4 * 1024 * 1024, 'maxContainerDepth': 32},
        'maxWitnessCanonicalBytes': max((len(reference.canonical(c['value'])) for c in corpus['cases']), default=0),
        'generatorLimits': report['limits'],
        'generationSeconds': report['seconds'],
        'budgetExhaustedTargets': [r for r, v in report['perTarget'].items() if v['budgetExhausted']],
        'uncoveredRefs': sorted(uncovered),
        'defects': defects,
        'passed': not defects,
    }
    (OUT / 'result.json').write_text(json.dumps(result, indent=1) + '\n')
    print(json.dumps({k: result[k] for k in ('totalTargets', 'covered', 'uncovered', 'provedUnsatisfiable', 'caseCount', 'casesByOrigin', 'passed')}))
    for d in defects[:30]:
        print('DEFECT', d, file=sys.stderr)
    return 0 if not defects else 1


if __name__ == '__main__':
    sys.exit(main())
