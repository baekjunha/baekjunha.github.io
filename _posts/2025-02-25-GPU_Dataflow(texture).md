---
categories: [graphics]
tags: [graphics, opengl, shader, texture, gpu]
math: true
image:
  path: https://learnopengl.com/img/thumbnails/textures.png
---

> **요약**: C++ 애플리케이션의 메모리에 올라와 있는 버텍스 데이터가 어떻게 GPU의 VRAM으로 전송되고, 셰이더 파이프라인(Vertex -> Rasterization -> Fragment)을 거쳐 최종 텍스처 픽셀 색상으로 스크린에 렌더링되는지 그 일련의 데이터 흐름(Dataflow)을 단계별로 요약한다.
{: .prompt-info }

## 목차
* TOC
{:toc}

---

## 1. 버텍스 데이터 정의 (CPU 영역)

모든 그래픽 렌더링의 시작점은 C++ 코드 내에서 선언된 정점 배열 데이터다. 이 원시 데이터는 메인보드의 시스템 RAM에 상주한다.

```cpp
float vertices[] = {
    // 위치(xyz)           // 색상(rgb)           // 텍스처 좌표(st)
     0.5f,  0.5f, 0.0f,   1.0f, 0.0f, 0.0f,   1.0f, 1.0f, // 우상단
     0.5f, -0.5f, 0.0f,   0.0f, 1.0f, 0.0f,   1.0f, 0.0f, // 우하단
    -0.5f, -0.5f, 0.0f,   0.0f, 0.0f, 1.0f,   0.0f, 0.0f, // 좌하단
    -0.5f,  0.5f, 0.0f,   1.0f, 1.0f, 0.0f,   0.0f, 1.0f  // 좌상단 
};
```
{: file="main.cpp" }

이 배열은 정점 1개당 총 8개의 실수(float) 속성값을 묶어 갖는 하이브리드 구조다.
1.  **위치 (`vec3`)**: 3D 공간상의 x, y, z 좌표.
2.  **색상 (`vec3`)**: 해당 정점의 고유 r, g, b 컬러 인자.
3.  **텍스처 좌표 (`vec2`)**: 이미지를 매핑할 s, t 좌표 (0~1 정규화 범위).

---

## 2. 버텍스 데이터 → GPU 전송 (VBO/VAO)

단순히 CPU 메모리에 있는 값을 곧바로 눈으로 볼 수는 없다. 이 막대한 기하학적 데이터를 GPU 내부의 초고속 VRAM으로 덤프(전송)해야 한다.

*   **VBO (Vertex Buffer Object):** 정점 배열 데이터를 통째로 복사해 보관하는 GPU 내부의 거대한 메모리 화물칸이다.
*   **VAO (Vertex Array Object):** 이 VBO 화물칸에 실린 1차원 데이터 더미를, "몇 개씩 잘라서 어떤 셰이더 슬롯에 꽂아 넣을지" 그 배선 설정 매뉴얼(상태 정보)을 녹화해두는 기억 장치다. 

전송된 데이터를 셰이더가 해석할 수 있도록 **버텍스 속성(Vertex Attribute)** 의 맵핑 규격을 정의하고 직렬화한다.

```cpp
// 0번 슬롯: 위치 데이터 (stride 8, offset 0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);

// 1번 슬롯: 색상 데이터 (stride 8, offset 3)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(3 * sizeof(float)));
glEnableVertexAttribArray(1);

// 2번 슬롯: 텍스처 좌표 (stride 8, offset 6)
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(6 * sizeof(float)));
glEnableVertexAttribArray(2);
```
{: file="main.cpp" }

이 직렬화 코드를 통해 향후 셰이더 코드 내의 슬롯 번호(`location = 0, 1, 2`)와 물리적 데이터 덩어리가 정확히 일대일로 체결된다.

---

## 3. 버텍스 셰이더 동작 (파이프라인 1단계)

버텍스 셰이더는 GPU 파이프라인의 수문장이다. 하드웨어로 흘러 들어온 정점 데이터의 공간을 재배치하고, 다음 단계로 토스할 추가 속성값들을 우회 패스(Pass-through) 시킨다.

```glsl
#version 330 core
// C++의 glVertexAttribPointer와 체결되는 입력(In) 슬롯
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
layout (location = 2) in vec2 aTexCoord;

// 프래그먼트 셰이더로 던져버릴 출력(Out) 변수
out vec3 ourColor;
out vec2 TexCoord;

void main()
{
    // 위치 데이터를 4차원 동차 좌표로 포맷팅하여 시스템 내장 변수에 대입
    gl_Position = vec4(aPos, 1.0); 
    ourColor = aColor; // 색상 패스
    TexCoord = aTexCoord; // 텍스처 좌표 패스
}
```
{: file="shader.vert" }

> [!note] 
> 셰이더 입력 변수는 `aPos`, `aColor`, `aTexCoord` 3개였으나, 하위 단계인 프래그먼트 셰이더로 토스되는 변수는 `ourColor`, `TexCoord` 단 2개뿐이다. 가장 중요한 좌표인 `gl_Position`은 파이프라인의 코어 래스터라이저 단계에서 화면 매핑 용도로 바로 쓰여버리기 때문에, 프래그먼트 셰이더 개발자의 접근 권한 밖으로 사라진다.

---

## 4. 래스터라이제이션 (Rasterization) 과정

버텍스 셰이더가 점 세계(3D 공간) 좌표를 픽셀 세계(2D 스크린 공간)로 욱여넣고 뼈대 프레임을 치면, 파이프라인 중간에 위치한 하드웨어 유닛인 래스터라이저가 **프레임 뼈대 내부의 빈 공간을 촘촘한 픽셀 단위 조각(Fragment)들로 잘라 채색 준비를 한다.**

이 과정에서 가장 무서운 마법인 **선형 보간(Linear Interpolation)** 이 터진다. 
왼쪽 정점의 빨간색 텍스처 파라미터와 오른쪽 정점의 파란색 텍스처 파라미터 값이 래스터라이저를 통과하면, 삼각형 내부를 채우는 수백 개의 프래그먼트마다 물리적인 거리에 비례하여 부드럽게 섞인 중간 좌표/색상값(그라데이션)을 하나씩 부여받아 독립적인 객체로 탄생한다.

---

## 5. 프래그먼트 셰이더 동작 (파이프라인 끝단)

독립된 각자의 컬러/텍스처 좌표값과 함께 도마 위에 올라온 수백만 개의 픽셀(프래그먼트) 파편들은, 최후의 채색 공정인 프래그먼트 셰이더에서 색상 심사 판정을 받는다. 

```glsl
#version 330 core
out vec4 FragColor; // 최종 모니터에 영사될 픽셀 색상

// 래스터라이저가 보간을 마쳐 던져준 속성들
in vec3 ourColor;
in vec2 TexCoord;

// GPU 메모리에 묶여(Bind)있는 0번 텍스처 이미지를 찌를 샘플러 바늘
uniform sampler2D texture1;

void main()
{
    // 텍스처 이미지(texture1)에서 TexCoord xy 지점의 RGBA 픽셀 도트 색을 추출(Sampling)한다.
    FragColor = texture(texture1, TexCoord);
}
```
{: file="shader.frag" }

`TexCoord`는 정점 끝에서 전달된 투박한 `0.0` 이나 `1.0` 이 아니다. 래스터라이저가 수백 단계로 쪼개 놓은 `0.45`, `0.88` 과 같은 극비율 보간 좌표이며, `texture` 내장 함수는 이 정밀한 좌표에 대응하는 질감 이미지 텍셀(Texel)의 원본 색상을 날카롭게 찍어내어 화면 픽셀의 `FragColor` 로 도색한다.

---

## 6. 전체 Dataflow 총정리

1.  **Cpu 영역 빌드**: C++ 램에 위치, 색상, 매핑 좌표 배열(`vertices[]`)을 박아 넣는다.
2.  **GPU 밀어넣기 (VBO/VAO)**: PCIe 고속 버스를 태워 데이터를 GPU VRAM 화물칸(VBO)에 적재하고 배선 슬롯 상태(VAO)를 녹화한다.
3.  **버텍스 셰이더 (도형 비틀기)**: 들어온 각 꼭짓점마다 공간 변환 행렬 연산을 수행해 2D 스크린 클립 좌표계(`gl_Position`)로 투영시키고 픽셀 속성 전파를 지시한다.
4.  **래스터라이제이션 (도화지 쪼개기)**: 점들의 프레임을 면적 단위의 프래그먼트 픽셀 조각으로 분쇄하고 텍스처 좌표(UV)를 삼각형 거리에 비례하여 선형 보간(Interpolation) 믹스한다. 
5.  **프래그먼트 셰이더 (도색 마감)**: 보간되어 건네받은 좌표를 들고 GPU 텍스처 메모리 공간을 바늘(`Sampler2D`)로 찔러 질감을 추출해 `FragColor` 를 최종 도색 처리한다.
6.  **Framebuffer 디스플레이**: 마감된 픽셀 컬러 배열이 Swap Buffer 과정을 거쳐 네 눈앞의 LCD 모니터 픽셀 소자로 송출된다.
