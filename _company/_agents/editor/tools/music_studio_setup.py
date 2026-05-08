#!/usr/bin/env python
# version: music_v5
"""?뚯븙 ?ㅽ뒠?붿삤 ???ㅼ쨷 紐⑤뜽 吏???먰겢由??ㅼ튂.

?좏깮 媛?ν븳 紐⑤뜽 (?붿뒪??룸찓紐⑤━쨌?덉쭏 ?몃젅?대뱶?ㅽ봽):

  ?뚢?????????????????????????р?????????р????????????р???????????????  ??MODEL                  ???붿뒪????硫붾え由?   ??異붿쿇        ??  ?쒋?????????????????????????쇄?????????쇄????????????쇄???????????????  ??musicgen-small (湲곕낯)  ??300MB  ??4GB+      ??紐⑤뱺 湲곌린   ??  ??musicgen-medium        ??1.5GB  ??6GB+      ??8GB+ RAM    ??  ??musicgen-large         ??3.3GB  ??12GB+     ??16GB+ RAM   ??  ??acestep-base           ??10GB   ??16GB+     ??16GB+ Mac   ??  ??acestep-xl             ??15GB+  ??24GB+     ??32GB+ 癒몄떊  ??  ?붴?????????????????????????닳?????????닳????????????닳???????????????
湲곕낯媛? musicgen-small ??300MB留?諛쏄퀬 30珥덈쭔??泥??뚯븙. 紐⑤뱺 湲곌린?먯꽌 ?덉젙??
??紐⑤뜽? 異붾줎 ??紐낆떆 RAM??1.5~2諛??ㅼ젣 ?뺣컯 諛쒖깮?댁꽌 ?먮룞 ?좏깮? 臾댁“嫄?small.
medium/large ?곌퀬 ?띠쑝硫?MODEL ?꾨뱶??吏곸젒 吏??

?숋툘 MODEL ?꾨뱶瑜???5媛?以??섎굹濡??ㅼ젙. ?ㅼ튂????踰덉뿉 ??紐⑤뜽留?(?좏깮??嫄?.
"""
import os, sys, json, subprocess, shutil, time

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "music_studio_setup.json")

# 紐⑤뜽 硫뷀? ???붿뒪??톀AM 異붿쿇쨌HuggingFace 寃쎈줈쨌?ㅼ튂 諛⑹떇
MODELS = {
    "musicgen-small": {
        "disk_gb": 0.3, "ram_gb": 4,
        "kind": "transformers", "hf_id": "facebook/musicgen-small",
        "deps": ["torch", "torchaudio", "transformers", "scipy", "soundfile"],
        "label": "MusicGen Small (300MB 쨌 紐⑤뱺 湲곌린)",
    },
    "musicgen-medium": {
        "disk_gb": 1.5, "ram_gb": 6,
        "kind": "transformers", "hf_id": "facebook/musicgen-medium",
        "deps": ["torch", "torchaudio", "transformers", "scipy", "soundfile"],
        "label": "MusicGen Medium (1.5GB 쨌 8GB+ RAM)",
    },
    "musicgen-large": {
        "disk_gb": 3.3, "ram_gb": 12,
        "kind": "transformers", "hf_id": "facebook/musicgen-large",
        "deps": ["torch", "torchaudio", "transformers", "scipy", "soundfile"],
        "label": "MusicGen Large (3.3GB 쨌 16GB+ RAM)",
    },
    "acestep-base": {
        "disk_gb": 10, "ram_gb": 16,
        "kind": "acestep", "hf_id": "ACE-Step/Ace-Step1.5",
        "repo": "https://github.com/ace-step/ACE-Step-1.5.git",
        "label": "ACE-Step 1.5 Base (10GB 쨌 16GB+ Mac/CUDA)",
    },
    "acestep-xl": {
        "disk_gb": 15, "ram_gb": 24,
        "kind": "acestep", "hf_id": "ACE-Step/acestep-v15-xl-base",
        "repo": "https://github.com/ace-step/ACE-Step-1.5.git",
        "label": "ACE-Step 1.5 XL (15GB 쨌 32GB+ 癒몄떊)",
    },
}

DEFAULT_INSTALL_DIR = os.path.expanduser("~/connect-ai-music")


def _log(msg, kind="info"):
    prefix = {"info": "[INFO]", "ok": "[OK]", "warn": "[WARN]", "err": "[ERR]"}.get(kind, "")
    print(f"{prefix} {msg}", file=sys.stderr, flush=True)


def _which(cmd):
    return shutil.which(cmd) is not None


def _system_ram_gb():
    """Detect system RAM. Cross-platform best effort."""
    try:
        import psutil
        return psutil.virtual_memory().total / (1024 ** 3)
    except ImportError:
        pass
    try:
        if sys.platform == "darwin":
            r = subprocess.run(["sysctl", "-n", "hw.memsize"], capture_output=True, text=True)
            return int(r.stdout.strip()) / (1024 ** 3)
        if sys.platform == "linux":
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        return int(line.split()[1]) / (1024 ** 2)
    except Exception:
        pass
    return 16  # 蹂댁닔??default


def _recommend_model(ram_gb):
    """RAM 湲곕컲 異붿쿇 紐⑤뜽. v2.89.78 ??蹂댁닔?곸쑝濡?small ?곗꽑.
    異붾줎????紐⑤뜽 weight + activation + scratch buffer ?⑹퀜??紐낆떆 RAM??1.5~2諛?    ?ㅼ젣 ?뺣컯 諛쒖깮. medium? 6GB 紐낆떆吏留??ㅼ젣濡?12GB+ ?뺣컯. 16GB Mac?먯꽌 OS쨌釉뚮씪?곗?쨌
    VS Code ?꾩슫 ?곹깭硫?medium 異붾줎 以?swap ??컻. small??紐⑤뱺 ?섍꼍?먯꽌 ?덉젙?곸씠怨?    ?덉쭏??異⑸텇. ?ъ슜?먭? ?먰븯硫?MODEL ?꾨뱶濡?吏곸젒 medium/large ?좏깮."""
    return "musicgen-small"


def _run(cmd, cwd=None):
    _log(f"$ {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        result = subprocess.run(
            cmd if isinstance(cmd, list) else cmd.split(),
            cwd=cwd, check=False, capture_output=True, text=True
        )
        # stderr媛 吏꾩쭨 ?먮윭硫??쒖떆, ?꾨땲硫?吏꾪뻾?곹솴?쇰줈 媛꾩＜ (pip ?깆? 吏꾪뻾?곹솴??stderr??
        for stream in (result.stdout, result.stderr):
            if stream and stream.strip():
                for line in stream.splitlines()[-20:]:  # 留덉?留?20以꾨쭔
                    _log(f"  {line}")
        return result.returncode == 0
    except Exception as e:
        _log(f"?ㅽ뻾 ?ㅻ쪟: {e}", "err")
        return False


def _load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def _install_transformers_model(model_key, install_dir):
    """MusicGen 瑜???pip + huggingface ?ㅼ슫濡쒕뱶. 媛踰쇱슫 寃쎈줈."""
    info = MODELS[model_key]
    venv = os.path.join(install_dir, ".venv")

    # venv ?앹꽦
    if not os.path.isdir(venv):
        _log("Python venv ?앹꽦...")
        if not _run(["python3", "-m", "venv", venv]):
            return False, "venv ?앹꽦 ?ㅽ뙣"

    venv_pip = os.path.join(venv, "bin", "pip")
    venv_python = os.path.join(venv, "bin", "python")
    if not os.path.exists(venv_pip):
        venv_pip = os.path.join(venv, "Scripts", "pip.exe")
        venv_python = os.path.join(venv, "Scripts", "python.exe")

    _log("Python ?섏〈???ㅼ튂 (1~3遺? ~500MB)...")
    _run([venv_pip, "install", "--upgrade", "pip", "--quiet"])
    if not _run([venv_pip, "install", "--quiet"] + info["deps"]):
        return False, "pip install ?ㅽ뙣"

    # 紐⑤뜽 weight ?ㅼ슫濡쒕뱶
    # v2.89.74 ??transformers/HF Hub??verbose 濡쒓렇 ?듭젣. ?댁쟾???ъ슜?먰븳??    # "decoder.model.decoder.embed_positions.weights | UNEXPECTED" 媛숈? ?대? 濡쒓렇 ?몄텧???쇰?.
    _log(f"紐⑤뜽 ?ㅼ슫濡쒕뱶 以? {info['hf_id']} ({info['disk_gb']}GB)...")
    download_script = f"""
import os
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'
os.environ['TRANSFORMERS_NO_ADVISORY_WARNINGS'] = '1'
import logging, warnings
logging.getLogger('transformers').setLevel(logging.ERROR)
logging.getLogger('huggingface_hub').setLevel(logging.WARNING)
warnings.filterwarnings('ignore')
print('?뵩 ?쇱씠釉뚮윭由?濡쒕뱶 以?..', flush=True)
from transformers import MusicgenForConditionalGeneration, AutoProcessor
print('?뵩 ?좏겕?섏씠?/?꾨줈?몄꽌 ?ㅼ슫濡쒕뱶 以?..', flush=True)
AutoProcessor.from_pretrained('{info['hf_id']}')
print('?뵩 紐⑤뜽 weight ?ㅼ슫濡쒕뱶 以?(??⑸웾, ?쒓컙 嫄몃┝)...', flush=True)
MusicgenForConditionalGeneration.from_pretrained('{info['hf_id']}')
print('??紐⑤뜽 ?ㅼ슫濡쒕뱶쨌濡쒕뱶 寃利??꾨즺')
"""
    if not _run([venv_python, "-c", download_script]):
        return False, "紐⑤뜽 ?ㅼ슫濡쒕뱶 ?ㅽ뙣 ???명꽣???곌껐 ?뺤씤"

    return True, venv_python


def _install_acestep(model_key, install_dir):
    """ACE-Step ??git clone + ???섏〈?? 臾닿굅??寃쎈줈."""
    info = MODELS[model_key]
    repo_dir = os.path.join(install_dir, "ace-step")

    if not os.path.isdir(repo_dir):
        _log(f"ACE-Step 1.5 clone 以???{repo_dir}")
        if not _run(["git", "clone", "--depth", "1", info["repo"], repo_dir]):
            return False, "git clone ?ㅽ뙣"

    venv = os.path.join(repo_dir, ".venv")
    if not os.path.isdir(venv):
        _log("Python venv ?앹꽦...")
        if not _run(["python3", "-m", "venv", venv]):
            return False, "venv ?앹꽦 ?ㅽ뙣"

    venv_pip = os.path.join(venv, "bin", "pip")
    venv_python = os.path.join(venv, "bin", "python")
    if not os.path.exists(venv_pip):
        venv_pip = os.path.join(venv, "Scripts", "pip.exe")
        venv_python = os.path.join(venv, "Scripts", "python.exe")

    requirements = os.path.join(repo_dir, "requirements.txt")
    if os.path.exists(requirements):
        _log(f"ACE-Step 의존성 설치 중 (5~10분 소요, 패키지 다운로드)...")
        _run([venv_pip, "install", "--upgrade", "pip", "--quiet"])
        if not _run([venv_pip, "install", "-r", requirements]):
            return False, "pip install 실패. 다시 실행하면 이어집니다."

    _log(f"모델 weight (~{info['disk_gb']}GB) 는 첫 음악 생성 시 자동 다운로드", "info")
    return True, venv_python


def main():
    cfg = _load_config()

    # 기본 의존성 검사
    missing = []
    if not _which("python3"):
        missing.append("python3 (https://www.python.org/downloads/)")
    if not _which("git"):
        missing.append("git (https://git-scm.com/downloads)")
    if missing:
        print("다음 도구 먼저 설치해주세요:")
        for m in missing:
            print(f"  - {m}")
        sys.exit(1)

    # 모델 선택: config에 MODEL 우선, 없으면 RAM 기반 추천
    requested = (cfg.get("MODEL") or "").strip()
    ram_gb = _system_ram_gb()
    if not requested:
        requested = _recommend_model(ram_gb)
        _log(f"시스템 RAM {ram_gb:.0f}GB 안전하게 {requested} 선택 (medium/large는 MODEL 필드에서 직접 지정)", "info")

    if requested not in MODELS:
        print(f"없는 MODEL: {requested}")
        print(f"  사용 가능: {', '.join(MODELS.keys())}")
        sys.exit(1)

    info = MODELS[requested]
    _log(f"설치 모델: {info['label']}")

    # 이미 설치되어있다면 빠르게 종료
    if cfg.get("INSTALLED_MODEL") == requested and cfg.get("VENV_PYTHON"):
        venv_python = cfg.get("VENV_PYTHON")
        if os.path.exists(venv_python):
            print(f"이미 설치 완료: {info['label']}")
            print(f"  경로 {cfg.get('INSTALL_DIR')}")
            print(f"  파이썬 {venv_python}")
            return

    install_dir = cfg.get("INSTALL_DIR") or DEFAULT_INSTALL_DIR
    os.makedirs(install_dir, exist_ok=True)

    if info["kind"] == "transformers":
        ok, result = _install_transformers_model(requested, install_dir)
    else:
        ok, result = _install_acestep(requested, install_dir)

    if not ok:
        print(f"설치 실패: {result}")
        sys.exit(1)

    venv_python = result
    cfg["INSTALLED_MODEL"] = requested
    cfg["MODEL"] = requested
    cfg["INSTALL_DIR"] = install_dir
    cfg["VENV_PYTHON"] = venv_python
    cfg["INSTALL_KIND"] = info["kind"]
    cfg["HF_ID"] = info["hf_id"]
    cfg["INSTALLED_AT"] = time.strftime("%Y-%m-%d %H:%M:%S")
    if info["kind"] == "acestep":
        cfg["ACE_STEP_DIR"] = os.path.join(install_dir, "ace-step")
    _save_config(cfg)

    print()
    print("=" * 50)
    print(f"🎵 음악 스튜디오 설치 완료!")
    print("=" * 50)
    print()
    print(f"✅ 무엇이 설치되었나요?")
    print(f"   - 모델:   {info['label']}")
    print(f"   - 위치:   {install_dir}")
    print(f"   - 디스크: ~{info['disk_gb']}GB 사용 중")
    print()
    print(f"🚀 이제 무엇을 할 수 있나요?")
    print(f"   - 'music_generate.py' 실행 -> 30초 BGM 생성")
    print(f"   - 'music_to_video.py' 실행 -> 영상에 BGM 합성")
    print()
    print(f"💡 (모델을 변경하려면 MODEL 설정을 바꾸고 다시 실행하세요)")
    print()
    print(f"ℹ️ (로그에 'WARNING / UNEXPECTED'가 보여도 무시해도 됩니다.)")
    print(f"   transformers 라이브러리 내부 메시지입니다. 설치는 정상 완료.")


if __name__ == "__main__":
    main()
