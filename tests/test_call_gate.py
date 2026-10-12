import json
import subprocess
import sys
import unittest

class CallGateTests(unittest.TestCase):
    def run_gate(self, *args):
        p = subprocess.run([sys.executable, "tools/call_gate.py", *args], capture_output=True, text=True)
        return p.returncode, json.loads(p.stdout)

    def test_default_is_blocked(self):
        rc, result = self.run_gate()
        self.assertNotEqual(rc, 0)
        self.assertEqual(result["reason"], "OWNER_CONSENT_REQUIRED")
        self.assertFalse(result["dialed"])

    def test_authorized_but_no_backend(self):
        rc, result = self.run_gate("--owner-consent")
        self.assertNotEqual(rc, 0)
        self.assertEqual(result["reason"], "NO_SIP_BACKEND_CONNECTED")

    def test_wrong_recipient_rejected(self):
        rc, result = self.run_gate("--owner-consent", "--target", "sip:other@sip.linphone.org")
        self.assertNotEqual(rc, 0)
        self.assertEqual(result["reason"], "ONLY_OWNER_TARGET_ALLOWED")

    def test_dry_run_does_not_call(self):
        rc, result = self.run_gate("--dry-run", "--owner-consent")
        self.assertEqual(rc, 0)
        self.assertFalse(result["ready"])
        self.assertFalse(result["dialed"])

if __name__ == "__main__":
    unittest.main()
