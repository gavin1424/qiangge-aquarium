# 強哥水族品牌 V2 QA 報告

更新日期：2026-07-27 12:15（Asia/Taipei）

## 結論

本機品牌 V2 QA 通過。22 個公開 HTML、8 個獨立魚種詳情頁、20 筆 sitemap URL 與 108 個本機頁面／資源 URL 均可讀取。瀏覽器 Console Error、破圖、404 資源及橫向溢位皆為 0。

`4173` 已由不屬於本專案的既有 Vite 服務占用；基於不可干擾其他網站的安全規則，本次未終止該程序，改以相同純靜態方式在 `127.0.0.1:4174` 完成全部本機瀏覽器 QA。

## 素材來源

- AI 生成示意圖：8 張。
- 已確認使用者手機實拍：0 張。
- 設計參考圖：5 張，只存放於 `assets/images/design-reference/`，未載入公開頁面。
- 8 張 AI 圖的卡片、Hero、相簿與詳情頁均有可見「AI 示意」標籤。
- `REAL FISH`、`網站只使用實際魚隻照片`、`八尾實際個體`、`全部為真實魚照`：公開頁面 0 筆。
- AI 圖對應 `assets/data/asset-provenance.json` 與 `ASSET_PROVENANCE.csv`，`canClaimRealFish` 均為 `false`。

## 自動 QA

執行：

```powershell
python scripts\build-site.py
python scripts\qa.py
node --check assets\js\main.js
python -m py_compile scripts\build-site.py scripts\qa.py
git diff --check
```

結果：

- 公開 HTML：22。
- 魚種資料：8。
- AI 來源紀錄：8。
- camera-photo 來源紀錄：0。
- AI 圖檔與響應式版本：40。
- sitemap URL：20。
- 警告：0。
- 錯誤：0。

## HTTP 與路由

- 解析全部公開 HTML、`srcset`、CSS、JavaScript、圖片、manifest 與 sitemap 後，共驗證 108 個本機 URL。
- HTTP 非 200：0。
- 8 個魚種靜態頁：全部 HTTP 200。
- `fish/detail.html?id=orange-fin`：正確導向 `fish/orange-fin/`。
- sitemap 的 20 個 URL：全部可對應本機 HTTP 200。

## 響應式 QA

已測試：

- 1440 × 1000
- 1280 × 900
- 1024 × 768
- 768 × 1024
- 390 × 844
- 360 × 800

六種尺寸的 `documentElement.scrollWidth` 均未大於視窗內容寬度，橫向溢位為 0。390 與 360 寬度的首頁首屏均包含魚形 Logo、品牌名稱、品牌定位、完整魚圖與主要 CTA。

桌機 Logo：52 × 38 CSS px。手機 Logo：42 × 32 CSS px。Footer Logo 計算顏色為白色。手機 Dock 顯示四個 SVG 圖示與 active 狀態，頁尾最後一個連結與固定 Dock 無重疊。

## 互動與鍵盤

- 手機選單：可開啟，`aria-expanded` 正確切換，可用 Escape 關閉，關閉後解除 body 捲動鎖定。
- 魚種篩選：「星點系」可選取，`aria-pressed="true"`。
- 搜尋：於星點系輸入「白點」後只顯示「白點星紋異形」。
- 詢問內容產生器：必填欄位、原生 select、內容產生與複製按鈕可操作。
- 測試產生內容時，頁面只顯示「已產生詢問內容」，不顯示「已送出」或「傳送成功」。
- 所有導覽、CTA、魚種詳情與政策連結均有有效目的地。
- 專案沒有 FAQ 折疊元件；其餘選單、篩選、表單與按鈕均完成鍵盤檢查。

## 圖片與標示

- 瀏覽器逐頁檢查 22 個公開頁面：破圖 0、缺少 alt 0。
- 瀏覽器找到的 AI 圖均能在最近的影像容器找到 `.source-badge--ai`，未標示 AI 圖為 0。
- 所有魚圖使用 `object-fit: contain`，未裁切魚頭、尾部或背鰭，未拉伸。
- Hero 使用 eager、preload 與高優先載入；其他魚圖依頁面位置使用 lazy loading。
- favicon 為魚形 SVG；Apple touch icon 與 192／512 App icon 已建立。

## SEO

- 8 個魚種詳情頁有 8 組不重複 title 與 meta description。
- 每個魚種詳情頁均有 canonical、OG、Twitter Card、BreadcrumbList 與繁體中文 alt。
- 首頁有 WebSite 與 Organization JSON-LD，Organization 未加入未確認聯絡資訊。
- 所有內頁有 BreadcrumbList。
- `sitemap.xml` 有 20 筆 URL、均含 `lastmod`，不含 query parameter、測試頁或 `detail.html`。
- `privacy/`、`terms/`、`image-disclosure/` 均完成並加入 Footer。

## Lighthouse

報告：`qa/lighthouse-home-v2.json`

- Performance：97
- Accessibility：100
- Best Practices：100
- SEO：100

Lighthouse 在 Windows 清除自身暫存資料夾時出現一次 EPERM 清理訊息，但 JSON 報告已完整產生且可正常解析；不影響頁面分數或網站執行。

## Console 與瀏覽器結果

- Browser Console Error：0。
- 破圖：0。
- 404 資源：0。
- 橫向溢位：0。
- Header／Footer／404／手機選單 Logo：一致使用異形魚標誌。
- AI 標籤缺漏：0。

## 視覺證據

- `qa/screenshots/home-desktop-v2.png`：桌機首頁。
- `qa/screenshots/home-mobile-v2.png`：390 × 844 手機首頁。
- `qa/screenshots/fish-list-v2.png`：魚種總覽。
- `qa/screenshots/fish-detail-v2.png`：魚種詳情。
- `qa/screenshots/breeding-v2.png`：繁殖紀錄。
- `qa/screenshots/contact-v2.png`：詢問整理。
- `qa/screenshots/compare-home-desktop-v2.jpg`：首頁概念圖與 V2。
- `qa/screenshots/compare-home-mobile-v2.jpg`：手機概念圖與 V2。
- `qa/screenshots/compare-fish-list-v2.jpg`：魚種概念圖與 V2。
- `qa/screenshots/compare-fish-detail-v2.jpg`：詳情概念圖與 V2。
- `qa/screenshots/compare-breeding-v2.jpg`：V1 與 V2 繁殖頁。
- `qa/screenshots/compare-contact-v2.jpg`：V1 與 V2 詢問頁。

## 尚待使用者補充

五張手機實拍原檔仍缺少：

1. 手持紅鰭條紋異形魚。
2. 紅色水盆、魚與黃色魚卵小碗。
3. 白色六角繁殖管與多尾異形魚。
4. 淺色／白化異形魚透明繁殖盒側面照。
5. 同一尾魚的透明繁殖盒俯視照。

官方聯絡設定仍為空白：LINE URL、LINE ID、Instagram、Facebook、Email、電話、地址、營業時間、地圖 URL。

## 本機最終狀態

本機 QA：通過。正式站仍需在合併與 GitHub Pages 建置完成後，重新驗證 Logo、favicon、AI 標示、八個魚種頁與 sitemap。
