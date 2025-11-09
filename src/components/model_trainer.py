from src.core.spark_manager import SparkManager
from src.logger import logging
from src.exception import CustomException
from src.utils import TIME

import os
import sys
from dataclasses import dataclass
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

@dataclass
class ModelTrainerConfig:
    model_path: str = os.path.join("artifacts",TIME,"model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_config = ModelTrainerConfig()
        self.spark = SparkManager.get_spark()

    def model_training(self,train_path,test_path):
        try:
            logging.info("Model Training Started")

            train_df = self.spark.read.parquet(train_path)
            test_df = self.spark.read.parquet(test_path)
            logging.info("Data Read Successfully")
            
            rf_class = RandomForestClassifier(
                featuresCol="features",
                labelCol="label",
                predictionCol="prediction",
                probabilityCol="probability",
                rawPredictionCol="raw_prediction",
                numTrees=100,
                maxDepth=8,
                featureSubsetStrategy="sqrt",
                impurity="gini",
                seed=42
            )
            
            model = rf_class.fit(train_df)
            logging.info("Model Created")
            predict = model.transform(test_df)

            evaluator = MulticlassClassificationEvaluator(labelCol="label",predictionCol="prediction",metricName="accuracy")
            logging.info("Evaluator Created")

            acc = evaluator.evaluate(predict)
            logging.info(f"Accuracy: {acc:.2f}")

            model.write().overwrite().save(self.model_config.model_path)
            logging.info("Model Saved")

            SparkManager.stop_spark()
            logging.info("Model Trained")
            return self.model_config.model_path
            
        except Exception as e:
            raise CustomException(e,sys)