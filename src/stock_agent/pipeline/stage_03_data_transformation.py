from stock_agent.components.data_transformation import DataTransformation
from stock_agent.config.configuration import ConfigurationManager
from stock_agent import logger

STAGE_NAME = "Data Transformation Stage"

class DataTransformationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):

        config = ConfigurationManager()
        data_transformation_config = config.get_data_transformation_config()
        data_transformation = DataTransformation(data_transformation_config)
        data_transformation.combine_data()
        data_transformation.train_test_spliting()

if __name__ == "__main__":
    try:
        logger.info(">>>>>>>>>>>> {STAGE_NAME} started <<<<<<<<<<<")
        obj = DataTransformationTrainingPipeline()
        obj.main()
        logger.info(">>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<<<")
    except Exception as e:
        logger.info(e)
        raise e