import re,subprocess,pathlib,shutil
src=pathlib.Path('work/tools/verify_design.py').read_text().splitlines(keepends=True)
target=pathlib.Path('mut/tools/verify_design.py')
res=[]
for i,l in enumerate(src):
    if not (130<=i+1<=254 or i+1 in (305,307,308)): continue
    m=re.match(r'^(\s*)raise DesignError\((.*)\)\s*$',l)
    if not m: continue
    mut=src[:]; mut[i]=m.group(1)+'pass\n'
    target.write_text(''.join(mut))
    r=subprocess.run(['python3','-B','-m','unittest','discover','-s','mut/tools/tests'],capture_output=True,text=True)
    res.append((i+1,'KILLED' if r.returncode else 'SURVIVED',m.group(2)[:70]))
# condition mutations
extra=[
 (163,"(len(key) > 1 and key[0] == \"0\") or ",""),
 (159,"i + 1 == len(token) or ",""),
 (212,"(\"sha256\", \"bytes\")","(\"sha256\",)"),
 (235,"not after or ",""),
 (235," or before == after",""),
 (147,"not 1 <= line","not 0 <= line"),
 (198,"!= binding[\"record\"]","is None"),
 (228,"!= parent","is None"),
 (230,"parent[\"path\"], ",""),
 (189," or assent.get(\"rootSubstantiveAssent\") is not True",""),
 (193,", size=True",""),
 (218,"pinned_bytes(architecture, record[\"previousCandidate\"])","pass"),
 (207,"pinned_bytes(architecture, row)","pass"),
 (196,"pinned_bytes(architecture, row)","pass"),
 (307,"{**effective, ","{**{r['path']:r for r in lock['inputs']}, "),
]
for ln,a,b in extra:
    mut=src[:]; assert a in mut[ln-1],(ln,a,mut[ln-1]); mut[ln-1]=mut[ln-1].replace(a,b,1)
    target.write_text(''.join(mut))
    r=subprocess.run(['python3','-B','-m','unittest','discover','-s','mut/tools/tests'],capture_output=True,text=True)
    res.append((ln,'KILLED' if r.returncode else 'SURVIVED','COND '+a[:50]))
target.write_text(''.join(src))
for x in res: print(*x)
