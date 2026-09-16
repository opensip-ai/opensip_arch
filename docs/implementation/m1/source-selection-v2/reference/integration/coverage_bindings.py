"""Joint10 coverage correction. Source membership remains an explicit host join.

Shape-fixture helpers are intentionally separate from real retained Run replay.
They preserve historical payload bytes, including known native-inconsistent
witnesses, and cannot establish that a synthetic evidence collection exists.
"""
from pathlib import Path
import ast,copy,hashlib,json
HERE=Path(__file__).resolve().parent
for row in json.loads((HERE/'coverage-inputs.json').read_bytes())['files']:
    path=Path(row['checkpoint']);raw=path.read_bytes()
    assert hashlib.sha256(raw).hexdigest()==row['checkpointSha256']
    assert row['member'] in json.loads(raw)['files']
    raw=(HERE/row['local']).read_bytes()
    assert len(raw)==row['member']['bytes'] and hashlib.sha256(raw).hexdigest()==row['member']['sha256']
SCHEMA=json.loads((HERE/'coverage/coverage-budget.experimental.schema.json').read_bytes())
PROVENANCE=SCHEMA['properties']['provenance']['const']
PROVENANCE['verifiedInDocument'][PROVENANCE['verifiedInDocument'].index('entry-payload-schema-is-selected-native-document')]='entry-payload-schema-is-registered-native-coverage-document'
PROVENANCE['hostAsserted'][PROVENANCE['hostAsserted'].index('source-is-exact-admitted-run-evidence')]='source-is-exact-admitted-run-or-ephemeral-plan-evidence'
NATIVE='urn:opensip:product-v1:native:evidence-schemas:v2'


def schema_into(report):
    data=copy.deepcopy(SCHEMA)
    for key in ['$id','$schema','description']:data.pop(key,None)
    retained=data['properties']['source']
    ephemeral={'type':'object','additionalProperties':False,'required':['planId','evidenceId'],
        'properties':{'planId':{'type':'string','pattern':r'^plan2:[0-9a-f]{64}(?![\s\S])'},'evidenceId':copy.deepcopy(retained['properties']['evidenceId'])}}
    data['properties']['source']={'oneOf':[retained,ephemeral],
        'description':'Exact retained Run/evidence or ephemeral Plan/evidence binding. Ephemeral evidence has no Run identity or retained-history authority.'}
    report['$defs']['EvidencePanelV1']=data
    # This is another candidate of the unreleased report1 carrier, with an
    # explicit incompatible development profile. Old readers must refuse it.
    report['$defs']['BudgetProfileV1']['properties']['profileId']['const']='opensip.report-projection.development-caps.6'
    report['$defs']['InvocationLedgerV1']['description']='Report-at-render projection of the selected invocation owner. Current producers use invocation5; legacy attempt observation majors remain explicit. This projection does not select a codec or retention policy for the full InvocationRecord (L01).'
    return report


def projector_source(raw):
    text=raw.decode();start=text.index('        elif name == "evidence":');end=text.index('        elif name == "graph":',start)
    old=text[start:end];assert old.count('"coverageId": src["coverageId"]')==1 and old.count('len(entries)')==2
    new=old.replace('"coverageId": src["coverageId"]','"source": src["source"]').replace('len(entries)','src["total"]')
    new=new.replace('            prefix(','''            if type(src["total"]) is not int or src["total"] < 0:
                raise ValueError("coverage source total")
            if type(item_cap) is not int or not 0 <= item_cap <= 3956:
                raise ValueError("coverage item cap")
            if len(entries) != min(src["total"], item_cap):
                raise ValueError("coverage hydration prefix incomplete")
            prefix(''')
    return (text[:start]+new+text[end:]).encode()


def native_digest(validation):
    return next(r['sha256'] for r in validation.source_check['schemaSources'] if r['uri']==NATIVE)


def shape_row(payload,validation):
    """Wrap a declared shape-only witness; no native or source admission claim."""
    descriptor={'schemaVersion':2,'scopeId':'scope2:'+payload['key']['subjectScopeCommitment'].split(':',1)[1],
        'payloadSchemaDigest':native_digest(validation),'payloadDigest':hashlib.sha256(validation.C.canonical(payload)).hexdigest()}
    return {'coverageId':'coverage2:'+validation.C.identity('coverage',descriptor),'descriptor':descriptor,'result':copy.deepcopy(payload)}


def shape_source(run_id):
    """Opaque fixture ID, not a minted or retained semantic-evidence descriptor."""
    return {'runId':run_id,'evidenceId':'evidence3:'+hashlib.sha256(('shape-only-coverage-collection:'+run_id).encode()).hexdigest()}


def shape_run_source(run):
    if run['authority']=='authoritative':return shape_source(run['runId'])
    if run['authority']=='ephemeral':return {'planId':run['planId'],'evidenceId':run['evidenceId']}
    raise ValueError('Unsupported coverage source authority')


def shape_input(envelope,payloads,cap,validation):
    # The inherited builder eagerly constructs every source even for query-only
    # commands. No Run coverage source is applicable in those documents.
    if envelope.get('kind')!='run':return None
    rows=sorted((shape_row(v,validation) for v in payloads),key=lambda r:r['coverageId'])
    return {'source':shape_run_source(envelope['run']),'entries':rows[:cap],'total':len(rows),'cap':cap}


def shape_panel(original,run,validation):
    if original.get('state')!='present':return copy.deepcopy(original)
    data=original['data'];rows=sorted((shape_row(v,validation) for v in data['entries']),key=lambda r:r['coverageId'])
    return {'state':'present','data':{'source':shape_run_source(run),'entries':rows,
        'entriesProjection':copy.deepcopy(data['entriesProjection']),'provenance':copy.deepcopy(PROVENANCE)}}


def amend_admission_nodes(nodes):
    fn=next(n for n in nodes if isinstance(n,ast.FunctionDef) and n.name=='admit_document')
    matches=[]
    for n in ast.walk(fn):
        if isinstance(n,ast.If) and ast.unparse(n.test)=='present(evidence)':matches.append(n)
    assert len(matches)==1
    matches[0].body=ast.parse('''data = evidence['data']
need(env['kind'] == 'run', 'J-EVIDENCE-SOURCE-RUN')
if run['authority'] == 'authoritative':
    need(data['source'].get('runId') == run['runId'], 'J-EVIDENCE-SOURCE-RUN')
else:
    need(data['source'] == {'planId': run['planId'], 'evidenceId': run['evidenceId']}, 'J-EVIDENCE-SOURCE-EPHEMERAL')
check_projection(data['entriesProjection'], len(data['entries']), b['maxEvidenceEntries'], 'J-EVIDENCE-COUNTS')
COVERAGE_ROWS(ctx, data, need)
if data['entriesProjection']['omissionCause'] == 'byte-budget':
    deltas.append(data['entriesProjection']['rejectedByteDelta'])
''').body
    walker=next(n for n in nodes if isinstance(n,ast.FunctionDef) and n.name=='embedded_owner_records')
    found=0
    for n in ast.walk(walker):
        if isinstance(n,ast.Tuple) and len(n.elts)==4 and isinstance(n.elts[0],ast.Constant) and n.elts[0].value=='coverage-entry':
            assert ast.unparse(n.elts[1])=='e';n.elts[1]=ast.parse("e['result']",mode='eval').body;found+=1
    assert found==1
    return nodes


def admit_rows(ctx,data,need):
    ids=[r['coverageId'] for r in data['entries']]
    need(ids==sorted(set(ids)),'J-EVIDENCE-ORDER')
    digests=registered_native_digests()
    for row in data['entries']:
        descriptor=row['descriptor'];ctx.reference.typed(descriptor)
        need(descriptor['payloadSchemaDigest'] in digests,'J-EVIDENCE-SCHEMA')
        need(row['coverageId']=='coverage2:'+ctx.reference.identity('coverage',descriptor),'J-EVIDENCE-DESCRIPTOR')
        need(descriptor['payloadDigest']==hashlib.sha256(ctx.reference.canonical(row['result'])).hexdigest(),'J-EVIDENCE-PAYLOAD')


def verify_source_prefix(data, expected_run_id, run, objects, blobs, owner, item_cap):
    """Reference host source join after full report admission.

    Replays the complete retained Run and checks source, total and exact ordered
    prefix. This does not establish the maximal byte-budget prefix or a real
    storage lease; caller must perform shared projection with its admitted inputs.
    """
    scope={}
    path=HERE/'coverage/coverage_source.py'
    exec(compile(path.read_bytes(),str(path),'exec'),scope)
    expected=scope['project'](expected_run_id,run,objects,blobs,item_cap,owner)
    n=len(data['entries'])
    if (data['source']!=expected['source'] or
        data['entriesProjection']['total']!=expected['entriesProjection']['total'] or
        n>len(expected['entries']) or
        owner.C.canonical(data['entries'])!=owner.C.canonical(expected['entries'][:n])):
        raise ValueError('J-EVIDENCE-SOURCE-PREFIX')
    return expected


def coverage_definition_closure(document):
    """Exact reachable local definitions, including descriptions and constraints.

    This comparison is conservative. Any changed coverage definition requires a
    separately selected digest-specific validator, never an inferred migration.
    """
    found={};pending=['CoverageResultV3']
    while pending:
        name=pending.pop()
        if name in found:continue
        node=document['$defs'][name];found[name]=node;walk=[node]
        while walk:
            item=walk.pop()
            if isinstance(item,dict):
                ref=item.get('$ref','')
                if ref.startswith('#/$defs/'):
                    name=ref[len('#/$defs/'):].split('/')[0].replace('~1','/').replace('~0','~');pending.append(name)
                elif ref.startswith('#'):raise ValueError('Unsupported native coverage local reference')
                walk.extend(item.values())
            elif isinstance(item,list):walk.extend(item)
    return found


def registered_native_digests():
    """Two exact registered schema files, not a URI-wide historical allowlist.

    The proposed native document adds new-Plan refusal metadata. Retained native
    payloads keep their original raw full-document digest. Both documents must
    have identical reachable CoverageResultV3 definitions for this shared shape
    validator. Final native source/registry selection remains a separate gate.
    """
    inputs=json.loads((HERE/'input-subjects.json').read_bytes())['subjects']
    unit=next(r for r in inputs if r['unit']=='report-projection')
    manifest_raw=Path(unit['manifest']).read_bytes()
    assert hashlib.sha256(manifest_raw).hexdigest()==unit['manifestSha256']
    pinrow=next(r for r in json.loads(manifest_raw)['files'] if r['path']=='source-pins.json')
    pins_raw=(Path(unit['subject'])/'source-pins.json').read_bytes()
    assert len(pins_raw)==pinrow['bytes'] and hashlib.sha256(pins_raw).hexdigest()==pinrow['sha256']
    pins=json.loads(pins_raw)['files']
    prior=next(r for r in pins if r['path'].endswith('/native/native-evidence.schemas.v2.json'))
    oldraw=Path(prior['path']).read_bytes()
    assert len(oldraw)==prior['bytes'] and hashlib.sha256(oldraw).hexdigest()==prior['sha256']
    current=next(r for r in json.loads((HERE/'source-check-result.json').read_bytes())['schemaSources'] if r['uri']==NATIVE)
    newraw=(HERE/current['path']).read_bytes();assert hashlib.sha256(newraw).hexdigest()==current['sha256']
    old=json.loads(oldraw);new=json.loads(newraw)
    assert old['$id']==new['$id']==NATIVE
    if coverage_definition_closure(old)!=coverage_definition_closure(new):
        raise ValueError('NATIVE-COVERAGE-SCHEMA-SUCCESSION-REQUIRES-VALIDATOR')
    return {prior['sha256'],current['sha256']}
