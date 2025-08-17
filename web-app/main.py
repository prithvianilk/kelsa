import datetime
import os
import sys

import altair as alt
from pages.page_state import PageState
import pandas as pd
from pinot_conn import conn
import streamlit as st
from ui import pretty_print_work_done, render_toggle_active_work, render_total_time_spent, to_app_metrics_page_link
from work_repo import PinotWorkRepo, WorkRepo
from time_util import seconds_to_minutes
from common.auth import decode_auth_header
import pytz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.logger import LogLevel, get_customised_logger, Logger

debug_logger = get_customised_logger(LogLevel.DEBUG)
info_logger = get_customised_logger(LogLevel.INFO)

class LandingPage(PageState):
    def __init__(self, logger: Logger, work_repo: WorkRepo):
        self.logger = logger
        self.work_repo = work_repo

    def render_pie_chart(self, work_done_since_start_time_by_app):
        source = pd.DataFrame(
            {
                "values": [seconds_to_minutes(w[0]) for w in work_done_since_start_time_by_app],
                "app": [w[1] for w in work_done_since_start_time_by_app],
            }
        )
        chart = (
            alt.Chart(source)
            .mark_arc(innerRadius=50)
            .encode(
                theta="values",
                color="app:N",
            )
        )
        st.altair_chart(chart)

    def render_bar_chart(self, work_done_since_start_time_by_app_and_date_hour):
        work_done_since_start_time_by_app_and_date_hour = list(
            filter(lambda w: w[0] > 60, work_done_since_start_time_by_app_and_date_hour)
        )
        source = pd.DataFrame(
            {
                "values": [seconds_to_minutes(w[0]) for w in work_done_since_start_time_by_app_and_date_hour],
                "app": [w[1] for w in work_done_since_start_time_by_app_and_date_hour],
                "done_at": [
                    pd.to_datetime(w[2]) for w in work_done_since_start_time_by_app_and_date_hour
                ],
            }
        )
        chart = (
            alt.Chart(source)
            .mark_line()
            .encode(
                x="done_at:T",
                y="values:Q",
                color="app:N",
            )
        )
        st.altair_chart(chart)

    def render_area_chart(self, work_done_since_start_time_by_app_and_date_hour):
        work_done_since_start_time_by_app_and_date_hour = list(
            filter(lambda w: w[0] > 60, work_done_since_start_time_by_app_and_date_hour)
        )
        source = pd.DataFrame(
            {
                "values": [seconds_to_minutes(w[0]) for w in work_done_since_start_time_by_app_and_date_hour],
                "app": [w[1] for w in work_done_since_start_time_by_app_and_date_hour],
                "done_at": [
                    pd.to_datetime(w[2]) for w in work_done_since_start_time_by_app_and_date_hour
                ],
            }
        )
        chart = (
            alt.Chart(source)
            .mark_area(opacity=0.3)
            .encode(x="done_at:T", y=alt.Y("values:Q").stack(None), color="app:N")
        )
        st.altair_chart(chart)

    def get_work_done_since_start_time_by_app(self, epoch_time: int, only_active_work: bool):
        if only_active_work:
            return self.work_repo.get_work_done_since_start_time_and_activity_is_by_application(
                epoch_time, True
            )
        else:
            return self.work_repo.get_work_done_since_start_time_by_application(epoch_time)

    def get_work_done_since_start_time_by_app_and_date_hour(
        self, epoch_time: int, only_active_work: bool
    ):
        if only_active_work:
            return (
                self.work_repo.get_work_done_since_start_time_and_activity_is_by_app_and_date_hour(
                    epoch_time, True
                )
            )
        else:
            return self.work_repo.get_work_done_since_start_time_by_app_and_date_hour(epoch_time)

    def render(self):
        st.title("Your work at a glance")
        d = st.date_input("Since", datetime.datetime.now(pytz.timezone("Asia/Kolkata")).date())
        t = st.time_input("At", datetime.time(0, 0, tzinfo=pytz.timezone("Asia/Kolkata")))
        self.logger.debug(f"Date: {d}")
        self.logger.debug(f"Time: {t}")

        self.logger.debug(f"Datetime: {datetime.datetime.combine(d, t)}")
        self.logger.debug(f"Datetime (millis): {int(datetime.datetime.combine(d, t).timestamp() * 1000)}")
        self.logger.debug(f"Datetime: {datetime.datetime.combine(d, t, tzinfo=None)}")
        self.logger.debug(f"Datetime (millis): {int(datetime.datetime.combine(d, t, tzinfo=None).timestamp() * 1000)}")
        self.logger.debug(f"Datetime: {datetime.datetime.combine(d, t, tzinfo=pytz.timezone('UTC'))}")
        self.logger.debug(f"Datetime (millis): {int(datetime.datetime.combine(d, t, tzinfo=pytz.timezone('UTC')).timestamp() * 1000)}")
        ist_datetime = pytz.timezone('Asia/Kolkata').localize(datetime.datetime.combine(d, t, tzinfo=None))
        self.logger.debug(f"Datetime: {ist_datetime}")
        self.logger.debug(f"Datetime (millis): {int(ist_datetime.timestamp() * 1000)}")

        epoch_time = int(ist_datetime.timestamp() * 1000)
        self.logger.debug(f"Epoch time: {epoch_time}")

        render_only_active_work = render_toggle_active_work()

        work_done_since_start_time_by_app = self.get_work_done_since_start_time_by_app(
            epoch_time, render_only_active_work
        )

        render_total_time_spent(sum([w[0] for w in work_done_since_start_time_by_app]))
        
        work_done_since_start_time_by_app = list(
            filter(lambda w: w[0] > 60, work_done_since_start_time_by_app)
        )

        df = pd.DataFrame(
            {
                "Work done": [
                    pretty_print_work_done(w[0]) for w in work_done_since_start_time_by_app
                ],
                "App": [
                    to_app_metrics_page_link(st.context.url, w[1], epoch_time)
                    for w in work_done_since_start_time_by_app
                ],
            }
        )
        st.table(df)
        self.render_pie_chart(work_done_since_start_time_by_app)

        work_done_since_start_time_by_app_and_date_hour = (
            self.get_work_done_since_start_time_by_app_and_date_hour(
                epoch_time, render_only_active_work
            )
        )
        self.render_area_chart(work_done_since_start_time_by_app_and_date_hour)

username = decode_auth_header(st.context.headers.get("authorization"))[0]
work_repo = PinotWorkRepo(conn, info_logger, username)
state = LandingPage(debug_logger, work_repo)
state.render()
