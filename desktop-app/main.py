import datetime
import streamlit as st
import pandas as pd
from work_repo import PinotWorkRepo
import altair as alt
from pinot_conn import conn

def pretty_print_work_done(work_done_since_start_time):
    if work_done_since_start_time > 3600:
        return f"{work_done_since_start_time // 3600}h {work_done_since_start_time % 3600 // 60}m"
    return f"{work_done_since_start_time // 60}m"

def render_pie_chart(st, work_done_since_start_time_by_app):
    source = pd.DataFrame({"values": [w[0] for w in work_done_since_start_time_by_app], "app": [w[1] for w in work_done_since_start_time_by_app]})
    base = alt.Chart(source).encode(
        alt.Theta("values:Q").stack(True),
        alt.Radius("values"),
        color="app:N",
    )
    c1 = base.mark_arc(innerRadius=20, stroke="#fff")
    c2 = base.mark_text(radiusOffset=10).encode(text="values:Q")
    chart = c1 + c2
    st.altair_chart(chart)

def to_app_level_metrics_page_link(app, epoch_time):
    return f"[{app}](http://localhost:8501/app_level_metrics_page?app={app}&epoch_time={epoch_time})"

work_repo = PinotWorkRepo(conn)

st.title("Your work at a glance")
d = st.date_input("Since", datetime.date.today())
t = st.time_input("At", datetime.time(0, 0))
epoch_time = int(datetime.datetime.combine(d, t).timestamp() * 1000)
work_done_since_start_time_by_app = work_repo.get_work_done_since_start_time_in_secs_by_application(epoch_time)
work_done_since_start_time_by_app = list(filter(lambda w: w[0] > 60, work_done_since_start_time_by_app))
print("Work done since", t, "is", work_done_since_start_time_by_app)

df = pd.DataFrame(
    {
        "Work done": [pretty_print_work_done(w[0]) for w in work_done_since_start_time_by_app],
        "App": [to_app_level_metrics_page_link(w[1], epoch_time) for w in work_done_since_start_time_by_app]
    }
)
st.table(df)
render_pie_chart(st, work_done_since_start_time_by_app)