import datetime
import os
import sys
import streamlit as st
import pandas as pd
from work_repo import PinotWorkRepo, WorkRepo
import altair as alt
from pinot_conn import conn
from ui import pretty_print_work_done, render_toggle_active_work, to_app_metrics_page_link
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.logger import ConsoleLogger

def render_pie_chart(st, work_done_since_start_time_by_app):
    source = pd.DataFrame({
        "values": [w[0] // 60 for w in work_done_since_start_time_by_app], 
        "app": [w[1] for w in work_done_since_start_time_by_app]
    })
    chart = alt.Chart(source).mark_arc(innerRadius=50).encode(
        theta="values",
        color="app:N",
    )
    st.altair_chart(chart)

def render_bar_chart(st, work_done_since_start_time_by_app_and_date_hour):
    work_done_since_start_time_by_app_and_date_hour = list(filter(lambda w: w[0] > 60, work_done_since_start_time_by_app_and_date_hour))
    source = pd.DataFrame({
        "values": [w[0] // 60 for w in work_done_since_start_time_by_app_and_date_hour], 
        "app": [w[1] for w in work_done_since_start_time_by_app_and_date_hour],
        "done_at": [pd.to_datetime(w[2]) for w in work_done_since_start_time_by_app_and_date_hour]
    })
    chart = alt.Chart(source).mark_line().encode(
        x='done_at:T',
        y='values:Q',
        color='app:N',
    )
    st.altair_chart(chart)

def render_area_chart(st, work_done_since_start_time_by_app_and_date_hour):
    work_done_since_start_time_by_app_and_date_hour = list(filter(lambda w: w[0] > 60, work_done_since_start_time_by_app_and_date_hour))
    source = pd.DataFrame({
        "values": [w[0] // 60 for w in work_done_since_start_time_by_app_and_date_hour], 
        "app": [w[1] for w in work_done_since_start_time_by_app_and_date_hour],
        "done_at": [pd.to_datetime(w[2]) for w in work_done_since_start_time_by_app_and_date_hour]
    })
    chart = alt.Chart(source).mark_area(opacity=0.3).encode(
        x="done_at:T",
        y=alt.Y("values:Q").stack(None),
        color="app:N"
    )
    st.altair_chart(chart)

def get_work_done_since_start_time_by_app(work_repo: WorkRepo, epoch_time: int, only_active_work: bool):
    if only_active_work:
        return work_repo.get_work_done_since_start_time_and_activity_is_by_application(epoch_time, True)
    else:
        return work_repo.get_work_done_since_start_time_by_application(epoch_time)

def get_work_done_since_start_time_by_app_and_date_hour(work_repo: WorkRepo, epoch_time: int, only_active_work: bool):
    if only_active_work:
        return work_repo.get_work_done_since_start_time_and_activity_is_by_app_and_date_hour(epoch_time, True)
    else:
        return work_repo.get_work_done_since_start_time_by_app_and_date_hour(epoch_time)

work_repo = PinotWorkRepo(conn)

st.title("Your work at a glance")
d = st.date_input("Since", datetime.date.today())
t = st.time_input("At", datetime.time(0, 0))
epoch_time = int(datetime.datetime.combine(d, t).timestamp() * 1000)

render_only_active_work = render_toggle_active_work()

work_done_since_start_time_by_app = get_work_done_since_start_time_by_app(work_repo, epoch_time, render_only_active_work)
work_done_since_start_time_by_app = list(filter(lambda w: w[0] > 60, work_done_since_start_time_by_app))

df = pd.DataFrame(
    {
        "Work done": [pretty_print_work_done(w[0]) for w in work_done_since_start_time_by_app],
        "App": [to_app_metrics_page_link(st.context.url, w[1], epoch_time) for w in work_done_since_start_time_by_app]
    }
)
st.table(df)
render_pie_chart(st, work_done_since_start_time_by_app)

work_done_since_start_time_by_app_and_date_hour = get_work_done_since_start_time_by_app_and_date_hour(work_repo, epoch_time, render_only_active_work)
render_area_chart(st, work_done_since_start_time_by_app_and_date_hour)