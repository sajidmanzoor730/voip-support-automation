"""Import shim for the parser stored in the hyphenated sip-parser directory."""
import importlib.util
from pathlib import Path

_module_path = Path(__file__).resolve().parent / "sip-parser" / "parse_sip_log.py"
_spec = importlib.util.spec_from_file_location("sip_log_parser", _module_path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Cannot load SIP parser from {_module_path}")
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
parse_log = _module.parse_log
