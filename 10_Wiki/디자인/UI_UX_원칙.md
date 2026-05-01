# UI/UX 디자인 원칙

> 넥스트하루 프로젝트에 적용하는 UI/UX 핵심 원칙

## 🎯 10가지 핵심 원칙

### 1. 일관성 (Consistency)
- 동일 기능은 동일 UI 패턴 사용
- 컬러, 폰트, 간격, 아이콘 스타일 통일

### 2. 피드백 (Feedback)
- 모든 사용자 액션에 즉각적 반응 (로딩, 성공, 에러)
- 버튼 클릭 → 시각적 변화 (0.1초 이내)

### 3. 가시성 (Visibility)
- 현재 상태를 사용자에게 항상 표시
- 비활성 버튼, 로딩 스피너, 진행률 표시

### 4. 여유 (Affordance)
- 클릭 가능한 요소는 클릭 가능하게 보여야 함
- 호버 효과, 커서 변경, 그림자 활용

### 5. 오류 방지 (Error Prevention)
- 위험한 행동 전 확인 모달
- 폼 실시간 유효성 검사
- 되돌리기(Undo) 기능 제공

### 6. 단순함 (Simplicity)
- 한 화면에 하나의 주요 목적
- 선택지는 3~5개 이하
- Progressive Disclosure: 필요할 때만 상세 정보 노출

### 7. 접근성 (Accessibility)
- 색상 대비 4.5:1 이상 (WCAG AA)
- 키보드 네비게이션 지원
- aria-label 적용

### 8. 반응형 (Responsive)
- 모바일 퍼스트 설계
- 브레이크포인트: 375px / 768px / 1280px
- 터치 타겟: 최소 44x44px

### 9. 성능 UX
- 스켈레톤 UI로 로딩 인지 개선
- 낙관적 업데이트 (Optimistic Update)
- 50ms 이내 상호작용 응답

### 10. 감정 디자인 (Emotional Design)
- 빈 상태(Empty State)에 유용한 안내
- 성공 시 축하 애니메이션
- 에러 메시지는 해결책 포함

## 🎨 컬러 시스템 구축법
```css
:root {
  /* Primary - HSL 기반으로 변형 용이 */
  --primary-50: hsl(220, 80%, 95%);
  --primary-100: hsl(220, 80%, 90%);
  --primary-500: hsl(220, 80%, 50%);  /* 메인 */
  --primary-900: hsl(220, 80%, 15%);

  /* Semantic */
  --success: hsl(145, 63%, 42%);
  --warning: hsl(38, 92%, 50%);
  --error: hsl(0, 72%, 51%);

  /* Neutral (다크모드 기준) */
  --bg-primary: hsl(220, 20%, 8%);
  --bg-secondary: hsl(220, 20%, 12%);
  --text-primary: hsl(220, 10%, 95%);
  --text-secondary: hsl(220, 10%, 60%);
}
```

## 📐 간격 시스템 (8px Grid)
| 토큰 | 값 | 용도 |
|------|-----|------|
| xs | 4px | 아이콘 내부 |
| sm | 8px | 요소 간 최소 간격 |
| md | 16px | 카드 패딩 |
| lg | 24px | 섹션 간 간격 |
| xl | 32px | 페이지 여백 |
| 2xl | 48px | 대형 섹션 간격 |

---
*Tags: #UI #UX #디자인원칙 #컬러시스템*
