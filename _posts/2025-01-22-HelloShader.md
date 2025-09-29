---
categories: graphics
tag: graphic
toc: true
toc_sticky: true
author_profile: false
use_math: true 
images: 
---
## 셰이더 개념과 코드 이해하기  

자료출처:https://learnopengl.com/

# 쉐이더란?

셰이더는 GPU에서 실행되는 프로그램으로, 화면을 그리거나 색을 입히는 기능을 가진다. 셰이더는 기본적으로 다른 셰이더와 소통하려면 그들의 입력값과 출력값으로 소통하는데, 입력값과 출력값은 동일한게 원칙이다.
opengl에서는 GLSL (OpenGL Shading Language)을 사용한다.
그래픽스 용으로 쓰이면서 벡터와 행렬에 강점을 지닌 언어이다.

# 쉐이더(GLSL) 코드의 기본 구조

쉐이더 코드는 다음과 같은 순서로 작성된다.
```
1.	버전 선언: 사용할 GLSL의 버전을 선언

2.	입력 변수 (in): 쉐이더로 들어오는 값들을 정의.(정점의 위치나 색상 등.)

3.	출력 변수 (out): 쉐이더가 끝난 후 결과를 출력할 변수를 정의함.

4.	유니폼 (uniform): 쉐이더가 실행되는 동안 바뀌지 않는 값들을 정의한다.

5.	메인 함수 (main):입력값을 받아서 처리를 하고, 결과를 출력값에 저장한다.
```
	
	
	

### 예문
```glsl
#version 330 core  // 버전 선언

in vec3 position;  // 입력변수 : 3D 공간에서 점의 위치
in vec4 color;     // 입력변수: 점의 색상

out vec4 fragColor; // 출력변수: 최종적으로 화면에 표시될 색상

uniform mat4 model;  // 유니폼: 모델 변환 행렬 (장면에서의 객체 위치. 삼각형 그리는데 위치가 변하진 않으니 유니폼 변수로 선언)

void main() {
    fragColor = color * model * vec4(position, 1.0); // 위치와 색상을 결합하여 최종 색상을 계산하도록 명령함.
}
```
---
GLSL의 데이터 타입
GLSL도 C언어와 마찬가지로 int,float같은 데이터 타입을 사용하고, 앞서 말했듯 벡터와 행렬을 활용할 수 있다. 

**벡터(Vector)**

GLSL에서 벡터는 2, 3, 4개의 기본 타입으로 이루어진 컨테이너이다. 예를 들어, vec2, vec3, vec4처럼 다양한 크기의 벡터를 사용할 수 있으며, 벡터는 다음과 같은 형태로 쓴다

	•	vecn: n개의 float로 이루어진 기본 벡터.
	•	bvecn: n개의 bool로 이루어진 벡터.
	•	ivecn: n개의 int로 이루어진 벡터.
	•	uvecn: n개의 unsigned int로 이루어진 벡터.
	•	dvecn: n개의 double로 이루어진 벡터.

벡터의 각 요소는 vec.x처럼 `.` 연산자를 이용해 접근할 수 있다.  
vec.x, vec.y, vec.z, vec.w와 같이 벡터의 첫 번째, 두 번째, 세 번째, 네 번째 요소를 각각 참조할 수 있다.

---

### **스위즐링(Swizzling)**

벡터의 기존 벡터의 요소를 섞어(재사용) 새로운 벡터를 만드는데 활용하는것.
```glsl
vec2 someVec;
vec4 differentVec = someVec.xyxx;  // someVec의 x와 y를 가져와서 다른 벡터의 값으로 설정

vec3 anotherVec = differentVec.zyw;  // differentVec의 z, y, w를 가져와서 새로운 벡터로 설정

vec4 otherVec = someVec.xxxx + anotherVec.yxzy;  // 벡터 요소들을 조합하여 새로운 벡터를 만들기
```

이렇게 기존의 요소를 활용함으로서 써야하는 인수의 수를 줄인다.

```glsl
vec2 vect = vec2(0.5, 0.7);

vec4 result = vec4(vect, 0.0, 0.0);  // vect 벡터를 사용해서 새로운 vec4 벡터 생성

vec4 otherResult = vec4(result.xyz, 1.0);  // result 벡터에서 xyz만 뽑아서 새로운 벡터 생성
```
---

이제 위의 내용들을 활용하여 셰이더간 데이터 전달을 확인해본다. 



## 버텍스 쉐이더 (Vertex Shader)
```glsl
#version 330 core
layout (location = 0) in vec3 aPos; // 위치 변수는 속성 위치 0에서 입력되며, 입력변수는 vec3 형태이다.
  
out vec4 vertexColor; // 프래그먼트 쉐이더로 전달할 색상 출력을 정의. vec4형태.

void main()
{
    gl_Position = vec4(aPos, 1.0); // vec3 타입을 vec4로 형 변환하여 gl_Position에 전달한다.
    vertexColor = vec4(0.5, 0.0, 0.0, 1.0); // 출력 변수에 어두운 빨간색 값으로 결정.
}
```

## 프래그먼트 쉐이더 (Fragment Shader)
```glsl
#version 330 core
out vec4 FragColor; // 최종 색상을 출력하는 출력변수
  
in vec4 vertexColor; // 버텍스 쉐이더에서 전달된 입력 변수 (이름과 타입이 동일)

void main()
{
    FragColor = vertexColor; // 버텍스 쉐이더에서 받은 색상 값을 최종 색상으로 출력합니다.
}
```

위 두 코드를 설명하자면, 버텍스 셰이더 코드는 vec4형태의 벡터를 2개 출력변수로 만들었고 각각 위치와 색상의 관한 값이다. 그리고 이를 프래그먼트 셰이더가 받아서 색상부분은 그대로 받아들여 최종색상으로 정했다는 내용이 됨을 알 수 있다.

---

이제 이 상황에서 유니폼 변수를 추가해서 배워보자.
프래그먼트 셰이더를 아래와 같이 작성했다고 해보자

```glsl
out vec4 FragColor;

uniform vec4 ourColor; // OpenGL 코드에서 이 값을 설정

void main()
{
    FragColor = ourColor; // Uniform 값을 출력 색상으로 설정
}
```


유니폼은 전역변수같은것으로 셰이더프로그램에서 언제든지 불러서 쓸 수 있는 편리한 변수이다.
아래와 같이 사용하면 된다.

```c++
while (!glfwWindowShouldClose(window))
{
    // 1. 입력 처리
    processInput(window);

    // 2. 화면 초기화
    glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT);

    // 3. 쉐이더 프로그램 활성화
    glUseProgram(shaderProgram);

    // 4. 시간 기반으로 색상 계산
    float timeValue = glfwGetTime();
    float greenValue = sin(timeValue) / 2.0f + 0.5f;

    // 5. Uniform 위치 가져오기 및 값 업데이트
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
5번라인을 잘 보면 내가 작성한 셰이더프로그램들 중에서 ourColor라고 쓴 유니폼 변수가 존재하면 그것을 찾아 위치를 vertexColorLocation에 저장한 것이고, glUniform4f은 그 ourColor에다가 색상을 부여한 것이다. 저상태로 렌더루프가 실행되면 [색이 변하는 삼각형](https://learnopengl.com/video/getting-started/shaders.mp4)이 나타난다.



## 더 많은 속성 다루기
이전 챕터에서 VAO는 속성정보와 VBO도 묶어서 가지고 있었는데, 동일한상황에서 색상 정보도 추가해 보려고 한다.

```glsl
float vertices[] = {
    // 위치               // 색상
     0.5f, -0.5f, 0.0f,  1.0f, 0.0f, 0.0f,  // 오른쪽 아래 (빨강)
    -0.5f, -0.5f, 0.0f,  0.0f, 1.0f, 0.0f,  // 왼쪽 아래 (초록)
     0.0f,  0.5f, 0.0f,  0.0f, 0.0f, 1.0f   // 위쪽 (파랑)
};

```

- 각 꼭짓점은 **위치(3 floats)** 와 색상(3 floats) 데이터를 포함합니다.
- *예: (x, y, z, red, green, blue)*




## 버텍스 쉐이더 수정

추가된 색상 데이터를 받으려면, 버텍스 쉐이더에 **새로운 속성(aColor)**을 추가해야 합니다:
```glsl
#version 330 core
layout (location = 0) in vec3 aPos;   // 위치 (attribute 0)
layout (location = 1) in vec3 aColor; // 색상 (attribute 1)

out vec3 ourColor; // 프래그먼트 쉐이더로 전달할 색상 변수

void main()
{
    gl_Position = vec4(aPos, 1.0); // 위치 계산
    ourColor = aColor;            // 입력받은 색상을 ourColor에 저장
}
```
	•	layout (location = 0): aPos 속성은 0번 위치에 있습니다.
	•	layout (location = 1): aColor 속성은 1번 위치에 있습니다.

## 프래그먼트 쉐이더 수정

프래그먼트 쉐이더는 버텍스 쉐이더로부터 색상 데이터를 받아와 화면에 출력합니다:
```glsl
#version 330 core
out vec4 FragColor;  
in vec3 ourColor; // 버텍스 쉐이더로부터 받은 색상

void main()
{
    FragColor = vec4(ourColor, 1.0); // 색상을 출력 (알파값 1.0)
}
```

  
![alt text](/images/vertex_attribute_pointer_interleaved.png) 
새로운 속성을 반영하기 위해 버텍스 속성 포인터를 재구성해야 한다.   
위치와 색상을 포함한 데이터는 교차(interleaved) 형태로 VBO에 저장된다.      

```glsl
// 위치 속성 (attribute 0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
glEnableVertexAttribArray(0);

// 색상 속성 (attribute 1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));
glEnableVertexAttribArray(1);
```

**설명**  

```
1.stride(보폭) :  한 꼭짓점 데이터의 크기 = 6 * sizeof(float) (위치 3개 + 색상 3개)    
2.offset (시작점)  
3.위치 속성: 0 (데이터의 첫 번째 값이 위치 시작점)
4.색상 속성: 3 * sizeof(float) (위치 데이터 다음부터 색상 시작)  
```

  

 
# 색상 변화의 원리: Fragment Interpolation

삼각형을 렌더링할 때, 실제 화면에 그려지는 **픽셀(fragment)** 의 수는 **정점(vertex)** 의 수보다 훨씬 많습니다. 쉐이더는 픽셀의 위치에 따라 각 정점의 색상을 ***선형 보간(linear interpolation)*** 한다.
	•	예: 삼각형의 한쪽 꼭짓점은 빨강, 다른 쪽은 파랑이라면, 중간에 위치한 픽셀은 보라색(빨강 + 파랑 혼합)으로 나타난다.
	•	삼각형 내부 색상은 자동으로 부드럽게 변화한다. 정가운데는 결국 흰색.  

![alt text](/images/image.png)
