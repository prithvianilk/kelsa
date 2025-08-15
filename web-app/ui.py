import streamlit as st
from time_util import is_less_than_an_hour, is_more_than_a_day, is_more_than_an_hour, seconds_to_days, seconds_to_hours, seconds_to_minutes, SECONDS_IN_A_DAY, SECONDS_IN_AN_HOUR

def pretty_print_work_done(work_done_since_start_time_in_secs):
    if is_more_than_a_day(work_done_since_start_time_in_secs):
        return f"{seconds_to_days(work_done_since_start_time_in_secs)}d {seconds_to_hours(work_done_since_start_time_in_secs % SECONDS_IN_A_DAY)}h"
    elif is_more_than_an_hour(work_done_since_start_time_in_secs):
        return f"{seconds_to_hours(work_done_since_start_time_in_secs)}h {seconds_to_minutes(work_done_since_start_time_in_secs % SECONDS_IN_AN_HOUR)}m"
    return f"{seconds_to_minutes(work_done_since_start_time_in_secs)}m"


def to_app_metrics_page_link(base_url, app, epoch_time):
    return f"[{app}]({base_url}/by_app?app={app}&epoch_time={epoch_time})"


def render_toggle_active_work():
    return st.toggle("Show only active work")


def render_total_time_spent(total_time_spent_in_seconds):
    if is_less_than_an_hour(total_time_spent_in_seconds):
        st.write("Total time spent: ", seconds_to_minutes(total_time_spent_in_seconds), "minutes")
    else:
        st.write("Total time spent: ", seconds_to_hours(total_time_spent_in_seconds), "hours")