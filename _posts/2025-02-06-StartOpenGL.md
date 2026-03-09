---
categories: [Graphics]
tags: [graphics, opengl, tutorial, setup]
math: true
image: https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTf6c44cGdSVe9jPWgeQWwXyCdwjADxP6NrLA&s
---

## 요약
> **요약**: OpenGL의 기본 개념(Core Profile, State Machine, Object)을 이해하고, GLFW와 GLAD 라이브러리를 활용하여 C++ 환경에서 빈 윈도우 창을 띄우고 렌더링 루프를 구성하는 기초 초기화 과정을 다룬다.

## 목차
* TOC
{:toc}

---

**자료 출처**: [LearnOpenGL](https://learnopengl.com/)

## 1. OpenGL이란 무엇인가?

OpenGL은 그래픽과 이미지를 조작하는 데 사용할 수 있는 다양한 함수들을 제공하는 API(Application Programming Interface)라고 할 수 있다. API 자체는 아니고, Khronos 그룹이 개발하고 관리하는 사양(specification)이라고 보는 것이 맞다. 마치 레시피처럼, 각 함수가 어떤 결과를 내야 하고 어떻게 동작해야 하는지 정확히 규정하는 것이다.

이 레시피(사양)만으로는 구체적인 실제 구현 방법은 나와있지 않다. 따라서 각 회사(주로 그래픽 카드 제조업체)는 자신들의 방식대로 이 사양을 구현할 수 있다. 하지만, 사용자에게 보이는 결과는 사양에 맞춰야 하기 때문에, 다른 구현 방식을 사용하더라도 사용자에게는 똑같이 보여야 한다. 예를 들어, 똑같은 `삼각형 그리기` 함수를 사용해도, A사 그래픽 카드와 B사 그래픽 카드에서 구현된 OpenGL 라이브러리가 다르더라도 삼각형이 같은 모양으로 그려져야 한다.

그래픽 카드 제조업체는 OpenGL 라이브러리를 만드는데, 만약 버그가 있으면, 그래픽 카드 드라이버 업데이트를 통해 해결할 수 있다. 드라이버에는 카드가 지원하는 최신 버전의 OpenGL이 포함되어 있기 때문이다. 그래서 그래픽 드라이버를 주기적으로 업데이트하는 것이 중요하다. 마치 자동차에 필요한 부품을 교체하듯이 말이다. 드라이버 업데이트는 시스템의 안정성과 성능 향상에 중요한 역할을 한다.

Khronos 그룹 웹사이트에는 모든 OpenGL 버전의 사양 문서가 공개되어 있다. 특히, 우리가 배울 OpenGL 3.3 버전의 사양은 자세한 내용을 파악하는 데 도움이 되는 좋은 참고 자료가 될 것이다. 사양서는 결과와 동작 방식을 설명하는데, 구현 세부 사항은 없다고 생각하면 된다.

## 2. 코어 프로파일(Core Profile) vs 즉각 모드(Immediate Mode)

초창기 OpenGL은 **'즉각 모드(Immediate Mode, Fixed Function Pipeline)'** 표준을 사용하여 그래픽을 그리는 것이 매우 쉬웠다. 대부분의 기능이 라이브러리 내부에 추상화되어 숨겨져 있었고, 개발자는 그래픽 파이프라인 연산 방식에 대해 세세한 통제권을 갖지 못했다.

하지만 즉각 모드는 사용하기 쉽지만 아키텍처 구조상 매우 비효율적이었다. 따라서 OpenGL 3.2 버전부터 즉각 모드 관련 레거시 기능을 완전히 폐기하고, 현대적인 **'코어 프로파일(Core Profile)'** 모드를 사용하도록 사양을 강제하기 시작했다.

> [!info]
> **코어 프로파일(Core Profile)이란?**  
> 과거의 낡은 함수들을 메모리에서 완전히 제거하고 최신 그래픽스 파이프라인 방식을 강요하는 엄격한 사양이다. 구형 함수를 호출하면 즉각적으로 런타임 에러가 발생하며 렌더링이 중단된다.

즉각 모드가 내부 동작을 가려주어 입문하기 쉬웠던 반면, 코어 프로파일은 그래픽스 지식에 대한 높은 이해도를 요구하므로 학습 곡선이 가파르다. 그러나 GPU에 대한 직접적인 제어권을 얻어 훨씬 유연하고 압도적인 렌더링 퍼포먼스를 뽑아낼 수 있다. (본 포스트 시리즈는 **OpenGL 3.3 코어 프로파일** 버전을 기준으로 코드를 전개한다.)

## 더 높은 버전의 OpenGL

요즘은 OpenGL 4.6 같은 더 높은 버전이 나와 있다. 왜 OpenGL 3.3을 배우는 걸까? OpenGL 3.3부터 나온 새로운 버전들은 OpenGL의 기본 원리를 바꾸지 않고 새로운 기능을 추가했기 때문이다. 새로운 기능은 같은 일을 더 효율적이거나 더 나은 방식으로 처리하는 방법일 뿐이다. 따라서 기본 개념과 기술은 최신 OpenGL 버전에서도 동일하다. 나중에 더 높은 버전의 기능을 사용하려면, 그때 배우면 된다.

## 확장(Extension)

OpenGL은 확장(extension)을 지원하는 훌륭한 기능을 가지고 있다. 그래픽 회사가 새로운 기술이나 최적화 기법을 개발하면, 드라이버에 구현된 확장으로 제공될 수 있다. 만약 응용 프로그램이 실행되는 하드웨어가 해당 확장을 지원한다면, 개발자는 확장으로 제공되는 기능을 이용해서 더욱 고급스럽거나 효율적인 그래픽을 만들 수 있다. 즉, OpenGL이 앞으로 버전 업데이트를 기다릴 필요 없이, 현재 지원하는 기능을 활용할 수 있는 것이다. 확장은 필요에 따라 활용하는 것이지, 무조건 써야 하는 필수적인 요소는 아니다.

## 4. 상태 머신 (State Machine)

OpenGL 아키텍처는 근본적으로 거대한 **상태 머신(State Machine)** 의 집합체로 구성되어 있다. OpenGL이 현재 어떤 파이프라인으로 동작해야 하는지 정의하는 수많은 환경 변수들의 모음집이다. 이 거대한 상태 집합을 **OpenGL 컨텍스트(Context)** 라고 부른다. 

우리가 코드를 작성할 때는 1) 상태 옵션을 변경하고, 2) 버퍼를 조작한 뒤, 3) 현재 세팅된 컨텍스트 상태를 기반으로 Draw Call(렌더링 명령)을 수행하는 흐름을 반복한다.

예를 들어 화면에 '삼각형' 대신 '선 뼈대(Wireframe)'만 그리고 싶다면, OpenGL의 폴리곤 모드 상태 변수를 변경하여 컨텍스트를 업데이트한다. 컨텍스트가 한 번 '선 렌더링 모드'로 세팅되면, 그 이후에 호출되는 모든 드로우(Draw) 명령어는 명시적으로 상태를 다시 원복하기 전까지 계속 선만 그리게 된다.

## 5. 객체 (Object)

OpenGL 라이브러리 자체는 C언어로 구현되어 객체 지향적인 언어 구조를 직접 지원하지 않는다. 그래서 C 구조체의 ID 포인터 맵핑 방식을 빌려와 **객체(Object)** 라는 추상화 개념을 도입했다. OpenGL의 객체는 특정 상태 세트의 옵션값들을 하나로 묶어둔 덩어리다.

객체를 조작하는 일반적인 C++ 워크플로우는 다음과 같다.
1. 객체를 생성하고 정수형(Int) 참조 ID를 발급받아 저장한다.
2. 해당 ID를 컨텍스트의 활성화 슬롯에 **바인딩(Binding)** 한다.
3. 활성화된 객체를 향해 세팅 함수를 호출해 옵션을 수정한다.
4. 조작이 끝났으면 다른 객체가 오염되지 않도록 기본값(0)으로 바인딩을 **해제(Unbinding)** 한다.

이러한 상태 기계와 ID 바인딩 패턴 덕분에 수십 개의 파이프라인 버퍼나 설정 데이터들을 각각 독립적인 객체로 묶어두고, 렌더링 루프를 돌 때마다 필요할 때 갈아 끼우며 화면을 그릴 수 있다.

## 6. 프로젝트 준비: 윈도우 생성 (GLFW)

화면에 직접 픽셀 렌더링을 제어하기 전에 가장 먼저 해야 할 일은 OpenGL 컨텍스트를 품을 수 있는 **애플리케이션 윈도우(Window)** 를 생성하는 것이다. 그러나 이 작업은 운영체제(Windows, Linux, macOS 등)의 그래픽 커널 API에 전적으로 의존한다. OpenGL 사양은 의도적으로 이러한 OS 종속적인 기능들로부터 자신을 철저히 격리시켰다. 즉, 프로그래머가 직접 OS API를 호출해 윈도우를 띄우고, 컨텍스트를 바인딩하고, 키보드나 마우스 등 사용자 입력(Input) 이벤트를 수동으로 처리해야 한다.

다행히도 이러한 험난한 초기화 작업을 크로스 플랫폼 스펙으로 깔끔하게 추상화해주는 검증된 라이브러리들이 존재한다. GLUT, SDL, SFML 등 수많은 선택지가 있지만, 본 포스트에서는 오직 OpenGL 렌더링 환경 구축에만 가장 콤팩트하게 특화된 **GLFW** 라이브러리를 채택한다.

### GLFW란?

**GLFW**는 C언어로 작성된 경량 유틸리티 라이브러리다. 화면에 그래픽을 렌더링하는 데 필요한 최소한의 필수 기능만을 날카롭게 제공한다. OS에 구애받지 않고 OpenGL 컨텍스트 생성, 윈도우 매개변수 정의, 조이스틱/키보드/마우스 등 하드웨어 입력 처리를 완벽하게 지원한다. 

이번 챕터에서는 소스 코드를 직접 다운로드하여 내 개발 환경에 맞게 직접 컴파일(빌드)하고, 프로젝트 링커(Linker)에 연결하는 정석적인 과정을 수행한다. (본 문서에서는 Windows 버전을 기준으로, Visual Studio 2019/2022와 같은 IDE 환경을 주로 상정한다.)

### 빌드 시스템: CMake 설정

GLFW 공식 홈페이지에서 제공하는 **사전 컴파일된 바이너리(Pre-compiled Binaries)** 를 바로 다운로드하여 써도 무방하지만, 안정적인 의존성 관리를 위해 **소스 패키지(Source Package)** 를 직접 받아 로컬 환경에서 파싱하는 방식을 권장한다.

> [!tip] 
> 소스 코드를 내 PC 아키텍처 환경에 맞춰 직접 컴파일하면 CPU 환경 지연 없이 가장 최적화된 네이티브 라이브러리(.lib / .a)를 확보할 수 있다.

C/C++ 생태계에서는 각기 다른 OS와 구구절절한 IDE 세팅(Visual Studio, Eclipse, Code::Blocks 등) 간의 호환성 파편화를 잡아주기 위해 **CMake** 라는 크로스 플랫폼 빌드 시스템 생성기 도구를 활용한다.

1. CMake 공식 다운로드 페이지에서 GUI 버전을 다운로드하여 설치한다.
2. CMake GUI를 실행하고, `Where is the source code:` 경로에 방금 압축을 푼 GLFW 소스 루트 폴더를 지정한다.
3. `Where to build the binaries:` 경로에 소스 폴더 하위에 임의로 새로운 폴더(예: `build`)를 생성하여 지정한다.
4. **Configure** 버튼을 누르고 본인의 IDE 버전에 맞는 제너레이터(예: Visual Studio 16 2019 / 17 2022 옵션, `x64` 플랫폼 환경)를 선택한다.
5. 붉은색 옵션 리스트가 뜨면 기본 설정 그대로 둔 채 다시 **Configure**를 누르고 붉은색이 사라지면 **Generate** 버튼을 클릭해 빌드 시스템 솔루션 파일을 최종 생성한다.

### 라이브러리 컴파일 (Compile)

방금 CMake를 통해 생성한 `build` 폴더에 진입하면 `GLFW.sln` 이라는 Visual Studio 전용 솔루션 파일이 생성되어 있다. 이를 실행하여 IDE를 켜준다.

1. CMake가 이미 모든 디펜던시를 잡아 두었으므로, 별도의 설정 없이 IDE 상단 메뉴의 **빌드(Build) -> 솔루션 빌드(Build Solution)** 단축키(F7)를 눌러 컴파일을 찌른다.
2. 컴파일이 성공적으로 터미널에 로깅되면, `build/src/Debug` 폴더 내부에 C++ 오브젝트 덩어리인 `glfw3.lib` 정적 라이브러리 파일이 탄생한다.

### 링킹 구조 세팅 (Linking)

이제 메인 그래픽스 프로젝트를 위한 빈 C++ 프로젝트를 새로 생성한다. 새로운 IDE 환경이 `glfw3.lib` 파일과 GLFW 동작 선언이 담긴 헤더(Header) 파일의 위치를 찾을 수 있도록 링커 환경을 강제로 주입해야 한다.

가장 깔끔한 방법은 별도의 `Dependencies` (또는 `Libs`, `Includes`) 디렉토리를 하나 생성하여 서드파티 모듈을 체계적으로 응집시켜 통합 관리하는 것이다.

1. 솔루션 탐색기에서 프로젝트 이름을 우클릭하여 **속성(Properties)** 창에 들어간다.
2. **VC++ 디렉터리** 탭에서 두 가지 항목을 추가 편집한다:
   * **포함 디렉터리 (Include Directories):** 다운받은 GLFW 소스 패키지 안의 `include` 폴더 경로 추가 (이 안에는 `<GLFW/glfw3.h>` 헤더가 들어있다).
   * **라이브러리 디렉터리 (Library Directories):** 방금 우리가 컴파일해서 얻어낸 `glfw3.lib` 파일이 존재하는 폴더 경로 (자체 구성한 `Libs` 묶음 폴더 등)를 추가.

이렇게 디렉터리 경로 레이더망을 세팅해 두면 `#include <GLFW/...>` 지시문이 즉각적으로 인식된다.

마지막으로 링커 탭을 열어 런타임 단계에서 실제 어떤 `.lib` 파일들을 바인딩할지 기입한다.
* **링커 (Linker) -> 입력 (Input) -> 추가 종속성 (Additional Dependencies)**
* 이곳에 수동으로 `glfw3.lib` 라는 파일명을 타이핑하여 명시한다 (Windows 환경의 경우 `opengl32.lib` 도 시스템 기본 변수로 함께 추가 타이핑해야 한다).

> [!warning]
> **리눅스 (Linux) 환경의 경우**
> 윈도우의 `.lib` 링커 체계 대신, 커맨드 라인 인수에 `-lglfw3 -lGL -lX11 -lpthread -lXrandr -lXi -ldl` 등을 엮어서 `.so` 공유 라이브러리를 바인딩해야 한다. 패키지 매니저를 통해 Mesa, NVidia 드라이버 개발 패키지를 추가로 설치해야 할 수도 있다.

---

## 7. OS별 함수 포인터 우회 장치: GLAD 라이브러리 

앞서 언급했듯, OpenGL은 단지 인터페이스 기능의 "표준 및 사양(Specification)" 껍데기일 뿐이다. 이 사양을 실제 그래픽 카드 드라이버 레벨에서 구현하고 메모리에 적재하는 작업은 코어 내부 런타임 단계에서 이루어진다. 수많은 제조사와 파생 버전이 존재하기 때문에 구체적인 함수 라이브러리의 메모리 주소(Pointer)를 컴파일(Compile) 시점에는 알 턱이 없다. 이 말인즉슨, 모든 OpenGL API 함수들을 호출하기 위해서는 프로그램 실행 도중에 해당 함수들의 주소 값을 운영체제로부터 일일이 조회해서 포인터 변수에 저장하는 끔찍한 절차를 밟아야 한다는 뜻이다.

Windows 환경에서 C++로 직접 원시적인 우회 코드를 작성하면 대략 이런 모양이 된다.

```cpp
// 함수의 프로토타입 원형 선언 정의
typedef void (*GL_GENBUFFERS) (GLsizei, GLuint*);
// OS를 찔러 실행 런타임에 GPU 드라이버 내장 함수 메모리 주소를 찾아 포인터에 맵핑
GL_GENBUFFERS glGenBuffers = (GL_GENBUFFERS)wglGetProcAddress("glGenBuffers");
// 이제야 비로소 정상적으로 함수를 호출할 수 있다
unsigned int buffer;
glGenBuffers(1, &buffer);
```

이 엄청난 노가다 코드를 수백 개의 OpenGL 핵심 함수마다 모조리 타이핑할 수는 없다. 이 번거로운 OS 종속 포인터 조회 작업을 내부적으로 완전히 매니징해주는 특급 라이브러리가 바로 **GLAD** 다.

### GLAD 패키지 셋업

GLAD는 보편적인 C/C++ 정적 라이브러리 다운로드 방식과 궤를 달리한다. 오픈 소스 컨트리뷰션 사이트 형태의 [GLAD 웹 서비스](http://glad.dav1d.de/)를 기반으로 동작한다.

1. 웹 서비스에 접속하여 환경을 산출한다:
   * **Language**: `C/C++`
   * **Specification**: `OpenGL`
   * **API - gl**: `Version 3.3` (또는 그 이상)
   * **Profile**: `Core`
2. 하단의 **GENERATE** 버튼을 클릭하여 커스텀 컨버팅된 압축 파일(Zip)을 다운로드한다.
3. 압축 파일 내부에 존재하는 `include` 폴더(`/glad` 및 `/KHR` 시스템 인터페이스 포함)를 프로젝트의 헤더 디렉터리 경로에 복사해 넣는다.
4. 마지막으로 압축 파일 내부에 들어있는 단 하나의 C 문법 소스 파일인 `glad.c` 파일을 프로젝트 솔루션 폴더 안에 드래그하여 집어넣고, 빌드 대상 파일로 포함시킨다.

이제 모든 세팅이 완료되었다. 다음과 같은 순서로 메인 C++ 엔진 코드 상단에 `#include` 지시문을 선언하면, 어떠한 포인터 오류 없이 네이티브한 C 함수처럼 모든 최신 OpenGL 스펙 API를 마음껏 호출할 수 있게 된다.

```cpp
// 반드시 GLFW나 여타 그래픽 라이브러리보다 GLAD를 가장 최우선으로 상단에 Include 해야 한다. (상태 충돌 방지)
#include <glad/glad.h>
#include <GLFW/glfw3.h>
```

> [!tip] 
> 초기 환경 구성이 헷갈리거나 빌드 과정이 귀찮다면 관련된 보일러플레이트 라이브러리들이 미리 통째로 세팅되어 있는 깃허브 오픈 리포지토리 [Polytonic/Glitter](https://github.com/Polytonic/Glitter)를 Clone하여 곧바로 시작해도 좋다.


## 8. 헬로 윈도우 (Hello Window)

GLFW와 GLAD 라이브러리 세팅이 무사히 끝났는지 검증하기 위해, 바탕화면에 모니터 프로그램 창을 하나 띄우는 예제를 작성해본다. C++ 파일을 하나 생성하고 다음과 같이 헤더를 포함한다.

```cpp
// GLAD가 내부적으로 필요한 OpenGL 헤더(GL/gl.h 등)를 품고 있으므로, 
// GLFW 등 다른 그래픽 라이브러리보다 무조건 먼저 선언해야 충돌이 나지 않는다.
#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>
```
{: file="main.cpp" }

다음으로, C++ 프로그램의 엔트리 포인트인 `main` 함수를 작성하고 GLFW 환경을 초기화한다.

```cpp
int main()
{
    // ① GLFW 라이브러리 초기화
    glfwInit();
    
    // ② GLFW 윈도우 힌트(옵션) 설정
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3); // OpenGL 3.x 버전 사용 명시
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3); // OpenGL x.3 버전 사용 명시 (즉 3.3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE); // 코어 프로파일 사용
    
#ifdef __APPLE__
    // macOS 환경에서는 포워드 호환성 옵션을 켜야 정상 동작할 수 있다.
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
#endif

    // ...
    return 0;
}
```
{: file="main.cpp" }

`glfwWindowHint` 함수를 통해 생성될 윈도우의 속성을 미리 규정할 수 있다. 첫 번째 인자로는 조작할 옵션의 Enum 값을, 두 번째 인자로는 설정할 정수값을 대입한다. 본 예제에서는 OpenGL 3.3 버전을 타겟으로 하고, 하위 호환 기능을 배제한 Core-Profile을 쓰겠다는 의지를 GLFW 시스템에 명시했다.

> [!important]
> 코드를 실행했는데 정의되지 않은 참조(Undefined Reference)나 링커(LNK) 에러가 잔뜩 뜬다면 `glfw3.lib` 라이브러리의 링킹 위치 지정이 잘못된 것이니 속성 페이지를 다시 확인해야 한다.

이제 설정해둔 옵션을 바탕으로 실제 윈도우 인스턴스 객체를 할당받는다.

```cpp
    // 해상도 800x600 짜리 "LearnOpenGL" 이라는 제목의 윈도우 객체 소환
    GLFWwindow* window = glfwCreateWindow(800, 600, "LearnOpenGL", NULL, NULL);
    if (window == NULL)
    {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate(); // 에러 발생 시 모든 할당 자원 반환
        return -1;
    }
    // 소환한 윈도우를 현재 쓰레드의 메인 컨텍스트로 지정 (내가 여기다 그림을 그리겠다)
    glfwMakeContextCurrent(window);
```
{: file="main.cpp" }

### GLAD 포인터 적재

앞서 설명한 바와 같이, 어떠한 OpenGL 함수라도 호출하기 직전에 반드시 OS 그래픽 드라이버의 내부 함수 포인터 주소들을 모조리 맵핑시키는 GLAD 로드 과정을 거쳐야 한다.

```cpp
    // GLFW가 OS를 통해 제공해주는 GetProcAddress 함수 주소를 넘겨주어 GLAD 맵핑 파이프라인 가동
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
    {
        std::cout << "Failed to initialize GLAD" << std::endl;
        return -1;
    }
```
{: file="main.cpp" }

### 뷰포트 (Viewport) 맵핑

OpenGL이 그림을 그릴 도화지 패널의 크기를 알아야 3D 공간상의 데이터 좌표들을 올바르게 모니터 픽셀 좌표계로 치환할 수 있다. 이를 위해 `glViewport` 함수를 호출한다.

```cpp
    // 좌측 하단(0,0)을 기준점으로 가로 800, 세로 600 픽셀만큼 렌더링 구역을 설정
    glViewport(0, 0, 800, 600);
```
{: file="main.cpp" }

> [!info] 
> 뷰포트 크기를 GLFW 윈도우 창 크기보다 작게 설정하면 화면 분할 시뮬레이션(에디터 미니맵 등) 효과를 낼 수 있다.

만약 사용자가 마우스로 윈도우 창의 귀퉁이를 잡고 크기를 잡고 당기면(Resize), 렌더링 구역의 뷰포트 역시 그것에 맞추어 유동적으로 변환(Update)되어야 비율이 찌그러지지 않는다. 이를 위해 GLFW 크기 변경 이벤트에 반응하는 콜백(Callback) 함수를 하나 작성하여 등록한다.

```cpp
// 윈도우 크기 변경 시 GLFW가 자동으로 호출해 줄 콜백 함수 원형
void framebuffer_size_callback(GLFWwindow* window, int width, int height)
{
    glViewport(0, 0, width, height);
}

// ... main 함수 내부 적당한 위치에 콜백 등록 호출 코드 ...
glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);
```
{: file="main.cpp" }

### 엔진 준비 (Render Loop)

위의 세팅만 마치고 프로그램을 실행하면 터미널 창과 검은 모니터 창이 눈 깜짝할 새 일순간 0.1초 떴다가 프로그램 생명주기 종료와 함께 즉시 소멸해버린다. 애플리케이션이 외부의 `종료 신호`를 받기 전까지는 계속해서 반복문을 돌며 프레임을 렌더링하고 사용자 입력 폴링(Polling)을 주시해야 한다. 이 메인 무한 루프를 **렌더링 루프(Render Loop)** 라고 부른다.

```cpp
    // 윈도우 종료 플래그가 True 로 활성화 되기 전까지 무한 루프
    while (!glfwWindowShouldClose(window))
    {
        // ① 입력 이벤트 점검 (키보드 연타 방향키 조작 등 감지 반응)
        glfwPollEvents();    

        // ② 이 위치 즈음에 다가오는 챕터에서 렌더링 명령 함수들을 짜넣게 된다.
        
        // ③ 다 그린 프레임 렌더 타겟을 전면 버퍼와 스왑(Swap)하여 스크린 모니터에 한방에 출력
        glfwSwapBuffers(window);
    }
```
{: file="main.cpp" }

> [!info]
> **더블 버퍼링 (Double Buffering) 메커니즘**  
> 단일 버퍼 하나로만 픽셀 데이터를 한 줄씩 실시간으로 화면에 갱신하면 모니터 주사율 속도 차이로 인해 화면이 찢어지거나 깜빡거리는 티어링(Tearing) 아티팩트가 심하게 생긴다. 이를 방지하기 위해 보이지 않는 백 버퍼(Back Buffer) 캔버스에 모든 복잡한 렌더 명령을 백그라운드에서 끝맞친 뒤, 완전히 완성된 풀 프레임 완성본을 모니터에 노출 중이던 프론트 버퍼(Front Buffer)와 일순간에 맞교환(Swap)하는 방식을 쓴다.

### 프로그램 종료 및 자원 정리 (Cleanup)

루프를 성공적으로 탈출했다는 것은 사용자가 우측 상단의 X 버튼을 눌렀다거나 스크립트 상에서 종료 신호가 발동했다는 뜻이다. 남겨진 모든 내부 메탈(Metal), 힙 메모리 리소스 할당량을 해제한다.

```cpp
    // 루프 탈출 직후
    glfwTerminate(); // 리소스 완전 삭감
    return 0; // 메인 종료
```
{: file="main.cpp" }

### 키보드 입력 감지 (Input Processing)

프로그래머가 특정 키를 눌렀을 때만 조작이 가능하도록 함수를 분리한다. `glfwGetKey` 함수를 호출하여 키 체류 상태가 `GLFW_PRESS` 상태인지, 안 누른 상태인지 실시간으로 파악할 수 있다.

```cpp
// 렌더링 루프 바깥에 분리된 입력 콜백 함수
void processInput(GLFWwindow *window)
{
    // ESC 키가 눌렸는지 감지
    if(glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true); // 프로그램 종료 플래그를 ON!
}
```
{: file="main.cpp" }

키보드의 **ESC 키**를 누르면 창이 닫히도록 논리를 구성했다. 이제 이 함수를 메인 렌더링 루프 가장 윗단에 꽂아 넣어 프레임이 시작될 때마다 감지하도록 만든다.

### 화면 단색 초기화 (Clear Color)

루프가 돌 때마다 이전 프레임에서 그렸던 물감 찌꺼기(버퍼 데이터)들이 모니터 상에 누적되어 시야를 마구잡이로 가린다. 매 프레임의 렌더링 로직을 시작하기 전에 도화지를 깨끗한 단일 지우개 색상으로 쫙 밀어버려야 한다.

```cpp
    // --- 렌더링 루프(while) 내부 영역 --- //
    // 1. 입력 감지
    processInput(window);

    // 2. 도화지를 무슨 색으로 지울건지 세팅 (R, G, B, Alpha)
    glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
    
    // 3. 실제 색상 버퍼 비트 초기화 명령 수행
    glClear(GL_COLOR_BUFFER_BIT);

    // 4. 이벤트 폴링 및 버퍼 스왑
    glfwPollEvents();
    glfwSwapBuffers(window);
```
{: file="main.cpp" }

`glClearColor`는 OpenGL 상태의 도화지 배경색을 정의하는 설정 함수고, 곧바로 이어지는 `glClear` 함수가 세팅된 해당 색상을 실제로 버퍼의 모든 화소에 폭격하여 덮어씌우는 로직 구동 함수다.

코드를 성공적으로 컴파일하고 실행하면, 은은한 다크 틸(Teal) 색상이 감도는 아름다운 빈 더미 윈도우 창이 여러분의 모니터 정중앙에 성공적으로 구동될 것이다. 본격적인 3D 삼각형 그리기 렌더링 기반이 완벽하게 세팅되었다!
