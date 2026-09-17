"""Reproduce the bounded reference-only malformed inventory locator correction."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,lzma,shutil,sys,tarfile,unicodedata
def require(value,message):
    if not value:raise ValueError(message)
def verify(raw,row):
    require(len(raw)==row['bytes']and hashlib.sha256(raw).hexdigest()==row['sha256'],'pin mismatch: '+row.get('path','cases'))
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();here=Path(__file__).resolve().parent
    require(sys.version_info[:3]==(3,12,13)and unicodedata.unidata_version=='15.0.0','pinned Python3.12.13/UCD15 required')
    require(sys.flags.isolated and sys.flags.dont_write_bytecode and sys.flags.int_max_str_digits==0 and sys.get_int_max_str_digits()==0,'use -I -B -X int_max_str_digits=0')
    require(not args.output.exists(),'fresh output required');args.output.mkdir(parents=True);before=args.output/'before-reference';before.mkdir()
    manifest=json.loads((here/'reference-fixture.json').read_bytes());rows={r['path']:r for r in manifest['files']};require(len(rows)==159,'reference census')
    with tarfile.open(here/'reference-fixture.tar.xz','r:xz')as tar:
        members=tar.getmembers();require(len(members)==len(rows)and {m.name for m in members}==set(rows),'archive census')
        for member in members:
            require(member.isfile() and all(p not in ('','.','..')for p in member.name.split('/'))and not member.name.startswith('/'),'nonregular/unsafe archive member')
            raw=tar.extractfile(member).read();verify(raw,rows[member.name]);dst=before/member.name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(raw)
    after=args.output/'after-reference';shutil.copytree(before,after);rel='archroot/docs/coop/design-corrections/foundation/enumeration_model.v1.py';candidate=(here/'candidate.py').read_bytes();(after/rel).write_bytes(candidate)
    old_source=(before/rel).read_text();new_source=candidate.decode();old_block='''            if loc in binding_by:
                schema_failed.add(loc)
            continue''';new_block='''            try:
                if loc in binding_by:
                    schema_failed.add(loc)
            except TypeError:
                # JSON-C array/object locator fields cannot name a binding.
                # Keep the schema refusal and allow missing-record accounting.
                pass
            continue'''
    require(old_source.count(old_block)==1 and old_source.replace(old_block,new_block)==new_source,'candidate exceeds exact narrow correction')
    old=load('totality42_before',before/rel);new=load('totality42_after',after/rel);raw=lzma.decompress((here/'cases.ndjson.xz').read_bytes());verify(raw,json.loads((here/'cases-pin.json').read_bytes()));cases=[json.loads(line)for line in raw.splitlines()];unchanged=0;corrected=0;bad=[]
    def run(model,q):
        try:return model.admit_enumeration(**q)
        except Exception as exc:return {'exception':type(exc).__name__,'message':str(exc)}
    for row in cases:
        q=copy.deepcopy(row['input']);q['source_blobs']={k:bytes.fromhex(v)for k,v in q['source_blobs'].items()};b=run(old,q);a=run(new,q)
        require(b==row['before']and a==row['expected'],'recorded reference output differs: '+row['label'])
        if b==a:unchanged+=1
        elif b.get('exception')=='TypeError' and a.get('result')=='REFUSE'and a.get('refusals')==['ENUMERATION_INVENTORY_SCHEMA','ENUMERATION_INVENTORY_MISSING_RECORD']:corrected+=1
        else:bad.append({'label':row['label'],'before':b,'after':a})
    result={'cases':len(cases),'unchangedDefined':unchanged,'formerTypeErrorsNowRefuse':corrected,'mismatches':bad,'predecessorSha256':hashlib.sha256(old_source.encode()).hexdigest(),'candidateSha256':hashlib.sha256(candidate).hexdigest(),'standing':'Proposed reference totality correction only, not selected; keeps all defined scalar locator semantics'}
    (args.output/'result.json').write_text(json.dumps(result,indent=2)+'\n');require(result==json.loads((here/'expected-result.json').read_bytes()),'comparison result differs');print(json.dumps(result))
if __name__=='__main__':main()
