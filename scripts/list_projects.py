#!/usr/bin/env python3
"""List all XAG projects visible on Crowdin with read-only token."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _common import get, XAG_PROJECTS

r = get("/projects", {"limit": 500})
if not r:
    sys.exit("Failed to list projects (check token).")

print(f"{'ID':>7}  {'Identifier':<35}  {'Project Name':<55}  {'Source':<8}  {'#Targets'}")
print("-" * 120)
for item in r["data"]:
    d = item["data"]
    is_xag = "✓" if d["id"] in XAG_PROJECTS else " "
    print(f"{d['id']:>7}  {d['identifier']:<35}  {d['name']:<55}  {d['sourceLanguageId']:<8}  {len(d['targetLanguageIds'])}  {is_xag}")
