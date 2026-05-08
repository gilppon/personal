#!/usr/bin/env python
"""YouTube Account / Channels ??shared config for every YouTube tool.

This script doesn't fetch anything by itself. It's listed in the agent panel
so you can click ?숋툘 once and fill in your API key, channel, watched
channels, etc. ??and every other tool will read from here.

Running it just prints a sanity-check report so you can confirm the values
are loaded correctly (without leaking the full API key)."""
import os, json, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "youtube_account.json")

def load():
    with open(CONFIG_PATH, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def main():
    cfg = load()
    api = (cfg.get("YOUTUBE_API_KEY") or "").strip()
    masked = (api[:4] + "?? + api[-3:]) if len(api) >= 8 else ("(鍮?媛?" if not api else "(吏㏃쓬)")
    print("??? YouTube 怨꾩젙 / 梨꾨꼸 ?ㅼ젙 ???")
    print(f"  API ??           : {masked}")
    print(f"  ??梨꾨꼸 ?몃뱾       : {cfg.get('MY_CHANNEL_HANDLE') or '(?놁쓬)'}")
    print(f"  ??梨꾨꼸 ID        : {cfg.get('MY_CHANNEL_ID') or '(?놁쓬)'}")
    watched = cfg.get('WATCHED_CHANNELS') or []
    print(f"  媛먯떆 梨꾨꼸 ({len(watched)}媛? : {', '.join(watched) if watched else '(?놁쓬)'}")
    competitors = cfg.get('COMPETITOR_CHANNELS') or []
    print(f"  寃쎌웳 梨꾨꼸 ({len(competitors)}媛?: {', '.join(competitors) if competitors else '(?놁쓬)'}")
    tg_bot = (cfg.get('TELEGRAM_BOT_TOKEN') or '').strip()
    tg_chat = (cfg.get('TELEGRAM_CHAT_ID') or '').strip()
    if tg_bot and tg_chat:
        print(f"  ?붾젅洹몃옩          : ?곌껐??(chat {tg_chat})")
    else:
        print(f"  ?붾젅洹몃옩          : 誘몄꽕??(蹂닿퀬 ?뚮┝ 鍮꾪솢??")
    print(f"  Ollama URL        : {cfg.get('OLLAMA_URL') or 'http://127.0.0.1:11434'}")
    print(f"  遺꾩꽍 紐⑤뜽          : {cfg.get('MODEL') or '(?먮룞 ?좏깮)'}")
    if not api:
        print("\n?좑툘  API ?ㅺ? 鍮꾩뼱?덉뼱?? ?ㅻⅨ ?꾧뎄?ㅼ씠 ?숈옉?섏? ?딆뒿?덈떎.")
        print("   諛쒓툒: https://console.cloud.google.com/ ??YouTube Data API v3")
        sys.exit(1)
    print("\n??怨듭쑀 ?ㅼ젙 濡쒕뱶 OK. ?ㅻⅨ ?꾧뎄?ㅼ씠 ??媛믪쓣 ?먮룞?쇰줈 ?ъ슜?⑸땲??")

if __name__ == "__main__":
    main()
