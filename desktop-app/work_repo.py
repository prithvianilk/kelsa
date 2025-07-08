from abc import abstractmethod

class WorkRepo:
    def __init__(self, conn):
        self.conn = conn

    @abstractmethod
    def get_work_done_since_start_time_in_secs_by_application(self, start_time: int, active: bool):
        pass

    @abstractmethod
    def get_work_done_since_start_time_in_secs_where_app_is_by_tab(self, start_time: int, app: str, active: bool):
        pass

    @abstractmethod
    def get_work_done_since_start_time_in_secs_where_app_is_by_tab_and_date_hour(self, start_time: int, app: str, active: bool):
        pass

    @abstractmethod
    def get_work_done_since_start_time_in_secs_by_app_and_date_hour(self, start_time: int, active: bool):
        pass

class PinotWorkRepo(WorkRepo):
    def get_work_done_since_start_time_in_secs_by_application(self, start_time: int, active: bool):
        query = f"""
            select count (1) work_done_in_seconds, application from work
            where done_at >= {start_time} and active = {active}
            group by 2
            order by 1 desc
            limit 1000;
        """
        curs = self.conn.cursor()
        curs.execute(query)
        return curs.fetchall()
    
    def get_work_done_since_start_time_in_secs_where_app_is_by_tab(self, start_time: int, app: str, active: bool):
        query = f"""
            select count (1) work_done_in_seconds, tab from work
            where done_at >= {start_time} and application = '{app}' and active = {active}
            group by 2
            order by 1 desc
            limit 1000;
        """
        curs = self.conn.cursor()
        curs.execute(query)
        return curs.fetchall()

    def get_work_done_since_start_time_in_secs_where_app_is_by_tab_and_date_hour(self, start_time: int, app: str, active: bool):
        query = f"""
            select count(1) work_done_in_seconds,
                tab,
                DATETIMECONVERT(
                    date_trunc('hour', done_at),
                    '1:MILLISECONDS:EPOCH',
                    '1:MILLISECONDS:SIMPLE_DATE_FORMAT:yyyy-MM-dd HH:mm:ss',
                    '1:MILLISECONDS'
                ) done_at
            from work
            where done_at >= {start_time} and application = '{app}' and active = {active}
            group by 2, 3
            order by 3 desc,
                1 desc
            limit 1000;
        """
        curs = self.conn.cursor()
        curs.execute(query)
        return curs.fetchall()
    
    def get_work_done_since_start_time_in_secs_by_app_and_date_hour(self, start_time: int, active: bool):
        query = f"""
            select count(1) work_done_in_seconds,
                application,
                DATETIMECONVERT(
                    date_trunc('hour', done_at),
                    '1:MILLISECONDS:EPOCH',
                    '1:MILLISECONDS:SIMPLE_DATE_FORMAT:yyyy-MM-dd HH:mm:ss',
                    '1:MILLISECONDS'
                ) done_at
            from work
            where done_at >= {start_time} and active = {active}
            group by 2, 3
            order by 3 desc,
                1 desc
            limit 1000;
        """
        curs = self.conn.cursor()
        curs.execute(query)
        return curs.fetchall()