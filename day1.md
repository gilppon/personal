제공해주신 자료인 **"트랜스포머를 활용한 자연어 처리(Natural Language Processing with Transformers)"** 도서를 바탕으로, 지식 관리 도구(Obsidian, Notion, Logseq 등)에 바로 저장할 수 있는 마크다운 형식의 요약 노트를 만들어 드립니다.

---

# [지식 노트] 트랜스포머를 활용한 자연어 처리 (Hugging Face)

## 📌 개요
- **도서명:** Natural Language Processing with Transformers (트랜스포머를 활용한 자연어 처리)
- **저자:** Lewis Tunstall, Leandro von Werra, Thomas Wolf (Hugging Face 팀)
- **핵심 주제:** Hugging Face 생태계를 활용하여 실무 수준의 NLP 애플리케이션을 구축하는 방법

---

## 🏗️ 1. 트랜스포머(Transformers) 아키텍처 핵심
트랜스포머는 기존 RNN의 순차적 처리 한계를 극복하고 **Self-Attention** 메커니즘을 통해 문장 내 단어 간의 관계를 병렬로 학습합니다.

- **인코더(Encoder):** 문장의 맥락을 이해하고 수치적 표현(임베딩)으로 변환 (예: BERT, RoBERTa).
- **디코더(Decoder):** 주어진 입력을 바탕으로 다음 토큰을 생성 (예: GPT 시리즈).
- **인코더-디코더(Encoder-Decoder):** 복잡한 매핑 작업에 사용 (예: T5, BART - 기계 번역, 요약).

---

## 🛠️ 2. Hugging Face 주요 라이브러리
이 책에서 다루는 핵심 도구 모음입니다.

1.  **Datasets:** 대규모 데이터셋을 효율적으로 로드하고 처리. `Apache Arrow` 형식을 사용하여 메모리 효율 극대화.
2.  **Tokenizers:** 텍스트를 모델이 이해할 수 있는 숫자(ID)로 변환. WordPiece, BPE, Unigram 등 다양한 알고리즘 지원.
3.  **Transformers:** 사전 학습된(Pre-trained) 모델을 로드하고 미세 조정(Fine-tuning)하는 핵심 라이브러리.
4.  **Accelerate:** 동일한 코드로 CPU, GPU, TPU 환경에서 모델을 학습할 수 있게 지원.

---

## 🚀 3. 주요 NLP 작업(Tasks) 및 워크플로우
책에서 다루는 주요 실습 내용입니다.

- **텍스트 분류 (Classification):** 감성 분석 등 문장 전체의 의미 파악.
- **개체명 인식 (NER):** 문장에서 이름, 장소, 조직 등 특정 정보 추출.
- **질의응답 (QA):** 주어진 본문에서 질문에 대한 답을 찾아내거나 생성.
- **텍스트 요약 (Summarization):** 긴 본문을 핵심 내용 위주로 축약.
- **언어 모델링 (Text Generation):** 문맥에 이어질 자연스러운 텍스트 생성.

---

## ⚡ 4. 모델 성능 및 최적화
실무 배포를 위한 모델 경량화 기법을 다룹니다.

- **지식 증류 (Knowledge Distillation):** 큰 모델(Teacher)의 지식을 작은 모델(Student)에게 전달 (예: DistilBERT).
- **양자화 (Quantization):** 가중치의 정밀도를 낮추어(예: FP32 → INT8) 추론 속도 향상 및 메모리 절약.
- **가지치기 (Pruning):** 모델의 중요도가 낮은 가중치를 제거하여 크기 축소.

---

## 💡 주요 인사이트
- **전이 학습(Transfer Learning):** 대규모 말뭉치로 사전 학습된 모델을 특정 도메인 데이터로 미세 조정하는 것이 현대 NLP의 표준 워크플로우임.
- **Zero-shot Transfer:** 다국어 모델(XLM-R 등)을 활용하면 한 언어로 학습한 모델을 다른 언어에도 바로 적용해 볼 수 있음.

---

## 🔗 참고 자료
- **Hugging Face Hub:** [huggingface.co](https://huggingface.co)
- **관련 소스 코드:** 책에서 제공하는 GitHub 리포지토리 활용 권장.

---
*Created on: 2024-05-23*
*Tags: #NLP #Transformers #HuggingFace #DeepLearning #TIL*