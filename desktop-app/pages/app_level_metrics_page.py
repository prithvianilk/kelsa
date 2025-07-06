import streamlit as st
import pandas as pd
from work_repo import PinotWorkRepo
from pinot_conn import conn

# TODO: move to utils
def pretty_print_work_done(work_done_since_start_time):
    if work_done_since_start_time > 3600:
        return f"{work_done_since_start_time // 3600}h {work_done_since_start_time % 3600 // 60}m"
    return f"{work_done_since_start_time // 60}m"


work_repo = PinotWorkRepo(conn)

app = st.query_params['app']
epoch_time = int(st.query_params['epoch_time'])
st.title(app)

work_done_since_start_time_by_tab = work_repo.get_work_done_since_start_time_in_secs_where_app_is_by_tab(epoch_time, app)
work_done_since_start_time_by_tab = list(filter(lambda w: w[0] > 60, work_done_since_start_time_by_tab))

df = pd.DataFrame(
    {
        "Work done": [pretty_print_work_done(w[0]) for w in work_done_since_start_time_by_tab],
        "Tab": [w[1] for w in work_done_since_start_time_by_tab]
    }
)
st.table(df)