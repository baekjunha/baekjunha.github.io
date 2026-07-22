---
title: "[LearnOpenGL] 02. 창 생성하기 (Creating a window)"
date: 2026-07-23 08:46:16 +0900
categories: [Graphics, LearnOpenGL]
tags: [opengl, cpp, graphics, translation, glfw, glad]
---

> 📢 **안내 및 출처 표기 (Attribution)**  
> * 본 포스팅은 Joey de Vries가 작성한 튜토리얼 **[LearnOpenGL.com](https://learnopengl.com/Getting-started/Creating-a-window)**의 원문을 바탕으로 한 한국어 번역 및 학습 정리입니다.  
> * 원문 저작권은 **Joey de Vries**에게 있으며, **CC BY-NC 4.0** 라이선스를 준수합니다. 원문: https://learnopengl.com/Getting-started/Creating-a-window

---

멋진 그래픽을 만들기 전에 가장 먼저 해야 할 일은 OpenGL 컨텍스트(context)와 그림을 그릴 애플리케이션 창(window)을 생성하는 것입니다. 하지만 이러한 작업은 운영체제마다 고유하며, OpenGL은 의도적으로 이러한 작업으로부터 스스로를 추상화하려고 합니다. 즉, 창을 생성하고, 컨텍스트를 정의하며, 사용자 입력을 처리하는 작업을 모두 직접 해결해야 함을 의미합니다.

다행히도 OpenGL을 주요 대상으로 하며 우리가 원하는 기능을 제공하는 라이브러리가 존재합니다. 이러한 라이브러리들은 운영체제별 특수 작업을 대신 처리해 주어, 렌더링에 필요한 창과 OpenGL 컨텍스트를 제공합니다. 대표적인 라이브러리로는 GLUT, SDL, SFML, GLFW 등이 있습니다. LearnOpenGL에서는 **GLFW**를 사용합니다. 다른 라이브러리를 사용하셔도 무방하며, 대부분의 설정 과정은 GLFW와 유사합니다.

---

## GLFW

GLFW는 C언어로 작성된 OpenGL 전용 라이브러리입니다. GLFW는 화면에 그래픽 요소를 렌더링하는 데 필요한 최소한의 필수 기능을 제공합니다. OpenGL 컨텍스트 생성, 창 파라미터 정의, 사용자 입력 처리를 지원하며 이는 본 튜토리얼의 목적에 충분합니다.

이번 장과 다음 장의 목표는 GLFW를 정상적으로 가동하고, OpenGL 컨텍스트를 올바르게 생성하며, 테스트할 수 있는 간단한 창을 띄우는 것입니다. 이번 장에서는 GLFW 라이브러리를 가져오고, 빌드하며, 링크하는 과정을 단계별로 다룹니다. 본문 작성 시점 기준 IDE로는 Microsoft Visual Studio 2019를 사용합니다(최신 버전의 Visual Studio에서도 과정은 동일합니다). Visual Studio가 아닌 다른 IDE(또는 이전 버전)를 사용하더라도 대부분의 과정은 유사합니다.

---

## GLFW 빌드하기 (Building GLFW)

GLFW는 공식 [다운로드 페이지](https://www.glfw.org/download.html)에서 얻을 수 있습니다. GLFW는 Visual Studio 2012부터 2019용으로 사전 컴파일된 바이너리(pre-compiled binaries) 및 헤더 파일을 제공하지만, 프로세스의 완전성을 위해 소스 코드로부터 직접 컴파일해 보겠습니다. 모든 라이브러리가 미리 컴파일된 바이너리를 제공하지는 않으므로 오픈소스 라이브러리를 직접 컴파일하는 과정에 익숙해지는 것이 좋습니다. **Source package**를 다운로드하세요.

> **입문자 참고**  
> 모든 라이브러리는 64비트 바이너리로 빌드할 예정이므로, 사전 컴파일된 바이너리를 사용할 경우에도 64비트 버전을 받으시기 바랍니다.

소스 패키지를 다운로드한 후 압축을 풀고 내부 항목을 확인합니다. 핵심적으로 필요한 항목은 다음과 같습니다:
* 컴파일 결과로 나올 라이브러리 파일
* `include` 폴더

소스 코드로부터 라이브러리를 직접 컴파일하면 사용 중인 CPU 및 OS 환경에 완벽히 최적화된 라이브러리를 얻을 수 있습니다. 이는 사전 컴파일된 바이너리가 항상 제공하지는 못하는 장점입니다. 하지만 오픈소스 코드의 문제는 개발자마다 사용하는 IDE나 빌드 시스템이 달라 제공된 프로젝트/솔루션 파일이 다른 환경과 호환되지 않을 수 있다는 점입니다. 

결국 각자의 환경에서 `.c`/`.cpp` 및 `.h`/`.hpp` 파일로 프로젝트를 직접 구성해야 하는 번거로움이 발생합니다. 이러한 문제를 해결하기 위해 **CMake**라는 도구가 사용됩니다.

---

## CMake

CMake는 미리 정의된 CMake 스크립트를 사용하여 소스 코드 파일 모음으로부터 사용자가 선택한 IDE(예: Visual Studio, Code::Blocks, Eclipse 등)의 프로젝트/솔루션 파일을 생성해 주는 도구입니다. 이를 통해 GLFW의 소스 패키지로부터 Visual Studio 프로젝트 파일을 생성하여 라이브러리를 컴파일할 수 있습니다. 먼저 [CMake 다운로드 페이지](https://cmake.org/download/)에서 CMake를 다운로드하여 설치합니다.

CMake가 설치되면 명령줄(Command Line) 또는 GUI 환경에서 실행할 수 있습니다. 복잡성을 피하기 위해 GUI를 사용합니다. CMake에는 소스 코드 폴더와 바이너리가 생성될 대상(destination) 폴더가 필요합니다. 소스 코드 폴더에는 다운로드한 GLFW 소스 패키지의 루트 폴더를 지정하고, 빌드 폴더에는 새 디렉터리 `build`를 생성한 후 해당 디렉터리를 선택합니다.

![CMake Logo](https://learnopengl.com/img/getting-started/cmake.png)

소스 폴더와 대상 폴더를 설정한 후 **Configure** 버튼을 누르면 CMake가 필요한 설정과 소스 코드를 읽어옵니다. 이어 프로젝트 생성기(Generator)를 선택해야 하는데, Visual Studio 2019를 사용하므로 **Visual Studio 16** 옵션을 선택합니다(Visual Studio 2019는 Visual Studio 16으로 불립니다). 선택 후 CMake는 생성될 라이브러리를 구성하기 위한 빌드 옵션들을 표시합니다. 기본값을 유지하고 **Configure**를 다시 눌러 설정을 저장합니다. 설정이 완료되면 **Generate**를 클릭하여 지정한 `build` 폴더 내에 프로젝트 파일을 생성합니다.

---

## 컴파일 (Compilation)

`build` 폴더 내부를 확인하면 `GLFW.sln` 파일이 생성되어 있습니다. 이 파일을 Visual Studio로 열어줍니다. CMake가 적절한 구성 설정이 포함된 프로젝트 파일을 생성했으므로, 솔루션을 빌드하기만 하면 됩니다. CMake가 64비트 라이브러리로 컴파일되도록 자동 구성해 두었으므로 **Build Solution**을 실행합니다. 컴파일이 완료되면 `build/src/Debug` 경로에 컴파일된 라이브러리 파일인 `glfw3.lib`가 생성됩니다.

라이브러리가 생성되면 IDE가 OpenGL 프로그램에서 해당 라이브러리와 인클루드(include) 파일의 위치를 찾을 수 있도록 설정해야 합니다. 이를 위한 두 가지 일반적인 접근 방식이 있습니다:

1. IDE/컴파일러의 `/lib` 및 `/include` 폴더를 찾아 GLFW의 `include` 폴더 내용을 IDE의 `/include`에 복사하고, `glfw3.lib`를 IDE의 `/lib` 폴더에 추가하는 방식입니다. 동작은 하지만 권장되지 않습니다. 라이브러리와 헤더 파일을 추적하기 어렵고, IDE/컴파일러를 재설치할 경우 이 과정을 반복해야 합니다.
2. 권장하는 방식은 원하는 위치에 서드파티 라이브러리의 모든 헤더 파일과 라이브러리를 보관할 디렉터리 구조를 새로 만들고, IDE/컴파일러에서 해당 위치를 참조하도록 설정하는 것입니다. 예를 들어 `Libs`와 `Include` 폴더가 포함된 단일 폴더를 만들어 OpenGL 프로젝트용 파일들을 보관할 수 있습니다. 이렇게 하면 모든 서드파티 라이브러리가 한 곳에서 관리됩니다. 단, 새 프로젝트를 생성할 때마다 해당 디렉터리 위치를 IDE에 지정해 주어야 합니다.

원하는 위치에 필요한 파일들을 저장한 후 첫 번째 OpenGL GLFW 프로젝트를 생성할 수 있습니다.

---

## 첫 번째 프로젝트 (Our first project)

Visual Studio를 열고 새 프로젝트를 생성합니다. 언어는 C++을 선택하고 **Empty Project(빈 프로젝트)**를 선택합니다(프로젝트 이름을 적절히 지정합니다). 모든 작업은 64비트로 진행되는데 프로젝트 기본값이 32비트(x86)로 되어 있을 수 있으므로, 상단 Debug 옆의 드롭다운을 x86에서 **x64**로 변경합니다.

![x86에서 x64로 변경](https://learnopengl.com/img/getting-started/x64.png)

설정이 완료되면 첫 번째 OpenGL 애플리케이션을 작성할 작업 공간이 준비됩니다.

---

## 링크 (Linking)

프로젝트에서 GLFW를 사용하려면 해당 라이브러리를 프로젝트에 링크해야 합니다. 링커 설정에서 `glfw3.lib`를 사용하도록 지정하면 되지만, 서드파티 라이브러리를 별도 디렉터리에 보관해 두었으므로 프로젝트가 아직 `glfw3.lib`의 위치를 알지 못합니다. 따라서 해당 디렉터리를 프로젝트 설정에 먼저 추가해야 합니다.

Solution Explorer에서 프로젝트 이름을 우클릭하고 **Properties**로 들어간 뒤 **VC++ Directories** 메뉴로 이동합니다.

![Visual Studio VC++ Directories 설정](https://learnopengl.com/img/getting-started/include.png)

여기서 디렉터리를 추가하여 프로젝트가 라이브러리 및 인클루드 파일을 탐색할 위치를 지정할 수 있습니다. 텍스트를 직접 입력하거나 클릭하여 `<Edit..>` 옵션을 선택할 수 있습니다. **Library Directories**와 **Include Directories** 모두에 대해 해당 작업을 수행합니다.

![Visual Studio Include Directories 설정](https://learnopengl.com/img/getting-started/include_directories.png)

원하는 만큼 디렉터리를 추가할 수 있으며, 설정 이후부터 IDE는 해당 경로에서도 라이브러리와 헤더 파일을 검색합니다. GLFW의 `include` 폴더가 포함되면 본문 코드에서 `#include <GLFW/..>` 형태로 GLFW의 헤더 파일을 인클루드할 수 있게 됩니다. 라이브러리 디렉터리도 동일하게 적용됩니다.

필요한 파일들의 경로 설정이 완료되었으므로 **Linker** 탭의 **Input** 메뉴로 이동하여 GLFW를 프로젝트에 최종 링크합니다.

![Visual Studio 링크 설정](https://learnopengl.com/img/getting-started/linker_input.png)

라이브러리를 링크하려면 링커에 라이브러리 이름을 명시해야 합니다. 라이브러리 이름이 `glfw3.lib`이므로 **Additional Dependencies(추가 의존성)** 항목에 해당 이름을 추가합니다. 컴파일 시 GLFW가 함께 링크됩니다. GLFW 외에도 OpenGL 라이브러리 링크 항목을 추가해야 하며, 이는 운영체제마다 차이가 있습니다.

### Windows에서의 OpenGL 라이브러리
Windows 환경에서 OpenGL 라이브러리인 `opengl32.lib`는 Visual Studio 설치 시 기본 설치되는 Microsoft SDK에 포함되어 있습니다. 따라서 링커 설정에 `opengl32.lib`를 추가해 주면 됩니다. 64비트용 OpenGL 라이브러리 이름도 32비트와 동일하게 `opengl32.lib`를 사용합니다.

### Linux에서의 OpenGL 라이브러리
Linux 시스템에서는 링커 설정에 `-lGL`을 추가하여 `libGL.so` 라이브러리에 링크해야 합니다. 해당 라이브러리를 찾을 수 없는 경우 Mesa, NVidia, 또는 AMD dev 패키지를 설치해야 합니다.

링커 설정에 GLFW와 OpenGL 라이브러리를 모두 추가한 후 다음과 같이 GLFW 헤더 파일을 인클루드할 수 있습니다:

```cpp
#include <GLFW/glfw3.h>

```

> **입문자 참고**
> GCC를 사용하는 Linux 사용자의 경우 다음 옵션을 사용하여 프로젝트를 컴파일할 수 있습니다: `-lglfw3 -lGL -lX11 -lpthread -lXrandr -lXi -ldl`. 관련 라이브러리가 올바르게 링크되지 않으면 수많은 `undefined reference` 에러가 발생합니다.

이것으로 GLFW의 설치 및 환경 설정이 완료되었습니다.

---

## GLAD

아직 한 가지 더 처리해야 할 과정이 남아있습니다. OpenGL은 사양/표준(specification)에 불과하기 때문에, 특정 그래픽 카드가 지원하는 드라이버에 해당 표준을 구현하는 것은 드라이버 제조사의 몫입니다. OpenGL 드라이버 버전이 다양하기 때문에, 대부분의 함수 위치는 컴파일 타임에 알 수 없으며 런타임에 조회를 거쳐야 합니다. 따라서 개발자는 필요한 함수의 위치를 찾아내어 나중에 사용할 수 있도록 함수 포인터에 저장해야 합니다. 이러한 위치 검색 과정은 [운영체제에 따라 다릅니다](https://www.khronos.org/opengl/wiki/Load_OpenGL_Functions). Windows에서는 다음과 같은 형태를 띱니다:

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

보시다시피 코드가 복잡하고 선언되지 않은 각 함수마다 이 작업을 수행하는 것은 매우 번거롭습니다. 다행히 이 목적을 위한 라이브러리가 존재하며, **GLAD**가 널리 사용되는 최신 라이브러리 중 하나입니다.

---

## GLAD 설정하기 (Setting up GLAD)

GLAD는 앞서 설명한 번거로운 작업을 관리해 주는 [오픈소스 라이브러리](https://www.google.com/search?q=https://github.com/Dav1de/glad)입니다. GLAD는 일반적인 오픈소스 라이브러리와는 조금 다른 구성 설정을 가지고 있습니다. GLAD는 [웹 서비스](https://glad.dav1d.de/)를 제공하며, 여기서 원하는 OpenGL 버전을 지정하면 해당 버전에 맞는 모든 관련 OpenGL 함수를 정의하고 로드할 수 있는 파일들을 생성해 줍니다.

[GLAD 웹 서비스](https://glad.dav1d.de/)로 이동하여 언어가 C++로 설정되어 있는지 확인하고, API 섹션에서 최소 **3.3** 이상의 OpenGL 버전을 선택합니다(본 튜토리얼에서 사용할 버전이며, 더 높은 버전도 무방합니다). Profile은 **Core**로 설정하고 **Generate a loader** 옵션이 체크되어 있는지 확인합니다. 확장(Extension) 부분은 우선 무시하고 **Generate**를 클릭하여 결과 라이브러리 파일들을 생성합니다.

> **입문자 참고**
> 반드시 링크된 웹 서비스의 **GLAD1** 버전을 사용하세요. GLAD2 버전의 경우 본 튜토리얼 환경에서 컴파일되지 않습니다.

GLAD 웹 서비스는 두 개의 `include` 폴더와 단일 `glad.c` 파일이 포함된 zip 파일을 제공합니다. 두 인클루드 폴더(`glad` 및 `KHR`)를 프로젝트의 `include` 디렉터리에 복사하고(또는 해당 폴더를 가리키도록 설정을 추가), `glad.c` 파일을 프로젝트에 추가합니다.

이전 단계들을 마치면 코드 파일 최상단에 다음 인클루드 지침을 추가할 수 있습니다:

```cpp
#include <glad/glad.h>

```

컴파일 시 에러가 발생하지 않는다면, GLFW와 GLAD를 활용해 OpenGL 컨텍스트를 구성하고 창을 생성하는 [다음 장](https://learnopengl.com/Getting-started/Hello-Window)으로 진행할 준비가 완료된 것입니다. 모든 인클루드 및 라이브러리 디렉터리가 올바른지, 링커 설정의 라이브러리 이름이 해당 라이브러리와 일치하는지 다시 한 번 확인하세요.

---

## 추가 참고 자료

* [GLFW: Window Guide](https://www.glfw.org/docs/latest/window_guide.html): GLFW 창 설정 및 구성에 대한 공식 가이드.
* [Building applications](https://www.glfw.org/docs/latest/build_guide.html): 애플리케이션 컴파일/링크 과정 및 발생 가능한 오류/해결책 목록 제공.
* [GLFW with Code::Blocks](https://www.google.com/search?q=https://wiki.codeblocks.org/index.php/OpenGL_and_GLFW): Code::Blocks IDE에서의 GLFW 빌드 방법.
* [Running CMake](https://cmake.org/runningcmake/): Windows 및 Linux에서의 CMake 실행 요약.
* [Writing a build system under Linux](https://www.lrde.epita.fr/~adl/autotools.html): Wouter Verholst의 Linux 빌드 시스템 작성 오토툴즈 튜토리얼.
* [Polytonic/Glitter](https://github.com/Polytonic/Glitter): 관련 라이브러리가 미리 구성되어 있는 보일러플레이트 프로젝트.
* [A Beginner’s Guide to Setup OpenGL in Linux (Debian)](https://www.google.com/search?q=https://m242.medium.com/a-beginners-guide-to-setup-opengl-in-linux-debian-148152bcbe0e): Ubuntu에서 GLFW 및 GLAD 라이브러리를 설치하고 OpenGL을 설정하는 단계별 가이드.

```
