from work_grouper import ArcProjectNameApplicationWorkGrouper

def test_arc_project_name_application_work_grouper():
    arc_project_name_application_work_grouper = ArcProjectNameApplicationWorkGrouper()
    work = [
        [100, "Arc", "2025-01-01 00:00:00"],
        [200, "(1) Arc", "2025-01-01 00:00:00"],
        [300, "(1) (2) Arc", "2025-01-01 00:00:00"],
        [400, "(1)"]
    ]
    expected_regrouped_work = [
        [100, "Arc"],
        [200, "Arc"],
        [300, "(2) Arc"],
        [400, "(1)"]
    ]
    assert expected_regrouped_work == arc_project_name_application_work_grouper.regroup_work_by_tab(work)

