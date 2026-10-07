from pathlib import Path
b=Path('/tmp/opensip-implementation/core-role-derivations-authoring');p=b/'product/crates/security/src/trust/core_inventory.rs';s=p.read_text();assert 'detector_closure: String' not in s
s=s.replace('    evaluator_closure: String,','    evaluator_closure: String,\n    detector_closure: String,\n    provider_closure: String,\n    adapter_closure: String,',1)
pos='    pub(super) fn files(&self)'
addition='''    /// CRC-1 identities only. Projection itself supplies no authentication
    /// or permission to use these identities in a Plan or producer field.
    pub(super) fn detector_closure(&self) -> &str { &self.detector_closure }
    pub(super) fn provider_closure(&self) -> &str { &self.provider_closure }
    pub(super) fn adapter_closure(&self) -> &str { &self.adapter_closure }
'''
s=s.replace(pos,addition+pos,1)
s=s.replace('    let evaluator_closure = closure_id(&evaluator_descriptor(&descriptor))?;','''    let evaluator_closure = closure_id(&evaluator_descriptor(&descriptor))?;
    let detector_closure = closure_id(&role_descriptor(&descriptor, CoreRole::Detector))?;
    let provider_closure = closure_id(&role_descriptor(&descriptor, CoreRole::Provider))?;
    let adapter_closure = closure_id(&role_descriptor(&descriptor, CoreRole::Adapter))?;''',1)
s=s.replace('        evaluator_closure,\n        files:', '        evaluator_closure,\n        detector_closure,\n        provider_closure,\n        adapter_closure,\n        files:',1)
s=s.replace('#[cfg(test)]\nmod tests {','''// CRC-1's closed core recipes. The caller cannot choose a manifest role or
// arbitrary kind. Every member except kind is the original core projection.
#[derive(Clone, Copy)]
enum CoreRole { Detector, Provider, Adapter }
fn role_descriptor(core: &V, role: CoreRole) -> V {
    let mut descriptor = core.clone();
    let V::Object(members) = &mut descriptor else { unreachable!("core descriptor") };
    let kind = match role {
        CoreRole::Detector => "detector",
        CoreRole::Provider => "provider",
        CoreRole::Adapter => "adapter",
    };
    members.insert("kind".into(), V::String(kind.into()));
    descriptor
}
#[cfg(test)]
mod tests {''',1)
tests='''    fn crc1_roles(p: &Projection) -> [(CoreRole, &str, &str); 3] {
        [(CoreRole::Detector, "detector", p.detector_closure()),
         (CoreRole::Provider, "provider", p.provider_closure()),
         (CoreRole::Adapter, "adapter", p.adapter_closure())]
    }
    #[test]
    fn crc1_vector_core_role_closures() {
        let (raw, platform) = baseline();
        let p = project(&raw, &platform).unwrap();
        let vectors = [
            ("closure2:be7bd6cc99990375edfc652b38f48fa5c51677970849b1dca3282245b0503c66", "b795a299770cbfd0386ef6d18f878851f9bc9841236a78515706dbadec897cf7"),
            ("closure2:df5e7cbab37c1ebccf867d343eaeb5d2739103492896e87d238a80efa1b8e662", "5b1ca657e61d56880cabad039d073a720fd75fbedc1f47ba923a6269f7e93a04"),
            ("closure2:670d260fd9956436fe1ef014d14ca18fb923e223f9a7f514a6fe4043fe36a0bf", "9c60b40d0020471ed6880659288854bcb7c9e5a727717dec1821402ad4e7e4d7"),
        ];
        assert_eq!(raw.len(), 5990);
        for ((role, kind, id), (expected_id, expected_sha)) in crc1_roles(&p).into_iter().zip(vectors) {
            let d = role_descriptor(p.descriptor(), role);
            assert_eq!(id, expected_id);
            assert_eq!(digest_hex(&raw_sha256(&canonical_bytes(&d).unwrap())), expected_sha);
            assert_eq!(object(&d)["kind"], V::String(kind.into()));
            assert_eq!(object(&d)["manifestDigest"], V::String("1d012c7d606524c238109dd4c1882b431e27325d57636f9a09099ec3cf98ac5d".into()));
        }
    }
    #[test]
    fn crc1_all_accepted_inventory_cases_preserve_members_and_distinct_ids() {
        let mut accepted = 0;
        for line in include_bytes!("../../tests/fixtures/core-inventory318.ndjson").split(|b| *b == b'\\n').filter(|b| !b.is_empty()) {
            let value = parse_json(line).unwrap(); let q = object(&value);
            let raw = if let Some(v) = q.get("rawRepeat") { let r=object(v); vec![number(&r["byte"]) as u8; number(&r["count"]) as usize] } else { bytes(&q["raw"]) };
            let Ok(p) = project(&raw, text(&q["platform"])) else { continue; };
            accepted += 1;
            let mut ids = BTreeSet::from([p.closure(), p.evaluator_closure()]);
            for (role, _, id) in crc1_roles(&p) {
                let mut d = role_descriptor(p.descriptor(), role);
                assert_eq!(closure_id(&d).unwrap(), id);
                assert!(ids.insert(id));
                let V::Object(m) = &mut d else { panic!() };
                m.insert("kind".into(), V::String("core".into()));
                assert_eq!(&d, p.descriptor());
                assert_eq!(object(&d)["manifestDigest"], V::String(digest_hex(&raw_sha256(&raw))));
            }
            assert_eq!(ids.len(),5);
        }
        assert_eq!(accepted,53);
    }
    #[test]
    fn crc1_v3_role_ids_bind_selected_platform_and_raw_body() {
        let (raw, platform) = baseline();
        let raw = v3(&raw, |_, _| {});
        let p = project_v3(&raw, &platform).unwrap();
        let inv=parse_json(&raw).unwrap();
        let other=text(&object(&array(&object(&inv)["platforms"])[0])["platform"]);
        assert_ne!(other, platform);
        let other_p=project_v3(&raw,other).unwrap();
        let mut spaced=raw.clone(); spaced.push(b' ');
        assert!(matches!(project_v3(&spaced,&platform), Err(Error::Shape(shapes::Error::NonCanonical))));
        let mut changed=inv.clone(); let V::Object(m)=&mut changed else {panic!()};
        m.insert("semanticVersion".into(),V::String("1.0.1".into()));
        let changed_raw=canonical_bytes(&changed).unwrap();
        let changed_p=project_v3(&changed_raw,&platform).unwrap();
        for (((role, _, id), (_, _, other_id)), (_, _, changed_id)) in crc1_roles(p.core()).into_iter().zip(crc1_roles(other_p.core())).zip(crc1_roles(changed_p.core())) {
            assert_ne!(id, other_id); assert_ne!(id, changed_id);
            let d=role_descriptor(p.core().descriptor(),role);
            assert_eq!(object(&d)["platform"],V::String(platform.clone()));
            assert_eq!(object(&d)["manifestDigest"],V::String(digest_hex(&raw_sha256(&raw))));
            assert_eq!(object(&d)["tree"], object(p.core().descriptor())["tree"]);
        }
    }
'''
s=s.replace('    #[test]\n    fn v3_projects_both_release_members_of_the_selected_row()',tests+'    #[test]\n    fn v3_projects_both_release_members_of_the_selected_row()',1);p.write_text(s)
p=b/'product/crates/security/src/trust/initial_core.rs';s=p.read_text();marker='    pub(crate) fn platform(&self)'
a='''    /// CRC-1: identities from the already authenticated core inventory.
    /// These accessors do not grant field-use or semanticClosures admission.
'''
for role in ['detector','provider','adapter']:
 a+=f'    pub(crate) fn {role}_closure(&self) -> &str {{\n        self.release.authentication().core().inventory().{role}_closure()\n    }}\n'
s=s.replace(marker,a+marker,1);p.write_text(s)
p=b/'product/crates/security/src/trust/initial_core_tests.rs';s=p.read_text();marker='#[test]\nfn a_signed_tree_yields_the_closure_k_and_a_rechecked_receipt()'
t='''#[test]
fn crc1_authenticated_initial_core_exposes_the_same_selected_role_ids() {
    let tree = Tree::new("crc1-positive", &spec(), None);
    let release = tree.release(STANDARD.0, STANDARD.1);
    let (core, _) = produce(&release, &tree.exe(), 0x0001_0301 | 0x4);
    let core = core.unwrap();
    let projection = Core::project_v3(&tree.signed.inventory, platform()).unwrap();
    let p=projection.core();
    assert_eq!(core.detector_closure(),p.detector_closure());
    assert_eq!(core.provider_closure(),p.provider_closure());
    assert_eq!(core.adapter_closure(),p.adapter_closure());
    assert_eq!(core.evaluator_closure(),p.evaluator_closure());
    assert_eq!(BTreeSet::from([core.closure(),core.evaluator_closure(),core.detector_closure(),core.provider_closure(),core.adapter_closure()]).len(),5);
}

'''
# Use existing test imports, explicit fully-qualified set avoids new import authority.
t=t.replace('BTreeSet::from','std::collections::BTreeSet::from');s=s.replace(marker,t+marker,1);p.write_text(s)
print('authored three existing files; four new controls')
