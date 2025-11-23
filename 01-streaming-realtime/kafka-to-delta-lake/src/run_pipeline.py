#!/usr/bin/env python3
"""
Main entry point for the Kafka to Delta Lake streaming pipeline.

Usage:
    python run_pipeline.py
    python run_pipeline.py --config config/pipeline_config.yaml
"""

import argparse
import sys
import os
import logging
import signal
from typing import Optional
import yaml
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from streaming_pipeline import StreamingPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('pipeline.log')
    ]
)
logger = logging.getLogger(__name__)


def load_config(config_path: Optional[str] = None) -> dict:
    """
    Load configuration from YAML file or use defaults.

    Args:
        config_path: Path to configuration file

    Returns:
        Configuration dictionary
    """
    default_config = {
        "kafka_bootstrap_servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
        "kafka_topic": os.getenv("KAFKA_TOPIC", "sensor-events"),
        "checkpoint_location": os.getenv("CHECKPOINT_LOCATION", "./checkpoints"),
        "delta_lake_path": os.getenv("DELTA_LAKE_PATH", "./delta-lake"),
        "trigger_interval": "10 seconds",
        "watermark_delay": "10 minutes",
        "max_offsets_per_trigger": 100000,
        "spark_master": os.getenv("SPARK_MASTER", "local[*]"),
        "executor_memory": os.getenv("SPARK_EXECUTOR_MEMORY", "4g"),
        "driver_memory": os.getenv("SPARK_DRIVER_MEMORY", "2g"),
        "starting_offsets": "latest"
    }

    if config_path and os.path.exists(config_path):
        logger.info(f"Loading configuration from: {config_path}")
        with open(config_path, 'r') as f:
            file_config = yaml.safe_load(f)
            # Merge with defaults
            default_config.update(file_config)
    else:
        logger.info("Using default configuration")

    return default_config


def print_banner():
    """Print startup banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║      Kafka to Delta Lake Streaming Pipeline                 ║
    ║      Production-Grade Data Engineering Pattern              ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_config(config: dict):
    """Print configuration summary."""
    logger.info("="*80)
    logger.info("PIPELINE CONFIGURATION")
    logger.info("="*80)
    logger.info(f"Kafka Brokers:        {config['kafka_bootstrap_servers']}")
    logger.info(f"Kafka Topic:          {config['kafka_topic']}")
    logger.info(f"Delta Lake Path:      {config['delta_lake_path']}")
    logger.info(f"Checkpoint Location:  {config['checkpoint_location']}")
    logger.info(f"Trigger Interval:     {config['trigger_interval']}")
    logger.info(f"Watermark Delay:      {config['watermark_delay']}")
    logger.info(f"Max Offsets/Trigger:  {config['max_offsets_per_trigger']}")
    logger.info(f"Spark Master:         {config['spark_master']}")
    logger.info("="*80)


def setup_signal_handlers(pipeline: StreamingPipeline):
    """Setup signal handlers for graceful shutdown."""
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}. Initiating graceful shutdown...")
        pipeline.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def validate_prerequisites(config: dict) -> bool:
    """
    Validate that prerequisites are met.

    Args:
        config: Configuration dictionary

    Returns:
        True if all prerequisites are met
    """
    logger.info("Validating prerequisites...")

    # Check if checkpoint directory is writable
    checkpoint_dir = Path(config['checkpoint_location'])
    try:
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"✓ Checkpoint directory accessible: {checkpoint_dir}")
    except Exception as e:
        logger.error(f"✗ Cannot create checkpoint directory: {e}")
        return False

    # Check if delta lake directory is writable
    delta_dir = Path(config['delta_lake_path'])
    try:
        delta_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"✓ Delta Lake directory accessible: {delta_dir}")
    except Exception as e:
        logger.error(f"✗ Cannot create Delta Lake directory: {e}")
        return False

    # Note: Kafka connectivity will be checked when pipeline starts
    logger.info("✓ Prerequisites validation passed")
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Kafka to Delta Lake Streaming Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default configuration
  python run_pipeline.py

  # Run with custom configuration file
  python run_pipeline.py --config config/production.yaml

  # Run with environment variables
  export KAFKA_BOOTSTRAP_SERVERS=broker1:9092,broker2:9092
  export KAFKA_TOPIC=my-events
  python run_pipeline.py

For more information, see README.md
        """
    )

    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration YAML file"
    )

    parser.add_argument(
        "--kafka-brokers",
        type=str,
        help="Kafka bootstrap servers (overrides config)"
    )

    parser.add_argument(
        "--kafka-topic",
        type=str,
        help="Kafka topic to consume from (overrides config)"
    )

    parser.add_argument(
        "--delta-path",
        type=str,
        help="Delta Lake base path (overrides config)"
    )

    parser.add_argument(
        "--checkpoint-path",
        type=str,
        help="Checkpoint base path (overrides config)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate configuration without starting pipeline"
    )

    args = parser.parse_args()

    try:
        # Print banner
        print_banner()

        # Load configuration
        config = load_config(args.config)

        # Override with command-line arguments
        if args.kafka_brokers:
            config['kafka_bootstrap_servers'] = args.kafka_brokers
        if args.kafka_topic:
            config['kafka_topic'] = args.kafka_topic
        if args.delta_path:
            config['delta_lake_path'] = args.delta_path
        if args.checkpoint_path:
            config['checkpoint_location'] = args.checkpoint_path

        # Print configuration
        print_config(config)

        # Validate prerequisites
        if not validate_prerequisites(config):
            logger.error("Prerequisites validation failed. Exiting.")
            sys.exit(1)

        if args.dry_run:
            logger.info("Dry run completed successfully. Exiting.")
            sys.exit(0)

        # Create and start pipeline
        logger.info("Initializing streaming pipeline...")
        pipeline = StreamingPipeline(config)

        # Setup signal handlers for graceful shutdown
        setup_signal_handlers(pipeline)

        # Start the pipeline
        logger.info("Starting pipeline...")
        pipeline.start()

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Pipeline failed with error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
