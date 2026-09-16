#![forbid(unsafe_code)]

/// Failure to obtain a complete independent OS CSPRNG draw.
#[derive(Debug)]
pub struct EntropyError;

/// Operational correlation only; never an input to semantic identity.
pub fn request_entropy() -> Result<[u8; 16], EntropyError> {
    let mut value = [0; 16];
    getrandom::fill(&mut value).map_err(|_| EntropyError)?;
    Ok(value)
}
