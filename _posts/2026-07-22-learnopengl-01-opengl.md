---
title: "[LearnOpenGL] 01. OpenGL"
date: 2026-07-22 18:02:36 +0900
categories: [Graphics, LearnOpenGL]
tags: [opengl, cpp, graphics, translation]
---

> 📢 **안내 및 출처 표기 (Attribution)**
> 
> * 본 포스팅은 Joey de Vries가 작성한 튜토리얼 **[LearnOpenGL.com](https://learnopengl.com/)**의 원문을 바탕으로 한 한국어 번역 및 학습 정리 기록입니다.
> * 원문 저작권은 **Joey de Vries**에게 있으며, **CC BY-NC 4.0** 라이선스를 준수합니다.

---

# OpenGL

여정을 시작하기 전에 먼저 OpenGL이 실제로 무엇인지 정의해야 합니다. OpenGL은 흔히 그래픽과 이미지를 조작하는 데 사용할 수 있는 거대한 함수 집합으로 설명되곤 합니다. 하지만 OpenGL은 라이브러리도 아니고 API도 아닙니다. OpenGL은 명세(specification)이며, 이 명세는 각 함수가 수행해야 할 작업과 출력을 정의합니다.

![OpenGL Logo](https://khronos.org/assets/images/api_logos/opengl.svg)

OpenGL 명세는 각 함수의 결과/출력이 무엇이어야 하고 어떻게 동작해야 하는지 정확히 규정합니다. 그리고 이 함수가 어떻게 동작할지에 대한 솔루션을 찾는 것은 라이브러리 개발자의 몫입니다.

실제 OpenGL 라이브러리를 개발하는 사람들은 주로 그래픽 카드 제조업체입니다. 여러분이 구매하는 각 그래픽 카드는 해당 카드(시리즈)를 위해 특별히 작성된 OpenGL 명세의 구현을 담당합니다. 그래픽 카드 제조업체들은 이 명세를 구현하는 드라이버를 제공하고 있습니다. 많은 OpenGL 명세가 상당히 방대하기 때문에, 대부분의 드라이버는 명세의 특정 버전을 구현하고 있습니다.

대부분의 구현이 그래픽 카드 제조업체에 의해 제작되기 때문에, 구현에 버그가 발생하면 일반적으로 비디오 카드 드라이버를 업데이트하여 해결합니다.

Khronos는 모든 OpenGL 버전에 대한 명세 문서를 공공에 공개하고 있습니다. 관심 있는 독자는 본 튜토리얼에서 사용할 OpenGL 버전 3.3의 명세를 [여기](https://www.khronos.org/registry/OpenGL/specs/gl/glspec33.core.pdf)에서 찾을 수 있습니다.

---

## 코어 프로필 vs 즉시 실행 모드 (Core-profile vs Immediate mode)

과거에 OpenGL을 사용한다는 것은 그래픽을 그리기 쉬운 방식인 **즉시 실행 모드(Immediate mode, 고정 기능 파이프라인이라고도 함)**로 개발함을 의미했습니다. 즉시 실행 모드는 OpenGL의 대부분의 기능이 라이브러리 내부에 숨겨져 있었고, 개발자들은 OpenGL의 동작 방식을 많이 알 필요 없이 기능을 사용할 수 있었습니다. 개발자는 `glBegin()`과 `glEnd()` 사이에 정점들을 보내면 되었고, 나머지는 라이브러리가 처리했습니다. 이 방식은 사용하기는 쉬웠지만 유연성이 부족했습니다.

OpenGL의 코어 프로필을 사용할 때, OpenGL은 우리에게 현대적인 방식을 사용하도록 강제합니다. OpenGL의 폐기된 함수 중 하나를 사용하려고 하면 OpenGL은 에러를 발생시키고 렌더링을 중지합니다. 현대적인 방식의 장점은 더 나은 유연성과 효율성을 제공하지만, 학습 곡선이 더 높다는 것입니다.

이 책이 코어 프로필 OpenGL 버전 3.3을 대상으로 하는 이유도 바로 여기에 있습니다. 비록 더 어렵지만 충분한 가치가 있습니다.

현재는 더 높은 버전의 OpenGL(작성 시점 기준 4.6)을 선택할 수 있는데, 그렇다면 "OpenGL 4.6이 나왔는데 왜 OpenGL 3.3을 배워야 하는가?"라는 의문이 들 수 있습니다.

가장 최신 버전의 OpenGL 기능을 사용할 경우, 가장 최신의 그래픽 카드에서만 애플리케이션을 실행할 수 있습니다. 이것이 대부분의 개발자가 일반적으로 수 년이 지난 버전을 대상으로 개발하는 이유입니다. 이 튜토리얼에서는 OpenGL 버전 3.3을 사용하는데, 이는 2010년대 초반의 거의 모든 그래픽 카드에서 지원되며, 동시에 최신 그래픽 카드에서도 지원됩니다.

일부 장에서는 더 현대적인 기능들이 등장하며, 이는 해당 부분에 별도로 명시되어 있습니다.

---

## 확장 (Extensions)

OpenGL의 훌륭한 특징 중 하나는 **확장(Extensions)** 지원입니다. 그래픽 회사에서 렌더링을 위한 새로운 기술이나 대규모 최적화 기법을 고안해 내면, 이를 확장으로 구현할 수 있습니다. 개발자는 이러한 확장이 지원되는 경우에만 사용할 수 있습니다.

개발자는 이러한 확장을 사용하기 전에 사용할 수 있는지 여부를 질의해야 합니다(또는 OpenGL 확장 라이브러리 사용):

```cpp
if (GL_ARB_extension_name)
{ 
    // 하드웨어에서 지원하는 멋지고 현대적인 새로운 기능 수행
} 
else 
{ 
    // 확장이 지원되지 않음: 기존 방식으로 수행
}

```

OpenGL 버전 3.3에서는 대부분의 기술에 확장이 거의 필요하지 않지만, 필요한 경우 적절한 안내가 제공됩니다.

---

## 상태 머신 (State machine)

OpenGL 그 자체는 커다란 상태 머신(State machine)입니다. 즉, OpenGL이 현재 어떻게 작동해야 하는지를 정의하는 변수들의 집합입니다. OpenGL의 상태는 흔히 OpenGL 컨텍스트(Context)라고 부릅니다.

예를 들어 OpenGL에 삼각형 대신 선을 그리고 싶다고 전달할 때, OpenGL이 그리는 방식을 설정하는 컨텍스트 변수를 변경하여 OpenGL의 상태를 바꿉니다. OpenGL이 그리는 방식이 변경되고, 다음 그리기 명령은 선을 그립니다.

OpenGL 작업을 할 때 컨텍스트를 변경하는 여러 상태 변경 함수(State-changing functions)와 현재 OpenGL 상태를 기반으로 연산을 수행하는 여러 상태 사용 함수(State-using functions)를 사용하게 됩니다. 현재 OpenGL 상태에 대해 질의할 때마다 OpenGL은 현재의 상태를 기반으로 연산을 수행합니다.

---

## 객체 (Objects)

OpenGL 라이브러리는 C 언어로 작성되었으며 다른 언어로의 많은 파생을 허용하지만, 그 핵심은 C 라이브러리로 남아 있습니다. C의 많은 언어 구조가 다른 고급 언어들로 쉽게 번역되지 않으므로, OpenGL은 상태를 유지하고 조작하기 위해 몇 가지 C 기반의 트릭을 개발했습니다. 그 중 하나가 객체입니다.

OpenGL에서의 객체는 OpenGL 상태의 일부분을 나타내는 옵션들의 집합입니다. 예를 들어, 그리기 창의 설정을 나타내는 객체가 있을 수 있습니다. 우리는 이것을 다음과 같은 구조체로 생각할 수 있습니다:

```cpp
struct object_name {
    float option1;
    int option2;
    char name[128];
};

```

객체를 사용하고자 할 때의 일반적인 워크플로는 다음과 같습니다(OpenGL의 컨텍스트를 거대한 구조체로 시각화함):

```cpp
// OpenGL의 상태 (Context)
struct OpenGL_Context {
    ...
    object_name* object_Window_Target;
    ...    
};

// 객체 생성
unsigned int objectId = 0;
glGenObject(1, &objectId);

// 객체를 컨텍스트에 바인딩/할당
glBindObject(GL_WINDOW_TARGET, objectId);

// 현재 GL_WINDOW_TARGET에 바인딩된 객체의 옵션 설정
glSetObjectOption(GL_WINDOW_TARGET, GL_OPTION_WINDOW_WIDTH, 800);
glSetObjectOption(GL_WINDOW_TARGET, GL_OPTION_WINDOW_HEIGHT, 600);

// 컨텍스트 타겟을 다시 기본값으로 되돌림
glBindObject(GL_WINDOW_TARGET, 0);

```

이 짧은 코드 조각은 OpenGL을 다룰 때 자주 보게 될 워크플로입니다. 먼저 객체를 생성하고 이에 대한 참조를 ID로 저장합니다(실제 객체 데이터는 비하인드에서 관리됩니다). 그 다음 객체를 특정 타겟에 바인딩합니다(이 예제에서는 GL_WINDOW_TARGET). 객체가 바인딩된 이후에는 설정(Setting) 함수를 호출하는 것으로 설정을 변경할 수 있고, 이는 현재 바인딩된 객체에만 영향을 미칩니다.

지금까지 제공된 코드 예제는 OpenGL이 작동하는 방식에 대한 근사치일 뿐이며, 본 튜토리얼 전반에 걸쳐 충분한 실제 예제를 접하게 될 것입니다.

이러한 객체를 사용하는 것의 큰 장점은 애플리케이션에서 하나 이상의 객체를 정의하고, 해당 옵션을 설정한 다음, OpenGL 상태를 사용하는 연산을 시작할 때마다 다시 바인딩하는 방식으로 여러 OpenGL 상태를 정의할 수 있다는 것입니다.

---

## 이제 시작해 봅시다 (Let's get started)

이제 명세이자 라이브러리로서의 OpenGL, OpenGL이 내부적으로 대략 어떻게 작동하는지, 그리고 OpenGL이 사용하는 몇 가지 고유한 트릭에 대해 알아보았습니다. 앞으로의 튜토리얼에서 이러한 개념들을 계속 접하게 될 것이며, 각 개념들이 실제로 어떻게 사용되는지 볼 수 있을 것입니다.

다음 튜토리얼에서 우리는 OpenGL 개발 환경을 설정하고 첫 번째 OpenGL 프로그램을 작성해 보겠습니다.

---

## 추가 참고 자료 (Additional resources)

* [opengl.org](https://www.opengl.org/) : OpenGL 공식 웹사이트.
* [OpenGL registry](https://www.khronos.org/registry/OpenGL/index_gl.php) : 모든 OpenGL 버전에 대한 OpenGL 명세 및 확장을 제공하는 레지스트리.
