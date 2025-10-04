from __future__ import annotations
from pyflink.datastream import DataStream

class FlinkDataStreamFactory:
    def __init__(self, bootstrap_servers: str, topic_name: str, flink_sql_connector_kafka_jar: str):
        from pyflink.datastream.execution_mode import RuntimeExecutionMode
        from pyflink.datastream.connectors.kafka import KafkaSource
        from pyflink.common.serialization import SimpleStringSchema
        from pyflink.datastream import StreamExecutionEnvironment

        self.env = StreamExecutionEnvironment.get_execution_environment()
        self.env.set_runtime_mode(RuntimeExecutionMode.STREAMING)
        self.env.add_jars(flink_sql_connector_kafka_jar)

        self.topic_name = topic_name
        self.kafka_source = KafkaSource.builder() \
            .set_bootstrap_servers(bootstrap_servers) \
            .set_topics(topic_name) \
            .set_value_only_deserializer(SimpleStringSchema()) \
            .build()

    def get_data_stream(self) -> (DataStream[str], StreamExecutionEnvironment):
        from pyflink.common.watermark_strategy import WatermarkStrategy

        return self.env.from_source(
            self.kafka_source,
            WatermarkStrategy.no_watermarks(),
            f"{self.topic_name}-source"
        ), self.env