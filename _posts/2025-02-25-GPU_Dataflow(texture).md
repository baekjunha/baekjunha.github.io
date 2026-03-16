---
categories: [graphics]
tags: [graphics, opengl, shader, texture, gpu]
math: true
image:
  path: /assets/img/thumbnails/opengl-textures.png
---

> **요약**: CPU 메모리에 상주하는 정점 데이터가 GPU VRAM으로 전송된 후, 셰이더 파이프라인(Vertex -> Rasterization -> Fragment)을 거쳐 최종 픽셀로 렌더링되는 데이터 흐름(Dataflow)을 분석합니다.
{: .prompt-info }

## 목차
* TOC
{:toc}

---

## 1. 정점 데이터 정의 (CPU)

렌더링의 시작은 C++ 환경에서 정의된 정점 배열 데이터입니다. 초기 데이터는 시스템 RAM에 저장됩니다.

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

각 정점은 위치, 색상, 텍스처 좌표라는 3가지 속성을 포함하는 구조를 가집니다.

---

## 2. 데이터 전송 및 가공 (VBO/VAO)

CPU 메모리의 데이터를 GPU VRAM으로 전송하여 처리 효율을 극대화합니다.

*   **VBO (Vertex Buffer Object):** 정점 데이터를 보관하는 GPU 내부의 메모리 버퍼입니다.
*   **VAO (Vertex Array Object):** VBO의 데이터를 셰이더 슬롯에 매핑하는 설정 정보(State)를 저장합니다.

버텍스 속성(Vertex Attribute)을 정의하여 데이터 레이아웃을 직렬화합니다.

```cpp
// 0번: 위치 (stride 8, offset 0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);

// 1번: 색상 (stride 8, offset 3)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(3 * sizeof(float)));
glEnableVertexAttribArray(1);

// 2번: 텍스처 좌표 (stride 8, offset 6)
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(6 * sizeof(float)));
glEnableVertexAttribArray(2);
```
{: file="main.cpp" }

---

## 3. 버텍스 셰이더 (Vertex Shader)

입력된 정점 좌표를 변환하고, 다음 파이프라인 단계로 속성값을 전달합니다.

```glsl
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
layout (location = 2) in vec2 aTexCoord;

out vec3 ourColor;
out vec2 TexCoord;

void main()
{
    gl_Position = vec4(aPos, 1.0); 
    ourColor = aColor;
    TexCoord = aTexCoord;
}
```
{: file="shader.vert" }

`gl_Position`은 래스터화 단계를 위해 시스템에서 예약된 변수이며, 나머지 속성들은 프래그먼트 셰이더로 전달됩니다.

---

## 4. 래스터라이제이션 (Rasterization)

버텍스 셰이더가 처리한 기하 데이터를 화면의 픽셀 단위 조각(Fragment)으로 분할하는 과정입니다. 이 단계에서 **선형 보간(Linear Interpolation)**이 수행되어, 각 프래그먼트는 정점 사이의 거리에 비례한 속성값을 할당받습니다.

---

## 5. 프래그먼트 셰이더 (Fragment Shader)

입력된 데이터를 바탕으로 최종 픽셀 색상을 결정합니다.

```glsl
#version 330 core
out vec4 FragColor;

in vec3 ourColor;
in vec2 TexCoord;

uniform sampler2D texture1;

void main()
{
    // 보간된 TexCoord를 사용하여 텍스처에서 색상을 샘플링
    FragColor = texture(texture1, TexCoord);
}
```
{: file="shader.frag" }

---

## 6. 전체 프로세스 요약

1.  **데이터 정의**: CPU(RAM)에 정점 속성 배열을 정의합니다.
2.  **데이터 전송**: VBO/VAO를 통해 데이터를 GPU VRAM으로 전송하고 레이아웃을 설정합니다.
3.  **좌표 변환**: 버텍스 셰이더에서 공간 변환을 수행하고 속성을 전달합니다.
4.  **래스터화**: 도형을 프래그먼트 단위로 분할하고 속성을 보간합니다.
5.  **색상 결정**: 프래그먼트 셰이더에서 텍스처를 참조하여 최종 색상을 결정합니다.
6.  **출력**: 처리된 데이터가 프레임버퍼를 거쳐 디스플레이 장치로 송출됩니다.
