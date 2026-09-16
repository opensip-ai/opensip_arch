from pathlib import Path
import json,hashlib
root=Path.cwd();out=Path('/tmp/opensip-design-corrections/application-draft.v3'); files=out/'files'; files.mkdir(exist_ok=True)
app='docs/coop/design-corrections/application.v1.json'; rm='docs/coop/design-corrections/readiness-row-map.v1.json'
rows=json.loads((out/'readiness-row-map.proposed.json').read_text())['rows']; edits=[]
def stage(rel,text):
 p=files/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text);old=(root/rel).read_bytes();edits.append({'path':rel,'beforeSha256':hashlib.sha256(old).hexdigest(),'proposedSha256':hashlib.sha256(p.read_bytes()).hexdigest()})
p='docs/START-HERE.md';s=(root/p).read_text();a=s.index('1. Read');b=s.index('\nThe result',a);s=s[:a]+'''1. Read [the product scope and delivery stages](v2/architecture/10-mvp-and-future-scope.md): one complete product design, implemented in stages.
2. Read [the consolidated product contracts](v2/contracts/product-v1/README.md) for the current identity/evidence, security/lifecycle, native language, workflow/output and admission contracts.
3. Read [the decision and readiness register](v2/architecture/08-decision-and-readiness-register.md#unified-product-design-readiness) for design acceptance, release obligations and separate implementation authorization.
4. Use [the current-source map](coop/design-corrections/current-source-map.proposed.md) when tracing older architecture chapters. D-372 applies its owning successors while preserving compatible inherited laws and historical reviews.
''' + s[b:];a=s.index('The unified intended-product design is in progress');s=s[:a]+'''The complete intended-product design is accepted under D-372, following actual Claude's independent review and a fresh blind consumer review. [The application record](coop/design-corrections/application.v1.json) pins the exact subjects and evidence. The [central register](v2/architecture/08-decision-and-readiness-register.md#unified-product-design-readiness) records conditions 1–4 at design level. Condition 5 remains NOT MET: implementation is not authorized, and release qualification is still required. D-369 remains the historical preview milestone.
''';s=s.replace('Read [the joint architecture audit](coop/architecture-depth-review/REVIEW.md): concrete defects, remaining contract joins and the correction order.','Read [the correction record](coop/design-corrections/README.md) for the addressed findings and retained independent reviews; the [original audit](coop/architecture-depth-review/REVIEW.md) remains historical evidence.');stage(p,s)
p='docs/v2/architecture/12-architecture-completion-goal.md';s=(root/p).read_text().replace('**Full-product design is IN PROGRESS.**','**Full-product design is accepted under D-372.**');s=s.replace('> implementation milestone within that design.','> implementation milestone within that design. Condition 5 remains NOT MET;\n> implementation and release qualification are separate.');stage(p,s)
p='docs/v2/architecture/10-mvp-and-future-scope.md';s=(root/p).read_text();pos=s.index('\n\n');s=s[:pos]+'''\n\nThe [consolidated product contracts](../contracts/product-v1/README.md), independently reviewed and applied by D-372, supply the complete selected design. [The central register](08-decision-and-readiness-register.md#unified-product-design-readiness) records its acceptance and separate implementation authorization. Language-independent discovery, evidence, workflow and output contracts are implemented by native TS/JS/Rust components where language semantics are required.''' + s[pos:];stage(p,s)
p='docs/catalog/current-design.md';s=(root/p).read_text();s=s.replace('Custody paths are intentionally unchanged.','Custody paths are intentionally unchanged. D-372 makes the consolidated product contracts the current owning account; historical chapters are read through its source map.');pos=s.index('\n- ');new='\n- `REFERENCED` [Product contract index](../v2/contracts/product-v1/README.md)\n- `REFERENCED` [Applied current-source map](../coop/design-corrections/current-source-map.proposed.md)\n';s=s[:pos]+new+s[pos:];stage(p,s)
p='docs/v2/architecture/08-decision-and-readiness-register.md';s=(root/p).read_text();s=s.replace('**IN PROGRESS for the unified intended product (D-371).**','**COMPLETE at design level for the unified intended product (D-372).**');a=s.index('## Unified product design readiness');b=s.index('## Blueprint-readiness decision',a);old=s[a:b];hist=old[old.index('### Joint depth-review evidence'):];hist=hist.replace('### Joint depth-review evidence — 2026-09-05','### Historical depth-review findings — 2026-09-05');hist=hist.replace('Its reconciled conclusion is NOT READY for implementation.','Its then-current conclusion was NOT READY for implementation.');c=hist.index('Every applicable obligation still needs');hist=hist[:c]+'''The audit found corrections required and did not itself satisfy condition 3. D-372's application below records the reviewed successors and actual blind consumer result; the original audit and its exact evidence remain unchanged. No product qualification is claimed.

'''
new='''## Unified product design readiness

**D-372: complete at design level; implementation is not authorized.** The
[application record](../../coop/design-corrections/application.v1.json) pins the
accepted complete product contracts, independent actual-Claude review, fresh
blind consumer B, every correction/residual disposition and exact documentation
delta. [The contract index](../contracts/product-v1/README.md) is the single
current owning account. D-369 remains a historical preview acceptance.

D-371's condition-2 set remains the same 28 existing rows: DR-101–107,
DR-109–115, DR-117–127 and DR-130/131/133. DR-108/116/128/129 remain explicitly
outside this bounded scope (credentials, third-party ecosystem, untrusted
contributions, TUI). No product capability was moved out of the design to obtain
completion. All selected features have contracts now, with implementation in
stages. Historical grades below retain their own scope; this section supplies
the current full-product application of the same rows, without duplicate IDs.

| Current full-product condition | Standing under D-372 |
|---|---|
| 1 — inherited semantics | MET by reviewed prospective dispositions for all DR-001–011, all sixteen DR-011 residuals and all thirty evaluation subresiduals. Actual fresh blind consumer B closes R10. DR-003's demonstration timing is explicitly disposed by the accepted D-372 act; native measurements remain mandatory release gates. No old rejected/unreviewed checker gains standing. |
| 2 — affected product rows | MET: all 28 existing affected rows have independently accepted full-product design dispositions in the per-row application map below. This is a design grade, not measured product qualification. |
| 3 — integrated independent review | MET through the retained fresh actual-Claude review of mixed final bytes, Codex technical review/assent, blind consumer B and independent application review under DR-201–205. Authors do not independently accept their own bytes. |
| 4 — qualification ownership and contracts | MET at design level: all32 DR-G01–32 mappings name current contracts, owners, harness scope and acceptance requirements. Harness implementation/execution and real supported-platform qualification remain required; none is claimed QUALIFIED or DEMONSTRATED here. |
| 5 — implementation authorization | NOT MET. The user authorized architecture/design/reference work only. Implementation requires a separate explicit authorization after these accepted design records. |

The [per-row map](../../coop/design-corrections/readiness-row-map.v1.json) records
exact successor hashes/selectors, compatible inherited accounts, required
release gates and independent grades. Each row below is SATISFIED at the
**design-contract** level for the D-371 intended product, subject to the retained
TCB assumptions and mandatory implementation/release evidence.

| Existing row | Accepted design disposition |
|---|---|
'''
for row in rows:new+='| '+row['id']+' | '+row['disposition']+' |\n'
new+='''
The [applied source map](../../coop/design-corrections/current-source-map.proposed.md)
and application record reconcile historical command vocabularies, platforms,
identity/retention reductions and preview standing. The proposed source filenames
are preserved as reviewed bytes; D-372 is the external act that makes the named
content effective. Current inventories are navigation/accounting records, never
retroactive authenticity for historical acceptance.

'''+hist
stage(p,s[:a]+new+s[b:])
(out/'documentation-proposal.json').write_text(json.dumps({'standing':'STAGED ONLY; requires substantive independent design, blind consumer and application acceptance before applying','edits':edits},indent=2)+'\n');print(len(edits),'documents staged; repository unchanged')
