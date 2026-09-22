from pathlib import Path
import json,hashlib,re,subprocess
T=Path('/tmp/opensip-implementation');D=T/'initial-diagnostics-generation404';P=D/'product';A=Path('/Users/sb/code/opensip-ai/opensip_arch');U=A/'docs/implementation/m2/initial-root-binding-owner-selection-v1'
p=P/'crates/identity/src/schema_registry.rs';s=p.read_text();pattern=r'(id: "urn:opensip:product-v1:workflows:evaluator3:common:4",\n        path: "schemas/sources/common-v4.schema.json",\n        bytes: )64866(,\n        sha256: \[)(.*?)(\n        \],)';m=re.search(pattern,s,re.S);assert m
raw=(P/'schemas/sources/common-v4.schema.json').read_bytes();digest=hashlib.sha256(raw).digest();assert bytes(int(n)for n in re.findall(r'\d+',m[3]))==bytes.fromhex('6af81f35c53ce74acbb0609d50524ab9d0b0ae1c2b772e9581dfb9f8535eaed9')
s=s[:m.start()]+m[1]+str(len(raw))+m[2]+'\n            '+', '.join(str(n)for n in digest)+','+m[4]+s[m.end():];p.write_text(s)
p=P/'crates/host/src/schema_sources.rs';s=p.read_text();marker='    #[test]\n    fn missing_extra_reordered_changed_and_truncated_sources_refuse()';assert s.count(marker)==1
new='''    #[test]
    fn initialization_details_are_current_only_and_unknown_codes_still_refuse() {
        use opensip_contracts::generated::evidence::{
            Common1DomainDetailCode, Common3DomainDetailCode, Common4DomainDetailCode,
        };
        let registry = embedded_schema_registry().unwrap();
        let current = "urn:opensip:product-v1:workflows:evaluator3:common:4";
        for code in [
            "INSTALLATION.DURABILITY_NOT_CHECKED",
            "INSTALLATION.NOT_INITIALIZED",
        ] {
            let raw = serde_json::to_vec(code).unwrap();
            assert!(registry.schema(current, "/$defs/DomainDetailCode").unwrap()
                .admit_json(&raw, 100_000).is_ok());
            assert!(serde_json::from_slice::<Common4DomainDetailCode>(&raw).is_ok());
            for historical in [
                "urn:opensip:product-v1:workflows:common",
                "urn:opensip:product-v1:workflows:evaluator3:common:3",
            ] {
                assert!(matches!(registry.schema(historical, "/$defs/DomainDetailCode").unwrap()
                    .admit_json(&raw, 100_000), Err(AdmissionError::Mismatch)));
            }
            assert!(serde_json::from_slice::<Common1DomainDetailCode>(&raw).is_err());
            assert!(serde_json::from_slice::<Common3DomainDetailCode>(&raw).is_err());
        }
        let unknown = br#""INSTALLATION.UNREGISTERED""#;
        assert!(matches!(registry.schema(current, "/$defs/DomainDetailCode").unwrap()
            .admit_json(unknown, 100_000), Err(AdmissionError::Mismatch)));
        assert!(serde_json::from_slice::<Common4DomainDetailCode>(unknown).is_err());
    }
'''
s=s.replace(marker,new+marker);p.write_text(s)
subprocess.run(['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024',str(P/'crates/identity/src/schema_registry.rs'),str(p)],check=True)
for rel in ['crates/identity/src/schema_registry.rs','crates/host/src/schema_sources.rs']:
 target=U/'product'/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((P/rel).read_bytes())
(U/'evidence/admission-pin-correction.md').write_text('''# Native admission pin correction

The first private admission test run failed22of23 tests with SourceBytes because RegisteredSchemas has its own compiled common4 SourcePin; updating the JSON admission registry alone does not update this trust binding. That refusal is correct. The candidate now explicitly changes only that common4 byte count/digest in crates/identity/src/schema_registry.rs and adds a host regression covering native schema admission and generated Rust enums: new details admitted in common4, refused in common1/common3, and unknown codes still refused. The complete source-set and corrupted-source refusal tests remain unchanged. No runtime self-rehash or fallback is introduced.

The original failing logs are retained. A fresh run is required before freezing. This was found by root native tests, not by the earlier compile-only check or Claude405's consumer audit.
''')
env=json.loads((D/'compile-environment.json').read_text());checks=[]
for name,args in [('admission-r2',['test','--locked','--offline','-p','opensip-host','--lib','schema_sources::']),('workspace-r2',['check','--locked','--offline','--workspace','--all-targets'])]:
 cmd=['/opt/homebrew/Cellar/rust/1.95.0/bin/cargo',*args]
 with (D/(name+'.stdout')).open('wb')as out,(D/(name+'.stderr')).open('wb')as err:r=subprocess.run(cmd,cwd=P,env=env,stdout=out,stderr=err)
 checks.append({'name':name,'command':cmd,'exitCode':r.returncode});(D/'admission-r2-checks.json').write_text(json.dumps(checks,indent=2)+'\n');print(name,r.returncode,flush=True);assert r.returncode==0
