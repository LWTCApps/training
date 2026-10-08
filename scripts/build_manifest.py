#!/usr/bin/env python3
"""Build training-assets/manifest.json from the <head> of each training page.

Run by the GitHub Action on every upload. Can also be run by hand:
    python3 scripts/build_manifest.py
Files whose names start with "_" or "." are skipped (templates and drafts).
"""
import json, re, sys
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

FOLDER = Path(__file__).resolve().parent.parent / "training-assets"


class Head(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta, self.title, self._in_title = {}, "", False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta" and a.get("name"):
            self.meta[a["name"].lower()] = (a.get("content") or "").strip()
        elif tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def valid_date(s):
    try:
        return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", s)) and bool(datetime.strptime(s, "%Y-%m-%d"))
    except ValueError:
        return False


def read_head(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    end = re.search(r"</head>", text, re.I)
    return text[: end.end()] if end else text[:50000]


def main():
    items = []
    for path in sorted(FOLDER.glob("*.htm*")):
        if path.name.startswith(("_", ".")):
            continue
        p = Head()
        p.feed(read_head(path))
        date = p.meta.get("training-date", "")
        if not valid_date(date):
            m = re.match(r"(\d{4}-\d{2}-\d{2})", path.name)
            date = m.group(1) if m and valid_date(m.group(1)) else ""
        if not date:
            print(f"::warning file={path.name}::No valid training date. Add "
                  f'<meta name="training-date" content="YYYY-MM-DD"> to the page head.')
        items.append({
            "file": path.name,
            "title": p.meta.get("training-title") or " ".join(p.title.split()) or path.stem,
            "date": date,
            "description": p.meta.get("description", ""),
            "minutes": p.meta.get("training-minutes", ""),
            "audience": p.meta.get("training-audience", ""),
        })
    items.sort(key=lambda t: (t["date"] == "", t["date"] and -int(t["date"].replace("-", "")), t["title"]))
    (FOLDER / "manifest.json").write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote manifest.json with {len(items)} training(s).")


if __name__ == "__main__":
    sys.exit(main())
