from __future__ import annotations

from pyflink.datastream import DataStream
from flink.data_stream_factory import DataStreamFactory
from work import Work
import threading

class ReportGenerationWorker:
    _ds: DataStream[str]

    def __init__(self, data_stream_factory: DataStreamFactory):
        self._ds, self._env = data_stream_factory.get_data_stream()

        self._ds \
            .map(lambda event: Work.model_validate_json(event)) \
            .map(lambda work: (work.application, 1)) \
            .key_by(lambda app: app[0]) \
            .reduce(lambda a, b: (a[0], a[1] + b[1])) \
            .print()

        threading.Thread(target=self._env.execute, daemon=True)
