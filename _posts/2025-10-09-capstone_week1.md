---
published: False
title: "살아있는 AI 캐릭터 구현 가이드(1)"
categories: capstone
tags: [capstone, ai, unity, guide]
date: 2025-10-09 13:11:43 +0900
toc: true
toc_sticky: true
author_profile: false
use_math: true 
thumbnail: https://mastermixmovies.wordpress.com/wp-content/uploads/2017/10/2001.gif?w=1241&h=546
---
## 1주차 AI 사회관계 시뮬레이션: 프로덕션급 비동기 통신 코어 구축 마스터 가이드

### 서론: 단순한 시작을 넘어 - 살아 숨 쉬는 AI를 위한 기술적 초석 다지기

본 1주차 구현 가이드는 '기억을 가진 살아 숨 쉬는 AI 캐릭터'라는 프로젝트의 핵심 철학을 현실로 구현하기 위한 첫 번째이자 가장 중요한 단계에 집중한다. 1주차의 기술적 과제들은 단순히 프로젝트를 시작하는 준비 단계를 넘어, 플레이어가 AI 캐릭터와 맺는 유대감의 기반이 되는 '환상'을 공학적으로 창조하는 과정이다.

프로젝트의 궁극적인 성공은 플레이어가 AI 캐릭터를 살아있는 존재로 인식하는 몰입감에 달려 있다. 그리고 이 몰입감은 아주 작은 기술적 결함만으로도 산산조각 날 수 있다. 기존의 모바일 환경에서는 대화 중 발생하는 미세한 화면 끊김이나 예측 불가능한 지연 시간이 주된 위험이었다면, PC 플랫폼에서는 여기에 더해 시각적 결함 - 예를 들어 화면 찢어짐(screen tearing), 불안정한 프레임률, 거친 폴리곤 가장자리(aliasing) - 까지도 몰입을 해치는 치명적인 요소로 작용한다. 플레이어는 기술적 한계가 느껴지는 가상 세계 속 캐릭터와 깊은 유대감을 형성할 수 없다.

따라서 이번 주에 구축할 안정적이고, 반응성이 뛰어나며, 막힘없는 (Non-blocking) 통신 계층은 프로젝트의 예술적, 경험적 목표를 달성하기 위한 기술적 전제 조건이다. 이와 동시에, PC의 강력한 하드웨어 성능을 십분 활용하여 시각적 완성도를 극대화하는 것은 감성적 핵심을 지탱하는 또 다른 기반이 된다.

본 가이드는 '끊김 없는 사용자 경험과 시각적 탁월함을 위한 기술적 토대'를 마련하여, 견고한 기반 위에서만 진정으로 믿을 수 있는 AI가 탄생할 수 있도록 안내할 것이다.

-----

### 섹션 1: 프로젝트 초기화 및 의존성 구성 (PC 플랫폼 최적화)

모든 후속 작업을 위한 안정적이고 올바른 기반을 마련하기 위해 Unity 프로젝트를 준비하는 실질적인 첫 단계를 안내한다. 이 초기 설정 단계에서 내리는 결정들은 단순한 개인적 선호가 아니라, 성능, 그래픽 품질, 플랫폼 호환성과 관련된 미래의 위험을 사전에 완화하기 위한 의도적이고 전문적인 선택이다. 특히 PC 프로젝트는 모바일과 달리 초기 아키텍처 결정이 프로젝트의 시각적 한계와 개발 방향성 전체를 규정하므로 신중을 기해야 한다.

#### 1.1. Unity 환경 기준선 설정

프로젝트의 복잡성을 고려할 때, 안정성은 무엇보다 중요하다. 예측 불가능한 버그를 최소화하고 장기적인 유지보수성을 확보하기 위해 최신 버전보다는 **Unity 2022.3.x LTS (Long-Term Support) 버전** 사용을 권장한다. LTS 릴리스는 장기간에 걸쳐 안정성이 검증되었으므로 프로덕션 수준의 프로젝트에 가장 적합하다.

#### 1.2. 대상 플랫폼 구성: PC, Mac & Linux Standalone

프로젝트의 기반을 PC 환경에 맞추는 첫 번째 단계는 빌드 대상을 명확히 설정하는 것이다. 이는 프로젝트가 데스크톱 클래스의 CPU와 GPU 성능을 온전히 활용할 수 있도록 하는 선언과 같다.

Unity 에디터에서 `File > Build Settings`로 이동하여 Platform 목록에서 **PC, Mac & Linux Standalone**을 선택한다. 이후 다음 세부 설정을 구성한다.

  * **Target Platform**: Windows, macOS, Linux 중 주 개발 환경 및 배포 대상을 선택한다. 이 설정은 언제든지 변경할 수 있다.
  * **Architecture**: **x86\_64**를 선택한다. 이는 현대 PC 게임의 표준인 64비트 시스템을 대상으로 빌드하겠다는 의미이며, 32비트 아키텍처는 특별한 이유가 없는 한 고려하지 않는다.

이 설정은 Steam이나 Itch.io와 같은 주요 PC 게임 배포 플랫폼을 목표로 할 때 가장 일반적이고 권장되는 구성이다.

#### 1.3. 핵심 아키텍처 결정: 렌더 파이프라인 선택 (URP vs. HDRP)

PC 프로젝트에서 가장 중요하고 되돌리기 어려운 결정 중 하나는 스크립터블 렌더 파이프라인(Scriptable Render Pipeline, SRP)을 선택하는 것이다. 이 선택은 프로젝트의 시각적 품질의 상한선, 개발 워크플로우, 그리고 에셋 제작 파이프라인 전체를 결정한다.

모바일 가이드에서는 성능을 위해 URP를 당연하게 선택했지만, PC에서는 URP와 HDRP(High Definition Render Pipeline) 사이의 전략적 선택이 필요하다. 이 결정은 프로젝트 초기에 반드시 내려야 한다. 두 파이프라인은 셰이더와 재질 시스템이 근본적으로 달라 서로 호환되지 않기 때문이다. 프로젝트가 상당히 진행된 후에 파이프라인을 변경하는 것은 사실상 프로젝트를 처음부터 다시 시작하는 것과 같은 막대한 비용을 초래할 수 있다.

  * **Universal Render Pipeline (URP)**: URP는 성능과 시각적 품질 사이의 균형을 맞춘 유연한 파이프라인이다. 광범위한 PC 하드웨어에서 안정적인 성능을 제공하며, 특히 양식화된(stylized) 아트 스타일에 더 적합하고 배우기 쉽다는 장점이 있다.
  * **High Definition Render Pipeline (HDRP)**: HDRP는 최고 수준의 시각적 충실도를 목표로 하는 하이엔드 PC 및 콘솔용 파이프라인이다. 볼류메트릭 조명, 물리적으로 정확한 하늘, 표면 아래 산란(subsurface scattering)과 같은 고급 재질, 뛰어난 시네마틱 후처리 효과 등을 기본적으로 제공한다.

다음 표는 AI 연애 시뮬레이션 프로젝트의 관점에서 두 파이프라인의 장단점을 비교 분석한 것이다.

| 비교 기준 | Universal Render Pipeline (URP) | High Definition Render Pipeline (HDRP) | Al 시뮬레이션을 위한 전략적 고려사항 |
| :--- | :--- | :--- | :--- |
| **대상 하드웨어** | 저사양부터 고사양 PC까지 폭넓게 지원 | 중-고사양 PC 및 최신 콘솔 | 더 많은 사용자를 포용하려면 URP가 유리. 최고 수준의 몰입감을 소수에게 제공하려면 HDRP가 적합. |
| **시각적 충실도** | 우수하지만, 사실주의보다는 양식화된 스타일에 강점 | 최상급. 사실적인 조명과 재질 표현에 특화 | HDRP의 사실적인 렌더링은 AI 캐릭터를 '실존하는 인물'처럼 느끼게 하는 데 결정적인 역할을 할 수 있다. |
| **학습 곡선** | 상대적으로 낮고 직관적 | 높고 복잡함. 물리 기반 조명 및 노출에 대한 이해 필요 | 빠른 프로토타이핑과 개발 속도가 중요하다면 URP. 시각적 품질을 위해 학습 시간을 투자할 수 있다면 HDRP. |
| **에셋 요구사항** | 일반적인 PBR 에셋으로도 충분히 좋은 결과물 도출 가능 | 고품질 모델, 고해상도 텍스처 등 최고 수준의 에셋 필요 | 고품질 캐릭터 모델에 투자할 계획이라면, HDRP의 고급 셰이더(피부, 머리카락 등)가 그 가치를 극대화할 수 있다. |
| **고급 조명/효과** | 기본적인 볼류메트릭, 후처리 효과 제공. 확장 필요시 에셋 스토어 활용 | 볼류메트릭 안개/조명, 고급 반사, 물리 기반 하늘 등 내장 | 대화 장면의 분위기(따뜻함, 우울함, 신비로움)를 빛과 대기로 연출하는 데 HDRP가 압도적으로 유리하다. |
| **성능 오버헤드** | 상대적으로 낮음 | 높음. 최적화를 위해 더 많은 노력 필요 | URP는 안정적인 60 FPS 이상을 유지하기 용이. HDRP는 동일한 프레임률을 위해 더 높은 사양을 요구하거나 최적화 작업이 더 많이 필요. |

#### 1.4. 고품질 그래픽을 위한 초기 프로젝트 설정

렌더 파이프라인 선택 후, 프로젝트의 시각적 기준선을 설정하기 위한 몇 가지 필수 구성이 남아있다.

  * **컬러 스페이스 (Color Space)**: 더 나은 그래픽 품질과 일관된 색상 표현을 위해 `Edit > Project Settings > Player > Other Settings`에서 Color Space를 **Linear**로 설정한다. Linear 컬러 스페이스는 조명 계산을 물리적으로 정확하게 만들어 URP와 HDRP 모두에서 훨씬 더 사실적이고 일관된 결과를 보장한다.
  * **품질 설정 (Quality Settings)**: PC 사용자는 그래픽 옵션 메뉴를 기대한다. `Edit > Project Settings > Quality`로 이동하여 기본 품질 수준을 **'High' 또는 'Ultra' 프리셋**으로 설정한다.

#### 1.5. 비동기 처리의 핵심, UniTask 통합

본 프로젝트는 C\#의 현대적인 **async/await** 패턴을 전면적으로 채택하며, 이를 위해 **UniTask** 라이브러리를 도입한다. UniTask는 Unity 환경에 최적화된 제로-할당 비동기 솔루션으로, 잦은 비동기 작업에서 발생하는 가비지 컬렉션(GC)으로 인한 프레임 드랍을 방지하여 부드러운 사용자 경험을 보장한다.

UniTask를 설치하는 가장 안정적이고 권장되는 방법은 공식 Cysharp GitHub 릴리스 페이지에서 최신 버전의 `.unitypackage` 파일을 직접 다운로드하여 프로젝트에 임포트하는 것이다.

#### 1.6. 실습 가이드: PC 프로젝트 설정 및 UniTask 임포트

1.  **Unity Hub에서 새 프로젝트 생성 (URP 또는 HDRP)**

    1.  Unity Hub를 실행한다.
    2.  `Projects` 탭에서 `New project` 버튼을 클릭한다.
    3.  All templates 목록에서, 1.3 섹션의 결정에 따라 **3D (URP)** 또는 **3D (HDRP)** 템플릿을 선택한다.
    4.  프로젝트 이름과 저장 위치를 지정한다.
    5.  `Create project` 버튼을 클릭하여 프로젝트를 생성한다.

2.  **빌드 플랫폼 설정 확인**

    1.  프로젝트가 열리면, `File > Build Settings`로 이동한다.
    2.  Platform 목록에서 **PC, Mac & Linux Standalone**이 선택되어 있는지 확인한다.
    3.  **Architecture**가 **x86\_64**로 설정되어 있는지 확인한다.

3.  **프로젝트 설정 확인**

    1.  `Edit > Project Settings`로 이동한다.
    2.  `Player` 탭을 선택하고 `Other Settings` 섹션을 펼친다.
    3.  Rendering 항목 아래의 **Color Space**가 **Linear**로 설정되어 있는지 확인한다.

4.  **UniTask 패키지 임포트**

    1.  웹 브라우저에서 `https://github.com/Cysharp/UniTask/releases`로 이동한다.
    2.  가장 최신 버전의 릴리스에서 `UniTask.x.x.x.unitypackage` 파일을 다운로드한다.
    3.  다운로드한 파일을 Unity 프로젝트의 Assets 폴더로 드래그 앤 드롭한다.
    4.  `Import Unity Package` 창이 나타나면 `Import` 버튼을 클릭한다.
    5.  임포트가 완료되면 Project 창의 Assets 폴더 아래에 `Cysharp` 폴더가 생성된 것을 확인할 수 있다.

-----

### 섹션 2: UniTask를 활용한 현대적 비동기 프로그래밍 마스터하기

이제 프로젝트 설정 단계를 넘어, 레거시 코루틴 방식에서 벗어나 현대적이고 효율적인 비동기 코드를 작성하는 핵심 원칙을 다룬다. UniTask의 채택은 단순한 기술 최적화를 넘어, 프로젝트의 핵심 철학에 대한 아키텍처적 약속이다.

#### 2.1. 패러다임의 전환: IEnumerator에서 async UniTask로

`IEnumerator` 기반 코루틴은 복잡한 비동기 흐름에서 소위 '콜백 지옥(Callback Hell)'을 유발하고 예외 처리를 어렵게 만든다. `async/await`와 UniTask는 이러한 문제들을 해결하고 코드를 동기 코드처럼 깔끔하고 선형적으로 작성할 수 있게 해준다.

  * **IEnumerator 코루틴 방식:**

    ```csharp
    using UnityEngine;
    using UnityEngine.Networking;
    using System.Collections;

    public class CoroutineExample: MonoBehaviour
    {
        void Start()
        {
            StartCoroutine(GetRequest("https://api.example.com/data"));
        }

        IEnumerator GetRequest(string uri)
        {
            using (UnityWebRequest webRequest = UnityWebRequest.Get(uri))
            {
                // 요청을 보내고 응답을 기다립니다.
                yield return webRequest.SendWebRequest();

                if (webRequest.result == UnityWebRequest.Result.ConnectionError || webRequest.result == UnityWebRequest.Result.ProtocolError)
                {
                    Debug.LogError("Error: " + webRequest.error);
                }
                else
                {
                    Debug.Log("Received: " + webRequest.downloadHandler.text);
                }
            }
        }
    }
    ```

  * **async UniTask 방식:**

    ```csharp
    using UnityEngine;
    using UnityEngine.Networking;
    using Cysharp.Threading.Tasks; // UniTask 네임스페이스 추가
    using System;

    public class UniTaskExample : MonoBehaviour
    {
        async void Start()
        {
            try
            {
                string result = await GetRequestAsync("https://api.example.com/data");
                Debug.Log("Received: " + result);
            }
            catch (Exception e)
            {
                Debug.LogError("Error: " + e.Message);
            }
        }

        async UniTask<string> GetRequestAsync(string uri)
        {
            using (UnityWebRequest webRequest = UnityWebRequest.Get(uri))
            {
                // SendWebRequest()는 이제 Awaitable 객체를 반환하며, await 키워드로 기다릴 수 있습니다.
                await webRequest.SendWebRequest();

                if (webRequest.result == UnityWebRequest.Result.ConnectionError || webRequest.result == UnityWebRequest.Result.ProtocolError)
                {
                    // 실패 시 예외를 발생시켜 호출자(caller)의 catch 블록에서 처리하도록 합니다.
                    throw new Exception(webRequest.error);
                }
                return webRequest.downloadHandler.text;
            }
        }
    }
    ```
두 번째 예시는 **try-catch** 구문을 사용하여 예외를 명확하고 우아하게 처리할 수 있음을 보여준다.

#### 2.2. 성능의 중요성 : UniTask가 타협 불가능한 선택인 이유

UniTask는 구조체(struct) 기반의 값 타입(value-type)으로 구현되어, 대부분의 async 작업에서 await를 사용할 때 힙(heap) 메모리 할당이 거의 발생하지 않는다. 이는 빈번한 API 호출 시 발생할 수 있는 가비지 컬렉션(GC)으로 인한 화면 끊김 현상을 방지하여 '살아있는 존재'라는 몰입감을 지키는 데 필수적이다.

반면, C\#의 표준 `System.Threading.Tasks.Task`는 클래스(class) 기반으로, 비동기 작업마다 힙 메모리에 객체들이 할당되어 GC 부담을 가중시키고 프레임 드랍을 유발할 수 있다.

| 비교 기준 | IEnumerator 코루틴 | C\# Task | Unity Awaitable | UniTask |
| :--- | :--- | :--- | :--- | :--- |
| **메모리 할당** | 낮음 | 매 호출마다 객체 할당 (높은 GC 부담) | 인스턴스 풀링 사용, 할당 가능성 존재 | **구조체 기반, 거의 제로에 가까운 GC 발생** |
| **API/예외 처리/가독성** | 제한적, 복잡함, 낮음 | 풍부하고 표준적, 명확한 try-catch, 높음 | 제한적, 명확한 try-catch, 높음 | **다양하고 풍부한 API, 명확한 try-catch, 높음** |
| **Unity 통합성** | 높음 | Unity 싱글 스레드 환경에 부적합 | Unity 기능에 최적화 | **Unity PlayerLoop에 완벽히 통합** |

#### 2.3. 기본 LLM API 클라이언트 구현

이제 UniTask를 바탕으로 간단한 `LLMApiClient` 클래스를 작성한다.

```csharp
using UnityEngine;
using UnityEngine.Networking;
using Cysharp.Threading.Tasks;
using System;
using System.Text;
using System.Threading;

public class LLMApiClient
{
    private readonly string _apiKey;
    private readonly string _apiUrl = "YOUR_LLM_API_ENDPOINT"; // 예: https://api.openai.com/v1/chat/completions

    public LLMApiClient(string apiKey)
    {
        if (string.IsNullOrEmpty(apiKey))
        {
            throw new ArgumentNullException(nameof(apiKey), "API key cannot be null or empty.");
        }
        _apiKey = apiKey;
    }

    public async UniTask<string> SendMessageAsync(string prompt, CancellationToken ct = default)
    {
        // POST 요청을 위한 JSON 바디 생성 (API 사양에 맞게 수정 필요)
        var requestBody = new
        {
            model = "gpt-4", // 사용할 모델
            messages = new[] { new { role = "user", content = prompt } }
        };
        string jsonBody = JsonUtility.ToJson(requestBody);
        byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonBody);

        using (UnityWebRequest webRequest = new UnityWebRequest(_apiUrl, "POST"))
        {
            webRequest.uploadHandler = new UploadHandlerRaw(bodyRaw);
            webRequest.downloadHandler = new DownloadHandlerBuffer();
            webRequest.SetRequestHeader("Content-Type", "application/json");
            webRequest.SetRequestHeader("Authorization", $"Bearer {_apiKey}");

            Debug.Log("Sending message to LLM API...");

            // WithCancellation을 통해 CancellationToken을 전달하여 작업 취소를 가능하게 합니다.
            await webRequest.SendWebRequest().WithCancellation(ct);

            if (webRequest.result == UnityWebRequest.Result.ConnectionError || webRequest.result == UnityWebRequest.Result.ProtocolError)
            {
                Debug.LogError($"API Error: {webRequest.error} | Response Code: {webRequest.responseCode}");
                throw new Exception($"LLM API request failed: {webRequest.error}");
            }
            
            // 이 예제에서는 전체 응답 텍스트를 반환합니다.
            return webRequest.downloadHandler.text;
        }
    }
}
```

#### 2.4. 실습 가이드: LLMApiClient 테스트용 MonoBehaviour 작성

1.  **LLMApiClient 스크립트 생성**

    1.  `Scripts` 폴더에 `LLMApiClient.cs` 파일을 생성한다.
    2.  위 2.3 섹션의 코드를 붙여넣는다.
    3.  `_apiUrl` 변수의 값을 실제 LLM API의 엔드포인트 URL로 변경한다.

2.  **테스트용 ApiClientTester 스크립트 생성**

    1.  `Scripts` 폴더에 `ApiClientTester.cs`라는 새 C\# 스크립트를 생성한다.
    2.  다음 코드를 붙여넣는다.
        ```csharp
        using UnityEngine;
        using Cysharp.Threading.Tasks;
        using System;

        public class ApiClientTester : MonoBehaviour
        {
            private string _apiKey = "YOUR_API_KEY_HERE";
            private string _testPrompt = "Hello, world!";
            private LLMApiClient _client;

            void Start()
            {
                if (string.IsNullOrEmpty(_apiKey) || _apiKey == "YOUR_API_KEY_HERE")
                {
                    Debug.LogError("API Key is not set in the ApiClientTester component.");
                    return;
                }
                _client = new LLMApiClient(_apiKey);
                SendMessageToAI().Forget();
            }

            private async UniTaskVoid SendMessageToAI()
            {
                Debug.Log($"Sending prompt: '{_testPrompt}'");
                try
                {
                    string response = await _client.SendMessageAsync(_testPrompt, this.GetCancellationTokenOnDestroy());
                    Debug.Log("Received response from AI: " + response);
                }
                catch (Exception e)
                {
                    Debug.LogError("Failed to get response from AI: " + e.Message);
                }
            }
        }
        ```

3.  **씬(Scene) 설정 및 테스트**

    1.  Hierarchy 창에서 빈 게임 오브젝트를 생성하고, 이름을 `AlTester`로 변경한다.
    2.  `AlTester` 게임 오브젝트에 `ApiClientTester` 스크립트를 추가한다.
    3.  `ApiClientTester` 컴포넌트의 Api Key 필드에 실제 LLM API 키를 입력한다.
    4.  씬을 실행하고 Console 창에서 응답이 정상적으로 출력되는지 확인한다.

-----

### 섹션 3: 프로덕션 수준의 내결함성을 갖춘 네트워크 계층 설계

2단계에서 만든 기본 클라이언트를 네트워크의 본질적인 불안정성을 우아하게 처리하는 견고하고 회복탄력성 있는 클라이언트로 발전시킨다.

기술적 실패를 서사적 기회로 전환할 수 있다. 예를 들어, 네트워크 타임아웃 발생 시, 기술적 오류 메시지 대신 "음... 그건 좀 깊이 생각해봐야겠는걸?"과 같이 AI 캐릭터의 개성이 담긴 대사를 출력할 수 있다. 이는 기술적 결함을 AI 캐릭터의 자연스러운 '생각하는 시간'으로 인식시켜 몰입 경험으로 전환시킨다.

#### 3.1. 응답 없는 요청 정복: 타임아웃 구현

LLM API 호출이 무한정 대기 상태에 빠지는 것을 방지하기 위해 모든 API 호출에 타임아웃을 적용한다. 이는 `CancellationTokenSource`를 사용하여 구현할 수 있다.

#### 3.2. 지능형 재시도: 지수 백오프와 지터

일시적인 네트워크 오류 발생 시, 즉시 재시도하는 대신 재시도 간의 대기 시간을 점차 늘리는 **'지수 백오프(Exponential Backoff)'** 전략을 사용한다. 여기에 재시도 간격에 무작위성을 더하는 \*\*'지터(Jitter)'\*\*를 추가하여 여러 클라이언트의 동시 요청으로 인한 서버 부하를 방지한다.

다음은 타임아웃과 지능형 재시도 로직이 통합된 최종 `RobustApiClient` 코드이다.

```csharp
using System;
using System.Threading;
using Cysharp.Threading.Tasks;
using UnityEngine;

public class RobustApiClient
{
    private const int MAX_RETRIES = 3;
    private const int BASE_DELAY_MS = 500;
    private static readonly System.Random random = new System.Random();

    public async UniTask<string> SendApiRequestAsync(string prompt, CancellationToken externalCt = default)
    {
        for (int i = 0; i < MAX_RETRIES; i++)
        {
            // 각 시도마다 10초 타임아웃을 위한 CancellationTokenSource 생성
            using (var timeoutCts = new CancellationTokenSource(TimeSpan.FromSeconds(10)))
            // 외부 CancellationToken과 타임아웃 CancellationToken을 연결
            using (var linkedCts = CancellationTokenSource.CreateLinkedTokenSource(externalCt, timeoutCts.Token))
            {
                try
                {
                    // 이 예제에서는 실제 요청 대신 딜레이로 시뮬레이션합니다.
                    await UniTask.Delay(200, cancellationToken: linkedCts.Token); 
                    return "Success";
                }
                catch (OperationCanceledException)
                {
                    // 타임아웃이 발생했는지, 아니면 외부에서 취소했는지 확인
                    if (timeoutCts.IsCancellationRequested)
                    {
                        Debug.LogWarning($"Attempt {i + 1}: Request timed out.");
                        if (i >= MAX_RETRIES - 1) throw new TimeoutException("API request timed out after all retries.");
                    }
                    else
                    {
                        // 외부에서 취소된 경우, 재시도 없이 즉시 예외를 다시 던짐
                        throw;
                    }
                }
                catch (Exception ex)
                {
                    Debug.LogWarning($"Attempt {i + 1}: Request failed: {ex.Message}");
                    if (i >= MAX_RETRIES - 1) throw; // 마지막 시도 후 실패 시 예외를 다시 던짐
                }
            }
            // Exponential Backoff with Jitter
            int delay = (int)Math.Pow(2, i) * BASE_DELAY_MS;
            int jitter = random.Next(0, delay / 2);
            await UniTask.Delay(delay + jitter, cancellationToken: externalCt);
        }
        throw new Exception("API request failed after all retries.");
    }
}
```

#### 3.3. 실습 가이드: 타임아웃 및 재시도 정책 적용 및 테스트

1.  **RobustApiClient 스크립트 생성**

    1.  기존 `LLMApiClient.cs` 파일의 이름을 `RobustApiClient.cs`로 변경하거나 새로 생성한다.
    2.  위 3.2 섹션의 `RobustApiClient` 클래스 코드를 붙여넣는다.

2.  **ApiClientTester 스크립트 수정**

    1.  `ApiClientTester.cs`를 열고 `LLMApiClient` 대신 `RobustApiClient`를 사용하도록 수정한다.
        ```csharp
        // private LLMApiClient client; -> 
        private RobustApiClient client;

        // client = new LLMApiClient(_apiKey); -> 
        client = new RobustApiClient(); 

        // string response = await _client.SendMessageAsync(_testPrompt,...); -> 
        string response = await client.SendApiRequestAsync(_testPrompt, ...);
        ```

3.  **네트워크 오류 시뮬레이션 및 테스트**

    1.  **타임아웃 테스트**: `RobustApiClient.cs`에서 `TimeSpan.FromSeconds(10)`을 `TimeSpan.FromMilliseconds(1)`로 변경하여 타임아웃을 강제로 발생시킨다.
    2.  **재시도 테스트**: `RobustApiClient.cs`의 `try` 블록 안에서 `throw new Exception("Simulated network error");` 코드를 추가하여 네트워크 오류를 강제로 시뮬레이션한다.

-----

### 섹션 4: 안전한 API 키 관리를 위한 다층적 전략

LLM API 키는 프로젝트의 가장 민감한 자산 중 하나로, 유출 시 막대한 금전적 손실로 이어질 수 있다.

#### 4.1. 로컬 개발: 안전하고 간단한 환경 변수 활용

개발 과정에서 API 키를 소스 코드에 직접 하드코딩하는 것은 심각한 보안 취약점이다. 이를 방지하기 위한 가장 기본적인 보안 조치는 로컬 머신의 **환경 변수**를 사용하는 것이다.

  * **코드에서 사용법:**
    ```csharp
    string apiKey = null;
    #if UNITY_EDITOR
        apiKey = System.Environment.GetEnvironmentVariable("MY_LLM_API_KEY");
    #endif

    if (string.IsNullOrEmpty(apiKey))
    {
        Debug.LogError("API Key not found. Please set the MY_LLM_API_KEY environment variable.");
    }
    ```

#### 4.1.1. 실습 가이드: 환경 변수 설정 및 코드 연동

1.  **운영체제에 환경 변수 설정**

      * **Windows 사용자**:
        1.  `sysdm.cpl` 실행 → `고급` 탭 → `환경 변수` 버튼 클릭.
        2.  `사용자 변수` 섹션에서 `새로 만들기` 클릭.
        3.  변수 이름에 `MY_LLM_API_KEY`, 변수 값에 실제 API 키를 입력.
        4.  Unity Hub와 Unity Editor를 완전히 재시작.
      * **macOS 사용자**:
        1.  터미널 앱 실행.
        2.  `nano ~/.zshrc` 실행 (사용하는 셀에 따라 다를 수 있음).
        3.  파일 맨 아래에 `export MY_LLM_API_KEY="your_api_key_here"` 라인 추가.
        4.  저장 후 `source ~/.zshrc` 명령어 실행.
        5.  Unity Hub와 Unity Editor를 완전히 재시작.

2.  **ApiClientTester에서 환경 변수 사용**

      * `ApiClientTester.cs` 스크립트에서 Inspector 필드 대신 환경 변수에서 API 키를 읽어오도록 변경한다.

#### 4.2. 프로덕션 보안: 프록시 아키텍처로의 전환

공개적으로 배포되는 상용 제품의 경우, 클라이언트가 직접 LLM API를 호출하는 모델은 근본적으로 안전하지 않다. 악의적인 사용자는 언제든지 클라이언트를 디컴파일하여 API 키를 추출할 수 있다.

따라서 프로덕션 환경에서는 서버 측 **프록시(Proxy) 아키텍처**로 전환해야 한다.

  * **프록시 아키텍처의 작동 방식**:
    1.  **클라이언트 요청**: 게임 클라이언트는 API 키 없이 자체 백엔드 서버(프록시)에 요청을 보낸다.
    2.  **서버 측 처리**: 프록시 서버가 안전한 저장소에서 API 키를 검색하여 LLM API를 직접 호출한다.
    3.  **응답 반환**: 프록시 서버는 LLM API로부터 받은 응답을 다시 게임 클라이언트로 전달한다.

#### 4.3. 대안 분석 (권장하지 않음): 클라이언트 측 암호화의 함정

API 키를 암호화하여 게임 빌드에 포함시키는 방법은 '보안을 통한 은닉(security through obscurity)'에 불과하다. 악의적인 사용자가 클라이언트를 디컴파일하면 암호화된 데이터와 복호화 로직을 모두 찾아내 원본 API 키를 추출할 수 있다.

-----

### 섹션 5 (신규): 고품질 PC 경험을 위한 그래픽 및 성능 최적화

이 섹션에서는 PC 플랫폼의 성능을 활용하여 AI 캐릭터와의 교감을 극대화하는 시각적 요소를 설정하고 최적화하는 방법을 다룬다.

#### 5.1. Quality Settings 심층 분석

PC 플레이어는 그래픽 품질 조절 옵션을 기대한다. `Edit > Project Settings > Quality`는 이러한 옵션을 제공하기 위한 핵심 설정들을 포함하고 있다.

  * **Anti-Aliasing (안티에일리어싱)**: 폴리곤의 계단 현상을 부드럽게 처리하여 깔끔한 이미지를 만든다.
  * **Texture Quality (텍스처 품질)**: 텍스처의 최대 해상도를 제어한다. 'Full Resolution'은 가장 선명한 텍스처를 제공하지만 더 많은 비디오 메모리(VRAM)를 사용한다.
  * **Anisotropic Textures (비등방성 텍스처)**: 비스듬한 각도에서 보이는 텍스처의 선명도를 크게 향상시킨다.
  * **Shadows (그림자)**: 장면에 깊이와 사실감을 더하는 가장 중요한 요소 중 하나다. `Shadow Resolution`, `Shadow Distance`, `Shadow Cascades` 등의 설정으로 품질을 조절할 수 있다.
  * **VSync (수직 동기화)**: 화면 찢어짐(screen tearing) 현상을 방지하기 위해 게임의 프레임률을 모니터의 주사율에 맞춘다.

#### 5.2. HDRP를 활용한 몰입형 리얼리즘 구현 (HDRP 선택 시)

HDRP를 선택했다면, 그 고유한 기능들을 활용하여 AI 시뮬레이션의 분위기와 감성적 깊이를 한 차원 높일 수 있다.

  * **볼류메트릭 안개/조명 (Volumetric Fog/Lighting)**: 창문으로 들어오는 부드러운 빛줄기나 공기 중의 미세한 먼지를 표현하여 공간을 더 아늑하고 생동감 있게 만들 수 있다.
  * **고급 후처리 (Advanced Post-Processing)**:
      * **피사계 심도 (Depth of Field)**: AI 캐릭터에 초점을 맞추고 배경을 흐리게 처리하여 플레이어의 시선을 집중시킨다.
      * **블룸 (Bloom)**: 빛이 부드럽게 번지는 효과를 만들어 몽환적이거나 따뜻한 분위기를 연출한다.
      * **컬러 그레이딩 (Color Grading)**: 장면의 전체적인 색조를 조절하여 감정적인 톤을 설정한다.

#### 5.3. PC 환경에서의 프로파일링 및 프레임률 관리

PC 플레이어들은 60 FPS 이상의 안정적인 프레임률을 기대한다. Unity 프로파일러(`Window > Analysis > Profiler`)는 성능 병목 현상을 식별하고 해결하는 데 필수적인 도구다.

프로파일러를 사용하여 CPU 및 GPU 사용량을 주기적으로 모니터링하고, 목표 프레임률을 유지하기 위해 그래픽 설정의 균형점을 찾아야 한다.

-----

### 결론: 지속 가능한 성장을 위한 견고한 토대

1주차를 통해 PC 플랫폼에 최적화된 프로덕션 수준의 완전한 비동기 통신 계층을 설계하고 구축했다. 이 견고한 토대는 다음과 같은 핵심적인 특성을 갖추고 있다:

  * **고성능**: UniTask를 통해 GC로 인한 프레임 드랍을 회피하여 플레이어의 몰입 경험을 최우선으로 존중한다.
  * **회복탄력성**: 취소 토큰과 지수 백오프를 통해 불안정한 네트워크 환경의 오류를 우아하게 처리한다.
  * **보안성**: 개발 및 프로덕션 환경을 위한 명확하고 안전한 API 키 관리 전략과 아키텍처를 수립했다.
  * **시각적 탁월성**: PC 플랫폼의 성능을 활용하기 위한 고품질 그래픽 설정 가이드를 통해 시각적 경험의 토대를 마련했다.

진정으로 '살아 숨 쉬는 AI'를 만들기 위한 가장 중요한 기술적 초석이 마련되었다.

-----

### 참고 자료

1.  PC, Mac & Linux Standalone build settings - Unity - Manual, [https://docs.unity3d.com/2020.1/Documentation/Manual/BuildSettingsStandalone.html](https://docs.unity3d.com/2020.1/Documentation/Manual/BuildSettingsStandalone.html) 
2.  Manual: Build Settings - Unity, [https://docs.unity.cn/2019.1/Documentation/Manual/BuildSettings.html](https://docs.unity.cn/2019.1/Documentation/Manual/BuildSettings.html) 
3.  PC, Mac & Linux Standalone build settings - Unity Manual, [https://docs.unity.cn/ru/2020.1/Manual/BuildSettingsStandalone.html](https://docs.unity.cn/ru/2020.1/Manual/BuildSettingsStandalone.html) 
4.  What is the difference between these platforms: PC, Mac, Linux Standalone / Windows Build Support (IL2CPP) / Universal Windows Platform Build Support?: r/Unity3D - Reddit, [https://www.reddit.com/r/Unity3D/comments/qcz09a/what\_is\_the\_difference\_between\_these\_platforms\_pc/](https://www.reddit.com/r/Unity3D/comments/qcz09a/what_is_the_difference_between_these_platforms_pc/) 
5.  [Answered] What are the differences between Unitys URP and HDRP?, [https://www.dragonflydb.io/faq/unity-urp-vs-hdrp](https://www.dragonflydb.io/faq/unity-urp-vs-hdrp) 
6.  Spent a few weeks rewriting everything from HDRP to URP: r/Unity3D - Reddit, [https://www.reddit.com/r/Unity3D/comments/1midj89/spent\_a\_few\_weeks\_rewriting\_everything\_from\_hdrp/](https://www.reddit.com/r/Unity3D/comments/1midj89/spent_a_few_weeks_rewriting_everything_from_hdrp/) 
7.  URP or HDRP? : r/Unity3D - Reddit, [https://www.reddit.com/r/Unity3D/comments/yvz6fa/urp\_or\_hdrp/](https://www.reddit.com/r/Unity3D/comments/yvz6fa/urp_or_hdrp/) 
8.  High Definition Render Pipeline (HDRP) - Unity, [https://unity.com/features/srp/high-definition-render-pipeline](https://unity.com/features/srp/high-definition-render-pipeline) 
9.  Introduction to HDRP - Unity Learn, [https://learn.unity.com/tutorial/introduction-to-hdrp-2019](https://learn.unity.com/tutorial/introduction-to-hdrp-2019) 
10. Why shouldn't I go with HDRP for every project?: r/Unity3D - Reddit, [https://www.reddit.com/r/Unity3D/comments/1cee5bl/why\_shouldnt\_i\_go\_with\_hdrp\_for\_every\_project/](https://www.reddit.com/r/Unity3D/comments/1cee5bl/why_shouldnt_i_go_with_hdrp_for_every_project/) 
11. Standalone build - Make the build in Unity - Flightmare documentation - Read the Docs, [https://flightmare.readthedocs.io/en/latest/building\_flightmare\_binary/standalone.html](https://flightmare.readthedocs.io/en/latest/building_flightmare_binary/standalone.html) 
12. Quality settings tab reference - Unity - Manual, [https://docs.unity3d.com/6000.2/Documentation/Manual/class-QualitySettings.html](https://docs.unity3d.com/6000.2/Documentation/Manual/class-QualitySettings.html) 
13. Low graphics after build settings: r/unity - Reddit, [https://www.reddit.com/r/unity/comments/174w6yw/low\_graphics\_after\_build\_settings/](https://www.reddit.com/r/unity/comments/174w6yw/low_graphics_after_build_settings/) 
14. Quality Settings - Unity - Manual, [https://docs.unity3d.com/2018.1/Documentation/Manual/class-QualitySettings.html](https://docs.unity3d.com/2018.1/Documentation/Manual/class-QualitySettings.html) 
15. Performance optimization for high-end graphics on PC and console - Unity, [https://unity.com/how-to/performance-optimization-high-end-graphics](https://unity.com/how-to/performance-optimization-high-end-graphics) 
16. Should I go for HDRP for a PC only game?: r/Unity3D - Reddit, [https://www.reddit.com/r/Unity3D/comments/1dkbsnn/should\_i\_go\_for\_hdrp\_for\_a\_pc\_only\_game/](https://www.reddit.com/r/Unity3D/comments/1dkbsnn/should_i_go_for_hdrp_for_a_pc_only_game/) 

---

### 실습의 목적파악

### ## 1. 실습 가이드: PC 프로젝트 설정 및 UniTask 임포트 (섹션 1.6)

- **핵심 목표:** 이론적으로 논의된 프로젝트의 '설계도'를 실제 유니티 프로젝트 파일로 구현하는 것입니다
- **문맥적 이유 (왜 이 시점에?):** 섹션 1은 프로젝트의 성공을 위해 가장 먼저 내려야 할 중요한 아키텍처 결정들을 설명합니다. 안정적인 **LTS 버전** 사용, 고품질 그래픽을 위한 **PC 플랫폼** 타겟팅, 시각적 방향을 결정하는 **렌더 파이프라인(URP/HDRP)** 선택, 그리고 끊김 없는 경험을 위한 비동기 라이브러리 **UniTask** 도입의 필요성을 강조했죠. 이 실습은 이러한 **이론적 선택들을 실제 행동으로 옮겨 프로젝트의 뼈대를 세우는 첫 단계**입니다. 마치 건물을 짓기 전, 설계도에 따라 땅을 고르고 정확한 자재(UniTask)를 가져와 기초 공사를 하는 것과 같습니다.
- **기대 효과:** 개발자는 앞으로의 모든 작업이 진행될, 안정적이고 올바른 기술적 토대 위에서 시작할 수 있다는 확신을 갖게 됩니다.

---

### ## 2. 실습 가이드: LLMApiClient 테스트용 MonoBehaviour 작성 (섹션 2.4)

- **핵심 목표:** UniTask를 활용한 현대적 비동기 코드(LLMApiClient)가 실제 유니티 환경에서 정말로 '작동'하는지 확인하는 것입니다.
- **문맥적 이유 (왜 이 시점에?):** 섹션 2는 기존의 복잡한 코루틴 방식에서 벗어나, `async/await`와 UniTask를 사용하는 것이 왜 코드 가독성과 성능(GC 최소화) 면에서 우월한지를 설명했습니다. 그리고 그 예시로 `LLMApiClient`라는 네트워크 통신 코드를 제시했죠. 이 실습은 **이론으로만 봤던 코드가 실제 유니티의 생명주기(`Start` 함수) 안에서 문제없이 실행되는지 직접 눈으로 확인하는 과정**입니다. 즉, 새로 배운 비동기 프로그래밍 패러다임에 대한 **최초의 동작 검증(Smoke Test)**인 셈입니다.
- **기대 효과:** 개발자는 UniTask 기반 비동기 코드를 유니티 오브젝트에 적용하고 실행하는 기본적인 방법을 체득하고, 해당 방식이 문제없이 작동함을 확인하여 자신감을 얻습니다.

---

### ## 3. 실습 가이드: 타임아웃 및 재시도 정책 적용 및 테스트 (섹션 3.3)

- **핵심 목표:** '실패를 대비해 설계한' 코드가 실제 실패 상황에서 의도대로 동작하는지 **직접 실패를 시뮬레이션하여 증명**하는 것입니다.
- **문맥적 이유 (왜 이 시점에?):** 섹션 3은 네트워크는 언제나 불안정할 수 있다는 현실을 직시하고, 타임아웃, 지수 백오프, 지터 같은 고급 예외 처리 기법을 도입하여 어떤 상황에서도 프로그램이 멈추거나 무너지지 않는 '강건한(Robust)' 클라이언트를 만드는 법을 다뤘습니다. 이 실습은 단순히 코드를 따라 치는 것을 넘어, **일부러 타임아웃과 네트워크 오류를 발생시켜 우리가 만든 안전장치가 실제로 작동하는지 시험해보는 과정**입니다. 이는 코드에 대한 **내결함성을 증명하는 일종의 '소방 훈련'**과 같습니다.
- **기대 효과:** 개발자는 예외 처리 로직이 실제로 어떻게 작동하는지 로그를 통해 직접 확인하며, 예측 불가능한 네트워크 문제에 대응할 수 있는 견고한 코드를 만들었다는 신뢰를 얻게 됩니다.

---

### ## 4. 실습 가이드: 환경 변수 설정 및 코드 연동 (섹션 4.1.1)

- **핵심 목표:** 민감한 정보(API 키)를 소스 코드로부터 분리하는 가장 기본적인 보안 원칙을 실제로 적용하는 방법을 배우는 것입니다.
- **문맥적 이유 (왜 이 시점에?):** 섹션 4는 API 키를 코드에 그대로 적어두는 것이 얼마나 위험한지 경고하며, Git 같은 버전 관리 시스템에 키가 노출되는 것을 막기 위한 첫걸음으로 '환경 변수' 활용을 제시했습니다 . 이 실습은 **프로젝트의 보안을 강화하기 위한 첫 번째 실천**입니다. 자신의 컴퓨터(로컬 환경)에만 키를 저장하고, 코드는 그 키를 참조만 하도록 만드는 과정을 직접 경험하게 합니다. 이는 **프로젝트의 '현관문을 잠그는' 가장 기초적이면서도 필수적인 보안 습관**을 들이는 단계입니다.
- **기대 효과:** 개발자는 소스 코드에 민감한 정보를 포함하지 않고 안전하게 관리하는 전문적인 개발 방식을 익히고, 프로젝트 보안의 첫 단계를 성공적으로 구축하게 됩니다.