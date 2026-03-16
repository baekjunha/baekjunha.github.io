---
title: "AI 캐릭터 구현 가이드 (1): 비동기 통신 코어 구축"
date: 2025-10-09 13:11:43 +0900
categories: [Capstone, Development]
tags: [capstone, ai, unity, architecture, unitask]
image:
  path: /assets/img/thumbnails/async-core.png
  alt: AI Simulation Concept
math: true
mermaid: true
---

## 요약
> **요약**: 대화형 AI 캐릭터 프로젝트의 1주차 과제인 비동기 통신 코어 구축 및 PC 플랫폼 최적화 가이드를 기술합니다. UniTask를 활용한 비차단(Non-blocking) 통신 계층 설계와 Unity 초기 설정 프로세스를 설명합니다.
{: .prompt-info }

## 목차
* TOC
{:toc}

---

## 1. 프로젝트 초기화 및 플랫폼 최적화

프로젝트의 시각적 품질과 개발 방향성을 결정하는 초기 설정 단계입니다.

### 1.1. Unity 환경 설정

*   **Unity 버전**: **Unity 2022.3.x LTS** 사용을 권장합니다.
*   **Target Platform**: **PC, Mac & Linux Standalone** (Architecture: **x86_64**).
*   **컬러 스페이스**: 물리 기반 렌더링을 위해 **Linear**로 설정합니다.

### 1.2. 렌더 파이프라인 분석 (URP vs HDRP)

| 비교 기준 | Universal Render Pipeline (URP) | High Definition Render Pipeline (HDRP) |
| :--- | :--- | :--- |
| **대상 하드웨어** | 범용 사양 | 고사양 하드웨어 |
| **시각적 품질** | 범용 및 최적화 중심 | 물리 기반 사실적 렌더링 특화 |
| **학습 곡선** | 상대적으로 낮음 | 높음 (물리 기반 렌더링 지식 필요) |

> [!important]
> 렌더 파이프라인은 상호 호환되지 않으므로 프로젝트의 시각적 목표에 따라 결정해야 합니다.
{: .prompt-warning }

### 1.3. UniTask 통합

Unity 환경에 최적화된 비동기 처리를 위해 **UniTask**를 도입합니다. 이는 표준 `Task` 대비 가비지 컬렉션(GC) 발생을 최소화하여 성능 유지에 기여합니다.

#### 설치 프로세스
1.  [UniTask GitHub](https://github.com/Cysharp/UniTask/releases)에서 `.unitypackage`를 확보합니다.
2.  Unity 프로젝트의 `Assets` 폴더에 임포트합니다.

---

## 2. UniTask 기반 비동기 프로그래밍

`IEnumerator` 코루틴의 한계를 보완하는 현대적인 비동기 워크플로우를 구축합니다.

### 2.1. async UniTask 전환

코루틴 대비 가독성이 높고 예외 처리가 용이한 UniTask를 활용합니다.

```csharp
// [기존 방식] IEnumerator 코루틴
IEnumerator GetRequest(string uri) {
    using (UnityWebRequest webRequest = UnityWebRequest.Get(uri)) {
        yield return webRequest.SendWebRequest();
        if (webRequest.result == UnityWebRequest.Result.Success) {
            Debug.Log(webRequest.downloadHandler.text);
        }
    }
}

// [권장 방식] async UniTask
async UniTask<string> GetRequestAsync(string uri) {
    using (UnityWebRequest webRequest = UnityWebRequest.Get(uri)) {
        await webRequest.SendWebRequest();
        return webRequest.downloadHandler.text;
    }
}
```
{: file="AsyncComparison.cs" }

### 2.2. LLM API 클라이언트 구현

{% raw %}
```csharp
using Cysharp.Threading.Tasks;
using UnityEngine.Networking;
using System.Text;

public class LLMApiClient {
    private readonly string _apiUrl = "https://api.openai.com/v1/chat/completions";
    private readonly string _apiKey;

    public LLMApiClient(string apiKey) => _apiKey = apiKey;

    public async UniTask<string> SendMessageAsync(string prompt) {
        var jsonBody = $"{{\"model\": \"gpt-4\", \"messages\": [{{\"role\": \"user\", \"content\": \"{prompt}\"}}]}}";
        byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonBody);

        using (var webRequest = new UnityWebRequest(_apiUrl, "POST")) {
            webRequest.uploadHandler = new UploadHandlerRaw(bodyRaw);
            webRequest.downloadHandler = new DownloadHandlerBuffer();
            webRequest.SetRequestHeader("Content-Type", "application/json");
            webRequest.SetRequestHeader("Authorization", $"Bearer {_apiKey}");

            await webRequest.SendWebRequest();
            return webRequest.downloadHandler.text;
        }
    }
}
```
{% endraw %}
{: file="LLMApiClient.cs" }

---

## 3. 네트워크 계층 가용성 설계

불안정한 네트워크 환경에 대비한 타임아웃 및 재시도 로직을 구현합니다.

### 3.1. 지수 백오프 (Exponential Backoff) 적용

실패 시 대기 시간을 점진적으로 늘려 재시도하는 전략을 적용합니다.

### 3.2. RobustApiClient 구현

```csharp
public async UniTask<string> SendWithRetryAsync(string prompt, CancellationToken ct) {
    int maxRetries = 3;
    for (int i = 0; i < maxRetries; i++) {
        try {
            using (var timeoutCts = new CancellationTokenSource(TimeSpan.FromSeconds(10)))
            using (var linkedCts = CancellationTokenSource.CreateLinkedTokenSource(ct, timeoutCts.Token)) {
                return await SendMessageAsync(prompt, linkedCts.Token);
            }
        } catch (Exception when (i < maxRetries - 1) {
            int delay = (int)Math.Pow(2, i) * 500 + UnityEngine.Random.Range(0, 250);
            await UniTask.Delay(delay, cancellationToken: ct);
        }
    }
    throw new Exception("재시도 한도 초과");
}
```
{: file="RobustApiClient.cs" }

---

## 4. API 키 보안 전략

### 4.1. 환경 변수 활용

코드 내 하드코딩을 방지하기 위해 시스템 환경 변수를 참조합니다.

```csharp
string apiKey = System.Environment.GetEnvironmentVariable("MY_LLM_API_KEY");
```
{: file="ApiKeyLoader.cs" }

### 4.2. 프록시 서버 아키텍처

클라이언트에서의 유출 방지를 위해 서버 측에서 API 호출을 대행하는 프록시 구조를 권장합니다.

---

## 5. 그래픽 및 성능 최적화

### 5.1. 품질 설정 (Quality Settings)

*   **Anti-Aliasing**: 계단 현상 제거.
*   **Shadow Resolution**: 그림자 정밀도 향상.
*   **VSync**: 화면 찢어짐 방지.

### 5.2. HDRP 연출 (선택 시)

*   **Depth of Field**: 피사계 심도 조절을 통한 시각적 집중.
*   **Volumetric Fog**: 공간 대기 질감 표현.
*   **Color Grading**: 장면의 톤 제어.

---

## 결론

1주차 과정을 통해 플랫폼 최적화 및 안정적인 비동기 통신 계층을 구축했습니다. 이는 고품질 AI 캐릭터 경험을 위한 기술적 기초가 됩니다.
