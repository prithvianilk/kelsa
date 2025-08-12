import streamlit as st
from time_util import seconds_to_minutes

def pretty_print_work_done(work_done_since_start_time):
    if work_done_since_start_time > 3600:
        return f"{work_done_since_start_time // 3600}h {work_done_since_start_time % 3600 // 60}m"
    return f"{work_done_since_start_time // 60}m"


def to_app_metrics_page_link(base_url, app, epoch_time):
    return f"[{app}]({base_url}/by_app?app={app}&epoch_time={epoch_time})"


def render_toggle_active_work():
    return st.toggle("Show only active work")


def render_total_time_spent(total_time_spent):
    st.write("Total time spent: ", seconds_to_minutes(total_time_spent), "minutes")