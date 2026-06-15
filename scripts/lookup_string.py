#!/usr/bin/env python3
"""
Look up a Crowdin string by identifier prefix or text content.

Note: read-only token cannot filter on the server. We must fetch all
strings and filter client-side. Use --max to early-exit after N matches.

Usage:
    python3 lookup_string.py --project 744513 --identifier mission_launch_error
    python3 lookup_string.py --project 744513 --text "设备未连接"
    python3 lookup_string.py --project 744513 --identifier survey_ --lang en --max 10
"""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _common import paginate


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", type=int, required=True)
    ap.add_argument("--identifier", help="Identifier prefix (case sensitive)")
    ap.add_argument("--text", help="Substring of source text (zh-CN)")
    ap.add_argument("--lang", help="If set, also fetch translation in this language")
    ap.add_argument("--max", type=int, default=50, help="Early-exit after N matches (default 50)")
    args = ap.parse_args()

    if not (args.identifier or args.text):
        sys.exit("Must provide --identifier or --text")

    print(f"Scanning project {args.project} (max {args.max} matches)...", file=sys.stderr)
    matches = []
    total = 0
    for item in paginate(f"/projects/{args.project}/strings"):
        d = item["data"]
        total += 1
        if args.identifier and not d["identifier"].startswith(args.identifier):
            continue
        if args.text:
            t = d.get("text", "")
            if isinstance(t, dict):
                t = " ".join(t.values())
            if args.text not in t:
                continue
        matches.append(d)
        if len(matches) >= args.max:
            break
    print(f"Scanned {total} strings, found {len(matches)} matches.\n", file=sys.stderr)

    translations = {}
    if args.lang and matches:
        for item in paginate(f"/projects/{args.project}/languages/{args.lang}/translations"):
            translations[item["data"]["stringId"]] = item["data"].get("text", "")

    for d in matches:
        print(f"[{d['id']}] {d['identifier']}")
        print(f"  ZH: {d.get('text','')}")
        if args.lang:
            print(f"  {args.lang.upper()}: {translations.get(d['id'], '(no translation)')}")
        if d.get("labelIds"):
            print(f"  Labels: {d['labelIds']}")
        print()


if __name__ == "__main__":
    main()
