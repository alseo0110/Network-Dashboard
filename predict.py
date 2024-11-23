import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input

def predict_network_traffic_lstm(history, sample_size=50):
    # 데이터가 충분하지 않으면 None 반환
    if len(history) < 5:
        print("데이터가 부족합니다.")
        return None

    # 최근 데이터 샘플링
    if len(history) > sample_size:
        history = history[-sample_size:]  # 최근 sample_size 개 데이터만 사용

    # 데이터 전처리 (시계열 데이터를 LSTM 모델에 맞게 변환)
    data = np.array(history)
    data = data.reshape((data.shape[0], 1, 1))  # (샘플 수, 타임스텝, 특성 수)

    # LSTM 모델 정의
    model = Sequential()
    model.add(Input(shape=(data.shape[1], data.shape[2])))  # Input(shape)로 첫 번째 레이어 정의
    model.add(LSTM(50, activation='relu'))  # LSTM 레이어 추가
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # 모델 학습 (간단한 예시로 한 번만 학습)
    print("모델 학습 시작...")
    model.fit(data, data, epochs=10, batch_size=1, verbose=0)
    print("모델 학습 완료.")

    # 예측 수행 (마지막 데이터를 기준으로 예측)
    print("예측 수행 중...")
    predicted_value = model.predict(data[-1].reshape(1, 1, 1))  # 마지막 데이터를 3차원 배열로 reshape
    print(f"예측값: {predicted_value[0][0]}")

    return predicted_value[0][0]
