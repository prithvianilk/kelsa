from abc import abstractmethod
import re


class ApplicationWorkGrouper:
    def __init__(self):
        pass

    @abstractmethod
    def group_key(self):
        pass

    @abstractmethod
    def clean_tab(self, tab):
        pass

    def regroup_work_by_tab(self, work):
        work = [[w[0], self.clean_tab(w[1]), w[2]] for w in work]
        work_by_group_key = {}
        for w in work:
            work_done_in_secs = w[0]
            group_key = w[1]
            if group_key not in work_by_group_key:
                work_by_group_key[group_key] = 0
            work_by_group_key[group_key] += work_done_in_secs
        result = [[work_by_group_key[group_key], group_key] for group_key in work_by_group_key]
        return self.sort_by_work_done_in_secs(result)

    def sort_by_work_done_in_secs(self, work):
        return sorted(work, key=lambda x: x[0], reverse=True)

    def regroup_work_by_tab_and_date_hour(self, work):
        work = [[w[0], self.clean_tab(w[1]), w[2]] for w in work]
        work_by_group_key_and_date_hour = {}
        for w in work:
            work_done_in_secs = w[0]
            group_key = w[1]
            date_hour = w[2]
            if (group_key, date_hour) not in work_by_group_key_and_date_hour:
                work_by_group_key_and_date_hour[(group_key, date_hour)] = 0
            work_by_group_key_and_date_hour[(group_key, date_hour)] += work_done_in_secs
        result = [[work_by_group_key_and_date_hour[(group_key, date_hour)], group_key, date_hour] for group_key, date_hour in work_by_group_key_and_date_hour]
        return self.sort_by_work_done_in_secs(result)

class NoOpApplicationWorkGrouper(ApplicationWorkGrouper):
    def group_key(self):
        return "tab"

    def clean_tab(self, tab):
        return tab

class CursorProjectNameApplicationWorkGrouper(ApplicationWorkGrouper):
    def group_key(self):
        return "project"

    def clean_tab(self, tab):
        items = tab.split(" — ")
        if len(items) == 2:
            return items[1]
        return tab

class SlackTabApplicationWorkGrouper(ApplicationWorkGrouper):
    def group_key(self):
        return "tab"

    def clean_tab(self, tab):
        return tab.split(" - ")[0]

class ArcProjectNameApplicationWorkGrouper(ApplicationWorkGrouper):
    def group_key(self):
        return "tab"

    def clean_tab(self, tab):
        if "Confluence" in tab:
            return self.clean_confluence_tab_name(tab)

        if tab.endswith(" | Datadog"):
            return "Datadog"

        if tab.endswith("- Databricks"):
            return "Databricks"

        if tab.endswith(" - Jenkins"):
            return "Jenkins"

        return self.remove_youtube_notification_count(tab)

    def remove_youtube_notification_count(self, tab):
        cleaned_tab = re.sub(r"\(([0-9]+)\) ", "", tab, count=1)
        if len(cleaned_tab.replace(" ", "")) == 0:
            return tab
        return cleaned_tab

    def clean_confluence_tab_name(self, tab):
        tab = tab.replace("- Confluence", "")
        tab = tab.replace("Add Page - ", "")
        tab = tab.replace("Edit - ", "")
        splits = tab.split(" - ")
        return " — ".join(splits[:-1])

class IdeaProjectNameApplicationWorkGrouper(ApplicationWorkGrouper):
    def group_key(self):
        return "project"

    def clean_tab(self, tab):
        items = tab.split(" – ")
        if len(items) == 2:
            return items[0]
        return tab

def get_work_grouper(application_name):
    if application_name == "Cursor":
        return CursorProjectNameApplicationWorkGrouper()
    if application_name == "Slack":
        return SlackTabApplicationWorkGrouper()
    if application_name == "Arc":
        return ArcProjectNameApplicationWorkGrouper()
    if application_name == "idea":
        return IdeaProjectNameApplicationWorkGrouper()
    return NoOpApplicationWorkGrouper()
