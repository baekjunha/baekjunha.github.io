---
title: "살아있는 AI 캐릭터 구현 가이드 (1): 비동기 통신 코어 구축"
date: 2025-10-09 13:11:43 +0900
categories: [Capstone, Development]
tags: [capstone, ai, unity, architecture, unitask]
image:
  path: https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/GitHub_Invertocat_Logo.svg/1200px-GitHub_Invertocat_Logo.svg.png
  alt: AI Simulation Concept
math: true
mermaid: true
---

> **요약**: '기억을 가진 살아 숨 쉬는 AI 캐릭터' 프로젝트의 1주차 핵심 과제인 비동기 통신 코어 구축과 PC 플랫폼 최적화 가이드를 다룬다. UniTask를 활용한 Non-blocking 통신 계층 설계와 고품질 그래픽을 위한 Unity 초기 설정 과정을 상세히 설명한다.
{: .prompt-info }

## 목차
* TOC
{:toc}

---

## 1. 프로젝트 초기화 및 PC 플랫폼 최적화

모든 후속 작업을 위한 안정적인 기반을 마련하는 단계다. PC 프로젝트는 초기 아키텍처 결정이 시각적 한계와 개발 방향성 전체를 규정하므로 신중한 선택이 필요하다.

### 1.1. Unity 환경 및 플랫폼 설정

성능과 그래픽 품질의 기준선을 설정하기 위해 다음 구성을 적용한다.

*   **Unity 버전**: 안정성이 검증된 **Unity 2022.3.x LTS** 버전 사용을 권장한다.
*   **Target Platform**: `File > Build Settings`에서 **PC, Mac & Linux Standalone**을 선택하고, Architecture는 **x86_64**로 설정한다.
*   **컬러 스페이스**: 물리적으로 정확한 조명 계산을 위해 `Player Settings`에서 Color Space를 **Linear**로 설정한다.

### 1.2. 렌더 파이프라인 선택 (URP vs HDRP)

PC 플랫폼에서는 시각적 품질의 상한선을 결정하는 파이프라인 선택이 중요하다.

| 비교 기준 | Universal Render Pipeline (URP) | High Definition Render Pipeline (HDRP) |
| :--- | :--- | :--- |
| **대상 하드웨어** | 전 사양 (폭넓은 사용자층) | 중-고사양 (하이엔드 지향) |
| **시각적 품질** | 양식화된 스타일에 강점 | 물리 기반의 사실적 렌더링 특화 |
| **학습 곡선** | 상대적으로 낮음 | 높고 복잡함 (물리 기반 이해 필요) |
| **주요 기능** | 범용성 및 최적화 용이 | 볼류메트릭 조명, 고급 후처리 |

> [!important]
> 두 파이프라인은 셰이더 시스템이 근본적으로 달라 상호 호환되지 않는다. 프로젝트 성격(Stylized vs Photorealistic)에 맞춰 신중히 결정해야 한다.
{: .prompt-warning }

### 1.3. UniTask 통합

현대적인 비동기 처리를 위해 **UniTask** 라이브러리를 도입한다. 이는 C# 표준 `Task`보다 Unity 환경에 최적화되어 있어, 가비지 컬렉션(GC) 발생을 최소화하고 부드러운 프레임 유지를 가능하게 한다.

#### 설치 방법
1.  [UniTask GitHub Releases](https://github.com/Cysharp/UniTask/releases)에서 최신 `.unitypackage`를 다운로드한다.
2.  다운로드한 파일을 Unity 프로젝트의 `Assets` 폴더에 임포트한다.
3.  임포트 성공 시 `Cysharp/UniTask` 폴더가 생성된 것을 확인한다.

---

-----

## 2. UniTask 기반의 현대적 비동기 프로그래밍

기존의 `IEnumerator` 코루틴 방식에서 벗어나, 현대적이고 효율적인 비동기 워크플로우를 구축한다.

### 2.1. 패러다임의 전환: 코루틴에서 async UniTask로

코루틴은 복잡한 비동기 흐름에서 콜백 지옥을 유발하고 예외 처리가 까다롭다. UniTask는 이를 선형적이고 가독성 높은 코드로 변환해준다.

#### [비교] 코루틴 vs UniTask

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
        await webRequest.SendWebRequest(); // await로 직관적 대기
        return webRequest.downloadHandler.text;
    }
}
```
{: file="AsyncComparison.cs" }

### 2.2. LLM API 클라이언트 기본 구현

UniTask를 적용한 기초적인 `LLMApiClient`를 작성한다.

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

## 3. 내결함성이 강한 네트워크 계층 설계

네트워크의 불안정성을 대비하여 타임아웃과 재시도 로직을 포함한 견고한 클라이언트를 구축한다.

### 3.1. 타임아웃 및 재시도 (Exponential Backoff)

무한 대기를 방지하는 타임아웃과, 실패 시 대기 시간을 늘려가며 다시 시도하는 '지수 백오프' 전략을 적용한다.

> [!tip]
> 기술적 실패를 AI 캐릭터의 '생각하는 시간'으로 서사화하면 몰입감을 해치지 않고 오류를 처리할 수 있다.
{: .prompt-tip }

### 3.2. RobustApiClient 구현 예시

```csharp
public async UniTask<string> SendWithRetryAsync(string prompt, CancellationToken ct) {
    int maxRetries = 3;
    for (int i = 0; i < maxRetries; i++) {
        try {
            // 10초 타임아웃 설정
            using (var timeoutCts = new CancellationTokenSource(TimeSpan.FromSeconds(10)))
            using (var linkedCts = CancellationTokenSource.CreateLinkedTokenSource(ct, timeoutCts.Token)) {
                return await SendMessageAsync(prompt, linkedCts.Token);
            }
        } catch (Exception) when (i < maxRetries - 1) {
            // 지수 백오프 + 지터(Jitter) 적용
            int delay = (int)Math.Pow(2, i) * 500 + UnityEngine.Random.Range(0, 250);
            await UniTask.Delay(delay, cancellationToken: ct);
        }
    }
    throw new Exception("모든 재시도 실패");
}
```
{: file="RobustApiClient.cs" }

---

-----

## 4. 안전한 API 키 관리 전략

LLM API 키 유출은 금전적 손실로 이어질 수 있으므로, 다층적인 보안 전략을 수립해야 한다.

### 4.1. 개발 환경: 환경 변수(Environment Variable) 활용

소스 코드에 API 키를 하드코딩하는 것은 금기다. 가장 기본적인 보안 조시는 환경 변수를 통해 키를 참조하는 것이다.

```csharp
string apiKey = null;
#if UNITY_EDITOR
    // OS 환경 변수에서 키를 읽어옴
    apiKey = System.Environment.GetEnvironmentVariable("MY_LLM_API_KEY");
#endif

if (string.IsNullOrEmpty(apiKey)) {
    Debug.LogError("API 키를 찾을 수 없습니다. 환경 변수를 설정하세요.");
}
```
{: file="ApiKeyLoader.cs" }

### 4.2. 프로덕션 환경: 프록시 서버 아키텍처

배포용 빌드에서는 클라이언트 측 암호화만으로 보안을 보장할 수 없다. 따라서 다음과 같은 프록시 구조를 권장한다.

1.  **클라이언트**: API 키 없이 백엔드 서버에 요청을 보낸다.
2.  **프록시 서버**: 안전한 서버 환경에서 API 키를 보관하며, 대신 LLM API를 호출한다.
3.  **검증**: 서버에서 응답을 정제하여 클라이언트에 전달한다.

> [!warning]
> 클라이언트 디컴파일을 통해 암호화 키와 로직이 노출될 수 있으므로, 중요한 서비스라면 반드시 프록시 서버를 구축해야 한다.
{: .prompt-warning }

---

## 5. PC 플랫폼 그래픽 및 성능 최적화

PC 하드웨어의 성능을 활용하여 AI 캐릭터와의 교감을 극대화하는 시각적 완성도를 달성한다.

### 5.1. 시각적 완성도를 위한 품질 설정 (Quality Settings)

`Project Settings > Quality`에서 고품질 경험을 위한 핵심 항목을 구성한다.

*   **Anti-Aliasing**: 계단 현상을 제거하여 깔끔한 캐릭터 실루엣을 구현한다.
*   **Shadow Resolution**: 그림자의 해상도를 높여 장면에 깊이감을 더한다.
*   **VSync**: 화면 찢어짐(Screen Tearing)을 방지하여 부드러운 화면 이동을 보장한다.

### 5.2. HDRP 기반 몰입형 연출 (HDRP 선택 시)

*   **피사계 심도 (Depth of Field)**: AI 캐릭터에 초점을 맞추고 배경을 흐리게 하여 플레이어의 시선을 집중시킨다.
*   **볼류메트릭 안개**: 빛의 산란을 표현하여 공간의 공기감을 형성한다.
*   **컬러 그레이딩**: 장면의 전체적인 색조를 조절하여 대화의 감성적 톤을 설정한다.

---

## 결론: 지속 가능한 AI 캐릭터 개발을 위한 초석

1주차 과정을 통해 PC 플랫폼에 최적화된 견고한 비동기 통신 계층을 구축했다.

*   **UniTask**: 제로 할당 비동기로 프레임 드랍 방지
*   **회복탄력성**: 타임아웃과 지수 백오프로 네트워크 안정성 확보
*   **보안**: 환경 변수와 프록시 기반의 API 키 관리 전략 수립
*   **시각적 토대**: PC 하드웨어를 고려한 고품질 그래픽 설정 적용

이러한 기술적 초석 위에서 비로소 '살아 숨 쉬는 AI'라는 몰입감 있는 경험을 쌓아 올릴 수 있다.

---

## 참고 자료

*   [Unity PC Build Settings Manual](https://docs.unity3d.com/2020.1/Documentation/Manual/BuildSettingsStandalone.html)
*   [UniTask Documentation](https://github.com/Cysharp/UniTask)
*   [Unity URP vs HDRP Guide](https://unity.com/features/srp/high-definition-render-pipeline)
*   [Exponential Backoff and Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)