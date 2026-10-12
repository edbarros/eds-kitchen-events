#!/usr/bin/env python3
"""Mirror of the app's validEvent/normalizeFeed. Usage: python3 validate.py [events.json]"""
import json, re, sys
STATUS = {"open", "check", "closed", "tba", "next"}
def md(s):
    m = re.fullmatch(r"(\d\d)-(\d\d)", s) if isinstance(s, str) else None
    return bool(m) and 1 <= int(m[1]) <= 12 and 1 <= int(m[2]) <= 31
def ok(e):
    if not isinstance(e, dict): return "not an object"
    if not isinstance(e.get("id"), str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,60}", e["id"]): return "bad id"
    if not isinstance(e.get("n"), str) or not e["n"] or not isinstance(e.get("city"), str) or not e["city"]: return "missing n/city"
    if e.get("st") not in STATUS: return "bad st"
    if not isinstance(e.get("mi"), (int, float)) or isinstance(e["mi"], bool) or e["mi"] < 0: return "bad mi"
    ds = list(e.get("d") or []) + list(e.get("p") or []) + list(e.get("r") or []) + ([e["dl"]] if e.get("dl") else [])
    if not all(md(x) for x in ds): return "bad date (use MM-DD)"
    if e.get("ap") and not str(e["ap"]).startswith("https://"): return "ap must be https"
    for k in ("fn", "rk"):
        if e.get(k) is not None and not isinstance(e[k], (int, float)): return k + " must be a number"
    return None
path = sys.argv[1] if len(sys.argv) > 1 else "events.json"
d = json.load(open(path))
bad = 0; seen = set()
if d.get("schema") != 1 or not isinstance(d.get("events"), list): sys.exit("FAIL: schema must be 1 with an events list")
for e in d["events"]:
    r = ok(e)
    if not r and e["id"] in seen: r = "duplicate id"
    if r: bad += 1; print("BAD", (e or {}).get("id") if isinstance(e, dict) else e, "-", r)
    else: seen.add(e["id"])
print(f"{len(seen)} valid, {bad} bad")
sys.exit(1 if bad or len(seen) < 50 else 0)
