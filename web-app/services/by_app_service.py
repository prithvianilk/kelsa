from typing import List
from dtos.by_app import ByAppData, WorkByGroup, WorkByGroupAndTime
from work_repo import WorkRepo
from common.logger import Logger
from services.work_grouper.work_grouper import get_work_grouper


class ByAppService:
    def __init__(self, logger: Logger, work_repo: WorkRepo):
        self.logger = logger
        self.work_repo = work_repo

    def filter_minimum_duration(self, work_data: List[tuple], min_seconds: int = 60) -> List[tuple]:
        return list(filter(lambda w: w[0] > min_seconds, work_data))

    def get_work_done_since_start_time_by_tab(
        self, since_time: int, till_time: int, app: str, only_active_work: bool
    ):
        if only_active_work:
            return self.work_repo.get_work_done_since_start_time_and_app_is_and_activity_is_by_tab(
                since_time, till_time, app, True
            )
        else:
            return self.work_repo.get_work_done_since_start_time_and_app_is_by_tab(since_time, till_time, app)

    def get_work_done_since_start_time_by_tab_and_date_hour(
        self, since_time: int, till_time: int, app: str, only_active_work: bool
    ):
        if only_active_work:
            return self.work_repo.get_work_done_since_start_time_and_app_is_and_activity_is_by_tab_and_date_hour(
                since_time, till_time, app, True
            )
        else:
            return self.work_repo.get_work_done_since_start_time_and_app_is_by_tab_and_date_hour(
                since_time, till_time, app
            )

    def get_by_app_data(self, since_time: int, till_time: int, app: str, only_active_work: bool = False) -> ByAppData:
        work_done_since_start_time_by_tab = self.get_work_done_since_start_time_by_tab(
            since_time, till_time, app, only_active_work
        )

        work_done_since_start_time_by_tab_and_date_hour = self.get_work_done_since_start_time_by_tab_and_date_hour(
            since_time, till_time, app, only_active_work
        )

        app_work_grouper = get_work_grouper(app)
        
        work_done_since_start_time_by_group = app_work_grouper.regroup_work_by_tab(
            work_done_since_start_time_by_tab,
            limit=20
        )
        work_done_since_start_time_by_group = self.filter_minimum_duration(work_done_since_start_time_by_group)

        work_done_since_start_time_by_group_and_date_hour = app_work_grouper.regroup_work_by_tab_and_date_hour(
            work_done_since_start_time_by_tab_and_date_hour, 
            limit=20
        )
        work_done_since_start_time_by_group_and_date_hour = self.filter_minimum_duration(work_done_since_start_time_by_group_and_date_hour)

        total_seconds = sum(w[0] for w in work_done_since_start_time_by_group)

        work_by_group = [
            WorkByGroup(seconds=w[0], group=w[1])
            for w in work_done_since_start_time_by_group
        ]

        work_by_group_and_time = [
            WorkByGroupAndTime(seconds=w[0], group=w[1], done_at=w[2])
            for w in work_done_since_start_time_by_group_and_date_hour
        ]

        return ByAppData(
            total_time_spent_seconds=total_seconds,
            work_by_group=work_by_group,
            work_by_group_and_time=work_by_group_and_time,
            app_name=app,
            group_key=app_work_grouper.group_key()
        )
