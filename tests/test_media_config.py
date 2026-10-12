import tempfile
import unittest
from pathlib import Path
from tools.audio_probe import generate
from tools.media_config import write_config

class MediaConfigTests(unittest.TestCase):
    def test_generates_without_secrets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            wave=root/"probe.wav"
            generate(wave)
            cfg=write_config(root/"cfg",wave)
            contents=cfg.read_text()
            self.assertIn("audio_source aufile,",contents)
            self.assertIn("audio_player aufile,",contents)
            self.assertNotIn("auth_pass",contents)
            self.assertNotIn("sip:eliramswis",contents)
    def test_requires_wave_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                write_config(Path(tmp)/"cfg",Path(tmp)/"missing.wav")
