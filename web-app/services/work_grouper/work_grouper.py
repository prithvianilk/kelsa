from abc import abstractmethod
from .tab_cleaner import get_tab_cleaner

class ApplicationWorkGrouper:
    def __init__(self):
        pass

    @abstractmethod
    def group_key(self):
        pass

    @abstractmethod
    def clean_tab(self, tab):
        pass

    def regroup_work_by_tab(self, work, limit: int = 1000):
        work = [[w[0], self.clean_tab(w[1])] for w in work]
        work_by_group_key = {}
        for w in work:
            work_done_in_secs = w[0]
            group_key = w[1]
            if group_key not in work_by_group_key:
                work_by_group_key[group_key] = 0
            work_by_group_key[group_key] += work_done_in_secs
        result = [[work_by_group_key[group_key], group_key] for group_key in work_by_group_key]
        sorted_result = self.sort_by_work_done_in_secs(result)
        return sorted_result[:limit]

    def sort_by_work_done_in_secs(self, work):
        return sorted(work, key=lambda x: x[0], reverse=True)

    def regroup_work_by_tab_and_date_hour(self, work, limit: int = 1000):
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
        sorted_result = self.sort_by_work_done_in_secs(result)
        return sorted_result[:limit]

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
        return get_tab_cleaner(tab).clean_tab(tab)

class IdeaProjectNameApplicationWorkGrouper(ApplicationWorkGrouper):
    def group_key(self):
        return "project"

    def clean_tab(self, tab):
        items = tab.split(" – ")
        if len(items) == 2:
            return items[0]
        return tab

def get_work_grouper(application_name) -> ApplicationWorkGrouper:
    if application_name == "Cursor":
        return CursorProjectNameApplicationWorkGrouper()
    if application_name == "Slack":
        return SlackTabApplicationWorkGrouper()
    if application_name == "Arc":
        return ArcProjectNameApplicationWorkGrouper()
    if application_name == "idea":
        return IdeaProjectNameApplicationWorkGrouper()
    return NoOpApplicationWorkGrouper()
