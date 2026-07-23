---
title: "[LearnOpenGL] 02. 창 생성하기 (Creating a window)"
date: 2026-07-23 08:46:16 +0900
categories: [Graphics, LearnOpenGL]
tags: [opengl, cpp, graphics, translation, glfw, glad]
---

> 📢 **안내 및 출처 표기 (Attribution)**  
> * 본 포스팅은 Joey de Vries가 작성한 튜토리얼 **[LearnOpenGL.com](https://learnopengl.com/Getting-started/Creating-a-window)**의 원문을 바탕으로 한 한국어 번역 및 학습 [...]
> * 원문 저작권은 **Joey de Vries**에게 있으며, **CC BY-NC 4.0** 라이선스를 준수합니다. 원문: https://learnopengl.com/Getting-started/Creating-a-window

---

멋진 그래픽을 만들기 전에 가장 먼저 해야 할 일은 OpenGL 컨텍스트(context)와 그림을 그릴 애플리케이션 창(window)을 생성하는 것입니다. 하지만 이러�...

다행히도 OpenGL을 주요 대상으로 하며 우리가 원하는 기능을 제공하는 라이브러리가 존재합니다. 이러한 라이브러리들은 운영체제별 특수작업을 ��[...]

---

## GLFW

GLFW는 C언어로 작성된 OpenGL 전용 라이브러리입니다. GLFW는 화면에 그래픽 요소를 렌더링하는 데 필요한 최소한의 필수 기능을 제공합니다. OpenGL 컨��[...]

이번 장과 다음 장의 목표는 GLFW를 정상적으로 가동하고, OpenGL 컨텍스트를 올바르게 생성하며, 테스트할 수 있는 간단한 창을 띄우는 것입니다. 이��[...]

---

## GLFW 빌드하기 (Building GLFW)

GLFW는 공식 [다운로드 페이지](https://www.glfw.org/download.html)에서 얻을 수 있습니다. GLFW는 Visual Studio 2012부터 2019용으로 사전 컴파일된 바이너리(pre-compi[...]

> **입문자 참고**  
> 모든 라이브러리는 64비트 바이너리로 빌드할 예정이므로, 사전 컴파일된 바이너리를 사용할 경우에도 64비트 버전을 받으시기 바랍니다.

소스 패키지를 다운로드한 후 압축을 풀고 내부 항목을 확인합니다. 핵심적으로 필요한 항목은 다음과 같습니다:
* 컴파일 결과로 나올 라이브러리 파일
* `include` 폴더

소스 코드로부터 라이브러리를 직접 컴파일하면 사용 중인 CPU 및 OS 환경에 완벽히 최적화된 라이브러리를 얻을 수 있습니다. 이는 사전 컴파일된 ��[...]

결국 각자의 환경에서 `.c`/`.cpp` 및 `.h`/`.hpp` 파일로 프로젝트를 직접 구성해야 하는 번거로움이 발생합니다. 이러한 문제를 해결하기 위해 **CMake**라는 ...

---

## CMake

CMake는 미리 정의된 CMake 스크립트를 사용하여 소스 코드 파일 모음으로부터 사용자가 선택한 IDE(예: Visual Studio, Code::Blocks, Eclipse 등)의 프로젝트/솔��[...]

CMake가 설치되면 명령줄(Command Line) 또는 GUI 환경에서 실행할 수 있습니다. 복잡성을 피하기 위해 GUI를 사용합니다. CMake에는 소스 코드 폴더와 바이��[...]

![CMake Logo](https://learnopengl.com/img/getting-started/cmake.png)

소스 폴더와 대상 폴더를 설정한 후 **Configure** 버튼을 누르면 CMake가 필요한 설정과 소스 코드를 읽어옵니다. 이어 프로젝트 생성기(Generator)를 선택해��...

---

## 컴파일 (Compilation)

`build` 폴더 내부를 확인하면 `GLFW.sln` 파일이 생성되어 있습니다. 이 파일을 Visual Studio로 열어줍니다. CMake가 적절한 구성 설정이 포함된 프로젝트 파일�...

라이브러리가 생성되면 IDE가 OpenGL 프로그램에서 해당 라이브러리와 인클루드(include) 파일의 위치를 찾을 수 있도록 설정해야 합니다. 이를 위한 두 가�...

1. IDE/컴파일러의 `/lib` 및 `/include` 폴더를 찾아 GLFW의 `include` 폴더 내용을 IDE의 `/include`에 복사하고, `glfw3.lib`를 IDE의 `/lib` 폴더에 추가하는 방식입니다.[...]
2. 권장하는 방식은 원하는 위치에 서드파티 라이브러리의 모든 헤더 파일과 라이브러리를 보관할 디렉터리 구조를 새로 만들고, IDE/컴파일러에서 해��...

원하는 위치에 필요한 파일들을 저장한 후 첫 번째 OpenGL GLFW 프로젝트를 생성할 수 있습니다.

---

## 첫 번째 프로젝트 (Our first project)

Visual Studio를 열고 새 프로젝트를 생성합니다. 언어는 C++을 선택하고 **Empty Project(빈 프로젝트)**를 선택합니다(프로젝트 이름을 적절히 지정합니다). 모...

![x86에서 x64로 변경](https://learnopengl.com/img/getting-started/x64.png)

설정이 완료되면 첫 번째 OpenGL 애플리케이션을 작성할 작업 공간이 준비됩니다.

---

## 링크 (Linking)

프로젝트에서 GLFW를 사용하려면 해당 라이브러리를 프로젝트에 링크해야 합니다. 링커 설정에서 `glfw3.lib`를 사용하도록 지정하면 되지만, 서드파티[...]

Solution Explorer에서 프로젝트 이름을 우클릭하고 **Properties**로 들어간 뒤 **VC++ Directories** 메뉴로 이동합니다.

![Visual Studio VC++ Directories 설정](https://learnopengl.com/img/getting-started/include.png)

여기서 디렉터리를 추가하여 프로젝트가 라이브러리 및 인클루드 파일을 탐색할 위치를 지정할 수 있습니다. 텍스트를 직접 입력하거나 클릭하여 `[...]

![Visual Studio Include Directories 설정](https://learnopengl.com/img/getting-started/include_directories.png)

원하는 만큼 디렉터리를 추가할 수 있으며, 설정 이후부터 IDE는 해당 경로에서도 라이브러리와 헤더 파일을 검색합니다. GLFW의 `include` 폴더가 포함�[...]

필요한 파일들의 경로 설정이 완료되었으므로 **Linker** 탭의 **Input** 메뉴로 이동하여 GLFW를 프로젝트에 최종 링크합니다.

![Visual Studio 링크 설정](https://learnopengl.com/img/getting-started/linker_input.png)

라이브러리를 링크하려면 링커에 라이브러리 이름을 명시해야 합니다. 라이브러리 이름이 `glfw3.lib`이므로 **Additional Dependencies(추가 의존성)** 항목��[...]

### Windows에서의 OpenGL 라이브러리

Windows 환경에서 OpenGL 라이브러리인 `opengl32.lib`는 Visual Studio 설치 시 기본 설치되는 Microsoft SDK에 포함되어 있습니다. 따라서 링커 설정에 `opengl32.lib`를 �...

### Linux에서의 OpenGL 라이브러리

Linux 시스템에서는 링커 설정에 `-lGL`을 추가하여 `libGL.so` 라이브러리에 링크해야 합니다. 해당 라이브러리를 찾을 수 없는 경우 Mesa, NVidia, 또는 AMD dev �...

링커 설정에 GLFW와 OpenGL 라이브러리를 모두 추가한 후 다음과 같이 GLFW 헤더 파일을 인클루드할 수 있습니다:

```cpp
#include <GLFW/glfw3.h>

```

> **입문자 참고**
> GCC를 사용하는 Linux 사용자의 경우 다음 옵션을 사용하여 프로젝트를 컴파일할 수 있습니다: `-lglfw3 -lGL -lX11 -lpthread -lXrandr -lXi -ldl`. 관련 라이브러[...]

이것으로 GLFW의 설치 및 환경 설정이 완료되었습니다.

---

## GLAD

아직 한 가지 더 처리해야 할 과정이 남아있습니다. OpenGL은 사양/표준(specification)에 불과하기 때문에, 특정 그래픽 카드가 지원하는 드라이버에 해�[...]

```cpp
// 함수의 프로토타입 정의
// original comment
// Korean: 함수의 프로토타입 정의 (원문: define the function's prototype)
typedef void (*GL_GENBUFFERS) (GLsizei, GLuint*); 

// 함수 위치를 찾아 함수 포인터에 할당
// original comment
// Korean: 함수 위치를 찾아 함수 포인터에 할당 (원문: find the function and assign it to a function pointer)
GL_GENBUFFERS glGenBuffers = (GL_GENBUFFERS)wglGetProcAddress("glGenBuffers"); 

// 이제 일반 함수처럼 호출 가능
// original comment
// Korean: 이제 일반 함수처럼 호출 가능 (원문: function can now be called as normal)
unsigned int buffer;
glGenBuffers(1, &buffer);

```

보시다시피 코드가 복잡하고 선언되지 않은 각 함수마다 이 작업을 수행하는 것은 매우 번거롭습니다. 다행히 이 목적을 위한 라이브러리가 존재��[...]

---

## GLAD 설정하기 (Setting up GLAD)

GLAD는 앞서 설명한 번거로운 작업을 관리해 주는 [오픈소스 라이브러리](https://github.com/Dav1dde/glad)입니다. GLAD는 일반적인 오픈소...

[GLAD 웹 서비스](https://glad.dav1d.de/)로 이동하여 언어가 C++로 설정되어 있는지 확인하고, API 섹션에서 최소 **3.3** 이상의 OpenGL 버전을 선택합니다(본 튜토...

> **입문자 참고**
> 반드시 링크된 웹 서비스의 **GLAD1** 버전을 사용하세요. GLAD2 버전의 경우 본 튜토리얼 환경에서 컴파일되지 않습니다.

GLAD 웹 서비스는 두 개의 `include` 폴더와 단일 `glad.c` 파일이 포함된 zip 파일을 제공합니다. 두 인클루드 폴더(`glad` 및 `KHR`)를 프로젝트의 `include` 디�[...]

이전 단계들을 마치면 코드 파일 최상단에 다음 인클루드 지침을 추가할 수 있습니다:

```cpp
#include <glad/glad.h>

```

컴파일 시 에러가 발생하지 않는다면, GLFW와 GLAD를 활용해 OpenGL 컨텍스트를 구성하고 창을 생성하는 [다음 장](https://learnopengl.com/Getting-started/Hello-Win[...]

---

## 추가 참고 자료

* [GLFW: Window Guide](https://www.glfw.org/docs/latest/window_guide.html): GLFW 창 설정 및 구성에 대한 공식 가이드.
* [Building applications](https://www.glfw.org/docs/latest/build_guide.html): 애플리케이션 컴파일/링크 과정 및 발생 가능한 오류/해결책 목록 제공.
* [GLFW with Code::Blocks](https://wiki.codeblocks.org/index.php/OpenGL_and_GLFW): Code::Blocks IDE에서의 GLFW 빌드 방법.
* [Running CMake](https://cmake.org/runningcmake/): Windows 및 Linux에서의 CMake 실행 요약.
* [Writing a build system under Linux](https://www.lrde.epita.fr/~adl/autotools.html): Wouter Verholst의 Linux 빌드 시스템 작성 오토툴즈 튜토리얼.
* [Polytonic/Glitter](https://github.com/Polytonic/Glitter): 관련 라이브러리가 미리 구성되어 있는 보일러플레이트 프로젝트.
* [A Beginner’s Guide to Setup OpenGL in Linux (Debian)](https://m242.medium.com/a-beginners-guide-to-setup-opengl-in-linux-debian-148152bcbe0e): Ubuntu에서 GL[...]

```
