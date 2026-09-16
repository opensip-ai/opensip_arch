from common import *
from referencing.exceptions import Unresolvable
import re
# Transitive closure of all $ref targets reachable from report-projection:1
seen_docs=set(); unresolved=[]; edges=0
def refs(o):
    if isinstance(o, dict):
        for k,v in o.items():
            if k=="$ref" and isinstance(v,str): yield v
            else: yield from refs(v)
    elif isinstance(o,list):
        for v in o: yield from refs(v)
queue=[(chk.RID, schema)]
all_docs={chk.RID:schema, **docs}
visited=set()
while queue:
    base_id, sub = queue.pop()
    for r in refs(sub):
        edges+=1
        target = r if not r.startswith("#") else base_id + r
        doc_id, _, frag = target.partition("#")
        if doc_id not in all_docs:
            unresolved.append((base_id, r)); continue
        key=(doc_id, frag)
        if key in visited: continue
        visited.add(key); seen_docs.add(doc_id)
        try:
            resolved = registry.resolver().lookup(target).contents
        except Unresolvable as e:
            unresolved.append((base_id, r)); continue
        queue.append((doc_id, resolved))
print("ref edges", edges, "distinct targets", len(visited), "documents reached", len(seen_docs))
for d in sorted(seen_docs): print("  ", d)
print("unresolved", unresolved)
print("registered-but-unreached", sorted(set(docs)-seen_docs))
# recursion reachable from envelope4: defs that (transitively) reference themselves
graph={}
for (d,frag) in visited:
    sub = registry.resolver().lookup(d+"#"+frag).contents if frag else all_docs[d]
    tg=set()
    for r in refs(sub):
        t = r if not r.startswith("#") else d + r
        tg.add(tuple(t.partition("#")[::2]))
    graph[(d,frag)]=tg
def reach(start):
    st=[start]; s=set()
    while st:
        n=st.pop()
        for m in graph.get(n,()):
            if m not in s: s.add(m); st.append(m)
    return s
rec=[n for n in graph if n in reach(n) and n[1]]
print("recursive defs:", sorted(rec)[:30])
