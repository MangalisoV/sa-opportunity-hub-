"""Daily opportunity feed collector. Requires configured, permitted official RSS/Atom feeds."""
import datetime
import json
import os
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

FILE = Path(__file__).parent / "data/opportunities.json"
CATEGORIES = {"Jobs", "Bursaries", "Tenders", "Internships", "Learnerships"}

def child_text(node, name):
    child = node.find(name)
    if child is None:
        child = node.find("{http://www.w3.org/2005/Atom}" + name)
    return "".join(child.itertext()).strip() if child is not None else ""

def run():
    existing = json.loads(FILE.read_text(encoding="utf-8"))
    records = {x["url"]: x for x in existing.get("items", []) if x.get("url")}
    feeds = json.loads(os.getenv("OFFICIAL_FEEDS_JSON", "[]"))
    for feed in feeds:
        url = feed.get("url", "")
        category = feed.get("category", "")
        if category not in CATEGORIES or urllib.parse.urlsplit(url).scheme != "https":
            print("Skipping invalid feed", url)
            continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "SAOpportunityHub/1.0 RSS reader"})
            with urllib.request.urlopen(req, timeout=15) as response:
                payload = response.read(2_000_000)
            root = ET.fromstring(payload)
            nodes = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")
            for node in nodes[:40]:
                title = child_text(node, "title")
                link = child_text(node, "link")
                if not link:
                    atom_link = node.find("{http://www.w3.org/2005/Atom}link")
                    link = atom_link.get("href", "") if atom_link is not None else ""
                if not title or urllib.parse.urlsplit(link).scheme != "https":
                    continue
                records[link] = {
                    "title": title[:180],
                    "url": link,
                    "category": category,
                    "organization": feed.get("organization", "Official publisher")[:100],
                    "description": child_text(node, "description")[:250] or "Visit official publisher for details.",
                    "deadline": ""
                }
            print("Processed", url)
        except Exception as exc:
            print("Feed error:", url, str(exc))
    FILE.write_text(json.dumps({"updated": datetime.date.today().isoformat(), "items": list(records.values())[:500]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    run()
