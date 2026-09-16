"""P06 — (a) is the prescribed provider-unavailable fallback actually gone from BOTH owners, and do
they agree? (b) planning layer4 and the unchanged populations."""
import hashlib, json, os, re

SRC = '/tmp/opensip-design-corrections/candidate-subject.v33'
F = os.path.join(SRC, 'docs/coop/design-corrections/foundation')
A = os.path.join(SRC, 'docs/v2/architecture')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v33/receipts'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v33.json'
man = {f['path']: f for f in json.load(open(MAN))['files']}
R = {}

COMP = os.path.join(F, 'evaluator-composition-contract.v3.md')
EXEC = os.path.join(F, 'execution-inputs-contract.v1.md')
MODEL = os.path.join(F, 'execution_inputs_model.v1.py')
comp, ex, mdl = (open(p, encoding='utf-8').read() for p in (COMP, EXEC, MODEL))

print('--- every provider-unavailable mention in the two contracts ---')
rows = []
for name, t in (('composition-contract', comp), ('execution-inputs-contract', ex)):
    for i, l in enumerate(t.splitlines(), 1):
        if 'provider-unavailable' in l:
            prescriptive = not re.search(r"do not|not carry|forbad|forbid|never|not `provider|is \*\*not\*\*|"
                                         r"may not|rewrit|prescribed the", l, re.I)
            rows.append({'owner': name, 'line': i, 'prescriptive': prescriptive,
                         'text': l.strip()[:230]})
            print('%-26s L%-4d %s %s' % (name, i, 'PRESCRIPTIVE?' if prescriptive else 'negated   ',
                                         l.strip()[:130]))
R['providerUnavailableMentions'] = rows
R['anyPrescriptiveFallbackRemaining'] = [r for r in rows if r['prescriptive']]
print('\nmentions that look prescriptive rather than negated:',
      len(R['anyPrescriptiveFallbackRemaining']))

R['compositionRecordsTheContradiction'] = 'contradiction between two' in comp
R['compositionCorrectsTheEarlierDiagnosis'] = 'too narrow' in comp
R['executionForbidsManufacturedCarrier'] = 'do not manufacture a carrier' in ex
R['bothOwnersNameNullNullForMissingWork'] = ('`(null, null)`' in ex or '(null, null)' in ex) and \
    ('`null`/`null`' in comp or 'null`/`null' in comp)
print('\ncomposition records it as a two-owner contradiction :', R['compositionRecordsTheContradiction'])
print('composition corrects the earlier narrow diagnosis   :', R['compositionCorrectsTheEarlierDiagnosis'])
print('execution forbids manufacturing a carrier           :', R['executionForbidsManufacturedCarrier'])
print('both owners name null/null for pure missing work    :', R['bothOwnersNameNullNullForMissingWork'])

# the model must not emit provider-unavailable as a derived carrier
mdl_rows = [l.strip()[:170] for l in mdl.splitlines() if 'provider-unavailable' in l]
R['modelProviderUnavailableLines'] = mdl_rows[:10]
print('\nmodel lines naming provider-unavailable (%d):' % len(mdl_rows))
for l in mdl_rows[:8]:
    print('   %s' % l[:160])

# ---------------- (b) planning ----------------
L4 = os.path.join(A, 'implementation-normative-inputs.v4.json')
l4 = json.load(open(L4))
R['layer4'] = {'path': 'docs/v2/architecture/implementation-normative-inputs.v4.json',
               'sha256': hashlib.sha256(open(L4, 'rb').read()).hexdigest(),
               'pins': len(l4['files']), 'binds29': len(l4['files']) == 29,
               'standing': str(l4.get('standing'))[:180]}
bad = [f['path'] for f in l4['files'] if man.get(f['path'], {}).get('sha256') != f['sha256']]
R['layer4PinsUnresolved'] = bad
R['layer4AllPinsResolve'] = not bad
print('\nlayer4: %d pins (29: %s) all resolve against frozen33: %s'
      % (len(l4['files']), R['layer4']['binds29'], R['layer4AllPinsResolve']))
for older, key in (('implementation-normative-inputs.v3.json', 'layer3'),
                   ('implementation-normative-inputs.v2.json', 'layer2'),
                   ('implementation-normative-inputs.v1.json', 'layer1Original25')):
    R[key + 'Preserved'] = ('docs/v2/architecture/' + older) in man
print('layer3/layer2/original25 preserved: %s / %s / %s'
      % (R['layer3Preserved'], R['layer2Preserved'], R['layer1Original25Preserved']))
newpins = [f['path'] for f in l4['files']
           if 'execution-inputs' in f['path'] or 'execution_inputs' in f['path']]
R['layer4ExecutionInputsPins'] = newpins
R['layer4PyFiles'] = [f['path'] for f in l4['files'] if f['path'].endswith('.py')]
print('layer4 execution-inputs pins:', newpins)
print('layer4 .py files (reference code must not be a normative input):', R['layer4PyFiles'])

inv = json.load(open(os.path.join(A, 'repository-file-inventory.v1.json')))
cov = json.load(open(os.path.join(A, 'implementation-coverage.v1.json')))
recp = json.load(open(os.path.join(A, 'commit-recovery-plan.v1.json')))
R['populations'] = {'paths': len(inv['files']), 'packages': len(inv['packages']),
                    'coverageMappings': sum(len(v) for v in cov['groups'].values()),
                    'coverageGroups': len(cov['groups']),
                    'milestoneOrder': cov.get('milestoneOrder'),
                    'recoveryCases': len(recp['cases']),
                    'coverageSources': len(cov.get('sources', []))}
R['populationsUnchanged'] = (R['populations']['paths'] == 198 and R['populations']['packages'] == 20
                             and R['populations']['coverageMappings'] == 320
                             and R['populations']['recoveryCases'] == 54)
print('\npopulations: %s' % json.dumps(R['populations']))
print('198/20/320/54 unchanged:', R['populationsUnchanged'])
json.dump(R, open(os.path.join(OUT, 'p06-fallback-planning.json'), 'w'), indent=1, default=str)
print('\nwrote p06-fallback-planning.json')
