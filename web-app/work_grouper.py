from abc import abstractmethod
import re

class ApplicationWorkGrouper:
    def __init__(self):
        pass

    @abstractmethod
    def group_key(self):
        pass

    @abstractmethod
    def regroup_work_by_tab(self, work):
        pass

    @abstractmethod
    def regroup_work_by_tab_and_date_hour(self, work):
        pass

class NoOpApplicationWorkGrouper(ApplicationWorkGrouper):
    def group_key(self):
        return "tab"

    def regroup_work_by_tab(self, work):
        return work

    def regroup_work_by_tab_and_date_hour(self, work):
        return work

class CursorProjectNameApplicationWorkGrouper(ApplicationWorkGrouper):
    def group_key(self):
        return "project"

    def regroup_work_by_tab(self, work):
        work_by_project_name = {}
        for w in work:
            work_done_in_secs = w[0]
            project_name = self.get_project_name(w[1])
            if project_name not in work_by_project_name:
                work_by_project_name[project_name] = 0
            work_by_project_name[project_name] += work_done_in_secs
        return [[work_by_project_name[project_name], project_name] for project_name in work_by_project_name]
    
    def get_project_name(self, tab):
        items = tab.split(" — ")
        if len(items) == 2:
            return items[1]
        return tab

    def regroup_work_by_tab_and_date_hour(self, work):
        work_by_project_name_and_date_hour = {}
        for w in work:
            work_done_in_secs = w[0]
            project_name = self.get_project_name(w[1])
            date_hour = w[2]
            if (project_name, date_hour) not in work_by_project_name_and_date_hour:
                work_by_project_name_and_date_hour[(project_name, date_hour)] = 0
            work_by_project_name_and_date_hour[(project_name, date_hour)] += work_done_in_secs
        return [[work_by_project_name_and_date_hour[(project_name, date_hour)], project_name, date_hour] for project_name, date_hour in work_by_project_name_and_date_hour]

class SlackChannelApplicationWorkGrouper(ApplicationWorkGrouper):
    def group_key(self):
        return "channel"

    def get_channel_name(self, tab):
        return tab.split(" ")[0]

    def regroup_work_by_tab(self, work):
        work_by_channel_name = {}
        for w in work:
            work_done_in_secs = w[0]
            channel_name = self.get_channel_name(w[1])
            if channel_name not in work_by_channel_name:
                work_by_channel_name[channel_name] = 0
            work_by_channel_name[channel_name] += work_done_in_secs
        return [[work_by_channel_name[channel_name], channel_name] for channel_name in work_by_channel_name]

    def regroup_work_by_tab_and_date_hour(self, work):
        work_by_channel_name_and_date_hour = {}
        for w in work:
            work_done_in_secs = w[0]
            channel_name = self.get_channel_name(w[1])
            date_hour = w[2]
            if (channel_name, date_hour) not in work_by_channel_name_and_date_hour:
                work_by_channel_name_and_date_hour[(channel_name, date_hour)] = 0
            work_by_channel_name_and_date_hour[(channel_name, date_hour)] += work_done_in_secs
        return [[work_by_channel_name_and_date_hour[(channel_name, date_hour)], channel_name, date_hour] for channel_name, date_hour in work_by_channel_name_and_date_hour]

class ArcProjectNameApplicationWorkGrouper(ApplicationWorkGrouper):
    def group_key(self):
        return "tab"

    def regroup_work_by_tab(self, work):
        return [[w[0], self.clean_tab_name(w[1])] for w in work]

    def remove_youtube_notification_count(self, tab): 
        cleaned_tab = re.sub(r'\(([0-9]+)\) ', '', tab, count=1)
        if len(cleaned_tab.replace(' ', '')) == 0:
            return tab
        return cleaned_tab

    def clean_tab_name(self, tab):
        return self.remove_youtube_notification_count(tab)

    def regroup_work_by_tab_and_date_hour(self, work):
        return [[w[0], self.clean_tab_name(w[1]), w[2]] for w in work]

def get_work_grouper(application_name):
    if application_name == "Cursor":
        return CursorProjectNameApplicationWorkGrouper()
    if application_name == "Slack":
        return SlackChannelApplicationWorkGrouper()
    if application_name == "Arc":
        return ArcProjectNameApplicationWorkGrouper()
    return NoOpApplicationWorkGrouper()