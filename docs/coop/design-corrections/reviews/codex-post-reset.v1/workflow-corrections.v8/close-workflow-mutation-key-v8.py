from pathlib import Path
import json
wf=Path('docs/coop/design-corrections/workflows');p=wf/'schemas/invocation-record.schema.json';x=json.loads(p.read_text());d=x['$defs']
d['MutationReplayScopeV1']={'type':'object','additionalProperties':False,'required':['schemaVersion','requestId','stepId','projectId','operation'],'properties':{'schemaVersion':{'const':1},'requestId':{'$ref':'urn:opensip:product-v1:workflows:common#/$defs/RequestId'},'stepId':{'$ref':'urn:opensip:product-v1:workflows:common#/$defs/StepId'},'projectId':{'$ref':'urn:opensip:product-v1:workflows:common#/$defs/ProjectId'},'operation':{'allOf':[{'$ref':'urn:opensip:product-v1:workflows:repair#/$defs/MutationOperation'},{'not':{'const':'repair-apply'}}]}},'description':'Retained operational replay namespace for a generic mutation. H(workflow.mutation-intent, this complete record) is its idempotencyKey. The admitted immutable invocation and step own effect inputs; a key grants no authority and never deduplicates different fresh requests. Repair apply uses its separate exact content-derived recipe.'}
d['MutationParams']['properties']['idempotencyKey']['description']='Bare H("workflow.mutation-intent", MutationReplayScopeV1) binding this host-minted requestId, stepId, projectId and mutationClass as operation. The exact scope and admitted immutable step parameters are retained and checked before receipt lookup. Equal COMPLETED replay performs no second effect; separate fresh requests have different keys. Repair apply has a separate step/recipe.'
d['MutationParams']['properties']['mutationClass']['allOf']=[{'not':{'const':'repair-apply'}}]
p.write_text(json.dumps(x,indent=2)+'\n')
p=wf/'workflows_model.v1.py';s=p.read_text();anchor='# ----------------------------------------------------------------------------- evidence retention projection\n';assert s.count(anchor)==1
s=s.replace(anchor,'''# ----------------------------------------------------------------------------- generic mutation replay scope

def mutation_replay_scope(request_id, step_id, project_id, operation):
    scope = {'schemaVersion': 1, 'requestId': request_id, 'stepId': step_id,
             'projectId': project_id, 'operation': operation}
    validate_import_record('workflows/schemas/invocation-record.schema.json', '#/$defs/MutationReplayScopeV1', scope)
    return scope

def mutation_replay_key(scope):
    validate_import_record('workflows/schemas/invocation-record.schema.json', '#/$defs/MutationReplayScopeV1', scope)
    return canonical.identity('workflow.mutation-intent', scope)

def admit_mutation_replay_key(params, scope):
    """Scope comes from the retained host invocation; never caller-selected receipt lookup input.
    This pure join does not admit the effect, authorize it, or implement a mutation ledger.
    """
    validate_import_record('workflows/schemas/invocation-record.schema.json', '#/$defs/MutationParams', params)
    key = mutation_replay_key(scope)
    if params['mutationClass'] != scope['operation'] or params['idempotencyKey'] != key:
        raise canonical.AdmissionError('MUTATION_REPLAY_SCOPE_JOIN')
    return key

'''+anchor);p.write_text(s)
p=Path('docs/v2/contracts/product-v1/workflows-and-surfaces.md');s=p.read_text();anchor='**Mutation idempotence and recovery.** Repair apply uses the raw SHA-256 of\n';assert s.count(anchor)==1
s=s.replace(anchor,'''**Mutation idempotence and recovery.** Generic `mutation` steps use the bare
64-hex `H("workflow.mutation-intent", MutationReplayScopeV1)`. The closed retained
scope is exactly `{schemaVersion:1,requestId,stepId,projectId,operation}`, with
`operation` equal to `MutationParams.mutationClass`. This explicitly succeeds the
former undefined `{operation,projectId,effect preimage}` description. The key is
operational and scoped to one host-minted request and admitted immutable step;
different fresh requests never deduplicate each other's generic mutations.
`sourceStep` resolves inside that same retained invocation, whose admitted
parameters and completed dependency results are immutable. Before lookup or
replay the host validates the scope and full params, recomputes the key and
requires the retained invocation/project/step/operation binding; a caller cannot
nominate another invocation's scope or change effect inputs under an old key.
Receipt lookup is never an effect-authorization mechanism. A same-scope COMPLETED
receipt permits delivery replay with no second effect. Failure, unknown state or
incomplete execution requires the operation's existing recovery law, not blind
re-execution. Recovery started in a new request retains its own operational scope
and the explicit original journal/intent links required by §§6/12.

Repair apply is the explicit content-derived exception: it is a dedicated
`repair-apply` step, excluded from generic MutationParams. It uses the raw SHA-256 of
''')
s=s.replace('and `workflow.candidate`\n(`candidate2:`).','and `workflow.candidate`\n(`candidate2:`). `workflow.mutation-intent` addresses the closed operational\nMutationReplayScopeV1 (§1), returning its bare 64-hex H value.')
p.write_text(s)
p=wf/'check_workflows.v1.py';s=p.read_text();anchor='# ----------------------------------------------------------------------------- complete pinned-purge refusal\n';assert s.count(anchor)==1
block='''# ----------------------------------------------------------------------------- exact generic replay keys
mutation_scope = M.mutation_replay_scope(C['REQ'], 0, C['PRJ'], 'baseline-adopt')
mutation_key = M.mutation_replay_key(mutation_scope)
check('mutation-key.exact-H-preimage-distinguished-from-raw-C',
      mutation_key == canonical.identity('workflow.mutation-intent', mutation_scope) and
      mutation_key != M.raw_sha(canonical.canonical(mutation_scope)))
mutation_params = {'kind':'mutation','mutationClass':'baseline-adopt','idempotencyKey':mutation_key}
check('mutation-key.host-scope-admits-bound-params', M.admit_mutation_replay_key(mutation_params, mutation_scope) == mutation_key)
for field, value in [('requestId','req1_'+'f'*32),('stepId',1),('projectId','prj1-'+'f'*64),('operation','purge')]:
    altered = dict(mutation_scope, **{field:value})
    check('mutation-key.'+field+'-changes-key', M.mutation_replay_key(altered) != mutation_key)
    try:M.admit_mutation_replay_key(mutation_params, altered)
    except canonical.AdmissionError:check('mutation-key.'+field+'-cannot-reuse-key',True)
    else:check('mutation-key.'+field+'-cannot-reuse-key',False)
for name, altered in [('undefined-effect',dict(mutation_scope,effect={})),('repair-apply',dict(mutation_scope,operation='repair-apply')),
                      ('caller-extra-nonce',dict(mutation_scope,nonce=1)),('newline-request',dict(mutation_scope,requestId=C['REQ']+'\\n'))]:
    must_invalid('mutation-key.closed-scope-refuses-'+name, U+'invocation-record#/$defs/MutationReplayScopeV1',altered)
must_invalid('mutation-key.repair-apply-not-generic-mutation', U+'invocation-record#/$defs/MutationParams', dict(mutation_params,mutationClass='repair-apply'))
# Repair apply's existing suite below/above retains its cross-request content-derived replay checks.

'''
p.write_text(s.replace(anchor,block+anchor));print('closed generic mutation scope; repair-apply unchanged')
