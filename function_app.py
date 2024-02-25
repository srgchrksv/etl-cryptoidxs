import requests
import azure.functions as func
import logging

from storage import storage_connection
from helpers import assert_fresh_data
from silver import silver_layer_transformation

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)


@app.route(route="get_data")
def get_data(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # storage configs
        storage_account_name = req.headers.get("storage_account_name")
        storage_account_key = req.headers.get("storage_account_key")
        container_name = req.headers.get("container_name")
        # timeseries configs
        url = req.headers.get("url")
        symbol = req.headers.get("symbol")
        limit = req.headers.get("limit")
        interval = req.headers.get("interval")

        # Set up the connection to Azure Storage Gen2
        container_client = storage_connection(
            storage_account_name, storage_account_key, container_name
        )

        # Check timeseries configs
        if not url or not symbol or not limit or not interval:
            msg = "Symbol specifications not provided in get_data az func"
            logging.error(msg)
            return func.HttpResponse(msg, status_code=400)

        # GET data request
        response = requests.get(
            url, params={"limit": limit, "interval": interval, "symbol": symbol}
        )

        assert_fresh_data(response.content, symbol)

        # Bronze layer raw data load to storage
        blob_name = f"layers/bronze/{symbol}"
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(response.content, overwrite=True)
        msg = f"Raw data for {symbol} uploaded successfully to {blob_name} in {container_name} container."
        logging.info(msg)

        # Silver layer transform - add schema and load as parquet to storage
        blob_name_to_write = f"layers/silver/{symbol}.parquet"
        buffer = silver_layer_transformation(response.content, symbol)
        container_client.upload_blob(name=blob_name_to_write, data=buffer, overwrite=True)
        msg = f"Parquet df for {symbol} uploaded successfully to {blob_name_to_write} in {container_name} container."
        logging.info(msg)

        return func.HttpResponse(msg, status_code=200)
    except Exception as e:
        msg = f"Error while running get_data on {symbol} - {e}"
        return func.HttpResponse(msg, status_code=500)
