#!/usr/bin/env python
"""Telegram ?곌껐 ??secretary_telegram_v2.

Secretary ?먯씠?꾪듃???붾젅洹몃옩 ?곌껐 ?꾧뎄. ?좏겙쨌chat_id瑜?Skills???숋툘 ?쇱뿉
?낅젰?섎㈃ `telegram_setup.json`????λ릺怨? ???ㅽ겕由쏀듃媛 硫붿떆吏 1諛?蹂대궡???곌껐???뚯뒪?명빀?덈떎. ?뚯궗??紐⑤뱺 ?먯씠?꾪듃(YouTube ?ы븿)媛 ???ㅼ젙??怨듭쑀?⑸땲??"""
import os, json, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "telegram_setup.json")

def main():
    if not os.path.exists(CONFIG):
        print("??telegram_setup.json???놁뼱?? 癒쇱? ?숋툘 ?대┃?댁꽌 ?좏겙???낅젰?댁＜?몄슂.")
        sys.exit(1)
    try:
        with open(CONFIG, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception as e:
        print(f"???ㅼ젙 ?뚯씪 ?뚯떛 ?ㅽ뙣: {e}")
        sys.exit(1)
    token = (cfg.get("TELEGRAM_BOT_TOKEN") or "").strip()
    chat  = (cfg.get("TELEGRAM_CHAT_ID") or "").strip()
    if not token or not chat:
        print("??TELEGRAM_BOT_TOKEN ?먮뒗 TELEGRAM_CHAT_ID媛 鍮꾩뼱?덉뼱??")
        print("   遊?留뚮뱾湲? Telegram ??@BotFather ??/newbot ???좏겙 諛쏄린")
        print("   chat_id  : 遊뉗뿉 硫붿떆吏 1踰???https://api.telegram.org/bot<TOKEN>/getUpdates ?먯꽌 chat.id")
        sys.exit(1)
    try:
        import requests
    except ImportError:
        print("??pip install requests")
        sys.exit(1)
    body = f"??鍮꾩꽌(Secretary) ?붾젅洹몃옩 ?곌껐 ?뺤긽 ??{time.strftime('%Y-%m-%d %H:%M:%S')}\n\n??硫붿떆吏媛 蹂댁씠硫?紐⑤뱺 ?먯씠?꾪듃媛 ??梨꾨꼸濡?蹂닿퀬瑜?蹂대궪 ???덉뼱??"
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat, "text": body, "parse_mode": "Markdown"},
            timeout=15,
        )
        r.raise_for_status()
        print(f"???꾩넚 OK ???붾젅洹몃옩?먯꽌 ?뺤씤?섏꽭?? ({len(body)}??")
    except Exception as e:
        print(f"???꾩넚 ?ㅽ뙣: {e}")
        if "Bad Request" in str(e):
            print("   chat_id媛 ?뺥솗?쒖?, 遊뉕낵 ??踰덉씠?쇰룄 ??붾? ?쒖옉?덈뒗吏 ?뺤씤?섏꽭??")
        sys.exit(1)

if __name__ == "__main__":
    main()
