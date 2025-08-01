import streamlit as st
import pandas as pd
from work_repo import PinotWorkRepo
from pinot_conn import conn
import altair as alt
from ui import pretty_print_work_done, render_toggle_active_work, get_password  
from work_grouper import get_work_grouper
from pages.page_state import PageState, LoggedOutState

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.logger import get_customised_logger, LogLevel
from common.config import DotEnvEnvironmentVariables
config = DotEnvEnvironmentVariables("config.env")
logger = get_customised_logger(LogLevel.INFO)

class LoggedInByAppPage(PageState):
    def __init__(self):
        self.work_repo = PinotWorkRepo(conn, logger)

    def render_pie_chart(self, work_done_since_start_time_by_tab, group_key):
        source = pd.DataFrame({
            "values": [w[0] // 60 for w in work_done_since_start_time_by_tab], 
            group_key: [w[1] for w in work_done_since_start_time_by_tab]
        })
        chart = alt.Chart(source).mark_arc(innerRadius=50).encode(
            theta="values",
            color=group_key + ":N",
        )
        st.altair_chart(chart)

    def render_area_chart(self, work_done_since_start_time_by_tab_and_date_hour, group_key):
        work_done_since_start_time_by_tab_and_date_hour = list(filter(lambda w: w[0] > 60, work_done_since_start_time_by_tab_and_date_hour))
        source = pd.DataFrame({
            "values": [w[0] // 60 for w in work_done_since_start_time_by_tab_and_date_hour], 
            group_key: [w[1] for w in work_done_since_start_time_by_tab_and_date_hour],
            "done_at": [pd.to_datetime(w[2]) for w in work_done_since_start_time_by_tab_and_date_hour]
        })
        chart = alt.Chart(source).mark_area(opacity=0.3).encode(
            x="done_at:T",
            y=alt.Y("values:Q").stack(None),
            color=group_key + ":N"
        )
        st.altair_chart(chart)

    def get_work_done_since_start_time_by_tab(self, epoch_time: int, app: str, only_active_work: bool):
        if only_active_work:
            return self.work_repo.get_work_done_since_start_time_and_app_is_and_activity_is_by_tab(epoch_time, app, True)
        else:
            return self.work_repo.get_work_done_since_start_time_and_app_is_by_tab(epoch_time, app)

    def get_work_done_since_start_time_by_tab_and_date_hour(self, epoch_time: int, app: str, only_active_work: bool):
        if only_active_work:
            return self.work_repo.get_work_done_since_start_time_and_app_is_and_activity_is_by_tab_and_date_hour(epoch_time, app, True)
        else:
            return self.work_repo.get_work_done_since_start_time_and_app_is_by_tab_and_date_hour(epoch_time, app)

    def render(self):
        app = st.query_params['app']
        epoch_time = int(st.query_params['epoch_time'])
        st.title("work done in " + app + " since " + pd.to_datetime(epoch_time // 1000, unit='s').strftime("%Y-%m-%d %H:%M:%S"))
        render_only_active_work = render_toggle_active_work()

        work_done_since_start_time_by_tab = self.get_work_done_since_start_time_by_tab(epoch_time, app, render_only_active_work)

        app_work_grouper = get_work_grouper(app)
        work_done_since_start_time_by_group = app_work_grouper.regroup_work_by_tab(work_done_since_start_time_by_tab)
        work_done_since_start_time_by_group = list(filter(lambda w: w[0] > 60, work_done_since_start_time_by_group))

        df = pd.DataFrame(
            {
                "Work done": [pretty_print_work_done(w[0]) for w in work_done_since_start_time_by_group],
                app_work_grouper.group_key().title(): [w[1] for w in work_done_since_start_time_by_group]
            }
        )
        st.table(df)
        self.render_pie_chart(work_done_since_start_time_by_group, app_work_grouper.group_key())

        work_done_since_start_time_by_tab_and_date_hour = self.get_work_done_since_start_time_by_tab_and_date_hour(epoch_time, app, render_only_active_work)
        work_done_since_start_time_by_group_and_date_hour = app_work_grouper.regroup_work_by_tab_and_date_hour(work_done_since_start_time_by_tab_and_date_hour)
        self.render_area_chart(work_done_since_start_time_by_group_and_date_hour, app_work_grouper.group_key())


password = get_password()
if password == config.get_config("WEB_APP_PASSWORD"):
    state = LoggedInByAppPage()
else:
    state = LoggedOutState(config.get_config("WEB_APP_URL"))

state.render()