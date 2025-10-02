from typing import List
from pydantic import BaseModel

class WorkByApp(BaseModel):
    seconds: int
    application: str

class WorkByAppAndTime(BaseModel):
    seconds: int
    application: str
    done_at: str

class MainPageData(BaseModel):
    total_time_spent_seconds: int
    work_by_app: List[WorkByApp]
    work_by_app_and_time: List[WorkByAppAndTime]
