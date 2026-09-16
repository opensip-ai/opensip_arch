"""Confined preparation child: derive schema documents by $id and run prepare.prepare.

The parent invokes this only as

  <pinned Python.app interpreter> -I -B -S prepare-inputs.py RAW_SCHEMAS OPTIONS CODE_DIR OUTPUT_DIR

under its rendered deny-default sandbox profile. RAW_SCHEMAS is a JSON array of raw
schema JSON strings, OPTIONS the recipe options, CODE_DIR the designated directory
holding prepare.py and runtime/schema.ts, and OUTPUT_DIR an empty writable root.
The child creates only the three prepared files the generator steps consume. The
parent keeps pin verification, merged-input construction (its own options,
raw schemas and provenance) and lstat/O_NOFOLLOW collection after exit; nothing
here is trusted by the parent, and the Sink below is not a security boundary.
"""
import json
import os
import stat
import sys

EMITTED = ('owners.json', 'rust-projection.json', 'ts-projection.json')
# prepare.prepare also writes targets.json. No generator step reads it, so it is
# dropped here rather than widening the collected output set.
DISCARDED = ('targets.json',)
DIALECT = 'https://json-schema.org/draft/2020-12/schema'
MAX_INPUT_BYTES = 1 << 26


class PrepareInputsError(ValueError):
    pass


def require_isolated():
    flags = sys.flags
    if not (flags.isolated and flags.ignore_environment and flags.no_user_site and flags.no_site
            and flags.dont_write_bytecode and flags.safe_path) or flags.optimize or 'site' in sys.modules:
        raise PrepareInputsError('invoke Python with -I -B -S and without optimization')
    if any('site-packages' in entry for entry in sys.path):
        raise PrepareInputsError('site-packages on the import path')


def decode(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise PrepareInputsError('duplicate JSON key: ' + key)
            result[key] = value
        return result

    def forbidden(_):
        raise PrepareInputsError('noninteger JSON number in preparation input')
    return json.loads(raw, object_pairs_hook=pairs, parse_float=forbidden, parse_constant=forbidden)


def read_regular(path):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise PrepareInputsError('input is not a regular file: ' + path)
        chunks, remaining = [], MAX_INPUT_BYTES + 1
        while remaining > 0:
            chunk = os.read(fd, min(remaining, 1 << 20))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        if remaining <= 0:
            raise PrepareInputsError('input byte limit exceeded: ' + path)
        return b''.join(chunks)
    finally:
        os.close(fd)


def documents(raw):
    values = decode(raw)
    if type(values) is not list or not values or any(type(v) is not str for v in values):
        raise PrepareInputsError('raw schemas must be a nonempty array of JSON strings')
    result = {}
    for text in values:
        document = decode(text)
        if type(document) is not dict or type(document.get('$id')) is not str or not document['$id'] \
                or document.get('$schema') != DIALECT:
            raise PrepareInputsError('schema document identity/dialect invalid')
        if document['$id'] in result:
            raise PrepareInputsError('duplicate schema $id: ' + document['$id'])
        result[document['$id']] = document
    return result


def load_prepare(code_dir):
    # Executed from its exact bytes: no import machinery, no bytecode cache.
    path = os.path.join(code_dir, 'prepare.py')
    module = type(sys)('opensip_prepare')
    module.__file__ = path
    exec(compile(read_regular(path), path, 'exec', dont_inherit=True), module.__dict__)
    if not callable(getattr(module, 'prepare', None)):
        raise PrepareInputsError('prepare.py defines no prepare()')
    return module


class Sink:
    """Destination handed to prepare.prepare: collects its write_text calls in memory."""

    def __init__(self):
        self.files = {}

    def __truediv__(self, name):
        return SinkFile(self.files, name)


class SinkFile:
    def __init__(self, files, name):
        self.files, self.name = files, name

    def write_text(self, data, encoding=None, errors=None, newline=None):
        if type(self.name) is not str or self.name not in EMITTED + DISCARDED or self.name in self.files:
            raise PrepareInputsError('unexpected prepared output: ' + repr(self.name))
        if type(data) is not str or not data.isascii() or (encoding, errors, newline) != (None, None, None):
            raise PrepareInputsError('prepared output is not plain ASCII text: ' + self.name)
        self.files[self.name] = data.encode('ascii')
        return len(data)


def open_empty_directory(path):
    directory = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    if os.listdir(directory):
        os.close(directory)
        raise PrepareInputsError('output root is not empty')
    return directory


def emit(output_dir, files):
    directory = open_empty_directory(output_dir)
    try:
        for name in EMITTED:
            fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644, dir_fd=directory)
            try:
                view = memoryview(files[name])
                while view:
                    view = view[os.write(fd, view):]
            finally:
                os.close(fd)
    finally:
        os.close(directory)


def main(argv):
    require_isolated()
    if len(argv) != 5 or not all(os.path.isabs(arg) for arg in argv[1:]):
        raise PrepareInputsError('usage: prepare-inputs.py RAW_SCHEMAS OPTIONS CODE_DIR OUTPUT_DIR (absolute)')
    raw_path, options_path, code_dir, output_dir = argv[1:]
    os.close(open_empty_directory(output_dir))
    schema_documents = documents(read_regular(raw_path))
    options = decode(read_regular(options_path))
    if type(options) is not dict:
        raise PrepareInputsError('options must be an object')
    sink = Sink()
    load_prepare(code_dir).prepare(schema_documents, options, sink)
    if set(sink.files) != set(EMITTED + DISCARDED):
        raise PrepareInputsError('prepare emitted a different output set')
    emit(output_dir, sink.files)


if __name__ == '__main__':
    try:
        main(sys.argv)
    except Exception as error:
        sys.stderr.write('prepare-inputs: ' + type(error).__name__ + ': ' + str(error)[:500] + '\n')
        sys.exit(1)
