---
title: "[LearnOpenGL] 01. OpenGL"
date: 2026-07-22 18:02:36 +0900
categories: [Graphics, LearnOpenGL]
tags: [opengl, cpp, graphics, translation]
---

> 📢 **안내 및 출처 표기 (Attribution)**
> * 본 포스팅은 Joey de Vries가 작성한 튜토리얼 **[LearnOpenGL.com](https://learnopengl.com/)**의 원문을 바탕으로 한 한국어 번역 및 학습 정리 기록입니다.
> * 원문 저작권은 **Joey de Vries**에게 있으며, **CC BY-NC 4.0** 라이선스를 준수합니다.

---

# OpenGL

3D 그래픽스 여정을 시작하기 전, **"OpenGL이 도대체 하드웨어인가, 소프트웨어인가, 아니면 라이브러리인가?"**라는 질문부터 시작해 보겠습니다.


![OpenGL Logo](https://khronos.org/assets/images/api_logos/opengl.svg)

> ### 📜 [깊이 읽기] Khronos 그룹의 표준 계약서와 하드웨어 드라이버
> 
> OpenGL은 그 자체로 실행 파일이나 완성된 C++ 코드 라이브러리가 아닙니다. **Khronos Group**이라는 비영리 표준화 단체가 작성한 거대한 **API 명세서(Specification; 규칙 및 계약서)**입니다.
> 
> 이 명세서에는 *"어떤 이름의 함수를 호출하면, 하드웨어는 무슨 결과값을 만들어내야 한다"*는 연산 규약만 엄격히 적혀 있습니다.
> 
> 이 계약서를 보고 C/C++로 실제 동작하는 바이너리 코드(GPU 드라이버)를 만들어내는 주체는 **NVIDIA, AMD, Intel 같은 그래픽 카드 제조업체**입니다. 그래픽 카드마다 내부에 들어있는 실리콘 칩셋과 아키텍처가 완전히 다르기 때문에, 각 제조사가 자사 GPU에 가장 최적화된 형태로 OpenGL 명세를 구현(Implementation)합니다.
> 
> 개발자가 작성한 동일한 OpenGL 코드가 NVIDIA 지포스, AMD 라데온, Intel 내장 그래픽 카드에서 모두 똑같이 동작할 수 있는 이유가 바로 이 **표준 명세(Specification)와 하드웨어 드라이버 구현(Driver Implementation)의 분리** 덕분입니다.

---

## ⚡ 코어 프로필 vs 즉시 실행 모드 (Core-profile vs Immediate mode)

과거 OpenGL 1.x~2.x 시절에는 **즉시 실행 모드(Immediate mode, 고정 기능 파이프라인)**라는 매우 직관적인 그리기 방식을 사용했습니다.

```cpp
// (과거 레거시 방식 예시) 명령을 내리는 즉시 화면에 그림
glBegin(GL_TRIANGLES);
    glVertex3f(-0.5f, -0.5f, 0.0f);
    glVertex3f( 0.5f, -0.5f, 0.0f);
    glVertex3f( 0.0f,  0.5f, 0.0f);
glEnd();
```

> ### 🏛️ [깊이 읽기] 왜 패러다임이 코어 프로필로 전환되었는가?
> 
> 과거의 즉시 실행 모드는 코드가 직관적이지만, CPU가 좌표를 `glVertex3f`로 하나하나 칭얼거리듯 GPU로 전송해야 했습니다. 현대 그래픽 카드는 수천 개의 병렬 코어를 탑재하고 있는데, 이처럼 작은 조각 단위로 명령을 내리면 CPU-GPU 사이 통로(PCIe 버스)가 병목에 걸려 GPU가 놀게 됩니다.
> 
> 그래서 OpenGL 3.3부터 이전 레거시 기능들을 폐기하고 **코어 프로필(Core-profile)**을 강제하기 시작했습니다.
> 
> 코어 프로필은 **"먼저 그릴 3D 형태(VBO)와 셰이더 프로그램을 GPU VRAM 메모리에 대량 등록해 두고, 렌더 루프에서는 한 줄의 드로잉 명령만 던진다"**는 파이프라인 방식입니다. 세부 설정은 까다로워졌지만, GPU 성능을 100% 한계까지 끌어올릴 수 있는 현대 모던 그래픽 프로그래밍의 기본 표준입니다.

---

## 🧩 상태 머신 (State machine)과 컨텍스트(Context)

OpenGL을 다룰 때 반드시 이해해야 하는 핵심 설계 패턴은 OpenGL이 거대한 **상태 머신(State machine)**이라는 점입니다.

> ### 🎨 [깊이 읽기] 화가의 팔레트와 캔버스 비유
> 
> 미술 화가가 캔버스에 그림을 그리는 과정을 떠올려 보세요.
> 
> 화가는 캔버스에 선을 긋기 전에 먼저 **1) 붓의 색상을 파란색으로 선택**하고, **2) 붓의 굵기를 5px로 설정**합니다. 그 후 도화지에 붓을 대고 쓱 그으면, 방금 설정한 파란색과 5px 굵기로 칠해집니다.
> 
> OpenGL도 정확히 동일합니다. 현재 OpenGL에 설정되어 있는 모든 변수(붓의 색, 사용할 셰이더, 바인딩된 메모리 등)의 집합을 **컨텍스트(Context)**라고 부릅니다.
> 
> * **상태 설정 함수 (State-changing function)**: `glClearColor(...)`처럼 컨텍스트 내의 설정값을 바꾸는 함수
> * **상태 사용 함수 (State-using function)**: `glClear(...)`나 `glDrawArrays(...)`처럼 현재 설정된 상태값들을 바탕으로 실제로 GPU 연산을 일으키는 함수

---

## 📦 C 언어 객체(Object) 워크플로와 포인터 핸들

OpenGL API는 pure C 언어 기반입니다. 따라서 C++의 클래스(`class`)나 객체 지향 상속 구조가 명시적으로 존재하지 않습니다. 대신 **객체 핸들(ID 정수 값)**과 **바인딩(Binding)** 개념을 통해 GPU 리소스를 제어합니다.

```cpp
// 1. 객체 할당 (ID 반환)
unsigned int objectId = 0;
glGenObject(1, &objectId);

// 2. 현재 상태 머신(Context)의 타겟 슬롯에 객체 바인딩 (선택)
glBindObject(GL_WINDOW_TARGET, objectId);

// 3. 현재 바인딩된 객체 옵션 설정
glSetObjectOption(GL_WINDOW_TARGET, GL_OPTION_WINDOW_WIDTH, 800);

// 4. 타겟 슬롯 바인딩 해제 (0 = 선택 해제)
glBindObject(GL_WINDOW_TARGET, 0);
```

> ### 💡 [깊이 읽기] 왜 직접 포인터를 안 쓰고 ID 정수값(Handle)을 쓸까?
> 
> C++ 애플리케이션의 메모리는 CPU 시스템 RAM에 위치하지만, OpenGL 객체의 실제 데이터(버텍스, 텍스처 등)는 **GPU 그래픽 카드 전용 고속 VRAM 메모리**에 저장됩니다.
> 
> CPU C++ 코드에서 GPU VRAM 메모리 주소 포인터에 직접 접근하는 것은 불가능하기 때문에, OpenGL은 GPU 리소스 번지수를 나타내는 정수 ID(예: `1`, `2`, `3`...)를 전달하고, CPU 코드는 이 ID 핸들을 사용하여 바인딩하고 조작하게 됩니다.

---

## 🚀 이제 시작해 봅시다!

OpenGL이 Khronos 명세를 기반으로 한 상태 머신이며, 하드웨어 VRAM 리소스를 ID 객체 바인딩 워크플로로 다룬다는 사실을 이해했습니다.

이제 환경 설정을 마치고 실전 코드로 창을 띄워보겠습니다!


---

## 추가 참고 자료 (Additional resources)

* [opengl.org](https://www.opengl.org/) : OpenGL 공식 웹사이트.
* [OpenGL registry](https://www.khronos.org/registry/OpenGL/index_gl.php) : 모든 OpenGL 버전에 대한 OpenGL 명세 및 확장을 제공하는 레지스트리.
