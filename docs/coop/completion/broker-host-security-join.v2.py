"""DRAFT broker request join to the receipt's required security enforcing boundary.
Synthetic host-owned current-grant observations, never product GRANT creation.
"""
import copy,hashlib,importlib.util,json
from pathlib import Path
P=Path(__file__).resolve().parent
RECEIPT=json.loads((P/'broker-security-inputs.v2.json').read_text())
if RECEIPT.get('standing') != 'EXACT-FROZEN-SECURITY-INPUTS-CONDITIONAL':raise RuntimeError('BROKER-SECURITY-INTEGRATION-PENDING')
for pin in RECEIPT['sources']:
 path=P.parents[2]/pin['path']
 if hashlib.sha256(path.read_bytes()).hexdigest()!=pin['sha256']:raise RuntimeError('BROKER-SECURITY-DEPENDENCY-CUSTODY')
s=importlib.util.spec_from_file_location('courier_security',P/RECEIPT['securityLibrary']);SEC=importlib.util.module_from_spec(s);s.loader.exec_module(SEC)
def context(body,sealed,byte_cap):
 binding={'installGenerationId':'fixture-generation','manifestDigest':'b'*64,'platform':'macos-arm64','stableId':'11111111-1111-4111-8111-111111111111'}
 broker='gj:'+'d'*64+':1:1';under='gj:'+'d'*64+':1:2';effect=body['effectClass']
 if effect=='HE-2':target={'snapshotDigest':sealed['snapshotDigest'],'memberPath':'src/member.ts'};scope={'snapshotDigest':sealed['snapshotDigest'],'pathPrefixes':['src']}
 else:target={'stateClass':'SC-OPS','byteCap':byte_cap};scope={'stateClass':'SC-OPS'}
 entry={'operationRef':body['operationRef'],'effectClass':effect,'brokerLocator':broker,'underlyingLocator':under,'grantGeneration':1,'seq':2,'binding':binding,'target':target}
 grants={broker:{'status':'GRANT','token':'PT-HOST-EFFECT-BROKERED','binding':copy.deepcopy(binding),'scope':copy.deepcopy(scope)},under:{'status':'GRANT','token':SEC.EFFECT_UNDERLYING_TOKEN[effect],'binding':copy.deepcopy(binding),'scope':copy.deepcopy(scope)}}
 return {'connectionMap':{body['authorizationRef']:entry},'currentBinding':copy.deepcopy(binding),'journalState':grants,'snapshotMembers':list(sealed['members'])}
def evaluate(body,ctx):
 reason=SEC.verify_effect_request(body,ctx)
 if reason is None:return None
 # Existing PR identities; no domain label becomes a new wire decision class.
 decision='PR-5' if reason=='RF-6:AUTHORIZATION.GRANT_NOT_CURRENT' and any(g.get('status') in ['REVOKED','CLOSED'] for g in ctx.get('journalState',{}).values()) else 'PR-4'
 return {'family':'RF-6','decisionClass':decision,'domainReason':reason}
