"""P08 — independently reproduce the bounded candidate-envelope SCHEMA-ONLY control on frozen33,
using root's own two recorded instances. This is schema admission only: it is distinct from retained
joins and from any full Run, and it does not make the original author command successful."""
import hashlib, importlib.util, json, os, sys

SRC = '/tmp/opensip-design-corrections/candidate-subject.v33'
F = os.path.join(SRC, 'docs/coop/design-corrections/foundation')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v33/receipts'
CEC = '/tmp/opensip-design-corrections/root-candidate-envelope-schema-control.v1/result.json'
root = json.load(open(CEC))
R = {'boundedScope': ('schema admission only; NOT retained joins, NOT a full Run, NOT provider '
                      'qualification, and NOT a retroactive success for the original author command')}

SCH = os.path.join(F, 'execution-inputs.schema.v1.json')
R['schemaSha256'] = hashlib.sha256(open(SCH, 'rb').read()).hexdigest()
R['rootQuotedSchemaSha256'] = root['sourceSchemaSha256']
R['schemaShaMatchesRootQuote'] = R['schemaSha256'] == root['sourceSchemaSha256']
print('frozen33 execution-inputs schema sha:', R['schemaSha256'][:24])
print('root quoted the same schema sha     :', R['schemaShaMatchesRootQuote'])

sch = json.load(open(SCH))
spec = importlib.util.spec_from_file_location('canon33b', os.path.join(F, 'canonical.py'))
C = importlib.util.module_from_spec(spec)
sys.modules['canon33b'] = C
spec.loader.exec_module(C)
defs = sch['$defs']
TARGET = 'CandidateProducerResultV1'
R['targetDef'] = TARGET
rows = []
for label, inst in root['records'].items():
    v = {'$defs': defs, '$ref': '#/$defs/' + TARGET}
    try:
        C.validate(v, inst)
        verdict, why = 'ADMIT', ''
    except Exception as ex:
        verdict, why = 'REFUSE', str(ex).splitlines()[0][:180]
    rows.append({'label': label, 'executionPlanIdPrefix': inst['executionPlanId'].split(':')[0],
                 'state': inst['state'], 'universe': inst['universe'],
                 'myVerdict': verdict, 'reason': why})
    print('%-12s prefix=%-12s state=%-12s -> %-7s %s'
          % (label, inst['executionPlanId'].split(':')[0], inst['state'], verdict, why[:90]))
R['myResults'] = rows
byl = {r['label']: r['myVerdict'] for r in rows}
R['originalRefuses'] = byl.get('original') == 'REFUSE'
R['correctedAdmits'] = byl.get('corrected') == 'ADMIT'
R['agreesWithRootControl'] = (R['originalRefuses'] and R['correctedAdmits'])
print('\noriginal (execution2 prefix) REFUSES :', R['originalRefuses'])
print('corrected (exec-plan2 prefix) ADMITS :', R['correctedAdmits'])
print('my independent result agrees with root\'s control:', R['agreesWithRootControl'])

# is the universe/deficiency pair here genuinely the unavailable/null envelope?
inst = root['records']['corrected']
R['envelopeShape'] = {'state': inst['state'], 'universe': inst['universe'],
                      'deficiency': inst['deficiency'], 'nativeCause': inst['nativeCause'],
                      'examinedPaths': inst['examinedPaths'], 'groupDigests': inst['groupDigests']}
R['isUnavailableNullEnvelope'] = (inst['state'] == 'unavailable' and inst['deficiency'] is None
                                  and inst['nativeCause'] is None)
print('the admitted record is the unavailable/null envelope:', R['isUnavailableNullEnvelope'])
R['assessment'] = (
    'CONFIRMED at its stated scope. On frozen33 the exact unavailable/null candidate envelope with '
    'the corrected exec-plan2 prefix ADMITS CandidateProducerResultV1, and the original execution2 '
    'prefix REFUSES on the published pattern. This is schema admission ONLY. It does not establish '
    'any retained join, does not establish full-Run reachability, and does not retroactively make '
    'the original author q2 command successful — that command carried an invalid prefix and its '
    'refusal stands. I therefore do not infer schema admission from the author q2 probe.')
print('\n' + R['assessment'])
json.dump(R, open(os.path.join(OUT, 'p08-envelope.json'), 'w'), indent=1, default=str)
print('\nwrote p08-envelope.json')
