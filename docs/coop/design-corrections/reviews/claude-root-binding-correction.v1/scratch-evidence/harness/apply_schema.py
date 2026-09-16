import json,hashlib,collections,sys
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch'
p=S+'/src25/docs/coop/design-corrections/native/native-evidence.schemas.v2.json'
raw=open(p,'rb').read()
before=hashlib.sha256(raw).hexdigest()
d=json.loads(raw,object_pairs_hook=collections.OrderedDict)
defs=d['$defs']; keys=list(defs.keys())
NUL=chr(92)+'u0000'
BS=chr(92)+chr(92)
SEG='[^'+NUL+BS+'/]+'
DOT='(?!.*(^|/)'+chr(92)+'.'+chr(92)+'.?(/|$))'
END='(?!['+chr(92)+'s'+chr(92)+'S])'
DIR='^'+DOT+SEG+'(/'+SEG+')*'+END
ROOT='^(?:|'+DOT+SEG+'(/'+SEG+')*)'+END
print('DIR ',DIR)
print('ROOT',ROOT)
dirdesc=('INTERNAL relative DIRECTORY form: one or more slash-joined non-empty segments, no leading or trailing slash, '
 'no empty segment, no . or .. segment, no NUL and no backslash. This restates CanonicalPath dot-segment and character '
 'custody for a DIRECTORY and additionally closes two spellings CanonicalPath accepts that are not canonical for a '
 'directory used as a membership prefix: a trailing slash and an interior empty segment. The project root is NOT '
 'spelled here; see InternalUnitRootV1.')
rootdesc=('INTERNAL unit root: the EMPTY STRING for the project root, otherwise a CanonicalRelativeDirV1. The external '
 'sentinel . is NEVER a value of this field. . is the EXTERNAL spelling only: Config2 discovery.workspaceRoots and CLI '
 '--workspace-root (normalized inward by discovery-defaults.normalize_explicit_root) and the outward workspaceRoot of '
 'enumeration cells (spelled by discovery-defaults.spell_root). A retained WorkspaceUnitV2 carries the internal form and '
 'is never silently normalized after retention: _under_unit, _rel and the deepest-unit length ranking all read this '
 'field as an exact prefix.')
cd=collections.OrderedDict()
cd['type']='string'; cd['minLength']=1; cd['maxLength']=4096; cd['pattern']=DIR; cd['description']=dirdesc
ir=collections.OrderedDict()
ir['type']='string'; ir['maxLength']=4096; ir['pattern']=ROOT; ir['description']=rootdesc
new=collections.OrderedDict()
for k in keys:
    new[k]=defs[k]
    if k=='CanonicalPath':
        new['CanonicalRelativeDirV1']=cd
        new['InternalUnitRootV1']=ir
d['$defs']=new
wu=new['WorkspaceUnitV2']['properties']
rp=collections.OrderedDict(); rp['$ref']='#/$defs/InternalUnitRootV1'
wu['rootPath']=rp
it=collections.OrderedDict(); it['$ref']='#/$defs/CanonicalRelativeDirV1'
wu['memberPackageRoots']['items']=it
out=json.dumps(d,indent=1)+chr(10)
open(p,'w',encoding='utf-8').write(out)
print('before',before)
print('after ',hashlib.sha256(out.encode()).hexdigest())
