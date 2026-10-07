from pathlib import Path
b=Path('/tmp/opensip-implementation/component-role-materialization-authoring');p=b/'product/crates/security/src/component_manifest.rs';s=p.read_text();at=s.index('    #[test]\n    fn generated_closed_schema_matches_entire_exact_schema_oracle()')
t='''    fn cr1_object(v: &mut V) -> &mut BTreeMap<String,V> {
        let V::Object(m)=v else {panic!()}; m
    }
    fn cr1_baseline() -> V {
        let line=include_bytes!("../tests/fixtures/manifest268-semantic.ndjson").split(|b| *b==b'\\n').find(|b| !b.is_empty()).unwrap();
        let q=crate::trust::metadata::parse(line).unwrap();
        assert_eq!(text(&object(&q)["label"]),"POS/full-security");
        crate::trust::metadata::parse(&bytes(&object(&q)["raw"])).unwrap()
    }
    fn cr1_body(role: &str) -> V {
        let mut v=cr1_baseline(); let m=cr1_object(&mut v);
        m.insert("role".into(),V::String(role.into()));
        if role != "analyzer" {
            m.remove("commands");
            m.insert("capabilities".into(),V::Array(vec![]));
            m.insert("permissions".into(),V::Array(vec![]));
        }
        v
    }
    fn cr1_validate(v: &V,c: &Context) -> Result<Validated,Error> {
        validate(&opensip_identity::canonical_bytes(v).unwrap(),c)
    }
    const CR1_ROLES: [&str;4]=["toolchain","stdlib","rust-dev-llvm","grammar"];
    #[test]
    fn cr1_exact_role_table_and_unknown_roles() {
        let c=Context::default();
        assert_eq!(cr1_validate(&cr1_body("analyzer"),&c).unwrap().closure_kind(),"provider");
        for role in CR1_ROLES {
            let v=cr1_body(role); assert!(!object(&v).contains_key("commands"));
            assert_eq!(cr1_validate(&v,&c).unwrap().closure_kind(),role);
        }
        for role in ["builder","evaluator","detector","adapter","core"] {
            assert!(matches!(cr1_validate(&cr1_body(role),&c),Err(Error::Schema)));
        }
    }
    #[test]
    fn cr1_closure_commands_are_absent_and_analyzer_commands_required() {
        let c=Context::default();
        let commands=object(&cr1_baseline())["commands"].clone();
        for role in CR1_ROLES {
            for member in [commands.clone(),V::Array(vec![]),V::Null] {
                let mut v=cr1_body(role); cr1_object(&mut v).insert("commands".into(),member);
                assert!(matches!(cr1_validate(&v,&c),Err(Error::Schema)));
            }
        }
        for member in [None,Some(V::Array(vec![])),Some(V::Null)] {
            let mut v=cr1_body("analyzer"); let m=cr1_object(&mut v);m.remove("commands");
            if let Some(member)=member {m.insert("commands".into(),member);}
            assert!(matches!(cr1_validate(&v,&c),Err(Error::Schema)));
        }
    }
    #[test]
    fn cr1_closure_capabilities_and_permissions_refuse_existing_codes() {
        let c=Context::default(); let baseline=cr1_baseline();
        for role in CR1_ROLES {
            let mut v=cr1_body(role);cr1_object(&mut v).insert("capabilities".into(),object(&baseline)["capabilities"].clone());
            assert!(matches!(cr1_validate(&v,&c),Err(Error::Capability)));
            let mut v=cr1_body(role);cr1_object(&mut v).insert("permissions".into(),object(&baseline)["permissions"].clone());
            assert!(!array(&object(&v)["permissions"]).is_empty());
            assert!(matches!(cr1_validate(&v,&c),Err(Error::Permission)));
        }
    }
    fn cr1_entry(v: &mut V,entry: &str) {
        let V::Array(platforms)=cr1_object(v).get_mut("platforms").unwrap() else {panic!()};
        for p in platforms {cr1_object(p).insert("entrypoint".into(),V::String(entry.into()));}
    }
    #[test]
    fn cr1_entrypoint_regular_file_and_analyzer_execution_rule() {
        let c=Context::default();
        for role in CR1_ROLES {
            let mut v=cr1_body(role);cr1_entry(&mut v,"lib/provider.js");
            assert!(cr1_validate(&v,&c).is_ok());
            cr1_entry(&mut v,"lib");assert!(matches!(cr1_validate(&v,&c),Err(Error::Path)));
        }
        let mut v=cr1_body("analyzer");cr1_entry(&mut v,"lib/provider.js");
        assert!(matches!(cr1_validate(&v,&c),Err(Error::Path)));
        cr1_entry(&mut v,"lib");assert!(matches!(cr1_validate(&v,&c),Err(Error::Path)));
    }
    #[test]
    fn cr1_manifest_name_and_alias_custody_remains_for_every_role() {
        for role in ["analyzer","toolchain","stdlib","rust-dev-llvm","grammar"] {
            let mut v=cr1_body(role);cr1_object(&mut v).insert("aliases".into(),V::Array(vec![V::String("role-alias".into())]));
            assert!(cr1_validate(&v,&Context::default()).is_ok());
            for name in ["typescript-analyzer","role-alias"] {
                let mut c=Context::default();c.reserved_names.insert(name.into());
                assert!(matches!(cr1_validate(&v,&c),Err(Error::Command)));
                assert!(matches!(validate_inventory(&opensip_identity::canonical_bytes(&v).unwrap(),&c.reserved_names),Err(Error::Command)));
                c.reserved_names.clear();
                c.live_names.push(LiveName{stable_id:"another-component".into(),provenance:object(&v)["provenance"].clone(),names:BTreeSet::from([name.into()])});
                assert!(matches!(cr1_validate(&v,&c),Err(Error::Command)));
                // Inventory validity has no live host namespace authority.
                assert!(validate_inventory(&opensip_identity::canonical_bytes(&v).unwrap(),&BTreeSet::new()).is_ok());
                c.live_names[0].stable_id=text(&object(&v)["stableId"]).into();
                assert!(cr1_validate(&v,&c).is_ok());
            }
            cr1_object(&mut v).insert("aliases".into(),V::Array(vec![V::String("typescript-analyzer".into())]));
            assert!(matches!(cr1_validate(&v,&Context::default()),Err(Error::Command)));
        }
    }
'''
s=s[:at]+t+s[at:];p.write_text(s);print('five new semantic controls appended; symlink control pending')
