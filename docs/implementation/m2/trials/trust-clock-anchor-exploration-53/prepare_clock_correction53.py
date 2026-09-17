from pathlib import Path
import json,hashlib,shutil
A=Path('/Users/sb/code/opensip-ai/opensip_arch');T=Path('/tmp/opensip-implementation/m2-trust-clock-exploration-53');assert not T.exists();T.mkdir();manifest=A/'docs/coop/design-corrections/reviews/candidate-subject.v45.json';assert hashlib.sha256(manifest.read_bytes()).hexdigest()=='8b4efbb04d9e25126ec7955931cf364f7013b3710a45c48bae8bc563a0c82155';pins={r['path']:r for r in json.loads(manifest.read_bytes())['files']}
names=['docs/coop/design-corrections/security/security_lifecycle_model_v1.py','docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json','docs/coop/design-corrections/security/trust-clock-cases.v1.json','docs/coop/design-corrections/foundation/canonical.py','docs/coop/design-corrections/discovery-defaults.py','docs/v2/contracts/product-v1/security-and-lifecycle.md']
for name in names:
 raw=(A/name).read_bytes();r=pins[name];assert(len(raw),hashlib.sha256(raw).hexdigest())==(r['bytes'],r['sha256'])
 for lane in ['parent','candidate']:
  p=T/lane/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
(T/'parent-inputs.json').write_text(json.dumps({'sourceManifest':{'path':str(manifest.relative_to(A)),'sha256':hashlib.sha256(manifest.read_bytes()).hexdigest()},'files':[pins[n]for n in names]},indent=2)+'\n')
p=T/'candidate'/names[0];s=p.read_text();old='''    continuity = {'available': False}
    excused = False
    if anchor is not None and anchor.get('bootId') == boot:
        if not _int(anchor.get('mono')) or mono < anchor['mono']:
            findings.append''';new='''    continuity = {'available': False}
    excused = False
    malformed_continuity = False
    if anchor is not None and anchor.get('bootId') == boot:
        if not _int(anchor.get('mono')) or mono < anchor['mono']:
            malformed_continuity = True
            findings.append''';assert s.count(old)==1;s=s.replace(old,new);old="    if not continuity.get('available') or abs(continuity['deviationSeconds']) <= SESSION_DEVIATION_TOLERANCE_S or excused:";assert s.count(old)==1;s=s.replace(old,"    if not malformed_continuity and (not continuity.get('available') or abs(continuity['deviationSeconds']) <= SESSION_DEVIATION_TOLERANCE_S or excused):");p.write_text(s)
p=T/'candidate'/names[-1];s=p.read_text();old='''   anchor is rewritten when continuity is unavailable, within tolerance, or
   excused by a witness.''';new='''   anchor is rewritten when continuity is unavailable because no same-boot
   anchor exists, within tolerance, or excused by a witness. Malformed
   same-boot continuity preserves the existing anchor, including when a
   payload is presented; it does not suppress the independently required
   floor or lastAccepted update.''';assert s.count(old)==1;p.write_text(s.replace(old,new))
(T/'README.md').write_text('Unaccepted trust-clock correction exploration53. Selected contract S4 step3 explicitly preserves the anchor when same-boot monotonic time regresses, but step5 broadly says unavailable continuity rewrites; selected model rewrites the malformed anchor. Proposed minimal correction preserves malformed same-boot anchors while retaining required floor/lastAccepted updates, findings, expiry and refusal/report-only rules. No product implementation, selected contract/source mutation or actual reviewer approval. All six parent inputs pinned to accepted candidate45. Future independent Grok review and formal successor selection required.\n')
print(str(T))
