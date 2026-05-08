#!/usr/bin/env python
"""Channel Full Analysis ??comprehensive overview of your YouTube channel.

Input: just YOUTUBE_API_KEY + MY_CHANNEL_ID/HANDLE from youtube_account.json.
No additional config needed. Output: full report with stats, patterns, and
data-driven recommendations.
"""
import os, json, sys, time, datetime, statistics, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ACCOUNT = os.path.join(HERE, "youtube_account.json")
REPORT  = os.path.join(HERE, "channel_full_analysis_report.md")

def _load(p):
    with open(p, "r", encoding="utf-8-sig") as f:
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

def _parse_iso_duration(d):
    """ISO 8601 duration (PT4M30S) ??seconds."""
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    if not m: return 0
    h, mi, s = m.groups()
    return int(h or 0) * 3600 + int(mi or 0) * 60 + int(s or 0)

def _fmt_duration(sec):
    if sec < 60: return f"{sec}s"
    if sec < 3600: return f"{sec//60}m {sec%60}s"
    return f"{sec//3600}h {(sec%3600)//60}m"

def _resolve_telegram(account):
    """Same fallback chain as my_videos_check.py."""
    import json as _json
    token = (account.get("TELEGRAM_BOT_TOKEN") or "").strip()
    chat  = (account.get("TELEGRAM_CHAT_ID") or "").strip()
    if token and chat:
        return token, chat
    brain_root = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    sec_json = os.path.join(brain_root, "_agents", "secretary", "tools", "telegram_setup.json")
    if (not token or not chat) and os.path.exists(sec_json):
        try:
            with open(sec_json, "r", encoding="utf-8-sig") as f:
                cfg = _json.load(f)
            if not token: token = (cfg.get("TELEGRAM_BOT_TOKEN") or "").strip()
            if not chat:  chat  = (cfg.get("TELEGRAM_CHAT_ID") or "").strip()
        except Exception:
            pass
    return token, chat

def _push_telegram(account, text):
    token, chat = _resolve_telegram(account)
    if not token or not chat:
        return
    try:
        import requests
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat, "text": text, "parse_mode": "Markdown"},
            timeout=10,
        )
        print("?벂 ?붾젅洹몃옩?쇰줈 蹂닿퀬 ?꾩넚")
    except Exception as e:
        print(f"?좑툘  ?붾젅洹몃옩 ?꾩넚 ?ㅽ뙣: {e}")

def main():
    if not os.path.exists(ACCOUNT):
        print("??youtube_account.json???놁뼱?? ?몃? ?곌껐 ?⑤꼸?먯꽌 YouTube API ?ㅼ? 梨꾨꼸 ID ?낅젰?댁＜?몄슂.")
        sys.exit(1)
    acct = _load(ACCOUNT)
    api_key = (acct.get("YOUTUBE_API_KEY") or "").strip()
    handle  = (acct.get("MY_CHANNEL_HANDLE") or "").strip()
    chan_id = (acct.get("MY_CHANNEL_ID") or "").strip()
    if not api_key:
        print("??YOUTUBE_API_KEY媛 鍮꾩뼱?덉뼱?? ?몃? ?곌껐 ?⑤꼸 ??YouTube Data API 移대뱶???낅젰?댁＜?몄슂.")
        sys.exit(1)
    if not (handle or chan_id):
        print("??MY_CHANNEL_HANDLE ?먮뒗 MY_CHANNEL_ID ?꾩슂. ?몃? ?곌껐 ?⑤꼸 ??梨꾨꼸 ID ?낅젰?댁＜?몄슂.")
        sys.exit(1)

    try:
        from googleapiclient.discovery import build
    except ImportError:
        print("??google-api-python-client 誘몄꽕移?")
        print("   ?곕??먯뿉????以? pip3 install google-api-python-client requests")
        sys.exit(1)
    youtube = build("youtube", "v3", developerKey=api_key)

    cid = _resolve_channel_id(youtube, handle, chan_id)
    if not cid:
        print("??梨꾨꼸 ID瑜?李얠? 紐삵뻽?댁슂. ?몃? ?곌껐 ?⑤꼸??梨꾨꼸 ID ?뺤씤.")
        sys.exit(1)

    print(f"?뱢 [梨꾨꼸 ?꾩쟾 遺꾩꽍] 梨꾨꼸 {handle or cid} 遺꾩꽍 以?..")
    print()

    # 1. 梨꾨꼸 硫뷀?
    ch = youtube.channels().list(part="snippet,statistics,brandingSettings", id=cid).execute()
    if not ch.get("items"):
        print("??梨꾨꼸 ?곗씠?곕? 媛?몄삤吏 紐삵뻽?댁슂. API ?ㅒ룻븷?밸웾 ?뺤씤.")
        sys.exit(1)
    c = ch["items"][0]
    sn = c.get("snippet", {})
    st = c.get("statistics", {})
    title = sn.get("title", "(?대쫫 ?놁쓬)")
    subs = int(st.get("subscriberCount", 0))
    total_views = int(st.get("viewCount", 0))
    video_count = int(st.get("videoCount", 0))
    pub_at = sn.get("publishedAt", "")[:10]

    print("??? 1. 梨꾨꼸 媛쒖슂 ???")
    print(f"  梨꾨꼸: {title}")
    print(f"  ?몃뱾: {sn.get('customUrl', handle or '(?놁쓬)')}")
    print(f"  援щ룆?? {subs:,}紐?)
    print(f"  珥?議고쉶?? {total_views:,}??)
    print(f"  ?낅줈???곸긽: {video_count}媛?)
    print(f"  梨꾨꼸 媛?? {pub_at}")
    avg_per_video = total_views // max(1, video_count)
    print(f"  ?곸긽???됯퇏 議고쉶: {avg_per_video:,}??)
    print()

    # 2. 理쒓렐 30???곸긽 遺꾩꽍 (uploads playlist ?ъ슜 ??search蹂대떎 quota ?덉빟)
    uploads = c.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads") if "contentDetails" in c else None
    if not uploads:
        # contentDetails ?놁쑝硫?search濡??대갚
        cd = youtube.channels().list(part="contentDetails", id=cid).execute()
        if cd.get("items"):
            uploads = cd["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30)
    recent_video_ids = []
    if uploads:
        next_token = None
        while len(recent_video_ids) < 50:
            args = {"part": "snippet,contentDetails", "playlistId": uploads, "maxResults": 50}
            if next_token: args["pageToken"] = next_token
            pi = youtube.playlistItems().list(**args).execute()
            for item in pi.get("items", []):
                pub = item["snippet"]["publishedAt"]
                pub_dt = datetime.datetime.fromisoformat(pub.replace("Z", "+00:00"))
                if pub_dt < cutoff:
                    break
                recent_video_ids.append(item["contentDetails"]["videoId"])
            next_token = pi.get("nextPageToken")
            if not next_token: break
            if recent_video_ids and datetime.datetime.fromisoformat(pi["items"][-1]["snippet"]["publishedAt"].replace("Z", "+00:00")) < cutoff:
                break

    if not recent_video_ids:
        print("?좑툘  理쒓렐 30???숈븞 ?낅줈?쒗븳 ?곸긽???놁뼱?? ?곸긽 ?낅줈?????ㅼ떆 遺꾩꽍?댁＜?몄슂.")
        sys.exit(0)

    # 3. ?곸긽蹂??듦퀎 (50媛쒖뵫 ?섎닠??
    all_vids = []
    for i in range(0, len(recent_video_ids), 50):
        chunk = recent_video_ids[i:i+50]
        st_resp = youtube.videos().list(part="snippet,statistics,contentDetails", id=",".join(chunk)).execute()
        for v in st_resp.get("items", []):
            stats = v.get("statistics", {})
            sn_v = v.get("snippet", {})
            cd_v = v.get("contentDetails", {})
            views = int(stats.get("viewCount", 0))
            likes = int(stats.get("likeCount", 0))
            comments = int(stats.get("commentCount", 0))
            duration_sec = _parse_iso_duration(cd_v.get("duration", ""))
            pub = sn_v.get("publishedAt", "")
            pub_dt = datetime.datetime.fromisoformat(pub.replace("Z", "+00:00"))
            all_vids.append({
                "id": v["id"],
                "title": sn_v.get("title", ""),
                "views": views,
                "likes": likes,
                "comments": comments,
                "duration_sec": duration_sec,
                "pub_dt": pub_dt,
                "engagement_rate": (likes + comments) / views if views > 0 else 0,
            })

    all_vids.sort(key=lambda x: x["views"], reverse=True)
    views_list = [v["views"] for v in all_vids]
    median_views = statistics.median(views_list) if views_list else 0
    mean_views = statistics.mean(views_list) if views_list else 0

    print("??? 2. 理쒓렐 30???낅줈???⑦꽩 ???")
    print(f"  ?낅줈???잛닔: {len(all_vids)}媛?(?뷀룊洹?{len(all_vids):.1f}媛?")
    weekday_counts = Counter(v["pub_dt"].strftime("%A") for v in all_vids)
    weekday_kr = {"Monday":"??,"Tuesday":"??,"Wednesday":"??,"Thursday":"紐?,"Friday":"湲?,"Saturday":"??,"Sunday":"??}
    top_day = weekday_counts.most_common(1)
    if top_day:
        print(f"  二쇰줈 ?낅줈?쒗븳 ?붿씪: {weekday_kr.get(top_day[0][0], top_day[0][0])}?붿씪 ({top_day[0][1]}??")
    avg_duration = sum(v["duration_sec"] for v in all_vids) / len(all_vids)
    print(f"  ?됯퇏 ?곸긽 湲몄씠: {_fmt_duration(int(avg_duration))}")
    print()

    print("??? 3. ?깃낵 ?듦퀎 ???")
    print(f"  以묎컙媛?議고쉶?? {int(median_views):,}??)
    print(f"  ?됯퇏 議고쉶?? {int(mean_views):,}??)
    avg_eng = sum(v["engagement_rate"] for v in all_vids) / len(all_vids) * 100 if all_vids else 0
    print(f"  ?됯퇏 李몄뿬??(醫뗭븘???볤?)/議고쉶: {avg_eng:.2f}%")
    print()

    # ?≪긽 / 遺吏?遺꾨쪟
    hot = [v for v in all_vids if v["views"] >= median_views * 1.5]
    cold = [v for v in all_vids if v["views"] < median_views * 0.5]

    print("??? 4. ?뵦 ?≪긽 ?곸긽 (以묎컙媛?횞 1.5 ?댁긽) ???")
    if not hot:
        print("  (?놁쓬 ??紐⑤뱺 ?곸긽???됯퇏 洹쇱쿂)")
    else:
        for v in hot[:5]:
            print(f"  ?뵦 {v['views']:>8,}??쨌 李몄뿬 {v['engagement_rate']*100:.2f}% 쨌 {_fmt_duration(v['duration_sec'])} 쨌 {v['title'][:50]}")
    print()

    print("??? 5. ?Ⅶ 遺吏??곸긽 (以묎컙媛?횞 0.5 誘몃쭔) ???")
    if not cold:
        print("  (?놁쓬 ??紐⑤뱺 ?곸긽???됯퇏 洹쇱쿂)")
    else:
        for v in cold[:5]:
            print(f"  ?Ⅶ {v['views']:>8,}??쨌 李몄뿬 {v['engagement_rate']*100:.2f}% 쨌 {_fmt_duration(v['duration_sec'])} 쨌 {v['title'][:50]}")
    print()

    # 6. ?⑦꽩 鍮꾧탳 ???≪긽 vs 遺吏꾩쓽 李⑥씠
    print("??? 6. ?≪긽 vs 遺吏????⑦꽩 鍮꾧탳 ???")
    if hot and cold:
        hot_avg_dur = sum(v["duration_sec"] for v in hot) / len(hot)
        cold_avg_dur = sum(v["duration_sec"] for v in cold) / len(cold)
        hot_avg_title = sum(len(v["title"]) for v in hot) / len(hot)
        cold_avg_title = sum(len(v["title"]) for v in cold) / len(cold)
        print(f"  ?≪긽 ?곸긽 ?됯퇏 湲몄씠: {_fmt_duration(int(hot_avg_dur))}")
        print(f"  遺吏??곸긽 ?됯퇏 湲몄씠: {_fmt_duration(int(cold_avg_dur))}")
        if abs(hot_avg_dur - cold_avg_dur) > 60:
            longer = "?≪긽" if hot_avg_dur > cold_avg_dur else "遺吏?
            print(f"  ??{longer} ?곸긽???됯퇏 {abs(int(hot_avg_dur - cold_avg_dur))}珥???湲몄뼱??)
        print(f"  ?≪긽 ?곸긽 ?됯퇏 ?쒕ぉ 湲몄씠: {hot_avg_title:.0f}??)
        print(f"  遺吏??곸긽 ?됯퇏 ?쒕ぉ 湲몄씠: {cold_avg_title:.0f}??)
    else:
        print("  (?≪긽 ?먮뒗 遺吏??곗씠??遺議????곸긽?????볦씠硫??ㅼ떆 遺꾩꽍)")
    print()

    # 7. ?먮룞 異붿쿇 (LLM ?놁씠 ?곗씠?곕쭔?쇰줈)
    print("??? 7. ?㎛ ?ㅼ쓬 ?≪뀡 異붿쿇 (?곗씠??湲곕컲) ???")
    actions = []
    if hot:
        actions.append(f"?뵦 ?≪긽??{len(hot)}媛??곸긽???쒕ぉ쨌?꾪겕 ?⑦꽩???ㅼ쓬 ?곸긽???곸슜 ??媛???????꾪겕??\"{hot[0]['title'][:50]}\"")
    if cold:
        actions.append(f"?Ⅶ 遺吏꾪븳 {len(cold)}媛쒕뒗 ?몃꽕??A/B ?뚯뒪???먮뒗 ?쒕ぉ 由щ꽕?대컢 ?꾨낫")
    if avg_eng < 2.0:
        actions.append(f"?뮉 ?됯퇏 李몄뿬??{avg_eng:.2f}% ???곸긽 ?앹뿉 紐낇솗??CTA(醫뗭븘?붋룰뎄?? 異붽? 異붿쿇 (蹂댄넻 3% ?댁긽??嫄닿컯??")
    elif avg_eng > 5.0:
        actions.append(f"?뮉 李몄뿬??{avg_eng:.2f}% ??留ㅼ슦 醫뗭쓬. ?쒖껌?먯? 媛뺥븳 ?곌껐 援ъ텞?? ?곹뭹쨌硫ㅻ쾭???꾩엯 怨좊젮 ?쒖젏")
    if len(all_vids) < 4:
        actions.append("?뱟 ??4媛?誘몃쭔 ?낅줈?????뚭퀬由ъ쬁 ?몄텧 ?꾪빐 理쒖냼 二?1??沅뚯옣")
    elif len(all_vids) > 12:
        actions.append("?뱟 ??12媛??댁긽 ?낅줈?????묒? 異⑸텇, ?곸긽蹂??덉쭏쨌?꾪겕??吏묒쨷 異붿쿇")
    if not actions:
        actions.append("??梨꾨꼸 ?곹깭 ?덉젙?????꾩옱 ?⑦꽩 ?좎??섎ŉ ?쒖껌???볤??먯꽌 ?ㅼ쓬 肄섑뀗痢??꾩씠?붿뼱 ?섏쭛")
    for a in actions:
        print(f"  ??{a}")
    print()

    # 8. 蹂닿퀬??.md ???    summary_lines = [
        f"# ?뱢 梨꾨꼸 ?꾩쟾 遺꾩꽍 ??{time.strftime('%Y-%m-%d %H:%M')}",
        f"梨꾨꼸: **{title}** 쨌 援щ룆??**{subs:,}** 쨌 ?곸긽 **{video_count}**媛?,
        "",
        "## 理쒓렐 30???듦퀎",
        f"- ?낅줈?? {len(all_vids)}媛?,
        f"- 議고쉶??以묎컙媛? **{int(median_views):,}**",
        f"- ?됯퇏 李몄뿬?? **{avg_eng:.2f}%**",
        f"- ?됯퇏 ?곸긽 湲몄씠: **{_fmt_duration(int(avg_duration))}**",
        "",
        f"## ?뵦 ?≪긽 ?곸긽 ({len(hot)}媛?",
    ]
    for v in hot[:5]:
        summary_lines.append(f"- {v['views']:,}??쨌 {v['title']}")
    summary_lines.append(f"\n## ?Ⅶ 遺吏??곸긽 ({len(cold)}媛?")
    for v in cold[:5]:
        summary_lines.append(f"- {v['views']:,}??쨌 {v['title']}")
    summary_lines.append("\n## ?㎛ ?ㅼ쓬 ?≪뀡 (?먮룞 異붿쿇)")
    for a in actions:
        summary_lines.append(f"- {a}")

    summary = "\n".join(summary_lines)
    with open(REPORT, "a", encoding="utf-8-sig") as f:
        f.write("\n\n" + summary + "\n\n---\n")
    print(f"??蹂닿퀬?? {REPORT}")
    _push_telegram(acct, summary)

if __name__ == "__main__":
    main()
