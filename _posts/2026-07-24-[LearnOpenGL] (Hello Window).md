---

title: "[LearnOpenGL] 03. Hello Window (Hello Window)"
date: 2026-07-24 17:56:32 +0900
categories: [Graphics, LearnOpenGL]
tags: [opengl, cpp, graphics, translation, glfw, glad, window]

---
> 📢 **안내 및 출처 표기 (Attribution)**
> * 본 포스팅은 Joey de Vries가 작성한 튜토리얼 **[LearnOpenGL.com](https://learnopengl.com/Getting-started/Hello-Window)**의 원문을 바탕으로 한 한국어 번역 및 학습 정리입니다.
> * 원문 저작권은 **Joey de Vries**에게 있으며, **CC BY-NC 4.0** 라이선스를 준수합니다. 원문: [https://learnopengl.com/Getting-started/Hello-Window](https://learnopengl.com/Getting-started/Hello-Window)
> 
> 


## Hello Window

GLFW가 정상적으로 작동하는지 확인해 보겠습니다. 먼저 `.cpp` 파일을 생성하고, 해당 파일의 최상단에 다음 헤더 파일들을 포함(include)합니다.

```cpp
#include <glad/glad.h>
#include <GLFW/glfw3.h>

```

> **입문자 참고**
> 반드시 GLFW보다 **GLAD를 먼저 include**해야 합니다. GLAD의 헤더 파일에는 뒤에서 필요한 OpenGL 헤더(`GL/gl.h` 등)가 포함되어 있으므로, OpenGL을 필요로 하는 다른 헤더 파일보다 앞서 포함시켜야 합니다.

다음으로, GLFW 창을 생성하고 인스턴스화할 `main` 함수를 작성합니다.

```cpp
int main()
{
    // GLFW 초기화
    glfwInit();
    // OpenGL 버전 설정 (3.3)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    // 코어 프로필(Core-profile) 사용 설정
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    // macOS의 경우 아래 라인의 주석을 해제해야 합니다.
    // glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);

    return 0;
}

```

`main` 함수에서는 먼저 `glfwInit`을 호출해 GLFW를 초기화합니다. 이후 `glfwWindowHint`를 사용하여 GLFW를 설정할 수 있습니다. `glfwWindowHint`의 첫 번째 인자는 설정하고자 하는 옵션으로, `GLFW_` 접두사가 붙은 열거형(enum) 값 중에서 선택합니다. 두 번째 인자는 해당 옵션에 할당할 정수 값입니다. 설정 가능한 모든 옵션 목록은 [GLFW의 창 관리 문서](https://www.google.com/search?q=https://www.glfw.org/docs/latest/window.html)에서 확인할 수 있습니다. 만약 앱 실행 시 정의되지 않은 참조(undefined reference) 에러가 많이 발생한다면, GLFW 라이브러리가 성공적으로 링크되지 않은 것입니다.

본 튜토리얼은 OpenGL 3.3 버전에 초점을 맞추므로, GLFW에 사용하고자 하는 OpenGL 버전이 3.3임을 알려줍니다. 이렇게 하면 GLFW가 OpenGL 컨텍스트(context)를 생성할 때 적절하게 준비할 수 있으며, 사용자의 시스템이 해당 OpenGL 버전을 지원하지 않을 경우 실행을 중단합니다. 주 버전(major)과 부 버전(minor)을 모두 3으로 설정합니다. 또한 코어 프로필(core-profile)을 명시적으로 사용하겠다고 설정합니다. 코어 프로필을 사용하면 더 이상 필요하지 않은 하위 호환 기능 없이, 더 작고 유용한 OpenGL 기능 집합에만 접근하게 됩니다. macOS 환경에서는 해당 코드가 작동하려면 `glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);` 구문을 추가해야 합니다.

시스템 및 그래픽 카드에 OpenGL 3.3 이상의 버전이 설치되어 있는지 확인하세요. 그렇지 않으면 애플리케이션이 충돌하거나 정의되지 않은 동작을 보일 수 있습니다. 시스템의 OpenGL 버전을 확인하려면 Linux에서는 `glxinfo`를 호출하거나 Windows에서는 [OpenGL Extension Viewer](http://www.realtech-vr.com/glview/)와 같은 유틸리티를 사용하세요.

---

### 창 객체 생성 (Creating a window)

다음으로 창 객체(window object)를 생성해야 합니다. 이 창 객체는 모든 창 관련 데이터를 보유하며, GLFW의 다른 대부분의 함수에서 필요로 합니다.

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

`glfwCreateWindow` 함수는 첫 번째와 두 번째 인자로 창의 너비(width)와 높이(height)를 받습니다. 세 번째 인자는 창의 타이틀을 설정하며, 여기서는 `"LearnOpenGL"`로 지정했습니다. 마지막 두 인자는 우선 무시해도 됩니다. 이 함수는 이후 다른 GLFW 작업에 사용할 `GLFWwindow` 객체의 포인터를 반환합니다. 창을 생성한 후에는 `glfwMakeContextCurrent`를 호출하여 생성한 창의 컨텍스트를 현재 쓰레드의 주 컨텍스트로 설정합니다.

---

## GLAD

GLAD는 OpenGL의 함수 포인터(function pointer)를 관리하므로, 어떠한 OpenGL 함수를 호출하기 전에 먼저 GLAD를 초기화해야 합니다.

```cpp
if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
{
    std::cout << "Failed to initialize GLAD" << std::endl;
    return -1;
}

```

GLAD에는 OpenGL 함수 포인터의 주소를 로드하는 OS 별 함수를 전달합니다. GLFW는 컴파일 타임의 운영체제에 맞춰 올바른 함수를 정의해 주는 `glfwGetProcAddress` 함수를 제공합니다.

---

## 뷰포트 (Viewport)

렌더링을 시작하기 전에 마지막으로 해야 할 작업이 있습니다. OpenGL에게 렌더링 창의 크기를 알려주어 데이터와 좌표를 창에 어떻게 표시할지 알 수 있도록 해야 합니다. 이 치수는 `glViewport` 함수를 통해 설정합니다.

```cpp
glViewport(0, 0, 800, 600);

```

`glViewport`의 첫 두 매개변수는 창의 좌측 하단 모서리 위치를 설정합니다. 세 번째와 네 번째 매개변수는 렌더링 창의 너비와 높이를 픽셀 단위로 설정하며, 이는 GLFW 창의 크기와 동일하게 설정합니다.

뷰포트 차원을 GLFW의 크기보다 작게 설정할 수도 있습니다. 그렇게 하면 모든 OpenGL 렌더링이 더 작은 창 안에 표시되며, 뷰포트 외부에 다른 요소들을 배치할 수 있습니다.

> **입문자 참고**
> OpenGL은 `glViewport`를 통해 지정된 데이터를 바탕으로 처리된 2D 좌표를 화면상의 좌표로 변환합니다. 예를 들어, 처리된 지점의 위치가 `(-0.5, 0.5)`라면 최종 변환을 거쳐 화면 좌표 `(200, 450)`으로 매핑됩니다. OpenGL의 정규화된 좌표(Normalized Device Coordinates)는 `-1`에서 `1` 사이이므로, 결과적으로 `(-1 ~ 1)` 범위가 `(0, 800)` 및 `(0, 600)`으로 매핑됩니다.

하지만 사용자가 창의 크기를 조정하는 순간 뷰포트도 함께 조정되어야 합니다. 창 크기가 변경될 때마다 호출되는 콜백 함수(callback function)를 창에 등록할 수 있습니다. 이 크기 조절 콜백 함수의 프로토타입은 다음과 같습니다.

```cpp
void framebuffer_size_callback(GLFWwindow* window, int width, int height);

```

프레임버퍼 크기 함수는 첫 번째 인자로 `GLFWwindow`를 받고, 새 창의 크기를 나타내는 두 개의 정수를 인자로 받습니다. 창 크기가 변경될 때마다 GLFW는 이 함수를 호출하여 알맞은 인수를 채워줍니다.

```cpp
void framebuffer_size_callback(GLFWwindow* window, int width, int height)
{
    glViewport(0, 0, width, height);
}

```

창 크기가 변경될 때마다 이 함수를 호출하도록 GLFW에 등록해야 합니다.

```cpp
glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

```

창이 처음 표시될 때도 변경된 창 차원과 함께 `framebuffer_size_callback`이 호출됩니다. 레티나(Retina) 디스플레이의 경우 너비와 높이가 원래 입력 값보다 훨씬 높게 설정될 수 있습니다.

사용자 정의 함수를 등록할 수 있는 콜백 함수는 다양합니다. 예를 들어 조이스틱 입력 변경, 에러 메시지 처리 등을 위한 콜백 함수를 만들 수 있습니다. 창을 생성한 후, 렌더 루프가 시작되기 전에 이러한 콜백 함수들을 등록합니다.

---

## 렌더 루프 (Render Loop)

애플리케이션이 단 하나의 이미지만 그리고 즉시 종료되는 것을 원치 않으며, 명시적으로 중지할 때까지 계속해서 이미지를 그리고 사용자 입력을 처리하도록 해야 합니다. 이를 위해 프로그램을 계속 실행하는 `while` 루프, 즉 렌더 루프(render loop)를 작성해야 합니다.

다음 코드는 아주 간단한 렌더 루프의 예시입니다.

```cpp
while (!glfwWindowShouldClose(window))
{
    // 버퍼 교체 (Double Buffering)
    glfwSwapBuffers(window);
    // 이벤트 조사 및 콜백 함수 호출
    glfwPollEvents();    
}

```

* `glfwWindowShouldClose`: 각 루프 반복의 시작 부분에서 GLFW가 종료하도록 지시받았는지 확인합니다. 만약 그렇다면 `true`를 반환하여 렌더 루프가 종료되고 애플리케이션을 닫을 수 있게 됩니다.
* `glfwPollEvents`: 키보드 입력이나 마우스 이동 이벤트가 발생했는지 확인하고, 창 상태를 업데이트하며 등록된 콜백 함수들을 호출합니다.
* `glfwSwapBuffers`: 이번 렌더링 반복 동안 프레임 버퍼에 그려진 컬러 버퍼(2D 버퍼)를 교체하여 화면에 출력합니다.

> **더블 버퍼링 (Double Buffer)**
> 애플리케이션이 단일 버퍼에 그림을 그릴 경우 깜빡임(flickering) 현상이 발생할 수 있습니다. 이미지가 순간적으로 한 번에 그려지는 것이 아니라 픽셀 단위로 좌에서 우, 위에서 아래로 그려지기 때문입니다. 이 문제를 방지하기 위해 렌더링 애플리케이션은 더블 버퍼를 적용합니다. **전면(Front) 버퍼**는 화면에 표시되는 최종 출력 이미지를 담고 있으며, 모든 렌더링 명령은 **후면(Back) 버퍼**에 그려집니다. 모든 렌더링 명령이 완료되면 후면 버퍼와 전면 버퍼를 **교체(swap)**하여 잔상이나 깜빡임 없이 완성된 이미지를 보여줍니다.

---

### 자원 해제 (One last thing)

렌더 루프를 빠져나오면 할당되었던 GLFW의 모든 자원을 적절히 정리하고 삭제해야 합니다. `main` 함수의 끝에서 `glfwTerminate` 함수를 호출하여 이 작업을 수행합니다.

```cpp
glfwTerminate();
return 0;

```

이제 애플리케이션을 컴파일해 보세요. 모든 과정이 성공적으로 진행되었다면 다음과 같은 윈도우 출력을 확인할 수 있습니다.

검은색의 심심한 창이 나타난다면 성공적으로 작성된 것입니다! 결과가 올바르지 않거나 코드 구조가 헷갈린다면 [전체 소스 코드](https://learnopengl.com/code_viewer_gh.php?code=src/1.getting_started/1.2.hello_window_clear/hello_window_clear.cpp)를 확인해 보세요.

---

## 사용자 입력 처리 (Input)

GLFW에서는 다양한 입력 함수를 통해 제어할 수 있습니다. `glfwGetKey` 함수는 창 객체와 키 값을 인자로 받아 해당 키가 현재 눌려 있는지 여부를 반환합니다. 입력을 깔끔하게 정리하기 위해 `processInput` 함수를 새로 작성합니다.

```cpp
void processInput(GLFWwindow *window)
{
    // ESC 키가 눌렸는지 확인
    if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true);
}

```

여기서는 사용자가 ESC 키를 눌렀는지 확인합니다(눌리지 않았다면 `GLFW_RELEASE`를 반환합니다). ESC 키가 눌렸다면 `glfwSetWindowShouldClose`를 호출하여 `WindowShouldClose` 속성을 `true`로 변경함으로써 GLFW를 종료하도록 설정합니다. 다음 렌더 루프 조건 확인 시 조건이 거짓이 되어 애플리케이션이 종료됩니다.

이후 렌더 루프의 각 프레임마다 `processInput`을 호출합니다.

```cpp
while (!glfwWindowShouldClose(window))
{
    // 입력 처리
    processInput(window);

    // 버퍼 교체 및 이벤트 폴링
    glfwSwapBuffers(window);
    glfwPollEvents();
}

```

이를 통해 매 프레임(frame)마다 특정 키 입력을 쉽게 확인하고 반응할 수 있습니다.

---

## 렌더링 (Rendering)

모든 렌더링 명령은 매 프레임 반복 실행되어야 하므로 렌더 루프 내에 작성합니다.

```cpp
// 렌더 루프 (render loop)
while (!glfwWindowShouldClose(window))
{
    // 1. 입력 처리 (input)
    processInput(window);

    // 2. 렌더링 명령 수행 (rendering commands)
    // ...

    // 3. 이벤트 조사 및 버퍼 교체 (check/call events and swap buffers)
    glfwPollEvents();
    glfwSwapBuffers(window);
}

```

정상 작동하는지 테스트하기 위해 선택한 색상으로 화면을 지워(clear) 봅니다. 매 프레임 시작 시 화면을 지우지 않으면 이전 프레임의 결과가 그대로 남아있게 됩니다. `glClear` 함수를 사용하여 색상 버퍼를 지우며, 지우고자 하는 버퍼 비트를 지정합니다. 설정 가능한 비트는 `GL_COLOR_BUFFER_BIT`, `GL_DEPTH_BUFFER_BIT`, `GL_STENCIL_BUFFER_BIT`가 있으며, 지금은 색상 값만 신경 쓰므로 `GL_COLOR_BUFFER_BIT`만 지웁니다.

```cpp
glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
glClear(GL_COLOR_BUFFER_BIT);

```

`glClearColor`를 사용하여 화면을 지울 때 사용할 색상을 지정합니다. `glClear`를 호출하면 색상 버퍼 전체가 `glClearColor`에서 설정한 어두운 청록색으로 채워집니다.

> **입문자 참고**
> `glClearColor`는 **상태 설정 함수(state-setting function)**이며, `glClear`는 지우기 색상을 가져와 적용하는 **상태 사용 함수(state-using function)**입니다.

해당 애플리케이션의 전체 소스 코드는 [여기](https://learnopengl.com/code_viewer_gh.php?code=src/1.getting_started/1.2.hello_window_clear/hello_window_clear.cpp)에서 확인할 수 있습니다.

이제 렌더 루프를 다양한 렌더링 호출로 채울 준비를 마쳤습니다. 다음 장에서 본격적인 렌더링을 다루어 보겠습니다.
