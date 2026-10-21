use crate::arguments::{self, Request};
use opensip_host::{MetadataError, MetadataHost, finalize_invocation};
use std::{
    ffi::OsString,
    io::{self, Write},
};

pub(crate) fn run(args: impl IntoIterator<Item = OsString>) -> u8 {
    // This ingress is explicitly process-custody: metadata, and the read-only
    // doctor (law X10), which observes the account installation through the
    // 458c read receipt and session only. It constructs no project or
    // configuration, writes nothing durably, and starts no provider or
    // network service. Nothing here selects a home, profile or release.
    let mut host = MetadataHost::new();
    let context = match host.begin() {
        Ok(value) => value,
        Err(_) => {
            let _ = writeln!(
                io::stderr().lock(),
                "HOST.IO_FAILURE: request identity allocation failed."
            );
            return 4;
        }
    };
    let request = arguments::parse(args);
    let response = match request.request {
        Request::Metadata(metadata) => host.execute(
            &context,
            metadata,
            request.format,
            request.correlation.as_deref(),
            env!("CARGO_PKG_VERSION"),
        ),
        Request::Doctor => doctor(&host, &context, &request),
    };
    let response = match response {
        Ok(value) => value,
        Err(MetadataError::Serialization) => return output_failure(),
        Err(MetadataError::Projection) => match host.delivery_failure(&context, request.format) {
            Ok(value) => value,
            Err(MetadataError::Serialization) => return output_failure(),
            Err(MetadataError::Projection) => {
                finalize_invocation(false);
                let _ = writeln!(
                    io::stderr().lock(),
                    "DELIVERY.REQUIRED_FAILED: required metadata projection failed."
                );
                return 4;
            }
        },
    };
    let output = match crate::terminal::stdout() {
        Ok(output) => output,
        Err(_) => return output_failure(),
    };
    match opensip_host::deliver_required(response, output) {
        Ok(exit_code) => {
            finalize_invocation(false);
            exit_code
        }
        // The host may already have written a prefix or all normal bytes.
        // Final output failure owns exit4; never append a replacement envelope.
        Err(_) => output_failure(),
    }
}

fn output_failure() -> u8 {
    finalize_invocation(false);
    let _ = writeln!(
        io::stderr().lock(),
        "OUTPUT.SERIALIZATION_FAILED: required output emission failed."
    );
    4
}

#[cfg(target_os = "macos")]
fn doctor(
    host: &MetadataHost,
    context: &opensip_host::RequestContext,
    request: &arguments::Arguments,
) -> Result<opensip_host::RenderedResponse, MetadataError> {
    host.doctor(context, request.format, request.correlation.as_deref())
}

// Doctor's installation owners are implemented for macOS only.
#[cfg(not(target_os = "macos"))]
fn doctor(
    host: &MetadataHost,
    context: &opensip_host::RequestContext,
    request: &arguments::Arguments,
) -> Result<opensip_host::RenderedResponse, MetadataError> {
    host.execute(
        context,
        opensip_host::MetadataRequest::Rejected {
            diagnostic: "Unknown command or arguments. Use opensip help.",
        },
        request.format,
        request.correlation.as_deref(),
        env!("CARGO_PKG_VERSION"),
    )
}
