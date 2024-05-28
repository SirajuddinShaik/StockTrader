from stock_agent.components.model_trainer import ModelTrainer
from stock_agent.config.configuration import ConfigurationManager
from stock_agent import logger

STAGE_NAME ="Model Training Stage"

class ModelTrainerTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer = ModelTrainer(model_trainer_config)
        model_trainer.train()

if __name__ == "__main__":
    try:
        logger.info(">>>>>>>>>>>>>> {STAGE_NAME} started <<<<<<<<<<<<")
        obj = ModelTrainerTrainingPipeline()
        obj.main()
        logger.info(">>>>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<<<<<<")
    except Exception as e:
        logger.info(e)
        raise e