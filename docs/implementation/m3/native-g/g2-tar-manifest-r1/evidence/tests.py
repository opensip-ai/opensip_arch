from pathlib import Path
p=Path('/tmp/opensip-implementation/g2-tar-manifest-authoring/product/providers/rust/src/dependency_inputs_tests.rs');p.write_text(p.read_text()+r'''

fn tar_manifest_check<'a>(f: &Fixture, ids: &Ids, index: usize, tar: &'a [u8]) -> Result<DeclaredTarManifest<'a>, DeclaredTarManifestError> {
    check_declared_tar_manifest(
        &RetainedInputs::new(schemas(), &f.objects, &f.blobs),
        &UniverseInputRequest { universe_digest: ids.u, context_digest: ids.c,
            expected_host_digest: ids.c, snapshot_id: &ids.snapshot,
            prepared_digest: ids.prepared, ownership_digest: ids.ownership },
        index, tar, WORK,
    )
}
fn manifest_test_tar(root: &str, path: &str, content: &[u8]) -> Vec<u8> {
    let mut tar=vec![];tar_test_entry(&mut tar,format!("{root}/{path}").as_bytes(),b'0',content);tar_test_end(&mut tar);tar
}
#[test]
fn declared_tar_manifest_matches_exact_borrowed_members_after_lock_join() {
    let mut f=one_locked_package();let ids=f.ids();let tar=manifest_test_tar("owned-1.0.0","src/lib.rs",b"member");
    let checked=tar_manifest_check(&f,&ids,0,&tar).unwrap();
    assert_eq!(checked.package_index(),0);assert_eq!(checked.lock_checks().lock_package_rows(),1);
    assert_eq!(checked.members()[0].path(),"src/lib.rs");assert_eq!(checked.members()[0].content(),b"member");
    assert_eq!(checked.members()[0].content().as_ptr(),tar[512..].as_ptr());
}
#[test]
fn declared_tar_manifest_uses_checked_tuple_not_a_caller_root_alias() {
    let mut f=one_locked_package();let ids=f.ids();
    for root in ["owned-1.0","other-1.0.0"] {
        let tar=manifest_test_tar(root,"src/lib.rs",b"member");
        assert!(matches!(tar_manifest_check(&f,&ids,0,&tar),Err(DeclaredTarManifestError::Tar(DeclaredTarError::Path))));
    }
}
#[test]
fn declared_tar_manifest_raw_hash_and_length_both_refuse_substitution() {
    let mut f=one_locked_package();let ids=f.ids();
    for (bytes,field) in [(b"forged".as_slice(),"contentSha256"),(b"short","byteLength")] {
        let tar=manifest_test_tar("owned-1.0.0","src/lib.rs",bytes);
        assert!(matches!(tar_manifest_check(&f,&ids,0,&tar),Err(DeclaredTarManifestError::Mismatch {field: actual}) if actual==field));
    }
}
#[test]
fn declared_tar_manifest_path_set_must_be_exact_no_extra_or_missing_rows() {
    let mut f=one_locked_package();let ids=f.ids();
    assert!(matches!(tar_manifest_check(&f,&ids,0,&vec![0;1024]),Err(DeclaredTarManifestError::Mismatch {field:"fileCount"})));
    let tar=manifest_test_tar("owned-1.0.0","different.rs",b"member");
    assert!(matches!(tar_manifest_check(&f,&ids,0,&tar),Err(DeclaredTarManifestError::Mismatch {field:"path"})));
    let mut tar=manifest_test_tar("owned-1.0.0","src/lib.rs",b"member");tar.truncate(tar.len()-1024);
    tar_test_entry(&mut tar,b"owned-1.0.0/extra.rs",b'0',b"extra");tar_test_end(&mut tar);
    assert!(matches!(tar_manifest_check(&f,&ids,0,&tar),Err(DeclaredTarManifestError::Mismatch {field:"fileCount"})));
}
#[test]
fn declared_tar_manifest_empty_retained_manifest_is_representable_without_completeness_authority() {
    let mut f=one_locked_package();let empty=package(&mut f,"owned",&JsonValue::Array(vec![]));packages(&mut f,vec![empty]);let ids=f.ids();
    let tar=vec![0;1024];assert!(tar_manifest_check(&f,&ids,0,&tar).unwrap().members().is_empty());
}
#[test]
fn declared_tar_manifest_invalid_ordinal_and_tar_never_bypass_mandatory_retention() {
    let mut f=one_locked_package();let ids=f.ids();
    assert!(matches!(tar_manifest_check(&f,&ids,1,b""),Err(DeclaredTarManifestError::SelectedPackage)));
    f.blobs.remove(&raw_sha256(b"member"));
    assert!(matches!(tar_manifest_check(&f,&ids,1,b""),Err(DeclaredTarManifestError::Lock(_))));
    assert!(matches!(tar_manifest_check(&f,&ids,0,b""),Err(DeclaredTarManifestError::Lock(_))));
}
#[test]
fn declared_tar_manifest_late_tar_refusal_cannot_publish_a_matching_prefix() {
    let mut f=one_locked_package();let ids=f.ids();let mut tar=manifest_test_tar("owned-1.0.0","src/lib.rs",b"member");let last=tar.len()-1;tar[last]=1;
    assert!(matches!(tar_manifest_check(&f,&ids,0,&tar),Err(DeclaredTarManifestError::Tar(DeclaredTarError::EndRegion))));
}
#[test]
fn declared_tar_manifest_unrelated_raw_crate_bytes_grant_no_inflation_join() {
    // A raw preimage can be retained, yet the manifest observation intentionally
    // takes independent declared inflated bytes; neither result proves inflation.
    let (mut f,sha)=crate_fixture(b"not gzip, merely hash-matched fixture");let ids=f.ids();
    assert_eq!(crate_check(&f,&ids,0,sha).unwrap().raw_bytes(),b"not gzip, merely hash-matched fixture");
    let tar=manifest_test_tar("owned-1.0.0","src/lib.rs",b"unadmitted extraction");
    assert_eq!(tar_manifest_check(&f,&ids,0,&tar).unwrap().members()[0].content(),b"unadmitted extraction");
}
''')
