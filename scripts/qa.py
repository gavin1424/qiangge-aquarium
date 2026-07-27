from __future__ import annotations

import csv
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
WARNINGS: list[str] = []
PUBLIC_HTML = sorted(
    path for path in ROOT.rglob("*.html") if "templates" not in path.parts
)
AI_DISCLOSURE = (
    "AI 生成示意圖，僅供網站視覺與外觀分類展示，"
    "不代表魚宅水族實際個體、品系、現貨或繁殖成果。"
)
STATIC_SLUGS = {
    "green-brown-armored",
    "maze-pattern",
    "light-stripe",
    "blue-spotted",
    "orange-fin",
    "white-spotted",
    "gold-spotted",
    "leopard-pattern",
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.images: list[dict[str, str | None]] = []
        self.html_lang: str | None = None
        self.has_viewport = False
        self.has_description = False
        self.has_title = False
        self.has_canonical = False
        self.has_theme_color = False
        self.has_favicon = False
        self.has_manifest = False
        self.has_og_image = False
        self.has_twitter_card = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.html_lang = values.get("lang")
        elif tag == "meta":
            name = values.get("name")
            prop = values.get("property")
            if name == "viewport":
                self.has_viewport = True
            if name == "description":
                self.has_description = True
            if name == "theme-color":
                self.has_theme_color = True
            if name == "twitter:card":
                self.has_twitter_card = True
            if prop == "og:image":
                self.has_og_image = True
        elif tag == "title":
            self.has_title = True
        elif tag == "link":
            rel = values.get("rel", "")
            if rel == "canonical":
                self.has_canonical = True
            if "icon" in rel:
                self.has_favicon = True
            if rel == "manifest":
                self.has_manifest = True
            if values.get("href"):
                self.links.append(values["href"] or "")
        elif tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        elif tag in {"script", "source"}:
            if values.get("src"):
                self.links.append(values["src"] or "")
            if values.get("srcset"):
                for candidate in (values["srcset"] or "").split(","):
                    self.links.append(candidate.strip().split()[0])
        elif tag == "img":
            self.images.append(values)
            if values.get("src"):
                self.links.append(values["src"] or "")
            if values.get("srcset"):
                for candidate in (values["srcset"] or "").split(","):
                    self.links.append(candidate.strip().split()[0])


def internal_path(page: Path, value: str) -> Path | None:
    if not value or value.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
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


if len(PUBLIC_HTML) != 22:
    ERRORS.append(f"Expected 22 public HTML pages, found {len(PUBLIC_HTML)}")

for page in PUBLIC_HTML:
    parser = PageParser()
    text = page.read_text(encoding="utf-8")
    parser.feed(text)
    rel = page.relative_to(ROOT)

    checks = {
        "lang=zh-Hant": parser.html_lang == "zh-Hant",
        "viewport": parser.has_viewport,
        "title": parser.has_title,
        "theme-color": parser.has_theme_color,
        "favicon": parser.has_favicon,
        "manifest": parser.has_manifest,
        "og:image": parser.has_og_image,
        "twitter:card": parser.has_twitter_card,
    }
    if page.name != "404.html":
        checks["description"] = parser.has_description
        checks["canonical"] = parser.has_canonical
    for label, passed in checks.items():
        if not passed:
            ERRORS.append(f"{rel}: missing {label}")

    if "brand-v2.css" not in text:
        ERRORS.append(f"{rel}: brand-v2.css is not loaded")
    if page.relative_to(ROOT).as_posix() != "fish/detail.html" and 'aria-label="魚宅水族首頁"' not in text:
        ERRORS.append(f"{rel}: shared fish logo is missing")

    for image in parser.images:
        if image.get("alt") is None:
            ERRORS.append(f"{rel}: image missing alt")
        if not image.get("width") or not image.get("height"):
            ERRORS.append(f"{rel}: image missing intrinsic dimensions")

    for value in parser.links:
        if re.match(r"^/(assets|index\.html)", value):
            ERRORS.append(f"{rel}: root-absolute project path is forbidden: {value}")
        target = internal_path(page, value)
        if target is not None and not target.exists():
            ERRORS.append(f"{rel}: missing local target {value}")


fish_data = json.loads((ROOT / "data" / "fish.json").read_text(encoding="utf-8"))
if len(fish_data) != 8:
    ERRORS.append(f"Expected 8 fish records, found {len(fish_data)}")
for fish in fish_data:
    if fish.get("image", {}).get("sourceType") != "ai-generated":
        ERRORS.append(f"{fish.get('id')}: sourceType must be ai-generated")
    if fish.get("image", {}).get("sourceLabel") != "AI 示意":
        ERRORS.append(f"{fish.get('id')}: missing AI source label")
    if fish.get("id") not in STATIC_SLUGS:
        ERRORS.append(f"{fish.get('id')}: invalid static slug")
    detail = ROOT / "fish" / fish["id"] / "index.html"
    if not detail.exists():
        ERRORS.append(f"Missing static detail page: {detail.relative_to(ROOT)}")


arrivals = json.loads((ROOT / "data" / "arrivals.json").read_text(encoding="utf-8"))
valid_statuses = {
    "image-updated",
    "available-for-inquiry",
    "pending-identification",
    "not-available",
    "archived",
}
if len(arrivals) != 8:
    ERRORS.append(f"Expected 8 arrivals records, found {len(arrivals)}")
for record in arrivals:
    if record.get("displayStatus") not in valid_statuses:
        ERRORS.append(f"Invalid arrival status: {record.get('displayStatus')}")
    if record.get("inquiryAvailable") is not False:
        ERRORS.append(f"Unverified inquiry status for {record.get('fishId')}")
    if record.get("updatedAt"):
        ERRORS.append(f"Unverified arrival date for {record.get('fishId')}")


provenance = json.loads(
    (ROOT / "assets" / "data" / "asset-provenance.json").read_text(encoding="utf-8")
)
if len(provenance) != 13:
    ERRORS.append(f"Expected 13 provenance records, found {len(provenance)}")
source_types = {"camera-photo", "ai-generated", "design-reference"}
ai_records = [row for row in provenance if row["sourceType"] == "ai-generated"]
camera_records = [row for row in provenance if row["sourceType"] == "camera-photo"]
if len(ai_records) != 8:
    ERRORS.append(f"Expected 8 AI provenance records, found {len(ai_records)}")
if camera_records:
    ERRORS.append(f"Expected 0 verified camera photos, found {len(camera_records)}")
for row in provenance:
    if row.get("sourceType") not in source_types:
        ERRORS.append(f"Invalid sourceType: {row.get('sourceType')}")
    if row.get("sourceType") == "ai-generated":
        if row.get("isAiGenerated") is not True or row.get("canClaimRealFish") is not False:
            ERRORS.append(f"Invalid AI provenance flags: {row.get('publicFilename')}")
        if row.get("disclosure") != AI_DISCLOSURE:
            ERRORS.append(f"Invalid AI disclosure: {row.get('publicFilename')}")


for csv_name in ("ASSET_MANIFEST.csv", "ASSET_PROVENANCE.csv"):
    with (ROOT / csv_name).open(encoding="utf-8-sig", newline="") as file:
        rows = list(csv.DictReader(file))
        if len(rows) != 13:
            ERRORS.append(f"{csv_name} expected 13 rows, found {len(rows)}")
        if not rows or not all(all(value.strip() for value in row.values()) for row in rows):
            ERRORS.append(f"{csv_name} contains incomplete rows")
        if csv_name == "ASSET_PROVENANCE.csv":
            csv_ai = [row for row in rows if row["sourceType"] == "ai-generated"]
            if any(row["disclosure"] != AI_DISCLOSURE for row in csv_ai):
                ERRORS.append("ASSET_PROVENANCE.csv contains inconsistent AI disclosure")


illustration_files = sorted((ROOT / "assets" / "images" / "illustrations").glob("*"))
photo_files = [
    path
    for path in (ROOT / "assets" / "images" / "photography").glob("*")
    if path.name != ".gitkeep"
]
if len(illustration_files) != 40:
    ERRORS.append(f"Expected 40 illustration image files, found {len(illustration_files)}")
if photo_files:
    ERRORS.append(f"Expected 0 photography files, found {len(photo_files)}")


forbidden_positive_claims = {
    "REAL FISH",
    "網站只使用實際魚隻照片",
    "八尾實際個體",
    "全部為真實魚照",
}
public_text = "\n".join(path.read_text(encoding="utf-8") for path in PUBLIC_HTML)
for claim in forbidden_positive_claims:
    if claim in public_text:
        ERRORS.append(f"Forbidden asset claim remains: {claim}")
if public_text.count("AI 示意") < 30:
    WARNINGS.append("AI 示意 label count is lower than expected")


sitemap = ROOT / "sitemap.xml"
tree = ET.parse(sitemap)
namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = tree.findall("s:url", namespace)
locations = [url.findtext("s:loc", namespaces=namespace) or "" for url in urls]
if len(locations) != 20:
    ERRORS.append(f"Expected 20 sitemap URLs, found {len(locations)}")
for url in urls:
    if not url.findtext("s:lastmod", namespaces=namespace):
        ERRORS.append("Sitemap URL missing lastmod")
for slug in STATIC_SLUGS:
    expected = f"https://gavin1424.github.io/qiangge-aquarium/fish/{slug}/"
    if expected not in locations:
        ERRORS.append(f"Sitemap missing {expected}")
if any("detail.html" in loc or "?" in loc for loc in locations):
    ERRORS.append("Sitemap includes compatibility or query URL")


required = [
    "AGENTS.md",
    "README.md",
    "PROJECT_STATUS.md",
    "YUZHAI_AQUARIUM_DEPLOY_REPORT_ZH.md",
    "ASSET_MANIFEST.csv",
    "ASSET_PROVENANCE.csv",
    "MISSING_ASSETS_REPORT_ZH.md",
    "BRAND_V2_QA_REPORT_ZH.md",
    "site.webmanifest",
    ".nojekyll",
    "robots.txt",
    "sitemap.xml",
    "assets/brand/logo-fish.svg",
    "assets/brand/favicon.svg",
    "assets/brand/apple-touch-icon.png",
    "assets/brand/icon-192.png",
    "assets/brand/icon-512.png",
    "assets/brand/og-cover.jpg",
    "assets/js/site-config.js",
    "templates/partials/header.html",
    "templates/partials/footer.html",
    "templates/partials/mobile-dock.html",
]
for name in required:
    if not (ROOT / name).exists():
        ERRORS.append(f"Missing required file: {name}")


print(f"Public HTML pages: {len(PUBLIC_HTML)}")
print(f"Fish records: {len(fish_data)}")
print(f"AI provenance records: {len(ai_records)}")
print(f"Camera-photo provenance records: {len(camera_records)}")
print(f"Illustration image files: {len(illustration_files)}")
print(f"Sitemap URLs: {len(locations)}")
print(f"Warnings: {len(WARNINGS)}")
for warning in WARNINGS:
    print(f"WARN: {warning}")
print(f"Errors: {len(ERRORS)}")
for error in ERRORS:
    print(f"ERROR: {error}")

sys.exit(1 if ERRORS else 0)
