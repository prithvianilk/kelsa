from typing import List
from dtos.main_page import MainPageData, WorkByApp, WorkByAppAndTime
from work_repo import WorkRepo
from common.logger import Logger

class MainPageService:
    def __init__(self, logger: Logger, work_repo: WorkRepo):
        self.logger = logger
        self.work_repo = work_repo

    def get_total_time_spent_seconds(self, work_data: List[tuple]) -> int:
        return sum(w[0] for w in work_data)

    def filter_minimum_duration(self, work_data: List[tuple], min_seconds: int = 60) -> List[tuple]:
        return list(filter(lambda w: w[0] > min_seconds, work_data))

    def get_work_done_since_start_time_by_app(self, epoch_time: int, only_active_work: bool) -> List[WorkByApp]:
        if only_active_work:
            work_data = self.work_repo.get_work_done_since_start_time_and_activity_is_by_application(
                epoch_time, True
            )
        else:
            work_data = self.work_repo.get_work_done_since_start_time_by_application(epoch_time)

        filtered_data = self.filter_minimum_duration(work_data)
        return [
            WorkByApp(seconds=w[0], application=w[1])
            for w in filtered_data
        ]

    def get_work_done_since_start_time_by_app_and_date_hour(
        self, epoch_time: int, only_active_work: bool
    ) -> List[WorkByAppAndTime]:
        if only_active_work:
            work_data = self.work_repo.get_work_done_since_start_time_and_activity_is_by_app_and_date_hour(
                epoch_time, True
            )
        else:
            work_data = self.work_repo.get_work_done_since_start_time_by_app_and_date_hour(epoch_time)

        filtered_data = self.filter_minimum_duration(work_data)
        return [
            WorkByAppAndTime(seconds=w[0], application=w[1], done_at=w[2])
            for w in filtered_data
        ]

    def get_main_page_data(self, epoch_time: int, only_active_work: bool = False) -> MainPageData:
        work_by_app = self.get_work_done_since_start_time_by_app(epoch_time, only_active_work)
        work_by_app_and_time = self.get_work_done_since_start_time_by_app_and_date_hour(
            epoch_time, only_active_work
        )

        total_seconds = sum(w.seconds for w in work_by_app)

        return MainPageData(
            total_time_spent_seconds=total_seconds,
            work_by_app=work_by_app,
            work_by_app_and_time=work_by_app_and_time
        )
