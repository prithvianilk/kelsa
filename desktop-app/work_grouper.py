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
            items = w[1].split(" — ")
            if len(items) == 2:
                project_name = items[1]
            else:
                project_name = w[1]

            if project_name not in work_by_project_name:
                work_by_project_name[project_name] = 0
            work_by_project_name[project_name] += w[0]
        return [[work_by_project_name[project_name], project_name] for project_name in work_by_project_name]

    def regroup_work_by_tab_and_date_hour(self, work):
        work_by_project_name_and_date_hour = {}
        for w in work:
            tab = w[1]
            items = tab.split(" — ")
            if len(items) == 2:
                project_name = items[1]
            else:
                project_name = w[1]

            if (project_name, w[2]) not in work_by_project_name_and_date_hour:
                work_by_project_name_and_date_hour[(project_name, w[2])] = 0
            work_by_project_name_and_date_hour[(project_name, w[2])] += w[0]
        return [[work_by_project_name_and_date_hour[project_name, w[2]], project_name, w[2]] for project_name, w[2] in work_by_project_name_and_date_hour]

def get_work_grouper(application_name):
    if application_name == "Cursor":
        return CursorProjectNameApplicationWorkGrouper()
    return NoOpApplicationWorkGrouper()