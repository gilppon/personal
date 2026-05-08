#!/usr/bin/env python
"""Comment Harvester ??for every channel in WATCHED_CHANNELS, pulls the most
recent N videos and their top M comments. Appends the results to the agent's
memory.md so the YouTube agent can reference real audience reactions on the
next think step.

Reads from youtube_account.json (api key, watched channels) and
comment_harvester.json (volume settings)."""
import os, json, sys, time, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ACCOUNT = os.path.join(HERE, "youtube_account.json")
CONFIG  = os.path.join(HERE, "comment_harvester.json")
# memory.md lives one level up ??under _agents/youtube/
MEMORY  = os.path.abspath(os.path.join(HERE, "..", "memory.md"))
REPORT  = os.path.join(HERE, "comment_harvester_report.md")

def _load(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def _resolve_channel_id(youtube, handle):
    h = handle.lstrip("@")
    try:
        r = youtube.search().list(part="snippet", q=h, type="channel", maxResults=1).execute()
        items = r.get("items", [])
        if items:
            return items[0]["snippet"]["channelId"], items[0]["snippet"]["title"]
    except Exception as e:
        print(f"?좑툘  {handle} 梨꾨꼸 議고쉶 ?ㅽ뙣: {e}")
    return None, None

def main():
    if not os.path.exists(ACCOUNT):
        print("??youtube_account.json???놁뼱?? 癒쇱? 洹??꾧뎄濡??ㅼ젙.")
        sys.exit(1)
    acct = _load(ACCOUNT)
    cfg  = _load(CONFIG) if os.path.exists(CONFIG) else {}
    api_key = (acct.get("YOUTUBE_API_KEY") or "").strip()
    watched = acct.get("WATCHED_CHANNELS") or []
    if not api_key:
        print("??YOUTUBE_API_KEY 鍮꾩뼱?덉쓬.")
        sys.exit(1)
    if not watched:
        print("??WATCHED_CHANNELS媛 鍮꾩뼱?덉뼱?? youtube_account.json???몃뱾 紐⑸줉???ｌ뼱二쇱꽭??")
        print('    ?? "WATCHED_CHANNELS": ["@channel_a", "@channel_b"]')
        sys.exit(1)
    vids_per = int(cfg.get("VIDEOS_PER_CHANNEL", 5))
    cmts_per = int(cfg.get("COMMENTS_PER_VIDEO", 20))
    lookback = int(cfg.get("LOOKBACK_DAYS", 14))

    try:
        from googleapiclient.discovery import build
    except ImportError:
        print("??pip install google-api-python-client")
        sys.exit(1)
    youtube = build("youtube", "v3", developerKey=api_key)
    after = (datetime.datetime.utcnow() - datetime.timedelta(days=lookback)).isoformat("T") + "Z"

    harvested = []
    for ch in watched:
        cid, ctitle = _resolve_channel_id(youtube, ch)
        if not cid:
            continue
        print(f"?뱻 [{ch}] 理쒓렐 ?곸긽 {vids_per}媛?媛?몄삤??以?..")
        sr = youtube.search().list(part="snippet", channelId=cid, maxResults=vids_per,
                                    order="date", publishedAfter=after, type="video").execute()
        for it in sr.get("items", []):
            vid = it["id"]["videoId"]
            vtitle = it["snippet"]["title"]
            print(f"  ?뮠 {vtitle[:60]}")
            try:
                cr = youtube.commentThreads().list(part="snippet", videoId=vid,
                                                    maxResults=cmts_per, order="relevance",
                                                    textFormat="plainText").execute()
            except Exception as e:
                msg = str(e)
                if "commentsDisabled" in msg or "disabled" in msg.lower():
                    continue
                print(f"  ?좑툘  ?볤? 媛?몄삤湲??ㅽ뙣: {e}")
                continue
            comments = []
            for ci in cr.get("items", []):
                top = ci["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "author": top.get("authorDisplayName", ""),
                    "likes": int(top.get("likeCount", 0)),
                    "text": (top.get("textDisplay", "") or "")[:280],
                })
            harvested.append({
                "channel": ch, "channel_title": ctitle,
                "video": vtitle, "video_id": vid, "comments": comments,
            })

    if not harvested:
        print("?좑툘  ?섏쭛???볤? ?놁쓬.")
        sys.exit(0)

    ts = time.strftime('%Y-%m-%d %H:%M')
    md_lines = [f"\n## ?뮠 ?쒖껌???볤? ?섏쭛 ??{ts}"]
    for h in harvested:
        md_lines.append(f"\n### {h['channel_title']} ({h['channel']}) ??{h['video']}")
        md_lines.append(f"https://youtu.be/{h['video_id']}")
        for c in h["comments"][:10]:
            md_lines.append(f"- ({c['likes']}?? **{c['author']}**: {c['text']}")
    block = "\n".join(md_lines)

    # Append to memory so the agent uses these comments next think.
    os.makedirs(os.path.dirname(MEMORY), exist_ok=True)
    if not os.path.exists(MEMORY):
        with open(MEMORY, "w", encoding="utf-8") as f:
            f.write("# YouTube ?먯씠?꾪듃 ??硫붾え由?n\n")
    with open(MEMORY, "a", encoding="utf-8") as f:
        f.write("\n" + block + "\n")
    with open(REPORT, "a", encoding="utf-8") as f:
        f.write("\n" + block + "\n\n---\n")
    print(f"\n??硫붾え由ъ뿉 異붽?: {MEMORY}")
    print(f"??蹂닿퀬?? {REPORT}")
    print(f"   {len(harvested)}媛??곸긽 쨌 ?됯퇏 {sum(len(h['comments']) for h in harvested)//max(len(harvested),1)}媛??볤?")

if __name__ == "__main__":
    main()
