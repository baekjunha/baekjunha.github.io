---
categories: graphics
tags: [graphics, opengl, shader, class, cpp]
toc: true
toc_sticky: true
author_profile: false
use_math: true 
---

# Shader 클래스: OpenGL 셰이더 관리  

**자료 출처**: [LearnOpenGL](https://learnopengl.com/)

이전에는 소스 코드에 셰이더 코드를 직접 문자열로 작성하고, 컴파일, 링크 과정을 모두 직접 처리해야 했다.(glCreateShader, glShaderSource, glCompileShader, glCreateProgram, glAttachShader, glLinkProgram 같은 OpenGL API를 매번 호출해야 해서 번거로웠다.) 하지만 셰이더 클래스를 사용하면 코드 양을 줄이고 번거로운 작업을 간소화할 수 있다.

이 Shader 클래스는 OpenGL에서 버텍스 셰이더와 프래그먼트 셰이더를 로드하고 컴파일하여 하나의 셰이더 프로그램으로 연결하는 역할을 한다. 셰이더를 효율적으로 관리하는 데 도움을 주는 클래스라고 할 수 있다.

## 코드 설명

### 1. 헤더 가드 

```c++
#ifndef SHADER_H
#define SHADER_H
...
#endif
```

*   `SHADER_H`가 정의되지 않았을 때만 이 파일의 내용을 포함하도록 하는 헤더 가드다.
*   동일한 파일이 여러 번 포함되는 것을 방지한다.

### 2. 필요한 라이브러리 포함 

```c++
#include <glad/glad.h>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
```

*   `glad/glad.h`: OpenGL 기능을 사용하기 위해 포함한다.
*   `<string>`: 문자열(`std::string`) 처리를 위해 포함한다.
*   `<fstream>`: 파일 입출력(`std::ifstream`)을 위해 포함한다.
*   `<sstream>`: 파일 내용을 문자열로 변환하기 위해 포함한다.
*   `<iostream>`: 디버깅을 위한 출력 (`std::cout`)을 위해 포함한다.

### 3. Shader 클래스 정의

```c++
class Shader
{
public:
    unsigned int ID;
    ...
};
```

*   Shader 클래스를 정의한다. `ID`는 셰이더 프로그램의 ID를 저장하는 멤버 변수다.
*   OpenGL에서는 셰이더 프로그램이 하나의 숫자 ID로 관리되므로, 이를 저장한다.

### 셰이더 생성 과정 (Shader 생성자)

```c++
Shader(const char* vertexPath, const char* fragmentPath)
```

이 생성자는 두 개의 파일 경로(버텍스 셰이더, 프래그먼트 셰이더)를 받아 셰이더를 로드하고 컴파일하며 프로그램으로 연결한다.

### 1.셰이더 파일 읽기

```c++
std::string vertexCode;
std::string fragmentCode;
std::ifstream vShaderFile;
std::ifstream fShaderFile;
```

*   `vertexCode`, `fragmentCode`: 셰이더 파일 내용을 저장할 문자열이다.
*   `vShaderFile`, `fShaderFile`: 파일 스트림 객체다.

```c++
vShaderFile.exceptions (std::ifstream::failbit | std::ifstream::badbit);
fShaderFile.exceptions (std::ifstream::failbit | std::ifstream::badbit);
```

*   파일을 읽을 때 예외 처리를 활성화한다. 파일이 없거나 읽기 실패 시 오류가 발생한다. (try-catch 블록을 사용하여 예외를 처리하는 코드를 추가하면 더욱 안정적인 코드가 된다.)

```c++
vShaderFile.open(vertexPath);
fShaderFile.open(fragmentPath);
std::stringstream vShaderStream, fShaderStream;
vShaderStream << vShaderFile.rdbuf();
fShaderStream << fShaderFile.rdbuf();
```

*   파일을 열고 내용을 stringstream에 저장한 후, 문자열로 변환한다.

```c++
vertexCode = vShaderStream.str();
fragmentCode = fShaderStream.str();

const char* vShaderCode = vertexCode.c_str();
const char* fShaderCode = fragmentCode.c_str();
```

*   stringstream의 내용을 std::string으로 변환한다.
*   OpenGL은 `std::string`을 직접 처리하지 못하므로 C 스타일 문자열(`char*`)로 변환한다. (`vShaderCode`와 `fShaderCode`는 `vertexCode`와 `fragmentCode` 객체의 내부 버퍼를 가리키는 포인터다. `vertexCode`와 `fragmentCode` 객체가 소멸되면 이 포인터는 더 이상 유효하지 않게 된다는 점에 유의해야 한다.)

### 2.버텍스 셰이더 컴파일

```c++
unsigned int vertex;
vertex = glCreateShader(GL_VERTEX_SHADER);
glShaderSource(vertex, 1, &vShaderCode, NULL);
glCompileShader(vertex);
checkCompileErrors(vertex, "VERTEX");
```

*   `glCreateShader(GL_VERTEX_SHADER)`: 버텍스 셰이더 객체를 생성한다.
*   `glShaderSource()`: 셰이더 소스 코드를 설정한다.
*   `glCompileShader()`: 셰이더를 컴파일한다.
*   `checkCompileErrors()`: 컴파일 오류를 확인한다.

### 3.프래그먼트 셰이더 컴파일

```c++
unsigned int fragment;
fragment = glCreateShader(GL_FRAGMENT_SHADER);
glShaderSource(fragment, 1, &fShaderCode, NULL);
glCompileShader(fragment);
checkCompileErrors(fragment, "FRAGMENT");
```

*   버텍스 셰이더와 동일한 방식으로 프래그먼트 셰이더를 컴파일한다.

### 4.셰이더 프로그램 생성 및 링크

```c++
ID = glCreateProgram();
glAttachShader(ID, vertex);
glAttachShader(ID, fragment);
glLinkProgram(ID);
checkCompileErrors(ID, "PROGRAM");
```

*   `glCreateProgram()`: 셰이더 프로그램을 생성한다.
*   `glAttachShader()`: 버텍스, 프래그먼트 셰이더를 프로그램에 추가한다.
*   `glLinkProgram()`: 셰이더들을 하나의 프로그램으로 연결한다.
*   `checkCompileErrors()`: 링크 오류를 확인한다.

```c++
glDeleteShader(vertex);
glDeleteShader(fragment);
```

*   셰이더 객체를 삭제한다. (프로그램에 이미 연결되었으므로 더 이상 필요하지 않다.)

### 셰이더 사용 (use() 메서드)

```c++
void use() 
{ 
    glUseProgram(ID); 
}
```

*   OpenGL에서 이 셰이더 프로그램을 사용하도록 설정한다.
*   `glUseProgram(ID)`를 호출하면, 이후의 렌더링은 이 셰이더를 사용하게 된다.

### 셰이더의 유니폼 변수 설정 (setBool, setInt, setFloat)

유니폼 변수란?

*   uniform 변수는 셰이더 내부에서 전역적으로 설정할 수 있는 변수다.
*   CPU에서 값을 설정하면, GPU에서 해당 값을 사용한다.

```c++
void setBool(const std::string &name, bool value) const
{         
    glUniform1i(glGetUniformLocation(ID, name.c_str()), (int)value); 
}
```

*   `glGetUniformLocation(ID, name.c_str())`: 유니폼 변수의 위치를 찾는다.
*   `glUniform1i()`: 불리언 값을 정수(0 또는 1)로 변환하여 설정한다.

```c++
void setInt(const std::string &name, int value) const
{ 
    glUniform1i(glGetUniformLocation(ID, name.c_str()), value); 
}
```

*   `glUniform1i()`: 정수 값을 설정한다.

```c++
void setFloat(const std::string &name, float value) const
{ 
    glUniform1f(glGetUniformLocation(ID, name.c_str()), value); 
}
```

*   `glUniform1f()`: 실수 값을 설정한다.

### 셰이더 오류 확인 (checkCompileErrors 메서드)

```c++
void checkCompileErrors(unsigned int shader, std::string type)
{
    int success;
    char infoLog[1024];
    if (type != "PROGRAM")
    {
        glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
        if (!success)
        {
            glGetShaderInfoLog(shader, 1024, NULL, infoLog);
            std::cout << "ERROR::SHADER_COMPILATION_ERROR of type: " << type << "\n" << infoLog << std::endl;
        }
    }
    else
    {
        glGetProgramiv(shader, GL_LINK_STATUS, &success);
        if (!success)
        {
            glGetProgramInfoLog(shader, 1024, NULL, infoLog);
            std::cout << "ERROR::PROGRAM_LINKING_ERROR of type: " << type << "\n" << infoLog << std::endl;
        }
    }
}
```

*   컴파일 오류를 확인한다 (`glGetShaderiv`).
*   에러 메시지를 출력한다 (`glGetShaderInfoLog`).
*   링크 오류를 확인한다 (`glGetProgramiv`).

### 정리

이 Shader 클래스는 셰이더 파일을 불러와서 OpenGL에서 사용할 수 있도록 준비하는 역할을 한다.

*   셰이더 파일 읽기 → 컴파일 → 링크 → 사용 가능
*   `use()`를 호출하면 셰이더 프로그램을 활성화할 수 있다.
*   `setBool()`, `setInt()`, `setFloat()`로 셰이더 유니폼 변수를 설정할 수 있다.

이제 이 클래스를 이용하면 복잡한 셰이더 관리를 더욱 쉽게 할 수 있다.


### 코드 예시

```cpp
Shader ourShader("3.3.shader.vs", "3.3.shader.fs"); 
```

이 코드는 Shader 클래스의 생성자를 호출하여 ourShader 객체를 초기화한다.  
Shader 클래스의 생성자는 주어진 파일 경로("3.3.shader.vs", "3.3.shader.fs")에서 버텍스 셰이더와 프래그먼트 셰이더의 소스 코드를 읽어온다.  
읽어온 소스 코드를 OpenGL에게 전달하여 버텍스 셰이더와 프래그먼트 셰이더를 컴파일한다.  
컴파일된 셰이더들을 하나의 셰이더 프로그램으로 연결(linking)한다.  
만약 컴파일 또는 링크 과정에서 오류가 발생하면, 오류 메시지를 출력한다.  
최종적으로, ourShader 객체는 컴파일 및 링크된 셰이더 프로그램을 관리하는 데 사용될 수 있다.  
예를 들어, ourShader.use()를 호출하여 셰이더 프로그램을 활성화하거나, ourShader.setFloat()를 호출하여 셰이더의 uniform 변수 값을 설정할 수 있다.  

