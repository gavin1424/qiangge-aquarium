# 魚宅水族

魚宅水族商用級多頁靜態網站，品牌定位為「異形魚繁殖・飼養紀錄・水族交流」。

正式網站：<https://gavin1424.github.io/qiangge-aquarium/>

Repository：<https://github.com/gavin1424/qiangge-aquarium>

## 技術架構

- HTML5、CSS3、Vanilla JavaScript
- JSON 內容資料與 SVG 品牌圖示
- Python 標準函式庫建置腳本
- GitHub Pages 專案頁部署
- 無資料庫、無後端、無付費 API、無外部追蹤程式

最終部署成品皆為純靜態檔案；GitHub Pages 不需執行 Python。

## 本機建置與預覽

```powershell
python scripts\build-site.py
python scripts\qa.py
python -m http.server 4173
```

再以瀏覽器開啟 `http://localhost:4173/`。

`scripts/build-site.py` 會同步共用 Header、Footer、手機 Dock，並依 `data/fish.json` 產生八個獨立魚種詳情頁。所有路徑均使用相對路徑，支援 `/qiangge-aquarium/` 子目錄部署。

## 圖片來源規範

- `assets/images/illustrations/`：8 張 AI 生成外觀示意圖，公開頁面均須顯示「AI 示意」。
- `assets/images/photography/`：僅能放入經確認的使用者手機實拍；目前為 0 張。
- `assets/images/design-reference/`：5 張網站概念圖，只供內部版面參考，不得載入公開頁面。
- `assets/data/asset-provenance.json` 與 `ASSET_PROVENANCE.csv`：圖片來源與允許用途的單一紀錄。
- `ASSET_MANIFEST.csv`：檔名、用途、尺寸、格式與使用狀態清單。

目前缺少的手機實拍與官方聯絡資料詳見 `MISSING_ASSETS_REPORT_ZH.md`。

## 維護規則

- 只允許操作 `gavin1424/qiangge-aquarium`。
- 不得加入未確認的魚種、L 編號、品系、價格、庫存、聯絡資訊或門市資訊。
- AI 圖不得宣稱為實際個體、現貨或繁殖成果。
- 每次修改後需重新執行建置與 QA。
