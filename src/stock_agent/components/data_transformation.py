from stock_agent.entity.config_entity import DataTransformationConfig
from stock_agent.utils.common import get_symbols
from stock_agent import logger

import pandas as pd
from sklearn.model_selection import train_test_split
import os

class DataTransformation:
    def __init__(self,config: DataTransformationConfig):
        self.config = config

    def split_datetime(self, dt_str):
        components = dt_str.replace('-', ' ').replace(':', ' ').split()
        return list(map(int, components))

    def combine_data(self):
        symbols = get_symbols()

        # Initialize an empty DataFrame
        data_frame = pd.DataFrame()

        for j in range(len(symbols)):
            i = symbols[j]
            df = pd.read_csv(os.path.join(self.config.data_dir, f"{i}.csv"))
            df = df.iloc[::-1].reset_index(drop=True)

            # Convert 'datetime' to datetime object for proper alignment

            # Extract date and time components
            if j == 0:
                data_frame[['year', 'month', 'day', 'hour', 'minute', 'second']] = df['datetime'].apply(self.split_datetime).apply(pd.Series)
                data_frame = data_frame.drop(columns=["second", "minute"])
                data_frame["datetime"] = df["datetime"]
                data_frame.set_index('datetime', inplace=True)

            # Set 'datetime' as index for merging
            df.set_index('datetime', inplace=True)

            # Select and rename columns
            df = df[['open', 'high', 'low', 'close', 'volume']]
            df.columns = [f'{col}_{i}' for col in df.columns]

            # Merge or concatenate DataFrames on 'datetime'
            if data_frame.empty:
                data_frame = df
            else:
                data_frame = data_frame.merge(df, left_index=True, right_index=True, how='outer')

        # Drop any rows with missing values
        data_frame = data_frame.dropna()

        # Reset index to get 'datetime' back as a column
        data_frame.reset_index(inplace=True)
        data_frame = data_frame.drop(columns=["datetime"])
        # Save the final DataFrame to CSV
        data_frame.to_csv(os.path.join(self.config.root_dir, self.config.file_name), index=False)
        logger.info(f"All Stocks Data Combined at {os.path.join(self.config.root_dir, self.config.file_name)}")

    def train_test_spliting(self):
        data = pd.read_csv(os.path.join(self.config.root_dir, self.config.file_name))

        # Split the data into training and test sets. (0.75, 0.25) split.
        train, test = train_test_split(data)

        train.to_csv(os.path.join(self.config.root_dir, "train.csv"),index = False)
        test.to_csv(os.path.join(self.config.root_dir, "test.csv"),index = False)

        logger.info("Splited data into training and test sets")
        logger.info(train.shape)
        logger.info(test.shape)

        print(train.shape)
        print(test.shape)