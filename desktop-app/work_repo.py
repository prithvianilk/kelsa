from abc import abstractmethod

class WorkRepo:
    def __init__(self, conn):
        self.conn = conn

    @abstractmethod
    def get_work_done_since_start_time_in_secs_by_application_and_tab(self, start_time: int):
        pass

class PinotWorkRepo(WorkRepo):
    def get_work_done_since_start_time_in_secs_by_application_and_tab(self, start_time: int):
        query = f"""
            select count (1) work_done_in_seconds, application, tab from work
            where done_at >= {start_time}
            group by 2, 3
            order by 1 desc
            limit 1000;
        """
        curs = self.conn.cursor()
        curs.execute(query)
        return curs.fetchall()
