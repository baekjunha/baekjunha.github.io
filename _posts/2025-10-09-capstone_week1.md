---
published: true
title: "살아있는 AI 캐릭터 구현 가이드(1)"
categories: capstone
tags: [capstone, ai, unity, guide]
date: 2025-09-29 17:11:43 +0900
toc: true
toc_sticky: true
author_profile: false
use_math: true 
thumbnail: https://mastermixmovies.wordpress.com/wp-content/uploads/2017/10/2001.gif?w=1241&h=546
---

## 1주차 AI 사회관계 시뮬레이션: 프로덕션급 비동기 통신 코어 구축 마스터 가이드
---


### 서론: 단순한 시작을 넘어 - 살아 숨 쉬는 AI를 위한 기술적 초석 다지기

[cite_start]본 1주차 구현 가이드는 **'기억을 가진 살아 숨 쉬는 AI 캐릭터'**라는 프로젝트의 핵심 철학을 현실로 구현하기 위한 첫 번째이자 가장 중요한 단계에 집중합니다[cite: 4]. [cite_start]1주차의 기술적 과제들은 단순히 프로젝트를 시작하는 준비 단계를 넘어, 플레이어가 AI 캐릭터와 맺는 유대감의 기반이 되는 **'환상'을 공학적으로 창조하는 과정**입니다[cite: 5].

[cite_start]프로젝트의 궁극적인 성공은 플레이어가 AI 캐릭터를 살아있는 존재로 인식하는 **몰입감**에 달려 있으며 [cite: 6][cite_start], 이 몰입감은 아주 작은 기술적 결함만으로도 산산조각 날 수 있습니다[cite: 7]. [cite_start]PC 플랫폼에서는 화면 찢어짐(screen tearing), 불안정한 프레임률, 거친 폴리곤 가장자리(aliasing)와 같은 시각적 결함이 몰입을 해치는 치명적인 요소로 작용합니다[cite: 8]. [cite_start]플레이어는 기술적 한계가 느껴지는 캐릭터와 깊은 유대감을 형성할 수 없습니다[cite: 9].

[cite_start]따라서 이번 주에 구축할 **안정적이고, 반응성이 뛰어나며, 막힘없는(Non-blocking) 통신 계층**은 프로젝트의 예술적, 경험적 목표를 달성하기 위한 기술적 전제 조건입니다[cite: 10]. [cite_start]이와 동시에, PC의 강력한 하드웨어 성능을 십분 활용하여 **시각적 완성도를 극대화**하는 것은 감성적 핵심을 지탱하는 또 다른 기반이 됩니다[cite: 11].

---

### 섹션 1: 프로젝트 초기화 및 의존성 구성 (PC 플랫폼 최적화)

[cite_start]모든 후속 작업을 위한 안정적이고 올바른 기반을 마련하기 위해 Unity 프로젝트를 준비하는 첫 단계를 안내합니다[cite: 15]. [cite_start]PC 프로젝트는 모바일과 달리 초기 아키텍처 결정이 프로젝트의 시각적 한계와 개발 방향성 전체를 규정하므로 신중을 기해야 합니다[cite: 17].

#### 1.1. Unity 환경 기준선 설정
* [cite_start]**권장 버전:** **Unity 2022.3.x LTS** (Long-Term Support) 버전 사용을 권장합니다[cite: 19]. [cite_start]LTS 릴리스는 장기간에 걸쳐 안정성이 검증되었으므로 프로덕션 수준의 프로젝트에 가장 적합합니다[cite: 20].

#### 1.2. 대상 플랫폼 구성: PC, Mac & Linux Standalone
* [cite_start]**빌드 대상:** Unity 에디터에서 `File > Build Settings`로 이동하여 Platform 목록에서 **PC, Mac & Linux Standalone**를 선택합니다[cite: 25, 22]. [cite_start]이는 데스크톱 클래스의 CPU와 GPU 성능을 온전히 활용할 수 있도록 하는 선언과 같습니다[cite: 23, 24].
* [cite_start]**Architecture:** **x86_64**를 선택합니다[cite: 28]. [cite_start]이는 현대 PC 게임의 표준인 64비트 시스템을 대상으로 빌드하겠다는 의미입니다[cite: 28, 29].

#### 1.3. 핵심 아키텍처 결정: 렌더 파이프라인 선택 (URP vs. HDRP)
[cite_start]스크립터블 렌더 파이프라인(SRP) 선택은 프로젝트의 시각적 품질의 상한선과 개발 워크플로우 전체를 결정하는, **되돌리기 어려운 중요한 결정**입니다[cite: 32, 33]. [cite_start]두 파이프라인(URP와 HDRP)은 셰이더와 재질 시스템이 근본적으로 달라 프로젝트가 진행된 후에 변경하는 것은 막대한 비용을 초래할 수 있습니다[cite: 35, 36].

| 비교 기준 | Universal Render Pipeline (URP) | High Definition Render Pipeline (HDRP) | AI 시뮬레이션을 위한 전략적 고려사항 |
| :--- | :--- | :--- | :--- |
| **대상 하드웨어** | [cite_start]저사양부터 고사양 PC까지 폭넓게 지원 [cite: 46] | [cite_start]중-고사양 PC 및 최신 콘솔 [cite: 46] | [cite_start]더 많은 사용자를 포용하려면 URP가 유리[cite: 46]. |
| **시각적 충실도** | [cite_start]우수하지만, 사실주의보다는 양식화된 스타일에 강점 [cite: 46, 47] | **최상급**. [cite_start]사실적인 조명과 재질 표현에 특화 [cite: 42, 46, 47] | [cite_start]HDRP의 사실적인 렌더링은 AI 캐릭터를 **'실존하는 인물'처럼 느끼게 하는 데 결정적인 역할**을 할 수 있습니다[cite: 47]. |
| **고급 조명/효과** | [cite_start]기본적인 볼류메트릭, 후처리 효과 제공 [cite: 47] | [cite_start]볼류메트릭 안개/조명, 고급 반사, 물리 기반 하늘 등 **내장** [cite: 43, 47] | [cite_start]대화 장면의 분위기를 빛과 대기로 연출하는 데 **HDRP가 압도적으로 유리**합니다[cite: 47]. |
| **성능 오버헤드** | [cite_start]상대적으로 낮음 [cite: 47] | **높음**. [cite_start]최적화를 위해 더 많은 노력 필요 [cite: 44, 47] | [cite_start]URP는 안정적인 60 FPS 이상을 유지하기 용이합니다[cite: 47]. |

#### 1.4. 고품질 그래픽을 위한 초기 프로젝트 설정
* [cite_start]**컬러 스페이스 (Color Space):** `Edit > Project Settings > Player > Other Settings`에서 Color Space를 **Linear**로 설정합니다[cite: 50]. [cite_start]Linear 컬러 스페이스는 조명 계산을 물리적으로 정확하게 만들어 URP와 HDRP 모두에서 훨씬 더 사실적이고 일관된 결과를 보장합니다[cite: 51].
* [cite_start]**품질 설정 (Quality Settings):** `Edit > Project Settings > Quality`로 이동하여 기본 품질 수준을 **'High' 또는 'Ultra'** 프리셋으로 설정하는 것이 PC 개발을 위한 좋은 출발점입니다[cite: 54, 55].

#### 1.5. 비동기 처리의 핵심, UniTask 통합
[cite_start]본 프로젝트는 C#의 `async/await` 패턴을 전면적으로 채택하며, 이를 위해 **UniTask** 라이브러리를 도입합니다[cite: 57]. [cite_start]UniTask는 Unity 환경에 최적화된 **제로-할당 비동기 솔루션**으로 [cite: 58][cite_start], 잦은 비동기 작업에서 발생하는 가비지 컬렉션(GC)으로 인한 프레임 드랍을 방지하여 부드러운 사용자 경험을 보장하며, 이는 PC 환경에서 안정적인 60 FPS 이상을 유지하는 데 필수적입니다[cite: 58, 59].

* [cite_start]**설치 권장 방법:** 공식 Cysharp GitHub 릴리스 페이지에서 최신 버전의 **`.unitypackage`** 파일을 직접 다운로드하여 프로젝트에 임포트하는 것이 가장 안정적이고 권장되는 방법입니다[cite: 59, 60].

---

### 섹션 2: UniTask를 활용한 현대적 비동기 프로그래밍 마스터하기

[cite_start]UniTask의 채택은 단순한 기술 최적화를 넘어, 프로젝트의 핵심 철학에 대한 아키텍처적 약속입니다[cite: 87]. [cite_start]`await`를 통해 가비지 컬렉션(GC) 급증을 피하는 것은 플레이어의 몰입감과 AI의 존재에 대한 믿음을 보존하는 데 직접적으로 기여합니다[cite: 88, 89].

#### 2.1. 패러다임의 전환: IEnumerator에서 async UniTask로
[cite_start]`async/await`와 UniTask는 기존 IEnumerator 기반 코루틴의 문제(콜백 지옥, 복잡한 예외 처리)를 해결하고 코드를 동기 코드처럼 깔끔하고 선형적으로 작성할 수 있게 해줍니다[cite: 91, 92].

| 비교 기준 | IEnumerator 코루틴 | C# Task | UniTask |
| :--- | :--- | :--- | :--- |
| **메모리 할당** | [cite_start]낮음 [cite: 182] | [cite_start]매 호출마다 객체 할당 (높은 GC 부담) [cite: 177, 182] | [cite_start]**구조체 기반, 거의 제로에 가까운 GC 발생** [cite: 174, 182] |
| **예외 처리** | [cite_start]복잡함 (상태 값 확인) [cite: 182] | [cite_start]`try-catch` 블록으로 명확하게 처리 [cite: 182] | [cite_start]**`try-catch` 블록으로 명확하게 처리** [cite: 170, 182] |
| **가독성** | [cite_start]낮음 (중첩 구조, 콜백 지옥) [cite: 182] | [cite_start]높음 (선형적 코드) [cite: 182] | [cite_start]**높음 (선형적 코드)** [cite: 182] |
| **Unity 통합성** | [cite_start]높음 [cite: 182] | [cite_start]Unity 싱글 스레드 환경에 부적합 [cite: 182] | [cite_start]**Unity PlayerLoop에 완벽히 통합**, AsyncOperation 호환 [cite: 182] |

#### 2.2. 성능의 중요성 : UniTask가 타협 불가능한 선택인 이유
[cite_start]UniTask는 구조체(struct) 기반의 값 타입(value-type)으로 구현되어, 대부분의 `async` 작업에서 `await`를 사용할 때 힙(heap) 메모리 할당이 거의 발생하지 않습니다[cite: 174]. [cite_start]이는 빈번한 API 호출 시 발생할 수 있는 **가비지 컬렉션(GC)으로 인한 화면 끊김 현상(프레임 드랍)을 방지**하여 **'살아있는 존재'라는 몰입감을 지키는 데 필수적**입니다[cite: 175, 179]. [cite_start]GC 동작 중 Unity의 메인 스레드가 일시적으로 멈추는 현상은 '살아있는 AI'라는 핵심 판타지를 치명적으로 훼손합니다[cite: 179, 180].

#### 2.3. 기본 LLM API 클라이언트 구현
[cite_start]UniTask를 활용하여 LLM API 서버로 프롬프트를 보내고 응답을 문자열로 반환하는 `LLMApiClient` 클래스의 기본 구조는 다음과 같은 핵심적인 UniTask 활용 방식을 보여줍니다[cite: 185, 186]:

* [cite_start]`async UniTask<string> SendMessageAsync(...)` 메서드를 사용하여 비동기 작업을 정의합니다[cite: 207].
* [cite_start]`await webRequest.SendWebRequest().WithCancellation(ct);`를 통해 UnityWebRequest를 비동기적으로 기다리며, **Cancellation Token**을 전달하여 작업 취소를 가능하게 합니다[cite: 155, 225, 226, 227].
* [cite_start]네트워크 요청 실패 시 `throw new Exception(webRequest.error);`를 통해 예외를 발생시켜 호출자(`caller`)의 `try-catch` 블록에서 처리하도록 합니다[cite: 162, 163, 164].

---

### 섹션 3: 프로덕션 수준의 내결함성을 갖춘 네트워크 계층 설계

[cite_start]2단계의 기본 클라이언트를 네트워크의 불안정성을 우아하게 처리하는 **견고하고 회복탄력성 있는 클라이언트**로 발전시켜야 합니다[cite: 300]. [cite_start]이는 **'실패를 대비한 설계'** 철학의 직접적인 구현입니다[cite: 301]. [cite_start]잘 처리된 예외는 단순히 충돌을 방지하는 것을 넘어, 캐릭터의 몰입감을 심화시키는 서사적 기회가 될 수 있습니다[cite: 302].

[cite_start]네트워크 타임아웃 발생 시 무미건조한 기술적 오류 메시지 대신, AI 캐릭터의 개성이 담긴 특정 대사(예: "음... 그건 좀 깊이 생각해봐야겠는걸?")를 출력하면 [cite: 304, 305, 306][cite_start], 네트워크 지연 시간이 기술적 결함이 아닌, AI 캐릭터의 자연스러운 **'생각하는 시간'**으로 인식되어 부정적인 사용자 경험을 긍정적인 몰입 경험으로 전환시킬 수 있습니다[cite: 307, 308].

#### 3.1. 응답 없는 요청 정복: 타임아웃 구현
[cite_start]모든 API 호출에 타임아웃을 적용하여 무한정 대기 상태에 빠지는 것을 방지해야 합니다[cite: 310]. [cite_start]타임아웃은 `CancellationTokenSource`를 사용하여 지정된 시간이 지나면 취소 신호를 보내는 방식으로 구현할 수 있습니다[cite: 311].

* [cite_start]**토큰 연결:** 외부에서 전달된 취소 토큰과 타임아웃 토큰을 `CancellationTokenSource.CreateLinkedTokenSource`로 연결하여, 둘 중 하나라도 취소되면 전체 작업이 취소되도록 설계합니다[cite: 312, 313].

#### 3.2. 지능형 재시도: 지수 백오프와 지터
[cite_start]일시적인 네트워크 오류 발생 시, 불안정한 서버에 부담을 줄 수 있는 즉각적인 재시도를 방지하기 위해 **'지수 백오프(Exponential Backoff)'** 전략을 사용합니다[cite: 315, 316].

* [cite_start]**지수 백오프:** 재시도 간의 대기 시간을 점차 늘리는 전략[cite: 316].
* [cite_start]**지터(Jitter) 추가:** 모든 클라이언트가 동시에 재시도를 시도하는 **'Thundering Herd'** 문제를 방지하기 위해, 재시도 간격에 무작위성(Jitter)을 추가합니다[cite: 317, 318]. [cite_start]지터는 재시도 타이밍을 분산시켜 시스템 전체의 부하를 완만하게 만들고 안정성을 극대화합니다[cite: 318].

---

### 섹션 4: 안전한 API 키 관리를 위한 다층적 전략

[cite_start]LLM API 키는 프로젝트의 가장 민감한 자산으로, 유출 시 막대한 금전적 손실로 이어질 수 있으므로 [cite: 411] [cite_start]개발 단계부터 배포 단계까지 체계적인 보안 전략을 수립해야 합니다[cite: 412].

#### 4.1. 로컬 개발: 안전하고 간단한 환경 변수 활용
[cite_start]개발 과정에서 API 키를 소스 코드에 직접 하드코딩하는 것은 심각한 보안 취약점입니다[cite: 415]. [cite_start]이를 방지하기 위해 로컬 머신의 **환경 변수**를 사용하여 API 키가 소스 코드에 전혀 남지 않도록 보장하는 것이 가장 기본적인 보안 조치입니다[cite: 416, 417].

* [cite_start]**코드에서 사용법:** Unity 에디터에서 실행될 때, `#if UNITY_EDITOR` 전처리기와 `System.Environment.GetEnvironmentVariable("MY_LLM_API_KEY")` 코드를 사용하여 환경 변수를 안전하게 불러올 수 있습니다[cite: 418, 420, 421, 422].

#### 4.2. 프로덕션 보안: 프록시 아키텍처로의 전환
[cite_start]공개적으로 배포되는 상용 제품의 경우, 클라이언트(게임 빌드)가 직접 LLM API를 호출하는 모델은 근본적으로 안전하지 않으며 **반드시 폐기되어야 합니다**[cite: 480]. [cite_start]악의적인 사용자는 PC 클라이언트를 디컴파일하여 API 키를 추출할 수 있기 때문입니다[cite: 481, 482].

* [cite_start]**필수적인 아키텍처 변경:** 프로덕션 환경에서는 클라이언트가 LLM API를 직접 호출하는 현재 아키텍처에서 **서버 측 프록시(Proxy) 아키텍처**로 전환해야 합니다[cite: 483].
* **작동 방식:**
    1.  [cite_start]**클라이언트 요청:** 게임 클라이언트는 LLM API 키를 알지 못하며, 자체 백엔드 서버(프록시)로 요청을 보냅니다[cite: 486, 487].
    2.  [cite_start]**프록시 서버 처리:** 프록시 서버가 안전한 저장소에서 LLM API 키를 검색하여 서버 환경에서 직접 LLM API를 호출합니다[cite: 488, 489, 490].
    3.  [cite_start]**응답 반환:** 프록시 서버는 LLM API로부터 받은 응답을 다시 게임 클라이언트로 전달합니다[cite: 491].
* [cite_start]이 구조는 LLM API 키가 클라이언트 디바이스에 절대로 노출되지 않도록 보장하여 **최고 수준의 보안을 달성**합니다[cite: 492].

---

### 섹션 5: 고품질 PC 경험을 위한 그래픽 및 성능 최적화

[cite_start]PC 플랫폼의 강력한 성능을 활용하여 AI 캐릭터와의 교감을 극대화하는 시각적 요소를 설정하고 최적화하는 방법을 다룹니다[cite: 500]. [cite_start]PC 플레이어는 자신의 하드웨어에 맞춰 그래픽 품질을 조절할 수 있는 옵션 메뉴를 기대합니다[cite: 502].

#### 5.1. Quality Settings 심층 분석
[cite_start]`Edit > Project Settings > Quality` 설정은 그래픽 옵션을 제공하기 위한 핵심 설정들을 포함합니다[cite: 503].

* [cite_start]**Anti-Aliasing (안티에일리어싱):** 폴리곤의 계단 현상을 부드럽게 처리하여 깔끔한 이미지를 만들며, 캐릭터의 실루엣을 자연스럽게 표현하는 데 중요합니다[cite: 505, 506].
    * [cite_start]**MSAA:** 매우 깔끔하지만 성능 비용이 높습니다[cite: 507].
    * [cite_start]**Post-processing AA (FXAA, TAA):** FXAA는 저렴하지만 흐릿해질 수 있고, TAA는 고품질이지만 움직이는 오브젝트 주변에 잔상(ghosting)을 남길 수 있습니다[cite: 509, 510].
* [cite_start]**Texture Quality (텍스처 품질):** Global Mipmap Limit을 통해 텍스처의 최대 해상도를 제어합니다[cite: 511]. [cite_start]'Full Resolution'은 가장 선명하지만 비디오 메모리(VRAM)를 많이 사용합니다[cite: 512].
* [cite_start]**Shadows (그림자):** 장면에 깊이와 사실감을 더하는 중요한 요소입니다[cite: 515].
    * [cite_start]**Shadow Resolution:** 해상도가 높을수록 그림자 가장자리가 선명하지만 GPU 부하가 증가합니다[cite: 516, 518].
    * [cite_start]**Shadow Cascades:** 방향성 광원의 그림자 품질을 향상시키는 기술로, 캐스케이드 수를 늘리면 카메라에 가까운 그림자가 더 높은 해상도로 렌더링되어 품질이 향상됩니다[cite: 521].
* [cite_start]**VSync (수직 동기화):** 화면 찢어짐(screen tearing) 현상을 방지하기 위해 프레임률을 모니터의 주사율에 맞춥니다[cite: 522]. [cite_start]'Every V Blank' 설정 시 부드러운 화면을 제공하지만 입력 지연이 발생할 수 있습니다[cite: 523].

#### 5.2. HDRP를 활용한 몰입형 리얼리즘 구현 (HDRP 선택 시)
[cite_start]HDRP의 기능들은 단순한 시각적 과시가 아니라, 대화의 감정적 톤을 조절하고 플레이어의 몰입을 유도하는 **강력한 서사적 도구**로 사용되어야 합니다[cite: 526, 527].

* [cite_start]**볼류메트릭 안개/조명 (Volumetric Fog/Lighting):** 공간에 실체적인 대기감을 부여하여 친밀감과 분위기를 조성하며, 창문으로 들어오는 부드러운 빛줄기 등을 표현할 수 있습니다[cite: 528, 529, 530].
* [cite_start]**고급 후처리 (Advanced Post-Processing):** HDRP의 볼륨(Volume) 시스템을 통해 시네마틱 효과를 적용할 수 있습니다[cite: 531, 532].
    * [cite_start]**피사계 심도 (Depth of Field):** AI 캐릭터에 초점을 맞추고 배경을 흐리게 처리하여 플레이어의 시선을 집중시키고 영화적인 느낌을 강화합니다[cite: 533].
    * [cite_start]**컬러 그레이딩 (Color Grading):** 장면의 전체적인 색조를 조절하여 감정적인 톤을 설정하며, 대화의 내용과 감정선에 맞춰 시각적으로 반응하게 할 수 있습니다[cite: 535, 536].

#### 5.3. PC 환경에서의 프로파일링 및 프레임률 관리
[cite_start]**60 FPS 이상의 안정적인 프레임률**은 몰입감 있는 경험의 기본 전제 조건입니다[cite: 538].

* [cite_start]**Unity 프로파일러:** `Window > Analysis > Profiler`를 사용하여 성능 병목 현상을 식별하고 해결해야 합니다[cite: 539].
* [cite_start]프로파일러는 프레임 드랍의 원인이 복잡한 스크립트(**CPU-bound**) 때문인지, 아니면 과도한 그래픽 설정(**GPU-bound**) 때문인지를 알려줍니다[cite: 540].
* [cite_start]목표 프레임률을 유지하기 위해 그림자 품질, 안티에일리어싱 수준, 후처리 효과 등을 **적절히 조절하는 균형점**을 찾아야 합니다[cite: 541]. [cite_start]'살아 숨 쉬는 AI'라는 환상은 불안정한 프레임률 앞에서는 쉽게 깨져버린다는 점을 명심해야 합니다[cite: 542].

---

### 결론: 지속 가능한 성장을 위한 견고한 토대

[cite_start]1주차를 통해 PC 플랫폼에 최적화된 프로덕션 수준의 완전한 비동기 통신 계층을 설계하고 구축했습니다[cite: 544]. [cite_start]이 기반은 다음과 같은 핵심적인 특성을 갖추고 있습니다[cite: 547]:
* [cite_start]**고성능:** UniTask를 통해 GC로 인한 프레임 드랍을 회피하여 플레이어의 몰입 경험을 최우선으로 존중합니다[cite: 548].
* [cite_start]**회복탄력성:** 취소 토큰과 지수 백오프를 통해 불안정한 네트워크 환경의 오류를 우아하게, 심지어 서사적으로 처리합니다[cite: 549].
* [cite_start]**보안성:** 개발 및 프로덕션 환경을 위한 명확하고 안전한 API 키 관리 전략과 아키텍처 경로를 수립했습니다[cite: 552].
* [cite_start]**시각적 탁월성:** PC 플랫폼의 성능을 활용하기 위한 렌더 파이프라인 선택 기준과 고품질 그래픽 설정 가이드를 통해 시각적 경험의 토대를 마련했습니다[cite: 553].

[cite_start]진정으로 '살아 숨 쉬는 AI'를 만들기 위한 가장 중요한 기술적 초석이 마련되었으며, 이 견고한 기반 위에서 최고 수준의 AI 기반 서사 경험을 위한 확장 가능하며 지속 가능한 플랫폼을 구축하게 될 것입니다[cite: 554, 555].