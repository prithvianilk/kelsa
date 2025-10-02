from typing import List
from pydantic import BaseModel


class WorkByGroup(BaseModel):
    seconds: int
    group: str


class WorkByGroupAndTime(BaseModel):
    seconds: int
    group: str
    done_at: str


class ByAppData(BaseModel):
    total_time_spent_seconds: int
    work_by_group: List[WorkByGroup]
    work_by_group_and_time: List[WorkByGroupAndTime]
    app_name: str
    group_key: str
