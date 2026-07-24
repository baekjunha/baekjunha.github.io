---
title: "[LearnOpenGL] 03. 창 띄우기 (Hello Window)"
date: 2026-07-24 18:02:26 +0900
categories: [Graphics, LearnOpenGL]
tags: [opengl, cpp, graphics, translation, glfw, glad, hellowindow]
---

```

> 📢 **안내 및 출처 표기 (Attribution)**
> * 본 포스팅은 Joey de Vries가 작성한 튜토리얼 **[LearnOpenGL.com](https://learnopengl.com/Getting-started/Hello-Window)**의 원문을 바탕으로 한 한국어 번역 및 학습 정리입니다.
> * 원문 저작권은 **Joey de Vries**에게 있으며, **CC BY-NC 4.0** 라이선스를 준수합니다. 원문: [https://learnopengl.com/Getting-started/Hello-Window](https://learnopengl.com/Getting-started/Hello-Window)
> 
> 

---

## 헬로 위도우 (Hello Window)

GLFW가 정상적으로 작동하는지 확인해 보겠습니다. 먼저 `.cpp` 파일을 하나 생성하고, 작성한 파일 최상단에 다음 `#include` 구문들을 추가합니다.

```cpp
#include <glad/glad.h>
#include <GLFW/glfw3.h>

```

> **입문자 참고**
> GLAD 헤더 파일은 GLFW보다 먼저 포함(include)해야 합니다. GLAD의 헤더 파일 내부에서 OpenGL에 필요한 관련 헤더(`GL/gl.h` 등)를 알아서 불러오므로, OpenGL 헤더를 요구하는 다른 헤더 파일보다 앞서 포함시켜야 합니다.

다음으로, GLFW 창을 생성할 `main` 함수를 작성합니다.

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

`main` 함수에서는 먼저 `glfwInit` 함수로 GLFW를 초기화합니다. 그 후 `glfwWindowHint` 함수를 사용하여 GLFW 옵션들을 설정합니다. 첫 번째 인자에는 설정하고자 하는 옵션 항목(GLFW_로 시작하는 열거형 값)을 전달하고, 두 번째 인자에는 해당 옵션에 적용할 정수 값을 지정합니다. 설정 가능한 모든 옵션 목록은 [GLFW's window handling](https://www.glfw.org/docs/latest/window_guide.html) 문서에서 확인하실 수 있습니다. 만약 이 상태로 실행했을 때 많은 *undefined reference* 에러가 발생한다면, GLFW 라이브러리가 프로젝트에 제대로 링크되지 않은 것입니다.

이 튜토리얼은 OpenGL 3.3 버전을 기준으로 진행되므로, GLFW에 사용할 OpenGL 버전을 3.3으로 알려줍니다. 이렇게 하면 사용자의 시스템이 해당 OpenGL 버전을 지원하지 않을 때 GLFW가 실행을 거부하도록 설정할 수 있습니다. 주 버전(Major)과 부 버전(Minor)을 모두 3으로 지정하고, 코어 프로파일(Core-profile)을 명시적으로 사용하겠다고 설정합니다. 코어 프로파일을 지정하면 하위 호환성을 위한 하위 지원 기능이 제거된 유용한 핵심 기능들에 접근할 수 있습니다. (macOS 사용자라면 `glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);` 코드를 추가해야 정상 작동합니다.)

> **입문자 참고**
> 시스템이나 그래픽 카드 드라이버에 OpenGL 3.3 이상의 버전이 설치되어 있는지 확인해야 합니다. 그렇지 않으면 애플리케이션이 충돌하거나 정의되지 않은 동작을 일으킬 수 있습니다.

이어서 창 객체(Window Object)를 생성합니다. 이 객체는 모든 창 관련 데이터를 보유하며 GLFW의 다른 함수들에서 지속적으로 참조됩니다.

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

`glfwCreateWindow` 함수는 순서대로 창의 너비(Width), 높이(Height), 창의 제목(Title)을 인자로 받습니다. 마지막 두 인자는 일단 `NULL`로 지정합니다. 이 함수는 생성된 `GLFWwindow` 객체의 포인터를 반환합니다. 생성에 실패하면 `NULL`을 반환합니다. 이후 `glfwMakeContextCurrent`를 호출하여 생성한 창의 컨텍스트(Context)를 현재 스레드의 주 컨텍스트로 지정합니다.

---

## GLAD 초기화 (GLAD)

OpenGL 함수를 호출하기 전에 OpenGL 함수 포인터를 관리해 주는 GLAD를 먼저 초기화해야 합니다.

```cpp
if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
{
    std::cout << "Failed to initialize GLAD" << std::endl;
    return -1;
}

```

GLAD에 OS별로 상이한 OpenGL 함수 포인터 주소를 로드하는 함수를 전달합니다. GLFW는 컴파일 대상 OS에 맞는 적절한 함수 주소를 가져오는 `glfwGetProcAddress` 함수를 제공합니다.

---

## 뷰포트 설정 (Viewport)

렌더링을 시작하기 전에 OpenGL에 렌더링 창의 크기와 좌표계를 알려주어야 합니다. 이는 `glViewport` 함수를 통해 설정합니다.

```cpp
glViewport(0, 0, 800, 600);

```

`glViewport`의 첫 두 인자는 창의 좌측 하단 모서리의 위치를 나타내며, 세 번째와 네 번째 인자는 픽셀 단위의 너비와 높이를 지정합니다.

OpenGL은 내부적으로 `glViewport`로 전달된 데이터를 바탕으로 처리된 2차원 좌표를 화면의 좌표로 변환합니다. 예컨대 처리된 위치 좌표 $(-0.5, 0.5)$는 최종 변환을 거쳐 화면 좌표 $(200, 450)$으로 매핑됩니다. (OpenGL의 정규화된 좌표는 $-1$에서 $1$ 사이이며, 이를 $0 \sim 800$, $0 \sim 600$ 범위로 매핑합니다.)

사용자가 창의 크기를 조절할 때 뷰포트도 함께 변경되어야 합니다. 이를 위해 창 크기가 변경될 때마다 호출될 콜백 함수(Callback function)를 등록할 수 있습니다.

```cpp
void framebuffer_size_callback(GLFWwindow* window, int width, int height)
{
    glViewport(0, 0, width, height);
}

```

그리고 GLFW가 창 크기 변경 시 이 함수를 호출하도록 등록합니다.

```cpp
glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

```

---

## 렌더 루프 (Render Loop)

애플리케이션이 단 한 프레임을 그리고 즉시 종료되지 않도록, 사용자가 중지 명령을 내릴 때까지 이미지 연산과 사용자 입력을 계속 처리하는 `while` 루프를 만듭니다. 이를 렌더 루프(render loop)라고 부릅니다.

```cpp
while (!glfwWindowShouldClose(window))
{
    // 입력 처리
    processInput(window);

    // 렌더링 버퍼 교체 및 이벤트 조사
    glfwSwapBuffers(window);
    glfwPollEvents();
}

```

* `glfwWindowShouldClose`: 루프 반복마다 GLFW가 종료 명령을 받았는지 확인합니다.
* `glfwPollEvents`: 키보드 입력이나 마우스 이동 등 발생한 이벤트를 조사하고 등록된 콜백 함수를 호출합니다.
* `glfwSwapBuffers`: 컬러 버퍼(Color Buffer)를 교체(Swap)하여 화면에 출력합니다.

> **입문자 참고: 더블 버퍼링 (Double Buffer)**
> 단일 버퍼로 그릴 경우, 이미지가 좌측 상단에서 우측 하단으로 화면에 픽셀 단위로 그려지는 과정이 노출되어 깜빡임(Flickering) 현상이 생길 수 있습니다. 이를 방지하기 위해 **더블 버퍼**를 사용합니다. 화면에 표시되는 **프론트 버퍼(Front buffer)**와 렌더링 명령이 기록되는 **백 버퍼(Back buffer)**를 두고, 백 버퍼 생성이 완료되면 두 버퍼를 교체하여 잔상 없는 깨끗한 화면을 표시합니다.

---

## 자원 해제 (Clean up)

렌더 루프가 끝나면 할당되었던 GLFW의 자원들을 정리해야 합니다.

```cpp
glfwTerminate();
return 0;

```


컴파일을 완료하고 실행하면 다음과 같은 검은색 창 출력을 확인할 수 있습니다.

![GLFW Window Output](https://learnopengl.com/img/getting-started/hellowindow.png)

---

## 사용자 입력 처리 (Input)

`glfwGetKey` 함수를 활용해 입력 이벤트를 처리할 수 있습니다. ESC 키를 누르면 창이 닫히도록 설정하는 `processInput` 함수를 정의합니다.

```cpp
void processInput(GLFWwindow *window)
{
    if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true);
}

```

이 함수를 렌더 루프 매 프레임마다 호출합니다.

```cpp
while (!glfwWindowShouldClose(window))
{
    processInput(window);

    glfwSwapBuffers(window);
    glfwPollEvents();
}

```

---

## 렌더링 (Rendering)

모든 렌더링 명령은 매 프레임 실행되도록 렌더 루프 내부에 위치해야 합니다.

```cpp
// 렌더 루프
while (!glfwWindowShouldClose(window))
{
    // 입력 처리
    processInput(window);

    // 렌더링 명령 수행
    glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);

    // 이벤트 체크 및 버퍼 교체
    glfwPollEvents();
    glfwSwapBuffers(window);
}

```



프레임 시작 부분에서 화면을 지정한 색상으로 지웁니다. `glClearColor`는 화면을 지울 색상을 지정하는 상태 설정 함수이며, `glClear`는 지정된 버퍼(여기서는 `GL_COLOR_BUFFER_BIT`)를 지우는 상태 사용 함수입니다.

![GLFW Clear Color Output](https://learnopengl.com/img/getting-started/hellowindow2.png)
전체 소스 코드는 [LearnOpenGL Code Repository](https://www.google.com/search?q=https://learnopengl.com/code_viewer_gh.php%3Fcode%3Dsrc/1.getting_started/2.1.hello_window/hello_window.cpp)에서 확인하실 수 있습니다.
