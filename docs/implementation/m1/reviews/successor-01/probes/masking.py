"""Show which guard actually fires for each subject test refusal case (reviewer probe)."""
import copy, importlib.util, sys, unittest
from pathlib import Path
S=Path('/tmp/opensip-implementation/m1-successor-subject-01')
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('tdb',S/'tools/tests/test_design_binding.py'); T=importlib.util.module_from_spec(spec); spec.loader.exec_module(T)
M=T.MODULE
class Probe(T.InventorySuccessorTests):
    def runTest(self): pass
def msg(t):
    try: M.verify(t.root,t.lock); return 'ACCEPTED'
    except M.DesignError as e: return str(e)
cases=[
 ("review verdict CHANGES-REQUIRED","review",lambda d:d.update(verdict="CHANGES-REQUIRED")),
 ("review requiredFindings open","review",lambda d:d.update(requiredFindings=["open"])),
 ("assessment requiredFindings open","review",lambda d:d["inventoryCandidateAssessment"].update(requiredFindings=["open"])),
 ("assessment sha changed","review",lambda d:d["inventoryCandidateAssessment"].update(sha256="0"*64)),
 ("assessment successorRecord sha changed","review",lambda d:d["inventoryCandidateAssessment"]["successorRecord"].update(sha256="0"*64)),
 ("record parent sha changed","record",lambda d:d["parent"].update(sha256="0"*64)),
 ("record candidate bytes 0","record",lambda d:d["candidate"].update(bytes=0)),
 ("record inheritedRowsEqualByValue False","record",lambda d:d.update(inheritedRowsEqualByValue=False)),
]
for name,key,mut in cases:
    t=Probe(); t.setUp(); t.change(key,mut); print(f'{name:45s} -> {msg(t)}')
t=Probe(); t.setUp(); other=t.write("other.json", t.parent); t.lock["inventorySuccessor"]["parent"]=other; print(f'{"parent other.json (test_parent_must_be_selected)":45s} -> {msg(t)}')
t=Probe(); t.setUp(); t.lock["inventorySuccessor"]["extra"]=True; print(f'{"extra binding key True":45s} -> {msg(t)}')
t=Probe(); t.setUp(); t.lock["inventorySuccessor"]["extra"]=t.lock["inventorySuccessor"]["record"]; print(f'{"extra binding key with valid pin":45s} -> {msg(t)}')
# Correctly rebound variants: mutate review, then rebind assent to the new review pin.
def rebound_review(mut):
    t=Probe(); t.setUp(); t.change("review",mut); rv=t.lock["inventorySuccessor"]["review"]
    t.change("assent",lambda d:d["actualClaudeReview"].update(sha256=rv["sha256"])); return msg(t)
for name,_,mut in cases[:5]: print(f'REBOUND {name:37s} -> {rebound_review(mut)}')
t=Probe(); t.setUp(); t.candidate=copy.deepcopy(t.parent); t.candidate["standing"]="x"; t.bind(); print(f'{"zero additions fully rebound":45s} -> {msg(t)}')
t=Probe(); t.setUp(); t.candidate=copy.deepcopy(t.parent); t.bind()
for k in ("candidate",): t.lock["inventorySuccessor"][k]=t.lock["inputs"][0]
print(f'{"candidate pin == parent pin":45s} -> {msg(t)}')
t.cleanup=None
