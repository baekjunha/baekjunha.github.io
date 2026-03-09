---
categories: [graphics]
tags: [graphics, opengl, shader, class, cpp]
math: true 
image:
  path: https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTf6c44cGdSVe9jPWgeQWwXyCdwjADxP6NrLA&s
---

> **요약**: 매번 C++ 소스 코드 최상단에 지저분하게 하드코딩했던 셰이더 문자열을 제거하고, 외부 `.vs`, `.fs` 파일에서 동적으로 셰이더 코드를 읽어 들여 컴파일 및 링크까지 한 번에 처리해 주는 모듈화된 `Shader` 클래스 구축 과정을 다룬다.
{: .prompt-info }

## 목차
* TOC
{:toc}

---

## 1. Shader 클래스의 등장 배경

**자료 출처**: [LearnOpenGL](https://learnopengl.com/)

초기 튜토리얼에서는 버텍스/프래그먼트 셰이더 코드를 C++ `main.cpp` 상단에 `const char*` 형태의 거대한 문자열 텍스트로 박아두고 컴파일을 진행했다. 이 방식은 셰이더 코드가 몇 줄 안 될 때는 버틸만하지만, 로직이 복잡해질수록 코드 가독성을 나락으로 떨어뜨린다.

매 프레임마다 `glCreateShader`, `glShaderSource`, `glCompileShader`, `glCreateProgram`, `glAttachShader`, `glLinkProgram` 같은 원시(Raw) OpenGL C API를 중복해서 타이핑하는 것 또한 엄청난 노동 낭비다.

따라서 셰이더 코드를 별도의 파일(`*.vs`, `*.fs`)로 분리 저장하고, 이 파일의 절대 경로만 넘겨주면 알아서 **파일 입출력(File I/O) → 파싱 → 컴파일 → 프로그램 링크 → 에러 핸들링**까지 원스톱으로 처리해 주는 객체 지향 C++ Wrapper 클래스를 설계할 것이다.

---

## 2. Shader 클래스 기초 설계

### 2.1. 헤더 가드 및 전처리

먼저 단일 헤더 파일 `Shader.h` 뼈대를 구축한다.

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

*   **`#ifndef SHADER_H`**: 동일한 헤더가 여러 번 `#include` 되어 중복 정의 선언(Multiple Definition) 컴파일 에러가 터지는 것을 막아주는 전통적인 헤더 가드다.
*   **`<glad/glad.h>`**: OpenGL 함수 포인터들을 매핑하기 위한 코어 헤더다.
*   **`<fstream>`, `<sstream>`**: 하드디스크에 저장된 셰이더 텍스트 파일을 스트림으로 퍼올려 메모리에 적재하기 위한 C++ 표준 입출력 라이브러리다.

### 2.2. 클래스 명세 (Interface)

```cpp
class Shader
{
public:
    // OpenGL이 관리하는 셰이더 프로그램의 고유 상태 식별자(ID)
    unsigned int ID;
    
    // 생성자: 버텍스 및 프래그먼트 셰이더 파일 경로를 인자로 받음
    Shader(const char* vertexPath, const char* fragmentPath);
    
    // 셰이더 활성화
    void use();
    
    // 런타임에 유니폼(Uniform) 변수를 찔러넣는 유틸리티 함수들
    void setBool(const std::string &name, bool value) const;
    void setInt(const std::string &name, int value) const;
    void setFloat(const std::string &name, float value) const;
};

#endif
```
{: file="Shader.h" }

`ID` 멤버 변수는 수많은 셰이더 프로그램 중 이 객체가 쥐고 있는 고유한 핸들 번호표다.

---

## 3. Shader 생성자: 파일 로드 및 컴파일 (Implementation)

C++ 클래스와 파일 I/O 스트림의 강력함을 활용해 생성자 블록 `Shader(...)` 내부 로직을 채워보자.

### 3.1. 디스크에서 셰이더 소스코드 읽기

```cpp
Shader(const char* vertexPath, const char* fragmentPath)
{
    // 1. 파일에서 소스 코드를 읽어올 string 컨테이너
    std::string vertexCode;
    std::string fragmentCode;
    std::ifstream vShaderFile;
    std::ifstream fShaderFile;

    // ifstream 객체가 에러 발생 시 C++ 예외(Exception)를 던지도록 설정
    vShaderFile.exceptions (std::ifstream::failbit | std::ifstream::badbit);
    fShaderFile.exceptions (std::ifstream::failbit | std::ifstream::badbit);

    try 
    {
        // 셰이더 파일 열기
        vShaderFile.open(vertexPath);
        fShaderFile.open(fragmentPath);
        std::stringstream vShaderStream, fShaderStream;

        // 파일 버퍼의 텍스트 스트림을 stringstream 메모리 버퍼로 몽땅 덤프
        vShaderStream << vShaderFile.rdbuf();
        fShaderStream << fShaderFile.rdbuf();

        // 스트림 닫기
        vShaderFile.close();
        fShaderFile.close();

        // 스트림 버퍼를 완전한 std::string 인스턴스로 복사 변환
        vertexCode   = vShaderStream.str();
        fragmentCode = fShaderStream.str();
    }
    catch (std::ifstream::failure& e)
    {
        std::cout << "ERROR::SHADER::FILE_NOT_SUCCESFULLY_READ: " << e.what() << std::endl;
    }
    
    // OpenGL C API 함수들은 std::string을 먹지 못하므로, Raw C 문자열(char*) 포인터로 환원
    const char* vShaderCode = vertexCode.c_str();
    const char * fShaderCode = fragmentCode.c_str();
```
{: file="Shader.h" }

> [!warning] 
> `c_str()`로 얻어낸 포인터는 원본 `std::string` 내장 버퍼를 가리키므로 메모리 라이프사이클에 각별히 유의해야 한다. 다행히 이 코드 블록을 벗어나 단기간 휘발되기 전, OpenGL 메모리에 소스를 모두 복사해 두기 때문에 안전하다.

### 3.2. 셰이더 런타임 컴파일

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

읽어 들인 포인터 소스를 바탕으로 GPU에 하사할 셰이더를 실시간 빌드한다.

```cpp
    // 2. 셰이더 컴파일
    unsigned int vertex, fragment;

    // 버텍스 셰이더 생성 및 소스 바인딩 후 컴파일
    vertex = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertex, 1, &vShaderCode, NULL);
    glCompileShader(vertex);
    checkCompileErrors(vertex, "VERTEX"); // 하단 유틸리티 함수 배치

    // 프래그먼트 셰이더 생성 및 소스 바인딩 후 컴파일
    fragment = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragment, 1, &fShaderCode, NULL);
    glCompileShader(fragment);
    checkCompileErrors(fragment, "FRAGMENT");
```
{: file="Shader.h" }

수백 줄의 타이핑 노가다가 깔끔한 모듈로 압축되었다.

### 3.3. 프로그램 링크 및 메모리 정리

양쪽 셰이더 병합 링크 작업까지 완료해야 최종 ID가 발급된다.

```cpp
    // 3. 셰이더 프로그램 융합 (Link)
    ID = glCreateProgram();
    glAttachShader(ID, vertex);
    glAttachShader(ID, fragment);
    glLinkProgram(ID);
    checkCompileErrors(ID, "PROGRAM");

    // 영구적인 프로그램 바이너리로 굳어졌으므로, 개별 셰이더 객체는 메모리 낭비를 잡기 위해 즉각 파기
    glDeleteShader(vertex);
    glDeleteShader(fragment);
} // 생성자 끝
```
{: file="Shader.h" }

---

## 4. 유틸리티 메서드 구현

클래스 하단에는 렌더 루프(`while`) 내부에서 밥 먹듯이 호출될 제어 편의 메서드들을 마저 구현해 준다.

### 4.1. 셰이더 활성화 (Use)

```cpp
void use() 
{ 
    // 이 객체가 감싸고 있는 셰이더 프로그램을 GPU 파이프라인의 현재 상태로 올려 장착
    glUseProgram(ID); 
}
```
{: file="Shader.h" }

### 4.2. 유니폼(Uniform) 갱신 세터

> [!note] 
> **유니폼 변수란?**  
> 셰이더 내부의 `uniform` 키워드 변수는, CPU 영역(C++ 앱)에서 GPU 셰이더 메모리로 직통 데이터를 꽂아 넣을 수 있는 전역 읽기 전용 통로다. 시간에 따른 애니메이션이나 행렬 변환 등 매 프레임 변하는 동적 데이터를 주입할 때 쓴다.

```cpp
void setBool(const std::string &name, bool value) const
{         
    //glGetUniformLocation으로 메모리 주소를 딴 뒤, glUniform1i로 불리언(을 정수화한) 값을 주입
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

생성자에서 컴파일 실패 시 콘솔 창에 친절하게 어느 파일의 몇 번째 줄에서 오타가 났는지 뿌려주는 오류 확인 파서다. 그래픽스 프로그래밍에서 디버깅 생명줄과도 같다.

```cpp
private:
    void checkCompileErrors(unsigned int shader, std::string type)
    {
        int success;
        char infoLog[1024];

        if (type != "PROGRAM") // 개별 셰이더 컴파일 에러
        {
            glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
            if (!success)
            {
                glGetShaderInfoLog(shader, 1024, NULL, infoLog);
                std::cout << "ERROR::SHADER_COMPILATION_ERROR of type: " << type << "\n" << infoLog << "\n -- --------------------------------------------------- -- " << std::endl;
            }
        }
        else // 최종 프로그램 링크 에러
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

모든 준비가 끝났다. `main.cpp` 최상단에서 이렇게 지저분한 코드는 모두 제거하고,

```cpp
// 이제 이 지옥 같은 하드코딩 볼륨은 영원히 안녕이다.
const char *vertexShaderSource = "#version 330 core\n"
    "layout (location = 0) in vec3 aPos;\n"
    "void main()\n"
    "{\n"
    "   gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);\n"
    "}\0";
```

딱 한 줄 인스턴스화로 교체하면 끝이다.

```cpp
// 객체 생성 순간 내부 로직이 돌아가 파일 I/O부터 컴파일, 링크 지옥이 알아서 원큐에 해결됨
Shader ourShader("3.3.shader.vs", "3.3.shader.fs"); 

// ... 렌더링 영역 ...

// 루프 돌기전에 사용할 셰이더 장착
ourShader.use();
// 유니폼 변수로 시간 오프셋값 주입
ourShader.setFloat("someUniformOffset", timeValue);
```
{: file="main.cpp" }

이 모듈화 덕분에 우리는 그래픽스 엔진을 한 차원 더 고도화할 튼튼한 객체 지향적 기반을 마련했다.
