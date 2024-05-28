from stock_agent import logger
from stock_agent.entity.config_entity import DataIngestionConfig
from stock_agent.utils.common import get_symbols


import requests
import time
from datetime import datetime ,timedelta
import pandas as pd
import os


class DataIngestion:
    def __init__(self, config:DataIngestionConfig):
        self.config = config



    def download_new_data(self, interval = "4h"):
        uri_format = "https://api.twelvedata.com/time_series?apikey={api}&interval={interval}&start_date={start_date}&end_date={end_date}&format=JSON&symbol={symbol}"
        symbols = get_symbols()
        ll,ul = self.get_interval(5)
        for i in range(len(symbols)):
            uri = uri_format.format(api = os.environ["TWELVE_DATA_API"], interval = interval, start_date = ll, end_date = ul, symbol = symbols[i])
            response = requests.get(uri).json()
            if response["status"] == "error":
                time.sleep(61)
                response = requests.get(uri).json()
            data = response["values"]
            df = pd.DataFrame(data)
            df.to_csv(self.config.local_data_file + f"{symbols[i]}.csv")
            logger.info(f">>>>>>>>>> {symbols[i]}.csv saved to artifacts <<<<<<<<")


    def get_interval(self, length = 5):
        ul = datetime.now()
        ll = ul - timedelta(days=length*365)
        return (ll.strftime("%Y-%m-%d %H:%M:%S"),ul.strftime("%Y-%m-%d %H:%M:%S"))


