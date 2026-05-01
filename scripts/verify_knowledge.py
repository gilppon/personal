#!/usr/bin/env python3
"""
🛡️ 넥스트하루 지식 엔진 검증 하네스 (Knowledge Verification Harness)
---
위키 문서의 무결성, decisions.md와의 정합성, 구조적 건전성을 검사합니다.
사용법: python scripts/verify_knowledge.py
"""

import os
import json
import sys
import io
from pathlib import Path

# === Windows 콘솔 UTF-8 강제 설정 ===
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# === 경로 설정 ===
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
WIKI_DIR = PROJECT_ROOT / "10_Wiki"
SHARED_DIR = PROJECT_ROOT / "_shared"
AGENTS_DIR = PROJECT_ROOT / "_agents"
STATE_FILE = PROJECT_ROOT / "company_state.json"
DECISIONS_FILE = SHARED_DIR / "decisions.md"
LEARNING_LOG = SHARED_DIR / "learning_log.md"
SYSTEM_FILE = SHARED_DIR / "_system.md"

# === 결과 수집기 ===
class VerificationResult:
    def __init__(self):
        self.passed = []
        self.warnings = []
        self.errors = []

    def ok(self, msg):
        self.passed.append(msg)
        print(f"  ✅ {msg}")

    def warn(self, msg):
        self.warnings.append(msg)
        print(f"  ⚠️  {msg}")

    def fail(self, msg):
        self.errors.append(msg)
        print(f"  ❌ {msg}")

    def summary(self):
        total = len(self.passed) + len(self.warnings) + len(self.errors)
        print("\n" + "=" * 60)
        print(f"📊 검증 결과: {total}건 검사 완료")
        print(f"  ✅ 통과: {len(self.passed)}건")
        print(f"  ⚠️  경고: {len(self.warnings)}건")
        print(f"  ❌ 실패: {len(self.errors)}건")
        print("=" * 60)
        return len(self.errors) == 0


# === 검증 1: 위키 구조 검사 ===
def check_wiki_structure(result: VerificationResult):
    print("\n🔍 [1/5] 위키 디렉토리 구조 검사...")
    
    required_dirs = ["개발", "디자인", "마케팅", "비즈니스", "보안", "운영"]
    
    if not WIKI_DIR.exists():
        result.fail("10_Wiki/ 디렉토리가 존재하지 않습니다!")
        return
    
    for dirname in required_dirs:
        dirpath = WIKI_DIR / dirname
        if dirpath.exists() and dirpath.is_dir():
            md_files = list(dirpath.glob("*.md"))
            if md_files:
                result.ok(f"10_Wiki/{dirname}/ — {len(md_files)}개 문서 확인")
            else:
                result.warn(f"10_Wiki/{dirname}/ — 디렉토리는 있지만 문서가 비어있음")
        else:
            result.fail(f"10_Wiki/{dirname}/ 디렉토리가 존재하지 않습니다!")


# === 검증 2: 위키 문서 품질 검사 ===
def check_wiki_quality(result: VerificationResult):
    print("\n🔍 [2/5] 위키 문서 품질 검사...")
    
    if not WIKI_DIR.exists():
        result.fail("10_Wiki/ 디렉토리 없음 — 품질 검사 건너뜀")
        return
    
    for md_file in sorted(WIKI_DIR.rglob("*.md")):
        rel_path = md_file.relative_to(PROJECT_ROOT)
        content = md_file.read_text(encoding="utf-8")
        lines = content.strip().split("\n")
        
        # H1 헤더 존재 여부
        has_h1 = any(line.startswith("# ") for line in lines)
        # 최소 길이 (100자 이상)
        is_substantial = len(content) >= 100
        # 빈 파일 체크
        is_empty = len(content.strip()) == 0
        
        if is_empty:
            result.fail(f"{rel_path} — 빈 파일입니다!")
        elif not has_h1:
            result.warn(f"{rel_path} — H1(#) 헤더가 없습니다")
        elif not is_substantial:
            result.warn(f"{rel_path} — 내용이 너무 짧습니다 ({len(content)}자)")
        else:
            result.ok(f"{rel_path} — 정상 ({len(content)}자, H1 있음)")


# === 검증 3: 공유 메모리 무결성 ===
def check_shared_memory(result: VerificationResult):
    print("\n🔍 [3/5] 공유 메모리(_shared/) 무결성 검사...")
    
    required_files = {
        "_system.md": "시스템 지침",
        "decisions.md": "의사결정 로그",
        "goals.md": "목표",
        "identity.md": "정체성",
        "learning_log.md": "학습 기록"
    }
    
    for filename, description in required_files.items():
        filepath = SHARED_DIR / filename
        if filepath.exists():
            size = filepath.stat().st_size
            if size > 0:
                result.ok(f"_shared/{filename} ({description}) — {size}bytes")
            else:
                result.fail(f"_shared/{filename} ({description}) — 빈 파일!")
        else:
            result.fail(f"_shared/{filename} ({description}) — 파일 없음!")
    
    # PTR 프로토콜 존재 확인
    if SYSTEM_FILE.exists():
        content = SYSTEM_FILE.read_text(encoding="utf-8")
        if "Post-Task Review" in content or "PTR" in content:
            result.ok("_system.md에 PTR 프로토콜 확인됨")
        else:
            result.warn("_system.md에 PTR 프로토콜이 없습니다 — 지식 환류 불가!")


# === 검증 4: company_state.json 스키마 검사 ===
def check_company_state(result: VerificationResult):
    print("\n🔍 [4/5] company_state.json 스키마 검사...")
    
    if not STATE_FILE.exists():
        result.fail("company_state.json 파일이 존재하지 않습니다!")
        return
    
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
    except json.JSONDecodeError as e:
        result.fail(f"company_state.json JSON 파싱 실패: {e}")
        return
    
    result.ok("JSON 파싱 성공")
    
    # 필수 필드 검사
    required_fields = ["foundedAt", "tasksCompleted", "knowledgeInjected"]
    for field in required_fields:
        if field in state:
            result.ok(f"필수 필드 '{field}' 존재 — 값: {state[field]}")
        else:
            result.fail(f"필수 필드 '{field}' 누락!")
    
    # knowledge_stats 존재 여부
    if "knowledge_stats" in state:
        stats = state["knowledge_stats"]
        if "분야별" in stats:
            for area, info in stats["분야별"].items():
                level = info.get("레벨", 0)
                docs = info.get("문서수", 0)
                result.ok(f"분야 '{area}' — Lv.{level}, {docs}개 문서")
        else:
            result.warn("knowledge_stats에 '분야별' 필드가 없습니다")
    else:
        result.warn("knowledge_stats 필드 없음 — 지식 레벨 추적 불가!")
    
    # learning_loop 존재 여부
    if "learning_loop" in state:
        loop = state["learning_loop"]
        ptr_status = loop.get("PTR_프로토콜", "unknown")
        result.ok(f"학습 루프 상태: PTR={ptr_status}")
    else:
        result.warn("learning_loop 필드 없음 — 학습 루프 상태 추적 불가!")


# === 검증 5: 에이전트 프롬프트 검사 ===
def check_agent_prompts(result: VerificationResult):
    print("\n🔍 [5/5] 에이전트 프롬프트 검사...")
    
    if not AGENTS_DIR.exists():
        result.fail("_agents/ 디렉토리가 존재하지 않습니다!")
        return
    
    expected_agents = [
        "ceo", "developer", "designer", "business",
        "youtube", "instagram", "writer", "editor",
        "secretary", "researcher"
    ]
    
    for agent in expected_agents:
        prompt_file = AGENTS_DIR / agent / "prompt.md"
        if prompt_file.exists():
            content = prompt_file.read_text(encoding="utf-8")
            if len(content) >= 200:
                result.ok(f"_agents/{agent}/prompt.md — {len(content)}자 (지식 주입 확인)")
            else:
                result.warn(f"_agents/{agent}/prompt.md — 내용이 부족합니다 ({len(content)}자)")
        else:
            result.fail(f"_agents/{agent}/prompt.md — 파일 없음!")


# === 메인 실행 ===
def main():
    print("=" * 60)
    print("🧠 넥스트하루 지식 엔진 검증 하네스 v1.0")
    print(f"   프로젝트 루트: {PROJECT_ROOT}")
    print("=" * 60)
    
    result = VerificationResult()
    
    check_wiki_structure(result)
    check_wiki_quality(result)
    check_shared_memory(result)
    check_company_state(result)
    check_agent_prompts(result)
    
    all_passed = result.summary()
    
    if all_passed:
        print("\n🎉 전체 검증 통과! 지식 엔진이 정상 가동 중입니다.")
    else:
        print("\n🚨 일부 검증 실패! 위의 ❌ 항목을 확인하세요.")
    
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
