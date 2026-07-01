---
status: active
priority: high
category: Technology
review_cycle: quarterly
last_verified: 2026-07-01
next_review: 2026-10-01
monitoring_method: manual
official_url: https://www.unrealengine.com
careers_url:
tech_blog:
github: https://github.com/EpicGames
linkedin:
newsletter:
rss:
related_notes: "[[01_대시보드]], [[05_버추얼_프로덕션_생태계]]"
---

# 언리얼 엔진 및 OpenUSD (Unreal Engine & OpenUSD)

이 문서는 실시간 가상 프로덕션 핵심 엔진인 **Unreal Engine 5**와 데이터 상호 호환 파이프라인의 산업 표준인 **OpenUSD(Universal Scene Description)** 기술군에 대한 서칭 쿼리, 역량 빌드업 가이드라인을 정의합니다.

---

## 1. 기술적 용도 및 상호 작용 (Technical Summary)

* **Unreal Engine 5**:
  - nDisplay 분산 렌더링 클러스터 인프라를 활용하여 온셋 LED Wall 가상 배경을 실시간 카메라 위치와 연동해 최적화 투사하는 중심 엔진.
* **OpenUSD**:
  - Pixar에서 주도하고 오토데스크, 에픽게임즈 등이 참여하는 Universal Scene Description.
  - Maya, Houdini, Unreal Engine 간의 대용량 에셋 데이터를 레이어와 베리언트 구조로 깨짐 없이 교환할 수 있는 파이프라인 표준 규격.

---

## 2. 채용 서칭 쿼리 및 검색 전략 (Search Queries)

채용 플랫폼(원티드, 링크드인, 점핏) 검색 시 활용하는 정밀 검색 식입니다.

### 1. Unreal Engine TD / 엔지니어 쿼리
- **사람인 / 원티드**:
  - `(언리얼 OR Unreal) AND (C++ OR nDisplay OR 렌더링 OR 쉐이더)`
- **LinkedIn (글로벌)**:
  - `"Unreal Engine Developer" AND ("C++" OR "nDisplay" OR "Virtual Production")`

### 2. Pipeline TD / OpenUSD 쿼리
- **원티드 / 점핏**:
  - `(파이프라인 OR TD) AND (USD OR OpenUSD OR Python OR Maya)`
- **LinkedIn (글로벌)**:
  - `"Pipeline TD" AND ("USD" OR "Universal Scene Description" OR "Python")`

---

## 3. 핵심 리소스 및 필수 학습 경로 (Learning Roadmap)

### 1. Unreal Engine R&D 학습 주제
* **나나이트(Nanite) 및 루멘(Lumen) 최적화**: 
  - 버추얼 프로덕션 특성상 실시간 60fps 이상이 보장되어야 하므로 가상 공간 최적화 기법 마스터.
* **nDisplay 구성 실무**:
  - 다중 렌더링 서버 노드 설정 및 동기화 기술.
* **C++ API 제어**:
  - 엔진 내부 소스코드를 디버깅하고 렌더 파이프라인(RHI) 커스텀 확장 제작 능력 개발.

### 2. OpenUSD 파이프라인 학습 주제
* **USD 파일 구조**:
  - `.usda`(텍스트 포맷), `.usdc`(바이너리 포맷), `.usdz`(압축 패키지) 분석.
* **컴포지션 아크(Composition Arcs)**:
  - Sublayers, References, Payloads, Variants 구성 요소를 Python API로 제어하는 자동화 툴 빌드.
* **Hydra 렌더 델리게이트(Hydra Render Delegate)**:
  - Unreal Engine 내부에 USD 렌더러를 연동하고 데이터를 뷰포트에 효율적으로 밀어넣는 구조 이해.

---

## 4. 포트폴리오 적용 및 검증 방안 (Portfolio Actions)

- [ ] **1. nDisplay 다중 노드 렌더링 시뮬레이션**: 로컬 PC에 가상 가상 환경을 구축하고 nDisplay 설정으로 프레임 락이 제대로 유지되는지 모니터링 수행.
- [ ] **2. Maya-Houdini-Unreal USD 파이프라인 셋업**: 오픈소스 USD 자원을 가공하여 씬 조립 툴을 Python으로 자동 생성하고 에셋이 엔진으로 자동 이전되는 툴체인 구현 및 GitHub 업로드.
