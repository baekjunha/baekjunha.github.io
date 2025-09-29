---
categories: graphics
tag: graphic
toc: true
toc_sticky: true
author_profile: false
use_math: true 
thumbnail: images/image.png
---

## 최종적으로 삼각형 렌더링 이해하기

자료출처:https://learnopengl.com/

## Hello Triangle (OpenGL 튜토리얼)

이 문서는 OpenGL에서 3D 좌표를 화면의 2D 픽셀로 변환하여 삼각형을 그리는 과정을 설명한다. OpenGL의 핵심인 그래픽 파이프라인을 이해하고, 이를 활용하여 기본적인 렌더링을 수행하는 방법을 배울 수 있다.

### 1. 그래픽 파이프라인 개요

OpenGL에서는 모든 것이 3D 공간에 존재하지만, 최종적으로 화면에 보이는 것은 2D 픽셀이다. 따라서 3D 좌표를 2D 픽셀로 변환하는 과정이 필수적이며, 이는 **그래픽 파이프라인(Graphics Pipeline)**에 의해 관리된다.

그래픽 파이프라인은 크게 두 부분으로 나뉜다.

*   **3D 좌표 -> 2D 좌표 변환:** 3차원 공간의 좌표를 2차원 평면에 투영한다.
*   **2D 좌표 -> 픽셀 변환:** 2차원 좌표를 기반으로 실제 픽셀의 색상을 결정한다.

그래픽 파이프라인은 여러 단계로 구성되어 있으며, 각 단계는 이전 단계의 출력을 입력으로 사용한다. 각 단계는 특정 작업만 수행하도록 고도로 특화되어 있으며, 병렬로 실행하기 용이하다. 이러한 병렬 구조 덕분에 현대 GPU는 수천 개의 코어를 활용하여 데이터를 빠르게 처리할 수 있다.

각 단계를 처리하는 작은 프로그램을 **셰이더(Shader)**라고 부른다. 개발자는 일부 셰이더를 직접 작성하여 파이프라인의 동작을 제어할 수 있다. 셰이더는 OpenGL 셰이딩 언어(GLSL)로 작성된다.

![alt text](https://learnopengl.com/img/getting-started/pipeline.png)

### 2. 그래픽 파이프라인 단계별 설명

다음은 그래픽 파이프라인의 각 단계에 대한 간략한 설명이다. 파란색으로 표시된 단계는 개발자가 직접 셰이더를 작성하여 제어할 수 있는 부분이다.

1.  **정점 데이터 (Vertex Data):**

    *   그래픽 파이프라인의 입력 데이터이다.
    *   3D 좌표와 추가적인 속성(색상, 텍스처 좌표 등)을 포함하는 **정점(Vertex)**들의 모음으로 구성된다.
    *   OpenGL은 이 데이터를 어떻게 렌더링할지 알기 위해 렌더링 형태를 지정하는 **프리미티브(Primitive)** 정보를 필요로 한다. (점, 선, 삼각형 등)

2.  **정점 셰이더 (Vertex Shader):** (개발자 제어 가능)

    *   하나의 정점을 입력으로 받아 3D 좌표를 변환한다.
    *   정점의 속성에 대한 기본적인 처리를 수행할 수 있다.

3.  **기하 셰이더 (Geometry Shader):** (선택 사항, 개발자 제어 가능)

    *   프리미티브를 구성하는 정점들의 모음을 입력으로 받아 새로운 정점을 생성하거나 새로운 프리미티브를 만들 수 있다.

4.  **프리미티브 조립 (Primitive Assembly):**

    *   정점 셰이더(또는 기하 셰이더)에서 출력된 정점들을 사용하여 지정된 프리미티브 형태(삼각형, 선 등)를 구성한다.

5.  **래스터화 (Rasterization):**

    *   프리미티브를 화면의 픽셀에 매핑하여 **프래그먼트(Fragment)**를 생성한다.
    *   프래그먼트는 픽셀을 렌더링하는 데 필요한 모든 데이터를 포함한다.
    *   래스터화 단계 전에 **클리핑(Clipping)**이 수행되어 화면 바깥쪽에 있는 프래그먼트를 제거하여 성능을 향상시킨다.

6.  **프래그먼트 셰이더 (Fragment Shader):** (개발자 제어 가능)

    *   픽셀의 최종 색상을 계산한다.
    *   조명, 그림자, 텍스처 등 복잡한 OpenGL 효과를 계산할 수 있다.

7.  **알파 테스트 및 블렌딩 (Alpha Test and Blending):**

    *   프래그먼트 셰이더에서 계산된 색상을 기반으로 최종 픽셀 색상을 결정한다.
    *   깊이 값(Depth Value)을 검사하여 다른 객체와의 전후 관계를 처리한다.
    *   알파 값(불투명도)을 사용하여 객체를 혼합한다.

### 3. 셰이더 (Shader) 이해

**셰이더**는 그래픽 하드웨어에서 실행되는 프로그램으로, 그래픽 처리의 특정 단계를 담당한다. 주로 사용되는 셰이더는 **정점 셰이더**와 **프래그먼트 셰이더**이다.

*   **정점 셰이더:** 각 정점의 위치를 처리한다.
*   **프래그먼트 셰이더:** 각 픽셀에 대한 색상을 결정한다.

#### 3.1. 정점 셰이더 (Vertex Shader) 코드 예시

```glsl
#version 330 core
layout (location = 0) in vec3 aPos;

void main()
{
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}
```

*   **`#version 330 core`**: GLSL 버전을 지정한다. (OpenGL 3.3 버전에 해당)
*   **`layout (location = 0) in vec3 aPos;`**: 입력 변수 `aPos`를 선언한다. `vec3`는 3차원 벡터를 의미하며, `location = 0`은 이 변수가 0번 위치에 바인딩됨을 나타낸다. 이 위치는 나중에 정점 데이터를 셰이더에 전달할 때 사용된다.
*   **`gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);`**: 각 정점의 위치를 지정한다. `gl_Position`은 OpenGL에서 제공하는 기본 변수로, 화면에 그려질 정점의 위치를 결정한다. `vec4`는 4차원 벡터를 의미하며, `w` 값은 1.0으로 설정된다. 이는 "동차 좌표(homogeneous coordinates)" 개념으로, 후속 변환(투영 등)에 필요하다.

이 예제는 가장 기본적인 정점 셰이더로, 입력 데이터를 별도의 처리 없이 그대로 출력한다. 실제 응용 프로그램에서는 입력 데이터가 NDC (Normalized Device Coordinates, 정규화된 장치 좌표) 영역에 포함되지 않는 경우가 많으므로, 변환 과정을 거쳐야 한다.

#### 3.2. 프래그먼트 셰이더 (Fragment Shader) 코드 예시

```glsl
#version 330 core
out vec4 FragColor;

void main()
{
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}
```

*   **`out vec4 FragColor;`**: 출력 변수 `FragColor`를 선언한다. 이 변수는 픽셀의 최종 색상을 저장하는 데 사용된다.
*   **`FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);`**: 픽셀의 색상을 오렌지색으로 설정한다. `vec4`는 RGBA (Red, Green, Blue, Alpha) 값을 나타내며, 각 색상 컴포넌트는 0.0에서 1.0 사이의 값을 가진다. Alpha 값은 불투명도를 나타낸다.

#### 3.3. 셰이더 컴파일

셰이더를 사용하기 위해서는 먼저 코드를 작성하고, OpenGL이 실행할 수 있도록 컴파일해야 한다.

1.  **소스 코드 저장:** 셰이더 소스 코드를 문자열 형태로 저장한다.

    ```c++
    const char *vertexShaderSource = "#version 330 core\n"
        "layout (location = 0) in vec3 aPos;\n"
        "void main()\n"
        "{\n"
        "   gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);\n"
        "}\0";

    const char *fragmentShaderSource = "#version 330 core\n"
        "out vec4 FragColor;\n"
        "void main()\n"
        "{\n"
        "   FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);\n"
        "}\n\0";
    ```

2.  **셰이더 객체 생성:** `glCreateShader` 함수를 사용하여 셰이더 객체를 생성한다.

    ```c++
    unsigned int vertexShader = glCreateShader(GL_VERTEX_SHADER);
    unsigned int fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    ```

3.  **소스 코드 첨부 및 컴파일:** `glShaderSource` 함수로 소스 코드를 셰이더 객체에 첨부하고, `glCompileShader` 함수로 셰이더를 컴파일한다.

    ```c++
    glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
    glCompileShader(vertexShader);

    glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
    glCompileShader(fragmentShader);
    ```

4.  **컴파일 성공 여부 확인:** `glGetShaderiv` 함수를 사용하여 컴파일 성공 여부를 확인하고, 오류가 발생했을 경우 `glGetShaderInfoLog` 함수를 사용하여 오류 메시지를 출력한다.

    ```c++
    int success;
    char infoLog[512];
    glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);
    if(!success)
    {
        glGetShaderInfoLog(vertexShader, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" << infoLog << std::endl;
    }

    glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &success);
    if(!success)
    {
        glGetShaderInfoLog(fragmentShader, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n" << infoLog << std::endl;
    }
    ```

### 4. 셰이더 프로그램 링크

컴파일된 셰이더들을 **셰이더 프로그램**에 연결해야 OpenGL에서 렌더링에 사용할 수 있다.

1.  **셰이더 프로그램 객체 생성:** `glCreateProgram` 함수를 사용하여 셰이더 프로그램 객체를 생성한다.

    ```c++
    unsigned int shaderProgram = glCreateProgram();
    ```

2.  **셰이더 첨부 및 링크:** `glAttachShader` 함수로 셰이더들을 프로그램에 첨부하고, `glLinkProgram` 함수로 셰이더들을 연결한다.

    ```c++
    glAttachShader(shaderProgram, vertexShader);
    glAttachShader(shaderProgram, fragmentShader);
    glLinkProgram(shaderProgram);
    ```

3.  **링크 성공 여부 확인:** `glGetProgramiv` 함수를 사용하여 링크 성공 여부를 확인하고, 오류가 발생했을 경우 `glGetProgramInfoLog` 함수를 사용하여 오류 메시지를 출력한다.

    ```c++
    glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
    if (!success) {
        glGetProgramInfoLog(shaderProgram, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER::PROGRAM::LINKING_FAILED\n" << infoLog << std::endl;
    }
    ```

4.  **셰이더 프로그램 활성화:** `glUseProgram` 함수를 사용하여 셰이더 프로그램을 활성화한다.

    ```c++
    glUseProgram(shaderProgram);
    ```

5.  **셰이더 객체 삭제:** 더 이상 필요하지 않은 개별 셰이더 객체를 `glDeleteShader` 함수를 사용하여 삭제한다.

    ```c++
    glDeleteShader(vertexShader);
    glDeleteShader(fragmentShader);
    ```

### 5. 버텍스 데이터와 셰이더 연결

이제 GPU에 정점 데이터를 보내고, 셰이더에서 데이터를 어떻게 처리할지 지정해야 한다. OpenGL에게 데이터를 어떻게 해석하고, 정점 셰이더의 속성들과 어떻게 연결할지 알려주어야 한다.

#### 5.1. 버텍스 속성 연결

정점 셰이더는 입력 데이터를 **버텍스 속성(Vertex Attribute)** 형식으로 받는다. 따라서 입력 데이터가 셰이더의 어느 버텍스 속성으로 연결될지 수동으로 지정해야 한다.

예를 들어, 다음과 같은 정점 데이터를 사용한다고 가정해 보자.

```c++
float vertices[] = {
    0.5f,  0.5f, 0.0f,  // 오른쪽 위
    0.5f, -0.5f, 0.0f,  // 오른쪽 아래
   -0.5f, -0.5f, 0.0f   // 왼쪽 아래
};
```

이 데이터는 다음과 같이 구성된다.

*   위치 데이터는 32비트(4바이트) 부동 소수점 값으로 저장된다.
*   각 위치는 3개의 값(X, Y, Z)으로 구성된다.
*   각 3개의 값 사이에 다른 값이나 공간이 없다. (데이터는 배열 안에서 빽빽하게 정렬되어 있다.)
*   데이터 배열의 첫 번째 값은 버퍼의 시작 부분에 있다.

이 정보를 바탕으로 OpenGL에게 버텍스 데이터를 어떻게 해석할지 지정해야 한다. 이를 위해 `glVertexAttribPointer` 함수를 사용한다.

```c++
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);
```

각 인자의 의미는 다음과 같다.

1.  **`0`**: 설정하려는 버텍스 속성의 번호이다. 셰이더에서 `layout (location = 0)`으로 지정된 위치와 일치해야 한다.
2.  **`3`**: 버텍스 속성의 크기이다. 여기서는 `vec3` 타입이므로 3개의 값으로 구성된다.
3.  **`GL_FLOAT`**: 데이터의 타입이다. 부동 소수점 값이므로 `vec*` 타입을 의미한다.
4.  **`GL_FALSE`**: 데이터를 정규화할지 여부를 지정한다. 부동 소수점 데이터를 사용하므로 `GL_FALSE`로 설정한다.
5.  **`3 * sizeof(float)`**: stride 값으로, 각 버텍스 속성 간의 간격을 나타낸다. 각 속성이 3개의 부동 소수점 값으로 구성되므로 `3 * sizeof(float)`으로 지정한다. 배열이 빽빽하게 정렬되어 있기 때문에 stride를 0으로 설정해도 OpenGL이 자동으로 계산할 수 있다.
6.  **`(void*)0`**: offset으로, 데이터를 배열에서 어디서부터 읽어야 하는지 알려준다. 위치 데이터를 배열의 처음부터 사용하므로 0으로 설정한다.

`glVertexAttribPointer` 함수를 사용하여 버텍스 데이터를 어떻게 해석해야 할지 알려줬으므로, `glEnableVertexAttribArray` 함수를 사용하여 해당 속성을 활성화한다. 기본적으로 버텍스 속성은 비활성화되어 있기 때문에 명시적으로 활성화해야 한다.

#### 5.2. 전체적인 흐름

이제 OpenGL은 어떻게 데이터를 읽고 처리할지 알고 있으며, 다음과 같은 과정으로 객체를 그릴 수 있다.

```c++
// 0. 버퍼에 버텍스 배열 복사
glBindBuffer(GL_ARRAY_BUFFER, VBO);
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

// 1. 버텍스 속성 포인터 설정
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);

// 2. 셰이더 프로그램 사용
glUseProgram(shaderProgram);

// 3. 객체 그리기
someOpenGLFunctionThatDrawsOurTriangle();
```

이 과정을 매번 객체를 그릴 때마다 반복해야 한다. 이 작업은 꽤 번거롭게 보일 수 있다. 만약 5개 이상의 버텍스 속성이나 100개 이상의 객체를 그려야 한다면, 버퍼 객체를 바인딩하고 각 객체의 버텍스 속성을 설정하는 작업은 점점 더 복잡해질 것이다. 이럴 때마다 객체 상태를 하나의 오브젝트로 묶어서 바인딩하여 상태를 복원할 수 있다면 훨씬 더 간편할 것이다. 그래서 VBO와 VAO가 쓰이게 된다.

### 6. VAO (Vertex Array Object)

**Vertex Array Object (VAO)**는 OpenGL에서 버텍스 데이터를 관리하고, 여러 버텍스 속성 설정을 효율적으로 처리할 수 있게 도와주는 객체이다. VAO를 사용하면 복잡한 버텍스 데이터를 다룰 때 코드가 간단해지고, 다양한 객체의 버텍스 속성 설정을 재사용할 수 있다.

#### 6.1. VAO의 역할

VAO는 주로 다음과 같은 정보를 저장한다.

1.  `glEnableVertexAttribArray` 및 `glDisableVertexAttribArray` 호출: 버텍스 속성 배열을 활성화하거나 비활성화한다.
2.  `glVertexAttribPointer` 호출: 버텍스 속성을 어떻게 해석할지 설정하는 함수이다.
3.  버텍스 버퍼 객체(VBO)와 관련된 버텍스 속성: `glVertexAttribPointer`를 통해 VBO를 바인딩하고, 버텍스 속성 데이터를 설정한다.

#### 6.2. VAO의 장점

*   VAO를 사용하면 버텍스 속성 설정을 한 번만 구성하고, 그 후에는 해당 VAO만 바인딩하여 언제든지 설정을 재사용할 수 있다.
*   여러 가지 버텍스 데이터와 속성 구성이 있는 경우, 각 객체에 대해 VAO를 설정하고, 그 후에 VAO만 바인딩하면 해당 객체를 그릴 수 있다. 즉, 속성 구성이 간편해지고 코드가 효율적이다.

#### 6.3. VAO 사용 절차

1.  **VAO 생성:**

    ```c++
    unsigned int VAO;
    glGenVertexArrays(1, &VAO);
    ```

2.  **VAO 바인딩 및 설정:**

    VAO를 바인딩한 후, VBO와 버텍스 속성 포인터를 설정한다.

    ```c++
    // VAO 바인딩
    glBindVertexArray(VAO);

    // VBO 바인딩 및 버텍스 데이터 복사
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

    // 버텍스 속성 포인터 설정
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    ```

3.  **그리기 코드 (렌더링 루프):**

    객체를 그릴 때는 VAO를 바인딩하고 그리기 명령을 호출한다.

    ```c++
    glUseProgram(shaderProgram);
    glBindVertexArray(VAO);
    glDrawArrays(GL_TRIANGLES, 0, 3);
    ```

#### 6.4. VAO 사용의 효과

*   각 객체의 버텍스 속성 설정을 VAO에 저장하여, 나중에 해당 객체를 그릴 때 VAO만 바인딩하면 된다.
*   여러 객체를 그릴 때, 각 객체에 해당하는 VAO를 바인딩하여 그리기 작업을 반복할 수 있다.

#### 6.5. glDrawArrays 함수

*   현재 활성화된 셰이더와 현재 바인딩된 VAO를 기반으로 그래픽 프리미티브(예: 삼각형)를 그린다.

```c++
glDrawArrays(GL_TRIANGLES, 0, 3);
```

*   **`GL_TRIANGLES`**: 그릴 프리미티브 유형을 지정한다. 삼각형을 그리려면 `GL_TRIANGLES`를 사용한다.
*   **`0`**: 그릴 버텍스 배열의 시작 인덱스를 지정한다. 여기서는 0번 인덱스부터 시작한다.
*   **`3`**: 그릴 버텍스의 수이다. 이 예제에서는 3개의 버텍스를 사용하여 삼각형을 그린다.

#### 6.6. VAO 요약

*   VAO는 버텍스 속성 설정을 저장하고, **버텍스 버퍼 객체(VBO)**와 결합하여 효율적인 렌더링을 지원한다.
*   VAO를 사용하면 버텍스 속성 설정을 한 번만 정의하고, 그 후에는 VAO만 바인딩하여 재사용할 수 있어 코드가 간결해지고 관리가 용이하다.

### 7. VBO (Vertex Buffer Object) 심층 이해

VBO는 정점 데이터를 GPU 메모리에 저장하는 역할을 한다. VAO와 함께 사용되어 효율적인 렌더링을 가능하게 한다.

#### 7.1. 정점 데이터 준비

GPU에 보낼 데이터는 그릴 도형의 꼭짓점 정보이다. 예를 들어, 삼각형을 그리려면 세 개의 좌표를 준비한다.

```c++
float vertices[] = {
    0.5f,  0.5f, 0.0f,  // 오른쪽 위
    0.5f, -0.5f, 0.0f,  // 오른쪽 아래
   -0.5f, -0.5f, 0.0f   // 왼쪽 아래
};
```

*   `vertices` 배열은 정점 데이터를 담고 있다.
*   각 정점은 3개의 값(X, Y, Z)으로 이루어져 있다.

#### 7.2. GPU 메모리 공간 생성

정점 데이터를 GPU에 저장하려면 OpenGL에서 **Vertex Buffer Object(VBO)**라는 것을 사용한다.

1.  **VBO 생성:**

    ```c++
    unsigned int VBO;
    glGenBuffers(1, &VBO);
    ```

    `glGenBuffers(1, &VBO)`는 VBO를 1개 생성하고, 생성된 VBO의 ID를 `VBO` 변수에 저장한다.

2.  **VBO 바인딩:**

    생성한 VBO를 활성화하려면 `glBindBuffer`를 사용한다.

    ```c++
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    ```

    `GL_ARRAY_BUFFER`는 버퍼의 종류를 나타낸다. 이후 VBO에 데이터를 저장하거나 설정할 때, 이 바인딩된 VBO를 사용하게 된다.

#### 7.3. 데이터를 GPU로 전송

이제 준비한 `vertices` 데이터를 GPU 메모리에 복사해야 한다. 이 작업은 `glBufferData`를 사용한다.

```c++
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
```

*   **매개변수 설명:**
    *   `GL_ARRAY_BUFFER`: 데이터를 보낼 대상이 VBO임을 나타낸다.
    *   `sizeof(vertices)`: 복사할 데이터의 크기를 바이트 단위로 나타낸다. 여기서는 `vertices` 배열 전체 크기이다.
    *   `vertices`: 복사할 실제 데이터이다.
    *   `GL_STATIC_DRAW`: 데이터가 거의 변하지 않을 것임을 GPU에 알려준다.

#### 7.4. 데이터 관리 방법 설정

`glBufferData`의 마지막 매개변수(GL_STATIC_DRAW)는 GPU가 데이터를 어떻게 관리할지 결정한다.

*   `GL_STATIC_DRAW`: 데이터가 한 번 정의되고 거의 변경되지 않을 때 사용한다.
*   `GL_DYNAMIC_DRAW`: 데이터가 자주 변경될 때 사용한다.
*   `GL_STREAM_DRAW`: 데이터가 매번 그릴 때마다 변경될 경우 사용한다.

삼각형 같은 정적 도형은 데이터가 변하지 않으므로 `GL_STATIC_DRAW`가 적합하다.

#### 7.5. 결과

이제 GPU 메모리에 `vertices` 데이터가 저장되었다. GPU 메모리에 저장된 데이터는 `VBO`라는 객체를 통해 관리된다. 셰이더가 데이터를 사용하여 화면에 도형을 그릴 수 있는 준비가 완료된 상태이다.

#### 7.6. 최종 코드 예제

위 내용을 하나로 정리한 코드는 다음과 같다.

```c++
float vertices[] = {
    0.5f,  0.5f, 0.0f,
    0.5f, -0.5f, 0.0f,
   -0.5f, -0.5f, 0.0f
};

unsigned int VBO;
glGenBuffers(1, &VBO);                     // 1. VBO 생성
glBindBuffer(GL_ARRAY_BUFFER, VBO);        // 2. VBO 바인딩
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW); // 3. 데이터 복사
```

#### 7.7. 핵심 요약

1.  정점 데이터(`vertices`)를 준비한다.
2.  OpenGL에서 VBO를 생성하고(`glGenBuffers`), 활성화한다(`glBindBuffer`).
3.  `glBufferData`로 데이터를 GPU 메모리에 복사한다.
4.  이후 셰이더를 작성해 데이터를 화면에 그린다.

### 8. VAO를 사용한 다중 객체 관리의 이점

**Vertex Array Object (VAO)**는 여러 개의 버텍스 속성이나 객체가 있을 때 발생하는 복잡함을 해결하는 데 매우 유용하다. 여러 객체를 그리거나, 각 객체마다 다양한 버텍스 속성을 설정해야 하는 상황에서 VAO는 상태를 캡슐화하여 상태 관리를 간소화한다.

#### 8.1. 문제 상황

*   여러 개의 버텍스 속성(예: 위치, 색상, 텍스처 좌표 등)을 가진 객체가 많다면, 각 객체를 그릴 때마다 버퍼 객체를 바인딩하고 버텍스 속성 포인터를 설정하는 작업을 반복해야 한다. 이 과정은 점점 번거로워지고 비효율적일 수 있다.
*   예를 들어, 100개 이상의 객체가 있고, 각 객체에 5개 이상의 버텍스 속성이 있다면, 매번 각 객체에 대해 버퍼 객체와 속성 설정을 반복하는 것은 코드가 복잡해지고 비효율적이다.

#### 8.2. 해결책: VAO

VAO는 버텍스 속성 설정과 관련된 모든 상태를 저장하여, 한 번 설정된 후에는 상태를 재사용할 수 있도록 한다. 즉, VAO를 사용하면 매번 객체를 그릴 때마다 각 객체의 속성을 일일이 설정할 필요 없이, 객체 상태를 하나의 오브젝트로 묶어서 간편하게 관리하고 사용할 수 있다.

#### 8.3. VAO로 해결하는 방법

1.  **상태 저장:** VAO는 `glEnableVertexAttribArray`, `glVertexAttribPointer` 호출 등 버텍스 속성을 설정하는 모든 작업을 내부에 저장한다. 한 번 VAO를 생성하고 설정하면, 해당 VAO에 관련된 모든 속성 설정이 저장되어 이후에는 VAO만 바인딩하면 된다.
2.  **한 번의 설정으로 재사용 가능:** 객체를 그릴 때마다 VAO를 재사용할 수 있다. 즉, VAO를 한 번 설정하고, 각 객체를 그릴 때마다 해당 VAO만 바인딩하면, 그 객체의 모든 버텍스 속성 설정이 자동으로 적용된다. 이는 매번 버퍼 객체와 속성 포인터를 일일이 설정하는 번거로움을 해결한다.
3.  **간편한 상태 복원:** VAO는 각 객체에 대해 설정된 버텍스 속성, VBO, 활성화된 버텍스 배열 등의 상태를 저장하고 있기 때문에, VAO를 바인딩하는 것만으로 해당 객체의 상태를 복원할 수 있다.

#### 8.4. 예시

1.  여러 개의 객체를 그려야 할 경우, 각 객체에 대해 별도의 VAO를 설정한다.

    ```c++
    unsigned int VAO1, VAO2;
    glGenVertexArrays(1, &VAO1);
    glGenVertexArrays(1, &VAO2);
    ```

2.  각 VAO에 대해 버텍스 속성 및 VBO 설정을 한 번만 진행한다.

    ```c++
    // VAO1 설정
    glBindVertexArray(VAO1);
    glBindBuffer(GL_ARRAY_BUFFER, VBO1);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    // VAO2 설정
    glBindVertexArray(VAO2);
    glBindBuffer(GL_ARRAY_BUFFER, VBO2);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    ```

3.  이후 객체를 그릴 때는 해당 VAO만 바인딩하면 모든 속성이 자동으로 설정된다.

    ```c++
    // 객체 1 그리기
    glUseProgram(shaderProgram);
    glBindVertexArray(VAO1);
    glDrawArrays(GL_TRIANGLES, 0, 3);

    // 객체 2 그리기
    glUseProgram(shaderProgram);
    glBindVertexArray(VAO2);
    glDrawArrays(GL_TRIANGLES, 0, 3);
    ```

#### 8.5. VAO 사용의 장점

*   **복잡성 감소:** 각 객체마다 버퍼 객체와 속성 포인터를 설정할 필요가 없어서 코드가 간결해진다.
*   **효율성 증가:** VAO를 재사용함으로써 설정된 속성들이 자동으로 적용되므로, 렌더링 루프가 더 빠르고 효율적으로 동작한다.
*   **상태 관리 간소화:** VAO를 바인딩하는 것만으로 객체의 상태를 쉽게 복원할 수 있다.

#### 8.6. 결론

VAO는 여러 객체와 복잡한 버텍스 속성 구성을 관리하는 데 매우 유용하며, 반복적인 설정 작업을 없애고 코드의 효율성을 높인다. 이 방식으로 객체마다 상태를 복원하고, 필요한 설정을 한 번만 지정함으로써 더 간단하고 빠르게 OpenGL 객체를 그릴 수 있다.

### 9. VAO, VBO, 정점 속성 설정의 관계 정리

**Vertex Array Object (VAO)**와 **Vertex Buffer Object (VBO)**는 OpenGL에서 버텍스 데이터를 처리하는 핵심 개념이다.

1.  **VBO (Vertex Buffer Object):**
    *   **목적:** GPU 메모리 상에 실제 버텍스 데이터를 저장하는 객체이다. 버텍스 데이터에는 객체의 정점 정보(위치, 색상, 텍스처 좌표 등)가 포함된다.
    *   **작동:** `glBufferData()`와 같은 함수로 데이터를 GPU 메모리로 복사하여 저장한다.
    *   **연관성:** VBO는 실제 버텍스 데이터를 저장하며, OpenGL은 VBO를 바인딩한 후 데이터를 사용할 수 있다.

2.  **VAO (Vertex Array Object):**
    *   **목적:** VAO는 VBO와 그 VBO를 사용하는 정점 속성(attribute) 설정들을 하나의 상태 객체로 묶어 저장하는 객체이다. VAO는 버텍스 속성(예: 위치, 색상 등)과 그 속성에 해당하는 VBO의 관계를 저장한다.
    *   **작동:** VAO를 바인딩하고, 그 후에 `glVertexAttribPointer`로 버텍스 속성(위치, 색상, 텍스처 좌표 등)을 정의하고, `glEnableVertexAttribArray()`로 이를 활성화한다.
    *   **연관성:** VAO는 VBO와 정점 속성 설정을 연결하여 하나의 객체로 관리할 수 있게 한다. VAO는 이 설정들을 저장하고 있기 때문에, VAO만 바인딩하여 여러 속성을 한 번에 설정할 수 있다.

3.  **정점 속성 설정:**
    *   **목적:** 정점 속성은 VBO에 저장된 데이터를 어떻게 해석할 것인지를 정의한다. 예를 들어, 3D 모델의 각 정점은 위치, 색상, 텍스처 좌표 등을 포함할 수 있다.
    *   **작동:** `glVertexAttribPointer`로 정점 속성의 데이터를 어떻게 해석할지 정의하고, `glEnableVertexAttribArray()`로 해당 속성을 활성화하여 셰이더에서 사용할 수 있게 한다.
    *   **연관성:** 이 설정은 VBO에 저장된 데이터와 VAO에 연결된다. 즉, VBO에 저장된 데이터는 `glVertexAttribPointer`를 통해 정점 속성으로 해석되고, 이 속성은 VAO에 저장된다.

#### 9.1. VAO, VBO, 정점 속성 설정의 관계 정리

1.  **VBO (버텍스 버퍼 객체)**는 GPU 메모리에 실제 데이터를 저장한다. 예를 들어, 정점의 좌표나 색상 같은 데이터를 저장한다.
2.  **VAO (버텍스 배열 객체)**는 이 VBO와 정점 속성 설정을 연결한다. `glVertexAttribPointer`와 `glEnableVertexAttribArray`로 설정한 정점 속성들이 VAO에 저장된다.
3.  정점 속성 설정은 VBO에 저장된 데이터를 어떻게 해석할지 정의하는 과정이다. `glVertexAttribPointer`로 속성(위치, 색상 등)을 정의하고, 이 속성을 VAO에 저장하여 나중에 객체를 그릴 때 효율적으로 사용할 수 있다.

#### 9.2. 코드 예시

```c++
// 1. VBO와 VAO ID생성
unsigned int VBO, VAO;
glGenVertexArrays(1, &VAO);
glGenBuffers(1, &VBO);

// 2. VAO 바인딩
glBindVertexArray(VAO);

// 3. VBO 바인딩 및 데이터 복사
glBindBuffer(GL_ARRAY_BUFFER, VBO);
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

// 4. 정점 속성 설정 (위치)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);  // 위치 속성 활성화

// 5. VBO와 VAO 언바인딩
glBindBuffer(GL_ARRAY_BUFFER, 0);
glBindVertexArray(0);
```

#### 9.3. 코드 설명

1.  VBO는 `vertices` 배열의 데이터를 GPU 메모리로 복사한다.
2.  VAO는 VBO와 속성 설정(`glVertexAttribPointer`, `glEnableVertexAttribArray`)을 연결하여 하나의 객체로 묶는다.
3.  나중에 VAO를 바인딩하면, 설정된 모든 속성과 VBO가 자동으로 준비되므로 객체를 그릴 때 매우 효율적이다.

#### 9.4. 요약

*   VBO는 실제 데이터를 저장하는 객체이다.
*   VAO는 VBO와 정점 속성 설정을 연결하여 하나의 객체로 묶어 관리하는 객체이다.
*   정점 속성 설정은 VBO의 데이터를 어떻게 해석할지를 지정하며, VAO에 저장된다.

### 10. VAO가 VBO와 속성을 묶는 과정 (단계별 설명)

**Vertex Array Object (VAO)**가 **Vertex Buffer Object (VBO)**와 정점 속성 설정을 연결하여 하나의 객체로 묶는 과정을 단계적으로 설명하겠다.

#### 10.1. VAO의 역할

VAO는 정점 속성 설정(예: 위치, 색상, 텍스처 좌표 등)을 VBO와 연결하여 이를 저장하는 OpenGL 객체이다.
VAO를 사용하면 복잡한 정점 데이터를 다룰 때 설정을 한 번만 정의하고 재사용할 수 있다.

*   VAO는 VBO와 **정점 속성 포인터 설정(glVertexAttribPointer)**을 기록한다.
*   이후에는 VAO를 바인딩하기만 하면 관련 설정이 자동으로 적용된다.

#### 10.2. VAO, VBO, 정점 속성의 관계

1.  **VBO:**
    *   정점 데이터를 GPU 메모리에 저장하는 데 사용된다.
    *   예: 정점의 위치 데이터가 담긴 배열.

2.  **정점 속성 설정:**
    *   셰이더에서 사용할 데이터의 구조와 위치를 OpenGL에 알려준다.
    *   예: `glVertexAttribPointer`를 통해 "이 데이터는 위치 정보이며, vec3 타입이다"라고 정의.

3.  **VAO:**
    *   VBO와 정점 속성 설정을 연결하고 관리한다.
    *   VAO를 바인딩하면 해당 설정을 재사용할 수 있다.

#### 10.3. VAO가 VBO와 속성을 묶는 방법

VAO는 다음 두 가지 작업을 저장한다.

1.  **VBO와의 연결 정보:**
    *   어떤 VBO에 데이터가 저장되어 있는지.
2.  **정점 속성 설정 정보:**
    *   `glVertexAttribPointer`로 정의된 속성 설정.

#### 10.4. VAO와 VBO를 연결하는 과정

1.  **VAO 생성 및 바인딩:**

    VAO를 생성하고 바인딩한다. 이 상태에서 설정된 모든 작업이 VAO에 기록된다.

    ```c++
    unsigned int VAO;
    glGenVertexArrays(1, &VAO);
    glBindVertexArray(VAO);
    ```

2.  **VBO 생성 및 데이터 복사:**

    VBO를 생성하고 데이터를 GPU 메모리에 복사한다.

    ```c++
    unsigned int VBO;
    glGenBuffers(1, &VBO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO); // VBO 바인딩
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW); // 데이터 복사
    ```

    이 단계에서 VBO는 VAO와 자동으로 연결된다. VAO는 "GL_ARRAY_BUFFER 타입으로 바인딩된 VBO"를 기록한다.

3.  **정점 속성 설정:**

    정점 데이터를 셰이더와 연결하는 설정을 VAO에 기록한다.

    ```c++
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    ```

    *   `glVertexAttribPointer`: VBO의 데이터를 셰이더의 속성과 연결.
    *   `glEnableVertexAttribArray`: 속성 번호(예: 0번)를 활성화.

4.  **VAO 바인딩 해제:**

    VAO를 바인딩 해제하여 기록 작업을 종료한다.

    ```c++
    glBindVertexArray(0);
    ```

#### 10.5. VAO 사용

이제 VAO를 사용하여 동일한 정점 속성 설정을 재사용할 수 있다.

```c++
// VAO 바인딩
glBindVertexArray(VAO);

// 객체 그리기
glDrawArrays(GL_TRIANGLES, 0, 3);

// VAO 바인딩 해제 (선택 사항)
glBindVertexArray(0);
```

#### 10.6. 전체 코드 예제

```c++
float vertices[] = {
    0.5f,  0.5f, 0.0f,  // 오른쪽 위
    0.5f, -0.5f, 0.0f,  // 오른쪽 아래
   -0.5f, -0.5f, 0.0f   // 왼쪽 아래
};

// VAO와 VBO 생성
unsigned int VAO, VBO;
glGenVertexArrays(1, &VAO);
glGenBuffers(1, &VBO);

// VAO 바인딩
glBindVertexArray(VAO);

// VBO 생성 및 데이터 복사
glBindBuffer(GL_ARRAY_BUFFER, VBO);
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

// 정점 속성 설정
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);

// VAO 바인딩 해제
glBindVertexArray(0);

// ----- 렌더링 루프 -----
while (!windowShouldClose) {
    // VAO 바인딩 및 객체 그리기
    glBindVertexArray(VAO);
    glDrawArrays(GL_TRIANGLES, 0, 3);
    glBindVertexArray(0);
}
```

#### 10.7. VAO의 장점

*   VBO와 정점 속성 설정을 묶어서 저장한다.
*   객체를 그릴 때마다 동일한 설정을 반복하지 않아도 된다.
*   복잡한 정점 데이터를 처리할 때 코드가 간단해지고 오류를 줄인다.

#### 10.8. 비유로 이해하기

*   VBO: 데이터가 저장된 책.
*   정점 속성 설정: 책에서 특정 페이지를 읽는 방법.
*   VAO: 책과 읽는 방법을 함께 기록한 메모지.

VAO를 사용하면 "책을 이렇게 읽어!"라는 규칙을 한 번만 작성하고, 그 메모지만 사용하면 된다.

### 11. 우리가 기다려온 삼각형 (glDrawArrays)

우리가 원하는 객체를 그리기 위해 OpenGL은 `glDrawArrays` 함수를 제공한다. 이 함수는 현재 활성화된 셰이더, 이전에 정의된 정점 속성 설정, 그리고 VAO를 통해 간접적으로 바인딩된 VBO의 정점 데이터를 사용하여 기본 도형을 그린다.

```c++
glUseProgram(shaderProgram);
glBindVertexArray(VAO);
glDrawArrays(GL_TRIANGLES, 0, 3);
```

*   `glDrawArrays` 함수의 첫 번째 인자는 우리가 그리고자 하는 OpenGL 기본 도형의 타입이다. 처음에 우리는 삼각형을 그리고 싶다고 말했으므로, `GL_TRIANGLES`를 전달한다.
*   두 번째 인자는 그릴 정점 배열에서 시작할 인덱스를 지정한다. 우리는 이 값을 0으로 설정한다.
*   마지막 인자는 몇 개의 정점을 그릴 것인지 지정하는데, 이 경우 3개이다(우리의 데이터는 정확히 3개의 정점으로 구성된 하나의 삼각형을 렌더링한다).

이제 코드를 컴파일하고, 오류가 발생하면 그 원인을 찾아가며 수정하십시오. 애플리케이션이 정상적으로 컴파일되면, 결과를 볼 수 있을 것이다.

### 12. EBO (Element Buffer Object)

정점 데이터를 렌더링할 때, 마지막으로 다뤄야 할 개념은 **Element Buffer Object (EBO)**이다. EBO가 어떻게 작동하는지 설명하기 위해 예를 들어 보겠다. 만약 우리가 삼각형 대신 사각형을 그리려고 한다면, 사각형을 두 개의 삼각형으로 나누어 그릴 수 있다(OpenGL은 기본적으로 삼각형을 사용하여 렌더링한다). 이를 통해 다음과 같은 정점 집합을 생성할 수 있다.

```c++
float vertices[] = {
    // 첫 번째 삼각형
     0.5f,  0.5f, 0.0f,  // 오른쪽 위
     0.5f, -0.5f, 0.0f,  // 오른쪽 아래
    -0.5f,  0.5f, 0.0f,  // 왼쪽 위
    // 두 번째 삼각형
     0.5f, -0.5f, 0.0f,  // 오른쪽 아래
    -0.5f, -0.5f, 0.0f,  // 왼쪽 아래
    -0.5f,  0.5f, 0.0f   // 왼쪽 위
};
```

보시다시피, 일부 정점이 겹치고 있다. 예를 들어, "오른쪽 아래"와 "왼쪽 위"는 두 번씩 사용된다! 이는 50%의 오버헤드를 발생시키며, 더 복잡한 모델에서 삼각형이 수천 개 이상일 경우 이 문제가 심각해진다. 더 나은 해결책은 고유한 정점만 저장하고, 그 정점들을 그릴 순서를 지정하는 것이다. 이렇게 하면 사각형을 그리기 위해 6개의 정점이 아닌 4개의 정점만 저장하면 된다. OpenGL이 이런 기능을 제공해주면 좋겠죠?

#### 12.1. EBO의 역할

**Element Buffer Object (EBO)**는 바로 이러한 문제를 해결한다. EBO는 정점 버퍼 객체(VBO)와 유사하게 작동하는 버퍼로, OpenGL이 어떤 정점을 그릴지 결정하는 데 사용하는 인덱스를 저장한다. 이를 "인덱스 드로잉"이라고 하며, 우리가 원하는 솔루션이다. 이제 사각형을 그리기 위해 고유한 정점과 그 정점을 그릴 순서를 지정하는 인덱스를 설정해 보겠다.

```c++
float vertices[] = {
     0.5f,  0.5f, 0.0f,  // 오른쪽 위
     0.5f, -0.5f, 0.0f,  // 오른쪽 아래
    -0.5f, -0.5f, 0.0f,  // 왼쪽 아래
    -0.5f,  0.5f, 0.0f   // 왼쪽 위
};
unsigned int indices[] = {  // 인덱스는 0부터 시작!
    0, 1, 3,   // 첫 번째 삼각형
    1, 2, 3    // 두 번째 삼각형
};
```
만일 이렇게 하지 않는다면 2개의 삼각형을 만들어야 하므로 vertices2 까지 만들어야 했을 것이다.

이제 인덱스를 사용하면, 6개 대신 4개의 정점만 필요하다. 그럼 EBO를 생성해 보겠다.

```c++
unsigned int EBO;
glGenBuffers(1, &EBO);
```

VBO와 마찬가지로 EBO를 바인딩하고, 인덱스를 버퍼에 복사한다. 이번에는 `GL_ELEMENT_ARRAY_BUFFER`를 버퍼 타입으로 지정하는데, 이는 EBO에 해당한다.

```c++
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
```

이제 `glDrawArrays` 대신 `glDrawElements`를 사용하여 인덱스 버퍼에서 삼각형을 렌더링한다.

```c++
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
```

이 함수에서 첫 번째 인자는 그릴 모드를 지정하고, 두 번째 인자는 그릴 요소의 개수이다. 우리는 6개의 인덱스를 사용하므로, 6개의 정점을 그리기를 원한다. 세 번째 인자는 인덱스의 타입을 지정하며, 네 번째 인자는 EBO에서의 오프셋을 지정한다. 여기서는 0으로 설정한다.

#### 12.2. EBO와 VAO의 관계

`glDrawElements` 함수는 현재 바인딩된 `GL_ELEMENT_ARRAY_BUFFER`에서 인덱스를 가져와서 그리기 때문에, 매번 객체를 렌더링할 때마다 해당 EBO를 바인딩해야 한다. 그러나 VAO가 EBO 바인딩을 추적하므로, VAO를 바인딩하면 자동으로 EBO가 바인딩된다.

#### 12.3. 최종 초기화 및 드로잉 코드

이제 최종 초기화 및 드로잉 코드는 다음과 같다.

```c++
// ..:: 초기화 코드 :: ..
// 1. VAO 바인딩
glBindVertexArray(VAO);
// 2. VBO에 정점 배열 복사
glBindBuffer(GL_ARRAY_BUFFER, VBO);
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
// 3. EBO에 인덱스 배열 복사
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
// 4. 정점 속성 포인터 설정
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);

// ..:: 드로잉 코드 (렌더 루프) :: ..
glUseProgram(shaderProgram);
glBindVertexArray(VAO);
glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
glBindVertexArray(0);
```

프로그램을 실행하면 왼쪽에는 우리가 만든 삼각형이 보이고, 오른쪽에는 와이어프레임 모드로 그려진 사각형이 나타날 것이다. 와이어프레임 모드에서는 사각형이 두 개의 삼각형으로 이루어져 있음을 확인할 수 있다.

(EBO를 사용해도 `glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0)` 호출에서 여전히 6개의 정점을 사용하여 삼각형을 그린다. 하지만, 이 정점들은 실제로 중복되지 않은 4개의 정점(`vertices` 배열)에서 참조된다. 이로써 데이터 중복을 방지하면서도 정확히 6개의 점을 사용해 삼각형을 그리는 것이다.)

와이어프레임 모드에서 그리려면 `glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)`을 사용한다. 이 설정은 이후 그려지는 삼각형들을 와이어프레임 모드로 렌더링한다. 기본값으로 되돌리려면 `glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)`을 사용한다.

#### 12.4. EBO 요약

**Element Buffer Object (EBO)**는 인덱스를 사용해 정점을 효율적으로 그리기 위해 사용된다. EBO를 생성하는 코드는 VBO 및 VAO와 유사하지만, 추가적으로 인덱스 데이터를 GPU 메모리에 전달한다.

#### 12.5. EBO를 포함한 전체 코드 예시

```c++
// 1. VBO, VAO, EBO 생성
unsigned int VBO, VAO, EBO;
glGenVertexArrays(1, &VAO);
glGenBuffers(1, &VBO);
glGenBuffers(1, &EBO);

// 2. VAO 바인딩
glBindVertexArray(VAO);

// 3. VBO 바인딩 및 데이터 복사
glBindBuffer(GL_ARRAY_BUFFER, VBO);
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

// 4. EBO 바인딩 및 데이터 복사
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);

// 5. 정점 속성 설정 (위치)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);  // 위치 속성 활성화

// 6. VAO 언바인딩
glBindVertexArray(0);

// 7. VBO 언바인딩 (선택 사항)
// glBindBuffer(GL_ARRAY_BUFFER, 0);
// glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0); // EBO는 VAO와 함께 바인딩되므로 언바인딩 불필요

// --- 드로잉 ---
// 셰이더 프로그램 사용
glUseProgram(shaderProgram);

// VAO 바인딩
glBindVertexArray(VAO);

// 인덱스를 사용해 그리기
glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);

// VAO 언바인딩
glBindVertexArray(0);
```

#### 12.6. EBO 사용 효과

*   EBO를 통해 동일한 정점을 중복해서 저장하지 않아 메모리 사용량을 줄이고 성능을 향상시킬 수 있다.

축하한다! 삼각형이나 사각형을 그리는 데 성공했다면, 현대 OpenGL의 첫 번째 장벽을 넘어선 것이다. 이제 이후의 장들이 훨씬 더 쉽게 이해될 것이다.

### 13. 핵심 정리: 삼각형 그리기를 위한 3가지 요소

그래픽스 파이프라인에서 삼각형을 그리기 위한 과정은 다음과 같은 3가지 핵심 요소로 요약할 수 있다.

1.  **GPU에 데이터를 저장할 메모리 (VBO, EBO):**
    *   VBO (Vertex Buffer Object): GPU에 정점 데이터를 저장하는 데 사용된다. 정점 데이터는 3D 모델의 위치 정보나 색상 정보 등을 포함할 수 있다.
    *   EBO (Element Buffer Object): 인덱스 데이터를 저장하는 데 사용된다. 여러 정점이 반복될 경우 인덱스를 통해 재사용하는 방식이다.
    *   이 데이터를 GPU 메모리에 할당하여 저장한다. 이 작업은 `glGenBuffers`와 `glBindBuffer`로 처리된다.

2.  **셰이더 프로그램 (버텍스 셰이더, 프래그먼트 셰이더):**
    *   버텍스 셰이더는 각 정점의 변환을 처리한다. 예를 들어, 모델을 화면에 그리기 위한 좌표 변환(모델, 뷰, 프로젝션 변환)을 수행한다.
    *   프래그먼트 셰이더는 픽셀 색상 계산을 담당한다. 각 픽셀에 대한 색상, 텍스처 등을 계산한다.
    *   이 셰이더 프로그램은 컴파일 후 링크하여 사용해야 하며, `glUseProgram` 함수로 활성화해야 한다.

3.  **데이터와 셰이더 프로그램을 연결하는 과정:**
    *   버텍스 속성 연결: `glVertexAttribPointer`와 `glEnableVertexAttribArray`를 사용하여 VBO에 저장된 데이터를 셰이더의 입력으로 연결한다.
    *   예를 들어, 위치 데이터는 버텍스 셰이더의 첫 번째 입력(`layout(location = 0)`)에 연결된다.
    *   셰이더 프로그램 사용: 데이터를 처리할 셰이더 프로그램을 활성화한 후, 데이터를 셰이더와 연결하여 GPU에서 렌더링이 가능하게 한다.

#### 13.1. 전체 과정

1.  **버퍼 생성 및 데이터 전송:**
    *   VBO와 EBO를 생성하고, 데이터를 GPU 메모리에 전송한다.
2.  **셰이더 프로그램 준비 및 활성화:**
    *   버텍스 셰이더와 프래그먼트 셰이더를 준비하고, 이를 하나의 프로그램으로 링크하여 활성화한다.
3.  **버텍스 속성 연결 및 데이터 렌더링:**
    *   셰이더 프로그램에 데이터를 연결하고, 렌더링을 위해 `glDrawArrays` 또는 `glDrawElements` 함수를 호출하여 그린다.

#### 13.2. 정리

그래픽 파이프라인에서 삼각형을 그리기 위해서는 GPU 메모리에 데이터를 저장하고, 셰이더 프로그램을 활성화하며, 버텍스 속성을 셰이더와 연결하는 과정이 필요하다. 이 세 가지 조건을 통해 OpenGL이 데이터를 처리하고 화면에 객체를 그릴 수 있게 된다.



