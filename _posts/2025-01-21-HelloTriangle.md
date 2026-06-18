---
categories: [Graphics]
tags: [graphics, opengl, tutorial]
math: true
---

## 요약
> **요약**: 그래픽스 파이프라인의 핵심인 삼각형 렌더링을 위해 필요한 필수 요소(VBO/EBO, 셰이더 프로그램, 속성 연결)와 전반적인 프로세스를 상세히 기술한다.

## 목차
* TOC
{:toc}

> 💡 **OpenGL 기초 학습 시리즈**
>
> 1. [OpenGL 시작하기 — GLFW, GLAD 초기화](/posts/StartOpenGL/)
> 2. 📌 **[현재 글] Hello Triangle — 삼각형 렌더링 기초 (VBO, EBO, 셰이더)**
> 3. [Hello Triangle 2 — 그래픽 파이프라인 심화](/posts/HelloTriangle2/)
> 4. [Hello Shader — 셰이더 구조와 데이터 흐름](/posts/HelloShader/)
> 5. [Hello Texture — 텍스처 매핑과 필터링](/posts/HelloTexture/)
> 6. [GPU 데이터 플로우 — CPU→GPU 렌더링 흐름 분석](/posts/gpu-dataflow-texture/)
> 7. [Shader Class — 셰이더 모듈화](/posts/ShaderClass/)
> 8. [GLM — 벡터/행렬 수학 라이브러리](/posts/HelloGLM/)
> 9. [좌표계 변환 — Local→Screen 5단계](/posts/CoordinateSystem/)
> 10. [카메라 (1) — 정의와 구성](/posts/camera/)
> 11. [카메라 (2) — 이동과 시점 전환](/posts/camera2/)
> 12. [카메라 (3) — FPS 시점 제어와 클래스화](/posts/camera3/)
{: .prompt-info }

---

<div class="webgl-demo-container" style="text-align: center; margin: 2.5rem 0; padding: 1.5rem; background: var(--card-bg); border-radius: 12px; box-shadow: var(--card-shadow); border: 1px solid var(--main-border-color);">
  <h4 style="margin-top: 0; color: var(--heading-color);">🎮 실시간 WebGL 데모: Hello Triangle</h4>
  <p style="font-size: 0.9em; color: var(--text-muted-color); margin-bottom: 1rem;">캔버스를 클릭하면 삼각형의 각 꼭짓점 색상이 무작위로 변경되고 보간(Interpolation)됩니다!</p>
  <canvas id="glcanvas" width="400" height="400" style="max-width: 100%; height: auto; border-radius: 8px; background: #1a1a1c; cursor: pointer; border: 1px solid #333;"></canvas>
</div>

<script>
document.addEventListener("DOMContentLoaded", function() {
  const canvas = document.querySelector("#glcanvas");
  if (!canvas) return;
  const gl = canvas.getContext("webgl");

  if (!gl) {
    console.error("WebGL is not supported");
    return;
  }

  const vsSource = `
    attribute vec4 aVertexPosition;
    attribute vec4 aVertexColor;
    varying lowp vec4 vColor;
    void main(void) {
      gl_Position = aVertexPosition;
      vColor = aVertexColor;
    }
  `;

  const fsSource = `
    varying lowp vec4 vColor;
    void main(void) {
      gl_FragColor = vColor;
    }
  `;

  function initShaderProgram(gl, vsSource, fsSource) {
    const vertexShader = loadShader(gl, gl.VERTEX_SHADER, vsSource);
    const fragmentShader = loadShader(gl, gl.FRAGMENT_SHADER, fsSource);
    const shaderProgram = gl.createProgram();
    gl.attachShader(shaderProgram, vertexShader);
    gl.attachShader(shaderProgram, fragmentShader);
    gl.linkProgram(shaderProgram);
    if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) return null;
    return shaderProgram;
  }

  function loadShader(gl, type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      gl.deleteShader(shader);
      return null;
    }
    return shader;
  }

  const shaderProgram = initShaderProgram(gl, vsSource, fsSource);
  const programInfo = {
    program: shaderProgram,
    attribLocations: {
      vertexPosition: gl.getAttribLocation(shaderProgram, 'aVertexPosition'),
      vertexColor: gl.getAttribLocation(shaderProgram, 'aVertexColor'),
    },
  };

  let colors = [
    1.0, 0.0, 0.0, 1.0,
    0.0, 1.0, 0.0, 1.0,
    0.0, 0.0, 1.0, 1.0,
  ];

  function drawScene() {
    gl.clearColor(0.1, 0.1, 0.1, 1.0);
    gl.clear(gl.COLOR_BUFFER_BIT);

    const positions = [
       0.0,  0.6,
      -0.6, -0.6,
       0.6, -0.6,
    ];

    const positionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(positions), gl.STATIC_DRAW);

    const colorBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(colors), gl.STATIC_DRAW);

    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    gl.vertexAttribPointer(programInfo.attribLocations.vertexPosition, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(programInfo.attribLocations.vertexPosition);

    gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
    gl.vertexAttribPointer(programInfo.attribLocations.vertexColor, 4, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(programInfo.attribLocations.vertexColor);

    gl.useProgram(programInfo.program);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  }

  drawScene();

  canvas.addEventListener('click', () => {
    colors = [
      Math.random(), Math.random(), Math.random(), 1.0,
      Math.random(), Math.random(), Math.random(), 1.0,
      Math.random(), Math.random(), Math.random(), 1.0,
    ];
    drawScene();
  });
});
</script>

**자료 출처**: [LearnOpenGL](https://learnopengl.com/)

그래픽스 파이프라인에서 삼각형을 렌더링하기 위한 과정은 다음과 같은 3가지 핵심 요소로 요약할 수 있다.

## 1. 정점 데이터 관리 (VBO, EBO)
*   **VBO (Vertex Buffer Object)**: GPU 메모리에 정점 데이터를 저장하는 객체다. 위치, 색상 등 3D 모델 구성을 위한 기초 데이터를 포함한다.
*   **EBO (Element Buffer Object)**: 인덱스 데이터를 관리하며, 정점의 중복 사용을 방지하여 효율적인 렌더링을 가능하게 한다.
*   `glGenBuffers`와 `glBindBuffer`를 통해 GPU 메모리에 데이터를 할당하고 업로드한다.

## 2. 셰이더 프로그램 (Vertex & Fragment Shader)
*   **버텍스 셰이더(Vertex Shader)**: 각 정점의 속성을 처리하며, 좌표 변환(Model, View, Projection)을 통해 정점의 최종 위치를 결정한다.
*   **프래그먼트 셰이더(Fragment Shader)**: 래스터화된 각 픽셀의 최종 색상을 계산하며, 텍스처링 및 조명 계산이 포함된다.
*   개별 셰이더를 컴파일한 후 하나의 프로그램으로 링크하여 사용하며, `glUseProgram`으로 활성화한다.

## 3. 데이터 및 셰이더 프로그램 인터페이스
*   **버텍스 속성 연결**: `glVertexAttribPointer`와 `glEnableVertexAttribArray`를 사용하여 VBO의 데이터를 셰이더 입력 변수에 매핑한다.
*   **렌더링 파이프라인 활성화**: 정의된 데이터 구조를 기반으로 셰이더 프로그램을 호출하여 GPU 수준의 렌더링을 수행한다.

---

## 전체 과정 요약
1.  **버퍼 생성 및 데이터 전송**: VBO와 EBO를 생성하고, 데이터를 GPU 메모리에 전송한다.
2.  **셰이더 프로그램 준비 및 활성화**: 버텍스 셰이더와 프래그먼트 셰이더를 준비하고, 이를 하나의 프로그램으로 링크하여 활성화한다.
3.  **버텍스 속성 연결 및 데이터 렌더링**: 셰이더 프로그램에 데이터를 연결하고, 렌더링을 위해 `glDrawArrays` 또는 `glDrawElements` 함수를 호출하여 그린다.

## 정리
OpenGL을 이용한 삼각형 렌더링은 **GPU 메모리 관리**, **셰이더 프로그램 구성**, 그리고 **데이터 인터페이스 설계**라는 세 가지 축을 중심으로 이루어진다. 본 파이프라인의 이해는 복잡한 3D 그래픽스 구현의 기초가 된다.
