---
title: "[LearnOpenGL] 03. Hello Window (Hello Window)"
date: 2026-07-24 17:39:08 +0900
categories: [Graphics, LearnOpenGL]
tags: [opengl, cpp, graphics, translation, glfw, glad, window, renderloop]
---

> 📢 **안내 및 출처 표기 (Attribution)**
> * 본 포스팅은 Joey de Vries가 작성한 튜토리얼 **[LearnOpenGL.com](https://learnopengl.com/Getting-started/Hello-Window)**의 원문을 바탕으로 한 한국어 번역 및 학습 정리입니다.
> * 원문 저작권은 **Joey de Vries**에게 있으며, **CC BY-NC 4.0** 라이선스를 준수합니다. 원문: [https://learnopengl.com/Getting-started/Hello-Window](https://learnopengl.com/Getting-started/Hello-Window)


이전 장에 이어 GLFW를 정상적으로 작동시켜 보겠습니다. 먼저 `.cpp` 파일을 생성하고 파일 최상단에 다음 헤더 파일들을 포함(include)합니다.

```cpp
#include <glad/glad.h>
#include <GLFW/glfw3.h>

```

> **입문자 참고**
> 반드시 GLFW보다 **GLAD를 먼저 include**해야 합니다. GLAD 헤더 파일에는 내부적으로 필수적인 OpenGL 헤더(`GL/gl.h` 등)가 포함되어 있으므로, OpenGL을 필요로 하는 다른 헤더 파일(GLFW 등)보다 앞서 선언되어야 합니다.

다음으로, GLFW 창(window)을 인스턴스화할 `main` 함수를 작성합니다.

```cpp
int main()
{
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    // glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);

    return 0;
}

```

`main` 함수 내에서 먼저 `glfwInit`을 호출하여 GLFW를 초기화합니다. 이후 `glfwWindowHint`를 사용하여 GLFW의 다양한 옵션 설정을 진행합니다.

`glfwWindowHint`의 첫 번째 인자는 설정하고자 하는 옵션이며, `GLFW_` 접두사가 붙은 열거형(enum) 값 중 하나를 선택합니다. 두 번째 인자는 설정할 옵션의 정수 값입니다. 설정 가능한 전체 옵션 목록과 값은 [GLFW Window Handling 문서](https://www.glfw.org/docs/latest/window_guide.html)에서 확인할 수 있습니다. 만약 이 단계에서 애플리케이션을 실행했을 때 많은 *undefined reference* 에러가 발생한다면, GLFW 라이브러리가 올바르게 링크되지 않은 것입니다.

이 튜토리얼의 중심 주제는 **OpenGL 3.3 버전**이므로, GLFW에 우리가 사용할 OpenGL 버전을 알려주어야 합니다. 이렇게 하면 GLFW가 OpenGL 컨텍스트(context)를 생성할 때 이에 맞는 준비를 할 수 있으며, 사용자의 시스템에 적합한 OpenGL 버전이 없는 경우 실행을 안전하게 중단시킵니다.

주 버전(Major)과 부 버전(Minor)을 모두 `3`으로 설정하고, explicit하게 코어 프로필(Core-profile)을 사용하도록 지정합니다. 코어 프로필을 사용한다는 것은 하위 호환성을 유지하기 위한 구식 기능들을 제거하고, 접근 가능한 더 작은 범위의 최신 기능 집합만을 사용하겠다는 의미입니다.

> **macOS 사용자 참고**
> macOS 환경에서는 위의 초기화 코드에 `glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);` 구문을 반드시 추가해야 정상적으로 작동합니다.

시스템 hardware에 OpenGL 3.3 이상의 버전이 설치되어 있는지 확인하세요. 그렇지 않으면 애플리케이션이 멈추거나 정의되지 않은 동작을 유발할 수 있습니다. 리눅스 환경이라면 `glxinfo` 명령어를 실행하고, 윈도우 환경이라면 [OpenGL Extension Viewer](http://www.realtech-vr.com/glview/) 같은 유틸리티를 사용하여 설치된 OpenGL 버전을 확인할 수 있습니다. 지원 버전이 낮다면 그래픽 카드가 OpenGL 3.3+을 지원하는지 확인하고 드라이버를 업데이트하세요.

---

## 창 객체 생성 (Creating a Window)

다음으로 창 객체(Window Object)를 생성해야 합니다. 이 객체는 모든 창 관련 데이터를 담고 있으며, GLFW의 대부분의 다른 함수에서 필수적으로 요구됩니다.

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

`glfwCreateWindow` 함수는 첫 번째와 두 번째 인자로 창의 가로(width)와 세로(height) 크기를 지정합니다. 세 번째 인자는 창의 타이틀 이름을 설정하며, 원하는 이름으로 지정할 수 있습니다. 마지막 두 인자는 우선 무시하셔도 됩니다.

이 함수는 이후 다른 GLFW 작업에 사용될 `GLFWwindow` 객체를 반환합니다. 창 생성 후에는 `glfwMakeContextCurrent`를 호출하여 생성한 창의 컨텍스트를 현재 스레드의 주 컨텍스트로 설정해 줍니다.

---

## GLAD 초기화

이전 장에서 설명했듯이 GLAD는 OpenGL의 함수 포인터(function pointer)를 관리하므로, OpenGL 관련 함수를 호출하기 전에 GLAD를 먼저 초기화해야 합니다.

```cpp
if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
{
    std::cout << "Failed to initialize GLAD" << std::endl;
    return -1;
}

```

GLAD에는 운영체제에 따라 달라지는 OpenGL 함수 포인터의 주소를 로드하는 함수를 전달해야 합니다. GLFW는 컴파일 대상 OS에 맞는 적절한 함수를 정의해 주는 `glfwGetProcAddress` 함수를 제공하므로 이를 매개변수로 전달합니다.

---

## 뷰포트 (Viewport)

렌더링을 시작하기 전 한 가지 작업을 더 수행해야 합니다. OpenGL에 렌더링 창의 크기를 알려주어 OpenGL이 데이터와 좌표를 창의 크기에 맞게 표시하는 방법을 인식하도록 해야 합니다. 이는 `glViewport` 함수를 통해 설정할 수 있습니다.

```cpp
glViewport(0, 0, 800, 600);

```

`glViewport`의 처음 두 매개변수는 창의 좌측 하단 모서리 위치를 설정합니다. 세 번째와 네 번째 매개변수는 렌더링 창의 가로와 세로 크기(픽셀 단위)를 지정하며, 여기서는 GLFW 창 크기와 동일하게 설정했습니다.

> **입문자 참고**
> 뷰포트 크기를 GLFW 창 크기보다 작게 설정할 수도 있습니다. 이렇게 하면 모든 OpenGL 렌더링이 더 작은 영역 안에서 표시되며, 뷰포트 외부에 다른 UI 요소 등을 배치하는 방식으로 활용이 가능합니다.

OpenGL은 내부적으로 `glViewport`로 지정된 데이터를 사용해 처리된 2차원 좌표를 화면 상의 실제 좌표로 변환합니다. 예를 들어 처리된 좌표 $(-0.5, 0.5)$는 최종 변환을 거쳐 화면 좌표 $(200, 450)$으로 매핑됩니다. OpenGL의 처리 좌표 범위는 $-1$에서 $1$ 사이이므로, 이를 $(0, 800)$ 및 $(0, 600)$ 범위로 매핑하는 것입니다.

하지만 사용자가 창의 크기를 조정하는 즉시 뷰포트도 함께 변경되어야 합니다. 창 크기가 변경될 때마다 호출되는 콜백 함수(callback function)를 등록할 수 있습니다. 프레임버퍼 크기 조정을 위한 콜백 함수 프로토타입은 다음과 같습니다.

```cpp
void framebuffer_size_callback(GLFWwindow* window, int width, int height);

```

이 함수는 첫 번째 인자로 `GLFWwindow`를 받고, 창의 새로운 차원(가로, 세로 크기)을 정수로 받습니다. 창 크기가 변경될 때마다 GLFW가 이 함수를 호출하여 새로 조정된 인자들을 채워줍니다.

```cpp
void framebuffer_size_callback(GLFWwindow* window, int width, int height)
{
    glViewport(0, 0, width, height);
}

```

창 크기가 변경될 때 해당 콜백 함수를 호출하도록 GLFW에 알려주어야 하므로, 콜백 함수를 등록해 줍니다.

```cpp
glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

```

창이 처음 화면에 표시될 때도 `framebuffer_size_callback`이 호출되어 결과적인 창 크기가 적용됩니다. 고해상도(Retina 등) 디스플레이의 경우, 가로 및 세로 크기가 초기 입력값보다 훨씬 크게 설정될 수 있습니다.

GLFW에는 조이스틱 입력 변경 처리, 에러 메시지 처리 등 다양한 이벤트를 등록할 수 있는 수많은 콜백 함수가 존재합니다. 콜백 함수 등록은 창을 생성한 후, 렌더 루프(render loop)가 시작되기 전에 진행합니다.

---

## 렌더 루프 (Ready your engines)

애플리케이션이 단 한 프레임의 이미지만 그리고 즉시 종료되는 대신, 프로그램에 중단 명령이 전달될 때까지 계속해서 이미지를 새로 그리고 사용자 입력을 처리하도록 만들어야 합니다. 이를 위해 명시적으로 정지 명령을 내릴 때까지 계속 실행되는 `while` 루프, 즉 렌더 루프(render loop)를 작성합니다.

가장 단순한 형태의 렌더 루프 구조는 다음과 같습니다.

```cpp
while (!glfwWindowShouldClose(window))
{
    glfwSwapBuffers(window);
    glfwPollEvents();    
}

```

* `glfwWindowShouldClose`: 루프 반복 시작 시 GLFW가 종료하도록 지시받았는지 확인합니다. 종료 요청이 들어왔다면 `true`를 반환하여 렌더 루프를 중단시키고 애플리케이션을 종료할 수 있게 합니다.
* `glfwPollEvents`: 키보드 입력이나 마우스 이동 등의 이벤트가 발생했는지 확인하고, 창 상태를 업데이트하며 등록된 콜백 함수들을 호출합니다.
* `glfwSwapBuffers`: 이번 렌더링 반복 단계 동안 그래픽을 그리는 데 사용된 컬러 버퍼(color buffer)를 교체하여 화면에 출력 결과물로 보여줍니다.

> **이중 버퍼 (Double Buffer)**
> 단일 버퍼에서 애플리케이션을 그릴 경우 화면이 번쩍이는 왜곡 현상(flickering)이 발생할 수 있습니다. 이미지가 즉각적으로 한 번에 그려지는 것이 아니라 좌측 상단에서 우측 하단으로 픽셀 단위로 그려지기 때문입니다. 이러한 렌더링 도중의 불완전한 상태가 사용자에게 노출되는 것을 방지하기 위해 이중 버퍼 기법을 적용합니다.
> **전면(Front) 버퍼**는 화면에 표시되는 최종 출력을 담고 있으며, 모든 렌더링 명령은 **후면(Back) 버퍼**에 작성됩니다. 후면 버퍼에 그리기 작업이 모두 완료되면 전면 버퍼와 후면 버퍼를 **교체(Swap)**하여 불완전하게 그려지는 이미지 잔상을 제거합니다.

---

## 자원 해제 (One last thing)

렌더 루프를 벗어나면 할당되었던 모든 GLFW 자원을 깔끔하게 정리하고 삭제해야 합니다. `main` 함수 종료 지점에서 `glfwTerminate` 함수를 호출하여 처리합니다.

```cpp
glfwTerminate();
return 0;

```

이 함수는 모든 자원을 정리하고 애플리케이션을 올바르게 종료시킵니다. 이제 작성한 코드를 컴파일해 보세요. 모든 작업이 정상적으로 완료되었다면 다음과 같은 출력을 확인할 수 있습니다.

단조롭고 지루한 검은색 화면이 나오더라도 당황하지 마세요. 올바르게 동작하고 있는 것입니다! 예상한 이미지가 나오지 않거나 전체적인 구조가 헷갈린다면 [전체 소스 코드](https://learnopengl.com/code_viewer_gh.php?code=src/1.getting_started/1.2.hello_window_clear/hello_window_clear.cpp)를 확인하시기 바랍니다.

---

## 사용자 입력 처리 (Input)

GLFW에서 키보드 입력을 제어하는 방법은 여러 입력 함수를 사용하는 것입니다. 대표적으로 `glfwGetKey` 함수는 입력 상태를 확인할 창 객체와 검사할 키(Key) 값을 인자로 받습니다. 이 함수는 해당 키가 현재 눌려 있는지의 여부를 반환합니다.

입력 처리 코드를 깔끔하게 유지하기 위해 `processInput` 함수를 새로 작성해 보겠습니다.

```cpp
void processInput(GLFWwindow *window)
{
    if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true);
}

```

이 함수는 사용자가 ESC 키를 눌렀는지 확인합니다(눌리지 않았다면 `GLFW_RELEASE`를 반환합니다). ESC 키가 눌렸다면 `glfwSetWindowShouldClose`를 호출하여 창의 `WindowShouldClose` 속성을 `true`로 설정하고 GLFW 종료 준비를 합니다. 그 다음 프레임의 `while` 루프 조건 검사에서 조건이 거짓이 되어 애플리케이션이 안전하게 종료됩니다.

이 작성한 함수를 매 프레임마다 렌더 루프 안에서 호출합니다.

```cpp
while (!glfwWindowShouldClose(window))
{
    processInput(window);

    glfwSwapBuffers(window);
    glfwPollEvents();
}

```

이를 통해 매 프레임마다 특정 키 입력을 확인하고 그에 맞는 반응을 쉽게 구현할 수 있습니다. 렌더 루프의 한 번의 반복 실행 단위를 흔히 프레임(frame)이라고 부릅니다.

---

## 렌더링 (Rendering)

모든 렌더링 명령은 매 루프 반복(프레임)마다 실행되어야 하므로 렌더 루프 내부의 적절한 위치에 배치해야 합니다.

```cpp
// 렌더 루프 (render loop)
while (!glfwWindowShouldClose(window))
{
    // 입력 처리 (input)
    processInput(window);

    // 렌더링 명령 작성 위치 (rendering commands here)
    // ...

    // 이벤트 확인 및 버퍼 교체 (check and call events and swap the buffers)
    glfwPollEvents();
    glfwSwapBuffers(window);
}

```

렌더링이 동작하는지 테스트하기 위해 화면을 원하는 색상으로 지워보는(clear) 작업을 해봅시다. 매 프레임 시작 시 이전 프레임의 잔상을 지우기 위해 화면을 초기화해야 합니다. `glClear` 함수에 단 비트(buffer bits)를 지정하여 원하는 버퍼를 비울 수 있으며, 설정 가능한 비트 종류는 `GL_COLOR_BUFFER_BIT`, `GL_DEPTH_BUFFER_BIT`, `GL_STENCIL_BUFFER_BIT`가 있습니다. 현재는 색상 값만 다루므로 컬러 버퍼만 비워줍니다.

```cpp
glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
glClear(GL_COLOR_BUFFER_BIT);

```

`glClearColor` 함수를 사용해 화면을 비울 단색(Clear color)을 미리 지정해 둔다는 점에 유의하세요. `glClear`가 호출되어 컬러 버퍼를 지울 때마다, 전체 버퍼가 `glClearColor`에 설정된 어두운 청록색 계열로 채워집니다.

> **상태 설정과 상태 사용 함수**
> 이전 장에서 다룬 것처럼 `glClearColor`는 **상태 설정 함수(state-setting function)**이고, `glClear`는 설정된 현재 상태에서 색상 값을 가져와 버퍼를 비우는 **상태 사용 함수(state-using function)**입니다.

이 단계까지 완성된 전체 소스 코드는 [이곳](https://learnopengl.com/code_viewer_gh.php?code=src/1.getting_started/1.2.hello_window_clear/hello_window_clear.cpp)에서 확인하실 수 있습니다.

이제 렌더 루프에 다양한 렌더링 호출 구문들을 채워 넣을 모든 준비를 마쳤습니다. 다음 장에서 본격적인 그래픽 그리기 작업을 이어서 진행하겠습니다.
