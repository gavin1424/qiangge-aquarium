# 強哥水族

異形專賣・專業繁殖・飼養交流

這是一個為 GitHub Pages 專案頁設計的純靜態多頁網站。網站不需要資料庫、後端伺服器、WordPress、付費 API 或第三方追蹤服務。

## 網站頁面

- 首頁
- 熱門魚種總覽
- 魚種照護詳情
- 新魚到港
- 飼養教學與文章
- 繁殖紀錄
- 圖片相簿
- 關於我們與養殖理念
- 聯絡與預約賞魚

## 本機預覽

請在專案根目錄啟動任一靜態 HTTP 伺服器，例如：

```powershell
python -m http.server 8000
```

接著瀏覽 `http://localhost:8000/`。直接雙擊 HTML 也可閱讀主要內容，但 JSON 魚種資料需透過 HTTP 預覽才能載入。

## 部署

正式 Repository：

```text
gavin1424/qiangge-aquarium
```

GitHub Pages 目標網址：

```text
https://gavin1424.github.io/qiangge-aquarium/
```

所有內部路徑使用相對位置，可安全部署於 `/qiangge-aquarium/` 子目錄。

## 素材狀態

目前取得五張網站概念圖與八張真實魚類照片。概念圖僅用作設計參考，沒有在公開頁面中顯示；真實魚照保留原始檔，並建立 WebP 響應式版本與 JPG 後備。網站不使用網路隨機圖片、AI 魚圖或從概念圖裁切的魚圖。仍待補的素材詳見 `MISSING_ASSETS_REPORT_ZH.md`。
