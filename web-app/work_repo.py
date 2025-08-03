from abc import abstractmethod
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.logger import Logger


class WorkRepo:
    def __init__(self, username: str):
        self.username = username

    @abstractmethod
    def get_work_done_since_start_time_by_application(self, start_time: int):
        pass

    @abstractmethod
    def get_work_done_since_start_time_and_activity_is_by_application(
        self, start_time: int, active: bool
    ):
        pass

    @abstractmethod
    def get_work_done_since_start_time_and_app_is_by_tab(self, start_time: int, app: str):
        pass

    @abstractmethod
    def get_work_done_since_start_time_and_app_is_and_activity_is_by_tab(
        self, start_time: int, app: str, active: bool
    ):
        pass

    @abstractmethod
    def get_work_done_since_start_time_and_app_is_by_tab_and_date_hour(
        self, start_time: int, app: str
    ):
        pass

    @abstractmethod
    def get_work_done_since_start_time_and_app_is_and_activity_is_by_tab_and_date_hour(
        self, start_time: int, app: str, active: bool
    ):
        pass

    @abstractmethod
    def get_work_done_since_start_time_by_app_and_date_hour(self, start_time: int):
        pass

    @abstractmethod
    def get_work_done_since_start_time_and_activity_is_by_app_and_date_hour(
        self, start_time: int, active: bool
    ):
        pass


class PinotWorkRepo(WorkRepo):
    def __init__(self, conn, logger: Logger, username: str):
        super().__init__(username)
        self.conn = conn
        self.logger = logger

    def get_work_done_since_start_time_by_application(self, start_time: int):
        query = f"""
            select count (1) work_done_in_seconds, application from work
            where done_at >= {start_time} and username = '{self.username}'
            group by 2
            order by 1 desc
            limit 1000;
        """
        curs = self.conn.cursor()
        curs.execute(query)
        result = curs.fetchall()
        self.logger.debug(f"Ran query: {query}\nResult: {result}")
        return result

    def get_work_done_since_start_time_and_activity_is_by_application(
        self, start_time: int, active: bool
    ):
        query = f"""
            select count (1) work_done_in_seconds, application from work
            where done_at >= {start_time} and active = {active} and username = '{self.username}'
            group by 2
            order by 1 desc
            limit 1000;
        """
        curs = self.conn.cursor()
        curs.execute(query)
        result = curs.fetchall()
        self.logger.debug(f"Ran query: {query}\nResult: {result}")
        return result

    def get_work_done_since_start_time_and_app_is_by_tab(self, start_time: int, app: str):
        query = f"""
            select count (1) work_done_in_seconds, tab from work
            where done_at >= {start_time} and application = '{app}' and username = '{self.username}'
            group by 2
            order by 1 desc
            limit 1000;
        """
        curs = self.conn.cursor()
        curs.execute(query)
        result = curs.fetchall()
        self.logger.debug(f"Ran query: {query}\nResult: {result}")
        return result

    def get_work_done_since_start_time_and_app_is_and_activity_is_by_tab(
        self, start_time: int, app: str, active: bool
    ):
        query = f"""
            select count (1) work_done_in_seconds, tab from work
            where done_at >= {start_time} and application = '{app}' and active = {active} and username = '{self.username}'
            group by 2
            order by 1 desc
            limit 1000;
        """
        curs = self.conn.cursor()
        curs.execute(query)
        result = curs.fetchall()
        self.logger.debug(f"Ran query: {query}\nResult: {result}")
        return result

    def get_work_done_since_start_time_and_app_is_by_tab_and_date_hour(
        self, start_time: int, app: str
    ):
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
            where done_at >= {start_time} and application = '{app}' and username = '{self.username}'
            group by 2, 3
            order by 3 desc,
                1 desc
            limit 1000;
        """
        curs = self.conn.cursor()
        curs.execute(query)
        result = curs.fetchall()
        self.logger.debug(f"Ran query: {query}\nResult: {result}")
        return result

    def get_work_done_since_start_time_and_app_is_and_activity_is_by_tab_and_date_hour(
        self, start_time: int, app: str, active: bool
    ):
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
            where done_at >= {start_time} and application = '{app}' and active = {active} and username = '{self.username}'
            group by 2, 3
            order by 3 desc,
                1 desc
            limit 1000;
        """
        curs = self.conn.cursor()
        curs.execute(query)
        return curs.fetchall()

    def get_work_done_since_start_time_by_app_and_date_hour(self, start_time: int):
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
            where done_at >= {start_time} and username = '{self.username}'
            group by 2, 3
            order by 3 desc,
                1 desc
            limit 1000;
        """
        curs = self.conn.cursor()
        curs.execute(query)
        result = curs.fetchall()
        self.logger.debug(f"Ran query: {query}\nResult: {result}")
        return result

    def get_work_done_since_start_time_and_activity_is_by_app_and_date_hour(
        self, start_time: int, active: bool
    ):
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
            where done_at >= {start_time} and active = {active} and username = '{self.username}'
            group by 2, 3
            order by 3 desc,
                1 desc
            limit 1000;
        """
        curs = self.conn.cursor()
        curs.execute(query)
        result = curs.fetchall()
        self.logger.debug(f"Ran query: {query}\nResult: {result}")
        return result
