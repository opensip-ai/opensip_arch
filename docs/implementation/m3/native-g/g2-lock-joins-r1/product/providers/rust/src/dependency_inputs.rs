//! Declared dependency-manifest/member retention, with no provenance admission.

use crate::universe_inputs::{
    UniverseInputChecks, UniverseInputError, UniverseInputRequest, check_declared_universe_inputs,
};
use opensip_identity::{
    GraphError, IdentityDomain, JsonValue, NativeFrameSet, RetainedInputError, RetainedInputs,
};
use std::collections::BTreeMap;

#[derive(Debug)]
pub enum DependencyInputError {
    Universe(UniverseInputError),
    Frame(GraphError),
    Retained(RetainedInputError),
    Representation,
    Mismatch { package: usize, field: &'static str },
    CountOverflow,
}

/// Inert byte/count observations, not an authenticated/complete dependency set.
#[derive(Debug)]
pub struct DependencyInputChecks {
    universe: UniverseInputChecks,
    dependency_digest: [u8; 32],
    package_count: usize,
    declared_files: u64,
    declared_bytes: u64,
}
impl DependencyInputChecks {
    pub fn universe_checks(&self) -> &UniverseInputChecks {
        &self.universe
    }
    pub fn dependency_digest(&self) -> [u8; 32] {
        self.dependency_digest
    }
    pub fn package_count(&self) -> usize {
        self.package_count
    }
    pub fn declared_files(&self) -> u64 {
        self.declared_files
    }
    pub fn declared_bytes(&self) -> u64 {
        self.declared_bytes
    }
}

/// Check §3.1's exact declared dependency manifest/member byte and count joins.
/// Mandatory universe/context/nested/snapshot correspondence runs first. Every
/// package names the H preimage of a current registered dependency-file-manifest,
/// whose sorted unique paths, file count, byte sum and member bytes are checked.
/// The selected snapshot's Cargo.lock raw bytes are retained at its exact length.
/// Shared member bytes may be verified once per immutable request; differing
/// declared lengths still refuse, and each file/package counts independently.
///
/// A declared checksumVerification=mismatch refuses the whole observation.
/// Other verification/provenance labels remain declarations: this does not parse
/// Cargo.lock, derive activated features/completeness, authenticate a tarball,
/// verify a vendor checksum file or git revision, admit import/source acquisition,
/// mount a dependency namespace or grant native context/Plan/provider authority.
pub fn check_declared_dependency_inputs(
    inputs: &RetainedInputs<'_>,
    request: &UniverseInputRequest<'_>,
    schema_work: usize,
) -> Result<DependencyInputChecks, DependencyInputError> {
    let universe = check_declared_universe_inputs(inputs, request, schema_work)
        .map_err(DependencyInputError::Universe)?;
    let universe_frame = inputs
        .frame_candidate(
            request.universe_digest,
            NativeFrameSet::SemanticUniverse,
            schema_work,
        )
        .map_err(DependencyInputError::Frame)?;
    let dependency_id = text(field(
        map(universe_frame.descriptor())?,
        "dependencySourceSetId",
    )?)?
    .strip_prefix("sha256:")
    .ok_or(DependencyInputError::Representation)?;
    let dependency_digest = digest(dependency_id)?;
    let dependency = inputs
        .frame_candidate(dependency_digest, NativeFrameSet::Nested, schema_work)
        .map_err(DependencyInputError::Frame)?;
    if dependency.domain() != "native.dependency-source-set.v1" {
        return Err(DependencyInputError::Representation);
    }
    let dependency = map(dependency.descriptor())?;
    let lock = map(field(dependency, "lockfileIdentity")?)?;
    let snapshot = inputs
        .object(request.snapshot_id, IdentityDomain::Snapshot, schema_work)
        .map_err(DependencyInputError::Retained)?;
    let mut lengths = BTreeMap::new();
    let lock_path = field(lock, "path")?;
    let mut found = false;
    for row in array(field(map(snapshot.descriptor())?, "sourceInventory")?)? {
        let row = map(row)?;
        if field(row, "path")? == lock_path {
            retain_blob(
                inputs,
                digest(text(field(lock, "contentSha256")?)?)?,
                number(field(row, "bytes")?)?,
                &mut lengths,
            )?;
            found = true;
        }
    }
    if !found {
        return Err(DependencyInputError::Representation);
    }
    let packages = array(field(dependency, "packages")?)?;
    let mut declared_files = 0u64;
    let mut declared_bytes = 0u64;
    for (index, package) in packages.iter().enumerate() {
        let package = map(package)?;
        if text(field(package, "checksumVerification")?)? == "mismatch" {
            return Err(DependencyInputError::Mismatch {
                package: index,
                field: "checksumVerification",
            });
        }
        let manifest = inputs
            .frame_candidate(
                digest(text(field(package, "fileManifestSha256")?)?)?,
                NativeFrameSet::Nested,
                schema_work,
            )
            .map_err(DependencyInputError::Frame)?;
        if manifest.domain() != "native.dependency-file-manifest.v1" {
            return Err(DependencyInputError::Mismatch {
                package: index,
                field: "fileManifest.domain",
            });
        }
        let files = array(manifest.descriptor())?;
        let count = u64::try_from(files.len()).map_err(|_| DependencyInputError::CountOverflow)?;
        if number(field(package, "fileCount")?)? != count {
            return Err(DependencyInputError::Mismatch {
                package: index,
                field: "fileCount",
            });
        }
        let total = files.iter().try_fold(0u64, |total, row| {
            total
                .checked_add(number(field(map(row)?, "byteLength")?)?)
                .ok_or(DependencyInputError::CountOverflow)
        })?;
        if number(field(package, "totalBytes")?)? != total {
            return Err(DependencyInputError::Mismatch {
                package: index,
                field: "totalBytes",
            });
        }
        for row in files {
            let row = map(row)?;
            retain_blob(
                inputs,
                digest(text(field(row, "contentSha256")?)?)?,
                number(field(row, "byteLength")?)?,
                &mut lengths,
            )?;
        }
        declared_files = declared_files
            .checked_add(count)
            .ok_or(DependencyInputError::CountOverflow)?;
        declared_bytes = declared_bytes
            .checked_add(total)
            .ok_or(DependencyInputError::CountOverflow)?;
    }
    Ok(DependencyInputChecks {
        universe,
        dependency_digest,
        package_count: packages.len(),
        declared_files,
        declared_bytes,
    })
}

/// Declared package tuple/checksum joins to exact retained lock bytes only.
#[derive(Debug)]
pub struct DependencyLockChecks {
    dependency: DependencyInputChecks,
    lockfile_version: u8,
    lock_package_rows: usize,
}
impl DependencyLockChecks {
    pub fn dependency_checks(&self) -> &DependencyInputChecks {
        &self.dependency
    }
    pub fn lockfile_version(&self) -> u8 {
        self.lockfile_version
    }
    pub fn lock_package_rows(&self) -> usize {
        self.lock_package_rows
    }
}
#[derive(Debug)]
pub enum DependencyLockError {
    Inputs(DependencyInputError),
    Parse(opensip_identity::TomlError),
    Shape(&'static str),
    Version,
    MissingTuple(usize),
    AmbiguousTuple(usize),
    Checksum(usize),
}
impl From<DependencyInputError> for DependencyLockError {
    fn from(error: DependencyInputError) -> Self {
        Self::Inputs(error)
    }
}

/// Observe exact Cargo.lock version/package tuple/checksum correspondence.
/// Mandatory retained universe/context/snapshot/dependency-manifest/member joins
/// run first. All exact inventoried lock bytes are parsed as one TOML document,
/// without recovery. The parsed version is 3 or 4 and equals the descriptor.
/// Every declared package joins by the exact (name, version, sourceId) tuple;
/// absent source means the path-package empty string. Missing or ambiguous joins
/// never choose a first/last/nearest row. Declared lockChecksum equals the
/// matching lock row's optional checksum, with absence remaining null.
///
/// This is not activated-feature membership/completeness, Cargo metadata or
/// Cargo's full lock-format validation. Other lock rows/fields are not an
/// activation list, and sourceKind/provenance/acquisition/tarball/vendor/git
/// admission remain separate. No packageKey codec, delimiter or mount spelling
/// is invented. The selected pure parser's local bounds remain local parse
/// errors, not a widened product scope bound or new wire refusal cause.
pub fn check_declared_lockfile_joins(
    inputs: &RetainedInputs<'_>,
    request: &UniverseInputRequest<'_>,
    schema_work: usize,
) -> Result<DependencyLockChecks, DependencyLockError> {
    let dependency = check_declared_dependency_inputs(inputs, request, schema_work)?;
    let frame = inputs
        .frame_candidate(
            dependency.dependency_digest(),
            NativeFrameSet::Nested,
            schema_work,
        )
        .map_err(DependencyInputError::Frame)?;
    let descriptor = map(frame.descriptor())?;
    let lock = map(field(descriptor, "lockfileIdentity")?)?;
    let raw = inputs
        .blob(digest(text(field(lock, "contentSha256")?)?)?)
        .map_err(DependencyInputError::Retained)?;
    let document = opensip_identity::parse_toml(raw.bytes()).map_err(DependencyLockError::Parse)?;
    let root = document.table();
    let parsed = root
        .get("version")
        .and_then(|v| v.as_integer())
        .ok_or(DependencyLockError::Shape("version"))?;
    let version = u8::from_str_radix(parsed.digits(), parsed.radix())
        .map_err(|_| DependencyLockError::Version)?;
    if !matches!(version, 3 | 4) || u64::from(version) != number(field(lock, "lockfileVersion")?)? {
        return Err(DependencyLockError::Version);
    }
    let mut by_tuple: BTreeMap<(&str, &str, &str), Vec<Option<&str>>> = BTreeMap::new();
    let mut lock_package_rows = 0;
    if let Some(value) = root.get("package") {
        let rows = value
            .as_array()
            .ok_or(DependencyLockError::Shape("package"))?;
        lock_package_rows = rows.len();
        for row in rows.iter() {
            let row = row
                .as_table()
                .ok_or(DependencyLockError::Shape("package.row"))?;
            let name = row
                .get("name")
                .and_then(|v| v.as_str())
                .ok_or(DependencyLockError::Shape("package.name"))?;
            let version = row
                .get("version")
                .and_then(|v| v.as_str())
                .ok_or(DependencyLockError::Shape("package.version"))?;
            let source = optional_lock_text(row, "source")?.unwrap_or("");
            let checksum = optional_lock_text(row, "checksum")?;
            by_tuple
                .entry((name, version, source))
                .or_default()
                .push(checksum);
        }
    }
    for (index, package) in array(field(descriptor, "packages")?)?.iter().enumerate() {
        let package = map(package)?;
        let key = (
            text(field(package, "name")?)?,
            text(field(package, "version")?)?,
            text(field(package, "sourceId")?)?,
        );
        let matches = by_tuple
            .get(&key)
            .ok_or(DependencyLockError::MissingTuple(index))?;
        if matches.len() != 1 {
            return Err(DependencyLockError::AmbiguousTuple(index));
        }
        let checksum = match field(package, "lockChecksum")? {
            JsonValue::Null => None,
            value => Some(text(value)?),
        };
        if matches[0] != checksum {
            return Err(DependencyLockError::Checksum(index));
        }
    }
    Ok(DependencyLockChecks {
        dependency,
        lockfile_version: version,
        lock_package_rows,
    })
}
fn optional_lock_text<'a>(
    row: opensip_identity::TomlTableView<'a>,
    name: &'static str,
) -> Result<Option<&'a str>, DependencyLockError> {
    row.get(name)
        .map(|v| v.as_str().ok_or(DependencyLockError::Shape(name)))
        .transpose()
}

fn retain_blob(
    inputs: &RetainedInputs<'_>,
    sha: [u8; 32],
    bytes: u64,
    checked: &mut BTreeMap<[u8; 32], u64>,
) -> Result<(), DependencyInputError> {
    if let Some(previous) = checked.get(&sha) {
        if *previous != bytes {
            return Err(DependencyInputError::Retained(
                RetainedInputError::BlobLength,
            ));
        }
    } else {
        inputs
            .blob(sha)
            .map_err(DependencyInputError::Retained)?
            .require_length(bytes)
            .map_err(DependencyInputError::Retained)?;
        checked.insert(sha, bytes);
    }
    Ok(())
}
fn map(value: &JsonValue) -> Result<&BTreeMap<String, JsonValue>, DependencyInputError> {
    match value {
        JsonValue::Object(value) => Ok(value),
        _ => Err(DependencyInputError::Representation),
    }
}
fn field<'a>(
    value: &'a BTreeMap<String, JsonValue>,
    name: &str,
) -> Result<&'a JsonValue, DependencyInputError> {
    value.get(name).ok_or(DependencyInputError::Representation)
}
fn text(value: &JsonValue) -> Result<&str, DependencyInputError> {
    match value {
        JsonValue::String(value) => Ok(value),
        _ => Err(DependencyInputError::Representation),
    }
}
fn array(value: &JsonValue) -> Result<&[JsonValue], DependencyInputError> {
    match value {
        JsonValue::Array(value) => Ok(value),
        _ => Err(DependencyInputError::Representation),
    }
}
fn number(value: &JsonValue) -> Result<u64, DependencyInputError> {
    match value {
        JsonValue::Integer(value) => {
            u64::try_from(value.get()).map_err(|_| DependencyInputError::Representation)
        }
        _ => Err(DependencyInputError::Representation),
    }
}
fn digest(value: &str) -> Result<[u8; 32], DependencyInputError> {
    if value.len() != 64 {
        return Err(DependencyInputError::Representation);
    }
    let mut result = [0; 32];
    for (index, pair) in value.as_bytes().chunks_exact(2).enumerate() {
        let digit = |value| match value {
            b'0'..=b'9' => Ok(value - b'0'),
            b'a'..=b'f' => Ok(value - b'a' + 10),
            _ => Err(DependencyInputError::Representation),
        };
        result[index] = digit(pair[0])? << 4 | digit(pair[1])?;
    }
    Ok(result)
}

#[cfg(test)]
#[path = "dependency_inputs_tests.rs"]
mod tests;
