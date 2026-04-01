---
published: False
title: "캡스톤 디자인 완전 정복: '살아있는' AI 캐릭터 구현 가이드"
categories: [Capstone]
tags: [capstone, ai, unity, guide]
date: 2025-09-29 17:11:43 +0900
math: true 
---

## 요약
> **요약**: 캡스톤 프로젝트 성공을 위해 작성된 **'살아있는' AI 캐릭터 구현 핵심 가이드라인**이다. 각 기술 스택(코어, 클라이언트, 게임플레이, UX)이 왜 필요한지, 어떻게 작동하는지, 그리고 실제 코드 구현은 어떻게 진행하는지 구체적으로 분석한다.

## 목차
* TOC
{:toc}

---

## 1. AI 코어 아키텍처: 캐릭터의 두뇌와 기억

AI 캐릭터가 지능적으로 사고하고, 일관된 정체성을 유지하며, 플레이어와의 관계를 기억하게 만드는 핵심 기술 파트다.

### 1.1. LLM (Gemini) API 통신

*   **역할**: 플레이어의 입력을 AI 서버로 전송하고 응답을 받아오는 **핵심 통신 채널**이다. 게임 내 실시간 대화 생성을 전담한다.
*   **구현**: Unity의 `UnityWebRequest`를 사용하여 Gemini **LLM** **API**에 **HTTP POST 요청**을 보낸다. 요청 시에는 보안을 위해 하드코딩을 배제하고 **환경 변수**에서 API 키를 로드하여 사용한다.

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
        // 1. 환경 변수에서 API 키를 안전하게 로드한다.
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

        // 2. Gemini API 규격에 맞는 JSON 형식으로 페이로드를 생성한다.
        string jsonPayload = "{\"contents\":[{\"parts\":[{\"text\":\"" + userMessage + "\"}]}]}";
        byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonPayload);

        UnityWebRequest request = new UnityWebRequest(url, "POST");
        request.uploadHandler = new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");

        // 3. API 요청을 비동기로 기다린다.
        yield return request.SendWebRequest();

        if (request.result != UnityWebRequest.Result.Success)
        {
            Debug.LogError(request.error);
        }
        else
        {
            // 4. 성공 시 응답 JSON 텍스트를 파싱하여 출력한다.
            string jsonResponse = request.downloadHandler.text;
            Debug.Log("Gemini API Response: " + jsonResponse);
        }
    }
}
```
{: file="GeminiApiIntegration.cs" }


### 1.2. RAG (검색 증강 생성) 시스템

*   **역할**: LLM의 기억력 한계를 보완하는 기술이다. 캐릭터의 고유 성격, 배경 이야기 등 **장기 기억**을 **데이터베이스**에 적재하고, 대화의 맥락에 부합하는 정보를 실시간 검색 및 주입하여 일관된 답변을 유도한다.
*   **핵심 기술 - 하이브리드 검색(Hybrid Search)**: 단순히 질문과 임베딩 의미가 유사한 벡터를 찾는 것을 넘어, **'호감도'나 '관계 상태' 등 현재 인게임 데이터 기반의 메타데이터를 1차로 필터링**한다. 이를 통해 AI가 과거의 상황을 인지하고 그에 맞는 응답을 생성할 수 있게 한다.

### 1.3. 프롬프트 엔지니어링

*   **역할**: AI에게 캐릭터의 페르소나, 말투, 규칙을 시스템 차원에서 명시적으로 지시하는 과정이다. 체계화된 프롬프트 템플릿은 캐릭터 일관성을 유지할 뿐만 아니라, 낭비되는 **토큰**을 억제하여 **가동 비용을 절감**시킨다.

---

## 2. 클라이언트 구현: 성능, 안정성, 비용 관리

**클라이언트**인 게임 앱이 AI 모델과 안정적으로 통신하고, 사용자에게 쾌적한 경험을 제공하며, 장기적인 운영 비용을 관리하는 기술 파트다.

### 2.1. UniTask 기반 비동기 처리 (멈춤 없는 작업 처리)

*   **역할**: API의 응답을 대기하는 동안 게임이 멈추는 현상(**프레임 드랍**)을 방지하는 핵심 기술이다. 모든 네트워크 I/O를 **메인 스레드**와 분리된 **비동기** 방식으로 처리하여 끊김 없는 성능을 제공한다.

### 2.2. 네트워크 복원력 설계 (통신 실패 대응 전략)

*   **역할**: API 응답 지연에 대비한 **타임아웃(Timeout)** 처리와 일시적인 네트워크 장애 시 **안정적으로 재시도**하는 패턴을 구현한다.

### 2.3. 의존성 주입 (VContainer) (유연한 설계의 비밀)

*   **역할**: 각 도메인을 독립적으로 분리하는 **IoC 아키텍처 패턴**이다. 컴포넌트 간의 결합을 느슨하게 하여 **유지보수성과 확장성을 높이고 효율적인 협업 구조를 구축**한다.

### 2.4. 지능형 응답 캐싱 (답변 임시 저장)

*   **역할**: 반복적이고 정적인 쿼리에 대한 응답을 **인메모리 캐시**에 저장한다. 중복 호출을 줄여 **비용을 절약하고 빠른 응답 속도를 보장**한다.
*   **구현**: `MemoryCache` 기반 인터페이스를 설계하고, API 통신 계층에서 캐시 활용 여부를 판단한다.

```csharp
// SimpleMemoryCache.cs - 로컬 캐시 스토리지
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
            SizeLimit = 1024 // 캐시 사이즈 설정
        });
    }
    
    public bool TryGetValue(string key, out string value) {
        return _cache.TryGetValue(key, out value);
    }
    
    public void Set(string key, string value) {
        var cacheEntryOptions = new MemoryCacheEntryOptions()
            .SetSize(1)
            .SetSlidingExpiration(TimeSpan.FromMinutes(5)); // 5분 TTL 설정
        _cache.Set(key, value, cacheEntryOptions);
    }
    
    public void Dispose() {
        _cache.Dispose();
    }
}
```
{: file="SimpleMemoryCache.cs" }

```csharp
// LLMApiClient.cs - 프록시 패턴이 적용된 API 클라이언트
public class LLMApiClient {
    private readonly IResponseCache _cache;

    // VContainer를 통한 의존성 주입
    public LLMApiClient(string apiKey, IResponseCache cache) {
        _cache = cache;
    }

    public async UniTask<string> SendMessageAsync(string prompt, bool isCacheable, CancellationToken ct = default) {
        // 1. 캐싱 정책 활성화 시, 캐시 확인
        if (isCacheable && _cache.TryGetValue(prompt, out string cachedResponse)) {
            Debug.Log("캐시 메모리에서 응답 리턴");
            return cachedResponse;
        }

        // 2. 캐시 미스 시 API 통신 진행
        // ... (apiResponse 처리 과정)

        // 3. 응답 도착 후 결과 캐싱
        if (isCacheable) {
            // _cache.Set(prompt, apiResponse);
        }
        
        return ""; // Placeholder
    }
}
```
{: file="LLMApiClient.cs" }

---

## 3. 게임플레이 시스템: 데이터 관리와 상호작용

플레이어의 선택이 AI 캐릭터와의 관계 데이터에 반영되도록 구조화하는 기술 파트다.

### 3.1. ScriptableObject 기반 데이터 설계 (데이터 중심 설계)

*   **역할**: 수치와 캐릭터 정의값을 **에셋 파일** 형태로 관리한다. 이를 통해 하드코딩 없이 에디터에서 **게임 밸런스를 즉각 조율**할 수 있다.
*   **구현**: 관계 스탯과 이벤트를 각각의 데이터 모듈로 선언한다.

```csharp
// RelationshipStatsSO.cs - 상태 지연 및 조건 검사 모듈
using UnityEngine;

[CreateAssetMenu(fileName = "RelationshipStats", menuName = "AI/Relationship Stats")]
public class RelationshipStatsSO : ScriptableObject
{
    public int Affection; // 호감도 수치
    public bool IsSpecialEventUnlocked;

    // 트리거 체크 로직
    public void CheckAndUnlockSpecialEvent()
    {
        if (Affection >= 50 && !IsSpecialEventUnlocked)
        {
            IsSpecialEventUnlocked = true;
            Debug.Log("호감도 50 달성! 특수 이벤트 해금.");
        }
    }
}
```
{: file="RelationshipStatsSO.cs" }

```csharp
// RelationshipEventSO.cs - 수치 변동 트리거 이벤트
using UnityEngine;

[CreateAssetMenu(fileName = "RelationshipEvent", menuName = "AI/Relationship Event")]
public class RelationshipEventSO : ScriptableObject
{
    public string EventName;
    public int AffectionChange; // 변동 수치

    // 효과 적용
    public void ApplyEffect(RelationshipStatsSO stats)
    {
        stats.Affection += AffectionChange;
        stats.CheckAndUnlockSpecialEvent(); 
    }
}
```
{: file="RelationshipEventSO.cs" }

### 3.2. 관계 발전 시스템

*   **역할**: 대화나 선택에 따른 영향을 수치화하여 모니터링한다. 시각적 보상을 통해 사용자의 입력이 세계에 영향을 미치고 있음을 체감할 수 있게 한다. 

### 3.3. 하이브리드 데이터베이스

*   **역할**: 로그 데이터는 로컬의 **SQLite**에 저장하고, 민감 정보나 동기화가 필요한 데이터는 **Firebase**에서 관리하는 방식이다. 

---

## 4. UX 및 라이브 운영: 몰입감과 지속 가능한 성장

AI 캐릭터에 생명력을 불어넣고 서비스를 안정적으로 운영하기 위한 기술 파트다.

### 4.1. 동적 립싱크 시스템

*   **역할**: 추출된 텍스트를 음성(**TTS**)으로 변환하고, **uLipSync** 플러그인을 사용하여 실시간으로 분석한다. 산출된 데이터를 캐릭터의 **입 모양(블렌드 셰이프)** 파라미터에 매핑하여 시각적 몰입감을 확보한다.

### 4.2. CI/CD 파이프라인 (자동 배포 시스템)

*   **역할**: **GitHub Actions**를 기반으로 빌드 환경을 구축하여 소스 코드 변경 시 **빌드**와 배포 과정을 **완전 자동화**한다. 이를 통해 안정적인 업데이트를 제공한다.
*   **구현**: 워크플로우 명세서를 작성하여 자동화 프로세스를 구성한다.

{% raw %}
```yaml
# unity-build.yml
name: Unity Build CI

on:
  push:
    branches: [ main ] # main 브랜치 통합 시 가동
  pull_request:

jobs:
  build:
    name: Build for Windows (x64)
    runs-on: ubuntu-latest
    steps:
      # 1. 레포지토리 체크아웃
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          lfs: true

      # 2. 라이브러리 캐싱으로 시간 단축
      - name: Cache Library folder
        uses: actions/cache@v3
        with:
          path: Library
          key: Library-${{ hashFiles('Assets/**', 'Packages/**', 'ProjectSettings/**') }}

      # 3. 라이선스 설정
      - name: Activate Unity License
        uses: game-ci/unity-activate@v3
        env:
          UNITY_LICENSE: ${{ secrets.UNITY_LICENSE }}

      # 4. 프로젝트 빌드
      - name: Build project
        uses: game-ci/unity-builder@v4
        with:
          targetPlatform: StandaloneWindows64

      # 5. 아티팩트 업로드
      - name: Upload build artifact
        uses: actions/upload-artifact@v4
        with:
          name: build-StandaloneWindows64
          path: build/StandaloneWindows64
```
{% endraw %}
{: file="unity-build.yml" }

### 4.3. AI 피드백 루프 (사용자 기반 개선)

*   **역할**: **Firebase Analytics**를 활용하여 AI 응답에 대한 사용자 반응 데이터를 수집한다. 이를 바탕으로 모델과 RAG 데이터를 정비하여 지속적으로 품질을 개선한다.
*   **구현**: 피드백 데이터를 전송하는 로거 스크립트를 작성한다.

```csharp
// AIFeedbackLogger.cs
using Firebase.Analytics;
using UnityEngine;

public class AIFeedbackLogger : MonoBehaviour
{
    // 긍정 피드백 로깅
    public void LogPositiveFeedback(string prompt, string response)
    {
        LogFeedbackEvent("ai_feedback_positive", prompt, response);
    }

    // 부정 피드백 로깅
    public void LogNegativeFeedback(string prompt, string response)
    {
        LogFeedbackEvent("ai_feedback_negative", prompt, response);
    }

    private void LogFeedbackEvent(string eventName, string prompt, string response)
    {
        // 데이터 길이 조정
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
{: file="AIFeedbackLogger.cs" }

---

## 5. 부록 및 용어 해설

*   **아키텍처(Architecture)**: 소프트웨어의 구조를 의미한다. 프로그램을 안정적이고 확장 가능하게 만드는 설계도와 같다.
*   **LLM (Large Language Model)**: 거대 언어 모델이다. 방대한 데이터를 학습하여 자연스러운 문맥을 이해하고 생성하는 코어 레이어다.
*   **API (Application Programming Interface)**: 소프트웨어 컴포넌트 간의 통신 규칙을 정의한 인터페이스다.
*   **HTTP POST 요청**: 클라이언트가 서버로 데이터를 전송하여 처리를 요청하는 방식이다.
*   **환경 변수(Environment Variable)**: 시스템 레벨에서 관리하는 값으로, 민감한 정보를 보호하는 데 사용된다.
*   **JSON (JavaScript Object Notation)**: 데이터를 주고받는 데 널리 쓰이는 텍스트 포맷이다.
*   **파싱(Parsing)**: 텍스트 데이터를 프로그램에서 사용할 수 있는 구조로 변환하는 과정이다.
*   **데이터베이스(Database)**: 데이터를 체계적으로 저장하고 검색할 수 있는 시스템이다.
*   **메타데이터(Metadata)**: 데이터에 대한 부가적인 정보를 담고 있는 데이터다.
*   **토큰(Token)**: 모델이 텍스트를 처리하는 최소 단위다.
*   **클라이언트(Client)**: 사용자의 기기에서 실행되는 프로그램이다.
*   **프레임 드랍(Frame Drop)**: 처리가 늦어져 화면이 끊기는 현상을 의미한다.
*   **메인 스레드(Main Thread)**: 프로그램의 주요 로직과 렌더링이 수행되는 경로다.
*   **비동기(Asynchronous)**: 작업을 기다리지 않고 백그라운드에서 처리하여 성능을 높이는 방식이다.
*   **아키텍처 패턴(Architecture Pattern)**: 검증된 소프트웨어 구조 설계 방법론이다.
*   **인메모리 캐시(In-memory Cache)**: 빠른 데이터 접근을 위해 메모리에 데이터를 임시 저장하는 방식이다.
*   **에셋 파일(Asset File)**: 엔진에서 관리하는 독립된 데이터 파일이다.
*   **로컬 DB / 클라우드 DB**: 기기 내부에 저장되는 방식과 서버를 통해 관리되는 방식의 저장소 체계다.
*   **플러그인 / 블렌드 셰이프**: 추가 기능을 제공하는 모듈과 모델의 형태를 변형하는 기술이다.
*   **CI/CD (Continuous Integration/Continuous Deployment)**: 빌드와 배포를 자동화하여 지속적으로 업데이트하는 워크플로우다.
*   **빌드 / 워크플로우 / Secrets / 아티팩트**: 자동화 파이프라인 구성과 결과물을 다루는 요소들이다.
*   **Firebase Analytics**: 사용자 행동을 분석하여 통계를 제공하는 도구다.