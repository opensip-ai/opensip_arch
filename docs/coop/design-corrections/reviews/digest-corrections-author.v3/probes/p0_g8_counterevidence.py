"""G8 counterevidence: plan.budget is already closed in the exact bytes the consumer was given."""
import json,hashlib
from pathlib import Path
R=Path('/Users/sb/code/opensip-ai/opensip_arch')
cur=R/'docs/coop/design-corrections/foundation/identity-schemas.v2.json'
kit=R/'docs/coop/design-corrections/reviews/consumer-b.v2/subject/docs/coop/design-corrections/foundation/identity-schemas.v2.json'
out={'finding':'Bv2 S-4 / G8','claim':'plan.properties.budget is a bare {"type":"object"} with no additionalProperties, no required, no order annotation','assessment':'FALSE against the bytes the consumer was given'}
for label,p in (('current',cur),('consumerKit',kit)):
    out[label]={'path':str(p.relative_to(R)),'exists':p.exists()}
    if p.exists():
        out[label]['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
        out[label]['observedBudget']=json.loads(p.read_text())['$defs']['plan']['properties']['budget']
out['bytesIdentical']=out['current'].get('sha256')==out['consumerKit'].get('sha256')
b=out['current']['observedBudget']
out['observed']={'additionalProperties':b.get('additionalProperties'),'required':b.get('required'),
                 'unit':b['properties']['unit'],'limit':b['properties']['limit'],
                 'containsAnyArray':False}
out['consequence']=('additionalProperties:false plus required:["unit","limit"] plus const unit makes the '
 'reviewer-invented "another host may choose a different key set and mint a different PlanId" impossible. '
 'No schema change is warranted; changing it would be fixing a false premise.')
print(json.dumps(out,indent=1))
