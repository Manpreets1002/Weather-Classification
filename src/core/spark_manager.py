from pyspark.sql import SparkSession

class SparkManager:
    _spark = None

    @staticmethod
    def get_spark(app_name: str = "WeatherOps"):
        if SparkManager._spark is None:
            SparkManager._spark = (
                SparkSession.builder
                .appName(app_name)
                .config("spark.sql.shuffle.partitions", "200")
                .config("spark.driver.memory", "4g")
                .config("spark.executor.memory", "4g")
                .config("spark.sql.execution.arrow.pyspark.enabled", "true")
                .getOrCreate()
            )
            SparkManager._spark.sparkContext.setLogLevel("WARN")
        return SparkManager._spark
    
    @staticmethod
    def stop_spark():
        if SparkManager._spark:
            SparkManager._spark.stop()
            SparkManager._spark = None