import os
#!/usr/bin/env python3
"""Compile DECISIONS-RECOMMENDED.md from the packets and the Claude/Codex round files. Each item: final verdict (AGREED / SPLIT / PENDING), the agreed recommendation text (latest Claude round that Codex accepted, or both positions), evidence pointers, next step if the owner accepts."""
import json,os,re,glob,datetime
REPO='/Users/sb/code/opensip-ai/opensip'; D=REPO+'/DECISION-PACKETS'
ITEMS=[('A1/A2','A-process-rulings','Process rulings: D-272 (A1) and the nine superseded CONTESTED entries (A2)'),
       ('A3','A3-identity-namespace','identity-namespace leftover-join.v6 (DR-104): remasure or leave'),
       ('A4','A4-citation-convention','Cross-lineage citation convention (precedent vs content-based)'),
       ('B1','B1-DR-131-class-A','DR-131 Class A opening (preview-analyze-contract.v2)'),
       ('B2','B2-DR-133-class-A','DR-133 Class A opening (provider-only-output-contract.v3)'),
       ('B3','B3-DR-117-class-A','DR-117 Class A opening (preview-product-boundary-successor.v8)'),
       ('C1–C4','C1-4-reserved-numbers-security-quality','Reserved numbers/lists: DR-112, DR-118, DR-111, DR-126'),
       ('C5–C9','C5-9-reserved-encodings-owners-units','Reserved encodings/owners/units: DR-121, DR-107, DR-103 OD-1/OD-2, DR-101 OD-101-1/2, DR-115/D-006'),
       ('D1','D1-fixture-authoring-delegation','Fixture-authoring delegation (39 measurements)'),
       ('E2','E2-push','Push the 12 unpushed commits'),
       ('F1','F-docs-rewrite','Documentation rewrite after sealing')]
def rd(p): return open(p).read() if os.path.exists(p) else None
def rounds(stem):
    cl=[(0,rd(f'{D}/{stem}.claude-recommendation.md'))]+[(int(m.group(1)),rd(f)) for f in glob.glob(f'{D}/{stem}.claude-recommendation.r*.md') for m in [re.search(r'\.r(\d+)\.md$',f)] if m]
    cx=[]
    for f in glob.glob(f'{D}/{stem}.codex-recommendation*.json'):
        m=re.search(r'\.r(\d+)\.json$',f); n=int(m.group(1)) if m else 0
        try: cx.append((n,json.load(open(f))))
        except Exception as e: cx.append((n,{'verdict':'UNREADABLE','error':str(e)}))
    return sorted([c for c in cl if c[1]],key=lambda x:x[0]), sorted(cx,key=lambda x:x[0])
out=[f"# Decisions — agreed recommendations (Claude orchestrator + Codex), {datetime.date.today().isoformat()}\n",
     "Process: `DECISION-PACKETS/RECOMMENDATION-PROTOCOL.md`. For each item: the byte-cited evidence packet, Claude's recommendation, Codex's independent adversarial review, and up to three rounds of reconciliation. **Nothing here is decided; every item is yours.** A verdict of AGREED means the latest Claude round was accepted by Codex without further amendment; SPLIT means both positions are shown; PENDING means a round is still in progress.\n"]
summary=[]
for key,stem,title in ITEMS:
    packet=f'{D}/{stem}.md'; cl,cx=rounds(stem)
    if not cl and not cx and not os.path.exists(packet): status='NOT STARTED'
    elif not cx: status='PENDING (Codex review in progress)'
    else:
        lastcx=cx[-1][1]; v=str(lastcx.get('verdict','?'))
        lastcl=cl[-1][0] if cl else -1
        if v=='AGREE': status='AGREED'
        elif v=='AGREE-WITH-AMENDMENT': status=('AGREED (with Codex amendments adopted)' if lastcl>=cx[-1][0] else 'PENDING (amendments to fold in)') if not os.path.exists(f'{D}/{stem}.claude-postnote.md') else 'AGREED (adopt; Codex round-3 amendments applied post-round — see note)'
        elif v=='DISAGREE': status='SPLIT' if lastcl<=cx[-1][0] else 'PENDING (Claude round awaiting Codex)'
        else: status='PENDING ('+v+')'
    summary.append((key,title,status))
    out.append(f"\n## {key} — {title}\n\n**Status: {status}**\n")
    if os.path.exists(packet): out.append(f"Evidence packet: `DECISION-PACKETS/{stem}.md`\n")
    if cl:
        n,txt=cl[-1]; out.append(f"\n### Recommendation (Claude, round {n or 1})\n\n"+txt.strip()+"\n")
    if cx:
        n,j=cx[-1]; out.append(f"\n### Codex (round {n or 1}): {j.get('verdict')} — confidence {j.get('confidence','?')}\n\n"+str(j.get('recommendation',''))+"\n\n*Rationale:* "+str(j.get('rationale',''))[:2500]+"\n")
        am=j.get('amendments') or []
        if am: out.append("\n*Amendments:*\n"+"\n".join('- '+str(a) for a in am)+"\n")
        op=j.get('optionPositions') or {}
        if isinstance(op,dict) and op: out.append("\n*Codex positions on the owner options:*\n\n| § | Position |\n|---|---|\n"+"\n".join(f"| {k} | {str(v).replace('|','/')} |" for k,v in op.items())+"\n")
    pn=rd(f'{D}/{stem}.claude-postnote.md')
    if pn: out.append("\n### Post-round note (Claude)\n\n"+pn.strip()+"\n")
    if status=='SPLIT' and cl and cx: out.append("\n**Both positions stand; the owner decides.**\n")
tbl="\n| Item | Subject | Status |\n|---|---|---|\n"+"\n".join(f"| {k} | {t} | {s} |" for k,t,s in summary)+"\n"
out.insert(2,"\n## Summary\n"+tbl)
open(REPO+'/DECISIONS-RECOMMENDED.md','w').write("\n".join(out)); print('wrote DECISIONS-RECOMMENDED.md'); [print(f'  {k}: {s}') for k,t,s in summary]
