from stock_agent.config.configuration import ConfigurationManager
from stock_agent import logger
from stock_agent.components.data_ingestion import DataIngestion
from stock_agent.utils.common import setup_env

STAGE_NAME = "Data Ingestion stage"


class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion.download_new_data()



if __name__ == "__main__":
    try:
        setup_env()
        logger.info(f">>>>>>>>>>>>> {STAGE_NAME} started <<<<<<<")
        obj = DataIngestionTrainingPipeline()
        obj.main()
        logger.info(f">>>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e

