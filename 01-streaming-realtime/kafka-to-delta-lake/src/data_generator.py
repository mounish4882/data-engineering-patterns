"""
Realistic IoT sensor data generator for testing the streaming pipeline.

Generates manufacturing sensor events with:
- Realistic patterns (daily cycles, anomalies)
- Multiple machine types
- Schema evolution simulation
- Configurable event rates
"""

import json
import random
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import argparse
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError
import numpy as np

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class MachineProfile:
    """Profile for a manufacturing machine with normal operating parameters."""
    machine_id: str
    machine_type: str
    location: str
    temp_mean: float
    temp_std: float
    pressure_mean: float
    pressure_std: float
    vibration_mean: float
    vibration_std: float
    rpm_mean: int
    rpm_std: int
    failure_rate: float = 0.001  # 0.1% chance of failure per event


class SensorDataGenerator:
    """
    Generate realistic IoT sensor data for manufacturing equipment.

    Features:
    - Multiple machine profiles
    - Daily operational patterns
    - Random anomalies and failures
    - Schema evolution (v1, v2, v3)
    - Configurable event rates

    Example:
        >>> generator = SensorDataGenerator(
        ...     kafka_brokers="localhost:9092",
        ...     topic="sensor-events"
        ... )
        >>> generator.generate_continuous(events_per_second=100)
    """

    def __init__(
        self,
        kafka_brokers: str = "localhost:9092",
        topic: str = "sensor-events",
        num_machines: int = 10
    ):
        """
        Initialize the data generator.

        Args:
            kafka_brokers: Comma-separated Kafka broker addresses
            topic: Kafka topic to produce to
            num_machines: Number of machines to simulate
        """
        self.kafka_brokers = kafka_brokers
        self.topic = topic
        self.producer = self._create_producer()
        self.machines = self._create_machine_profiles(num_machines)
        self.schema_version = 1
        self.events_sent = 0
        self.errors = 0

        logger.info(f"Initialized generator with {num_machines} machines")

    def _create_producer(self) -> KafkaProducer:
        """Create Kafka producer with optimized settings."""
        try:
            producer = KafkaProducer(
                bootstrap_servers=self.kafka_brokers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
                # Performance settings
                compression_type='snappy',
                batch_size=32768,
                linger_ms=10,
                buffer_memory=67108864,
                # Reliability settings
                acks='all',
                retries=3,
                max_in_flight_requests_per_connection=5
            )
            logger.info("Kafka producer created successfully")
            return producer

        except Exception as e:
            logger.error(f"Failed to create Kafka producer: {e}")
            raise

    def _create_machine_profiles(self, num_machines: int) -> List[MachineProfile]:
        """Create diverse machine profiles for realistic simulation."""
        machine_types = [
            ("Assembly", "FactoryFloor_A", 65, 5, 45, 8, 1.2, 0.3, 1800, 100),
            ("Welding", "FactoryFloor_A", 85, 10, 60, 12, 2.5, 0.5, 1200, 150),
            ("CNC", "FactoryFloor_B", 70, 7, 50, 10, 1.8, 0.4, 2400, 200),
            ("Paint", "FactoryFloor_B", 75, 8, 35, 6, 0.8, 0.2, 900, 80),
            ("Packaging", "FactoryFloor_C", 60, 6, 30, 5, 0.5, 0.1, 600, 50),
        ]

        profiles = []
        for i in range(num_machines):
            machine_type_data = machine_types[i % len(machine_types)]
            machine_type, location, temp_m, temp_s, press_m, press_s, vib_m, vib_s, rpm_m, rpm_s = machine_type_data

            profile = MachineProfile(
                machine_id=f"MACH-{i+1:04d}",
                machine_type=machine_type,
                location=location,
                temp_mean=temp_m,
                temp_std=temp_s,
                pressure_mean=press_m,
                pressure_std=press_s,
                vibration_mean=vib_m,
                vibration_std=vib_s,
                rpm_mean=rpm_m,
                rpm_std=rpm_s
            )
            profiles.append(profile)

        return profiles

    def _apply_daily_pattern(self, base_value: float, hour: int) -> float:
        """
        Apply daily operational pattern (8AM-6PM higher load).

        Args:
            base_value: Base sensor value
            hour: Hour of day (0-23)

        Returns:
            Adjusted value based on time of day
        """
        if 8 <= hour <= 18:  # Working hours
            multiplier = 1.0 + (np.sin((hour - 8) * np.pi / 10) * 0.15)
        else:  # Off hours
            multiplier = 0.7 + random.uniform(-0.1, 0.1)

        return base_value * multiplier

    def _inject_anomaly(self, profile: MachineProfile, current_time: datetime) -> bool:
        """
        Randomly inject anomalies/failures.

        Returns:
            True if anomaly was injected
        """
        return random.random() < profile.failure_rate

    def generate_event_v1(self, profile: MachineProfile) -> Dict:
        """
        Generate schema v1 event (basic fields).

        Args:
            profile: Machine profile

        Returns:
            Event dictionary
        """
        now = datetime.utcnow()
        hour = now.hour

        # Apply daily patterns
        temp = self._apply_daily_pattern(
            np.random.normal(profile.temp_mean, profile.temp_std),
            hour
        )
        pressure = self._apply_daily_pattern(
            np.random.normal(profile.pressure_mean, profile.pressure_std),
            hour
        )
        vibration = self._apply_daily_pattern(
            np.random.normal(profile.vibration_mean, profile.vibration_std),
            hour
        )

        # Check for anomalies
        is_anomaly = self._inject_anomaly(profile, now)
        status = "FAULT" if is_anomaly else "NORMAL"

        if is_anomaly:
            temp *= random.uniform(1.3, 1.8)
            pressure *= random.uniform(1.2, 1.5)
            vibration *= random.uniform(2.0, 3.0)

        event = {
            "event_id": str(uuid.uuid4()),
            "timestamp": now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
            "machine_id": profile.machine_id,
            "sensor_type": "multi-sensor",
            "location": profile.location,
            "temperature": round(temp, 2),
            "pressure": round(pressure, 2),
            "vibration": round(vibration, 3),
            "humidity": round(random.uniform(30, 70), 1),
            "rpm": int(np.random.normal(profile.rpm_mean, profile.rpm_std)),
            "status": status,
            "error_code": f"ERR-{random.randint(1000,9999)}" if is_anomaly else None
        }

        return event

    def generate_event_v2(self, profile: MachineProfile) -> Dict:
        """
        Generate schema v2 event (adds metadata and quality metrics).

        Args:
            profile: Machine profile

        Returns:
            Event dictionary with extended schema
        """
        event = self.generate_event_v1(profile)

        # Add v2 fields
        event["metadata"] = {
            "firmware_version": f"v{random.randint(1,5)}.{random.randint(0,9)}",
            "calibration_date": (datetime.utcnow() - timedelta(days=random.randint(1,90))).strftime("%Y-%m-%d"),
            "operator_id": f"OP-{random.randint(100,999)}",
            "shift": "A" if 6 <= datetime.utcnow().hour < 14 else "B" if 14 <= datetime.utcnow().hour < 22 else "C"
        }

        event["quality_score"] = round(random.uniform(0.85, 0.99) if event["status"] == "NORMAL" else random.uniform(0.3, 0.7), 3)
        event["sensor_health"] = "GOOD" if event["quality_score"] > 0.9 else "DEGRADED" if event["quality_score"] > 0.7 else "POOR"

        return event

    def generate_event_v3(self, profile: MachineProfile) -> Dict:
        """
        Generate schema v3 event (adds arrays and advanced analytics).

        Args:
            profile: Machine profile

        Returns:
            Event dictionary with full schema
        """
        event = self.generate_event_v2(profile)

        # Add v3 fields
        event["recent_readings"] = [
            round(random.uniform(event["temperature"] - 5, event["temperature"] + 5), 2)
            for _ in range(5)
        ]

        event["metadata"]["maintenance_history"] = random.choice([
            "Last maintenance 30 days ago",
            "Last maintenance 60 days ago",
            "Last maintenance 15 days ago"
        ])

        return event

    def generate_event(self, profile: MachineProfile) -> Dict:
        """
        Generate event with current schema version.

        Args:
            profile: Machine profile

        Returns:
            Event dictionary
        """
        if self.schema_version == 1:
            return self.generate_event_v1(profile)
        elif self.schema_version == 2:
            return self.generate_event_v2(profile)
        else:
            return self.generate_event_v3(profile)

    def send_event(self, event: Dict) -> bool:
        """
        Send event to Kafka.

        Args:
            event: Event dictionary

        Returns:
            True if successfully sent
        """
        try:
            future = self.producer.send(
                self.topic,
                key=event["machine_id"],
                value=event
            )

            # Wait for send to complete (with timeout)
            future.get(timeout=5)
            self.events_sent += 1

            if self.events_sent % 1000 == 0:
                logger.info(f"Sent {self.events_sent} events (Schema v{self.schema_version})")

            return True

        except KafkaError as e:
            logger.error(f"Failed to send event: {e}")
            self.errors += 1
            return False

    def generate_continuous(
        self,
        events_per_second: int = 100,
        duration_seconds: Optional[int] = None,
        evolve_schema: bool = True
    ) -> None:
        """
        Generate continuous stream of events.

        Args:
            events_per_second: Target event rate
            duration_seconds: Run duration (None = infinite)
            evolve_schema: Whether to evolve schema over time
        """
        logger.info("="*80)
        logger.info(f"Starting continuous data generation")
        logger.info(f"Target rate: {events_per_second} events/sec")
        logger.info(f"Machines: {len(self.machines)}")
        logger.info(f"Schema evolution: {evolve_schema}")
        logger.info("="*80)

        start_time = time.time()
        events_generated = 0
        schema_evolution_interval = 300  # Evolve schema every 5 minutes

        try:
            while True:
                batch_start = time.time()

                # Generate batch of events
                for _ in range(events_per_second):
                    profile = random.choice(self.machines)
                    event = self.generate_event(profile)
                    self.send_event(event)
                    events_generated += 1

                # Schema evolution
                if evolve_schema and events_generated % (events_per_second * schema_evolution_interval) == 0:
                    if self.schema_version < 3:
                        self.schema_version += 1
                        logger.info(f"🔄 Schema evolved to v{self.schema_version}")

                # Sleep to maintain target rate
                elapsed = time.time() - batch_start
                sleep_time = max(0, 1.0 - elapsed)
                time.sleep(sleep_time)

                # Check duration
                if duration_seconds and (time.time() - start_time) >= duration_seconds:
                    break

                # Print stats every 30 seconds
                if events_generated % (events_per_second * 30) == 0:
                    self._print_stats()

        except KeyboardInterrupt:
            logger.info("\nStopping data generation...")
        finally:
            self.producer.flush()
            self.producer.close()
            self._print_stats()
            logger.info("Data generator stopped")

    def _print_stats(self) -> None:
        """Print generation statistics."""
        logger.info(f"📊 Stats: Sent={self.events_sent}, Errors={self.errors}, "
                   f"Success Rate={100*(1-self.errors/max(1,self.events_sent)):.2f}%")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="IoT Sensor Data Generator")
    parser.add_argument("--kafka-brokers", default="localhost:9092",
                       help="Kafka bootstrap servers")
    parser.add_argument("--topic", default="sensor-events",
                       help="Kafka topic name")
    parser.add_argument("--machines", type=int, default=10,
                       help="Number of machines to simulate")
    parser.add_argument("--events-per-second", type=int, default=100,
                       help="Target events per second")
    parser.add_argument("--duration", type=int, default=None,
                       help="Duration in seconds (default: infinite)")
    parser.add_argument("--no-schema-evolution", action="store_true",
                       help="Disable schema evolution")

    args = parser.parse_args()

    generator = SensorDataGenerator(
        kafka_brokers=args.kafka_brokers,
        topic=args.topic,
        num_machines=args.machines
    )

    generator.generate_continuous(
        events_per_second=args.events_per_second,
        duration_seconds=args.duration,
        evolve_schema=not args.no_schema_evolution
    )


if __name__ == "__main__":
    main()
