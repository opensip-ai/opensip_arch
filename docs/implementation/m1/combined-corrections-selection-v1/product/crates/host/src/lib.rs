#![forbid(unsafe_code)]
mod delivery;
mod outcomes;
mod request;
pub use delivery::deliver_required;
pub use outcomes::{Format, MetadataError, MetadataHost, MetadataRequest, RenderedResponse};
pub use request::{RequestAllocationError, RequestContext};
