# 環境化學 × 生成式 AI 模組教學懶人包（envchem-ai-module-kit）

**提示詞驅動環境數據科學：運用環境部 API 與 AI 協作之花蓮在地環境化學 PBL 探究**

國立東華大學 自然資源與環境學系｜環境化學（NRES20050）｜115-1「生成式 AI 融入專業課程」計畫
可複製、可轉移的開源教學包：Prompt 指南、Colab 範本、環境部 API 常用代碼庫、學生操作手冊、課後學習單、離線備援資料。

👉 網站（學生版入口）：https://rlirdo.github.io/envchem-ai-module-kit/

| 模組 | 日期 | 主題 | Colab 範本 |
|---|---|---|---|
| 活動一 | 2026/11/30（第 13 週） | 公開資料、API 與 Prompt-driven Notebook：真實抓取花蓮站空品資料 | [M1](https://colab.research.google.com/github/rlirdo/envchem-ai-module-kit/blob/main/notebooks/M1_moenv_api_fetch.ipynb) |
| 活動二 | 2026/12/07（第 14 週） | AI 輔助 EDA 與視覺化：清洗、結構化、折線圖與散佈圖 | [M2](https://colab.research.google.com/github/rlirdo/envchem-ai-module-kit/blob/main/notebooks/M2_clean_visualize.ipynb) |
| 活動三 | 2026/12/21（第 16 週） | 環境化學解讀與 AI 查證：揪出 AI 幻覺 | [M3](https://colab.research.google.com/github/rlirdo/envchem-ai-module-kit/blob/main/notebooks/M3_interpret_verify.ipynb) |

## 檔案
- `moenv_api.py`：環境部 API 常用代碼庫（組網址、抓資料、自動翻頁、清洗無效值、寬表轉長表、中文字型）
- `notebooks/`：三份 Colab 範本（先寫 Prompt，卡關才展開參考解答）
- `data/`：花蓮站真實資料離線備援包（環境部環境資料開放平臺，政府資料開放授權條款－第 1 版）
- `img/`：學生操作手冊用的實際網站截圖（已標註步驟）
- `worksheets/`：三份課後學習單

## 安全提醒
API 金鑰等同帳號密碼：請放在 Colab「🔑 密鑰」，**不要**寫進程式碼、截圖或上傳到任何公開空間。本 repo 不含任何金鑰。

## 授權
教材文字與範本：CC BY-NC-SA 4.0（請註明出處）；資料：環境部環境資料開放平臺，依政府資料開放授權條款－第 1 版。

---
NDHU 自資系 游豐兆 博士生製作｜指導教授 楊悠娟 副教授
