from pathlib import Path
import json
root=Path.cwd();dc=root/'docs/coop/design-corrections';wf=dc/'workflows';common=wf/'schemas/common.schema.json'
x=json.loads(common.read_text());defs=x['$defs'];dd=defs['DomainDetail']
assert 'evidence.pinned' not in defs['DomainDetailCode']['enum']
defs['DomainDetailCode']['enum'].append('evidence.pinned');defs['DomainDetailCode']['enum'].sort()
consequences=['named-pins-revoked','dependent-evidence-replay-unavailable','sealed-history-retained']
defs['PinnedPurgeDisclosure']={
 'type':'object','additionalProperties':False,'required':['runId','activePins','consequences'],
 'description':'Complete current pin inventory observed under the purge writer lease. Operational pinId is a host-ledger name scoped to this Run, not a content identity or authority token. Never truncate this disclosure or infer destructive consent from it.',
 'properties':{'runId':{'$ref':'#/$defs/RunId'},'activePins':{'type':'array','minItems':1,'maxItems':4096,'x-opensip-order':{'by':['pinId']},'items':{'type':'object','additionalProperties':False,'required':['pinId','kind'],'properties':{'pinId':{'type':'string','minLength':1,'maxLength':256},'kind':{'type':'string','enum':['baseline','repair-prerequisite','backup-export','other-authorized']}}}},'consequences':{'type':'array','const':consequences,'items':{'type':'string'},'x-opensip-order':'sequence'}}}
dd['properties']['purgeDisclosure']={'$ref':'#/$defs/PinnedPurgeDisclosure'}
dd['allOf']=[{'if':{'properties':{'code':{'const':'evidence.pinned'}}},'then':{'required':['subject','purgeDisclosure']},'else':{'not':{'required':['purgeDisclosure']}}}]
defs['StepTermination'].setdefault('allOf',[]).append({'if':{'required':['domainDetail'],'properties':{'domainDetail':{'required':['code'],'properties':{'code':{'const':'evidence.pinned'}}}}},'then':{'required':['errorCode'],'properties':{'class':{'const':'request-rejected'},'errorCode':{'const':'REQUEST.PRECONDITION_FAILED'}}}})
common.write_text(json.dumps(x,indent=2)+'\n')
p=dc/'public-detail-registry.v1.json';x=json.loads(p.read_text());x['records'].append({'code':'evidence.pinned','owner':'foundation','selector':'identity-and-evidence.md section 5; workflows-and-surfaces.md section 12; workflows/schemas/common.schema.json#/$defs/PinnedPurgeDisclosure'});x['records'].sort(key=lambda r:r['code']);p.write_text(json.dumps(x,indent=2)+'\n')
p=wf/'workflows_model.v1.py';s=p.read_text();anchor='# ----------------------------------------------------------------------------- D9 terminations\n';assert s.count(anchor)==1
s=s.replace(anchor,'''# ----------------------------------------------------------------------------- evidence retention projection

PINNED_PURGE_CONSEQUENCES = ['named-pins-revoked', 'dependent-evidence-replay-unavailable', 'sealed-history-retained']

def pinned_purge_refusal(request_id, run_id, active_pins):
    """Project an actual pinned store refusal using the complete host-observed pin inventory.

    Pure public projection only: no pin discovery, lease, consent, revocation or GC occurs here.
    The authenticated host supplies all current named pins after the store refuses; neither this
    record nor a caller's --revoke-pins flag establishes destructive lifecycle authorization.
    """
    disclosure = {'runId': run_id, 'activePins': sorted(active_pins, key=lambda p: p['pinId'].encode('utf-8')),
                  'consequences': list(PINNED_PURGE_CONSEQUENCES)}
    validate_import_record('workflows/schemas/common.schema.json', '#/$defs/PinnedPurgeDisclosure', disclosure)
    detail = {'code': 'evidence.pinned', 'subject': run_id,
              'remedy': 'Purge refused. Retain the evidence, release the named pins, or explicitly authorize their revocation after reviewing these consequences.',
              'purgeDisclosure': disclosure}
    term = {'class': 'request-rejected', 'errorCode': 'REQUEST.PRECONDITION_FAILED', 'domainDetail': detail}
    envelope = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 2, 'kind': 'failure',
                'requestId': request_id, 'termination': term, 'exitCode': 2, 'errors': [detail]}
    validate_import_record('workflows/schemas/command-envelope.schema.json', '', envelope)
    return envelope

'''+anchor);p.write_text(s)
p=root/'docs/v2/contracts/product-v1/workflows-and-surfaces.md';s=p.read_text();anchor='and `evidence.corrupt` retain their distinct meaning in query results.\n';assert s.count(anchor)==1
s=s.replace(anchor,anchor+'''
`evidence.pinned` is the foundation-owned refusal for a direct purge blocked by
active pins. It projects as `request-rejected`, `REQUEST.PRECONDITION_FAILED`,
exit 2, in a failure CommandEnvelope with that DomainDetail in both the
termination and `errors`. The detail's `subject` equals the requested RunId and
its required `purgeDisclosure` is the closed common-schema
`PinnedPurgeDisclosure`: the same RunId, the complete current `activePins`
inventory sorted uniquely by UTF-8 `pinId`, and the three ordered consequences
`named-pins-revoked`, `dependent-evidence-replay-unavailable`,
`sealed-history-retained`. Each operational pin name identifies a host-ledger
pin scoped to this Run and declares `baseline`, `repair-prerequisite`,
`backup-export` or `other-authorized`; names are not content hashes or permission
tokens. No pins are omitted, truncated or aggregated into an anonymous count.
Pin admission bounds each name to 256 Unicode scalar characters and each Run to
4,096 active pins, so the complete refusal stays representable; a new pin that
would exceed these bounds refuses durable admission under the existing retention
precondition rule before any protected operation starts.

The host observes that inventory under the exclusive purge lease and preserves
all named pins on refusal. A later destructive attempt requires the existing
lifecycle authorization and disclosure of its then-current complete pin set;
a flag, this disclosure or the pure projection helper confers no authority.
Revocation and purge occur in the existing protected mutation transaction; a
changed pin inventory requires renewed disclosure before destruction. Shared
bytes and sealed history retain identity §5's rules. JSON, human and agent
purge output preserve the exact named pins and consequences as the
`purge-disclosure` parity field. The reference `pinned_purge_refusal` constructs
the closed refusal from synthetic trusted ledger observations; it implements
neither ledger pin discovery nor destructive authorization.
''');p.write_text(s)
p=wf/'command-inventory.v1.json';x=json.loads(p.read_text());row=next(r for r in x['commands'] if r['name']=='purge');row['parityFields'].append('purge-disclosure');p.write_text(json.dumps(x,indent=2)+'\n')
p=wf/'workflow-cases.v1.json';x=json.loads(p.read_text());print('case keys',list(x));p.write_text(json.dumps(x,indent=2)+'\n') if False else None
print('pinned purge schema/projection/contract/current registry corrected; tests next')
