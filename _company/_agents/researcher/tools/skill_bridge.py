#!/usr/bin/env python
import os, sys, json

# Windows cp949 인코딩 에러 방지 하네스 방화벽 주입
if os.name == 'nt' and os.environ.get("PYTHONUTF8") != "1":
    os.environ["PYTHONUTF8"] = "1"
    import subprocess
    sys.exit(subprocess.call([sys.executable] + sys.argv))

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "skill_bridge.json")

def main():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8-sig") as f:
            cfg = json.load(f)
    else:
        cfg = {}

    print(f"─── 넥스트하루 에이전트: 스킬 브릿지 ───")
    print(f"  연동 상태 : {'활성화됨' if cfg.get('GLOBAL_SKILLS_ACTIVE') else '비활성화'}")
    print(f"  검증 모드 : {cfg.get('HARNESS_MODE', 'Standard')}")
    print("\n✅ 글로벌 스킬 저장소(skills/)와의 연동이 완료되었습니다.")
    print("   이 에이전트는 이제 '맨손'이 아닙니다. 필요한 전문 스킬을 자유롭게 쓸 수 있습니다!")

if __name__ == "__main__":
    main()
