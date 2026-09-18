#!/usr/bin/env python3
"""Parse a small SIP support log into structured incident facts.

Input format:
YYYY-MM-DD HH:MM:SS LEVEL method/status call_id message

This is intentionally dependency-free so it can run in a support environment.
"""
import json
import re
import sys
from collections import Counter

LINE = re.compile(
    r"^(?P<ts>\S+ \S+)\s+(?P<level>[A-Z]+)\s+"
    r"(?P<kind>\S+)\s+call_id=(?P<call_id>\S+)\s+(?P<message>.*)$"
)

def parse(path):
    events = []
    with open(path, encoding="utf-8") as f:
        for n, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            m = LINE.match(line)
            if not m:
                continue
            item = m.groupdict()
            item["line"] = n
            events.append(item)
    return events

def summarize(events):
    by_call = {}
    for e in events:
        by_call.setdefault(e["call_id"], []).append(e)

    result = []
    for call_id, items in by_call.items():
        messages = " ".join(x["message"] for x in items)
        codes = [x["kind"] for x in items if re.fullmatch(r"[45]\\d\\d", x["kind"])]
        result.append({
            "call_id": call_id,
            "event_count": len(items),
            "error_codes": codes,
            "has_timeout": "timeout" in messages.lower(),
            "has_one_way_audio": "one-way audio" in messages.lower(),
            "methods": [x["kind"] for x in items],
        })
    return result

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 parse_sip_log.py sample_sip.log")
        raise SystemExit(2)
    events = parse(sys.argv[1])
    summary = summarize(events)
    print(json.dumps({
        "parsed_events": len(events),
        "calls": summary,
        "error_code_counts": dict(Counter(code for c in summary for code in c["error_codes"]))
    }, indent=2))

if __name__ == "__main__":
    main()
