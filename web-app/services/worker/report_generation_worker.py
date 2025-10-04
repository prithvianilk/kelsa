from __future__ import annotations

from pyflink.datastream import DataStream
from flink.data_stream_factory import FlinkDataStreamFactory
from work import Work
import threading
import os

class ReportGenerationWorker:
    _ds: DataStream[str]

    def __init__(self, data_stream_factory: FlinkDataStreamFactory, stream_output_logs_dir: str):
        self._ds, self._env = data_stream_factory.get_data_stream()
        
        os.makedirs(stream_output_logs_dir, exist_ok=True)
        
        # TODO: Optimise this
        def write_to_file(value):
            with open(f"{stream_output_logs_dir}/work_report_generation_worker.log", "a") as f:
                f.write(f"{value}\n")
            return value 

        self._ds \
            .map(lambda event: Work.model_validate_json(event)) \
            .key_by(lambda work: work.username) \
            .map(lambda work: (work.application, 1)) \
            .key_by(lambda app: app[0]) \
            .reduce(lambda a, b: (a[0], a[1] + b[1])) \
            .map(lambda app_tuple: f"{app_tuple[0]},{app_tuple[1]}") \
            .map(write_to_file)

        def run_flink():
            self._env.execute()

        thread = threading.Thread(target=run_flink, daemon=True)
        thread.start()
