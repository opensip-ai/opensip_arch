"""Execute owner projections against composed carriers; whole-report joins pending."""
from pathlib import Path
import copy
import hashlib
import json
import types
import unittest
from referencing import Registry,Resource
from referencing.jsonschema import DRAFT202012

HERE=Path(__file__).resolve().parent
source_check=json.loads((HERE/'source-check-result.json').read_text());assert source_check['passed']
schemas={}
for row in source_check['schemaSources']:
    path=Path(row['path']);path=path if path.is_absolute() else HERE/path
    raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==row['sha256']
    schemas[row['uri']]=json.loads(raw)
registry=Registry().with_resources((uri,Resource(contents=doc,specification=DRAFT202012)) for uri,doc in schemas.items())
for row in json.loads((HERE/'model-generation-result.json').read_text())['outputs']:
    raw=(HERE/row['path']).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']


def load(path,name):
    module=types.ModuleType(name);module.__file__=str(path)
    exec(compile(path.read_bytes(),str(path),'exec'),module.__dict__)
    return module


subject_rows=json.loads((HERE/'input-subjects.json').read_text())['subjects']
subjects={r['unit']:Path(r['subject']) for r in subject_rows}
unit_files={}
for row in subject_rows:
    raw=Path(row['manifest']).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['manifestSha256']
    unit_files[row['unit']]={f['path']:f for f in json.loads(raw)['files']}


def read_unit(unit,name):
    raw=(subjects[unit]/name).read_bytes();pin=unit_files[unit][name]
    assert len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256']
    return raw


config_pins=json.loads(read_unit('config-disclosure','input-pins.json'))['files']
for row in config_pins:
    raw=Path(row['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['sha256']
roles={r['role']:Path(r['path']) for r in config_pins}
C=load(roles['canonical'],'joint_canonical')
T=load(HERE/'models/timing.py','joint_timing')
D=load(HERE/'models/disclosure.py','joint_disclosure')
H=load(HERE/'models/history/history.py','joint_history')
report=json.loads((HERE/'composed-sources/report-projection.proposed.schema.json').read_text())
identity=json.loads(roles['identity'].read_text())
config_schema=json.loads((HERE/'composed-sources/configuration-disclosure.schema.json').read_text())
policy=json.loads(read_unit('config-disclosure','field-policy.json'))
history_schema=json.loads((HERE/'composed-sources/explicit-history-panel.schema.json').read_text())
query_schema=json.loads((HERE/'composed-sources/graph-query.proposed.schema.json').read_text())
PID='prj1-'+'2'*64


def validate(ref,value):C.ExactValidator({'$ref':ref},registry=registry).validate(value)


def validate_sub(schema,value):C.ExactValidator(schema,registry=registry).validate(value)


class CarrierTests(unittest.TestCase):
    def test_timing5_owner_projection_matches_composed_attempt_carrier(self):
        shape=report['$defs']['LedgerStepV1']['properties']['attempts']['items']
        for major in [3,4,5]:
            source={'executionId':'exec1_'+'1'*32,'outcome':'completed'}
            if major!=3:source['observedDuration']={'state':'measured','milliseconds':12}
            projected=T.project_attempt(major,source)
            validate_sub(shape,projected)
            self.assertEqual(projected['sourceSchemaMajor'],major)
            self.assertEqual(projected['duration'],{'state':'unavailable','reason':'not-retained'} if major==3 else source['observedDuration'])
            service=T.summarize_attempts([projected])
            validate(report['$id']+'#/$defs/AttemptServiceTimeV1',service)
        self.assertEqual(T.source_support(6),{'state':'incompatible','reason':'retained-schema-major-unsupported'})

    def test_legacy_and_abandoned_timing_cannot_be_forged_in_document(self):
        shape=report['$defs']['LedgerStepV1']['properties']['attempts']['items']
        for major,outcome,value in [(3,'completed',{'state':'measured','milliseconds':0}),
                                   (5,'abandoned',{'state':'measured','milliseconds':1}),
                                   (5,'completed',{'state':'unavailable','reason':'supervisor-lost'}),
                                   (5,'completed',{'state':'unavailable','reason':'not-retained'}),
                                   (5,'completed',{'state':'measured','milliseconds':1.0})]:
            projection={'executionId':'exec1_'+'1'*32,'outcome':outcome,'sourceSchemaMajor':major,'duration':value}
            with self.assertRaises(C.ValidationError):validate_sub(shape,projection)
        abandoned=T.project_attempt(5,{'executionId':'exec1_'+'1'*32,'outcome':'abandoned','observedDuration':T.unavailable('supervisor-lost')})
        validate_sub(shape,abandoned)

    def test_current_render_timing_is_not_a_measured_zero(self):
        step={'stepId':1,'kind':'render','requirement':'required','dependsOn':[0],'dependencyGate':'completed','planRole':'render','recorded':False,
              'attemptServiceTime':{'state':'not-finalized','reason':'render-in-progress'}}
        validate(report['$id']+'#/$defs/LedgerStepV1',step)
        bad=copy.deepcopy(step);bad['attemptServiceTime']={'state':'measured','attemptCount':1,'milliseconds':0}
        with self.assertRaises(C.ValidationError):validate(report['$id']+'#/$defs/LedgerStepV1',bad)

    def test_configuration_owner_output_fits_new_carrier_and_rejects_raw_values(self):
        # Shape/identity-joined synthetic Plan, not full retained Run replay.
        config={'analysis':{'profileId':'private-profile','capabilities':['private-capability'],'budget':{'unit':'work-units','limit':100}},
                'components':{},'discovery':{},'policy':{},'evidence':{}}
        plan={'schemaVersion':2,'snapshotId':'snapshot2:'+'2'*64,'capabilityManifestId':'3'*64,'semanticClosures':[],
              'analysisSpecDigest':'4'*64,'resolvedConfigDigest':hashlib.sha256(C.canonical(config)).hexdigest(),
              'nativeContextDigests':[],'importIds':[],'policyDigest':'5'*64,'waiverDigest':'6'*64,'scopeDigest':'7'*64,
              'budget':config['analysis']['budget'],'semanticGrantDigest':'8'*64,'capabilityManifestBytesDigest':'9'*64}
        disclosure=D.project('plan2:'+C.identity('plan',plan),plan,config,policy,C,identity,config_schema)
        value={'state':'present','data':disclosure}
        validate(report['$id']+'#/$defs/ConfigurationPanelStateV1',value)
        self.assertNotIn(b'private-profile',C.canonical(value));self.assertNotIn(b'private-capability',C.canonical(value))
        bad=copy.deepcopy(value);bad['data']['fields']['analysis.profileId']={'field':'analysis.profileId','state':'disclosed','value':'private-profile'}
        with self.assertRaises(C.ValidationError):validate(report['$id']+'#/$defs/ConfigurationPanelStateV1',bad)

    def test_configuration_loss_uses_existing_closed_panel_states(self):
        for reason in D.SOURCE_FAILURES:
            validate(report['$id']+'#/$defs/ConfigurationPanelStateV1',D.unavailable_source(reason))
        with self.assertRaises(D.DisclosureRefusal):D.unavailable_source('arbitrary host exception')

    def test_typed_query4_and_explicit_history_preserve_current_and_unavailable_slots(self):
        current='run3:'+'1'*64;missing='run3:'+'2'*64
        request=H.admit_request([current,missing],'html');selection=H.plan_selection(request,current)
        queries=[]
        def lookup(run_id):
            queries.append(run_id)
            return {'query':H.QUERY.unavailable(PID,run_id,'purged'),
                    'history':{'state':'unavailable','runId':run_id,'availability':'purged'}}
        rows=H.resolve_slots(selection,PID,lookup,
            lambda v:validate(query_schema['$id']+'#/$defs/GraphQueryResponseV1',v),
            lambda v:validate(history_schema['$id']+'#/$defs/RetainedHistorySlotV1',v))
        self.assertEqual(queries,[missing])
        panel={'selection':selection,'runs':rows,'provenance':copy.deepcopy(history_schema['properties']['provenance']['const'])}
        H.validate_panel(panel,current,lambda v:validate(history_schema['$id'],v))
        validate(report['$id']+'#/$defs/HistoryPanelV1',panel)
        disclosure=report['$defs']['DisclosuresV1']['properties']['explicitHistorySelection']
        validate_sub(disclosure,selection);validate_sub(disclosure,None)
        wrong=H.QUERY.unavailable(PID,missing,'purged');wrong['schemaMajor']=3
        with self.assertRaises(C.ValidationError):validate(query_schema['$id']+'#/$defs/GraphQueryResponseV1',wrong)

    def test_old_automatic_history_shape_remains_admissible(self):
        original=json.loads(read_unit('report-projection','fixtures.json'))
        rows=[d['panels']['history']['data'] for d in original['bases'].values() if d.get('panels',{}).get('history',{}).get('state')=='present']
        self.assertGreater(len(rows),0)
        for row in rows:validate(report['$id']+'#/$defs/HistoryPanelV1',row)

    def test_catalogue_owner_receipts_fit_closed_report_carrier(self):
        # Execute the unchanged owner fixture helpers in a read-only module.
        for name in ['check.py','catalog.py','build_schema.py','input-pins.json','presentation-catalog.schema.json']:
            read_unit('presentation-catalog',name)
        O=load(subjects['presentation-catalog']/'check.py','catalogue_fixture_helpers')
        data=O.fixture();ctx,raw,declared=O.bound(data);receipt=O.admit(ctx,raw,declared)
        selected={g:sorted([list(k) for k in declared[g]],key=C.canonical) for g in O.catalog.GROUPS}
        owner_selected={g:[tuple(k) for k in keys] for g,keys in selected.items()}
        projected=O.select(receipt,owner_selected,ctx['closureId'])
        validate(report['$id']+'#/$defs/DescriptionReceiptV1',projected)
        self.assertEqual(projected['tree'],ctx['closure']['tree'])
        for field in ['tree','platform','protocolMajor','componentManifestDigest','capabilityAuthority']:
            bad=copy.deepcopy(projected);del bad[field]
            with self.assertRaises(C.ValidationError):validate(report['$id']+'#/$defs/DescriptionReceiptV1',bad)
        missing=O.catalog.select_descriptions(None,owner_selected,ctx['closureId'],owner_selected,source_state='not-retained')
        validate(report['$id']+'#/$defs/DescriptionReceiptV1',missing)
        self.assertEqual(missing['reason'],'catalog-not-retained')
        no_catalog=copy.deepcopy(ctx);no_catalog['tree']=[];no_catalog['closure']['tree']=[]
        absent=O.admit(no_catalog,None,declared)
        projected_absent=O.select(absent,owner_selected,ctx['closureId'])
        validate(report['$id']+'#/$defs/DescriptionReceiptV1',projected_absent)
        self.assertEqual(projected_absent['state'],'no-catalogue-declared')

    def test_catalogue_shared_validator_preserves_semantic_order(self):
        catalog_schema=schemas['urn:opensip:product-v1:workflows:presentation-catalog:1']
        O=load(subjects['presentation-catalog']/'check.py','catalogue_order_helpers')
        for group in O.catalog.GROUPS:
            data=O.fixture();data[group][0]['tags'].reverse()
            with self.assertRaises(C.ValidationError):C.validate(catalog_schema,data,registry)


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(CarrierTests))
    value={'standing':'Root owner-output/carrier integration checks only; no complete report/Run custody/product/Claude approval',
           'groups':result.testsRun,'passed':result.wasSuccessful(),
           'limits':['Configuration uses a synthetic shape/identity-admitted Plan','History scenario tests typed unavailable responses; retained Run replay remains a separate owner check','No complete report budget/ledger/source admission or browser checks','Some whole-document semantic joins remain unimplemented']}
    (HERE/'model-carrier-result.json').write_text(json.dumps(value,indent=2)+'\n');print(json.dumps(value,indent=2))
    raise SystemExit(0 if result.wasSuccessful() else 1)
