---
title: "[LearnOpenGL] 02. 창 생성하기 (Creating a window)"
date: 2026-07-24 17:39:08 +0900
categories: [Graphics, LearnOpenGL]
tags: [opengl, cpp, graphics, translation, glfw, glad, window, renderloop]
---

> 📢 **안내 및 출처 표기 (Attribution)**
> * 본 포스팅은 Joey de Vries가 작성한 튜토리얼 **[LearnOpenGL.com](https://learnopengl.com/Getting-started/Creating-a-window)**의 원문을 바탕으로 한 한국어 번역 및 학습 정리입니다.
> * 원문 저작권은 **Joey de Vries**에게 있으며, **CC BY-NC 4.0** 라이선스를 준수합니다. 원문: [https://learnopengl.com/Getting-started/Creating-a-window](https://learnopengl.com/Getting-started/Creating-a-window)

---

## GLFW 설정

이제 GLFW를 실제로 사용해봅시다. 먼저 새로운 `.cpp` 파일을 생성하고, 파일 최상단에 GLAD와 GLFW의 헤더 파일을 포함합니다.

```cpp
#include <glad/glad.h>
#include <GLFW/glfw3.h>
```

> **⚠️ 헤더 파일 순서 주의**
> GLAD는 **GLFW보다 먼저 include**해야 합니다. GLAD 헤더에는 내부적으로 필요한 OpenGL 헤더들이 포함되어 있기 때문입니다.

## main 함수 작성

다음으로 `main` 함수를 만들고 GLFW를 초기화합니다.

```cpp
int main()
{
    // GLFW 초기화
    glfwInit();
    
    // OpenGL 버전 및 프로필 설정
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    
    // macOS 사용자는 아래 줄 추가
    // glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
    
    return 0;
}
```

**코드 설명:**
- `glfwInit()`: GLFW 라이브러리 초기화
- `glfwWindowHint()`: 창 생성 전 설정 지정
  - `GLFW_CONTEXT_VERSION_MAJOR/MINOR`: OpenGL 버전 설정 (3.3)
  - `GLFW_OPENGL_PROFILE`: 코어 프로필 사용 지정

> **💡 OpenGL 버전 선택**
> OpenGL 3.3 이상이 설치되어 있는지 확인하세요. 지원하지 않는 버전을 요청하면 애플리케이션이 작동하지 않습니다.

---

## 창(Window) 객체 생성

이제 실제 창을 생성합니다.

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

**함수 설명:**
- `glfwCreateWindow(width, height, title, monitor, share)`: 창 생성
  - width, height: 창의 크기 (픽셀)
  - title: 창의 제목
  - monitor, share: NULL로 설정 (기본값)
- `glfwMakeContextCurrent()`: 생성한 창을 현재 OpenGL 컨텍스트로 설정

---

## GLAD 초기화

GLAD는 OpenGL 함수 포인터를 관리하므로, OpenGL 함수 호출 전에 반드시 초기화해야 합니다.

```cpp
if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
{
    std::cout << "Failed to initialize GLAD" << std::endl;
    return -1;
}
```

`glfwGetProcAddress`를 통해 OS에 맞는 OpenGL 함수 주소를 로드합니다.

---

## 뷰포트(Viewport) 설정

렌더링을 시작하기 전에 OpenGL에 렌더링 영역의 크기를 알려줘야 합니다.

```cpp
glViewport(0, 0, 800, 600);
```

**매개변수:**
- 처음 두 개: 좌측 하단 모서리 좌표 (0, 0)
- 나중 두 개: 렌더링 영역의 너비와 높이

> **💡 동적 뷰포트**
> 사용자가 창 크기를 조정할 때 자동으로 뷰포트도 변경되도록 콜백 함수를 등록할 수 있습니다.

---

## 윈도우 리사이징 콜백 함수

창 크기가 변경될 때 뷰포트도 함께 조정하려면 콜백 함수를 등록하세요.

```cpp
void framebuffer_size_callback(GLFWwindow* window, int width, int height)
{
    glViewport(0, 0, width, height);
}

// main 함수 내에서 콜백 등록
glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);
```

이제 창의 크기가 변경될 때마다 자동으로 뷰포트가 업데이트됩니다.

---

## 렌더 루프(Render Loop)

애플리케이션이 계속 실행되도록 렌더 루프를 만듭니다.

```cpp
while (!glfwWindowShouldClose(window))
{
    glfwSwapBuffers(window);
    glfwPollEvents();
}
```

**함수 설명:**
- `glfwWindowShouldClose()`: 창 종료 신호 확인
- `glfwSwapBuffers()`: 버퍼 교체 (더블 버퍼링)
- `glfwPollEvents()`: 입력/이벤트 처리

> **🎨 더블 버퍼링 (Double Buffering)**
> 단일 버퍼로 렌더링하면 화면이 깜빡이는 현상이 발생합니다. 전면 버퍼(화면 표시)와 후면 버퍼(렌더링)를 나누어 사용하여 이를 해결합니다.

---

## 렌더링 테스트

렌더링이 제대로 작동하는지 테스트하기 위해 화면을 지워봅시다.

```cpp
while (!glfwWindowShouldClose(window))
{
    // 화면을 청회색으로 지우기
    glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);
    
    glfwSwapBuffers(window);
    glfwPollEvents();
}
```

**함수 설명:**
- `glClearColor(r, g, b, a)`: 화면을 지울 색상 지정 (RGBA, 0.0~1.0)
- `glClear()`: 지정된 버퍼 초기화

---

## 자원 정리

렌더 루프를 벗어나면 모든 GLFW 자원을 해제해야 합니다.

```cpp
glfwTerminate();
return 0;
```

---

## 사용자 입력 처리

ESC 키를 눌러 창을 닫도록 구현해봅시다.

```cpp
void processInput(GLFWwindow *window)
{
    if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true);
}

// 렌더 루프에서 호출
while (!glfwWindowShouldClose(window))
{
    processInput(window);
    
    glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);
    
    glfwSwapBuffers(window);
    glfwPollEvents();
}
```

---

## 완전한 예제 코드

```cpp
#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>

void framebuffer_size_callback(GLFWwindow* window, int width, int height)
{
    glViewport(0, 0, width, height);
}

void processInput(GLFWwindow *window)
{
    if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true);
}

int main()
{
    // GLFW 초기화
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    // 창 생성
    GLFWwindow* window = glfwCreateWindow(800, 600, "LearnOpenGL", NULL, NULL);
    if (window == NULL)
    {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    
    // 콜백 함수 등록
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

    // GLAD 초기화
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
    {
        std::cout << "Failed to initialize GLAD" << std::endl;
        return -1;
    }

    // 뷰포트 설정
    glViewport(0, 0, 800, 600);

    // 렌더 루프
    while (!glfwWindowShouldClose(window))
    {
        processInput(window);

        glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glfwTerminate();
    return 0;
}
```

이제 컴파일하고 실행하면 청회색 창이 나타날 것입니다! ESC 키를 눌러 닫을 수 있습니다.

다음 장에서는 본격적으로 그래픽을 그리기 위한 셰이더(Shader)를 학습합니다.
