


from stock_agent import logger
from stock_agent.components.data_validation import DataValidation
from stock_agent.config.configuration import ConfigurationManager

STAGE_NAME = "Data Validation stage"

class DataValidationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):

        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(data_validation_config)
        data_validation.clean()


if __name__ == "__main__":

    try:
        logger.info(f">>>>>>>>>>>>> {STAGE_NAME} started <<<<<<<")
        obj = DataValidationTrainingPipeline()
        obj.main()
        logger.info(f">>>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<")
    except Exception as e:
        logger.exception(e)
        raise e