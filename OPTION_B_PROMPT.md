# OPTION B: Build Manufacturing Data Platform from Scratch

## 🎯 MISSION STATEMENT

Build a **production-grade, enterprise-scale manufacturing IoT data platform reference repository** from the ground up. This repository documents battle-tested patterns, troubleshooting playbooks, and architectural decisions from real multi-plant manufacturing environments processing billions of records.

---

## 👤 MY PROFILE & CONTEXT

### Who I Am
- **Senior Data Engineer** specializing in industrial IoT and manufacturing data
- **Scale**: Multi-plant deployments across domains, billions of records
- **Focus**: Real-time streaming, dimensional modeling, performance optimization
- **Tech Stack**: Kafka → Spark → Delta Lake → Databricks

### What I Work On Daily

**1. Production Streaming Pipelines**
- Kafka with SASL_SSL authentication (troubleshooting auth failures regularly)
- Kafka Streams for preprocessing → Spark for complex transformations
- Delta Lake with schema evolution challenges
- Checkpointing strategies and recovery

**2. Schema Management Nightmares**
- `DELTA_MERGE_INCOMPATIBLE_DATATYPE` errors in production
- MAP type evolution in `customExtension` fields
- 11-step progressive flattening strategy for nested IoT sensor data
- Handling unpredictable schema changes from 100+ machines

**3. Performance Optimization**
- Spark UI analysis to identify bottlenecks
- Eliminating unnecessary shuffles and explosions
- Optimizing pipelines processing billions of records
- Memory tuning, partition sizing, skew handling

**4. Dimensional Data Modeling**
- Multi-plant star/snowflake schemas
- SCD Type 2 for machine configurations
- Manufacturing fact tables (test results, sensor readings)
- Cross-plant dimension conformance

**5. Enterprise Integration**
- SAP system integration
- OPP (Offline Programming Platform) data processing
- Multiple data sources per plant
- Complex upstream dependencies

**6. DevOps & Deployment**
- Databricks Asset Bundles for multi-environment deployment
- HOCON configuration patterns
- GitHub Actions CI/CD pipelines
- Environment-specific configurations (dev/QA/prod)
- VasapiValidator test framework integration

---

## 📁 REPOSITORY STRUCTURE

Build this structure from scratch:

```
manufacturing-data-platform/
│
├── README.md                                    # Platform overview & quick start
├── ARCHITECTURE.md                              # High-level architecture decisions
├── CONTRIBUTING.md                              # Contribution guidelines
├── LICENSE                                      # MIT License
│
├── 01-authentication-security/                  # PRIORITY 1
│   ├── README.md
│   ├── kafka-sasl-ssl/
│   │   ├── README.md                           # Comprehensive SASL_SSL guide
│   │   ├── configs/
│   │   │   ├── sasl-plain.yaml                # PLAIN mechanism
│   │   │   ├── sasl-scram-256.yaml            # SCRAM-SHA-256
│   │   │   ├── sasl-scram-512.yaml            # SCRAM-SHA-512
│   │   │   └── kerberos-gssapi.yaml           # GSSAPI for Kerberos
│   │   ├── databricks-integration/
│   │   │   ├── secrets-management.py          # Secret scope integration
│   │   │   ├── kafka-config-builder.py        # Dynamic config builder
│   │   │   └── connection-validator.py        # Test Kafka connectivity
│   │   ├── certificates/
│   │   │   ├── truststore-setup.md            # Truststore/Keystore guide
│   │   │   ├── cert-rotation-playbook.md      # Certificate rotation
│   │   │   └── cert-troubleshooting.md        # Common cert issues
│   │   └── troubleshooting/
│   │       ├── auth-failure-playbook.md       # Step-by-step debugging
│   │       ├── common-errors.md               # Error codes & solutions
│   │       └── connection-diagnostics.sh      # Diagnostic scripts
│   │
│   ├── unity-catalog-authentication/
│   │   ├── README.md
│   │   ├── service-principal-setup.md
│   │   └── token-management.py
│   │
│   └── secrets-management/
│       ├── azure-key-vault.md
│       ├── databricks-secrets.md
│       └── secret-rotation-strategy.md
│
├── 02-schema-evolution/                         # PRIORITY 1
│   ├── README.md
│   ├── delta-type-conflicts/
│   │   ├── README.md                           # Handling incompatible types
│   │   ├── src/
│   │   │   ├── __init__.py
│   │   │   ├── schema_validator.py            # Pre-merge validation
│   │   │   ├── type_conflict_resolver.py      # Auto-resolution strategies
│   │   │   ├── compatibility_checker.py       # Schema compatibility matrix
│   │   │   └── merge_error_handler.py         # DELTA_MERGE_INCOMPATIBLE_DATATYPE
│   │   ├── examples/
│   │   │   ├── int_to_long_promotion.py
│   │   │   ├── string_to_int_cast.py
│   │   │   ├── map_type_evolution.py
│   │   │   └── nested_struct_changes.py
│   │   ├── tests/
│   │   │   └── test_type_conflicts.py
│   │   └── docs/
│   │       ├── error-reference.md             # All error codes explained
│   │       └── resolution-strategies.md       # When to use each strategy
│   │
│   ├── map-type-flattening/
│   │   ├── README.md                           # Your 11-step methodology
│   │   ├── src/
│   │   │   ├── __init__.py
│   │   │   ├── progressive_flattener.py       # Core flattening logic
│   │   │   ├── custom_extension_handler.py    # MAP<STRING,STRING> handler
│   │   │   ├── dynamic_key_discovery.py       # Discover unknown keys
│   │   │   ├── type_inference.py              # Infer value types
│   │   │   └── optimization.py                # Avoid unnecessary explosions
│   │   ├── examples/
│   │   │   ├── iot_sensor_flattening.py       # Manufacturing sensors
│   │   │   ├── test_equipment_data.py         # Test result flattening
│   │   │   └── performance_comparison.ipynb   # Before/after benchmarks
│   │   └── docs/
│   │       ├── 11-step-methodology.md         # Document your strategy
│   │       └── optimization-techniques.md     # Shuffle elimination
│   │
│   ├── schema-registry-integration/
│   │   ├── README.md
│   │   ├── avro-schema-evolution.py
│   │   └── compatibility-modes.md
│   │
│   └── production-patterns/
│       ├── backward-compatible-changes.md
│       ├── breaking-change-strategy.md
│       └── schema-versioning.md
│
├── 03-streaming-architecture/                   # PRIORITY 1
│   ├── README.md
│   ├── kafka-to-delta-lake/
│   │   ├── README.md                           # Production streaming pattern
│   │   ├── src/
│   │   │   ├── __init__.py
│   │   │   ├── streaming_pipeline.py          # Medallion architecture
│   │   │   ├── checkpoint_manager.py          # Checkpoint strategies
│   │   │   ├── watermark_handler.py           # Late data handling
│   │   │   ├── backpressure_manager.py        # Rate limiting
│   │   │   └── monitoring.py                  # Metrics & health checks
│   │   ├── configs/
│   │   │   ├── dev.yaml
│   │   │   ├── qa.yaml
│   │   │   └── prod.yaml
│   │   ├── docker/
│   │   │   └── docker-compose.yml             # Local development
│   │   └── docs/
│   │       ├── exactly-once-semantics.md
│   │       ├── checkpoint-recovery.md
│   │       └── failure-scenarios.md
│   │
│   ├── kstreams-preprocessing/
│   │   ├── README.md                           # Your hybrid architecture
│   │   ├── java-topology/
│   │   │   ├── pom.xml
│   │   │   └── src/main/java/com/manufacturing/
│   │   │       ├── PreprocessingTopology.java
│   │   │       ├── SensorDataValidator.java
│   │   │       ├── StatefulAggregator.java
│   │   │       ├── MachineMetadataEnricher.java
│   │   │       └── serdes/
│   │   │           ├── SensorEventSerde.java
│   │   │           └── AggregatedMetricsSerde.java
│   │   ├── spark-consumer/
│   │   │   ├── README.md
│   │   │   ├── consume_preprocessed.py        # Spark consumer
│   │   │   └── delta_writer.py
│   │   ├── deployment/
│   │   │   ├── docker-compose.yml
│   │   │   └── kubernetes/
│   │   │       ├── kstreams-deployment.yaml
│   │   │       └── spark-deployment.yaml
│   │   └── docs/
│   │       ├── architecture-decisions.md      # Why KStreams + Spark?
│   │       ├── when-to-use-each.md            # Decision matrix
│   │       └── stateful-operations.md
│   │
│   ├── exactly-once-semantics/
│   │   ├── README.md
│   │   ├── kafka-idempotent-producer.py
│   │   ├── transactional-writes.py
│   │   └── delta-idempotent-writes.md
│   │
│   └── failure-recovery/
│       ├── checkpoint-strategies.md
│       ├── restart-procedures.md
│       └── data-consistency-checks.py
│
├── 04-dimensional-modeling/                     # PRIORITY 2
│   ├── README.md                               # Manufacturing DWH patterns
│   ├── star-schema-design/
│   │   ├── README.md
│   │   ├── schemas/
│   │   │   ├── dim_plant.sql                  # Plant dimension
│   │   │   ├── dim_machine.sql                # Machine dimension
│   │   │   ├── dim_test_equipment.sql         # Equipment dimension
│   │   │   ├── dim_product.sql                # Product dimension
│   │   │   ├── dim_date.sql                   # Date dimension
│   │   │   ├── dim_shift.sql                  # Shift dimension
│   │   │   ├── fact_manufacturing_test.sql    # Test results fact
│   │   │   ├── fact_sensor_readings.sql       # Sensor readings fact
│   │   │   └── fact_production_output.sql     # Production fact
│   │   ├── docs/
│   │   │   ├── dimensional-modeling-guide.md
│   │   │   ├── grain-definition.md
│   │   │   └── conforming-dimensions.md
│   │   └── diagrams/
│   │       └── star-schema-erd.mmd            # Mermaid diagram
│   │
│   ├── slowly-changing-dimensions/
│   │   ├── README.md
│   │   ├── src/
│   │   │   ├── __init__.py
│   │   │   ├── scd_type1.py                   # Overwrite
│   │   │   ├── scd_type2.py                   # Historical tracking
│   │   │   ├── scd_type3.py                   # Limited history
│   │   │   ├── scd_type6.py                   # Hybrid
│   │   │   └── dimension_builder.py           # Generic builder
│   │   ├── examples/
│   │   │   ├── machine_config_scd2.py         # Your actual use case
│   │   │   ├── plant_hierarchy_scd1.py
│   │   │   └── product_versioning_scd3.py
│   │   └── docs/
│   │       ├── scd-type-comparison.md
│   │       └── effective-dating-strategies.md
│   │
│   ├── fact-table-patterns/
│   │   ├── README.md
│   │   ├── src/
│   │   │   ├── fact_builder.py
│   │   │   ├── surrogate_key_generator.py
│   │   │   ├── incremental_load.py
│   │   │   └── aggregate_fact_builder.py
│   │   ├── examples/
│   │   │   ├── manufacturing_test_fact.py     # Billions of records
│   │   │   ├── sensor_readings_fact.py
│   │   │   └── production_summary_fact.py
│   │   └── docs/
│   │       ├── fact-table-types.md
│   │       └── partitioning-strategies.md
│   │
│   ├── multi-plant-hierarchy/
│   │   ├── README.md
│   │   ├── hierarchical_dimensions.py         # Plant → Site → Division
│   │   ├── cross_plant_conformance.py
│   │   └── rollup_aggregations.sql
│   │
│   └── incremental-loading/
│       ├── README.md
│       ├── cdc_merge.py
│       ├── watermark_based_load.py
│       └── change_tracking.md
│
├── 05-performance-optimization/                 # PRIORITY 2
│   ├── README.md
│   ├── spark-ui-analysis/
│   │   ├── README.md                           # Your methodology
│   │   ├── guides/
│   │   │   ├── reading-spark-ui.md            # How to read Spark UI
│   │   │   ├── stage-analysis.md              # Analyze stages
│   │   │   ├── identifying-bottlenecks.md     # Find slow operations
│   │   │   ├── shuffle-analysis.md            # Understand shuffles
│   │   │   ├── memory-analysis.md             # Memory issues
│   │   │   └── skew-detection.md              # Detect data skew
│   │   ├── src/
│   │   │   ├── __init__.py
│   │   │   ├── spark_ui_client.py            # REST API client
│   │   │   ├── stage_analyzer.py             # Stage metrics
│   │   │   ├── task_analyzer.py              # Task distribution
│   │   │   ├── skew_detector.py              # Skew analysis
│   │   │   ├── shuffle_analyzer.py           # Shuffle analysis
│   │   │   └── recommendation_engine.py      # Auto recommendations
│   │   ├── notebooks/
│   │   │   ├── spark_ui_deep_dive.ipynb
│   │   │   └── performance_troubleshooting.ipynb
│   │   └── examples/
│   │       ├── analyze_slow_job.py
│   │       └── before_after_optimization.md
│   │
│   ├── shuffle-optimization/
│   │   ├── README.md
│   │   ├── src/
│   │   │   ├── eliminating_shuffles.py        # Avoid shuffles
│   │   │   ├── broadcast_joins.py             # Use broadcast
│   │   │   ├── partition_optimization.py      # Partition tuning
│   │   │   └── coalesce_vs_repartition.py     # When to use each
│   │   ├── examples/
│   │   │   ├── map_flattening_no_shuffle.py   # Your 11-step strategy
│   │   │   ├── avoiding_explosions.py
│   │   │   └── salting_for_skew.py
│   │   └── docs/
│   │       ├── shuffle-types.md
│   │       └── optimization-patterns.md
│   │
│   ├── billion-record-optimization/
│   │   ├── README.md
│   │   ├── src/
│   │   │   ├── partition_calculator.py        # Calculate optimal partitions
│   │   │   ├── memory_tuner.py                # Executor/driver sizing
│   │   │   ├── file_sizing_optimizer.py       # Optimize file sizes
│   │   │   └── z_order_optimizer.py           # Z-ordering strategy
│   │   ├── configs/
│   │   │   ├── small_cluster.yaml             # <1TB
│   │   │   ├── medium_cluster.yaml            # 1-10TB
│   │   │   └── large_cluster.yaml             # >10TB
│   │   └── docs/
│   │       ├── scaling-guidelines.md
│   │       └── cost-optimization.md
│   │
│   ├── adaptive-query-execution/
│   │   ├── README.md
│   │   ├── aqe-configuration.md
│   │   ├── skew-join-optimization.py
│   │   └── dynamic-partition-coalescing.py
│   │
│   └── benchmarking/
│       ├── README.md
│       ├── benchmark_runner.py
│       ├── tpcds_manufacturing_variant.sql
│       └── performance_regression_tests.py
│
├── 06-databricks-deployment/                    # PRIORITY 3
│   ├── README.md
│   ├── asset-bundles/
│   │   ├── README.md                           # Complete bundle guide
│   │   ├── databricks.yml                     # Main bundle config
│   │   ├── resources/
│   │   │   ├── jobs/
│   │   │   │   ├── streaming_pipeline.yml
│   │   │   │   ├── batch_processing.yml
│   │   │   │   ├── dimensional_load.yml
│   │   │   │   └── monitoring_job.yml
│   │   │   ├── clusters/
│   │   │   │   ├── streaming_cluster.yml
│   │   │   │   ├── batch_cluster.yml
│   │   │   │   └── ml_cluster.yml
│   │   │   ├── workflows/
│   │   │   │   └── end_to_end_etl.yml
│   │   │   └── pipelines/
│   │   │       └── delta_live_tables.yml
│   │   ├── environments/
│   │   │   ├── dev.yaml
│   │   │   ├── qa.yaml
│   │   │   └── prod.yaml
│   │   └── docs/
│   │       ├── bundle-deployment-guide.md
│   │       └── environment-promotion.md
│   │
│   ├── hocon-configurations/
│   │   ├── README.md                           # Your HOCON patterns
│   │   ├── application.conf                   # Base config
│   │   ├── environments/
│   │   │   ├── dev.conf
│   │   │   ├── qa.conf
│   │   │   └── prod.conf
│   │   ├── src/
│   │   │   └── config_loader.py               # Load HOCON in Python
│   │   └── docs/
│   │       └── hocon-best-practices.md
│   │
│   ├── github-actions-cicd/
│   │   ├── README.md
│   │   ├── workflows/
│   │   │   ├── databricks-deploy.yml          # Main deployment
│   │   │   ├── bundle-validate.yml            # PR validation
│   │   │   ├── integration-tests.yml          # Run tests
│   │   │   └── smoke-tests.yml                # Post-deploy tests
│   │   ├── scripts/
│   │   │   ├── deploy_to_workspace.sh
│   │   │   ├── run_integration_tests.sh
│   │   │   └── rollback_deployment.sh
│   │   └── docs/
│   │       ├── cicd-pipeline-design.md
│   │       └── deployment-strategies.md
│   │
│   ├── cluster-management/
│   │   ├── README.md
│   │   ├── autoscaling-strategies.md
│   │   ├── instance-pool-setup.md
│   │   └── cost-optimization.md
│   │
│   └── workspace-organization/
│       ├── folder-structure.md
│       ├── naming-conventions.md
│       └── access-control-patterns.md
│
├── 07-enterprise-integration/                   # PRIORITY 3
│   ├── README.md
│   ├── sap-integration/
│   │   ├── README.md
│   │   ├── extractors/
│   │   │   ├── sap_bapi_extractor.py
│   │   │   ├── sap_table_extractor.py
│   │   │   └── sap_rfc_connector.py
│   │   ├── change-data-capture/
│   │   │   ├── cdc_pattern.md
│   │   │   └── incremental_extraction.py
│   │   └── docs/
│   │       └── sap-integration-architecture.md
│   │
│   ├── opp-data-processing/                    # Your OPP system
│   │   ├── README.md
│   │   ├── src/
│   │   │   ├── opp_data_ingestion.py
│   │   │   └── opp_transformation.py
│   │   └── docs/
│   │       └── opp-integration-guide.md
│   │
│   ├── change-data-capture/
│   │   ├── README.md
│   │   ├── debezium-kafka-delta/
│   │   │   ├── debezium-connector-config.json
│   │   │   └── cdc_consumer.py
│   │   └── incremental-processing/
│   │       ├── watermark_strategy.py
│   │       └── merge_upsert.py
│   │
│   └── orchestration/
│       ├── airflow-dags/
│       │   ├── manufacturing_etl_dag.py
│       │   └── dimensional_load_dag.py
│       └── dependency-management/
│           └── task-dependency-patterns.md
│
├── 08-testing-validation/                       # PRIORITY 3
│   ├── README.md
│   ├── vasapi-validator/                       # Your test framework
│   │   ├── README.md
│   │   ├── integration/
│   │   │   ├── vasapi_setup.md
│   │   │   └── test_runner.py
│   │   └── examples/
│   │       ├── data_quality_tests.py
│   │       └── pipeline_validation.py
│   │
│   ├── data-quality-testing/
│   │   ├── README.md
│   │   ├── src/
│   │   │   ├── quality_checks.py
│   │   │   ├── schema_validation.py
│   │   │   ├── completeness_checks.py
│   │   │   └── accuracy_checks.py
│   │   └── great-expectations/
│   │       └── expectations/
│   │
│   ├── integration-testing/
│   │   ├── README.md
│   │   ├── test-containers/
│   │   │   └── docker-compose.test.yml
│   │   └── tests/
│   │       ├── test_kafka_to_delta.py
│   │       └── test_dimensional_load.py
│   │
│   └── performance-testing/
│       ├── README.md
│       ├── load_tests/
│       └── regression_tests/
│
├── 09-monitoring-observability/                 # PRIORITY 3
│   ├── README.md
│   ├── prometheus-monitoring/
│   │   ├── README.md
│   │   ├── metrics/
│   │   │   ├── pipeline_metrics.py
│   │   │   ├── kafka_metrics.py
│   │   │   └── delta_metrics.py
│   │   ├── prometheus.yml
│   │   └── alert-rules.yml
│   │
│   ├── grafana-dashboards/
│   │   ├── README.md
│   │   ├── dashboards/
│   │   │   ├── streaming-pipeline.json
│   │   │   ├── kafka-cluster.json
│   │   │   ├── spark-performance.json
│   │   │   └── data-quality.json
│   │   └── provisioning/
│   │       └── datasources.yml
│   │
│   ├── logging/
│   │   ├── structured-logging.py
│   │   ├── log-aggregation.md
│   │   └── log-analysis-queries.md
│   │
│   └── alerting/
│       ├── pagerduty-integration.md
│       ├── slack-notifications.py
│       └── alert-runbooks/
│
├── 10-production-playbooks/                     # PRIORITY 1
│   ├── README.md
│   ├── troubleshooting/
│   │   ├── schema-evolution-errors.md         # Your daily issues
│   │   ├── kafka-auth-failures.md
│   │   ├── delta-merge-conflicts.md
│   │   ├── checkpoint-recovery.md
│   │   ├── performance-degradation.md
│   │   ├── data-skew-issues.md
│   │   └── out-of-memory-errors.md
│   │
│   ├── runbooks/
│   │   ├── pipeline-restart.md
│   │   ├── schema-migration.md
│   │   ├── cluster-scaling.md
│   │   ├── incident-response.md
│   │   └── disaster-recovery.md
│   │
│   ├── operational-procedures/
│   │   ├── deployment-checklist.md
│   │   ├── rollback-procedure.md
│   │   ├── data-backfill.md
│   │   └── maintenance-windows.md
│   │
│   └── error-reference/
│       ├── kafka-errors.md
│       ├── spark-errors.md
│       ├── delta-errors.md
│       └── databricks-errors.md
│
├── 11-real-world-case-studies/                 # YOUR PROJECTS
│   ├── README.md
│   ├── multi-plant-streaming/
│   │   ├── README.md                          # Document your architecture
│   │   ├── architecture-diagram.mmd
│   │   ├── data-flow.md
│   │   ├── challenges-solved.md
│   │   └── lessons-learned.md
│   │
│   ├── billion-record-processing/
│   │   ├── README.md
│   │   ├── optimization-journey.md            # Your optimizations
│   │   ├── performance-metrics.md
│   │   └── cost-analysis.md
│   │
│   ├── opp-data-integration/
│   │   ├── README.md
│   │   ├── integration-architecture.md
│   │   └── data-pipeline.md
│   │
│   └── sap-manufacturing-integration/
│       ├── README.md
│       ├── extraction-patterns.md
│       └── transformation-logic.md
│
├── docs/                                        # General documentation
│   ├── architecture/
│   │   ├── platform-overview.md
│   │   ├── technology-decisions.md
│   │   └── patterns-catalog.md
│   ├── best-practices/
│   │   ├── coding-standards.md
│   │   ├── naming-conventions.md
│   │   └── code-review-checklist.md
│   └── reference/
│       ├── technology-stack.md
│       ├── glossary.md
│       └── useful-resources.md
│
├── tools/                                       # Utility tools
│   ├── config-generators/
│   │   ├── kafka-config-gen.py
│   │   ├── spark-config-gen.py
│   │   └── databricks-bundle-gen.py
│   ├── data-generators/
│   │   ├── sensor_data_generator.py
│   │   └── test_data_factory.py
│   └── scripts/
│       ├── setup-dev-environment.sh
│       ├── validate-configs.sh
│       └── generate-documentation.sh
│
└── examples/                                    # Complete examples
    ├── quickstart/
    │   ├── 01_kafka_to_delta_basic.py
    │   ├── 02_dimensional_modeling.py
    │   └── 03_spark_optimization.py
    └── end-to-end/
        └── manufacturing_etl_pipeline/
            ├── README.md
            ├── configs/
            ├── src/
            ├── tests/
            └── deployment/
```

---

## 🎯 PHASE 1: FOUNDATION (Week 1-2)

### Task 1: Repository Setup & Documentation

**Create base files:**

1. **README.md** (Repository root):
```markdown
# Manufacturing Data Platform - Production Patterns

> Enterprise-scale data engineering patterns for manufacturing IoT, tested in production with billions of records across multi-plant deployments.

## 🎯 What This Repository Provides

This repository documents **battle-tested patterns** for:
- **Real-time streaming**: Kafka → Spark → Delta Lake at scale
- **Schema evolution**: Handling type conflicts, MAP flattening, production errors
- **Performance optimization**: Spark UI analysis, billion-record optimization
- **Dimensional modeling**: Manufacturing star schemas, SCD patterns
- **Enterprise integration**: SAP, OPP, multi-system orchestration
- **Production operations**: Troubleshooting playbooks, runbooks, deployment

## 🏭 Built for Manufacturing

These patterns solve real challenges in:
- Multi-plant IoT sensor data processing
- Manufacturing test equipment data (billions of records)
- Production floor real-time analytics
- Quality control and compliance tracking
- Cross-plant data integration and conformance

## ⚡ Quick Start

### Prerequisites
- Apache Kafka 3.x with SASL_SSL
- Apache Spark 3.4+ / Databricks Runtime 13.x+
- Delta Lake 3.0+
- Python 3.10+
- Java 11+ (for Kafka Streams)

### 1. Kafka SASL_SSL Authentication
```python
from manufacturing_platform.auth import get_kafka_sasl_config

# Get production Kafka config from Databricks secrets
kafka_config = get_kafka_sasl_config(env="prod")

# Use in streaming pipeline
df = spark.readStream.format("kafka") \
    .options(**kafka_config) \
    .option("subscribe", "sensor-events") \
    .load()
```

See: [Kafka SASL_SSL Guide](01-authentication-security/kafka-sasl-ssl/README.md)

### 2. Handle Schema Evolution
```python
from manufacturing_platform.schema import TypeConflictResolver

# Resolve DELTA_MERGE_INCOMPATIBLE_DATATYPE errors
resolver = TypeConflictResolver()
conflicts = resolver.identify_conflicts(source_df.schema, target_schema)
resolved_df = resolver.resolve_conflicts(source_df, conflicts)
```

See: [Schema Evolution Guide](02-schema-evolution/README.md)

### 3. Optimize for Billions of Records
```python
from manufacturing_platform.optimization import optimize_for_scale

# Auto-configure Spark for your data volume
spark = optimize_for_scale(
    spark,
    data_volume_gb=5000,
    partition_keys=["plant_id", "date"]
)
```

See: [Performance Optimization Guide](05-performance-optimization/README.md)

## 📚 Pattern Catalog

### Production-Critical Patterns
1. [Kafka SASL_SSL Authentication](01-authentication-security/kafka-sasl-ssl/) - Troubleshoot auth failures
2. [Delta Type Conflicts](02-schema-evolution/delta-type-conflicts/) - Handle merge errors
3. [MAP Type Flattening](02-schema-evolution/map-type-flattening/) - 11-step strategy
4. [Spark UI Analysis](05-performance-optimization/spark-ui-analysis/) - Performance methodology

### Architecture Patterns
5. [Kafka Streams + Spark](03-streaming-architecture/kstreams-preprocessing/) - Hybrid architecture
6. [Dimensional Modeling](04-dimensional-modeling/star-schema-design/) - Manufacturing DWH
7. [SCD Type 2](04-dimensional-modeling/slowly-changing-dimensions/) - Historical tracking

### Deployment Patterns
8. [Databricks Bundles](06-databricks-deployment/asset-bundles/) - Multi-env deployment
9. [GitHub Actions CI/CD](06-databricks-deployment/github-actions-cicd/) - Automated deployment

### Operational Patterns
10. [Production Playbooks](10-production-playbooks/) - Troubleshooting guides

## 🏆 Real-World Impact

These patterns power production systems processing:
- **5M+ events/day** from manufacturing sensors
- **Billions of records** in Delta Lake tables
- **Sub-30 second latency** for real-time analytics
- **99.9% uptime** across multiple plants
- **40% cost reduction** through optimization

## 🤝 Contributing

This repository is built from real production experience. Contributions welcome for:
- New patterns from your production deployments
- Troubleshooting guides for errors you've solved
- Performance optimization techniques
- Architecture decision records

See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

**Built with ❤️ for manufacturing data engineers**
```

2. **ARCHITECTURE.md**:
```markdown
# Platform Architecture

## Design Principles

### 1. Production-First
All patterns in this repository are derived from production deployments, not theoretical examples.

### 2. Multi-Plant Scale
Designed for enterprise manufacturing with:
- Multiple plants across geographies
- Diverse equipment and sensor types
- Billions of records
- Complex organizational hierarchies

### 3. Real-Time + Batch Hybrid
Combines streaming for real-time insights with batch for complex analytics:
- **Kafka Streams**: Sub-second preprocessing
- **Spark Streaming**: Medallion architecture (Bronze → Silver → Gold)
- **Batch Processing**: Dimensional modeling, aggregations

### 4. Schema Flexibility
Manufacturing environments have unpredictable schema evolution:
- Sensors added/removed dynamically
- Firmware updates change data structures
- Cross-plant schema variations

## Technology Stack

### Core Technologies
- **Messaging**: Apache Kafka 3.6+ (SASL_SSL secured)
- **Stream Processing**: Kafka Streams 3.6+, Spark Structured Streaming 3.4+
- **Storage**: Delta Lake 3.0+ on cloud object storage
- **Compute**: Databricks Runtime 13.x+ (or open-source Spark)
- **Data Warehouse**: Dimensional modeling with Delta Lake

### Integration Layer
- **SAP**: BAPI/RFC extractors for master data
- **OPP**: Offline Programming Platform integration
- **MES**: Manufacturing Execution Systems
- **Quality Systems**: SPC, 6-sigma tools

### DevOps
- **Deployment**: Databricks Asset Bundles
- **CI/CD**: GitHub Actions
- **Configuration**: HOCON for type-safe configs
- **Monitoring**: Prometheus + Grafana
- **Testing**: VasapiValidator framework

## Architecture Decisions

### ADR-001: Kafka Streams for Preprocessing
**Context**: Need low-latency stateful operations before Spark

**Decision**: Use Kafka Streams for:
- Data validation (malformed JSON rejection)
- Machine metadata enrichment
- Windowed aggregations (1-minute windows)
- Topic compaction

**Rationale**:
- Sub-second latency
- Stateful operations without external state store
- Natural fit for per-record processing

**Consequences**:
- Need Java codebase in addition to Python
- Adds operational complexity (deploy KStreams apps)
- Better separation of concerns

### ADR-002: Delta Lake for All Storage
**Context**: Need ACID, time travel, schema evolution

**Decision**: Use Delta Lake for Bronze/Silver/Gold layers

**Rationale**:
- ACID transactions
- Schema evolution with `mergeSchema`
- Time travel for debugging and compliance
- Efficient upserts with MERGE
- Z-ordering for query performance

**Consequences**:
- Vendor lock-in considerations (open-source Delta protocol)
- Requires understanding of Delta internals
- Optimized for lakehouse, not data warehouse

### ADR-003: Medallion Architecture
**Context**: Need data quality tiers

**Decision**: Implement Bronze → Silver → Gold

**Bronze**: Raw ingestion, preserve everything
**Silver**: Cleaned, validated, conformed
**Gold**: Business-level aggregations

**Rationale**:
- Clear data quality contracts
- Enables reprocessing from raw
- Separation of concerns

### ADR-004: Hybrid KStreams + Spark
**Context**: Need both low-latency and complex transformations

**Decision**: KStreams preprocessing → Spark complex SQL

**KStreams for**:
- Validation
- Enrichment
- Simple windowing

**Spark for**:
- Complex SQL transformations
- Joins with large dimensions
- ML model inference
- Delta Lake writes

[Continue with more ADRs...]
```

3. **CONTRIBUTING.md**:
```markdown
# Contributing to Manufacturing Data Platform

## Contribution Philosophy

This repository captures **real production patterns**, not theoretical examples. When contributing:

1. **Production-Tested**: Pattern should be deployed in production
2. **Problem-Solving**: Document the problem solved, not just the solution
3. **Scale-Proven**: If claiming performance benefits, include metrics
4. **Troubleshooting-First**: Include error scenarios and solutions

## Types of Contributions

### 1. Production Patterns
Share a pattern from your deployment:
- **Problem**: What production issue did this solve?
- **Solution**: Implementation details
- **Metrics**: Performance impact (before/after)
- **Lessons Learned**: What would you do differently?

### 2. Troubleshooting Guides
Document an error you solved:
- **Error Message**: Exact error text
- **Root Cause**: Why it occurred
- **Solution**: Step-by-step fix
- **Prevention**: How to avoid in future

### 3. Performance Optimizations
Share optimization techniques:
- **Baseline**: Performance before optimization
- **Changes**: What you changed and why
- **Results**: Performance after optimization
- **Trade-offs**: What you sacrificed (if anything)

### 4. Architecture Decisions
Document important decisions:
- **Context**: What problem needed solving?
- **Options Considered**: What alternatives did you evaluate?
- **Decision**: What did you choose and why?
- **Consequences**: What are the implications?

## Contribution Process

### 1. Check Existing Patterns
Search the repository to avoid duplicates.

### 2. Open an Issue First
Describe what you plan to contribute. Get feedback before writing code.

### 3. Follow Structure
Use the appropriate template for your contribution type.

### 4. Include Complete Examples
- Working code (tested)
- Configuration files
- Test data (synthetic, no real data)
- Documentation

### 5. Submit Pull Request
- Reference the issue
- Describe changes
- Include test results

## Code Standards

### Python
- PEP 8 compliant
- Type hints (Python 3.10+)
- Google-style docstrings
- 100 character line length

### Java (Kafka Streams)
- Java 11+
- Google Java Style Guide
- Javadoc for public APIs

### SQL
- Uppercase keywords
- Lowercase table/column names
- Indented for readability

### Documentation
- Markdown for all docs
- Mermaid for diagrams
- Code examples with comments

## Testing Requirements

### Unit Tests
- Required for all code contributions
- pytest for Python
- JUnit for Java

### Integration Tests
- Required for architectural patterns
- Use test containers

### Performance Tests
- Required for optimization claims
- Include benchmark scripts
- Document test environment

## Review Process

1. **Automated Checks**: CI/CD pipeline runs
2. **Peer Review**: At least one maintainer reviews
3. **Production Validation**: Confirm pattern is production-tested
4. **Documentation Review**: Ensure docs are clear and complete

## Recognition

Contributors will be:
- Listed in README
- Mentioned in release notes
- Featured in pattern documentation

## Questions?

Open a GitHub Discussion or email the maintainers.

---

Thank you for contributing! 🙏
```

---

### Task 2: Kafka SASL_SSL Authentication (CRITICAL)

**Location**: `01-authentication-security/kafka-sasl-ssl/`

**Files to create** (see Option A prompt for detailed code - same implementation)

---

### Task 3: Schema Evolution & Type Conflicts (CRITICAL)

**Location**: `02-schema-evolution/delta-type-conflicts/`

**Files to create** (see Option A prompt for detailed code)

---

### Task 4: MAP Type Flattening (YOUR SPECIALTY)

**Location**: `02-schema-evolution/map-type-flattening/`

**Create**: `docs/11-step-methodology.md`

```markdown
# 11-Step Progressive Flattening Methodology

## Problem Statement

Manufacturing IoT sensors send data with `customExtension` MAP<STRING, STRING> fields containing:
- Unpredictable keys (different per machine, firmware version)
- 100+ potential fields
- Nested structures (sometimes JSON strings as values)
- Frequent schema changes without notice

**Naive Approach (Don't Do This)**:
```python
# ❌ Causes expensive shuffle, OOM on large data
df.select("*", explode(col("customExtension")))
```

## The 11-Step Strategy

### Step 1: Sample-Based Key Discovery
Discover keys without full table scan:
```python
def discover_keys(df: DataFrame, sample_size: int = 1000) -> List[str]:
    """
    Sample-based key discovery.
    Cost: O(sample_size) instead of O(n)
    """
    keys_df = (
        df.select(explode(map_keys(col("customExtension"))).alias("key"))
        .limit(sample_size)
        .distinct()
    )
    return [row.key for row in keys_df.collect()]
```

### Step 2: Extract Known Keys Without Explosion
Use getItem() instead of explode():
```python
known_keys = ["temperature", "pressure", "vibration", "rpm"]

for key in known_keys:
    df = df.withColumn(
        f"ext_{key}",
        col("customExtension").getItem(key)
    )
# ✅ No shuffle! Column-wise operation
```

### Step 3: Handle Null/Missing Keys
```python
# Provide defaults for missing keys
df = df.withColumn(
    "ext_temperature",
    coalesce(col("customExtension").getItem("temperature"), lit(None))
)
```

### Step 4: Type Inference
```python
def infer_and_cast(df: DataFrame, key: str) -> DataFrame:
    """
    Infer type from sample and cast.
    """
    # Sample values
    sample_values = df.select(col("customExtension").getItem(key)).limit(100).collect()

    # Infer type (numeric, timestamp, string, json)
    inferred_type = infer_type_from_samples(sample_values)

    # Cast accordingly
    if inferred_type == "numeric":
        df = df.withColumn(f"ext_{key}", col("customExtension").getItem(key).cast("double"))
    elif inferred_type == "timestamp":
        df = df.withColumn(f"ext_{key}", to_timestamp(col("customExtension").getItem(key)))
    # ... etc

    return df
```

### Step 5: Nested JSON Handling
```python
# Some values are JSON strings - parse them
df = df.withColumn(
    "ext_config_parsed",
    when(
        col("customExtension").getItem("config").isNotNull(),
        from_json(col("customExtension").getItem("config"), config_schema)
    ).otherwise(lit(None))
)
```

### Step 6: Explosion Only When Necessary
```python
# Only explode for truly dynamic keys (rare case)
# AND only after filtering to small subset
filtered_df = df.filter("plant_id = 'PLANT_001' AND date = '2025-01-01'")  # Small subset
exploded_df = filtered_df.select("*", explode(col("customExtension")))
```

### Step 7: Partition Before Explosion
```python
# If explosion is unavoidable, partition first to parallelize
df = df.repartition(200, "machine_id")  # Spread across executors
exploded_df = df.select("*", explode(col("customExtension")))
```

### Step 8: Incremental Key Addition
```python
# Track new keys over time, add incrementally
current_keys = get_current_extracted_keys()  # From metadata table
discovered_keys = discover_keys(df)

new_keys = set(discovered_keys) - set(current_keys)

if new_keys:
    logger.info(f"Found {len(new_keys)} new keys: {new_keys}")
    for key in new_keys:
        df = df.withColumn(f"ext_{key}", col("customExtension").getItem(key))
        register_new_key(key)  # Update metadata
```

### Step 9: Schema Evolution-Friendly Storage
```python
# Write with schema evolution enabled
df.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \  # Allow new columns
    .save(path)
```

### Step 10: Optimize File Layout
```python
# After adding many columns, optimize
spark.sql(f"""
    OPTIMIZE delta.`{path}`
    ZORDER BY (machine_id, timestamp)
""")
```

### Step 11: Monitor Column Count
```python
# Alert if too many columns
num_columns = len(df.columns)
if num_columns > 1000:
    logger.warning(f"Table has {num_columns} columns. Consider archiving old columns.")
```

## Performance Comparison

| Approach | Duration | Shuffle GB | Memory |
|----------|----------|------------|--------|
| Naive explosion | 45 min | 500 GB | OOM |
| 11-step strategy | 4 min | 5 GB | Stable |

## When to Use

✅ **Use this pattern when**:
- MAP columns with 10+ dynamic keys
- Frequent schema changes
- Large data volumes (>1TB)
- Mixed data types in values

❌ **Don't use when**:
- Fixed, known keys (just extract directly)
- Small data (<100GB)
- Values are uniform type

## Real-World Example

See: [Manufacturing IoT Sensors](../examples/iot_sensor_flattening.py)
```

---

## 🎯 PHASE 2: CORE PATTERNS (Week 3-4)

Continue with:
- Dimensional modeling
- Kafka Streams + Spark integration
- Spark UI analysis methodology
- Databricks deployment

(Use Option A code examples - same implementations)

---

## 🎯 PHASE 3: PRODUCTION OPERATIONS (Week 5-6)

### Production Playbooks

**Location**: `10-production-playbooks/troubleshooting/`

**Create**: `schema-evolution-errors.md`

```markdown
# Schema Evolution Errors - Production Playbook

## Error: DELTA_MERGE_INCOMPATIBLE_DATATYPE

### Symptom
```
org.apache.spark.sql.delta.schema.DeltaInvariantViolationException:
DELTA_MERGE_INCOMPATIBLE_DATATYPE: Cannot merge field 'customExtension'
of type MAP<STRING, STRING> with MAP<STRING, STRUCT<...>>
```

### When It Occurs
- Source schema changed (firmware update, new sensor type)
- Attempting MERGE operation with incompatible types
- Usually happens in Silver/Gold layer writes

### Root Cause
Delta Lake strict schema enforcement. MAP key types must match, value types must be compatible.

### Immediate Fix

**Option 1: Cast to Compatible Type** (Recommended)
```python
from pyspark.sql.functions import col

# Identify the conflict
source_type = source_df.schema["customExtension"].dataType
target_type = target_df.schema["customExtension"].dataType

# Cast source to match target (or vice versa)
source_df = source_df.withColumn(
    "customExtension",
    col("customExtension").cast(target_type)
)

# Now merge works
target_table.merge(source_df, merge_condition) \
    .whenMatchedUpdateAll() \
    .whenNotMatchedInsertAll() \
    .execute()
```

**Option 2: Column Versioning**
```python
# Keep both versions
source_df = source_df.withColumnRenamed("customExtension", "customExtension_v2")

# Write without merge (append mode)
source_df.write.format("delta").mode("append").save(path)

# Update downstream to use v2 when available
```

**Option 3: Rewrite Target Schema** (Use with caution)
```python
# ⚠️  This rewrites the entire table!
source_df.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .save(path)
```

### Long-Term Prevention

1. **Schema Validation Gate**
```python
# Add to pipeline BEFORE merge
from manufacturing_platform.schema import validate_schema_compatibility

is_compatible = validate_schema_compatibility(source_df.schema, target_schema)

if not is_compatible:
    # Send to DLQ or alert
    raise SchemaIncompatibilityError("Schema validation failed")
```

2. **Automated Type Promotion**
```python
# Use type conflict resolver
from manufacturing_platform.schema import TypeConflictResolver

resolver = TypeConflictResolver()
resolved_df = resolver.auto_resolve(source_df, target_schema)
```

3. **Schema Registry Integration**
```python
# Validate against schema registry before write
from confluent_kafka.schema_registry import SchemaRegistryClient

sr_client = SchemaRegistryClient({"url": "http://schema-registry:8081"})
# Validate schema before merge
```

### Monitoring & Alerting

Add this metric to Prometheus:
```python
schema_conflicts_total.labels(table="manufacturing_silver").inc()
```

Alert if > 10 conflicts/hour:
```yaml
# prometheus/alerts.yml
- alert: HighSchemaConflicts
  expr: rate(schema_conflicts_total[1h]) > 10
  annotations:
    summary: "High schema conflict rate on {{ $labels.table }}"
```

### Post-Incident

1. **Root Cause Analysis**
   - Which system produced incompatible schema?
   - Was it a planned firmware update?
   - Communication breakdown?

2. **Update Runbook**
   - Add this specific error pattern
   - Document resolution

3. **Improve Prevention**
   - Coordinate with firmware teams
   - Add schema validation earlier in pipeline

### Related Errors
- `DELTA_SCHEMA_MISMATCH`
- `DELTA_INCOMPATIBLE_SCHEMA_MERGE`
- `DELTA_MERGE_PRECONDITION_VIOLATED`

### See Also
- [Type Conflict Resolver](../../02-schema-evolution/delta-type-conflicts/src/type_conflict_resolver.py)
- [Schema Validation Guide](../../02-schema-evolution/README.md)
```

**Create**: `kafka-auth-failures.md`

```markdown
# Kafka Authentication Failures - Production Playbook

## Error: "Authentication failed: Invalid username or password"

### Symptom
```
org.apache.kafka.common.errors.SaslAuthenticationException:
Authentication failed: Invalid username or password
```

### Diagnostic Steps

#### Step 1: Verify Credentials in Secrets
```python
# In Databricks notebook
secret_scope = "kafka-prod"

# This should return [REDACTED], not error
try:
    username = dbutils.secrets.get(secret_scope, "username")
    print("Username secret exists: ✓")
except Exception as e:
    print(f"❌ Username secret missing: {e}")

try:
    password = dbutils.secrets.get(secret_scope, "password")
    print("Password secret exists: ✓")
except Exception as e:
    print(f"❌ Password secret missing: {e}")
```

#### Step 2: Test Basic Network Connectivity
```bash
# From Databricks cluster driver node
%sh
telnet <kafka-broker-host> 9093
# Should connect (Ctrl+C to exit)
```

#### Step 3: Verify SASL Mechanism
```python
# Check what mechanism broker expects vs what you're using
expected_mechanism = "SCRAM-SHA-512"  # Check with Kafka admin
your_mechanism = kafka_config.get("kafka.sasl.mechanism")

if expected_mechanism != your_mechanism:
    print(f"❌ Mechanism mismatch! Expected: {expected_mechanism}, Using: {your_mechanism}")
```

#### Step 4: Test with kafkacat (Debugging Tool)
```bash
# Install kafkacat on driver
%sh
apt-get install -y kafkacat

# Test connection
kafkacat -b <broker>:9093 \
  -X security.protocol=SASL_SSL \
  -X sasl.mechanism=PLAIN \
  -X sasl.username=<username> \
  -X sasl.password=<password> \
  -L  # List metadata

# If this works, issue is in Spark config
# If this fails, issue is with credentials/network
```

### Common Causes & Fixes

#### Cause 1: Expired Credentials
**Fix**: Rotate secrets in Azure Key Vault / AWS Secrets Manager
```python
# Update Databricks secret from Key Vault
# (Usually done via Databricks CLI or Terraform)
```

#### Cause 2: Wrong SASL Mechanism
**Fix**: Match broker configuration
```python
# Change from PLAIN to SCRAM-SHA-512
kafka_config = {
    "kafka.sasl.mechanism": "SCRAM-SHA-512",  # Was: "PLAIN"
    # ... rest of config
}
```

#### Cause 3: Incorrect JAAS Config Format
**Fix**: Validate JAAS string
```python
# ❌ Wrong (missing semicolon, wrong quotes)
jaas_config = """org.apache.kafka.common.security.plain.PlainLoginModule required
username='user' password='pass'"""

# ✅ Correct
jaas_config = """org.apache.kafka.common.security.plain.PlainLoginModule required
username="user"
password="pass";"""
```

#### Cause 4: Secret Scope Permissions
**Fix**: Grant cluster access to secret scope
```bash
# Databricks CLI
databricks secrets put-acl \
  --scope kafka-prod \
  --principal <cluster-service-principal> \
  --permission READ
```

### Quick Fix Script

```python
from manufacturing_platform.auth import diagnose_kafka_auth

# Run diagnostics
diagnosis = diagnose_kafka_auth(
    broker="kafka-prod.company.com:9093",
    secret_scope="kafka-prod",
    mechanism="SCRAM-SHA-512"
)

# Prints:
# ✓ Secret scope accessible
# ✓ Network connectivity OK
# ✓ SASL mechanism matches broker
# ✓ Credentials valid
# OR
# ❌ Issue found: [specific problem]
```

### Prevention

1. **Automated Secret Rotation**
   - Set up Key Vault rotation policy
   - Test credentials before expiry

2. **Connection Validation in CI/CD**
   ```yaml
   # .github/workflows/validate-kafka-auth.yml
   - name: Validate Kafka Connection
     run: |
       python scripts/test_kafka_connectivity.py --env prod
   ```

3. **Monitoring**
   ```python
   # Add metric
   kafka_auth_failures_total.labels(env="prod").inc()
   ```

### Escalation

If diagnostics don't resolve:
1. Contact Kafka platform team
2. Provide:
   - Exact error message
   - Broker address
   - SASL mechanism used
   - Timestamp of failure
3. Check for platform-wide issues

### Related Errors
- `SASL_HANDSHAKE_FAILED`
- `NETWORK_EXCEPTION`
- `SSL_HANDSHAKE_FAILED`

### See Also
- [Kafka SASL_SSL Guide](../../01-authentication-security/kafka-sasl-ssl/README.md)
- [Databricks Secrets Setup](../../01-authentication-security/kafka-sasl-ssl/databricks-integration/)
```

---

## 🎯 EXECUTION ROADMAP

### Week 1-2: Foundation & Critical Patterns
- [ ] Repository structure & documentation
- [ ] Kafka SASL_SSL authentication (complete implementation)
- [ ] Schema evolution & type conflicts (complete implementation)
- [ ] MAP type flattening (document your 11-step strategy)

### Week 3-4: Architecture & Modeling
- [ ] Dimensional modeling (star schema, SCD Type 2)
- [ ] Kafka Streams + Spark integration (Java topology + Python consumer)
- [ ] Multi-plant hierarchy patterns

### Week 5-6: Performance & Deployment
- [ ] Spark UI analysis (methodology + tooling)
- [ ] Billion-record optimization (calculators + configs)
- [ ] Databricks bundles (multi-environment deployment)
- [ ] GitHub Actions CI/CD

### Week 7-8: Production Operations
- [ ] Troubleshooting playbooks (schema, auth, performance)
- [ ] Runbooks (restart, migration, incident response)
- [ ] Monitoring & alerting setup
- [ ] Real-world case studies (document your projects)

---

## 💬 HOW TO USE THIS PROMPT

1. **Copy this entire document**
2. **Feed it to Claude** with:
   ```
   "I want to build the Manufacturing Data Platform repository from scratch.
   Let's start with Phase 1, Task 1: Repository setup.
   Create the README.md, ARCHITECTURE.md, and CONTRIBUTING.md files."
   ```
3. **Work through phases sequentially**
4. **Each task builds on previous ones**

---

## 🎯 SUCCESS CRITERIA

This repository is successful when:
- [ ] Solves YOUR actual production problems
- [ ] Team members use it as reference for new pipelines
- [ ] Troubleshooting time reduced by 50%
- [ ] Onboarding time for new engineers cut in half
- [ ] Patterns prevent recurring production issues
- [ ] Codebase reflects your expertise and domain knowledge

---

## 🌟 UNIQUE VALUE PROPOSITION

This isn't another tutorial repo. This is:
- **Your playbook** for manufacturing data at scale
- **Your team's knowledge base** for production patterns
- **Your portfolio** demonstrating real-world expertise
- **Your contribution** to the data engineering community

---

**Ready to build? Feed this prompt back to me and let's start with Phase 1!**
