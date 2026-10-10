use crate::process_error::ProcessError;
use crate::read2;

use anyhow::{Context, Result, bail};
use jobserver::Client;
use shell_escape::escape;
use tempfile::NamedTempFile;

use std::collections::BTreeMap;
use std::env;
use std::ffi::{OsStr, OsString};
use std::fmt;
use std::io::{self, Write};
use std::iter::once;
use std::path::Path;
use std::process::{Command, ExitStatus, Output, Stdio};

/// A builder object for an external process, similar to [`std::process::Command`].
#[derive(Clone, Debug)]
pub struct ProcessBuilder {
    /// The program to execute.
    program: OsString,
    /// Best-effort replacement for arg0
    arg0: Option<OsString>,
    /// A list of arguments to pass to the program.
    args: Vec<OsString>,
    /// Any environment variables that should be set for the program.
    env: BTreeMap<String, Option<OsString>>,
    /// The directory to run the program from.
    cwd: Option<OsString>,
    /// A list of wrappers that wrap the original program when calling
    /// [`ProcessBuilder::wrapped`]. The last one is the outermost one.
    wrappers: Vec<OsString>,
    /// The `make` jobserver. See the [jobserver crate] for
    /// more information.
    ///
    /// [jobserver crate]: https://docs.rs/jobserver/
    jobserver: Option<Client>,
    /// `true` to include environment variable in display.
    display_env_vars: bool,
    /// `true` to retry with an argfile if hitting "command line too big" error.
    /// See [`ProcessBuilder::retry_with_argfile`] for more information.
    retry_with_argfile: bool,
    /// Data to write to stdin.
    stdin: Option<Vec<u8>>,
    experimental_query: Option<ExperimentalQuery>,
}

/// Outside-product experiment data, never a native executable capability.
#[derive(Clone, Debug)]
struct ExperimentalQuery {
    program: std::path::PathBuf,
    cwd: std::path::PathBuf,
    allowed_arguments: Vec<Vec<OsString>>,
    expected_sha256: String,
    output_root: std::path::PathBuf,
    next: std::sync::Arc<std::sync::atomic::AtomicUsize>,
    exact_environment: BTreeMap<String, OsString>,
    environment_registered: bool,
}

impl ExperimentalQuery {
    fn validate(&self, builder: &ProcessBuilder) {
        use sha2::{Digest, Sha256};
        assert_eq!(builder.program, self.program.as_os_str());
        assert_eq!(builder.get_cwd(), Some(self.cwd.as_path()));
        assert!(builder.wrappers.is_empty());
        assert!(builder.arg0.is_none());
        assert!(builder.jobserver.is_none());
        assert!(!builder.retry_with_argfile);
        assert!(builder.stdin.as_ref().is_none_or(|s| s.is_empty()));
        let supplied: BTreeMap<_, _> = builder
            .env
            .iter()
            .filter_map(|(k, v)| v.as_ref().map(|v| (k.clone(), v.clone())))
            .collect();
        assert_eq!(supplied, self.exact_environment);
        assert!(self.allowed_arguments.contains(&builder.args));
        let metadata =
            std::fs::symlink_metadata(&self.program).expect("experiment executable metadata");
        assert!(metadata.is_file() && !metadata.file_type().is_symlink());
        let mut file = std::fs::File::open(&self.program).expect("experiment executable read");
        let mut hasher = Sha256::new();
        let mut buffer = [0u8; 65536];
        loop {
            let count =
                std::io::Read::read(&mut file, &mut buffer).expect("experiment executable hash");
            if count == 0 {
                break;
            }
            hasher.update(&buffer[..count]);
        }
        assert_eq!(hex::encode(hasher.finalize()), self.expected_sha256);
    }
}

impl fmt::Display for ProcessBuilder {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "`")?;

        if self.display_env_vars {
            for (key, val) in self.env.iter() {
                if let Some(val) = val {
                    let val = escape(val.to_string_lossy());
                    if cfg!(windows) {
                        write!(f, "set {}={}&& ", key, val)?;
                    } else {
                        write!(f, "{}={} ", key, val)?;
                    }
                }
            }
        }

        write!(f, "{}", self.get_program().to_string_lossy())?;

        for arg in self.get_args() {
            write!(f, " {}", escape(arg.to_string_lossy()))?;
        }

        write!(f, "`")
    }
}

impl ProcessBuilder {
    /// Creates a new [`ProcessBuilder`] with the given executable path.
    pub fn new<T: AsRef<OsStr>>(cmd: T) -> ProcessBuilder {
        ProcessBuilder {
            program: cmd.as_ref().to_os_string(),
            arg0: None,
            args: Vec::new(),
            cwd: None,
            env: BTreeMap::new(),
            wrappers: Vec::new(),
            jobserver: None,
            display_env_vars: false,
            retry_with_argfile: false,
            stdin: None,
            experimental_query: None,
        }
    }

    /// Explicit experiment-only exact query vectors. Supplied pins and paths
    /// are data, not authenticated ownership or runtime closure. No cache.
    pub fn experimental_information_queries(
        program: &Path,
        cwd: &Path,
        allowed_arguments: Vec<Vec<OsString>>,
        expected_sha256: String,
        output_root: &Path,
    ) -> ProcessBuilder {
        assert!(program.is_absolute() && cwd.is_absolute() && output_root.is_absolute());
        assert!(!allowed_arguments.is_empty());
        let mut builder = Self::new(program);
        builder.cwd(cwd);
        builder.experimental_query = Some(ExperimentalQuery {
            program: program.to_path_buf(),
            cwd: cwd.to_path_buf(),
            allowed_arguments,
            expected_sha256,
            output_root: output_root.to_path_buf(),
            next: std::sync::Arc::new(std::sync::atomic::AtomicUsize::new(0)),
            exact_environment: BTreeMap::new(),
            environment_registered: false,
        });
        builder
    }

    /// Separate outside-product original-configuration DATA registration.
    /// The default constructor still requires an empty set environment.
    pub fn experimental_register_original_environment(
        &mut self,
        values: BTreeMap<String, OsString>,
    ) {
        assert!(values.keys().all(|k| matches!(
            k.as_str(),
            "MACOSX_DEPLOYMENT_TARGET" | "CARGO_WORKSPACE_DIR"
        )));
        let guard = self
            .experimental_query
            .as_mut()
            .expect("not an experimental query instance");
        assert!(!guard.environment_registered);
        assert_eq!(guard.next.load(std::sync::atomic::Ordering::Relaxed), 0);
        assert!(self.env.values().all(Option::is_none));
        guard.environment_registered = true;
        // Registration creates a fresh experiment association. Earlier clones
        // cannot reuse it by retaining the old counter identity.
        guard.next = std::sync::Arc::new(std::sync::atomic::AtomicUsize::new(0));
        guard.exact_environment = values.clone();
        for (key, value) in values {
            self.env.insert(key, Some(value));
        }
    }

    /// Require the same experiment instance before this branch consumes a
    /// supplied command. Equal strings or bytes from another instance do not
    /// grant reuse of the first instance's registered query set.
    pub fn experimental_output_for(&self, base: &ProcessBuilder) -> Result<Output> {
        let Some(own) = &self.experimental_query else {
            bail!("command has no experiment query association");
        };
        let Some(expected) = &base.experimental_query else {
            bail!("base has no experiment query association");
        };
        if !std::sync::Arc::ptr_eq(&own.next, &expected.next) {
            bail!("foreign experiment query association");
        }
        self.exec_with_output()
    }

    /// (chainable) Sets the executable for the process.
    pub fn program<T: AsRef<OsStr>>(&mut self, program: T) -> &mut ProcessBuilder {
        self.program = program.as_ref().to_os_string();
        self
    }

    /// (chainable) Overrides `arg0` for this program.
    pub fn arg0<T: AsRef<OsStr>>(&mut self, arg: T) -> &mut ProcessBuilder {
        self.arg0 = Some(arg.as_ref().to_os_string());
        self
    }

    /// (chainable) Adds `arg` to the args list.
    pub fn arg<T: AsRef<OsStr>>(&mut self, arg: T) -> &mut ProcessBuilder {
        self.args.push(arg.as_ref().to_os_string());
        self
    }

    /// (chainable) Adds multiple `args` to the args list.
    pub fn args<T: AsRef<OsStr>>(&mut self, args: &[T]) -> &mut ProcessBuilder {
        self.args
            .extend(args.iter().map(|t| t.as_ref().to_os_string()));
        self
    }

    /// (chainable) Replaces the args list with the given `args`.
    pub fn args_replace<T: AsRef<OsStr>>(&mut self, args: &[T]) -> &mut ProcessBuilder {
        if let Some(program) = self.wrappers.pop() {
            // User intend to replace all args, so we
            // - use the outermost wrapper as the main program, and
            // - cleanup other inner wrappers.
            self.program = program;
            self.wrappers = Vec::new();
        }
        self.args = args.iter().map(|t| t.as_ref().to_os_string()).collect();
        self
    }

    /// (chainable) Sets the current working directory of the process.
    pub fn cwd<T: AsRef<OsStr>>(&mut self, path: T) -> &mut ProcessBuilder {
        self.cwd = Some(path.as_ref().to_os_string());
        self
    }

    /// (chainable) Sets an environment variable for the process.
    pub fn env<T: AsRef<OsStr>>(&mut self, key: &str, val: T) -> &mut ProcessBuilder {
        self.env
            .insert(key.to_string(), Some(val.as_ref().to_os_string()));
        self
    }

    /// (chainable) Unsets an environment variable for the process.
    pub fn env_remove(&mut self, key: &str) -> &mut ProcessBuilder {
        self.env.insert(key.to_string(), None);
        self
    }

    /// Gets the executable name.
    pub fn get_program(&self) -> &OsString {
        self.wrappers.last().unwrap_or(&self.program)
    }

    /// Gets the program arg0.
    pub fn get_arg0(&self) -> Option<&OsStr> {
        self.arg0.as_deref()
    }

    /// Gets the program arguments.
    pub fn get_args(&self) -> impl Iterator<Item = &OsString> {
        self.wrappers
            .iter()
            .rev()
            .chain(once(&self.program))
            .chain(self.args.iter())
            .skip(1) // Skip the main `program
    }

    /// Gets the current working directory for the process.
    pub fn get_cwd(&self) -> Option<&Path> {
        self.cwd.as_ref().map(Path::new)
    }

    /// Gets an environment variable as the process will see it (will inherit from environment
    /// unless explicitly unset).
    pub fn get_env(&self, var: &str) -> Option<OsString> {
        self.env
            .get(var)
            .cloned()
            .or_else(|| Some(env::var_os(var)))
            .and_then(|s| s)
    }

    /// Gets all environment variables explicitly set or unset for the process (not inherited
    /// vars).
    pub fn get_envs(&self) -> &BTreeMap<String, Option<OsString>> {
        &self.env
    }

    /// Sets the `make` jobserver. See the [jobserver crate][jobserver_docs] for
    /// more information.
    ///
    /// [jobserver_docs]: https://docs.rs/jobserver/latest/jobserver/
    pub fn inherit_jobserver(&mut self, jobserver: &Client) -> &mut Self {
        self.jobserver = Some(jobserver.clone());
        self
    }

    /// Enables environment variable display.
    pub fn display_env_vars(&mut self) -> &mut Self {
        self.display_env_vars = true;
        self
    }

    /// Enables retrying with an argfile if hitting "command line too big" error
    ///
    /// This is primarily for the `@path` arg of rustc and rustdoc, which treat
    /// each line as an command-line argument, so `LF` and `CRLF` bytes are not
    /// valid as an argument for argfile at this moment.
    /// For example, `RUSTDOCFLAGS="--crate-version foo\nbar" cargo doc` is
    /// valid when invoking from command-line but not from argfile.
    ///
    /// To sum up, the limitations of the argfile are:
    ///
    /// - Must be valid UTF-8 encoded.
    /// - Must not contain any newlines in each argument.
    ///
    /// Ref:
    ///
    /// - <https://doc.rust-lang.org/rustdoc/command-line-arguments.html#path-load-command-line-flags-from-a-path>
    /// - <https://doc.rust-lang.org/rustc/command-line-arguments.html#path-load-command-line-flags-from-a-path>
    pub fn retry_with_argfile(&mut self, enabled: bool) -> &mut Self {
        self.retry_with_argfile = enabled;
        self
    }

    /// Sets a value that will be written to stdin of the process on launch.
    pub fn stdin<T: Into<Vec<u8>>>(&mut self, stdin: T) -> &mut Self {
        self.stdin = Some(stdin.into());
        self
    }

    fn should_retry_with_argfile(&self, err: &io::Error) -> bool {
        self.retry_with_argfile && imp::command_line_too_big(err)
    }

    /// Like [`Command::status`] but with a better error message.
    pub fn status(&self) -> Result<ExitStatus> {
        self._status()
            .with_context(|| ProcessError::could_not_execute(self))
    }

    fn _status(&self) -> io::Result<ExitStatus> {
        if !debug_force_argfile(self.retry_with_argfile) {
            let mut cmd = self.build_command();
            match cmd.spawn() {
                Err(ref e) if self.should_retry_with_argfile(e) => {}
                Err(e) => return Err(e),
                Ok(mut child) => return child.wait(),
            }
        }
        let (mut cmd, argfile) = self.build_command_with_argfile()?;
        let status = cmd.spawn()?.wait();
        close_tempfile_and_log_error(argfile);
        status
    }

    /// Runs the process, waiting for completion, and mapping non-success exit codes to an error.
    pub fn exec(&self) -> Result<()> {
        let exit = self.status()?;
        if exit.success() {
            Ok(())
        } else {
            Err(ProcessError::new(
                &format!("process didn't exit successfully: {}", self),
                Some(exit),
                None,
            )
            .into())
        }
    }

    /// Replaces the current process with the target process.
    ///
    /// On Unix, this executes the process using the Unix syscall `execvp`, which will block
    /// this process, and will only return if there is an error.
    ///
    /// On Windows this isn't technically possible. Instead we emulate it to the best of our
    /// ability. One aspect we fix here is that we specify a handler for the Ctrl-C handler.
    /// In doing so (and by effectively ignoring it) we should emulate proxying Ctrl-C
    /// handling to the application at hand, which will either terminate or handle it itself.
    /// According to Microsoft's documentation at
    /// <https://docs.microsoft.com/en-us/windows/console/ctrl-c-and-ctrl-break-signals>.
    /// the Ctrl-C signal is sent to all processes attached to a terminal, which should
    /// include our child process. If the child terminates then we'll reap them in Cargo
    /// pretty quickly, and if the child handles the signal then we won't terminate
    /// (and we shouldn't!) until the process itself later exits.
    pub fn exec_replace(&self) -> Result<()> {
        imp::exec_replace(self)
    }

    /// Like [`Command::output`] but with a better error message.
    pub fn output(&self) -> Result<Output> {
        self._output()
            .with_context(|| ProcessError::could_not_execute(self))
    }

    fn _output(&self) -> io::Result<Output> {
        if let Some(guard) = &self.experimental_query {
            guard.validate(self);
            let ordinal = guard
                .next
                .fetch_add(1, std::sync::atomic::Ordering::Relaxed);
            let prefix = guard.output_root.join(format!("query-{ordinal}"));
            let mut environment_file = std::fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(prefix.with_extension("environment"))?;
            environment_file.write_all(&(guard.exact_environment.len() as u64).to_be_bytes())?;
            for (key, value) in &guard.exact_environment {
                #[cfg(unix)]
                {
                    use std::os::unix::ffi::OsStrExt;
                    for bytes in [key.as_bytes(), value.as_os_str().as_bytes()] {
                        environment_file.write_all(&(bytes.len() as u64).to_be_bytes())?;
                        environment_file.write_all(bytes)?;
                    }
                }
            }
            let mut args_file = std::fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(prefix.with_extension("arguments"))?;
            for arg in &self.args {
                #[cfg(unix)]
                {
                    use std::os::unix::ffi::OsStrExt;
                    let bytes = arg.as_os_str().as_bytes();
                    args_file.write_all(&(bytes.len() as u64).to_be_bytes())?;
                    args_file.write_all(bytes)?;
                }
            }
            let mut stdout = std::fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(prefix.with_extension("stdout"))?;
            let mut stderr = std::fs::OpenOptions::new()
                .write(true)
                .create_new(true)
                .open(prefix.with_extension("stderr"))?;
            let mut command = self.build_command();
            command
                .stdin(Stdio::null())
                .stdout(stdout.try_clone()?)
                .stderr(stderr.try_clone()?);
            let status = command.status()?;
            stdout.flush()?;
            stderr.flush()?;
            std::fs::write(prefix.with_extension("status"), format!("{status}\n"))?;
            guard.validate(self);
            return Ok(Output {
                status,
                stdout: std::fs::read(prefix.with_extension("stdout"))?,
                stderr: std::fs::read(prefix.with_extension("stderr"))?,
            });
        }
        if !debug_force_argfile(self.retry_with_argfile) {
            let mut cmd = self.build_command();
            match piped(&mut cmd, self.stdin.is_some()).spawn() {
                Err(ref e) if self.should_retry_with_argfile(e) => {}
                Err(e) => return Err(e),
                Ok(mut child) => {
                    if let Some(stdin) = &self.stdin {
                        child.stdin.take().unwrap().write_all(stdin)?;
                    }
                    return child.wait_with_output();
                }
            }
        }
        let (mut cmd, argfile) = self.build_command_with_argfile()?;
        let mut child = piped(&mut cmd, self.stdin.is_some()).spawn()?;
        if let Some(stdin) = &self.stdin {
            child.stdin.take().unwrap().write_all(stdin)?;
        }
        let output = child.wait_with_output();
        close_tempfile_and_log_error(argfile);
        output
    }

    /// Executes the process, returning the stdio output, or an error if non-zero exit status.
    pub fn exec_with_output(&self) -> Result<Output> {
        let output = self.output()?;
        if output.status.success() {
            Ok(output)
        } else {
            Err(ProcessError::new(
                &format!("process didn't exit successfully: {}", self),
                Some(output.status),
                Some(&output),
            )
            .into())
        }
    }

    /// Executes a command, passing each line of stdout and stderr to the supplied callbacks, which
    /// can mutate the string data.
    ///
    /// If any invocations of these function return an error, it will be propagated.
    ///
    /// If `capture_output` is true, then all the output will also be buffered
    /// and stored in the returned `Output` object. If it is false, no caching
    /// is done, and the callbacks are solely responsible for handling the
    /// output.
    pub fn exec_with_streaming(
        &self,
        on_stdout_line: &mut dyn FnMut(&str) -> Result<()>,
        on_stderr_line: &mut dyn FnMut(&str) -> Result<()>,
        capture_output: bool,
    ) -> Result<Output> {
        let mut stdout = Vec::new();
        let mut stderr = Vec::new();

        let mut callback_error = None;
        let mut stdout_pos = 0;
        let mut stderr_pos = 0;

        let spawn = |mut cmd| {
            if !debug_force_argfile(self.retry_with_argfile) {
                match piped(&mut cmd, false).spawn() {
                    Err(ref e) if self.should_retry_with_argfile(e) => {}
                    Err(e) => return Err(e),
                    Ok(child) => return Ok((child, None)),
                }
            }
            let (mut cmd, argfile) = self.build_command_with_argfile()?;
            Ok((piped(&mut cmd, false).spawn()?, Some(argfile)))
        };

        let status = (|| {
            let cmd = self.build_command();
            let (mut child, argfile) = spawn(cmd)?;
            let out = child.stdout.take().unwrap();
            let err = child.stderr.take().unwrap();
            read2(out, err, &mut |is_out, data, eof| {
                let pos = if is_out {
                    &mut stdout_pos
                } else {
                    &mut stderr_pos
                };
                let idx = if eof {
                    data.len()
                } else {
                    match data[*pos..].iter().rposition(|b| *b == b'\n') {
                        Some(i) => *pos + i + 1,
                        None => {
                            *pos = data.len();
                            return;
                        }
                    }
                };

                let new_lines = &data[..idx];

                for line in String::from_utf8_lossy(new_lines).lines() {
                    if callback_error.is_some() {
                        break;
                    }
                    let callback_result = if is_out {
                        on_stdout_line(line)
                    } else {
                        on_stderr_line(line)
                    };
                    if let Err(e) = callback_result {
                        callback_error = Some(e);
                        break;
                    }
                }

                if capture_output {
                    let dst = if is_out { &mut stdout } else { &mut stderr };
                    dst.extend(new_lines);
                }

                data.drain(..idx);
                *pos = 0;
            })?;
            let status = child.wait();
            if let Some(argfile) = argfile {
                close_tempfile_and_log_error(argfile);
            }
            status
        })()
        .with_context(|| ProcessError::could_not_execute(self))?;
        let output = Output {
            status,
            stdout,
            stderr,
        };

        {
            let to_print = if capture_output { Some(&output) } else { None };
            if let Some(e) = callback_error {
                let cx = ProcessError::new(
                    &format!("failed to parse process output: {}", self),
                    Some(output.status),
                    to_print,
                );
                bail!(anyhow::Error::new(cx).context(e));
            } else if !output.status.success() {
                bail!(ProcessError::new(
                    &format!("process didn't exit successfully: {}", self),
                    Some(output.status),
                    to_print,
                ));
            }
        }

        Ok(output)
    }

    /// Builds the command with an `@<path>` argfile that contains all the
    /// arguments. This is primarily served for rustc/rustdoc command family.
    fn build_command_with_argfile(&self) -> io::Result<(Command, NamedTempFile)> {
        use std::io::Write as _;

        let mut tmp = tempfile::Builder::new()
            .prefix("cargo-argfile.")
            .tempfile()?;

        let mut arg = OsString::from("@");
        arg.push(tmp.path());
        let mut cmd = self.build_command_without_args();
        cmd.arg(arg);
        tracing::debug!("created argfile at {} for {self}", tmp.path().display());

        let cap = self.get_args().map(|arg| arg.len() + 1).sum::<usize>();
        let mut buf = Vec::with_capacity(cap);
        for arg in &self.args {
            let arg = arg.to_str().ok_or_else(|| {
                io::Error::new(
                    io::ErrorKind::Other,
                    format!(
                        "argument for argfile contains invalid UTF-8 characters: `{}`",
                        arg.to_string_lossy()
                    ),
                )
            })?;
            if arg.contains('\n') {
                return Err(io::Error::new(
                    io::ErrorKind::Other,
                    format!("argument for argfile contains newlines: `{arg}`"),
                ));
            }
            writeln!(buf, "{arg}")?;
        }
        tmp.write_all(&mut buf)?;
        Ok((cmd, tmp))
    }

    /// Builds a command from `ProcessBuilder` for everything but not `args`.
    fn build_command_without_args(&self) -> Command {
        let mut command = {
            let mut iter = self.wrappers.iter().rev().chain(once(&self.program));
            let mut cmd = Command::new(iter.next().expect("at least one `program` exists"));
            cmd.args(iter);
            cmd
        };
        if let Some(guard) = &self.experimental_query {
            guard.validate(self);
            command.env_clear();
        }
        #[cfg(unix)]
        if let Some(arg0) = self.get_arg0() {
            use std::os::unix::process::CommandExt as _;
            command.arg0(arg0);
        }
        if let Some(cwd) = self.get_cwd() {
            command.current_dir(cwd);
        }
        for (k, v) in &self.env {
            match *v {
                Some(ref v) => {
                    command.env(k, v);
                }
                None => {
                    command.env_remove(k);
                }
            }
        }
        if let Some(ref c) = self.jobserver {
            c.configure(&mut command);
        }
        command
    }

    /// Converts `ProcessBuilder` into a `std::process::Command`, and handles
    /// the jobserver, if present.
    ///
    /// Note that this method doesn't take argfile fallback into account. The
    /// caller should handle it by themselves.
    pub fn build_command(&self) -> Command {
        let mut command = self.build_command_without_args();
        for arg in &self.args {
            command.arg(arg);
        }
        command
    }

    /// Wraps an existing command with the provided wrapper, if it is present and valid.
    ///
    /// # Examples
    ///
    /// ```rust
    /// use cargo_util::ProcessBuilder;
    /// // Running this would execute `rustc`
    /// let cmd = ProcessBuilder::new("rustc");
    ///
    /// // Running this will execute `sccache rustc`
    /// let cmd = cmd.wrapped(Some("sccache"));
    /// ```
    pub fn wrapped(mut self, wrapper: Option<impl AsRef<OsStr>>) -> Self {
        if let Some(wrapper) = wrapper.as_ref() {
            let wrapper = wrapper.as_ref();
            if !wrapper.is_empty() {
                self.wrappers.push(wrapper.to_os_string());
            }
        }
        self
    }
}

/// Forces the command to use `@path` argfile.
///
/// You should set `__CARGO_TEST_FORCE_ARGFILE` to enable this.
fn debug_force_argfile(retry_enabled: bool) -> bool {
    cfg!(debug_assertions) && env::var("__CARGO_TEST_FORCE_ARGFILE").is_ok() && retry_enabled
}

/// Creates new pipes for stderr, stdout, and optionally stdin.
fn piped(cmd: &mut Command, pipe_stdin: bool) -> &mut Command {
    cmd.stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .stdin(if pipe_stdin {
            Stdio::piped()
        } else {
            Stdio::null()
        })
}

fn close_tempfile_and_log_error(file: NamedTempFile) {
    file.close().unwrap_or_else(|e| {
        tracing::warn!("failed to close temporary file: {e}");
    });
}

#[cfg(unix)]
mod imp {
    use super::{ProcessBuilder, ProcessError, close_tempfile_and_log_error, debug_force_argfile};
    use anyhow::Result;
    use std::io;
    use std::os::unix::process::CommandExt;

    pub fn exec_replace(process_builder: &ProcessBuilder) -> Result<()> {
        let mut error;
        let mut file = None;
        if debug_force_argfile(process_builder.retry_with_argfile) {
            let (mut command, argfile) = process_builder.build_command_with_argfile()?;
            file = Some(argfile);
            error = command.exec()
        } else {
            let mut command = process_builder.build_command();
            error = command.exec();
            if process_builder.should_retry_with_argfile(&error) {
                let (mut command, argfile) = process_builder.build_command_with_argfile()?;
                file = Some(argfile);
                error = command.exec()
            }
        }
        if let Some(file) = file {
            close_tempfile_and_log_error(file);
        }

        Err(anyhow::Error::from(error).context(ProcessError::new(
            &format!("could not execute process {}", process_builder),
            None,
            None,
        )))
    }

    pub fn command_line_too_big(err: &io::Error) -> bool {
        err.raw_os_error() == Some(libc::E2BIG)
    }
}

#[cfg(windows)]
mod imp {
    use super::{ProcessBuilder, ProcessError};
    use anyhow::Result;
    use std::io;
    use windows_sys::Win32::Foundation::{FALSE, TRUE};
    use windows_sys::Win32::System::Console::SetConsoleCtrlHandler;
    use windows_sys::core::BOOL;

    unsafe extern "system" fn ctrlc_handler(_: u32) -> BOOL {
        // Do nothing; let the child process handle it.
        TRUE
    }

    pub fn exec_replace(process_builder: &ProcessBuilder) -> Result<()> {
        unsafe {
            if SetConsoleCtrlHandler(Some(ctrlc_handler), TRUE) == FALSE {
                return Err(ProcessError::new("Could not set Ctrl-C handler.", None, None).into());
            }
        }

        // Just execute the process as normal.
        process_builder.exec()
    }

    pub fn command_line_too_big(err: &io::Error) -> bool {
        use windows_sys::Win32::Foundation::ERROR_FILENAME_EXCED_RANGE;
        err.raw_os_error() == Some(ERROR_FILENAME_EXCED_RANGE as i32)
    }
}

#[cfg(test)]
mod tests {
    use super::ProcessBuilder;
    use std::fs;

    #[test]
    fn argfile_build_succeeds() {
        let mut cmd = ProcessBuilder::new("echo");
        cmd.args(["foo", "bar"].as_slice());
        let (cmd, argfile) = cmd.build_command_with_argfile().unwrap();

        assert_eq!(cmd.get_program(), "echo");
        let cmd_args: Vec<_> = cmd.get_args().map(|s| s.to_str().unwrap()).collect();
        assert_eq!(cmd_args.len(), 1);
        assert!(cmd_args[0].starts_with("@"));
        assert!(cmd_args[0].contains("cargo-argfile."));

        let buf = fs::read_to_string(argfile.path()).unwrap();
        assert_eq!(buf, "foo\nbar\n");
    }

    #[test]
    fn argfile_build_fails_if_arg_contains_newline() {
        let mut cmd = ProcessBuilder::new("echo");
        cmd.arg("foo\n");
        let err = cmd.build_command_with_argfile().unwrap_err();
        assert_eq!(
            err.to_string(),
            "argument for argfile contains newlines: `foo\n`"
        );
    }

    #[test]
    fn argfile_build_fails_if_arg_contains_invalid_utf8() {
        let mut cmd = ProcessBuilder::new("echo");

        #[cfg(windows)]
        let invalid_arg = {
            use std::os::windows::prelude::*;
            std::ffi::OsString::from_wide(&[0x0066, 0x006f, 0xD800, 0x006f])
        };

        #[cfg(unix)]
        let invalid_arg = {
            use std::os::unix::ffi::OsStrExt;
            std::ffi::OsStr::from_bytes(&[0x66, 0x6f, 0x80, 0x6f]).to_os_string()
        };

        cmd.arg(invalid_arg);
        let err = cmd.build_command_with_argfile().unwrap_err();
        assert_eq!(
            err.to_string(),
            "argument for argfile contains invalid UTF-8 characters: `fo�o`"
        );
    }
}

#[cfg(test)]
mod experimental_information_tests {
    use super::*;
    fn prepared(root: &Path) -> ProcessBuilder {
        ProcessBuilder::experimental_information_queries(
            Path::new("/tmp/opensip-implementation/sm-compiler-query-kernel-2026-10-10/probe"),
            root,
            vec![vec![OsString::from("-vV")]],
            "1e177c008a0cfb448d942062de33c080b1248dd8d8d763fe51f3f848690b5436".to_owned(),
            root,
        )
    }
    #[test]
    fn actual_empty_environment_eof_cwd_and_retained_output() {
        let root = tempfile::Builder::new()
            .prefix("opensip-query-process-control-")
            .tempdir()
            .unwrap()
            .keep();
        let mut builder = prepared(&root);
        builder.arg("-vV");
        let output = builder.exec_with_output().unwrap();
        let text = String::from_utf8(output.stdout.clone()).unwrap();
        assert!(text.contains("ENV_COUNT=0\n"));
        assert!(text.contains("STDIN_BYTES=0\n"));
        assert!(text.contains("ARGS=[\"-vV\"]\n"));
        let observed = text.lines().find_map(|l| l.strip_prefix("CWD=")).unwrap();
        assert!(same_file::is_same_file(observed, root.as_path()).unwrap());
        assert_eq!(
            std::fs::read(root.as_path().join("query-0.stdout")).unwrap(),
            output.stdout
        );
        assert!(root.as_path().join("query-0.arguments").is_file());
        assert!(root.as_path().join("query-0.status").is_file());
        let again = builder.exec_with_output().unwrap();
        assert!(again.status.success());
        assert!(root.as_path().join("query-1.stdout").is_file());
        // Retain the actual controls outside the ephemeral TempDir owner.
        let retained = root;
        eprintln!("ACTUAL_EXPERIMENT_QUERY_CONTROL={}", retained.display());
    }
    #[test]
    fn unregistered_arguments_refused_before_any_output() {
        let root = tempfile::tempdir().unwrap();
        let mut builder = prepared(root.path());
        builder.arg("--print=target-spec-json");
        assert!(
            std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| builder.output())).is_err()
        );
        assert_eq!(std::fs::read_dir(root.path()).unwrap().count(), 0);
    }
    #[test]
    fn executable_override_wrapper_environment_and_argfile_refused() {
        let root = tempfile::tempdir().unwrap();
        for variant in 0..4 {
            let mut builder = prepared(root.path());
            builder.arg("-vV");
            match variant {
                0 => {
                    builder.program("/usr/bin/false");
                }
                1 => {
                    builder = builder.wrapped(Some(Path::new("/usr/bin/env")));
                }
                2 => {
                    builder.env("TMPDIR", root.path());
                }
                _ => {
                    builder.retry_with_argfile(true);
                }
            }
            assert!(
                std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| builder.output()))
                    .is_err()
            );
        }
        assert_eq!(std::fs::read_dir(root.path()).unwrap().count(), 0);
    }
    #[test]
    fn foreign_equal_and_ordinary_commands_refused_before_output() {
        let root = tempfile::tempdir().unwrap();
        let base = prepared(root.path());
        let mut equal = prepared(root.path());
        equal.arg("-vV");
        assert!(equal.experimental_output_for(&base).is_err());
        let mut ordinary = ProcessBuilder::new(base.get_program());
        ordinary.arg("-vV").cwd(root.path());
        assert!(ordinary.experimental_output_for(&base).is_err());
        assert_eq!(std::fs::read_dir(root.path()).unwrap().count(), 0);
    }
    #[test]
    fn mismatched_pin_refused_before_any_output() {
        let root = tempfile::tempdir().unwrap();
        let mut builder = prepared(root.path());
        builder.experimental_query.as_mut().unwrap().expected_sha256 = "0".repeat(64);
        builder.arg("-vV");
        assert!(
            std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| builder.output())).is_err()
        );
        assert_eq!(std::fs::read_dir(root.path()).unwrap().count(), 0);
    }

    #[test]
    fn original_environment_exact_values_and_no_ambient_environment() {
        let root = tempfile::Builder::new()
            .prefix("opensip-original-env-control-")
            .tempdir()
            .unwrap()
            .keep();
        let mut builder = prepared(&root);
        builder.experimental_register_original_environment(BTreeMap::from([
            ("MACOSX_DEPLOYMENT_TARGET".into(), "12.0".into()),
            ("CARGO_WORKSPACE_DIR".into(), root.as_os_str().to_owned()),
        ]));
        builder.arg("-vV");
        let output = builder.exec_with_output().unwrap();
        let text = String::from_utf8(output.stdout).unwrap();
        assert!(
            output.status.success()
                && text.contains("ENV_COUNT=2\n")
                && text.contains("STDIN_BYTES=0\n")
                && text.contains("ARGS=[\"-vV\"]\n")
        );
        let retained = std::fs::read(root.join("query-0.environment")).unwrap();
        assert_eq!(u64::from_be_bytes(retained[..8].try_into().unwrap()), 2);
        assert!(retained.windows(4).any(|w| w == b"12.0"));
        eprintln!(
            "ACTUAL_ORIGINAL_ENVIRONMENT_QUERY_CONTROL={}",
            root.display()
        );
    }
    #[test]
    fn original_environment_changed_value_refused_before_output() {
        let root = tempfile::tempdir().unwrap();
        let mut builder = prepared(root.path());
        builder.experimental_register_original_environment(BTreeMap::from([(
            "MACOSX_DEPLOYMENT_TARGET".into(),
            "12.0".into(),
        )]));
        builder.env("MACOSX_DEPLOYMENT_TARGET", "13.0").arg("-vV");
        assert!(
            std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| builder.output())).is_err()
        );
        assert_eq!(std::fs::read_dir(root.path()).unwrap().count(), 0);
    }
    #[test]
    fn original_environment_home_registration_refused() {
        let root = tempfile::tempdir().unwrap();
        let mut builder = prepared(root.path());
        assert!(
            std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| builder
                .experimental_register_original_environment(BTreeMap::from([(
                    "HOME".into(),
                    "/synthetic/forbidden".into()
                )]))))
            .is_err()
        );
        assert_eq!(std::fs::read_dir(root.path()).unwrap().count(), 0);
    }
    #[test]
    fn original_environment_other_arguments_remain_refused() {
        let root = tempfile::tempdir().unwrap();
        let mut builder = prepared(root.path());
        builder.experimental_register_original_environment(BTreeMap::from([(
            "MACOSX_DEPLOYMENT_TARGET".into(),
            "12.0".into(),
        )]));
        builder.arg("--print=target-spec-json");
        assert!(
            std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| builder.output())).is_err()
        );
        assert_eq!(std::fs::read_dir(root.path()).unwrap().count(), 0);
    }
    #[test]
    fn original_environment_registration_creates_new_association() {
        let root = tempfile::tempdir().unwrap();
        let base = prepared(root.path());
        let mut changed = base.clone();
        changed.experimental_register_original_environment(BTreeMap::from([(
            "MACOSX_DEPLOYMENT_TARGET".into(),
            "12.0".into(),
        )]));
        changed.arg("-vV");
        assert!(changed.experimental_output_for(&base).is_err());
        assert_eq!(std::fs::read_dir(root.path()).unwrap().count(), 0);
    }
}
