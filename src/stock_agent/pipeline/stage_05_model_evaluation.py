from stock_agent.components.model_evaluation import ModelEvaluation
from stock_agent.config.configuration import ConfigurationManager
from stock_agent import logger

STAGE_NAME = "Model Evaluation Stage"

class ModelEvaluationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()

        model_evaluation_config = config.get_model_evaluation_config()
        model_evaluation = ModelEvaluation(model_evaluation_config)
        return model_evaluation.eval()


if __name__ == "__main__":
    try:
        logger.info(f">>>>>>>>>>>>>>> {STAGE_NAME} started <<<<<<<<<<<")
        obj = ModelEvaluationTrainingPipeline()
        obj.main()
        logger.info(f">>>>>>>>>>>>>>> {STAGE_NAME} completed <<<<<<<<<<<")
    except Exception as e:
        logger.info(e)
        raise e
