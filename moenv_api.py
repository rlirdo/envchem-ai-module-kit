# -*- coding: utf-8 -*-
"""
環境部 API 常用代碼庫（moenv_api.py）
=====================================
給「環境化學 × 生成式 AI 模組」學生使用：在 Google Colab 一行載入、一行抓資料。

    !wget -q https://rlirdo.github.io/envchem-ai-module-kit/moenv_api.py
    import moenv_api as ma
    df = ma.fetch("aqx_p_432", API_KEY, filters="sitename,EQ,花蓮")

‧ API 金鑰請放在 Colab 左側「🔑 密鑰」(Secrets)，名稱 MOENV_API_KEY；不要寫進程式碼、不要上傳 GitHub。
‧ 資料來源：環境部環境資料開放平臺 https://data.moenv.gov.tw/ （政府資料開放授權條款－第 1 版）

NDHU 自資系 游豐兆 博士生製作｜指導教授 楊悠娟 副教授
"""
import io
import time
import urllib.parse

import pandas as pd
import requests

BASE = "https://data.moenv.gov.tw/api/v2/"

# 常用資料集（DataID → 說明）。DataID 可在平臺每個資料集頁面的「API」分頁看到。
DATASETS = {
    "aqx_p_432": "空氣品質指標(AQI)－現況，每小時更新，全臺各測站一筆",
    "aqx_p_488": "空氣品質指標(AQI)(歷史資料)－逐時，可用 filters 篩測站",
    "aqx_p_13":  "空品測站每日逐時監測值－一列一天一項目（monitorvalue00～23），含 O3、NO2、NOx、NMHC、溫濕度、雨量",
    "aqx_p_07":  "空氣品質監測站基本資料－測站地址、類型（一般站／交通站／工業站…）、經緯度",
}

# 無效值的常見寫法：儀器維修、校正或資料不足時會出現
INVALID = ["", " ", "-", "--", "—", "ND", "NA", "N/A", "x", "X", "#", "*", "-999", "-999.0", "-9999"]


def build_url(dataset_id, api_key, limit=1000, offset=0, fmt="JSON", filters=None, sort=None):
    """組出 API 網址。filters 例：'sitename,EQ,花蓮'；sort 例：'datacreationdate desc'。"""
    params = {"api_key": api_key, "limit": limit, "offset": offset, "format": fmt}
    if filters:
        params["filters"] = filters
    if sort:
        params["sort"] = sort
    return BASE + dataset_id + "?" + urllib.parse.urlencode(params, safe=",|")


def mask(url):
    """把網址裡的 api_key 遮起來，方便截圖或貼給 AI。"""
    import re
    return re.sub(r"(api_key=)[^&]+", r"\1********", url)


def get_json(url, timeout=60):
    """下載 JSON。先用 requests；若遇到政府網站憑證的
    『certificate verify failed: Missing Subject Key Identifier』（Python 3.13 起的嚴格檢查），
    改用「仍然驗證憑證、只關掉 X509 嚴格模式」的連線再試一次。"""
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.SSLError:
        import json, ssl, urllib.request
        ctx = ssl.create_default_context()
        ctx.verify_flags &= ~getattr(ssl, "VERIFY_X509_STRICT", 0)
        with urllib.request.urlopen(url, timeout=timeout, context=ctx) as resp:
            return json.loads(resp.read())


def fetch(dataset_id, api_key, limit=1000, offset=0, filters=None, sort=None, timeout=60):
    """抓一頁資料，回傳 pandas DataFrame（所有欄位先是文字）。"""
    url = build_url(dataset_id, api_key, limit, offset, "JSON", filters, sort)
    data = get_json(url, timeout)
    if isinstance(data, dict):            # 少數資料集會包一層 records
        data = data.get("records", [])
    return pd.DataFrame(data)


def fetch_all(dataset_id, api_key, filters=None, sort=None, max_rows=5000, page=1000, pause=0.5):
    """自動翻頁（offset）直到抓滿 max_rows 或沒有資料。"""
    frames = []
    for offset in range(0, max_rows, page):
        df = fetch(dataset_id, api_key, limit=page, offset=offset, filters=filters, sort=sort)
        if df.empty:
            break
        frames.append(df)
        if len(df) < page:
            break
        time.sleep(pause)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def clean_numeric(df, cols, invalid=INVALID):
    """把指定欄位的無效值換成 NaN，並轉成數字；回傳新表與各欄被清掉的筆數。"""
    out = df.copy()
    report = {}
    for c in cols:
        raw = out[c].astype(str).str.strip()
        bad = raw.isin(invalid)
        num = pd.to_numeric(raw.where(~bad), errors="coerce")
        report[c] = int(num.isna().sum())
        out[c] = num
    return out, report


def p13_to_long(df):
    """aqx_p_13（一列一天一項目、24 個 monitorvalueHH 欄）→ 長表：time, item, value。"""
    hours = [f"monitorvalue{h:02d}" for h in range(24)]
    long = df.melt(id_vars=["siteid", "sitename", "itemengname", "itemunit", "monitordate"],
                   value_vars=hours, var_name="hour", value_name="value")
    long["hour"] = long["hour"].str[-2:].astype(int)
    long["time"] = pd.to_datetime(long["monitordate"].str.strip()) + pd.to_timedelta(long["hour"], unit="h")
    long, _ = clean_numeric(long, ["value"])
    return long.sort_values(["itemengname", "time"]).reset_index(drop=True)


def use_chinese_font():
    """讓 matplotlib 圖表可以顯示中文（Colab 用；第一次約 10 秒）。"""
    import os, logging
    import matplotlib
    from matplotlib import font_manager
    logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)   # 關掉 findfont 警告
    path = ("/content/" if os.path.isdir("/content") else "") + "NotoSansTC.ttf"
    if not os.path.exists(path):
        url = "https://github.com/google/fonts/raw/main/ofl/notosanstc/NotoSansTC%5Bwght%5D.ttf"
        open(path, "wb").write(requests.get(url, timeout=60).content)
    font_manager.fontManager.addfont(path)
    matplotlib.rcParams["font.family"] = font_manager.FontProperties(fname=path).get_name()
    matplotlib.rcParams["axes.unicode_minus"] = False
