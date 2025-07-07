from abc import abstractmethod

class ApplicationWorkGrouper:
    def __init__(self):
        pass

    @abstractmethod
    def regroup_work_by_project(self, work):
        pass

class NoOpApplicationWorkGrouper(ApplicationWorkGrouper):
    def regroup_work_by_project(self, work):
        return work

class CursorProjectNameApplicationWorkGrouper(ApplicationWorkGrouper):
    def regroup_work_by_project(self, work):
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

def get_work_grouper(application_name):
    if application_name == "Cursor":
        return CursorProjectNameApplicationWorkGrouper()
    return NoOpApplicationWorkGrouper()