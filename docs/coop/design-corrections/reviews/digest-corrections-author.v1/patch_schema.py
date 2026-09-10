"""Author patch: close the auxiliary-digest law in identity-schemas.v2.json.
Adds the machine-readable x-opensip-digest annotation to every 64-hex field,
the digest-domain registry, and the missing closed records."""
import json,sys
from pathlib import Path
P=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/foundation/identity-schemas.v2.json')
d=json.loads(P.read_text())
defs=d['$defs']
HEX='^[0-9a-f]{64}(?![\\s\\S])'
def hexf(ann,**extra):
    node={'type':'string','pattern':HEX,'x-opensip-digest':ann}
    node.update(extra);return node
POLICY_DOC='workflows/schemas/policy-document.schema.json'
IMPORTED='workflows/schemas/imported-evidence.schema.json'
COMMON='workflows/schemas/common.schema.json'
NATIVE='native/native-evidence.schemas.v2.json'

raw=lambda artifact:{'representation':'raw-artifact','artifact':artifact}
local=lambda sel:{'representation':'canonical-record','record':{'bundle':'identity','selector':'#/$defs/'+sel}}
foreign=lambda doc,sel:{'representation':'canonical-record','record':{'document':doc,'selector':sel}}
registered=lambda field:{'representation':'canonical-record','record':{'registeredBy':field}}
hid=lambda ds:{'representation':'h-identity','domainSet':ds}
CAPID={'representation':'capability-manifest-id'}
BYDOMAIN={'representation':'by-domain','registry':'x-opensip-digest-domains'}

# ---------------------------------------------------------------- new closed records
defs['source-inventory']={
 'type':'array','maxItems':100000,'uniqueItems':True,
 'items':{'$ref':'#/$defs/Blob'},'x-opensip-order':'path',
 'description':'The snapshot source inventory as a registered record in its own right, so that '
   'vcs-observation.sourceInventoryDigest names a record rather than an unnamed canonical fragment.'}
defs['program-predicate']={
 'type':'object','additionalProperties':False,
 'required':['schemaVersion','ruleProgramDigest','ruleId','predicateId','operation','nodeDigest'],
 'description':'The closed record digested by predicate-witness.programPredicateDigest. It addresses ONE '
   'predicate node of the admitted RuleProgramV1; it introduces no second policy language. predicateId is the '
   'node address: the rule root is "p", the i-th operand of an and/or node at address a is a+"."+i (zero-based, '
   'shortest decimal), and the operand of a not node at address a is a+".0".',
 'properties':{
   'schemaVersion':{'const':2},
   'ruleProgramDigest':hexf(foreign(POLICY_DOC,'#/$defs/RuleProgramV1'),
       description='equal to the proof bundle ruleProgramDigest this witness belongs to'),
   'ruleId':{'$ref':'#/$defs/Text'},
   'predicateId':{'$ref':'#/$defs/Text'},
   'operation':{'type':'string','enum':['exists','none','count-at-most','all-covered','and','or','not']},
   'nodeDigest':hexf(foreign(POLICY_DOC,'#/$defs/Predicate'),
       description='raw SHA-256 of the canonical bytes of the exact predicate node the rule program carries at '
                   'rules[ruleId].emitWhen addressed by predicateId; its op equals operation')}}
defs['finding-parameters']={
 'type':'object','additionalProperties':False,
 'required':['schemaVersion','messageCode','parameters'],
 'description':'The closed record digested by finding.parameterDigest. parameters is an object map so that '
   'parameter names are unique and ordered by the canonical encoder itself, with no ordering annotation to elect.',
 'properties':{
   'schemaVersion':{'const':2},
   'messageCode':{'$ref':'#/$defs/Text'},
   'parameters':{'type':'object','maxProperties':64,
     'propertyNames':{'type':'string','minLength':1,'maxLength':128,'pattern':'^[a-z][a-zA-Z0-9]*(?![\\s\\S])'},
     'additionalProperties':{'oneOf':[
        {'type':'string','minLength':0,'maxLength':4096},
        {'type':'integer','minimum':-9223372036854775808,'maximum':18446744073709551615},
        {'type':'boolean'}]}}}}
defs['stage-spec']={
 'type':'object','additionalProperties':False,
 'required':['schemaVersion','planId','producerClosure','operation','parameters','outputDomains','outputSchemaDigest'],
 'description':'The closed record digested by stageSpecDigest. execution-plan.stages[].stageSpecDigest and '
   'cache-key.stageSpecDigest are the SAME field name because they are the same digest of the same record under '
   'the same recipe; there are not two recipes for one spelling.',
 'properties':{
   'schemaVersion':{'const':2},
   'planId':{'type':'string','pattern':'^plan2:[0-9a-f]{64}(?![\\s\\S])'},
   'producerClosure':{'type':'string','pattern':'^closure2:[0-9a-f]{64}(?![\\s\\S])'},
   'operation':{'$ref':'#/$defs/Text'},
   'parameters':{'type':'array','uniqueItems':True,'maxItems':128,
     'items':{'type':'object','additionalProperties':False,'required':['schemaDigest','payloadDigest'],
       'properties':{'schemaDigest':hexf(raw('the exact complete registered parameter schema document bytes')),
                     'payloadDigest':hexf(registered('schemaDigest'))}},
     'x-opensip-order':'canonical-set',
     'description':'every row must also be a row of the Plan analysis-spec parameters: a stage takes no hidden input'},
   'outputDomains':{'type':'array','maxItems':128,'uniqueItems':True,'items':{'$ref':'#/$defs/Text'},
     'x-opensip-order':'canonical-set'},
   'outputSchemaDigest':hexf(raw('the exact complete registered stage output schema document bytes'))}}
defs['commit-inventory']={
 'type':'object','additionalProperties':False,
 'required':['schemaVersion','runId','objects','blobs'],
 'description':'The closed record digested by commit-receipt.inventoryDigest: the exact set of typed object '
   'identities and retained raw blob digests the commit published for this Run.',
 'properties':{
   'schemaVersion':{'const':2},
   'runId':{'type':'string','pattern':'^run2:[0-9a-f]{64}(?![\\s\\S])'},
   'objects':{'type':'array','maxItems':1000000,'uniqueItems':True,'items':{'$ref':'#/$defs/Text'},
     'x-opensip-order':'canonical-set'},
   'blobs':{'type':'array','maxItems':1000000,'uniqueItems':True,'items':{'$ref':'#/$defs/Hash'},
     'x-opensip-order':'canonical-set'}}}
defs['owner-source-set']={
 'type':'array','maxItems':1024,'uniqueItems':True,
 'description':'The closed record digested by semantic-grant.principals[].ownerSourceDigest: the security '
   'contract RepoExecutionGrantV2 owner projection, strictly ascending and unique by ownerKey UTF-8 bytes. '
   'The ownerKey order is not yet an x-opensip-order vocabulary value; the closure checker enforces it.',
 'items':{'type':'object','additionalProperties':False,
   'required':['ownerKey','source','ownerFileManifestSha256'],
   'properties':{'ownerKey':{'$ref':'#/$defs/Text'},'source':{'$ref':'#/$defs/Text'},
                 'ownerFileManifestSha256':hexf(raw('the exact retained owner file-manifest bytes'))}},
 'x-opensip-order':'sequence'}

# ---------------------------------------------------------------- annotate every existing 64-hex field
def setann(node,ann):
    node['x-opensip-digest']=ann
    return node
S=defs
setann(S['Blob']['properties']['sha256'],raw('the exact retained file bytes named by path; bytes is their exact length'))
for name in ['Ref','ProofInputRef','FindingEvidenceRef']:
    setann(S[name]['properties']['digest'],BYDOMAIN)
ap=S['analysis-spec']['properties']['parameters']['items']['properties']
ap['schemaDigest']=hexf(raw('the exact complete registered parameter schema document bytes'))
ap['payloadDigest']=hexf(registered('schemaDigest'))
setann(S['cache-key']['properties']['outputSchemaDigest'],raw('the exact complete registered stage output schema document bytes; equal to stage-spec.outputSchemaDigest'))
setann(S['cache-key']['properties']['stageSpecDigest'],local('stage-spec'))
setann(S['closure']['properties']['manifestDigest'],raw('the admitted component manifest body bytes under the security metadata profile, excluding the signature envelope'))
setann(S['commit-receipt']['properties']['inventoryDigest'],local('commit-inventory'))
setann(S['coverage']['properties']['payloadSchemaDigest'],raw('the exact complete registered Coverage payload schema document bytes'))
setann(S['coverage']['properties']['payloadDigest'],registered('payloadSchemaDigest'))
setann(S['evaluation-seal']['properties']['policyDigest'],foreign(POLICY_DOC,'#/$defs/PolicyDocumentV1'))
st=S['execution-plan']['properties']['stages']['items']['properties']
setann(st['stageSpecDigest'],local('stage-spec'))
setann(S['fact']['properties']['anchors']['items']['properties']['blobDigest'],raw('the exact retained source blob bytes named by path in the snapshot inventory'))
setann(S['fact']['properties']['payloadSchemaDigest'],raw('the exact complete registered relation payload schema document bytes'))
setann(S['fact']['properties']['payloadDigest'],registered('payloadSchemaDigest'))
for f in ['sourceUniverse','targetUniverse']:
    setann(S['fact']['properties'][f],hid('native-semantic-universe'))
    setann(S['subject-scope']['properties'][f],hid('native-semantic-universe'))
setann(S['finding']['properties']['parameterDigest'],local('finding-parameters'))
setann(S['import']['properties']['buildDigest'],foreign(IMPORTED,'#/$defs/BuildIdentityV1'))
setann(S['import']['properties']['observationDigest'],foreign(IMPORTED,'#/$defs/ImportObservationV1'))
setann(S['import']['properties']['payloadSchemaDigest'],raw('the exact complete registered import payload schema document bytes'))
setann(S['import']['properties']['payloadDigest'],registered('payloadSchemaDigest'))
setann(S['import']['properties']['scopeDigest'],local('scope-descriptor'))
setann(S['import']['properties']['sourceCorrespondenceDigest'],foreign(COMMON,'#/$defs/SourceCorrespondence'))
pl=S['plan']['properties']
setann(pl['analysisSpecDigest'],local('analysis-spec'))
pl['capabilityManifestBytesDigest']={'$ref':'#/$defs/Hash','x-opensip-digest':raw('the exact committed CVE1 capability manifest artifact bytes')}
pl['capabilityManifestId']={'$ref':'#/$defs/Hash','x-opensip-digest':CAPID}
setann(pl['nativeContextDigests']['items'],hid('native-context'))
setann(pl['policyDigest'],foreign(POLICY_DOC,'#/$defs/PolicyDocumentV1'))
setann(pl['resolvedConfigDigest'],local('semantic-configuration'))
setann(pl['scopeDigest'],local('scope-descriptor'))
setann(pl['semanticGrantDigest'],local('semantic-grant'))
setann(pl['waiverDigest'],foreign(POLICY_DOC,'#/$defs/WaiverSetV1'))
setann(S['policy-derivation']['properties']['policyDigest'],foreign(POLICY_DOC,'#/$defs/PolicyDocumentV1'))
setann(S['policy-derivation']['properties']['waiverDigest'],foreign(POLICY_DOC,'#/$defs/WaiverSetV1'))
S['predicate-witness']['properties']['programPredicateDigest']={'$ref':'#/$defs/Hash','x-opensip-digest':local('program-predicate')}
setann(S['proof-bundle']['properties']['predicateProofs']['items']['properties']['witnessDigest'],local('predicate-witness'))
setann(S['proof-bundle']['properties']['ruleProgramDigest'],foreign(POLICY_DOC,'#/$defs/RuleProgramV1'))
S['run']['properties']['capabilityManifestId']={'$ref':'#/$defs/Hash','x-opensip-digest':CAPID}
osd=S['semantic-grant']['properties']['principals']['items']['properties']['ownerSourceDigest']
osd['oneOf']=[{'type':'null'},{'$ref':'#/$defs/Hash','x-opensip-digest':local('owner-source-set')}]
setann(S['semantic-grant']['properties']['scopeDigest'],local('scope-descriptor'))
S['snapshot']['properties']['sourceInventory']={'$ref':'#/$defs/source-inventory'}
setann(S['snapshot']['properties']['resolvedConfigDigest'],local('semantic-configuration'))
setann(S['snapshot']['properties']['scopeDigest'],local('scope-descriptor'))
setann(S['snapshot']['properties']['vcsDigest'],local('vcs-observation'))
S['vcs-observation']['properties']['sourceInventoryDigest']={'$ref':'#/$defs/Hash','x-opensip-digest':local('source-inventory')}
setann(S['view']['properties']['schemaDigests']['items'],raw('the exact complete registered schema document bytes of a schema this view admitted'))

# ---------------------------------------------------------------- the digest-domain registry
identity_domains={x:{'representation':'h-identity','domain':x} for x in
  ['snapshot','closure','import','plan','subject-scope','coverage','view','execution-plan',
   'finding-fingerprint','finding','proof-bundle','semantic-evidence','evaluation-seal','run',
   'cache-key','regeneration-key','policy-derivation']}
d['x-opensip-digest-domains']={
 'standing':'Normative machine-readable registry for identity-and-evidence section 3. Every 64-hex field in '
            'this bundle carries x-opensip-digest; a field without one is not admissible.',
 'byDomain':dict(sorted({**identity_domains,
   'blob':raw('the exact retained blob bytes'),
   'schema':raw('the exact complete registered schema document bytes'),
   'capability-manifest':CAPID,
   'native-context':hid('native-context'),
   'rule-program':foreign(POLICY_DOC,'#/$defs/RuleProgramV1'),
   'policy':foreign(POLICY_DOC,'#/$defs/PolicyDocumentV1'),
   'waiver':foreign(POLICY_DOC,'#/$defs/WaiverSetV1'),
   'configuration':local('semantic-configuration'),
   'analysis-spec':local('analysis-spec'),
   'finding-parameters':local('finding-parameters'),
   'predicate-witness':local('predicate-witness'),
   'fact':{'representation':'h-identity','domain':'fact'},
   'coverage-payload':{'representation':'canonical-record','record':{'ownerRegistered':'coverage.payloadSchemaDigest'}},
   'import-payload':{'representation':'canonical-record','record':{'ownerRegistered':'import.payloadSchemaDigest'}},
   'fact-payload':{'representation':'canonical-record','record':{'ownerRegistered':'fact.payloadSchemaDigest'}},
  }.items())),
 'domainSets':{
   'native-context':{
     'native.context.typescript.v2':{'document':NATIVE,'selector':'#/$defs/TypeScriptNativeContextV2',
       'closureJoins':[{'path':['toolClosure','closureId'],'form':'closure2-identity','kind':'toolchain'},
                       {'path':['toolchain','typescriptStdlibMerkleRoot'],'form':'closure2-suffix','kind':'stdlib'}]},
     'native.context.rust.v2':{'document':NATIVE,'selector':'#/$defs/NativeContextV2',
       'closureJoins':[{'path':['toolClosure','closureId'],'form':'closure2-identity','kind':'toolchain'},
                       {'path':['toolchain','rustcDevLlvmDigest'],'form':'closure2-suffix','kind':'rust-dev-llvm'}]}},
   'native-semantic-universe':{
     'native.semantic-universe.typescript.v2':{'document':NATIVE,'selector':'#/$defs/TypeScriptUniverseV2ResolvedInputs',
       'contextField':['nativeContextId'],'contextForm':'sha256-text'}}}}
d['$defs']=dict(sorted(defs.items()))
P.write_text(json.dumps(d,indent=2)+'\n')
print('written',P)
