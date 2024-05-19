from stock_agent import logger
from stock_agent.entity.config_entity import DataIngestionConfig


import requests
import time
from datetime import datetime ,timedelta
import pandas as pd
import os


class DataIngestion:
    def __init__(self, config:DataIngestionConfig):
        self.config = config



    def download_new_data(self, interval = 30):
        uri_format = "https://api.twelvedata.com/time_series?apikey={api}&interval={interval}min&start_date={start_date}&end_date={end_date}&format=JSON&previous_close=true&symbol={symbol}"
        f = open(self.config.source_URL)
        symbols = list(map(str.strip, symbols))
        symbols = f.readlines()
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


