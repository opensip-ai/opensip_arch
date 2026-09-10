"""v2 diagnosis measurements. Does not rerun original parser or mutate v1/frozen/consumer.

Reads v1 artifacts, kit manifest, selected retained rules, recompute/tamper source,
and root recompute counterexample. Not acceptance.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1 = Path('/tmp/opensip-design-corrections/grok-blind11-diagnosis.v1')
KIT_MAN = Path('/tmp/opensip-design-corrections/consumer-b.v11/subject/consumer-input-manifest.json')
EXPORTS = Path('/tmp/opensip-design-corrections/consumer-b.v11/output/exports')
RECOMPUTE = Path('/tmp/opensip-design-corrections/consumer-b.v11/output/recompute.py')
TAMPER_SRC = Path('/tmp/opensip-design-corrections/consumer-b.v11/output/reconstruct_rest.py')
COUNTER = Path('/tmp/opensip-design-corrections/blind11-root-recompute-counterexample.v1/report.json')
EVAL = Path('/tmp/opensip-design-corrections/consumer-b.v11/output/helpers/evaluator.py')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    man = json.loads(KIT_MAN.read_text())
    kit_paths = [f['path'] for f in man['files']]
    v1_files = {}
    for p in sorted(V1.rglob('*')):
        if p.is_file() and p.name not in ('stderr.log',) and 'exact-inputs' not in p.parts:
            # record all v1 files except huge diagnostic store copies? user said preserve ALL v1 bytes, not copy them.
            # Hash the diagnosis artifacts and note diagnostic dirs exist.
            pass
    artifacts = [
        'review.md',
        'review.json',
        'probes.json',
        'probe-blind11-admission.v1.py',
        'gap-dispositions.json',
        'process.json',
        'prompt.txt',
        'response.raw.json',
        'stderr.log',
    ]
    v1_hashes = {name: {'sha256': sha(V1 / name), 'bytes': (V1 / name).stat().st_size} for name in artifacts}
    v1_probes = json.loads((V1 / 'probes.json').read_text())
    recompute_src = RECOMPUTE.read_text()
    tamper_src = TAMPER_SRC.read_text()
    eval_src = EVAL.read_text()
    selected = []
    for p in sorted(EXPORTS.glob('*.replay.json')):
        d = json.loads(p.read_text())
        selected.append(
            {
                'path': p.name,
                'runId': d.get('runId'),
                'claimedVerdict': d.get('claimedVerdict'),
                'recomputedVerdict': d.get('recomputedVerdict'),
                'proofId': d.get('proofId'),
                'ruleIds': [r.get('ruleId') for r in d.get('ruleResults') or []],
                'compare': d.get('compare'),
            }
        )
    # ts retained program rule
    store = json.loads((EXPORTS / 'ts.store.json').read_text())
    import base64

    blobs = {k: base64.b64decode(v) for k, v in store['blobs'].items()}
    proof = next(o['descriptor'] for o in store['objectTable'].values() if o.get('domain') == 'proof-bundle')
    program = json.loads(blobs[proof['ruleProgramDigest']])
    fact_rels = sorted(
        {
            o['descriptor']['relation']
            for o in store['objectTable'].values()
            if o.get('domain') == 'fact'
        }
    )
    counter = json.loads(COUNTER.read_text())
    report = {
        'standing': (
            'v2 correction measurements. v1 bytes not rewritten. Original parser not rerun. '
            'Not admission or acceptance.'
        ),
        'v1Standing': 'INTERRUPTED_NOT_COMPLETE',
        'v1Hashes': v1_hashes,
        'v1HelperObservationRecomputeFlag': v1_probes['helperObservations']['recomputeComparesSavedReplayVerdicts'],
        'kit': {
            'fileCount': len(man['files']),
            'pythonFiles': [p for p in kit_paths if p.endswith('.py')],
            'includesIdentityModelPy': any(p.endswith('identity-model.v3.py') for p in kit_paths),
            'includesCanonicalPy': any(p.endswith('canonical.py') for p in kit_paths),
            'includesIdentityAndEvidenceMd': any(p.endswith('identity-and-evidence.md') for p in kit_paths),
            'includesIdentitySchemasV3': any('identity-schemas.v3.json' in p for p in kit_paths),
        },
        'recomputeSource': {
            'usesDoubleQuotedReplayKeys': 'replay["claimedVerdict"]' in recompute_src
            and 'replay["recomputedVerdict"]' in recompute_src,
            'usesSingleQuotedReplayKeys': "replay['claimedVerdict']" in recompute_src,
            'comparesSavedVerdictInequalityOnly': 'claimed != recomputed' in recompute_src,
            'invokesEvaluatorReplay': 'from helpers.evaluator' in recompute_src or 'eval_atom' in recompute_src,
            'importsHelperCloseRun': 'from helpers.closure import close_run' in recompute_src,
            'readsProofIdOrRuleResults': 'proofId' in recompute_src or 'ruleResults' in recompute_src,
        },
        'tamperSource': {
            'functionPresent': 'def tamper(' in tamper_src,
            'flipsProofVerdictOnly': 'proof["verdict"]' in tamper_src,
            'setsReplayRefusesFromInequality': 'replayRefuses' in tamper_src and 'proof["verdict"] != original' in tamper_src,
            'invokesEvaluatorOrRecompute': any(
                s in tamper_src[tamper_src.find('def tamper(') : tamper_src.find('def tamper(') + 800]
                for s in ('eval_atom', 'close_run(', 'recompute')
            ),
        },
        'rootRecomputeCounterexample': {
            'path': str(COUNTER),
            'sha256': sha(COUNTER),
            'counterexampleObserved': counter.get('counterexampleObserved'),
            'originalExitCode': counter['observations'][0]['exitCode'],
            'falsifiedExitCode': counter['observations'][1]['exitCode'],
        },
        'selectedReplayRules': selected,
        'tsRetainedProgramRules': program.get('rules'),
        'tsFactRelationsPresent': fact_rels,
        'evalAtomMatchesFileAndClones': 'elif rel == "clones"' in eval_src and 'rel == "file"' in eval_src,
        'evalMayPutHEvaluationSubject': 'put_h("evaluation-subject"' in eval_src or "put_h('evaluation-subject'" in eval_src,
        'actualApplicationPerformed': False,
    }
    (HERE / 'v2-measurements.json').write_text(json.dumps(report, indent=2) + '\n')
    print(
        json.dumps(
            {
                'kitPy': report['kit']['pythonFiles'],
                'v1RecomputeFlag': report['v1HelperObservationRecomputeFlag'],
                'doubleQuoted': report['recomputeSource']['usesDoubleQuotedReplayKeys'],
                'tamperInvokesReplay': report['tamperSource']['invokesEvaluatorOrRecompute'],
                'counterexampleBothExit0': [
                    report['rootRecomputeCounterexample']['originalExitCode'],
                    report['rootRecomputeCounterexample']['falsifiedExitCode'],
                ],
                'selectedRuleIds': sorted({r for row in selected for r in row['ruleIds']}),
                'tsProgram': program.get('rules'),
            },
            indent=2,
        )
    )


if __name__ == '__main__':
    main()
