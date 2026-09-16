"""Compare the native helper with independently captured compiler observations."""
from pathlib import Path
import argparse
import importlib.util
import json

parser=argparse.ArgumentParser()
parser.add_argument('--source',type=Path,required=True)
parser.add_argument('--out',type=Path,required=True)
parser.add_argument('--expect-mismatches',type=int,required=True)
args=parser.parse_args()
base=Path(__file__).parent
observations=json.loads((base/'compiler-observations.json').read_text())
spec=importlib.util.spec_from_file_location('root_a5_native',args.source/'docs/coop/design-corrections/native/native_evidence_model.v2.py')
model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)
rows=[]
for case in observations['rows']:
    listing=['main.ts']+(['helper.js'] if case['jsFilePresent'] else [])
    cfg={'compilerOptions':case['options']}
    got=model.typescript_mode(listing,'',None,cfg if case['origin']=='tsconfig' else None,cfg if case['origin']=='jsconfig' else None,[],False)
    expected=dict(allowJs=case['effectiveAllowJs'],checkJs=case['checkJs'],jsAdmittedToProgram=case['effectiveAllowJs'] and bool(case['jsRootFiles']),jsDiagnosticsEnabled=case['checkJs'],resolutionCompletenessImplied=False,languageMode='js-allowjs' if case['effectiveAllowJs'] else 'ts-tsconfig')
    actual={key:got[key] for key in expected}
    rows.append(dict(origin=case['origin'],options=case['options'],jsFilePresent=case['jsFilePresent'],expected=expected,actual=actual,agrees=expected==actual,compilerOptionDiagnosticCodes=[d['code'] for d in case['optionDiagnostics']]))
mismatches=sum(not r['agrees'] for r in rows)
args.out.write_text(json.dumps(dict(standing='32 bounded direct-option cases compared with official compiler observations. Existing reference helper consumes trusted observations; this is not full config-inheritance/provider/Run/host qualification.',source=str(args.source),cases=len(rows),mismatches=mismatches,rows=rows),indent=2)+'\n')
print(json.dumps(dict(cases=len(rows),mismatches=mismatches,expectedMismatches=args.expect_mismatches)))
assert len(rows)==32 and mismatches==args.expect_mismatches
