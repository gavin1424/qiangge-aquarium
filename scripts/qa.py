from __future__ import annotations

import csv
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
WARNINGS: list[str] = []


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self.images: list[dict[str, str | None]] = []
        self.html_lang: str | None = None
        self.has_viewport = False
        self.has_description = False
        self.has_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.html_lang = values.get("lang")
        elif tag == "meta":
            if values.get("name") == "viewport":
                self.has_viewport = True
            if values.get("name") == "description":
                self.has_description = True
        elif tag == "title":
            self.has_title = True
        elif tag == "a" and values.get("href"):
            self.links.append(("href", values["href"] or ""))
        elif tag in {"link", "script", "source"}:
            for key in ("href", "src"):
                if values.get(key):
                    self.links.append((key, values[key] or ""))
            if values.get("srcset"):
                for candidate in (values["srcset"] or "").split(","):
                    self.links.append(("srcset", candidate.strip().split()[0]))
        elif tag == "img":
            self.images.append(values)
            if values.get("src"):
                self.links.append(("src", values["src"] or ""))


def internal_path(page: Path, value: str) -> Path | None:
    if not value or value.startswith(("#", "mailto:", "tel:", "data:")):
        return None
    parsed = urlparse(value)
    if parsed.scheme or parsed.netloc:
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    resolved = (page.parent / path).resolve()
    if path.endswith("/"):
        resolved = resolved / "index.html"
    return resolved


html_files = sorted(ROOT.rglob("*.html"))
if len(html_files) < 10:
    ERRORS.append(f"Expected at least 10 HTML pages, found {len(html_files)}")

for page in html_files:
    parser = PageParser()
    text = page.read_text(encoding="utf-8")
    parser.feed(text)
    rel = page.relative_to(ROOT)

    if parser.html_lang != "zh-Hant":
        ERRORS.append(f"{rel}: missing html lang=zh-Hant")
    if not parser.has_viewport:
        ERRORS.append(f"{rel}: missing viewport meta")
    if not parser.has_title:
        ERRORS.append(f"{rel}: missing title")
    if page.name != "404.html" and not parser.has_description:
        ERRORS.append(f"{rel}: missing meta description")

    for image in parser.images:
        if image.get("alt") is None:
            ERRORS.append(f"{rel}: image missing alt")
        if not image.get("width") or not image.get("height"):
            ERRORS.append(f"{rel}: image missing intrinsic dimensions")
        if image.get("loading") not in {"lazy", "eager"} and page.name != "404.html":
            WARNINGS.append(f"{rel}: image has no explicit loading policy")

    for _, value in parser.links:
        if re.match(r"^/(assets|index\.html)", value):
            ERRORS.append(f"{rel}: root-absolute project path is forbidden: {value}")
        target = internal_path(page, value)
        if target is not None and not target.exists():
            ERRORS.append(f"{rel}: missing local target {value}")

json.loads((ROOT / "data" / "fish.json").read_text(encoding="utf-8"))

with (ROOT / "ASSET_MANIFEST.csv").open(encoding="utf-8-sig", newline="") as file:
    rows = list(csv.DictReader(file))
    if len(rows) < 13:
        ERRORS.append(f"ASSET_MANIFEST.csv expected at least 13 rows, found {len(rows)}")
    if not all(row.get("原始檔名") and row.get("新檔名") for row in rows):
        ERRORS.append("ASSET_MANIFEST.csv contains incomplete rows")

optimized = sorted((ROOT / "assets" / "images" / "optimized").glob("*"))
if len(optimized) != 32:
    ERRORS.append(f"Expected 32 optimized image files, found {len(optimized)}")

required = [
    "AGENTS.md",
    "README.md",
    "PROJECT_STATUS.md",
    "QIANGGE_AQUARIUM_DEPLOY_REPORT_ZH.md",
    "ASSET_MANIFEST.csv",
    "MISSING_ASSETS_REPORT_ZH.md",
    ".nojekyll",
    "robots.txt",
    "sitemap.xml",
]
for name in required:
    if not (ROOT / name).exists():
        ERRORS.append(f"Missing required file: {name}")

print(f"HTML pages: {len(html_files)}")
print(f"Manifest rows: {len(rows)}")
print(f"Optimized images: {len(optimized)}")
print(f"Warnings: {len(WARNINGS)}")
for warning in WARNINGS:
    print(f"WARN: {warning}")
print(f"Errors: {len(ERRORS)}")
for error in ERRORS:
    print(f"ERROR: {error}")

sys.exit(1 if ERRORS else 0)
