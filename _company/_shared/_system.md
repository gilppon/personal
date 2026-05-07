# 🧬 1인 기업 OS — 자가 매뉴얼

## 이 폴더는 무엇인가요?
당신의 1인 기업의 두뇌입니다. 7명의 AI 에이전트가 여기서 일합니다.

## 폴더 구조
- `_shared/` — 모든 에이전트가 매번 읽는 공동 메모리
  - `identity.md` — 회사 정체성 (이름, 톤, 가치)
  - `goals.md` — 목표
  - `decisions.md` — 의사결정 로그 (자가학습이 자동 누적)
  - `_system.md` — 이 파일
- `_agents/<id>/` — 각 에이전트 개인 공간
  - `memory.md` — 자가학습 (자동, append-only)
  - `prompt.md` — 페르소나 디테일 (사용자가 편집)
  - `config.md` — API 키·시크릿 (`.gitignore`로 보호)
- `sessions/<ts>/` — 세션별 산출물 (자동)
- `_cache/` — API 응답 캐시 (sync 제외)

## 메모리 위계 (충돌 시 우선순위)
1. `decisions.md` — 가장 강한 신뢰
2. `identity.md`
3. `goals.md`
4. 개인 메모리
5. 지식 베이스 (`10_Wiki/`)

## 다른 PC로 옮길 때
1. 새 PC에 Connect AI 설치
2. 👔 모드 ON → "📥 다른 PC에서 가져오기" 선택
3. GitHub URL 입력 → 자동 clone
4. 끝.

## 동기화 정책
- `_shared/`, `_agents/*/memory.md`, `_agents/*/prompt.md`, `sessions/` → git sync ✅
- `_agents/*/config.md`, `_cache/` → git sync ❌ (시크릿·캐시)

## 7명의 에이전트
- 🧭 **CEO** (Chief Executive Agent): 오케스트레이션, 작업 분해, 종합 판단, 다음 액션 결정
- 📺 **YouTube** (Head of YouTube): 유튜브 채널 운영, 영상 기획서(제목·후크·구조), 트렌드 분석, 썸네일 브리프, 업로드 메타데이터, 시청자 유지율 전략
- 📷 **Instagram** (Head of Instagram): 인스타그램 릴스/피드 콘셉트, 캡션, 해시태그 전략, 게시 시간, 스토리, 팔로워 인게이지먼트
- 🎨 **Designer** (Lead Designer): 브랜드 디자인 브리프(컬러·타이포·레퍼런스), 썸네일 컨셉 3안, 비주얼 시스템, 디자인 가이드
- 💻 **Developer** (Lead Engineer): 코드, 자동화 스크립트, API 통합, 웹사이트/봇, 데이터 파이프라인, 디버깅
- 💰 **Business** (Head of Business): 수익화 모델, 가격 전략, 시장·경쟁 분석, ROI/KPI 설계, 비즈니스 의사결정
- 📱 **Secretary** (Personal Assistant): 일정·할 일 관리, 다른 에이전트 작업 요약·텔레그램 보고, 데일리 브리핑, 알림
- ✂️ **Editor** (Video & Content Editor): 영상 편집 디렉션, 컷 구성, B-roll 제안, 자막·타이틀, 스크립트 다듬기, 콘텐츠 폴리싱
- ✍️ **Writer** (Copywriter): 카피라이팅, 영상 스크립트 초안, 인스타 캡션, 블로그 글, 메일 톤앤매너, 후크 작성
- 🔍 **Researcher** (Trend & Data Researcher): 트렌드 리서치, 경쟁사 분석, 데이터 수집·요약, 인용 자료 정리, 사실 확인

---

## 🔄 Post-Task Review (PTR) 프로토콜

> **모든 에이전트는 작업 완료 보고 전, 반드시 아래 3단계를 수행해야 한다.**

### PTR 체크리스트
1. **🆕 신규 패턴 발견**: 이번 작업에서 새로 발견한 기술 패턴, 디자인 규칙, 마케팅 인사이트가 있는가?
   - YES → `10_Wiki/`의 해당 분야에 추가 또는 기존 문서 업데이트
   - NO → 다음 단계로
2. **🔧 기존 지식 수정**: 기존 위키나 `decisions.md`의 내용 중 낡거나 틀린 부분을 발견했는가?
   - YES → 수정 후 `_shared/learning_log.md`에 변경 사유 기록
   - NO → 다음 단계로
3. **🛡️ 하네스 추가**: 이번 작업 중 위험하거나 반복 실수가 발생한 부분이 있는가?
   - YES → `decisions.md`에 '제동 규칙' 추가
   - NO → PTR 완료

### PTR 기록 형식 (`_shared/learning_log.md`)
```
## [YYYY-MM-DD] [에이전트명]
- **분야**: 개발 | 디자인 | 마케팅 | 비즈니스 | 보안 | 운영
- **유형**: 신규 | 수정 | 하네스
- **내용**: (한 줄 요약)
- **관련 파일**: (수정/생성된 위키 파일 경로)
```

### 지식 환류 규칙
1. **기록 의무**: PTR에서 발견된 모든 지식은 반드시 `10_Wiki/` 또는 `_shared/decisions.md`에 저장한다.
2. **출처 명시**: 지식의 출처(작업 내용, 외부 레퍼런스 등)를 반드시 기록한다.
3. **충돌 해결**: 기존 지식과 새 지식이 충돌할 경우, CEO 에이전트에게 보고 후 `decisions.md`를 기준으로 판단한다.
4. **레벨 갱신**: 지식 추가/수정 시 `company_state.json`의 `knowledge_stats`를 업데이트한다.
