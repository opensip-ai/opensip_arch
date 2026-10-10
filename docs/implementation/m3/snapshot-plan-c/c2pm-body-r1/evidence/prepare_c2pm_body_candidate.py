from pathlib import Path
import json,hashlib,shutil,subprocess
P=Path('/Users/sb/code/opensip-ai/opensip-c2pm-body');A=P.parent/'opensip_arch';S=Path('/tmp/opensip-implementation/c2pm-body-generation');S.mkdir()
schema='tools/security/inputs/manifest-schema.json';source=A/'docs/implementation/m3/snapshot-plan-c/c2pm-1-r2/completion/manifest-schema.completed.v1.json'
old=json.loads((P/schema).read_text());new=json.loads(source.read_text());diff=dict(new);props=dict(diff['properties']);assert props.pop('closureProtocolMajor')==dict(type='integer',minimum=1,maximum=9223372036854775807);diff['properties']=props;assert diff==old
shutil.copyfile(source,P/schema)
pins=P/'tools/security/inputs/sources.json';j=json.loads(pins.read_text());row=next(r for r in j['files'] if r['path']==schema);raw=source.read_bytes();row.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest());pins.write_text(json.dumps(j,indent=2)+'\n')
(S/'inputs').mkdir();shutil.copyfile(source,S/'inputs/manifest-schema.json');(S/'product/crates/security/src').mkdir(parents=True)
out=subprocess.check_output(['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B',str(P/'tools/security/generators/manifest_shape.py'),str(S)])
shutil.copyfile(S/'product/crates/security/src/component_manifest_shape.rs',P/'crates/security/src/generated/component_manifest_shape.rs')
f=P/'crates/security/src/component_manifest.rs';t=f.read_text();assert t.count('    Compatibility,')==1;t=t.replace('    Compatibility,','    Compatibility,\n    ClosureProtocolMismatch,')
needle='''    let mut exceptions = BTreeMap::new();'''
assert t.count(needle)==1;t=t.replace(needle,'''    // C2PM-1 present declaration consistency is shared by both body readers.
    // Absence stays valid for ordinary M2 validation; no closure is projected here.
    if analyzer
        && m.get("closureProtocolMajor")
            .is_some_and(|major| major != &compat["providerProtocol"])
    {
        return Err(Error::ClosureProtocolMismatch);
    }
'''+needle)
i=t.index('    const CR1_ROLES:')
tests='''    #[test]
    fn c2pm_body_presence_is_optional_and_not_projection_admission() {
        let context = Context::default();
        for role in ["analyzer", "toolchain", "stdlib", "rust-dev-llvm", "grammar"] {
            let mut body = cr1_body(role);
            let absent = opensip_identity::canonical_bytes(&body).unwrap();
            assert!(validate(&absent, &context).is_ok());
            assert!(validate_inventory(&absent, &context.reserved_names).is_ok());
            let major = if role == "analyzer" {
                object(&object(&body)["compatibility"])["providerProtocol"].clone()
            } else {
                V::Integer(opensip_identity::JsonInteger::new(1).unwrap())
            };
            cr1_object(&mut body).insert("closureProtocolMajor".into(), major);
            let present = opensip_identity::canonical_bytes(&body).unwrap();
            assert!(validate(&present, &context).is_ok());
            assert!(validate_inventory(&present, &context.reserved_names).is_ok());
        }
    }
    #[test]
    fn c2pm_analyzer_mismatch_is_distinct_in_both_readers() {
        let context = Context::default();
        let mut body = cr1_body("analyzer");
        let existing = int(&object(&object(&body)["compatibility"])["providerProtocol"]);
        let different = if existing == 1 { 2 } else { 1 };
        cr1_object(&mut body).insert("closureProtocolMajor".into(),
            V::Integer(opensip_identity::JsonInteger::new(different).unwrap()));
        let raw = opensip_identity::canonical_bytes(&body).unwrap();
        assert!(matches!(validate(&raw, &context), Err(Error::ClosureProtocolMismatch)));
        assert!(matches!(validate_inventory(&raw, &context.reserved_names), Err(Error::ClosureProtocolMismatch)));
        cr1_object(&mut body).remove("closureProtocolMajor");
        let compat = cr1_object(cr1_object(&mut body).get_mut("compatibility").unwrap());
        compat.insert("manifest".into(), V::Integer(opensip_identity::JsonInteger::new(2).unwrap()));
        let raw = opensip_identity::canonical_bytes(&body).unwrap();
        assert!(matches!(validate(&raw, &context), Err(Error::Compatibility)));
        assert!(matches!(validate_inventory(&raw, &context.reserved_names), Err(Error::Compatibility)));
    }
    #[test]
    fn c2pm_raw_integer_spelling_and_closed_root() {
        let context = Context::default();
        let baseline = opensip_identity::canonical_bytes(&cr1_body("toolchain")).unwrap();
        for (literal, parse_error) in [
            ("1.0", true), ("1e0", true), ("10e-1", true),
            ("true", false), ("null", false), ("\\"1\\"", false),
            ("0", false), ("-1", false), ("9223372036854775808", true),
        ] {
            let raw = format!("{{\\"closureProtocolMajor\\":{literal},{}", std::str::from_utf8(&baseline[1..]).unwrap());
            let host = validate(raw.as_bytes(), &context);
            let inventory = validate_inventory(raw.as_bytes(), &context.reserved_names);
            if parse_error {
                assert!(matches!(host, Err(Error::Parse)), "{literal}");
                assert!(matches!(inventory, Err(Error::Parse)), "{literal}");
            } else {
                assert!(matches!(host, Err(Error::Schema)), "{literal}");
                assert!(matches!(inventory, Err(Error::Schema)), "{literal}");
            }
        }
        let max = format!("{{\\"closureProtocolMajor\\":9223372036854775807,{}", std::str::from_utf8(&baseline[1..]).unwrap());
        assert!(validate(max.as_bytes(), &context).is_ok());
        assert!(validate_inventory(max.as_bytes(), &context.reserved_names).is_ok());
        let unknown = format!("{{\\"closureProtocolMajor\\":1,\\"extraMajor\\":1,{}", std::str::from_utf8(&baseline[1..]).unwrap());
        assert!(matches!(validate(unknown.as_bytes(), &context), Err(Error::Schema)));
        assert!(matches!(validate_inventory(unknown.as_bytes(), &context.reserved_names), Err(Error::Schema)));
    }
'''
t=t[:i]+tests+t[i:];f.write_text(t)
print(out.decode().strip(),'candidate shared body validation prepared; no admission projection or public mapper')
