#!/usr/bin/env python3
"""Freeze preview-product-boundary-successor.v9 into docs/coop/artifacts (0444), write its Stage A review prompt (0444) and the dispatch text."""
import os, sys, json, hashlib, subprocess, shutil, re
REPO='/Users/sb/code/opensip-ai/opensip'; os.chdir(REPO); A='docs/coop/artifacts/'; P=lambda n: A+n
V=int(sys.argv[1]) if len(sys.argv)>1 else 9
SRC=f'/private/tmp/claude-501/-Users-sb-code-opensip-ai-opensip/dcbad0ae-7fad-4c78-89e7-e93d989f5501/scratchpad/ppbs-v9/preview-product-boundary-successor.v{V}.json'
COORD='docs/coop/COORDINATOR-DECISIONS.md'; F08='docs/v2/architecture/08-decision-and-readiness-register.md'
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def git(*a): return subprocess.check_output(['git',*a],text=True).strip()
HEAD=git('rev-parse','HEAD'); heads=[l for l in open(COORD).read().split('\n') if l.startswith('## D-')]; LASTD=re.match(r'## (D-\d+)',heads[-1]).group(1)
j=json.load(open(SRC)); assert j['head']==HEAD, ('regenerate v9 at HEAD', j['head'], HEAD); assert j['version']==V and j['requiredNowUnchanged']==28
DST=P(f'preview-product-boundary-successor.v{V}.json'); assert not os.path.exists(DST)
shutil.copyfile(SRC,DST); os.chmod(DST,0o444); DS=sha(DST)
joins=[(k,v) for k,v in j['basedOn'].items() if isinstance(v,dict) and 'Join' in k and v.get('path')]
joinlist='\n'.join(f"- `{v['path']}` `{v['sha256']}` ({v.get('recording','')})" for k,v in joins)
CL=f'preview-product-boundary-successor.v{V}.review-independent.claude2.json'; CX=f'preview-product-boundary-successor.v{V}.review-independent.codex.json'
rejected=[v for v in range(9,V) if os.path.exists(P(f'preview-product-boundary-successor.v{v}.json'))]
rejsent=''.join(f" preview-product-boundary-successor.v{v} (`{sha(P(f'preview-product-boundary-successor.v{v}.json'))}`) was REJECTED at Stage A by both reviewers and is unrecorded; it remains frozen; do not treat it as this subject; check that this subject lands every finding of both v{v} reviews (their ids are named in the subject's findingDisposition)." for v in rejected)
prompt=f"""# Independent review — preview-product-boundary-successor.v{V}

Independent, refute not confirm.

**SUBJECT:** `{DST}`
Expected sha256:
`{DS}`
Mode 0444. If the subject moves, OBJECT / REJECT.

preview-product-boundary-successor.v8 (`{sha(P('preview-product-boundary-successor.v8.json'))}`, D-207) remains frozen and remains the current recorded DR-117 leftover remasurement until a coordinator act records this subject.{rejsent} Do not treat preview-product-boundary-successor.v8 as this subject. product-boundary-successor-contract.v8 (`{sha(P('product-boundary-successor-contract.v8.json'))}`, D-116) is a distinct lineage; do not treat it as this subject either.

**WRITE ONLY:**
- Claude 2: `{P(CL)}`
- Codex: `{P(CX)}`

Do not edit the subject. Do not commit. Do not edit file 08 or COORD.
Do not mark SATISFIED. Do not SATISFY DR-117.
Do not reopen leftover-design of unnamed EE classes.
Do not steal leftover-design of OBL-G29-FX-AUTHORING or OBL-G30-FX-AUTHORING.
Do not steal leftover-design of OBL-FX-AUTHORING, OBL-G14-FX-AUTHORING, OBL-G16-FX-AUTHORING, or OBL-G21-FX-AUTHORING.
Do not steal leftover-design of OBL-THRESHOLDS, OBL-MATRIX-CORPUS, or OBL-G13-RESERVED.
Do not name G13 into required-now.
Do not invent fixture bytes or the DR-131 pack.
Do not lift D-137's Class A reservation; do not open D-056 Class A (only the owner-controlled entry D-293 Decision 5 reserves can).
Do not change live required-now 28.
Do not authorize implementation. Do not read the other reviewer.

HEAD is `{HEAD}` ({LASTD} ADOPTED). Last heading is {LASTD}. Required-now is 28.
Live COORD sha256 is `{sha(COORD)}`; file 08 sha256 is `{sha(F08)}`.
This is an architecture-row successor (DR-117), not a gate row. It is the candidate limb of the DR-117 programme the owner adopted at D-293 Decision 5 (read that entry): author the successor re-citing the twelve current leftover-joins and stating its relationship to product-boundary-successor-contract.v8; then a fresh application-grade dual review bound to the successor's final digest — this review; then the owner-controlled opening entry; then G29/G30 fixture authoring; then a separate SATISFIED-GRADE + MF-6 cycle.
Under D-294 (ADOPTED), a cross-lineage leftover-join citation is custody at the citing artifact's recording; measure the twelve citations against the versions current at HEAD (the highest non-CONTESTED `## D-NNN — Record <lineage> leftover-join.vN` heading), which the subject names as:
{joinlist}
Stating that D-056 gates 2 and 3 hold for DR-117 is lawful (D-159). Claiming that Gate 1 Class A holds, or is opened by this subject, is not.

**The grade question (D-005 form; answer it in a top-level `gradeRuling` object):** is this subject, as bytes, acceptable at application grade — T2-02's "application-grade acceptance with no express reservation" — as DR-117's preview-scoped design candidate, once the owner lifts D-137's reservation by the owner-controlled entry? Answer `"ruling": "SUSTAINED FOR APPLICATION"` or `"NOT SUSTAINED"`, with `"reservationSweep"`: every reservation-language sentence your own verdict carries (quote each; an empty list means none), and `"reasons"`. Answering SUSTAINED does not open Class A and marks nothing SATISFIED; it records a reviewer judgment the record currently lacks for this lineage (packet B3 §4c). Answer NOT SUSTAINED if any byte of the subject would need to change before application.

Attack:
- leftover-design of unnamed EE classes reopened
- leftover-design of OBL-G29-FX-AUTHORING or OBL-G30-FX-AUTHORING stolen or claimed closed
- preview-product-boundary-successor.v8 recorded as a current remasurement, or its history misstated (v5 D-137; v6 rejected, unrecorded; v7 D-168; v8 D-207)
- the fourteen enforcement-evidence classes or the seven dispositions differ from preview-product-boundary-successor.v8's bytes other than by the currency sentences refreshed under D-294 Decision 3 (the subject must enumerate those sites and assert equality after normalizing them)
- any present-tense currency sentence anywhere in the subject names a superseded leftover-join version
- SATISFIES DR-117, opens Class A, or lifts D-137's reservation
- the contract.v8 relationship statement misstates D-116 / D-137 / D-207, or decides which artifact a Class A opening names (the record does not)
- any of the twelve joins cited at other than its current version, or its leftoverDesign partition misquoted (note g23 leftover-join.v8 flags no obligation leftoverDesign true)
- G13 named into required-now; fixture bytes or the DR-131 pack invented
- cited digests do not match; recordedInputs.HEAD is not live HEAD; requiredNowUnchanged is not 28; file08StatusToken is not DR-117's live leading label
- deictic or bare version tokens; claims contradicted by the bytes (e.g. "unchanged" for a rewritten field)
- subject moved; authorizes docs/v2/implementation/

ACCEPT only at 0 blockers and 0 SHOULD-FIX.
Final chat: ACCEPT or REJECT, then the grade ruling.
"""
pp=P(f'preview-product-boundary-successor.v{V}.review-prompt.md'); assert not os.path.exists(pp); open(pp,'w').write(prompt); os.chmod(pp,0o444)
dispatch=f"""Independent Stage A review of preview-product-boundary-successor.v{V} (DR-117). Refute, do not confirm.

Read {pp}
and execute it.

SUBJECT sha256 must be
{DS}
Mode 0444. If the subject moved, REJECT.

Write only your review JSON path from that prompt, including the top-level gradeRuling object the prompt defines.
Do not edit the subject. Do not commit. Do not edit file 08 or COORD. Do not read the other reviewer.
Final chat: ACCEPT or REJECT, then the grade ruling.
"""
dp=P(f'_dispatch.ppbs-v{V}.txt'); open(dp,'w').write(dispatch)
print('frozen',DST,DS); print('prompt',pp,sha(pp)); print('dispatch',dp,len(dispatch))
