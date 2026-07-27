# 專案狀態

- 專案：強哥水族品牌網站 V2
- Repository：`gavin1424/qiangge-aquarium`
- 修改分支：`brand-v2`
- 備份標籤：`before-brand-v2-20260727-112204`
- 正式部署分支：`main`
- 正式網址：<https://gavin1424.github.io/qiangge-aquarium/>
- 更新日期：2026-07-27

## V2 完成範圍

- 建立異形魚／吸盤甲鯰輪廓 SVG 品牌系統，替換舊有圓形「強」字標誌。
- 將 8 張 AI 生成魚圖移至 `assets/images/illustrations/` 並全面顯示「AI 示意」。
- 本機未找到五張手機實拍，因此目前實拍數量為 0，繁殖頁清楚列出缺件。
- 建立圖片來源 JSON/CSV、統一圖片聲明與獨立圖片來源說明頁。
- 重寫首頁、魚種、近期魚況、繁殖紀錄、圖片相簿與詢問整理流程。
- 建立八個獨立魚種 SEO 詳情頁。
- 建立 Privacy、Terms、site.webmanifest、OG 分享圖及更新 sitemap。
- 建立共用模板與 `scripts/build-site.py`，目前產生 22 個公開 HTML。

## QA 狀態

- 22 個公開頁面、20 筆 sitemap URL 與 108 個本機頁面／資源 URL 均通過。
- Lighthouse：Performance 97、Accessibility 100、Best Practices 100、SEO 100。
- Console Error、破圖、404 資源與橫向溢位均為 0。
- 本機 QA 已通過；正式站結果以最終部署複驗為準。

## 待使用者補充

- 五張手機實拍原檔。
- 官方 LINE、Instagram、Facebook、Email、電話、地址、營業時間與地圖資料。
