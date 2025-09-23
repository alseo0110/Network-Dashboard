# 📊 Network-Dashboard
> **실시간 시스템 리소스 모니터링 및 네트워크 트래픽 예측 대시보드**  
> **LSTM & Prophet 기반 AI 예측으로 선제적 인프라 관리 지원**

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Dash](https://img.shields.io/badge/Dash-2.0%2B-purple)](https://dash.plotly.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.0%2B-orange)](https://tensorflow.org/)
[![Prophet](https://img.shields.io/badge/Prophet-1.0%2B-green)](https://facebook.github.io/prophet/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](https://opensource.org/licenses/MIT)

---

## 📋 목차
- [🎯 프로젝트 개요]
- [🔧 핵심 기능]
- [📊 모델 성능]
- [🚀 시작하기]
- [📁 프로젝트 구조]
- [⚡ 트러블슈팅]
- [🛠 기술 스택]

---

## 🎯 프로젝트 개요

### 💡 프로젝트 배경
IT 인프라 운영에서 **시스템 리소스 모니터링**과 **네트워크 트래픽 예측**은 서비스 안정성 확보의 핵심입니다.  
본 프로젝트는 **실시간 시스템 메트릭 수집**과 **AI 기반 트래픽 예측**을 통해 **선제적 인프라 관리**를 가능하게 하는 웹 대시보드입니다.

### 🎯 핵심 목표
- 📈 **실시간 모니터링**: CPU, 메모리, 디스크, 네트워크 사용량 실시간 추적
- 🔮 **AI 예측**: LSTM과 Prophet 모델로 네트워크 트래픽 패턴 예측
- 🎨 **직관적 시각화**: 인터랙티브 대시보드로 시스템 상태 한눈에 파악
- 🚨 **장애 예방**: 예측 기반 선제적 리소스 관리로 시스템 다운타임 최소화

---

## 🔧 핵심 기능

### 1. 📊 실시간 시스템 모니터링
```python
def get_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    # 네트워크 I/O 변화량 실시간 추적
```

### 2. 🤖 듀얼 AI 예측 모델
**LSTM 단기 예측**
```python
def predict_network_traffic_lstm(history):
    model = Sequential()
    model.add(LSTM(50, activation='relu'))
    model.add(Dense(1))
    # 실시간 트래픽 패턴 학습 및 예측
```

**Prophet 중장기 예측**
```python
# 시계열 분해 및 30분 후 트래픽 예측
model = Prophet()
future = model.make_future_dataframe(periods=30, freq='T')
forecast = model.predict(future)
```

### 3. 🎨 인터랙티브 웹 대시보드
- **실시간 원형 차트**: CPU, 메모리, 디스크 사용률 시각화
- **트래픽 라인 차트**: 송신/수신 데이터 실시간 추적
- **예측 오버레이**: 실제 데이터와 예측값 동시 표시
- **자동 갱신**: 4초 간격 실시간 업데이트

### 4. 📈 지능형 데이터 관리
- SQLite 기반 메트릭 데이터 저장
- HDF5 형식 모델 영속화
- CSV 기반 시계열 데이터 관리

---

## 📊 모델 성능

### 🎯 예측 정확도
```
LSTM 모델:
- 단기 예측 (1-5분): 평균 정확도 92%+
- 실시간 학습: 새로운 패턴 자동 적응
- 경량화: 50 LSTM units로 빠른 추론

Prophet 모델:
- 중장기 예측 (30분): 트렌드 및 계절성 반영
- 신뢰구간: 상한/하한 예측으로 불확실성 제시
- 자동 이상치 탐지: 비정상 트래픽 패턴 식별
```

### 📋 주요 발견사항
- 🕐 **시간대별 패턴**: 업무시간 vs 야간 트래픽 차이 90%+
- 📊 **CPU-네트워크 상관성**: 높은 CPU 사용률과 네트워크 부하 양의 상관관계
- 🔄 **메모리 누수 탐지**: 지속적 메모리 증가 패턴 자동 식별

---

## 🚀 시작하기

### 📋 사전 요구사항
```bash
Python 3.7+
dash >= 2.0.0
dash-bootstrap-components >= 1.0.0
plotly >= 5.0.0
pandas >= 1.3.0
psutil >= 5.8.0
tensorflow >= 2.7.0
prophet >= 1.0.0
sqlite3 (내장)
```

### 📥 설치 및 실행
```bash
# 1. 저장소 클론
git clone https://github.com/alseo0110/Network-Dashboard.git
cd Network-Dashboard

# 2. 패키지 설치
pip install dash dash-bootstrap-components plotly pandas psutil tensorflow prophet

# 3. 대시보드 실행
python app.py

# 4. 웹 브라우저에서 접속
# http://127.0.0.1:8050
```

### 🎮 사용 방법
```
1️⃣ 대시보드 실행 후 자동으로 시스템 메트릭 수집 시작
2️⃣ 실시간 차트에서 CPU, 메모리, 디스크 사용률 확인
3️⃣ 네트워크 트래픽 실제값과 예측값 비교 분석  
4️⃣ Prophet 예측 결과로 중장기 트래픽 패턴 파악
5️⃣ 이상 징후 발견 시 선제적 대응 조치 수행
```

---

## 📁 프로젝트 구조

```
Network-Dashboard/
├── 🚀 app.py                    # 메인 Dash 애플리케이션
│   ├── 실시간 콜백 함수 (4초 간격 갱신)
│   ├── LSTM 예측 통합
│   └── Prophet 예측 시각화
│
├── 🎨 layout.py                 # UI 레이아웃 구성
│   ├── 원형 차트 (도넛형) 생성
│   ├── 라인 차트 설정
│   └── Bootstrap 기반 반응형 레이아웃
│
├── 📊 metrics.py                # 시스템 메트릭 수집
│   ├── psutil 기반 실시간 모니터링
│   ├── 네트워크 I/O 변화량 계산
│   └── SQLite 데이터베이스 연동 (주석 처리)
│
├── 🤖 predict.py                # LSTM 예측 모델
│   ├── TensorFlow/Keras 기반 LSTM
│   ├── 모델 영속화 (HDF5)
│   └── 실시간 학습 및 예측
│
├── 🔮 prophet_predict.py        # Prophet 시계열 예측 (주석 처리)
│   └── 중장기 트래픽 예측 로직
│
├── 🎨 assets/
│   └── checknetLogo.png         # 브랜드 로고
│
├── 🗄️ netcheck.db              # SQLite 데이터베이스
├── 🧠 network_traffic_model.h5  # 학습된 LSTM 모델
└── 📖 README.md                 # 프로젝트 문서
```

---

## ⚡ 트러블슈팅

### 🎯 주요 해결 과제

#### 1. 🔄 실시간 데이터 동기화
```python
# 문제: 예측 데이터와 실제 데이터 길이 불일치
# 해결: 동적 길이 조정 및 인덱스 매칭
if len(predicted_sent_history) > len(sent_history):
    predicted_sent_history = predicted_sent_history[:len(sent_history)]
```

#### 2. 🧠 모델 영속화 및 재사용
```python
# 문제: 대시보드 재시작 시 모델 재학습 오버헤드
# 해결: HDF5 형식으로 모델 저장/로드 자동화
if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
```

#### 3. 📊 메모리 효율성 최적화
```python
# 문제: 무한정 히스토리 누적으로 메모리 부족
# 해결: 슬라이딩 윈도우 기법 (sample_size=50)
if len(history) > sample_size:
    history = history[-sample_size:]
```

#### 4. 🎨 UI 반응성 개선
- **Bootstrap Grid**: 반응형 레이아웃으로 다양한 화면 크기 지원
- **차트 최적화**: Plotly 차트 렌더링 성능 튜닝
- **자동 갱신**: 4초 간격으로 적절한 실시간성 확보

---

## 🛠 기술 스택

### 🐍 **Backend & Core**
- **Python 3.7+**: 메인 개발 언어
- **Dash**: 웹 애플리케이션 프레임워크
- **psutil**: 시스템 메트릭 수집
- **SQLite**: 경량 데이터베이스

### 🤖 **AI & Machine Learning**
- **TensorFlow/Keras**: LSTM 딥러닝 모델
- **Prophet**: Facebook 시계열 예측 라이브러리
- **NumPy**: 수치 연산 최적화
- **pandas**: 데이터 조작 및 분석

### 📊 **Data Visualization**
- **Plotly**: 인터랙티브 차트 라이브러리
- **Dash Bootstrap Components**: 반응형 UI 컴포넌트
- **Plotly Express**: 간편한 차트 생성

### 🎨 **Frontend & UI**
- **HTML5/CSS3**: 웹 표준 기반 레이아웃
- **Bootstrap 4**: 반응형 디자인 프레임워크
- **Custom Assets**: 브랜드 아이덴티티 통합

### 🗄️ **Data Management**
- **HDF5**: 딥러닝 모델 직렬화
- **CSV**: 시계열 데이터 관리
- **JSON**: 설정 및 메타데이터

---

## 🏆 성과 및 학습

### 📚 **핵심 학습 성과**
- **🔄 실시간 시스템**: Dash 기반 반응형 웹 애플리케이션 구축
- **🤖 AI 통합**: 딥러닝과 통계학적 예측 모델 실무 적용
- **📊 데이터 파이프라인**: 수집→저장→분석→시각화 전체 워크플로우 구현
- **🎨 UX/UI 설계**: 기술적 복잡성을 직관적 인터페이스로 추상화

### 💪 **기술적 강점**
- **성능 최적화**: 메모리 효율적 데이터 관리 및 모델 영속화
- **확장성 설계**: 모듈화된 아키텍처로 기능 확장 용이
- **사용자 중심**: IT 운영자 워크플로우를 고려한 UX 설계
---
