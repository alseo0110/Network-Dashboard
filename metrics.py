# metrics.py
import sqlite3
import psutil
from datetime import datetime

# 데이터베이스 연결 및 테이블 생성
# def create_db():
#     conn = sqlite3.connect('netcheck.db')
#     cursor = conn.cursor()
#
#     # 모든 시스템 메트릭을 저장할 테이블 생성
#     cursor.execute('''
#     CREATE TABLE IF NOT EXISTS system_metrics (
#         timestamp TEXT,
#         cpu_usage REAL,
#         memory_usage REAL,
#         disk_usage REAL,
#         network_bytes_sent INTEGER,
#         network_bytes_recv INTEGER
#     )
#     ''')
#
#     conn.commit()
#     conn.close()

# 시스템 메트릭스 삽입 함수
# def insert_metrics(metrics):
#     conn = sqlite3.connect('netcheck.db')
#     cursor = conn.cursor()
#
#     # 현재 타임스탬프
#     timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#
#     # 모든 메트릭 데이터 삽입
#     cursor.execute('''
#     INSERT INTO system_metrics (
#         timestamp, cpu_usage, memory_usage, disk_usage, network_bytes_sent, network_bytes_recv
#     ) VALUES (?, ?, ?, ?, ?, ?)
#     ''', (timestamp, metrics['cpu_usage'], metrics['memory_usage'], metrics['disk_usage'],
#           metrics['network_bytes_sent'], metrics['network_bytes_recv']))
#
#     conn.commit()
#     conn.close()

# 이전 네트워크 상태 저장용 변수 초기화
prev_sent = None
prev_recv = None

def get_system_metrics():
    global prev_sent, prev_recv

    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    disk_info = psutil.disk_usage('/')
    disk_usage = disk_info.percent

    net_io = psutil.net_io_counters()
    current_sent = net_io.bytes_sent
    current_recv = net_io.bytes_recv

    # 처음 실행 시 이전 값을 초기화
    if prev_sent is None:
        prev_sent = current_sent
        prev_recv = current_recv

    # 단위 시간당 변화량 계산
    sent_diff = current_sent - prev_sent
    recv_diff = current_recv - prev_recv

    # 현재 값을 이전 값으로 업데이트
    prev_sent = current_sent
    prev_recv = current_recv

    metrics = {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_usage': disk_usage,
        'network_bytes_sent': sent_diff,
        'network_bytes_recv': recv_diff,
    }
    return metrics