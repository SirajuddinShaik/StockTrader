from pathlib import Path
from stock_agent.constants import SYMBOLS_FILE_PATH
from stock_agent.entity.config_entity import DataValidationConfig
from stock_agent.utils.common import get_symbols

import pandas as pd

class DataValidation:
    def __init__(self, config:DataValidationConfig):
        self.config = config
        self.symbols = get_symbols()
        self.data_dir=config.data_dir+"/{symbol}.csv"
        self.root_dir=config.root_dir+"/{symbol}.csv"


    def clean(self):
        for symbol in self.symbols:
            file = self.data_dir.format(symbol = symbol)
            df = pd.read_csv(file)
            df = self.remove_null(df)
            self.save_csv(df, symbol)
            
        
    def remove_null(self ,df:pd.DataFrame) -> pd.DataFrame:
        df = df.dropna()
        return df
    
    def save_csv(self,df:pd.DataFrame, symbol:str):
        df.to_csv(self.root_dir.format(symbol = symbol))
    
