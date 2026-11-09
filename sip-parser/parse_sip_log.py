#!/usr/bin/env python3
"""Parse sanitized SIP log fixtures into a support-oriented JSON summary.

This is a fixture parser, not a SIP protocol stack or live network monitor.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

LINE_RE = re.compile(
    r"^(?P<timestamp>\S+\s+\S+)\s+(?P<level>INFO|WARN|ERROR)\s+"
    r"(?P<event>REGISTER|INVITE|\d{3}|RTP|BYE)\s+"
    r"call_id=(?P<call_id>\S+)\s+(?P<message>.*)$"
)


def parse_log(path: str | Path) -> dict:
    calls = defaultdict(lambda: {
        "call_id": "", "event_count": 0, "methods": [], "error_codes": [],
        "has_timeout": False, "has_one_way_audio": False, "warnings": [],
        "first_timestamp": None, "last_timestamp": None,
    })
    parsed_events = 0
    malformed_lines = 0

    with Path(path).open(encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            match = LINE_RE.match(line)
            if not match:
                malformed_lines += 1
                continue
            event = match.groupdict()
            call = calls[event["call_id"]]
            call["call_id"] = event["call_id"]
            call["event_count"] += 1
            call["methods"].append(event["event"])
            call["first_timestamp"] = call["first_timestamp"] or event["timestamp"]
            call["last_timestamp"] = event["timestamp"]
            parsed_events += 1

            if event["event"].isdigit() and int(event["event"]) >= 400:
                call["error_codes"].append(int(event["event"]))
            message = event["message"].lower()
            if "timeout" in message or "no rtp" in message:
                call["has_timeout"] = True
            if "one-way audio" in message:
                call["has_one_way_audio"] = True
            if event["level"] in {"WARN", "ERROR"}:
                call["warnings"].append(event["message"])

    summaries = []
    for call in calls.values():
        codes = call["error_codes"]
        if call["has_one_way_audio"]:
            call["classification"] = "MEDIA_PATH_REVIEW"
            call["recommended_checks"] = [
                "Compare SDP media addresses and ports",
                "Check bidirectional RTP in the capture",
                "Review NAT and firewall rules",
            ]
        elif 403 in codes:
            call["classification"] = "REGISTRATION_FORBIDDEN"
            call["recommended_checks"] = [
                "Verify account/device authorization",
                "Check endpoint policy",
                "Review registrar logs for the rejection reason",
            ]
        elif 401 in codes:
            call["classification"] = "AUTH_CHALLENGE"
            call["recommended_checks"] = [
                "Confirm digest challenge/response sequence",
                "Verify credentials if authentication does not complete",
            ]
        elif 407 in codes:
            call["classification"] = "PROXY_AUTH_CHALLENGE"
            call["recommended_checks"] = [
                "Confirm proxy authentication challenge and retry",
                "Check proxy credentials and Proxy-Authorization handling",
            ]
        elif 408 in codes:
            call["classification"] = "REQUEST_TIMEOUT"
            call["recommended_checks"] = [
                "Check transaction timers and response path",
                "Review packet loss, routing and remote endpoint availability",
            ]
        elif 486 in codes:
            call["classification"] = "CALL_REJECTED_BUSY"
            call["recommended_checks"] = [
                "Confirm destination user/device availability",
                "Check whether call forwarding or busy policy is expected",
            ]
        elif 488 in codes:
            call["classification"] = "SDP_MEDIA_NEGOTIATION_FAILURE"
            call["recommended_checks"] = [
                "Compare SDP offer and answer codec lists",
                "Check media profile, transport and required SDP attributes",
            ]
        elif 503 in codes:
            call["classification"] = "SERVICE_UNAVAILABLE"
            call["recommended_checks"] = [
                "Check service health and upstream dependency status",
                "Review Retry-After if present; avoid uncontrolled retry loops",
            ]
        elif call["has_timeout"]:
            call["classification"] = "MEDIA_TIMEOUT"
            call["recommended_checks"] = [
                "Check RTP flow in both directions",
                "Review routing, NAT and firewall timeouts",
            ]
        else:
            call["classification"] = "NO_FIXTURED_ERROR"
            call["recommended_checks"] = [
                "No explicit failure is represented in this fixture"
            ]
        summaries.append(call)

    return {
        "parsed_events": parsed_events,
        "malformed_lines": malformed_lines,
        "calls": summaries,
        "error_code_counts": dict(
            Counter(str(code) for item in summaries for code in item["error_codes"])
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("log_file", nargs="?", default="sip-parser/sample_sip.log")
    parser.add_argument("--json", dest="json_file", help="Write full report to a JSON file")
    args = parser.parse_args()
    try:
        report = parse_log(args.log_file)
    except OSError as exc:
        parser.error(str(exc))
    print(f"Parsed events: {report['parsed_events']}")
    print(f"Malformed non-comment lines: {report['malformed_lines']}")
    for call in report["calls"]:
        print(
            f"- {call['call_id']}: {call['classification']} "
            f"(events={call['event_count']}, SIP errors={call['error_codes']})"
        )
    if args.json_file:
        Path(args.json_file).write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
        print(f"JSON report written to: {args.json_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
