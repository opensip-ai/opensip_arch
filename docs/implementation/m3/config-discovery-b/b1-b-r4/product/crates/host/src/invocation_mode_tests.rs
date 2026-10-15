// M3-B r5 item 3 (unit B1-b; plan r3 section 2, "Mode"): the rule, the
// observation under pipes and under a pseudo-terminal, and no environment.
use super::*;

#[test]
fn interactive_exactly_when_both_streams_are_terminals() {
    for (stdin, stderr, interactive) in [
        (true, true, true),
        (true, false, false),
        (false, true, false),
        (false, false, false),
    ] {
        assert_eq!(
            invocation_mode(stdin, stderr),
            InvocationModeV1 { interactive }
        );
    }
}

/// Children of the observation controls, run only when invoked explicitly
/// by the parents below.
#[test]
#[ignore = "child of the pipe observation control"]
fn b1b_mode_child_not_interactive() {
    assert_eq!(
        observe_invocation_mode(),
        InvocationModeV1 { interactive: false }
    );
}
#[test]
#[ignore = "child of the pseudo-terminal observation control"]
fn b1b_mode_child_interactive() {
    assert_eq!(
        observe_invocation_mode(),
        InvocationModeV1 { interactive: true }
    );
}

fn child(name: &str) -> std::process::Command {
    let mut command = std::process::Command::new(std::env::current_exe().unwrap());
    command.args(["--ignored", "--exact", name, "--test-threads=1"]);
    command
}

#[test]
fn pipes_and_files_are_not_interactive() {
    let status = child("invocation_mode::tests::b1b_mode_child_not_interactive")
        .stdin(std::process::Stdio::piped())
        .stdout(std::process::Stdio::piped())
        .stderr(std::process::Stdio::piped())
        .status()
        .unwrap();
    assert!(status.success());
    let status = child("invocation_mode::tests::b1b_mode_child_not_interactive")
        .stdin(std::process::Stdio::null())
        .stdout(std::process::Stdio::null())
        .stderr(std::process::Stdio::null())
        .status()
        .unwrap();
    assert!(status.success());
}

#[test]
fn a_pseudo_terminal_on_both_streams_is_interactive() {
    // /usr/bin/script runs the child with its standard streams on a fresh
    // pseudo-terminal; the child's own assertion is the control.
    let exe = std::env::current_exe().unwrap();
    let output = std::process::Command::new("/usr/bin/script")
        .arg("-q")
        .arg("/dev/null")
        .arg(&exe)
        .args([
            "--ignored",
            "--exact",
            "invocation_mode::tests::b1b_mode_child_interactive",
            "--test-threads=1",
        ])
        .stdin(std::process::Stdio::null())
        .output()
        .unwrap();
    let transcript = String::from_utf8_lossy(&output.stdout);
    assert!(output.status.success(), "{transcript}");
    assert!(transcript.contains("1 passed"), "{transcript}");
}

#[test]
fn the_mode_reads_no_environment() {
    let source = include_str!("invocation_mode.rs");
    let production = source.split("#[cfg(test)]").next().unwrap();
    for forbidden in ["std::env", "env!", "var(", "var_os(", "vars("] {
        assert!(!production.contains(forbidden), "{forbidden}");
    }
}
