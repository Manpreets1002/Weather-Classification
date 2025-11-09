from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.utils import MODEL_PATH,PIPELINE_PATH


class Training:
    def __init__(self):
        self.ingestion = DataIngestion()
        self.transformation = DataTransformation()
        self.model_train = ModelTrainer()

    def training(self):
        train_path,test_path = self.ingestion.ingestion_pipeline()
        transformed_train_path,transformed_test_path,pipeline_path = self.transformation.transformation_pipeline(train_path,test_path)
        model_path = self.model_train.model_training(transformed_train_path,transformed_test_path)

        PIPELINE_PATH = pipeline_path
        MODEL_PATH = model_path