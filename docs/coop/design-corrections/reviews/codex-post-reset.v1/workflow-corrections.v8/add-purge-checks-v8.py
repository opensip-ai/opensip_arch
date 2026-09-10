from pathlib import Path
p=Path('docs/coop/design-corrections/workflows/check_workflows.v1.py');s=p.read_text();anchor='# ----------------------------------------------------------------------------- render parity\n';assert s.count(anchor)==1
block='''# ----------------------------------------------------------------------------- complete pinned-purge refusal
PURGE_PINS = [{'pinId':'repair:fix-42','kind':'repair-prerequisite'}, {'pinId':'baseline:main','kind':'baseline'}]
purge_envelope = M.pinned_purge_refusal(C['REQ'], C['RUN1'], PURGE_PINS)
check('purge.failure-is-closed-precondition-2', purge_envelope['kind'] == 'failure' and
      purge_envelope['termination']['errorCode'] == 'REQUEST.PRECONDITION_FAILED' and M.exit_code(purge_envelope['termination']) == 2)
must_valid('purge.complete-envelope-schema', U + 'command-envelope', purge_envelope)
purge_detail = purge_envelope['termination']['domainDetail']
check('purge.names-complete-pins-deterministically', purge_detail['purgeDisclosure']['activePins'] == list(reversed(PURGE_PINS)))
check('purge.disclosure-has-exact-consequences', purge_detail['purgeDisclosure']['consequences'] ==
      ['named-pins-revoked','dependent-evidence-replay-unavailable','sealed-history-retained'])
check('purge.projection-does-not-mutate-ledger-observation', PURGE_PINS[0]['pinId'] == 'repair:fix-42')
for name, change in [
    ('missing-disclosure', lambda d: d.pop('purgeDisclosure')),
    ('empty-pins', lambda d: d['purgeDisclosure'].update(activePins=[])),
    ('duplicate-pin', lambda d: d['purgeDisclosure']['activePins'].append(d['purgeDisclosure']['activePins'][0])),
    ('wrong-pin-order', lambda d: d['purgeDisclosure']['activePins'].reverse()),
    ('unknown-pin-kind', lambda d: d['purgeDisclosure']['activePins'][0].update(kind='guessed')),
    ('unknown-pin-field', lambda d: d['purgeDisclosure']['activePins'][0].update(authorized=True)),
    ('missing-consequence', lambda d: d['purgeDisclosure']['consequences'].pop()),
    ('misordered-consequences', lambda d: d['purgeDisclosure']['consequences'].reverse()),
    ('newline-run-id', lambda d: d['purgeDisclosure'].update(runId=C['RUN1']+'\\n')),
    ('disclosure-on-other-code', lambda d: d.update(code='evidence.purged')),
]:
    bad = copy.deepcopy(purge_detail); change(bad)
    must_invalid('purge.detail-refuses-'+name, U + 'common#/$defs/DomainDetail', bad)
for name, change in [
    ('wrong-subject', lambda e: e['termination']['domainDetail'].update(subject='run2:'+'f'*64)),
    ('hidden-error-disclosure', lambda e: e['errors'][0]['purgeDisclosure']['activePins'].pop()),
    ('wrong-exit', lambda e: e.update(exitCode=0)),
    ('wrong-class', lambda e: e['termination'].update({'class':'operational-failed','errorCode':'HOST.IO_FAILURE','faultCause':'host-io'})),
]:
    bad = copy.deepcopy(purge_envelope)
    # Break aliasing of the producer's repeated detail for an actual cross-field disagreement.
    bad['errors'] = copy.deepcopy(bad['errors']); change(bad)
    try: M.validate_pinned_purge_refusal(bad)
    except (M.Refusal, canonical.AdmissionError): check('purge.envelope-refuses-'+name, True)
    else: check('purge.envelope-refuses-'+name, False)
many_pins = [{'pinId':f'baseline:{i:04}', 'kind':'baseline'} for i in range(65)]
check('purge.more-than-64-pins-not-truncated', len(M.pinned_purge_refusal(C['REQ'], C['RUN1'], many_pins)['errors'][0]['purgeDisclosure']['activePins']) == 65)
purge_cmd = next(c for c in INV['commands'] if c['name']=='purge')
purge_parity = {'run-id':C['RUN1'], 'receipt-id':None, 'availability':'retained', 'termination-class':'request-rejected',
                'purge-disclosure':purge_detail['purgeDisclosure']}
purge_renderings = [M.render({'envelope':purge_envelope,'parity':purge_parity}, fmt, purge_cmd) for fmt in purge_cmd['formats']]
check('purge.complete-disclosure-all-advertised-renderers', M.parity_holds(purge_renderings) and
      all(r['parity']['purge-disclosure'] == purge_detail['purgeDisclosure'] for r in purge_renderings))
reduced = copy.deepcopy(purge_cmd); reduced['parityFields'].remove('purge-disclosure')
must_invalid('purge.inventory-cannot-drop-disclosure', U + 'command-inventory#/$defs/Command', reduced)

'''
p.write_text(s.replace(anchor,block+anchor))
p=Path('docs/coop/design-corrections/check-integration.py');s=p.read_text();anchor="check('integration-check-identifiers-unique', len({c['id'] for c in checks}) == len(checks))";assert s.count(anchor)==1
block='''# Actual reference-store refusal -> complete current public projection. Ledger names/lease
# remain explicit trusted observations; this does not simulate destructive authorization.
rstore.pins.add(rrid)
retained_run_before = F.C.canonical(rstore.query(rrid))
refusal_result = rstore.purge(rrid)
named_pin_observation = [{'pinId':'baseline:main','kind':'baseline'}, {'pinId':'repair:42','kind':'repair-prerequisite'}]
check('pinned-store-refusal-preserves-run-and-pins', refusal_result == 'pinned' and rrid in rstore.pins and
      F.C.canonical(rstore.query(rrid)) == retained_run_before and rstore.availability[rrid]['state'] == 'retained')
purge_public = M.W.pinned_purge_refusal('req1_'+'d'*32, rrid, named_pin_observation)
check('pinned-store-to-closed-public-envelope', M.W.validate_pinned_purge_refusal(purge_public) == purge_public and
      purge_public['termination']['domainDetail']['code'] == 'evidence.pinned' and purge_public['exitCode'] == 2)
check('pinned-store-public-output-names-all-observed-pins',
      purge_public['errors'][0]['purgeDisclosure']['activePins'] == named_pin_observation)
'''
p.write_text(s.replace(anchor,block+anchor))
print('added23 workflow checks and3 actual store-to-public integration checks')
