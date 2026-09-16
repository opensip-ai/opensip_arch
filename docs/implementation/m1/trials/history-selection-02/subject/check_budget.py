"""Exact history disclosure and unavailable-slot bounds under the pinned codec."""
import copy,json,types
from pathlib import Path
HERE=Path(__file__).resolve().parent
T=types.ModuleType('history_budget_fixture');T.__file__=str(HERE/'check.py');exec(compile((HERE/'check.py').read_bytes(),T.__file__,'exec'),T.__dict__)
C=types.ModuleType('history_canonical');exec(compile(T.paths['canonical'].read_bytes(),'pinned-canonical-owner','exec'),C.__dict__)
max_text=json.loads(T.paths['common'].read_bytes())['$defs']['BoundedText']['maxLength']
# U+0000 occupies six bytes in canonical JSON, greater than any raw UTF-8
# scalar (<=4 bytes); the selected BoundedText permits it as escaped JSON data.
text='\0'*max_text
ids=[T.rid(i) for i in range(4)]
selections=[T.module.plan_selection(T.module.admit_request(ids,'html'),current) for current in [None,T.rid(99),*ids]]
selection=max(selections,key=lambda v:len(C.canonical(v)))
choices=[]
for availability,code in [('expired','evidence.expired'),('purged','evidence.purged'),('corrupt','evidence.corrupt'),('unavailable','QUERY.VIEW_UNKNOWN')]:
 row={'state':'unavailable','runId':ids[0],'availability':availability,'detail':{'code':code,'remedy':text,'subject':text}}
 T.validate_history(row);choices.append(row)
worst=max(choices,key=lambda v:len(C.canonical(v)))
rows=[{**copy.deepcopy(worst),'runId':rid} for rid in ids]
minimal=[{'state':'unavailable','runId':rid,'availability':'unavailable'} for rid in ids]
panel={'selection':selection,'runs':rows,'provenance':copy.deepcopy(T.panel['properties']['provenance']['const'])}
T.module.validate_panel(panel,selection['currentRunId'],lambda value:T.validator(T.panel,registry=T.registry).validate(value))
# The optional detail cannot turn into a purge inventory: its code is joined to
# the closed four read-availability states, so evidence.pinned is inadmissible.
bad=copy.deepcopy(worst);bad['detail']['code']='evidence.pinned';bad['detail']['purgeDisclosure']={}
try:T.validate_history(bad)
except T.ValidationError:pass
else:raise AssertionError('purge disclosure escaped explicit read-detail subset')
result={'standing':'Exact root02 reference encoding bound; not full report capacity or browser qualification',
 'boundedTextScalars':max_text,'worstEncodedBytesPerScalar':6,'selectionMaxBytes':len(C.canonical(selection)),
 'fourMinimalUnavailableRowsBytes':len(C.canonical(minimal)),'worstUnavailableSlotIncludingDetailBytes':len(C.canonical(worst)),
 'fourMaximalUnavailableRowsIncludingDetailBytes':len(C.canonical(rows)),'wholeExplicitUnavailablePanelMaxBytes':len(C.canonical(panel)),
 'derivation':'Four fixed-length distinct RunIds; maximum nonmatching current RunId; longest source token in each slot; constant provenance; max closed availability/detail code spelling; optional subject included; each of two BoundedText fields has 1024 six-byte escaped scalars. No arbitrary/purge detail payload allowed.',
 'integrationDuty':'Reserve selectionMaxBytes plus its enclosing member syntax as mandatory disclosure before optional panels. Present history findings and complete panels use actual remaining whole-document budget; never truncate requested IDs or drop individual unavailable slots to fit. If no panel fits, disclose panel omission while retaining the exact selection. L02 global delivery capacity remains unresolved.'}
(HERE/'budget-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
