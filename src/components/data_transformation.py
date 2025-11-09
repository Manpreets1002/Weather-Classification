from src.core.spark_manager import SparkManager
from src.logger import logging
from src.exception import CustomException
from src.utils import TIME

import os
import sys
from dataclasses import dataclass

from pyspark.sql.types import StringType,NumericType
from pyspark.sql.functions import col
from pyspark.ml.feature import StringIndexer,VectorAssembler,OneHotEncoder,StandardScaler
from pyspark.ml.pipeline import Pipeline
from pyspark.ml.linalg import VectorUDT

LABEL_NAME = "weather_condition"

@dataclass
class DataTransformationConfig:
    pipeline_path: str = os.path.join("artifacts",TIME,"pipeline.pkl")
    train_data_path: str = os.path.join("artifacts",TIME,"Training","train_data.parquet")
    test_data_path: str = os.path.join("artifacts",TIME,"Training","test_data.parquet")


class DataTransformation:
    def __init__(self):
        self.transform_config = DataTransformationConfig()
        self.spark = SparkManager.get_spark()

    def pipeline_formation(df):
        cat_col = [f.name for f in df.schema.fields if isinstance(f.datatype,StringType) and f.name != LABEL_NAME]
        num_col = [f.name for f in df.schema.fields if isinstance(f.datatype,NumericType) and f.name != LABEL_NAME]

        indexer = [StringIndexer(inputCol=c, outputCol=c + "_index", handleInvalid="keep") for c in cat_col]
        encoder = [OneHotEncoder(inputCol=c + "_index", outputCol=c + "_vector") for c in cat_col]

        num_assembler = VectorAssembler(inputCols=num_col, outputCol="numeric_features")
        scaler = StandardScaler(inputCol="numeric_features", outputCol="scaled_numeric_features")
        
        assembler_input = [c + "_vec" for c in cat_col] + ["scaled_numeric_features"]
        final_assembler = VectorAssembler(inputCols=assembler_input,outputCol="features")

        pipeline = Pipeline(stages=indexer + encoder + [num_assembler + scaler + final_assembler])

        return pipeline


    def transformation_pipeline(self,train_path,test_path):
        try:
            logging.info("Transformation Pipeline Started")
            train_data = self.spark.read.csv(train_path)
            test_data = self.spark.read.csv(test_path)
            logging.info("Data Read Successfully")

            logging.info("Pipeline Creation Started")
            preprocessor = self.pipeline_formation(train_data)
            logging.info("Pipeline Created")

            preprocessor = preprocessor.fit(train_data)
            logging.info("Pipeline Model Fitted")

            train_transformed_data = preprocessor.transform(train_data)
            test_transformed_data = preprocessor.transform(test_data)
            logging.info("Training & Testing data converted")

            preprocessor.write().overwrite().save(self.transform_config.pipeline_path)
            logging.info("Pipeline Saved Successfully")

            train_df = train_transformed_data.select(
                col("features").cast(VectorUDT()),
                col(LABEL_NAME).alias("label")
            )

            test_df = test_transformed_data.select(
                col("features").cast(VectorUDT()),
                col(LABEL_NAME).alias("label")
            )

            train_df.write().overwrite().save(self.transform_config.train_data_path)
            test_df.write().overwrite().save(self.transform_config.test_data_path)
            logging.info("Training Data Saved")

            logging.info("Transformation Completed")
            return self.transform_config.train_data_path,self.transform_config.test_data_path,self.transform_config.pipeline_path
        except Exception as e:
            raise CustomException(e,sys)