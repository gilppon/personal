# Harness Engineering for Developers (2026)

## ⚡ 정밀 타격 코딩 (Precision Coding)
- **PEV Pattern 필수:** 
  1. **Plan:** `implementation_plan.md`를 통해 설계를 먼저 제안합니다.
  2. **Execute:** `TargetContent`와 `ReplacementContent`를 사용하여 파일의 최소 영역만 수정합니다.
  3. **Verify:** `verify.py` 또는 유닛 테스트를 통해 변경 사항을 실사 확인합니다.

## 🔗 MCP 및 컨텍스트 최적화
- **Standardized Tools:** MCP 서버를 활용하여 외부 API나 DB에 정밀하게 접근합니다.
- **Context Firewall:** 불필요한 파일 스캔을 지양하고, 필요한 파일의 특정 라인만 로드하여 컨텍스트 창을 보호합니다.

## 🛡️ 하드 바운더리 (Hard Boundaries)
- 설정 파일(`.config`, `package.json` 등) 수정 전 반드시 CEO(사용자)의 승인을 받습니다.
- Lint 에러 발생 시 즉각 중단하고 해결책을 먼저 보고합니다.
