#!/usr/bin/env python3
from pathlib import Path
import csv, json, subprocess, sys

root = Path(__file__).resolve().parent
required = [
    root/"README.md",
    root/"postman/voip-api-health.postman_collection.json",
    root/"wireshark/voip-filters.md",
    root/"sip-parser/parse_sip_log.py",
    root/"sip-parser/sample_sip.log",
    root/"sql/schema.sql",
    root/"sql/voip_metrics.sql",
    root/"data/call_records.csv",
    root/"automation/jira-zendesk-blueprint.md",
]
missing = [str(p.relative_to(root)) for p in required if not p.exists()]
if missing:
    print("Missing:", missing)
    raise SystemExit(1)

rows = list(csv.DictReader((root/"data/call_records.csv").open()))
print(f"Validation OK: {len(rows)} synthetic call records found.")
print("Running SIP parser...")
subprocess.run([sys.executable, str(root/"sip-parser/parse_sip_log.py"), str(root/"sip-parser/sample_sip.log")], check=True)
