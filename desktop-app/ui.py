def pretty_print_work_done(work_done_since_start_time):
    if work_done_since_start_time > 3600:
        return f"{work_done_since_start_time // 3600}h {work_done_since_start_time % 3600 // 60}m"
    return f"{work_done_since_start_time // 60}m"

def to_app_metrics_page_link(app, epoch_time):
    return f"[{app}](http://localhost:8501/app?app={app}&epoch_time={epoch_time})"