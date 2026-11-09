#!/usr/bin/env python3
"""Check required project assets and run the SIP parser and unit tests."""
from pathlib import Path
import csv
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REQUIRED = [
    "README.md",
    "postman/voip-api-health.postman_collection.json",
    "wireshark/voip-filters.md",
    "sip-parser/parse_sip_log.py",
    "sip-parser/sample_sip.log",
    "sql/schema.sql",
    "sql/voip_metrics.sql",
    "data/public_capture_inventory.csv",
    "data/rtp_measurements.csv",
    "data/source_notes.md",
    "automation/jira-zendesk-blueprint.md",
    "docs/incident-runbook.md",
    "docs/worked-incidents.md",
    "docs/api-sms-troubleshooting.md",
    "tests/test_sip_parser.py",
]
missing = [name for name in REQUIRED if not (ROOT / name).is_file()]
if missing:
    print("Missing required project files:")
    for name in missing:
        print(f"  - {name}")
    raise SystemExit(1)

with (ROOT / "data/public_capture_inventory.csv").open(
    newline="", encoding="utf-8"
) as handle:
    capture_rows = list(csv.DictReader(handle))
with (ROOT / "data/rtp_measurements.csv").open(
    newline="", encoding="utf-8"
) as handle:
    rtp_rows = list(csv.DictReader(handle))

print(f"Required files present: {len(REQUIRED)}")
print(f"Public capture inventory rows: {len(capture_rows)}")
print(f"Documented RTP measurement rows: {len(rtp_rows)}")

print("\nRunning SIP parser...")
subprocess.run(
    [sys.executable, "sip-parser/parse_sip_log.py", "sip-parser/sample_sip.log"],
    cwd=ROOT,
    check=True,
)

print("\nRunning unit tests...")
subprocess.run(
    [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
    cwd=ROOT,
    check=True,
)

print("\nProject validation passed.")
