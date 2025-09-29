---
categories: graphics
tags: [graphics, opengl, shader, texture, gpu]
toc: true
toc_sticky: true
author_profile: false
use_math: true
---

# 버텍스 데이터의 흐름 정리(with texture)

## 1. 버텍스 데이터 정의

```c++
float vertices[] = {
    // 위치                // 색상              // 텍스처 좌표
     0.5f,  0.5f, 0.0f,   1.0f, 0.0f, 0.0f,   1.0f, 1.0f, // 우상단
     0.5f, -0.5f, 0.0f,   0.0f, 1.0f, 0.0f,   1.0f, 0.0f, // 우하단
    -0.5f, -0.5f, 0.0f,   0.0f, 0.0f, 1.0f,   0.0f, 0.0f, // 좌하단
    -0.5f,  0.5f, 0.0f,   1.0f, 1.0f, 0.0f,   0.0f, 1.0f  // 좌상단 
};
```

## 버텍스 데이터 구조

각 버텍스는 8개의 속성값을 갖는다.

1.  **위치 (aPos, vec3)** → x, y, z 좌표
2.  **색상 (aColor, vec3)** → r, g, b 색상값
3.  **텍스처 좌표 (aTexCoord, vec2)** → s, t 좌표 (0~1 범위)

## 2. 버텍스 데이터 → 버텍스 셰이더로 전달**

버텍스 데이터를 GPU에 전송하기 위해 **VAO (Vertex Array Object), VBO (Vertex Buffer Object)**를 사용한다.

*   **VBO (Vertex Buffer Object):** 버텍스 데이터를 GPU 메모리에 저장하는 버퍼다. CPU의 데이터를 GPU로 효율적으로 전달하는 역할을 한다.
*   **VAO (Vertex Array Object):** 버텍스 속성(위치, 색상, 텍스처 좌표 등)의 설정 상태를 저장하는 객체다. 셰이더에서 어떤 속성을 어떻게 사용할지 미리 정의해두면, 매번 속성을 설정할 필요 없이 VAO만 바인딩하여 사용할 수 있다.

각 속성은 Vertex Attribute로 설정되어 버텍스 셰이더의 입력 변수로 전달된다. 쉽게 말해, 각 속성(위치, 색상, 텍스처 좌표)을 버텍스 셰이더가 이해할 수 있는 형태로 설정하는 과정이다.

## 버텍스 속성 바인딩

```c++
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);

glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(3 * sizeof(float)));
glEnableVertexAttribArray(1);

glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(float), (void*)(6 * sizeof(float)));
glEnableVertexAttribArray(2);
```

각각의 속성을 버텍스 셰이더의 입력 변수에 매칭한다.

*   aPos (location = 0) → (x, y, z)
*   aColor (location = 1) → (r, g, b)
*   aTexCoord (location = 2) → (s, t)

## 3. 버텍스 셰이더 동작

```glsl
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;
layout (location = 2) in vec2 aTexCoord;

out vec3 ourColor;
out vec2 TexCoord;

void main()
{
    gl_Position = vec4(aPos, 1.0); // aPos를 4차원 벡터로 변환 (1.0은 동차 좌표계의 w 값)
    ourColor = aColor;
    TexCoord = vec2(aTexCoord.x, aTexCoord.y);
}
```

## 데이터 흐름

*   aPos (버텍스 위치) → `gl_Position`으로 변환 (클립 공간 좌표)
*   aColor (색상 정보) → ourColor로 전달 (프래그먼트 셰이더로 전달)
*   aTexCoord (텍스처 좌표) → TexCoord로 전달 (프래그먼트 셰이더로 전달)

```버텍스 셰이더의 입력값은 aPos, aColor, aTexCoord 총 3개이며, 출력값은 gl_Position, ourColor, TexCoord 로 총 3개다. 하지만, 프래그먼트 셰이더로 직접 전달되는 데이터는 ourColor와 TexCoord 총 2개다. gl_Position은 래스터라이제이션 단계에서 사용되어 프래그먼트의 위치를 결정하는 데 사용되며, 프래그먼트 셰이더로는 전달되지 않는다.```

## 4. 래스터라이제이션 과정

버텍스 셰이더에서 정의한 정점이 화면에 매핑될 픽셀 단위의 **프래그먼트**를 생성하는 과정이다. 이 과정에서 **각 프래그먼트의 색상 및 텍스처 좌표가 보간(Interpolation)**된다. 즉, 삼각형 내부의 픽셀들은 정점의 색상과 텍스처 좌표를 바탕으로 선형 보간을 통해 자신만의 색상과 텍스처 좌표를 갖게 된다.

## 5. 프래그먼트 셰이더 동작

```glsl
#version 330 core
out vec4 FragColor;

in vec3 ourColor;
in vec2 TexCoord;

uniform sampler2D texture1; // 텍스처 샘플러

void main()
{
    FragColor = texture(texture1, TexCoord);
}
```

## 데이터 흐름

*   TexCoord → 보간된 텍스처 좌표 값 (프래그먼트별로 다름)
*   `uniform sampler2D texture1;` → 텍스처를 샘플링하기 위한 객체. 텍스처 이미지를 GPU에 로드하고, 셰이더에서 텍스처에 접근할 수 있도록 해준다.
*   texture(texture1, TexCoord) → 텍스처에서 해당 좌표의 색상을 가져온다.
*   FragColor → 최종 픽셀 색상 출력

## 정리

→ 버텍스 셰이더에서 전달받은 텍스처 좌표(TexCoord)를 기반으로  
→ 텍스처에서 해당 좌표의 색상을 샘플링(`texture(texture1, TexCoord)`)하여  
→ 화면에 픽셀 색상을 최종 출력하는 역할을 한다.

## 6. 최종 출력

이제 모든 데이터가 GPU에서 픽셀 단위로 변환되어 화면에 렌더링된다.

*   버텍스 데이터의 각 정점(네 개의 꼭짓점)이 버텍스 셰이더를 통해 위치를 결정한다.
*   래스터라이제이션을 통해 삼각형 내부 픽셀들이 보간된다.
*   프래그먼트 셰이더에서 각 픽셀의 텍스처 좌표를 사용하여 텍스처 이미지에서 해당 위치의 색상을 가져와 최종 픽셀 색상으로 사용한다. 이를 통해 텍스처 매핑이 이루어진다.
*   최종적으로 GPU가 색상을 렌더링하여 화면에 사각형 형태로 텍스처가 출력된다.

## 전체 데이터 흐름 요약 (간결하게)

1.  **정점 정의:** 위치, 색상, 텍스처 좌표 정의
2.  **GPU 전송:** VAO/VBO를 통해 OpenGL에 데이터 전달
3.  **정점 셰이더:** 정점 위치 변환 (`gl_Position`), 프래그먼트 셰이더에 데이터 전달
4.  **래스터라이제이션:** 픽셀 단위 프래그먼트 생성 및 보간
5.  **프래그먼트 셰이더:** 텍스처 샘플링 후 픽셀 색상 결정
6.  **화면 렌더링:** 최종 픽셀 색상으로 화면에 출력

---


