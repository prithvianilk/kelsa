import streamlit as st
import pandas as pd
from work_repo import PinotWorkRepo
from pinot_conn import conn
import altair as alt
from ui import pretty_print_work_done

def render_pie_chart(st, work_done_since_start_time_by_tab):
    source = pd.DataFrame({
        "values": [w[0] // 60 for w in work_done_since_start_time_by_tab], 
        "tab": [w[1] for w in work_done_since_start_time_by_tab]
    })
    chart = alt.Chart(source).mark_arc(innerRadius=50).encode(
        theta="values",
        color="tab:N",
    )
    st.altair_chart(chart)

def render_area_chart(st, work_done_since_start_time_by_tab_and_date_hour):
    work_done_since_start_time_by_tab_and_date_hour = list(filter(lambda w: w[0] > 60, work_done_since_start_time_by_tab_and_date_hour))
    source = pd.DataFrame({
        "values": [w[0] // 60 for w in work_done_since_start_time_by_tab_and_date_hour], 
        "tab": [w[1] for w in work_done_since_start_time_by_tab_and_date_hour],
        "done_at": [pd.to_datetime(w[2]) for w in work_done_since_start_time_by_tab_and_date_hour]
    })
    chart = alt.Chart(source).mark_area(opacity=0.3).encode(
        x="done_at:T",
        y=alt.Y("values:Q").stack(None),
        color="tab:N"
    )
    st.altair_chart(chart)

work_repo = PinotWorkRepo(conn)

app = st.query_params['app']
epoch_time = int(st.query_params['epoch_time'])
st.title("work done in " + app + " since " + pd.to_datetime(epoch_time // 1000, unit='s').strftime("%Y-%m-%d %H:%M:%S"))

work_done_since_start_time_by_tab = work_repo.get_work_done_since_start_time_in_secs_where_app_is_by_tab(epoch_time, app)
work_done_since_start_time_by_tab = list(filter(lambda w: w[0] > 60, work_done_since_start_time_by_tab))

df = pd.DataFrame(
    {
        "Work done": [pretty_print_work_done(w[0]) for w in work_done_since_start_time_by_tab],
        "Tab": [w[1] for w in work_done_since_start_time_by_tab]
    }
)
st.table(df)
render_pie_chart(st, work_done_since_start_time_by_tab)

work_done_since_start_time_by_tab_and_date_hour = work_repo.get_work_done_since_start_time_in_secs_where_app_is_by_tab_and_date_hour(epoch_time, app)
render_area_chart(st, work_done_since_start_time_by_tab_and_date_hour)