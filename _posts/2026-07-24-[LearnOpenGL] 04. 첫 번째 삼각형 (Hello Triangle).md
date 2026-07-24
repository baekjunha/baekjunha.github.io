---
title: "[LearnOpenGL] 04. 첫 번째 삼각형 (Hello Triangle)"
date: 2026-07-24 18:10:33 +0900
categories: [Graphics, LearnOpenGL]
tags: [opengl, cpp, graphics, translation, vertex-shader, fragment-shader, vao, vbo, ebo]
---

> 📢 **안내 및 출처 표기 (Attribution)**
> * 본 포스팅은 Joey de Vries가 작성한 튜토리얼 **[LearnOpenGL.com](https://learnopengl.com/Getting-started/Hello-Triangle)**의 원문을 바탕으로 한 한국어 번역 및 학습 정리입니다.
> * 원문 저작권은 **Joey de Vries**에게 있으며, **CC BY-NC 4.0** 라이선스를 준수합니다. 원문: [https://learnopengl.com/Getting-started/Hello-Triangle](https://learnopengl.com/Getting-started/Hello-Triangle)

---

## 🔺 3D 공간을 2D 픽셀로 변환하는 서사: 그래픽스 파이프라인

그래픽스 프로그래밍의 본질은 **"가상의 3D 공간 좌표들을 모니터라는 평면 2D 픽셀 배열로 변환하는 것"**입니다. 이 장엄한 데이터 변환 여정을 담당하는 렌더링 공장이 바로 **그래픽스 파이프라인(Graphics Pipeline)**입니다.

그래픽스 파이프라인은 수많은 단계로 세분화되어 있으며, 각 단계는 오직 한 가지 작업만 빠르게 수행하도록 설계되어 있습니다. 이 단계들은 서로 독립적이고 극도로 병렬화가 가능하여, GPU 내부의 수천 개 미니 처리 코어(ALU)에서 동시에 실행됩니다. 이 GPU 병렬 코어에서 작동하는 미니 프로그램을 **셰이더(Shader)**라고 부릅니다.

![렌더링 파이프라인](https://learnopengl.com/img/getting-started/pipeline.png)

### 🌊 그래픽스 파이프라인 6단계 데이터 흐름

1. **버텍스 셰이더 (Vertex Shader - 프로그래밍 가능)**:
   삼각형의 꼭짓점인 3D 버텍스 좌표 하나하나를 변환합니다. 좌표 공간 변환(3D $\rightarrow$ 2D) 및 기기 정규화(NDC)를 담당합니다.
2. **지오메트리 셰이더 (Geometry Shader - 프로그래밍 가능 / 선택)**:
   선택적 단계로, 입력받은 도형(점, 선, 삼각형)의 버텍스들을 바탕으로 새로운 도형을 생성해 냅니다.
3. **프리미티브 조립 (Primitive Assembly)**:
   버텍스 셰이더가 내놓은 점들을 이어붙여 점(`GL_POINTS`), 선(`GL_LINES`), 삼각형(`GL_TRIANGLES`) 등 지정된 도형 형태(Primitive)로 연결합니다.
4. **래스터화 (Rasterization)**:
   조립된 3D 도형을 모니터 해상도 픽셀 grid 위에 놓아두고, 도형 내부를 덮는 2D 조각들인 **프래그먼트(Fragment)**를 한 땀 한 땀 쪼개어 생성합니다. 화면 밖 영역은 성능을 위해 클리핑(Clipping) 처리됩니다.
5. **프래그먼트 셰이더 (Fragment Shader - 프로그래밍 가능)**:
   래스터화가 쪼개놓은 프래그먼트 하나하나의 **최종 픽셀 색상(RGBA)**을 계산합니다. 조명, 그림자, 텍스처 컬러링 등 그래픽스의 화려한 시각 효과가 주로 발생합니다.
6. **알파 테스트 및 블렌딩 (Alpha Test & Blending)**:
   그려질 픽셀이 다른 물체 뒤에 가려졌는지 검사(Depth Test)하고, 투명도(Alpha)를 고려해 기존 화면 색상과 합성합니다.

---

## 📦 1. 데이터의 GPU 이동: 버텍스 버퍼 오브젝트 (VBO)

삼각형을 그리려면 세 개의 3D 좌표 꼭짓점이 필요합니다.

```cpp
float vertices[] = {
    -0.5f, -0.5f, 0.0f, // 좌측 하단
     0.5f, -0.5f, 0.0f, // 우측 하단
     0.0f,  0.5f, 0.0f  // 중앙 상단
};
```

> ### 💡 [깊이 읽기] 버스(Bus) 병목과 VBO: 왜 RAM이 아닌 VRAM에 데이터를 둘까?
> 
> 컴퓨터 구조에서 CPU(RAM)에서 GPU(VRAM)로 데이터를 전송하는 통로(PCIe 버스)는 그래픽 연산 속도에 비해 상대적으로 둔하고 느립니다.
> 
> 매 프레임마다 CPU가 RAM에서 좌표를 꺼내 GPU로 하나씩 전송한다면, GPU는 전송 대기시간 동안 노는 병목 현상(Bottleneck)이 발생합니다.
> 
> 이 문제를 해결하기 위해 **VBO (Vertex Buffer Object)**를 만듭니다. CPU 메모리(RAM)에 있는 버텍스 좌표 배열 덩어리를 GPU 고속 메모리(VRAM)에 단 한 번 대량 복사해 두고, 렌더 루프에서는 *"VRAM 메모리 번지 `VBO`에 올려둔 좌표들로 바로 그려라"* 라고 명령만 내립니다.

```cpp
// 1. GPU 메모리에 버퍼 번호(ID) 할당
unsigned int VBO;
glGenBuffers(1, &VBO);

// 2. GL_ARRAY_BUFFER 슬롯에 VBO 바인딩 (선택)
glBindBuffer(GL_ARRAY_BUFFER, VBO);

// 3. CPU RAM(vertices) 데이터를 현재 바인딩된 GPU VRAM(GL_ARRAY_BUFFER)으로 전송
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
```

`GL_STATIC_DRAW` 힌트는 *"이 데이터는 한 번 복사해 두면 변경되지 않고 계속 렌더링에 재사용된다"*는 의미로, GPU가 최고속 읽기 전용 VRAM 영역에 데이터를 배치하도록 유도합니다.

---

## ⚡ 2. GPU 미니 프로그램 작성: 버텍스 & 프래그먼트 셰이더

모던 OpenGL에서는 GPU가 기본적으로 해주는 셰이더가 없습니다. 반드시 직접 작성한 GLSL(OpenGL Shading Language) 코드를 런타임 컴파일해 주입해야 합니다.

### 버텍스 셰이더 (Vertex Shader)
```glsl
#version 330 core
layout (location = 0) in vec3 aPos; // VBO에서 들어올 0번 속성 (3D 좌표)

void main()
{
    // 내장 변수 gl_Position에 4D 동차 좌표(Homogeneous Coordinates) 지정
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
```

### 프래그먼트 셰이더 (Fragment Shader)
```glsl
#version 330 core
out vec4 FragColor; // 최종 출력 픽셀 색상 (RGBA)

void main()
{
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f); // 주황색 설정
}
```

### 셰이더 컴파일과 프로그램 링킹 서사

```cpp
// 1. 버텍스 셰이더 컴파일
unsigned int vertexShader = glCreateShader(GL_VERTEX_SHADER);
glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
glCompileShader(vertexShader);

// 2. 프래그먼트 셰이더 컴파일
unsigned int fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
glCompileShader(fragmentShader);

// 3. 셰이더 프로그램(Shader Program) 생성 및 파이프라인 링킹
unsigned int shaderProgram = glCreateProgram();
glAttachShader(shaderProgram, vertexShader);
glAttachShader(shaderProgram, fragmentShader);
glLinkProgram(shaderProgram);

// 링킹 후 개별 셰이더 객체 메모리 해제
glDeleteShader(vertexShader);
glDeleteShader(fragmentShader);
```

우리가 만든 셰이더 코드는 C++ 문자열 형태로 존재하다가, 실행 중 `glCompileShader`와 `glLinkProgram`을 통해 GPU 그래픽 드라이버의 전용 컴파일러에 의해 **GPU 기계어로 번역되어 셰이더 프로그램 객체에 탑재**됩니다.

---

## 📋 3. 메모리 데이터 해석과 레시피 북: VAO (Vertex Array Object)

GPU VRAM에 바이트 덩어리(VBO)를 올렸고, GPU 셰이더 프로그램도 준비했습니다. 이제 둘을 연결해 주어야 합니다.

GPU 입장에서 VBO에 들어있는 데이터는 단순한 0과 1의 연속된 바이너리일 뿐입니다. 데이터의 몇 바이트가 위치($x, y, z$)이고 어디까지가 다음 좌표인지 알지 못합니다.

```cpp
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);
```

* `0`: 셰이더의 `layout (location = 0)` 입력 변수에 연결
* `3`: 데이터가 3개의 성분(`vec3`)으로 구성됨
* `GL_FLOAT`: 데이터타입은 32비트 float
* `3 * sizeof(float)`: **Stride (보폭)**. 한 버텍스 데이터에서 다음 버텍스 데이터까지 떨어져 있는 메모리 간격
* `(void*)0`: **Offset**. 이 속성이 버퍼의 몇 번째 바이트부터 시작하는지 나타내는 위치 offset

> ### 💡 [깊이 읽기] 무대 뒤 레시피 북: VAO (Vertex Array Object)
> 
> 만약 렌더링할 3D 물체가 수천 개라면, 매 프레임 수천 번씩 `glBindBuffer`, `glVertexAttribPointer`, `glEnableVertexAttribArray` 명령을 반복해야 할까요? 이는 심각한 CPU 오버헤드를 일으킵니다.
> 
> **VAO (Vertex Array Object)**는 이 버텍스 속성 설정과 VBO 바인딩 상태 전체를 캡슐화해 기록하는 **"바인더(설명서) 객체"**입니다.

```cpp
// --- [초기화 단계] 단 한 번만 수행 ---
unsigned int VAO, VBO;
glGenVertexArrays(1, &VAO);
glGenBuffers(1, &VBO);

// 1. 레시피 바인더(VAO) 바인딩 시작
glBindVertexArray(VAO);

// 2. VBO 바인딩 및 데이터 업로드 (이 바인딩 정보가 VAO에 기록됨)
glBindBuffer(GL_ARRAY_BUFFER, VBO);
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

// 3. 버텍스 속성 해석법 설정 (이 포맷 정보도 VAO에 기록됨)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);

// 4. VAO 바인딩 해제 (설정 기록 완료)
glBindVertexArray(0);

// --- [렌더 루프] 매 프레임 그리기 ---
glUseProgram(shaderProgram);
glBindVertexArray(VAO); // 바인더만 바인딩하면 준비 완료!
glDrawArrays(GL_TRIANGLES, 0, 3);
```

이 덕분에 렌더 루프 안에서는 복잡한 버퍼 설정을 재호출할 필요 없이 `glBindVertexArray(VAO)` 한 줄만 호출하면 삼각형을 바로 그릴 수 있게 됩니다!

---

## 💎 4. 인덱스 드로잉과 엘리먼트 버퍼 오브젝트 (EBO)

사각형(Rectangle)을 그리려면 삼각형 2개가 필요하며 총 6개의 버텍스 좌표가 요구됩니다.

```cpp
// 6개의 버텍스 중 2개가 중복됨 (우측하단, 좌측상단 좌표)
float vertices[] = {
     0.5f,  0.5f, 0.0f,  // 0: 우측 상단
     0.5f, -0.5f, 0.0f,  // 1: 우측 하단
    -0.5f,  0.5f, 0.0f,  // 2: 좌측 상단

     0.5f, -0.5f, 0.0f,  // 1: 우측 하단 (중복!)
    -0.5f, -0.5f, 0.0f,  // 3: 좌측 하단
    -0.5f,  0.5f, 0.0f   // 2: 좌측 상단 (중복!)
};
```

수천 개의 복잡한 3D 메쉬 모델에서 버텍스가 중복되면 수십 MB의 VRAM 정크 메모리가 낭비됩니다.

이를 해결하기 위해 **고유한 버텍스 4개만 저장하고, 이 버텍스들을 어떤 순서로 조합해서 삼각형을 만들지 정수 인덱스 배열로 정의하는 인덱스 드로잉(Indexed Drawing)**을 활용하며, 이 인덱스 배열을 VRAM에 보관하는 객체가 **EBO (Element Buffer Object)**입니다.

```cpp
// 고유 좌표 4개만 정의
float vertices[] = {
     0.5f,  0.5f, 0.0f,  // 0: 우측 상단
     0.5f, -0.5f, 0.0f,  // 1: 우측 하단
    -0.5f, -0.5f, 0.0f,  // 2: 좌측 하단
    -0.5f,  0.5f, 0.0f   // 3: 좌측 상단
};

// 삼각형 2개를 만들 버텍스 인덱스 순서 지정
unsigned int indices[] = {
    0, 1, 3, // 첫 번째 삼각형 (0번, 1번, 3번 점 연결)
    1, 2, 3  // 두 번째 삼각형 (1번, 2번, 3번 점 연결)
};
```

```cpp
// EBO 생성 및 VAO에 기록
unsigned int EBO;
glGenBuffers(1, &EBO);

glBindVertexArray(VAO);

glBindBuffer(GL_ARRAY_BUFFER, VBO);
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);

// 렌더 루프 드로잉 (glDrawArrays 대신 glDrawElements 사용)
glUseProgram(shaderProgram);
glBindVertexArray(VAO);
glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
```

VAO는 `GL_ELEMENT_ARRAY_BUFFER` 바인딩 상태도 함께 저장하므로, EBO 설정 역시 VAO 하나로 완벽하게 캡슐화됩니다.

![Hello Triangle Output](https://learnopengl.com/img/getting-started/hellotriangle.png)

---

## 🎯 전체 소스 코드 및 연습문제

* **삼각형 예제 소스 코드**: [LearnOpenGL Hello Triangle Source](https://github.com/JoeyDeVries/LearnOpenGL/blob/master/src/1.getting_started/2.1.hello_triangle/hello_triangle.cpp)
* **EBO 사각형 예제 소스 코드**: [LearnOpenGL Hello Triangle Indexed Source](https://github.com/JoeyDeVries/LearnOpenGL/blob/master/src/1.getting_started/2.2.hello_triangle_indexed/hello_triangle_indexed.cpp)

### 💡 도전 연습문제
1. `glDrawArrays`를 활용해 좌표를 추가하여 두 개의 삼각형을 나란히 그려보세요 ([해답 소스](https://github.com/JoeyDeVries/LearnOpenGL/blob/master/src/1.getting_started/2.3.hello_triangle_exercise1/hello_triangle_exercise1.cpp))
2. 두 개의 서로 다른 VAO와 VBO를 만들어 두 개의 삼각형을 각각 독립적으로 제어해 보세요 ([해답 소스](https://github.com/JoeyDeVries/LearnOpenGL/blob/master/src/1.getting_started/2.4.hello_triangle_exercise2/hello_triangle_exercise2.cpp))
3. 셰이더 프로그램을 2개 만든 뒤 하나는 노란색 프래그먼트 셰이더를 주입해, 두 삼각형 중 하나만 노란색으로 출력되도록 해보세요 ([해답 소스](https://github.com/JoeyDeVries/LearnOpenGL/blob/master/src/1.getting_started/2.5.hello_triangle_exercise3/hello_triangle_exercise3.cpp))
