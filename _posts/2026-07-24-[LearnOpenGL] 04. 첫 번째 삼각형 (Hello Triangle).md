---
title: "[LearnOpenGL] 04. 첫 번째 삼각형 (Hello Triangle)"
date: 2026-07-24 18:10:33 +0900
categories: [Graphics, LearnOpenGL]
tags: [opengl, cpp, graphics, translation, vertex-shader, fragment-shader, vao, vbo, ebo]
---

> 📢 **안내 및 출처 표기 (Attribution)**
> * 본 포스팅은 Joey de Vries가 작성한 튜토리얼 **[LearnOpenGL.com](https://learnopengl.com/Getting-started/Hello-Triangle)**의 원문을 바탕으로 한 한국어 번역 및 학습 정리입니다.
> * 원문 저작권은 **Joey de Vries**에게 있으며, **CC BY-NC 4.0** 라이선스를 준수합니다. 원문: [https://learnopengl.com/Getting-started/Hello-Triangle](https://learnopengl.com/Getting-started/Hello-Triangle)
> 
> 



OpenGL에서 모든 것은 3D 공간에 존재하지만, 화면이나 창은 2D 픽셀 배열입니다. 따라서 OpenGL 작업의 상당 부분은 모든 3D 좌표를 화면에 맞는 2D 픽셀로 변환하는 것과 관련이 있습니다. 3D 좌표를 2D 픽셀로 변환하는 프로세스는 OpenGL의 그래픽스 파이프라인(graphics pipeline)에 의해 관리됩니다. 그래픽스 파이프라인은 두 가지 큰 부분으로 나누어집니다. 첫 번째 파이프라인은 3D 좌표를 2D 좌표로 변환하고, 두 번째 파이프라인은 2D 좌표를 실제 색상이 지정된 픽셀로 변환합니다. 이번 장에서는 그래픽스 파이프라인에 대해 간략히 논의하고, 이를 활용해 멋진 픽셀을 생성하는 방법을 알아보겠습니다.

그래픽스 파이프라인은 3D 좌표 세트를 입력받아 화면의 색상 지정된 2D 픽셀로 변환합니다. 그래픽스 파이프라인은 여러 단계로 나누어지며, 각 단계는 이전 단계의 출력을 입력으로 사용합니다. 이 모든 단계는 매우 특화되어 있으며(하나의 특정 기능만 수행) 병렬로 쉽게 실행될 수 있습니다. 병렬 특성 때문에 오늘날의 그래픽 카드는 그래픽스 파이프라인 내에서 데이터를 빠르게 처리할 수 있는 수천 개의 작은 처리 코어를 가지고 있습니다. 이 처리 코어들은 파이프라인의 각 단계를 위해 GPU에서 작동하는 작은 프로그램을 실행하며, 이러한 작은 프로그램을 셰이더(shader)라고 부릅니다.

이러한 셰이더 중 일부는 개발자가 직접 구성할 수 있으므로 기본 셰이더를 대체할 자신만의 셰이더를 작성할 수 있습니다. 이를 통해 파이프라인의 특정 부분에 대한 훨씬 더 정교한 제어가 가능하며 GPU에서 실행되기 때문에 귀중한 CPU 시간을 절약할 수 있습니다. 셰이더는 GLSL(OpenGL Shading Language)로 작성되며 다음 장에서 자세히 다룰 예정입니다.

아래는 그래픽스 파이프라인의 모든 단계를 추상화하여 표현한 이미지입니다. 파란색 섹션은 자신만의 셰이더를 주입할 수 있는 단계를 나타냅니다.

![렌더링 파이프라인](https://learnopengl.com/img/getting-started/pipeline.png)

보시다시피 그래픽스 파이프라인에는 버텍스 데이터를 완전히 렌더링된 픽셀로 변환하는 각 특정 단계를 처리하는 수많은 섹션이 포함되어 있습니다. 파이프라인이 어떻게 작동하는지 잘 이해할 수 있도록 간략하게 설명하겠습니다.

그래픽스 파이프라인의 입력으로 삼각형을 형성하는 3D 좌표 목록을 전달합니다. 이를 버텍스 데이터(Vertex Data)라고 하며, 버텍스의 집합입니다. 버텍스(vertex)는 3D 좌표당 데이터의 집합을 의미합니다. 이 버텍스 데이터는 버텍스 속성(vertex attribute)을 사용하여 표현되며 원하는 모든 데이터를 포함할 수 있지만, 이해를 돕기 위해 각 버텍스가 3D 위치와 색상 값으로만 구성되어 있다고 가정하겠습니다.

OpenGL이 좌표 및 색상 값의 모음을 어떻게 처리할지 알기 위해서는 데이터를 사용하여 어떤 종류의 렌더링 유형을 형성할지 힌트를 주어야 합니다. 데이터를 점의 집합으로 렌더링할지, 삼각형의 집합으로 렌더링할지, 아니면 하나의 긴 선으로 렌더링할지 알려주어야 합니다. 이러한 힌트를 프리미티브(primitives)라고 하며 드로잉 명령을 호출할 때 OpenGL에 제공됩니다. 이 중 일부 힌트는 `GL_POINTS`, `GL_TRIANGLES`, `GL_LINE_STRIP` 등이 있습니다.

파이프라인의 첫 번째 부분은 단일 버텍스를 입력으로 받는 버텍스 셰이더(vertex shader)입니다. 버텍스 셰이더의 주 목적은 3D 좌표를 다른 3D 좌표로 변환하는 것이며, 버텍스 속성에 대한 몇 가지 기본 처리를 수행할 수 있도록 해줍니다.

버텍스 셰이더 단계의 출력은 선택적으로 지오메트리 셰이더(geometry shader)로 전달됩니다. 지오메트리 셰이더는 프리미티브를 형성하는 버텍스 집합을 입력으로 받으며, 새로운 버텍스를 내보내어 다른 형상을 생성할 수 있는 능력이 있습니다. 이 예시에서는 주어진 형상에서 두 번째 삼각형을 생성합니다.

**프리미티브 조립(primitive assembly)** 단계는 버텍스(또는 지오메트리) 셰이더로부터 하나 이상의 프리미티브를 형성하는 모든 버텍스를 입력으로 받아 지정된 프리미티브 모양으로 모든 점을 조립합니다. (이 경우 두 개의 삼각형이 됩니다.)

프리미티브 조립 단계의 출력은 래스터화 단계(rasterization stage)로 전달되어 결과 프리미티브를 최종 화면의 해당 픽셀에 매핑하여 프래그먼트(fragment)를 생성합니다. 프래그먼트 셰이더가 실행되기 전에 클리핑(clipping)이 수행됩니다. 클리핑은 시야 밖에 있는 모든 프래그먼트를 버려 성능을 향상시킵니다.

> **입문자 참고**
> OpenGL에서 **프래그먼트(fragment)**란 OpenGL이 단일 픽셀을 렌더링하는 데 필요한 모든 데이터를 의미합니다.

프래그먼트 셰이더(fragment shader)의 주 목적은 픽셀의 최종 색상을 계산하는 것이며 일반적으로 이 단계에서 모든 고급 OpenGL 효과가 발생합니다. 일반적으로 프래그먼트 셰이더에는 최종 픽셀 색상을 계산하는 데 사용할 수 있는 3D 씬에 대한 데이터(조명, 그림자, 광원 색상 등)가 포함됩니다.

모든 해당하는 색상 값이 결정된 후 최종 개체는 **알파 테스트 및 블렌딩(alpha test and blending)** 단계를 거치게 됩니다. 이 단계는 프래그먼트의 깊이(depth) 및 스텐실(stencil) 값을 확인하여 결과 프래그먼트가 다른 개체보다 앞에 있는지 뒤에 있는지 확인하고 필요한 경우 버립니다. 또한 알파 값(투명도)을 확인하고 개체를 블렌딩합니다. 따라서 프래그먼트 셰이더에서 계산된 픽셀 출력 색상이 최종 픽셀 색상과 완전히 달라질 수 있습니다.

그래픽스 파이프라인은 복잡한 전체이며 구성을 변경할 수 있는 파트가 많습니다. 하지만 거의 모든 경우에 버텍스 셰이더와 프래그먼트 셰이더만 작업하면 됩니다. 지오메트리 셰이더는 선택 사항이며 기본 셰이더로 두는 경우가 많습니다.

모던 OpenGL에서는 적어도 사용자 지정 버텍스 셰이더와 프래그먼트 셰이더를 정의해야 합니다. (GPU에 기본 버텍스/프래그먼트 셰이더가 없습니다.) 그렇기 때문에 첫 번째 삼각형을 렌더링하기 전까지 상당한 양의 지식이 필요하여 초기 진입 장벽이 다소 높은 편입니다.

---

## 버텍스 입력 (Vertex input)

무언가를 그리기 위해 먼저 OpenGL에 버텍스 데이터를 전달해야 합니다. OpenGL은 3D 그래픽 라이브러리이므로 모든 좌표는 3D($x$, $y$, $z$) 좌표입니다. OpenGL은 모든 3D 좌표를 화면으로 변환하지 않으며, 3D 좌표가 3개의 축 모두에서 -1.0과 1.0 사이의 특정 범위에 있을 때만 처리합니다. 이 범위 내의 모든 좌표를 정규화된 기기 좌표(NDC; Normalized Device Coordinates)라고 하며 화면에 표시됩니다.

단일 삼각형을 렌더링하기 위해 각 버텍스가 3D 위치를 갖는 총 3개의 버텍스를 지정합니다. 이를 float 배열의 정규화된 기기 좌표로 정의합니다.

```cpp
float vertices[] = {
    -0.5f, -0.5f, 0.0f, // 좌측 하단
     0.5f, -0.5f, 0.0f, // 우측 하단
     0.0f,  0.5f, 0.0f  // 중앙 상단
};

```

OpenGL은 3D 공간에서 작업하므로 $z$ 좌표가 `0.0`인 2D 삼각형을 렌더링합니다. 이렇게 하면 삼각형의 깊이가 동일하게 유지되어 2D처럼 보입니다.

### 정규화된 기기 좌표 (NDC)

버텍스 좌표가 버텍스 셰이더에서 처리되면 $x$, $y$, $z$ 값이 -1.0에서 1.0까지 변하는 영역인 정규화된 기기 좌표에 있어야 합니다. 이 범위를 벗어난 모든 좌표는 버려지거나(clipping) 화면에 표시되지 않습니다.

![](https://learnopengl.com/img/getting-started/ndc.png)

일반적인 화면 좌표와 달리 양의 $y$축은 위쪽 방향을 가리키며 $(0,0)$ 좌표는 좌측 상단이 아닌 중앙에 위치합니다.

NDC 좌표는 `glViewport`로 제공한 데이터를 사용해 뷰포트 변환을 통해 화면 공간 좌표(screen-space coordinates)로 변환됩니다. 그런 다음 프래그먼트 셰이더의 입력으로 전달됩니다.

버텍스 데이터가 정의되었으므로 파이프라인의 첫 번째 프로세스인 버텍스 셰이더의 입력으로 전달해야 합니다. 이는 버텍스 데이터를 저장할 메모리를 GPU에 생성하고, OpenGL이 메모리를 해석하는 방법을 구성하며, 데이터를 그래픽 카드로 전송하는 방법을 지정함으로써 수행됩니다.

메모리는 GPU의 메모리에 다량의 버텍스를 저장할 수 있는 버텍스 버퍼 오프젝트(VBO; Vertex Buffer Object)를 통해 관리됩니다. 이러한 버퍼 오프젝트를 사용하는 이점은 데이터를 하나씩 보내지 않고 한 번에 대량의 데이터를 그래픽 카드로 전송하고 메모리가 남아있다면 유지할 수 있다는 것입니다. CPU에서 그래픽 카드로 데이터를 전송하는 것은 상대적으로 느리기 때문에 가능한 한 한 번에 전송해야 합니다. 데이터가 GPU 메모리에 들어가면 버텍스 셰이더는 매우 빠르게 접근할 수 있습니다.

VBO는 고유한 ID를 가지며 `glGenBuffers` 함수를 통해 생성할 수 있습니다.

```cpp
unsigned int VBO;
glGenBuffers(1, &VBO);

```

VBO의 버퍼 유형은 `GL_ARRAY_BUFFER`입니다. OpenGL은 다른 버퍼 유형인 경우 여러 버퍼를 동시에 바인딩할 수 있습니다. `glBindBuffer` 함수를 사용하여 버퍼를 `GL_ARRAY_BUFFER` 타깃에 바인딩할 수 있습니다.

```cpp
glBindBuffer(GL_ARRAY_BUFFER, VBO);

```

이후 만드는 모든 버퍼 호출(`GL_ARRAY_BUFFER` 타깃에 대한)은 현재 바인딩된 버퍼인 `VBO`를 구성하는 데 사용됩니다. 그런 다음 `glBufferData` 함수를 호출하여 이전에 정의한 버텍스 데이터를 버퍼 메모리로 복사합니다.

```cpp
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

```

`glBufferData`는 사용자 정의 데이터를 바인딩된 버퍼로 복사하도록 전용된 함수입니다.

* 첫 번째 인자는 데이터를 복사할 버퍼의 유형입니다.
* 두 번째 인자는 전달할 데이터의 크기(바이트 단위)입니다.
* 세 번째 인자는 보내려는 실제 데이터입니다.
* 네 번째 인자는 그래픽 카드가 데이터를 관리하는 방식을 지정합니다.
* `GL_STREAM_DRAW`: 데이터가 한 번만 설정되고 GPU에서 수차례만 사용됩니다.
* `GL_STATIC_DRAW`: 데이터가 한 번만 설정되고 여러 번 사용됩니다.
* `GL_DYNAMIC_DRAW`: 데이터가 자주 변경되고 여러 번 사용됩니다.



삼각형의 위치 데이터는 변경되지 않고 렌더링 호출 시 매번 사용되므로 `GL_STATIC_DRAW`가 가장 적합합니다.

---

## 버텍스 셰이더 (Vertex shader)

버텍스 셰이더는 프로그래밍 가능한 셰이더 중 하나입니다. 모던 OpenGL에서는 무언가를 렌더링하려면 최소한 버텍스 및 프래그먼트 셰이더를 설정해야 합니다.

가장 먼저 할 일은 GLSL로 버텍스 셰이더를 작성하고 컴파일하는 것입니다. 아래는 아주 기본적인 버텍스 셰이더 소스 코드입니다.

```glsl
#version 330 core
layout (location = 0) in vec3 aPos;

void main()
{
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}

```

각 셰이더는 버전을 선언하며 시작합니다. OpenGL 3.3 이상부터 GLSL 버전 번호는 OpenGL 버전과 일치합니다. 또한 코어 프로파일(core profile) 기능을 사용하고 있음을 명시합니다.

다음으로 `in` 키워드를 사용해 입력을 받습니다. GLSL에는 1~4개의 float을 포함하는 벡터 데이터 유형이 있습니다. 각 버텍스에 3D 좌표가 있으므로 이름이 `aPos`인 `vec3` 입력 변수를 만듭니다. 또한 `layout (location = 0)`을 통해 입력 변수의 위치(location)를 지정합니다.

출력을 설정하기 위해 사전 정의된 `gl_Position` 변수에 위치 데이터를 할당해야 합니다. `gl_Position`은 내부적으로 `vec4`이므로 `vec3` 입력을 `vec4` 생성자에 넣어 변환하고 $w$ 구성 요소를 `1.0f`로 설정합니다.

---

## 셰이더 컴파일 (Compiling a shader)

버텍스 셰이더 소스 코드를 C 문자열로 저장합니다.

```cpp
const char *vertexShaderSource = "#version 330 core\n"
    "layout (location = 0) in vec3 aPos;\n"
    "void main()\n"
    "{\n"
    "   gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);\n"
    "}\0";

```

OpenGL이 셰이더를 사용하려면 런타임에 소스 코드로부터 동적으로 컴파일해야 합니다. 먼저 `glCreateShader`로 셰이더 객체를 생성합니다.

```cpp
unsigned int vertexShader;
vertexShader = glCreateShader(GL_VERTEX_SHADER);

```

생성할 셰이더 유형으로 `GL_VERTEX_SHADER`를 전달합니다. 그런 다음 소스 코드를 셰이더 객체에 연결하고 컴파일합니다.

```cpp
glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
glCompileShader(vertexShader);

```

컴파일 오류 발생 여부를 확인하기 위해 다음과 같은 코드를 사용할 수 있습니다.

```cpp
int success;
char infoLog[512];
glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);

if (!success)
{
    glGetShaderInfoLog(vertexShader, 512, NULL, infoLog);
    std::cout << "ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" << infoLog << std::endl;
}

```

---

## 프래그먼트 셰이더 (Fragment shader)

프래그먼트 셰이더는 픽셀의 색상 출력을 계산합니다. 간단한 예제를 위해 프래그먼트 셰이더는 항상 주황색 계열의 색상을 출력하도록 작성합니다.

컴퓨터 그래픽의 색상은 빨강, 초록, 파랑, 알파(투명도) 4개 구성 요소(RGBA)로 표현되며 각 값은 0.0에서 1.0 사이로 설정합니다.

```glsl
#version 330 core
out vec4 FragColor;

void main()
{
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}

```

`out` 키워드로 출력 변수인 `FragColor`를 선언하고 주황색 값(`vec4(1.0f, 0.5f, 0.2f, 1.0f)`)을 할당합니다.

프래그먼트 셰이더를 컴파일하는 프로세스는 버텍스 셰이더와 비슷하지만 `GL_FRAGMENT_SHADER` 상수를 사용합니다.

```cpp
unsigned int fragmentShader;
fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
glCompileShader(fragmentShader);

```

---

## 셰이더 프로그램 (Shader program)

컴파일된 셰이더들을 렌더링에 사용하기 위해 하나의 셰이더 프로그램 객체(shader program object)로 연결(linking)해야 합니다.

```cpp
unsigned int shaderProgram;
shaderProgram = glCreateProgram();

glAttachShader(shaderProgram, vertexShader);
glAttachShader(shaderProgram, fragmentShader);
glLinkProgram(shaderProgram);

```

링킹 성공 여부도 `glGetProgramiv` 및 `glGetProgramInfoLog`로 확인할 수 있습니다.

```cpp
glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
if (!success) {
    glGetProgramInfoLog(shaderProgram, 512, NULL, infoLog);
    std::cout << "ERROR::SHADER::PROGRAM::LINKING_FAILED\n" << infoLog << std::endl;
}

```

결과로 얻은 프로그램 객체는 `glUseProgram`을 호출하여 활성화합니다.

```cpp
glUseProgram(shaderProgram);

```

프로그램 객체에 셰이더를 링킹한 후에는 더 이상 필요하지 않은 셰이더 객체를 삭제합니다.

```cpp
glDeleteShader(vertexShader);
glDeleteShader(fragmentShader);

```

---

## 버텍스 속성 연결하기 (Linking Vertex Attributes)

OpenGL은 메모리의 버텍스 데이터를 어떻게 해석하고 버텍스 셰이더의 속성에 연결해야 하는지 모르기 때문에 수동으로 지정해주어야 합니다.

버텍스 버퍼 데이터 포맷 구조:
![](https://learnopengl.com/img/getting-started/vertex_attribute_pointer.png)
* 위치 데이터는 32비트(4바이트) 부동 소수점 값으로 저장됩니다.
* 각 위치는 3개의 값으로 구성됩니다.
* 값 사이에 공백 없이 조밀하게 패킹되어 있습니다.
* 데이터의 첫 번째 값은 버퍼의 시작점에 있습니다.

`glVertexAttribPointer`를 사용해 데이터 해석 방법을 지정할 수 있습니다.

```cpp
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);

```

`glVertexAttribPointer` 매개변수 설명:

1. `0`: 구성할 버텍스 속성을 지정합니다. (`layout (location = 0)`에 지정한 값)
2. `3`: 버텍스 속성의 크기입니다. (`vec3`이므로 3)
3. `GL_FLOAT`: 데이터의 타입입니다.
4. `GL_FALSE`: 데이터 정규화(normalization) 여부입니다.
5. `3 * sizeof(float)`: 보폭(**stride**)으로, 연속적인 버텍스 속성 신호 사이의 간격입니다.
6. `(void*)0`: 오프셋(**offset**)으로, 버퍼에서 위치 데이터가 시작하는 지점입니다.

`glEnableVertexAttribArray(0)`을 호출하여 버텍스 속성을 활성화합니다.

---

## 버텍스 어레이 오브젝트 (VAO; Vertex Array Object)

버텍스 어레이 오브젝트(VAO)는 VBO처럼 바인딩될 수 있으며, 이후 수행되는 모든 버텍스 속성 설정이 VAO 내에 저장됩니다. 이렇게 하면 설정 호출을 한 번만 수행하고 필요할 때 해당 VAO만 바인딩하여 사용할 수 있습니다.

> **입문자 참고**
> 코어 프로파일 OpenGL에서는 VAO 사용이 **필수**입니다. VAO를 바인딩하지 않으면 OpenGL이 아무것도 그리지 않을 수 있습니다.

VAO가 저장하는 상태:

* `glEnableVertexAttribArray` 또는 `glDisableVertexAttribArray` 호출
* `glVertexAttribPointer`를 통한 버텍스 속성 구성
* `glVertexAttribPointer` 호출에 의해 연결된 버텍스 버퍼 오프젝트(VBO)
![](https://learnopengl.com/img/getting-started/vertex_array_objects.png)

VAO 생성 및 초기화 예시 코드:

```cpp
// 1. VAO 바인딩
unsigned int VAO;
glGenVertexArrays(1, &VAO);
glBindVertexArray(VAO);

// 2. VBO 설정
glBindBuffer(GL_ARRAY_BUFFER, VBO);
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

// 3. 버텍스 속성 포인터 설정
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);

```

그리기 코드:

```cpp
glUseProgram(shaderProgram);
glBindVertexArray(VAO);
someOpenGLFunctionThatDrawsOurTriangle();

```

---

## 첫 번째 삼각형을 그리며 (The triangle we've all been waiting for)

물체를 그리기 위해 `glDrawArrays` 함수를 사용합니다.

```cpp
glUseProgram(shaderProgram);
glBindVertexArray(VAO);
glDrawArrays(GL_TRIANGLES, 0, 3);

```

`glDrawArrays` 매개변수:

* 첫 번째 인자: 그릴 OpenGL 프리미티브 유형 (`GL_TRIANGLES`)
* 두 번째 인자: 그리기 시작할 버텍스 배열의 시작 인덱스 (`0`)
* 세 번째 인자: 그릴 버텍스의 개수 (`3`)

성공적으로 컴파일하고 실행하면 다음과 같은 주황색 삼각형이 출력됩니다.

전체 소스 코드는 [LearnOpenGL Code Repository](https://learnopengl.com/code_viewer_gh.php?code=src/1.getting_started/2.1.hello_triangle/hello_triangle.cpp)에서 찾을 수 있습니다.

---

## 엘리먼트 버퍼 오브젝트 (EBO; Element Buffer Objects)

사각형을 그리기 위해 두 개의 삼각형을 사용하는 경우를 예로 들어보겠습니다.

```cpp
float vertices[] = {
    // 첫 번째 삼각형
     0.5f,  0.5f, 0.0f,  // 우측 상단
     0.5f, -0.5f, 0.0f,  // 우측 하단
    -0.5f,  0.5f, 0.0f,  // 좌측 상단
    // 두 번째 삼각형
     0.5f, -0.5f, 0.0f,  // 우측 하단
    -0.5f, -0.5f, 0.0f,  // 좌측 하단
    -0.5f,  0.5f, 0.0f   // 좌측 상단
};

```

우측 하단과 좌측 상단 버텍스가 중복 정의되어 있습니다. 50%의 오버헤드가 발생합니다. 중복 없이 고유한 버텍스만 저장하고 그리는 순서를 지정하는 방식이 인덱스 드로잉(indexed drawing)이며, 이를 가능하게 해주는 것이 엘리먼트 버퍼 오브젝트(EBO)입니다.

```cpp
float vertices[] = {
     0.5f,  0.5f, 0.0f,  // 우측 상단
     0.5f, -0.5f, 0.0f,  // 우측 하단
    -0.5f, -0.5f, 0.0f,  // 좌측 하단
    -0.5f,  0.5f, 0.0f   // 좌측 상단
};

unsigned int indices[] = {
    0, 1, 3, // 첫 번째 삼각형
    1, 2, 3  // 두 번째 삼각형
};

```

EBO 생성 및 인덱스 복사:

```cpp
unsigned int EBO;
glGenBuffers(1, &EBO);

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);

```

렌더링 시에는 `glDrawElements`를 호출합니다.

```cpp
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);

```

VAO는 `GL_ELEMENT_ARRAY_BUFFER` 바인딩도 함께 추적하여 저장합니다.

최종 초기화 및 렌더링 코드:

```cpp
// Initialization
glBindVertexArray(VAO);

glBindBuffer(GL_ARRAY_BUFFER, VBO);
glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);

// Render loop
glUseProgram(shaderProgram);
glBindVertexArray(VAO);
glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
glBindVertexArray(0);

```

결과물:

![](https://learnopengl.com/img/getting-started/hellotriangle.png)

> **와이어프레임 모드 (Wireframe mode)**
> 삼각형을 와이어프레임 모드로 그리려면 `glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)`을 호출합니다. 기본 채우기 모드로 돌리려면 `glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)`을 사용합니다.

EBO 예제의 전체 소스 코드는 [LearnOpenGL Code Repository](https://learnopengl.com/code_viewer_gh.php?code=src/1.getting_started/2.2.hello_triangle_indexed/hello_triangle_indexed.cpp)에서 볼 수 있습니다.

---

## 추가 리소스 (Additional resources)

* **[antongerdelan.net/hellotriangle](https://antongerdelan.net/opengl/hellotriangle.html)**: Anton Gerdelan의 첫 삼각형 렌더링 가이드
* **[open.gl/drawing](https://open.gl/drawing)**: Alexander Overvoorde의 첫 삼각형 렌더링 가이드
* **[antongerdelan.net/vertexbuffers](https://antongerdelan.net/opengl/vertexbuffers.html)**: 버텍스 버퍼 오프젝트에 대한 추가 통찰

---

## 연습 문제 (Exercises)

1. `glDrawArrays`를 사용하여 버텍스 데이터를 추가하고 두 개의 삼각형을 서로 나란히 그려보세요: **[해답](https://learnopengl.com/code_viewer_gh.php?code=src/1.getting_started/2.3.hello_triangle_exercise1/hello_triangle_exercise1.cpp)**
2. 동일한 두 개의 삼각형을 두 개의 다른 VAO 및 VBO를 사용하여 그려보세요: **[해답](https://learnopengl.com/code_viewer_gh.php?code=src/1.getting_started/2.4.hello_triangle_exercise2/hello_triangle_exercise2.cpp)**
3. 두 개의 셰이더 프로그램을 생성하여 두 번째 프로그램은 노란색을 출력하는 프래그먼트 셰이더를 사용하도록 하고, 두 삼각형 중 하나가 노란색으로 출력되도록 해보세요: **[해답](https://learnopengl.com/code_viewer_gh.php?code=src/1.getting_started/2.5.hello_triangle_exercise3/hello_triangle_exercise3.cpp)**
