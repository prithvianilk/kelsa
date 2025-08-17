import os
import sys

import altair as alt
from pages.page_state import PageState
import pandas as pd
from pinot_conn import conn
import streamlit as st
from ui import pretty_print_work_done, render_toggle_active_work, render_total_time_spent
from work_repo import PinotWorkRepo, WorkRepo
from time_util import epoch_time_from_utc_to_ist, seconds_to_minutes
from common.auth import decode_auth_header
from services.open_ai import get_open_ai_client
from services.work_summarisation_service import ArcWorkSummarisationService, OpenAIGpt4oMiniLlm, SummarisationService
from services.work_grouper.work_grouper import get_work_grouper


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.config import DotEnvEnvironmentVariables
from common.logger import LogLevel, get_customised_logger

info_logger = get_customised_logger(LogLevel.INFO)
debug_logger = get_customised_logger(LogLevel.DEBUG)
config = DotEnvEnvironmentVariables("config.env")


class ByAppPage(PageState):
    def __init__(self, work_repo: WorkRepo, summarisation_service: SummarisationService):
        self.work_repo = work_repo
        self.summarisation_service = summarisation_service

    def render_pie_chart(self, work_done_since_start_time_by_tab, group_key):
        source = pd.DataFrame(
            {
                "values": [seconds_to_minutes(w[0]) for w in work_done_since_start_time_by_tab],
                group_key: [w[1] for w in work_done_since_start_time_by_tab],
            }
        )
        chart = (
            alt.Chart(source)
            .mark_arc(innerRadius=50)
            .encode(
                theta="values",
                color=group_key + ":N",
            )
        )
        st.altair_chart(chart)

    def render_area_chart(self, work_done_since_start_time_by_tab_and_date_hour, group_key):
        work_done_since_start_time_by_tab_and_date_hour = list(
            filter(lambda w: w[0] > 60, work_done_since_start_time_by_tab_and_date_hour)
        )
        source = pd.DataFrame(
            {
                "values": [seconds_to_minutes(w[0]) for w in work_done_since_start_time_by_tab_and_date_hour],
                group_key: [w[1] for w in work_done_since_start_time_by_tab_and_date_hour],
                "done_at": [
                    pd.to_datetime(w[2]) for w in work_done_since_start_time_by_tab_and_date_hour
                ],
            }
        )
        chart = (
            alt.Chart(source)
            .mark_area(opacity=0.3)
            .encode(x="done_at:T", y=alt.Y("values:Q").stack(None), color=group_key + ":N")
        )
        st.altair_chart(chart)

    def get_work_done_since_start_time_by_tab(
        self, epoch_time: int, app: str, only_active_work: bool
    ):
        if only_active_work:
            return self.work_repo.get_work_done_since_start_time_and_app_is_and_activity_is_by_tab(
                epoch_time, app, True
            )
        else:
            return self.work_repo.get_work_done_since_start_time_and_app_is_by_tab(epoch_time, app)

    def get_work_done_since_start_time_by_tab_and_date_hour(
        self, epoch_time: int, app: str, only_active_work: bool
    ):
        if only_active_work:
            return self.work_repo.get_work_done_since_start_time_and_app_is_and_activity_is_by_tab_and_date_hour(
                epoch_time, app, True
            )
        else:
            return self.work_repo.get_work_done_since_start_time_and_app_is_by_tab_and_date_hour(
                epoch_time, app
            )

    def is_work_summary_enabled(self, app: str) -> bool:
        return app == "Arc"

    def render_work_summary(self, work_done_since_start_time_by_app_and_date_hour):
        if st.button("Summarise work"):
            work_summary = self.summarisation_service.summarise_work(work_done_since_start_time_by_app_and_date_hour)
            st.write(work_summary)

    def render(self):
        app = st.query_params["app"]
        epoch_time = int(st.query_params["epoch_time"])
        st.title(
            "work done in "
            + app
            + " since "
            + pd.to_datetime(epoch_time_from_utc_to_ist(epoch_time), unit="ms", utc=False).strftime("%Y-%m-%d %I:%M%p")
        )
        render_only_active_work = render_toggle_active_work()

        work_done_since_start_time_by_tab = self.get_work_done_since_start_time_by_tab(
            epoch_time, app, render_only_active_work
        )

        render_total_time_spent(sum([w[0] for w in work_done_since_start_time_by_tab]))

        app_work_grouper = get_work_grouper(app)
        work_done_since_start_time_by_group = app_work_grouper.regroup_work_by_tab(
            work_done_since_start_time_by_tab,
            limit=20
        )
        work_done_since_start_time_by_group = list(
            filter(lambda w: w[0] > 60, work_done_since_start_time_by_group)
        )

        df = pd.DataFrame(
            {
                "Work done": [
                    pretty_print_work_done(w[0]) for w in work_done_since_start_time_by_group
                ],
                app_work_grouper.group_key().title(): [
                    w[1] for w in work_done_since_start_time_by_group
                ],
            }
        )
        st.table(df)
        self.render_pie_chart(work_done_since_start_time_by_group, app_work_grouper.group_key())

        work_done_since_start_time_by_tab_and_date_hour = (
            self.get_work_done_since_start_time_by_tab_and_date_hour(
                epoch_time, app, render_only_active_work
            )
        )
        work_done_since_start_time_by_group_and_date_hour = (
            app_work_grouper.regroup_work_by_tab_and_date_hour(
                work_done_since_start_time_by_tab_and_date_hour, 
                limit=20
            )
        )
        self.render_area_chart(
            work_done_since_start_time_by_group_and_date_hour, app_work_grouper.group_key()
        )

        if self.is_work_summary_enabled(app):
            self.render_work_summary(work_done_since_start_time_by_group_and_date_hour)


username = decode_auth_header(st.context.headers.get("authorization"))[0]
work_repo = PinotWorkRepo(conn, info_logger, username)
open_ai_client = get_open_ai_client(config.get_config("OPEN_AI_API_TOKEN"))
llm = OpenAIGpt4oMiniLlm(info_logger, open_ai_client)
summarisation_service = ArcWorkSummarisationService(info_logger, llm)
state = ByAppPage(work_repo, summarisation_service)
state.render()
