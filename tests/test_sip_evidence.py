import unittest
from tools.sip_evidence import classify

class EvidenceClassifierTests(unittest.TestCase):
    def test_no_signal_no_success(self):
        self.assertEqual(classify("baresip exited with code 0"),"UNVERIFIED_NO_CALL_EVIDENCE")
    def test_zero_codecs_fails(self):
        self.assertEqual(classify("Populated 0 audio codecs"),"FAIL_MEDIA_OR_SIGNALING")
    def test_normal_auth_challenge_not_failure(self):
        self.assertEqual(classify("SIP/2.0 407 Proxy Authentication Required"),"UNVERIFIED_NO_CALL_EVIDENCE")
    def test_signaling_not_equivalent_media(self):
        self.assertEqual(classify("call established"),"SIGNALING_POSSIBLY_CONNECTED_MEDIA_NOT_VERIFIED")

if __name__=="__main__":
    unittest.main()
