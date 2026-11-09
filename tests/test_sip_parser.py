import tempfile
import unittest
from pathlib import Path

from sip_parser import parse_log


class SipParserTests(unittest.TestCase):
    def test_sample_fixture_classifies_known_scenarios(self):
        root = Path(__file__).resolve().parents[1]
        report = parse_log(root / "sip-parser" / "sample_sip.log")
        by_id = {item["call_id"]: item for item in report["calls"]}

        self.assertEqual(report["parsed_events"], 17)
        self.assertEqual(by_id["demo-reg-002"]["classification"], "REGISTRATION_FORBIDDEN")
        self.assertEqual(by_id["demo-call-1002"]["classification"], "MEDIA_PATH_REVIEW")
        self.assertEqual(by_id["demo-call-1001"]["classification"], "NO_FIXTURED_ERROR")

    def test_malformed_line_is_counted_not_crashing(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "bad.log"
            log.write_text("not a valid fixture line\n", encoding="utf-8")
            report = parse_log(log)
        self.assertEqual(report["parsed_events"], 0)
        self.assertEqual(report["malformed_lines"], 1)
        self.assertEqual(report["calls"], [])

    def test_401_challenge_is_not_misreported_as_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            log = Path(tmp) / "auth.log"
            log.write_text(
                "2026-09-15 09:14:02 INFO REGISTER call_id=auth-1 request received\n"
                "2026-09-15 09:14:02 INFO 401 call_id=auth-1 digest challenge sent\n"
                "2026-09-15 09:14:03 INFO REGISTER call_id=auth-1 authenticated request accepted\n",
                encoding="utf-8",
            )
            report = parse_log(log)
        self.assertEqual(report["calls"][0]["classification"], "AUTH_CHALLENGE")
        self.assertEqual(report["error_code_counts"], {"401": 1})


if __name__ == "__main__":
    unittest.main()
