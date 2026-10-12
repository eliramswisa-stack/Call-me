import tempfile
import unittest
from pathlib import Path
from tools.audio_probe import generate, inspect

class AudioProbeTests(unittest.TestCase):
    def test_pcm_wav(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "reference.wav"
            generate(path)
            self.assertEqual(inspect(path)["sample_rate"], 16000)
            self.assertEqual(inspect(path)["frames"], 32000)

    def test_parameter_lock(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                generate(Path(directory) / "bad.wav", frequency=1000)
