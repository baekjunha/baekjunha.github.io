---
categories: [graphics]
tags: [graphics, opengl, triangle, tutorial]
math: true 
image:
  path: /images/image.png
---

> **요약**: 3D 그래픽스의 기초인 삼각형 렌더링을 위해 그래픽 파이프라인의 핵심 구조를 고찰합니다. 셰이더(Shader) 구현 및 정점 데이터를 GPU로 전송하는 일련의 과정을 상세히 학습합니다.
{: .prompt-info }

## 목차
* TOC
{:toc}

---

## 그래픽 파이프라인 (Graphics Pipeline)

이 문서는 OpenGL에서 3D 공간 좌표를 2D 화면 픽셀로 변환하여 삼각형을 그려내는 전체 과정을 설명한다. OpenGL의 핵심 구조인 **그래픽 파이프라인(Graphics Pipeline)**의 동작 메커니즘을 파악하고, 이를 제어하기 위한 초기 렌더링 설정을 구축하는 방법을 다룬다.

### 1. 그래픽 파이프라인 개요

OpenGL 환경에서 모든 객체 데이터는 3차원 공간 좌표로 정의되지만, 최종 출력은 2차원 화면상의 픽셀 격자로 변환되어야 한다. 이러한 데이터 변환 과정을 **그래픽 파이프라인(Graphics Pipeline)**이라고 한다.

그래픽 파이프라인은 크게 두 단계로 나뉜다.
1. **3D 좌표 → 2D 좌표 변환**: 3차원 공간의 정점들을 화면 평면으로 투영한다.
2. **2D 좌표 → 픽셀 변환**: 투영된 영역 내부를 실제 색상 픽셀(Fragment)로 변환한다.

이 파이프라인은 고도로 병렬화된 구조로 설계되어 GPU에서 효율적으로 처리된다. 개발자는 파이프라인의 특정 단계에 개입하여 로직을 구성할 수 있는데, 이를 **셰이더(Shader)**라고 하며 주로 **GLSL (OpenGL Shading Language)**을 사용하여 작성한다.

### 2. 그래픽 파이프라인 단계별 역할

정점 데이터가 픽셀로 변환되는 그래픽 파이프라인의 주요 단계는 다음과 같다. 이 중 개발자가 직접 코드를 작성하여 제어할 수 있는 핵심 단계는 **정점 셰이더**와 **프래그먼트 셰이더**다.

1.  **정점 데이터 (Vertex Data):**
    *   파이프라인에 입력되는 초기 데이터다.
    *   3D 좌표, 법선 벡터(Normal), 색상, UV 텍스처 좌표 등을 포함하는 **정점(Vertex)** 배열이다.
    *   정점들을 점(Point), 선(Line), 면(Triangle) 중 어떤 형태로 연결할지 결정하는 **프리미티브(Primitive)** 속성을 함께 전달한다.

2.  **정점 셰이더 (Vertex Shader):** *(필수 구현)*
    *   입력된 각 정점의 3D 공간 좌표를 변환한다. 월드, 뷰, 투영 행렬 연산이 이 단계에서 수행된다.

3.  **기하 셰이더 (Geometry Shader):** *(선택 사항)*
    *   구성된 프리미티브(예: 삼각형의 정점 3개)를 입력받아 새로운 정점을 생성하거나 프리미티브의 형태를 변경할 수 있다.

4.  **프리미티브 조립 (Primitive Assembly):**
    *   셰이더 단계를 거친 정점들을 입력받아 설정된 프리미티브 형태(삼각형, 선 등)에 맞춰 논리적 도형을 구성한다.

5.  **래스터화 (Rasterization):**
    *   구성된 도형을 실제 화면 해상도의 픽셀 격자에 대응시키고, 도형 내부에 해당하는 픽셀 단위인 **프래그먼트(Fragment)**를 생성한다.
    *   이 단계 직전에 화면 밖의 정점들을 제거하는 **클리핑(Clipping)** 연산이 수행되어 처리 효율을 높인다.

6.  **프래그먼트 셰이더 (Fragment Shader):** *(필수 구현)*
    *   래스터화로 생성된 각 프래그먼트의 최종 색상을 결정한다. 텍스처 매핑, 조명(Lighting), 그림자 계산 등이 이 단계에서 처리된다.

7.  **테스트 및 블렌딩 (Test and Blending):**
    *   최종 산출된 색상 데이터를 화면에 출력할지 결정한다.
    *   깊이 테스트(Depth Test)를 통해 가려진 픽셀을 제거하고, 알파 블렌딩(Alpha Blending)을 통해 투명도를 처리한다.

### 3. 셰이더 (Shader)의 이해

모던 OpenGL에서는 **정점 셰이더**와 **프래그먼트 셰이더**를 개발자가 직접 작성해야 화면에 데이터를 출력할 수 있다.

*   **정점 셰이더 (Vertex Shader):** 정점의 위치 데이터를 처리한다.
*   **프래그먼트 셰이더 (Fragment Shader):** 픽셀의 색상 데이터를 결정한다.

#### 3.1. 정점 셰이더 구현 (Vertex Shader)

가장 기본적인 정점 셰이더 코드는 다음과 같다.

```glsl
#version 330 core
// 입력 속성 선언: location 0번 슬롯에서 vec3 형태의 정점 좌표(aPos)를 입력받음
layout (location = 0) in vec3 aPos;

void main()
{
    // 정점 좌표를 OpenGL 내장 출력 변수인 gl_Position에 할당
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
```
{: file="shader.vert" }

*   **`#version 330 core`**: GLSL 3.3 Core 프로필 사용을 명시한다.
*   **`in vec3 aPos;`**: 외부 버퍼에서 유입되는 정점 데이터 중 위치 정보를 `aPos` 변수에 담는다.
*   **`layout (location = 0)`**: 이 데이터가 VAO 속성 설정의 0번 인덱스와 연결됨을 명시한다.
*   **`gl_Position`**: 셰이더의 최종 출력 위치를 저장하는 내장 변수(vec4)다.

#### 3.2. 프래그먼트 셰이더 구현 (Fragment Shader)

특정 색상을 출력하는 기본적인 프래그먼트 셰이더 코드는 다음과 같다.

```glsl
#version 330 core
// 출력 변수 선언: 최종 픽셀 색상을 저장할 변수
out vec4 FragColor;

void main()
{
    // RGBA 컬러 값을 할당 (예: 주황색)
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}
```
{: file="shader.frag" }

*   **`out vec4 FragColor;`**: 연산된 결과물인 색상 데이터를 외부로 출력한다.
*   이 셰이더는 래스터화된 모든 프래그먼트에 대해 병렬로 실행되어 도형 내부를 지정된 색상으로 채운다.

#### 3.3. 셰이더 컴파일 (Compile)

셰이더 코드는 런타임에 GPU가 이해할 수 있는 형태로 컴파일되어야 한다.

1.  **소스 코드 정의:** 셰이더 코드를 문자열 형태로 준비한다.

2.  **셰이더 객체 생성:** `glCreateShader`로 셰이더 객체 ID를 생성한다.

    ```cpp
    unsigned int vertexShader = glCreateShader(GL_VERTEX_SHADER);
    unsigned int fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    ```

3.  **소스 코드 연결 및 컴파일:** `glShaderSource`로 코드를 전달하고 `glCompileShader`로 컴파일한다.

    ```cpp
    glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
    glCompileShader(vertexShader);
    ```

4.  **오류 검출:** `glGetShaderiv`와 `glGetShaderInfoLog`를 사용하여 컴파일 성공 여부를 확인하고 에러 메시지를 출력한다.

### 4. 셰이더 프로그램 링크 (Linking)

컴파일된 셰이더들을 하나의 **셰이더 프로그램(Shader Program)** 객체로 연결해야 렌더링에 사용할 수 있다.

1.  **프로그램 객체 생성:** `glCreateProgram`으로 생성한다.
2.  **셰이더 첨부 및 링크:** `glAttachShader`로 셰이더를 연결하고 `glLinkProgram`으로 링크한다.
3.  **링크 오류 검출:** `glGetProgramiv`로 링크 성공 여부를 확인한다.
4.  **프로그램 활성화:** `glUseProgram`으로 해당 프로그램을 현재 렌더링 상태에 적용한다.
5.  **셰이더 객체 삭제:** 링크가 완료된 후 개별 셰이더 객체는 메모리 관리를 위해 `glDeleteShader`로 제거한다.

### 5. 메모리 설정 및 속성 정의

GPU로 전송된 정점 데이터(VBO)를 셰이더의 입력 변수와 연결하는 과정이 필요하다.

#### 5.1. 정점 속성 포인터 (Vertex Attribute Pointer) 설정

입력 데이터의 형식을 `glVertexAttribPointer` 함수를 통해 OpenGL에 전달한다.

```cpp
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);
```

*   **첫 번째 인자 (0)**: 셰이더의 `location = 0`과 일치시킨다.
*   **두 번째 인자 (3)**: 속성의 구성 요소 개수(X, Y, Z)다.
*   **세 번째 인자 (GL_FLOAT)**: 데이터의 자료형이다.
*   **다섯 번째 인자 (Stride)**: 정점 간의 간격(바이트 단위)이다.
*   **여섯 번째 인자 (Offset)**: 데이터가 시작되는 위치다.

### 6. 정점 배열 객체 (VAO, Vertex Array Object)

**VAO (Vertex Array Object)**는 정점 속성 설정 상태를 저장하는 컨테이너 객체다. 

#### 6.1. VAO의 역할
VAO는 다음과 같은 정보를 기록한다.
1. `glVertexAttribPointer`를 통한 속성 레이아웃 설정
2. `glEnableVertexAttribArray`의 활성화 상태
3. 연결된 VBO와의 관계

코어 프로필 환경에서는 VAO를 반드시 바인딩한 상태에서 드로우 콜을 실행해야 한다.

#### 6.2. VAO 설정 예시

```cpp
unsigned int VAO;
glGenVertexArrays(1, &VAO);
glBindVertexArray(VAO);

// VBO 설정 및 속성 정의가 VAO에 기록됨
glBindBuffer(GL_ARRAY_BUFFER, VBO);
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);
```

### 7. VBO (Vertex Buffer Object)

**VBO (Vertex Buffer Object)**는 CPU 메모리의 정점 데이터를 GPU 메모리(VRAM)로 전송하여 보관하는 버퍼 객체다. 데이터를 한 번에 업로드하여 렌더링 성능을 최적화한다.

*   **`GL_STATIC_DRAW`**: 데이터가 거의 변경되지 않을 때 사용한다.
*   **`GL_DYNAMIC_DRAW`**: 데이터가 자주 변경될 때 사용한다.

### 8. 인덱스 버퍼 객체 (EBO, Element Buffer Object)

중복되는 정점 데이터를 효율적으로 관리하기 위해 **EBO (Element Buffer Object)**를 사용한다.

#### 8.1. 인덱스 드로잉 (Index Drawing)
고유한 정점 좌표만 VBO에 저장하고, 이들을 어떤 순서로 조합하여 삼각형을 만들지 결정하는 인덱스 배열을 EBO에 저장한다.

```cpp
unsigned int indices[] = {
    0, 1, 3, // 첫 번째 삼각형
    1, 2, 3  // 두 번째 삼각형
};
```

#### 8.2. EBO 적용 및 출력
`glDrawElements` 함수를 사용하여 인덱스 기반 렌더링을 수행한다.

```cpp
glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
```

---

### 9. 요약

삼각형 렌더링 과정은 다음과 같이 요약할 수 있다.

1.  **데이터 준비 (VBO/EBO):** GPU 메모리에 정점 위치 데이터와 조립 순서(인덱스)를 저장한다.
2.  **셰이더 설정 (GLSL):** 정점 변환 및 픽셀 색상을 결정하는 셰이더 프로그램을 작성하고 컴파일한다.
3.  **상태 관리 및 실행 (VAO/Draw Call):** 정점 속성 설정을 VAO에 기록하고, 이를 활용하여 드로우 콜을 실행함으로써 최종 화면을 구성한다.
