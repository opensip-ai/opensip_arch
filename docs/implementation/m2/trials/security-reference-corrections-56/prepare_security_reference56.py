from pathlib import Path
import json,hashlib
A=Path('/Users/sb/code/opensip-ai/opensip_arch');T=Path('/tmp/opensip-implementation');S=T/'m2-trust-clock-exploration-53';D=T/'m2-security-reference-corrections-56';assert not D.exists();D.mkdir();pins=json.loads((S/'parent-inputs.json').read_bytes());manifest=json.loads((A/'docs/coop/design-corrections/reviews/candidate-subject.v45.json').read_bytes());selected={r['path']:r for r in manifest['files']}
names=[r['path']for r in pins['files']]+['docs/coop/completion/security_unit_lib_v8.py','docs/coop/completion/security-completion.v8.md','docs/coop/design-corrections/security/root-schema-cases.v1.json'];rows=[]
for name in names:
 r=selected[name];raw=(A/name).read_bytes();assert(len(raw),hashlib.sha256(raw).hexdigest())==(r['bytes'],r['sha256']);rows.append(r)
 for lane in ['parent','candidate']:
  p=D/lane/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
for name in ['docs/coop/design-corrections/security/security_lifecycle_model_v1.py','docs/v2/contracts/product-v1/security-and-lifecycle.md']:(D/'candidate'/name).write_bytes((S/'candidate'/name).read_bytes())
p=D/'candidate/docs/coop/design-corrections/security/security_lifecycle_model_v1.py';s=p.read_text();old="    dt = datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)\n    return int(dt.timestamp())";new="    try:\n        dt = datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)\n        return int(dt.timestamp())\n    except (ValueError, OverflowError) as exc:\n        raise Reject('TIMESTAMP_GRAMMAR:%r' % (s,)) from exc";assert s.count(old)==1;s=s.replace(old,new);old="'revocation': ('revocation v8', 'opensip.metadata.revocation.1', 'TR-INDEX keys@threshold')";new="'revocation': ('revocation v8', 'opensip.metadata.revocation.1', 'ROOT keys@rootThreshold')";assert s.count(old)==1;p.write_text(s.replace(old,new))
p=D/'candidate/docs/v2/contracts/product-v1/security-and-lifecycle.md';s=p.read_text();old='''are closed: `root` (body RootV1|RootV2, domain by `rootSchema`), `catalog` and
`revocation` (v8 bodies, TR-INDEX), `trust-recovery-epoch` (S4.5,''';new='''are closed: `root` (body RootV1|RootV2, domain by `rootSchema`), `catalog`
(v8 body, TR-INDEX), `revocation` (v8 body, ROOT), `trust-recovery-epoch` (S4.5,''';assert s.count(old)==1;s=s.replace(old,new);marker='## S4. Trust time (AR-04)\n';assert s.count(marker)==1;s=s.replace(marker,marker+'''
Timestamp inputs require a valid calendar date and time under the fixed
`YYYY-MM-DDTHH:MM:SSZ` grammar (years 0001–9999 and seconds 00–59).
A pattern-shaped but invalid date, such as February 31, receives the owning
typed timestamp refusal; it must not escape as a calendar-parser exception.
This requirement applies to the shared timestamp reader used by root and
lifecycle admission as well as trust-clock inputs.
''');p.write_text(s)
(D/'parent-inputs.json').write_text(json.dumps({'standing':'All nine parents pinned to accepted candidate45. Candidate subsumes UNACCEPTED clock53 plus two additional corrections; no selected source is changed.','sourceManifest':pins['sourceManifest'],'files':rows},indent=2)+'\n');(D/'original-probes.json').write_bytes((T/'security-reference-probes56.json').read_bytes());(D/'README.md').write_text('Unaccepted security-reference correction56, subsuming unaccepted clock53. Three issues: malformed same-boot monotonic anchor preservation; revocation authority drift(TR-INDEX in S9 versus retainedROOT routing, proposedpreserveROOT); invalid calendar timestamps escaping asValueError from sharedts/rootadmission. Only candidatecontract/model change. Rootdate16probes all reproduceuncaughtValueError in selectedparent. Signatureverification/signers/rootkeyIDbinding are NOT qualified by the role/schema model; root-schema fixtures contain synthetic keys and cannot substitute for full retainedv8 keybinding and actualcrypto verification. No producttrustauthority, independentreview orselectionclaimed.\n');print(D)
