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
  const prefix = `${basePath}assets/images/optimized/${image.base}`;

  source.type = "image/webp";
  source.srcset = `${prefix}-400.webp 400w, ${prefix}-640.webp 640w, ${prefix}-960.webp 960w`;
  source.sizes = options.sizes || "(max-width: 620px) 100vw, 33vw";

  img.src = `${prefix}-960.jpg`;
  img.alt = image.alt;
  img.width = 960;
  img.height = 1200;
  img.loading = options.eager ? "eager" : "lazy";
  img.decoding = "async";
  if (options.eager) {
    img.fetchPriority = "high";
  }

  picture.append(source, img);
  return picture;
}

const menuToggle = qs("[data-menu-toggle]");
const siteNav = qs("[data-site-nav]");

if (menuToggle && siteNav) {
  const closeMenu = () => {
    menuToggle.setAttribute("aria-expanded", "false");
    menuToggle.textContent = "選單";
    siteNav.classList.remove("is-open");
    body.classList.remove("menu-open");
  };

  menuToggle.addEventListener("click", () => {
    const willOpen = menuToggle.getAttribute("aria-expanded") !== "true";
    menuToggle.setAttribute("aria-expanded", String(willOpen));
    menuToggle.textContent = willOpen ? "關閉" : "選單";
    siteNav.classList.toggle("is-open", willOpen);
    body.classList.toggle("menu-open", willOpen);
  });

  siteNav.addEventListener("click", (event) => {
    if (event.target instanceof HTMLAnchorElement) {
      closeMenu();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeMenu();
      menuToggle.focus();
    }
  });
}

qsa("[data-current-year]").forEach((element) => {
  element.textContent = String(new Date().getFullYear());
});

async function loadFishData() {
  const response = await fetch(`${basePath}data/fish.json`);
  if (!response.ok) {
    throw new Error(`Fish data request failed: ${response.status}`);
  }
  return response.json();
}

function createFishCard(fish) {
  const article = document.createElement("article");
  article.className = "fish-card";

  const media = document.createElement("div");
  media.className = "fish-card__media";
  media.append(createResponsivePicture(fish.image));

  const status = document.createElement("span");
  status.className = "status-label";
  status.textContent = fish.status;
  media.append(status);

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
  footer.href = `${basePath}fish/detail.html?id=${encodeURIComponent(fish.id)}`;
  footer.innerHTML = "<span>查看照護重點</span><span aria-hidden=\"true\">→</span>";
  footer.setAttribute("aria-label", `查看${fish.name}照護重點`);

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
        "<h2>沒有符合條件的魚種</h2><p>請清除搜尋文字或改用其他外觀分類。</p>";
      fishGrid.append(empty);
    }

    if (resultMeta) {
      resultMeta.textContent = `顯示 ${visible.length} 筆實際個體資料；正式品系仍待人工確認。`;
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
      if (resultMeta) {
        resultMeta.textContent = "資料載入失敗";
      }
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

const detailRoot = qs("[data-fish-detail]");

if (detailRoot) {
  const params = new URLSearchParams(window.location.search);
  const requestedId = params.get("id") || "light-stripe";

  loadFishData()
    .then((fishList) => {
      const fish =
        fishList.find((item) => item.id === requestedId) ||
        fishList.find((item) => item.id === "light-stripe") ||
        fishList[0];

      document.title = `${fish.name}｜強哥水族`;
      const imageSlot = qs("[data-detail-image]", detailRoot);
      const nameSlots = qsa("[data-detail-name]", detailRoot);
      const category = qs("[data-detail-category]", detailRoot);
      const summary = qs("[data-detail-summary]", detailRoot);
      const temperament = qs("[data-detail-temperament]", detailRoot);
      const careLevel = qs("[data-detail-care]", detailRoot);
      const water = qs("[data-detail-water]", detailRoot);
      const habitat = qs("[data-detail-habitat]", detailRoot);
      const feeding = qs("[data-detail-feeding]", detailRoot);
      const notes = qs("[data-detail-notes]", detailRoot);

      if (imageSlot) {
        imageSlot.replaceChildren(
          createResponsivePicture(fish.image, {
            sizes: "(max-width: 860px) 100vw, 50vw",
            eager: true,
          })
        );
      }

      nameSlots.forEach((slot) => {
        slot.textContent = fish.name;
      });
      if (category) category.textContent = `${fish.category}・${fish.status}`;
      if (summary) summary.textContent = fish.summary;
      if (temperament) temperament.textContent = fish.temperament;
      if (careLevel) careLevel.textContent = fish.careLevel;
      if (water) water.textContent = fish.waterFocus;
      if (habitat) habitat.textContent = fish.habitat;
      if (feeding) feeding.textContent = fish.feeding;
      if (notes) {
        notes.replaceChildren();
        fish.notes.forEach((note) => {
          const li = document.createElement("li");
          li.textContent = note;
          notes.append(li);
        });
      }
    })
    .catch(() => {
      detailRoot.innerHTML =
        '<div class="container section"><div class="empty-state"><h1>魚種資料暫時無法載入</h1><p>請返回魚種總覽後重新選擇。</p><a class="button button--primary" href="./index.html">返回魚種總覽</a></div></div>';
    });
}

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
      "強哥水族｜預約／交流內容",
      `稱呼：${formData.get("name")}`,
      `交流主題：${formData.get("topic")}`,
      `偏好日期：${formData.get("date") || "未指定"}`,
      `聯絡方式：${formData.get("contact") || "尚未填寫"}`,
      "",
      "想了解的內容：",
      String(formData.get("message") || "").trim(),
      "",
      "備註：網站不會自動送出或儲存以上資料。",
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
      copyButton.textContent = "已複製";
    } catch {
      const range = document.createRange();
      range.selectNodeContents(summaryText);
      const selection = window.getSelection();
      selection?.removeAllRanges();
      selection?.addRange(range);
      copyButton.textContent = "請手動複製";
    }

    window.setTimeout(() => {
      copyButton.textContent = "複製內容";
    }, 2200);
  });
}
