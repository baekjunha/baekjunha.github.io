---
categories: [Graphics]
tags: [graphics, opengl, shader, class, cpp]
math: true 
---

## 요약
> **요약**: 매번 C++ 소스 코드 최상단에 지저분하게 하드코딩했던 셰이더 문자열을 제거하고, 외부 `.vs`, `.fs` 파일에서 동적으로 셰이더 코드를 읽어 들여 컴파일 및 링크까지 한 번에 처리해 주는 모듈화된 `Shader` 클래스 구축 과정을 다룬다.

## 목차
* TOC
{:toc}

---

## 1. Shader 클래스의 등장 배경

**자료 출처**: [LearnOpenGL](https://learnopengl.com/)

초기 튜토리얼에서는 버텍스/프래그먼트 셰이더 코드를 C++ `main.cpp` 상단에 `const char*` 형태의 거대한 문자열 텍스트로 저장하고 컴파일을 진행했다. 이 방식은 셰이더 코드가 몇 줄 안 될 때는 유효하지만, 로직이 복잡해질수록 코드 가독성을 저해한다.

매 프레임마다 `glCreateShader`, `glShaderSource`, `glCompileShader`, `glCreateProgram`, `glAttachShader`, `glLinkProgram` 같은 원시(Raw) OpenGL C API를 반복해서 작성하는 것 또한 비효율적이다.

따라서 셰이더 코드를 별도의 파일(`*.vs`, `*.fs`)로 분리하여 저장하고, 이 파일의 경로만 인자로 넘겨주면 **파일 입출력(File I/O) → 파싱 → 컴파일 → 프로그램 링크 → 에러 핸들링**까지 한 번에 처리해 주는 객체 지향 C++ 클래스를 설계해 보았다.

---

## 2. Shader 클래스 기초 설계

### 2.1. 헤더 가드 및 전처리

먼저 단일 헤더 파일 `Shader.h`의 구조를 잡는다.

```cpp
#ifndef SHADER_H
#define SHADER_H

#include <glad/glad.h>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>
```
{: file="Shader.h" }

*   **`#ifndef SHADER_H`**: 동일한 헤더가 여러 번 `#include` 되어 중복 정의 오류가 발생하는 것을 방지하는 헤더 가드다.
*   **`<glad/glad.h>`**: OpenGL 함수 포인터들을 매핑하기 위한 코어 헤더다.
*   **`<fstream>`, `<sstream>`**: 파일을 읽어 메모리에 적재하기 위한 C++ 표준 입출력 라이브러리다.

### 2.2. 클래스 명세 (Interface)

```cpp
class Shader
{
public:
    // OpenGL이 관리하는 셰이더 프로그램의 고유 식별자(ID)
    unsigned int ID;
    
    // 생성자: 버텍스 및 프래그먼트 셰이더 파일 경로를 인자로 받음
    Shader(const char* vertexPath, const char* fragmentPath);
    
    // 셰이더 활성화
    void use();
    
    // 런타임에 유니폼(Uniform) 변수를 설정하는 유틸리티 함수들
    void setBool(const std::string &name, bool value) const;
    void setInt(const std::string &name, int value) const;
    void setFloat(const std::string &name, float value) const;
};

#endif
```
{: file="Shader.h" }

`ID` 멤버 변수는 생성된 셰이더 프로그램을 식별하기 위한 고유 핸들이다.

---

## 3. Shader 생성자: 파일 로드 및 컴파일 (Implementation)

C++ 클래스와 스트림을 활용해 생성자 내부 로직을 구현한다.

### 3.1. 디스크에서 셰이더 소스코드 읽기

```cpp
Shader(const char* vertexPath, const char* fragmentPath)
{
    // 1. 파일에서 소스 코드를 읽어올 string 컨테이너
    std::string vertexCode;
    std::string fragmentCode;
    std::ifstream vShaderFile;
    std::ifstream fShaderFile;

    // ifstream 객체가 에러 발생 시 예외를 던지도록 설정
    vShaderFile.exceptions (std::ifstream::failbit | std::ifstream::badbit);
    fShaderFile.exceptions (std::ifstream::failbit | std::ifstream::badbit);

    try 
    {
        // 셰이더 파일 열기
        vShaderFile.open(vertexPath);
        fShaderFile.open(fragmentPath);
        std::stringstream vShaderStream, fShaderStream;

        // 파일 버퍼의 내용을 스트림으로 읽어들임
        vShaderStream << vShaderFile.rdbuf();
        fShaderStream << fShaderFile.rdbuf();

        // 스트림 닫기
        vShaderFile.close();
        fShaderFile.close();

        // 스트림 내용을 std::string으로 변환
        vertexCode   = vShaderStream.str();
        fragmentCode = fShaderStream.str();
    }
    catch (std::ifstream::failure& e)
    {
        std::cout << "ERROR::SHADER::FILE_NOT_SUCCESFULLY_READ: " << e.what() << std::endl;
    }
    
    // OpenGL API에 전달하기 위해 C 스타일 문자열로 변환
    const char* vShaderCode = vertexCode.c_str();
    const char * fShaderCode = fragmentCode.c_str();
```
{: file="Shader.h" }

> [!warning] 
> `c_str()`로 반환된 포인터는 `std::string` 객체의 수명과 연동되므로 주의해야 한다. 소스 코드를 OpenGL로 전달하기 전까지 데이터가 유지되어야 한다.

### 3.2. 셰이더 런타임 컴파일

```c++
unsigned int vertex;
vertex = glCreateShader(GL_VERTEX_SHADER);
glShaderSource(vertex, 1, &vShaderCode, NULL);
glCompileShader(vertex);
checkCompileErrors(vertex, "VERTEX");
```

*   `glCreateShader(GL_VERTEX_SHADER)`: 버텍스 셰이더 객체를 생성한다.
*   `glShaderSource()`: 셰이더 소스 코드를 연결한다.
*   `glCompileShader()`: 셰이더를 컴파일한다.
*   `checkCompileErrors()`: 컴파일 오류를 체크한다.

### 3.프래그먼트 셰이더 컴파일

읽어 들인 소스를 바탕으로 프래그먼트 셰이더를 컴파일한다.

```cpp
    // 2. 셰이더 컴파일
    unsigned int vertex, fragment;

    // 버텍스 셰이더 생성 및 컴파일
    vertex = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertex, 1, &vShaderCode, NULL);
    glCompileShader(vertex);
    checkCompileErrors(vertex, "VERTEX"); 

    // 프래그먼트 셰이더 생성 및 컴파일
    fragment = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragment, 1, &fShaderCode, NULL);
    glCompileShader(fragment);
    checkCompileErrors(fragment, "FRAGMENT");
```
{: file="Shader.h" }

반복적인 코드를 모듈화하여 해결했다.

### 3.3. 프로그램 링크 및 메모리 정리

두 셰이더를 링크하여 최종 프로그램을 생성한다.

```cpp
    // 3. 셰이더 프로그램 링크
    ID = glCreateProgram();
    glAttachShader(ID, vertex);
    glAttachShader(ID, fragment);
    glLinkProgram(ID);
    checkCompileErrors(ID, "PROGRAM");

    // 링크 완료 후에는 개별 셰이더 객체가 필요 없으므로 삭제
    glDeleteShader(vertex);
    glDeleteShader(fragment);
} // 생성자 끝
```
{: file="Shader.h" }

---

## 4. 유틸리티 메서드 구현

클래스에 렌더링 루프에서 호출할 수 있는 유틸리티 메서드들을 추가한다.

### 4.1. 셰이더 활성화 (Use)

```cpp
void use() 
{ 
    // 생성된 셰이더 프로그램을 활성화
    glUseProgram(ID); 
}
```
{: file="Shader.h" }

### 4.2. 유니폼(Uniform) 갱신 세터

> [!note] 
> **유니폼 변수란?**  
> 셰이더 내부의 `uniform` 변수는 CPU에서 GPU 셰이더로 데이터를 전달하는 핵심 통로다. 프레임마다 변하는 동적 데이터를 주입하는 데 활용된다.

```cpp
void setBool(const std::string &name, bool value) const
{         
    // 유니폼 변수의 위치를 찾은 뒤 값을 주입
    glUniform1i(glGetUniformLocation(ID, name.c_str()), (int)value); 
}

void setInt(const std::string &name, int value) const
{ 
    glUniform1i(glGetUniformLocation(ID, name.c_str()), value); 
}

void setFloat(const std::string &name, float value) const
{ 
    glUniform1f(glGetUniformLocation(ID, name.c_str()), value); 
}
```
{: file="Shader.h" }

### 4.3. 컴파일/링크 에러 감지기

컴파일 과정에서 발생한 오류를 콘솔에 출력하여 디버깅을 돕는다.

```cpp
private:
    void checkCompileErrors(unsigned int shader, std::string type)
    {
        int success;
        char infoLog[1024];

        if (type != "PROGRAM") // 개별 셰이더 컴파일 오류 체크
        {
            glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
            if (!success)
            {
                glGetShaderInfoLog(shader, 1024, NULL, infoLog);
                std::cout << "ERROR::SHADER_COMPILATION_ERROR of type: " << type << "\n" << infoLog << "\n -- --------------------------------------------------- -- " << std::endl;
            }
        }
        else // 프로그램 링크 오류 체크
        {
            glGetProgramiv(shader, GL_LINK_STATUS, &success);
            if (!success)
            {
                glGetProgramInfoLog(shader, 1024, NULL, infoLog);
                std::cout << "ERROR::PROGRAM_LINKING_ERROR of type: " << type << "\n" << infoLog << "\n -- --------------------------------------------------- -- " << std::endl;
            }
        }
    }
```
{: file="Shader.h" }

---

## 5. 실전 적용 예시

준비가 완료되었으므로 `main.cpp`에서 복잡한 셰이더 코드를 제거할 수 있다.

```cpp
// 기존의 하드코딩된 소스 코드는 더 이상 필요하지 않다.
const char *vertexShaderSource = "#version 330 core\n"
    "layout (location = 0) in vec3 aPos;\n"
    "void main()\n"
    "{\n"
    "   gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);\n"
    "}\0";
```

대신 파일 경로를 통해 클래스를 인스턴스화한다.

```cpp
// 파일로부터 셰이더를 읽어와 컴파일 및 링크를 자동으로 수행한다.
Shader ourShader("3.3.shader.vs", "3.3.shader.fs"); 

// ... 렌더링 루프 ...

// 셰이더 활성화
ourShader.use();
// 유니폼 변수 설정
ourShader.setFloat("someUniformOffset", timeValue);
```
{: file="main.cpp" }

이러한 모듈화를 통해 더욱 체계적인 그래픽스 프로그래밍이 가능해졌다.
