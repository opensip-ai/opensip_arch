import pathlib,json,hashlib,datetime,collections,subprocess
root=pathlib.Path('/Users/sb/code/opensip-ai/opensip_arch')
tmp=pathlib.Path('/tmp/opensip-design-corrections/grok-subject-assessment.v1')
reviews=root/'docs/coop/design-corrections/reviews'
out=reviews/'grok-subject-assessment.v1'
out.mkdir(exist_ok=False)
session=pathlib.Path('/Users/sb/.grok/sessions/%2Fprivate%2Ftmp%2Fopensip-design-corrections%2Fgrok-subject-assessment.v1/0d7f2cda-0e54-45e1-9a68-a8782587a8a0')
raw=json.loads((tmp/'response.json').read_text())
assert raw['stopReason']=='end_turn' and raw['sessionId']=='0d7f2cda-0e54-45e1-9a68-a8782587a8a0'
for n in ['prompt.txt','process.json','response.public.json','assessment.md','stderr.log','source-integrity.json','retain-and-assess.py']:
 (out/n).write_bytes((tmp/n).read_bytes())
public=[]; names=collections.Counter(); models=set()
for line in (session/'chat_history.jsonl').read_text().splitlines():
 j=json.loads(line)
 if j['type']=='assistant':
  public.append({k:j[k] for k in ['type','content','tool_calls','model_id'] if k in j})
  if j.get('model_id'):models.add(j['model_id'])
  for t in j.get('tool_calls',[]):names[t['name']]+=1
 elif j['type']=='tool_result':public.append({k:j[k] for k in ['type','tool_call_id','content'] if k in j})
(out/'public-tools-and-responses.jsonl').write_text(''.join(json.dumps(j,ensure_ascii=False)+'\n' for j in public))
record={
 'standing':'Completed actual Grok bounded COAUTHOR assessment. Root accepts selected design directions, not the complete proposal. No source assent, blind review, Claude agreement or implementation readiness.',
 'actualSession':raw['sessionId'],'actualModels':sorted(models),'numTurns':raw['num_turns'],'publicToolCalls':dict(names),'publicBlocks':len(public),
 'userAuthorization':'User explicitly offered Grok as temporary replacement while Claude unavailable. Architecture/design/reference scope continues; no product implementation, commit or push.',
 'fullReadPublicAssessment':True,'testsExecuted':'No evaluator or schema tests. Grok recomputed manifest SHA; root checked all 12212 declared frozen21 files with no mismatch.',
 'acceptedDirections':[
  'Prefer universe-qualified evaluation subjects; retain separate per-universe coverage obligations and keep volatile universe H out of stable logical fingerprints.',
  'Retain typed native subject attribution with snapshot, universe and selected provider binding, rather than parse opaque subject strings as paths.',
  'Preserve exported-subject functionality. Unknown export membership requires disclosure and indeterminate gating, including zero known exported subjects.',
  'Separate invalid metadata, unavailable evidence and loss of promised retained bytes. Preserve operational precedence.',
  'This is language-independent infrastructure; TypeScript, Rust and syntax-provider cases all matter.'
 ],
 'requiredRefinements':[
  {'id':'GR1','issue':'Two universe-qualified findings may share one logical fingerprint; baseline entries explicitly reject duplicate fingerprints. The proposal identifies waiver spanning but supplies no finding/baseline aggregation law.','required':'Specify exact aggregation and evidence/parameter/conflict handling; preserve per-universe deficiencies and baseline correspondence. Reference workflows/schemas/baseline-artifact.schema.json#/$defs/BaselineDescriptor/properties/entries.'},
  {'id':'GR2','issue':'Whole-rule indeterminate/disclosure for zero selected subjects is asserted without a typed retained carrier. Frozen proof-bundle only retains per-subject predicateProofs plus aggregate verdict.','required':'Define schema-bound enumeration result/deficiency with exact selection and input references; recompute it during complete replay. Known-true findings still evaluate, and a separate indeterminate enumeration must not erase fail dominance.'},
  {'id':'GR3','issue':'U(R) still ranges over retained universes and inventories without a complete obligation mapping from selected Plan contexts/cells. Scope-to-row subset checks cannot prove the inventory includes symbols never present in scopes or facts.','required':'Define expected universe/inventory population, producer selection and completeness/unavailable states from Plan requirements. Distinguish omitted required data from legitimate unavailable evidence; never infer complete empty population merely from absence of rows.'},
  {'id':'GR4','issue':'Inventory.language is equated with universe engine language and then used in finding correspondence. Syntax engine language is syntax; TypeScript engine can analyze JavaScript.','required':'Define subject/source language attribution separately from provider domain. Existing domainSets languageVersionBinding.bodyLanguageLaw explicitly distinguishes engine and body language. Cover grammar-only data/inventory subjects as well as compiler symbols.'},
  {'id':'GR5','issue':'New evaluation-subject H descriptor has no explicit retained or derived closure traversal, registry row or ProofInputRef binding in the proposal. Inventory uniqueness by triple does not select one provider when several are selected.','required':'Specify acyclic graph traversal and exact derivation/retention joins, provider selection and mismatch refusal, including same universe/native id supplied by two providers.'},
  {'id':'GR6','issue':'Empty signatureTokens is permitted for every row, without preserving the existing anonymous/ambiguous-symbol correspondence refusal or tying token projection to its selected detector.','required':'Define signature-less file/package identity explicitly; retain the existing symbol ambiguity limits and bind the projection producer. Do not silently widen anonymous symbol matching.'},
  {'id':'GR7','issue':'The proposal states all bare-string union is unsound. A union with retained per-universe quantification/coverage could be designed soundly; its example establishes failure of a naive union only.','required':'Record qualified identity as the chosen design with explicit tradeoffs, not a theorem forced by tuple uniqueness or an inadequately specified union comparator.'},
  {'id':'GR8','issue':'Identifier majors, error routing, schema/Ref annotations and maximum sizes remain choices, not an implementable normative patch. Missing and corrupt bytes are grouped too broadly without checking existing diagnostic laws.','required':'Provide exact schema and registry changes, limits, domain majors and downstream identity consequences, preserving frozen history; map faults to published routes or explicitly add reviewed routes.'}
 ],
 'nextWork':'Give Grok these bounded root refinements, settle concrete subject/enumeration schema proposal, then integrate with the remaining G3-G9/E1 evaluator corrections. Apply only reviewed coherent successor design/reference bytes. Actual Claude final independent acceptance, NEW blind consumer B, and application/readiness reconciliation remain pending.',
 'claudeStatus':'Weekly quota observed earlier; September 11 2026 17:00 America/Los_Angeles reset. No new Claude retry in this Grok turn.',
 'acceptedSourceEdited':False,'implementationReady':False,
 'privacy':'Retained only public final text, tool calls/results, prompt and process metadata. CLI JSON includes a non-public field; it was excluded from the durable public response. No private reasoning retained in this evidence bundle.',
 'recordedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()
}
(out/'root-assessment.json').write_text(json.dumps(record,indent=2)+'\n')
custody=[]
for q in sorted(out.iterdir()):
 if q.is_file():
  b=q.read_bytes();custody.append({'path':q.name,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)})
(out/'custody.json').write_text(json.dumps({'standing':'Public evidence only; exclusions described in root-assessment.json','files':custody},indent=2)+'\n')
print(json.dumps({'retained':str(out),'files':len(custody),'models':sorted(models),'toolCalls':dict(names)},indent=2))
