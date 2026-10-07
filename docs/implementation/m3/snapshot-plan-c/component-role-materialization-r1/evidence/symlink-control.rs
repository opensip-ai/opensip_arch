    #[test]
    fn cr1_closure_symlink_entrypoint_refuses_but_analyzer_resolution_remains() {
        for role in ["analyzer","toolchain","stdlib","rust-dev-llvm","grammar"] {
            let mut v=cr1_body(role);
            let V::Array(platforms)=cr1_object(&mut v).get_mut("platforms").unwrap() else {panic!()};
            for p in platforms {
                let m=cr1_object(p);m.insert("entrypoint".into(),V::String("bin/link".into()));
                let tree=cr1_object(m.get_mut("tree").unwrap());
                let V::Array(entries)=tree.get_mut("entries").unwrap() else {panic!()};
                entries.push(V::Object(BTreeMap::from([
                    ("path".into(),V::String("bin/link".into())),
                    ("type".into(),V::String("symlink".into())),
                    ("mode".into(),V::String("0755".into())),
                    ("target".into(),V::String("entry".into()))])));
            }
            let got=cr1_validate(&v,&Context::default());
            if role=="analyzer" { assert!(got.is_ok(),"{:?}",got.err()); }
            else { assert!(matches!(got,Err(Error::Path))); }
        }
    }
