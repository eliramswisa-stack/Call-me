import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

class SipEvidenceExitTests(unittest.TestCase):
    def run_case(self, log):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "session.log"
            path.write_text(log)
            return subprocess.run([sys.executable,"tools/sip_evidence.py",str(path)],capture_output=True,text=True)

    def test_no_sip_evidence_fails(self):
        self.assertEqual(self.run_case("baresip exited normally").returncode,3)

    def test_missing_codec_fails(self):
        self.assertEqual(self.run_case("Populated 0 audio codecs").returncode,2)

    def test_connection_does_not_claim_audio(self):
        result=self.run_case("call established")
        self.assertEqual(result.returncode,0)
        self.assertIn("MEDIA_NOT_VERIFIED",result.stdout)
