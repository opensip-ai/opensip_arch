"""Mutation probe: does the 17-test suite detect weakened successor checks?"""
import shutil, subprocess, sys, tempfile
from pathlib import Path
S=Path('/tmp/opensip-implementation/m1-successor-subject-01'); SRC=(S/'tools/verify_design.py').read_text()
TEST=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else S/'tools/tests/test_design_binding.py'
print('TEST FILE',TEST)
MUT={
 'M01 drop parent-in-inputs': ('    if parent_pin not in selected_inputs:\n        raise','    if False:\n        raise'),
 'M02 drop candidate!=parent path': ('    if binding["candidate"]["path"] == parent_pin["path"]:','    if False:'),
 'M03 record candidate without size': ('same_reference(record.get("candidate"), binding["candidate"], "successor candidate", size=True)','same_reference(record.get("candidate"), binding["candidate"], "successor candidate")'),
 'M04 drop record flags': ('if record.get("parentArtifactBytesUnchanged") is not True or record.get("inheritedRowsEqualByValue") is not True:','if False:'),
 'M05 drop review verdict': ('review.get("verdict") != "ACCEPT-UNIT" or ',''),
 'M06 drop assessment verdict': (' or assessment.get("verdict") != "ACCEPT"',''),
 'M07 drop assessment findings': (' or assessment.get("requiredFindings") != []',''),
 'M08 drop review candidate join': ('    same_reference(assessment, binding["candidate"], "review candidate", size=True)\n',''),
 'M09 drop review parent join': ('    same_reference(assessment.get("parent"), parent_pin, "review parent", size=True)\n',''),
 'M10 drop review record join': ('    same_reference(assessment.get("successorRecord"), binding["record"], "review successor record")\n',''),
 'M11 drop assent status': ('assent.get("status") != "ACCEPTED-UNIT" or ',''),
 'M12 drop assent unit findings': (' or assent.get("requiredUnitFindings") != []',''),
 'M13 drop root review join': ('    same_reference(assent.get("actualClaudeReview"), binding["review"], "root review")\n',''),
 'M14 drop root inventory join': ('    same_reference(assent.get("acceptedInventory"), binding["candidate"], "root inventory")\n',''),
 'M15 drop subject digest equality': (' or subject["sha256"] != review.get("subjectManifestSha256")',''),
 'M16 drop top-level key set equality': ('set(parent) != set(candidate) or ',''),
 'M17 exempt packages from equality': ('("standing", "files")','("standing", "files", "packages")'),
 'M18 drop sorted check': ('list(current) != sorted(current) or ',''),
 'M19 allow zero additions': ('not set(inherited) < set(current)','not set(inherited) <= set(current)'),
 'M20 drop inherited row equality': ('    if any(current.get(path) != row for path, row in inherited.items()):\n        raise','    if False:\n        raise'),
 'M21 v1 may carry inventorySuccessor': ('({"inventorySuccessor"} if version == 2 else set())','({"inventorySuccessor"} if version == 2 else {"inventorySuccessor"})'),
 'M22 v2 successor optional': ('    if version == 2:\n','    if version == 2 and "inventorySuccessor" in lock:\n'),
 'M23 drop closed binding keys': ('set(binding) != fields','not fields <= set(binding)'),
 'M24 drop duplicate row path': ('or path in result:','or False:'),
 'M25 drop assent substantive': (' or assent.get("rootSubstantiveAssent") is not True',''),
 'M26 drop review findings': (' or review.get("requiredFindings") != []',''),
}
survivors=[]
for name,(old,new) in MUT.items():
    assert SRC.count(old)==1, (name, SRC.count(old))
    if name=='M22 v2 successor optional':
        mutated=SRC.replace(old,new).replace('set(lock) != fields | ({"inventorySuccessor"} if version == 2 else set())','not (set(lock) - {"inventorySuccessor"}) == fields')
    else: mutated=SRC.replace(old,new)
    d=Path(tempfile.mkdtemp(prefix='mut-',dir='.'))
    try:
        (d/'tools/tests').mkdir(parents=True); (d/'tools/verify_design.py').write_text(mutated)
        shutil.copy(TEST, d/'tools/tests/test_design_binding.py')
        r=subprocess.run([sys.executable,'-I','-B','-m','unittest','discover','-s','tools/tests','-t','tools/tests'],cwd=d,capture_output=True,text=True)
        killed=r.returncode!=0; tail=r.stderr.strip().splitlines()[-1]
        print(('KILLED  ' if killed else 'SURVIVED'),name,'::',tail)
        if not killed: survivors.append(name)
    finally: shutil.rmtree(d)
print('SURVIVORS',len(survivors),survivors)
