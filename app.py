# app.py
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dcc, html
from layout import create_layout, create_donut_chart  # 함수 가져오기
from metrics import get_system_metrics
from predict import predict_network_traffic_lstm
import pandas as pd
import plotly.graph_objects as go  # 이 줄을 추가

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

if __name__ == '__main__':
    app.run_server(debug=True)
