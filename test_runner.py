from pathlib import Path
from runner import execute_tools

TESTS = [
    ("good call",        "check_online_renewal_eligibility", '{"days_to_expiry": 30}'),
    ("number as text",   "check_online_renewal_eligibility", '{"days_to_expiry": "30"}'),
    ("word not number",  "check_online_renewal_eligibility", '{"days_to_expiry": "thirty"}'),
    ("out of range",     "check_online_renewal_eligibility", '{"days_to_expiry": 99999}'),
    ("missing argument", "check_online_renewal_eligibility", '{}'),
    ("extra argument",   "check_online_renewal_eligibility", '{"days_to_expiry": 30, "country": "US"}'),
    ("unknown signal",   "get_signal_meaning",               '{"signal": "purple"}'),
    ("broken JSON",      "search_handbook",                  '{"query": "parking"'),
    ("unknown tool",     "pay_fee",                          '{"amount": 5}'),
    ("empty query",      "search_handbook",                  '{"query": ""}'),
]

lines = []
for label, name, raw in TESTS:
    line = f"{label:17} -> {str(execute_tools(name, raw))[:150]}"
    print(line)
    lines.append(line)

Path("output").mkdir(exist_ok=True)
Path("output/w1d4_validation.txt").write_text("\n".join(lines), encoding="utf-8")