"""Refresh official SA opportunity directories and optional permitted RSS feeds."""
import datetime as dt
import json, os, re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

OUT = Path(__file__).parent / "data/opportunities.json"
DPSA = "https://www.dpsa.gov.za/newsroom/psvc/"
FUNZA = "https://www.funzalushaka.doe.gov.za/Home/"
CATEGORIES = {"Jobs", "Tenders", "Bursaries", "Internships", "Learnerships"}

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs).get("href", ""))

def load(url):
    with urlopen(Request(url, headers={"User-Agent": "SAOpportunityHub/1.0 official-source-checker"}), timeout=20) as response:
        return response.read(2_000_000).decode("utf-8", errors="replace")

def make(title, url, category, organization, description, deadline=""):
    return dict(title=title, url=url, category=category, organization=organization, description=description, deadline=deadline)

def dpsa(records):
    links = Links()
    links.feed(load(DPSA))
    found = []
    for href in links.links:
        url = urljoin(DPSA, href)
        match = re.search(r"/circular-(\d+)-of-(20\d{2})/?(?:[?#].*)?$", url, re.I)
        if match and urlsplit(url).hostname == "www.dpsa.gov.za":
            found.append((int(match.group(2)), int(match.group(1)), url))
    if not found:
        raise ValueError("No circular links found in official DPSA index")
    for year, number, url in sorted(set(found), reverse=True)[:3]:
        if not dt.date.today().year - 1 <= year <= dt.date.today().year:
            continue
        records[url] = make(f"Public Service Vacancy Circular {number} of {year}", url, "Jobs", "Department of Public Service and Administration", "Official government vacancy circular. Check individual advertisements and their closing dates.")

def funza(records):
    html = load(FUNZA)
    if dt.date.today() <= dt.date(2027, 1, 31) and "2027" in html and "31/01/2027" in html:
        records[FUNZA] = make("Funza Lushaka Teaching Bursary 2027", FUNZA, "Bursaries", "Department of Basic Education", "New applications close 31 January 2027. Returning bursars close 30 November 2026. Check the official site for conditions.", "2027-01-31")

def feeds(records):
    for feed in json.loads(os.getenv("OFFICIAL_FEEDS_JSON") or "[]"):
        url, category = feed.get("url", ""), feed.get("category", "")
        if urlsplit(url).scheme != "https" or category not in CATEGORIES: continue
        try:
            root = ET.fromstring(load(url))
            for node in (root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry"))[:40]:
                title = (node.findtext("title") or node.findtext("{http://www.w3.org/2005/Atom}title") or "").strip()
                link = (node.findtext("link") or "").strip()
                if not link:
                    atom = node.find("{http://www.w3.org/2005/Atom}link")
                    if atom is not None: link = atom.get("href", "")
                if title and urlsplit(link).scheme == "https":
                    records[link] = make(title[:180], link, category, feed.get("organization", "Official publisher"), "See official publisher for full details and closing dates.")
        except Exception as error:
            print("Feed failed:", url, error)

def main():
    previous = json.loads(OUT.read_text(encoding="utf-8"))
    records = {item["url"]: item for item in previous.get("items", []) if item.get("url", "").startswith("https://")}
    for name, func in [("DPSA", dpsa), ("Funza Lushaka", funza), ("Optional feeds", feeds)]:
        try:
            func(records)
            print(name, "checked")
        except Exception as error:
            print(name, "failed:", error)
    today = dt.date.today().isoformat()
    records = {url: item for url, item in records.items() if not item.get("deadline") or item["deadline"] >= today}
    OUT.write_text(json.dumps({"updated": today, "items": list(records.values())[:500]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
