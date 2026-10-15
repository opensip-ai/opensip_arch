"""Drift and mutation controls for the host configuration registries and PCM vectors (M3-B r4 item 8; unit B1-a)."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
ARCH = ROOT.parent / "opensip_arch"
RUSTFMT = "/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tables = load("configuration_tables_generator", ROOT / "tools/host/generate_configuration_tables.py")
vectors = load("configuration_vectors_generator", ROOT / "tools/host/configuration_vectors.py")


class ConfigurationTableControls(unittest.TestCase):
    def setUp(self):
        self.work = Path(tempfile.mkdtemp(prefix="opensip-configuration-controls-"))
        self.addCleanup(shutil.rmtree, self.work)
        self.arch = self.work / "arch"
        self.product = self.work / "product"
        for path, _, _ in tables.ARCH:
            (self.arch / path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ARCH / path, self.arch / path)
        for path in (tables.PCS[0], tables.IDS, tables.CLASSES):
            (self.product / path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, self.product / path)

    def test_the_checked_in_tables_are_the_generated_tables(self):
        raw = tables.formatted(tables.tables(ARCH, ROOT), RUSTFMT)
        self.assertEqual(raw, (ROOT / tables.OUTPUT).read_bytes())
        self.assertEqual(tables.tables(self.arch, self.product), tables.tables(ARCH, ROOT))

    def test_a_renamed_shared_flag_refuses(self):
        path = self.arch / tables.ARCH[1][0]
        path.write_bytes(path.read_bytes().replace(b'"--workspace-root"', b'"--workspace-dir"', 1))
        with self.assertRaisesRegex(ValueError, "input pin mismatch"):
            tables.tables(self.arch, self.product)

    def mapping(self, edit):
        path = self.product / tables.CLASSES
        value = json.loads(path.read_text())
        edit(value)
        path.write_text(json.dumps(value))

    def test_a_pcs_leaf_without_a_row_refuses(self):
        self.mapping(lambda m: m["rows"].pop())
        with self.assertRaisesRegex(ValueError, "mapping rows differ"):
            tables.tables(self.arch, self.product)

    def test_a_row_naming_a_non_leaf_refuses(self):
        self.mapping(lambda m: m["rows"].append({"leaf": "ui.theme", "class": "host.operability.nonsemantic", "layers": ["project"]}))
        with self.assertRaisesRegex(ValueError, "mapping rows differ"):
            tables.tables(self.arch, self.product)

    def test_a_class_outside_the_drc_vocabulary_refuses(self):
        self.mapping(lambda m: m["rows"][-1].update({"class": "host.operability.semantic"}))
        with self.assertRaisesRegex(ValueError, "class outside"):
            tables.tables(self.arch, self.product)

    def test_a_semantic_leaf_classed_operational_refuses(self):
        self.mapping(lambda m: m["rows"][0].update({"class": "host.operability.nonsemantic"}))
        with self.assertRaisesRegex(ValueError, "semantic leaves differ"):
            tables.tables(self.arch, self.product)

    def test_an_environment_layer_refuses(self):
        self.mapping(lambda m: m["rows"][0]["layers"].append("environment"))
        with self.assertRaisesRegex(ValueError, "layers unknown"):
            tables.tables(self.arch, self.product)

    def test_a_changed_matrix_refuses(self):
        path = self.arch / tables.ARCH[0][0]
        path.write_bytes(path.read_bytes().replace(b'"id": "calls"', b'"id": "call-graph"', 1))
        with self.assertRaisesRegex(ValueError, "input pin mismatch"):
            tables.tables(self.arch, self.product)


class ConfigurationVectorControls(unittest.TestCase):
    def test_the_checked_in_vectors_are_pcms_results(self):
        packages = ROOT if (ROOT / "tools/contracts/python-packages").is_dir() else ROOT.parent / "opensip"
        self.assertEqual(vectors.vectors(ARCH, ROOT, packages), (ROOT / vectors.OUTPUT).read_bytes())


if __name__ == "__main__":
    unittest.main()
