---
published: true
title: "캡스톤 디자인 완전 정복: '살아있는' AI 캐릭터 구현 가이드"
categories: capstone
tags: [capstone, ai, unity, guide]
date: 2025-09-29 17:11:43 +0900
toc: true
toc_sticky: true
author_profile: false
use_math: true 
thumbnail: https://mastermixmovies.wordpress.com/wp-content/uploads/2017/10/2001.gif?w=1241&h=546
---

### 캡톤 디자인 완전 정복: '살아있는' AI 캐릭터 구현 가이드(feat.최우식)

우리 프로젝트의 성공적인 완수를 위해 구현해야 할 핵심 기술들을 총정리했습니다. 이 문서는 각 기술이 **왜 필요하고, 어떻게 작동하며, 실제로 어떻게 코드를 작성하는지**에 대한 구체적인 가이드입니다.

---

### **기술목차**

1.  AI 코어 아키텍처: 캐릭터의 지능과 기억
2.  클라이언트 구현: 성능, 안정성, 비용 관리
3.  게임플레이 시스템: 데이터 관리와 상호작용
4.  UX 및 라이브 운영: 몰입감과 지속 가능한 성장
-----

### 1\. AI 코어 아키텍처: 캐릭터의 두뇌와 기억

> AI 캐릭터가 지능적으로 사고하고, 일관된 정체성을 유지하며, 플레이어와의 관계를 기억하게 만드는 핵심 기술<sup><a href="#footnote-1">1</a></sup> 파트입니다.

#### **LLM (Gemini) API 통신**

  * **역할**: 플레이어의 입력을 AI 서버로 전송하고 응답을 받아오는 **핵심 통신 채널**입니다. 게임 내 실시간 대화 생성을 담당합니다.

  * **구현**: Unity의 `UnityWebRequest`를 사용하여 Gemini **LLM**<sup><a href="#footnote-2">2</a></sup> **API**<sup><a href="#footnote-3">3</a></sup>에 **HTTP POST 요청**<sup><a href="#footnote-4">4</a></sup>을 보냅니다. 요청 시에는 보안을 위해 소스 코드에 직접 노출하지 않고 **환경 변수**<sup><a href="#footnote-5">5</a></sup>에서 API 키를 불러와 사용합니다.

    ```csharp
    // GeminiApiIntegration.cs
    using UnityEngine;
    using UnityEngine.Networking;
    using System.Text;
    using System.Collections;

    public class GeminiApiIntegration : MonoBehaviour
    {
        private const string GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=";
        private string apiKey;

        void Start()
        {
            // 1. 환경 변수에서 API 키를 안전하게 로드합니다.
            apiKey = System.Environment.GetEnvironmentVariable("GEMINI_API_KEY");
            if (string.IsNullOrEmpty(apiKey))
            {
                Debug.LogError("API key not found.");
                return;
            }
            StartCoroutine(CallGeminiApi("안녕, 자기소개해 줄래?"));
        }

        public IEnumerator CallGeminiApi(string userMessage)
        {
            string url = GEMINI_API_URL + apiKey;

            // 2. Gemini API가 요구하는 JSON 형식으로 요청 데이터를 만듭니다.
            string jsonPayload = "{\"contents\":[{\"parts\":[{\"text\":\"" + userMessage + "\"}]}]}";
            byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonPayload);

            UnityWebRequest request = new UnityWebRequest(url, "POST");
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");

            // 3. API에 요청을 보내고 응답을 기다립니다.
            yield return request.SendWebRequest();

            if (request.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError(request.error);
            }
            else
            {
                // 4. 성공 시, 응답받은 JSON⁶ 텍스트를 파싱⁷하여 사용합니다.
                string jsonResponse = request.downloadHandler.text;
                Debug.Log("Gemini API Response: " + jsonResponse);
            }
        }
    }
    ```

    *(출처: 게임 기술 구현 상세 보고서.pdf, II. 유니티-제미니 API 통합 구현)*

#### **RAG (검색 증강 생성) 시스템**

  * **역할**: LLM의 기억력 한계(대화가 길어지면 앞 내용을 잊어버리는 현상)를 보완하는 기술입니다. 캐릭터의 고유한 성격, 배경 이야기 등 **장기 기억**을 **데이터베이스**⁸에 저장하고, 대화의 맥락에 맞는 정보를 실시간으로 검색하여 LLM에게 제공함으로써 일관된 답변을 유도합니다.

  * **핵심 기술 - 하이브리드 검색(Hybrid Search)**: 우리 프로젝트의 핵심은 바로 이 기술입니다. 단순히 사용자의 질문과 의미가 비슷한 과거 기억을 찾는 것을 넘어, **'호감도'나 '관계 상태' 같은 현재 게임 데이터와 연결된 정보(메타데이터)⁹를 먼저 필터링**합니다. 이 덕분에 AI는 '어제 다퉜던 상황'을 인지하고 그에 맞는 미묘한 감정적 답변을 생성할 수 있습니다. *(출처: 5주차\_구현 가이드.pdf, 1.2. 두뇌: 상황 인식적 하이브리드 RAG 기억 시스템)*

#### **프롬프트 엔지니어링**

  * **역할**: AI에게 캐릭터의 정체성, 말투, 행동 규칙을 명시적으로 지시하는 과정입니다. 체계적인 프롬프트 설계는 캐릭터의 일관성을 유지할 뿐만 아니라, 불필요한 **토큰**<sup><a href="#footnote-10">10</a></sup> 사용을 줄여 **API 호출 비용을 직접적으로 절감**하는 효과도 있습니다. *(출처: 5주차\_구현 가이드.pdf, 1.3. 영혼: 다층적 페르소나 프롬프트 프레임워크)*

-----

### 2\. 클라이언트 구현: 성능, 안정성, 비용 관리

> **클라이언트**¹¹인 게임 앱이 AI 모델과 안정적으로 통신하고, 사용자에게 쾌적한 경험을 제공하며, 장기적인 운영 비용을 관리하는 기술 파트입니다.

#### **UniTask 기반 비동기 처리 (멈춤 없는 작업 처리)**

  * **역할**: LLM API의 응답을 기다리는 긴 시간 동안 게임이 멈추는 현상(**프레임 드랍**)¹²을 방지하는 핵심 기술입니다. 모든 네트워크 통신을 **메인 스레드**¹³와 분리된 **비동기**¹⁴ 방식으로 처리하여 끊김 없는 사용자 경험을 제공합니다. *(출처: 5주\_게임 학습 계획.pdf, 1.1. 코루틴을 넘어서)*

#### **네트워크 복원력 설계 (통신 실패 대응 전략)**

  * **역할**: API 응답이 지연될 경우를 대비한 **타임아웃(Timeout)** 처리와, 일시적인 통신 오류 발생 시 서버에 부담을 주지 않으면서 **안정적으로 재시도**하는 스마트 재시도 로직을 구현합니다. *(출처: 5주\_게임 학습 계획.pdf, 1.2. 실패를 대비한 설계)*

#### **의존성 주입 (VContainer) (유연한 설계의 비밀)**

  * **역할**: API 통신, 데이터 관리, UI 등 각 기능 모듈을 독립적인 부품처럼 설계하는 **아키텍처 패턴**¹⁵입니다. 기능 간의 의존도를 낮춰 코드의 **유지보수성과 확장성을 높이고, 팀원 간의 협업 효율을 극대화**합니다. *(출처: 5주\_게임 학습 계획.pdf, 2.1. 시스템 분리)*

#### **지능형 응답 캐싱 (답변 임시 저장)**

  * **역할**: "이름이 뭐야?"처럼 상황과 관계없이 답변이 항상 동일한 정적인 정보는 그 응답을 **인메모리 캐시**¹⁶에 저장합니다. 불필요한 API 호출을 줄여 **비용을 절감하고 응답 속도를 향상**시킵니다.

  * **구현**: `MemoryCache`를 사용하여 간단한 인메모리 캐시를 만들고, API 클라이언트에서 캐시를 먼저 확인하는 로직을 추가합니다.

    ```csharp
    // SimpleMemoryCache.cs - 캐시 관리자 클래스
    using Microsoft.Extensions.Caching.Memory;
    using System;

    public interface IResponseCache {
        bool TryGetValue(string key, out string value);
        void Set(string key, string value);
    }

    public class SimpleMemoryCache : IResponseCache, IDisposable {
        private readonly MemoryCache _cache;
        public SimpleMemoryCache() {
            _cache = new MemoryCache(new MemoryCacheOptions {
                SizeLimit = 1024 // 캐시 크기 제한
            });
        }
        public bool TryGetValue(string key, out string value) {
            return _cache.TryGetValue(key, out value);
        }
        public void Set(string key, string value) {
            var cacheEntryOptions = new MemoryCacheEntryOptions()
                .SetSize(1)
                .SetSlidingExpiration(TimeSpan.FromMinutes(5)); // 5분간 접근 없으면 만료
            _cache.Set(key, value, cacheEntryOptions);
        }
        public void Dispose() {
            _cache.Dispose();
        }
    }
    ```

    ```csharp
    // LLMApiClient.cs (수정) - 캐시 로직이 통합된 API 클라이언트
    public class LLMApiClient {
        private readonly IResponseCache _cache;

        // VContainer를 통해 IResponseCache 주입
        public LLMApiClient(string apiKey, IResponseCache cache) {
            // ... 기존 생성자 로직
            _cache = cache;
        }

        public async UniTask<string> SendMessageAsync(string prompt, bool isCacheable, CancellationToken ct = default) {
            // 1. 캐싱 가능한 요청일 경우, 캐시에서 먼저 검색
            if (isCacheable && _cache.TryGetValue(prompt, out string cachedResponse)) {
                Debug.Log("Returning response from cache.");
                return cachedResponse;
            }

            // 2. 캐시에 없으면 API 호출 (기존 로직)
            // ... (apiResponse를 받아오는 과정)

            // 3. API 응답 후, 캐싱 가능한 요청이었다면 결과 저장
            if (isCacheable) {
                // _cache.Set(prompt, apiResponse);
            }
            // return apiResponse;
            return ""; // Placeholder
        }
    }
    ```

    *(출처: 5주차\_구현 가이드.pdf, 2.3. 지능형 응답 캐싱의 실제 구현)*

-----

### 3\. 게임플레이 시스템: 데이터 관리와 상호작용

> 플레이어의 행동이 AI 캐릭터와의 관계에 실질적인 영향을 미치도록 만드는 게임 로직과 데이터 관리 기술 파트입니다.

#### **ScriptableObject 기반 데이터 설계 (데이터 중심 설계)**

  * **역할**: **호감도, 신뢰도** 같은 캐릭터의 관계 데이터를 코드와 분리된 **에셋 파일**¹⁷로 관리합니다. 이를 통해 기획자나 디자이너가 코드를 직접 수정하지 않고도 **게임 밸런스를 쉽게 조절**할 수 있습니다.

  * **구현**: 관계 상태(`RelationshipStatsSO`)와 관계 이벤트(`RelationshipEventSO`)를 ScriptableObject로 정의합니다.

    ```csharp
    // RelationshipStatsSO.cs - 관계 상태를 저장하는 데이터 컨테이너
    using UnityEngine;

    [CreateAssetMenu(fileName = "RelationshipStats", menuName = "AI/Relationship Stats")]
    public class RelationshipStatsSO : ScriptableObject
    {
        public int Affection; // 호감도
        public bool IsSpecialEventUnlocked;

        // 호감도 임계값에 따라 특별 이벤트를 해금하는 로직
        public void CheckAndUnlockSpecialEvent()
        {
            if (Affection >= 50 && !IsSpecialEventUnlocked)
            {
                IsSpecialEventUnlocked = true;
                Debug.Log("호감도 50 달성! 특별 이벤트가 해금되었습니다!");
            }
        }
    }
    ```

    ```csharp
    // RelationshipEventSO.cs - 관계에 영향을 주는 이벤트를 정의
    using UnityEngine;

    [CreateAssetMenu(fileName = "RelationshipEvent", menuName = "AI/Relationship Event")]
    public class RelationshipEventSO : ScriptableObject
    {
        public string EventName;
        public int AffectionChange; // 이 이벤트가 호감도에 미치는 영향

        // 이벤트 효과를 실제 관계 상태에 적용
        public void ApplyEffect(RelationshipStatsSO stats)
        {
            stats.Affection += AffectionChange;
            stats.CheckAndUnlockSpecialEvent(); // 상태 변경 후 조건 확인
        }
    }
    ```

    *(출처: 5주\_게임 학습 계획.pdf, 3.1. ScriptableObjects를 활용한 데이터 중심 설계)*

#### **관계 발전 시스템**

  * **역할**: 플레이어의 선택이 캐릭터의 호감도 같은 데이터에 미치는 영향을 시스템화합니다. **"+10 호감도"** 같은 시각적 피드백과 **관계 진행 막대(Progress Bar)** UI를 통해 플레이어에게 자신의 행동이 관계에 긍정적인 영향을 미치고 있음을 명확하게 인지시킵니다. *(출처: 프로젝트 개선을 위한 심층 질문.pdf, 3.1. 관계 발전 시스템 설계)*

#### **하이브리드 데이터베이스**

  * **역할**: 대화 기록처럼 기기 내에서만 사용되는 데이터는 \*\*SQLite(로컬 DB)\*\*¹⁸에, 여러 기기에서 동기화가 필요한 계정 정보는 \*\*Firebase(클라우드 DB)\*\*¹⁹에 저장하는 방식으로 데이터의 성격에 맞게 저장소를 분리하여 안정성과 효율성을 확보합니다. *(출처: 게임 기술 구현 상세 보고서.pdf, III. 데이터베이스 및 저장 방식)*

-----

### 4\. UX 및 라이브 운영: 몰입감과 지속 가능한 성장

> AI 캐릭터에 생명력을 불어넣고, 출시 이후에도 서비스를 안정적으로 운영하며 지속적으로 개선하기 위한 기술 파트입니다.

#### **동적 립싱크 시스템**

  * **역할**: LLM이 생성한 텍스트를 음성(**TTS**)으로 변환하고, **uLipSync** **플러그인**²⁰을 이용해 음성 파형을 실시간으로 분석하여 캐릭터 모델의 \*\*입 모양(블렌드 셰이프)\*\*²¹을 동기화합니다. 캐릭터가 실제로 말하는 듯한 느낌을 주어 **몰입감을 극대화**하는 핵심 UX 기술입니다. *(출처: 5주\_게임 학습 계획.pdf, 4.1. 동적 립싱크)*

#### **CI/CD 파이프라인²² (자동 배포 시스템)**

  * **역할**: **GitHub Actions**를 활용해 코드 변경사항이 저장소에 반영될 때마다 **빌드**²³와 배포 과정을 자동화합니다. 이를 통해 버그 수정이나 새로운 콘텐츠 업데이트를 사용자에게 빠르고 안정적으로 전달할 수 있습니다.

  * **구현**: 프로젝트 루트 폴더에 `.github/workflows/unity-build.yml` 파일을 생성하고 아래와 같이 **워크플로우**²⁴를 작성합니다.

    ```yaml
    # unity-build.yml
    name: Unity Build CI

    on:
      push:
        branches: [ main ] # main 브랜치에 push될 때마다 실행
      pull_request:

    jobs:
      build:
        name: Build for Windows (x64)
        runs-on: ubuntu-latest
        steps:
          # 1. 프로젝트 코드 가져오기
          - name: Checkout repository
            uses: actions/checkout@v4
            with:
              lfs: true

          # 2. 빌드 시간 단축을 위해 Library 폴더 캐싱
          - name: Cache Library folder
            uses: actions/cache@v3
            with:
              path: Library
              key: Library-${{ hashFiles('Assets/**', 'Packages/**', 'ProjectSettings/**') }}

          # 3. Unity 라이선스 활성화 (Secrets²⁵에 등록된 정보 사용)
          - name: Activate Unity License
            uses: game-ci/unity-activate@v3
            env:
              UNITY_LICENSE: ${{ secrets.UNITY_LICENSE }}

          # 4. Unity 프로젝트 빌드
          - name: Build project
            uses: game-ci/unity-builder@v4
            with:
              targetPlatform: StandaloneWindows64

          # 5. 빌드 결과물을 아티팩트²⁶로 업로드
          - name: Upload build artifact
            uses: actions/upload-artifact@v4
            with:
              name: build-StandaloneWindows64
              path: build/StandaloneWindows64
    ```

    *(출처: 5주차\_구현 가이드.pdf, 3.2. 구현 가이드: GitHub Actions를 이용한 Unity 빌드 자동화)*

#### **AI 피드백 루프 (사용자 기반 개선)**

  * **역할**: **Firebase Analytics**²⁷로 AI 응답에 대한 플레이어의 피드백(예: 좋아요/싫어요) 데이터를 수집하고, 분석 결과를 바탕으로 RAG 데이터베이스나 프롬프트를 수정하여 AI의 성능을 개선합니다. 이는 플레이어와의 상호작용을 통해 **AI 캐릭터가 스스로 학습하고 성장**하게 만드는 장기적인 운영의 핵심입니다.

  * **구현**: UI 버튼 이벤트에 연결하여 Firebase로 피드백 데이터를 전송하는 로거 스크립트를 작성합니다.

    ```csharp
    // AIFeedbackLogger.cs
    using Firebase.Analytics;
    using UnityEngine;

    public class AIFeedbackLogger : MonoBehaviour
    {
        // UI의 '좋아요' 버튼 OnClick 이벤트에 이 메서드를 연결
        public void LogPositiveFeedback(string prompt, string response)
        {
            LogFeedbackEvent("ai_feedback_positive", prompt, response);
        }

        // UI의 '싫어요' 버튼 OnClick 이벤트에 이 메서드를 연결
        public void LogNegativeFeedback(string prompt, string response)
        {
            LogFeedbackEvent("ai_feedback_negative", prompt, response);
        }

        private void LogFeedbackEvent(string eventName, string prompt, string response)
        {
            // Firebase Analytics 파라미터 길이 제한에 맞춰 텍스트 자르기
            string truncatedPrompt = prompt.Length > 100 ? prompt.Substring(0, 100) : prompt;
            string truncatedResponse = response.Length > 100 ? response.Substring(0, 100) : response;

            FirebaseAnalytics.LogEvent(
                eventName,
                new Parameter("player_prompt", truncatedPrompt),
                new Parameter("ai_response", truncatedResponse)
            );
            Debug.Log($"Logged event '{eventName}' to Firebase Analytics.");
        }
    }
    ```

    *(출처: 5주차\_구현 가이드.pdf, 4.1. 실습 가이드: Firebase Analytics로 AI 응답 피드백 수집하기)*

-----

<a id="footnote-1"></a>¹ **아키텍처(Architecture)**: 소프트웨어의 뼈대나 구조를 의미합니다. 좋은 아키텍처는 집을 튼튼하게 짓는 설계도처럼, 프로그램을 안정적이고 확장 가능하게 만듭니다.  
<a id="footnote-2"></a>² **LLM (Large Language Model)**: '거대 언어 모델'의 약자. Google의 Gemini처럼 방대한 텍스트 데이터를 학습하여 인간처럼 자연스러운 글을 이해하고 생성하는 인공지능 모델입니다.  
<a id="footnote-3"></a>³ **API (Application Programming Interface)**: 프로그램들이 서로 소통하기 위한 약속이나 규칙입니다. 게임(클라이언트)이 구글의 AI 서버(서버)와 대화하기 위해 API를 사용합니다.  
<a id="footnote-4"></a>⁴ **HTTP POST 요청**: 웹에서 클라이언트가 서버로 데이터를 전송(요청)하는 방식 중 하나입니다. 주로 로그인, 글쓰기 등 정보를 서버에 제출할 때 사용됩니다.  
<a id="footnote-5"></a>⁵ **환경 변수(Environment Variable)**: 컴퓨터 운영체제에 설정하는 동적인 값으로, 소스 코드에 직접 민감한 정보를 넣지 않고도 프로그램이 해당 정보에 접근할 수 있게 해주는 안전한 방법입니다.  
⁶ **JSON (JavaScript Object Notation)**: 데이터를 교환할 때 사용하는 가벼운 텍스트 형식입니다. 사람이 읽고 쓰기 쉬우며, 기계가 분석하고 생성하기도 용이합니다.  
⁷ **파싱(Parsing)**: 컴퓨터가 이해할 수 없는 데이터(예: JSON 텍스트)를 의미 있는 구조로 분석하고 변환하는 과정입니다.  
⁸ **데이터베이스(Database)**: 체계적으로 정리된 데이터의 집합입니다. 캐릭터의 기억, 사용자 정보 등을 효율적으로 저장하고 관리하는 데 사용됩니다.  
⁹ **메타데이터(Metadata)**: '데이터에 대한 데이터'라는 뜻입니다. 예를 들어, '어제 싸웠다'는 기억(데이터)에 '관계 상태: 나쁨'이라는 추가 정보(메타데이터)를 붙이는 것입니다.  
<a id="footnote-10"></a>¹⁰ **토큰(Token)**: LLM이 텍스트를 처리하는 기본 단위입니다. 보통 단어, 혹은 그보다 작은 단위로 나뉩니다. API 비용은 보통 이 토큰 사용량에 따라 결정됩니다.  
¹¹ **클라이언트(Client)**: 서버에 서비스를 요청하는 컴퓨터나 프로그램을 의미합니다. 우리 프로젝트에서는 유니티로 만든 게임 앱이 클라이언트입니다.  
¹² **프레임 드랍(Frame Drop)**: 게임 화면이 순간적으로 멈칫거리거나 버벅거리는 현상. 1초에 그려지는 화면의 수(FPS)가 급격히 떨어질 때 발생하며, 사용자 경험을 크게 해칩니다.  
¹³ **메인 스레드(Main Thread)**: Unity에서 화면 업데이트, 사용자 입력 처리 등 대부분의 핵심 작업을 순차적으로 처리하는 기본 실행 흐름입니다. 이 작업이 멈추면 게임 전체가 멈춥니다.  
¹⁴ **비동기(Asynchronous)**: 하나의 작업이 끝날 때까지 기다리지 않고 다른 작업을 동시에 처리하는 방식입니다. 덕분에 API 응답을 기다리는 동안에도 게임은 멈추지 않고 계속 실행될 수 있습니다.  
¹⁵ **아키텍처 패턴(Architecture Pattern)**: 소프트웨어 설계 시 자주 발생하는 문제에 대한 일반적인 해결책입니다. 레고 블록을 조립하는 방법처럼, 검증된 구조를 따라 프로그램을 효율적으로 만들 수 있습니다.  
¹⁶ **인메모리 캐시(In-memory Cache)**: 데이터를 하드디스크가 아닌, 훨씬 빠른 컴퓨터의 주 메모리(RAM)에 임시로 저장하는 기술입니다. 반복적인 요청에 대해 매우 빠른 응답을 가능하게 합니다.  
¹⁷ **에셋 파일(Asset File)**: Unity 프로젝트에서 사용되는 모든 자원(3D 모델, 이미지, 사운드, 스크립트 등)을 의미합니다. ScriptableObject는 코드 로직이 아닌 데이터를 저장하는 용도의 에셋입니다.  
¹⁸ **로컬 DB(Local Database)**: 인터넷 연결 없이 사용자 기기 내부에 데이터를 저장하는 데이터베이스입니다.  
¹⁹ **클라우드 DB(Cloud Database)**: 인터넷을 통해 원격 서버에 데이터를 저장하는 데이터베이스입니다. 여러 기기에서 데이터를 동기화할 때 유용합니다.  
²⁰ **플러그인(Plugin)**: 기존 프로그램에 특정 기능을 추가하기 위해 설치하는 보조 소프트웨어입니다. uLipSync는 유니티에 립싱크 기능을 추가해주는 플러그인입니다.  
²¹ **블렌드 셰이프(Blend Shape)**: 3D 모델의 정점(vertex) 위치를 변형하여 표정을 만들거나 입 모양을 바꾸는 기술입니다. '아', '오', '음' 같은 입 모양을 미리 여러 개 만들어두고, 이 값들을 조합하여 자연스러운 애니메이션을 만듭니다.  
²² **CI/CD (Continuous Integration/Continuous Deployment)**: '지속적 통합/지속적 배포'의 약자. 개발자가 코드를 변경할 때마다 빌드, 테스트, 배포 과정을 자동으로 실행하여 개발 생산성을 높이고 안정적인 서비스를 유지하는 개발 방법론입니다.  
²³ **빌드(Build)**: 프로그래머가 작성한 소스 코드를 컴퓨터가 실행할 수 있는 파일(예: .exe)로 변환하는 과정입니다.  
²⁴ **워크플로우(Workflow)**: 특정 목표를 달성하기 위한 자동화된 작업들의 순서나 흐름을 의미합니다.  
²⁵ **Secrets**: GitHub Actions와 같은 서비스에서 API 키, 비밀번호 등 민감한 정보를 안전하게 저장하고 관리하는 기능입니다.  
²⁶ **아티팩트(Artifact)**: 빌드 과정의 결과물로 생성되는 파일들(예: 실행 파일, 로그 파일)을 의미합니다.  
²⁷ **Firebase Analytics**: 구글에서 제공하는 앱 데이터 분석 도구입니다. 사용자의 행동을 추적하고 분석하여 앱을 개선하는 데 도움을 줍니다.