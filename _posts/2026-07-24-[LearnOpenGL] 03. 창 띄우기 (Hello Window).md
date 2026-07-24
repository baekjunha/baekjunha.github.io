---
title: "[LearnOpenGL] 03. 창 띄우기 (Hello Window)"
date: 2026-07-24 18:02:26 +0900
categories: [Graphics, LearnOpenGL]
tags: [opengl, cpp, graphics, translation, glfw, glad, hellowindow]
---

> 📢 **안내 및 출처 표기 (Attribution)**
> * 본 포스팅은 Joey de Vries가 작성한 튜토리얼 **[LearnOpenGL.com](https://learnopengl.com/Getting-started/Hello-Window)**의 원문을 바탕으로 한 한국어 번역 및 학습 정리입니다.
> * 원문 저작권은 **Joey de Vries**에게 있으며, **CC BY-NC 4.0** 라이선스를 준수합니다. 원문: [https://learnopengl.com/Getting-started/Hello-Window](https://learnopengl.com/Getting-started/Hello-Window)

---

## 🖥️ 헬로 위도우 (Hello Window)

우리가 그래픽스 프로그래밍을 시작할 때 제일 먼저 부딪히는 장벽은 **"컴퓨터 화면에 어떻게 3D 캔버스(Window)를 띄우고, GPU와 대화를 시작할까?"** 하는 문제입니다. 

운영체제(Windows, macOS, Linux)마다 창을 띄우고 GPU 그래픽 컨텍스트를 가져오는 방식이 전부 다릅니다. 이 차이를 직접 구현하려면 운영체제 전용 코드 수천 줄을 작성해야 하지만, 다행히 **GLFW** 라이브러리가 이 복잡성을 깔끔하게 추상화해 줍니다.

우선 `.cpp` 파일을 하나 생성하고, 파일 최상단에 다음 헤더 파일들을 인클루드합니다.

```cpp
#include <glad/glad.h>
#include <GLFW/glfw3.h>
```

> ### 💡 [깊이 읽기] 왜 GLAD 헤더를 GLFW보다 먼저 포함해야 할까?
> 
> C/C++ 전처리기 맥락에서 헤더 파일의 포함 순서는 생각보다 매우 중요합니다.
> 
> `glad.h`에는 우리가 사용할 최신 OpenGL 함수들의 런타임 포인터 선언과 기본 OpenGL 시스템 헤더(`GL/gl.h`)가 정의되어 있습니다. 반면 `glfw3.h` 내부에는 OpenGL 관련 헤더가 미리 포함되어 있지 않다면 자체적으로 시스템 기본 OpenGL 헤더를 불러오는 로직이 들어있습니다. 
> 
> 만약 GLFW 헤더를 먼저 불러오면 OS에 내장된 오래된 레거시 OpenGL 헤더가 주입되어, 런타임 함수 포인터를 로드해야 하는 GLAD와 심볼 충돌(Duplicate symbols / Undefined reference)이 발생할 수 있습니다. 따라서 **항상 GLAD를 최상단에 놓아 OpenGL 표준 정의를 선점**하게 만들어야 합니다.

---

### 1. GLFW 초기화 및 버전을 향한 협상

다음으로 애플리케이션의 시작점인 `main` 함수를 작성하고 GLFW를 초기화합니다.

```cpp
int main()
{
    // GLFW 초기화
    glfwInit();
    // OpenGL 주요 버전(Major Version)을 3으로 설정
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    // OpenGL 보조 버전(Minor Version)을 3으로 설정
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    // 코어 프로파일(Core-profile) 사용 설정
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    // macOS의 경우 아래 옵션의 주석을 해제해야 합니다.
    // glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);

    return 0;
}
```

`glfwInit()`으로 GLFW 라이브러리를 깨운 뒤 `glfwWindowHint`로 우리가 만들 애플리케이션의 그래픽 스펙을 설정합니다.

이 과정은 **"GPU와 사전 계약을 맺는 과정"**입니다. 우리는 주요 버전(Major) 3, 보조 버전(Minor) 3을 지정하여 **OpenGL 3.3**을 요청하고, `GLFW_OPENGL_CORE_PROFILE`을 명시합니다. 과거 레거시 파이프라인(Immediate mode)의 하위 호환 기능을 완전히 배제하고, 현대적인 셰이더 기반 파이프라인만을 사용하겠다는 다짐입니다. 만약 사용자의 컴퓨터 그래픽 드라이버가 OpenGL 3.3 코어 프로파일을 지원하지 않는다면 GLFW는 창 생성을 거부하게 됩니다.

---

### 2. 창 생성과 OpenGL 컨텍스트(Context) 획득

이어서 실제 화면에 노출될 창 객체(Window Object)를 생성합니다.

```cpp
GLFWwindow* window = glfwCreateWindow(800, 600, "LearnOpenGL", NULL, NULL);
if (window == NULL)
{
    std::cout << "Failed to create GLFW window" << std::endl;
    glfwTerminate();
    return -1;
}
glfwMakeContextCurrent(window);
```

`glfwCreateWindow` 함수는 800x600 해상도와 타이틀바 이름("LearnOpenGL")을 가진 메모리 공간을 생성하고 그 포인터를 반환합니다.

> ### 💡 [깊이 읽기] OpenGL은 상태 머신이다: 컨텍스트(Context)의 의미
> 
> `glfwMakeContextCurrent(window);` 코드는 단순히 창을 지정하는 것 이상의 핵심적인 의미를 갖습니다.
> 
> OpenGL은 내부적으로 거대한 **상태 머신(State Machine)**입니다. 현재 선택된 붓의 색상, 사용할 셰이더, 바인딩된 버퍼 메모리 등의 모든 설정값 집합을 **컨텍스트(Context)**라고 부릅니다. 
> 
> 컴퓨터에는 여러 개의 창이나 스레드가 존재할 수 있습니다. `glfwMakeContextCurrent`를 호출하는 순간, *"앞으로 이 스레드에서 내리는 모든 OpenGL 렌더링 명령은 방금 만든 이 창(`window`)의 그래픽 상태 공간(Context)에 적용해라"* 라고 선언하는 것입니다.

---

## 🔌 GLAD 초기화: 런타임 함수 포인터 연결

OpenGL 컨텍스트를 얻었으니, 이제 `glDrawArrays`나 `glClear` 같은 OpenGL 함수들을 호출할 차례입니다. 하지만 한 가지 걸림돌이 있습니다.

```cpp
if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
{
    std::cout << "Failed to initialize GLAD" << std::endl;
    return -1;
}
```

> ### 💡 [깊이 읽기] 왜 런타임 시점에 함수 주소를 검색해야 하는가?
> 
> C++의 일반적인 라이브러리는 컴파일 시점에 함수 주소가 결정됩니다. 그러나 OpenGL 함수들은 **운영체제와 그래픽 카드 드라이버(NVIDIA, AMD, Intel) 런타임 내부**에 존재합니다. 즉, 사용자의 그래픽 카드마다 함수가 배치된 RAM/VRAM 메모리 주소가 제각각 다릅니다.
> 
> `gladLoadGLLoader`는 GLFW가 제공하는 OS 전용 주소 검색기(`glfwGetProcAddress`)를 빌려, 런타임 시점에 그래픽 카드 드라이버 메모리를 뒤져 수백 개의 OpenGL 함수 포인터 주소를 슬롯에 자동으로 채워넣습니다. 이 과정이 성공해야만 비로소 C++ 코드에서 `glClear` 같은 OpenGL 함수를 정상 호출할 수 있게 됩니다.

---

## 📐 뷰포트 설정 (Viewport): N차원 공간에서 2D 픽셀로

렌더링에 앞서 OpenGL이 처리한 2D 좌표를 실제 화면의 픽셀 좌표계로 변환할 비율을 정해야 합니다.

```cpp
glViewport(0, 0, 800, 600);
```

OpenGL의 내부 가상 좌표계인 **정규화된 기기 좌표(NDC; Normalized Device Coordinates)**는 중앙이 $(0, 0)$이고 좌측 하단이 $(-1, -1)$, 우측 상단이 $(1, 1)$인 $2 \times 2$ 크기의 정규화 공간입니다.

`glViewport(0, 0, 800, 600)`은 이 $-1 \sim 1$ 범위의 NDC 좌표를 화면 창의 $0 \sim 800$ (너비) 및 $0 \sim 600$ (높이) 픽셀 좌표 공간으로 1:1 대응하여 늘려 붙이는(Screen-space Mapping) 기준점을 만듭니다.

창 크기가 사용자에 의해 동적으로 변경될 때 뷰포트도 함께 맞춰지도록 콜백 함수를 등록해 줍니다.

```cpp
void framebuffer_size_callback(GLFWwindow* window, int width, int height)
{
    glViewport(0, 0, width, height);
}

// 창 크기 변경 이벤트 시 콜백 등록
glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);
```

---

## 🔄 렌더 루프 (Render Loop)와 더블 버퍼링

프로그램이 실행되자마자 단 한 순간만 그리고 꺼지지 않도록, 사용자가 닫기 버튼을 누를 때까지 무한히 실행되는 **렌더 루프(Render Loop)**를 구축합니다.

```cpp
while (!glfwWindowShouldClose(window))
{
    // 1. 사용자 입력 처리
    processInput(window);

    // 2. 렌더링 버퍼 교체 및 이벤트 조사
    glfwSwapBuffers(window);
    glfwPollEvents();
}
```

* `glfwWindowShouldClose`: 창 닫기 명령이 내려졌는지 감시합니다.
* `glfwPollEvents`: 키보드/마우스 입력, 창 이동 등의 윈도우 이벤트를 수집하여 콜백 함수를 깨웁니다.

> ### 🎨 [깊이 읽기] 화면이 찢어지지 않는 비밀: 더블 버퍼링 (Double Buffer)
> 
> 그래픽 프로그래밍에서 초당 60회 이상 이미지를 갱신할 때 가장 큰 적은 **화면 찢어짐(Tearing)**과 **깜빡임(Flickering)**입니다.
> 
> 단 하나의 캔버스(Single Buffer)만 사용한다면, GPU가 화면 위쪽부터 아래쪽으로 픽셀을 칠해나가는 어수선한 렌더링 과정이 관객(사용자)의 눈에 그대로 보이게 됩니다.
> 
> 이를 막기 위해 **더블 버퍼링**을 도입합니다:
> 1. **프론트 버퍼 (Front Buffer)**: 지금 관객 화면에 노출되고 있는 완벽히 그려진 도화지
> 2. **백 버퍼 (Back Buffer)**: 관객 뒤에서 GPU가 다음 장면을 조용히 칠하고 있는 무대 뒤 도화지
> 
> GPU는 모든 렌더링 연산을 백 버퍼에서만 수행합니다. 백 버퍼의 픽셀 그리기가 완료되면, `glfwSwapBuffers(window)` 명령으로 **두 버퍼의 포인터만 순식간에 교체(Swap)**합니다. 이 덕분에 사용자는 잔상이나 픽셀 갱신 찰나를 보지 않고 항상 완성된 단일 프레임만 연속해서 감상할 수 있습니다.

---

## 🎨 렌더링 및 창 색상 칠하기 (Rendering)

매 프레임마다 화면을 깨끗이 비우고 원하는 배경색으로 채우는 렌더링 명령을 렌더 루프에 주입합니다.

```cpp
// 렌더 루프
while (!glfwWindowShouldClose(window))
{
    // 입력 처리
    processInput(window);

    // 렌더링 명령 수행 (상태 설정 + 상태 적용)
    glClearColor(0.2f, 0.3f, 0.3f, 1.0f); // 배경색 상태 지정 (Dark Turquoise)
    glClear(GL_COLOR_BUFFER_BIT);          // 프론트/백 버퍼의 색상 버퍼 비우기

    // 이벤트 조사 및 백 버퍼/프론트 버퍼 교체
    glfwPollEvents();
    glfwSwapBuffers(window);
}
```

여기서 `glClearColor`는 *"앞으로 비울 배경색 상태 값"*을 저장하는 **상태 설정 함수(State-setting function)**이며, `glClear`는 지정된 그 색상으로 현재 프레임 버퍼를 실제로 채워버리는 **상태 사용 함수(State-using function)**입니다.

모든 루프가 끝나고 프로그램이 종료되면 할당되었던 GLFW 메모리를 깔끔하게 정리해 줍니다.

```cpp
glfwTerminate();
return 0;
```

---

## 🖼️ 최종 실행 결과

코드를 빌드하고 실행하면 짙은 청록색(Dark Turquoise, RGBA `0.2, 0.3, 0.3, 1.0`) 배경의 아름다운 OpenGL 창이 성공적으로 띄워집니다!

![GLFW Clear Color Output](https://learnopengl.com/img/getting-started/hellowindow2.png)

전체 소스 코드는 [LearnOpenGL Code Repository](https://github.com/JoeyDeVries/LearnOpenGL/blob/master/src/1.getting_started/2.1.hello_window/hello_window.cpp)에서 확인하실 수 있습니다.

