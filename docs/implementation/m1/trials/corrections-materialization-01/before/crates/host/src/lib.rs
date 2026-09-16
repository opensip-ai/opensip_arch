#![forbid(unsafe_code)]
mod outcomes;
mod request;
pub use outcomes::{Format, MetadataError, MetadataHost, MetadataRequest, RenderedResponse};
pub use request::{RequestAllocationError, RequestContext};
