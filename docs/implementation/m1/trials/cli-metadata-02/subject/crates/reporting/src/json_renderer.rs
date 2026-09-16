use opensip_contracts::generated::output::Envelope4Root;
/// Encode the already selected host projection. Rendering confers no admission.
pub fn render_json(value: &Envelope4Root) -> Result<Vec<u8>, serde_json::Error> {
    let mut bytes = serde_json::to_vec(value)?;
    bytes.push(b'\n');
    Ok(bytes)
}
