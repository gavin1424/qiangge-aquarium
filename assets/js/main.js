"use strict";

const body = document.body;
const basePath = body.dataset.base || "./";

function qs(selector, context = document) {
  return context.querySelector(selector);
}

function qsa(selector, context = document) {
  return Array.from(context.querySelectorAll(selector));
}

function createResponsivePicture(image, options = {}) {
  const picture = document.createElement("picture");
  const source = document.createElement("source");
  const img = document.createElement("img");
  const folder = image.folder || "illustrations";
  const prefix = `${basePath}assets/images/${folder}/${image.base}`;

  source.type = "image/webp";
  source.srcset = `${prefix}-400.webp 400w, ${prefix}-640.webp 640w, ${prefix}-960.webp 960w`;
  source.sizes = options.sizes || "(max-width: 620px) 100vw, 33vw";

  img.src = `${prefix}-960.jpg`;
  img.alt = image.alt;
  img.width = 960;
  img.height = 1200;
  img.loading = options.eager ? "eager" : "lazy";
  img.decoding = "async";
  if (options.eager) img.fetchPriority = "high";

  picture.append(source, img);
  return picture;
}

function sourceBadge(label = "AI 示意", type = "ai-generated") {
  const badge = document.createElement("span");
  badge.className =
    type === "camera-photo"
      ? "source-badge source-badge--camera"
      : "source-badge source-badge--ai";
  badge.textContent = label;
  return badge;
}

const menuToggle = qs("[data-menu-toggle]");
const siteNav = qs("[data-site-nav]");

if (menuToggle && siteNav) {
  const label = qs("span", menuToggle);
  const closeMenu = (restoreFocus = false) => {
    menuToggle.setAttribute("aria-expanded", "false");
    if (label) label.textContent = "選單";
    siteNav.classList.remove("is-open");
    body.classList.remove("menu-open");
    if (restoreFocus) menuToggle.focus();
  };

  menuToggle.addEventListener("click", () => {
    const willOpen = menuToggle.getAttribute("aria-expanded") !== "true";
    menuToggle.setAttribute("aria-expanded", String(willOpen));
    if (label) label.textContent = willOpen ? "關閉" : "選單";
    siteNav.classList.toggle("is-open", willOpen);
    body.classList.toggle("menu-open", willOpen);
    if (willOpen) qs("a", siteNav)?.focus();
  });

  siteNav.addEventListener("click", (event) => {
    if (event.target instanceof HTMLAnchorElement) closeMenu();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && siteNav.classList.contains("is-open")) {
      closeMenu(true);
    }
  });
}

qsa("[data-current-year]").forEach((element) => {
  element.textContent = String(new Date().getFullYear());
});

async function loadFishData() {
  const response = await fetch(`${basePath}data/fish.json`);
  if (!response.ok) throw new Error(`Fish data request failed: ${response.status}`);
  return response.json();
}

function createFishCard(fish) {
  const article = document.createElement("article");
  article.className = "fish-card";

  const media = document.createElement("div");
  media.className = "fish-card__media";
  media.append(createResponsivePicture(fish.image));
  media.append(sourceBadge(fish.image.sourceLabel, fish.image.sourceType));

  const content = document.createElement("div");
  content.className = "fish-card__body";

  const category = document.createElement("div");
  category.className = "fish-card__category";
  category.textContent = fish.category;

  const heading = document.createElement("h2");
  heading.textContent = fish.name;

  const summary = document.createElement("p");
  summary.textContent = fish.summary;

  const footer = document.createElement("a");
  footer.className = "fish-card__footer";
  footer.href = `${basePath}fish/${encodeURIComponent(fish.id)}/`;
  footer.innerHTML = "<span>查看外觀與照護重點</span><span aria-hidden=\"true\">→</span>";
  footer.setAttribute("aria-label", `查看${fish.name}外觀與照護重點`);

  content.append(category, heading, summary, footer);
  article.append(media, content);
  return article;
}

const fishGrid = qs("[data-fish-grid]");

if (fishGrid) {
  const resultMeta = qs("[data-result-meta]");
  const searchInput = qs("[data-fish-search]");
  const filterButtons = qsa("[data-filter]");
  let allFish = [];
  let activeFilter = "全部";

  const render = () => {
    const query = (searchInput?.value || "").trim().toLocaleLowerCase("zh-Hant");
    const visible = allFish.filter((fish) => {
      const matchesFilter =
        activeFilter === "全部" || fish.category === activeFilter;
      const haystack = `${fish.name} ${fish.category} ${fish.summary}`.toLocaleLowerCase(
        "zh-Hant"
      );
      return matchesFilter && (!query || haystack.includes(query));
    });

    fishGrid.replaceChildren();
    visible.forEach((fish) => fishGrid.append(createFishCard(fish)));

    if (!visible.length) {
      const empty = document.createElement("div");
      empty.className = "empty-state";
      empty.innerHTML =
        "<h2>沒有符合條件的外觀分類</h2><p>請清除搜尋文字或改用其他分類。</p>";
      fishGrid.append(empty);
    }

    if (resultMeta) {
      resultMeta.textContent = `顯示 ${visible.length} 筆 AI 外觀示意；正式品系仍待來源資料確認。`;
    }
  };

  loadFishData()
    .then((fish) => {
      allFish = fish;
      render();
    })
    .catch(() => {
      fishGrid.innerHTML =
        '<div class="empty-state"><h2>魚種資料暫時無法載入</h2><p>請重新整理頁面，或稍後再試。</p></div>';
      if (resultMeta) resultMeta.textContent = "資料載入失敗";
    });

  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      activeFilter = button.dataset.filter || "全部";
      filterButtons.forEach((item) => {
        const active = item === button;
        item.classList.toggle("is-active", active);
        item.setAttribute("aria-pressed", String(active));
      });
      render();
    });
  });

  searchInput?.addEventListener("input", render);
}

const detailRedirect = qs("[data-detail-redirect]");

if (detailRedirect) {
  const params = new URLSearchParams(window.location.search);
  const requestedId = params.get("id");
  const known = new Set([
    "green-brown-armored",
    "maze-pattern",
    "light-stripe",
    "blue-spotted",
    "orange-fin",
    "white-spotted",
    "gold-spotted",
    "leopard-pattern",
  ]);
  const target = known.has(requestedId) ? requestedId : "light-stripe";
  window.location.replace(`./${target}/`);
}

function buildOfficialChannels() {
  const root = qs("[data-contact-channels]");
  const emptyNotice = qs("[data-no-contact-channel]");
  const detailsRoot = qs("[data-contact-details]");
  if (!root) return;

  const config = window.YUZHAI_CONFIG || {};
  const links = [];
  const add = (label, href, external = true) => {
    if (!href) return;
    const link = document.createElement("a");
    link.className = "button button--outline";
    link.href = href;
    link.textContent = label;
    if (external) {
      link.target = "_blank";
      link.rel = "noopener noreferrer";
    }
    links.push(link);
  };

  add("LINE 詢問", config.lineUrl);
  add("Instagram 私訊", config.instagramUrl);
  add("Facebook 訊息", config.facebookUrl);
  add("Email 詢問", config.email ? `mailto:${config.email}` : "", false);
  add("電話聯絡", config.phone ? `tel:${config.phone}` : "", false);
  add("查看地圖", config.address && config.mapUrl ? config.mapUrl : "");

  root.replaceChildren(...links);
  root.hidden = links.length === 0;
  if (emptyNotice) emptyNotice.hidden = links.length > 0;

  if (detailsRoot) {
    const details = [
      ["LINE ID", config.lineId],
      ["地址", config.address],
      ["營業時間", config.openingHours],
    ].filter(([, value]) => value);
    detailsRoot.replaceChildren(
      ...details.map(([label, value]) => {
        const wrapper = document.createElement("div");
        const term = document.createElement("dt");
        const description = document.createElement("dd");
        term.textContent = label;
        description.textContent = value;
        wrapper.append(term, description);
        return wrapper;
      })
    );
    detailsRoot.hidden = details.length === 0;
  }
}

buildOfficialChannels();

const contactForm = qs("[data-contact-form]");

if (contactForm) {
  const output = qs("[data-summary-output]");
  const summaryText = qs("[data-summary-text]");
  const copyButton = qs("[data-copy-summary]");

  contactForm.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!contactForm.reportValidity()) return;

    const formData = new FormData(contactForm);
    const summary = [
      "魚宅水族｜詢問內容",
      `稱呼：${formData.get("name")}`,
      `詢問主題：${formData.get("topic")}`,
      `偏好日期：${formData.get("date") || "未指定"}`,
      `回覆方式：${formData.get("contact") || "未填寫"}`,
      "",
      "想了解的內容：",
      String(formData.get("message") || "").trim(),
    ].join("\n");

    if (summaryText) summaryText.textContent = summary;
    if (output) output.hidden = false;
    output?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  });

  copyButton?.addEventListener("click", async () => {
    const text = summaryText?.textContent || "";
    if (!text) return;

    try {
      await navigator.clipboard.writeText(text);
      copyButton.textContent = "已複製詢問內容";
    } catch {
      const range = document.createRange();
      range.selectNodeContents(summaryText);
      const selection = window.getSelection();
      selection?.removeAllRanges();
      selection?.addRange(range);
      copyButton.textContent = "請手動複製";
    }

    window.setTimeout(() => {
      copyButton.textContent = "複製詢問內容";
    }, 2200);
  });
}
