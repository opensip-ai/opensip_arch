use crate::arguments;
use opensip_host::{MetadataError, MetadataHost};
use std::{
    ffi::OsString,
    io::{self, Write},
};

pub(crate) fn run(args: impl IntoIterator<Item = OsString>) -> u8 {
    // This ingress is explicitly process-custody metadata only. It constructs
    // no project/configuration, durable storage, provider or network service.
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
    let response = match host.execute(
        &context,
        request.request,
        request.format,
        request.correlation.as_deref(),
        env!("CARGO_PKG_VERSION"),
    ) {
        Ok(value) => value,
        Err(MetadataError::Serialization) => return output_failure(),
        Err(MetadataError::Projection) => match host.delivery_failure(&context, request.format) {
            Ok(value) => value,
            Err(MetadataError::Serialization) => return output_failure(),
            Err(MetadataError::Projection) => {
                let _ = writeln!(
                    io::stderr().lock(),
                    "DELIVERY.REQUIRED_FAILED: required metadata projection failed."
                );
                return 4;
            }
        },
    };
    if crate::terminal::write_stdout(&response.bytes).is_err() {
        // A partial write or flush failure can leave normal bytes visible.
        // Final output failure owns exit4; never append a replacement envelope.
        return output_failure();
    }
    response.exit_code
}

fn output_failure() -> u8 {
    let _ = writeln!(
        io::stderr().lock(),
        "OUTPUT.SERIALIZATION_FAILED: required output emission failed."
    );
    4
}
