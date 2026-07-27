# Design QA

## 比對目標

概念圖：

- `assets/images/design-reference/reference-concept-01-home-desktop.jpg`
- `assets/images/design-reference/reference-concept-02-home-mobile.jpg`
- `assets/images/design-reference/reference-concept-03-fish-list.jpg`
- `assets/images/design-reference/reference-concept-05-fish-detail.jpg`

V1 正式站基準：

- `qa/audit-v2-baseline/01-home-desktop.png`
- `qa/audit-v2-baseline/02-fish-list.png`
- `qa/audit-v2-baseline/03-breeding.png`
- `qa/audit-v2-baseline/04-contact.png`
- `qa/audit-v2-baseline/05-home-mobile.png`

V2 實作：

- `qa/screenshots/home-desktop-v2.png`
- `qa/screenshots/home-mobile-v2.png`
- `qa/screenshots/fish-list-v2.png`
- `qa/screenshots/fish-detail-v2.png`
- `qa/screenshots/breeding-v2.png`
- `qa/screenshots/contact-v2.png`

並排證據：

- `qa/screenshots/compare-home-desktop-v2.jpg`
- `qa/screenshots/compare-home-mobile-v2.jpg`
- `qa/screenshots/compare-fish-list-v2.jpg`
- `qa/screenshots/compare-fish-detail-v2.jpg`
- `qa/screenshots/compare-breeding-v2.jpg`
- `qa/screenshots/compare-contact-v2.jpg`

## 視覺檢查

- 字體：維持系統無襯線與繁體中文襯線展示字，不下載外部字型。桌機與手機的標題比例、行高與換行均保持可讀。
- 色彩：延續深海藍、墨綠藍、青綠與白色。Lighthouse 對比度修正後 Accessibility 為 100。
- Logo：魚頭朝右、寬扁頭部、高背鰭、胸鰭與尾部條紋在 42px 手機尺寸仍可辨認；Header 深海藍、Footer 白色。
- 圖像：所有公開魚圖皆為 AI 外觀示意並有可見標籤；魚身使用 contain，不裁切、不拉伸。
- 版面：桌機 Hero 保留概念圖的白色 Header、深色水族背景、左側品牌文案與右側魚影像；內頁採深色導言與淺色內容交錯。
- 手機：魚圖先於文案，390 × 844 與 360 × 800 首屏可見 Logo、品牌、定位、完整魚圖與 CTA；固定 Dock 不遮住 Footer。
- 元件：圓角、按鈕高度、Badge、Hover、Focus、陰影與行動間距統一。

## 比對與修正紀錄

1. P1：390 × 844 首屏主要 CTA 原先落在折線下方。
   - 修正：手機魚圖高度改為 300px，縮短段落間距，三個 CTA 改為單列。
   - 複驗：390 × 844 與 360 × 800 的主要 CTA 均在第一視窗內。

2. P2：魚種、繁殖與詢問頁的桌機 Hero 過高，核心內容進入首屏太少。
   - 修正：共用內頁 Hero 改為 360px 節奏並縮短 padding。
   - 複驗：魚種卡片、繁殖實拍缺件區與聯絡狀態進入首屏。

3. P1：詢問表單使用新標記後未匹配舊 `.field` 選擇器，欄位呈現瀏覽器預設樣式。
   - 修正：為 `.contact-form` 建立獨立欄位、select、textarea、全寬列與說明樣式。
   - 複驗：桌機欄位高 50px、背景與圓角符合品牌系統，手機維持單欄。

4. P1：Lighthouse 初次 Accessibility 95，輔助文字與青綠標籤對比不足。
   - 修正：加深 muted／teal、狀態卡改白色實底、深色媒體區使用 aqua-soft、CTA 說明改高對比白。
   - 複驗：Accessibility 100。

## 功能與可及性

- 手機選單、Escape 關閉、魚種篩選、搜尋、詢問內容產生與複製均可操作。
- 可見 Focus、原生標籤、aria-expanded、aria-pressed、alt、reduced motion 均保留。
- 22 個公開頁面無破圖、無 Console Error、無橫向溢位。
- 沒有可操作的 FAQ 元件；選單、篩選、表單與按鈕已完成鍵盤檢查。

## 已知內容限制

- 五張使用者手機實拍未在本機找到，因此繁殖頁使用清楚的缺件狀態，不以 AI 圖或空白色塊偽裝實拍。
- 官方聯絡設定全為空白，聯絡頁顯示「官方聯絡管道尚待設定」，只提供內容產生器。
- 概念圖包含未確認價格、庫存、聯絡方式、學名與 L 編號，V2 依規則不複製這些商業資訊。

## 最終結果

final result: passed
