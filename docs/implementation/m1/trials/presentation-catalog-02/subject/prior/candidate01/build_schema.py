"""Build the proposed metadata-only catalogue from exact selected owner types."""
import copy
import hashlib
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
ARCH = Path('/Users/sb/code/opensip-ai/opensip_arch')
COMMON = 'urn:opensip:product-v1:workflows:evaluator3:common:3'
SOURCES = {
 'common': 'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json',
 'policy': 'docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json',
 'repair': 'docs/coop/design-corrections/workflows/schemas/evaluator3/repair.schema.json',
 'invocation': 'docs/coop/design-corrections/workflows/schemas/evaluator3/invocation-record.schema.json',
 'canonical': 'docs/coop/design-corrections/foundation/canonical.py',
 'security-owner': 'docs/v2/contracts/product-v1/security-and-lifecycle.md',
 'workflow-owner': 'docs/v2/contracts/product-v1/workflows-and-surfaces.md',
 'native-owner': 'docs/v2/contracts/product-v1/native-evidence.md',
 'dispositions': 'docs/v2/architecture/prototype-report-inventory.md',
}

def obj(properties):
 return {'type':'object','additionalProperties':False,'required':list(properties),'properties':properties}
def arr(items, cap, order):
 return {'type':'array','maxItems':cap,'items':items,'x-opensip-order':order}
def build(docs):
 # Exact owner-derived types; no closureId inside its own closure tree listing.
 recipe = copy.deepcopy(docs['repair']['$defs']['RecipeRef'])
 recipe['required'].remove('closureId'); del recipe['properties']['closureId']
 rule = copy.deepcopy(docs['policy']['$defs']['Rule']['properties']['ruleProgramRef'])
 # Retain the original Rule reference URNs; the input closure owns them.
 ident = {'$ref':COMMON+'#/$defs/CanonicalIdentifier'}
 name = {'type':'string','minLength':1,'maxLength':256}
 desc = {'type':'string','minLength':1,'maxLength':8192}
 tags = arr(ident,32,'utf8');tags['uniqueItems']=True
 display = {'name':name,'description':desc,'tags':tags}
 capability = obj({'capabilityId':ident,**display})
 rule_record = obj({'ruleProgramRef':rule,**display})
 params = docs['invocation']['$defs']['RepairPreviewParams']
 selector = obj({'kind':{'const':'finding-fingerprints'},'minimumTargets':{'const':params['properties']['targets']['minItems']},'maximumTargets':{'const':params['properties']['targets']['maxItems']}})
 parameter_doc = obj({'evidenceSource':{'type':'string','minLength':1,'maxLength':4096},'targets':{'type':'string','minLength':1,'maxLength':4096}})
 recipe_record = obj({'recipeKey':recipe,**display,'selector':selector,'parameterDescriptions':parameter_doc})
 schema = {'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:opensip:product-v1:workflows:presentation-catalog:1','title':'Metadata-only presentation catalogue inside an admitted contribution closure',**obj({'schemaFamily':{'const':'opensip.presentation-catalog'},'schemaMajor':{'const':1},'capabilities':arr({'$ref':'#/$defs/CapabilityDescriptionV1'},4096,'canonical-set'),'rules':arr({'$ref':'#/$defs/RuleDescriptionV1'},4096,'canonical-set'),'recipes':arr({'$ref':'#/$defs/RecipeDescriptionV1'},4096,'canonical-set')})}
 schema['$defs']={'CapabilityDescriptionV1':capability,'RuleDescriptionV1':rule_record,'RecipeDescriptionV1':recipe_record}
 return schema

if __name__ == '__main__':
 docs={}; pins=[]
 for key, relative in SOURCES.items():
  p=ARCH/relative;raw=p.read_bytes();pins.append({'role':key,'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
  if relative.endswith('.json'):docs[key]=json.loads(raw)
 # Legacy common is required by the unchanged ruleProgramRef owner type.
 p=ARCH/'docs/coop/design-corrections/workflows/schemas/common.schema.json';raw=p.read_bytes();pins.append({'role':'legacy-common','path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)})
 (HERE/'input-pins.json').write_text(json.dumps({'schemaVersion':1,'files':pins},indent=2)+'\n')
 (HERE/'presentation-catalog.schema.json').write_text(json.dumps(build(docs),indent=2,ensure_ascii=False)+'\n')
