# layout.py
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# 원형 그래프를 위한 설정 함수
def create_donut_chart(title, value):
    fig = go.Figure(data=[go.Pie(
        labels=["사용량", "남은 용량"],
        values=[value, 100 - value],
        hole=.7,
        marker=dict(colors=['#00CC99', '#F2F2F2']),
        textinfo='none'
    )])
    fig.update_layout(
        title=title,
        showlegend=False,
        margin=dict(t=50, b=0, l=0, r=0),
        height=250
    )
    return fig

# 선 그래프를 위한 설정 함수
def create_line_chart(title, x, y):
    # DataFrame을 생성하여 px.line에 전달
    df = pd.DataFrame({'x': x, 'y': y})
    fig = px.line(
        df,
        x='x',
        y='y',
        labels={'x': '시간', 'y': title},
        title=title
    )
    fig.update_traces(line=dict(color='#00CC99'))
    fig.update_layout(height=250, margin=dict(t=50, b=0, l=0, r=0))
    return fig

# 레이아웃 생성 함수
def create_layout():
    layout = dbc.Container([
        dbc.Row([
            dbc.Col(html.Img(src='assets/checknetLogo.png', style={'width': '300px', 'height': '150px', 'marginRight': '10px'}), width='auto'),
        ]),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("CPU 사용량"),
                dbc.CardBody(dcc.Graph(id='cpu-usage'))
            ], className="mb-4"), width=4),

            dbc.Col(dbc.Card([
                dbc.CardHeader("메모리 사용량"),
                dbc.CardBody(dcc.Graph(id='memory-usage'))
            ], className="mb-4"), width=4),

            dbc.Col(dbc.Card([
                dbc.CardHeader("디스크 사용량"),
                dbc.CardBody(dcc.Graph(id='disk-usage'))
            ], className="mb-4"), width=4),
        ]),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("네트워크 송신 데이터"),
                dbc.CardBody(dcc.Graph(id='network-sent-data'))
            ], className="mb-4"), width=6),

            dbc.Col(dbc.Card([
                dbc.CardHeader("네트워크 수신 데이터"),
                dbc.CardBody(dcc.Graph(id='network-recv-data'))
            ], className="mb-4"), width=6),
        ]),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Prophet 송신 데이터 예측 결과"),
                dbc.CardBody(dcc.Graph(id='prophet-forecast-sent'))
            ], className="mb-4"), width=12),
        ]),

        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Prophet 수신 데이터 예측 결과"),
                dbc.CardBody(dcc.Graph(id='prophet-forecast-recv'))
            ], className="mb-4"), width=12),
        ]),

        dcc.Interval(id='interval-component', interval=4000, n_intervals=0)
    ], fluid=True)

    return layout
