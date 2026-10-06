"""Read-only SD-2 design projection controls; no manifest/session/codec admission."""
import argparse,hashlib,json,pathlib

def pin(root,row):
 raw=(root/row['path']).read_bytes()
 assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
def same(a,b):
 if type(a) is not type(b): return False
 if isinstance(a,dict): return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
 if isinstance(a,list): return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def fate(row):
 selected=row['selected']
 allowed=[{'role':'analyzer','roleSubprotocol':'typescript-semantic','subprotocolVersion':2},{'role':'analyzer','roleSubprotocol':'rust-semantic','subprotocolVersion':3}]
 if not any(same(selected,t) for t in allowed):return 'SELECTION'
 manifest=row['manifest']
 if not same(manifest['role'],selected['role']) or not same(manifest['compatibility']['providerProtocol'],selected['subprotocolVersion']):return 'MANIFEST'
 if not any(same(c.get('roleSubprotocol'),selected['roleSubprotocol']) and same(c.get('subprotocolVersion'),selected['subprotocolVersion']) for c in manifest['capabilities']):return 'CAPABILITY'
 if not same(row['offer'],[selected]):return 'OFFER'
 if not same(row['select'],selected):return 'SELECT'
 return 'MATCH'
def main():
 p=argparse.ArgumentParser();p.add_argument('--architecture',type=pathlib.Path,required=True);p.add_argument('--product',type=pathlib.Path,required=True);args=p.parse_args()
 local=pathlib.Path(__file__).parent; authority=json.loads((local/'authority.json').read_text())
 for row in authority['architecture']:pin(args.architecture,row)
 for row in authority['product']:pin(args.product,row)
 cms=json.loads((args.architecture/'docs/coop/completion/manifest-schema.completed.v1.json').read_text())
 assert cms['properties']['role']=={'const':'analyzer'}
 assert cms['properties']['compatibility']['properties']['providerProtocol']=={'type':'integer','minimum':1,'maximum':9223372036854775807}
 cap=cms['$defs']['capability'];assert {(r['properties']['roleSubprotocol']['const'],r['properties']['subprotocolVersion']['const']) for r in cap['oneOf']}=={('typescript',1)}
 control=json.loads((args.product/'schemas/sources/control-v3.schema.json').read_text())
 properties=[]
 def walk(value):
  if isinstance(value,dict):
   if 'subprotocolVersion' in value.get('properties',{}):properties.append(value['properties'])
   for v in value.values():walk(v)
  elif isinstance(value,list):
   for v in value:walk(v)
 walk(control);assert properties
 for row in properties:assert row['subprotocolVersion']['type']=='integer' and row['subprotocolVersion']['minimum']==1 and row['roleSubprotocol']['type']=='string'
 dr103=json.loads((args.architecture/'docs/coop/artifacts/component-manifest-schemas.v11.json').read_text())
 fields={row['name']:row for row in dr103['manifestSchema']['fields']}
 assert 'host-owned' in fields['role']['semantics'] and 'opaque tokens' in fields['capabilities']['semantics']
 assert 'EMPTY array is a VALID declaration' in fields['capabilities']['semantics']
 md=(args.architecture/'docs/implementation/m3/supervisor-d/PROPOSAL-r5.md').read_text();assert 'exactly one tuple' in md and 'compatibility.providerProtocol' in md and 'session-spec-inconsistent' in md
 ml=(args.architecture/'docs/implementation/m3/provider-protocol-l/PROPOSAL-r5.md').read_text();assert 'X5 stays open until that record is accepted' in ml
 ne=(args.architecture/'docs/v2/contracts/product-v1/native-evidence.md').read_text();assert '`rust-semantic` protocol major **3**; `typescript-semantic` protocol major **2**.' in ne
 cc=(args.architecture/'docs/coop/completion/control-completion.contract.v5.md').read_text();assert 'roleSubprotocol typescript and version1' in cc and 'synthetic, non-shipping' in cc
 cases=json.loads((local/'cases.json').read_text())['cases'];assert len(cases)==21;assert len({r['case'] for r in cases})==len(cases)
 rows=[]
 for row in cases:
  observed=fate(row['input']);assert observed==row['expected'],(row['case'],observed,row['expected']);rows.append({'case':row['case'],'fate':observed})
 assert not pathlib.Path('/Users/sb/Library/Application Support/OpenSIP').exists()
 print(json.dumps({'passed':True,'standing':'SD-2 DESIGN PROJECTION CONTROLS ONLY','caseCount':len(rows),'positiveCount':sum(r['fate']=='MATCH' for r in rows),'cases':rows,'authorityPinsChecked':len(authority['architecture'])+len(authority['product']),'manifestAdmitted':False,'sessionAdmitted':False,'codecRan':False,'providerLaunched':False,'installationAbsent':True,'productQualification':False},indent=2))
if __name__=='__main__':main()
