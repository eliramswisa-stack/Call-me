import json
import unittest
from unittest.mock import patch, MagicMock
from tools import hebrew_voice as hv

class HebrewVoiceTests(unittest.TestCase):
    def test_check_has_no_call(self):
        result=hv.test_only()
        self.assertEqual(result["sip_rtp"],"NOT_CONNECTED")
        self.assertEqual(result["runtime"],"NOT_DEPLOYED")

    def test_ollama_refuses_remote_url(self):
        with self.assertRaises(ValueError):
            hv.ask_local_model([],"qwen2.5:3b","https://external.example/api")

    def test_local_response_parsing(self):
        fake=MagicMock()
        fake.__enter__.return_value=fake
        fake.__exit__.return_value=False
        fake.read.return_value=b'{"message":{"content":"שלום, מה תרצה לדעת?"}}'
        with patch("urllib.request.urlopen",return_value=fake):
            text=hv.ask_local_model([{"role":"user","content":"שלום"}])
        self.assertEqual(text,"שלום, מה תרצה לדעת?")

    def test_tts_empty_rejected(self):
        with self.assertRaises(ValueError):
            hv.speak_hebrew("")

if __name__=="__main__":
    unittest.main()
