#!/usr/bin/env python
# version: music_v3
"""?앹꽦??BGM???곸긽???⑹튂湲?(ffmpeg ?섑띁).

?ㅼ젙?먯꽌 VIDEO_PATH 吏??(?먮뒗 LAST_GENERATED ?먮룞 ?ъ슜).
?곸긽 湲몄씠??BGM ?먮룞 留욎땄 (loop ?먮뒗 fade out).
"""
import os, sys, json, subprocess, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
GEN_CONFIG = os.path.join(HERE, "music_generate.json")
MERGE_CONFIG = os.path.join(HERE, "music_to_video.json")


def _log(msg, kind="info"):
    prefix = {"info": "[INFO]", "ok": "[OK]", "warn": "[WARN]", "err": "[ERR]"}.get(kind, "")
    print(f"{prefix} {msg}", file=sys.stderr, flush=True)


def _load(p):
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def main():
    if not shutil.which("ffmpeg"):
        print("??ffmpeg媛 ?ㅼ튂?쇱엳吏 ?딆븘??")
        print("  macOS: brew install ffmpeg")
        print("  Windows: https://ffmpeg.org/download.html")
        sys.exit(1)

    cfg = _load(MERGE_CONFIG)
    gen = _load(GEN_CONFIG)

    video_path = (cfg.get("VIDEO_PATH") or "").strip()
    if not video_path:
        print("??VIDEO_PATH 誘몄꽕?? ?숋툘 ?대┃?댁꽌 ?곸긽 ?뚯씪 寃쎈줈 ?낅젰?댁＜?몄슂.")
        sys.exit(1)
    video_path = os.path.expanduser(video_path)
    if not os.path.exists(video_path):
        print(f"???곸긽 ?뚯씪 ?놁쓬: {video_path}")
        sys.exit(1)

    # BGM ?뚯씪: 紐낆떆???먮뒗 留덉?留??앹꽦??嫄??먮룞
    music_path = (cfg.get("MUSIC_PATH") or "").strip()
    if not music_path:
        music_path = gen.get("LAST_OUTPUT") or ""
    if not music_path or not os.path.exists(music_path):
        print("??BGM ?뚯씪 ?놁쓬. 癒쇱? 'music_generate.py' ?ㅽ뻾?댁꽌 BGM ?앹꽦?섍굅??")
        print("  ?숋툘?먯꽌 MUSIC_PATH 吏곸젒 吏??")
        sys.exit(1)

    bgm_volume = float(cfg.get("BGM_VOLUME", 0.3))  # 0.0~1.0, ?뷀뤃??30%
    output_path = cfg.get("OUTPUT_PATH") or video_path.rsplit(".", 1)[0] + "_with_bgm.mp4"

    _log(f"?곸긽: {video_path}")
    _log(f"BGM: {music_path}")
    _log(f"BGM 蹂쇰ⅷ: {int(bgm_volume * 100)}%")
    _log(f"異쒕젰: {output_path}")

    # ffmpeg: ?곸긽 + BGM 誘뱀떛. ?곸긽 湲몄씠??BGM 留욎땄 (BGM??吏㏃쑝硫?loop, 湲몃㈃ ?먮쫫)
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-stream_loop", "-1",  # BGM 臾댄븳 loop (?곸긽 湲몄씠源뚯?)
        "-i", music_path,
        "-filter_complex",
        f"[0:a]volume=1.0[orig];[1:a]volume={bgm_volume}[bgm];[orig][bgm]amix=inputs=2:duration=first[a]",
        "-map", "0:v",
        "-map", "[a]",
        "-c:v", "copy",  # ?곸긽 肄붾뜳 洹몃?濡?(?ъ씤肄붾뵫 ?놁쓬 = 鍮좊쫫)
        "-c:a", "aac",
        "-shortest",
        output_path,
    ]
    _log("ffmpeg ?ㅽ뻾 以?..")
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"??ffmpeg ?ㅽ뙣 (exit {proc.returncode})")
        print(proc.stderr[-1000:])
        sys.exit(1)

    if not os.path.exists(output_path):
        print(f"??異쒕젰 ?뚯씪 ?놁쓬")
        sys.exit(1)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"✅ 영상 + BGM 합성 완료")
    print(f"  - 위치: {output_path}")
    print(f"  - 크기: {size_mb:.1f} MB")
    print(f"  - 볼륨: BGM 볼륨 {int(bgm_volume * 100)}%로 믹싱됨")


if __name__ == "__main__":
    main()
