"""Read-only S-B proposed-passage/authority and arithmetic specimen audit; no consumer execution."""
import argparse,hashlib,json,pathlib
def main():
 p=argparse.ArgumentParser();p.add_argument('--architecture',type=pathlib.Path,required=True);p.add_argument('--product',type=pathlib.Path,required=True);a=p.parse_args();local=pathlib.Path(__file__).parent;authority=json.loads((local/'authority.json').read_bytes())
 for group,root in [('architecture',a.architecture),('product',a.product)]:
  for row in authority[group]:
   raw=(root/row['path']).read_bytes();assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],row['path']
 draft=local.parent/'successor.json'
 if not draft.exists():draft=local.parent/'successor-draft.json'
 record=json.loads(draft.read_bytes());assert record['passageOverrides']==[] and len(record['passageSupersessions'])==2
 lock=json.loads((a.product/'design-lock.json').read_bytes());bound={b['record']['path']:b['record'] for b in lock['contractSuccessors']};rows=record['passageSupersessions'];assert [r['selector']['line'] for r in rows]==[3534,4276];assert [r['supersedes'] for r in rows]==authority['supersededPassages']
 for row in rows:
  ref=row['supersedes'];assert bound[ref['record']['path']]==ref['record'];previous=json.loads((a.architecture/ref['record']['path']).read_bytes());old=[r for r in previous['passageOverrides'] if r['parent']==ref['parent'] and r['selector']==ref['selector']];assert len(old)==1 and row['before']==old[0]['after'];assert row['after'].startswith(row['before']+'\n')
  for b in lock['contractSuccessors']:
   existing=json.loads((a.architecture/b['record']['path']).read_bytes());assert not any(r['parent']==row['parent'] and r['selector']==row['selector'] for r in existing.get('passageSupersessions',[]))
 schema=json.loads((a.architecture/'docs/implementation/fallow-expansion/capacity-r2/schemas/identity-schemas.v3.json').read_bytes());assert schema['$defs']['source-inventory']['maxItems']==100000;assert schema['$defs']['subject-scope']['properties']['subjects']['maxItems']==100000
 canonical=(a.product/'crates/identity/src/canonical.rs').read_text();assert 'pub const MAX_BYTES: usize = 4 * 1024 * 1024;' in canonical
 protocol=json.loads((a.architecture/'docs/coop/artifacts/rust-provider-protocol.v2.json').read_bytes());assert protocol['limits']['maxSnapshotTotalFileBytes']==8589934592
 native=(a.architecture/'docs/v2/contracts/product-v1/native-evidence.md').read_text();assert '`maxDependencySourcePackages 4096`, `maxDependencySourceEntries 1000000`' in native and '`maxDependencySourceTotalBytes 8589934592`' in native
 c=(a.architecture/'docs/implementation/m3/snapshot-plan-c/PROPOSAL-r8.md').read_text();h=(a.architecture/'docs/implementation/m3/fact-admission-h/PROPOSAL-r3.md').read_text();j=(a.architecture/'docs/implementation/m3/host-pipeline-j/PROPOSAL-r6.md').read_text();assert 'candidate sources (archives and trees alike): at most 16,384' in c and 'candidate logical files: at most 4,000,000' in c and 'candidate content: at most 32 GiB' in c;assert 'subject-scope.subjects:count>100000' in h;assert 'J1 adopts S-B: request-rejected 2' in j
 projection=json.loads((local/'projection.json').read_bytes());fields=projection['fields'];assert len(fields)==11 and len({r['field'] for r in fields})==11;expected=[100000,4194304,8589934592,4096,1000000,8589934592,16384,4000000,34359738368,100000,4194304];assert [r['limit'] for r in fields]==expected
 samples=[]
 for row in fields:
  for observed in [row['limit']-1,row['limit'],row['limit']+1]:samples.append({'field':row['field'],'observed':observed,'limit':row['limit'],'crossed':observed>row['limit'],'subjectIfCrossed':f"{row['field']}:{observed}>{row['limit']}" if observed>row['limit'] else None})
 assert len(samples)==33 and sum(r['crossed'] for r in samples)==11
 after=rows[1]['after'];extension=after[len(rows[1]['before']):]
 for row in fields:assert row['field'] in extension and str(row['limit']) in extension
 for phrase in ['Per-archive decoder D1-D4 crossings remain archive-profile breaches','sources, then files, then content','S-B adds no priority across independent producer boundaries','an existing Plan','null, boolean, string, object','same final set','Inactive candidates and rejected archives','before Plan minting','after provider execution','add ignorePaths or select a narrower project root']:
  assert phrase in extension,phrase
 assert '11264' in rows[1]['before'] and 'limit1024 (FX-CAP-1)' in rows[1]['before'];assert not projection['consumerRan'] and not projection['productQualification'];assert not pathlib.Path('/Users/sb/Library/Application Support/OpenSIP').exists()
 print(json.dumps({'passed':True,'standing':'S-B design text/pin and arithmetic specimens only; no consumer/producer/decoder/emitter execution','authorityPins':sum(len(authority[k]) for k in ['architecture','product']),'supersededPassages':authority['supersededPassages'],'effectiveCapacityTextPreservedExactly':True,'numericQuantities':len(fields),'arithmeticSampleCount':len(samples),'samples':samples,'schemaBoundsUnchanged':True,'consumerRan':False,'producerRan':False,'providerRan':False,'installationAbsent':True,'productQualification':False},indent=2))
if __name__=='__main__':main()
