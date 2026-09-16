"""N34/N28/N29 equivalence probe on the real lock: a parent pin sharing an input path but differing sha/bytes cannot pass pinning."""
import copy, importlib.util
from pathlib import Path
S=Path('/tmp/opensip-implementation/m1-successor-subject-02'); A=Path('/Users/sb/code/opensip-ai/opensip_arch')
spec=importlib.util.spec_from_file_location('vd',S/'tools/verify_design.py'); M=importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
base=M.decode((S/'design-lock.json').read_bytes())
for label,change in [('parent sha differs, same path',{'sha256':'0'*64}),('parent bytes differ, same path',{'bytes':1}),('parent sha+bytes differ',{'sha256':'1'*64,'bytes':2})]:
    l=copy.deepcopy(base); l['inventorySuccessor']['parent'].update(change)
    try: M.verify(A,l); print(label,'-> ACCEPTED')
    except M.DesignError as e: print(label,'-> REFUSED:',e)
