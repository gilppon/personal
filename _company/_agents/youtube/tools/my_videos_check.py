#!/usr/bin/env python
"""Professional YouTube Channel Analysis ??pro_v4.

梨꾨꼸 硫뷀? 쨌 ?곸긽蹂??곸꽭 (議고쉶?샕룹쥕?꾩슂?㉱룸뙎湲?㉱룰만?는룹슂?? 쨌 ?곸쐞/?섏쐞 ?곸긽???⑦꽩 쨌
?멸린 ?볤? ?섑뵆 쨌 諛쒗뻾 ?붿씪 遺꾩꽍 쨌 ?쒕ぉ ?ㅼ썙??쨌 ?곗꽑?쒖쐞 ?≪뀡 異붿쿇. 紐⑤뱺 遺꾩꽍?
?ㅼ젣 YouTube Data API ?몄텧 寃곌낵 湲곕컲.

Reads YOUTUBE_API_KEY + MY_CHANNEL_HANDLE/ID from youtube_account.json.
Reads LOOKBACK_DAYS / TOP_N / COMMENT_SAMPLES from my_videos_check.json."""
import os, json, sys, time, datetime, re, statistics, warnings, html as html_lib
from collections import Counter
# v2.89.49 ??DeprecationWarning(utcnow ?? ?몄씠利??쒓굅. ?ъ슜??梨꾪똿李?異쒕젰???쇰㈃ 紐살깮源.
warnings.filterwarnings("ignore", category=DeprecationWarning)

HERE = os.path.dirname(os.path.abspath(__file__))
ACCOUNT = os.path.join(HERE, "youtube_account.json")
CONFIG  = os.path.join(HERE, "my_videos_check.json")
REPORT  = os.path.join(HERE, "my_videos_check_report.md")

def _load(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def _resolve_channel_id(youtube, handle, channel_id):
    if channel_id:
        return channel_id
    if not handle:
        return None
    h = handle.lstrip("@")
    try:
        r = youtube.search().list(part="snippet", q=h, type="channel", maxResults=1).execute()
        items = r.get("items", [])
        if items:
            return items[0]["snippet"]["channelId"]
    except Exception as e:
        print(f"?좑툘  梨꾨꼸 ID 議고쉶 ?ㅽ뙣: {e}")
    return None

def _resolve_telegram(account):
    """telegram_v3 ??Secretary's tools/telegram_setup.json is the canonical
    UI-managed home (input via Skills ?숋툘). Fallback chain:
      1) youtube_account.json (this tool's local override, back-compat)
      2) _agents/secretary/tools/telegram_setup.json (UI-managed, canonical)
      3) _agents/secretary/config.md (legacy markdown, back-compat)
    """
    import re, json as _json
    token = (account.get("TELEGRAM_BOT_TOKEN") or "").strip()
    chat  = (account.get("TELEGRAM_CHAT_ID") or "").strip()
    if token and chat:
        return token, chat
    brain_root = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    # 2) Secretary's tool JSON
    sec_json = os.path.join(brain_root, "_agents", "secretary", "tools", "telegram_setup.json")
    if (not token or not chat) and os.path.exists(sec_json):
        try:
            with open(sec_json, "r", encoding="utf-8") as f:
                cfg = _json.load(f)
            if not token: token = (cfg.get("TELEGRAM_BOT_TOKEN") or "").strip()
            if not chat:  chat  = (cfg.get("TELEGRAM_CHAT_ID") or "").strip()
        except Exception:
            pass
    # 3) Legacy config.md
    sec_cfg = os.path.join(brain_root, "_agents", "secretary", "config.md")
    if (not token or not chat) and os.path.exists(sec_cfg):
        try:
            with open(sec_cfg, "r", encoding="utf-8") as f:
                txt = f.read()
            if not token:
                m = re.search(r"TELEGRAM_BOT_TOKEN\s*[:竊?]\s*([A-Za-z0-9:_\-]+)", txt)
                if m: token = m.group(1).strip()
            if not chat:
                m = re.search(r"TELEGRAM_CHAT_ID\s*[:竊?]\s*(-?\d+)", txt)
                if m: chat = m.group(1).strip()
        except Exception:
            pass
    return token, chat

def _push_telegram(account, text):
    """v2.89.49 ??留덊겕?ㅼ슫 紐⑤뱶??*,[,(,),# 媛숈? ?뱀닔臾몄옄 留롮? 蹂닿퀬?쒖뿉???먯＜ 400 嫄곕?.
    ?댁쟾??洹몃옒??'sent' print?댁꽌 ?ъ슜?먰븳??媛吏??깃났 蹂닿퀬. ?댁젣 plain text 紐⑤뱶濡?    ?덉쟾?섍쾶 蹂대궡怨?HTTP status 泥댄겕?댁꽌 吏꾩쭨 ?깃났/?ㅽ뙣 ?뺥솗???뚮젮以?"""
    token, chat = _resolve_telegram(account)
    if not token or not chat:
        print("?좑툘  ?붾젅洹몃옩 ?좏겙/chat_id 誘몄꽕?????꾩넚 ????, file=sys.stderr)
        return
    try:
        import requests
        # plain text (parse_mode ?놁쓬) ???대뼡 ?뱀닔臾몄옄???듦낵
        r = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat, "text": text[:4000]},
            timeout=10,
        )
        if r.status_code == 200:
            print("?벂 ?붾젅洹몃옩 ?꾩넚 ?깃났", file=sys.stderr)
        else:
            try:
                err = r.json().get("description", r.text[:200])
            except Exception:
                err = r.text[:200]
            print(f"?좑툘  ?붾젅洹몃옩 ?꾩넚 ?ㅽ뙣 (HTTP {r.status_code}): {err}", file=sys.stderr)
    except Exception as e:
        print(f"?좑툘  ?붾젅洹몃옩 ?꾩넚 ?먮윭: {e}", file=sys.stderr)

def _fmt_num(n):
    if n >= 1_000_000: return f"{n/1_000_000:.1f}M"
    if n >= 1_000: return f"{n/1_000:.1f}K"
    return f"{n:,}"

def _parse_duration(iso):
    """ISO 8601 duration (PT5M30S) ??seconds"""
    m = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso or '')
    if not m: return 0
    h, mn, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mn * 60 + s

def _fmt_duration(secs):
    if secs >= 3600: return f"{secs//3600}?쒓컙 {(secs%3600)//60}遺?
    if secs >= 60: return f"{secs//60}遺?{secs%60}珥?
    return f"{secs}珥?

def _korean_weekday(dt):
    return ["??,"??,"??,"紐?,"湲?,"??,"??][dt.weekday()]

def main():
    if not os.path.exists(ACCOUNT):
        print("??youtube_account.json???놁뼱?? 吏곸썝 ?먯씠?꾪듃 蹂닿린 ??YouTube ???꾧뎄 ?숋툘?먯꽌 API ?ㅼ? 梨꾨꼸 ID瑜??낅젰?섏꽭??")
        sys.exit(1)
    acct = _load(ACCOUNT)
    cfg  = _load(CONFIG) if os.path.exists(CONFIG) else {}
    api_key = (acct.get("YOUTUBE_API_KEY") or "").strip()
    handle  = (acct.get("MY_CHANNEL_HANDLE") or "").strip()
    chan_id = (acct.get("MY_CHANNEL_ID") or "").strip()
    if not api_key:
        print("??YOUTUBE_API_KEY 誘몄꽕?? youtube_account.json??梨꾩썙二쇱꽭??")
        sys.exit(1)
    if not (handle or chan_id):
        print("??MY_CHANNEL_HANDLE ?먮뒗 MY_CHANNEL_ID ?꾩슂.")
        sys.exit(1)
    lookback = int(cfg.get("LOOKBACK_DAYS", 30))
    top_n    = int(cfg.get("TOP_N", 15))
    comment_samples = int(cfg.get("COMMENT_SAMPLES", 5))

    try:
        from googleapiclient.discovery import build
    except ImportError:
        print("??google-api-python-client 誘몄꽕移? pip install google-api-python-client requests")
        sys.exit(1)
    youtube = build("youtube", "v3", developerKey=api_key)

    cid = _resolve_channel_id(youtube, handle, chan_id)
    if not cid:
        print("??梨꾨꼸 ID瑜?李얠? 紐삵뻽?댁슂. youtube_account.json???몃뱾/ID ?뺤씤.")
        sys.exit(1)

    # === 1. 梨꾨꼸 硫뷀? ===
    print(f"?뵇 梨꾨꼸 ?뺣낫 媛?몄삤??以?..", file=sys.stderr)
    cr = youtube.channels().list(part="snippet,statistics,contentDetails,brandingSettings", id=cid).execute()
    cit = cr.get("items", [])
    if not cit:
        print(f"??梨꾨꼸 ?곗씠???놁쓬 (ID: {cid})")
        sys.exit(1)
    ch = cit[0]
    snip = ch.get("snippet", {})
    cstats = ch.get("statistics", {})
    # v2.89.55 ??YouTube API媛 媛??&amp; / &#39; 媛숈? HTML entity濡??몄퐫?⑸맂 ?쒕ぉ 諛섑솚.
    # ?닿구 洹몃?濡?異쒕젰?섎㈃ 梨꾪똿李쎌뿉??"&#39;" 媛 literal濡?蹂댁엫. 誘몃━ ?붿퐫??
    ch_title = html_lib.unescape(snip.get("title", "") or "")
    custom_url = snip.get("customUrl", "")
    published = (snip.get("publishedAt", "") or "")[:10]
    country = snip.get("country", "")
    sub_count = int(cstats.get("subscriberCount", 0))
    subs_hidden = cstats.get("hiddenSubscriberCount", False)
    view_count_total = int(cstats.get("viewCount", 0))
    video_count_total = int(cstats.get("videoCount", 0))
    if published:
        try:
            age_days = (datetime.date.today() - datetime.date.fromisoformat(published)).days
        except Exception:
            age_days = 0
    else:
        age_days = 0
    age_years = age_days / 365.25 if age_days > 0 else 0
    avg_views_per_video_alltime = view_count_total // video_count_total if video_count_total else 0

    # === 2. 理쒓렐 ?곸긽 紐⑸줉 ===
    print(f"?뵇 理쒓렐 {lookback}???곸긽 媛?몄삤??以?..", file=sys.stderr)
    after = (datetime.datetime.utcnow() - datetime.timedelta(days=lookback)).isoformat("T") + "Z"
    sr = youtube.search().list(part="snippet", channelId=cid, maxResults=top_n,
                                order="date", publishedAfter=after, type="video").execute()
    vids = [(it["id"]["videoId"], it["snippet"]["title"], it["snippet"]["publishedAt"])
            for it in sr.get("items", [])]
    if not vids:
        # Fallback to most recent regardless of lookback window
        sr = youtube.search().list(part="snippet", channelId=cid, maxResults=top_n,
                                    order="date", type="video").execute()
        vids = [(it["id"]["videoId"], it["snippet"]["title"], it["snippet"]["publishedAt"])
                for it in sr.get("items", [])]
    if not vids:
        # v2.89.55 ??鍮??곸긽 ??stderr濡? stdout??鍮꾩뼱 ?덉뼱??TS shortcut???ㅽ뙣濡??뺥솗??泥섎━.
        print(f"?좑툘  ?낅줈?쒕맂 ?곸긽???놁뼱??", file=sys.stderr)
        sys.exit(0)

    # === 3. ?곸긽 ?곸꽭 ?듦퀎 ===
    print(f"?뵇 ?곸긽 {len(vids)}媛??곸꽭 ?듦퀎 + 湲몄씠쨌?쒓렇 媛?몄삤??以?..", file=sys.stderr)
    vstats = youtube.videos().list(
        part="statistics,contentDetails,snippet",
        id=",".join(v[0] for v in vids)
    ).execute()
    sm = {it["id"]: it for it in vstats.get("items", [])}
    rows = []
    for vid, vtitle, pub in vids:
        item = sm.get(vid, {})
        s = item.get("statistics", {})
        cd = item.get("contentDetails", {})
        sn = item.get("snippet", {})
        views = int(s.get("viewCount", 0))
        likes = int(s.get("likeCount", 0))
        comments = int(s.get("commentCount", 0))
        dur_sec = _parse_duration(cd.get("duration", "PT0S"))
        like_rate = (likes / views * 100) if views > 0 else 0
        comment_rate = (comments / views * 100) if views > 0 else 0
        try:
            pub_dt = datetime.datetime.fromisoformat(pub.replace("Z", "+00:00"))
            weekday = _korean_weekday(pub_dt)
            hour = pub_dt.hour
        except Exception:
            weekday, hour = "-", 0
        rows.append({
            # v2.89.55 ??title HTML entity ?붿퐫??(&#39; ??', &amp; ??& ??
            "id": vid, "title": html_lib.unescape(vtitle or ""), "pub": pub[:10],
            "weekday": weekday, "hour": hour,
            "views": views, "likes": likes, "comments": comments,
            "duration_sec": dur_sec,
            "like_rate": like_rate, "comment_rate": comment_rate,
            "tags": sn.get("tags", []) or [],
            "is_short": dur_sec <= 60,
        })

    # === 4. 吏묎퀎 ===
    views_list = [r["views"] for r in rows]
    median_views = int(statistics.median(views_list)) if views_list else 0
    avg_views = int(statistics.mean(views_list)) if views_list else 0
    avg_likes = int(statistics.mean([r["likes"] for r in rows])) if rows else 0
    avg_comments = int(statistics.mean([r["comments"] for r in rows])) if rows else 0
    avg_duration = int(statistics.mean([r["duration_sec"] for r in rows])) if rows else 0
    avg_like_rate = statistics.mean([r["like_rate"] for r in rows]) if rows else 0
    avg_comment_rate = statistics.mean([r["comment_rate"] for r in rows]) if rows else 0
    title_lengths = [len(r["title"]) for r in rows]
    avg_title_len = int(statistics.mean(title_lengths)) if title_lengths else 0
    shorts_count = sum(1 for r in rows if r["is_short"])

    rows_sorted = sorted(rows, key=lambda r: r["views"], reverse=True)
    top_videos = rows_sorted[:3]
    bottom_videos = rows_sorted[-3:][::-1] if len(rows_sorted) >= 4 else []

    # ?붿씪쨌?쒓컙? ?⑦꽩
    weekday_views = {}
    for r in rows:
        weekday_views.setdefault(r["weekday"], []).append(r["views"])
    weekday_avg = {wd: int(statistics.mean(vs)) for wd, vs in weekday_views.items()}

    # ?곸쐞 ?곸긽 ?쒕ぉ ?ㅼ썙??    top_title_words = Counter()
    stop_kr = {'洹몃━怨?,'洹쇰뜲','?덈Т','吏꾩쭨','?뺣쭚','?닿?','吏湲?,'?닿굅','???,'?쒓?','?곕━'}
    stop_en = {'this','that','and','the','for','with','have','will','your','from','about'}
    for r in top_videos:
        words = re.findall(r'[媛-??+|[a-zA-Z]+', r["title"])
        top_title_words.update(w for w in words if len(w) >= 2 and w.lower() not in stop_en and w not in stop_kr)
    top_keywords = [w for w, _ in top_title_words.most_common(8)]

    # === 5. ?멸린 ?볤? ?섑뵆 (?곸쐞 3媛??곸긽) ===
    print(f"?뮠 ?곸쐞 ?곸긽???멸린 ?볤? 媛?몄삤??以?..", file=sys.stderr)
    comments_by_video = {}
    for r in top_videos[:3]:
        try:
            cr_resp = youtube.commentThreads().list(
                part="snippet", videoId=r["id"], maxResults=comment_samples, order="relevance"
            ).execute()
            comments_by_video[r["id"]] = [
                {
                    # v2.89.55 ??author/text??HTML entity ?붿퐫??                    "author": html_lib.unescape(c["snippet"]["topLevelComment"]["snippet"].get("authorDisplayName", "") or ""),
                    "text": html_lib.unescape(c["snippet"]["topLevelComment"]["snippet"].get("textOriginal", "") or "")[:200],
                    "likes": int(c["snippet"]["topLevelComment"]["snippet"].get("likeCount", 0)),
                }
                for c in cr_resp.get("items", [])
            ]
        except Exception:
            comments_by_video[r["id"]] = []  # ?볤? 鍮꾪솢???곸긽?대㈃ 403

    # === 6. 醫낇빀 蹂닿퀬??===
    # v2.89.50 ???쒓컖?곸쑝濡???硫뗭쭊 ?덉씠?꾩썐. 釉붾줉?몄슜쨌?대え吏 ?됯?쨌?쒓컖 遺꾨━???쒖슜.
    sub_str = "鍮꾧났媛? if subs_hidden else f"{_fmt_num(sub_count)}紐?
    like_rating = "?윟 醫뗭쓬" if avg_like_rate >= 2.0 else ("?윞 蹂댄넻" if avg_like_rate >= 1.0 else "?뵶 媛쒖꽑")
    comment_rating = "?윟 醫뗭쓬" if avg_comment_rate >= 0.5 else ("?윞 蹂댄넻" if avg_comment_rate >= 0.2 else "?뵶 媛쒖꽑")
    L = []
    L.append(f"# ?렗 {ch_title}")
    L.append(f"_{time.strftime('%Y-%m-%d %H:%M')} 쨌 理쒓렐 {lookback}??遺꾩꽍 쨌 ?곸긽 {len(rows)}媛?")
    L.append("")
    # 梨꾨꼸 硫뷀? ???몄슜 釉붾줉?쇰줈 ?쒕늿??    L.append(f"> **{sub_str}** 援щ룆??쨌 **{_fmt_num(view_count_total)}** ?꾩쟻 議고쉶 쨌 **{video_count_total:,}媛?* ?곸긽" + (f" 쨌 **{age_years:.1f}??* ?댁쁺" if age_years > 0 else ""))
    L.append(f"> ?몃뱾 `{custom_url or handle or '-'}`" + (f" 쨌 ?뙇 {country}" if country else "") + f" 쨌 ?곸긽???됯퇏 **{_fmt_num(avg_views_per_video_alltime)}** 議고쉶")
    L.append("")
    L.append("?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺")
    L.append("")

    # 理쒓렐 ?깃낵 ?붿빟 ??移대뱶 ?ㅽ???    L.append(f"## ?뱤 理쒓렐 {lookback}???깃낵 ?쒕늿??)
    L.append("")
    L.append("| 吏??| 媛?| ?됯? |")
    L.append("|---|---|---|")
    pace = (len(rows) * 30 / lookback) if lookback > 0 else 0
    pace_rating = "?윟 ?쒕컻" if pace >= 4 else ("?윞 蹂댄넻" if pace >= 2 else "?뵶 ?議?)
    L.append(f"| ?낅줈??| {len(rows)}媛?(??{pace:.1f}媛? | {pace_rating} |")
    if rows:
        L.append(f"| 議고쉶??以묎컙媛?| **{_fmt_num(median_views)}** | 理쒓퀬 {_fmt_num(rows_sorted[0]['views'])} 쨌 理쒖? {_fmt_num(rows_sorted[-1]['views'])} |")
    L.append(f"| 醫뗭븘?붿쑉 | **{avg_like_rate:.2f}%** | {like_rating} (?낃퀎 2~5%) |")
    L.append(f"| ?볤???| **{avg_comment_rate:.2f}%** | {comment_rating} (?낃퀎 0.3~1%) |")
    L.append(f"| ?됯퇏 湲몄씠 | {_fmt_duration(avg_duration)} | ?쒕ぉ ?됯퇏 {avg_title_len}??|")
    if shorts_count:
        L.append(f"| Shorts | {shorts_count}媛?/ {len(rows)} | - |")
    L.append("")
    L.append("?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺")
    L.append("")

    # ?곸긽蹂??곸꽭 ??    L.append("## ?벟 ?곸긽蹂??곸꽭 (議고쉶????")
    L.append("| # | 議고쉶??| 醫뗭븘??(?? | ?볤? (?? | 湲몄씠 | 諛쒗뻾 | ?쒕ぉ |")
    L.append("|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows_sorted, 1):
        marker = "?뵦" if r["views"] >= median_views * 1.5 else ("?몟" if r["views"] >= median_views else "?Ⅶ")
        title_short = r['title'].replace('|', '\\|')[:60]
        L.append(f"| {i}{marker} | {_fmt_num(r['views'])} | {_fmt_num(r['likes'])} ({r['like_rate']:.1f}%) | {_fmt_num(r['comments'])} ({r['comment_rate']:.1f}%) | {_fmt_duration(r['duration_sec'])} | {r['pub']}({r['weekday']}) | {title_short} |")
    L.append("")

    # ?곸쐞 ?곸긽 ?ъ링 遺꾩꽍 ??移대뱶 ?ㅽ???+ 硫붾떖 ?대え吏
    L.append("## ?룇 TOP 3 ??臾댁뾿?????먮굹")
    L.append("")
    medals = ["?쪍", "?쪎", "?쪏"]
    for idx, r in enumerate(top_videos):
        medal = medals[idx] if idx < 3 else "?몟"
        L.append(f"### {medal} {_fmt_num(r['views'])}??쨌 {r['title']}")
        L.append("")
        L.append(f"> ?뱟 {r['pub']} ({r['weekday']}?붿씪 {r['hour']:02d}?? 쨌 ??{_fmt_duration(r['duration_sec'])} 쨌 ?몟 {r['like_rate']:.2f}% 쨌 ?뮠 {r['comment_rate']:.2f}%")
        if r['tags']:
            tag_str = ' '.join(f"`{t}`" for t in r['tags'][:5])
            L.append(f"> ?뤇 {tag_str}" + (' ?? if len(r['tags']) > 5 else ''))
        L.append(f"> ?뵕 [?곸긽 蹂닿린](https://youtu.be/{r['id']}) 쨌 ?뼹 [?몃꽕??(https://i.ytimg.com/vi/{r['id']}/mqdefault.jpg)")
        cs = comments_by_video.get(r["id"], [])
        if cs:
            L.append("")
            L.append("**?뮠 ?멸린 ?볤?:**")
            for c in cs[:3]:
                txt = c['text'].replace(chr(10), ' ').replace(chr(13), ' ')[:140]
                L.append(f"> _{c['author']}_ (?몟{c['likes']}): {txt}")
        L.append("")

    # ?섏쐞 ?곸긽 ???쒓컖?곸쑝濡?遺吏?媛뺤“
    if bottom_videos:
        L.append("?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺")
        L.append("")
        L.append("## ?Ⅶ ?섏쐞 ?곸긽 ??媛쒖꽑 ?꾩슂")
        L.append("")
        for r in bottom_videos:
            gap_pct = int((1 - r['views'] / median_views) * 100) if median_views else 0
            L.append(f"- **{_fmt_num(r['views'])}??* 쨌 以묎컙媛??鍮?**-{gap_pct}%** ??)
            L.append(f"  - {r['title']}")
            L.append(f"  - ?뱟 {r['pub']}({r['weekday']}, {r['hour']:02d}?? 쨌 ??{_fmt_duration(r['duration_sec'])} 쨌 ?뵕 [?곸긽](https://youtu.be/{r['id']})")
        L.append("")

    # ?⑦꽩
    L.append("?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺")
    L.append("")
    L.append("## ?뵇 ?⑦꽩 遺꾩꽍")
    L.append("")
    if weekday_avg and len(weekday_avg) >= 2:
        best_day = max(weekday_avg.items(), key=lambda x: x[1])
        worst_day = min(weekday_avg.items(), key=lambda x: x[1])
        ratio = best_day[1] / worst_day[1] if worst_day[1] else 1
        L.append(f"- ?뱟 **理쒓퀬 ?붿씪**: {best_day[0]}?붿씪 (?됯퇏 {_fmt_num(best_day[1])}?? ??理쒖? ?鍮?**{ratio:.1f}諛?*")
        L.append(f"- ?뱟 **理쒖? ?붿씪**: {worst_day[0]}?붿씪 (?됯퇏 {_fmt_num(worst_day[1])}??")
    if top_keywords:
        L.append(f"- ?뵎 **?곸쐞 ?곸긽 ?ㅼ썙??*: {' '.join('`'+k+'`' for k in top_keywords)}")
    if title_lengths:
        L.append(f"- ?뱷 **?쒕ぉ 湲몄씠**: ?됯퇏 {avg_title_len}??(理쒕떒 {min(title_lengths)}??쨌 理쒖옣 {max(title_lengths)}??")
    if avg_duration > 0:
        L.append(f"- ??**?곸긽 湲몄씠**: ?됯퇏 {_fmt_duration(avg_duration)}" + (f" 쨌 Shorts(60珥??댄븯) {shorts_count}/{len(rows)}媛? if shorts_count else ""))
    L.append("")

    # ?≪뀡 異붿쿇 ??移대뱶 ?ㅽ???    L.append("")
    L.append("?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺")
    L.append("")
    L.append("## ?렞 ?ㅼ쓬 ?≪뀡 (?곗꽑?쒖쐞)")
    L.append("")
    recs = []
    if bottom_videos:
        worst = bottom_videos[0]
        recs.append(("?뵶", f"**遺吏??곸긽 ?대━湲?* ??`{worst['title'][:40]}` ({_fmt_num(worst['views'])}??. ?몃꽕??A/B ?먮뒗 ?쒕ぉ 由щ꽕?대컢."))
    if top_videos:
        winner = top_videos[0]
        recs.append(("?뵦", f"**?≪긽 ?⑦꽩 蹂듭젣** ??`{winner['title'][:40]}` ({_fmt_num(winner['views'])}??. 媛숈? ?꾪겕/?щ㎎?쇰줈 ?꾩냽??"))
    if weekday_avg and len(weekday_avg) >= 3:
        best_day = max(weekday_avg.items(), key=lambda x: x[1])[0]
        recs.append(("?뱟", f"**諛쒗뻾 ?붿씪 理쒖쟻??* ??{best_day}?붿씪 ?곸긽???됯퇏 媛?????? ?ㅼ쓬 ?낅줈??{best_day}?붿씪 異붿쿇."))
    if avg_like_rate < 2.0 and avg_views > 100:
        recs.append(("?몟", f"**醫뗭븘?붿쑉 媛쒖꽑** ???꾩옱 {avg_like_rate:.2f}% (?낃퀎 2~5%). ?곸긽 ??肄쒖븘??媛뺥솕."))
    if avg_comment_rate < 0.3 and avg_views > 100:
        recs.append(("?뮠", f"**?볤? ?좊룄 媛뺥솕** ???꾩옱 {avg_comment_rate:.2f}% (?낃퀎 0.3~1%). ?곸긽 以묎컙 ?쒖껌???섍껄 吏덈Ц ?쎌엯."))
    if top_keywords:
        recs.append(("?뵎", f"**?쒕ぉ ?ㅼ썙???쒖슜** ???곸쐞 ?곸긽??`{', '.join(top_keywords[:3])}` ?ㅼ썙?쒕? ?ㅼ쓬 ?쒕ぉ???듯빀."))
    if shorts_count == 0 and len(rows) >= 5:
        recs.append(("?벑", f"**Shorts ?쒕룄** ??理쒓렐 {lookback}?쇱뿉 Shorts 0媛? ?좉퇋 ?좎엯 梨꾨꼸濡?醫뗭쓬."))
    if pace < 2:
        recs.append(("??, f"**?낅줈??鍮덈룄 ?먭?** ????{pace:.1f}媛??섏씠?? ?뚭퀬由ъ쬁 移쒗솕???섏씠?ㅻ뒗 二?1??."))
    if not recs:
        recs.append(("?뱄툘", "?곗씠??遺議?????留롮? ?곸긽 ?낅줈?????щ텇??沅뚯옣"))
    for i, (icon, rec) in enumerate(recs, 1):
        L.append(f"**{i}. {icon} {rec}**" if i == 1 else f"{i}. {icon} {rec}")
    L.append("")

    # ?쒖껌??諛섏쓳 ?ㅼ썙??(?곸쐞 ?곸긽 ?볤? 湲곕컲)
    all_comments = []
    for cs in comments_by_video.values():
        all_comments.extend(c["text"] for c in cs)
    if all_comments:
        L.append("?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺?곣봺")
        L.append("")
        L.append("## ?뮠 ?쒖껌?먭? ?④릿 ?ㅼ썙??)
        L.append("")
        all_text = " ".join(all_comments)
        words = re.findall(r'[媛-??{2,}|[a-zA-Z]{3,}', all_text)
        # URL 議곌컖쨌?꾨찓?몄? ?섎? ?놁쑝???쒖쇅
        url_noise = {'https', 'http', 'youtu', 'www', 'com'}
        words = [w for w in words if w.lower() not in stop_en and w not in stop_kr and w.lower() not in url_noise and not re.match(r'^[a-zA-Z0-9_]{8,}$', w)]
        word_freq = Counter(words).most_common(8)
        if word_freq:
            kw_line = ' 쨌 '.join(f"`{w}`({c})" for w, c in word_freq)
            L.append(kw_line)
            L.append("")
            L.append("> ?쒖껌??癒몃┸?띿뿉 ?⑥? ?⑥뼱. ?ㅼ쓬 ?곸긽 ?쒕ぉ쨌?몃꽕?셋룻썑?ъ뿉 ?쒖슜.")
        L.append("")

    summary = chr(10).join(L)
    # v2.89.49 ??stdout? 蹂닿퀬??markdown留? 硫뷀?쨌吏꾨떒 硫붿떆吏??stderr濡?
    print(summary)
    with open(REPORT, "a", encoding="utf-8") as f:
        f.write(chr(10) + chr(10) + summary + chr(10) + chr(10) + "---" + chr(10))
    print(f"\n??蹂닿퀬????? {REPORT}", file=sys.stderr)
    # Telegram (4096???쒗븳 ??plain text??留덊겕?ㅼ슫 ?뱀닔臾몄옄 洹몃?濡?蹂대궡???듦낵)
    tg_lines = []
    tg_lines.append(f"?뱤 {ch_title} ??梨꾨꼸 遺꾩꽍")
    tg_lines.append(f"({time.strftime('%Y-%m-%d %H:%M')} 쨌 理쒓렐 {lookback}??쨌 ?곸긽 {len(rows)}媛?")
    tg_lines.append("")
    tg_lines.append(f"援щ룆??{sub_str} 쨌 ?꾩쟻 {_fmt_num(view_count_total)} 쨌 珥?{video_count_total}媛?)
    if rows:
        tg_lines.append(f"以묎컙媛?{_fmt_num(median_views)}??쨌 理쒓퀬 {_fmt_num(rows_sorted[0]['views'])} 쨌 理쒖? {_fmt_num(rows_sorted[-1]['views'])}")
    tg_lines.append(f"醫뗭븘?붿쑉 {avg_like_rate:.2f}% 쨌 ?볤???{avg_comment_rate:.2f}%")
    tg_lines.append("")
    if top_videos:
        tg_lines.append(f"?룇 理쒓퀬: {_fmt_num(top_videos[0]['views'])} {top_videos[0]['title'][:40]}")
    if bottom_videos:
        tg_lines.append(f"?Ⅶ 遺吏? {_fmt_num(bottom_videos[0]['views'])} {bottom_videos[0]['title'][:40]}")
    tg_lines.append("")
    if recs:
        tg_lines.append("?렞 ?≪뀡:")
        for i, (icon, rec) in enumerate(recs[:3], 1):
            # 留덊겕?ㅼ슫 ** ?쒓굅?섍퀬 plain text濡?            clean = re.sub(r'\*\*|`', '', rec.split(' ??')[0] if ' ??' in rec else rec)
            tg_lines.append(f"{i}. {icon} {clean[:80]}")
    tg_lines.append("")
    tg_lines.append("(?꾩껜 遺꾩꽍? IDE 梨꾪똿李??뺤씤)")
    tg_text = chr(10).join(tg_lines)
    _push_telegram(acct, tg_text)

if __name__ == "__main__":
    main()
