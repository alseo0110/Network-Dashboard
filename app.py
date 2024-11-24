# app.py
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt
from layout import create_layout, create_donut_chart
from metrics import get_system_metrics
from predict import predict_network_traffic_lstm
import pandas as pd
import plotly.graph_objects as go
from prophet import Prophet

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = create_layout()

# 데이터 저장을 위한 리스트 초기화
sent_history = []
recv_history = []
predicted_sent_history = []
predicted_recv_history = []

# 마지막 데이터베이스 저장 시간을 추적할 변수 초기화
last_db_save_time = pd.Timestamp.now()

# 실시간 대시보드 갱신 콜백 함수
@app.callback(
    [Output('cpu-usage', 'figure'),
     Output('memory-usage', 'figure'),
     Output('disk-usage', 'figure'),
     Output('network-sent-data', 'figure'),
     Output('network-recv-data', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    global sent_history, recv_history, predicted_sent_history, predicted_recv_history, last_db_save_time

    # 시스템 메트릭 수집
    metrics = get_system_metrics()
    print("Collected system metrics:", metrics)  # 시스템 메트릭 수집 로그 출력

    # CPU, 메모리, 디스크 사용량 원형 그래프 업데이트
    cpu_usage = metrics['cpu_usage']
    memory_usage = metrics['memory_usage']
    disk_usage = metrics['disk_usage']

    cpu_fig = create_donut_chart("CPU 사용량", cpu_usage)
    memory_fig = create_donut_chart("메모리 사용량", memory_usage)
    disk_fig = create_donut_chart("디스크 사용량", disk_usage)

    # 송신 및 수신 데이터 기록
    sent_history.append(metrics['network_bytes_sent'])
    recv_history.append(metrics['network_bytes_recv'])

    # 예측 (현재 송신 및 수신 데이터 기반으로 예측)
    predicted_sent = predict_network_traffic_lstm(sent_history)
    predicted_recv = predict_network_traffic_lstm(recv_history)

    # 예측된 송신 데이터, 예측된 수신 데이터 업데이트
    if predicted_sent is not None:
        predicted_sent_history.append(predicted_sent)
    if predicted_recv is not None:
        predicted_recv_history.append(predicted_recv)

    # 예측값을 실시간 데이터와 동일한 시간선상에 맞추기 위해 길이를 맞추거나 인덱스 조정
    if len(predicted_sent_history) > len(sent_history):
        predicted_sent_history = predicted_sent_history[:len(sent_history)]
    if len(predicted_recv_history) > len(recv_history):
        predicted_recv_history = predicted_recv_history[:len(recv_history)]

    # 예측값을 실시간 데이터의 다음 시점에 맞추기 위해 예측된 값을 마지막에 추가
    if len(predicted_sent_history) < len(sent_history):
        predicted_sent_history.append(predicted_sent_history[-1] if len(predicted_sent_history) > 0 else 0)
    if len(predicted_recv_history) < len(recv_history):
        predicted_recv_history.append(predicted_recv_history[-1] if len(predicted_recv_history) > 0 else 0)

    # 네트워크 송신 데이터와 예측된 송신 데이터를 하나의 그래프에 추가
    fig_sent = go.Figure()

    # 실제 송신 데이터
    fig_sent.add_trace(go.Scatter(x=list(range(len(sent_history))), y=sent_history, mode='lines', name='실제 송신 데이터', line=dict(color='#00CC99')))
    # 예측된 송신 데이터
    if len(predicted_sent_history) > 0:
        fig_sent.add_trace(go.Scatter(x=list(range(len(predicted_sent_history))), y=predicted_sent_history, mode='lines', name='예측 송신 데이터', line=dict(color='#FF5733', dash='dash')))

    # 네트워크 수신 데이터와 예측된 수신 데이터를 하나의 그래프에 추가
    fig_recv = go.Figure()

    # 실제 수신 데이터
    fig_recv.add_trace(go.Scatter(x=list(range(len(recv_history))), y=recv_history, mode='lines', name='실제 수신 데이터', line=dict(color='#00CC99')))
    # 예측된 수신 데이터
    if len(predicted_recv_history) > 0:
        fig_recv.add_trace(go.Scatter(x=list(range(len(predicted_recv_history))), y=predicted_recv_history, mode='lines', name='예측 수신 데이터', line=dict(color='#FF5733', dash='dash')))

    return cpu_fig, memory_fig, disk_fig, fig_sent, fig_recv

@app.callback(
    [Output('prophet-forecast-sent', 'figure'),  # 송신 데이터 예측 그래프
     Output('prophet-forecast-recv', 'figure')],  # 수신 데이터 예측 그래프
    [Input('interval-component', 'n_intervals')]
)
def update_prophet_forecast(n):
    # CSV 파일 읽기
    data = pd.read_csv('system_metrics1.csv', parse_dates=['timestamp'])

    # 송신 데이터 예측을 위한 데이터 준비
    prophet_data_sent = data[['timestamp', 'network_bytes_sent']].rename(
        columns={'timestamp': 'ds', 'network_bytes_sent': 'y'})

    # 수신 데이터 예측을 위한 데이터 준비
    prophet_data_recv = data[['timestamp', 'network_bytes_recv']].rename(
        columns={'timestamp': 'ds', 'network_bytes_recv': 'y'})

    # 송신 모델 생성 및 학습
    model_sent = Prophet()
    model_sent.fit(prophet_data_sent)

    # 수신 모델 생성 및 학습
    model_recv = Prophet()
    model_recv.fit(prophet_data_recv)

    # 향후 30개의 시간 데이터 생성
    future_sent = model_sent.make_future_dataframe(periods=30, freq='T')
    future_recv = model_recv.make_future_dataframe(periods=30, freq='T')

    # 예측 수행
    forecast_sent = model_sent.predict(future_sent)
    forecast_recv = model_recv.predict(future_recv)

    # 송신 데이터 예측 결과 시각화
    fig_sent = go.Figure()
    fig_sent.add_trace(go.Scatter(x=prophet_data_sent['ds'], y=prophet_data_sent['y'], mode='lines', name='실제 송신 데이터'))
    fig_sent.add_trace(go.Scatter(x=forecast_sent['ds'], y=forecast_sent['yhat'], mode='lines', name='예측 송신값', line=dict(dash='dash', color='orange')))
    fig_sent.add_trace(go.Scatter(x=forecast_sent['ds'], y=forecast_sent['yhat_upper'], mode='lines', name='송신 상한', line=dict(color='lightgrey', dash='dash')))
    fig_sent.add_trace(go.Scatter(x=forecast_sent['ds'], y=forecast_sent['yhat_lower'], mode='lines', name='송신 하한', line=dict(color='lightgrey', dash='dash')))
    fig_sent.update_layout(title='송신 데이터 Prophet 예측 결과', xaxis_title='시간', yaxis_title='송신 데이터 바이트')

    # 수신 데이터 예측 결과 시각화
    fig_recv = go.Figure()
    fig_recv.add_trace(go.Scatter(x=prophet_data_recv['ds'], y=prophet_data_recv['y'], mode='lines', name='실제 수신 데이터'))
    fig_recv.add_trace(go.Scatter(x=forecast_recv['ds'], y=forecast_recv['yhat'], mode='lines', name='예측 수신값', line=dict(dash='dash', color='orange')))
    fig_recv.add_trace(go.Scatter(x=forecast_recv['ds'], y=forecast_recv['yhat_upper'], mode='lines', name='수신 상한', line=dict(color='lightgrey', dash='dash')))
    fig_recv.add_trace(go.Scatter(x=forecast_recv['ds'], y=forecast_recv['yhat_lower'], mode='lines', name='수신 하한', line=dict(color='lightgrey', dash='dash')))
    fig_recv.update_layout(title='수신 데이터 Prophet 예측 결과', xaxis_title='시간', yaxis_title='수신 데이터 바이트')

    return fig_sent, fig_recv


if __name__ == '__main__':
    app.run_server(debug=True)
