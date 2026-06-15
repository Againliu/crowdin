#!/usr/bin/env python3
"""Get translation progress for all target languages of a Crowdin project."""
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _common import get, XAG_PROJECTS


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", type=int, required=True)
    args = ap.parse_args()

    proj = get(f"/projects/{args.project}")
    if not proj:
        sys.exit(f"Project {args.project} not found.")
    d = proj["data"]
    print(f"Project: {d['name']} ({d['identifier']}, id={d['id']})")
    print(f"Source: {d['sourceLanguageId']}\n")

    print(f"{'Lang':<8}  {'Translated %':>12}  {'Approved %':>11}  "
          f"{'Words T/Total':>16}  {'Phrases T/Total':>18}  {'QA Failed':>10}")
    print("-" * 90)
    for lang in sorted(d["targetLanguageIds"]):
        r = get(f"/projects/{args.project}/languages/{lang}/progress")
        if not r or not r.get("data"):
            print(f"{lang:<8}  (no data)")
            continue
        p = r["data"][0]["data"]
        w = p.get("words", {})
        ph = p.get("phrases", {})
        qa = p.get("qaChecksStatus", {})
        print(f"{lang:<8}  {p.get('translationProgress',0):>11}%  "
              f"{p.get('approvalProgress',0):>10}%  "
              f"{w.get('translated',0):>9}/{w.get('total',0):<6}  "
              f"{ph.get('translated',0):>9}/{ph.get('total',0):<8}  "
              f"{qa.get('failed',0):>10}")


if __name__ == "__main__":
    main()
