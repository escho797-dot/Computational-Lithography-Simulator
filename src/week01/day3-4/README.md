# Day3-4. Lithography Simulator Refactoring & OPC Analysis

기존 Lithography 시뮬레이션 코드를 리팩토링하고, OPC(Optical Proximity Correction)를 위한 분석 모듈을 구현한다.

### 1. Lithography Simulator 리팩토링

기존에 하나의 스크립트에서 수행하던 Lithography 시뮬레이션을 함수 단위로 분리하였다.

구현 내용
- `create_mask()` 함수 구현
- `simulate_lithography(mask)` 함수 구현
- Mask를 외부에서 입력받도록 구조 변경
- `visualize=True` 옵션을 추가하여 계산과 시각화를 분리
- `if __name__ == "__main__"` 구조 적용

### 2. OPC 분석 모듈 구현

Lithography 결과를 정량적으로 평가하기 위한 OPC 분석 함수를 구현하였다.

구현 함수

- Difference Map 계산
- Error Pixel 계산
- Error Rate 계산
- Edge Detection
- Critical Dimension(CD) 측정

이를 위해 `opc.py` 모듈을 새롭게 작성하였다.

### 3. Main 프로그램 작성

`main.py`에서 전체 시뮬레이션 흐름을 구성하였다.

```
Target Pattern
      │
Mask 생성
      │
Lithography Simulation
      │
Resist Pattern
      │
Difference Map
      │
Error Metric
      │
CD Measurement
```

---

## 프로젝트 구조

```
day3-4/

├── lithography.py
├── opc.py
└── main.py
```

## 학습 내용

이번 단계에서는 단순히 Lithography 시뮬레이션을 구현하는 것을 넘어 프로젝트 구조를 개선하는 데 집중하였다.

학습한 내용

- 함수(Function) 설계
- Parameter와 Return 사용
- 모듈(Module) 분리
- 코드 재사용성(Reusability)
- 계산과 시각화 분리
- Difference Map 생성
- Error Metric 계산
- Critical Dimension(CD) 측정
- Edge Detection

## 검증

아래 조건을 변경하며 시뮬레이션 결과를 비교하였다.

- Threshold
- Cutoff Frequency
- Mask Width

변수 변화에 따른

- Resist Pattern
- Error Rate
- Critical Dimension(CD)

변화를 확인하여 시뮬레이션이 정상적으로 동작함을 검증하였다.

### Observations
- Threshold 값을 변화시키면 Resist Pattern의 크기와 형상이 변하며, 이에 따라 Error Rate도 함께 변화하는 것을 확인하였다.
- Cutoff Frequency에 따라 Pattern의 형상과 CD가 변화하는 것을 확인하였다.
- Mask Width를 변경하면 Resist Pattern의 CD도 함께 변화하였다.
- Difference Map을 이용하여 Target과 Resist의 오차를 직관적으로 확인할 수 있었다.