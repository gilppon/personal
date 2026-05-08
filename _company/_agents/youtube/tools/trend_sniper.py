#!/usr/bin/env python
"""Trend Sniper ??pulls top YouTube videos for target keywords, asks a local
LLM (Ollama/LM Studio) to extract the algorithmic patterns, and writes a
planning report next to this script.

Shared keys (API key, OLLAMA_URL, MODEL) come from youtube_account.json so
you only set them once. Per-tool keys (TARGET_KEYWORDS) come from
trend_sniper.json. If a key exists in both, trend_sniper.json wins.

Requires:  pip install google-api-python-client requests
"""
import os, json, time, random, datetime, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "trend_sniper.json")
ACCOUNT_PATH = os.path.join(HERE, "youtube_account.json")
REPORT_PATH = os.path.join(HERE, "trend_sniper_report.md")

def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"???ㅼ젙 ?뚯씪???쎌쓣 ???놁뼱?? {CONFIG_PATH}\n{e}")
        sys.exit(1)

def load_account():
    try:
        if os.path.exists(ACCOUNT_PATH):
            with open(ACCOUNT_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}

def _shared(cfg, acct, key, default=""):
    """Per-tool config wins; falls back to shared account; finally default."""
    v = cfg.get(key)
    if v not in (None, "", []):
        return v
    v = acct.get(key)
    if v not in (None, "", []):
        return v
    return default

def main():
    cfg = load_config()
    acct = load_account()
    api_key = (_shared(cfg, acct, "YOUTUBE_API_KEY") or "").strip()
    if not api_key:
        print("?좑툘  YOUTUBE_API_KEY媛 鍮꾩뼱?덉뼱?? youtube_account.json ?먮뒗 trend_sniper.json???낅젰?섏꽭??")
        print("   諛쒓툒: https://console.cloud.google.com/ ??YouTube Data API v3 ?ъ슜 ?ㅼ젙 ???ъ슜???몄쬆 ?뺣낫 ??API ??)
        sys.exit(1)
    target_keywords = cfg.get("TARGET_KEYWORDS", [])
    if not target_keywords:
        print("?좑툘  TARGET_KEYWORDS媛 鍮꾩뼱?덉뼱?? 遺꾩꽍???ㅼ썙?쒕? 1媛??댁긽 異붽??섏꽭??")
        sys.exit(1)
    ollama_url = (_shared(cfg, acct, "OLLAMA_URL", "http://127.0.0.1:11434") or "http://127.0.0.1:11434").rstrip("/")
    model = _shared(cfg, acct, "MODEL", "") or ""
    pick = min(2, len(target_keywords))
    chosen = random.sample(target_keywords, pick)

    try:
        from googleapiclient.discovery import build
    except ImportError:
        print("??google-api-python-client媛 ?ㅼ튂?섏? ?딆븯?댁슂.")
        print("   ?ㅼ튂: pip install google-api-python-client requests")
        sys.exit(1)
    try:
        import requests
    except ImportError:
        print("??requests媛 ?ㅼ튂?섏? ?딆븯?댁슂. pip install requests")
        sys.exit(1)

    print(f"\n?렞 [?몃젋???ㅻ굹?댄띁] ?ㅼ썙??{chosen} ?ㅼ틪 ?쒖옉...")
    youtube = build('youtube', 'v3', developerKey=api_key)
    last_month = (datetime.datetime.utcnow() - datetime.timedelta(days=30)).isoformat("T") + "Z"
    sniper_data = []
    for q in chosen:
        print(f"?뱻 [{q}] 寃??以?..")
        try:
            req = youtube.search().list(
                part="snippet", q=q, maxResults=5, order="viewCount",
                publishedAfter=last_month, type="video"
            )
            res = req.execute()
            for item in res.get('items', []):
                title = item['snippet']['title']
                channel = item['snippet']['channelTitle']
                sniper_data.append(f"[{q}] 梨꾨꼸: {channel} | ?쒕ぉ: {title}")
        except Exception as e:
            print(f"??寃???ㅻ쪟 ({q}): {e}")

    if not sniper_data:
        print("???섏쭛???곗씠???놁쓬. API ???쒕룄/?ㅽ듃?뚰겕 ?뺤씤.")
        sys.exit(1)

    data_text = "\n".join(sniper_data)
    prompt = f"""?뱀떊? ?좏뒠釉??뚭퀬由ъ쬁 留덉뒪?곕쭏?몃뱶?낅땲?? ?꾨옒??理쒓렐 30???≪긽 ?곸긽?낅땲??

[?ㅼ썙?? {', '.join(chosen)}
[?곗씠??
{data_text}

遺꾩꽍?댁꽌 留덊겕?ㅼ슫 蹂닿퀬?쒕? ?묒꽦?섏꽭?? 諛섎뱶??3?뱀뀡:
1. ?뙇 ?몃젋???댄궧 遺꾩꽍 ???대뼡 ?⑦꽩??議고쉶?섎? ?뚭퀬 ?덈뒗吏
2. ?렞 鍮덉쭛 ?멸린 ?꾨왂 ??李⑤퀎??媛?ν븳 ?덉깉 二쇱젣
3. ?렗 ?뚭눼???곸긽 湲고쉷?????몃꽕??移댄뵾, ?쒕ぉ 3媛? ?꾪궧 ?ㅽ봽??泥?5珥?
"""

    # v2.89.70 ??LM Studio (OpenAI ?명솚 API) + Ollama ????吏?? URL/?ы듃濡??먮룞 媛먯?.
    is_lm_studio = ('1234' in ollama_url) or ('/v1' in ollama_url)
    print(f"?쭬 [LLM 遺꾩꽍 以?.. ?붿쭊: {'LM Studio' if is_lm_studio else 'Ollama'}]")

    # 紐⑤뜽 ?먮룞 ?좏깮 ???붿쭊蹂꾨줈 ?ㅻⅨ endpoint
    if not model:
        try:
            if is_lm_studio:
                # LM Studio: GET /v1/models (OpenAI ?명솚)
                base = ollama_url.rstrip('/')
                if not base.endswith('/v1'):
                    base = base + '/v1'
                r = requests.get(f"{base}/models", timeout=5)
                r.raise_for_status()
                models = [m["id"] for m in r.json().get("data", [])]
            else:
                # Ollama: GET /api/tags
                r = requests.get(f"{ollama_url}/api/tags", timeout=5)
                r.raise_for_status()
                models = [m["name"] for m in r.json().get("models", [])]
            if not models:
                print(f"??濡쒖뺄 LLM???ㅼ튂??紐⑤뜽???놁뼱?? {'LM Studio' if is_lm_studio else 'Ollama'} ?먯꽌 紐⑤뜽 濡쒕뱶/??섏꽭??")
                sys.exit(1)
            model = models[0]
            print(f"   ?먮룞 ?좏깮 紐⑤뜽: {model}")
        except Exception as e:
            print(f"??濡쒖뺄 LLM ?곌껐 ?ㅽ뙣 ({ollama_url}): {e}")
            print(f"   ?붿쭊 ?ㅽ뻾 ?뺤씤: {'LM Studio (?ы듃 1234)' if is_lm_studio else 'Ollama (?ы듃 11434)'}")
            sys.exit(1)

    # 異붾줎 ?몄텧 ???붿쭊蹂??ㅻⅨ endpoint쨌payload ?뺤떇
    try:
        if is_lm_studio:
            base = ollama_url.rstrip('/')
            if not base.endswith('/v1'):
                base = base + '/v1'
            r = requests.post(
                f"{base}/chat/completions",
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                    "max_tokens": 2048,
                },
                timeout=180,
            )
            r.raise_for_status()
            report = r.json().get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        else:
            r = requests.post(
                f"{ollama_url}/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=180,
            )
            r.raise_for_status()
            report = r.json().get("response", "").strip()
    except Exception as e:
        print(f"??LLM ?몄텧 ?ㅽ뙣: {e}")
        sys.exit(1)

    print("\n" + "="*60)
    print(report)
    print("="*60)

    with open(REPORT_PATH, "a", encoding="utf-8") as f:
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"\n\n# ?렞 ?몃젋???ㅻ굹?댄븨 蹂닿퀬????{now}\n")
        f.write(f"## ?뱻 ?ㅼ썙?? {', '.join(chosen)}\n\n")
        f.write(report)
        f.write("\n\n---\n")
    print(f"\n??蹂닿퀬????? {REPORT_PATH}")

if __name__ == "__main__":
    main()
