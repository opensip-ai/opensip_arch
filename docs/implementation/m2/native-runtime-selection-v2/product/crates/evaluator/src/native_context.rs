//! Native context owner checks over a registered frame and retained descriptors.
//! This does not establish transitive closure, Plan selection or evaluator replay.
use alloc::{
    collections::{BTreeMap, BTreeSet},
    format,
    string::{String, ToString},
    vec::Vec,
};
use opensip_identity::{
    CandidateError, GraphError, NativeFrameSet, RetainedInputError as InputError, RetainedInputs,
    SchemaAdmissionError, SchemaError,
};
use opensip_identity::{IdentityDomain, JsonValue as V, parse_json};

const LAW: &[u8] = include_bytes!("native-context-registry.json");

#[derive(Debug, PartialEq, Eq)]
pub enum NativeContextError {
    Frame(GraphError),
    Unsupported(&'static str),
    RegistryLaw,
    CaseDataUnavailable,
}

/// The native owner's diagnostics for one context. Empty refusals establish
/// only these context checks, not retained member bytes or a selected Run.
pub struct NativeContextChecks {
    digest: [u8; 32],
    domain: String,
    refusals: Vec<String>,
}
impl NativeContextChecks {
    pub fn digest(&self) -> [u8; 32] {
        self.digest
    }
    pub fn domain(&self) -> &str {
        &self.domain
    }
    pub fn refusals(&self) -> &[String] {
        &self.refusals
    }
}

fn field<'a>(v: &'a V, key: &str) -> Result<&'a V, NativeContextError> {
    if let V::Object(o) = v {
        o.get(key).ok_or(NativeContextError::RegistryLaw)
    } else {
        Err(NativeContextError::RegistryLaw)
    }
}
fn text(v: &V) -> Result<&str, NativeContextError> {
    if let V::String(s) = v {
        Ok(s)
    } else {
        Err(NativeContextError::RegistryLaw)
    }
}
fn array(v: &V) -> Result<&[V], NativeContextError> {
    if let V::Array(a) = v {
        Ok(a)
    } else {
        Err(NativeContextError::RegistryLaw)
    }
}
fn string<'a>(v: &'a V, key: &str) -> Result<&'a str, NativeContextError> {
    text(field(v, key)?)
}

struct Checks<'s, 'a> {
    inputs: &'s RetainedInputs<'a>,
    work: usize,
    refusals: BTreeSet<String>,
}
impl Checks<'_, '_> {
    fn typescript(&mut self, context: &V) -> Result<(), NativeContextError> {
        let toolchain = field(context, "toolchain")?;
        let tools = field(context, "toolClosure")?;
        let options = field(field(context, "configProjection")?, "honoredOptions")?;
        let stdlib = self.closure(
            &format!(
                "closure2:{}",
                string(toolchain, "typescriptStdlibMerkleRoot")?
            ),
            "stdlib",
            "toolchain.typescriptStdlibMerkleRoot",
        )?;
        if field(context, "moduleResolutionMode")? != field(options, "moduleResolution")? {
            self.refuse("native.native-context-field-mismatch:moduleResolutionMode");
        }
        let fold = |s: &str| {
            crate::unicode_case::lowercase(s).map_err(|_| NativeContextError::CaseDataUnavailable)
        };
        let selection = array(field(toolchain, "libSelection")?)?
            .iter()
            .map(text)
            .collect::<Result<Vec<_>, _>>()?;
        let selected = selection
            .iter()
            .map(|s| fold(s))
            .collect::<Result<Vec<_>, _>>()?;
        let selected_set: BTreeSet<_> = selected.iter().collect();
        if selected_set.len() != selected.len() {
            self.refuse("native.native-context-field-mismatch:duplicate-lib-selection");
        }
        if selection
            .windows(2)
            .any(|w| w[0].as_bytes() > w[1].as_bytes())
        {
            self.refuse("native.native-context-field-mismatch:lib-selection-order");
        }
        if !matches!(field(options, "lib")?, V::Null) {
            let options_lib = array(field(options, "lib")?)?
                .iter()
                .map(|v| fold(text(v)?))
                .collect::<Result<BTreeSet<_>, _>>()?;
            if selected.into_iter().collect::<BTreeSet<_>>() != options_lib {
                self.refuse("native.native-context-field-mismatch:libSelection");
            }
        }
        let components = array(field(toolchain, "standardLibraryComponentDigests")?)?;
        let names = components
            .iter()
            .map(|v| string(v, "component"))
            .collect::<Result<Vec<_>, _>>()?;
        if names.windows(2).any(|w| w[0].as_bytes() >= w[1].as_bytes()) {
            self.refuse("native.native-context-field-mismatch:stdlib-component-order");
        }
        if let Some(stdlib) = stdlib {
            let mut by_component = BTreeMap::new();
            for blob in array(field(&stdlib, "tree")?)? {
                let path = string(blob, "path")?;
                if !path.ends_with(".d.ts") {
                    continue;
                }
                let name = path
                    .rsplit('/')
                    .next()
                    .ok_or(NativeContextError::RegistryLaw)?;
                if by_component.insert(name, string(blob, "sha256")?).is_some() {
                    self.refuse(format!(
                        "native.native-context-stdlib-tree-ambiguous-basename:{name}"
                    ));
                }
            }
            let declared: BTreeSet<_> = names.iter().copied().collect();
            for component in components {
                let name = string(component, "component")?;
                if by_component.get(name).copied() != Some(string(component, "sha256")?) {
                    self.refuse(format!("native.native-context-stdlib-tree-mismatch:{name}"));
                }
            }
            for name in by_component.keys().filter(|n| !declared.contains(**n)) {
                self.refuse(format!(
                    "native.native-context-stdlib-inventory-incomplete:{name}"
                ));
            }
            for lib in selection {
                if !declared.contains(format!("lib.{}.d.ts", fold(lib)?).as_str()) {
                    self.refuse(format!("native.native-context-lib-not-retained:{lib}"));
                }
            }
        }
        if let Some(closure) = self.closure(
            string(tools, "closureId")?,
            "toolchain",
            "toolClosure.closureId",
        )? {
            let digests: BTreeSet<_> = array(field(&closure, "tree")?)?
                .iter()
                .map(|v| string(v, "sha256"))
                .collect::<Result<_, _>>()?;
            if field(&closure, "semanticVersion")? != field(toolchain, "compilerVersion")? {
                self.refuse("native.native-context-compiler-version-not-from-manifest");
            }
            for role in ["compiler", "runtime"] {
                if !digests.contains(string(tools, role)?) {
                    self.refuse(format!("native.native-context-tool-not-in-closure:{role}"));
                }
            }
            if !digests.contains(string(toolchain, "compilerPackageDigest")?) {
                self.refuse("native.native-context-tool-not-in-closure:compilerPackageDigest");
            }
        }
        Ok(())
    }
    fn refuse(&mut self, cause: impl Into<String>) {
        self.refusals.insert(cause.into());
    }
    fn closure(
        &mut self,
        key: &str,
        kind: &str,
        label: &str,
    ) -> Result<Option<V>, NativeContextError> {
        let result = self.inputs.object(key, IdentityDomain::Closure, self.work);
        let candidate = match result {
            Ok(c) => c,
            Err(error) => {
                if matches!(
                    error,
                    InputError::Candidate(CandidateError::Schema(SchemaAdmissionError::Schema(
                        SchemaError::Limit
                    )))
                ) {
                    return Err(NativeContextError::Frame(GraphError::Limit));
                }
                let cause = match error {
                    InputError::MissingObject(_) | InputError::ObjectDomain => "unretained",
                    InputError::ObjectIdentity => "identity-mismatch",
                    _ => "malformed",
                };
                self.refuse(format!("native.native-context-closure-{cause}:{label}"));
                return Ok(None);
            }
        };
        if string(candidate.descriptor(), "kind")? != kind {
            self.refuse(format!(
                "native.native-context-closure-kind-mismatch:{label}"
            ));
            return Ok(None);
        }
        Ok(Some(candidate.descriptor().clone()))
    }
    fn rust(&mut self, context: &V) -> Result<(), NativeContextError> {
        let toolchain = field(context, "toolchain")?;
        let tools = field(context, "toolClosure")?;
        self.closure(
            &format!("closure2:{}", string(toolchain, "rustcDevLlvmDigest")?),
            "rust-dev-llvm",
            "toolchain.rustcDevLlvmDigest",
        )?;
        if let Some(closure) = self.closure(
            string(tools, "closureId")?,
            "toolchain",
            "toolClosure.closureId",
        )? {
            let digests: BTreeSet<&str> = array(field(&closure, "tree")?)?
                .iter()
                .map(|v| string(v, "sha256"))
                .collect::<Result<_, _>>()?;
            for role in ["rustc", "cargo", "procMacroServer", "linker", "ar"] {
                let value = field(tools, role)?;
                if matches!(value, V::Null) && matches!(role, "linker" | "ar") {
                    continue;
                }
                if !digests.contains(text(value)?) {
                    self.refuse(format!("native.native-context-tool-not-in-closure:{role}"));
                }
            }
            if field(&closure, "semanticVersion")? != field(toolchain, "rustcVersion")? {
                self.refuse("native.native-context-compiler-version-not-from-manifest");
            }
        }
        if field(toolchain, "targetTriple")? != field(context, "targetTriple")? {
            self.refuse("native.native-context-field-mismatch:targetTriple");
        }
        let components = array(field(toolchain, "standardLibraryComponentDigests")?)?
            .iter()
            .map(|c| string(c, "component"))
            .collect::<Result<Vec<_>, _>>()?;
        if components
            .windows(2)
            .any(|w| w[0].as_bytes() >= w[1].as_bytes())
        {
            self.refuse("native.native-context-field-mismatch:stdlib-component-order");
        }
        if field(
            field(field(context, "configProjection")?, "rustflags")?,
            "executableSelected",
        )? == &V::Bool(true)
        {
            self.refuse("native.native-context-field-mismatch:executableSelected");
        }
        Ok(())
    }
    fn syntax(&mut self, context: &V) -> Result<(), NativeContextError> {
        let bundle = field(context, "grammarBundle")?;
        let grammars = array(field(bundle, "grammars")?)?;
        if let Some(closure) = self.closure(
            string(bundle, "closureId")?,
            "grammar",
            "grammarBundle.closureId",
        )? {
            let digests: BTreeSet<&str> = array(field(&closure, "tree")?)?
                .iter()
                .map(|v| string(v, "sha256"))
                .collect::<Result<_, _>>()?;
            if field(&closure, "semanticVersion")? != field(bundle, "parserVersion")? {
                self.refuse("native.syntax-grammar-version-not-from-manifest");
            }
            if !digests.contains(string(bundle, "bundleDigest")?) {
                self.refuse("native.syntax-grammar-bundle-not-in-closure");
            }
            for grammar in grammars {
                if !digests.contains(string(grammar, "grammarDigest")?) {
                    self.refuse(format!(
                        "native.syntax-grammar-not-in-closure:{}",
                        string(grammar, "grammarId")?
                    ));
                }
            }
            if !digests.contains(string(field(bundle, "normalizer")?, "specificationDigest")?) {
                self.refuse("native.syntax-normalizer-spec-not-in-closure");
            }
        }
        let mut owners: BTreeMap<&str, usize> = BTreeMap::new();
        for grammar in grammars {
            for suffix in array(field(grammar, "suffixes")?)? {
                *owners.entry(text(suffix)?).or_default() += 1;
            }
        }
        for (suffix, count) in owners {
            if count > 1 {
                self.refuse(format!("native.syntax-grammar-suffix-ambiguous:{suffix}"));
            }
        }
        let law = parse_json(LAW).map_err(|_| NativeContextError::RegistryLaw)?;
        let V::Object(capabilities) = field(&law, "grammarCapabilities")? else {
            return Err(NativeContextError::RegistryLaw);
        };
        let V::Object(bundled) = field(&law, "bundledGrammars")? else {
            return Err(NativeContextError::RegistryLaw);
        };
        let body_languages = array(field(&law, "bodyLanguages")?)?;
        for grammar in grammars {
            let language = string(grammar, "languageId")?;
            let Some(row) = capabilities.get(language) else {
                self.refuse(format!(
                    "native.syntax-grammar-language-not-in-capability-registry:{language}"
                ));
                continue;
            };
            let selected_class = string(row, "syntaxClass")?;
            let declared = string(grammar, "syntaxClass")?;
            if declared != selected_class {
                self.refuse(format!("native.syntax-grammar-class-not-the-registered-one:{language}:declared={declared}:registered={selected_class}"));
            }
            let body = body_languages
                .iter()
                .any(|v| matches!(v, V::String(s) if s == language));
            if selected_class == "code" && !body {
                self.refuse(format!(
                    "native.syntax-grammar-code-language-not-body-identifiable:{language}"
                ));
            }
            if selected_class == "data-document" && body {
                self.refuse(format!(
                    "native.syntax-grammar-data-language-claims-body-identity:{language}"
                ));
            }
            for suffix in array(field(grammar, "suffixes")?)? {
                let suffix = text(suffix)?;
                if !matches!(bundled.get(suffix), Some(V::String(l)) if l == language) {
                    self.refuse(format!(
                        "native.syntax-grammar-suffix-not-bundled-for-language:{suffix}:{language}"
                    ));
                }
            }
        }
        Ok(())
    }
}

/// Rehash and shape-admit the context frame, then run the native context owner
/// over retained closure descriptors. A caller-supplied admission is never read.
/// TypeScript uses the separately pinned Unicode15 FULL default lowercase owner;
/// neither Unicode normalization nor the toolchain's Unicode version supplies it.
pub fn inspect_native_context(
    inputs: &RetainedInputs<'_>,
    digest: [u8; 32],
    descriptor_work: usize,
) -> Result<NativeContextChecks, NativeContextError> {
    let frame = inputs
        .frame_candidate(digest, NativeFrameSet::Context, descriptor_work)
        .map_err(NativeContextError::Frame)?;
    let mut checks = Checks {
        inputs,
        work: descriptor_work,
        refusals: BTreeSet::new(),
    };
    match frame.domain() {
        "native.context.rust.v2" => checks.rust(frame.descriptor())?,
        "native.context.syntax.v2" => checks.syntax(frame.descriptor())?,
        "native.context.typescript.v2" => checks.typescript(frame.descriptor())?,
        _ => return Err(NativeContextError::RegistryLaw),
    }
    Ok(NativeContextChecks {
        digest,
        domain: frame.domain().to_string(),
        refusals: checks.refusals.into_iter().collect(),
    })
}
