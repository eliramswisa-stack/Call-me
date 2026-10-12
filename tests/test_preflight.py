import unittest
from tools.preflight import parse_target

class SipPreflightTests(unittest.TestCase):
    def test_owner_address(self):
        self.assertEqual(parse_target("sip:eliramswis@sip.linphone.org"), ("eliramswis", "sip.linphone.org"))

    def test_blocks_non_linphone_host(self):
        with self.assertRaises(ValueError):
            parse_target("sip:somebody@example.com")

    def test_blocks_shell_injection(self):
        with self.assertRaises(ValueError):
            parse_target("sip:hello@localhost;curl bad")

    def test_blocks_missing_username(self):
        with self.assertRaises(ValueError):
            parse_target("sip:@sip.linphone.org")

    def test_blocks_invalid_format(self):
        with self.assertRaises(ValueError):
            parse_target("https://sip.linphone.org")

if __name__ == "__main__":
    unittest.main()
