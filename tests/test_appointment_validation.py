import unittest
from datetime import datetime,timezone,timedelta
from tools.appointment_validation import validate,make_body,TITLE,OWNER
class AppointmentValidationTests(unittest.TestCase):
    def setUp(self):
        self.now=datetime(2026,10,13,10,0,tzinfo=timezone.utc)
    def test_due(self):
        self.assertEqual(validate(TITLE,make_body(self.now),OWNER,self.now),"DUE")
    def test_future(self):
        self.assertEqual(validate(TITLE,make_body(self.now+timedelta(hours=1)),OWNER,self.now),"WAITING")
    def test_expired(self):
        self.assertEqual(validate(TITLE,make_body(self.now-timedelta(hours=2)),OWNER,self.now),"EXPIRED")
    def test_other_user_rejected(self):
        self.assertEqual(validate(TITLE,make_body(self.now),"outsider",self.now),"REJECTED")
    def test_requires_explicit_consent(self):
        self.assertEqual(validate(TITLE,"CALL_AT_UTC=2026-10-13T10:00:00Z",OWNER,self.now),"REJECTED")
    def test_naive_time_rejected(self):
        with self.assertRaises(ValueError):
            make_body(datetime(2026,10,13,10))
if __name__=="__main__":
    unittest.main()
