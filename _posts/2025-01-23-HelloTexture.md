---
categories: graphics
tags: [graphics, opengl, texture, tutorial]
toc: true
toc_sticky: true
author_profile: false
use_math: true 
thumbnail: https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTf6c44cGdSVe9jPWgeQWwXyCdwjADxP6NrLA&s
---

## 텍스처 (Texture)  

**자료 출처**: [LearnOpenGL](https://learnopengl.com/)

텍스처는 일반적으로 2D 이미지이며, 오브젝트에 씌우면 오브젝트의 겉모습과 무늬가 쉽게 변한다.

![alt text](/images/image-1.png)

위 그림은 삼각형에 텍스처를 입힌 모습이다. 이러한 결과를 얻기 위해서는 삼각형의 각 정점이 텍스처의 어느 부분에 해당하는지를 알아야 한다. 이를 **텍스처 좌표 (texture coordinate)** 와 매핑하는 것이라고 한다. 텍스처 좌표는 (u, v)로 나타내며, 보통 0.0 ~ 1.0 사이의 정규화된 값을 사용한다. (*아래 사진*)

![alt text](/images/image-2.png)

위 삼각형을 예로 들면 다음과 같다.

*   삼각형의 왼쪽 하단을 텍스처 좌표에서 (0,0)으로 한다.
*   오른쪽 하단을 텍스처 좌표에서 (1,0)으로 한다.
*   가운데 위를 텍스처 좌표에서 (0.5, 1)으로 한다.

---

이렇게 나온 텍스처 좌표를 버텍스 셰이더 (vertex shader)에 전달하면, 버텍스 셰이더는 이를 프래그먼트 셰이더 (fragment shader)로 전달한다. 프래그먼트 셰이더는 선택받지 못한 (3점을 제외한 나머지) 픽셀의 위치가 텍스처에서 어디에 해당하는지 보간하여 처리한다.

### 텍스처 래핑 모드 (Texture Wrapping Mode)  

텍스처 좌표의 범위는 (0,0) ~ (1,1)이라고 하였다. 만약 ***이 범위를 벗어나면*** 처리할 수 있는 방식은 크게 4가지이며, 이를 **텍스처 래핑 모드 (Texture Wrapping Mode)** 라고 한다.

![alt text](/images/Fragment_Interpolation.png)

*   **GL_REPEAT** {#gl_repeat}: 텍스처 이미지를 반복한다.

*   **GL_MIRRORED_REPEAT** {#gl_mirrored_repeat}: 반복 시 거울처럼 이미지가 반전된다.

*   **GL_CLAMP_TO_EDGE** {#gl_clamp_to_edge}: 텍스처의 가장자리 색상을 사용하여 값을 채우는 방식이다. (텍스처 좌표가 0.0보다 작을 경우 → 0.0에 해당하는 가장자리 색상 사용 & 텍스처 좌표가 1.0보다 클 경우 → 1.0에 해당하는 가장자리 색상 사용)

*   **GL_CLAMP_TO_BORDER** {#gl_clamp_to_border}: 범위를 벗어난 좌표는 사용자가 지정한 색으로 처리한다.

위 4가지 래핑 모드는 `glTexParameter` 함수를 사용해서 하나씩 설정할 수 있다. 텍스처가 2D이면 s, t (x = s, y = t, r은 3D 텍스처에서 정의되면 z값과 같다)를 사용한다.

```cpp
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_MIRRORED_REPEAT);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_MIRRORED_REPEAT);
```

만일 `GL_CLAMP_TO_BORDER` 모드라면, 좌표를 벗어난 부분의 경계색도 지정해야 하므로, 매개변수가 하나 더 있는 함수인 `glTexParameterfv`를 사용하여 `GL_TEXTURE_BORDER_COLOR` 옵션으로 float 값을 넘겨주어야 한다.

```cpp
float borderColor[] = { 1.0f, 1.0f, 0.0f, 1.0f };
glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, borderColor); // 경계색 인자 (GL_TEXTURE_BORDER_COLOR) 추가
```

---

### 텍스처 필터링 (Texture Filtering) 

만일 삼각형이 텍스처보다 훨씬 크다면, 텍스처를 입혔을 때 해상도가 깨진 상태가 될 것이다. 이를 극복하기 위해서 **텍스처 필터링 (Texture Filtering)** 기술로 이를 보완할 수 있다. 텍스처 필터링이란 텍스처 샘플링 중에 픽셀 크기와 텍스처 좌표가 일치하지 않을 때 부드러운 결과를 생성하기 위해 사용하는 기법을 의미한다.

텍스처는 **텍셀 (texel)** 이라는 기본 픽셀 단위로 구성되는데, 텍셀은 텍스처와 화면에 대응되도록 하는 텍스처상의 픽셀을 의미한다.

필터링 방식은 매우 다양하지만, 여기서는 대표적으로 `GL_NEAREST`와 `GL_LINEAR`를 소개한다.

#### GL_NEAREST

![alt text](/images/texture3.png)

`GL_NEAREST`는 OpenGL에서 기본으로 적용하는 필터링 방식이다. 텍스처 좌표가 있으면 이 위치에서 가장 가까운 텍셀을 선택해서 적용한다. 위 그림을 보면 텍스처 좌표는 왼쪽 위 텍셀의 중심과 가장 가깝기 때문에 이 텍셀로 샘플링하여 색을 결정한다.

#### GL_LINEAR 

![alt text](/images/texture4.png)

`GL_LINEAR` 방식은 텍스처 좌표가 있고 그 좌표값에 인접한 텍셀들에 대해서 가까운 만큼 (비율에 맞게) 혼합적으로 보간을 해줘서 최종 텍셀을 생성한다.

![alt text](/images/texture5.png)

필터링 방식에 따라 픽셀이 두드러질 수도 있고, 부드러워질 수도 있다.

```cpp
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
```

위 코드는 텍스처 필터링이 확대되거나 축소되는 경우 어떤 방식으로 필터링할지 결정할 수 있음을 보여준다. 첫 번째 라인은 텍스처가 축소될 때 가장 가까운 텍셀 하나만 샘플링하는 `GL_NEAREST` 방식을, 두 번째 라인은 확대될 때 주변 텍셀 값들에 선형 보간을 적용한 `GL_LINEAR` 방식을 사용한다.

---

### 밉맵 (Mipmap) 

오브젝트에 텍스처를 입혔을 때, 가까이 있건 멀리 있건 계속 고해상도 상태로 유지된다면, 멀리 있을 때는 텍스처를 구체적으로 표현할 이유가 없기도 하고 메모리 낭비이므로 고해상도 텍스처가 될 필요가 없게 된다.

그래서 미리 기존의 텍스처 이미지를 **밉맵 (Mipmap)** 하는 방식을 사용한다. 밉맵은 ***텍스처 이미지를 여러 크기로 줄여서 저장해 놓은 것*** 으로, 대개 2배 기준으로 작게 만들고 이를 따로 저장해 둔다.

![alt text](/images/texture6.png)

만약 텍스처가 적용되는 object까지의 거리가 특정 값 이상으로 넘어가면 거기에 알맞은 밉맵 텍스처를 적용시키는 것이다. 위 사진은 밉맵을 모아둔 한 예이다.

밉맵은 텍스처 하나하나마다 생성시키기 번거로우니, `glGenerateMipmap` 함수를 써서 자동으로 밉맵을 생성할 수 있다.

그런데 이전에 설명했듯 텍스처의 크기가 늘어나거나 줄어들 때, **텍스처 필터링 (Texture Filtering)** 을 할 수 있다고 하였다. 텍스처가 적용되는 거리가 특정 값을 넘어가는 경우 텍스처가 사이즈가 변하게 될 텐데, 이때도 마찬가지로 필터링 기술을 적용할 수 있다. 이 역시 대표적으로 `NEAREST`, `LINEAR`가 있고, 옵션은 크게 4가지로 나뉜다.

#### 밉맵 필터링 옵션 

*   **GL_NEAREST_MIPMAP_NEAREST** {#gl_nearest_mipmap_nearest-1}: 밉맵 중에서 픽셀 크기에 가장 가까운 하나를 고르고, 그 레벨에서 **가장 가까운 텍셀 (근접 보간)** 을 가져온다.

*   **GL_LINEAR_MIPMAP_NEAREST** {#gl_linear_mipmap_nearest-1}: 밉맵 중에서 픽셀 크기에 가장 가까운 하나를 고르고, 그 레벨에서 여러 텍셀을 선형 보간하여 값을 가져온다.

*   **GL_NEAREST_MIPMAP_LINEAR** {#gl_nearest_mipmap_linear-1}: 픽셀 크기에 가장 가까운 두 개의 밉맵을 고르고, 둘을 섞은 다음에 근접 보간으로 텍셀 값을 가져온다.

*   **GL_LINEAR_MIPMAP_LINEAR** {#gl_linear_mipmap_linear-1}: 픽셀 크기에 가장 가까운 두 개의 밉맵을 고르고, 둘을 섞은 다음, 각각의 밉맵에서 선형 보간하여 값을 가져온다.

---

```cpp
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
```

위 코드는 아까와 같은 함수 (`glTexParameteri`)인데, 필터링 방식이 위 4가지로 수정된 것 뿐이다.

### stb_image.h 라이브러리 및 #define 키워드 

`stb_image.h`는 웬만한 이미지를 로드할 수 있는 라이브러리이다. 사용 시 다음과 같은 코드를 입력한다.

```cpp
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
```

`#define`은 라이브러리에서 특정 구현을 활성화할 때 자주 쓴다. 예를 들어 `stb_image.h`에서 `#define STB_IMAGE_IMPLEMENTATION`은 함수 구현을 활성화하기 위해 사용한다.

```C
#ifdef STB_IMAGE_IMPLEMENTATION
// 실제 함수 구현 코드
unsigned char *stbi_load(const char *filename, int *x, int *y, int *comp, int req_comp) {
    // 이미지 로드하는 함수 구현
    return NULL; // 예시를 위해 NULL 반환
}
#endif
```

`std_image.h`는 일반적인 헤더 파일과는 다르게 함수 선언뿐 아니라 구현부까지 넣어놓았다. 즉 `define` 키워드를 내가 실행할 파일에서 사용해야 함수 부분을 활성화시킬 수 있다는 것이다.

단, 프로그램 내에서 단 한 번만 선언해야 한다. 프로그램을 만들 때 여러 개의 실행 파일들이 존재할 텐데, 그 파일들 중 여러 개는 `stb_image.h`의 함수를 사용하게 될 것이다. 그렇더라도 모든 파일 말고 단 한 개의 파일에서 한 번의 선언만 하면 된다.

여러 번 `define` 키워드로 활성화시킬 경우, 동일 함수가 여러 번 구현되어 오류가 나기 때문이다.

#### #define STB_IMAGE_IMPLEMENTATION 

#### 중복 정의 오류 {#중복-정의-오류}

### 텍스처 사용 시작 {#텍스처-사용-시작}

`stb_image.h` 함수를 활성화 했다면 코드 작성으로 텍스처 이미지를 사용하겠다는 표시를 해주어야 한다.

```cpp
int width, height, nrChannels;
unsigned char *data = stbi_load("container.jpg", &width, &height, &nrChannels, 0);
```

폭, 너비, 색상 채널 수를 선언하고, texture 이미지를 사용하기 위해 `stbi_load` 함수를 사용한다. 선언했던 `int`들이 인자로 넘어간 것을 볼 수 있다.

#### 이미지 로드 {#이미지-로드}

#### 텍스처 객체 생성 및 바인딩

```cpp
unsigned int texture;
glGenTextures(1, &texture); // 1개의 텍스처 오브젝트를 만들고 이 ID를 texture 변수에 저장.
```

이 코드는 마치 VAO를 만들었을 때랑 유사하다. 텍스처도 다른 오브젝트처럼 ID를 담아서 참조하는 것이다. 결국 texture ID를 생성하는 코드이다. 그리고 여느 오브젝트들이 그래왔듯 바인딩으로 활성화 시키고 그 활성화된 오브젝트를 조정한다.

```cpp
glBindTexture(GL_TEXTURE_2D, texture);

glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data);
glGenerateMipmap(GL_TEXTURE_2D);
```

`glTexImage2D`는 텍스처 이미지를 생성하는 함수이다.

#### 텍스처 이미지 생성 (glTexImage2D) 

```cpp
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data);
```

1.  **텍스처 타겟 (첫 번째 인수)**: 첫 번째 인수는 어떤 종류의 텍스처를 생성할지 정하는 인수이다. `GL_TEXTURE_2D`를 쓴다면 2D 텍스처를 사용하겠다는 뜻이다.

2.  **Mipmap 레벨 (두 번째 인수)**: 두 번째 인수는 Mipmap은 텍스처의 여러 해상도 버전을 말한다. 이 인수는 어떤 Mipmap 레벨을 설정할지 지정한다. 보통 기본 레벨인 0을 사용한다.

3.  **텍스처 저장 형식 (세 번째 인수)**: 세 번째 인수는 OpenGL이 텍스처를 어떤 형식으로 저장할지 결정한다. 예를 들어, 이미지가 RGB 값만 가지고 있다면, `GL_RGB`와 같은 형식을 사용한다.

4.  **텍스처의 너비와 높이 (네 번째와 다섯 번째 인수)**: 네 번째, 다섯 번째는 텍스처의 크기, 높이를 지정한다. 예를 들어, 256x256 픽셀의 텍스처를 생성하려면 너비와 높이를 각각 256으로 설정한다.

5.  **레거시 요소 (여섯 번째 인수)**: 여섯 번째는 항상 0으로 설정한다. 이는 과거의 호환성을 위해 남겨진 것이다.

6.  **소스 이미지 형식과 데이터 유형 (일곱 번째와 여덟 번째 인수)**: 일곱 번째, 여덟 번째 인수들은 소스 이미지의 형식과 데이터 유형을 지정한다. 예를 들어, 이미지가 RGB 형식이고 각 픽셀이 바이트 (8비트)로 저장되어 있다면, `GL_RGB`와 `GL_UNSIGNED_BYTE`를 사용한다.

7.  **이미지 데이터 (마지막 인수)**: 마지막 인수는 실제 이미지 데이터를 전달한다. 이 데이터는 픽셀 값들의 배열로, 텍스처로 로드될 것이다.

이렇게 `glTexImage2D`를 정상 호출했다면 텍스처 오브젝트 (texture)는 텍스처 이미지 (data)를 갖게 된다. 그리고 다음 라인에 `glGenerateMipmap`을 사용하면 필요한 모든 밉맵이 생성된다.

#### 밉맵 생성 (glGenerateMipmap) 

밉맵 생성을 완료하면 이미지 메모리는 지워주도록 한다.

#### 메모리 해제 (stbi_image_free) 

```cpp
stbi_image_free(data); // 이미지 메모리 지움.
```

### 텍스처 적용하기 

이전에 사각형을 그릴 때 썼던 `glDrawElements` 코드를 발전시킬 것이다. vertex data에서 texture coordinate (텍스처 좌표)를 추가하면,

#### 버텍스 데이터 수정 (텍스처 좌표 추가) 

```cpp
float vertices[] = {
    // positions          // colors           // texture coords
     0.5f,  0.5f, 0.0f,   1.0f, 0.0f, 0.0f,   1.0f, 1.0f,   // top right
     0.5f, -0.5f, 0.0f,   0.0f, 1.0f, 0.0f,   1.0f, 0.0f,   // bottom right
    -0.5f, -0.5f, 0.0f,   0.0f, 0.0f, 1.0f,   0.0f, 0.0f,   // bottom left
    -0.5f,  0.5f, 0.0f,   1.0f, 1.0f, 0.0f,   0.0f, 1.0f    // top left
};
```

이렇게 되면 vertex attribute는 다음과 같아진다.

![alt text](/images/texture7.png)

이렇다면 각 attribute마다 보폭 (stride)는 32, 즉 `8 * sizeof(float)`가 된다. position, color, texture 모두 보폭을 설정해준다. (`glVertexAttribPointer`)

이제 버텍스 셰이더 코드를 수정하고 프래그먼트 셰이더에게 넘겨준다.

#### 버텍스 셰이더 수정

```cpp
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

이렇게 버텍스 셰이더에서 넘겨주면 프래그먼트 셰이더에서 `aTexCoord` 변수를 받는 것이다.

#### 프래그먼트 셰이더 수정 

```cpp
#version 330 core
out vec4 FragColor;
  
in vec3 ourColor;
in vec2 TexCoord;

uniform sampler2D ourTexture;

void main()
{
    FragColor = texture(ourTexture, TexCoord);
}
```

프래그먼트 셰이더는 텍스처 오브젝트에 접근해서 텍스처 이미지를 가져와야 한다. GLSL에는 텍스처 오브젝트를 가져오는 타입인 `sampler1D`, `sampler2D`, `sampler3D` 같은 타입이 존재한다. 2D 텍스처이므로 `sampler2D`를 사용하여 유니폼 변수로 `ourTexture`라는 변수를 선언해준다.

GLSL에서 `texture`라는 함수를 사용하여 좌표에 해당하는 텍스처에서 color를 샘플링한다. 결국 텍스처 좌표 (`TexCoord`)를 사용해 텍스처 (`ourTexture`)에서 색상을 가져와 픽셀에 적용한다. 여기서 말하는 픽셀은 우리가 보는 화면의 픽셀이다.

### 텍스처 유닛 (Texture Unit) 

텍스처 유닛은 텍스처가 저장되는 곳으로 셰이더에서 여러 개의 텍스처를 동시에 사용할 수 있도록 도와준다. 사용하려면 해당 텍스처 유닛을 바인딩 단계 이전에 활성화 시켜야 한다.

#### 텍스처 유닛 활성화 (glActiveTexture) 

```cpp
unsigned int texture;
glGenTextures(1, &texture); // 텍스처 객체 생성, ID 저장
.
..
...
glActiveTexture(GL_TEXTURE0); // 텍스처 유닛 활성화
glBindTexture(GL_TEXTURE_2D, texture); // 텍스처 바인딩
```

`glActiveTexture`로 텍스처 유닛을 활성화하면 이후의 `glBindTexture` 호출은 해당 텍스처 유닛에 텍스처를 바인딩한다. 기본적으로 `GL_TEXTURE0` 텍스처 유닛이 활성화되어 있기 때문에 이전 섹션에서는 `glActiveTexture`를 호출하지 않아도 문제가 없었다.

#### 여러 개의 텍스처 사용 

여러 텍스처를 사용하려면 프래그먼트 셰이더에 샘플러를 추가로 정의해야 한다. 예시는 다음과 같다.

```glsl
#version 330 core

uniform sampler2D texture1;
uniform sampler2D texture2; // 사용할 텍스처 2개!

void main()
{
    FragColor = mix(texture(texture1, TexCoord), texture(texture2, TexCoord), 0.2);
}
```

위 코드에서 `mix` 함수는 두 텍스처의 색상을 섞어준다. 세 번째 인자가 0.0이면 첫 번째 텍스처만, 1.0이면 두 번째 텍스처만 사용한다. 0.2를 넣으면 첫 번째 텍스처의 80%와 두 번째 텍스처의 20%가 섞인 결과를 반환한다.

텍스처 코드는 수정했고, 이제 다시 본 코드로 돌아가 텍스처를 하나 더 추가해준다. 예를 들어, `awesomeface.png` 이미지를 로드한다.

```cpp
unsigned char *data = stbi_load("awesomeface.png", &width, &height, &nrChannels, 0);
if (data)
{
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data);
    glGenerateMipmap(GL_TEXTURE_2D);
}
```

아래와 같은 코드를 사용해 두 텍스처를 각각의 텍스처 유닛에 바인딩한다.

```cpp
glActiveTexture(GL_TEXTURE0);
glBindTexture(GL_TEXTURE_2D, texture1);

glActiveTexture(GL_TEXTURE1);
glBindTexture(GL_TEXTURE_2D, texture2);

glBindVertexArray(VAO);
glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
```

그리고 셰이더의 샘플러가 어떤 텍스처 유닛과 연결되어있는지 알려줘야 한다. 그럴 땐 `glUniformli` 함수를 사용하여 샘플러 설정을 한다. 이건 렌더 루프 밖에서 한 번 해주면 된다.

#### 샘플러 설정 (glUniform1i 및 glUniformli) 

```cpp
ourShader.use(); // 유니폼을 설정하기 전에 셰이더를 활성화하는 것을 잊지 마세요!
glUniform1i(glGetUniformLocation(ourShader.ID, "texture1"), 0); // 수동으로 설정
ourShader.setInt("texture2", 1); // 또는 셰이더 클래스 사용

while(...)
{
    [...]
}
```

이렇게 하면 uniform sampler가 텍스처 유닛과 연결되어 아래와 같은 사진이 된다.

![alt text](/images/texture8.png)

### 이미지 뒤집힘 문제 해결 (stbi_set_flip_vertically_on_load) 

사진이 뒤집어져 있는데, 이는 OpenGL이 y축에서 0.0 좌표를 이미지의 하단에 위치시키기를 기대하는 반면에 보통 이미지에서는 0.0이 상단에 위치하기 때문에 그렇다. 그래서 `stb_image.h`는 이미지를 로드할 때 y축을 뒤집을 수 있는 기능을 제공한다. 아래와 같은 코드를 추가한다.

```cpp
stbi_set_flip_vertically_on_load(true); // y축 뒤집기 명령임.
```

### 최종 결과

![alt text](/images/texture9.png)

---
