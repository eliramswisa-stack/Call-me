import tempfile
import unittest
from pathlib import Path
from tools.resolve_modules import resolve

class ModuleResolutionTests(unittest.TestCase):
    def test_resolves_existing_modules(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            paths=[root/(name+".so") for name in ("g711","aufile","menu","stdio")]
            for path in paths: path.touch()
            config=root/"config"
            config.write_text("# probe\n")
            self.assertEqual(resolve(config,paths),["aufile","g711","menu","stdio"])
            self.assertIn("module_path ",config.read_text())
            self.assertIn("module_app stdio.so",config.read_text())
    def test_missing_codec_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            path=root/"aufile.so"
            path.touch()
            config=root/"config"
            config.write_text("# probe\n")
            with self.assertRaises(RuntimeError):
                resolve(config,[path])
