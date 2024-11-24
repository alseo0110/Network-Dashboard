import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet

# CSV 파일 읽기
data = pd.read_csv('system_metrics1.csv', parse_dates=['timestamp'])

# Prophet이 요구하는 형식으로 데이터 준비
# 'timestamp'를 'ds'로, 'network_bytes_sent'를 'y'로 이름을 변경
prophet_data = data[['timestamp', 'network_bytes_sent']].rename(columns={'timestamp': 'ds', 'network_bytes_sent': 'y'})

# 모델 생성 및 학습
model = Prophet()
model.fit(prophet_data)

# 향후 10개의 시간 데이터 생성
future = model.make_future_dataframe(periods=30, freq='T')  # 30분 이후 예측

# 예측 수행
forecast = model.predict(future)

# 예측 결과 시각화
fig = model.plot(forecast)
plt.title('네트워크 송신 데이터 예측 (Prophet)')
plt.xlabel('시간')
plt.ylabel('송신 데이터 (바이트)')
plt.show()

# 예측된 데이터 시각화
fig2 = model.plot_components(forecast)
plt.show()