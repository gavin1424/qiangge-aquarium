# 魚宅水族素材缺件報告

更新日期：2026-07-27

## 搜尋結果

已搜尋最近 14 天內建立或修改的 JPG、JPEG、PNG、WEBP，範圍包括：

- `C:\Users\wwwas\Desktop\魚宅水族網站素材`：資料夾不存在。
- `C:\Users\wwwas\Desktop`：未找到可確認為魚宅水族手機實拍的五張照片。
- `C:\Users\wwwas\Downloads`：未找到可確認的手機實拍原檔。
- `C:\Users\wwwas\Pictures`：未找到可確認的手機實拍原檔。
- `C:\Users\wwwas\OneDrive\Desktop`：資料夾不存在。
- 本次與前次附件：確認 8 張 AI 生成魚圖與 5 張網站概念圖。
- 另以 EXIF 相機資訊協助檢索，找到的近期相機檔案與本網站魚類素材無關。

未依檔名或影像外觀看似真實而判定來源。

## 目前已整合素材

- AI 生成魚圖：8 張，公開使用時皆顯示「AI 示意」標籤。
- 網站概念圖：5 張，只保留於 `assets/images/design-reference/` 作內部設計參考，不載入公開頁面。
- 使用者手機實拍：0 張。
- AI 圖放置於 `assets/images/illustrations/`。
- 未來確認的實拍原檔應複製到 `assets/images/photography/`，不得覆蓋原始檔。

## 尚缺少的五張手機實拍

請重新提供以下原始照片；在確認來源前，網站不會把任何現有魚圖標示為實拍：

1. 手持一尾紅色鰭、條紋異形魚，背景為紅色水盆。
2. 紅色水盆內有魚，以及一個裝著黃色魚卵的小碗。
3. 多尾異形魚聚集在白色六角繁殖管。
4. 淺色／白化異形魚在透明繁殖盒中的側面照片。
5. 同一尾淺色／白化異形魚在透明繁殖盒中的俯視照片。

建議放置路徑：

```text
assets/images/photography/breeding-parent-red-basin.jpg
assets/images/photography/breeding-eggs-yellow-bowl.jpg
assets/images/photography/breeding-hex-caves-group.jpg
assets/images/photography/light-fish-breeding-box-side.jpg
assets/images/photography/light-fish-breeding-box-top.jpg
```

收到後仍需逐張確認來源、建立 WebP/JPG 尺寸版本、補齊 `ASSET_MANIFEST.csv` 與來源清單，完成 QA 後才能公開標示「實拍紀錄」。

## 尚缺少的官方聯絡資訊

`assets/js/site-config.js` 目前所有欄位皆留白，因此網站只提供「詢問內容產生器」，不顯示未確認的聯絡資料。尚待補充：

- LINE 連結與 LINE ID
- Instagram 網址
- Facebook 網址
- Email
- 電話
- 地址
- 營業時間
- 地圖網址

空白欄位會完全隱藏，不會以概念圖中的範例資料代替。
