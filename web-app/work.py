from pydantic import BaseModel

class Work(BaseModel):
    application: str
    tab: str
    active: bool
    done_at: int
    username: str