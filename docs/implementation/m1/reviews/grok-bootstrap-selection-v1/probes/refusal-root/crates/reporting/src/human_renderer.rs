use opensip_contracts::generated::{
    evidence::FieldPresence,
    output::{Envelope7Root, Metadata1Root},
};
use std::fmt::Write;

pub fn render_human(value: &Envelope7Root) -> Result<Vec<u8>, &'static str> {
    let mut text = String::new();
    match &value.meta {
        FieldPresence::Present(Some(Metadata1Root::HelpMetadataV1(meta))) => {
            text.push_str("OpenSIP\n\n");
            if let Some(topic) = &meta.topic {
                writeln!(&mut text, "Help: {topic}\n").map_err(|_| "render failure")?;
            }
            for command in &meta.commands {
                writeln!(
                    &mut text,
                    "{}\n  {}\n  {}\n",
                    command.name,
                    command.usage.as_str(),
                    command.summary.as_str()
                )
                .map_err(|_| "render failure")?;
            }
        }
        FieldPresence::Present(Some(Metadata1Root::VersionMetadataV1(meta))) => {
            writeln!(
                &mut text,
                "OpenSIP {} ({})",
                meta.host_release.as_str(),
                meta.build_channel
            )
            .map_err(|_| "render failure")?;
            if meta.closure_ids.is_empty() {
                text.push_str("Component closures: none\n");
            } else {
                for id in &meta.closure_ids {
                    writeln!(&mut text, "Component closure: {}", id.as_str())
                        .map_err(|_| "render failure")?;
                }
            }
        }
        FieldPresence::Missing => {
            writeln!(&mut text, "Termination: {}", value.termination.class)
                .map_err(|_| "render failure")?;
            if let FieldPresence::Present(Some(code)) = &value.termination.error_code {
                writeln!(&mut text, "Error: {code}").map_err(|_| "render failure")?;
            }
            if let FieldPresence::Present(details) = &value.errors {
                for detail in details {
                    writeln!(
                        &mut text,
                        "Detail: {}\nRemedy: {}",
                        detail.code,
                        detail.remedy.as_str()
                    )
                    .map_err(|_| "render failure")?;
                }
            }
            writeln!(&mut text, "Request: {}", value.request_id.as_str())
                .map_err(|_| "render failure")?;
            if let FieldPresence::Present(rows) = &value.diagnostics {
                for row in rows {
                    writeln!(&mut text, "{}", row.as_str()).map_err(|_| "render failure")?;
                }
            } else {
                return Err("missing required human projection");
            }
        }
        _ => return Err("invalid metadata projection"),
    }
    if matches!(&value.meta, FieldPresence::Present(Some(_))) {
        writeln!(&mut text, "Termination: {}", value.termination.class)
            .map_err(|_| "render failure")?;
    }
    Ok(text.into_bytes())
}

/// Shell code uses only the host's closed compiled command catalogue.
pub fn completion(
    shell: &str,
    commands: &[opensip_contracts::generated::output::Metadata1HelpCommand],
) -> Option<Vec<u8>> {
    let names = commands
        .iter()
        .map(|row| row.name.to_string())
        .collect::<Vec<_>>()
        .join(" ");
    let value = match shell {
        "bash" => format!("complete -W '{names}' opensip\n"),
        "zsh" => format!("#compdef opensip\n_arguments '1:command:({names})'\n"),
        "fish" => format!("complete -c opensip -f -a '{names}'\n"),
        _ => return None,
    };
    Some((value + "# Termination: success\n").into_bytes())
}
