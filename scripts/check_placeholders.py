#!/usr/bin/env python3
"""
Crowdin placeholder consistency check

Check all XAG projects for placeholder mismatches between source (zh-CN) and translations.
Placeholder formats:
  - Android: %s, %d, %f, %1$s, %2$d, %%
  - iOS: %@, %d, %ld, %1$@
  - Generic: {name}, {count}, ${var}, {{var}}
  - HTML tags: <b>, </b>, <br/>, <a>, </a>, <span>, </span>

Group by project -> language, output mismatched records.

Usage:
  python3 check_placeholders.py                  # Run check, report to stdout
  python3 check_placeholders.py --project 744513 # Check single project only
  python3 check_placeholders.py --json           # Output as JSON
"""

import json, os, re, sys, time
from collections import defaultdict
import requests

cred_path = os.path.expanduser("~/.hermes/credentials/crowdin.txt")
TOKEN = open(cred_path).read().strip()
H = {"Authorization": "Bearer " + TOKEN}
BASE = "https://api.crowdin.com/api/v2"

# Placeholder regex patterns
PLACEHOLDER_PATTERNS = [
    # Android/iOS format: %s %d %f %ld %@ %1$s %2$d %1s %2d %%
    # NOTE: (?:\d+\$?)? makes $ optional — %1s %2d (positional without $) MUST match
    r'%(?:\d+\$?)?[sdfcxeEgGaAn@%]|%[lL]?[dDuUxXoOfFeEgGaAcCsSpn@]',
    # Brace variables: {name} {{name}} ${var}
    r'\{[^{}]+\}',
    r'\$\{[^{}]+\}',
    r'\{\{[^{}]+\}\}',
    # HTML tags (common ones)
    r'</?[a-zA-Z][a-zA-Z0-9]*(?:\s[^>]*)?\s*/?>',
]

PLACEHOLDER_RE = re.compile('|'.join(PLACEHOLDER_PATTERNS))


def normalize_placeholders(placeholders):
    return sorted(placeholders)


def extract_placeholders(text):
    if not text or not isinstance(text, str):
        return []
    return PLACEHOLDER_RE.findall(text)


def fetch_all_strings(project_id):
    all_strings = {}
    offset = 0
    while True:
        r = requests.get(
            BASE + "/projects/" + str(project_id) + "/strings",
            headers=H,
            params={"limit": 500, "offset": offset}
        )
        if r.status_code != 200:
            break
        data = r.json().get("data", [])
        if not data:
            break
        for item in data:
            s = item.get("data", {})
            sid = s.get("id")
            text = s.get("text", "")
            if isinstance(text, dict):
                text = " ".join(str(v) for v in text.values())
            ident = s.get("identifier", "")
            all_strings[sid] = {"text": str(text), "identifier": ident}
        if len(data) < 500:
            break
        offset += 500
        time.sleep(0.1)
    return all_strings


def fetch_translations(project_id, lang):
    translations = {}
    offset = 0
    while True:
        r = requests.get(
            BASE + "/projects/" + str(project_id) + "/languages/" + lang + "/translations",
            headers=H,
            params={"limit": 500, "offset": offset}
        )
        if r.status_code != 200:
            break
        data = r.json().get("data", [])
        if not data:
            break
        for item in data:
            t = item.get("data", {})
            sid = t.get("stringId")
            text = t.get("text", "")
            if isinstance(text, dict):
                text = " ".join(str(v) for v in text.values())
            translations[sid] = str(text)
        if len(data) < 500:
            break
        offset += 500
        time.sleep(0.1)
    return translations


def get_projects(single_id=None):
    r = requests.get(BASE + "/projects", headers=H, params={"limit": 50})
    if r.status_code != 200:
        return []
    projects = [(p["data"]["id"], p["data"]["identifier"], p["data"]["name"],
                 p["data"].get("targetLanguageIds", []))
                for p in r.json().get("data", [])]
    if single_id:
        projects = [p for p in projects if p[0] == single_id]
    return projects


def check_project(project_id, identifier, name, target_langs):
    print("  Fetching source strings (" + identifier + ")...", file=sys.stderr)
    sources = fetch_all_strings(project_id)
    if not sources:
        return {}

    results = {}

    for lang in target_langs:
        print("    Checking " + lang + "...", file=sys.stderr)
        translations = fetch_translations(project_id, lang)
        if not translations:
            continue

        mismatches = []
        for sid, src_info in sources.items():
            tgt_text = translations.get(sid)
            if not tgt_text:
                continue

            src_ph = normalize_placeholders(extract_placeholders(src_info["text"]))
            tgt_ph = normalize_placeholders(extract_placeholders(tgt_text))

            if src_ph != tgt_ph:
                mismatches.append({
                    "key": src_info["identifier"],
                    "source": src_info["text"][:120],
                    "translation": tgt_text[:120],
                    "source_placeholders": src_ph,
                    "target_placeholders": tgt_ph,
                })

        if mismatches:
            results[lang] = mismatches

        time.sleep(0.1)

    return results


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Crowdin placeholder consistency check")
    parser.add_argument("--project", type=int, help="Check single project ID only")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    print("[" + time.strftime("%Y-%m-%d %H:%M:%S") + "] Starting Crowdin placeholder check", file=sys.stderr)

    projects = get_projects(single_id=args.project)
    if not projects:
        print("Failed to get project list")
        sys.exit(1)

    print(str(len(projects)) + " projects found", file=sys.stderr)

    all_results = {}
    total_issues = 0

    for pid, ident, name, langs in projects:
        if not langs:
            continue
        print("Processing: " + name + " (" + ident + ") - " + str(len(langs)) + " languages", file=sys.stderr)
        results = check_project(pid, ident, name, langs)
        if results:
            all_results[name + " (" + ident + ")"] = results
            for lang, mismatches in results.items():
                total_issues += len(mismatches)
        issue_count = sum(len(v) for v in results.values())
        print("  -> " + str(issue_count) + " mismatches", file=sys.stderr)

    if args.json:
        output = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "projects_checked": len(projects),
            "total_issues": total_issues,
            "results": all_results,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    if total_issues == 0:
        print("✅ **Crowdin placeholder check passed** - All translations match source placeholders")
        return

    print("⚠️ **Crowdin placeholder consistency report** (" + time.strftime("%Y-%m-%d") + ")")
    print("")
    print("Checked " + str(len(projects)) + " projects, found **" + str(total_issues) + "** placeholder mismatches:")
    print("")

    for project_key, lang_results in all_results.items():
        print("### " + project_key)
        for lang, mismatches in sorted(lang_results.items()):
            # Categorize mismatches
            lost = [m for m in mismatches if m["source_placeholders"] and not m["target_placeholders"]]
            added = [m for m in mismatches if not m["source_placeholders"] and m["target_placeholders"]]
            changed = [m for m in mismatches if m["source_placeholders"] and m["target_placeholders"]]

            print("")
            print("**" + lang + "** - " + str(len(mismatches)) + " mismatches (lost:" + str(len(lost)) + " added:" + str(len(added)) + " changed:" + str(len(changed)) + "):")
            print("")

            for items, label in [
                (lost, "🔴 Placeholder lost (translation missing source placeholders)"),
                (changed, "🟡 Format changed (placeholder format mismatch)"),
                (added, "🔵 Placeholder added (translation has extra placeholders)"),
            ]:
                if not items:
                    continue
                print("**" + label + "** (" + str(len(items)) + "):\n")
                print("| # | Key | Source | Src placeholders | Translation (" + lang + ") | Tgt placeholders |")
                print("|---|-----|--------|----------------|-----------------|-----------------|")
                for i, m in enumerate(items[:50], 1):
                    src = m["source"].replace("|", "\\|").replace("\n", " ")
                    tgt = m["translation"].replace("|", "\\|").replace("\n", " ")
                    key = m["key"]
                    key_short = key if len(key) <= 45 else key[:42] + "..."
                    src_short = src if len(src) <= 50 else src[:47] + "..."
                    tgt_short = tgt if len(tgt) <= 50 else tgt[:47] + "..."
                    src_ph = ", ".join(m["source_placeholders"]) if m["source_placeholders"] else "(none)"
                    tgt_ph = ", ".join(m["target_placeholders"]) if m["target_placeholders"] else "(none)"
                    print("| " + str(i) + " | `" + key_short + "` | " + src_short + " | `" + src_ph + "` | " + tgt_short + " | `" + tgt_ph + "` |")
                if len(items) > 50:
                    print("")
                    print("_... " + str(len(items) - 50) + " more not listed_")
                print("")
        print("")

    print("Checked at: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    print("Source: Crowdin API (read-only token)")


if __name__ == "__main__":
    main()
