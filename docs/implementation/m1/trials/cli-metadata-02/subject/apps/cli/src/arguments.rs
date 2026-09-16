use opensip_host::{Format, MetadataRequest};
use std::ffi::OsString;

pub(crate) struct Arguments {
    pub request: MetadataRequest,
    pub format: Format,
    pub correlation: Option<String>,
}
pub(crate) fn parse(args: impl IntoIterator<Item = OsString>) -> Arguments {
    let mut format = Format::Human;
    let mut correlation = None;
    let mut words = Vec::new();
    let mut failure = None;
    let mut format_seen = false;
    let mut items = args.into_iter();
    let mut count = 0;
    while let Some(item) = items.next() {
        count += 1;
        if count > 1024 {
            failure = Some("Too many command arguments.");
            break;
        }
        let Some(word) = item.to_str() else {
            failure = Some("Command arguments must be valid Unicode.");
            continue;
        };
        if word.len() > 4096 {
            failure = Some("Command argument exceeds its size limit.");
            continue;
        }
        if word == "--format" || word.starts_with("--format=") {
            if format_seen {
                failure = Some("Output format was specified more than once.");
            }
            format_seen = true;
            let value = if let Some((_, value)) = word.split_once('=') {
                Some(value.to_owned())
            } else {
                items.next().and_then(|x| x.into_string().ok())
            };
            match value.as_deref() {
                Some("json") => format = Format::Json,
                Some("human") => format = Format::Human,
                Some("html" | "sarif" | "agent") => failure = Some("format-not-applicable"),
                _ => failure = Some("Expected --format human or --format json."),
            }
        } else if word == "--client-correlation-id" || word.starts_with("--client-correlation-id=")
        {
            if correlation.is_some() {
                failure = Some("Correlation ID was specified more than once.");
            }
            let value = if let Some((_, value)) = word.split_once('=') {
                Some(value.to_owned())
            } else {
                items.next().and_then(|x| x.into_string().ok())
            };
            match value {
                Some(x) if (1..=128).contains(&x.chars().count()) => correlation = Some(x),
                _ => failure = Some("Invalid client correlation ID."),
            }
        } else if word.starts_with('-') && !matches!(word, "--help" | "-h" | "--version" | "-V") {
            failure = Some("Unknown command option. Use opensip help.");
        } else {
            words.push(word.to_owned());
        }
    }
    let request = if let Some(reason) = failure {
        if reason == "format-not-applicable" {
            MetadataRequest::FormatNotApplicable
        } else {
            MetadataRequest::Rejected { diagnostic: reason }
        }
    } else {
        match words
            .iter()
            .map(String::as_str)
            .collect::<Vec<_>>()
            .as_slice()
        {
            ["help" | "--help" | "-h"] => MetadataRequest::Help { topic: None },
            ["help", topic] => MetadataRequest::Help {
                topic: Some(
                    match *topic {
                        "--version" | "-V" => "version",
                        "--help" | "-h" => "help",
                        other => other,
                    }
                    .to_owned(),
                ),
            },
            ["version" | "--version" | "-V"] => MetadataRequest::Version,
            ["completion", shell] => MetadataRequest::Completion {
                shell: (*shell).to_owned(),
            },
            [] => MetadataRequest::Rejected {
                diagnostic: "Default analysis is not implemented in this development build. Use opensip help.",
            },
            _ => MetadataRequest::Rejected {
                diagnostic: "Unknown command or arguments. Use opensip help.",
            },
        }
    };
    Arguments {
        request,
        format,
        correlation,
    }
}
