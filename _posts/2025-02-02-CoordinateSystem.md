---
categories: graphics
tag: graphic
toc: true
toc_sticky: true
author_profile: false
use_math: true 
thumbnail: images/coordinate_system1.png
---

### 좌표 변환 과정 해석  

자료출처:https://learnopengl.com/

# Coordinate Systems

그래픽스 파이프라인에서 정점(Vertex)의 좌표는 여러 단계의 좌표 변환을 거쳐 Normalized Device Coordinates(NDC) 범위인 [-1, +1]로 변환된다. 이를 위해 오브젝트의 Vertex 좌표를 여러 단계의 Coordinate System을 따라 변환하는 과정이 필요하다.

그래픽스 파이프라인에서 거치는 좌표 변환 단계는 다음과 같다.
- Local Space (Object Space)
- World Space
- View Space (Eye Space)
- Clip Space
- Screen Space

이러한 좌표 변환 과정을 모두 거친 후, 최종적으로 정점(Vertex)은 NDC 좌표로 변환되어 래스터라이제이션을 통해 Fragment로 변환된다.

<img src="https://learnopengl.com/img/getting-started/coordinate_systems.png" style="background-color:white;">

사진을 보면 알 수있듯이 5단계를 거치는 것을 알 수있다.
각 단계를 거치기 위해선 중간에 행렬(matrix)의 도움이 필요하다. 각각 MODEL,VIEW,PROJECTION 행렬이 그것이다.  
각 단계를 요약하자면 버텍스가 프래그먼트가 되기위한 과정은 로컬 - 월드 - 뷰 - 클립 - 스크린 coordinate 순을 거치게 된다는 것이다.


### 좌표 변환 과정 해석

1. **로컬 좌표 (Local Coordinates)**

로컬 좌표는 객체의 원점(local origin)을 기준으로 한 좌표를 의미한다. 이는 객체가 처음 정의될 때 사용되는 좌표이며, 모델링 단계에서 주어진다.  
예를 들어, Blender 같은 모델링 소프트웨어에서 큐브를 만들었다고 가정하면,
이 큐브의 원점(origin)은 **(0,0,0)** 일 가능성이 높다.

---

2. **월드 좌표 (World Coordinates)**

다음 단계는 로컬 좌표를 월드 좌표로 변환하는 것이다.
월드 좌표는 객체가 전체 세계(global world) 내에서 어디에 위치하는지 나타내는 좌표이다.
즉, 여러 개의 객체가 존재하는 하나의 큰 세계에서, 각 객체가 월드의 원점(global origin)을 기준으로 배치되는 좌표계라고 할 수 있다.
즉, 모든 정점(Vertex)들이 월드 원점(0,0,0) 기준으로 배치된 좌표계이다.  

우리는 객체를 배치할 때 **모델 행렬(Model Matrix)** 을 사용하여 로컬 좌표를 월드 좌표로 변환하게 된다.

모델 행렬(Model Matrix)이 하는 일:
- 객체를 이동(Translate)
- 객체를 회전(Rotate)
- 객체를 크기 조절(Scale)  
  
예를 들어, 집 모델을 생각해 보자.
원래 모델링한 집의 크기가 너무 크다면, 모델 행렬을 이용해 **축소(Scale Down)** 할 수 있다.
이 집을 서브 도시(suburb)로 **이동(Translate)** 시켜 배치할 수 있다.
주변 건물과 정렬되도록 **Y축을 기준으로 조금 회전(Rotate)** 할 수도 있다.

이전 장에서 특정 위치에 컨테이너를 배치하기 위해 사용했던 행렬도 일종의 모델 행렬이라고 볼 수 있다.
즉, 로컬 좌표(Local Coordinates)를 특정 위치(World)로 변환하는 과정이 모델 행렬의 역할이다.
  
---

3. **뷰 좌표 (View Coordinates)**

이제 월드(world) 좌표를 뷰 좌표(view-space coordinates)로 변환해야 한다.
이 단계에서는 모든 객체가 카메라(또는 관찰자)의 시점에서 보이는 좌표로 변환된다.
즉, 객체들이 “카메라의 위치와 방향”을 기준으로 어떻게 보이는지를 결정하는 변환이다.  
카메라가 위치하는 좌표를 중심으로 장면을 변환하는 과정이다.
이를 위해 **뷰 행렬(View Matrix)** 을 사용하며, 이 행렬은 보통 **회전(Rotation)과 이동(Translation)** 으로 구성된다.

예를 들어,
- 특정 객체를 화면 정중앙에 보이도록 하려면, 카메라를 이동해야 한다.
- 특정 객체를 다른 각도에서 보려면, 카메라를 회전해야 한다.

이 모든 변환을 **뷰 행렬(View Matrix)** 이 담당하며,
뷰 행렬을 적용하면 **월드 좌표 → 카메라 좌표(View Space)** 로 변환된다.

---

4. **클립 좌표 (Clip Coordinates)**

뷰 좌표가 구해지면, 이제 이를 클립 좌표(clip-space coordinates)로 변환해야 한다.
이 과정에서는 -1.0에서 1.0 사이의 범위로 좌표를 변환하여, 화면에 표시될 정점을 결정한다.  

(특히 **투영 변환(Projection Transformation)** 을 적용하면 원근감을 추가할 수 있다.
이때 사용되는 투영 방식에는 **원근 투영(Perspective Projection)** 과 **직교 투영(Orthographic Projection)** 이 있다.)

각 정점(Vertex)이 Vertex Shader를 통과한 후, OpenGL은 각 좌표가 특정 범위 안에 있는지 검사한다.
이 과정에서 해당 범위를 벗어난 좌표는 잘려(Clip) 버려지고, 남은 좌표들만 화면에 출력한다.
이러한 이유로, 이 공간을 **클립 공간(Clip Space)** 이라고 부른다.

하지만..
- 모든 좌표를 -1.0 ~ 1.0 범위에 맞춰 직접 지정하는 것은 어렵다. 
- 따라서, 우리는 좀 더 직관적인 좌표계를 사용하고, 이를 NDC(Normalized Device Coordinates)로 변환하는 과정을 거친다.

이 변환을 담당하는 것이 **투영 행렬(Projection Matrix)** 이다.
이 행렬은 뷰 공간(View Space) 좌표를 클립 공간(Clip Space)으로 변환하며,
이 과정에서 특정 **가시 영역(Frustum)** 을 정의한다.

예를 들어,
- 우리가 지정한 범위가 **(-1000, 1000)** 이라고 가정하면,
- 좌표 (1250, 500, 750)는 X축 범위를 초과하므로,
- NDC 범위를 벗어나며 잘려(Clipped) 화면에 보이지 않게 한다.


### 💡 참고! 
```
- 만약 삼각형의 일부만 클리핑 범위를 벗어난다면?
→ OpenGL은 삼각형을 다시 구성하여 화면에 맞도록 자동으로 변형한다.  

투영 행렬(Projection Matrix)의 역할은?
- 3D 좌표를 2D 정규화 좌표(NDC)로 변환 ⬅️ 이 과정을 투영(Projection)이라고 함
- 우리가 정한 가시 범위를 Frustum이라 함

투영 행렬에는 두 가지 방식이 있다.
	1.	직교 투영(Orthographic Projection)
	2.	원근 투영(Perspective Projection)
```
clip space 변환 후 perspective division이라는 계산과정이 포함되는데, 여기선 x,y,z와 같은 벡터 성분을 w값으로 나누어 준다.

---
### 직교 투영(Orthographic Projection)

직교 투영 행렬(orthographic projection matrix)은 정육면체 모양의 frustum(절두체) 을 정의하는데, 이 frustum 상자의 바깥에 있는 모든 정점(vertex)은 잘려나가게 된다.(clip). 직교 투영 행렬을 만들 때, 우리는 frustum의 가로(width), 세로(height), 깊이(depth)를 지정한다. 이 frustum 내부에 있는 모든 좌표는 변환된 후 NDC(Normalized Device Coordinates, 정규화 장치 좌표) 범위(-1.0 ~ 1.0) 안에 들어오게 되며, 그렇지 않은 좌표들은 잘려 나간다.

### 직교 투영의 특징
- Frustum은 가로, 세로, 깊이(near, far plane) 로 정의된다.
- Near plane 앞의 좌표는 잘리고, 마찬가지로 far plane 뒤의 좌표도 잘린다.
- 변환된 벡터의 w 컴포넌트를 변경하지 않으므로, 원근 왜곡이 없다.
- 즉, 원근감이 적용되지 않고, 모든 물체가 같은 크기로 보이게 된다.
   
<img src="https://learnopengl.com/img/getting-started/orthographic_frustum.png" style="background-color:white;">  

위 사진에서 만들어지는 입체도형이 절두체라고 보면 된다.  
(직교 투영에서 왜 직교가 들어가냐면, 투영선과 투영 평면이 직교하기 때문이라고 한다...)  
그래서 원근 투영과 다르게 원근감이 존재하지 않는다.  

직교 투영 행렬은 glm::ortho 함수를 이용하여 생성한다.
```cpp
glm::ortho(0.0f, 800.0f, 0.0f, 600.0f, 0.1f, 100.0f); //매개변수 6개

//각 매개변수 설명
//left, right : frustum의 좌/우 경계 (여기서는 0~800)
//bottom, top : frustum의 아래/위 경계 (여기서는 0~600)
//near, far : 가까운 면과 먼 면의 거리 (여기서는 0.1~100)

이 행렬은 지정한 x, y, z 범위 내의 모든 좌표를 NDC(-1.0 ~ 1.0) 범위로 변환하게 된다.
``` 


### 원근 투영(Perspective Projection)

<img src="https://learnopengl.com/img/getting-started/perspective_frustum.png" style="background-color:white;">  

현실에서 사물을 보면 멀리 있는 물체가 더 작게 보이는 현상(원근감, Perspective)이 있다. 예를 들어, 기차 선로를 보면 먼 곳으로 갈수록 선로가 좁아지는 것처럼 보이다. 원근 투영은 이와 같은 원근감을 반영하는 투영 방법이다.

원근 투영 행렬은 frustum을 clip space로 변환할 때 w 값도 조작하여, 멀리 있는 정점이 더 작게 보이도록 만든다. 즉, z 값이 클수록(=멀수록) w 값도 커지며, 최종 좌표는 w로 나누어지므로 더 작아진다. 이를 원근 나눗셈(Perspective Division) 이라고 한다.

### 원근 투영 행렬 변환 과정
- w 컴포넌트가 조작됨
- 변환 후 clip space에서 x, y, z를 각각 w로 나누어(원근 나눗셈) 멀리 있는 정점이 작게 보이도록 만듦
- 변환 후 NDC(-1.0 ~ 1.0) 범위 내에 있는 좌표만 화면에 렌더링됨  

원근 투영 행렬은 다음 코드로 실행 된다.
```cpp
glm::mat4 proj = glm::perspective(glm::radians(45.0f), (float)width/(float)height, 0.1f, 100.0f);

//매개변수 설명
fov(Field of View, 시야각): 일반적으로 45도 정도가 현실적인 값이며, 값이 클수록 더 넓은 영역을 볼 수 있음.

aspect ratio(종횡비): 뷰포트 너비를 높이로 나눈 값. ➡️ (float)width/(float)height

near, far: 카메라에서 가까운 평면과 먼 평면 거리 (일반적으로 0.1f ~ 100.0f)
```
![alt text](https://learnopengl.com/img/getting-started/perspective_orthographic.png)

➡️ 다음과 같이 직교투영과 원근투영시 결과가 다른 것을 알 수있다.
(직교 투영에선 perspective div의 효과가 없는 상태로 clip space에 매핑.)  
***매핑(mapping)“은 3D 공간의 좌표나 데이터를 다른 공간으로 변환하는 과정을 의미***

투영행렬이 가시영역(절두체)를 정의하는 거고, 원근 나누기 과정이 정점 데이터를 NDC로 변환해주는 과정이다.

---

5. 화면 좌표 (Screen Coordinates) & 뷰포트 변환 (Viewport Transform)

마지막으로, 클립 좌표를 **화면 좌표(Screen Coordinates)** 로 변환하는 단계이다.
이 과정은 **뷰포트 변환(Viewport Transform)** 이라고 하며, glViewport 함수에 의해 정의된 화면 크기에 맞게 NDC 좌표(-1.0 ~ 1.0)를 실제 픽셀 단위의 화면 좌표로 변환한다.
변환된 좌표들은 **래스터라이저(Rasterizer)** 에 의해 프래그먼트(Fragments)로 변환되어 픽셀을 생성하는 과정으로 넘어가게 된다.

```
요약
1. Local Coordinates → 객체의 로컬 원점을 기준으로 한 좌표
2. World Coordinates → 월드 원점을 기준으로 배치된 좌표
3. View Coordinates → 카메라 시점에서 본 좌표
4. Clip Coordinates → -1.0 ~ 1.0 범위로 변환된 좌표 (투영 변환 적용)
5. Screen Coordinates → glViewport를 사용해 실제 픽셀 단위의 화면 좌표로 변환됨
```

이후 **래스터라이저(Rasterizer)** 가 화면 좌표를 **프래그먼트(Fragments)** 로 변환하여 최종 픽셀을 생성한다. 

<img src="https://learnopengl.com/img/getting-started/coordinate_systems.png" style="background-color:white;">



## putting in together
이제 각 과정을 위해 필요한 행렬들 MODEL,VIEW,PROJECTION 행렬을 생성하여 오른쪽에서 왼쪽 방향으로 곱해준다면 clip coordination에 범위에 맞는 정점인 
$ V_{\text{clip}} $
를 구할 수 있다.  

$ 
V_{\text{clip}} = M_{\text{projection}} \cdot M_{\text{view}} \cdot M_{\text{model}} \cdot V_{\text{local}} 
$

## Going 3D

이제부터 위에서 설명한 것들을 코드로 구현할 때이다.	우리는 객체를 배치할 때 **모델 행렬(Model Matrix)** 을 사용하여 로컬 좌표를 월드 좌표로 변환하게 된다고 하였다.  

### 1. 모델 행렬(Model Matrix) 수행하기 : 바닥 쪽으로 눕히기
- 객체를 이동(Translate)
- 객체를 회전(Rotate)
- 객체를 크기 조절(Scale)  

```cpp
glm::mat4 model = glm::mat4(1.0f);
model = glm::rotate(model, glm::radians(-55.0f), glm::vec3(1.0f, 0.0f, 0.0f));
```
model 이라는 기본 4x4 항등행렬을 생성하고, 그 행렬을 회전한 모습이다. 회전 축은 X축임을 세번째 인수로 알 수있다.  
MODEL 행렬을 곱한다면 vertex 좌표를 world 좌표로 변환하는 1단계가 이루어진다.  
X축을 잡고 돌린다고 생각하면, 결국 바닥쪽으로 눕혀지는 모습이 나오게 될 것이다.

### 2. 뷰 행렬(View Matrix) & 투영 행렬 수행하기 : 멀어지는 방향으로
이제 월드 좌표를 뷰 행렬과 곱합으로서 카메라 시점인 뷰 좌표로 변환시켜주어야 한다.  
기억해야 할것은 "카메라가 뒤로 멀어지는 것과 scene이 앞으로 당겨지는것은 같은 방향이다." 
즉 view(카메라)가 뒤로 이동하는 효과를 위해 scene를 z축의 음의 방향으로 이동(Translation)해주면 된다.

![alt text](/images/coordinate_system1.png)  
참고로 OpenGL은 ***오른손 시스템*** 을 사용한다.   
```
엄지 = X축 양의 방향  
검지 = Y축 양의 방향
중지 = Z축 양의 방향
```

아무튼 뷰 행렬을 설정, 생성해보면... 
```cpp
glm::mat4 view = glm::mat4(1.0f);
// 우리가 이동하고자 하는 방향의 반대 방향으로 장면을 이동시키는 것을 주의하세요
view = glm::translate(view, glm::vec3(0.0f, 0.0f, -3.0f));
```
view라는 이름의 항등행렬을 생성하고 , 이후 translate 함수를 이용하여 Z축의 음의 방향으로 이동시킨 것을 볼 수있다.  
다음은 투영 행렬 코드이다. 	
```cpp
glm::mat4 projection;
projection = glm::perspective(glm::radians(45.0f), 800.0f / 600.0f, 0.1f, 100.0f);
```
projection 이라는 행렬을 선언하고, (투영 행렬은 항등행렬로 초기화하는 과정이 없다.) 바로 투영 과정을 설정한다.

```cpp
#version 330 core
layout (location = 0) in vec3 aPos;
...
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    // 행렬 곱셈을 오른쪽에서 왼쪽으로 읽는다는 것을 주의하세요
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    ...
}
```
버텍스 셰이더에는 이렇게 코드를 작성해주면 된다. 

OpenGL의 코드에는 아래와 같이 작성한다.

```cpp
int modelLoc = glGetUniformLocation(ourShader.ID, "model");
glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm::value_ptr(model));
... // View Matrix와 Projection Matrix도 동일하게 처리해줄것.
```


결과는 다음과 같다.  

![alt text](/images/coordinate_system2.png)  


## 3D 큐브 렌더링하기
큐브는 삼각형 2개 * 6개의 평면이므로 36개의 정점 데이터를 받는다.

```cpp
float vertices[] = {
    -0.5f, -0.5f, -0.5f,  0.0f, 0.0f,
     0.5f, -0.5f, -0.5f,  1.0f, 0.0f,
     0.5f,  0.5f, -0.5f,  1.0f, 1.0f,
     0.5f,  0.5f, -0.5f,  1.0f, 1.0f,
    -0.5f,  0.5f, -0.5f,  0.0f, 1.0f,
    -0.5f, -0.5f, -0.5f,  0.0f, 0.0f,

    -0.5f, -0.5f,  0.5f,  0.0f, 0.0f,
     0.5f, -0.5f,  0.5f,  1.0f, 0.0f,
     0.5f,  0.5f,  0.5f,  1.0f, 1.0f,
     0.5f,  0.5f,  0.5f,  1.0f, 1.0f,
    -0.5f,  0.5f,  0.5f,  0.0f, 1.0f,
    -0.5f, -0.5f,  0.5f,  0.0f, 0.0f,

    -0.5f,  0.5f,  0.5f,  1.0f, 0.0f,
    -0.5f,  0.5f, -0.5f,  1.0f, 1.0f,
    -0.5f, -0.5f, -0.5f,  0.0f, 1.0f,
    -0.5f, -0.5f, -0.5f,  0.0f, 1.0f,
    -0.5f, -0.5f,  0.5f,  0.0f, 0.0f,
    -0.5f,  0.5f,  0.5f,  1.0f, 0.0f,

     0.5f,  0.5f,  0.5f,  1.0f, 0.0f,
     0.5f,  0.5f, -0.5f,  1.0f, 1.0f,
     0.5f, -0.5f, -0.5f,  0.0f, 1.0f,
     0.5f, -0.5f, -0.5f,  0.0f, 1.0f,
     0.5f, -0.5f,  0.5f,  0.0f, 0.0f,
     0.5f,  0.5f,  0.5f,  1.0f, 0.0f,

    -0.5f, -0.5f, -0.5f,  0.0f, 1.0f,
     0.5f, -0.5f, -0.5f,  1.0f, 1.0f,
     0.5f, -0.5f,  0.5f,  1.0f, 0.0f,
     0.5f, -0.5f,  0.5f,  1.0f, 0.0f,
    -0.5f, -0.5f,  0.5f,  0.0f, 0.0f,
    -0.5f, -0.5f, -0.5f,  0.0f, 1.0f,

    -0.5f,  0.5f, -0.5f,  0.0f, 1.0f,
     0.5f,  0.5f, -0.5f,  1.0f, 1.0f,
     0.5f,  0.5f,  0.5f,  1.0f, 0.0f,
     0.5f,  0.5f,  0.5f,  1.0f, 0.0f,
    -0.5f,  0.5f,  0.5f,  0.0f, 0.0f,
    -0.5f,  0.5f, -0.5f,  0.0f, 1.0f
};
```




