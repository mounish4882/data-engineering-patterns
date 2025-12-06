# OPTION A: Fork & Rebuild Existing Repo for Manufacturing IoT

## 🎯 CONTEXT & OBJECTIVE

You are transforming the existing `data-engineering-patterns` repository into a **production-grade, enterprise-scale manufacturing IoT data platform reference**. This repo will reflect real-world patterns used in multi-plant manufacturing environments processing billions of records.

---

## 👤 MY BACKGROUND & USE CASES

### Primary Work
- **Senior Data Engineer** specializing in manufacturing IoT/industrial data
- **Scale**: Billions of records across multiple plants and domains
- **Tech Stack**: Kafka → Spark Streaming → Delta Lake → Databricks
- **Focus Areas**: Real-time data processing, dimensional modeling, performance optimization

### Daily Pain Points I Deal With
1. **Schema Evolution**: Handling `DELTA_MERGE_INCOMPATIBLE_DATATYPE` errors with MAP types in `customExtension` fields
2. **Authentication**: SASL_SSL Kafka configuration and troubleshooting in production
3. **Performance**: Eliminating unnecessary shuffles, optimizing 11-step progressive flattening, Spark UI analysis
4. **Architecture**: Kafka Streams preprocessing → Spark transformations, checkpointing strategies
5. **Dimensional Modeling**: SCD Type 2, multi-plant hierarchies, manufacturing fact tables
6. **DevOps**: Databricks bundles, HOCON configs, GitHub Actions deployment, multi-environment (dev/QA/prod)
7. **Integration**: SAP integration, OPP data processing, VasapiValidator testing

---

## 📋 TRANSFORMATION PLAN

### Phase 1: Restructure Repository (CRITICAL)

**Current structure** is tutorial-focused. Transform it to enterprise-focused:

```
data-engineering-patterns/
├── 01-production-authentication/          # NEW - Top priority
│   ├── kafka-sasl-ssl/
│   │   ├── README.md
│   │   ├── configs/
│   │   │   ├── sasl-plain-config.yaml
│   │   │   ├── sasl-scram-config.yaml
│   │   │   └── databricks-secrets-integration.py
│   │   ├── certificates/
│   │   │   ├── cert-setup-guide.md
│   │   │   └── truststore-keystore-management.md
│   │   └── troubleshooting/
│   │       ├── auth-failure-playbook.md
│   │       └── connection-debugging.py
│   └── databricks-unity-catalog-auth/
│
├── 02-schema-evolution-advanced/          # NEW - Critical pain point
│   ├── delta-type-conflicts/
│   │   ├── README.md
│   │   ├── src/
│   │   │   ├── schema_validator.py
│   │   │   ├── type_conflict_resolver.py
│   │   │   ├── incompatible_type_handler.py
│   │   │   └── schema_compatibility_checker.py
│   │   ├── examples/
│   │   │   ├── delta_merge_incompatible_datatype_fix.py
│   │   │   ├── map_type_evolution.py
│   │   │   └── nested_struct_changes.py
│   │   └── tests/
│   └── map-type-flattening/
│       ├── README.md  # Document your 11-step progressive strategy
│       ├── src/
│       │   ├── progressive_flattener.py
│       │   ├── custom_extension_handler.py
│       │   └── dynamic_schema_inference.py
│       └── examples/
│           └── manufacturing_iot_sensors.py
│
├── 03-streaming-realtime/                 # ENHANCE EXISTING
│   ├── kafka-to-delta-lake/              # Keep and enhance
│   │   ├── (existing files...)
│   │   └── ENHANCE with SASL_SSL integration
│   ├── kstreams-preprocessing/            # NEW - Your actual workflow
│   │   ├── README.md
│   │   ├── java-topology/
│   │   │   ├── pom.xml
│   │   │   └── src/main/java/
│   │   │       ├── PreprocessingTopology.java
│   │   │       ├── SensorDataValidator.java
│   │   │       ├── StatefulAggregator.java
│   │   │       └── SerdeFactory.java
│   │   ├── spark-consumer/
│   │   │   └── consume_preprocessed_stream.py
│   │   └── deployment/
│   │       ├── docker-compose.yml
│   │       └── kubernetes-manifests/
│   └── hybrid-architecture/               # NEW
│       ├── README.md
│       └── kstreams-spark-integration-pattern.md
│
├── 04-dimensional-modeling/               # NEW - Critical for your work
│   ├── manufacturing-star-schema/
│   │   ├── README.md
│   │   ├── schemas/
│   │   │   ├── dim_plant.sql
│   │   │   ├── dim_machine.sql
│   │   │   ├── dim_test_equipment.sql
│   │   │   ├── dim_date.sql
│   │   │   └── fact_manufacturing_test.sql
│   │   ├── src/
│   │   │   ├── dimension_builder.py
│   │   │   ├── scd_type2_handler.py
│   │   │   ├── fact_table_builder.py
│   │   │   └── surrogate_key_generator.py
│   │   └── examples/
│   │       ├── multi_plant_hierarchy.py
│   │       ├── scd2_machine_config.py
│   │       └── incremental_fact_load.py
│   └── slowly-changing-dimensions/
│       ├── README.md
│       ├── scd-type1.py
│       ├── scd-type2.py
│       └── scd-type3.py
│
├── 05-performance-optimization/           # NEW - Spark UI focus
│   ├── spark-ui-analysis/
│   │   ├── README.md  # Methodology guide
│   │   ├── guides/
│   │   │   ├── stage-analysis-methodology.md
│   │   │   ├── identifying-bottlenecks.md
│   │   │   ├── shuffle-optimization.md
│   │   │   └── memory-tuning-guide.md
│   │   ├── src/
│   │   │   ├── stage_analyzer.py
│   │   │   ├── skew_detector.py
│   │   │   ├── shuffle_analyzer.py
│   │   │   └── optimization_recommender.py
│   │   └── notebooks/
│   │       ├── spark_ui_deep_dive.ipynb
│   │       └── before_after_optimization.ipynb
│   ├── billion-record-optimization/
│   │   ├── README.md
│   │   ├── partition-sizing-calculator.py
│   │   ├── broadcast-join-optimizer.py
│   │   └── adaptive-query-execution-tuning.md
│   └── eliminating-shuffles/
│       ├── README.md
│       ├── shuffle-elimination-patterns.py
│       └── explosion-optimization.py
│
├── 06-databricks-deployment/             # NEW - Your deployment stack
│   ├── databricks-bundles/
│   │   ├── README.md
│   │   ├── databricks.yml
│   │   ├── resources/
│   │   │   ├── jobs/
│   │   │   │   ├── streaming-pipeline.yml
│   │   │   │   └── batch-processing.yml
│   │   │   ├── clusters/
│   │   │   │   ├── job-cluster.yml
│   │   │   │   └── all-purpose-cluster.yml
│   │   │   └── workflows/
│   │   │       └── manufacturing-etl.yml
│   │   └── environments/
│   │       ├── dev.yaml
│   │       ├── qa.yaml
│   │       └── prod.yaml
│   ├── hocon-configurations/
│   │   ├── README.md
│   │   ├── application.conf
│   │   └── environment-specific/
│   └── github-actions-cicd/
│       ├── README.md
│       ├── workflows/
│       │   ├── databricks-deploy.yml
│       │   ├── bundle-validate.yml
│       │   └── integration-tests.yml
│       └── scripts/
│           └── deploy-to-workspace.sh
│
├── 07-enterprise-integration/            # NEW - SAP & systems
│   ├── sap-integration/
│   │   ├── README.md
│   │   ├── cdc-patterns/
│   │   └── batch-extraction/
│   ├── change-data-capture/
│   │   ├── debezium-kafka-delta/
│   │   └── incremental-processing/
│   └── dependency-orchestration/
│
├── 08-testing-validation/                # NEW - VasapiValidator
│   ├── vasapi-validator-integration/
│   │   ├── README.md
│   │   └── test-framework-setup.md
│   ├── data-quality-tests/
│   └── integration-tests/
│
├── 09-production-playbooks/              # NEW - Troubleshooting guides
│   ├── troubleshooting/
│   │   ├── schema-evolution-errors.md
│   │   ├── kafka-auth-failures.md
│   │   ├── performance-degradation.md
│   │   └── checkpoint-recovery.md
│   ├── runbooks/
│   │   ├── pipeline-restart-procedure.md
│   │   ├── schema-migration-runbook.md
│   │   └── incident-response.md
│   └── monitoring/
│       ├── prometheus-alerts.yml
│       └── grafana-dashboards/
│
└── 10-real-world-case-studies/          # NEW - Your actual projects
    ├── multi-plant-streaming/
    │   └── README.md  # Document your actual architecture
    ├── billion-record-processing/
    └── opp-data-processing/
```

---

## 🎯 IMMEDIATE TASKS - START HERE

### Task 1: Production SASL_SSL Authentication (PRIORITY 1)

**Location**: `01-production-authentication/kafka-sasl-ssl/`

**Create these files:**

1. **README.md** - Comprehensive guide covering:
   - SASL_SSL overview and when to use each mechanism (PLAIN, SCRAM, GSSAPI)
   - Step-by-step setup for Databricks
   - Troubleshooting auth failures
   - Common errors and solutions

2. **configs/sasl-plain-config.yaml**:
```yaml
kafka:
  security_protocol: "SASL_SSL"
  sasl_mechanism: "PLAIN"
  ssl_truststore_location: "/dbfs/secrets/kafka.truststore.jks"
  ssl_truststore_password: "{{secrets/prod/kafka-truststore-pwd}}"
  sasl_jaas_config: |
    org.apache.kafka.common.security.plain.PlainLoginModule required
    username="{{secrets/prod/kafka-username}}"
    password="{{secrets/prod/kafka-password}}";
```

3. **configs/databricks-secrets-integration.py**:
```python
from pyspark.sql import SparkSession
import os

def get_kafka_sasl_ssl_config(env: str = "prod") -> dict:
    """
    Retrieve Kafka SASL_SSL configuration from Databricks secrets.

    Args:
        env: Environment (dev/qa/prod)

    Returns:
        Complete Kafka configuration dictionary
    """
    # Databricks secret scope integration
    secret_scope = f"kafka-{env}"

    config = {
        "kafka.bootstrap.servers": dbutils.secrets.get(secret_scope, "bootstrap-servers"),
        "kafka.security.protocol": "SASL_SSL",
        "kafka.sasl.mechanism": "PLAIN",
        "kafka.ssl.truststore.location": dbutils.secrets.get(secret_scope, "truststore-path"),
        "kafka.ssl.truststore.password": dbutils.secrets.get(secret_scope, "truststore-password"),
        "kafka.sasl.jaas.config": f"""org.apache.kafka.common.security.plain.PlainLoginModule required
            username="{dbutils.secrets.get(secret_scope, 'username')}"
            password="{dbutils.secrets.get(secret_scope, 'password')}";"""
    }

    return config

# Usage in streaming pipeline
def create_authenticated_kafka_stream(spark: SparkSession, topic: str, env: str):
    kafka_config = get_kafka_sasl_ssl_config(env)

    df = (
        spark.readStream
        .format("kafka")
        .options(**kafka_config)
        .option("subscribe", topic)
        .option("startingOffsets", "latest")
        .load()
    )

    return df
```

4. **troubleshooting/auth-failure-playbook.md**:
```markdown
# Kafka Authentication Failure Playbook

## Common Error: "Authentication failed: Invalid username or password"

### Diagnostic Steps:
1. Verify secret scope exists:
   ```python
   dbutils.secrets.listScopes()
   ```

2. Check secret values (masked):
   ```python
   # Should return [REDACTED], not error
   dbutils.secrets.get("kafka-prod", "username")
   ```

3. Test connectivity without SASL:
   ```bash
   telnet <broker-host> 9093
   ```

4. Validate JAAS config format...

[Continue with detailed troubleshooting]
```

---

### Task 2: Schema Evolution & Type Conflict Resolution (PRIORITY 1)

**Location**: `02-schema-evolution-advanced/delta-type-conflicts/`

**Create these files:**

1. **src/type_conflict_resolver.py**:
```python
from pyspark.sql import DataFrame
from pyspark.sql.types import StructType, DataType, StringType, IntegerType, LongType
from pyspark.sql.functions import col, expr
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class TypeConflictResolver:
    """
    Handles DELTA_MERGE_INCOMPATIBLE_DATATYPE errors in production.

    Your actual production scenarios:
        - customExtension: MAP<STRING, STRING> → MAP<STRING, STRUCT<...>>
        - Sensor fields: INT → LONG promotion
        - Nested struct evolution
    """

    def __init__(self):
        self.type_promotion_rules = {
            (IntegerType, LongType): "promote",
            (StringType, IntegerType): "cast_with_validation",
        }

    def identify_conflicts(
        self,
        source_schema: StructType,
        target_schema: StructType
    ) -> List[Dict]:
        """
        Identify type conflicts between source and target schemas.

        Returns:
            List of conflicts with recommended resolution strategy
        """
        conflicts = []

        source_fields = {f.name: f.dataType for f in source_schema.fields}
        target_fields = {f.name: f.dataType for f in target_schema.fields}

        for field_name in source_fields.keys() & target_fields.keys():
            source_type = source_fields[field_name]
            target_type = target_fields[field_name]

            if source_type != target_type:
                strategy = self._get_resolution_strategy(source_type, target_type)
                conflicts.append({
                    "field": field_name,
                    "source_type": str(source_type),
                    "target_type": str(target_type),
                    "strategy": strategy
                })

        return conflicts

    def resolve_conflicts(
        self,
        df: DataFrame,
        conflicts: List[Dict]
    ) -> DataFrame:
        """
        Apply conflict resolution strategies.

        Strategies:
            - promote: Safe type widening (INT → LONG)
            - cast_with_validation: Cast with null on failure
            - column_versioning: Create new versioned column
            - error: Incompatible, requires manual intervention
        """
        for conflict in conflicts:
            field = conflict["field"]
            strategy = conflict["strategy"]

            if strategy == "promote":
                df = df.withColumn(field, col(field).cast(conflict["target_type"]))

            elif strategy == "cast_with_validation":
                # Cast with null on failure instead of error
                df = df.withColumn(
                    field,
                    expr(f"try_cast({field} as {conflict['target_type']})")
                )

            elif strategy == "column_versioning":
                # Keep both versions
                df = df.withColumnRenamed(field, f"{field}_v1")
                logger.warning(f"Created versioned column: {field}_v1")

            elif strategy == "error":
                raise ValueError(
                    f"Incompatible type conflict for {field}: "
                    f"{conflict['source_type']} → {conflict['target_type']}. "
                    "Manual intervention required."
                )

        return df

    def _get_resolution_strategy(
        self,
        source_type: DataType,
        target_type: DataType
    ) -> str:
        """Determine resolution strategy based on type pair."""
        type_pair = (type(source_type), type(target_type))

        if type_pair in self.type_promotion_rules:
            return self.type_promotion_rules[type_pair]

        # MAP type special handling
        if "MapType" in str(type(source_type)) and "MapType" in str(type(target_type)):
            return "map_evolution"  # Custom handler

        # Default: Create versioned column
        return "column_versioning"

# Production usage example
def safe_delta_merge_with_schema_evolution(
    source_df: DataFrame,
    target_path: str,
    merge_keys: List[str]
):
    """
    Your actual production merge with conflict handling.
    """
    from delta.tables import DeltaTable

    resolver = TypeConflictResolver()
    target_table = DeltaTable.forPath(spark, target_path)

    # Identify conflicts
    conflicts = resolver.identify_conflicts(
        source_df.schema,
        target_table.toDF().schema
    )

    if conflicts:
        logger.warning(f"Found {len(conflicts)} schema conflicts. Resolving...")
        for conflict in conflicts:
            logger.warning(f"  - {conflict}")

        # Resolve conflicts
        source_df = resolver.resolve_conflicts(source_df, conflicts)

    # Proceed with merge
    target_table.alias("target").merge(
        source_df.alias("source"),
        " AND ".join([f"target.{k} = source.{k}" for k in merge_keys])
    ).whenMatchedUpdateAll() \
     .whenNotMatchedInsertAll() \
     .execute()

    logger.info("Delta merge completed successfully")
```

2. **src/custom_extension_handler.py** (Your MAP type flattening):
```python
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, explode, map_keys, map_values, expr
from typing import List, Optional

class CustomExtensionFlattener:
    """
    11-step progressive flattening strategy for customExtension MAP fields.

    Your production pattern for handling unpredictable MAP<STRING, STRING> fields
    from manufacturing IoT sensors.
    """

    def __init__(self, map_column: str = "customExtension"):
        self.map_column = map_column
        self.known_keys = []  # Track discovered keys

    def progressive_flatten(
        self,
        df: DataFrame,
        known_keys: Optional[List[str]] = None,
        discover_keys: bool = True
    ) -> DataFrame:
        """
        Progressive flattening without unnecessary explosions.

        Steps:
            1. Discover keys (if enabled)
            2. Extract known keys as columns
            3. Handle null/missing keys
            4. Type inference for values
            5. Nested structure handling
            6. Optimize to avoid shuffle
            7-11. [Your specific steps]
        """
        # Step 1: Discover keys from sample
        if discover_keys:
            self.known_keys = self._discover_map_keys(df)
        elif known_keys:
            self.known_keys = known_keys

        # Step 2: Extract known keys without explosion
        for key in self.known_keys:
            df = df.withColumn(
                f"ext_{key}",
                col(self.map_column).getItem(key)
            )

        # Step 3: Handle remaining unknown keys (optional)
        # [Your implementation]

        return df

    def _discover_map_keys(self, df: DataFrame, sample_size: int = 1000) -> List[str]:
        """
        Discover all unique keys in MAP column from sample.
        Avoids full table scan.
        """
        keys_df = (
            df.select(explode(map_keys(col(self.map_column))).alias("key"))
            .limit(sample_size)
            .distinct()
        )

        discovered_keys = [row.key for row in keys_df.collect()]
        logger.info(f"Discovered {len(discovered_keys)} unique keys in {self.map_column}")

        return discovered_keys
```

---

### Task 3: Dimensional Modeling for Manufacturing (PRIORITY 2)

**Location**: `04-dimensional-modeling/manufacturing-star-schema/`

**Create these files:**

1. **schemas/dim_plant.sql**:
```sql
-- Dimension: Plant Master
-- Multi-level hierarchy for manufacturing plants

CREATE OR REPLACE TABLE dim.dim_plant (
    plant_sk BIGINT GENERATED ALWAYS AS IDENTITY,  -- Surrogate key
    plant_code STRING NOT NULL,                     -- Natural key
    plant_name STRING,
    plant_type STRING,                              -- Assembly, Testing, Packaging
    region STRING,
    country STRING,
    timezone STRING,

    -- Hierarchy
    site_code STRING,
    site_name STRING,
    division STRING,

    -- Operational metadata
    is_active BOOLEAN DEFAULT true,
    commissioning_date DATE,

    -- Audit columns
    effective_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_date TIMESTAMP,
    is_current BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Constraints
    CONSTRAINT pk_dim_plant PRIMARY KEY (plant_sk),
    CONSTRAINT uk_dim_plant UNIQUE (plant_code, effective_date)
)
USING DELTA
PARTITIONED BY (region);

-- Optimize for common queries
OPTIMIZE dim.dim_plant ZORDER BY (plant_code, site_code);
```

2. **src/scd_type2_handler.py**:
```python
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, lit, current_timestamp, when
from delta.tables import DeltaTable
from datetime import datetime
from typing import List

class SCDType2Handler:
    """
    Slowly Changing Dimension Type 2 implementation.

    Your use case: Track machine configuration changes over time
    for compliance and historical analysis.
    """

    def __init__(self, spark: SparkSession):
        self.spark = spark

    def merge_scd2(
        self,
        source_df: DataFrame,
        target_table_path: str,
        natural_keys: List[str],
        scd_columns: List[str],
        effective_date_col: str = "effective_date",
        end_date_col: str = "end_date",
        is_current_col: str = "is_current"
    ) -> None:
        """
        Perform SCD Type 2 merge.

        Args:
            source_df: New/updated dimension records
            target_table_path: Delta table path
            natural_keys: Business keys (e.g., machine_id)
            scd_columns: Columns that trigger new version on change

        Process:
            1. Identify changed records
            2. Expire old records (set end_date, is_current=false)
            3. Insert new versions with current timestamp
            4. Insert completely new records
        """
        target_table = DeltaTable.forPath(self.spark, target_table_path)

        # Prepare source with SCD metadata
        source_df = (
            source_df
            .withColumn(effective_date_col, current_timestamp())
            .withColumn(end_date_col, lit(None).cast("timestamp"))
            .withColumn(is_current_col, lit(True))
        )

        # Build merge condition
        merge_condition = " AND ".join([
            f"target.{k} = source.{k}" for k in natural_keys
        ]) + f" AND target.{is_current_col} = true"

        # Build change detection condition
        change_condition = " OR ".join([
            f"target.{col} != source.{col}" for col in scd_columns
        ])

        # Perform SCD Type 2 merge
        (
            target_table.alias("target")
            .merge(source_df.alias("source"), merge_condition)

            # When record changed: expire old version
            .whenMatchedUpdate(
                condition=change_condition,
                set={
                    end_date_col: "current_timestamp()",
                    is_current_col: "false"
                }
            )

            # When no change: do nothing (keep current version)
            .whenNotMatchedInsertAll()

            .execute()
        )

        # Insert new versions for changed records
        # (This requires a second pass to insert the new version)
        self._insert_new_versions(
            source_df, target_table_path, natural_keys,
            scd_columns, change_condition
        )

    def _insert_new_versions(self, source_df, target_path, natural_keys, scd_columns, change_condition):
        """Insert new versions for records that changed."""
        # Implementation for inserting new versions after expiring old ones
        pass  # [Your implementation]

# Usage example
def update_machine_dimension_scd2():
    """
    Your actual use case: Track machine config changes.
    """
    # New machine configurations from source system
    new_configs = spark.read.table("staging.machine_config_updates")

    scd_handler = SCDType2Handler(spark)

    scd_handler.merge_scd2(
        source_df=new_configs,
        target_table_path="dim.dim_machine",
        natural_keys=["machine_id"],
        scd_columns=["machine_config", "firmware_version", "calibration_status"],
        effective_date_col="config_effective_date"
    )
```

3. **examples/multi_plant_hierarchy.py**:
```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, row_number
from pyspark.sql.window import Window

def build_multi_plant_dimension_hierarchy(spark: SparkSession):
    """
    Build plant dimension with multi-level hierarchy.

    Your scenario:
        - Multiple plants across regions
        - Plants belong to sites
        - Sites belong to divisions
        - Need for roll-up aggregations
    """

    # Read plant master data from source systems
    plants_raw = spark.read.table("raw.plant_master")
    sites_raw = spark.read.table("raw.site_master")
    divisions_raw = spark.read.table("raw.division_master")

    # Build hierarchical dimension
    dim_plant = (
        plants_raw
        .join(sites_raw, "site_code", "left")
        .join(divisions_raw, "division_code", "left")
        .select(
            # Natural keys
            col("plant_code"),
            col("plant_name"),
            col("plant_type"),

            # Level 2: Site
            col("site_code"),
            col("site_name"),

            # Level 3: Division
            col("division_code"),
            col("division_name"),

            # Level 4: Region/Country
            col("region"),
            col("country"),

            # Attributes
            col("is_active"),
            col("commissioning_date"),
            col("timezone")
        )
    )

    # Generate surrogate keys
    window_spec = Window.orderBy("plant_code")
    dim_plant = dim_plant.withColumn(
        "plant_sk",
        row_number().over(window_spec)
    )

    # Write dimension
    (
        dim_plant.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .partitionBy("region")
        .saveAsTable("dim.dim_plant")
    )

    # Optimize for hierarchy queries
    spark.sql("""
        OPTIMIZE dim.dim_plant
        ZORDER BY (plant_code, site_code, division_code)
    """)

    print("Plant dimension hierarchy created successfully")
```

---

### Task 4: Spark Performance Optimization & UI Analysis (PRIORITY 2)

**Location**: `05-performance-optimization/spark-ui-analysis/`

**Create these files:**

1. **guides/stage-analysis-methodology.md**:
```markdown
# Spark UI Stage Analysis Methodology

## Your Workflow for Performance Optimization

### Step 1: Identify Slow Stages
1. Open Spark UI → Stages tab
2. Sort by Duration (descending)
3. Focus on stages with:
   - Duration > 5 minutes
   - High shuffle read/write
   - Task time skew

### Step 2: Analyze Stage Details
For each slow stage:

#### Check Shuffle Metrics
- **Shuffle Read**: Amount of data read from previous shuffle
- **Shuffle Write**: Amount of data written for next stage
- **Rule of thumb**:
  - > 10GB shuffle read = expensive operation
  - Consider broadcast join if one side < 1GB

#### Check Task Distribution
- **Max task duration / Median task duration**
- **Ratio > 3** = Data skew issue
- **Solution**: Salting, AQE skew join optimization

#### Check DAG Visualization
- Identify unnecessary operations
- Look for:
  - Multiple consecutive exchanges (shuffles)
  - Wide dependencies that could be narrow
  - Explosion operations (explode, flatMap)

### Step 3: Root Cause Analysis

Common patterns in manufacturing data:

#### Pattern 1: Expensive Shuffles from MAP Flattening
**Symptom**: High shuffle after explode() on customExtension

**Fix**:
```python
# Before (expensive)
df.select("*", explode(col("customExtension")))

# After (optimized)
known_keys = ["temp", "pressure", "vibration"]
for key in known_keys:
    df = df.withColumn(key, col("customExtension").getItem(key))
# Avoid explosion entirely!
```

#### Pattern 2: Data Skew in Multi-Plant Joins
**Symptom**: Few tasks take 10x longer, others finish quickly

**Fix**:
```python
# Enable AQE skew join
spark.conf.set("spark.sql.adaptive.skewJoin.enabled", "true")
spark.conf.set("spark.sql.adaptive.skewJoin.skewedPartitionThresholdInBytes", "256MB")

# Or manual salting for extreme skew
```

[Continue with more patterns...]
```

2. **src/stage_analyzer.py**:
```python
import requests
import json
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class StageMetrics:
    """Metrics for a Spark stage."""
    stage_id: int
    stage_name: str
    num_tasks: int
    duration_ms: int
    shuffle_read_bytes: int
    shuffle_write_bytes: int
    task_durations: List[int]

    @property
    def duration_seconds(self) -> float:
        return self.duration_ms / 1000

    @property
    def shuffle_read_gb(self) -> float:
        return self.shuffle_read_bytes / (1024**3)

    @property
    def shuffle_write_gb(self) -> float:
        return self.shuffle_write_bytes / (1024**3)

    @property
    def max_task_duration_ms(self) -> int:
        return max(self.task_durations) if self.task_durations else 0

    @property
    def median_task_duration_ms(self) -> int:
        if not self.task_durations:
            return 0
        sorted_durations = sorted(self.task_durations)
        n = len(sorted_durations)
        return sorted_durations[n // 2]

    @property
    def skew_ratio(self) -> float:
        """Ratio of max task duration to median. > 3 indicates skew."""
        median = self.median_task_duration_ms
        if median == 0:
            return 0
        return self.max_task_duration_ms / median

    @property
    def has_expensive_shuffle(self) -> bool:
        """Check if shuffle is expensive (> 10GB)."""
        return self.shuffle_read_gb > 10 or self.shuffle_write_gb > 10

    @property
    def has_skew(self) -> bool:
        """Check if stage has data skew."""
        return self.skew_ratio > 3

class SparkUIAnalyzer:
    """
    Analyze Spark UI programmatically for performance insights.

    Your workflow:
        1. Run pipeline
        2. Analyze Spark UI for bottlenecks
        3. Identify optimization opportunities
        4. Apply fixes and re-run
    """

    def __init__(self, spark_ui_url: str = "http://localhost:4040"):
        self.spark_ui_url = spark_ui_url
        self.api_base = f"{spark_ui_url}/api/v1"

    def get_application_id(self) -> str:
        """Get the current application ID."""
        response = requests.get(f"{self.api_base}/applications")
        apps = response.json()
        return apps[0]["id"] if apps else None

    def get_stage_metrics(self, app_id: str, stage_id: int) -> StageMetrics:
        """Retrieve detailed metrics for a specific stage."""
        # Get stage summary
        stage_url = f"{self.api_base}/applications/{app_id}/stages/{stage_id}"
        stage_data = requests.get(stage_url).json()[0]

        # Get task metrics
        tasks_url = f"{stage_url}/tasks"
        tasks_data = requests.get(tasks_url).json()

        task_durations = [task["taskMetrics"]["executorRunTime"] for task in tasks_data]

        return StageMetrics(
            stage_id=stage_id,
            stage_name=stage_data.get("name", "Unknown"),
            num_tasks=stage_data.get("numTasks", 0),
            duration_ms=stage_data.get("executorRunTime", 0),
            shuffle_read_bytes=stage_data.get("shuffleReadBytes", 0),
            shuffle_write_bytes=stage_data.get("shuffleWriteBytes", 0),
            task_durations=task_durations
        )

    def analyze_all_stages(self, app_id: str) -> List[Dict]:
        """
        Analyze all stages and provide optimization recommendations.
        """
        stages_url = f"{self.api_base}/applications/{app_id}/stages"
        stages = requests.get(stages_url).json()

        analysis_results = []

        for stage in stages:
            stage_id = stage["stageId"]
            metrics = self.get_stage_metrics(app_id, stage_id)

            recommendations = self._generate_recommendations(metrics)

            analysis_results.append({
                "stage_id": stage_id,
                "stage_name": metrics.stage_name,
                "duration_seconds": metrics.duration_seconds,
                "shuffle_read_gb": metrics.shuffle_read_gb,
                "shuffle_write_gb": metrics.shuffle_write_gb,
                "skew_ratio": metrics.skew_ratio,
                "has_issues": len(recommendations) > 0,
                "recommendations": recommendations
            })

        return analysis_results

    def _generate_recommendations(self, metrics: StageMetrics) -> List[str]:
        """Generate optimization recommendations based on metrics."""
        recommendations = []

        if metrics.has_expensive_shuffle:
            recommendations.append(
                f"⚠️  Expensive shuffle detected ({metrics.shuffle_read_gb:.2f}GB read, "
                f"{metrics.shuffle_write_gb:.2f}GB write). "
                "Consider broadcast join if one side is small."
            )

        if metrics.has_skew:
            recommendations.append(
                f"⚠️  Data skew detected (skew ratio: {metrics.skew_ratio:.2f}). "
                f"Max task: {metrics.max_task_duration_ms}ms, "
                f"Median task: {metrics.median_task_duration_ms}ms. "
                "Enable AQE skew join or apply salting."
            )

        if metrics.duration_seconds > 300:  # > 5 minutes
            recommendations.append(
                f"⚠️  Long-running stage ({metrics.duration_seconds:.0f}s). "
                "Review DAG for optimization opportunities."
            )

        return recommendations

# Usage example
def analyze_pipeline_performance():
    """
    Your actual workflow after running a pipeline.
    """
    analyzer = SparkUIAnalyzer("http://localhost:4040")

    app_id = analyzer.get_application_id()
    results = analyzer.analyze_all_stages(app_id)

    # Print analysis
    print("\n" + "="*80)
    print("SPARK PERFORMANCE ANALYSIS")
    print("="*80)

    for result in results:
        print(f"\nStage {result['stage_id']}: {result['stage_name']}")
        print(f"  Duration: {result['duration_seconds']:.2f}s")
        print(f"  Shuffle: {result['shuffle_read_gb']:.2f}GB read, {result['shuffle_write_gb']:.2f}GB write")
        print(f"  Skew Ratio: {result['skew_ratio']:.2f}")

        if result['recommendations']:
            print("  Recommendations:")
            for rec in result['recommendations']:
                print(f"    {rec}")

    print("\n" + "="*80)
```

---

### Task 5: Kafka Streams + Spark Integration (PRIORITY 2)

**Location**: `03-streaming-realtime/kstreams-preprocessing/`

**File**: `java-topology/src/main/java/PreprocessingTopology.java`

```java
package com.manufacturing.streaming;

import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.*;
import org.apache.kafka.streams.state.Stores;

import java.time.Duration;
import java.util.Properties;

/**
 * Kafka Streams preprocessing topology for manufacturing sensor data.
 *
 * Your workflow:
 *   1. KStreams: Data validation, enrichment, windowed aggregation
 *   2. Write preprocessed data to Kafka topic
 *   3. Spark: Consume preprocessed data for complex transformations
 *
 * Why this pattern:
 *   - KStreams: Low-latency stateful operations, per-record processing
 *   - Spark: Complex SQL transformations, ML, Delta Lake writes
 */
public class PreprocessingTopology {

    private final String inputTopic = "raw-sensor-events";
    private final String outputTopic = "preprocessed-for-spark";
    private final String invalidDataTopic = "invalid-sensor-events";

    public Topology buildTopology() {
        StreamsBuilder builder = new StreamsBuilder();

        // Input stream: Raw sensor events
        KStream<String, SensorEvent> rawEvents = builder.stream(
            inputTopic,
            Consumed.with(Serdes.String(), new SensorEventSerde())
        );

        // Step 1: Validation & filtering
        KStream<String, SensorEvent>[] branches = rawEvents.branch(
            (key, event) -> isValid(event),     // Valid events
            (key, event) -> true                 // Invalid events
        );

        KStream<String, SensorEvent> validEvents = branches[0];
        KStream<String, SensorEvent> invalidEvents = branches[1];

        // Send invalid events to dead letter queue
        invalidEvents.to(invalidDataTopic);

        // Step 2: Enrichment with machine metadata
        KTable<String, MachineMetadata> machineTable = builder.table(
            "machine-metadata",
            Consumed.with(Serdes.String(), new MachineMetadataSerde())
        );

        KStream<String, EnrichedEvent> enrichedEvents = validEvents
            .selectKey((key, event) -> event.getMachineId())
            .join(
                machineTable,
                (event, metadata) -> enrichEvent(event, metadata),
                Joined.with(Serdes.String(), new SensorEventSerde(), new MachineMetadataSerde())
            );

        // Step 3: Stateful windowed aggregation (1-minute tumbling windows)
        KTable<Windowed<String>, AggregatedMetrics> aggregated = enrichedEvents
            .groupByKey(Grouped.with(Serdes.String(), new EnrichedEventSerde()))
            .windowedBy(TimeWindows.ofSizeWithNoGrace(Duration.ofMinutes(1)))
            .aggregate(
                AggregatedMetrics::new,
                (key, event, aggregate) -> aggregate.add(event),
                Materialized.with(Serdes.String(), new AggregatedMetricsSerde())
            );

        // Step 4: Write preprocessed data to output topic for Spark consumption
        aggregated
            .toStream()
            .map((windowedKey, metrics) -> KeyValue.pair(
                windowedKey.key(),
                metrics.toJson()  // Serialize for Spark
            ))
            .to(outputTopic, Produced.with(Serdes.String(), Serdes.String()));

        return builder.build();
    }

    private boolean isValid(SensorEvent event) {
        // Your validation logic
        return event != null
            && event.getMachineId() != null
            && event.getTimestamp() != null
            && event.getTemperature() != null
            && event.getTemperature() > -50
            && event.getTemperature() < 200;
    }

    private EnrichedEvent enrichEvent(SensorEvent event, MachineMetadata metadata) {
        return new EnrichedEvent(
            event.getEventId(),
            event.getTimestamp(),
            event.getMachineId(),
            event.getTemperature(),
            event.getPressure(),
            event.getVibration(),
            metadata.getMachineType(),
            metadata.getPlantCode(),
            metadata.getLocation(),
            metadata.getMaintenanceStatus()
        );
    }

    public static void main(String[] args) {
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "sensor-preprocessing");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());

        // Enable exactly-once semantics
        props.put(StreamsConfig.PROCESSING_GUARANTEE_CONFIG, StreamsConfig.EXACTLY_ONCE_V2);

        PreprocessingTopology topology = new PreprocessingTopology();
        KafkaStreams streams = new KafkaStreams(topology.buildTopology(), props);

        streams.start();

        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }
}
```

**Spark Consumer**: `spark-consumer/consume_preprocessed_stream.py`

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

def consume_kstreams_preprocessed_data():
    """
    Consume preprocessed data from Kafka Streams for complex transformations.

    Your architecture:
        KStreams → [Validation + Enrichment + Windowing] → Kafka Topic
        Spark → [Complex SQL + Delta Lake + ML] → Analytics
    """

    spark = SparkSession.builder \
        .appName("ConsumeKStreamsPreprocessed") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

    # Schema for preprocessed data
    schema = StructType([
        StructField("machine_id", StringType()),
        StructField("window_start", TimestampType()),
        StructField("window_end", TimestampType()),
        StructField("event_count", IntegerType()),
        StructField("avg_temperature", DoubleType()),
        StructField("max_temperature", DoubleType()),
        StructField("avg_pressure", DoubleType()),
        StructField("machine_type", StringType()),
        StructField("plant_code", StringType()),
        StructField("location", StringType())
    ])

    # Read from KStreams output topic
    df = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "preprocessed-for-spark")
        .option("startingOffsets", "latest")
        .load()
    )

    # Parse JSON from KStreams
    parsed_df = (
        df.select(
            col("key").cast("string").alias("machine_id"),
            from_json(col("value").cast("string"), schema).alias("data")
        )
        .select("machine_id", "data.*")
    )

    # Complex transformations in Spark
    # (Things KStreams doesn't do well: complex SQL, joins with Delta, ML)
    transformed_df = (
        parsed_df
        .join(
            spark.read.format("delta").load("dim.dim_machine"),
            "machine_id"
        )
        .withColumn("anomaly_score", ml_model_prediction(col("avg_temperature")))
        .filter("anomaly_score > 0.8")
    )

    # Write to Delta Lake
    query = (
        transformed_df.writeStream
        .format("delta")
        .outputMode("append")
        .option("checkpointLocation", "/checkpoints/spark-from-kstreams")
        .option("mergeSchema", "true")
        .start("gold.manufacturing_anomalies")
    )

    query.awaitTermination()
```

---

### Task 6: Databricks Deployment (PRIORITY 3)

**Location**: `06-databricks-deployment/databricks-bundles/`

**File**: `databricks.yml`

```yaml
# Databricks Asset Bundle configuration
# Your multi-environment deployment strategy

bundle:
  name: manufacturing-streaming-platform

# Include patterns for dynamic configuration
include:
  - "resources/**/*.yml"

# Variables for environment-specific values
variables:
  catalog:
    description: Unity Catalog name
    default: dev_manufacturing

  checkpoint_path:
    description: Base path for checkpoints
    default: /mnt/checkpoints

# Development environment
environments:
  dev:
    default: true

    variables:
      catalog: dev_manufacturing
      checkpoint_path: /mnt/dev/checkpoints

    workspace:
      host: https://adb-1234567890.azuredatabricks.net
      root_path: ~/.bundle/${bundle.name}/${bundle.environment}

    resources:
      jobs:
        streaming_pipeline:
          name: "[DEV] Manufacturing Streaming Pipeline"

          git_source:
            git_url: https://github.com/your-org/manufacturing-platform
            git_branch: develop

          tasks:
            - task_key: ingest_sensor_data
              job_cluster_key: streaming_cluster

              notebook_task:
                notebook_path: ./notebooks/01_ingest_sensors.py
                base_parameters:
                  env: dev
                  checkpoint_path: ${var.checkpoint_path}/ingest

              libraries:
                - pypi:
                    package: delta-spark==3.0.0

            - task_key: process_to_silver
              depends_on:
                - task_key: ingest_sensor_data
              job_cluster_key: streaming_cluster

              notebook_task:
                notebook_path: ./notebooks/02_silver_processing.py
                base_parameters:
                  env: dev
                  checkpoint_path: ${var.checkpoint_path}/silver

            - task_key: build_gold_layer
              depends_on:
                - task_key: process_to_silver
              job_cluster_key: processing_cluster

              python_wheel_task:
                package_name: manufacturing_etl
                entry_point: build_gold_layer
                parameters:
                  - --env=dev
                  - --catalog=${var.catalog}

          job_clusters:
            - job_cluster_key: streaming_cluster
              new_cluster:
                spark_version: 13.3.x-scala2.12
                node_type_id: Standard_D16s_v3
                num_workers: 4

                spark_conf:
                  spark.databricks.delta.optimizeWrite.enabled: "true"
                  spark.databricks.delta.autoCompact.enabled: "true"
                  spark.sql.adaptive.enabled: "true"
                  spark.sql.adaptive.coalescePartitions.enabled: "true"
                  spark.sql.shuffle.partitions: "400"

                spark_env_vars:
                  ENVIRONMENT: dev

            - job_cluster_key: processing_cluster
              new_cluster:
                spark_version: 13.3.x-scala2.12
                node_type_id: Standard_D32s_v3
                num_workers: 8

                autoscale:
                  min_workers: 4
                  max_workers: 16

          schedule:
            quartz_cron_expression: "0 0 * * * ?"  # Hourly
            timezone_id: "America/Los_Angeles"
            pause_status: UNPAUSED

          email_notifications:
            on_failure:
              - data-engineering@company.com

  # QA environment
  qa:
    variables:
      catalog: qa_manufacturing
      checkpoint_path: /mnt/qa/checkpoints

    workspace:
      host: https://adb-0987654321.azuredatabricks.net

    resources:
      jobs:
        streaming_pipeline:
          name: "[QA] Manufacturing Streaming Pipeline"
          # Similar structure to dev, with QA-specific configurations

  # Production environment
  prod:
    variables:
      catalog: prod_manufacturing
      checkpoint_path: /mnt/prod/checkpoints

    workspace:
      host: https://adb-prod.azuredatabricks.net
      root_path: /Shared/.bundle/${bundle.name}

    resources:
      jobs:
        streaming_pipeline:
          name: "[PROD] Manufacturing Streaming Pipeline"

          max_concurrent_runs: 1

          job_clusters:
            - job_cluster_key: streaming_cluster
              new_cluster:
                spark_version: 13.3.x-scala2.12
                node_type_id: Standard_D64s_v3  # Larger for prod
                num_workers: 16

                autoscale:
                  min_workers: 8
                  max_workers: 32

                spark_conf:
                  spark.sql.shuffle.partitions: "2000"  # Higher for prod scale
                  spark.databricks.delta.optimizeWrite.enabled: "true"
                  spark.databricks.delta.autoCompact.enabled: "true"

          schedule:
            quartz_cron_expression: "0 */5 * * * ?"  # Every 5 minutes
            timezone_id: "UTC"

          email_notifications:
            on_start:
              - data-engineering@company.com
            on_success:
              - data-engineering@company.com
            on_failure:
              - data-engineering@company.com
              - platform-oncall@company.com

          webhook_notifications:
            on_failure:
              - id: pagerduty-webhook
```

**Deployment Script**: `github-actions/workflows/databricks-deploy.yml`

```yaml
name: Deploy to Databricks

on:
  push:
    branches:
      - main
      - develop
  pull_request:
    branches:
      - main

jobs:
  deploy-dev:
    name: Deploy to DEV
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install Databricks CLI
        run: |
          pip install databricks-cli

      - name: Configure Databricks CLI
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_DEV_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_DEV_TOKEN }}
        run: |
          echo "[DEFAULT]" > ~/.databrickscfg
          echo "host = $DATABRICKS_HOST" >> ~/.databrickscfg
          echo "token = $DATABRICKS_TOKEN" >> ~/.databrickscfg

      - name: Validate bundle
        run: |
          databricks bundle validate --environment dev

      - name: Deploy bundle
        run: |
          databricks bundle deploy --environment dev

      - name: Run integration tests
        run: |
          databricks bundle run --environment dev integration_tests

  deploy-qa:
    name: Deploy to QA
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    needs: [deploy-dev]

    steps:
      # Similar to dev deployment
      - name: Deploy to QA
        run: |
          databricks bundle deploy --environment qa

  deploy-prod:
    name: Deploy to PROD
    if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    needs: [deploy-qa]

    environment:
      name: production
      url: https://adb-prod.azuredatabricks.net

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy to PROD
        env:
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_PROD_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_PROD_TOKEN }}
        run: |
          databricks bundle deploy --environment prod

      - name: Notify deployment
        run: |
          echo "Deployed to production"
          # Send notification to Slack/Teams
```

---

## 🎯 EXECUTION CHECKLIST

Use this checklist to track your progress:

### Phase 1: Critical Production Patterns (Week 1-2)
- [ ] Task 1: SASL_SSL authentication with troubleshooting guide
- [ ] Task 2: Schema evolution & type conflict resolution
- [ ] Task 2a: MAP type flattening (11-step strategy)
- [ ] Task 2b: `DELTA_MERGE_INCOMPATIBLE_DATATYPE` handler

### Phase 2: Architecture & Modeling (Week 3-4)
- [ ] Task 3: Dimensional modeling patterns
- [ ] Task 3a: SCD Type 2 implementation
- [ ] Task 3b: Multi-plant dimension hierarchy
- [ ] Task 3c: Manufacturing fact tables
- [ ] Task 5: Kafka Streams + Spark integration

### Phase 3: Performance & Deployment (Week 5-6)
- [ ] Task 4: Spark UI analysis methodology
- [ ] Task 4a: Stage analyzer tool
- [ ] Task 4b: Optimization playbooks
- [ ] Task 6: Databricks bundle configuration
- [ ] Task 6a: Multi-environment deployment
- [ ] Task 6b: GitHub Actions CI/CD

### Phase 4: Production Readiness (Week 7-8)
- [ ] Production playbooks & runbooks
- [ ] Troubleshooting guides
- [ ] Real-world case studies documentation
- [ ] Testing & validation framework

---

## 💬 HOW TO USE THIS PROMPT

1. **Copy this entire document**
2. **Feed it to Claude in a new session** with:
   ```
   "I want to implement the patterns in this prompt.
   Let's start with Task 1: Production SASL_SSL Authentication.
   Create the complete implementation for all files mentioned."
   ```
3. **Work through tasks sequentially**
4. **Each task is independent** - you can work on them in parallel or out of order

---

## 🎯 SUCCESS CRITERIA

This transformation is successful when:
- [ ] Repo reflects your actual production work
- [ ] Patterns solve your daily pain points
- [ ] Code is copy-paste ready for your projects
- [ ] Troubleshooting guides help your team
- [ ] Performance methodology is documented
- [ ] Deployment matches your actual stack

---

**Ready to start? Feed this prompt back to me and specify which task to begin with!**
