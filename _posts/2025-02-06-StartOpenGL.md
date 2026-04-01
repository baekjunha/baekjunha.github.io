---
math: true
---

## 요약
> **요약**: OpenGL의 기본 개념(Core Profile, State Machine, Object)을 분석하고, GLFW 및 GLAD 라이브러리를 활용하여 C++ 환경에서 윈도우 생성 및 렌더링 루프를 구성하는 초기화 프로세스를 기술한다.

## 목차
* TOC
{:toc}

---

**자료 출처**: [LearnOpenGL](https://learnopengl.com/)

## 1. OpenGL 개요

OpenGL은 그래픽 데이터를 제어하기 위한 API 명세(Specification)다. Khronos 그룹이 관리하며, 각 하드웨어 제조사(NVIDIA, AMD 등)는 이 명세에 따라 실제 라이브러리를 구현한다. 따라서 제조사에 관계없이 동일한 명세의 함수를 호출하면 일관된 결과를 얻을 수 있다.

그래픽 드라이버에는 해당 하드웨어가 지원하는 OpenGL 라이브러리가 포함되어 있으므로, 드라이버를 최신 상태로 유지하는 것이 중요하다. Khronos 그룹 웹사이트에서 각 버전의 상세 명세 문서를 확인할 수 있다.

## 2. 코어 프로파일(Core Profile) vs 즉각 모드(Immediate Mode)

초기 OpenGL은 **즉각 모드(Immediate Mode, Fixed Function Pipeline)**를 사용하여 구현이 용이했으나, 내부 추상화로 인해 효율성이 낮았다. 이에 OpenGL 3.2 버전부터는 레거시 기능을 제외하고 현대적인 그래픽스 파이프라인을 강제하는 **코어 프로파일(Core Profile)** 모드가 도입되었다.

> [!info]
> **코어 프로파일(Core Profile)**  
> 레거시 함수를 제외하고 최신 그래픽스 파이프라인 방식을 준수하도록 설계된 명표시다. 하위 호환성을 지원하지 않으므로 학습 난이도가 높으나, GPU 제어권을 직접 확보하여 높은 렌더링 성능을 낼 수 있다. (본 포스트는 **OpenGL 3.3 코어 프로파일**을 기준으로 한다.)

## 3. 확장(Extension)

OpenGL은 하드웨어 제조사가 새로운 기술을 드라이버를 통해 제공할 수 있는 확장 기능을 지원한다. 이를 통해 공식 버전 업데이트 전에도 최신 하드웨어 기능을 활용할 수 있다.

## 4. 상태 머신 (State Machine)

OpenGL 아키텍처는 **상태 머신(State Machine)** 구조를 띤다. 파이프라인 동작을 정의하는 환경 변수들의 집합인 **OpenGL 컨텍스트(Context)**를 기반으로 작동한다. 사용자는 상태 옵션을 변경하고 버퍼를 조작한 뒤, 현재 설정된 컨텍스트를 바탕으로 드로우 콜(Draw Call)을 수행한다.

## 5. 객체 (Object)

OpenGL은 C언어 기반이므로 직접적인 객체 지향 구조를 지원하지 않으나, ID 참조 방식을 통한 **객체(Object)** 개념을 도입했다. 객체는 특정 상태의 집합을 캡슐화한 데이터 덩어리다.

일반적인 워크플로우:
1. 객체 생성 및 고유 ID 발급.
2. ID를 컨텍스트의 활성화 슬롯에 **바인딩(Binding)**.
3. 활성화된 객체의 속성 수정.
4. 작업 완료 후 바인딩 **해제(Unbinding)**.

## 6. 프로젝트 준비: 윈도우 생성 (GLFW)

OpenGL 컨텍스트를 생성하고 윈도우를 관리하기 위해 **GLFW** 라이브러리를 사용한다. OpenGL 명세 자체는 OS 종속적인 기능을 배제하므로, 윈도우 생성 및 입력 처리는 외부 라이브러리에 위임하는 것이 효율적이다.

### 빌드 및 설정

GLFW는 CMake를 통해 각 환경에 맞는 빌드 시스템 파일(예: Visual Studio 솔루션)을 생성할 수 있다. 소스 코드를 직접 컴파일하면 해당 아키텍처에 최적화된 정적 라이브러리(`glfw3.lib`)를 확보할 수 있다.

1. **CMake 구성**: 소스 및 빌드 경로 설정 후 Configure/Generate 수행.
2. **라이브러리 컴파일**: 생성된 솔루션 파일을 빌드하여 `.lib` 파일 획득.
3. **링킹 설정**: 프로젝트 속성에서 헤더 경로(Include) 및 라이브러리 경로(Library)를 지정하고 `glfw3.lib`와 `opengl32.lib`를 추가 종속성에 명시.

---

## 7. 함수 포인터 매핑: GLAD 라이브러리 

OpenGL API 함수는 런타임에 그래픽 드라이버에서 메모리에 적재되므로, 컴파일 시점에는 실제 주소를 알 수 없다. 따라서 실행 시점에 OS로부터 함수 주소를 조회하여 매핑해야 한다. 이를 자동화해주는 라이브러리가 **GLAD**다.

### GLAD 설정

1. [GLAD 웹 서비스](https://glad.dav1d.de/)에서 OpenGL 3.3 Core Profile 사양에 맞는 패키지 생성 및 다운로드.
2. `include` 폴더의 헤더를 프로젝트 경로에 추가.
3. `glad.c` 소스 파일을 프로젝트에 포함시켜 컴파일.

```cpp
#include <glad/glad.h>
#include <GLFW/glfw3.h>
```

---

## 8. 초기화 코드 구현 (Hello Window)

### 윈도우 생성 및 컨텍스트 초기화

```cpp
#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>

int main()
{
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(800, 600, "LearnOpenGL", NULL, NULL);
    if (window == NULL) {
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
        return -1;
    }

    glViewport(0, 0, 800, 600);
    return 0;
}
```

### 렌더링 루프 (Render Loop)

애플리케이션이 종료 신호를 받기 전까지 매 프레임을 렌더링하고 사용자 입력을 처리하는 루프를 구성한다.

```cpp
while (!glfwWindowShouldClose(window))
{
    // 입력 처리
    processInput(window);

    // 렌더링 상태 초기화
    glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);

    // 버퍼 스왑 및 이벤트 폴링
    glfwSwapBuffers(window);
    glfwPollEvents();
}
glfwTerminate();
```

> [!info]
> **더블 버퍼링 (Double Buffering)**  
> 렌더링 시 발생하는 티어링(Tearing) 현상을 방지하기 위해 프론트 버퍼와 백 버퍼를 교체(Swap)하며 화면을 출력한다.

### 자원 해제 및 종료

루프 종료 시 `glfwTerminate()`를 호출하여 할당된 자원을 모두 해제한다.
