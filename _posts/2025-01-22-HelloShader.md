---
categories: [Graphics]
tags: [graphics, opengl, shader, tutorial]
math: true
---
## 요약
> **요약**: 셰이더의 기본 개념과 GLSL 코드의 구조를 이해하고, 버텍스 셰이더와 프래그먼트 셰이더 간의 데이터 전달 및 유니폼(Uniform) 변수의 활용 원리를 알아본다.

## 목차
* TOC
{:toc}

---

**자료 출처**: [LearnOpenGL](https://learnopengl.com/)

## 셰이더란?

셰이더는 GPU에서 실행되는 프로그램으로, 화면을 그리거나 색을 입히는 기능을 수행한다. 셰이더는 기본적으로 다른 셰이더와 소통하기 위해 입력값과 출력값을 매개로 사용하며, 이전 셰이더의 출력값과 다음 셰이더의 입력값은 동일하게 맞춰주어야 한다.

OpenGL에서는 그래픽스 프로그래밍에 특화되어 벡터와 행렬 연산에 강점을 지닌 **GLSL (OpenGL Shading Language)** 언어를 사용한다.

## 셰이더(GLSL) 코드의 기본 구조

셰이더 코드는 일반적으로 다음과 같은 구조와 순서로 작성된다.

1. **버전 선언**: 사용할 GLSL의 런타임 버전을 선언한다.
2. **입력 변수 (`in`)**: 셰이더로 들어오는 값들(정점의 위치나 색상 등)을 정의한다.
3. **출력 변수 (`out`)**: 셰이더 처리가 끝난 후 다음 파이프라인으로 넘겨줄 결과 변수를 정의한다.
4. **유니폼 (`uniform`)**: 셰이더가 실행되는 동안 전역적으로 변하지 않는 값들을 정의한다.
5. **메인 함수 (`main`)**: 입력값을 받아 실제 연산을 처리하고, 결과를 출력 변수에 저장한다.

### 기본 작성 예시

```glsl
#version 330 core  // 버전 선언

in vec3 position;  // 입력 변수: 3D 공간에서 정점의 위치
in vec4 color;     // 입력 변수: 정점의 색상

out vec4 fragColor; // 출력 변수: 최종적으로 화면에 표시될 색상

uniform mat4 model;  // 유니폼 변수: 모델 변환 행렬 (장면에서의 객체 위치)

void main() {
    // 위치와 색상을 결합하고 행렬 연산을 수행하여 최종 색상을 계산한다.
    fragColor = color * model * vec4(position, 1.0); 
}
```
{: file="example.glsl" }

---

## GLSL의 데이터 타입

GLSL도 C/C++ 언어와 마찬가지로 `int`, `float` 같은 데이터 타입을 사용하지만, 3D 그래픽스 연산에 필요한 요소인 **벡터(Vector)**와 **행렬(Matrix)**을 기본적으로 다룰 수 있다.

### 벡터 (Vector)

GLSL에서 벡터는 2, 3, 4개의 기본 타입으로 이루어진 컨테이너다. `vec2`, `vec3`, `vec4` 처럼 다양한 크기의 벡터를 사용할 수 있으며 형태는 다음과 같다.

*   `vecn`: n개의 float로 이루어진 기본 벡터.
*   `bvecn`: n개의 bool로 이루어진 벡터.
*   `ivecn`: n개의 int로 이루어진 벡터.
*   `uvecn`: n개의 unsigned int로 이루어진 벡터.
*   `dvecn`: n개의 double로 이루어진 벡터.

벡터의 요소는 구조체 멤버 접근처럼 연산자를 이용해 손쉽게 접근할 수 있다. 예를 들어 `vec.x`, `vec.y`, `vec.z`, `vec.w`와 같이 벡터의 첫 번째부터 네 번째 요소를 각각 참조할 수 있다.

---

### 스위즐링 (Swizzling)

스위즐링은 기존 벡터의 요소들을 섞거나 재구성하여 새로운 벡터를 쉽게 만드는 GLSL만의 강력한 문법이다.
```glsl
vec2 someVec;
vec4 differentVec = someVec.xyxx;  // someVec의 x와 y를 가져와서 다른 벡터의 값으로 설정

vec3 anotherVec = differentVec.zyw;  // differentVec의 z, y, w를 가져와서 새로운 벡터로 설정

vec4 otherVec = someVec.xxxx + anotherVec.yxzy;  // 벡터 요소들을 조합하여 새로운 벡터를 만들기
```

이렇게 기존의 요소를 활용함으로써 써야 하는 인수의 수를 줄인다.

```glsl
vec2 vect = vec2(0.5, 0.7);

vec4 result = vec4(vect, 0.0, 0.0);  // vect 벡터를 사용해서 새로운 vec4 벡터 생성

vec4 otherResult = vec4(result.xyz, 1.0);  // result 벡터에서 xyz만 뽑아서 새로운 벡터 생성
```
---

위의 내용들을 활용하여 셰이더 간의 실제 데이터 전달 메커니즘을 확인해 본다.

## 버텍스 셰이더 (Vertex Shader)

```glsl
#version 330 core
layout (location = 0) in vec3 aPos; // 위치 변수는 속성 위치 0에서 입력되며, vec3 형태다.
  
out vec4 vertexColor; // 프래그먼트 셰이더로 전달할 색상 출력을 정의한다. (vec4 형태)

void main()
{
    gl_Position = vec4(aPos, 1.0); // vec3 타입을 vec4로 형변환하여 내장 변수 gl_Position에 전달한다.
    vertexColor = vec4(0.5, 0.0, 0.0, 1.0); // 출력 변수에 어두운 빨간색 값을 할당한다.
}
```
{: file="shader.vert" }

## 프래그먼트 셰이더 (Fragment Shader)

```glsl
#version 330 core
out vec4 FragColor; // 최종 색상을 출력하는 출력 변수
  
in vec4 vertexColor; // 버텍스 셰이더에서 전달된 입력 변수 (★이름과 타입이 동일해야 함)

void main()
{
    FragColor = vertexColor; // 버텍스 셰이더에서 받은 색상 값을 픽셀의 최종 색상으로 칠한다.
}
```
{: file="shader.frag" }

위 두 코드를 요약하자면, 버텍스 셰이더는 위치 연산을 수행함과 동시에 `vertexColor`라는 `vec4` 형태의 출력 변수를 만들어 어두운 빨간색을 담아 보냈다. 프래그먼트 셰이더는 **동일한 이름과 타입의 입력 변수**로 그 값을 받아들여 픽셀의 최종 색상(`FragColor`)으로 결정하게 된다.

---

이제 위의 상황에 **유니폼(Uniform) 변수**를 추가해서 활용해 본다. 프래그먼트 셰이더를 아래와 같이 수정했다고 가정하자.

```glsl
out vec4 FragColor;

uniform vec4 ourColor; // OpenGL의 C++ 코드 측에서 이 값을 직접 설정할 수 있다.

void main()
{
    FragColor = ourColor; // Uniform으로 받은 값을 최종 출력 색상으로 설정한다.
}
```
{: file="shader.frag" }

> [!info] 
> 유니폼(Uniform)은 셰이더 프로그램 내에서 전역 변수처럼 작동하므로 프로그램 어디서든지 자유롭게 불러다 쓸 수 있는 매우 편리하고 강력한 변수다.

C++(OpenGL) 코드에서 유니폼 변수를 조작하는 방법은 아래와 같다.

```cpp
while (!glfwWindowShouldClose(window))
{
    // 1. 입력 처리
    processInput(window);

    // 2. 화면 초기화
    glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);

    // 3. 셰이더 프로그램 활성화
    glUseProgram(shaderProgram);

    // 4. 시간 기반으로 색상 값 수학적 계산
    float timeValue = glfwGetTime();
    float greenValue = sin(timeValue) / 2.0f + 0.5f;

    // 5. Uniform 변수 위치를 가져오고 매 프레임마다 값 업데이트
    int vertexColorLocation = glGetUniformLocation(shaderProgram, "ourColor");
    glUniform4f(vertexColorLocation, 0.0f, greenValue, 0.0f, 1.0f);

    // 6. 삼각형 렌더링
    glBindVertexArray(VAO);
    glDrawArrays(GL_TRIANGLES, 0, 3);

    // 7. 버퍼 교체 및 이벤트 처리
    glfwSwapBuffers(window);
    glfwPollEvents();
}
```
{: file="main.cpp" }

위 코드 5번 라인(`glGetUniformLocation`)에서 볼 수 있듯, 활성화된 셰이더 프로그램 내에서 `"ourColor"`로 명명된 유니폼 변수의 메모리 위치를 찾아 `vertexColorLocation`에 저장한다. 이후 `glUniform4f` 함수를 이용해 해당 위치에 색상 값을 프레임 단위로 주입한다. 이 상태로 렌더 루프가 실행되면, 시간이 지남에 따라 점진적으로 [초록색이 명멸하는 삼각형](https://learnopengl.com/video/getting-started/shaders.mp4)을 화면에서 확인할 수 있다.

---
## 더 많은 버텍스 속성(Attribute) 다루기

초기 단계에서 VAO는 위치 데이터(속성)만 포함된 VBO를 바인딩해서 다루었다. 이제 한 단계 더 나아가 동일한 VBO 버퍼 컨텍스트 안에 정점의 **색상 정보**까지 추가해 보자.

```cpp
float vertices[] = {
    // 위치 (x, y, z)      // 색상 (R, G, B)
     0.5f, -0.5f, 0.0f,  1.0f, 0.0f, 0.0f,  // 오른쪽 아래 정점 (빨강)
    -0.5f, -0.5f, 0.0f,  0.0f, 1.0f, 0.0f,  // 왼쪽 아래 정점 (초록)
     0.0f,  0.5f, 0.0f,  0.0f, 0.0f, 1.0f   // 위쪽 정점 (파랑)
};
```

각 꼭짓점은 이제 3개의 위치 float 데이터와 3개의 색상 float 데이터를 교차 형태로 포함한다.

### 버텍스 셰이더 수정

추가된 색상 데이터를 입력받으려면, 버텍스 셰이더에 새로운 입력 변수(Attribute)인 `aColor`를 열어주어야 한다.

```glsl
#version 330 core
layout (location = 0) in vec3 aPos;   // 속성 인덱스 0번: 위치
layout (location = 1) in vec3 aColor; // 속성 인덱스 1번: 색상

out vec3 ourColor; // 프래그먼트 셰이더로 색상을 토스할 출력 변수

void main()
{
    gl_Position = vec4(aPos, 1.0); // 위치 계산 및 할당
    ourColor = aColor;             // 입력받은 정점 색상을 ourColor에 그대로 저장
}
```
{: file="shader.vert" }

`layout (location = N)` 지정자를 통해 위치는 0번, 색상은 1번 인덱스로 메모리 레이아웃을 확정 짓는다.

### 프래그먼트 셰이더 수정

프래그먼트 셰이더는 버텍스 셰이더로부터 브릿지된 색상 데이터를 받아와 화면에 최종 출력한다.

```glsl
#version 330 core
out vec4 FragColor;  

in vec3 ourColor; // 버텍스 셰이더로부터 토스받은 입력 색상 변수

void main()
{
    FragColor = vec4(ourColor, 1.0); // 알파값(투명도) 1.0을 더해 최종 색상으로 도출
}
```
{: file="shader.frag" }

### 버텍스 속성 포인터 재설정

새로운 버퍼 레이아웃 구조를 반영하려면, C++ 코드 단에서 속성 포인터(Attribute Pointer)를 다시 해석해 주어야 한다. 위치와 색상 데이터가 VBO 내부에 나란히 교차(interleaved)되어 직렬화되었기 때문이다.

![VBO Interleaved Layout](/images/vertex_attribute_pointer_interleaved.png){: width="700" }
_위치(XYZ)와 색상(RGB) 값이 번갈아 저장된 VBO 메모리 레이아웃_

```cpp
// 위치 속성 해독 규칙 (attribute 0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);

// 색상 속성 해독 규칙 (attribute 1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));
glEnableVertexAttribArray(1);
```
{: file="main.cpp" }

> [!important] 
> **포인터 해독 요소 분석**
> *   `stride (보폭)`: 한 묶음의 정점 데이터 전체 크기는 `6 * sizeof(float)` (위치 3개 + 색상 3개)로 설정된다. GPU는 데이터를 읽을 때마다 이 크기만큼 점프해야 한다.
> *   `offset (시작점)`: 위치 데이터(0번 속성)는 메모리 덩어리의 맨 앞마당인 `0`에서 시작하고, 색상 데이터(1번 속성)는 위치 데이터 크기를 건너뛴 `3 * sizeof(float)` 지점에서 시작해야 한다.

---

## 렌더링 결과의 미학: 프래그먼트 보간 (Fragment Interpolation)

삼각형 렌더링 루프를 돌려보면 경이로운 결과를 확인할 수 있다. 개발자가 명시한 정점 색상은 빨강, 초록, 파랑 3개뿐이었지만 화면에는 이 색상들이 부드러운 그라데이션으로 섞여 묘사된다.

이는 렌더링 시 **픽셀(Fragment)의 수가 정점(Vertex)의 수보다 압도적으로 많기 때문**에 발생하는 기하학적 현상이다. 

*   래스터라이제이션 단계에서 그래픽스 파이프라인은 정점 사이의 수많은 픽셀들에 대해 색상을 **선형 보간(Linear Interpolation)** 한다.
*   예를 들어, 1번(빨강)과 2번(파랑) 정점 사이를 잇는 선상 내부의 픽셀 색상들은 빨강에서 파랑으로 점진적으로 부드럽게 변환된다. 삼각형의 정중앙에 가까워질수록 세 색상이 균일하게 섞여 흰색 톤 픽셀이 렌더링된다.

![Fragment Interpolation Result](/images/image.png){: width="400" }
_보간(Interpolation) 연산으로 부드러운 그라데이션이 적용되어 그려진 삼각형_
