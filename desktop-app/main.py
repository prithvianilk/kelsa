import datetime
import streamlit as st
import pandas as pd
import pinotdb
from work_repo import PinotWorkRepo

def pretty_print_work_done(work_done_since_start_time):
    if work_done_since_start_time[0] > 3600:
        return f"{work_done_since_start_time[0] // 3600}h {work_done_since_start_time[0] % 3600 // 60}m"
    elif work_done_since_start_time[0] > 60:
        return f"{work_done_since_start_time[0] // 60}m {work_done_since_start_time[0] % 60}s"
    else:
        return f"{work_done_since_start_time[0]}s"

conn = pinotdb.connect(
    host="localhost",
    port=8099,
    path="/query/sql"
)
work_repo = PinotWorkRepo(conn)

st.title("Your work at a glance")
d = st.date_input("Since", datetime.date.today())
t = st.time_input("At", datetime.time(0, 0))
epoch_time = int(datetime.datetime.combine(d, t).timestamp() * 1000)
work_done_since_start_time = work_repo.get_work_done_since_start_time_in_secs_by_application_and_tab(epoch_time)
print("Work done since", t, "is", work_done_since_start_time)

df = pd.DataFrame(
    {
        "Work done": [pretty_print_work_done(w) for w in work_done_since_start_time],
        "App": [w[1] for w in work_done_since_start_time],
        "Tab": [w[2] for w in work_done_since_start_time]
    }
)
st.table(df)
