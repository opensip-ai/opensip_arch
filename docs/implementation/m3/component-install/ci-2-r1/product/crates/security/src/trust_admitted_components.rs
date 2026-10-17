// M3-C r8 item 7 (unit C2a-1; C2a plan r4, section 2's C2a-1 row and
// LD-C2A-10): the trust owner's read-only bridge to the components the
// ordinary reader verified. Each one lends its authenticated body bytes, its
// validated manifest, its catalog release row and its verified envelope, by
// reference: nothing is copied, re-verified or charged again. Only the trust
// owner constructs one, so a caller cannot assert a manifest, a body or a
// release row of its own.
use super::component_manifest::Validated;
use opensip_identity::JsonValue as V;

/// One verified component, borrowed from the ordinary reader's evidence.
/// It is not Clone, Default or serializable, and authorizes nothing: it is
/// the input of `component_closure`'s unadmitted candidate.
pub struct AuthenticatedComponent<'a> {
    path: &'a str,
    body: &'a [u8],
    envelope: &'a [u8],
    manifest: &'a Validated,
    release: &'a V,
}
impl<'a> AuthenticatedComponent<'a> {
    pub(in crate::trust) fn new(
        path: &'a str,
        body: &'a [u8],
        envelope: &'a [u8],
        manifest: &'a Validated,
        release: &'a V,
    ) -> Self {
        Self {
            path,
            body,
            envelope,
            manifest,
            release,
        }
    }
    /// The catalog member path of the manifest.
    pub fn path(&self) -> &'a str {
        self.path
    }
    /// The authenticated body bytes, excluding the signature envelope.
    pub fn body(&self) -> &'a [u8] {
        self.body
    }
    /// The verified signature envelope's raw bytes.
    pub fn envelope(&self) -> &'a [u8] {
        self.envelope
    }
    /// The validated manifest value.
    pub fn manifest(&self) -> &'a V {
        self.manifest.value()
    }
    /// CR-1's kind for the manifest's role (`component_manifest.rs`), the
    /// only source of a component closure's kind (LD-C2A-2).
    pub fn closure_kind(&self) -> &'static str {
        self.manifest.closure_kind()
    }
    /// The catalog release row the ordinary reader joined to the manifest.
    pub fn release(&self) -> &'a V {
        self.release
    }
}

/// A test holder for one component whose body went through the real body
/// validation (`component_manifest::validate`, with the default host
/// context). It skips no check of the body; its release row and envelope are
/// the test's own, standing in for the ordinary reader's joins, which C2a-2's
/// signed fixtures exercise end to end. Shared fixture gate 7 (law CI r5
/// item 6, unit CI-2): the component installer's and the retained-tree
/// reader's fixtures in opensip-lifecycle build their evidence with it.
#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
pub struct TestComponent {
    body: Vec<u8>,
    envelope: Vec<u8>,
    manifest: Validated,
    release: V,
}
#[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
impl TestComponent {
    pub fn new(body: Vec<u8>, envelope: Vec<u8>, release: V) -> Option<Self> {
        let manifest = super::component_manifest::validate(
            &body,
            &super::component_manifest::Context::default(),
        )
        .ok()?;
        Some(Self {
            body,
            envelope,
            manifest,
            release,
        })
    }
    pub fn authenticated(&self) -> AuthenticatedComponent<'_> {
        AuthenticatedComponent::new(
            "components/test/payload.json",
            &self.body,
            &self.envelope,
            &self.manifest,
            &self.release,
        )
    }
}
