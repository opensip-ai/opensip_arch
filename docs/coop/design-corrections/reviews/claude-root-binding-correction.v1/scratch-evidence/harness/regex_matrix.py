import re,json,sys
SEG=r'[^\u0000\\/]+'
DOT=r'(?!.*(^|/)\.\.?(/|$))'
DIR='^'+DOT+SEG+'(/'+SEG+')*(?![\\s\\S])'
ROOT='^(?:|'+DOT+SEG+'(/'+SEG+')*)(?![\\s\\S])'
print('CanonicalRelativeDirV1 pattern:',DIR)
print('InternalUnitRootV1     pattern:',ROOT)
print()
old=re.compile(r'^(?!/)(?!.*(^|/)\.\.?(/|$))[^\u0000\\]+(?![\s\S])')
d=re.compile(DIR);r=re.compile(ROOT)
cases=['','.','..','a','crates/alpha','crates/alpha/','crates//alpha','/abs','a/./b','a/../b','a/.','a/..','./a','../a','a\\b','a\x00b','a/','//','a b','crates/foo#bar','deep/a/b/c/d','.hidden','a/.hidden','..a','a..','x/./','/']
print('%-18s %-14s %-22s %-20s' % ('value','CanonicalPath','CanonicalRelativeDirV1','InternalUnitRootV1'))
for c in cases:
    print('%-18s %-14s %-22s %-20s' % (repr(c), bool(old.search(c)), bool(d.search(c)), bool(r.search(c))))
json.dump({'CanonicalRelativeDirV1':DIR,'InternalUnitRootV1':ROOT},open(sys.argv[1],'w'),indent=1)
