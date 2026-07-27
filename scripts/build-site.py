from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PARTIALS = ROOT / "templates" / "partials"
SITE_URL = "https://gavin1424.github.io/qiangge-aquarium/"
LASTMOD = "2026-07-27"


def page_key(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "home"
    if rel.startswith("fish/"):
        return "fish"
    if rel.startswith("guides/"):
        return "guides"
    for name in ("breeding", "gallery", "about", "contact"):
        if rel.startswith(f"{name}/"):
            return name
    return ""


def base_for(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parts) - 1
    return "./" if depth == 0 else "../" * depth


def render_partial(name: str, path: Path) -> str:
    content = (PARTIALS / name).read_text(encoding="utf-8")
    key = page_key(path)
    replacements = {"{{BASE}}": base_for(path)}
    for item in ("home", "fish", "guides", "breeding", "gallery", "about", "contact"):
        replacements[f"{{{{ACTIVE_{item.upper()}}}}}"] = (
            ' aria-current="page"' if key == item else ""
        )
    for token, value in replacements.items():
        content = content.replace(token, value)
    return content


def replace_common(html_text: str, path: Path) -> str:
    blocks = (
        (
            "header.html",
            r"<!-- HEADER:START -->.*?<!-- HEADER:END -->|<header class=\"site-header\">.*?</header>",
        ),
        (
            "footer.html",
            r"<!-- FOOTER:START -->.*?<!-- FOOTER:END -->|<footer class=\"site-footer\">.*?</footer>",
        ),
        (
            "mobile-dock.html",
            r"<!-- MOBILE_DOCK:START -->.*?<!-- MOBILE_DOCK:END -->|<nav class=\"mobile-dock\".*?</nav>",
        ),
    )
    for partial, pattern in blocks:
        rendered = render_partial(partial, path)
        if re.search(pattern, html_text, flags=re.S):
            html_text = re.sub(pattern, rendered, html_text, count=1, flags=re.S)
    return html_text


def ensure_head(html_text: str, path: Path) -> str:
    base = base_for(path)
    rel = path.relative_to(ROOT).as_posix()
    if 'rel="icon"' not in html_text:
        html_text = html_text.replace(
            "</head>",
            f'    <link rel="icon" href="{base}assets/brand/favicon.svg" type="image/svg+xml">\n'
            f'    <link rel="apple-touch-icon" href="{base}assets/brand/apple-touch-icon.png">\n'
            f'    <link rel="manifest" href="{base}site.webmanifest">\n'
            "</head>",
        )
    if "assets/css/brand-v2.css" not in html_text:
        html_text = html_text.replace(
            "</head>",
            f'    <link rel="stylesheet" href="{base}assets/css/brand-v2.css?v=6">\n</head>',
        )
    html_text = re.sub(
        r'(assets/css/brand-v2\.css)(?:\?v=\d+)?',
        r'\1?v=6',
        html_text,
    )
    if "assets/js/site-config.js" not in html_text:
        html_text = html_text.replace(
            "</head>",
            f'    <script src="{base}assets/js/site-config.js" defer></script>\n</head>',
        )

    title_match = re.search(r"<title>(.*?)</title>", html_text, flags=re.S)
    desc_match = re.search(
        r'<meta name="description" content="([^"]*)">', html_text, flags=re.S
    )
    canonical_match = re.search(
        r'<link rel="canonical" href="([^"]*)">', html_text, flags=re.S
    )
    title = title_match.group(1).strip() if title_match else "強哥水族"
    description = (
        desc_match.group(1).strip()
        if desc_match
        else "強哥水族｜異形專賣・專業繁殖・飼養交流"
    )
    canonical = (
        canonical_match.group(1).strip()
        if canonical_match
        else f"{SITE_URL}{rel}"
    )

    if 'property="og:image"' not in html_text:
        social = (
            '    <meta property="og:type" content="website">\n'
            '    <meta property="og:locale" content="zh_TW">\n'
            f'    <meta property="og:title" content="{html.escape(title)}">\n'
            f'    <meta property="og:description" content="{html.escape(description)}">\n'
            f'    <meta property="og:url" content="{html.escape(canonical)}">\n'
            f'    <meta property="og:image" content="{SITE_URL}assets/brand/og-cover.jpg">\n'
            '    <meta name="twitter:card" content="summary_large_image">\n'
            f'    <meta name="twitter:title" content="{html.escape(title)}">\n'
            f'    <meta name="twitter:description" content="{html.escape(description)}">\n'
            f'    <meta name="twitter:image" content="{SITE_URL}assets/brand/og-cover.jpg">\n'
        )
        html_text = html_text.replace("</head>", social + "</head>")

    social_fallbacks = (
        (
            'name="twitter:card"',
            '    <meta name="twitter:card" content="summary_large_image">\n',
        ),
        (
            'name="twitter:title"',
            f'    <meta name="twitter:title" content="{html.escape(title)}">\n',
        ),
        (
            'name="twitter:description"',
            f'    <meta name="twitter:description" content="{html.escape(description)}">\n',
        ),
        (
            'name="twitter:image"',
            f'    <meta name="twitter:image" content="{SITE_URL}assets/brand/og-cover.jpg">\n',
        ),
    )
    for needle, markup in social_fallbacks:
        if needle not in html_text:
            html_text = html_text.replace("</head>", markup + "</head>")

    if (
        rel != "index.html"
        and "404" not in rel
        and '"@type":"BreadcrumbList"' not in html_text
        and '"@type": "BreadcrumbList"' not in html_text
    ):
        items = [
            {"@type": "ListItem", "position": 1, "name": "首頁", "item": SITE_URL}
        ]
        current_name = title.split("｜", 1)[0]
        if rel == "guides/article.html":
            items.append(
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "飼養教學",
                    "item": f"{SITE_URL}guides/",
                }
            )
        items.append(
            {
                "@type": "ListItem",
                "position": len(items) + 1,
                "name": current_name,
                "item": canonical,
            }
        )
        breadcrumb = json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": items,
            },
            ensure_ascii=False,
        )
        html_text = html_text.replace(
            "</head>",
            f'    <script type="application/ld+json">{breadcrumb}</script>\n</head>',
        )
    return html_text


def responsive_picture(fish: dict, base: str, eager: bool = False) -> str:
    image = fish["image"]
    prefix = f"{base}assets/images/{image['folder']}/{image['base']}"
    loading = ' loading="eager" fetchpriority="high"' if eager else ' loading="lazy"'
    return f"""<picture>
      <source type="image/webp" srcset="{prefix}-400.webp 400w, {prefix}-640.webp 640w, {prefix}-960.webp 960w" sizes="(max-width: 860px) 100vw, 52vw">
      <img src="{prefix}-960.jpg" width="960" height="1200" alt="{html.escape(image['alt'])}"{loading} decoding="async">
    </picture>"""


def detail_page(fish: dict) -> str:
    base = "../../"
    slug = fish["id"]
    canonical = f"{SITE_URL}fish/{slug}/"
    image_url = (
        f"{SITE_URL}assets/images/{fish['image']['folder']}/"
        f"{fish['image']['base']}-960.jpg"
    )
    description = (
        f"{fish['name']}外觀分類與一般照護觀察重點。圖片為 AI 外觀示意，"
        "不代表強哥水族實際個體、品系或供應狀況。"
    )
    notes = "".join(f"<li>{html.escape(note)}</li>" for note in fish["notes"])
    breadcrumb = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "首頁", "item": SITE_URL},
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": "魚種總覽",
                    "item": f"{SITE_URL}fish/",
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": fish["name"],
                    "item": canonical,
                },
            ],
        },
        ensure_ascii=False,
    )
    return f"""<!doctype html>
<html lang="zh-Hant">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{html.escape(fish['name'])}外觀與照護重點｜強哥水族</title>
    <meta name="description" content="{html.escape(description)}">
    <meta name="theme-color" content="#031f27">
    <link rel="canonical" href="{canonical}">
    <link rel="icon" href="{base}assets/brand/favicon.svg" type="image/svg+xml">
    <link rel="apple-touch-icon" href="{base}assets/brand/apple-touch-icon.png">
    <link rel="manifest" href="{base}site.webmanifest">
    <meta property="og:type" content="article">
    <meta property="og:locale" content="zh_TW">
    <meta property="og:title" content="{html.escape(fish['name'])}外觀與照護重點｜強哥水族">
    <meta property="og:description" content="{html.escape(description)}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{image_url}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{html.escape(fish['name'])}外觀與照護重點｜強哥水族">
    <meta name="twitter:description" content="{html.escape(description)}">
    <meta name="twitter:image" content="{image_url}">
    <script type="application/ld+json">{breadcrumb}</script>
    <link rel="stylesheet" href="{base}assets/css/styles.css">
    <script src="{base}assets/js/site-config.js" defer></script>
    <script src="{base}assets/js/main.js" defer></script>
  </head>
  <body data-base="{base}">
    <a class="skip-link" href="#main-content">跳到主要內容</a>
    <!-- HEADER:START --><!-- HEADER:END -->
    <main id="main-content">
      <section class="detail-hero">
        <div class="container detail-layout">
          <div class="detail-media">
            {responsive_picture(fish, base, eager=True)}
            <span class="source-badge source-badge--ai">AI 示意</span>
          </div>
          <div class="detail-copy">
            <nav class="breadcrumbs" aria-label="麵包屑"><a href="{base}index.html">首頁</a><span>/</span><a href="../index.html">魚種總覽</a><span>/</span><span>{html.escape(fish['name'])}</span></nav>
            <span class="eyebrow">外觀分類</span>
            <h1>{html.escape(fish['name'])}</h1>
            <p class="detail-lead">{html.escape(fish['summary'])}</p>
            <div class="detail-tags"><span>{html.escape(fish['category'])}</span><span>{html.escape(fish['status'])}</span></div>
            <div class="image-disclosure image-disclosure--compact">
              AI 生成示意圖，僅供網站視覺與外觀分類展示，不代表強哥水族實際個體、品系、現貨或繁殖成果。
            </div>
          </div>
        </div>
      </section>
      <section class="section">
        <div class="container">
          <div class="care-grid">
            <article><span>行為觀察</span><h2>{html.escape(fish['temperament'])}</h2></article>
            <article><span>照護程度</span><h2>{html.escape(fish['careLevel'])}</h2></article>
            <article><span>水質重點</span><h2>{html.escape(fish['waterFocus'])}</h2></article>
            <article><span>環境安排</span><h2>{html.escape(fish['habitat'])}</h2></article>
            <article><span>餵食方向</span><h2>{html.escape(fish['feeding'])}</h2></article>
          </div>
          <div class="detail-notes">
            <div><span class="eyebrow">觀察筆記</span><h2>從來源與多角度特徵開始確認。</h2></div>
            <ul>{notes}</ul>
          </div>
          <div class="notice">品系確認提示：單張 AI 示意圖只能協助理解外觀分類；正式名稱、學名與 L 編號仍需以可靠來源、親魚資訊與實際個體特徵確認。</div>
          <div class="button-row"><a class="button button--primary" href="../index.html">返回魚種總覽</a><a class="button button--outline" href="{base}image-disclosure/index.html">圖片來源說明</a></div>
        </div>
      </section>
    </main>
    <!-- FOOTER:START --><!-- FOOTER:END -->
    <!-- MOBILE_DOCK:START --><!-- MOBILE_DOCK:END -->
  </body>
</html>
"""


def generate_details() -> None:
    fish_list = json.loads((ROOT / "data" / "fish.json").read_text(encoding="utf-8"))
    for fish in fish_list:
        output = ROOT / "fish" / fish["id"] / "index.html"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(detail_page(fish), encoding="utf-8", newline="\n")


def public_html_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.html")
        if "templates" not in path.parts and "qa" not in path.parts
    )


def sync_all() -> None:
    for path in public_html_files():
        source = path.read_text(encoding="utf-8")
        updated = ensure_head(source, path)
        updated = replace_common(updated, path)
        path.write_text(updated, encoding="utf-8", newline="\n")


def generate_sitemap() -> None:
    paths = [
        "",
        "fish/",
        "fish/green-brown-armored/",
        "fish/maze-pattern/",
        "fish/light-stripe/",
        "fish/blue-spotted/",
        "fish/orange-fin/",
        "fish/white-spotted/",
        "fish/gold-spotted/",
        "fish/leopard-pattern/",
        "arrivals/",
        "guides/",
        "guides/article.html",
        "breeding/",
        "gallery/",
        "about/",
        "contact/",
        "privacy/",
        "terms/",
        "image-disclosure/",
    ]
    items = "\n".join(
        f"  <url><loc>{SITE_URL}{path}</loc><lastmod>{LASTMOD}</lastmod></url>"
        for path in paths
    )
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{items}\n"
        "</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    generate_details()
    sync_all()
    generate_sitemap()
    print(f"Built {len(public_html_files())} public HTML files.")
