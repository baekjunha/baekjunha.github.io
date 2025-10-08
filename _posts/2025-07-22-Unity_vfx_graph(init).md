---
categories: graphics
tags: [graphics, unity, vfx, particle, shader]
toc: true
toc_sticky: true
author_profile: false
use_math: true 
images: 
  
thumbnail: 
---

# Unity VFX Graph - Initialize Context 정리

> **참고 링크**: [URP VFX Learning Templates (1) - 어제와 내일의 나 그 사이의 이야기](https://lycos7560.com/unity/urp-vfx-learning-templates-1/39596/#1-contextflow)

---

## Initialize란?

**Initialize Context**는 **Spawn Event** 또는 **GPU Event**를 받아서 **새로운 파티클(또는 파티클 스트립)을 초기화**하는 역할을 한다.

### 실행 흐름

```
Spawn Event → Initialize Context → Update Context → Output Context
```

**시각적 표현:**
```
┌─────────────┐    ┌─────────────────┐    ┌──────────────┐    ┌─────────────┐
│ Spawn Event │───▶│ Initialize      │───▶│ Update       │───▶│ Output      │
│             │    │ Context         │    │ Context      │    │ Context     │
└─────────────┘    └─────────────────┘    └──────────────┘    └─────────────┘
```

### 주요 특징
- 파티클이 처음 만들어질 때 **딱 한 번만** 실행된다
- 이후 Update Context와 Output Context로 흐름이 이어진다

### 용어 설명
- **파티클(Particle)**: 작고 짧게 표시되는 시각적 효과 조각 (불꽃, 연기, 먼지 등)
- **파티클 스트립(Particle Strip)**: 파티클이 선처럼 연결된 구조 (줄기, 꼬리, 빛줄기 표현)

---

## 메뉴 경로

**Context → Initialize Particle**

> VFX Graph 안에서 Context를 추가할 때 메뉴 위치

---

## 주요 설정 항목 (Context Settings)

### 1. **Space (Enum)**
시뮬레이션 공간 설정

| 옵션 | 설명 | 사용 예시 |
|------|------|-----------|
| **Local** | 이펙트가 오브젝트 위치에 따라 움직임 | 캐릭터가 움직일 때 이펙트도 따라감 |
| **World** | 이펙트가 월드 좌표계 기준으로 고정됨 | 고정된 위치에서 지속되는 이펙트 |

### 2. **Data Type (Enum)**
이펙트가 생성할 요소의 종류 선택

| 옵션 | 설명 | 시각적 표현 |
|------|------|-------------|
| **Particle** | 일반 개별 파티클 | `●●●●●` |
| **Particle Strip** | 파티클들이 서로 이어진 형태 | `●●●──●●●` |

**상세 비교:**

**Particle (개별 파티클)**
```
┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐
│●│ │●│ │●│ │●│ │●│
└─┘ └─┘ └─┘ └─┘ └─┘
```

**Particle Strip (연결된 파티클)**
```
┌─┐─┌─┐─┌─┐─┌─┐─┌─┐
│●│ │●│ │●│ │●│ │●│
└─┘─└─┘─└─┘─└─┘─└─┘
```

### 3. **Capacity (UInt)**
- 전체 시뮬레이션에서 사용할 **최대 파티클 개수**
- 이 값이 높을수록 더 많은 파티클이 만들어질 수 있지만, 성능에 영향이 있다
- > UInt는 음수가 없는 정수

### 4. **Particle Per Strip Count (UInt)**
- 한 개의 스트립 안에 들어갈 파티클 수
- 이 항목은 Data Type이 Particle Strip일 때만 나타난다

### 5. **Bounds Setting Mode (Enum)**
이펙트의 **공간 범위(바운딩 박스)**를 어떻게 정할지 결정

| 옵션 | 설명 | 장단점 |
|------|------|--------|
| **Manual** | 직접 범위 크기 지정 | 정확하지만 수동 작업 필요 |
| **Recorded** | 실행 중 이펙트 움직임을 녹화해서 자동 설정 | 자동화되지만 초기 설정 시간 필요 |
| **Automatic** | Unity가 알아서 계산해줌 | 간편하지만 정확도 떨어질 수 있음 |

#### 바운딩 박스(Bounding Box)란?
이펙트가 차지할 수 있는 **가상의 공간 크기**이다.

**시각적 표현:**

**1. 기본 바운딩 박스**
```
┌─────────────────┐
│   Bounding Box  │
│   ┌─────────┐   │
│   │ Effect  │   │
│   │ Area    │   │
│   └─────────┘   │
└─────────────────┘
```

**2. 패딩이 적용된 바운딩 박스**
```
┌─────────────────────────┐
│     Padding Area        │
│  ┌─────────────────┐    │
│  │   Bounding Box  │    │
│  │   ┌─────────┐   │    │
│  │   │ Effect  │   │    │
│  │   │ Area    │   │    │
│  │   └─────────┘   │    │
│  └─────────────────┘    │
└─────────────────────────┘
```

**3. 성능 비교**

| 설정 | 크기 | 성능 | 정확도 |
|------|------|------|--------|
| **Manual** | 사용자 정의 | 중간 | 높음 |
| **Recorded** | 자동 계산 | 높음 | 중간 |
| **Automatic** | Unity 계산 | 낮음 | 낮음 |

- 이 범위를 벗어나면 Unity는 해당 이펙트를 화면에 그리지 않는다
- 너무 작으면 이펙트가 잘릴 수 있고, 너무 크면 성능 낭비가 생긴다

---

## Input 속성

### **Bounds (AABox)**
- 이펙트가 차지할 수 있는 최대 영역
- AABox는 축에 정렬된 직육면체
- 이 값은 Visual Effect Asset의 Culling Flags 설정에 따라 평가된다

### **Bounds Padding (Vector3)**
- 바운딩 박스에 **여유 공간**을 추가할 수 있다
- 값은 x, y, z축 기준으로 얼마나 더 넓힐지를 설정한다
- 너무 작아서 효과가 잘리는 걸 방지한다

#### Culling Flags
Unity가 "카메라에 안 보이면 이펙트 계산을 생략할지"를 결정하는 기준

| 옵션 | 설명 | 성능 영향 |
|------|------|-----------|
| **Off** | 항상 그린다 | 높음 |
| **Based On Bounds** | 바운딩 박스 기준으로 잘라냄 | 중간 |
| **Always** | 무조건 생략 (디버그용) | 낮음 |

---

## 흐름 (Flow)

### **Input**
- Spawn Context
- GPU Event Context
- 일반 Event Context

### **Output**
- Update Context
- Output Context (Single 또는 Multiple)

#### Context란?
VFX Graph에서 흐름을 구성하는 블록 단위이다.

```
Spawn → Initialize → Update → Output
```

**Context 흐름:**
```
┌─────────┐    ┌─────────────┐    ┌─────────┐    ┌─────────┐
│ Spawn   │───▶│ Initialize  │───▶│ Update  │───▶│ Output  │
│         │    │             │    │         │    │         │
└─────────┘    └─────────────┘    └─────────┘    └─────────┘
```

---

## 상세 동작

### [1] **Overspawn**
- Initialize Context 안에 Block을 추가해서 파티클 속성을 초기화할 수 있다
- 예: 파티클의 색, 속도, 방향 등을 설정
- 하지만 Capacity를 초과하면 파티클은 **생성되지 않고 버려진다**

### [2] **Alive 속성**
- Alive를 false로 설정하면 해당 파티클은 **처음부터 죽은 상태(dead)**로 만들어진다
- 이런 파티클은 다음 Update에서 더 이상 처리되지 않는다
- 이 방법은 조건에 따라 파티클을 **생성하자마자 없애는 데 유용**하다
- 단, 여전히 메모리를 차지하므로 Capacity는 넘길 수 없다

### [3] **실행 순서**
- Initialize는 **파티클 생성 시점에 단 한 번만 실행된다**
- 실행 순서: `Initialize → 첫 Update → 렌더링`

---

## Source Attribute 사용

- Get Attribute (Source) Operator 또는 Inherit `<Attribute>` Block 사용 가능
- Spawn 시점에 정의된 속성(예: 위치, 속도 등)을 읽어서 Initialize 단계에서 이어받을 수 있다

#### Attribute란?
각 파티클이 가지고 있는 속성 값들이다.

**예시:**
- 위치(Position)
- 속도(Velocity)
- 색상(Color)

---

## Input Flow 호환성

### **가능한 연결 방식**
- 여러 개의 Spawn Context 입력 가능
- 여러 개의 Event Context 입력 가능
- 단일 GPU Event 연결 가능

### **혼합 금지**
- CPU 기반 Context(Spawn/Event)와 GPU Event를 동시에 연결하면 안 된다
- 연결하면 아래와 같은 에러가 발생한다

#### 에러 메시지 예시
```
Exception while compiling expression graph:
System.InvalidOperationException: Cannot mix GPU & CPU spawners in init
```

---

## 요약

Initialize Context는 VFX Graph에서 파티클을 초기화하는 핵심 역할을 한다. 올바른 설정과 제약사항을 이해하면 효과적인 파티클 시스템을 구축할 수 있다.

### 핵심 포인트
1. **한 번만 실행**: 파티클 생성 시점에 단 한 번만 실행된다
2. **Capacity 제한**: 설정된 최대 파티클 수를 초과하면 생성되지 않는다
3. **CPU/GPU 분리**: CPU와 GPU 기반 Context를 혼합하면 안 된다
4. **Alive 속성 활용**: 조건부 파티클 생성에 유용하다

---

## 추가 자료

### 관련 링크
- [Unity VFX Graph 공식 문서](https://docs.unity3d.com/Packages/com.unity.visualeffectgraph@latest)
- [VFX Graph 예제 프로젝트](https://github.com/Unity-Technologies/VisualEffectGraph-Samples)

### 시각적 표현 방법들

#### 1. **플로우차트 스타일**
```
┌─────────────┐    ┌─────────────────┐    ┌──────────────┐
│   START     │───▶│   PROCESS       │───▶│    END       │
└─────────────┘    └─────────────────┘    └──────────────┘
```

#### 2. **트리 구조**
```
Initialize Context
├── Space (Local/World)
├── Data Type (Particle/Strip)
├── Capacity
├── Bounds Setting
└── Input Properties
```

#### 3. **상태 다이어그램**
```
[생성] ──▶  [초기화] ──▶ [업데이트] ──▶  [출력]
  │           │           │           │
  ▼           ▼           ▼           ▼
[Event]    [Setup]    [Process]   [Render]
```

#### 4. **비교 테이블**

| 단계 | 입력 | 처리 | 출력 |
|------|------|------|------|
| **Spawn** | Event | 생성 | Particle |
| **Initialize** | Particle | 설정 | Configured Particle |
| **Update** | Configured Particle | 계산 | Updated Particle |
| **Output** | Updated Particle | 렌더링 | Visual Effect |

