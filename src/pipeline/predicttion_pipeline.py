from src.utils import MODEL_PATH,PIPELINE_PATH
from pyspark.sql import SparkSession
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml import PipelineModel
from src.logger import logging
from src.exception import CustomException
import sys

class Prediction:
    def __init__(self):
        self.spark = SparkSession.builder.appName("Testing").getOrCreate()
    
    def predict(self,test):
        try:
            logging.info(f"Spark Session {self.spark.sparkContext.appName} createde")
            pipeline = PipelineModel.load(PIPELINE_PATH)
            logging.info("Pipeline Loaded")
            model = RandomForestClassifier.load(MODEL_PATH)
            logging.info("Model Loaded")

            ytest = pipeline.transform(test)
            predict = model.transform(test)
            logging.info(predict.show())
        
        except Exception as e:
            raise CustomException(e,sys)