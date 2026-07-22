import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from .mock_data import ARTICLES, AIS_SAMPLE, PRICE_HISTORY, SUPPLIERS


class DataHub:
    """No-key adapters. Every network path fails closed to bundled demo data."""

    def news(self, live: bool = False) -> tuple[list[dict], str]:
        if not live:
            return ARTICLES, "bundled deterministic demo"
        query = urllib.parse.quote('(oil OR tanker OR LNG) (war OR sanctions OR disruption)')
        url = f"https://api.gdeltproject.org/api/v2/doc/doc?query={query}&mode=artlist&maxrecords=10&format=rss"
        try:
            with urllib.request.urlopen(url, timeout=4) as response:
                root = ET.fromstring(response.read())
            items = []
            for item in root.findall(".//item"):
                items.append({
                    "title": item.findtext("title", "Untitled"),
                    "summary": item.findtext("description", ""),
                    "source": "GDELT DOC RSS",
                    "published_at": item.findtext("pubDate", ""),
                })
            if items:
                return items, "live GDELT RSS"
        except Exception:
            pass
        return ARTICLES, "bundled fallback (live feed unavailable)"

    def snapshot(self) -> dict:
        return {
            "articles": ARTICLES,
            "prices": PRICE_HISTORY,
            "suppliers": SUPPLIERS,
            "ais": AIS_SAMPLE,
            "provenance": {
                "news": "GDELT DOC 2.0 RSS-compatible adapter",
                "shipping": "NOAA/USCG Marine Cadastre schema; bundled sample",
                "prices": "World Bank Pink Sheet-shaped monthly series; bundled sample",
                "trade": "UN Comtrade HS 2709 preview-compatible supplier baseline",
            },
        }


data_hub = DataHub()
