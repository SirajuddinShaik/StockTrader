from stock_agent.constants import *
from stock_agent.utils.common import create_files, read_yaml, create_directories
from stock_agent.entity.config_entity import (
    DataIngestionConfig,
    DataTransformationConfig,
    DataValidationConfig,
    ModelEvaluationConfig,
    ModelTrainerConfig,
    )

class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH,
        params_filepath = PARAMS_FILE_PATH,
        schema_filepath = SCHEMA_FILE_PATH):

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        create_directories([self.config.artifacts_root])


    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL,
            local_data_file=config.local_data_file,
        )

        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation

        create_directories([config.root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=config.root_dir,
            data_dir=config.data_dir,
            STATUS_FILE=config.STATUS_FILE,
        )

        return data_validation_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation

        create_directories([config.root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=config.root_dir,
            data_dir=config.data_dir,
            file_name=config.file_name,
        )

        return data_transformation_config

    
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        config = self.config.model_trainer

        create_directories([config.root_dir])
        create_files([config.best_score_file])

        model_trainer_config = ModelTrainerConfig(
            root_dir=config.root_dir,
            data_dir=config.data_dir,
            alpha=config.alpha,
            beta=config.beta,
            gamma=config.gamma,
            max_size=config.max_size,
            tau=config.tau,
            batch_size=config.batch_size,
            history_len=config.history_len,
            re_train=config.re_train,
            epochs=config.epochs,
            best_score_file=config.best_score_file,
        )
        return model_trainer_config

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        config = self.config.model_evaluation

        create_directories([config.root_dir])

        model_eval_config = ModelEvaluationConfig(
            root_dir=config.root_dir,
            data_dir=config.data_dir,
            best_score_file=config.best_score_file,
            history_len=config.history_len,
            model=config.model,
        )
        return model_eval_config