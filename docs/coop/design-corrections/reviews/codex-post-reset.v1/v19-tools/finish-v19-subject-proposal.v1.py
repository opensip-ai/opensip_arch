from pathlib import Path
import json,hashlib,shutil,ast,copy
b=Path('/tmp/opensip-design-corrections');co=b/'v19-subject-coauthor.v1';out=b/'v19-combined-proposal.v1';root=out/'work';load=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();h=load(co/'handoff.json');receipt=load(co/'response.json');assert not receipt['is_error'] and receipt['session_id']=='4b48ccdd-92fb-4f92-9db2-ac8942f796d6';assert h['technicalAssent']['value'];wfrel='docs/coop/design-corrections/workflows/workflows_model.v1.py';assert sha(root/wfrel)==h['proposedFix']['beforeSha256'];assert sha(co/'workflow.proposed.py')==h['proposedFix']['afterSha256']
s=(co/'workflow.proposed.py').read_text();start=s.index('            # The DYNAMIC half');end=s.index("            if obs.get('subject'):",start)
s=s[:start]+'''            # Preserve an explicitly supplied subject, including an empty string, which the
            # published BoundedText schema admits. Native scope refusals carry field:count>limit.
            # This projects trusted observations; schema validation still owns malformed values.
'''+s[end:];s=s.replace("            if obs.get('subject'):\n                t['domainDetail']['subject'] = obs['subject']", "            if 'subject' in obs:\n                t['domainDetail']['subject'] = obs['subject']",1)
(root/wfrel).write_text(s)
# Root chooses the literal-presence alternative explicitly accepted in coauthor handoff V19S-ROOT-3.
# BoundedText admits empty strings; falsy malformed values should not silently disappear either.
checks=[]
for name,rel,anchor in [('check_workflows.subject.block.py','docs/coop/design-corrections/workflows/check_workflows.v1.py','a = argparse.ArgumentParser();'),('check_integration.subject.block.py','docs/coop/design-corrections/check-integration.py','parser = argparse.ArgumentParser();')]:
 block=(co/'checks'/name).read_text();first=block.index('_SUBJECT_OBS =') if 'workflows.' in name else block.index('def scope_limit_observation(')
 block='# Preserve the bounded subject when projecting native refusals through workflows.\n'+block[first:]
 if 'workflows.' in name:
  a=block.index('# ONE record, ONE rule.');z=block.index('# The subject is COPIED',a)
  block=block[:a]+'''# Existing nonempty/absent subject behavior agrees with Refusal.termination().
for _label, _subject in (('present', 'importIds:257>256'), ('absent', None)):
    _obs = {k: v for k, v in _SUBJECT_OBS.items() if k != 'subject'}
    if _subject is not None:
        _obs['subject'] = _subject
    check('termination.both-producers-agree-on-nonempty-or-absent.' + _label,
          M.terminate(_obs) == M.Refusal(_SUBJECT_OBS['errorCode'], _SUBJECT_OBS['detail'],
                                         _SUBJECT_OBS['remedy'], _subject).termination())
check('termination.explicit-empty-subject-is-preserved',
      M.terminate(dict(_SUBJECT_OBS, subject=''))['domainDetail'].get('subject') == '')
'''+block[z:]
  block=block.replace('A malformed trusted observation is still the schema\'s to','A malformed supplied subject is still the schema\'s to')
 else:
  # Add actual invocation composition to durable integration checks, not just terminate helper.
  block+='''
# Synthetic trusted invocation and earlier result from the existing fixture, not an admitted Run.
def _scope_expand(value):
    if isinstance(value, str) and value.startswith('$'):
        return wf['constants'][value[1:]]
    if isinstance(value, list):
        return [_scope_expand(x) for x in value]
    if isinstance(value, dict):
        return {k: _scope_expand(v) for k, v in value.items()}
    return value
_scope_case = _scope_expand(copy.deepcopy(wf['invocationCases'][0]))
_scope_step = _scope_case['steps'][0]
_scope_record = {'schemaFamily': 'opensip.product.invocation', 'schemaMajor': 1,
    'requestId': wf['constants']['REQ'], 'projectId': wf['constants']['PRJ'],
    'workflow': {'kind': 'builtin', 'name': 'analyze'}, 'mode': _scope_case['mode'],
    'orderedSteps': [{'stepId': i, 'kind': _scope_step['kind'],
        'requirement': _scope_step['requirement'], 'dependsOn': [] if i == 0 else [0],
        'dependencyGate': 'completed', 'retryPolicy': _scope_step['retry'],
        'params': _scope_step['params']} for i in range(2)]}
for _field, _count, _prefix in (('semanticClosures', 129, 'closure2:'),
                               ('nativeContextDigests', 129, ''), ('importIds', 257, 'import2:')):
    _detail, _obs = scope_limit_observation(_field, _count, _prefix)
    _inv, _exit = M.W.run_invocation(copy.deepcopy(_scope_record),
        {'0': copy.deepcopy(_scope_case['script']['0']), '1': [_obs]})
    _first, _refused = _inv['stepResults']
    check('scope-refusal-invocation-keeps-exact-step-and-aggregate-subject.' + _field,
          _refused['termination']['domainDetail'] == _detail
          and _inv['termination']['domainDetail'] == _detail and _exit == 2)
    check('scope-refusal-invocation-preserves-earlier-result.' + _field,
          _first['result'] == _scope_case['script']['0'][0]['result'])
    check('scope-refusal-invocation-mints-no-refused-result-or-derivation.' + _field,
          _refused['outcome'] == 'rejected' and 'result' not in _refused
          and all('derivation' not in a for a in _refused['attempts']))
    M.W.validate_import_record('workflows/schemas/invocation-record.schema.json', '', _inv)
    check('scope-refusal-invocation-record-is-schema-admitted.' + _field, True)
'''
 p=root/rel;before=p.read_text();assert before.count(anchor)==1;after=before.replace(anchor,block+'\n'+anchor);ast.parse(after);p.write_text(after);checks.append({'path':rel,'coauthorBlockSha256':sha(co/'checks'/name),'afterSha256':sha(p)})
report={'standing':'Root selected literal key-presence variant expressly accepted by actual coauthor; compacted comments to remove overclaims. Empty string is schema-valid and preserved; malformed supplied values are projected for schema rejection, not silently dropped. Root added actual full invocation composition controls to durable integration checker.','workflowModel':{'path':wfrel,'beforeSha256':h['proposedFix']['beforeSha256'],'coauthorProposalSha256':h['proposedFix']['afterSha256'],'finalSha256':sha(root/wfrel)},'variantAuthority':'v19-subject-coauthor.v1/handoff.json /proposedFix/oneDeliberateDivergenceFromRootsSketch and /changesRequired/2','checkers':checks,'rootAdditionalChecks':'12 actual-invocation composition controls; earlier result is synthetic trusted observation, not proof of earlier fullRunclosure.'};(out/'root-subject-integration.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
