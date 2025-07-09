from abc import abstractmethod

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

def get_work_grouper(application_name):
    if application_name == "Cursor":
        return CursorProjectNameApplicationWorkGrouper()
    return NoOpApplicationWorkGrouper()