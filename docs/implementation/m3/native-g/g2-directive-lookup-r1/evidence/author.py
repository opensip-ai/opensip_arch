from pathlib import Path
b=Path('/tmp/opensip-implementation/g2-directive-lookup-authoring');p=Path('/Users/sb/code/opensip-ai/opensip/providers/rust/src');s=(p/'prepared_inputs.rs').read_text();assert 'lookup_declared_build_script_directives' not in s
new='''/// Inert declared directive output, not admitted cfg or environment settings.
#[derive(Debug)]
pub enum DeclaredBuildScriptDirectives {
    Missing,
    Bytes(std::sync::Arc<[u8]>),
}
#[derive(Debug)]
pub enum DirectiveLookupError {
    Prepared(PreparedInputError),
    Ambiguous,
}
impl From<PreparedInputError> for DirectiveLookupError {
    fn from(value: PreparedInputError) -> Self { Self::Prepared(value) }
}

/// Observe retained directive bytes for an exact owner after whole-set checks.
/// PO-2 failed build-script owners supply no directive bytes, irrespective of
/// row order. Only ok build-script-directives rows match. Multiple matching ok
/// rows are a local ambiguity error, never an implicit concatenation or priority.
/// Bytes remain uninterpreted: no directive parser, cfg/env application, Cargo
/// execution, faithful producer, owner/context/import admission, fallback or
/// worker authority is supplied by this observation.
pub fn lookup_declared_build_script_directives(
    inputs: &RetainedInputs<'_>,
    request: &PreparedInputRequest<'_>,
    owner_key: &str,
    schema_work: usize,
) -> Result<DeclaredBuildScriptDirectives, DirectiveLookupError> {
    check_declared_prepared_inputs(inputs, request, schema_work)
        .map_err(DirectiveLookupError::Prepared)?;
    let Some(prepared_digest) = request.universe.prepared_digest else {
        return Ok(DeclaredBuildScriptDirectives::Missing);
    };
    let frame = inputs.frame_candidate(prepared_digest, NativeFrameSet::Nested, schema_work)
        .map_err(PreparedInputError::Frame)?;
    let rows = array(field(map(frame.descriptor())?, "rows")?)?;
    for row in rows {
        let row = map(row)?;
        if text(field(row, "ownerKey")?)? == owner_key
            && text(field(row, "kind")?)? == "build-script-directives"
            && text(field(row, "status")?)? == "failed" {
            return Ok(DeclaredBuildScriptDirectives::Missing);
        }
    }
    let mut selected = None;
    for row in rows {
        let row = map(row)?;
        if text(field(row, "ownerKey")?)? != owner_key
            || text(field(row, "kind")?)? != "build-script-directives"
            || text(field(row, "status")?)? != "ok" { continue; }
        if selected.is_some() { return Err(DirectiveLookupError::Ambiguous); }
        selected = Some(digest(field(map(field(row, "blob")?)?, "sha256")?)?);
    }
    match selected {
        Some(sha) => Ok(DeclaredBuildScriptDirectives::Bytes(std::sync::Arc::from(
            inputs.blob(sha).map_err(PreparedInputError::Retained)?.bytes()))),
        None => Ok(DeclaredBuildScriptDirectives::Missing),
    }
}

'''
(b/'prepared_inputs.rs').write_text(s.replace('fn inert_media(',new+'fn inert_media('))
tests='''
fn directive_lookup(f: &Fixture, ids: &Ids, owner: &str) -> Result<DeclaredBuildScriptDirectives, DirectiveLookupError> {
    lookup_declared_build_script_directives(
        &RetainedInputs::new(schemas(), &f.objects, &f.blobs),
        &PreparedInputRequest {
            universe: UniverseInputRequest {
                universe_digest: ids.u, context_digest: ids.c,
                expected_host_digest: ids.c, snapshot_id: &ids.snapshot,
                prepared_digest: ids.prepared, ownership_digest: ids.ownership,
            }, owner_manifests: &owners(),
        }, owner, WORK,
    )
}
#[test]
fn directive_lookup_retains_exact_uninterpreted_owned_bytes() {
    let mut f = prepared();
    let raw = b"cargo:rustc-cfg=custom\\ncargo:rustc-env=KEY=value\\n\\xff\\0";
    let row = output(&mut f, "build-script-directives", "text/x-cargo-directives", raw);
    set_rows(&mut f, vec![row]);
    let ids = f.ids();
    let DeclaredBuildScriptDirectives::Bytes(bytes) = directive_lookup(&f, &ids, "owned").unwrap() else { panic!("directives"); };
    f.blobs.insert(raw_sha256(raw), b"replacement".to_vec()); drop(f);
    assert_eq!(&*bytes, raw);
}
#[test]
fn directive_lookup_owner_and_kind_are_exact() {
    let mut f = prepared();
    let row = output(&mut f, "build-script-directives", "text/x-cargo-directives", b"captured");
    let other = expansion_row(&mut f, b"expansion");
    set_rows(&mut f, vec![row, other]); let ids = f.ids();
    for owner in ["", "own", "owned-more", "Owned"] {
        assert!(matches!(directive_lookup(&f, &ids, owner).unwrap(), DeclaredBuildScriptDirectives::Missing));
    }
    let mut f = prepared(); let row = expansion_row(&mut f, b"expansion");
    set_rows(&mut f, vec![row]); let ids = f.ids();
    assert!(matches!(directive_lookup(&f, &ids, "owned").unwrap(), DeclaredBuildScriptDirectives::Missing));
}
#[test]
fn directive_lookup_failed_owner_dominates_ok_rows_in_either_order() {
    for reverse in [false, true] {
        let mut f = prepared();
        let ok = output(&mut f, "build-script-directives", "text/x-cargo-directives", b"captured");
        let mut failed = output(&mut f, "build-script-directives", "text/x-cargo-directives", b"partial");
        fields(&mut failed).insert("status".into(), text("failed"));
        fields(&mut failed).insert("failureDetail".into(), text("build failed"));
        let mut rows = vec![ok, failed]; if reverse { rows.reverse(); }
        set_rows(&mut f, rows); let ids = f.ids();
        assert!(matches!(directive_lookup(&f, &ids, "owned").unwrap(), DeclaredBuildScriptDirectives::Missing));
    }
}
#[test]
fn directive_lookup_duplicate_ok_rows_never_merge_or_choose_by_order() {
    for reverse in [false, true] {
        let mut f = prepared();
        let a = output(&mut f, "build-script-directives", "text/x-cargo-directives", b"one");
        let b = output(&mut f, "build-script-directives", "text/x-cargo-directives", b"two");
        let mut rows = vec![a, b]; if reverse { rows.reverse(); }
        set_rows(&mut f, rows); let ids = f.ids();
        assert!(matches!(directive_lookup(&f, &ids, "owned"), Err(DirectiveLookupError::Ambiguous)));
    }
}
#[test]
fn directive_lookup_empty_and_absent_sets_are_missing() {
    for mut f in [prepared(), Fixture::new()] {
        let ids = f.ids();
        assert!(matches!(directive_lookup(&f, &ids, "owned").unwrap(), DeclaredBuildScriptDirectives::Missing));
    }
}
#[test]
fn directive_lookup_miss_and_failed_owner_cannot_bypass_whole_set_checks() {
    let mut f = prepared();
    let mut row = output(&mut f, "build-script-directives", "text/x-cargo-directives", b"captured");
    fields(fields(&mut row).get_mut("inputBinding").unwrap()).insert("cfgSetId".into(), text("stale"));
    set_rows(&mut f, vec![row]); let ids = f.ids();
    assert!(matches!(directive_lookup(&f, &ids, "missing"), Err(DirectiveLookupError::Prepared(PreparedInputError::Binding { field: "cfgSetId", .. }))));
    let mut f = prepared();
    let mut row = output(&mut f, "build-script-directives", "text/x-cargo-directives", b"partial");
    fields(&mut row).insert("status".into(), text("failed")); fields(&mut row).insert("failureDetail".into(), text("failed"));
    set_rows(&mut f, vec![row]); let ids = f.ids(); f.blobs.remove(&raw_sha256(b"partial"));
    assert!(matches!(directive_lookup(&f, &ids, "owned"), Err(DirectiveLookupError::Prepared(PreparedInputError::Retained(_)))));
}
'''
(b/'prepared_inputs_tests.rs').write_bytes((p/'prepared_inputs_tests.rs').read_bytes()+tests.encode())
