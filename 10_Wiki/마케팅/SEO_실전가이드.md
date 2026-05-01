# SEO 실전 가이드

> 검색 엔진 최적화의 핵심 전략과 실행 방법

## 🔍 SEO 3대 축

### 1. 기술적 SEO (Technical SEO)
- **사이트맵**: `sitemap.xml` 자동 생성 → Google Search Console 제출
- **robots.txt**: 크롤링 허용/차단 규칙 설정
- **구조화 데이터**: Schema.org JSON-LD로 리치 스니펫 확보
- **Core Web Vitals**: LCP < 2.5초, INP < 200ms, CLS < 0.1
- **모바일 우선 인덱싱**: 모바일 버전이 데스크톱보다 우선

```html
<!-- 기본 메타 태그 -->
<title>핵심키워드 | 브랜드명</title>
<meta name="description" content="155자 이내의 매력적인 설명 + CTA">

<!-- Open Graph -->
<meta property="og:title" content="공유 시 표시될 제목">
<meta property="og:image" content="1200x630px 이미지 URL">

<!-- 구조화 데이터 -->
<script type="application/ld+json">
{ "@context": "https://schema.org", "@type": "WebApplication", ... }
</script>
```

### 2. 콘텐츠 SEO
- **키워드 리서치**: Google Keyword Planner, 네이버 키워드 도구
- **롱테일 키워드**: 경쟁 낮은 3~4단어 조합 공략
- **검색 의도 매칭**: 정보형(블로그), 거래형(랜딩페이지), 탐색형(비교글)
- **콘텐츠 구조**: H1(1개) → H2(3~5개) → H3(세부) 계층화
- **첫 100자**: 핵심 키워드 자연스럽게 포함

### 3. 오프페이지 SEO
- **백링크**: 관련 분야 사이트에서의 링크 확보
- **SNS 시그널**: 콘텐츠 공유로 간접적 영향
- **브랜드 검색량**: 직접 검색 늘리기 (콘텐츠 마케팅)

## 🤖 GEO (Generative Engine Optimization)
AI 검색엔진(Gemini, ChatGPT Search 등)에 최적화하는 전략
- **명확한 Q&A 구조**: 질문-답변 형식으로 콘텐츠 작성
- **인용 가능한 데이터**: 구체적 수치, 표, 목록 포함
- **전문성 신호**: 저자 정보, 참고 문헌, 업데이트 날짜 명시
- **구조화 데이터**: FAQ, HowTo, Product 스키마 적극 활용

## 📊 측정 도구
| 도구 | 용도 | 비용 |
|------|------|------|
| Google Search Console | 검색 성과, 인덱싱 | 무료 |
| Google Analytics 4 | 트래픽 분석 | 무료 |
| Lighthouse | 기술 성능 점검 | 무료 |
| Ahrefs/SEMrush | 키워드/백링크 분석 | 유료 |

---
*Tags: #SEO #검색최적화 #GEO #마케팅*
