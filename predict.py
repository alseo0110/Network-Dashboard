import numpy as np
import os
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Input

# 모델과 파일 경로를 전역으로 설정
model = None
MODEL_PATH = 'network_traffic_model.h5'

def initialize_model(input_shape):
    global model
    if os.path.exists(MODEL_PATH):
        # 모델이 이미 저장되어 있으면 로드
        model = load_model(MODEL_PATH)
    else:
        # 모델이 없으면 새로 생성
        model = Sequential()
        model.add(Input(shape=input_shape))
        model.add(LSTM(50, activation='relu'))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')

def predict_network_traffic_lstm(history, sample_size=50, retrain=False):
    global model

    if len(history) < 5:
        print("데이터가 부족합니다.")
        return None

    if len(history) > sample_size:
        history = history[-sample_size:]

    data = np.array(history)
    data = data.reshape((data.shape[0], 1, 1))

    # 모델 초기화 및 재사용
    initialize_model(input_shape=(data.shape[1], data.shape[2]))

    # 학습이 필요한 경우에만 모델 학습
    if retrain or not os.path.exists(MODEL_PATH):
        print("모델 학습 시작...")
        model.fit(data, data, epochs=10, batch_size=1, verbose=0)
        model.save(MODEL_PATH)  # 학습된 모델 저장
        print("모델 학습 완료 및 저장.")

    # 예측 수행
    print("예측 수행 중...")
    predicted_value = model.predict(data[-1].reshape(1, 1, 1))
    print(f"예측값: {predicted_value[0][0]}")

    return predicted_value[0][0]

