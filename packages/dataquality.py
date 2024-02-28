from datetime import datetime
import json

def assert_fresh_data(response: bytes, symbol: str):
    datapoint = lambda x: datetime.fromtimestamp(json.loads(response)[-1][x]/1000)
    interval = round((datapoint(6)  - datapoint(0)).total_seconds() / 3600)
    now_and_open_time_diff = (
        datetime.utcnow()
        - datapoint(0)
    ).seconds // 3600
    assert now_and_open_time_diff <= interval, f'Data for {symbol} is outdated'