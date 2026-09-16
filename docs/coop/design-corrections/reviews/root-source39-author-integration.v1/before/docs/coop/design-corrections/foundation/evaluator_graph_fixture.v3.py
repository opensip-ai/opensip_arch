"""Synthetic retained-input fixture for evaluator3; no compiler or repository execution.

Reuses ONLY definitions of historical native-input fixture helpers. It does not execute
historical test suites or reuse their claimed proofs. Every new proof/output is composed
from the new input graph. Native tool/grammar observations remain synthetic, as in the
parent reference; native qualification is expressly not claimed.
"""
import ast,copy,hashlib,importlib.util,json,types
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('graph_composition3',HERE/'evaluator_composition_model.v3.py');E=importlib.util.module_from_spec(spec);spec.loader.exec_module(E)
M=E.M;C=M.C

def fixture_helpers():
    p=HERE/'check-identity.py';tree=ast.parse(p.read_text());body=[]
    for node in tree.body:
        # The first top-level suite loop is a boundary, not a line-number dependency.
        if isinstance(node,ast.For):break
        body.append(node)
    scope={'__file__':str(p),'__name__':'historical_fixture_definitions_only'}
    exec(compile(ast.Module(body=body,type_ignores=[]),str(p),'exec'),scope)
    return types.SimpleNamespace(**scope)

def build_file_inputs(*, atom_override=None, enabled=True, gate=True, budget_limit=10000, enumeration_filter=None, waiver_rows=None, import_specs=None, evidence_use=None, multiple_universes=False, symbol_rows=None, symbol_state="complete", select_exports=False, scope_document=None, complete_required_native=True, import_producer_kind='provider', import_adapter_kind='adapter', additional_disabled_rule=False, symbol_only_second_program=False, unsupported_cell=None, optional_unselected_cell=False, file_coverage_subjects=None, package_coverage_unknown=False):
    """`symbol_only_second_program` (AUTHOR_PENDING_REVIEW, default OFF, changes nothing unless
    set) builds the ASYMMETRIC selected-program shape: the first universe binds only on the
    `inventory` cell and the second binds only on the symbol-kind `syntax` cell. The second
    universe then owns its symbol-extent paths through the retained EnumerationPlan while having
    NO source-path (`file`/`clones`/`vcs-change`) subject scope at all. It requires
    `multiple_universes` and `symbol_rows`, and it alters no default: every existing caller is
    byte-identical. It is used by the repair closed-world selection controls to discriminate a
    selected-program owner census from a source-path scope census on a fully admitted Run.

    `unsupported_cell` (`'required'` / `'optional'`, default OFF) appends a
    `references|syntax-only` cell, which the native capability matrix states as
    `UNSUPPORTED-TYPED`. Its binding is SELECTED with a NON-NULL universe, and the native owner
    helper mints the Coverage that `native-evidence.md` says such a request is answered with:
    `coverage=unknown`, `language-tier-unsupported` / `capability-missing`, admitted by
    `admit_coverage_result_v3`. The fixture asserts nothing about support: the pair is derived by
    the producer helper from the admitted grammars. Used by the execution-account controls for the
    selected-U unsupported disclosure and, when `'required'`, for the matrix-pair proof bridge.

    `optional_unselected_cell` (default OFF) appends an OPTIONAL `syntax|syntax-only` cell -
    a `SUPPORTED-DESIGN` matrix cell, so applicability is decided by the enumerator rather than the
    matrix - whose single binding is the lawful `UnavailableProgramBindingV1` shape of
    `enumeration-contract.v1.md` §1: `{status:'unselected', reason:'optional-unselected'}`,
    `universe=null`, a typed `provider-unavailable`/null pair, host extents still populated, and an
    empty `unavailable` inventory matching that pair. No shape is bent to reach a branch.

    `file_coverage_subjects` (list of paths, default OFF) narrows the RETURNED `file@enumerated`
    partition's committed subjects while the file inventory and binding extent still name every
    path. That is the census shape: nonempty, honestly `complete` partitions whose retained
    Coverage carries NO pair, over an expected-subject set the partitions do not cover.

    `package_coverage_unknown` (default OFF, requires `complete_required_native`) mints the
    required `package@manifest-declared` partition as the producer's own honest UNKNOWN answer
    rather than a complete one. The helper DERIVES the pair and the native owner admits it, so the
    package account carries a REAL typed carrier while an earlier account may carry none. That is
    the discriminating shape for the cross-source first-typed-pair law.

    All four options are keyword-only and default OFF: every existing caller stays byte-identical."""
    if unsupported_cell not in (None,'required','optional'):raise C.AdmissionError('FIXTURE3_UNSUPPORTED_CELL_OPTION')
    H=fixture_helpers();N=H.N;objects={};blobs={}
    def blob(value):
        raw=value if type(value) is bytes else C.canonical(value)
        digest=hashlib.sha256(raw).hexdigest();blobs[digest]=raw;return digest
    def add(domain,**fields):
        record={'schemaVersion':2,**fields};key=M.identifier(domain,record);objects[key]=(domain,record);return key
    def tree(files):return sorted(({'path':p,'sha256':blob(b),'bytes':len(b)} for p,b in files.items()),key=lambda r:r['path'].encode())
    evaluator=add('closure',kind='evaluator',manifestDigest=blob(b'evaluator3 fixture manifest'),tree=[],semanticVersion='3.0.0',protocolMajor=3,platform='macos-aarch64')
    provider=add('closure',kind='provider',manifestDigest=blob(b'enumerator fixture manifest'),tree=[],semanticVersion='1.0.0',protocolMajor=3,platform='macos-aarch64')
    detector=add('closure',kind='detector',manifestDigest=blob(b'declarative detector fixture manifest'),tree=[],semanticVersion='1.0.0',protocolMajor=3,platform='any')
    native=H.syntax_inputs(objects,blobs,add,blob,tree)
    sources={'README.md':b'# Synthetic fixture\n','src/index.ts':b'export const x = 1;\n','extensionless':b'fixture\n'}
    if symbol_rows is not None:sources['src/index.ts']=b'export function x() {}\n'
    universe_ids=[native['universeDigest']]
    if multiple_universes:
        alternate=copy.deepcopy(native['universe']);alternate['selectedGrammarIds']=['typescript.v1']
        bound=N.bind_syntax_universe(alternate,native['admission'],native['context'],{},[])
        if bound['result']!='ADMIT':raise C.AdmissionError('FIXTURE3_ALTERNATE_NATIVE_UNIVERSE')
        digest=M.native_universe_frame('native.semantic-universe.syntax.v2',alternate,blobs)
        assert digest==bound['sourceUniverse'] and digest!=universe_ids[0]
        universe_ids.append(digest)
    inventory=tree(sources);paths=[r['path'] for r in inventory]
    config=blob({'analysis':{'profileId':'default','capabilities':['inventory'],'budget':{'unit':'work-units','limit':budget_limit}},'components':{},'discovery':{},'policy':{},'evidence':{}})
    scope=blob({'schemaVersion':2,'workspaceRoots':['.'],'pathPrefixes':['.'],'excludedPathPrefixes':[]})
    vcs=blob({'schemaVersion':2,'kind':'none','commitId':None,'dirty':False,'sourceInventoryDigest':blob(inventory)})
    project='prj1-'+hashlib.sha256(b'fixture project').hexdigest()
    snapshot=add('snapshot',projectId=project,sourceInventory=inventory,resolvedConfigDigest=config,scopeDigest=scope,vcsDigest=vcs)
    # Empty admitted boundary list for the synthetic source; no real filesystem discovery claim.
    membership=N.assign_membership([],paths)
    enum={'schemaVersion':1,'snapshotId':snapshot,'scopeDigest':scope,'membershipDigest':blob(membership),'cells':[{'capabilityId':'inventory','languageMode':'syntax-only','workspaceRoot':'.','required':True,'kinds':['file','package'],
        'programBindings':[{'ordinal':0,'provenance':'default-unit','enumerator':{'status':'selected','closureId':provider},'nativeContextDigest':native['contextDigest'],'universe':native['universeDigest'],'programEntry':None,'extents':[{'kind':'file','paths':E.cset(paths)},{'kind':'package','paths':[]}]}]}]}
    if multiple_universes:
        binding=copy.deepcopy(enum['cells'][0]['programBindings'][0]);binding.update(ordinal=1,provenance='explicit-plan-selection',universe=universe_ids[1]);enum['cells'][0]['programBindings'].append(binding)
    if symbol_rows is not None:
        cell=copy.deepcopy(enum['cells'][0]);cell.update(capabilityId='syntax',kinds=['symbol'])
        for binding in cell['programBindings']:binding['extents']=[{'kind':'symbol','paths':['src/index.ts']}]
        enum['cells'].append(cell)
    if symbol_only_second_program:
        # The second universe leaves the inventory cell entirely and keeps only its symbol
        # binding, so it owns src/index.ts through the retained symbol extent alone.
        if not multiple_universes or symbol_rows is None:raise C.AdmissionError('FIXTURE3_SYMBOL_ONLY_REQUIRES_TWO_PROGRAMS')
        enum['cells'][0]['programBindings']=[enum['cells'][0]['programBindings'][0]]
        second=copy.deepcopy(enum['cells'][1]['programBindings'][1]);second['ordinal']=0
        enum['cells'][1]['programBindings']=[second]
    # Extra cells for the execution-account applicability/disclosure controls. Both default OFF.
    if unsupported_cell is not None:
        enum['cells'].append({'capabilityId':'references','languageMode':'syntax-only','workspaceRoot':'.',
            'required':unsupported_cell=='required','kinds':['symbol'],
            'programBindings':[{'ordinal':0,'provenance':'default-unit',
                'enumerator':{'status':'selected','closureId':provider},
                'nativeContextDigest':native['contextDigest'],'universe':universe_ids[0],
                'programEntry':None,'extents':[{'kind':'symbol','paths':['src/index.ts']}]}]})
    if optional_unselected_cell:
        # `syntax|syntax-only` is SUPPORTED-DESIGN, so applicability is decided by the ENUMERATOR
        # and not by the matrix. Its symbol kind is also not the kind the default `file` rule
        # enumerates, so the unavailable inventory this shape requires does not silently turn the
        # rule's own enumeration incomplete and confuse what the control is measuring.
        if symbol_rows is not None:raise C.AdmissionError('FIXTURE3_UNSELECTED_SYNTAX_CELL_CONFLICTS_WITH_SYMBOL_ROWS')
        enum['cells'].append({'capabilityId':'syntax','languageMode':'syntax-only','workspaceRoot':'.',
            'required':False,'kinds':['symbol'],
            'programBindings':[{'ordinal':0,'provenance':'default-unit',
                'enumerator':{'status':'unselected','reason':'optional-unselected'},
                'nativeContextDigest':None,'universe':None,'programEntry':None,
                'extents':[{'kind':'symbol','paths':['src/index.ts']}],
                'deficiency':'provider-unavailable','nativeCause':None}]})
    # cells is x-opensip-order {by:[capabilityId,languageMode,workspaceRoot]} and cellOrdinal IS
    # the index in that sorted array, so a new cell may land before an existing one. Sort once and
    # read every cellOrdinal from this map instead of a literal. With no extra cell the order is
    # already inventory < syntax, so this is a no-op and existing callers stay byte-identical.
    enum['cells'].sort(key=lambda c:(c['capabilityId'],c['languageMode'],c['workspaceRoot']))
    cell_ordinal_of={c['capabilityId']:i for i,c in enumerate(enum['cells'])}
    enum_digest=blob(enum)
    atom=atom_override or {'op':'exists','relation':'file','minResolution':'enumerated','filters':[]}
    if symbol_rows is not None and atom_override is None:atom={'op':'exists','relation':'declares','minResolution':'syntactic','filters':[]}
    primary_kind='symbol' if symbol_rows is not None else 'file'
    rule={'ruleId':'file-observed','ruleProgramRef':{'contributionId':'fixture','ruleStableId':'file-observed','semanticsMajor':2,'programDigest':blob(atom)},'enabled':enabled,'severity':'error','gate':gate,'subjectEnumeration':{'universe':'syntax','subjectKind':'export' if select_exports else primary_kind},'emitWhen':atom,'evidenceUse':evidence_use or []}
    if enumeration_filter:rule['subjectEnumeration'].update(enumeration_filter)
    rules=[rule]
    if additional_disabled_rule:
        disabled=copy.deepcopy(rule);disabled.update(ruleId='z-disabled',enabled=False)
        disabled['ruleProgramRef']['ruleStableId']='z-disabled';rules.append(disabled)
    policy={'schemaFamily':'opensip.product.policy','schemaMajor':2,'gateSeverityAtLeast':'error','rules':rules};policy_digest=blob(policy)
    waivers={'schemaFamily':'opensip.product.waivers','schemaMajor':1,'waivers':waiver_rows or []}
    emission={'schemaVersion':1,'policyDigest':policy_digest,'rules':[{'ruleId':rule['ruleId'],'contributionId':'fixture','ruleStableId':'file-observed','semanticsMajor':2,'detectorClosure':detector,'stabilityClass':'path-stable','emissionProfile':'declarative-subject-v1'}]}
    if additional_disabled_rule:
        disabled_emission=copy.deepcopy(emission['rules'][0])
        disabled_emission.update(ruleId='z-disabled',ruleStableId='z-disabled');emission['rules'].append(disabled_emission)
    parameters=E.cset([{'schemaDigest':blob((HERE/'enumeration-plan.schema.v1.json').read_bytes()),'payloadDigest':enum_digest},
                      {'schemaDigest':blob((HERE/'evaluator-emission-plan.schema.v1.json').read_bytes()),'payloadDigest':blob(emission)}])
    if scope_document is not None:
        parameters=E.cset(parameters+[{'schemaDigest':blob((HERE.parent/'workflows/schemas/policy-document.schema.json').read_bytes()),'payloadDigest':blob(scope_document)}])
    spec_record={'schemaVersion':2,'requestedCapabilities':[{'capabilityId':'inventory','languageMode':'syntax-only','workspaceRoot':'.','required':True}],'policyPackIds':['fixture.file-observed'],'parameters':parameters}
    if symbol_rows is not None:spec_record['requestedCapabilities'].append({'capabilityId':'syntax','languageMode':'syntax-only','workspaceRoot':'.','required':True})
    if unsupported_cell is not None:spec_record['requestedCapabilities'].append({'capabilityId':'references','languageMode':'syntax-only','workspaceRoot':'.','required':unsupported_cell=='required'})
    if optional_unselected_cell:spec_record['requestedCapabilities'].append({'capabilityId':'syntax','languageMode':'syntax-only','workspaceRoot':'.','required':False})
    # requestedCapabilities is x-opensip-order: canonical-set. Cells and requests are joined as
    # sorted TUPLE SETS, so this reorders nothing for existing callers and only keeps the new
    # rows lawful. (The default and `syntax` callers are already in canonical order.)
    spec_record['requestedCapabilities']=E.cset(spec_record['requestedCapabilities'])
    cap=H.CURRENT_CAPABILITY_MANIFEST_BYTES;cap_digest=blob(cap);cap_id=hashlib.sha256(b'opensip.capability-manifest.v1\0'+cap).hexdigest()
    import_ids=[]
    W=M.workflow_admission()
    adapter=add('closure',kind=import_adapter_kind,manifestDigest=blob(b'import adapter fixture manifest'),tree=[],semanticVersion='1.0.0',protocolMajor=3,platform='any') if import_specs else None
    import_provider=provider if import_producer_kind=='provider' else add('closure',kind=import_producer_kind,manifestDigest=blob(b'import producer fixture manifest'),tree=[],semanticVersion='1.0.0',protocolMajor=3,platform='any')
    for item in import_specs or []:
        kind=item['kind'];payload=item['payload'];schema_doc=W.registry_row(kind,payload['payloadDomain'])['schemaDocument'];raw=(HERE.parent/schema_doc).read_bytes()
        built=W.build_import(kind,payload,payload['payloadDomain'],{payload['payloadDomain']:raw},{'kind':'exact-snapshot','snapshotId':snapshot},import_provider,adapter,[],item.get('scope') or C.parse(blobs[scope]),item['observation'])
        blob(raw);blob(payload)
        for body in item.get('extra_blobs',[]):blob(body)
        for retained in built['retainedPreimages'].values():blob(retained)
        iid=M.identifier('import',built['wrapper']);objects[iid]=('import',built['wrapper']);import_ids.append(iid)
    import_ids=E.cset(import_ids)
    grant=blob({'schemaVersion':2,'projectId':project,'principals':[{'kind':'first-party','closureId':evaluator,'ownerSourceDigest':None}],'analysisOperations':sorted(['native-analysis','read-source']+(['read-import'] if import_ids else [])),'scopeDigest':scope})
    plan_fields=dict(snapshotId=snapshot,capabilityManifestId=cap_id,capabilityManifestBytesDigest=cap_digest,semanticClosures=sorted([evaluator,provider,detector]),analysisSpecDigest=blob(spec_record),resolvedConfigDigest=config,nativeContextDigests=[native['contextDigest']],importIds=import_ids,policyDigest=policy_digest,waiverDigest=blob(waivers),scopeDigest=scope,budget={'unit':'work-units','limit':budget_limit},semanticGrantDigest=grant)
    plan_id=add('plan',**plan_fields);plan=objects[plan_id][1]
    inventory_results=[];population={}
    languages={'README.md':'markdown','src/index.ts':'typescript','extensionless':'unspecified'}
    # Under symbol_only_second_program the inventory cell binds only the first universe and the
    # syntax cell only the second, so each loop below owes records for its own universes only.
    inventory_universes=universe_ids[:1] if symbol_only_second_program else universe_ids
    symbol_universes=universe_ids[1:] if symbol_only_second_program else universe_ids
    for program_ordinal,universe in enumerate(inventory_universes):
        for kind in ['file','package']:
            rows=[{'nativeSubjectId':path,'kind':'file','path':path,'qualifiedName':path,'subjectLanguage':languages[path],'signatureTokens':[],'projections':[]} for path in paths] if kind=='file' else []
            inv={'schemaVersion':1,'planId':plan_id,'parameterDigest':enum_digest,'cellOrdinal':cell_ordinal_of['inventory'],'programOrdinal':program_ordinal,'kind':kind,'state':'complete','deficiency':None,'nativeCause':None,'examinedPaths':E.cset(paths) if kind=='file' else [],'rows':sorted(rows,key=lambda r:r['nativeSubjectId'].encode())}
            digest=blob(inv);inventory_results.append((digest,inv))
            for row in rows:
                sid=M.identifier('evaluation-subject',{'schemaVersion':3,'universe':universe,'kind':'file','nativeSubjectId':row['nativeSubjectId']})
                population[sid]={'subjectId':sid,'universe':universe,'kind':'file','row':row,'collisionPopulationComplete':True}
    if symbol_rows is not None:
        for program_ordinal,universe in enumerate(symbol_universes):
            rows=[]
            for item in symbol_rows:
                tokens=item.get('signatureTokens',['function','x','(',')'])
                projections=[] if item.get('projectionAvailable',True) is False else [{'closureId':detector,'signatureTokens':item.get('detectorTokens',tokens)}]
                row={'nativeSubjectId':item['nativeSubjectId'],'kind':'symbol','path':'src/index.ts','qualifiedName':item.get('qualifiedName','x'),'subjectLanguage':'typescript','signatureTokens':tokens,'projections':projections,'exported':item.get('exported','exported')};rows.append(row)
            inv={'schemaVersion':1,'planId':plan_id,'parameterDigest':enum_digest,'cellOrdinal':cell_ordinal_of['syntax'],'programOrdinal':program_ordinal,'kind':'symbol','state':symbol_state,'deficiency':None if symbol_state=='complete' else 'budget-exhausted','nativeCause':None,'examinedPaths':['src/index.ts'],'rows':sorted(rows,key=lambda r:r['nativeSubjectId'].encode())}
            digest=blob(inv);inventory_results.append((digest,inv))
            for row in rows:
                sid=M.identifier('evaluation-subject',{'schemaVersion':3,'universe':universe,'kind':'symbol','nativeSubjectId':row['nativeSubjectId']})
                population[sid]={'subjectId':sid,'universe':universe,'kind':'symbol','row':row,'collisionPopulationComplete':symbol_state=='complete'}
    if unsupported_cell is not None:
        # Complete symbol census over exactly this binding's symbol extent (the enumeration
        # owner requires examinedPaths == extent for a complete inventory) with no declared
        # symbols. The cell's own answer is the matrix disclosure, not an inventory claim.
        inv={'schemaVersion':1,'planId':plan_id,'parameterDigest':enum_digest,'cellOrdinal':cell_ordinal_of['references'],
            'programOrdinal':0,'kind':'symbol','state':'complete','deficiency':None,'nativeCause':None,
            'examinedPaths':['src/index.ts'],'rows':[]}
        inventory_results.append((blob(inv),inv))
    if optional_unselected_cell:
        # enumeration-contract §1: an optional-unselected binding keeps host extents and empty
        # `unavailable` inventories MATCHING the binding's own typed pair.
        inv={'schemaVersion':1,'planId':plan_id,'parameterDigest':enum_digest,'cellOrdinal':cell_ordinal_of['syntax'],
            'programOrdinal':0,'kind':'symbol','state':'unavailable','deficiency':'provider-unavailable',
            'nativeCause':None,'examinedPaths':[],'rows':[]}
        inventory_results.append((blob(inv),inv))
    view_ids=[];scope_ids=[];coverage_ids=[];all_facts=[]
    for universe in inventory_universes:
        # file_coverage_subjects narrows only the RETURNED partition's committed subjects; the
        # file inventory and the binding extent still name every path, so the expected-source
        # census is genuinely short while the returned Coverage is honestly `complete` over what
        # it did commit to. Nothing is made unlawful to produce the shape.
        scope_id=add('subject-scope',snapshotId=snapshot,sourceUniverse=universe,targetUniverse=universe,relation='file',resolution='enumerated',enumeratorClosure=provider,subjects=E.cset(paths if file_coverage_subjects is None else file_coverage_subjects))
        facts=[]
        relation_schema=blob((HERE/'relation-payload-schemas.v2.json').read_bytes());coverage_schema=blob((HERE.parent/'native/native-evidence.schemas.v2.json').read_bytes())
        for row in inventory:
            facts.append(add('fact',snapshotId=snapshot,relation='file',resolution='enumerated',sourceUniverse=universe,targetUniverse=universe,producerClosure=provider,payloadSchemaDigest=relation_schema,payloadDigest=blob({'path':row['path'],'contentSha256':row['sha256'],'byteLength':row['bytes']}),anchors=[],confidenceMillionths=1000000))
        coverage_payload=H.coverage_result(objects[scope_id][1],universe,True,blobs,paths)
        admitted=N.admit_coverage_result_v3(coverage_payload,objects[scope_id][1],[],coverage_schema)
        if admitted['result']!='ADMIT':raise C.AdmissionError('FIXTURE3_NATIVE_COVERAGE:'+str(admitted))
        coverage_id=add('coverage',scopeId=scope_id,payloadSchemaDigest=coverage_schema,payloadDigest=blob(coverage_payload))
        view_id=add('view',planId=plan_id,scopeIds=[scope_id],facts=E.cset(facts),coverageIds=[coverage_id],producerClosure=provider,schemaDigests=sorted([relation_schema,coverage_schema]))
        view_ids.append(view_id);scope_ids.append(scope_id);coverage_ids.append(coverage_id);all_facts.extend(facts)
    if symbol_rows is not None:
        for universe in symbol_universes:
            subjects=E.cset(row['nativeSubjectId'] for row in symbol_rows)
            scope_id=add('subject-scope',snapshotId=snapshot,sourceUniverse=universe,targetUniverse=universe,relation='declares',resolution='syntactic',enumeratorClosure=provider,subjects=subjects)
            facts=[];raw=sources['src/index.ts'];anchor={'path':'src/index.ts','blobDigest':blob(raw),'startByte':0,'endByte':len(raw)}
            for sid in subjects:
                facts.append(add('fact',snapshotId=snapshot,relation='declares',resolution='syntactic',sourceUniverse=universe,targetUniverse=universe,producerClosure=provider,payloadSchemaDigest=relation_schema,payloadDigest=blob({'container':'symbol:module','declared':sid,'declarationKind':'function'}),anchors=[anchor],confidenceMillionths=1000000))
            coverage_payload=H.coverage_result(objects[scope_id][1],universe,True,blobs,paths)
            admitted=N.admit_coverage_result_v3(coverage_payload,objects[scope_id][1],[],coverage_schema)
            if admitted['result']!='ADMIT':raise C.AdmissionError('FIXTURE3_SYMBOL_COVERAGE:'+str(admitted))
            coverage_id=add('coverage',scopeId=scope_id,payloadSchemaDigest=coverage_schema,payloadDigest=blob(coverage_payload))
            view_id=add('view',planId=plan_id,scopeIds=[scope_id],facts=E.cset(facts),coverageIds=[coverage_id],producerClosure=provider,schemaDigests=sorted([relation_schema,coverage_schema]))
            view_ids.append(view_id);scope_ids.append(scope_id);coverage_ids.append(coverage_id);all_facts.extend(facts)
    if complete_required_native:
        # Explicit complete-empty required work. No absence is inferred merely
        # because no finding/fact was emitted. Native owner admits each Coverage.
        for universe in universe_ids:
            # A required-native pair belongs to the universe whose CELL owns that kind: package
            # work to the inventory-bound universes, symbol work to the symbol-bound ones.
            # Without the split these views bind to no cell outcome and the host capture drops
            # them from selectedRefs, which is EVALUATION_VIEW_ROOTS rather than a real Run.
            pairs=[('package','manifest-declared',[])] if universe in inventory_universes else []
            if symbol_rows is not None and universe in symbol_universes:
                syms=E.cset(row['nativeSubjectId'] for row in symbol_rows)
                pairs.extend([('literal','syntactic',syms),('control-flow','syntactic',syms)])
            for relation,rung,subjects in pairs:
                sid=add('subject-scope',snapshotId=snapshot,sourceUniverse=universe,targetUniverse=universe,relation=relation,resolution=rung,enumeratorClosure=provider,subjects=subjects)
                # package_coverage_unknown mints the required package partition as the producer's
                # own honest UNKNOWN answer instead of a complete one; the helper DERIVES the pair
                # (budget-exhausted / null for this non-resolved rung) and the native owner admits
                # it. Used to put a real typed carrier on a LATER account than the file one.
                _resolved=not (package_coverage_unknown and relation=='package')
                payload=H.coverage_result(objects[sid][1],universe,_resolved,blobs,paths)
                admitted=N.admit_coverage_result_v3(payload,objects[sid][1],[],coverage_schema)
                if admitted['result']!='ADMIT':raise C.AdmissionError('FIXTURE3_EMPTY_REQUIRED_COVERAGE:'+str(admitted))
                cid=add('coverage',scopeId=sid,payloadSchemaDigest=coverage_schema,payloadDigest=blob(payload))
                vid=add('view',planId=plan_id,scopeIds=[sid],facts=[],coverageIds=[cid],producerClosure=provider,schemaDigests=sorted([relation_schema,coverage_schema]))
                view_ids.append(vid);scope_ids.append(sid);coverage_ids.append(cid)
    if unsupported_cell is not None:
        # The lawfully returned answer for an UNSUPPORTED-TYPED request. The producer helper
        # DERIVES the unavailable pair from the admitted grammars and the committed extent; the
        # fixture does not assert it, and the native owner admits the record. It is retained in a
        # real returned view, so it reaches selectedRefs through that view's coverageIds even
        # though the unsupported-typed account will name no coverageIds at all.
        sid=add('subject-scope',snapshotId=snapshot,sourceUniverse=universe_ids[0],targetUniverse=universe_ids[0],relation='references',resolution='resolved-binding',enumeratorClosure=provider,subjects=[])
        payload=H.coverage_result(objects[sid][1],universe_ids[0],True,blobs,paths)
        admitted=N.admit_coverage_result_v3(payload,objects[sid][1],[],coverage_schema)
        if admitted['result']!='ADMIT':raise C.AdmissionError('FIXTURE3_UNSUPPORTED_COVERAGE:'+str(admitted))
        if payload['entry']['coverage']!='unknown' or payload['entry']['deficiency'] is None:
            raise C.AdmissionError('FIXTURE3_UNSUPPORTED_COVERAGE_NOT_DISCLOSED:'+str(payload['entry']))
        cid=add('coverage',scopeId=sid,payloadSchemaDigest=coverage_schema,payloadDigest=blob(payload))
        vid=add('view',planId=plan_id,scopeIds=[sid],facts=[],coverageIds=[cid],producerClosure=provider,schemaDigests=sorted([relation_schema,coverage_schema]))
        view_ids.append(vid);scope_ids.append(sid);coverage_ids.append(cid)
    stage_schema={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:opensip:fixture:evaluator3-view-output','type':'object','additionalProperties':False,'required':['viewId'],'properties':{'viewId':{'type':'string','pattern':'^view2:[0-9a-f]{64}(?![\\s\\S])'}}}
    stage=blob({'schemaVersion':2,'planId':plan_id,'producerClosure':provider,'operation':'derive-inventory-view','parameters':parameters,'outputDomains':['view'],'outputSchemaDigest':blob(stage_schema)})
    execution_id=add('execution-plan',planId=plan_id,stages=[{'ordinal':0,'stageSpecDigest':stage,'requires':[],'outputDomains':['view']}])
    refs=E.cset([{'domain':'view','digest':v.split(':',1)[1]} for v in view_ids]+[{'domain':'import','digest':iid.split(':',1)[1]} for iid in import_ids]+[{'domain':'subject-inventory','digest':d} for d,inv in inventory_results])
    enum_refs=[{'domain':'subject-inventory','digest':d} for d,inv in inventory_results if inv['kind']==primary_kind]
    inputs={'plan':plan,'planId':plan_id,'executionPlanId':execution_id,'evaluatorClosure':evaluator,'policy':policy,'effectiveWaivers':waivers,'emissionPlan':emission,'population':population,
        'enumerations':{rule['ruleId']:{'state':'complete','inventoryRefs':E.cset(enum_refs),'selectedSubjectIds':E.cset(sid for sid,item in population.items() if item['kind']==primary_kind),'unresolvedSubjectIds':[],'incompleteInventoryRefs':[]}},'enumerationDeficiencies':{rule['ruleId']:[]},'requiredEvidenceDeficiencies':{rule['ruleId']:[]},'executionDeficiencies':[],'evaluationInputRefs':refs,'inventoryRowCount':sum(len(inv['rows']) for d,inv in inventory_results),'inventoryLocatorCount':len(inventory_results),'factCount':len(all_facts),'observationCount':0,'coverageCount':len(coverage_ids),'importKinds':{iid:objects[iid][1]['kind'] for iid in import_ids},'closures':{k:v for k,(dom,v) in objects.items() if dom=='closure'}}
    if not enabled:inputs['enumerations'][rule['ruleId']]={'state':'disabled','inventoryRefs':[],'selectedSubjectIds':[],'unresolvedSubjectIds':[],'incompleteInventoryRefs':[]}
    if additional_disabled_rule:
        inputs['enumerations']['z-disabled']={'state':'disabled','inventoryRefs':[],'selectedSubjectIds':[],'unresolvedSubjectIds':[],'incompleteInventoryRefs':[]}
        inputs['enumerationDeficiencies']['z-disabled']=[];inputs['requiredEvidenceDeficiencies']['z-disabled']=[]
    return {'objects':objects,'blobs':blobs,'inputs':inputs,'native':native,'snapshot':objects[snapshot][1],'membership':membership,'enumerationPlan':enum,'inventoryResults':inventory_results,'viewId':view_id,'scopeId':scope_id,'coverageId':coverage_id,'viewIds':E.cset(view_ids),'scopeIds':E.cset(scope_ids),'coverageIds':E.cset(coverage_ids),'coveragePayload':coverage_payload}

def fixture_file_scanner(graph):
    """Bootstrap file scanner for owner-closure input admission only; ignores filters. Its claimed output is never used by full replay or exported as a semantic positive."""
    objects,blobs=graph['objects'],graph['blobs'];scope=objects[graph['scopeId']][1];view=objects[graph['viewId']][1]
    def scan(rule,subject,node,pid):
        if node.get('evidence'):
            return {'kind':'imported-atom','value':'indeterminate','matchingFactIds':[],'uncertainFactIds':[],'matchingImportRows':[],'uncertainImportRows':[],'coverageIds':[],'scopeIds':[],'inputRefs':graph['inputs']['evaluationInputRefs'],'deficiencies':[]}
        if node.get('relation')=='declares':
            matches=[fid for fid in view['facts'] if objects[fid][1]['relation']=='declares' and objects[fid][1]['sourceUniverse']==subject['universe'] and C.parse(blobs[objects[fid][1]['payloadDigest']])['declared']==subject['row']['nativeSubjectId']]
            return {'kind':'native-atom','value':'true' if matches else 'false','matchingFactIds':E.cset(matches),'uncertainFactIds':[],'matchingImportRows':[],'uncertainImportRows':[],'coverageIds':[graph['coverageId']],'scopeIds':[graph['scopeId']],'inputRefs':graph['inputs']['evaluationInputRefs'],'deficiencies':[]}
        if node.get('relation')!='file' or node.get('minResolution')!='enumerated':raise C.AdmissionError('FIXTURE3_ATOM_SUBSET')
        matches=[]
        for fid in view['facts']:
            fact=objects[fid][1];payload=C.parse(blobs[fact['payloadDigest']])
            if fact['sourceUniverse']==subject['universe'] and fact['relation']=='file' and payload['path']==subject['row']['nativeSubjectId']:matches.append(fid)
        return {'kind':'native-atom','value':('true' if matches else 'false') if node['op']=='exists' else ('false' if matches else 'true') if node['op']=='none' else ('true' if len(matches)<=node['n'] else 'false') if node['op']=='count-at-most' else 'true','matchingFactIds':E.cset(matches),'uncertainFactIds':[],'matchingImportRows':[],'uncertainImportRows':[],'coverageIds':[graph['coverageId']],'scopeIds':[graph['scopeId']],'inputRefs':[{'domain':'view','digest':graph['viewId'].split(':',1)[1]}],'deficiencies':[]}
    return scan

def seal_fixture(graph):
    xs=importlib.util.spec_from_file_location('graph_execution_capture3',HERE/'execution_inputs_fixture.v3.py')
    X=importlib.util.module_from_spec(xs);xs.loader.exec_module(X)
    if 'executionInputsDigest' not in graph['inputs']:X.attach_host_capture(graph)
    out=E.compose(graph['inputs'],fixture_file_scanner(graph));objects=copy.deepcopy(graph['objects']);blobs=copy.deepcopy(graph['blobs']);objects.update(out['objects']);blobs.update(out['blobs']);i=graph['inputs']
    def add(domain,fields):
        value={'schemaVersion':3,**fields};key=M.identifier(domain,value);objects[key]=(domain,value);return key
    evidence=add('semantic-evidence',{'planId':i['planId'],'viewIds':graph['viewIds'],'coverageIds':graph['coverageIds'],'importIds':i['plan']['importIds'],'findingIds':out['proof']['findingIds'],'proofBundleId':out['proofBundleId']})
    seal=add('evaluation-seal',{'planId':i['planId'],'executionPlanId':i['executionPlanId'],'evidenceId':evidence,'evaluatorClosure':i['evaluatorClosure'],'policyDigest':i['plan']['policyDigest'],'proofBundleId':out['proofBundleId'],'verdict':out['proof']['verdict']})
    run={'schemaVersion':3,'projectId':graph['snapshot']['projectId'],'snapshotId':i['plan']['snapshotId'],'planId':i['planId'],'evidenceId':evidence,'evaluationSealId':seal,'capabilityManifestId':i['plan']['capabilityManifestId']}
    return run,objects,blobs,out
