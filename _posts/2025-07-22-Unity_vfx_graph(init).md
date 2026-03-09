---
categories: graphics
tags: [graphics, unity, vfx, particle, shader]
toc: true
toc_sticky: true
author_profile: false
use_math: true   
thumbnail: https://unity.com/_next/image?url=https%3A%2F%2Fcdn.sanity.io%2Fimages%2Ffuvbjjlp%2Fproduction%2F19d1656d78819d6634202b73c53c29a6e2933353-811x455.png&w=3840&q=100
---

# Unity VFX Graph - Initialize Context 정리

> **참고 링크**: [URP VFX Learning Templates (1) - 어제와 내일의 나 그 사이의 이야기](https://lycos7560.com/unity/urp-vfx-learning-templates-1/39596/#1-contextflow)

> **요약**: Unity VFX Graph에서 파티클 생성의 첫 관문인 **Initialize Context**의 역할과 핵심 설정(Space, Data Type, Capacity, Bounds)을 분석한다. 파티클 수명 주기의 시작점을 완벽히 통제하는 방법을 다룬다.
{: .prompt-info }

## 목차
* TOC
{:toc}

---

## 1. Initialize Context 란?

**Initialize Context**는 `Spawn Event` 또는 `GPU Event`를 전달받아 **새로운 파티클(또는 파티클 스트립)을 초기화**하는 역할을 수행한다. 파티클이 우주에 탄생하는 빅뱅의 순간과 같다.

### 1.1. 파티클 실행 흐름 (Flow)

파티클 시스템은 다음과 같은 단방향 라이프사이클을 거친다.

```mermaid
graph LR
    A[Spawn Event] --> B[Initialize Context]
    B --> C[Update Context]
    C --> D[Output Context]
    
    style B fill:#f9f,stroke:#333,stroke-width:4px
```

### 1.2. 주요 특징
*   파티클이 처음 생성될 때 **단 한 번만** 실행된다. 초기 로켓 발사의 각도와 연료를 세팅하는 작업이다.
*   이후 프레임 단위의 연산은 `Update Context`와 `Output Context`로 흐름이 이양된다.

### 1.3. 용어 설명
*   **파티클(Particle)**: 독립적으로 짧은 수명을 가지는 단일 시각적 효과 단위 (불꽃, 연기, 먼지 등).
*   **파티클 스트립(Particle Strip)**: 파티클이 선형 체인 구조로 이어진 형태 (검기, 투사체 꼬리, 빛줄기 궤적 등).

---

## 2. 메뉴 접근 경로

VFX Graph 에디터 작업 공간에서 Node를 추가할 때 다음 경로를 따른다.
*   **Context → Initialize Particle**

---

## 3. 핵심 설정 항목 (Context Settings)

Initialize Context Block의 인스펙터 속성을 뜯어보자.

### 3.1. Space (시뮬레이션 좌표계)

| 옵션 | 설명 | 사용 예시 |
| :--- | :--- | :--- |
| **Local** | 이펙트가 부모 게임오브젝트의 Transform (위치/회전)에 완전히 종속된다. | 캐릭터 손끝에 매달려 같이 움직이는 마법 진 형태 |
| **World** | 파티클이 한 번 스폰되면 부모가 이동해도 그 자리에 잔류한다. | 자동차 머플러에서 뿜어져 나와 허공에 흩어지는 배기가스 |

### 3.2. Data Type (파티클 위상)

이펙트가 렌더링할 기하학적 형태의 본질을 결정한다.

| 옵션 | 설명 | 시각적 특징 |
| :--- | :--- | :--- |
| **Particle** | 독립적인 점 기반 파티클 | 파편들이 각자 흩날림 |
| **Particle Strip** | 하나의 연속된 면/선으로 이어진 파티클 띠 | 부드럽게 이어지는 곡선 궤적 |

### 3.3. Capacity (최대 파티클 수용량)

*   전체 시뮬레이션 라이프사이클에서 동시에 존재할 수 있는 **최대 파티클 개수(UInt)** 다.
*   GPU 메모리 페이징 사이즈를 결정하는 제일 중요한 척도다. 이 값을 낭비하면 프로젝트 성능(FPS)이 급하강한다. 메모리 오버플로우를 막는 안전핀 역할도 한다.

### 3.4. Particle Per Strip Count (스트립 길이)

*   `Data Type`이 **Particle Strip**일 때만 활성화되는 옵션이다.
*   1개의 연속된 줄기(Strip)를 구성하는 버텍스(파티클)의 마디 개수를 조절한다. 늘어날수록 곡선이 둥글고 부드러워진다.

### 3.5. Bounds Setting Mode (컬링 바운딩 박스)

이펙트가 차지하는 **3차원 공간 범위(AABB, Axis-Aligned Bounding Box)** 를 계산하는 방식을 지정한다. 이 상자를 카메라 렌즈(Frustum)가 쳐다보지 않으면 Unity는 파티클 렌더링 자체를 통째로 스킵(Culling)하여 성능을 확보한다.

| 옵션 | 설명 | 장점 | 단점 |
| :--- | :--- | :--- | :--- |
| **Manual** | X, Y, Z 사이즈를 사용자가 직접 고정 타이핑한다. | 오버헤드가 없고 성능이 가장 압도적이다. | 파티클이 박스 밖으로 튀어나가면 투명해진다. |
| **Recorded** | 에디터에서 플레이를 눌러 움직임 궤적을 샘플링 녹화하여 크기를 확정한다. | 자동화되어 편하고 런타임 계산 비용이 없다. | 랜덤성이 강해 범위가 그때그때 다른 이펙트엔 부적합하다. |
| **Automatic** | 매 프레임 GPU가 파티클들의 최대 분포 경계를 직접 계산한다. | 절대 파티클이 화면에서 짤릴 일이 없다. | 매 프레임 추가 연산 지연시간이 발생한다. (비추천) |

> [!important]
> 최적화를 위해서는 `Recorded`로 베이스라인 박스를 딴 뒤, 여유 공간(Padding)을 살짝 주어 `Manual` 로 고정해두는 것이 AAA급 게임 개발의 국룰(Best Practice)이다.

---

## 4. Input 속성

Initialize Context 블록 상단에 노출되는 외부 입력 포트들이다.

### 4.1. Bounds (AABox)
*   Manual 모드일 때 이펙트가 노는 최대의 놀이터 영역 박스 셰이프를 정의한다.

### 4.2. Bounds Padding (Vector3)
*   Record를 땄거나 수동으로 맞춘 바운딩 박스 표면에 **여유 마진(Margin) 두께 공간**을 덧댐 처리한다.
*   카메라를 휙 돌릴 때 경계선에 걸친 파티클이 억울하게 컬링(시야 밖 삭제 처리) 당하는 팝핑(Popping) 이슈를 방어하는 용도다.

### 4.3. Culling Flags (시스템 세팅)

에셋 글로벌 세팅에서 카메라 판별을 어떻게 할지 정한다.
*   **Off**: 무조건 그린다. (GUI 같은 특수 목적 아니면 절대 쓰지 말 것)
*   **Based On Bounds**: 정직하게 Ба운딩 박스가 카메라 시야(Frustum) 절두체에 걸치는지 검사한다. (기본값)
*   **Always**: 무조건 그리지 않는다. (그래프 로직만 태우고 눈으로 볼 필요 없을 때 쓰는 디버깅용)

---

## 5. 상세 동작 원리와 제약사항

### 5.1. Overspawn 방지 설계
Initialize Context 내부에 Block 노드를 우클릭해 추가하면 파티클의 초기 Color, Velocity, Position 등을 맛깔나게 셋업할 수 있다.
그런데 만약 외부 `Spawn Context`가 미쳐 날뛰어서 내부에 지정해둔 `Capacity` 1000개를 초과하는 1001번째 생성 신호를 던진다면 어떻게 될까?
안전하게 **생성되지 않고 버려진다(Ignored).** 

### 5.2. Alive 속성을 이용한 즉각 처형
Initialize 블록 안에서 파티클의 시스템 속성 `Alive` 값을 `false` 로 덮어씌우면, 파티클은 태어나자마자 **첫 숨을 쉬기도 전에 즉사(Dead) 판정**을 받는다.
*   이 기법은 조건부 `If` 로직을 태워 특정 조건에 미달하는 파티클 찌꺼기들을 Update Context 연산 루프 체인에 태우기 전 효율적으로 치워버리는 최적화 꼼수로 쓰인다.
*   단, 죽었더라도 찰나의 순간 메모리 빈 방은 할당받았던 것이므로 전체 Capacity 파이 카운트를 소모한다.

### 5.3. Source Attribute (속성 상속)
Initialize 단계에서 이전 족보의 데이터를 물려받을 수 있다.
*   `Get Attribute (Source)` Operator 노드를 쓰거나 `Inherit <Attribute>` Block을 붙이면 된다.
*   이 방식을 통해 Spawn 이벤트 발생 진원지의 좌표나 부모 파티클의 사망 직전의 속도(Velocity) 등을 고스란히 계승할 수 있다. 

---

## 6. Input Flow 호환성 주의사항 (에러 유발)

VFX Graph는 노드 선 연결에 있어 엄격한 법을 가진다.

✅ **가능한 연결 방식 (합법)**
*   여러 개의 `Spawn Context` 펄스를 다중으로 끌고 와서 하나의 Initialize에 꽂기
*   여러 개의 C# `Event Context` 를 끌어다 꽂기

❌ **혼합 금지 (불법)**
*   **CPU 기반 생태계 (Spawn/Event) 와 GPU Event 노드 선을 하나의 Initialize에 동시 타격(Mix)하면 안 된다.**

> [!warning]
> 다음과 같은 치명적인 예외(Exception)를 뱉으며 그래프 컴파일이 뻗어버린다.
> `System.InvalidOperationException: Cannot mix GPU & CPU spawners in init`

---

## 7. 결론

Initialize Context는 파티클 수명 주기 시스템의 **입국 심사대**와 같다. 이곳에서 `Capacity`라는 비자 발급량이 통제되며, `Bounds`라는 체류 구역이 정해지고, `Space`라는 물리 법칙이 적용된다. 이 설정을 대충 넘기면 겉보기엔 화려해도 내부적으로는 GPU를 살살 녹이는 최적화 폭탄 파티클이 완성되므로 각별한 주의가 필요하다.

<br/>

### 참고 및 추가 자료
*   [Unity VFX Graph 공식 Document](https://docs.unity3d.com/Packages/com.unity.visualeffectgraph@latest)
*   [VFX Graph 깃허브 Examples](https://github.com/Unity-Technologies/VisualEffectGraph-Samples)
