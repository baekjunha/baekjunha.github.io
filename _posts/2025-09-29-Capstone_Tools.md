---
published: False
title: "캡스톤 디자인 완전 정복: '살아있는' AI 캐릭터 구현 가이드"
categories: [capstone]
tags: [capstone, ai, unity, guide]
date: 2025-09-29 17:11:43 +0900
math: true 
image:
  path: https://mastermixmovies.wordpress.com/wp-content/uploads/2017/10/2001.gif?w=1241&h=546
---

> **요약**: 캡스톤 프로젝트 성공을 위해 직성된 **'살아있는' AI 캐릭터 구현 핵심 가이드라인**이다. 각 기술 스택(코어, 클라이언트, 게임플레이, UX)이 왜 필요한지, 어떻게 작동하는지, 그리고 실제 코드 구현은 어떻게 진행하는지 구체적으로 해부한다.
{: .prompt-info }

## 목차
* TOC
{:toc}

---

## 1. AI 코어 아키텍처: 캐릭터의 두뇌와 기억

> AI 캐릭터가 지능적으로 사고하고, 일관된 정체성을 유지하며, 플레이어와의 관계를 기억하게 만드는 핵심 기술<sup><a href="#footnote-1">1</a></sup> 파트다.

### 1.1. LLM (Gemini) API 통신

*   **역할**: 플레이어의 입력을 AI 서버로 전송하고 응답을 받아오는 **핵심 통신 채널**이다. 게임 내 실시간 대화 생성을 전담한다.
*   **구현**: Unity의 `UnityWebRequest`를 사용하여 Gemini **LLM**<sup><a href="#footnote-2">2</a></sup> **API**<sup><a href="#footnote-3">3</a></sup>에 **HTTP POST 요청**<sup><a href="#footnote-4">4</a></sup>을 보낸다. 요청 시에는 보안을 위해 하드코딩을 배제하고 **환경 변수**<sup><a href="#footnote-5">5</a></sup>에서 API 키를 로드하여 사용한다.

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
            // 4. 성공 시 응답 JSON⁶ 텍스트를 파싱⁷하여 출력한다.
            string jsonResponse = request.downloadHandler.text;
            Debug.Log("Gemini API Response: " + jsonResponse);
        }
    }
}
```
{: file="GeminiApiIntegration.cs" }

*(출처: 게임 기술 구현 상세 보고서.pdf, II. 유니티-제미니 API 통합 구현)*

### 1.2. RAG (검색 증강 생성) 시스템

*   **역할**: LLM의 기억력 한계(컨텍스트 윈도우 초과 시 망각)를 보완하는 기술이다. 캐릭터의 고유 성격, 배경 이야기 등 **장기 기억**을 **데이터베이스**⁸에 적재하고, 대화의 맥락에 부합하는 정보를 실시간 검색 및 주입하여 일관된 답변을 유도한다.
*   **핵심 기술 - 하이브리드 검색(Hybrid Search)**: 프로젝트의 알파이자 오메가다. 단순히 질문과 임베딩 의미가 유사한 벡터를 찾는 것을 넘어, **'호감도'나 '관계 상태' 등 현재 인게임 데이터 기반의 메타데이터⁹를 1차로 필터링**한다. 이를 통해 AI가 과거 다퉜던 상황을 인지하고 그에 맞는 미묘한 스탠스를 취할 수 있다. *(출처: 5주차_구현 가이드.pdf, 1.2. 두뇌: 상황 인식적 하이브리드 RAG 기억 시스템)*

### 1.3. 프롬프트 엔지니어링

*   **역할**: AI에게 캐릭터의 페르소나, 말투, 금기 사항을 시스템 차원에서 명시적으로 지시하는 과정이다. 체계화된 프롬프트 템플릿은 캐릭터 일관성을 사수할 뿐만 아니라, 낭비되는 **토큰**<sup><a href="#footnote-10">10</a></sup>을 억제하여 **가동 비용을 직접적으로 절감**시킨다. *(출처: 5주차_구현 가이드.pdf, 1.3. 영혼: 다층적 페르소나 프롬프트 프레임워크)*

---

## 2. 클라이언트 구현: 성능, 안정성, 비용 관리

> **클라이언트**¹¹인 게임 앱이 AI 모델과 안정적으로 통신하고, 사용자에게 쾌적한 경험을 제공하며, 장기적인 운영 비용을 관리하는 기술 파트다.

### 2.1. UniTask 기반 비동기 처리 (멈춤 없는 작업 처리)

*   **역할**: LLM API의 응답을 대기하는 딜레이 동안 게임이 멈추는 현상(**프레임 드랍**)¹²을 방지하는 핵심 기술이다. 모든 네트워크 I/O를 **메인 스레드**¹³와 분리된 **비동기**¹⁴ 방식으로 논블로킹 처리하여 끊김 없는 체감 성능을 제공한다. *(출처: 5주_게임 학습 계획.pdf, 1.1. 코루틴을 넘어서)*

### 2.2. 네트워크 복원력 설계 (통신 실패 대응 전략)

*   **역할**: API 응답 지연에 대비한 **타임아웃(Timeout)** 예외 처리 및, 일시적인 네트워크 장애 시 서버 핑퐁 비용을 낭비하지 않으면서 **안정적으로 재시도**하는 스마트 재시도 패턴(Exponential Backoff 등)을 구현한다. *(출처: 5주_게임 학습 계획.pdf, 1.2. 실패를 대비한 설계)*

### 2.3. 의존성 주입 (VContainer) (유연한 설계의 비밀)

*   **역할**: API 클라이언트, 데이터 레포지토리, UI 컨트롤러 등 각 도메인을 독립적인 부품처럼 분리하는 **IoC 아키텍처 패턴**¹⁵이다. 컴포넌트 간의 강결합을 느슨하게 풀어 레이어별 **유지보수성과 확장성을 비약적으로 높이고, 팀 단위 병렬 개발을 수월케 한다**. *(출처: 5주_게임 학습 계획.pdf, 2.1. 시스템 분리)*

### 2.4. 지능형 응답 캐싱 (답변 임시 저장)

*   **역할**: "이름이 뭐야?" 혹은 "지금 몇 시야?" 같은 상황과 결탁이 무관한 정적인 쿼리는 그 응답을 **인메모리 캐시**¹⁶에 보존한다. 파편화된 중복 API 호출을 근절하여 **비용을 절약하고 0초에 수렴하는 응답 속도를 보장**한다.
*   **구현**: `MemoryCache` 기반 인터페이스를 설계하고, API 통신 래퍼(Wrapper) 계층에서 캐시 히트 여부를 앞단에서 가로채는 방식이다.

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
            SizeLimit = 1024 // 캐시 사이즈 블록
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

    // VContainer를 통한 의존성 주입 (IResponseCache 의존)
    public LLMApiClient(string apiKey, IResponseCache cache) {
        _cache = cache;
    }

    public async UniTask<string> SendMessageAsync(string prompt, bool isCacheable, CancellationToken ct = default) {
        // 1. 캐싱 정책 활성화 시, 프론트 반환
        if (isCacheable && _cache.TryGetValue(prompt, out string cachedResponse)) {
            Debug.Log("캐시 메모리에서 응답 리턴");
            return cachedResponse;
        }

        // 2. 미스(Miss) 시 원격 API 통신 진행 (기존 로직)
        // ... (apiResponse 패치 과정)

        // 3. 응답 도착 후 파이프라인에 결과 캐싱
        if (isCacheable) {
            // _cache.Set(prompt, apiResponse);
        }
        
        return ""; // Placeholder
    }
}
```
{: file="LLMApiClient.cs" }

*(출처: 5주차_구현 가이드.pdf, 2.3. 지능형 응답 캐싱의 실제 구현)*

---

## 3. 게임플레이 시스템: 데이터 관리와 상호작용

> 플레이어의 인게임 초이스가 AI 캐릭터와의 관계망 파라미터에 실질적인 파급형 영향을 미치도록 구조화하는 기술 파트다.

### 3.1. ScriptableObject 기반 데이터 설계 (데이터 중심 설계)

*   **역할**: **호감도, 스트레스, 친밀도** 같은 런타임 수치와 캐릭터 정의값을 C# 하드코딩 볼륨에서 분리된 **에셋 파일**¹⁷ 풀로 밀어낸다. 이를 통해 어셈블리 리빌드 없이 기획자가 에디터 인스펙터상에서 **게임 밸런스 수치를 즉각 조율**할 수 있다.
*   **구현**: 관계 현황(`RelationshipStatsSO`)과 증감 이벤트(`RelationshipEventSO`)를 각각의 데이터 모듈로 선언한다.

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
            Debug.Log("호감도 50 달성! 특수 분기 이벤트 해금.");
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
    public int AffectionChange; // 인과율 산정

    // 퍼블리싱 이펙트
    public void ApplyEffect(RelationshipStatsSO stats)
    {
        stats.Affection += AffectionChange;
        stats.CheckAndUnlockSpecialEvent(); 
    }
}
```
{: file="RelationshipEventSO.cs" }

*(출처: 5주_게임 학습 계획.pdf, 3.1. ScriptableObjects를 활용한 데이터 중심 설계)*

### 3.2. 관계 발전 시스템

*   **역할**: 대화의 어조나 선택에 따른 영향을 수치화하여 모니터링한다. **"+10 호감도"** 식의 플로팅 텍스트나 **관계 진행 막대(Progress Bar)** 등 시각적 보상을 표출해, 유저 본인의 인풋이 세계에 영향을 미치고 있음을 확실히 체감케 한다. *(출처: 프로젝트 개선을 위한 심층 질문.pdf, 3.1. 관계 발전 시스템 설계)*

### 3.3. 하이브리드 데이터베이스

*   **역할**: 단말기 종속성이 커 날려도 무관한 로그 데이터는 로컬의 **SQLite**¹⁸에 마운트하고, 크로스 동기화 및 결제/인증에 묶이는 유저 민감 정보는 클라우드 NoSQL 인스턴스인 **Firebase Realtime Database**¹⁹에 격리해 투트랙으로 관리한다. *(출처: 게임 기술 구현 상세 보고서.pdf, III. 데이터베이스 및 저장 방식)*
---

## 4. UX 및 라이브 운영: 몰입감과 지속 가능한 성장

> AI 캐릭터에 생명력을 불어넣고, 출시 이후에도 서비스를 안정적으로 운영하며 지속적으로 피드백 루프를 돌리기 위한 기술 파트다.

### 4.1. 동적 립싱크 시스템

*   **역할**: LLM이 뽑아낸 텍스트를 음성(**TTS**)으로 치환하고, **uLipSync** 플러그인²⁰을 오디오 소스에 물려 음향 파형을 실시간 분석한다. 여기서 산출된 볼륨과 모음 팩터를 3D 캐릭터 모델의 **입 모양(블렌드 셰이프)**²¹ 파라미터에 매핑하여 스크립트에 종속되지 않은 즉각적인 **몰입감을 선사**하는 킬러 UX 기술이다. *(출처: 5주_게임 학습 계획.pdf, 4.1. 동적 립싱크)*

### 4.2. CI/CD 파이프라인²² (자동 배포 시스템)

*   **역할**: **GitHub Actions** 기반의 헤드리스 유니티 빌드 환경을 구축해, 소스 코드 변경이 트리거될 때마다 **빌드**²³와 릴리즈 아티팩트 생성을 **완전 자동화**한다. 이를 통해 치명적 버그 수정이나 라이브 업데이트를 유저에게 논스톱으로 딜리버리한다.
*   **구현**: 프로젝트 리포지토리 루트에 `.github/workflows/unity-build.yml` 명세서를 작성하여 **워크플로우**²⁴ 트리거를 오픈한다.

```yaml
# unity-build.yml
name: Unity Build CI

on:
  push:
    branches: [ main ] # main 브랜치 통합 시 파이프라인 가동
  pull_request:

jobs:
  build:
    name: Build for Windows (x64)
    runs-on: ubuntu-latest
    steps:
      # 1. 깃 체크아웃
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          lfs: true

      # 2. Library 캐싱 히트로 빌드 타임 압축
      - name: Cache Library folder
        uses: actions/cache@v3
        with:
          path: Library
          key: Library-${{ hashFiles('Assets/**', 'Packages/**', 'ProjectSettings/**') }}

      # 3. Secrets²⁵ 컨테이너에 은닉된 라이선스 마운트
      - name: Activate Unity License
        uses: game-ci/unity-activate@v3
        env:
          UNITY_LICENSE: ${{ secrets.UNITY_LICENSE }}

      # 4. 헤드리스 타겟 빌드
      - name: Build project
        uses: game-ci/unity-builder@v4
        with:
          targetPlatform: StandaloneWindows64

      # 5. 아티팩트²⁶ 클라우드 업로드
      - name: Upload build artifact
        uses: actions/upload-artifact@v4
        with:
          name: build-StandaloneWindows64
          path: build/StandaloneWindows64
```
{: file="unity-build.yml" }

*(출처: 5주차_구현 가이드.pdf, 3.2. 구현 가이드: GitHub Actions를 이용한 Unity 빌드 자동화)*

### 4.3. AI 피드백 루프 (사용자 기반 개선)

*   **역할**: **Firebase Analytics**²⁷ SDK를 클라이언트에 적재해, 모델이 뱉은 답변에 대한 유저 리액션(좋아요/싫어요) 이벤트를 수집한다. 이 로깅 데이터를 근거로 프롬프트를 컨디셔닝하거나 RAG 백엔드를 정비하여 **AI 모델이 스스로 강화 생태계를 구축**하게 만드는 롱텀 비전이다.
*   **구현**: UI 버튼 옵저버에 바인딩되어 통계 서버로 페이로드를 전송하는 로거 스크립트 작성.

```csharp
// AIFeedbackLogger.cs
using Firebase.Analytics;
using UnityEngine;

public class AIFeedbackLogger : MonoBehaviour
{
    // 좋아요 이벤트 델리게이트
    public void LogPositiveFeedback(string prompt, string response)
    {
        LogFeedbackEvent("ai_feedback_positive", prompt, response);
    }

    // 싫어요 이벤트 델리게이트
    public void LogNegativeFeedback(string prompt, string response)
    {
        LogFeedbackEvent("ai_feedback_negative", prompt, response);
    }

    private void LogFeedbackEvent(string eventName, string prompt, string response)
    {
        // 애널리틱스 파장 제약 조건에 따른 절삭
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

*(출처: 5주차_구현 가이드.pdf, 4.1. 실습 가이드: Firebase Analytics로 AI 응답 피드백 수집하기)*

---

## 5. 부록 및 용어 해설

*   **아키텍처(Architecture)**<sup>1</sup>: 소프트웨어의 뼈대나 구조를 의미한다. 좋은 아키텍처는 집을 튼튼하게 짓는 설계도처럼, 프로그램을 안정적이고 확장 가능하게 만든다.
*   **LLM (Large Language Model)**<sup>2</sup>: 거대 언어 모델의 약자다. 구글의 제미니처럼 방대한 텍스트 데이터를 훈련시켜 인간처럼 자연스러운 문맥을 이해하고 산출해내는 코어 레이어 구조다.
*   **API (Application Programming Interface)**<sup>3</sup>: 소프트웨어 컴포넌트 간 트랜잭션을 정의한 통신 프로토콜이다.
*   **HTTP POST 요청**<sup>4</sup>: 클라이언트가 웹 호스트 측으로 바이너리 풀을 보내 서버의 상태를 변경(요청)하는 프로토콜이다.
*   **환경 변수(Environment Variable)**<sup>5</sup>: OS 레벨에서 주입하는 런타임 값으로, 하드코딩 없이 민감 정보를 보호하는 기본 장치다.
*   **JSON (JavaScript Object Notation)**<sup>6</sup>: 데이터를 주고받을 때 웹에서 범용적으로 기용되는 객체 지향 텍스트 묶음이다.
*   **파싱(Parsing)**<sup>7</sup>: 평문 데이터인 JSON 등을 런타임 구조(클래스 등)체로 디코딩하는 연산이다.
*   **데이터베이스(Database)**<sup>8</sup>: RAG가 장기 기억을 아카이빙하고 검색할 때 조회하는 영속적 저장 프로토콜 묶음이다.
*   **메타데이터(Metadata)**<sup>9</sup>: '데이터를 상술하는 데이터'. '어제 싸웠다'라는 코퍼스에 '관계 타격치: 극심함'이라는 꼬리표를 붙이는 용도다.
*   **토큰(Token)**<sup>10</sup>: 텍스트를 파싱하는 말뭉치의 최소 단위다. 과금 모델의 통화로 쓰인다.
*   **클라이언트(Client)**<sup>11</sup>: 플레이어의 디바이스에 적재되는 Unity 런타임 결과물이다.
*   **프레임 드랍(Frame Drop)**<sup>12</sup>: 동기화 지연으로 인해 3D 렌더링 사이클이 지연되어 게임이 일시적으로 멈추고 버벅거리는 현상이다.
*   **메인 스레드(Main Thread)**<sup>13</sup>: Unity가 렌더 파이프라인 및 Update 함수를 병목 없이 제어하는 싱글 코어 작업 지시망이다.
*   **비동기(Asynchronous)**<sup>14</sup>: 스레드를 대기시키지 않고 I/O 콜을 백그라운드로 전위시켜 애플리케이션 프리징을 방지하는 패러다임이다.
*   **아키텍처 패턴(Architecture Pattern)**<sup>15</sup>: 소프트웨어 스파게티화를 방어하기 위한 검증된 디자인 방법론 모음집.
*   **인메모리 캐시(In-memory Cache)**<sup>16</sup>: HDD나 SDD 엑세스 없이 RAM에 휘발성으로 도큐먼트를 로드해 0초 딜레이로 히트시키는 로직.
*   **에셋 파일(Asset File)**<sup>17</sup>: 씬 계층에서 독립된 파일 메타데이터 모델. ScriptableObject이 이 구조에 속한다.
*   **로컬 DB / 클라우드 DB**<sup>18, 19</sup>: 사용자 디바이스에 저장되는 폐쇄형 저장소와, TCP/IP를 경유해 중앙화되는 개방형 저장소 체계.
*   **플러그인 / 블렌드 셰이프**<sup>20, 21</sup>: 확장 기능을 주관하는 에셋과, 3D 버텍스의 좌표를 벡터 배열 기반으로 리깅하는 엔진 컨트롤 패러다임.
*   **CI/CD (Continuous Integration/Continuous Deployment)**<sup>22</sup>: 테스트 보일러플레이트를 통한 지속 통합, 지속 배포 오토메이션 워크플로우.
*   **빌드 / 워크플로우 / Secrets / 아티팩트**<sup>23, 24, 25, 26</sup>: 개발 파이프라인의 생애주기 전반(컴파일-액션-보안-산출물)을 주관하는 요소들.
*   **Firebase Analytics**<sup>27</sup>: BaaS 플랫폼의 분석 툴로, 플레이어 세션 텔레메트리를 클라우드 파이프라인으로 쏴주는 통계 SDK.