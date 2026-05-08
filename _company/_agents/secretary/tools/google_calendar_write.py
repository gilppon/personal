#!/usr/bin/env python
"""Google Calendar ?먮룞 ?쇱젙 ?깅줉 ??secretary_calendar_write_v1.

???ㅽ겕由쏀듃??OAuth? ?ㅼ젣 ?대깽???앹꽦??吏곸젒 ?섏? ?딆뒿?덈떎 ??VS Code
?몄뒪??extension.ts)?먯꽌 吏곸젒 泥섎━?댁슂. ???꾧뎄????븷?:
  1) ?ㅼ젙 ?곹깭瑜??뺤씤?댁꽌 ?ъ슜?먯뿉寃??뚮젮二쇨린 (???대┃ ??
  2) ?숋툘 ?쇱뿉??CALENDAR_ID / DEFAULT_DURATION_MINUTES 媛숈? 蹂댁“ ?ㅼ젙 ?몄텧

?곌껐 ?먯껜??紐낅졊 ?붾젅?몄뿉??
  Cmd+Shift+P ??'Connect AI: Google Calendar ?먮룞 ?쇱젙 ?곌껐 ?뱟'
"""
import os, json, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "google_calendar_write.json")

def main():
    if not os.path.exists(CONFIG):
        print("?좑툘 ?꾩쭅 ?ㅼ젙???놁뼱??")
        print("   紐낅졊 ?붾젅??Cmd+Shift+P) ??'Connect AI: Google Calendar ?먮룞 ?쇱젙 ?곌껐' ?ㅽ뻾")
        sys.exit(1)
    try:
        with open(CONFIG, "r", encoding="utf-8-sig") as f:
            cfg = json.load(f)
    except Exception as e:
        print(f"???ㅼ젙 ?뚯씪 ?뚯떛 ?ㅽ뙣: {e}")
        sys.exit(1)
    cid = (cfg.get("CLIENT_ID") or "").strip()
    cs  = (cfg.get("CLIENT_SECRET") or "").strip()
    rt  = (cfg.get("REFRESH_TOKEN") or "").strip()
    cal = (cfg.get("CALENDAR_ID") or "primary").strip()
    dur = int(cfg.get("DEFAULT_DURATION_MINUTES") or 60)
    who = (cfg.get("_CONNECTED_AS") or "").strip()
    when = (cfg.get("_CONNECTED_AT") or "").strip()
    print("??? Google Calendar ?먮룞 ?쇱젙 ?깅줉 ?곹깭 ???")
    print(f"  Client ID         : {'?ㅼ젙??(' + cid[:8] + '??' if cid else '(?놁쓬)'}")
    print(f"  Client Secret     : {'?ㅼ젙?? if cs else '(?놁쓬)'}")
    print(f"  Refresh Token     : {'?좏슚 ?? if rt else '(?놁쓬)'}")
    print(f"  Calendar ID       : {cal}")
    print(f"  湲곕낯 ?쇱젙 湲몄씠     : {dur}遺?)
    if who:
        print(f"  ?곌껐 怨꾩젙          : {who}")
    if when:
        print(f"  ?곌껐 ?쒓컖          : {when[:19]}")
    if not (cid and cs and rt):
        print()
        print("?좑툘 ?뗭뾽???꾨즺?섏? ?딆븯?댁슂.")
        print("   紐낅졊 ?붾젅??Cmd+Shift+P) ??'Connect AI: Google Calendar ?먮룞 ?쇱젙 ?곌껐'")
        sys.exit(1)
    print()
    print("???곌껐 ?뺤긽. 留덇컧??due) ?덈뒗 異붿쟻 ?묒뾽???깅줉?섎㈃ ?먮룞?쇰줈 罹섎┛?붿뿉 ?쇱젙???앹꽦?⑸땲??")

if __name__ == "__main__":
    main()
