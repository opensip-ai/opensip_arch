import copy,json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
ARCH=Path('/Users/sb/code/opensip-ai/opensip_arch')
PUBLIC=('analysis.budget','components.allowedScopes')
def obj(props):return {'type':'object','additionalProperties':False,'required':list(props),'properties':props}
def build(identity):
 cfg=identity['$defs']['semantic-configuration'];rows={};policies=[]
 for group,spec in cfg['properties'].items():
  for field,value_schema in spec['properties'].items():
   key=group+'.'+field
   if key in PUBLIC:
    present=obj({'field':{'const':key},'state':{'const':'disclosed'},'value':copy.deepcopy(value_schema)})
    policy='public-closed-value'
   else:
    props={'field':{'const':key},'state':{'const':'redacted'},'reason':{'const':'configuration-value-not-public'}}
    if value_schema.get('type')=='array':props['itemCount']={'type':'integer','minimum':0,'maximum':value_schema['maxItems']}
    present=obj(props);policy='redact-with-count' if 'itemCount' in props else 'redact-value'
   absent=obj({'field':{'const':key},'state':{'const':'not-present'}})
   rows[key]=present if field in spec.get('required',[]) else {'oneOf':[present,absent]}
   policies.append({'field':key,'policy':policy})
 # Field membership is fixed by the pinned owner, not by untrusted object keys.
 properties={'schemaFamily':{'const':'opensip.report.configuration-disclosure'},'schemaMajor':{'const':1},'policy':{'const':'semantic-configuration-public-fields-v1'},'source':obj({'kind':{'const':'retained-plan-resolved-configuration'},'planId':{'type':'string','pattern':'^plan2:[0-9a-f]{64}(?![\\s\\S])'},'resolvedConfigDigest':copy.deepcopy(identity['$defs']['plan']['properties']['resolvedConfigDigest'])}),
             'fields':obj(rows),
             'limitations':{'const':['resolved-semantic-configuration-only','raw-layers-and-winning-layer-provenance-not-in-this-projection','operational-retention-and-ui-settings-not-plan-bound','other-report-evidence-has-its-own-disclosure-contract']}}
 # The digest annotation points into the source owner's schema, not this one.
 properties['source']['properties']['resolvedConfigDigest'].pop('x-opensip-digest',None)
 return {'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:opensip:product-v1:report:configuration-disclosure:1',**obj(properties)},policies
if __name__=='__main__':
 paths={'identity':'docs/coop/design-corrections/foundation/identity-schemas.v3.json','canonical':'docs/coop/design-corrections/foundation/canonical.py','configuration':'docs/coop/design-corrections/foundation/product-configuration.schema.v2.json','configuration-model':'docs/coop/design-corrections/foundation/product-configuration-model.py','security-owner':'docs/v2/contracts/product-v1/security-and-lifecycle.md','report-dispositions':'docs/v2/architecture/prototype-report-inventory.md'}
 pins=[];docs={}
 for role,path in paths.items():
  p=ARCH/path;raw=p.read_bytes();pins.append({'role':role,'path':str(p),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
  if role=='identity':docs[role]=json.loads(raw)
 schema,policy=build(docs['identity'])
 (HERE/'input-pins.json').write_text(json.dumps({'schemaVersion':1,'files':pins},indent=2)+'\n')
 (HERE/'configuration-disclosure.schema.json').write_text(json.dumps(schema,indent=2)+'\n')
 (HERE/'field-policy.json').write_text(json.dumps({'schemaVersion':1,'standing':'root proposed closed allowlist; no keyword heuristics, per-value digests, paths or arbitrary field names','fields':policy},indent=2)+'\n')
