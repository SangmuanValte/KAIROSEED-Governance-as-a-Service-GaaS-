"""Public RSS ingestion for the Agentic Failure Observatory.

The collector only reads public feeds and returns normalized observations.
It does not execute links, tools, or agent actions.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from hashlib import sha256
from typing import Iterable
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class NewsObservation:
    incident_id: str
    source: str
    title: str
    url: str
    published_at: str | None
    summary: str | None


def _text(element: ET.Element | None) -> str | None:
    if element is None:
        return None
    value = " ".join("".join(element.itertext()).split())
    return value or None


def _parse_date(value: str | None) -> str | None:
    if not value:
        return None
    try:
        return parsedate_to_datetime(value).astimezone(timezone.utc).isoformat()
    except (TypeError, ValueError, OverflowError):
        return value


def parse_rss(xml_bytes: bytes, source: str) -> list[NewsObservation]:
    root = ET.fromstring(xml_bytes)
    observations: list[NewsObservation] = []

    for item in root.findall(".//item"):
        title = _text(item.find("title")) or "Untitled"
        url = _text(item.find("link")) or ""
        published = _parse_date(_text(item.find("pubDate")))
        summary = _text(item.find("description"))
        identity = "|".join((source, title, url, published or ""))
        incident_id = sha256(identity.encode("utf-8")).hexdigest()[:24]
        observations.append(
            NewsObservation(incident_id, source, title, url, published, summary)
        )

    return observations


def fetch_rss(url: str, timeout: float = 10.0) -> list[NewsObservation]:
    request = Request(url, headers={"User-Agent": "KAIROSEED-Agentic-Failure-Observatory/0.1"})
    with urlopen(request, timeout=timeout) as response:
        return parse_rss(response.read(), source=url)


def collect(feeds: Iterable[str]) -> list[dict]:
    observations: list[dict] = []
    for feed in feeds:
        observations.extend(asdict(item) for item in fetch_rss(feed))
    return observations
