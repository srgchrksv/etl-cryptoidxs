import polars as pl
import json
import io

schema = [
    ("Open time", pl.Int64),
    ("Open", pl.Float64),
    ("High", pl.Float64),
    ("Low", pl.Float64),
    ("Close", pl.Float64),
    ("Volume", pl.Float64),
    ("Close time", pl.Int64),
    ("Quote asset volume", pl.Int64),
    ("Number of trades", pl.Int64),
    ("Taker buy base asset volume", pl.Int64),
    ("Taker buy quote asset volume", pl.Int64),
    ("Ignore", pl.Float64),
]


def silver_layer_transformation(response: bytes, symbol: str) -> io.BytesIO:
    df = pl.DataFrame(json.loads(response), schema=schema)
    datetime_columns = ["Open time", "Close time"]
    for column in datetime_columns:
        df = df.with_columns(pl.col(column).cast(pl.Datetime(time_unit="ms")))

    buffer = io.BytesIO()
    df.write_parquet(buffer)
    buffer.seek(0)

    return buffer
