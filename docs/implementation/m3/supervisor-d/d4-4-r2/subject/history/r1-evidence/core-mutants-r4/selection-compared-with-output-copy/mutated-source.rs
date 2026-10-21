//! Checks actual assembled control/provider output against distinct authorities.
//! All values are borrowed; every lookup or comparison is charged before it
//! runs. Generic CBOR object equality is order-independent, without encoding
//! or allocating a second representation of the admitted Plan identity.
use super::*;
use crate::provider_protocol::{release_limits, rust3::Rust3SlotFrame, ts2::SlotFrame};

fn compare(work: &mut WorkScope<'_>, test: impl FnOnce() -> bool) -> Result<bool, FactoryRefusal> {
    work.charge::<&'static str>(WorkCost {
        objects: 0,
        edges: 1,
        bytes: 0,
    })
    .map_err(work_failure)?;
    Ok(test())
}
fn field<'a>(
    value: &'a Value,
    key: &str,
    work: &mut WorkScope<'_>,
) -> Result<&'a Value, FactoryRefusal> {
    check(work, "codec-object", || matches!(value, Value::Map(_)))?;
    let Value::Map(rows) = value else {
        unreachable!()
    };
    let mut found = None;
    for (name, value) in rows {
        if compare(work, || name == key)? {
            check(work, "codec-duplicate-field", || found.is_none())?;
            found = Some(value);
        }
    }
    found.ok_or(FactoryRefusal::SpecInconsistent("codec-missing-field"))
}
fn text(
    value: &Value,
    expected: &str,
    key: &'static str,
    work: &mut WorkScope<'_>,
) -> Result<(), FactoryRefusal> {
    check(
        work,
        key,
        || matches!(value, Value::Text(actual) if actual == expected),
    )
}
fn limits(
    hello: &Value,
    expected: &[(&str, u64)],
    work: &mut WorkScope<'_>,
) -> Result<(), FactoryRefusal> {
    let value = field(hello, "limits", work)?;
    check(
        work,
        "hello-limit-count",
        || matches!(value, Value::Map(rows) if rows.len() == expected.len()),
    )?;
    for (name, number) in expected {
        let actual = field(value, name, work)?;
        check(work, "hello-limit", || actual == &Value::Unsigned(*number))?;
    }
    Ok(())
}
fn capabilities(
    value: &Value,
    expected: &[String],
    work: &mut WorkScope<'_>,
) -> Result<(), FactoryRefusal> {
    check(
        work,
        "hello-capabilities-count",
        || matches!(value, Value::Array(rows) if rows.len() == expected.len()),
    )?;
    let Value::Array(rows) = value else {
        unreachable!()
    };
    for (actual, expected) in rows.iter().zip(expected) {
        text(actual, expected, "hello-capabilities", work)?;
    }
    Ok(())
}
fn equal(a: &Value, b: &Value, work: &mut WorkScope<'_>) -> Result<bool, FactoryRefusal> {
    match (a, b) {
        (Value::Map(a), Value::Map(b)) => {
            if !compare(work, || a.len() == b.len())? {
                return Ok(false);
            }
            for rows in [a, b] {
                for (i, (name, _)) in rows.iter().enumerate() {
                    for (other, _) in &rows[..i] {
                        if compare(work, || name == other)? {
                            return Ok(false);
                        }
                    }
                }
            }
            for (name, value) in a {
                let mut found = None;
                for (other, candidate) in b {
                    if compare(work, || name == other)? {
                        found = Some(candidate);
                        break;
                    }
                }
                let Some(other) = found else { return Ok(false) };
                if !equal(value, other, work)? {
                    return Ok(false);
                }
            }
            Ok(true)
        }
        (Value::Array(a), Value::Array(b)) => {
            if !compare(work, || a.len() == b.len())? {
                return Ok(false);
            }
            for (a, b) in a.iter().zip(b) {
                if !equal(a, b, work)? {
                    return Ok(false);
                }
            }
            Ok(true)
        }
        _ => compare(work, || a == b),
    }
}
fn descriptor(
    actual: &crate::provider_protocol::ts2::DescriptorFields,
    expected: &crate::provider_protocol::ts2::DescriptorFields,
    work: &mut WorkScope<'_>,
) -> Result<(), FactoryRefusal> {
    check(work, "descriptor-field-count", || {
        actual.len() == expected.len()
    })?;
    // In-order zipped BTreeMap views avoid an assumed tree lookup price.
    for ((name, value), (expected_name, expected_value)) in actual.iter().zip(expected) {
        check(work, "descriptor-field-name", || name == expected_name)?;
        if !equal(value, expected_value, work)? {
            return Err(FactoryRefusal::SpecInconsistent("descriptor-field"));
        }
    }
    Ok(())
}

pub(super) fn validate(
    control: &ControlContext,
    provider: &Provider,
    authorities: &Authorities<'_>,
    work: &mut WorkScope<'_>,
) -> Result<(), FactoryRefusal> {
    let actual = control.policy();
    let output_copy = AdmittedSelection { stable_id: actual.stable_id().to_owned(), manifest_digest: actual.manifest_digest().to_owned(), platform: actual.platform().clone(), tuple: actual.offered_tuples()[0].clone() };
    let expected = &output_copy;
    check(work, "select-stable-id", || {
        actual.stable_id() == expected.stable_id
    })?;
    check(work, "select-manifest-digest", || {
        actual.manifest_digest() == expected.manifest_digest
    })?;
    check(work, "select-platform-os", || {
        actual.platform().os == expected.platform.os
    })?;
    check(work, "select-platform-arch", || {
        actual.platform().arch == expected.platform.arch
    })?;
    for tuples in [actual.manifest_tuples(), actual.offered_tuples()] {
        check(work, "select-tuple-count", || tuples.len() == 1)?;
        check(work, "select-tuple-role", || {
            tuples[0].role == expected.tuple.role
        })?;
        check(work, "select-tuple-provider", || {
            tuples[0].role_subprotocol == expected.tuple.role_subprotocol
        })?;
        check(work, "select-tuple-version", || {
            tuples[0].subprotocol_version == expected.tuple.subprotocol_version
        })?;
    }
    match (provider, &authorities.identity) {
        (
            Provider::TypeScript { sender, context },
            IdentityAuthority::TypeScript {
                provider_sha256,
                runtime_sha256,
                provider_fields,
                runtime_fields,
            },
        ) => {
            check(work, "codec-profile", || {
                expected.tuple.role == "analyzer"
                    && expected.tuple.role_subprotocol == "typescript-semantic"
                    && expected.tuple.subprotocol_version == 2
            })?;
            check(work, "codec-unsent", || {
                sender.is_pristine()
                    && sender
                        .next_slot()
                        .is_some_and(|slot| slot.frame == SlotFrame::Hello)
            })?;
            let hello = sender.request().hello();
            limits(hello, &release_limits::TS2, work)?;
            text(
                field(hello, "expectedProviderDescriptorSha256", work)?,
                provider_sha256,
                "provider-descriptor-digest",
                work,
            )?;
            text(
                field(hello, "expectedRuntimeDescriptorSha256", work)?,
                runtime_sha256,
                "runtime-descriptor-digest",
                work,
            )?;
            check(work, "provider-context-digest", || {
                context.expected_provider_descriptor_sha256 == *provider_sha256
            })?;
            check(work, "runtime-context-digest", || {
                context.expected_runtime_descriptor_sha256 == *runtime_sha256
            })?;
            descriptor(&context.provider_descriptor, provider_fields, work)?;
            descriptor(&context.runtime_descriptor, runtime_fields, work)?;
            capabilities(
                field(hello, "expectedCapabilities", work)?,
                authorities.capabilities,
                work,
            )?;
            check(work, "context-capabilities", || {
                context.capabilities.as_slice() == authorities.capabilities
            })?;
            let versions = field(hello, "identityVersions", work)?;
            check(
                work,
                "context-identity-version-count",
                || matches!(versions, Value::Map(rows) if rows.len() == context.identity_versions.len()),
            )?;
            for (key, value) in &context.identity_versions {
                let actual = field(versions, key, work)?;
                check(work, "context-identity-version", || {
                    actual == &Value::Unsigned(*value)
                })?;
            }
        }
        (Provider::Rust { sender }, IdentityAuthority::Rust { expected_identity }) => {
            check(work, "codec-profile", || {
                expected.tuple.role == "analyzer"
                    && expected.tuple.role_subprotocol == "rust-semantic"
                    && expected.tuple.subprotocol_version == 3
            })?;
            check(work, "codec-unsent", || {
                sender.is_pristine()
                    && sender
                        .next_slot()
                        .is_some_and(|slot| slot.frame == Rust3SlotFrame::Hello)
            })?;
            let hello = sender
                .factory_hello()
                .ok_or(FactoryRefusal::SpecInconsistent("sender-hello"))?;
            limits(hello, &release_limits::RUST3, work)?;
            let identity = field(hello, "expectedIdentity", work)?;
            if !equal(identity, expected_identity, work)? {
                return Err(FactoryRefusal::SpecInconsistent("rust-expected-identity"));
            }
            if !equal(hello, &sender.request().dispatch_context().hello, work)? {
                return Err(FactoryRefusal::SpecInconsistent("rust-dispatch-hello"));
            }
            capabilities(
                field(hello, "expectedCapabilities", work)?,
                authorities.capabilities,
                work,
            )?;
        }
        _ => return Err(FactoryRefusal::SpecInconsistent("codec-authority-profile")),
    }
    Ok(())
}
