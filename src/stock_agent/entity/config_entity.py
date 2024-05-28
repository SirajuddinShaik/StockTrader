from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_URL: str
    local_data_file: Path


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    data_dir: Path
    STATUS_FILE: Path


@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_dir: Path
    file_name: str

@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    data_dir: Path  
    alpha: float
    beta: float
    gamma: float
    max_size: int
    tau: float
    batch_size: int
    history_len : int
    re_train: bool
    epochs: int
    best_score_file: Path