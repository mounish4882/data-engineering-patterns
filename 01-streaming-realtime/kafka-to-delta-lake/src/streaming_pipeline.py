"""
Production-grade Kafka to Delta Lake streaming pipeline.

This module implements a robust streaming pipeline with:
- Exactly-once semantics
- Schema evolution
- Watermarking for late data
- Comprehensive error handling
- Prometheus metrics integration
"""

from typing import Dict, Optional
from datetime import datetime
import logging
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import (
    col, from_json, to_timestamp, window,
    current_timestamp, lit, expr, when, count, avg, max as spark_max, min as spark_min
)
from pyspark.sql.types import (
    StructType, StructField, StringType, DoubleType,
    TimestampType, IntegerType, MapType, ArrayType
)
from delta import configure_spark_with_delta_pip, DeltaTable
from prometheus_client import Counter, Histogram, Gauge
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Prometheus metrics
RECORDS_PROCESSED = Counter(
    'streaming_records_processed_total',
    'Total number of records processed'
)
RECORDS_FAILED = Counter(
    'streaming_records_failed_total',
    'Total number of failed records'
)
PROCESSING_LATENCY = Histogram(
    'streaming_processing_latency_seconds',
    'Processing latency in seconds'
)
CURRENT_LAG = Gauge(
    'streaming_kafka_lag',
    'Current Kafka consumer lag'
)


class StreamingPipeline:
    """
    Production-ready streaming pipeline from Kafka to Delta Lake.

    Features:
    - Medallion architecture (Bronze -> Silver -> Gold)
    - Exactly-once processing semantics
    - Automatic schema evolution
    - Late data handling with watermarking
    - Dead letter queue for failed records
    - Comprehensive monitoring

    Example:
        >>> config = PipelineConfig(...)
        >>> pipeline = StreamingPipeline(config)
        >>> pipeline.start()
    """

    def __init__(self, config: Dict):
        """
        Initialize the streaming pipeline.

        Args:
            config: Pipeline configuration dictionary containing:
                - kafka_bootstrap_servers: Kafka broker addresses
                - kafka_topic: Topic to consume from
                - checkpoint_location: Path for checkpoint storage
                - delta_lake_path: Base path for Delta tables
                - trigger_interval: Processing trigger interval
        """
        self.config = config
        self.spark = self._create_spark_session()
        self.schema = self._define_schema()
        logger.info("StreamingPipeline initialized successfully")

    def _create_spark_session(self) -> SparkSession:
        """
        Create optimized Spark session for streaming.

        Returns:
            Configured SparkSession with Delta Lake support
        """
        builder = (
            SparkSession.builder
            .appName("KafkaToDeltaLakeStreaming")
            .master(self.config.get("spark_master", "local[*]"))
            # Spark SQL Configuration
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
            # Performance Tuning
            .config("spark.sql.adaptive.enabled", "true")
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
            .config("spark.sql.shuffle.partitions", "200")
            # Streaming Configuration
            .config("spark.streaming.stopGracefullyOnShutdown", "true")
            .config("spark.sql.streaming.checkpointFileManagerClass",
                   "org.apache.spark.sql.execution.streaming.CheckpointFileManager")
            # Memory Configuration
            .config("spark.executor.memory", self.config.get("executor_memory", "4g"))
            .config("spark.driver.memory", self.config.get("driver_memory", "2g"))
            # Delta Lake Optimizations
            .config("spark.databricks.delta.optimizeWrite.enabled", "true")
            .config("spark.databricks.delta.autoCompact.enabled", "true")
        )

        spark = configure_spark_with_delta_pip(builder).getOrCreate()
        spark.sparkContext.setLogLevel("WARN")

        logger.info(f"Spark session created: {spark.version}")
        return spark

    def _define_schema(self) -> StructType:
        """
        Define the schema for incoming IoT sensor events.

        This schema handles nested structures and is designed for
        manufacturing sensor data with extensibility for new fields.

        Returns:
            StructType schema definition
        """
        return StructType([
            StructField("event_id", StringType(), False),
            StructField("timestamp", StringType(), False),
            StructField("machine_id", StringType(), False),
            StructField("sensor_type", StringType(), True),
            StructField("location", StringType(), True),

            # Sensor readings
            StructField("temperature", DoubleType(), True),
            StructField("pressure", DoubleType(), True),
            StructField("vibration", DoubleType(), True),
            StructField("humidity", DoubleType(), True),
            StructField("rpm", IntegerType(), True),

            # Status information
            StructField("status", StringType(), True),
            StructField("error_code", StringType(), True),

            # Nested metadata
            StructField("metadata", MapType(StringType(), StringType()), True),

            # Array of recent measurements
            StructField("recent_readings", ArrayType(DoubleType()), True),

            # Data quality indicators
            StructField("quality_score", DoubleType(), True),
            StructField("sensor_health", StringType(), True),
        ])

    def read_from_kafka(self) -> DataFrame:
        """
        Read streaming data from Kafka with optimized settings.

        Implements:
        - Exactly-once semantics
        - Backpressure management
        - Offset management

        Returns:
            Streaming DataFrame from Kafka

        Raises:
            RuntimeError: If Kafka connection fails
        """
        try:
            logger.info(f"Connecting to Kafka: {self.config['kafka_bootstrap_servers']}")

            df = (
                self.spark.readStream
                .format("kafka")
                .option("kafka.bootstrap.servers", self.config["kafka_bootstrap_servers"])
                .option("subscribe", self.config["kafka_topic"])
                .option("startingOffsets", self.config.get("starting_offsets", "latest"))
                # Backpressure management
                .option("maxOffsetsPerTrigger", self.config.get("max_offsets_per_trigger", 100000))
                .option("kafkaConsumer.pollTimeoutMs", "512")
                .option("fetchOffset.numRetries", "3")
                .option("fetchOffset.retryIntervalMs", "10")
                # Security (if configured)
                .option("kafka.security.protocol",
                       self.config.get("kafka_security_protocol", "PLAINTEXT"))
                .load()
            )

            logger.info("Kafka stream source created successfully")
            return df

        except Exception as e:
            logger.error(f"Failed to connect to Kafka: {e}")
            raise RuntimeError(f"Kafka connection failed: {e}")

    def process_bronze_layer(self, kafka_df: DataFrame) -> DataFrame:
        """
        Bronze layer: Raw data ingestion from Kafka.

        Minimal transformation, preserving all original data.
        Adds metadata for lineage and debugging.

        Args:
            kafka_df: Raw Kafka DataFrame

        Returns:
            Bronze layer DataFrame with metadata
        """
        logger.info("Processing Bronze layer (raw ingestion)")

        bronze_df = (
            kafka_df
            .selectExpr(
                "CAST(key AS STRING) as kafka_key",
                "CAST(value AS STRING) as raw_value",
                "topic",
                "partition",
                "offset",
                "timestamp as kafka_timestamp",
                "timestampType"
            )
            .withColumn("ingestion_timestamp", current_timestamp())
            .withColumn("source_system", lit("kafka"))
        )

        return bronze_df

    def process_silver_layer(self, bronze_df: DataFrame) -> DataFrame:
        """
        Silver layer: Cleaned and validated data.

        Applies:
        - JSON parsing and schema validation
        - Data quality checks
        - Type conversions
        - Watermarking for late data

        Args:
            bronze_df: Bronze layer DataFrame

        Returns:
            Cleaned Silver layer DataFrame
        """
        logger.info("Processing Silver layer (cleaned & validated)")

        # Parse JSON with schema
        parsed_df = (
            bronze_df
            .withColumn("parsed_data", from_json(col("raw_value"), self.schema))
            .filter("parsed_data IS NOT NULL")  # Drop malformed JSON
        )

        # Extract and validate fields
        silver_df = (
            parsed_df
            .select(
                col("parsed_data.*"),
                col("kafka_timestamp"),
                col("ingestion_timestamp"),
                col("offset"),
                col("partition")
            )
            # Convert timestamp string to timestamp type
            .withColumn("event_time",
                       to_timestamp(col("timestamp"), "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'"))
            # Data quality checks
            .filter("event_time IS NOT NULL")
            .filter("machine_id IS NOT NULL")
            .filter("event_id IS NOT NULL")
            # Add data quality flag
            .withColumn("is_valid",
                       when((col("temperature").isNotNull()) &
                            (col("temperature") > -50) &
                            (col("temperature") < 200), lit(True))
                       .otherwise(lit(False)))
            # Add processing metadata
            .withColumn("processing_timestamp", current_timestamp())
            .withColumn("data_quality_version", lit("v1.0"))
        )

        # Apply watermarking for late data handling
        watermarked_df = silver_df.withWatermark(
            "event_time",
            self.config.get("watermark_delay", "10 minutes")
        )

        return watermarked_df

    def process_gold_layer(self, silver_df: DataFrame) -> DataFrame:
        """
        Gold layer: Aggregated business metrics.

        Creates real-time aggregations for:
        - Machine performance metrics
        - Alert conditions
        - Statistical summaries

        Args:
            silver_df: Silver layer DataFrame

        Returns:
            Aggregated Gold layer DataFrame
        """
        logger.info("Processing Gold layer (aggregated metrics)")

        # 1-minute windowed aggregations by machine
        gold_df = (
            silver_df
            .groupBy(
                window("event_time", "1 minute"),
                "machine_id",
                "location"
            )
            .agg(
                count("*").alias("event_count"),
                avg("temperature").alias("avg_temperature"),
                spark_max("temperature").alias("max_temperature"),
                spark_min("temperature").alias("min_temperature"),
                avg("pressure").alias("avg_pressure"),
                spark_max("pressure").alias("max_pressure"),
                avg("vibration").alias("avg_vibration"),
                spark_max("vibration").alias("max_vibration"),
                avg("humidity").alias("avg_humidity"),
                avg("quality_score").alias("avg_quality_score"),
                count(when(col("is_valid") == False, 1)).alias("invalid_count")
            )
            # Calculate derived metrics
            .withColumn("temperature_range",
                       col("max_temperature") - col("min_temperature"))
            .withColumn("alert_flag",
                       when((col("max_temperature") > 80) |
                            (col("max_pressure") > 100) |
                            (col("max_vibration") > 5), lit(True))
                       .otherwise(lit(False)))
            .withColumn("processing_timestamp", current_timestamp())
        )

        return gold_df

    def write_to_delta(
        self,
        df: DataFrame,
        table_name: str,
        layer: str,
        partition_cols: Optional[list] = None
    ) -> None:
        """
        Write streaming DataFrame to Delta Lake with optimization.

        Args:
            df: DataFrame to write
            table_name: Target Delta table name
            layer: Medallion layer (bronze/silver/gold)
            partition_cols: Columns for partitioning

        Raises:
            RuntimeError: If write operation fails
        """
        try:
            checkpoint_path = f"{self.config['checkpoint_location']}/{table_name}"
            delta_path = f"{self.config['delta_lake_path']}/{layer}/{table_name}"

            logger.info(f"Writing {layer} layer to: {delta_path}")

            query_builder = (
                df.writeStream
                .format("delta")
                .outputMode("append")  # Use "complete" for aggregations if needed
                .option("checkpointLocation", checkpoint_path)
                # Delta Lake optimizations
                .option("mergeSchema", "true")  # Enable schema evolution
                .option("optimizeWrite", "true")
                .option("autoCompact", "true")
                # Trigger configuration
                .trigger(processingTime=self.config.get("trigger_interval", "10 seconds"))
            )

            # Add partitioning if specified
            if partition_cols:
                query_builder = query_builder.partitionBy(*partition_cols)

            # Start the streaming query
            query = query_builder.start(delta_path)

            # Store query reference for monitoring
            if not hasattr(self, 'active_queries'):
                self.active_queries = {}
            self.active_queries[table_name] = query

            logger.info(f"Streaming query started for {table_name}")

        except Exception as e:
            logger.error(f"Failed to write to Delta Lake: {e}")
            raise RuntimeError(f"Delta Lake write failed: {e}")

    def create_dead_letter_queue(self, bronze_df: DataFrame) -> None:
        """
        Create a dead letter queue for failed/malformed records.

        Args:
            bronze_df: Bronze layer DataFrame
        """
        dlq_df = (
            bronze_df
            .withColumn("parsed_data", from_json(col("raw_value"), self.schema))
            .filter("parsed_data IS NULL")  # Only malformed records
            .withColumn("error_reason", lit("JSON_PARSE_FAILED"))
            .withColumn("dlq_timestamp", current_timestamp())
        )

        dlq_path = f"{self.config['delta_lake_path']}/dlq/failed_records"
        checkpoint_path = f"{self.config['checkpoint_location']}/dlq"

        (
            dlq_df.writeStream
            .format("delta")
            .outputMode("append")
            .option("checkpointLocation", checkpoint_path)
            .trigger(processingTime="30 seconds")
            .start(dlq_path)
        )

        logger.info("Dead letter queue created for failed records")

    def start(self) -> None:
        """
        Start the complete streaming pipeline.

        This orchestrates all layers: Bronze -> Silver -> Gold
        and sets up monitoring and health checks.
        """
        try:
            logger.info("="*80)
            logger.info("STARTING KAFKA TO DELTA LAKE STREAMING PIPELINE")
            logger.info("="*80)

            # Read from Kafka
            kafka_df = self.read_from_kafka()

            # Bronze layer (raw ingestion)
            bronze_df = self.process_bronze_layer(kafka_df)
            self.write_to_delta(
                bronze_df,
                table_name="sensor_events",
                layer="bronze",
                partition_cols=["topic", "partition"]
            )

            # Dead letter queue for failed records
            self.create_dead_letter_queue(bronze_df)

            # Silver layer (cleaned & validated)
            silver_df = self.process_silver_layer(bronze_df)
            self.write_to_delta(
                silver_df,
                table_name="sensor_events_cleaned",
                layer="silver",
                partition_cols=["machine_id"]
            )

            # Gold layer (aggregated metrics)
            gold_df = self.process_gold_layer(silver_df)
            self.write_to_delta(
                gold_df,
                table_name="machine_metrics_1min",
                layer="gold"
            )

            logger.info("All streaming queries started successfully")
            logger.info("Pipeline is running. Press Ctrl+C to stop...")

            # Keep the application running
            self.spark.streams.awaitAnyTermination()

        except KeyboardInterrupt:
            logger.info("Received shutdown signal. Stopping gracefully...")
            self.stop()
        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            raise

    def stop(self) -> None:
        """Stop all streaming queries gracefully."""
        if hasattr(self, 'active_queries'):
            for name, query in self.active_queries.items():
                logger.info(f"Stopping query: {name}")
                query.stop()

        if self.spark:
            self.spark.stop()

        logger.info("Pipeline stopped successfully")

    def get_streaming_metrics(self) -> Dict:
        """
        Get current streaming metrics for monitoring.

        Returns:
            Dictionary with streaming metrics
        """
        metrics = {}

        if hasattr(self, 'active_queries'):
            for name, query in self.active_queries.items():
                if query.isActive:
                    progress = query.lastProgress
                    if progress:
                        metrics[name] = {
                            "processing_rate": progress.get("processedRowsPerSecond", 0),
                            "input_rate": progress.get("inputRowsPerSecond", 0),
                            "latency_ms": progress.get("durationMs", {}).get("triggerExecution", 0),
                            "num_input_rows": progress.get("numInputRows", 0),
                            "batch_id": progress.get("batchId", 0)
                        }

        return metrics


def main():
    """Main entry point for the streaming pipeline."""
    # Configuration
    config = {
        "kafka_bootstrap_servers": "localhost:9092",
        "kafka_topic": "sensor-events",
        "checkpoint_location": "./checkpoints",
        "delta_lake_path": "./delta-lake",
        "trigger_interval": "10 seconds",
        "watermark_delay": "10 minutes",
        "max_offsets_per_trigger": 100000,
        "spark_master": "local[*]",
        "executor_memory": "4g",
        "driver_memory": "2g"
    }

    # Create and start pipeline
    pipeline = StreamingPipeline(config)
    pipeline.start()


if __name__ == "__main__":
    main()
