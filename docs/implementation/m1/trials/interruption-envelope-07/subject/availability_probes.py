"""Composite delivery checks using the existing native availability projector."""
import ast
import copy
import types


def run(native_bytes, ref, registry, schema, inventory, fixtures, join_module, base_probes):
    tree = ast.parse(native_bytes)
    names = {"release_absence_notices", "invocation_availability"}
    nodes = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in names:
            nodes.append(node)
        elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "PUBLIC_ROUTE_REMEDIES" for t in node.targets):
            nodes.append(node)
    assert len(nodes) == 3
    owner = {}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), "pinned-native-availability-functions", "exec"), owner)
    project = owner['invocation_availability']
    captured = []

    def capture(record, envelope):
        result = join_module.validate_interruption_join(record, envelope)
        captured.append((copy.deepcopy(record), copy.deepcopy(envelope)))
        return result

    adapter = types.SimpleNamespace(JoinRefusal=join_module.JoinRefusal,
                                    validate_interruption_join=capture,
                                    validate_preplanning_interruption=join_module.validate_preplanning_interruption)
    base_probes.run(ref, registry, schema, {'reportFixtures': fixtures, 'inventory': inventory}, adapter)
    before = captured[0]
    after = next((r, e) for r, e in captured if e['kind'] == 'run')
    multiple = next((r, e) for r, e in captured if len(r['orderedSteps']) == 3 and
                    sum(s['kind'] == 'analysis' for s in r['orderedSteps']) == 2)
    query = next((r, e) for r, e in captured if r['workflow'] == {'kind': 'builtin', 'name': 'candidates'})
    rows = []

    def context(record, selections):
        return {'requestId': record['requestId'], 'workflow': copy.deepcopy(record['workflow']),
                'perStep': copy.deepcopy(selections)}

    def notice(path='workspace'):
        return {'capabilityId': 'call-graph', 'languageMode': 'typescript', 'workspaceRoot': path}

    def env_with(record_env, selections, include=True):
        record, envelope = copy.deepcopy(record_env)
        envelope.pop('availability', None)
        if include:
            envelope['availability'] = project([(s['stepId'], s['undeclared']) for s in selections])
        return record, envelope, context(record, selections)

    def probe(name, record, envelope, selected, expected=None, shape=True):
        if shape:
            ref.validate({'$ref': 'urn:opensip:product-v1:workflows:evaluator3:invocation:3'}, record, registry)
            ref.validate({'$ref': schema['$id']}, envelope, registry)
        got = None
        try:
            join_module.validate_interruption_delivery(record, envelope, selected, inventory, project)
        except join_module.JoinRefusal as error:
            got = str(error)
        assert got == expected, (name, got, expected)
        rows.append({'case': name, 'result': got or 'accepted', 'bothShapesAdmitted': shape})

    for label, selected in [('no-selection', []), ('selected-no-absences', [{'stepId': 0, 'undeclared': []}]),
                            ('selected-before-commit', [{'stepId': 0, 'undeclared': [notice()]}])]:
        args = env_with(before, selected)
        probe(label, *args)
        r, e, c = copy.deepcopy(args)
        e.pop('availability')
        probe(label+'-omission', r, e, c, 'J-AVAILABILITY-PROJECTION')
    selected = [{'stepId': 0, 'undeclared': [notice('w'*4096)]}]
    for label, pair in [('no-run-failure', before), ('committed-run', after)]:
        args = env_with(pair, selected)
        probe(label+'-full-root', *args)
        r, e, c = copy.deepcopy(args)
        e['availability']['steps'][0]['notices'][0]['workspaceRoot'] = 'w'*1024
        probe(label+'-root-truncation', r, e, c, 'J-AVAILABILITY-PROJECTION')
    r, e, c = env_with(before, selected)
    e.pop('errors'); e['kind'] = 'invocation'; e['invocation'] = copy.deepcopy(r)
    probe('no-run-invocation-keeps-selection', r, e, c)
    r, e, c = env_with(before, selected)
    r['stepResults'][0] = {'stepId': 0, 'outcome': 'rejected', 'attempts': [{'executionId': 'exec1_'+'1'*32, 'outcome': 'rejected'}],
                           'termination': {'class': 'request-rejected', 'errorCode': 'CONFIG.INVALID',
                                           'domainDetail': {'code': 'CONFIG.INVALID', 'remedy': 'Correct the invalid configuration.'}}}
    e['errors'] = [copy.deepcopy(r['stepResults'][0]['termination']['domainDetail'])]
    probe('recorded-error-and-availability-coexist-without-run', r, e, c)
    for outcome in ('cancelled', 'rejected'):
        r, e, c = env_with(before, [{'stepId': 0, 'undeclared': [notice()]}])
        r['stepResults'][0]['attempts'] = []
        if outcome == 'rejected':
            r['stepResults'][0]['outcome'] = 'rejected'
            r['stepResults'][0]['termination'] = {'class': 'request-rejected', 'errorCode': 'REQUEST.PRECONDITION_FAILED'}
        probe('unstarted-'+outcome+'-cannot-select', r, e, c, 'J-AVAILABILITY-SELECTION')
    pair = copy.deepcopy(multiple)
    selected = [{'stepId': 0, 'undeclared': [notice('unit-'+str(i)) for i in range(1023)]},
                {'stepId': 1, 'undeclared': [notice('unit-'+str(i)) for i in range(1023)]}]
    args = env_with(pair, selected)
    assert args[1]['availability']['totalNoticeCount'] == 2046
    probe('two-selections-compose-2046-duplicate-cross-step-tuples', *args)
    for name, edit in [
        ('count', lambda c: c.update(totalNoticeCount=0)),
        ('step-omission', lambda c: c['steps'].pop()),
        ('step-order', lambda c: c['steps'].reverse()),
        ('remedy', lambda c: c['steps'][0]['notices'][0].update(remedy='Invented remedy.')),
        ('tuple-omission', lambda c: c['steps'][0]['notices'].pop())]:
        r, e, c = copy.deepcopy(args); edit(e['availability'])
        probe('projection-'+name, r, e, c, 'J-AVAILABILITY-PROJECTION')
    r, e, c = env_with(query, [], include=False)
    probe('query-has-no-selections-and-no-availability', r, e, c)
    e['availability'] = project([])
    probe('query-cannot-invent-empty-selection-disclosure', r, e, c, 'J-AVAILABILITY-PROJECTION')
    for name, edit in [
        ('request', lambda c: c.update(requestId='req1_'+'f'*32)),
        ('workflow', lambda c: c.update(workflow={'kind': 'builtin', 'name': 'fit'})),
        ('duplicate-step', lambda c: c['perStep'].append(copy.deepcopy(c['perStep'][0]))),
        ('duplicate-tuple', lambda c: c['perStep'][0]['undeclared'].append(copy.deepcopy(c['perStep'][0]['undeclared'][0]))),
        ('non-analysis-step', lambda c: c['perStep'][0].update(stepId=1)),
        ('bool-step', lambda c: c['perStep'][0].update(stepId=False))]:
        r, e, c = env_with(before, [{'stepId': 0, 'undeclared': [notice()]}]); edit(c)
        expected = 'J-AVAILABILITY-CORRELATION' if name in ('request', 'workflow') else 'J-AVAILABILITY-SELECTION'
        probe('context-'+name, r, e, c, expected)
    r, e, c = env_with(before, [{'stepId': 0, 'undeclared': []}])
    r['stepResults'][0] = {'stepId': 0, 'outcome': 'skipped', 'attempts': [], 'skipReason': 'dependency-not-completed',
                           'termination': {'class': 'request-rejected', 'errorCode': 'REQUEST.PRECONDITION_FAILED'}}
    probe('skipped-step-cannot-retain-selection', r, e, c, 'J-AVAILABILITY-SELECTION')
    r['stepResults'][0]['termination']['domainDetail'] = {'code': 'CONFIG.INVALID', 'remedy': 'Invented skipped detail.'}
    probe('skipped-step-detail-laundering-refused', r, e, c, 'J-INTERRUPTION-SKIPPED-STEP')
    for name in (None, 'analyze', 'candidates'):
        ctx = {'stage': 'before-planning', 'requestId': before[0]['requestId'], 'signal': 'SIGINT'}
        env = copy.deepcopy(before[1]); env.pop('projectId', None); env.pop('availability', None)
        if name == 'analyze': env['availability'] = project([])
        ref.validate({'$ref': schema['$id']}, env, registry)
        assert join_module.validate_preplanning_delivery(ctx, env, name, inventory, project)
        rows.append({'case': 'preplanning-command-'+str(name), 'result': 'accepted', 'envelopeShapeAdmitted': True})
        env['availability'] = project([(0, [notice()])])
        try:
            join_module.validate_preplanning_delivery(ctx, env, name, inventory, project)
        except join_module.JoinRefusal as error:
            assert str(error) == 'J-AVAILABILITY-PROJECTION'
        else:
            raise AssertionError('invented preplanning selection')
        rows.append({'case': 'preplanning-command-'+str(name)+'-invented-selection', 'result': 'refused'})
    return {'nativeFunctionsExecuted': sorted(names), 'probes': rows,
            'limits': 'Synthetic already-admitted host selection contexts; real RequestContext custody, selection retention and final dispatcher integration remain implementation duties.'}
