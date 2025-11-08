from src.core.spark_manager import SparkManager
from src.logger import logging
from src.exception import CustomException
from src.utils import TIME

import os
import sys
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join("artifacts",TIME,"raw_data.parquet")
    train_data_path: str = os.path.join("artifacts",TIME,"train_data.parquet")
    test_data_path: str = os.path.join("artifacts",TIME,"test_data.parquet")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        self.spark = SparkManager.get_spark()

    def ingestion_pipeline(self):
        try:
            logging.info("Ingestion Pipeline Started")
            raw_df = self.spark.read.csv("C:\\Users\\HP\\Github\\Weather-Classification\\Weather_Classification.csv")
            logging.info("Data Read Successfully")
            
            raw_df.write.mode("overwrite").save(self.ingestion_config.raw_data_path)
            logging.info("Raw Data Saved")

            train_df,test_df = raw_df.randomSplit([0.8,0.2],seed=42)

            train_df.write.mode("overwrite").save(self.ingestion_config.train_data_path)
            test_df.write.mode("overwrite").save(self.ingestion_config.test_data_path)
            logging.info("Training and Testing data saved")

            SparkManager.stop_spark()
            logging.info("Ingestion pipeline ended")
            return self.ingestion_config.train_data_path,self.ingestion_config.test_data_path
            
        except Exception as e:
            raise CustomException(e,sys)