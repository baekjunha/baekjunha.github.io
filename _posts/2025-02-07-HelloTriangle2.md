---
categories: [graphics]
tags: [graphics, opengl, triangle, tutorial]
math: true 
image:
  path: https://learnopengl.com/img/getting-started/pipeline.png
---

> **요약**: 3D 그래픽스의 가장 기초인 삼각형을 화면에 렌더링하기 위한 모조리 분해된 그래픽 파이프라인의 개념과, 셰이더(Shader) 작성, 그리고 정점 데이터를 GPU로 넘겨주는 일련의 핵심 과정을 학습한다.
{: .prompt-info }

## 목차
* TOC
{:toc}

---

## Hello Triangle (삼각형 렌더링 파이프라인)

이 문서는 OpenGL에서 3D 공간 좌표를 2D 모니터 픽셀 해상도로 투영하여, 마침내 하나의 완성된 **삼각형**을 그려내는 전체 과정을 상세히 분석한다. OpenGL의 척추라 할 수 있는 **그래픽 파이프라인(Graphics Pipeline)** 동작 메커니즘을 확실히 파악하고, 이를 통제하는 초기 렌더링 셋업을 구축한다.

## Hello Triangle (OpenGL 튜토리얼)

이 문서는 OpenGL에서 3D 좌표를 화면의 2D 픽셀로 변환하여 삼각형을 그리는 과정을 설명한다. OpenGL의 핵심인 그래픽 파이프라인을 이해하고, 이를 활용하여 기본적인 렌더링을 수행하는 방법을 배울 수 있다.

### 1. 그래픽 파이프라인 개요

OpenGL 환경에서 모든 객체 데이터는 연속된 3D 공간 상의 좌표계에 둥둥 떠 있다. 하지만 최후에 사용자 모니터에 비춰지는 결과물은 2D 평면 위의 격자 픽셀 덩어리일 뿐이다. 따라서 3D 부동소수점 좌표군을 2D 픽셀 컬러 배열로 압축 변환하는 중대한 공정이 반드시 필요하며, 이 모든 과정을 도맡아 처리하는 거대한 공장이 바로 **그래픽 파이프라인(Graphics Pipeline)** 이다.

그래픽 파이프라인은 본질적으로 다음 두 개의 거대한 메인 페이즈로 나뉜다.
1.  **3D 좌표 -> 2D 좌표 변환:** 3차원 공간 정점들을 2차원 화면 평면으로 원근 투영한다.
2.  **2D 좌표 -> 픽셀 변환:** 2차원 외곽선 좌표 내부를 실제 색상 픽셀(Fragment)들로 칠하고 채워 넣는다.

이 거대한 파이프라인은 세부적으로 여러 구획화된 파트(단계)로 조각나 있으며, 컨테이어 벨트처럼 앞 단계 결과물을 다음 단계의 입력 데이터로 넘겨 일방향 처리한다. 각 단계는 오직 본인에게 할당된 하나의 좁은 임무만을 극도로 빠르게 수행하도록 특화되어 있어, 현대 GPU의 수천 개 코어 아키텍처를 통한 미친듯한 병렬 처리(Parallel Processing) 연산 효율을 뽑아낸다.

개발자는 이 파이프라인 벨트 중간중간에 자리 잡은 특정 핵심 코어 장비들에 본인만의 프로그래밍 로직을 집어넣어, 변환 메커니즘을 자유롭게 입맛대로 커스터마이징할 수 있다. 이렇게 파이프라인 단계에 삽입되어 GPU 위에서 돌아가는 아주 작고 뾰족한 프로그램을 **셰이더(Shader)** 라고 부른다. 셰이더는 OpenGL 전용 언어인 **GLSL (OpenGL Shading Language)** 로 작성된다.

### 2. 그래픽 파이프라인 단계별 해부

다음은 정점 뭉치가 픽셀로 환골탈태하는 그래픽 파이프라인의 핵심 파트들을 순서대로 나열한 것이다. 이 중 개발자가 직접 셰이더 코드를 짜서 전권을 쥐고 흔들 수 있는 핵심 단계는 **정점 셰이더**와 **프래그먼트 셰이더**다.

1.  **정점 데이터 (Vertex Data):**
    *   파이프라인 공장에 투입되는 최초의 날것 원자재다.
    *   3D 좌표, 노멀 벡터, 색상, UV 텍스처 좌표 등을 묶어놓은 **정점(Vertex)** 배열 구조체 덩어리다.
    *   이때 모래알 같은 정점들을 점(Point), 선(Line), 면(Triangle) 중 어떤 식으로 이어서 도형을 만들 것인지 규정하는 **프리미티브(Primitive)** 지시 속성을 함께 넘겨준다.

2.  **정점 셰이더 (Vertex Shader):** *(커스텀 필수)*
    *   유입된 정점 하나하나를 개별적으로 붙잡아 3D 공간상 좌표를 1차적으로 변환 조작한다. (월드, 뷰, 투영 행렬 연산 등이 이곳에서 발생한다.)

3.  **기하 셰이더 (Geometry Shader):** *(커스텀 옵션)*
    *   완성된 프리미티브(예: 삼각형 점 3개)를 통째로 입력받아, 정점을 임의로 더 증식시키거나 새로운 프리미티브 모양으로 변이시킨다. 

4.  **프리미티브 조립 (Primitive Assembly):**
    *   셰이더 단계들을 거친 각 정점들을 입력받아, 1번 단계에서 지시받았던 프리미티브 형태 조건(삼각형, 선 등)에 맞게끔 구체적인 철사 외곽선 뼈대를 물리적으로 조립한다.

5.  **래스터화 (Rasterization):**
    *   조립된 외곽선 형태를 실제 모니터 해상도 픽셀 격자망에 겹쳐보고, 도형 내부 면적에 속하는 모든 픽셀들을 타일 조각들, 즉 **프래그먼트(Fragment)** 들로 무수히 잘게 쪼개어 생성해낸다.
    *   이 단계 직전에 화면 카메라 프레임 바깥에 위치한 정점들을 모조리 잘라내 폐기하는 **클리핑(Clipping)** 연산이 선제되어 막대한 GPU 부하를 절감해준다.

6.  **프래그먼트 셰이더 (Fragment Shader):** *(커스텀 필수)*
    *   래스터화로 쪼개진 픽셀 조각 하나하나에 무슨 물감 색상을 칠할지 최종 RGBA 컬러값을 산출해낸다. 텍스처 맵핑, 정교한 라이팅(Lighting), 그림자 계산 등 그래픽스의 화려한 시각적 마법은 99% 모두 이곳에서 탄생한다.

7.  **알파 테스트 및 블렌딩 (Alpha Test and Blending):**
    *   최종 산출된 색상 후보 픽셀을 모니터 화면(프론트 버퍼)에 진짜로 그릴지 말지 최후의 심판을 거친다.
    *   깊이 버퍼(Depth Buffer)를 뒤져 나보다 앞에 무언가 가리고 있다면 그리기 컷, 투명도(Alpha)가 껴있다면 뒤의 배경색과 혼합(Blend) 연산을 수행한다.

### 3. 필연적 코어: 셰이더 (Shader)의 이해

구형 고정 함수 파이프라인(Fixed-Function Pipeline) 시대에는 이 모든 것이 하드웨어 칩에 박혀있어 조작 불가능했으나, 모던 그래픽스에서는 **정점 셰이더**와 **프래그먼트 셰이더** 두 개를 무조건 개발자가 직접 타이핑해야 화면에 단 픽셀 한 조각이라도 띄울 수 있다.

*   **정점 셰이더 (Vertex Shader):** 들어온 점들의 3차원 위치를 조정한다.
*   **프래그먼트 셰이더 (Fragment Shader):** 칠해질 픽셀의 물감 색상을 결정한다.

#### 3.1. 기본 정점 셰이더 구현 (Vertex Shader)

가장 기초적인 뼈대 수준의 정점 셰이더 GLSL 코드는 이렇다.

```glsl
#version 330 core
// 데이터 입구 선언: 파이프라인 0번 슬롯(location=0)에서 3차원 벡터(vec3) 형태의 정점 데이터(aPos)를 받아오겠다.
layout (location = 0) in vec3 aPos;

void main()
{
    // 최후의 투영 반환: 공간 변환 연산을 마친 점 좌표를 OpenGL 빌트인 출력 변수인 gl_Position에 박아넣는다.
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
```
{: file="shader.vert" }

*   **`#version 330 core`**: GLSL 3.3 코어 스펙을 엄격히 준수하겠다는 첫 줄 명시 선언이다. C/C++ 전처리 지시자처럼 반드시 최상단에 자리해야 한다.
*   **`in vec3 aPos;`**: 외부 버퍼에서 그래픽 카드 메모리로 유입되는 정점 직렬 데이터 중에서, 3차원(`vec3`) 위치 포지션 구조체 하나만 떼어내서 `aPos`라는 변수에 잠시 담아두겠다는 입력 인터페이스 약속이다.
*   **`layout (location = 0)`**: 이 입력 인터페이스가 추후 우리가 조작할 VAO 버퍼 할당 속성표 상의 **0번째 인덱스 슬롯** 과 맞물린다는 강제 바인딩 명시다.
*   **`gl_Position`**: 셰이더가 출력을 던지는 종점이다. OpenGL 내부 로직에서 기본적으로 요구하는 내장 4차원 벡터(`vec4`) 변수다. 마지막 `w` 성분에 들어간 역수값 `1.0` 은 동차 좌표계(Homogeneous Coordinates) 개념으로 먼 뷰 변환 파트에서 깊이 원근감을 나누는 데 쓰인다.

위의 예제 코드는 일말의 변환 행렬 가공 조작 없이, C++ 코드에서 날아온 정점 점 좌표를 액면가 그대로 패스스루(Pass-through)시켜 래스터라이저로 던지는 극저수준 단계다. 

#### 3.2. 기본 프래그먼트 셰이더 구현 (Fragment Shader)

다음 타겟 픽셀 단 하나를 주먹구구식 노가다 단색으로 밀어버리는 극단적 형태의 프래그먼트 셰이더 코드다.

```glsl
#version 330 core
// 데이터 출구 선언: 최종 연산된 픽셀 색상값 RGBA 벡터를 뽑아낼 변수를 하나 임의로 만든다.
out vec4 FragColor;

void main()
{
    // (픽셀을 주황색 R:1.0, G:0.5, B:0.2, Alpha:1.0 불투명으로 고정 할당)
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}
```
{: file="shader.frag" }

*   **`out vec4 FragColor;`**: 정점 셰이더가 `in` 으로 데이터를 받았듯, 이곳은 `out` 키워드로 산출 결과물인 `vec4` RGBA 컬러 구조체를 외부 출력 파이프라인으로 퍼펙트하게 떠넘긴다.
*   이 셰이더가 작동하면, 래스터라이저가 쪼개놓은 삼각형 면적 내부의 수백, 수천만 개 프래그먼트 조각 각각에 이 셰이더 프로그램이 개별적으로 병렬 연산 타격을 꽂아넣으며 순수 100% 오렌지색 단일 컬러로 삼각형 내부를 가득 채우게 된다.

#### 3.3. 셰이더 컴파일 (Compile)

셰이더 소스 코드는 단순한 문자열(String) 비정형 텍스트에 불과하다. 이를 런타임에 그래픽 카드가 이해할 수 있는 머신 코드로 번역(컴파일)하는 과정을 거쳐야 한다.

1.  **소스 코드 저장:** 셰이더 소스 코드를 C-Style 문자열 상수로 하드코딩 저장한다.

    ```cpp
    const char *vertexShaderSource = "#version 330 core\n"
        "layout (location = 0) in vec3 aPos;\n"
        "void main()\n"
        "{\n"
        "   gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);\n"
        "}\0";

    const char *fragmentShaderSource = "#version 330 core\n"
        "out vec4 FragColor;\n"
        "void main()\n"
        "{\n"
        "   FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);\n"
        "}\n\0";
    ```
    {: file="main.cpp" }

2.  **셰이더 객체 생성:** `glCreateShader` 함수를 호출하여 셰이더 객체 ID(핸들)를 발급받는다.

    ```cpp
    unsigned int vertexShader = glCreateShader(GL_VERTEX_SHADER);
    unsigned int fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    ```
    {: file="main.cpp" }

3.  **소스 코드 첨부 및 컴파일:** `glShaderSource` 함수로 텍스트 소스 코드를 셰이더 객체에 밀어넣고, `glCompileShader` 함수로 다이렉트 런타임 컴파일을 때린다.

    ```cpp
    glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
    glCompileShader(vertexShader);

    glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
    glCompileShader(fragmentShader);
    ```
    {: file="main.cpp" }

4.  **컴파일 디버깅 (오류 검출):** GLSL 코드 문법에 오타가 났을 경우 컴파일은 조용히 실패하고 치명적인 블랙스크린을 유발한다. 따라서 `glGetShaderiv` 함수로 컴파일 성공 여부 상태 플래그를 뽑아내고, 실패 시 `glGetShaderInfoLog` 함수를 호출해 에러 원인 문자열 버퍼를 터미널에 강제 표출시키는 안전장치를 달아야 한다.

    ```cpp
    int success;
    char infoLog[512];
    glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);
    if(!success)
    {
        glGetShaderInfoLog(vertexShader, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" << infoLog << std::endl;
    }

    // (프래그먼트 셰이더도 동일한 에러 캐치 수행)
    glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &success);
    if(!success)
    {
        glGetShaderInfoLog(fragmentShader, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n" << infoLog << std::endl;
    }
    ```
    {: file="main.cpp" }

### 4. 셰이더 프로그램 링크 (Linking)

컴파일된 파편 셰이더들을 **셰이더 프로그램(Shader Program)** 이라는 단일 객체 체인으로 연결(Link)해야 비로소 렌더링 도구로 써먹을 수 있다.

1.  **셰이더 프로그램 객체 생성:** `glCreateProgram` 함수로 거푸집 객체를 생성한다.

    ```cpp
    unsigned int shaderProgram = glCreateProgram();
    ```
    {: file="main.cpp" }

2.  **셰이더 첨부 및 링크:** 앞서 컴파일 성공한 정점/프래그먼트 셰이더 조각들을 `glAttachShader` 로 프로그램에 이어 붙이고, `glLinkProgram` 으로 하나로 접합(Link)한다.

    ```cpp
    glAttachShader(shaderProgram, vertexShader);
    glAttachShader(shaderProgram, fragmentShader);
    glLinkProgram(shaderProgram);
    ```
    {: file="main.cpp" }

3.  **링크 오류 검출:** 컴파일 단계와 마찬가지로 링킹 과정에서도 변수 타입 불일치 등으로 실패할 수 있으니 `glGetProgramiv` 로 안전망을 구축한다.

    ```cpp
    glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
    if (!success) {
        glGetProgramInfoLog(shaderProgram, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER::PROGRAM::LINKING_FAILED\n" << infoLog << std::endl;
    }
    ```
    {: file="main.cpp" }

4.  **셰이더 프로그램 장착:** `glUseProgram` 함수를 호출하여 지금부터 그려질 모든 렌더링 형상들이 방금 접합한 이 셰이더 프로그램을 관통하도록 활성화한다.

    ```cpp
    glUseProgram(shaderProgram);
    ```
    {: file="main.cpp" }

5.  **셰이더 찌꺼기 청소:** 프로그램에 성공적으로 링크가 완료된 원본 셰이더 조각들은 더 이상 필요 없으므로 메모리 누수를 막기 위해 즉시 삭제(`glDeleteShader`) 처분한다.

    ```cpp
    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);
    ```
    {: file="main.cpp" }

### 5. 메모리 세팅: 버퍼 속성 규정

셰이더 프로그램이 준비되었다 한들, GPU로 쏘아보낸 연속된 1차원 배열 숫자 덩어리(VBO)들을 셰이더의 어떤 변수(`location=0 등`)로, 어떤 간격으로 잘라서 대입할지 OpenGL은 전혀 알지 못한다. 프로그래머가 이를 수동으로 맵핑(Mapping) 규정해 주어야만 한다.

#### 5.1. 정점 속성 포인터 (Vertex Attribute Pointer) 세팅

가령 C++ 진영에서 다음과 같이 삼각형 좌표 정점 배열을 선언해 넘겼다고 가정해 보자.

```cpp
float vertices[] = {
     0.5f,  0.5f, 0.0f,  // 우상단 꼭짓점
     0.5f, -0.5f, 0.0f,  // 우하단 꼭짓점
    -0.5f, -0.5f, 0.0f   // 좌하단 꼭짓점
};
```
{: file="main.cpp" }

이 메모리 덩어리의 포맷 특징은 다음과 같다.
* 위치 데이터는 1개당 32비트(4바이트) 부동소수점(`float`) 1개 값이다.
* 한 정점의 위치는 3개(`X, Y, Z`)의 값으로 이루어진다.
* 배열 내부에 여백이나 빈 공간 없이 텍스처나 노멀값 등 다른 이물질 데이터가 없다. 아주 촘촘하게 타이트(Tight)하게 정렬되어 있다.
* 데이터 파싱 시작점(오프셋)은 버퍼의 맨 앞단 0바이트 지점부터 출발한다.

이 해석 규칙을 `glVertexAttribPointer` 함수를 통해 OpenGL 스테이트 머신에 통보한다.

```cpp
// 어떻게 데이터를 파싱할 것인가?
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
// 파싱한 데이터를 0번 슬롯(location=0) 셰이더 입력구에 활성화시켜 꽂아 넣는다!
glEnableVertexAttribArray(0);
```
{: file="main.cpp" }

*   **`0`**: 셰이더 코드에서 명시했던 타겟 목적지 로케이션(`layout (location = 0)`) 인덱스 번호다.
*   **`3`**: 속성의 컴포넌트 갯수다. 공간 좌표는 3개(`X, Y, Z`)이므로 3 상수값을 넣는다. (참고로 색상 RGBA를 묘사한다면 4를 넣게 된다).
*   **`GL_FLOAT`**: 각 컴포넌트 요소 1개가 뜻하는 원시 자료형(Type)이다.
*   **`GL_FALSE`**: 데이터를 가져올 때 자동으로 범위를 -1.0 ~ 1.0으로 정규화(Normalize) 시킬 것인지 묻는 스위치다. 순수 float 좌표이므로 `GL_FALSE`를 대입한다.
*   **`3 * sizeof(float)`**: **스트라이드(Stride)** 라고 불리며, 버퍼에서 정점 1세트 데이터 크기의 바이트 단위 폭격을 명시한다.
*   **`(void*)0`**: **오프셋(Offset)** 으로, 이 파싱이 시작되는 최초 출발점이 버퍼 맨 앞 0번째 바이트부터 시작됨을 알리는 포인터 값이다.

#### 5.2. 고전적인 그리기 플로우의 한계 파악하기

여기까지 왔으면 이론상으로는 삼각형 하나를 스크린에 띄울 수 있다. 고전적인 렌더링 호출 플로우는 대략 이러할 것이다.

```cpp
// --- (렌더 루프 돌아갈 때마다 매 프레임 반복 호출) ---
// 0. 타겟 VBO 바인딩
glBindBuffer(GL_ARRAY_BUFFER, VBO);
// 1. 메모리에 정점 속성 포인터 맵핑 규정 다시 세팅
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);
// 2. 셰이더 프로그램 장착
glUseProgram(shaderProgram);
// 3. 실제 드로우 콜(Draw Call) 폭격
glDrawArrays(GL_TRIANGLES, 0, 3);
```
{: file="main.cpp" }

삼각형 하나 그릴 때는 별 문제가 되지 않지만, 만약 렌더링해야 할 캐릭터나 지형 오브젝트가 수천 개 단위를 넘어간다면 매 프레임마다 버퍼를 바인딩하고 엄청난 길이의 `glVertexAttribPointer`를 속성 갯수(위치, 노멀, UV 등)만큼 일일이 재호출해야 한다. 이는 심각한 CPU 오버헤드 병목과 스파게티 코드를 유발한다. 이 번거로움을 단 한 줄로 축약시켜주는 궁극의 압축 백업 객체가 바로 앞으로 설명할 **VAO** 다.

---

### 6. 정점 배열 객체 (VAO, Vertex Array Object)

**VAO (Vertex Array Object)** 는 OpenGL이 버텍스 속성 맵핑 히스토리(상태 변이)를 하나로 똘똘 뭉쳐서 통째로 레코딩해 기억해 두는 거대한 메모장(컨테이너) 객체다.

#### 6.1. VAO의 막강한 역할

VAO는 특정 객체를 렌더링하기 위한 복잡다단한 사전 준비 작업들을 단일 핸들(ID) 하나로 압축해 묶어버린다. 구체적으로 다음 행동들을 녹화한다.
1. `glEnableVertexAttribArray` 와 `glDisableVertexAttribArray` 호출 스위치 개폐 로그
2. `glVertexAttribPointer` 를 찔러 설정했던 맵핑 레이아웃 정보
3. 이 정보가 어떤 VBO (Vertex Buffer Object) 데이터 주소와 통신해야 하는지에 대한 VBO 링킹 연결고리

> [!important]
> **Core-Profile 환경에서의 엄격성**
> 현세대 OpenGL 코어 프로파일 환경에서는 **아무런 VAO도 바인딩하지 않고 렌더링 드로우 콜을 때리면 에러를 뿜으며 화면에 일절 아무것도 그리지 않는다.** 최소한 더미 VAO라도 하나 바인딩해 두는 것이 필수 규칙이다.

#### 6.2. VAO 셋업 실전 예시

VAO 설정은 VBO 생성 직후, 속성을 정의하기 직전 가장 바깥에서 껍데기처럼 바인딩하며 스코프(Scope)를 연다.

```cpp
// ① VAO 객체 생성 및 바인딩 (녹화 스위치 ON)
unsigned int VAO;
glGenVertexArrays(1, &VAO);
glBindVertexArray(VAO);

// ② VBO 바인딩 및 버텍스 데이터 복사 
glBindBuffer(GL_ARRAY_BUFFER, VBO);
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

// ③ 버텍스 속성 포인터 설정 (이 정보가 모조리 VAO에 녹화됨)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);

// ④ [녹화 종료] VAO 바인딩 해제로 안전망 구축 (권장 사항)
glBindVertexArray(0); 
```
{: file="main.cpp" }

이제 방대한 렌더링 루프에서는 복잡한 맵핑 함수 호출을 일절 생략하고, 내가 만들어준 특정 모델의 `VAO` 하나만 딸깍 하고 바인딩 스왑(Swap)한 뒤 `glDraw` 명령을 내리면 된다.

```cpp
// --- 렌더 루프(while) 내부 영역 ---
glUseProgram(shaderProgram);
glBindVertexArray(VAO); // 방금 녹화해둔 VAO 세트 호출
glDrawArrays(GL_TRIANGLES, 0, 3);
```
{: file="main.cpp" }

#### 6.3. glDrawArrays 함수 구동 원리

*   **`glDrawArrays(GL_TRIANGLES, 0, 3);`**
    *   **첫 번째 인자 (`GL_TRIANGLES`)**: 현재 바인딩된 버퍼 뭉치들의 정점을 꺼내어 어떤 프리미티브(도형) 형태로 조립할 것인지 엔진에 지시한다.
    *   **두 번째 인자 (`0`)**: VAO에 등록된 VBO 배열 어레이에서, 정점 몇 번 인덱스부터 뽑아 쓰기 시작할 것인지 오프셋을 정한다.
    *   **세 번째 인자 (`3`)**: 삼각형 하나를 그릴 것이므로 정점 딱 3개만 차례대로 뽑아다 조립하겠다는 뜻이다.

### 7. VBO (Vertex Buffer Object)를 통한 GPU 메모리 업로드

CPU 측인 RAM 메모리(C++ 배열 등)에 자리 잡은 수백 메가바이트의 3D 모델 정점 데이터를 GPU VRAM(그래픽 메모리 보드)으로 쫙 끌어올려 업로드하는 용기가 바로 **VBO (Vertex Buffer Object)** 다. VBO를 활용하지 않으면 매 프레임 그리기 호출마다 CPU-GPU를 잇는 좁은 병목 구간(PCIe 버스 등)으로 데이터가 전송되므로 치명적인 렌더링 성능 저하가 발생한다. VBO로 한 번에 데이터를 덤프해 두면, GPU가 초고속 내부 대역폭 메모리에 직접 접근해 데이터를 갈퀴 모양으로 쓸어담아 렌더링 연산을 수행할 수 있다.

#### 7.1. VBO 객체 발급 및 바인딩

1.  **VBO 생성:** `glGenBuffers` 함수로 GPU 메모리 공간 상의 버퍼 버킷 ID 번호를 발급받는다.

    ```cpp
    unsigned int VBO;
    glGenBuffers(1, &VBO);
    ```
    {: file="main.cpp" }

2.  **VBO 바인딩:** OpenGL 스테이트 머신의 타겟 포인터를 방금 만든 VBO 통으로 맞춰둔다. (이제부터 내리는 버퍼 조작 명령은 모조리 이 녀석에게 들어간다.)

    ```cpp
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    ```
    {: file="main.cpp" }

    *   `GL_ARRAY_BUFFER` 지시자는 이 버퍼가 단순 인덱스나 텍스처 픽셀 조각이 아닌, "정점 속성 어레이" 배열을 담는 통렬 버퍼임을 타입(Type)으로 선언하는 것이다.

#### 7.2. GPU로 데이터 복사 적재

이제 포인터를 맞춰둔 버퍼를 향해 실제 `vertices` 부동소수점 C++ 배열 복사본을 GPU 메모리 공간으로 쏘아보낸다.

```cpp
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
```
{: file="main.cpp" }

*   **`sizeof(vertices)`**: 복사할 총 데이터 바이트 용량을 잰다.
*   **`vertices`**: 복사 원본 소스의 시작점 포인터다.
*   **`GL_STATIC_DRAW`**: 이 데이터가 앞으로 얼마나 빈번하게 오르락내리락 수정될 운명인지 GPU에게 미리 힌트를 귀띔하는 옵션표다. GPU는 이 힌트를 보고 메모리 캐싱 전략을 최적화한다.
    *   **`GL_STATIC_DRAW`**: 데이터가 한 번 업로드되면 절대 변하지 않고 무한 반복되어만 쓰인다. (일반적인 배경 바위 장식 모델링, 지형 좌표 등에 최적)
    *   **`GL_DYNAMIC_DRAW`**: 데이터가 자주 변경되어 새로 복사될 확률이 높다 (물 표면 애니메이션, 나뭇잎 떨림 처리 등).
    *   **`GL_STREAM_DRAW`**: 데이터가 매 프레임마다 완전히 교체된다 (고도로 연산 집약적인 UI 텍스트 타이포그래피 좌표 변경 등).

정적인 삼각형을 한 번 그리면 좌표는 변하지 않으므로 본 예제에서는 최상단 디폴트 퍼포먼스 힌트인 `GL_STATIC_DRAW`를 배정했다. 이 과정을 무사히 마치면 방금 타이핑했던 9개의 부동소수점 데이터가 여러분의 그래픽 카드 메모리판 위에 완전히 이식된다.

### 8. VAO를 통한 다중 모델 상태 관리 패러다임

**Vertex Array Object (VAO)** 는 씬(Scene) 내부에 여러 개의 이기종 3D 객체가 스폰될 때 발생하는 극악무도한 상태 맵핑 복잡도를 깨끗하게 청소해 준다.

#### 8.1. 문제 제기

단일 객체가 아니라 수백 개의 각기 다른 모델을 렌더링해야 하는 상황을 가정해보자. 위치값, 색상값, 노멀 벡터값 등 모델마다 `glVertexAttribPointer` 레이아웃 구조가 완전히 천차만별일 수 있다. VAO가 없다면 매 프레임마다 그리기 직전에 100개 모델 각각의 맵핑 코드를 일일이 100번 호출하며 상태 머신을 오염시켜야 한다.

#### 8.2. 해결책: VAO의 상태 캡슐화 (Capsulation)

앞서 설명했듯 VAO는 VBO 바인딩 기록과 속성 레이아웃 연결 맵핑 정보를 내부에 꽁꽁 싸매어(Capsulate) 캡처해 두는 프로파일(Profile) 객체다. 

1.  **모델별 프로필 생성:** 객체 A, 객체 B마다 전담 VAO를 무조건 하나씩 생성한다.

    ```cpp
    unsigned int VAO1, VAO2;
    glGenVertexArrays(1, &VAO1);
    glGenVertexArrays(1, &VAO2);
    ```
    {: file="main.cpp" }

2.  **프로필별 고유 셋업(1회성 작업):** 초기화 함수(Init) 단계에서 딱 한 번만 각자의 VAO를 바인딩하고, 각자의 골격에 맞는 VBO와 속성 맵핑을 하드코딩해둔다.

    ```cpp
    // VAO 1번 객체 모델 셋업
    glBindVertexArray(VAO1);
    glBindBuffer(GL_ARRAY_BUFFER, VBO1);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    // VAO 2번 객체 모델 셋업
    glBindVertexArray(VAO2);
    glBindBuffer(GL_ARRAY_BUFFER, VBO2);
    // (만약 VBO2가 X,Y 2D 좌표 모델이라면 아래처럼 다르게 파싱)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    ```
    {: file="main.cpp" }

3.  **렌더링 루프에서의 혁신 (Swap & Draw):** 이제 실시간으로 모니터에 그림을 뿌리는 `while` 루프 안에서는 수많은 맵핑 함수들을 모조리 소거하고 오직 VAO 스왑(Swap)만으로 모든 레이아웃 변경을 해결한다.

    ```cpp
    // --- 렌더 루프 ---
    glUseProgram(shaderProgram);

    // 모델 1번 소환
    glBindVertexArray(VAO1);
    glDrawArrays(GL_TRIANGLES, 0, 3); // 3D 삼각형 그리기

    // 모델 2번 소환
    glBindVertexArray(VAO2);
    glDrawArrays(GL_TRIANGLES, 0, 3); // 2D 삼각형 그리기
    ```
    {: file="main.cpp" }

이처럼 VAO는 수많은 객체의 파편화된 그래픽 상태(State)를 개별 박스로 포장해 주어, 엔진 코드의 거시적인 객체 지향적 관리를 가능케 한다.

---

### 9. 통합 복습: VAO, VBO, 정점 속성의 유기적 결합 구조

이 세 가지 개념의 얽히고설킨 타임라인을 명확하게 시각화하면 다음과 같다.

1.  **VBO (데이터 창고):** 정규군 병사(데이터)들이 탑승하는 거대한 트럭이다. 단순무식하게 `glBufferData`를 통해 GPU 메모리로 병력들을 뭉텅이로 실어 나르는 우직한 역할을 담당한다.
2.  **정점 속성 (용도 지침서):** 이 병사 무리들을 부대(셰이더 Variable)별로 어떻게 편재해서 할당시킬 것인지 규칙을 정하는 문서표다. `glVertexAttribPointer` 라는 함수 서명을 통해 작성된다.
3.  **VAO (최종 브리핑 폴더):** VBO 트럭 번호판과 용도 지침서(정점 속성)를 거대한 결재판 하나에 철(File)해 두는 보관소다. 렌더링 호출을 실행할 때 엔진은 오직 이 최종 결재판(VAO) 하나만 검토하고 즉각 병동 배치를 수행한다.

---

### 10. 궁극의 뼈대: 인덱스 버퍼 객체 (EBO, Element Buffer Object)

정점 배열(Vertex Array) 방식의 치명적인 문제점을 해결하기 위해 등장한 마지막 퍼즐 조각이 바로 **EBO (Element Buffer Object)** 혹은 IBO (Index Buffer Object) 다.

#### 10.1. 오버헤드의 발생 원리

삼각형 2개를 딱 붙여서 일반적인 통짜 사각형(Quad) 하나를 화면에 그리고 싶다고 가정해보자. 삼각형은 정점 3개가 필요하므로 사각형은 $3 \times 2 = 6$ 개의 정점이 필요하다.

```cpp
float quadVertices[] = {
    // 윗쪽 삼각형 (#1)
     0.5f,  0.5f, 0.0f,  // 우상단 (A)
     0.5f, -0.5f, 0.0f,  // 우하단 (B)
    -0.5f,  0.5f, 0.0f,  // 좌상단 (C)
    // 아랫쪽 삼각형 (#2)
     0.5f, -0.5f, 0.0f,  // 우하단 (B) - 중복 데이터!
    -0.5f, -0.5f, 0.0f,  // 좌하단 (D)
    -0.5f,  0.5f, 0.0f   // 좌상단 (C) - 중복 데이터!
};
```
{: file="main.cpp" }

수학적으로 사각형의 꼭짓점은 단 4개면 충분하지만, 단순 삼각형 나열법(DrawArrays)을 사용하면 대각선의 (B)와 (C) 좌표가 메모리에 2번씩 하드코딩으로 중복 할당된다. 

지금은 2개(24바이트)의 오버헤드지만 고퀄리티의 3D 사람 얼굴 모델링은 수백만 개의 삼각형으로 촘촘히 쪼개져 있다. 가운데 코에 솟아오른 정점 하나는 무려 삼각형 6개 공간에서 동시에 공유된다. 이처럼 무수한 정점들의 중복 좌표 데이터를 고스란히 저장하면 GPU VRAM 메모리는 금세 터져버리고 대역폭은 마비된다.

#### 10.2. 인덱스 드로잉 (Index Drawing) 전략 도입

이 끔찍한 메모리 낭비를 방지하고자, 데이터 창고(VBO)에는 오로지 **"절대 겹치지 않는 순수 고유 정점 4개"** 만 타이트하게 저장한다. 대신, "이 정점 번호표들을 몇 번씩, 어떤 삼각형 순서로 이어 그릴 것인지" 를 지시하는 **조립 설명서(Index Array)** 를 별도의 전용 버퍼 구역에 저장하여 엔진에 제공한다.

```cpp
// 1. 순수 고유 데이터 좌표 (VBO 용) - 딱 4개만!
float vertices[] = {
     0.5f,  0.5f, 0.0f,  // 우상단 (0)
     0.5f, -0.5f, 0.0f,  // 우하단 (1)
    -0.5f, -0.5f, 0.0f,  // 좌하단 (2)
    -0.5f,  0.5f, 0.0f   // 좌상단 (3)
};

// 2. 조립 번호표 설명서 (EBO 용)
unsigned int indices[] = {  // 반드시 부호 없는 양수 Int여야 한다.
    0, 1, 3,   // 우상단(0) -> 우하단(1) -> 좌상단(3) 점을 이어 윗 삼각형 생성
    1, 2, 3    // 우하단(1) -> 좌하단(2) -> 좌상단(3) 점을 이어 아래 삼각형 생성
};
```
{: file="main.cpp" }

이 조립 번호표(Indices)들을 GPU 메모리에 전송하기 위해 쓰이는 특수 목적의 컨테이너가 바로 **EBO** 다. VBO와 생성 메커니즘은 소름 돋게 똑같다.

```cpp
unsigned int EBO;
glGenBuffers(1, &EBO);

// 타입이 GL_ARRAY_BUFFER 가 아닌 GL_ELEMENT_ARRAY_BUFFER 임을 명심하라.
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
```
{: file="main.cpp" }

#### 10.3. VAO와 EBO의 끈끈한 결속

가장 중요한 사실 하나, **VAO는 자신이 바인딩된 스코프 내부에서 호출되어 활성화(Bind)된 EBO의 체결 상태마저도 함께 캡처(녹화)하여 영구 보존한다.**

따라서 VAO 셋업 블록에 EBO 바인딩 코드 한 줄만 끼워 넣으면, 추후 렌더링 루프에서 VAO를 호출할 때 VBO는 물론, 이 모델을 그리기 위한 인덱스 설명서(EBO)까지 모두 세트로 장착되는 마법이 펼쳐진다.

#### 10.4. 인덱스 드로잉 실전 적용 (glDrawElements)

기존의 단순 배열 순차 렌더링(`glDrawArrays`) 대신, EBO 인덱스를 참조하여 퍼즐을 조립하듯 정점을 발췌해 그리는 드로우 명령은 `glDrawElements` 다.

```cpp
// -- 렌더링 루프 진입 --
glUseProgram(shaderProgram);
glBindVertexArray(VAO);
// 기존: glDrawArrays(GL_TRIANGLES, 0, 3);
// EBO 적용 버전:
glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
```
{: file="main.cpp" }

*   **`GL_TRIANGLES`**: 기하 도형 프리미티브 형태 조건.
*   **`6`**: "이번 드로잉에서 EBO 설명서에 나열된 인덱스 번호 6개를 차례대로 다 소모해라" 라는 횟수 명시다. (삼각형 2개 조립 지시)
*   **`GL_UNSIGNED_INT`**: 넘겨준 Ин덱스 배열 데이터가 부호 없는 32비트 정수형(`unsigned int`) 공간 박스를 활용하고 있다는 포맷 통보.
*   **`0`**: EBO 버퍼 내에서 0바이트부터 오프셋 없이 읽기 시작하라는 지시.

코드를 컴파일하고 실행하면, 고작 4개의 유니크한 정점 데이터 덩어리로 완벽하게 2개의 3D 삼각형을 스냅 접합시켜 완성한 하나의 네모반듯한 사각형(Quad)이 모니터 화면에 은은하게 출력될 것이다. 

> [!tip] 
> 현재 렌더링되는 폴리곤 형태를 색상으로 채우지 않고 순수 철사(Wireframe) 골조 형태만 뽑아서 화면에 그리고 싶다면, 초기화 설정 단계에 **`glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);`** 함수를 선언하면 된다. 다시 원래 면적 채색으로 돌리는 옵션은 인자를 `GL_FILL` 로 바꾼다. 이 모드는 개발 단계에서 EBO 접합 부위 구석구석 정점들이 내가 의도한 대로 잘 박혀있는지 메쉬(Mesh) 버그를 디버깅할 때 천금 같은 역할을 발휘한다.

---

### 11. 요약 및 결론

그래픽스 파이프라인에서 삼각형 하나를 띄우기 위해 거쳐 왔던 험난한 대장정을 최종 3줄로 극압축 요약하면 이렇다.

1.  **메모리 스토리지 (VBO/EBO):** GPU VRAM 내부에 정점 부품 좌표 세트(VBO)와 인덱스 조립 설명서(EBO)를 양껏 우겨 넣고 대기시킨다.
2.  **셰이더 두뇌 가동 (GLSL Program):** 공간 원근을 맞추는 정점 단위 두뇌(Vertex Shader)와, 색상 픽셀 물감을 뿌리는 픽셀 단위 두뇌(Fragment Shader) 프로그램을 코딩해 체인으로 이은 뒤 런타임에 GPU 파이프라인 정중앙에 플러그인 시켜 푹 꽂아둔다.
3.  **관리자 호출 및 사격 (VAO & Draw Call):** 모든 복잡한 메모리 속성 맵핑 연결 상태를 하나의 프로필 번호판(VAO)에 클립으로 집어 녹화해 둔 뒤, 렌더링 루프가 1프레임 회전할 때마다 오직 이 VAO 파일표만 호출하여 `glDrawElements` 방아쇠를 당겨 그래픽 카드에 폭격을 명한다.



